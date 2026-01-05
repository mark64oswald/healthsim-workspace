# Generative Framework Implementation Plan

**Created**: 2026-01-05
**Status**: In Progress

---

## Overview

This plan addresses two tracks:
1. **Product Consistency** - Complete remaining consistency items across all products
2. **Generative Framework Gaps** - Close gaps between design documents and implementation

---

## Track 1: Product Consistency (3 Items)

### 1.1 Database Index Names
**Status**: ✅ Complete
**Effort**: Small

Rename scenario-based index names to cohort-based:
- [x] Audit `packages/core/src/healthsim/state/migrations.py` for `idx_*_scenario` patterns
- [x] Added migration 1.6 to drop legacy idx_*_scenario indexes
- [x] Verify no breaking changes
- [x] Run state management tests (295 passed)

### 1.2 MemberSim/RxMemberSim MCP Audit
**Status**: ✅ Complete
**Effort**: Small-Medium

Check for remaining "scenario" terminology in MCP layers:
- [x] Audit `packages/membersim/src/membersim/mcp/` for scenario references
- [x] Audit `packages/rxmembersim/src/rxmembersim/mcp/` for scenario references
- [x] Update user-facing messages to use "cohort/skill" terminology
- [x] Run MemberSim tests (183 passed)
- [x] Run RxMemberSim tests (213 passed)

### 1.3 TrialSim MCP Server
**Status**: ✅ Complete
**Effort**: Medium

Add MCP server integration to TrialSim following PatientSim pattern:
- [x] Create `packages/trialsim/src/trialsim/mcp/generation_server.py`
- [x] Create `packages/trialsim/src/trialsim/mcp/state_server.py`
- [x] Create `packages/trialsim/src/trialsim/mcp/formatters.py`
- [x] Add MCP tools: generate_subject, generate_visit_schedule, generate_adverse_events
- [x] Add state tools: save_cohort, load_cohort, list_saved_cohorts
- [x] Create tests for MCP layer (33 passed)
- [x] Update TrialSim README with MCP documentation

---

## Track 2: Generative Framework Gaps

### 2.1 Cross-Product Integration
**Status**: ⬜ Not Started
**Effort**: Medium-Large

Connect generation across product domains:
- [ ] Implement `CrossDomainSync` class in core
- [ ] Add identity correlation (same person across MemberSim/PatientSim/RxMemberSim)
- [ ] Add event triggers (enrollment triggers eligibility, claim triggers encounter)
- [ ] Create cross-domain journey templates
- [ ] Add integration tests

### 2.2 MCP Tools for Profile Management
**Status**: ⬜ Not Started
**Effort**: Medium

Add MCP tools to manage profiles and journeys:
- [ ] Create `packages/core/src/healthsim/mcp/profile_server.py`
- [ ] Add tools: build_profile, save_profile, load_profile, list_profiles
- [ ] Add tools: build_journey, save_journey, load_journey, list_journeys
- [ ] Add tools: execute_profile, execute_journey
- [ ] Create tests for profile MCP layer

### 2.3 Journey Validation Framework
**Status**: ⬜ Not Started
**Effort**: Small-Medium

Enhance journey execution validation:
- [ ] Add journey specification validation (before execution)
- [ ] Add timeline validation (after execution)
- [ ] Add cross-event consistency checks
- [ ] Create validation report format

### 2.4 TrialSim SDTM Export
**Status**: ⬜ Not Started
**Effort**: Medium

Implement CDISC SDTM format export for TrialSim:
- [ ] Create `packages/trialsim/src/trialsim/formats/sdtm/exporter.py`
- [ ] Implement DM (Demographics) domain
- [ ] Implement AE (Adverse Events) domain
- [ ] Implement EX (Exposure) domain
- [ ] Implement VS (Vital Signs) domain
- [ ] Add SDTM validation
- [ ] Create tests for SDTM export

### 2.5 PopulationSim Reference Data Integration
**Status**: ⬜ Not Started
**Effort**: Medium

Connect PopulationSim reference data to generation framework:
- [ ] Audit existing PopulationSim DuckDB schema
- [ ] Create reference data adapters for generation
- [ ] Add geographic distribution queries
- [ ] Add disease prevalence queries
- [ ] Integrate with ProfileExecutor

---

## Execution Order

| Phase | Items | Estimated Sessions |
|-------|-------|-------------------|
| **Phase A** | 1.1, 1.2, 1.3 | 1-2 sessions |
| **Phase B** | 2.2 (MCP Tools) | 1-2 sessions |
| **Phase C** | 2.1 (Cross-Product) | 2-3 sessions |
| **Phase D** | 2.3, 2.4, 2.5 | 2-3 sessions |

---

## Progress Tracking

### Session Log

| Date | Items Completed | Tests Status | Commits |
|------|-----------------|--------------|---------|
| 2026-01-05 | TrialSim core implementation, PatientSim cleanup, README standardization | 1,760 passing | 3 commits |
| 2026-01-05 | Track 1: 1.1 DB indexes, 1.2 MCP audit, 1.3 TrialSim MCP | 1,777 passing | 1 commit |
| | | | |

---

## Dependencies

- Track 1 items are independent and can proceed in any order
- Track 2.2 (MCP Tools) should precede 2.1 (Cross-Product) 
- Track 2.4 (SDTM) depends on 1.3 (TrialSim MCP)
- Track 2.5 (PopulationSim) is independent

---

## Definition of Done

Each item is complete when:
1. ✅ Code implemented
2. ✅ Tests passing
3. ✅ Documentation updated
4. ✅ Changes committed and pushed
5. ✅ Plan updated with status

---

*End of Plan*
