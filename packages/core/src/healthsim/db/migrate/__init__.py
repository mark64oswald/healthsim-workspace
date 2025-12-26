"""
Migration tools for HealthSim database.

Provides utilities to migrate from previous storage formats
(JSON files) to the unified DuckDB database.
"""

from .json_scenarios import (
    MigrationResult,
    discover_json_scenarios,
    migrate_scenario,
    migrate_all_scenarios,
    backup_json_scenarios,
    verify_migration,
    LEGACY_PATH,
    BACKUP_PATH,
)

__all__ = [
    "MigrationResult",
    "discover_json_scenarios",
    "migrate_scenario",
    "migrate_all_scenarios",
    "backup_json_scenarios",
    "verify_migration",
    "LEGACY_PATH",
    "BACKUP_PATH",
]
