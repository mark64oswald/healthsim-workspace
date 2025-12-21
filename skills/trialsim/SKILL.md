---
name: healthsim-trialsim
description: "Generate realistic clinical trial synthetic data including study definitions, sites, subjects, visits, adverse events, efficacy assessments, and disposition. Use when user requests: clinical trial data, CDISC/SDTM/ADaM datasets, trial scenarios (Phase I/II/III/IV), FDA submission test data, or specific therapeutic areas like oncology or biologics/CGT."
---

# TrialSim

**Status**: In Development

TrialSim generates realistic synthetic clinical trial data for testing, training, and development purposes.

## Overview

TrialSim provides:
- Complete study lifecycle data (protocol to closeout)
- Multi-site, multi-country trial configurations
- Subject-level longitudinal data with realistic patterns
- Safety data (adverse events, labs, vitals)
- Efficacy endpoints (primary, secondary, exploratory)
- CDISC-compliant output (SDTM, ADaM)

## Trigger Phrases

Activate TrialSim when user mentions:
- "clinical trial" or "clinical study"
- "Phase I/II/III/IV" or "pivotal trial"
- "CDISC", "SDTM", "ADaM"
- "FDA submission data" or "regulatory data"
- "adverse events" or "safety data"
- "efficacy endpoints"
- Trial therapeutic areas (oncology, cardiology, etc.)

## Quick Links

| Topic | Skill | Description |
|-------|-------|-------------|
| Domain Knowledge | [clinical-trials-domain.md](clinical-trials-domain.md) | Core trial concepts, phases, regulatory |
| Recruitment | [recruitment-enrollment.md](recruitment-enrollment.md) | Screening funnel, enrollment patterns |
| Phase 3 Trials | [phase3-pivotal.md](phase3-pivotal.md) | Pivotal registration trials |
| Oncology | [therapeutic-areas/oncology.md](therapeutic-areas/oncology.md) | Oncology-specific patterns |

## Output Formats

| Format | Skill | Use Case |
|--------|-------|----------|
| SDTM | [../../formats/cdisc-sdtm.md](../../formats/cdisc-sdtm.md) | Regulatory submission |
| ADaM | [../../formats/cdisc-adam.md](../../formats/cdisc-adam.md) | Statistical analysis |
| JSON | Default | API integration |
| CSV | [../../formats/csv.md](../../formats/csv.md) | Spreadsheet analysis |

## Core Entities

### Study
```json
{
  "study_id": "ABC-123-001",
  "protocol_title": "A Phase 3, Randomized, Double-Blind Study...",
  "phase": "Phase 3",
  "therapeutic_area": "Oncology",
  "indication": "Non-Small Cell Lung Cancer",
  "sponsor": "Example Pharma Inc.",
  "status": "Ongoing",
  "sites": [],
  "arms": []
}
```

### Subject
```json
{
  "subject_id": "001-0001",
  "site_id": "001",
  "screening_date": "2024-01-15",
  "randomization_date": "2024-01-22",
  "arm": "Treatment",
  "status": "Active",
  "demographics": {},
  "visits": [],
  "adverse_events": [],
  "efficacy_assessments": []
}
```

## Integration with Other Products

TrialSim integrates with other HealthSim products for complete clinical trial data:

| From | To | Integration Pattern |
|------|-----|---------------------|
| PatientSim | TrialSim | Patient → Subject (add consent, randomization, protocol visits) |
| NetworkSim | TrialSim | Provider → Investigator (add credentials, training, delegation log) |
| PopulationSim | TrialSim | Demographics → Recruitment pool (geographic, demographic eligibility) |

### Cross-Product: PatientSim

Trial subjects are patients with additional trial-specific data:

- [../patientsim/oncology/](../patientsim/oncology/) - Oncology trial subjects
- [../patientsim/heart-failure.md](../patientsim/heart-failure.md) - CV outcomes trial subjects
- [../patientsim/behavioral-health.md](../patientsim/behavioral-health.md) - CNS trial subjects
- [../patientsim/diabetes-management.md](../patientsim/diabetes-management.md) - Metabolic trial subjects

> **Integration Pattern:** Use PatientSim for baseline clinical characteristics. TrialSim adds protocol-specific assessments (RECIST, NYHA class changes), randomization, and SDTM-formatted data.

### Therapeutic Area Skills

| Area | PatientSim Skill | TrialSim Skill |
|------|------------------|----------------|
| Oncology | `oncology/*.md` | `therapeutic-areas/oncology.md` |
| Cardiovascular | `heart-failure.md` | `therapeutic-areas/cardiovascular.md` |
| CNS/Neurology | `behavioral-health.md` | `therapeutic-areas/cns.md` |

## Development Status

| Component | Status |
|-----------|--------|
| SKILL.md (this file) | ✅ Complete |
| clinical-trials-domain.md | 🔄 In Progress |
| recruitment-enrollment.md | 📋 Planned |
| phase3-pivotal.md | 🔄 In Progress |
| formats/cdisc-sdtm.md | 📋 Planned |
| formats/cdisc-adam.md | 📋 Planned |

## Related Skills

- [PatientSim](../patientsim/SKILL.md) - Clinical patient data
- [MemberSim](../membersim/SKILL.md) - Claims integration
- [Code Systems](../../references/code-systems.md) - Standard terminologies

## Usage Examples

### Example 1: Basic Phase 3 Trial

**Prompt:** "Generate a Phase 3 oncology trial with 200 subjects"

**Output:**
```json
{
  "study": {
    "study_id": "ONCO-2025-001",
    "protocol_title": "A Phase 3, Randomized, Double-Blind, Placebo-Controlled Study of ABC-123 in Advanced NSCLC",
    "phase": "Phase 3",
    "therapeutic_area": "Oncology",
    "indication": "Non-Small Cell Lung Cancer",
    "design": "Randomized, Double-Blind, Placebo-Controlled",
    "primary_endpoint": "Overall Survival",
    "target_enrollment": 200,
    "arms": [
      { "arm_id": "A", "name": "ABC-123 + SOC", "allocation_ratio": 1 },
      { "arm_id": "B", "name": "Placebo + SOC", "allocation_ratio": 1 }
    ]
  },
  "sites": [
    { "site_id": "001", "name": "Memorial Cancer Center", "country": "USA", "enrolled": 25 },
    { "site_id": "002", "name": "University Oncology", "country": "USA", "enrolled": 22 }
  ],
  "subjects": [
    {
      "subject_id": "001-0001",
      "site_id": "001",
      "arm": "A",
      "status": "Active",
      "randomization_date": "2025-01-15"
    }
  ]
}
```

### Example 2: Adverse Events

**Prompt:** "Generate adverse events for a 50-subject immunotherapy trial"

**Output:**
```json
{
  "adverse_events": [
    {
      "subject_id": "001-0023",
      "ae_term": "Fatigue",
      "meddra_pt": "Fatigue",
      "meddra_soc": "General disorders and administration site conditions",
      "severity": "Mild",
      "ctcae_grade": 1,
      "onset_date": "2025-02-10",
      "resolution_date": "2025-02-18",
      "relationship": "Possibly Related",
      "serious": false,
      "action_taken": "None"
    },
    {
      "subject_id": "001-0007",
      "ae_term": "Immune-mediated colitis",
      "meddra_pt": "Colitis",
      "meddra_soc": "Gastrointestinal disorders",
      "severity": "Severe",
      "ctcae_grade": 3,
      "onset_date": "2025-03-05",
      "resolution_date": null,
      "relationship": "Related",
      "serious": true,
      "action_taken": "Drug Interrupted"
    }
  ]
}
```

### Example 3: Screening and Enrollment

**Prompt:** "Generate screening data with 30% screen failure rate for 100 subjects"

**Output:**
```json
{
  "screening_summary": {
    "total_screened": 143,
    "screen_passed": 100,
    "screen_failed": 43,
    "screen_failure_rate": 0.30
  },
  "screen_failures": [
    {
      "screening_id": "SCR-0015",
      "failure_reason": "Inclusion criteria not met",
      "failure_detail": "EGFR mutation negative",
      "screening_date": "2025-01-20"
    },
    {
      "screening_id": "SCR-0028",
      "failure_reason": "Exclusion criteria met",
      "failure_detail": "Prior immunotherapy within 6 months",
      "screening_date": "2025-01-25"
    }
  ],
  "enrolled_subjects": [
    {
      "subject_id": "001-0001",
      "screening_id": "SCR-0001",
      "consent_date": "2025-01-10",
      "screening_date": "2025-01-12",
      "randomization_date": "2025-01-22"
    }
  ]
}
```

### Example 4: SDTM Output

**Prompt:** "Generate DM domain for 10 subjects as SDTM"

**Output:**
```json
{
  "domain": "DM",
  "records": [
    {
      "STUDYID": "ONCO-2025-001",
      "DOMAIN": "DM",
      "USUBJID": "ONCO-2025-001-001-0001",
      "SUBJID": "001-0001",
      "SITEID": "001",
      "RFSTDTC": "2025-01-22",
      "RFENDTC": null,
      "BRTHDTC": "1958-05-15",
      "AGE": 66,
      "AGEU": "YEARS",
      "SEX": "M",
      "RACE": "WHITE",
      "ETHNIC": "NOT HISPANIC OR LATINO",
      "ARMCD": "A",
      "ARM": "ABC-123 + SOC",
      "COUNTRY": "USA"
    }
  ]
}
```
