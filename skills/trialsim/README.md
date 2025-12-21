# TrialSim Skills

Clinical trial synthetic data generation skills for HealthSim.

## Directory Structure

```
skills/trialsim/
├── README.md                          # This file
├── SKILL.md                           # Product router
├── clinical-trials-domain.md          # Core domain knowledge
├── recruitment-enrollment.md          # Recruitment funnel
│
├── phase1-dose-escalation.md          # Phase I scenarios (planned)
├── phase2-proof-of-concept.md         # Phase II scenarios (planned)
├── phase3-pivotal.md                  # Phase III scenarios
├── phase4-postmarket.md               # Phase IV scenarios (planned)
├── adaptive-design.md                 # Adaptive trial designs (planned)
├── rare-disease.md                    # Small population trials (planned)
│
├── domains/                           # SDTM Domain Skills
│   ├── README.md                      # Domain index, SDTM overview
│   ├── demographics-dm.md             # DM - Subject demographics
│   ├── adverse-events-ae.md           # AE - Adverse events (MedDRA)
│   ├── vital-signs-vs.md              # VS - Vital sign measurements
│   ├── laboratory-lb.md               # LB - Laboratory results (LOINC)
│   ├── concomitant-meds-cm.md         # CM - Concomitant medications (ATC)
│   ├── exposure-ex.md                 # EX - Study drug exposure (planned)
│   ├── disposition-ds.md              # DS - Subject disposition (planned)
│   └── medical-history-mh.md          # MH - Medical history (planned)
│
├── therapeutic-areas/                 # Indication-specific skills
│   ├── README.md                      # Therapeutic area index
│   ├── oncology.md                    # Solid tumors, RECIST
│   ├── cardiovascular.md              # MACE, CV outcomes
│   ├── cns.md                         # Neurological endpoints
│   └── cgt.md                         # Cell & Gene Therapy
│
└── rwe/                               # Real World Evidence
    ├── README.md                      # RWE concepts index
    ├── overview.md                    # RWE fundamentals
    └── synthetic-control.md           # External control generation
```

**Note:** TrialSim uses subdirectories for complex, related skill groups (domains, therapeutic areas, RWE). This matches PatientSim's pattern with `oncology/` and `pediatrics/` subdirectories.

## Quick Reference

| I want to generate... | Skill | Key Triggers |
|-----------------------|-------|--------------|
| Subject demographics (DM) | `domains/demographics-dm.md` | "demographics", "DM domain", "USUBJID" |
| Adverse events (AE) | `domains/adverse-events-ae.md` | "adverse events", "AE domain", "MedDRA", "SAE" |
| Vital signs (VS) | `domains/vital-signs-vs.md` | "vital signs", "VS domain", "blood pressure" |
| Laboratory results (LB) | `domains/laboratory-lb.md` | "lab results", "LB domain", "chemistry", "LOINC" |
| Concomitant meds (CM) | `domains/concomitant-meds-cm.md` | "concomitant meds", "CM domain", "ATC" |
| A Phase III pivotal trial | `phase3-pivotal.md` | "Phase 3", "pivotal", "registrational" |
| An oncology trial | `therapeutic-areas/oncology.md` | "oncology", "cancer", "RECIST", "ORR" |
| A cardiovascular trial | `therapeutic-areas/cardiovascular.md` | "cardiovascular", "MACE", "heart failure" |
| A CNS/neurology trial | `therapeutic-areas/cns.md` | "CNS", "neurology", "Alzheimer's", "Parkinson's" |
| A cell/gene therapy trial | `therapeutic-areas/cgt.md` | "gene therapy", "CAR-T", "CGT" |
| Recruitment/screening data | `recruitment-enrollment.md` | "screening", "enrollment", "screen failure" |
| External control arm | `rwe/synthetic-control.md` | "synthetic control", "external control", "RWE" |

## Implementation Status

### Core Skills

| Skill | Status | Notes |
|-------|--------|-------|
| clinical-trials-domain.md | ✅ Complete | Core domain knowledge |
| phase3-pivotal.md | ✅ Complete | Comprehensive Phase III |
| recruitment-enrollment.md | ✅ Complete | Screening funnel, I/E |

### SDTM Domain Skills

| Domain | Skill | Status | Notes |
|--------|-------|--------|-------|
| DM | domains/demographics-dm.md | ✅ Complete | Required for all studies |
| AE | domains/adverse-events-ae.md | ✅ Complete | MedDRA coding, SAE flags |
| VS | domains/vital-signs-vs.md | ✅ Complete | BP, HR, temp, weight |
| LB | domains/laboratory-lb.md | ✅ Complete | LOINC coding, ref ranges |
| CM | domains/concomitant-meds-cm.md | ✅ Complete | ATC classification |
| EX | domains/exposure-ex.md | 📋 Planned | Study drug exposure |
| DS | domains/disposition-ds.md | 📋 Planned | Subject disposition |
| MH | domains/medical-history-mh.md | 📋 Planned | Medical history |

### Therapeutic Area Skills

| Skill | Status | Notes |
|-------|--------|-------|
| therapeutic-areas/oncology.md | ✅ Complete | RECIST, survival |
| therapeutic-areas/cardiovascular.md | ✅ Complete | MACE, HF |
| therapeutic-areas/cns.md | ✅ Complete | Cognitive, imaging |
| therapeutic-areas/cgt.md | ✅ Complete | CAR-T, gene therapy |

### RWE Skills

| Skill | Status | Notes |
|-------|--------|-------|
| rwe/overview.md | ✅ Complete | RWE concepts |
| rwe/synthetic-control.md | ✅ Complete | External controls |

### Planned Skills

| Skill | Phase | Notes |
|-------|-------|-------|
| phase1-dose-escalation.md | Phase 2 | 3+3 design, MTD |
| phase2-proof-of-concept.md | Phase 2 | Dose ranging, futility |
| phase4-postmarket.md | Phase 3 | Safety surveillance |
| adaptive-design.md | Phase 3 | Adaptive randomization |
| rare-disease.md | Phase 3 | Small populations |

## Development Roadmap

See [TrialSim Development Plan](../../docs/TRIALSIM-DEVELOPMENT-PLAN.md) for complete roadmap.

**Phase 1 (Foundation):** Domain knowledge, Phase 3 pivotal ✅  
**Phase 2 (SDTM Domains):** Core domain skills (DM, AE, VS, LB, CM) ✅  
**Phase 3 (Expanded Domains):** EX, DS, MH + additional trial phases  
**Phase 4 (Advanced):** Adaptive designs, rare disease, platform trials

## Related Documentation

- [HealthSim Architecture Guide](../../docs/HEALTHSIM-ARCHITECTURE-GUIDE.md)
- [Hello HealthSim Examples](../../hello-healthsim/examples/)
- [CDISC SDTM Format](../../formats/cdisc-sdtm.md)
- [Domain Skills Index](domains/README.md)
