"""
Install, package and migrate HealthSim data for the plugin layout.

The plugin layout keeps data in ``~/.healthsim`` (see ``healthsim.db.paths``):

- ``reference.duckdb``: read-only reference data (NPPES, CDC PLACES, SVI, ADI)
- ``cohorts.duckdb``: the user's generated cohorts

This module moves data into that layout:

- ``extract_reference``: copy the reference schemas out of a unified
  ``healthsim.duckdb`` into a standalone reference database (publishing)
- ``package_reference``: gzip a reference database and write its manifest
- ``download_reference``: fetch a published release, verify it, install it
- ``install_reference_from_file``: install from a local database file
- ``import_cohorts``: copy cohorts from a unified database into cohorts.duckdb

Command line (used by the plugin's setup command)::

    python -m healthsim.db.install status
    python -m healthsim.db.install download [--tag data-2026.10]
    python -m healthsim.db.install from-file /path/to/healthsim.duckdb [--import-cohorts]
    python -m healthsim.db.install import-cohorts /path/to/healthsim.duckdb
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
import shutil
import sys
import tempfile
import urllib.request
from datetime import date
from pathlib import Path
from typing import Callable, Iterable, Optional, Union

import duckdb

from .paths import (
    COHORTS_FILENAME,
    REFERENCE_FILENAME,
    ensure_database,
    get_healthsim_home,
    is_valid_duckdb,
    resolve_layout,
)

GITHUB_REPO = os.environ.get("HEALTHSIM_DATA_REPO", "mark64oswald/healthsim-workspace")
RELEASE_PREFIX = "data-"
ASSET_NAME = "reference.duckdb.gz"
MANIFEST_NAME = "reference-manifest.json"

# Schemas that hold reference data in the unified database
REFERENCE_SCHEMAS = ("network", "population")
# Legacy reference tables kept in main
LEGACY_REFERENCE_PREFIX = "ref_"

# Tables whose integer ids come from sequences, and the sequence for each
SEQUENCED_TABLES = {
    "cohort_entities": "cohort_entities_seq",
    "cohort_tags": "cohort_tags_seq",
    "profile_executions": "profiles_seq",
    "journey_executions": "journeys_seq",
}

# Tables other tables reference by foreign key; imported first
PARENT_TABLES = ("cohorts", "profiles", "journeys")

_CHUNK = 1024 * 1024


def _log(message: str) -> None:
    print(message, file=sys.stderr, flush=True)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(_CHUNK), b""):
            digest.update(block)
    return digest.hexdigest()


def _quote(identifier: str) -> str:
    return '"' + identifier.replace('"', '""') + '"'


def _sql_path(path: Path) -> str:
    return str(path).replace("'", "''")


# -----------------------------------------------------------------------------
# Publishing (run by the maintainer, from a machine with the real database)
# -----------------------------------------------------------------------------

def extract_reference(source_db: Union[str, Path], dest: Union[str, Path]) -> dict:
    """Copy reference schemas from a unified database into a new reference database.

    Returns a summary of the tables copied and their row counts.
    """
    source_db, dest = Path(source_db), Path(dest)
    if not is_valid_duckdb(source_db):
        raise FileNotFoundError(f"Not a usable DuckDB file (missing or Git LFS pointer): {source_db}")
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        dest.unlink()

    conn = duckdb.connect(str(dest))
    tables: dict = {}
    try:
        conn.execute(f"ATTACH '{_sql_path(source_db)}' AS src (READ_ONLY)")
        rows = conn.execute(
            """
            SELECT schema_name, table_name FROM duckdb_tables()
            WHERE database_name = 'src'
              AND (schema_name IN ('network', 'population')
                   OR (schema_name = 'main' AND table_name LIKE 'ref\\_%' ESCAPE '\\'))
            ORDER BY schema_name, table_name
            """
        ).fetchall()
        for schema in sorted({s for s, _ in rows}):
            conn.execute(f"CREATE SCHEMA IF NOT EXISTS {_quote(schema)}")
        for schema, table in rows:
            target = f"{_quote(schema)}.{_quote(table)}"
            _log(f"  copying {schema}.{table}")
            conn.execute(f"CREATE TABLE {target} AS SELECT * FROM src.{target}")
            tables[f"{schema}.{table}"] = conn.execute(f"SELECT count(*) FROM {target}").fetchone()[0]
        conn.execute("DETACH src")
        conn.execute("CHECKPOINT")
    finally:
        conn.close()
    return {"tables": tables, "table_count": len(tables)}


def package_reference(
    reference_db: Union[str, Path],
    out_dir: Union[str, Path],
    tag: Optional[str] = None,
    tables: Optional[dict] = None,
) -> Path:
    """Gzip a reference database and write the manifest next to it.

    Returns the manifest path.
    """
    reference_db, out_dir = Path(reference_db), Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    tag = tag or f"{RELEASE_PREFIX}{date.today():%Y.%m}"
    archive = out_dir / ASSET_NAME
    _log(f"  compressing {reference_db} -> {archive}")
    with open(reference_db, "rb") as src, gzip.open(archive, "wb", compresslevel=6) as dst:
        shutil.copyfileobj(src, dst, _CHUNK)
    manifest = {
        "tag": tag,
        "asset": ASSET_NAME,
        "asset_sha256": _sha256(archive),
        "asset_bytes": archive.stat().st_size,
        "database_sha256": _sha256(reference_db),
        "database_bytes": reference_db.stat().st_size,
        "duckdb_version": duckdb.__version__,
        "created": date.today().isoformat(),
        "tables": tables or {},
    }
    manifest_path = out_dir / MANIFEST_NAME
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest_path


# -----------------------------------------------------------------------------
# Installing (run by users, through the plugin's setup command)
# -----------------------------------------------------------------------------

def _install_file(candidate: Path, home: Path) -> Path:
    """Validate a reference database and move it into place atomically."""
    conn = duckdb.connect(str(candidate), read_only=True)
    try:
        schemas = {
            r[0] for r in conn.execute("SELECT schema_name FROM duckdb_schemas()").fetchall()
        }
    finally:
        conn.close()
    missing = [s for s in REFERENCE_SCHEMAS if s not in schemas]
    if missing:
        raise ValueError(f"{candidate} is not a HealthSim reference database (missing schemas: {missing})")
    home.mkdir(parents=True, exist_ok=True)
    target = home / REFERENCE_FILENAME
    os.replace(candidate, target)
    return target


def install_reference_from_file(source: Union[str, Path], home: Optional[Path] = None) -> Path:
    """Install reference data from a local file.

    ``source`` may be a standalone reference database or a unified
    ``healthsim.duckdb``; in the second case the reference schemas are
    extracted, leaving cohort tables behind.
    """
    source = Path(source).expanduser()
    home = home or get_healthsim_home()
    if not is_valid_duckdb(source):
        raise FileNotFoundError(
            f"Not a usable DuckDB file (missing or Git LFS pointer): {source}. "
            "In a checkout, run `git lfs pull` first."
        )
    home.mkdir(parents=True, exist_ok=True)
    tmp = Path(tempfile.mkstemp(prefix="reference-", suffix=".duckdb", dir=home)[1])
    tmp.unlink()
    try:
        extract_reference(source, tmp)
        return _install_file(tmp, home)
    finally:
        if tmp.exists():
            tmp.unlink()


def _get_json(url: str) -> object:
    request = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.load(response)


def latest_data_release(repo: str = GITHUB_REPO) -> str:
    """Tag of the newest ``data-*`` release in the repository."""
    releases = _get_json(f"https://api.github.com/repos/{repo}/releases?per_page=50")
    tags = sorted(
        (r["tag_name"] for r in releases if r["tag_name"].startswith(RELEASE_PREFIX) and not r.get("draft")),
        reverse=True,
    )
    if not tags:
        raise LookupError(f"No {RELEASE_PREFIX}* release found in {repo}")
    return tags[0]


def _download(url: str, dest: Path, progress: Optional[Callable[[int, int], None]] = None) -> None:
    with urllib.request.urlopen(url, timeout=120) as response, open(dest, "wb") as out:
        total = int(response.headers.get("Content-Length") or 0)
        done = 0
        while True:
            block = response.read(_CHUNK)
            if not block:
                break
            out.write(block)
            done += len(block)
            if progress:
                progress(done, total)


def _print_progress(done: int, total: int) -> None:
    if total and (done == total or done % (50 * _CHUNK) < _CHUNK):
        _log(f"  downloaded {done / 1e6:,.0f} of {total / 1e6:,.0f} MB")


def download_reference(
    tag: Optional[str] = None,
    home: Optional[Path] = None,
    repo: str = GITHUB_REPO,
) -> Path:
    """Download a published reference release, verify it, and install it."""
    home = home or get_healthsim_home()
    tag = tag or latest_data_release(repo)
    base = f"https://github.com/{repo}/releases/download/{tag}"
    _log(f"Installing HealthSim reference data {tag} into {home}")
    manifest = _get_json(f"{base}/{MANIFEST_NAME}")

    home.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=home, prefix=".download-") as tmpdir:
        archive = Path(tmpdir) / ASSET_NAME
        _download(f"{base}/{manifest['asset']}", archive, _print_progress)
        if _sha256(archive) != manifest["asset_sha256"]:
            raise ValueError("Downloaded archive failed its SHA-256 check; try again")
        database = Path(tmpdir) / REFERENCE_FILENAME
        _log("  decompressing")
        with gzip.open(archive, "rb") as src, open(database, "wb") as dst:
            shutil.copyfileobj(src, dst, _CHUNK)
        archive.unlink()
        if _sha256(database) != manifest["database_sha256"]:
            raise ValueError("Decompressed database failed its SHA-256 check; try again")
        target = _install_file(database, home)
    (home / MANIFEST_NAME).write_text(json.dumps(manifest, indent=2) + "\n")
    return target


# -----------------------------------------------------------------------------
# Cohort migration
# -----------------------------------------------------------------------------

def _main_tables(conn: duckdb.DuckDBPyConnection, database: str) -> list:
    return [
        r[0]
        for r in conn.execute(
            """
            SELECT table_name FROM duckdb_tables()
            WHERE database_name = ? AND schema_name = 'main'
              AND table_name NOT LIKE 'ref\\_%' ESCAPE '\\'
            """,
            [database],
        ).fetchall()
    ]


def import_cohorts(
    source_db: Union[str, Path],
    dest: Optional[Union[str, Path]] = None,
    skip_tables: Iterable[str] = ("schema_migrations",),
) -> dict:
    """Copy cohort and entity tables from a unified database into cohorts.duckdb.

    Rows are matched by column name, so a source on an older schema version
    still imports. Sequences are advanced past the imported ids. Run it on an
    empty cohorts database; importing twice duplicates rows.

    Returns row counts per table.
    """
    source_db = Path(source_db).expanduser()
    dest = Path(dest) if dest else get_healthsim_home() / COHORTS_FILENAME
    if not is_valid_duckdb(source_db):
        raise FileNotFoundError(f"Not a usable DuckDB file (missing or Git LFS pointer): {source_db}")
    ensure_database(dest)

    conn = duckdb.connect(str(dest))
    counts: dict = {}
    try:
        existing = conn.execute("SELECT count(*) FROM cohorts").fetchone()[0]
        if existing:
            raise ValueError(f"{dest} already has {existing} cohorts; import into an empty database")
        conn.execute(f"ATTACH '{_sql_path(source_db)}' AS src (READ_ONLY)")
        dest_db = conn.execute("SELECT current_database()").fetchone()[0]
        dest_tables = set(_main_tables(conn, dest_db))
        shared = set(_main_tables(conn, "src")) & dest_tables - set(skip_tables)
        ordered = [t for t in PARENT_TABLES if t in shared] + sorted(shared - set(PARENT_TABLES))
        for table in ordered:
            n = conn.execute(f"SELECT count(*) FROM src.main.{_quote(table)}").fetchone()[0]
            if n:
                conn.execute(
                    f"INSERT INTO main.{_quote(table)} BY NAME SELECT * FROM src.main.{_quote(table)}"
                )
            counts[table] = n
        for table, sequence in SEQUENCED_TABLES.items():
            if counts.get(table):
                top = conn.execute(f"SELECT coalesce(max(id), 0) FROM main.{_quote(table)}").fetchone()[0]
                conn.execute(f"SELECT nextval('{sequence}') FROM range(?)", [int(top)])
        conn.execute("DETACH src")
        conn.execute("CHECKPOINT")
    finally:
        conn.close()
    return counts


# -----------------------------------------------------------------------------
# Command line
# -----------------------------------------------------------------------------

def status() -> dict:
    layout = resolve_layout()
    info = layout.describe()
    manifest = get_healthsim_home() / MANIFEST_NAME
    if manifest.exists():
        info["installed_release"] = json.loads(manifest.read_text()).get("tag")
    return info


def main(argv: Optional[list] = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m healthsim.db.install", description=__doc__.split("\n\n")[0])
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("status", help="Show where HealthSim data lives")
    p_dl = sub.add_parser("download", help="Download published reference data into ~/.healthsim")
    p_dl.add_argument("--tag", help="Release tag, e.g. data-2026.10 (default: newest)")
    p_ff = sub.add_parser("from-file", help="Install reference data from a local DuckDB file")
    p_ff.add_argument("path")
    p_ff.add_argument("--import-cohorts", action="store_true", help="Also copy cohorts from the same file")
    p_ic = sub.add_parser("import-cohorts", help="Copy cohorts from a unified healthsim.duckdb")
    p_ic.add_argument("path")
    p_pub = sub.add_parser("package", help="Maintainers: extract and package reference data for a release")
    p_pub.add_argument("path", help="Unified healthsim.duckdb with the reference schemas")
    p_pub.add_argument("--out", default="dist/reference-data")
    p_pub.add_argument("--tag")
    args = parser.parse_args(argv)

    try:
        if args.command == "status":
            print(json.dumps(status(), indent=2))
        elif args.command == "download":
            print(download_reference(tag=args.tag))
        elif args.command == "from-file":
            print(install_reference_from_file(args.path))
            if args.import_cohorts:
                print(json.dumps(import_cohorts(args.path), indent=2))
        elif args.command == "import-cohorts":
            print(json.dumps(import_cohorts(args.path), indent=2))
        elif args.command == "package":
            out = Path(args.out)
            db = out / REFERENCE_FILENAME
            summary = extract_reference(args.path, db)
            print(package_reference(db, out, tag=args.tag, tables=summary["tables"]))
    except (OSError, ValueError, LookupError) as e:
        _log(f"error: {e}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
