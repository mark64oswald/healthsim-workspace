# TrialSim

Synthetic clinical trial data generation for CDISC/SDTM formats.

## Overview

TrialSim generates realistic clinical trial data including:
- **Subjects**: Trial participants with demographics and eligibility
- **Protocol Visits**: Scheduled and unscheduled visit events
- **Adverse Events**: AE/SAE with severity, causality, and outcomes
- **Exposures**: Drug exposure records with dosing information
- **Lab Results**: Central and local laboratory data
- **Efficacy Data**: Response assessments and endpoints

## Installation

```bash
cd packages/trialsim
pip install -e ".[dev]"
```

## Quick Start

```python
from trialsim import TrialSubjectGenerator, ProtocolVisitGenerator

# Generate trial subjects
subject_gen = TrialSubjectGenerator(seed=42)
subjects = subject_gen.generate_many(100, protocol_id="PROTO-001")

# Generate visits for a subject
visit_gen = ProtocolVisitGenerator()
visits = visit_gen.generate_schedule(
    subject=subjects[0],
    protocol_phase="phase3",
    duration_weeks=52
)

# Generate adverse events
from trialsim import AdverseEventGenerator
ae_gen = AdverseEventGenerator()
aes = ae_gen.generate_for_subject(subjects[0], visit_count=len(visits))
```

## Architecture

```
trialsim/
├── core/           # Core models (Subject, Visit, AE)
├── protocol/       # Protocol definitions and schedules
├── subjects/       # Subject generation and enrollment
├── visits/         # Visit scheduling and events
├── adverse_events/ # AE/SAE generation
├── exposures/      # Drug exposure records
├── formats/        # CDISC/SDTM export
├── journeys/       # Journey integration with core
└── mcp/            # MCP server for AI integration
```

## Integration with Core

TrialSim uses the unified journey engine from `healthsim-core`:

```python
from healthsim.generation import JourneyEngine, get_journey_template

engine = JourneyEngine(seed=42)
journey = get_journey_template("phase3-pivotal-subject")

timeline = engine.create_timeline(
    entity=subject,
    entity_type="subject",
    journey=journey,
    start_date=date(2025, 1, 15),
)
```

## CDISC/SDTM Export

```python
from trialsim.formats import SDTMExporter

exporter = SDTMExporter()
datasets = exporter.export(
    subjects=subjects,
    visits=visits,
    adverse_events=aes,
    format="xpt"  # or "csv", "json"
)
```

## Related

- [HealthSim Core](../core/README.md) - Shared models and journey engine
- [PatientSim](../patientsim/README.md) - Clinical data generation
- [TrialSim Skills](../../skills/trialsim/README.md) - AI conversation skills

## License

Apache 2.0
