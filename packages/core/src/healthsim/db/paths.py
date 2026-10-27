"""
Data location resolution for HealthSim.

HealthSim keeps two kinds of data:

- Reference data (read-only, large): NPPES providers, CDC PLACES, SVI, ADI,
  stored in the ``network`` and ``population`` schemas.
- Cohort data (read-write, small): generated entities and saved cohorts,
  stored in the ``main`` schema.

These can live in one file (the original ``healthsim.duckdb`` at the repo
root) or in two files under ``~/.healthsim`` (the plugin layout), where
``cohorts.duckdb`` is the main database and ``reference.duckdb`` is attached
read-only. Code that queries ``network.providers`` or ``population.svi_county``
works unchanged in both layouts because the attached catalog is put on the
DuckDB ``search_path``.

Resolution order (first match wins):

1. ``HEALTHSIM_DB_PATH`` set: single database at that path, or MotherDuck
   when it starts with ``md:``. ``HEALTHSIM_REFERENCE_PATH`` may add a
   separate reference file.
2. ``$HEALTHSIM_HOME/reference.duckdb`` is a real database file: split
   layout under ``$HEALTHSIM_HOME`` (default ``~/.healthsim``).
3. ``HEALTHSIM_HOME`` is not set and ``<repo root>/healthsim.duckdb`` is a
   real database file (not a Git LFS pointer): single database, the
   developer layout. Setting ``HEALTHSIM_HOME`` opts out of this fallback.
4. Otherwise: split layout under ``$HEALTHSIM_HOME`` with no reference data
   yet. Cohort tools still work; reference tools report how to install data.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Union

import duckdb

REFERENCE_ALIAS = "healthsim_ref"
REFERENCE_FILENAME = "reference.duckdb"
COHORTS_FILENAME = "cohorts.duckdb"
LEGACY_FILENAME = "healthsim.duckdb"

# Schemas in the reference database that should resolve without a catalog
# prefix. "main" covers legacy ref_* tables.
REFERENCE_SCHEMAS = ("network", "population", "main")

# packages/core/src/healthsim/db/paths.py -> repo root is 5 levels up. In the
# Railway image the package sits at /app/healthsim, so there may be no repo.
_PARENTS = Path(__file__).resolve().parents
_REPO_ROOT_CANDIDATE = _PARENTS[5] if len(_PARENTS) > 5 else None


@dataclass(frozen=True)
class DataLayout:
    """Where HealthSim reads and writes data for this process."""

    mode: str  # "single", "split", or "motherduck"
    db_path: Union[str, Path]
    reference_path: Optional[Path]
    source: str  # human-readable reason this layout was chosen

    @property
    def is_motherduck(self) -> bool:
        return self.mode == "motherduck"

    @property
    def has_reference(self) -> bool:
        """True when reference tables are expected to be queryable."""
        if self.mode in ("single", "motherduck"):
            return True
        return self.reference_path is not None and is_valid_duckdb(self.reference_path)

    def describe(self) -> dict:
        return {
            "mode": self.mode,
            "db_path": _redact(str(self.db_path)),
            "reference_path": str(self.reference_path) if self.reference_path else None,
            "has_reference": self.has_reference,
            "source": self.source,
            "healthsim_home": str(get_healthsim_home()),
        }


def _redact(value: str) -> str:
    import re

    return re.sub(r"motherduck_token=[^&\s]+", "motherduck_token=***", value)


def get_healthsim_home() -> Path:
    """User data directory, ``$HEALTHSIM_HOME`` or ``~/.healthsim``."""
    env = os.environ.get("HEALTHSIM_HOME")
    return Path(env).expanduser() if env else Path.home() / ".healthsim"


def get_repo_root() -> Optional[Path]:
    """Repo root when running from a checkout or installed plugin, else None."""
    root = _REPO_ROOT_CANDIDATE
    if root is not None and (root / "skills").is_dir() and (root / "packages").is_dir():
        return root
    return None


def is_valid_duckdb(path: Union[str, Path]) -> bool:
    """True when ``path`` exists and is not a Git LFS pointer or empty stub."""
    from .lfs_check import is_lfs_pointer

    p = Path(path)
    if not p.is_file():
        return False
    if is_lfs_pointer(p):
        return False
    return p.stat().st_size > 1024


def resolve_layout() -> DataLayout:
    """Decide where data lives, following the order in the module docstring."""
    env_db = os.environ.get("HEALTHSIM_DB_PATH", "").strip()
    env_ref = os.environ.get("HEALTHSIM_REFERENCE_PATH", "").strip()
    ref_override = Path(env_ref).expanduser() if env_ref else None

    if env_db:
        if env_db.startswith("md:"):
            return DataLayout("motherduck", env_db, None, "HEALTHSIM_DB_PATH (MotherDuck)")
        mode = "split" if ref_override else "single"
        return DataLayout(mode, Path(env_db).expanduser(), ref_override, "HEALTHSIM_DB_PATH")

    home = get_healthsim_home()
    home_ref = ref_override or home / REFERENCE_FILENAME
    if is_valid_duckdb(home_ref):
        return DataLayout("split", home / COHORTS_FILENAME, home_ref, f"{home_ref}")

    repo = None if os.environ.get("HEALTHSIM_HOME", "").strip() else get_repo_root()
    if repo is not None and is_valid_duckdb(repo / LEGACY_FILENAME):
        return DataLayout("single", repo / LEGACY_FILENAME, None, "repo-root healthsim.duckdb")

    return DataLayout(
        "split",
        home / COHORTS_FILENAME,
        home_ref,
        "no reference data installed (run /healthsim:setup)",
    )


def reference_db_path() -> Optional[Path]:
    """Path of a local file that holds the reference schemas, or None.

    In the single layout that's the unified database; in the split layout
    it's ``reference.duckdb``. Code that only reads reference data can open
    this file directly, read-only.
    """
    layout = resolve_layout()
    if layout.mode == "single" and is_valid_duckdb(layout.db_path):
        return Path(layout.db_path)
    if layout.mode == "split" and layout.reference_path and is_valid_duckdb(layout.reference_path):
        return layout.reference_path
    return None


def attach_reference(conn: duckdb.DuckDBPyConnection, reference_path: Optional[Path]) -> bool:
    """Attach the reference database read-only and put its schemas on the search path.

    Returns True when the reference database was attached.
    """
    if reference_path is None or not is_valid_duckdb(reference_path):
        return False
    attached = {
        row[0] for row in conn.execute("SELECT database_name FROM duckdb_databases()").fetchall()
    }
    if REFERENCE_ALIAS not in attached:
        escaped = str(reference_path).replace("'", "''")
        conn.execute(f"ATTACH '{escaped}' AS {REFERENCE_ALIAS} (READ_ONLY)")
    schemas = {
        row[0]
        for row in conn.execute(
            "SELECT schema_name FROM duckdb_schemas() WHERE database_name = ?",
            [REFERENCE_ALIAS],
        ).fetchall()
    }
    search = ["main"] + [f"{REFERENCE_ALIAS}.{s}" for s in REFERENCE_SCHEMAS if s in schemas]
    conn.execute(f"SET search_path = '{','.join(search)}'")
    return True


def connect(
    read_only: bool = False,
    layout: Optional[DataLayout] = None,
) -> duckdb.DuckDBPyConnection:
    """Open the HealthSim database for the resolved layout, with reference attached."""
    layout = layout or resolve_layout()
    if layout.is_motherduck:
        return duckdb.connect(str(layout.db_path))
    db_path = Path(layout.db_path)
    if not db_path.exists():
        ensure_database(db_path)
    conn = duckdb.connect(str(db_path), read_only=read_only)
    attach_reference(conn, layout.reference_path)
    return conn


def ensure_database(db_path: Union[str, Path]) -> None:
    """Create the cohorts database with the canonical schema if it is new.

    A fresh plugin install has no cohorts file, and read-only connections
    can't create tables, so this runs once before the first connection.
    """
    from .migrations import run_migrations
    from .schema import apply_schema

    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = duckdb.connect(str(path))
    try:
        has_schema = conn.execute(
            "SELECT count(*) FROM information_schema.tables WHERE table_name = 'schema_migrations'"
        ).fetchone()[0]
        if has_schema:
            run_migrations(conn)
        else:
            apply_schema(conn)
        conn.execute("CHECKPOINT")
    finally:
        conn.close()
