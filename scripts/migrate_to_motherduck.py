"""
migrate_to_motherduck.py — Migrate data from local DuckDB to MotherDuck.

Modes:
    --sample   Migrate a small sample (quick connectivity test)
    --full     Migrate all reference data + empty cohort schemas (default)

Usage:
    .venv/bin/python3 scripts/migrate_to_motherduck.py           # full migration
    .venv/bin/python3 scripts/migrate_to_motherduck.py --sample  # quick test

Environment:
    MOTHERDUCK_TOKEN must be set (via .env or shell export).
"""

import argparse
import os
import sys
import time
from pathlib import Path

import duckdb
from dotenv import load_dotenv

# Load .env from workspace root
WORKSPACE_ROOT = Path(__file__).parent.parent
load_dotenv(WORKSPACE_ROOT / ".env")

MOTHERDUCK_TOKEN = os.environ.get("MOTHERDUCK_TOKEN")
LOCAL_DB = WORKSPACE_ROOT / "healthsim.duckdb"

# MotherDuck schema mapping: local schema → MotherDuck schema
# network.* and population.* → reference.*  (read-only reference data)
# main.* cohort/scenario tables → cohort.*   (runtime synthetic data)
# main.schema_migrations → runtime.*         (system metadata)
SCHEMA_MAP = {
    "network": "reference",
    "population": "reference",
}

# Tables that go into 'cohort' schema (runtime synthetic data structures)
COHORT_TABLES = {
    "cohorts", "cohort_entities", "cohort_tags",
    "scenarios", "scenario_entities", "scenario_tags",
    "patients", "members", "claims", "claim_lines",
    "encounters", "diagnoses", "lab_results", "medications",
    "vital_signs", "prescriptions", "pharmacy_claims",
    "clinical_notes", "orders", "subjects", "trial_visits",
    "adverse_events", "exposures",
}

# Tables that go into 'runtime' schema (system metadata)
RUNTIME_TABLES = {"schema_migrations"}


def connect_motherduck():
    """Connect to MotherDuck and ensure database + schemas exist."""
    if not MOTHERDUCK_TOKEN:
        print("ERROR: MOTHERDUCK_TOKEN not set. Check .env file.", file=sys.stderr)
        sys.exit(1)

    print("Connecting to MotherDuck...")
    md = duckdb.connect(f"md:?motherduck_token={MOTHERDUCK_TOKEN}")
    md.execute("CREATE DATABASE IF NOT EXISTS healthsim_ref")
    md.execute("USE healthsim_ref")
    print("  Database 'healthsim_ref' ready")

    for schema in ("reference", "cohort", "runtime"):
        md.execute(f"CREATE SCHEMA IF NOT EXISTS {schema}")
        print(f"  Schema '{schema}' ready")

    return md


def migrate_table(local, md, source_table, dest_table, batch_size=500_000):
    """Migrate a single table from local DuckDB to MotherDuck, batched for large tables."""
    total = local.execute(f"SELECT COUNT(*) FROM {source_table}").fetchone()[0]
    print(f"  {source_table} → {dest_table} ({total:,} rows)", end="", flush=True)

    if total == 0:
        # Empty table — copy schema only
        md.execute(f"DROP TABLE IF EXISTS {dest_table}")
        cols = local.execute(f"DESCRIBE {source_table}").fetchall()
        col_defs = ", ".join(f'"{c[0]}" {c[1]}' for c in cols)
        md.execute(f"CREATE TABLE {dest_table} ({col_defs})")
        print(" [schema only]")
        return 0

    if total <= batch_size:
        # Small table — single batch via DataFrame
        data = local.execute(f"SELECT * FROM {source_table}").fetchdf()
        md.execute(f"DROP TABLE IF EXISTS {dest_table}")
        md.execute(f"CREATE TABLE {dest_table} AS SELECT * FROM data")
        print(f" ✓")
        return total

    # Large table — batched transfer
    md.execute(f"DROP TABLE IF EXISTS {dest_table}")
    migrated = 0
    batch_num = 0
    start = time.time()

    while migrated < total:
        data = local.execute(
            f"SELECT * FROM {source_table} LIMIT {batch_size} OFFSET {migrated}"
        ).fetchdf()

        if batch_num == 0:
            md.execute(f"CREATE TABLE {dest_table} AS SELECT * FROM data")
        else:
            md.execute(f"INSERT INTO {dest_table} SELECT * FROM data")

        migrated += len(data)
        batch_num += 1
        elapsed = time.time() - start
        rate = migrated / elapsed if elapsed > 0 else 0
        print(f"\r  {source_table} → {dest_table} ({migrated:,}/{total:,} rows, "
              f"{rate:,.0f} rows/s)", end="", flush=True)

    print(" ✓")
    return migrated


def resolve_dest(schema, table):
    """Map a local schema.table to the MotherDuck destination."""
    if schema in SCHEMA_MAP:
        return f"{SCHEMA_MAP[schema]}.{table}"
    if table in COHORT_TABLES:
        return f"cohort.{table}"
    if table in RUNTIME_TABLES:
        return f"runtime.{table}"
    # Fallback: put in runtime
    return f"runtime.{table}"


def migrate_full(local, md):
    """Migrate all tables to MotherDuck."""
    tables = local.execute("""
        SELECT table_schema, table_name
        FROM information_schema.tables
        WHERE table_schema NOT IN ('information_schema', 'pg_catalog')
        ORDER BY table_schema, table_name
    """).fetchall()

    print(f"\nMigrating {len(tables)} tables...\n")
    total_rows = 0
    start = time.time()

    for schema, table in tables:
        source = f"{schema}.{table}"
        dest = resolve_dest(schema, table)
        rows = migrate_table(local, md, source, dest)
        total_rows += rows

    elapsed = time.time() - start
    print(f"\n--- Migration complete ---")
    print(f"  Tables: {len(tables)}")
    print(f"  Total rows: {total_rows:,}")
    print(f"  Elapsed: {elapsed:.1f}s")


def migrate_sample(local, md):
    """Migrate a small sample for connectivity testing."""
    samples = [
        ("network.providers", "reference.nppes_sample", 1000),
        ("population.svi_county", "reference.svi_county", None),
        ("network.hospital_quality", "reference.hospital_quality", None),
    ]
    print(f"\nMigrating sample ({len(samples)} tables)...\n")
    for source, dest, limit in samples:
        if limit:
            query = f"SELECT * FROM {source} LIMIT {limit}"
            data = local.execute(query).fetchdf()
            md.execute(f"DROP TABLE IF EXISTS {dest}")
            md.execute(f"CREATE TABLE {dest} AS SELECT * FROM data")
            count = md.execute(f"SELECT COUNT(*) FROM {dest}").fetchone()[0]
            print(f"  {source} → {dest} ({count:,} rows, sampled)")
        else:
            migrate_table(local, md, source, dest)


def verify(md):
    """Print verification summary of what's in MotherDuck."""
    print("\n--- Verification ---")
    for schema in ("reference", "cohort", "runtime"):
        tables = md.execute(f"""
            SELECT table_name FROM information_schema.tables
            WHERE table_schema = '{schema}'
            ORDER BY table_name
        """).fetchall()
        if not tables:
            print(f"  {schema}: (empty)")
            continue
        for (table,) in tables:
            count = md.execute(
                f"SELECT COUNT(*) FROM {schema}.{table}"
            ).fetchone()[0]
            print(f"  {schema}.{table:40s} {count:>12,}")

    print("\nVerify at https://app.motherduck.com")


def main():
    parser = argparse.ArgumentParser(
        description="Migrate HealthSim data to MotherDuck"
    )
    parser.add_argument(
        "--sample", action="store_true",
        help="Migrate only a small sample (quick connectivity test)"
    )
    args = parser.parse_args()

    if not LOCAL_DB.exists():
        print(f"ERROR: Local database not found at {LOCAL_DB}", file=sys.stderr)
        sys.exit(1)

    local = duckdb.connect(str(LOCAL_DB), read_only=True)
    md = connect_motherduck()

    if args.sample:
        migrate_sample(local, md)
    else:
        migrate_full(local, md)

    verify(md)

    local.close()
    md.close()


if __name__ == "__main__":
    main()
