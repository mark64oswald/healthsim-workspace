# HealthSim Skills

A Skills-first synthetic healthcare data generation system. This repository replaces traditional Python libraries with Claude Skills - structured markdown documents that Claude uses to generate clinically coherent, realistic healthcare data.

## What is Skills-First Architecture?

Instead of code libraries, HealthSim Skills uses structured markdown documents that:

1. **Encode domain knowledge** - Medical codes, validation rules, data models
2. **Define generation patterns** - How to create realistic data with proper distributions
3. **Ensure consistency** - Cross-entity validation and temporal coherence
4. **Enable natural language requests** - Just describe what you need

Claude reads these Skills and uses them to generate data that is:
- Clinically coherent (diagnoses match medications match labs)
- Temporally consistent (no prescriptions before diagnosis)
- Properly formatted (valid codes, correct schemas)
- Reproducible (same seed = same output)

## Quick Start

### With Claude

1. Add this repository as a Claude Project or point Claude to the SKILL.md file
2. Make requests in natural language:

```
Generate 5 patients with Type 2 diabetes, including their quarterly A1C labs
and metformin prescriptions over the past year. Output as JSON.
```

```
Create insurance claims for a 3-day hospital stay with DRG payment.
Include professional and facility claims.
```

```
Generate pharmacy claims showing a brand-to-generic substitution
with prior authorization workflow.
```

## Repository Structure

```
healthsim-skills/
├── SKILL.md                      # Entry point - routing and overview
├── README.md                     # This file
│
├── references/                   # Domain knowledge (all scenarios use these)
│   ├── data-models.md           # Entity schemas (Patient, Claim, Rx, etc.)
│   ├── validation-rules.md      # Validation framework
│   ├── code-systems.md          # ICD-10, CPT, LOINC, medications
│   └── generation-patterns.md   # ID formats, distributions, seeds
│
├── scenarios/                    # Data generators
│   ├── patientsim/              # Clinical EHR data
│   │   └── SKILL.md
│   ├── membersim/               # Insurance claims
│   │   └── SKILL.md
│   └── rxmembersim/             # Pharmacy benefits
│       └── SKILL.md
│
├── formats/                      # Output transformers
│   ├── fhir-r4.md               # FHIR R4 Bundle format
│   ├── x12.md                   # X12 837/835 format
│   ├── ncpdp.md                 # NCPDP D.0 format
│   └── flat.md                  # CSV/flat file format
│
└── scripts/                      # Utility scripts
```

## Scenarios

### PatientSim - Clinical EHR Data
Generate patient records with:
- Demographics and identifiers
- Encounters (office visits, ED, inpatient)
- Diagnoses and procedures
- Lab results and vitals
- Medication history

### MemberSim - Insurance Claims
Generate insurance data with:
- Members and dependents
- Benefit plans and accumulators
- Professional and institutional claims
- Payment adjudication
- EOB/remittance

### RxMemberSim - Pharmacy Benefits
Generate pharmacy data with:
- Prescriptions and fills
- Pharmacy claims
- DUR (Drug Utilization Review)
- Prior authorization workflows
- Formulary management

## Output Formats

| Format | Use Case | Standards |
|--------|----------|-----------|
| JSON | Default, API integration | Custom schema |
| FHIR R4 | Interoperability | HL7 FHIR R4 |
| X12 | Claims submission | ANSI X12 837/835 |
| NCPDP | Pharmacy claims | NCPDP D.0 |
| CSV | Analytics, data warehouse | Flat files |

## Features

### Clinical Coherence
- Diagnoses appropriate for age and gender
- Medications have proper indications
- Lab values correlate with conditions
- Procedures match diagnoses

### Temporal Consistency
- No activity before birth or after death
- Prescriptions follow diagnoses
- Refills respect days supply
- Claims follow service dates

### Configurable Generation
- Control age distributions
- Specify conditions of interest
- Set complexity levels
- Include edge cases and errors

### Reproducibility
- Seed-based generation
- Same seed = identical output
- Batch generation support

## Example Output

### Patient with Diabetes (JSON)
```json
{
  "mrn": "MRN00001234",
  "name": {
    "family": "Johnson",
    "given": ["Robert", "James"]
  },
  "birth_date": "1965-03-15",
  "gender": "male",
  "diagnoses": [
    {
      "code": "E11.9",
      "display": "Type 2 diabetes without complications",
      "onset_date": "2020-06-15"
    }
  ],
  "medications": [
    {
      "medication": {
        "name": "Metformin",
        "rxnorm": "6809",
        "strength": "500mg"
      },
      "dosage": {
        "text": "Take 1 tablet by mouth twice daily",
        "frequency": "BID"
      }
    }
  ],
  "labs": [
    {
      "code": {"code": "4548-4", "display": "Hemoglobin A1c"},
      "value": {"value": 7.2, "unit": "%"},
      "effective_date": "2024-01-15"
    }
  ]
}
```

## Migration Context

This repository is part of a Skills-first migration from four Python libraries:
- `patientsim` - Clinical data generation
- `membersim` - Insurance claims generation
- `rxmembersim` - Pharmacy data generation
- `healthsim` - Shared utilities

The migration consolidates domain knowledge into Skills that Claude can use directly, eliminating the need for Python code execution.

## Session Progress

- [x] Session 1: Domain knowledge extraction
- [x] Session 2: Architecture design
- [x] Session 3: Core reference skills (this session)
- [ ] Session 4: PatientSim scenario skill
- [ ] Session 5: MemberSim scenario skill
- [ ] Session 6: RxMemberSim scenario skill
- [ ] Session 7: Output format skills
- [ ] Session 8: Integration and testing

## Contributing

This is a personal project for exploring Skills-first architecture. Feel free to fork and adapt for your own use.

## License

MIT

## Related

- [Claude Skills Documentation](https://docs.anthropic.com/)
- [HL7 FHIR R4](https://hl7.org/fhir/R4/)
- [X12 Standards](https://x12.org/)
- [NCPDP Standards](https://www.ncpdp.org/)
