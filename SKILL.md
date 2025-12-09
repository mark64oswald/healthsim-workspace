---
name: HealthSim Skills
description: Skills-first synthetic healthcare data generation system. Generates realistic patient records, insurance claims, and pharmacy data for testing healthcare applications.
---

# HealthSim Skills

A comprehensive synthetic healthcare data generation system built as Claude Skills.

## Quick Start

Tell me what you need:

- **"Generate 5 patients with diabetes"** → PatientSim scenario
- **"Create insurance claims for a hospital stay"** → MemberSim scenario
- **"Generate pharmacy claims with prior auth"** → RxMemberSim scenario
- **"I need FHIR R4 output"** → Any scenario with format specification

## Skill Navigation

### Reference Skills (Foundational Knowledge)

These skills contain domain knowledge used by all scenario skills:

| Reference | Purpose | Use When |
|-----------|---------|----------|
| [data-models.md](references/data-models.md) | Entity schemas (Patient, Claim, Prescription) | Need field definitions, types, constraints |
| [validation-rules.md](references/validation-rules.md) | Validation framework | Checking data coherence, clinical validity |
| [code-systems.md](references/code-systems.md) | ICD-10, CPT, LOINC, NDC codes | Need realistic medical codes |
| [generation-patterns.md](references/generation-patterns.md) | ID formats, distributions, seeds | Controlling randomization |

### Scenario Skills (Data Generators)

Each scenario skill generates a specific type of healthcare data:

| Scenario | Domain | Primary Output |
|----------|--------|----------------|
| [patientsim/](scenarios/patientsim/) | Clinical EHR | Patients, encounters, diagnoses, labs, vitals |
| [membersim/](scenarios/membersim/) | Insurance Claims | Members, claims, payments, accumulators |
| [rxmembersim/](scenarios/rxmembersim/) | Pharmacy Benefits | Prescriptions, pharmacy claims, formulary |

### Output Formats

| Format | File | Use Case |
|--------|------|----------|
| FHIR R4 | [formats/fhir-r4.md](formats/fhir-r4.md) | Interoperability, EHR integration |
| X12 837/835 | [formats/x12.md](formats/x12.md) | Claims submission/remittance |
| NCPDP | [formats/ncpdp.md](formats/ncpdp.md) | Pharmacy claims |
| Flat Files | [formats/flat.md](formats/flat.md) | Data warehouse, analytics |

## Request Routing

Based on your request, I'll route to the appropriate skill:

```
Patient/clinical data → scenarios/patientsim/
Insurance claims     → scenarios/membersim/
Pharmacy/Rx data     → scenarios/rxmembersim/
Code lookups         → references/code-systems.md
Schema questions     → references/data-models.md
```

## Common Parameters

All generation requests support these parameters:

| Parameter | Description | Default |
|-----------|-------------|---------|
| `count` | Number of records to generate | 1 |
| `seed` | Random seed for reproducibility | None (random) |
| `format` | Output format (json, fhir, x12, csv) | json |
| `include_related` | Generate related records | true |

## Example Requests

### Simple Patient Generation
```
Generate 3 patients aged 40-60 with hypertension
```

### Complex Clinical Scenario
```
Generate a diabetic patient with:
- 2 years of quarterly visits
- A1C labs trending from 8.5 to 7.0
- Metformin prescription with refills
- Output as FHIR R4 Bundle
```

### Insurance Claims Scenario
```
Generate insurance claims for:
- Member with family plan
- Hospital admission (3 days)
- Include professional and facility claims
- Show payment adjudication
```

### Pharmacy Scenario
```
Generate pharmacy claims showing:
- Brand drug requiring prior auth
- Initial rejection and approval
- 90-day mail order fill
```

## Architecture

```
SKILL.md (this file - entry point)
├── references/           # Domain knowledge
│   ├── data-models.md   # Entity schemas
│   ├── validation-rules.md
│   ├── code-systems.md
│   └── generation-patterns.md
├── scenarios/           # Data generators
│   ├── patientsim/     # Clinical data
│   ├── membersim/      # Insurance claims
│   └── rxmembersim/    # Pharmacy
└── formats/            # Output transformers
    ├── fhir-r4.md
    ├── x12.md
    └── ncpdp.md
```

## Principles

1. **Clinically Coherent**: Generated data maintains medical logic (diagnoses match procedures, labs support diagnoses)
2. **Temporally Consistent**: Timelines make sense (no prescriptions before diagnosis)
3. **Configurable Realism**: Control complexity, edge cases, and error scenarios
4. **Reproducible**: Same seed produces identical output
5. **Format Flexible**: Generate once, output in any format
