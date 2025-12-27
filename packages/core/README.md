# HealthSim Core

Shared Python foundation for the HealthSim product family.

## Overview

This package provides:
- **Person & Entity Models**: Base classes for patients, members, subjects
- **Benefits Processing**: Accumulator tracking, deductibles, OOP calculations
- **Dimensional Modeling**: Star schema transformers for analytics
- **State Management**: Session, workspace, and scenario persistence
- **Generation Utilities**: Faker-based realistic data generation
- **Format Transformations**: FHIR, X12, NCPDP converters

## Installation

```bash
cd packages/core
pip install -e ".[dev]"
```

## Quick Start

```python
from healthsim import Person, generate_person

# Generate a realistic person
person = generate_person()
print(person.model_dump_json(indent=2))
```

---

## State Management API

HealthSim provides two patterns for scenario persistence: Traditional (full data) and Auto-Persist (token-efficient).

### Traditional Pattern

Best for scenarios under 50 entities where you want full data in context:

```python
from healthsim.state import (
    save_scenario,
    load_scenario, 
    list_scenarios,
    delete_scenario,
    scenario_exists,
)

# Save a scenario
scenario_id = save_scenario(
    name='my-scenario',
    entities={'patients': [...], 'encounters': [...]},
    tags=['diabetes', 'training'],
    description='Diabetes cohort for ML training'
)

# Load a scenario
scenario = load_scenario('my-scenario')
# Returns: {'patients': [...], 'encounters': [...], 'metadata': {...}}

# List scenarios
scenarios = list_scenarios(tag='diabetes', search='cohort')
for s in scenarios:
    print(f"{s['name']}: {s['entity_count']} entities")

# Check existence
if scenario_exists('my-scenario'):
    delete_scenario('my-scenario', confirm=True)
```

### Auto-Persist Pattern (Token-Efficient)

Best for large batches (50+ entities) where context efficiency matters:

```python
from healthsim.state import (
    persist,
    get_summary,
    query_scenario,
    get_auto_persist_service,
)

# Persist entities - returns summary, NOT full data (~500 tokens)
result = persist(
    entities={'patients': [...]},  # 200 patients
    context='diabetic patients in Texas over 65',
    tags=['diabetes', 'texas']
)
print(result.summary)  # ScenarioSummary with counts and 3 samples
print(result.scenario_name)  # 'diabetes-texas-20241227'

# Load summary only (~500-3500 tokens)
summary = get_summary('diabetes-texas-20241227')
print(f"Patients: {summary.entity_counts.get('patients', 0)}")
print(f"Samples: {summary.samples}")

# Query specific data with pagination
results = query_scenario(
    scenario_id=result.scenario_id,
    query="SELECT * FROM patients WHERE gender = 'F' AND birth_date < '1960-01-01'"
)
print(f"Found {results.total_count} matching patients")
print(f"Page {results.page + 1}, {len(results.results)} shown")
```

### Auto-Persist Service API

The `AutoPersistService` provides the full API:

```python
from healthsim.state import get_auto_persist_service

service = get_auto_persist_service()

# Core operations
result = service.persist_entities(entities, entity_type='patient')
summary = service.get_scenario_summary(scenario_id=..., include_samples=True)
query_result = service.query_scenario(scenario_id, "SELECT * FROM patients")
scenarios = service.list_scenarios(filter_pattern='diabetes', tag='training')
old, new = service.rename_scenario(scenario_id, 'new-name')
deleted = service.delete_scenario(scenario_id, confirm=True)
samples = service.get_entity_samples(scenario_id, 'patients', count=5)

# Tag management
tags = service.add_tag(scenario_id, 'validated')
tags = service.remove_tag(scenario_id, 'draft')
tags = service.get_tags(scenario_id)
all_tags = service.list_all_tags()  # [{tag, count}, ...]
scenarios = service.scenarios_by_tag('training')

# Cloning
clone = service.clone_scenario(
    source_scenario_id=...,
    new_name='my-clone',
    tags=['variation-a']
)

# Merging
merged = service.merge_scenarios(
    source_scenario_ids=[id1, id2, id3],
    target_name='combined-cohort',
    conflict_strategy='skip'  # or 'overwrite', 'rename'
)

# Export
export = service.export_scenario(
    scenario_id=...,
    format='json',  # or 'csv', 'parquet'
    output_path='/path/to/output.json'
)
# Convenience methods
service.export_to_json(scenario_id)
service.export_to_csv(scenario_id)
service.export_to_parquet(scenario_id)
```

### Data Classes

```python
from healthsim.state.auto_persist import (
    PersistResult,
    QueryResult,
    ScenarioBrief,
    CloneResult,
    MergeResult,
    ExportResult,
)

# PersistResult
result.scenario_id        # UUID
result.scenario_name      # Auto-generated name
result.entities_persisted # Count
result.entity_ids         # List of IDs
result.summary           # ScenarioSummary
result.is_new_scenario   # True if created

# QueryResult
query.results      # List[Dict]
query.total_count  # Total matching
query.page         # Current page (0-indexed)
query.page_size    # Results per page
query.has_more     # More pages available

# ScenarioSummary
summary.scenario_id
summary.name
summary.description
summary.tags
summary.entity_counts  # {'patients': 200, 'encounters': 500}
summary.statistics     # Domain-specific stats
summary.samples        # {'patients': [...3 samples...]}
summary.to_dict()
summary.to_json()
```

---

## JSON Import/Export

```python
from healthsim.state import export_scenario_to_json, import_scenario_from_json

# Export
path = export_scenario_to_json('my-scenario', '/path/to/export.json')

# Import
scenario_id = import_scenario_from_json(
    '/path/to/import.json',
    name_override='imported-scenario',
    overwrite=False
)
```

---

## DuckDB Schema

HealthSim stores all data in DuckDB (auto-created at `~/.healthsim/healthsim.duckdb`):

| Table | Description | ID Column |
|-------|-------------|-----------|
| `scenarios` | Scenario metadata | `scenario_id` |
| `scenario_tags` | Scenario tags | - |
| `patients` | PatientSim patients | `id` |
| `encounters` | Patient encounters | `encounter_id` |
| `diagnoses` | Diagnosis records | `id` |
| `members` | MemberSim members | `member_id` |
| `claims` | Insurance claims | `claim_id` |
| `prescriptions` | RxMemberSim prescriptions | `prescription_id` |
| `subjects` | TrialSim subjects | `subject_id` |
| ... | (41 total tables) | ... |

All entity tables include:
- `scenario_id` - Links to parent scenario
- `created_at` - Creation timestamp
- `source_type` - 'generated', 'loaded', 'derived'
- `source_system` - 'patientsim', 'membersim', etc.
- `skill_used` - Skill that created the entity

---

## Testing

```bash
# Run all tests
pytest

# Run state management tests only
pytest packages/core/tests/state/ -v

# Run with coverage
pytest --cov=healthsim --cov-report=html
```

Current test counts:
- Core package: **708 tests**
- State management: 222 tests
- Auto-persist: 63 tests (Phase 1) + 40 tests (Phase 2)

---

## Related Packages

- `packages/patientsim/` - PatientSim MCP and utilities
- `packages/membersim/` - MemberSim MCP and utilities  
- `packages/rxmembersim/` - RxMemberSim MCP and utilities

---

## Documentation

- [State Management Skill](../../skills/common/state-management.md)
- [DuckDB Skill](../../skills/common/duckdb-skill.md)
- [Auto-Persist Architecture](../../docs/healthsim-auto-persist-architecture.html)
- [Auto-Persist Examples](../../hello-healthsim/examples/auto-persist-examples.md)
