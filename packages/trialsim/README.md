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
from trialsim import TrialSubjectGenerator, VisitGenerator, AdverseEventGenerator

# Generate trial subjects
subject_gen = TrialSubjectGenerator(seed=42)
subjects = subject_gen.generate_many(100, protocol_id="PROTO-001")

# Generate visits for a subject
visit_gen = VisitGenerator()
visits = visit_gen.generate_schedule(
    subject=subjects[0],
    duration_weeks=52
)

# Generate adverse events
ae_gen = AdverseEventGenerator()
aes = ae_gen.generate_for_subject(subjects[0], visit_count=len(visits))
```

## Architecture

```
trialsim/
├── core/           # Core models and generators
│   ├── models.py   # Subject, Visit, AdverseEvent, Exposure
│   ├── generator.py # TrialSubjectGenerator
│   ├── visits.py   # VisitGenerator
│   ├── adverse_events.py # AdverseEventGenerator
│   └── exposures.py # ExposureGenerator
├── formats/        # CDISC/SDTM export (planned)
│   └── sdtm/       # SDTM domain exporters
└── mcp/            # MCP server for AI integration
    ├── generation_server.py # Subject/visit generation tools
    ├── state_server.py      # Cohort save/load tools
    └── formatters.py        # Human-readable output formatting
```

## MCP Server Integration

TrialSim provides MCP (Model Context Protocol) servers for AI-assisted clinical trial data generation.

### Generation Server

The generation server exposes tools for creating trial data:

| Tool | Description |
|------|-------------|
| `generate_subject` | Generate a single trial subject |
| `generate_subject_cohort` | Generate multiple subjects for a protocol |
| `generate_visit_schedule` | Create visit schedule for a subject |
| `generate_adverse_events` | Generate adverse events |
| `generate_exposures` | Generate drug exposure records |
| `list_skills` | List available generation skills |
| `get_skill_details` | Get details about a specific skill |

### State Server

The state server provides workspace persistence:

| Tool | Description |
|------|-------------|
| `save_cohort` | Save workspace as a named cohort |
| `load_cohort` | Load a previously saved cohort |
| `list_saved_cohorts` | List saved cohorts with filtering |
| `delete_cohort` | Delete a saved cohort |
| `workspace_summary` | Get current workspace state |

### Running the MCP Servers

```bash
# Generation server
python -m trialsim.mcp.generation_server

# State server  
python -m trialsim.mcp.state_server
```

### Claude Desktop Configuration

Add to your Claude Desktop config:

```json
{
  "mcpServers": {
    "trialsim-generation": {
      "command": "python",
      "args": ["-m", "trialsim.mcp.generation_server"],
      "cwd": "/path/to/healthsim-workspace/packages/trialsim"
    },
    "trialsim-state": {
      "command": "python",
      "args": ["-m", "trialsim.mcp.state_server"],
      "cwd": "/path/to/healthsim-workspace/packages/trialsim"
    }
  }
}
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

## CDISC/SDTM Export (Planned)

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
- [MemberSim](../membersim/README.md) - Health plan member generation

## License

Apache 2.0
