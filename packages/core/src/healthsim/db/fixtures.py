"""
Tiny reference database for tests and smoke tests.

Builds a ``reference.duckdb`` with the same schemas, tables and key columns as
the real HealthSim reference data (``network.providers``,
``population.svi_county`` and friends), holding a handful of made-up rows.
It lets the plugin layout be tested without the 1.7 GB Git LFS file.

Usage:
    python -m healthsim.db.fixtures /path/to/reference.duckdb
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Union

import duckdb

_PROVIDERS = [
    # npi, type, first, last, org, credential, taxonomy, address, city, state, zip, county_fips, phone
    ("1000000001", 1, "Ana", "Rivera", None, "MD", "207Q00000X", "100 Main St", "San Diego", "CA", "92101", "06073", "6195550101"),
    ("1000000002", 1, "Ben", "Okafor", None, "MD", "207R00000X", "200 Elm St", "San Diego", "CA", "92103", "06073", "6195550102"),
    ("1000000003", 2, None, None, "Harbor Community Hospital", None, "282N00000X", "1 Harbor Way", "San Diego", "CA", "92101", "06073", "6195550103"),
    ("1000000004", 1, "Chen", "Li", None, "NP", "363L00000X", "300 Oak St", "Houston", "TX", "77002", "48201", "7135550104"),
    ("1000000005", 2, None, None, "Bayou Pharmacy", None, "3336C0003X", "400 Pine St", "Houston", "TX", "77003", "48201", "7135550105"),
]

_COUNTIES = [
    # fips, state, county name, svi overall, diabetes %, obesity %
    ("06073", "CA", "San Diego", 0.52, 9.8, 26.1),
    ("48201", "TX", "Harris", 0.81, 12.4, 33.0),
]


def build_reference_fixture(path: Union[str, Path]) -> Path:
    """Create (or replace) a small reference database at ``path``."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        path.unlink()
    conn = duckdb.connect(str(path))
    try:
        conn.execute("CREATE SCHEMA network")
        conn.execute("CREATE SCHEMA population")
        conn.execute("""
            CREATE TABLE network.providers (
                npi VARCHAR, entity_type_code INTEGER,
                first_name VARCHAR, last_name VARCHAR, organization_name VARCHAR,
                credential VARCHAR,
                taxonomy_1 VARCHAR, taxonomy_2 VARCHAR, taxonomy_3 VARCHAR, taxonomy_4 VARCHAR,
                practice_address_1 VARCHAR, practice_city VARCHAR, practice_state VARCHAR,
                practice_zip VARCHAR, county_fips VARCHAR, phone VARCHAR
            )
        """)
        conn.executemany(
            "INSERT INTO network.providers VALUES (?, ?, ?, ?, ?, ?, ?, NULL, NULL, NULL, ?, ?, ?, ?, ?, ?)",
            _PROVIDERS,
        )
        conn.execute("""
            CREATE TABLE population.svi_county (
                fips VARCHAR, st_abbr VARCHAR, county VARCHAR, rpl_themes DOUBLE
            )
        """)
        conn.execute("""
            CREATE TABLE population.places_county (
                countyfips VARCHAR, stateabbr VARCHAR, countyname VARCHAR,
                diabetes_crudeprev DOUBLE, obesity_crudeprev DOUBLE
            )
        """)
        for fips, state, county, svi, diabetes, obesity in _COUNTIES:
            conn.execute(
                "INSERT INTO population.svi_county VALUES (?, ?, ?, ?)",
                [fips, state, f"{county} County", svi],
            )
            conn.execute(
                "INSERT INTO population.places_county VALUES (?, ?, ?, ?, ?)",
                [fips, state, county, diabetes, obesity],
            )
        conn.execute("CHECKPOINT")
    finally:
        conn.close()
    return path


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python -m healthsim.db.fixtures /path/to/reference.duckdb", file=sys.stderr)
        sys.exit(2)
    print(build_reference_fixture(sys.argv[1]))
