# HealthSim Auto-Persist Implementation Plan

**Status**: 🟡 IN PROGRESS  
**Started**: December 26, 2024  
**Last Updated**: December 26, 2024  
**Architecture Doc**: [healthsim-auto-persist-architecture.html](./healthsim-auto-persist-architecture.html)

---

## Quick Status Summary

| Phase | Status | Progress |
|-------|--------|----------|
| Phase 0: Preparation | ✅ Complete | 4/4 |
| Phase 1: Core MCP Tools | ⚪ Not Started | 0/8 |
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
| Core Package Tests | 605 passing ✅ |
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
- Build new tools as extensions to existing `healthsim.db` module
- Leverage existing `StateManager` class infrastructure
- Add new tools to `packages/core/src/healthsim/db/tools/` directory
- Update existing skills rather than create new ones

---

## Phase 1: Core MCP Tools (4-5 hours)

### Super-Prompt Location
`docs/super-prompts/phase1-core-mcp-tools.md`

### 1.1 persist_entities Tool
**File**: `packages/core/src/healthsim/db/tools/persist_entities.py`

- [ ] Create tool file with proper structure
- [ ] Implement entity type to table mapping (all 38 types)
- [ ] Implement auto-scenario creation logic
- [ ] Implement auto-naming logic (extract keywords from context)
- [ ] Implement batch insert with transaction
- [ ] Implement ID extraction and return
- [ ] Implement summary refresh after insert
- [ ] Add to module `__init__.py`
- [ ] Write unit tests
- [ ] Test with sample entities

**Signature**:
```python
def persist_entities(
    entities: List[Dict],
    entity_type: str,
    scenario_id: Optional[str] = None,
    scenario_name: Optional[str] = None,
    scenario_description: Optional[str] = None,
    tags: Optional[List[str]] = None
) -> PersistResult
```

### 1.2 get_scenario_summary Tool
**File**: `packages/core/src/healthsim/db/tools/get_scenario_summary.py`

- [ ] Create tool file
- [ ] Implement scenario lookup (by ID or name)
- [ ] Implement entity count aggregation
- [ ] Implement statistics calculation:
  - [ ] Date ranges
  - [ ] Financial totals (billed, paid, patient responsibility)
  - [ ] Age statistics (range, median)
  - [ ] Gender distribution
  - [ ] Top diagnoses/conditions
  - [ ] Encounter type distribution
- [ ] Implement sample entity retrieval
- [ ] Add to module `__init__.py`
- [ ] Write unit tests
- [ ] Test with existing scenario

**Signature**:
```python
def get_scenario_summary(
    scenario_id: Optional[str] = None,
    scenario_name: Optional[str] = None,
    include_samples: bool = True,
    samples_per_type: int = 3
) -> ScenarioSummary
```

### 1.3 query_scenario Tool
**File**: `packages/core/src/healthsim/db/tools/query_scenario.py`

- [ ] Create tool file
- [ ] Implement SQL validation (SELECT only)
- [ ] Implement scenario scoping (filter by scenario_id)
- [ ] Implement pagination (limit/offset)
- [ ] Implement total count query
- [ ] Implement result serialization
- [ ] Add to module `__init__.py`
- [ ] Write unit tests
- [ ] Test with various SQL queries

**Signature**:
```python
def query_scenario(
    scenario_id: str,
    query: str,
    limit: int = 20,
    offset: int = 0
) -> QueryResult
```

### 1.4 list_scenarios Tool
**File**: `packages/core/src/healthsim/db/tools/list_scenarios.py`

- [ ] Create tool file (extend existing queries.list_scenarios)
- [ ] Implement scenario listing with brief stats
- [ ] Implement filtering (by name pattern, date range, tags)
- [ ] Implement sorting (by date, name, entity count)
- [ ] Add to module `__init__.py`
- [ ] Write unit tests
- [ ] Test listing

**Signature**:
```python
def list_scenarios(
    filter_pattern: Optional[str] = None,
    tag: Optional[str] = None,
    limit: int = 20,
    sort_by: str = "updated_at"
) -> List[ScenarioBrief]
```

### 1.5 Phase 1 Integration
- [ ] Create `packages/core/src/healthsim/db/tools/__init__.py`
- [ ] Update `packages/core/src/healthsim/db/__init__.py` to export tools
- [ ] Run full test suite (maintain 605+ passing)
- [ ] Manual integration test

---

## Phase 2: Scenario Management (2-3 hours)

### Super-Prompt Location
`docs/super-prompts/phase2-scenario-management.md`

### 2.1 rename_scenario Tool
**File**: `packages/core/src/healthsim/db/tools/rename_scenario.py`

- [ ] Create tool file
- [ ] Implement rename with validation
- [ ] Handle duplicate name prevention
- [ ] Add to module exports
- [ ] Write unit tests

### 2.2 delete_scenario Tool  
**File**: `packages/core/src/healthsim/db/tools/delete_scenario.py`

- [ ] Create tool file
- [ ] Implement cascade delete (scenario + all linked entities)
- [ ] Add confirmation requirement
- [ ] Add to module exports
- [ ] Write unit tests

### 2.3 get_entity_samples Tool
**File**: `packages/core/src/healthsim/db/tools/get_entity_samples.py`

- [ ] Create tool file
- [ ] Implement random sampling with diversity
- [ ] Support all entity types
- [ ] Add to module exports
- [ ] Write unit tests

### 2.4 Auto-Naming Service
**File**: `packages/core/src/healthsim/db/services/auto_naming.py`

- [ ] Create service file
- [ ] Implement keyword extraction from generation request
- [ ] Implement date formatting
- [ ] Implement uniqueness check (append counter if needed)
- [ ] Write unit tests

### 2.5 Phase 2 Integration
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

- [ ] Add all 7 new MCP tools documentation
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
**File**: `skills/healthsim-master-SKILL.md` (if exists)

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

### 5.1 Unit Tests
**Directory**: `packages/core/tests/db/tools/`

- [ ] `test_persist_entities.py`
- [ ] `test_get_scenario_summary.py`
- [ ] `test_query_scenario.py`
- [ ] `test_list_scenarios.py`
- [ ] `test_rename_scenario.py`
- [ ] `test_delete_scenario.py`
- [ ] `test_get_entity_samples.py`
- [ ] `test_auto_naming.py`

### 5.2 Integration Tests
- [ ] Test full generation → persist → query workflow
- [ ] Test batch generation with 100+ entities
- [ ] Test scenario load → generate more → query
- [ ] Test cross-product scenarios (Patient + Member + Claim)

### 5.3 Regression Tests
- [ ] Verify all 605+ existing tests still pass
- [ ] Verify loader/saver utilities still work
- [ ] Verify existing scenarios can still be loaded

### 5.4 Manual Testing Scenarios
- [ ] "Generate a diabetic patient" → verify persist
- [ ] "Generate 100 Medicare members" → verify batch persist
- [ ] "Load scenario X" → verify summary only loaded
- [ ] "Show claims over $10,000" → verify paginated query
- [ ] "Rename this scenario" → verify rename works

### 5.5 Final Validation
- [ ] Full test suite passes (605+ tests)
- [ ] No regressions in existing functionality
- [ ] Documentation is complete and consistent
- [ ] Git commit with comprehensive message

---

## Complete File Inventory

### Files to CREATE

| File | Phase | Priority |
|------|-------|----------|
| `packages/core/src/healthsim/db/tools/__init__.py` | 1 | High |
| `packages/core/src/healthsim/db/tools/persist_entities.py` | 1 | High |
| `packages/core/src/healthsim/db/tools/get_scenario_summary.py` | 1 | High |
| `packages/core/src/healthsim/db/tools/query_scenario.py` | 1 | High |
| `packages/core/src/healthsim/db/tools/list_scenarios.py` | 1 | High |
| `packages/core/src/healthsim/db/tools/rename_scenario.py` | 2 | Medium |
| `packages/core/src/healthsim/db/tools/delete_scenario.py` | 2 | Medium |
| `packages/core/src/healthsim/db/tools/get_entity_samples.py` | 2 | Medium |
| `packages/core/src/healthsim/db/services/__init__.py` | 2 | Medium |
| `packages/core/src/healthsim/db/services/auto_naming.py` | 2 | Medium |
| `packages/core/tests/db/tools/__init__.py` | 5 | Medium |
| `packages/core/tests/db/tools/test_persist_entities.py` | 5 | Medium |
| `packages/core/tests/db/tools/test_scenario_tools.py` | 5 | Medium |
| `hello-healthsim/examples/auto-persist-examples.md` | 4 | Medium |
| `docs/super-prompts/phase1-core-mcp-tools.md` | 0 | High |
| `docs/super-prompts/phase2-scenario-management.md` | 0 | Medium |
| `docs/super-prompts/phase3-skill-updates.md` | 0 | Medium |
| `docs/super-prompts/phase4-documentation.md` | 0 | Medium |
| `docs/super-prompts/phase5-testing.md` | 0 | Medium |

### Files to MODIFY

| File | Phase | Changes |
|------|-------|---------|
| `packages/core/src/healthsim/db/__init__.py` | 1 | Export new tools |
| `skills/common/state-management.md` | 3 | Major update for auto-persist |
| `skills/common/duckdb-skill.md` | 3 | Add 7 new tools |
| `skills/patientsim/*.md` | 3 | Add persist patterns |
| `skills/membersim/*.md` | 3 | Add persist patterns |
| `skills/rxmembersim/*.md` | 3 | Add persist patterns |
| `skills/trialsim/*.md` | 3 | Add persist patterns |
| `docs/healthsim-duckdb-architecture.html` | 4 | Add auto-persist section |
| `docs/healthsim-auto-persist-architecture.html` | 4 | Change status to Active |
| `hello-healthsim/examples/patientsim-examples.md` | 4 | Add persist examples |
| `hello-healthsim/examples/membersim-examples.md` | 4 | Add persist examples |
| `hello-healthsim/examples/cross-domain-examples.md` | 4 | Add query examples |
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

#### Key Findings
- Existing `StateManager` class provides good foundation
- `packages/core/src/healthsim/db/` has connection, schema, queries
- Can extend existing infrastructure rather than create new
- 605 tests passing in core package as baseline

#### Next Session Focus
- Create Phase 1 super-prompt
- Begin implementation of persist_entities tool

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
- Use format: `[AutoPersist] Phase X: Brief description`
- Push at end of each session
- Tag major milestones: `auto-persist-phase-1`, etc.

---

*Last updated by Claude - December 26, 2024*
