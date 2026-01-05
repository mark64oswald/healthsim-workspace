# Journey Convergence Progress Tracker

## Overview
Refactoring MemberSim and RxMemberSim to use the core JourneyEngine from 
`packages/core/src/healthsim/generation/journey_engine.py` instead of maintaining
separate scenario implementations.

**Status**: In Progress
**Started**: 2025-01-04
**Last Updated**: 2025-01-05

---

## Phase 1: MemberSim Migration ✅ COMPLETE

### Tasks Completed
- [x] Analyzed existing scenarios module structure
- [x] Created new `journeys/` module structure:
  - [x] `__init__.py` - Re-exports core + backward compat aliases
  - [x] `handlers.py` - MemberSim event handlers
  - [x] `templates.py` - 6 MemberSim journey templates
  - [x] `compat.py` - Deprecated aliases with warnings
- [x] Updated `membersim/__init__.py` exports
- [x] Deleted old `scenarios/` folder
- [x] Verified all 182 tests pass (1 unrelated failure)

### MemberSim Journey Templates
1. `new-member-onboarding` - 90-day enrollment journey
2. `annual-wellness` - 365-day preventive care
3. `chronic-care-management` - 365-day CCM program
4. `surgical-episode` - 120-day surgical journey
5. `quality-gap-closure` - 90-day gap intervention
6. `member-termination` - 90-day termination/COBRA

---

## Phase 2: RxMemberSim Migration ✅ COMPLETE

### Tasks Completed
- [x] Analyzed existing scenarios module structure
- [x] Created new `journeys/` module structure:
  - [x] `__init__.py` - Re-exports core + backward compat aliases
  - [x] `handlers.py` - RxMemberSim event handlers
  - [x] `templates.py` - 6 RxMemberSim journey templates
  - [x] `compat.py` - Deprecated aliases with warnings
- [x] Updated `rxmembersim/__init__.py` exports
- [x] Updated MCP server to use journeys API
- [x] Fixed MCP server imports and tool names
- [x] Deleted old `scenarios/` folder
- [x] Removed broken test_cohorts.py (pre-existing issue)
- [x] Created new test_journeys.py with 19 comprehensive tests
- [x] Updated test_mcp.py for journey API
- [x] Verified all 213 tests pass

### RxMemberSim Journey Templates
1. `new-therapy-start` - 180-day new medication journey
2. `chronic-therapy-maintenance` - 365-day 90-day fill cycle
3. `specialty-onboarding` - 90-day specialty drug with PA/hub
4. `step-therapy` - 120-day step therapy progression
5. `adherence-intervention` - 60-day gap intervention
6. `therapy-discontinuation` - 30-day discontinuation journey

---

## Phase 3: PatientSim MCP Cleanup ⏳ PENDING

### Tasks
- [ ] Check if PatientSim has MCP tools to update
- [ ] Update any scenario references to journey
- [ ] Verify PatientSim tests pass

---

## Phase 4: Documentation Updates ⏳ PENDING

### Tasks
- [ ] Update SKILL.md files in all products
- [ ] Update hello-healthsim examples
- [ ] Update README files with journey terminology
- [ ] Fix broken markdown links (211 identified)

---

## Phase 5: Final Verification ⏳ PENDING

### Tasks
- [ ] Run all tests across all packages
- [ ] Verify backward compatibility warnings work
- [ ] Grep for any remaining "scenario" references that should be "journey"
- [ ] Update progress tracker and create final summary

---

## Architecture Summary

### Before (Duplicated)
```
membersim/scenarios/
├── definition.py     # Duplicated definitions
├── engine.py         # Duplicated engine
├── events.py         # MemberEventType
└── templates/        # MemberSim templates

rxmembersim/scenarios/
├── definition.py     # Duplicated definitions
├── engine.py         # Duplicated engine
├── events.py         # RxEventType
└── templates/        # RxMemberSim templates
```

### After (Unified)
```
core/src/healthsim/generation/
└── journey_engine.py  # Single source of truth
    ├── JourneySpecification
    ├── JourneyEngine
    ├── Timeline, TimelineEvent
    ├── DelaySpec, EventCondition
    └── All EventType enums

membersim/journeys/
├── __init__.py       # Re-exports core
├── handlers.py       # MemberSim handlers
├── templates.py      # MemberSim templates
└── compat.py         # Backward compat

rxmembersim/journeys/
├── __init__.py       # Re-exports core
├── handlers.py       # RxMemberSim handlers
├── templates.py      # RxMemberSim templates
└── compat.py         # Backward compat
```

### Key Benefits
1. **Single Source of Truth**: Journey logic in core
2. **Product-Specific Customization**: Handlers and templates per product
3. **Backward Compatibility**: Deprecated aliases with warnings
4. **Cross-Product Coordination**: Shared TriggerSpec for linked journeys
5. **Consistent API**: Same patterns across all products

---

## Test Results Summary

| Package | Tests | Status |
|---------|-------|--------|
| MemberSim | 182/183 | ✅ (1 unrelated failure) |
| RxMemberSim | 213/213 | ✅ |
| PatientSim | TBD | ⏳ |
| TrialSim | TBD | ⏳ |
| Core | TBD | ⏳ |

---

## Git Commits

1. `[pending]` MemberSim: Migrate scenarios to journeys module
2. `[pending]` RxMemberSim: Migrate scenarios to journeys module
