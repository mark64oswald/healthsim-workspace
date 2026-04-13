"""
migrate_to_motherduck.py — Migrate reference data from local DuckDB to MotherDuck.

Phase 0: Migrates a small sample to validate the connection and query patterns.
Phase 1: Full migration (--full flag, not yet implemented).

Usage:
    .venv/bin/python3 scripts/migrate_to_motherduck.py          # Phase 0 sample
    .venv/bin/python3 scripts/migrate_to_motherduck.py --full    # Phase 1 (not yet)

Environment:
    MOTHERDUCK_TOKEN must be set (via .env or shell export).
"""

import argparse
import os
import sys
from pathlib import Path

import duckdb
from dotenv import load_dotenv

# Load .env from workspace root
WORKSPACE_ROOT = Path(__file__).parent.parent
load_dotenv(WORKSPACE_ROOT / ".env")

MOTHERDUCK_TOKEN = os.environ.get("MOTHERDUCK_TOKEN")
LOCAL_DB = WORKSPACE_ROOT / "healthsim.duckdb"

# Tables to migrate in Phase 0 sample: (source, destination, limit)
SAMPLE_TABLES = [
    ("network.providers", "reference.nppes_sample", 1000),
    ("population.svi_county", "reference.svi_county", None),  # full table — serves as FIPS crosswalk
    ("network.hospital_quality", "reference.hospital_quality", None),  # small ref table
]


def migrate_sample():
    """Migrate a small slice of reference data to MotherDuck."""
    if not MOTHERDUCK_TOKEN:
        print("ERROR: MOTHERDUCK_TOKEN not set. Check your .env file.", file=sys.stderr)
        sys.exit(1)

    if not LOCAL_DB.exists():
        print(f"ERROR: Local database not found at {LOCAL_DB}", file=sys.stderr)
        sys.exit(1)

    # Connect to local DuckDB (read-only)
    print(f"Connecting to local DuckDB: {LOCAL_DB}")
    local = duckdb.connect(str(LOCAL_DB), read_only=True)

    # Connect to MotherDuck and create the database if needed
    print("Connecting to MotherDuck...")
    md = duckdb.connect(f"md:?motherduck_token={MOTHERDUCK_TOKEN}")
    md.execute("CREATE DATABASE IF NOT EXISTS healthsim_ref")
    md.execute("USE healthsim_ref")
    print("  Database 'healthsim_ref' ready")

    # Create schemas
    for schema in ("reference", "cohort", "runtime"):
        md.execute(f"CREATE SCHEMA IF NOT EXISTS {schema}")
        print(f"  Schema '{schema}' ready")

    # Migrate each table
    print()
    for source_table, dest_table, limit in SAMPLE_TABLES:
        print(f"Migrating {source_table} → {dest_table}", end="")
        if limit:
            print(f" (LIMIT {limit:,})")
        else:
            print(" (full table)")

        # Read from local
        query = f"SELECT * FROM {source_table}"
        if limit:
            query += f" LIMIT {limit}"
        data = local.execute(query).fetchdf()

        # Write to MotherDuck
        md.execute(f"DROP TABLE IF EXISTS {dest_table}")
        md.execute(f"CREATE TABLE {dest_table} AS SELECT * FROM data")

        # Verify
        count = md.execute(f"SELECT COUNT(*) FROM {dest_table}").fetchone()[0]
        print(f"  → {count:,} rows written")

    # Run verification query
    print("\n--- Verification ---")
    result = md.execute("""
        SELECT COUNT(*) as total,
               COUNT(DISTINCT practice_state) as states
        FROM reference.nppes_sample
    """).fetchone()
    print(f"nppes_sample: {result[0]:,} rows, {result[1]} distinct states")

    result = md.execute("SELECT COUNT(*) FROM reference.svi_county").fetchone()
    print(f"svi_county: {result[0]:,} rows")

    result = md.execute("SELECT COUNT(*) FROM reference.hospital_quality").fetchone()
    print(f"hospital_quality: {result[0]:,} rows")

    # Summary
    print("\nPhase 0 migration complete. Verify at https://app.motherduck.com")

    local.close()
    md.close()


def main():
    parser = argparse.ArgumentParser(description="Migrate reference data to MotherDuck")
    parser.add_argument("--full", action="store_true", help="Full migration (Phase 1)")
    args = parser.parse_args()

    if args.full:
        print("Full migration not yet implemented — use without --full for the Phase 0 sample.")
        sys.exit(0)

    migrate_sample()


if __name__ == "__main__":
    main()
