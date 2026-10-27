"""Tests for packaging, installing and migrating data into the plugin layout."""

import gzip
import json
import shutil
from pathlib import Path

import duckdb
import pytest

from healthsim.db import install
from healthsim.db.fixtures import build_reference_fixture
from healthsim.db.paths import ensure_database


@pytest.fixture
def unified_db(tmp_path):
    """A unified healthsim.duckdb: reference schemas plus a saved cohort."""
    path = build_reference_fixture(tmp_path / "unified" / "healthsim.duckdb")
    ensure_database(path)
    conn = duckdb.connect(str(path))
    conn.execute(
        "INSERT INTO cohorts (id, name, created_at, updated_at) VALUES ('c-1', 'diabetes-cohort', now(), now())"
    )
    conn.execute(
        "INSERT INTO cohort_entities (cohort_id, entity_type, entity_id, entity_data) "
        "VALUES ('c-1', 'patients', 'P-1', '{}'), ('c-1', 'patients', 'P-2', '{}')"
    )
    conn.execute("CHECKPOINT")
    conn.close()
    return path


@pytest.fixture
def home(tmp_path, monkeypatch):
    home = tmp_path / "healthsim-home"
    monkeypatch.setenv("HEALTHSIM_HOME", str(home))
    monkeypatch.delenv("HEALTHSIM_DB_PATH", raising=False)
    monkeypatch.delenv("HEALTHSIM_REFERENCE_PATH", raising=False)
    return home


def _tables(path):
    conn = duckdb.connect(str(path), read_only=True)
    try:
        return {f"{s}.{t}" for s, t in conn.execute("SELECT schema_name, table_name FROM duckdb_tables()").fetchall()}
    finally:
        conn.close()


class TestExtractReference:
    def test_copies_only_reference_schemas(self, unified_db, tmp_path):
        out = tmp_path / "ref.duckdb"
        summary = install.extract_reference(unified_db, out)
        tables = _tables(out)
        assert "network.providers" in tables
        assert "population.svi_county" in tables
        assert "main.cohorts" not in tables
        assert summary["tables"]["network.providers"] == 5

    def test_rejects_lfs_pointer(self, tmp_path):
        pointer = tmp_path / "healthsim.duckdb"
        pointer.write_text("version https://git-lfs.github.com/spec/v1\noid sha256:abc\nsize 1\n")
        with pytest.raises(FileNotFoundError, match="LFS"):
            install.extract_reference(pointer, tmp_path / "out.duckdb")


class TestInstallFromFile:
    def test_installs_into_home_and_layout_switches(self, unified_db, home):
        target = install.install_reference_from_file(unified_db)
        assert target == home / "reference.duckdb"
        info = install.status()
        assert info["mode"] == "split"
        assert info["has_reference"] is True
        assert not any(p.name.startswith("reference-") for p in home.iterdir())

    def test_rejects_database_without_reference(self, tmp_path, home):
        empty = tmp_path / "empty.duckdb"
        ensure_database(empty)
        with pytest.raises(ValueError, match="missing schemas"):
            install.install_reference_from_file(empty)
        assert not (home / "reference.duckdb").exists()


class TestPackageAndDownload:
    def test_round_trip_through_a_release(self, unified_db, tmp_path, home, monkeypatch):
        release = tmp_path / "release"
        db = release / "reference.duckdb"
        summary = install.extract_reference(unified_db, db)
        manifest_path = install.package_reference(db, release, tag="data-2026.10", tables=summary["tables"])
        manifest = json.loads(manifest_path.read_text())
        assert manifest["tag"] == "data-2026.10"
        assert manifest["tables"]["network.providers"] == 5

        base = "https://github.com/owner/repo/releases/download/data-2026.10"
        monkeypatch.setattr(
            install, "_get_json", lambda url: json.loads((release / Path(url).name).read_text())
        )
        monkeypatch.setattr(
            install, "_download", lambda url, dest, progress=None: shutil.copy(release / Path(url).name, dest)
        )
        target = install.download_reference(tag="data-2026.10", repo="owner/repo")
        assert target == home / "reference.duckdb"
        assert "network.providers" in _tables(target)
        assert install.status()["installed_release"] == "data-2026.10"

    def test_checksum_mismatch_is_rejected(self, unified_db, tmp_path, home, monkeypatch):
        release = tmp_path / "release"
        db = release / "reference.duckdb"
        install.extract_reference(unified_db, db)
        manifest_path = install.package_reference(db, release, tag="data-2026.10")
        manifest = json.loads(manifest_path.read_text())
        manifest["asset_sha256"] = "0" * 64
        monkeypatch.setattr(install, "_get_json", lambda url: manifest)
        monkeypatch.setattr(
            install, "_download", lambda url, dest, progress=None: shutil.copy(release / Path(url).name, dest)
        )
        with pytest.raises(ValueError, match="SHA-256"):
            install.download_reference(tag="data-2026.10", repo="owner/repo")
        assert not (home / "reference.duckdb").exists()

    def test_latest_release_ignores_code_tags(self, monkeypatch):
        monkeypatch.setattr(
            install,
            "_get_json",
            lambda url: [
                {"tag_name": "v1.2.0"},
                {"tag_name": "data-2026.09"},
                {"tag_name": "data-2026.10"},
                {"tag_name": "data-2026.11", "draft": True},
            ],
        )
        assert install.latest_data_release("owner/repo") == "data-2026.10"


class TestImportCohorts:
    def test_copies_cohorts_and_advances_sequences(self, unified_db, home):
        counts = install.import_cohorts(unified_db)
        assert counts["cohorts"] == 1
        assert counts["cohort_entities"] == 2
        conn = duckdb.connect(str(home / "cohorts.duckdb"))
        try:
            assert conn.execute("SELECT name FROM cohorts").fetchone()[0] == "diabetes-cohort"
            conn.execute(
                "INSERT INTO cohort_entities (cohort_id, entity_type, entity_id, entity_data) "
                "VALUES ('c-1', 'patients', 'P-3', '{}')"
            )
            ids = [r[0] for r in conn.execute("SELECT id FROM cohort_entities ORDER BY id").fetchall()]
            assert len(set(ids)) == 3
        finally:
            conn.close()

    def test_refuses_non_empty_destination(self, unified_db, home):
        install.import_cohorts(unified_db)
        with pytest.raises(ValueError, match="already has"):
            install.import_cohorts(unified_db)


class TestCommandLine:
    def test_status_and_from_file(self, unified_db, home, capsys):
        assert install.main(["from-file", str(unified_db), "--import-cohorts"]) == 0
        assert install.main(["status"]) == 0
        out = capsys.readouterr().out
        assert '"has_reference": true' in out

    def test_errors_return_nonzero(self, tmp_path, home):
        assert install.main(["from-file", str(tmp_path / "missing.duckdb")]) == 1
