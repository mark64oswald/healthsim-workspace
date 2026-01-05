# MemberSim

Synthetic insurance member data generation for payer and claims simulations.

## Overview

MemberSim is part of the HealthSim workspace, providing realistic synthetic member data generation for healthcare insurance simulation cohorts. It generates members, subscribers, claims, and supports X12 EDI transaction formats.

## Features

- **Member Enrollment**: Generate member demographics, eligibility periods, and coverage
- **Claims Generation**: Professional (837P) and facility (837I) claims with realistic coding
- **Payment Processing**: Remittance advice (835) with adjudication details
- **Eligibility Management**: 834 enrollment transactions and 270/271 eligibility inquiries
- **Prior Authorization**: 278 authorization request/response generation
- **Value-Based Care**: Capitation, attribution, and quality measure cohorts
- **Network Contracts**: Fee schedules and provider network management

## Installation

```bash
cd packages/membersim
pip install -e ".[dev]"
```

## Quick Start

```python
from membersim.core import MemberGenerator, ClaimGenerator

# Generate members
gen = MemberGenerator(seed=42)
members = gen.generate_many(count=10, plan_type="commercial")

# Generate claims for a member
claim_gen = ClaimGenerator()
claims = claim_gen.generate_for_member(members[0], claim_count=5)
```

## Architecture

```
membersim/
├── core/           # Member, subscriber, plan models
├── claims/         # Claim generation and payment
├── authorization/  # Prior authorization
├── formats/        # X12 EDI export (834, 835, 837, 270/271, 278)
├── network/        # Provider contracts and fee schedules
├── quality/        # HEDIS measures and care gaps
├── vbc/            # Value-based care arrangements
├── dimensional/    # Star schema transforms
├── journeys/       # Journey templates and handlers
├── mcp/            # MCP server for AI integration
└── validation/     # Claims validation
```

## Integration with Core

MemberSim uses the unified state management from `healthsim-core`:

```python
from healthsim.state import save_cohort, load_cohort

# Save generated members
save_cohort(
    name="commercial-members-q1",
    entities={"members": members, "claims": claims},
    tags=["commercial", "2025-q1"]
)
```

## X12 Export

```python
from membersim.formats.x12 import EDI837Generator

# Generate 837P claim file
generator = EDI837Generator()
edi_content = generator.generate(claims, claim_type="professional")
```

## Testing

```bash
cd packages/membersim
pytest tests/ -v
```

## Related

- [HealthSim Core](../core/README.md) - Shared models and state management
- [MemberSim Skills](../../skills/membersim/README.md) - AI conversation skills
- [PatientSim](../patientsim/README.md) - Clinical data generation

## License

Apache 2.0
