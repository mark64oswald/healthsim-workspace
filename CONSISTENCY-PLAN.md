# HealthSim Product Consistency Plan

## Current State Analysis

### Package Structure Patterns

| Package | Structure | Status |
|---------|-----------|--------|
| core | `src/healthsim/` | ✅ Correct |
| membersim | `src/membersim/` | ✅ Correct |
| rxmembersim | `src/rxmembersim/` | ✅ Correct |
| patientsim | `src/patientsim/` + `src/core/` etc. | ⚠️ Has duplicate legacy structure |
| trialsim | `src/trialsim/` (empty) | ⚠️ Needs implementation |

### Terminology Consistency

| Item | PatientSim | MemberSim | RxMemberSim | TrialSim |
|------|------------|-----------|-------------|----------|
| Save/Load | `save_cohort` | `save_cohort` | `save_cohort` | TBD |
| List saved | `list_saved_cohorts` | `list_cohorts` | `list_cohorts` | TBD |
| Templates | `list_skills` | `list_journeys` | `list_journeys` | TBD |
| state_server | ⚠️ Uses "scenario" | ✅ Uses "cohort" | ✅ Uses "cohort" | TBD |

---

## Action Plan

### Phase 1: Fix PatientSim State Server (HIGH PRIORITY)
- [ ] Rename tools in state_server.py from `*_scenario` to `*_cohort`

### Phase 2: Remove PatientSim Legacy Structure
- [ ] Remove `packages/patientsim/src/core/` (duplicate of `src/patientsim/core/`)
- [ ] Remove `packages/patientsim/src/dimensional/`
- [ ] Remove `packages/patientsim/src/formats/`
- [ ] Remove `packages/patientsim/src/mcp/`
- [ ] Remove `packages/patientsim/src/validation/`
- [ ] Keep only `packages/patientsim/src/patientsim/`

### Phase 3: Implement TrialSim Package
Following the established pattern from MemberSim/RxMemberSim:

```
packages/trialsim/
├── src/trialsim/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── generator.py      # TrialSubjectGenerator
│   │   ├── models.py         # Subject, Visit, AE models
│   │   └── protocol.py       # Protocol definitions
│   ├── subjects/
│   │   ├── __init__.py
│   │   └── enrollment.py     # Enrollment logic
│   ├── visits/
│   │   ├── __init__.py
│   │   └── schedule.py       # Visit scheduling
│   ├── adverse_events/
│   │   ├── __init__.py
│   │   └── generator.py      # AE generation
│   ├── exposures/
│   │   ├── __init__.py
│   │   └── generator.py      # Exposure generation
│   ├── dimensional/
│   │   ├── __init__.py
│   │   └── transformer.py    # Dimensional model transforms
│   ├── formats/
│   │   ├── __init__.py
│   │   ├── export.py
│   │   └── sdtm/
│   │       ├── __init__.py
│   │       └── exporter.py   # SDTM export
│   ├── journeys/
│   │   ├── __init__.py
│   │   ├── compat.py         # Backward compatibility
│   │   ├── handlers.py       # Event handlers
│   │   └── templates.py      # Journey templates
│   ├── mcp/
│   │   ├── __init__.py
│   │   ├── server.py         # Main MCP server
│   │   ├── session.py        # Session management
│   │   └── state_server.py   # State persistence
│   └── validation/
│       ├── __init__.py
│       └── framework.py      # Validation logic
└── tests/
    ├── __init__.py
    ├── conftest.py
    ├── test_core.py
    ├── test_subjects.py
    ├── test_visits.py
    └── test_adverse_events.py
```

### Phase 4: Documentation Consistency
- [ ] Align README.md format across all packages
- [ ] Align CLAUDE.md format across all packages
- [ ] Fix or remove broken profile template links

### Phase 5: Database Migrations
- [ ] Update index names from idx_*_scenario to idx_*_cohort

---

## Execution Order

1. PatientSim state_server.py terminology fix
2. Remove PatientSim legacy src/ structure
3. Create TrialSim implementation
4. Update documentation
5. Database index names (lowest priority)
