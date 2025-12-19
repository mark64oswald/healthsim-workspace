# HealthSim Core

Shared Python foundation for the HealthSim product family.

## Overview

This package provides:
- **Person & Entity Models**: Base classes for patients, members, subjects
- **Benefits Processing**: Accumulator tracking, deductibles, OOP calculations
- **Dimensional Modeling**: Star schema transformers for analytics
- **State Management**: Session, workspace, and provenance tracking
- **Generation Utilities**: Faker-based realistic data generation
- **Format Transformations**: FHIR, X12, NCPDP converters

## Installation

```bash
cd packages/core
pip install -e ".[dev]"
```

## Usage

```python
from healthsim import Person, generate_person

# Generate a realistic person
person = generate_person()
print(person.model_dump_json(indent=2))
```

## Testing

```bash
pytest
```

## Related Packages

- `packages/patientsim/` - PatientSim MCP and utilities
- `packages/membersim/` - MemberSim MCP and utilities  
- `packages/rxmembersim/` - RxMemberSim MCP and utilities
