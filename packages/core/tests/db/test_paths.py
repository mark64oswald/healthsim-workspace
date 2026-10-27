"""Tests for data location resolution and the split reference/cohorts layout."""

from pathlib import Path

import duckdb
import pytest

from healthsim.db import paths
from healthsim.db.fixtures import build_reference_fixture
from healthsim.db.paths import (
    REFERENCE_ALIAS,
    attach_reference,
    connect,
    ensure_database,
    is_valid_duckdb,
    resolve_layout,
)

LFS_POINTER = (
    "version https://git-lfs.github.com/spec/v1\n"
    "oid sha256:0000000000000000000000000000000000000000000000000000000000000000\n"
    "size 1789569024\n"
)


@pytest.fixture
def clean_env(monkeypatch, tmp_path):
    """Isolate HEALTHSIM_* variables and point the repo root at an empty dir."""
    for var in ("HEALTHSIM_DB_PATH", "HEALTHSIM_HOME", "HEALTHSIM_REFERENCE_PATH"):
        monkeypatch.delenv(var, raising=False)
    home = tmp_path / "home"
    repo = tmp_path / "repo"
    (repo / "skills").mkdir(parents=True)
    (repo / "packages").mkdir()
    monkeypatch.setenv("HEALTHSIM_HOME", str(home))
    monkeypatch.setattr(paths, "_REPO_ROOT_CANDIDATE", repo)
    return home, repo


class TestResolveLayout:
    def test_env_db_path_wins(self, clean_env, monkeypatch, tmp_path):
        home, _ = clean_env
        build_reference_fixture(home / "reference.duckdb")
        monkeypatch.setenv("HEALTHSIM_DB_PATH", str(tmp_path / "custom.duckdb"))
        layout = resolve_layout()
        assert layout.mode == "single"
        assert layout.db_path == tmp_path / "custom.duckdb"
        assert layout.reference_path is None

    def test_env_motherduck(self, clean_env, monkeypatch):
        monkeypatch.setenv("HEALTHSIM_DB_PATH", "md:healthsim_ref?motherduck_token=secret")
        layout = resolve_layout()
        assert layout.is_motherduck
        assert "secret" not in layout.describe()["db_path"]

    def test_env_db_with_reference_override(self, clean_env, monkeypatch, tmp_path):
        ref = build_reference_fixture(tmp_path / "ref.duckdb")
        monkeypatch.setenv("HEALTHSIM_DB_PATH", str(tmp_path / "c.duckdb"))
        monkeypatch.setenv("HEALTHSIM_REFERENCE_PATH", str(ref))
        layout = resolve_layout()
        assert layout.mode == "split"
        assert layout.reference_path == ref

    def test_home_reference_gives_split_layout(self, clean_env):
        home, repo = clean_env
        build_reference_fixture(home / "reference.duckdb")
        # A real repo-root database should not win over installed home data
        duckdb.connect(str(repo / "healthsim.duckdb")).close()
        layout = resolve_layout()
        assert layout.mode == "split"
        assert layout.db_path == home / "cohorts.duckdb"
        assert layout.reference_path == home / "reference.duckdb"
        assert layout.has_reference

    def test_repo_root_database_for_developers(self, clean_env):
        _, repo = clean_env
        con = duckdb.connect(str(repo / "healthsim.duckdb"))
        con.execute("CREATE TABLE t (x INT)")
        con.close()
        layout = resolve_layout()
        assert layout.mode == "single"
        assert layout.db_path == repo / "healthsim.duckdb"

    def test_lfs_pointer_is_ignored(self, clean_env):
        home, repo = clean_env
        (repo / "healthsim.duckdb").write_text(LFS_POINTER)
        layout = resolve_layout()
        assert layout.mode == "split"
        assert layout.db_path == home / "cohorts.duckdb"
        assert not layout.has_reference
        assert "setup" in layout.source

    def test_no_repo_root(self, clean_env, monkeypatch):
        home, _ = clean_env
        monkeypatch.setattr(paths, "_REPO_ROOT_CANDIDATE", None)
        layout = resolve_layout()
        assert layout.db_path == home / "cohorts.duckdb"


class TestValidity:
    def test_pointer_and_missing_are_invalid(self, tmp_path):
        pointer = tmp_path / "p.duckdb"
        pointer.write_text(LFS_POINTER)
        assert not is_valid_duckdb(pointer)
        assert not is_valid_duckdb(tmp_path / "missing.duckdb")

    def test_real_database_is_valid(self, tmp_path):
        assert is_valid_duckdb(build_reference_fixture(tmp_path / "r.duckdb"))


class TestSplitLayoutQueries:
    @pytest.fixture
    def layout(self, clean_env):
        home, _ = clean_env
        build_reference_fixture(home / "reference.duckdb")
        return resolve_layout()

    def test_schema_qualified_reference_names_resolve(self, layout):
        conn = connect(read_only=True, layout=layout)
        try:
            n = conn.execute(
                "SELECT count(*) FROM network.providers WHERE practice_state = 'CA'"
            ).fetchone()[0]
            assert n == 3
            row = conn.execute(
                "SELECT county FROM population.svi_county WHERE fips = '06073'"
            ).fetchone()
            assert row[0] == "San Diego County"
        finally:
            conn.close()

    def test_cohort_tables_created_in_main(self, layout):
        conn = connect(read_only=True, layout=layout)
        try:
            assert conn.execute("SELECT count(*) FROM cohorts").fetchone()[0] == 0
            catalog = conn.execute(
                "SELECT table_catalog FROM information_schema.tables WHERE table_name = 'patients'"
            ).fetchone()[0]
            assert catalog == "cohorts"
        finally:
            conn.close()

    def test_writes_go_to_cohorts_not_reference(self, layout):
        conn = connect(read_only=False, layout=layout)
        try:
            conn.execute("CREATE TABLE scratch (x INT)")
            conn.execute("INSERT INTO scratch VALUES (1)")
            with pytest.raises(duckdb.Error):
                conn.execute("INSERT INTO network.providers (npi) VALUES ('x')")
        finally:
            conn.close()
        ref = duckdb.connect(str(layout.reference_path), read_only=True)
        try:
            tables = {r[0] for r in ref.execute("SELECT table_name FROM duckdb_tables()").fetchall()}
            assert "scratch" not in tables
        finally:
            ref.close()

    def test_attach_is_idempotent(self, layout):
        conn = connect(read_only=True, layout=layout)
        try:
            assert attach_reference(conn, layout.reference_path)
            dbs = [r[0] for r in conn.execute("SELECT database_name FROM duckdb_databases()").fetchall()]
            assert dbs.count(REFERENCE_ALIAS) == 1
        finally:
            conn.close()

    def test_missing_reference_does_not_attach(self, tmp_path):
        conn = duckdb.connect()
        assert attach_reference(conn, tmp_path / "missing.duckdb") is False
        conn.close()


class TestEnsureDatabase:
    def test_creates_schema_once(self, tmp_path):
        db = tmp_path / "nested" / "cohorts.duckdb"
        ensure_database(db)
        ensure_database(db)  # second call runs migrations only
        conn = duckdb.connect(str(db), read_only=True)
        try:
            tables = {r[0] for r in conn.execute("SHOW TABLES").fetchall()}
            assert {"cohorts", "cohort_entities", "patients", "schema_migrations"} <= tables
        finally:
            conn.close()
