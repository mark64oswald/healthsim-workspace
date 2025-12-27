# HealthSim Auto-Persist Implementation Plan

**Status**: 🟡 IN PROGRESS  
**Started**: December 26, 2024  
**Last Updated**: December 27, 2024  
**Architecture Doc**: [healthsim-auto-persist-architecture.html](./healthsim-auto-persist-architecture.html)

---

## Quick Status Summary

| Phase | Status | Progress |
|-------|--------|----------|
| Phase 0: Preparation | ✅ Complete | 4/4 |
| Phase 1: Core Service Modules | 🟡 In Progress | 8/12 |
| Phase 2: Scenario Management | ⚪ Not Started | 0/6 |
| Phase 3: Skill Updates | ⚪ Not Started | 0/12 |
| Phase 4: Documentation | ⚪ Not Started | 0/10 |
| Phase 5: Testing & Validation | ⚪ Not Started | 0/6 |

**Legend**: ✅ Complete | 🟡 In Progress | ⚪ Not Started | ❌ Blocked

---

## Confirmed Design Decisions

| Decision | Value | Confirmed |
|----------|-------|-----------|
| Batch Size | 50 entities per batch | ✅ |
| Auto-Naming Format | `{keywords}-{YYYYMMDD}` | ✅ |
| Samples per Entity Type | 3 | ✅ |
| Default Query Page Size | 20 results | ✅ |
| Context Budget | ~5,500 tokens working | ✅ |

---

## Baseline Metrics (Captured Dec 26, 2024)

| Metric | Value |
|--------|-------|
| Core Package Tests | 668 passing ✅ |
| DuckDB Schema Tables | 41 |
| Entity Types Supported | 38 |
| Skills Files | ~30 |
| Hello-HealthSim Examples | 10 |

---

## Phase 0: Preparation ✅ COMPLETE

### 0.1 Documentation Review
- [x] Create implementation plan (this document)
- [x] Review existing MCP server structure (`packages/core/src/healthsim/db/`)
- [x] Review existing state-management skill
- [x] Inventory all files that need updates

### 0.2 Pre-Implementation Checklist
- [x] Verify DuckDB schema has all 41 tables
- [x] Verify existing tests pass (605 passing)
- [x] Review existing StateManager implementation
- [x] Document current file structure

### 0.3 Key Findings

**Existing Infrastructure**:
- `packages/core/src/healthsim/db/` - Database layer with connection, schema, queries, migrations
- `packages/core/src/healthsim/state/manager.py` - Existing StateManager class with save/load/list/delete
- `packages/core/src/healthsim/db/queries.py` - Has `get_scenario_summary`, `list_scenarios` already
- `skills/common/state-management.md` - Current skill (needs major update)
- `skills/common/duckdb-skill.md` - Current DuckDB skill (needs tool additions)

**Integration Strategy**:
- Build new services as extensions to existing `healthsim.state` module
- Leverage existing `StateManager` class infrastructure
- Add new modules to `packages/core/src/healthsim/state/` directory
- Update existing skills rather than create new ones

---

## Phase 1: Core Service Modules (4-5 hours) 🟡 IN PROGRESS

### 1.1 Service Modules ✅ COMPLETE

**Files Created**:
- `packages/core/src/healthsim/state/auto_naming.py` - Intelligent scenario naming
- `packages/core/src/healthsim/state/summary.py` - Token-efficient scenario summaries  
- `packages/core/src/healthsim/state/auto_persist.py` - Main AutoPersistService class

**Unit Tests Created** (63 tests, all passing):
- `packages/core/tests/state/test_auto_naming.py` - 25 tests
- `packages/core/tests/state/test_summary.py` - 13 tests
- `packages/core/tests/state/test_auto_persist.py` - 25 tests

**Schema Updates**:
- Added `scenario_id` column to all 18 canonical tables
- Added migration 1.2 for existing databases
- Updated schema version to 1.2
- Added indexes for scenario filtering

**Module Exports** (in `__init__.py`):
- Auto-naming: `generate_scenario_name`, `extract_keywords`, `ensure_unique_name`, `sanitize_name`, `parse_scenario_name`
- Summary: `ScenarioSummary`, `generate_summary`, `get_scenario_by_name`
- Auto-persist: `AutoPersistService`, `PersistResult`, `QueryResult`, `ScenarioBrief`, `get_auto_persist_service`, `reset_service`

### 1.2 Integration with StateManager ⚪ NOT STARTED

- [ ] Update `StateManager.save()` to use `AutoPersistService.persist_entities()`
- [ ] Update `StateManager.load()` to use `AutoPersistService.get_scenario_summary()`
- [ ] Add convenience methods to StateManager for query_scenario, list_scenarios
- [ ] Ensure backward compatibility with existing save/load behavior
- [ ] Write integration tests

### 1.3 Serializer Updates ⚪ NOT STARTED

- [ ] Update all serializers to include scenario_id in output
- [ ] Update deserializers to handle scenario_id
- [ ] Test roundtrip serialization with scenario_id

### 1.4 Phase 1 Final Integration ⚪ NOT STARTED

- [ ] Update `packages/core/src/healthsim/state/__init__.py` exports (if needed)
- [ ] Run full test suite (maintain 668+ passing)
- [ ] Manual integration test with sample generation

---

## Phase 2: Scenario Management (2-3 hours)

### Super-Prompt Location
`docs/super-prompts/phase2-scenario-management.md`

### 2.1 Additional Service Methods ⚪ NOT STARTED

AutoPersistService already has these methods implemented:
- ✅ `rename_scenario()` - Implemented with validation and duplicate check
- ✅ `delete_scenario()` - Implemented with cascade delete and confirmation
- ✅ `get_entity_samples()` - Implemented with diverse/random/recent strategies

Need to verify and enhance:
- [ ] Add tag management methods (add_tag, remove_tag)
- [ ] Add scenario cloning capability
- [ ] Add scenario merging capability

### 2.2 Export Utilities ⚪ NOT STARTED

- [ ] Add `export_scenario()` method to AutoPersistService
- [ ] Support JSON, CSV, and Parquet export formats
- [ ] Implement selective entity type export

### 2.3 Phase 2 Integration ⚪ NOT STARTED

- [ ] Update module exports
- [ ] Run full test suite
- [ ] Manual integration test

---

## Phase 3: Skill Updates (3-4 hours)

### Super-Prompt Location
`docs/super-prompts/phase3-skill-updates.md`

### 3.1 State Management Skill
**File**: `skills/common/state-management.md`

- [ ] Update overview to describe auto-persist behavior
- [ ] Add new trigger phrases for persist operations
- [ ] Update examples to show auto-persist workflow
- [ ] Add batch generation pattern
- [ ] Add scenario loading pattern (summary-only)
- [ ] Add query pattern with pagination
- [ ] Update validation rules
- [ ] Update related skills section

### 3.2 DuckDB Skill
**File**: `skills/common/duckdb-skill.md`

- [ ] Add all new MCP tools documentation
- [ ] Add trigger phrases for each tool
- [ ] Add examples for each tool
- [ ] Update the query patterns section
- [ ] Add batch generation guidance

### 3.3 PatientSim Skills (Generation)
**Files**: `skills/patientsim/*.md`

- [ ] Update patient-related skills with auto-persist pattern
- [ ] Add batch generation examples
- [ ] Update examples to show persist behavior

### 3.4 MemberSim Skills (Generation)
**Files**: `skills/membersim/*.md`

- [ ] Update member/claim skills with auto-persist pattern
- [ ] Add batch generation examples

### 3.5 Other Product Skills
- [ ] RxMemberSim skills update
- [ ] TrialSim skills update
- [ ] PopulationSim skills update
- [ ] NetworkSim skills update

### 3.6 Master SKILL.md Updates
**File**: `skills/healthsim-master-SKILL.md`

- [ ] Add auto-persist section
- [ ] Update routing to include persist-related triggers

---

## Phase 4: Documentation (2-3 hours)

### Super-Prompt Location
`docs/super-prompts/phase4-documentation.md`

### 4.1 Architecture Documentation
- [ ] Update `docs/healthsim-duckdb-architecture.html` with auto-persist
- [ ] Update `docs/healthsim-data-architecture.html`
- [ ] Finalize `docs/healthsim-auto-persist-architecture.html` (change status to Active)

### 4.2 README Files
- [ ] Update main `README.md` with auto-persist overview
- [ ] Update `packages/core/README.md` with new tools
- [ ] Update `tools/README.md` with persist utilities
- [ ] Update `skills/README.md` (if exists)

### 4.3 Hello-HealthSim Examples
**Directory**: `hello-healthsim/examples/`

- [ ] Create `auto-persist-examples.md`
- [ ] Update `patientsim-examples.md` with persist examples
- [ ] Update `membersim-examples.md` with persist examples
- [ ] Update `cross-domain-examples.md` with query examples
- [ ] Update main `README.md` index

### 4.4 CHANGELOG
- [ ] Add comprehensive entry for auto-persist feature

---

## Phase 5: Testing & Validation (2-3 hours)

### Super-Prompt Location
`docs/super-prompts/phase5-testing.md`

### 5.1 Unit Tests ✅ LARGELY COMPLETE

Tests created in Phase 1.1:
- [x] `test_auto_naming.py` - 25 tests
- [x] `test_summary.py` - 13 tests  
- [x] `test_auto_persist.py` - 25 tests

Additional tests needed:
- [ ] Integration tests with StateManager
- [ ] Serializer tests with scenario_id

### 5.2 Integration Tests ⚪ NOT STARTED

- [ ] Test full generation → persist → query workflow
- [ ] Test batch generation with 100+ entities
- [ ] Test scenario load → generate more → query
- [ ] Test cross-product scenarios (Patient + Member + Claim)

### 5.3 Regression Tests ⚪ NOT STARTED

- [x] Verify all existing tests still pass (668 passing)
- [ ] Verify loader/saver utilities still work
- [ ] Verify existing scenarios can still be loaded

### 5.4 Manual Testing Scenarios ⚪ NOT STARTED

- [ ] "Generate a diabetic patient" → verify persist
- [ ] "Generate 100 Medicare members" → verify batch persist
- [ ] "Load scenario X" → verify summary only loaded
- [ ] "Show claims over $10,000" → verify paginated query
- [ ] "Rename this scenario" → verify rename works

### 5.5 Final Validation ⚪ NOT STARTED

- [ ] Full test suite passes (668+ tests)
- [ ] No regressions in existing functionality
- [ ] Documentation is complete and consistent
- [ ] Git commit with comprehensive message

---

## Complete File Inventory

### Files CREATED (Phase 1.1)

| File | Status | Notes |
|------|--------|-------|
| `packages/core/src/healthsim/state/auto_naming.py` | ✅ | Keyword extraction, name generation |
| `packages/core/src/healthsim/state/summary.py` | ✅ | ScenarioSummary, statistics |
| `packages/core/src/healthsim/state/auto_persist.py` | ✅ | AutoPersistService class |
| `packages/core/tests/state/test_auto_naming.py` | ✅ | 25 unit tests |
| `packages/core/tests/state/test_summary.py` | ✅ | 13 unit tests |
| `packages/core/tests/state/test_auto_persist.py` | ✅ | 25 unit tests |

### Files MODIFIED (Phase 1.1)

| File | Status | Changes |
|------|--------|---------|
| `packages/core/src/healthsim/state/__init__.py` | ✅ | Added exports for new modules |
| `packages/core/src/healthsim/db/schema.py` | ✅ | Added scenario_id, version 1.2 |
| `packages/core/src/healthsim/db/migrations.py` | ✅ | Added migration 1.2 |

### Files Still to CREATE

| File | Phase | Priority |
|------|-------|----------|
| `hello-healthsim/examples/auto-persist-examples.md` | 4 | Medium |
| `docs/super-prompts/phase2-scenario-management.md` | 2 | Medium |
| `docs/super-prompts/phase3-skill-updates.md` | 3 | Medium |
| `docs/super-prompts/phase4-documentation.md` | 4 | Medium |
| `docs/super-prompts/phase5-testing.md` | 5 | Medium |

### Files Still to MODIFY

| File | Phase | Changes |
|------|-------|---------|
| `packages/core/src/healthsim/state/manager.py` | 1.2 | Integrate AutoPersistService |
| `packages/core/src/healthsim/db/serializers.py` | 1.3 | Add scenario_id handling |
| `skills/common/state-management.md` | 3 | Major update for auto-persist |
| `skills/common/duckdb-skill.md` | 3 | Add new tools |
| `skills/patientsim/*.md` | 3 | Add persist patterns |
| `skills/membersim/*.md` | 3 | Add persist patterns |
| `docs/healthsim-duckdb-architecture.html` | 4 | Add auto-persist section |
| `docs/healthsim-auto-persist-architecture.html` | 4 | Change status to Active |
| `hello-healthsim/examples/patientsim-examples.md` | 4 | Add persist examples |
| `README.md` | 4 | Add auto-persist section |
| `CHANGELOG.md` | 4 | Add feature entry |

---

## Session Log

### Session 1: December 26, 2024
**Focus**: Phase 0 (Preparation)
**Duration**: ~30 minutes
**Status**: ✅ Complete

#### Completed
- [x] Created implementation plan document
- [x] Confirmed design decisions with user
- [x] Created architecture document
- [x] Reviewed existing code structure
- [x] Ran baseline tests (605 passing)
- [x] Documented existing infrastructure
- [x] Created complete file inventory

### Session 2: December 26-27, 2024
**Focus**: Phase 1.1 (Service Modules)
**Duration**: ~2 hours
**Status**: ✅ Complete

#### Completed
- [x] Created `auto_naming.py` with keyword extraction, name generation
- [x] Created `summary.py` with ScenarioSummary dataclass, statistics
- [x] Created `auto_persist.py` with AutoPersistService class (7 methods)
- [x] Created 63 unit tests across 3 test files
- [x] Updated schema to add scenario_id to all canonical tables
- [x] Added migration 1.2 for existing databases
- [x] Updated module exports in `__init__.py`
- [x] All 668 tests passing

#### Key Accomplishments
- Complete AutoPersistService with persist/query/list/delete/rename operations
- SQL safety validation (SELECT-only queries, dangerous pattern blocking)
- Token-efficient summaries with configurable samples
- Healthcare-aware keyword extraction for auto-naming
- Fuzzy scenario lookup by name

#### Next Session Focus
- Phase 1.2: Integration with existing StateManager
- Phase 1.3: Serializer updates for scenario_id

---

## Recovery Instructions

If context is lost or session crashes:

1. **Read this document first**: `docs/AUTO-PERSIST-IMPLEMENTATION-PLAN.md`
2. **Check the Session Log** above for current status
3. **Review architecture**: `docs/healthsim-auto-persist-architecture.html`
4. **Check git status**: `git status` and `git log -5`
5. **Run tests**: `cd packages/core && pytest` to verify current state
6. **Resume from last incomplete task** in the checklist

---

## Git Commit Strategy

- Commit after each phase completion
- Use format: `[Auto-Persist] Phase X.Y: Brief description`
- Push at end of each session
- Tag major milestones: `auto-persist-phase-1`, etc.

### Commits Made
- `[Auto-Persist] Phase 1.1 complete - Service modules and unit tests` (Dec 27, 2024)

---

*Last updated by Claude - December 27, 2024*
