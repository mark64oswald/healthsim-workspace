"""
Database connection management for HealthSim.

Provides:
- Automatic database creation on first access
- Connection pooling (via DuckDB's built-in)
- Read-only mode support to avoid locking issues
- Dual backend: local DuckDB files or MotherDuck (cloud)

Backend selection:
  - Set HEALTHSIM_DB_PATH=md:database?motherduck_token=TOKEN for MotherDuck
  - Unset or set to a file path for local DuckDB (default)

MotherDuck note:
  MotherDuck handles concurrency server-side, so the close-before-write
  pattern used for local DuckDB files is unnecessary. When IS_MOTHERDUCK
  is True, read_only is ignored (MotherDuck connections are always r/w)
  and _ensure_directory is skipped (no local files).
"""

import atexit
import os
from pathlib import Path
from typing import Optional, Union
import duckdb

from .paths import DataLayout, attach_reference, ensure_database, resolve_layout

# Developer default: the unified database at the repo root (Git LFS). The
# plugin layout keeps data under ~/.healthsim instead; see healthsim.db.paths
# for the full resolution order.
#   - main schema: Entity tables (patients, members, etc.)
#   - population schema: PopulationSim reference data
#   - network schema: NetworkSim provider/facility data
WORKSPACE_ROOT = Path(__file__).parent.parent.parent.parent.parent.parent
DEFAULT_DB_PATH = WORKSPACE_ROOT / "healthsim.duckdb"

# Detect MotherDuck from environment
_db_env = os.environ.get("HEALTHSIM_DB_PATH", "")
IS_MOTHERDUCK = _db_env.startswith("md:")


def _resolve_db_path() -> Union[str, Path]:
    """Resolve the database path from environment or default."""
    return resolve_layout().db_path


class DatabaseConnection:
    """Manages DuckDB connections for HealthSim.

    Supports both local DuckDB files and MotherDuck cloud connections.
    The public API is identical for both backends — callers don't need
    to know which backend they're talking to.
    """

    _instance: Optional['DatabaseConnection'] = None
    _connection: Optional[duckdb.DuckDBPyConnection] = None
    _read_only: bool = False

    def __init__(self, db_path=None, read_only: bool = False):
        """
        Initialize database connection.

        Args:
            db_path: Path to database file, or MotherDuck connection string.
                     Uses HEALTHSIM_DB_PATH env var or DEFAULT_DB_PATH if not specified.
            read_only: If True, open database in read-only mode (local only;
                       ignored for MotherDuck).
        """
        layout: Optional[DataLayout] = None if db_path else resolve_layout()
        self.db_path = db_path or layout.db_path
        self.reference_path = layout.reference_path if layout else None
        self.is_motherduck = str(self.db_path).startswith("md:")
        self._read_only = read_only if not self.is_motherduck else False
        if not read_only and not self.is_motherduck:
            self._ensure_directory()

    def _ensure_directory(self) -> None:
        """Create database directory if it doesn't exist."""
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)

    def connect(self) -> duckdb.DuckDBPyConnection:
        """
        Get or create database connection.

        Returns:
            Active DuckDB connection.
        """
        if self._connection is None:
            if self.is_motherduck:
                self._connection = duckdb.connect(str(self.db_path))
            elif self._read_only:
                if not Path(self.db_path).exists():
                    ensure_database(self.db_path)
                self._connection = duckdb.connect(str(self.db_path), read_only=True)
            else:
                self._connection = duckdb.connect(str(self.db_path))
                self._initialize_if_needed()
            attach_reference(self._connection, self.reference_path)
        return self._connection

    def _initialize_if_needed(self) -> None:
        """Apply schema if this is a new database."""
        from .schema import apply_schema
        from .migrations import run_migrations

        # Check if schema_migrations table exists
        result = self._connection.execute("""
            SELECT count(*) FROM information_schema.tables
            WHERE table_name = 'schema_migrations'
        """).fetchone()

        if result[0] == 0:
            # New database - apply full schema
            apply_schema(self._connection)
        else:
            # Existing database - run any pending migrations
            run_migrations(self._connection)

    def close(self) -> None:
        """Close the database connection."""
        if self._connection:
            self._connection.close()
            self._connection = None

    @classmethod
    def get_instance(cls, db_path=None, read_only: bool = False) -> 'DatabaseConnection':
        """
        Get singleton database connection instance.

        Args:
            db_path: Override default path (only used on first call).
            read_only: If True, open in read-only mode (only used on first call).

        Returns:
            DatabaseConnection singleton.
        """
        if cls._instance is None:
            cls._instance = cls(db_path, read_only=read_only)
        return cls._instance

    @classmethod
    def reset(cls) -> None:
        """Reset singleton (for testing)."""
        if cls._instance:
            cls._instance.close()
        cls._instance = None


def get_connection(db_path=None, read_only: bool = False) -> duckdb.DuckDBPyConnection:
    """
    Convenience function to get database connection.

    Args:
        db_path: Optional path override (only used on first call).
        read_only: If True, open in read-only mode (only used on first call).

    Returns:
        Active DuckDB connection.
    """
    return DatabaseConnection.get_instance(db_path, read_only=read_only).connect()


def get_read_only_connection(db_path=None) -> duckdb.DuckDBPyConnection:
    """
    Get a read-only database connection (separate from main connection).

    This creates a separate connection that won't hold write locks,
    useful for concurrent query operations.

    For MotherDuck, returns a normal connection (MotherDuck handles
    concurrency server-side).

    Args:
        db_path: Optional path override.

    Returns:
        Read-only DuckDB connection.
    """
    if db_path is None:
        from .paths import connect

        return connect(read_only=True)
    if str(db_path).startswith("md:"):
        return duckdb.connect(str(db_path))
    return duckdb.connect(str(db_path), read_only=True)


def _cleanup_singleton():
    """Clean up singleton connection on process exit."""
    DatabaseConnection.reset()


# Register cleanup to run when Python exits
atexit.register(_cleanup_singleton)
