# PatientSim

Synthetic patient data generation for clinical and EMR simulations.

## Overview

PatientSim is part of the HealthSim workspace, providing realistic synthetic patient data generation for healthcare simulation cohorts. It generates patients, encounters, diagnoses, and supports clinical data exchange formats.

## Features

- **Patient Demographics**: Realistic patient demographics with medical history
- **Clinical Encounters**: Inpatient, outpatient, and emergency encounters
- **Diagnoses & Conditions**: ICD-10 coded diagnoses with clinical context
- **Procedures**: CPT/HCPCS coded procedures and interventions
- **Observations**: Vital signs, lab results, and clinical observations
- **Medications**: Prescription and administration records
- **Clinical Documents**: C-CDA document generation
- **Multi-Format Export**: FHIR R4, HL7v2, C-CDA, MIMIC-III

## Installation

```bash
cd packages/patientsim
pip install -e ".[dev]"
```

## Quick Start

```python
from patientsim.core import PatientGenerator

# Generate patients
gen = PatientGenerator(seed=42)
patients = gen.generate_many(count=10)

# Generate with a clinical skill
patient = gen.generate(skill="icu_sepsis")
```

## Architecture

```
patientsim/
├── core/           # Patient, encounter, diagnosis models
├── skills/         # Clinical skill templates
├── formats/        # Export formats
│   ├── fhir/       # FHIR R4 resources
│   ├── hl7v2/      # HL7 v2.x messages
│   ├── ccda/       # C-CDA documents
│   └── mimic/      # MIMIC-III schema
├── dimensional/    # Star schema transforms
├── mcp/            # MCP servers for AI integration
│   ├── generation_server.py
│   ├── export_server.py
│   ├── validation_server.py
│   └── state_server.py
└── validation/     # Clinical validation
```

## Integration with Core

PatientSim uses the unified state management from `healthsim-core`:

```python
from healthsim.state import save_cohort, load_cohort

# Save generated patients
save_cohort(
    name="icu-sepsis-cohort",
    entities={"patients": patients, "encounters": encounters},
    tags=["icu", "sepsis", "critical-care"]
)
```

## Clinical Skills

PatientSim supports skill-based generation for common clinical cohorts:

```python
from patientsim.skills import get_skill, list_skills

# List available skills
skills = list_skills()

# Generate using a skill
patient = gen.generate(skill="diabetic_foot_ulcer")
```

## Format Export

```python
from patientsim.formats.fhir import FHIRTransformer
from patientsim.formats.hl7v2 import HL7v2Generator

# Export to FHIR
transformer = FHIRTransformer()
bundle = transformer.transform(patients)

# Export to HL7v2
generator = HL7v2Generator()
adt_message = generator.generate_adt(patient)
```

## Testing

```bash
cd packages/patientsim
pytest tests/ -v
```

## Related

- [HealthSim Core](../core/README.md) - Shared models and state management
- [PatientSim Skills](../../skills/patientsim/README.md) - AI conversation skills
- [MemberSim](../membersim/README.md) - Insurance claims generation
- [TrialSim](../trialsim/README.md) - Clinical trial data

## License

Apache 2.0
