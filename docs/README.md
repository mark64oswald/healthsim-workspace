# HealthSim Documentation Hub

The complete guide to generating realistic synthetic healthcare data with HealthSim.

---

## The HealthSim Ecosystem

HealthSim is a suite of products for generating synthetic healthcare data through natural conversation with Claude. Here's how everything fits together:

```text
                              HealthSim Ecosystem
    ┌─────────────────────────────────────────────────────────────────┐
    │                                                                 │
    │   ┌─────────────────────────────────────────────────────────┐   │
    │   │              healthsim-common (Skills)               │   │
    │   │   Scenarios, Formats, References, Documentation         │   │
    │   └─────────────────────────────────────────────────────────┘   │
    │                              │                                  │
    │              ┌───────────────┼───────────────┐                  │
    │              ▼               ▼               ▼                  │
    │   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
    │   │  PatientSim  │  │  MemberSim   │  │ RxMemberSim  │          │
    │   │   Clinical   │  │    Claims    │  │   Pharmacy   │          │
    │   │     Data     │  │     Data     │  │     Data     │          │
    │   └──────────────┘  └──────────────┘  └──────────────┘          │
    │              │               │               │                  │
    │              └───────────────┼───────────────┘                  │
    │                              ▼                                  │
    │   ┌─────────────────────────────────────────────────────────┐   │
    │   │                   healthsim-common                        │   │
    │   │   Shared Models, Validation, State, Generation          │   │
    │   └─────────────────────────────────────────────────────────┘   │
    │                                                                 │
    └─────────────────────────────────────────────────────────────────┘
```

---

## Repository Overview

| Repository | Purpose | GitHub | Key Contents |
|------------|---------|--------|--------------|
| **[healthsim-common](https://github.com/mark64oswald/healthsim-common)** | Skills & shared docs | [repo](https://github.com/mark64oswald/healthsim-common) | Scenarios, formats, references, SKILL.md files |
| **[healthsim-common](https://github.com/mark64oswald/healthsim-common)** | Shared Python library | [repo](https://github.com/mark64oswald/healthsim-common) | Models, validation, state management, generation |
| **[PatientSim](https://github.com/mark64oswald/PatientSim)** | Clinical/EMR data | [repo](https://github.com/mark64oswald/PatientSim) | Patients, encounters, diagnoses, labs, vitals |
| **[MemberSim](https://github.com/mark64oswald/membersim)** | Claims/payer data | [repo](https://github.com/mark64oswald/membersim) | Members, claims, benefits, prior auth |
| **[RxMemberSim](https://github.com/mark64oswald/rxmembersim)** | Pharmacy/PBM data | [repo](https://github.com/mark64oswald/rxmembersim) | Prescriptions, formularies, DUR alerts |
| **[healthsim-hello](https://github.com/mark64oswald/healthsim-hello)** | Demo & examples | [repo](https://github.com/mark64oswald/healthsim-hello) | Sample integrations, test harness |

---

## Quick Start

**New to HealthSim? Start here:**

| Step | Resource | Time |
|------|----------|------|
| 1. Setup | [hello-healthsim/README.md](../hello-healthsim/README.md) | 5 min |
| 2. First generation | [hello-healthsim/examples/](../hello-healthsim/examples/) | 10 min |
| 3. Understand Skills | [SKILL.md](../SKILL.md) | 15 min |
| 4. Explore skills | [skills/](../skills/) | As needed |

---

## Documentation by Topic

### Getting Started

| Document | Description | Audience |
|----------|-------------|----------|
| [hello-healthsim/README.md](../hello-healthsim/README.md) | Quick start guide | Everyone |
| [hello-healthsim/CLAUDE-DESKTOP.md](../hello-healthsim/CLAUDE-DESKTOP.md) | Claude Desktop setup | Desktop users |
| [hello-healthsim/CLAUDE-CODE.md](../hello-healthsim/CLAUDE-CODE.md) | Claude Code CLI setup | Developers |
| [hello-healthsim/TROUBLESHOOTING.md](../hello-healthsim/TROUBLESHOOTING.md) | Common issues & fixes | Everyone |
| [hello-healthsim/EXTENDING.md](../hello-healthsim/EXTENDING.md) | How to extend HealthSim | Developers |

### Skills & Scenarios

| Document | Description |
|----------|-------------|
| [SKILL.md](../SKILL.md) | Master skill file (start here) |
| [skills/patientsim/](../skills/patientsim/) | Clinical scenarios (diabetes, heart failure, oncology, etc.) |
| [skills/membersim/](../skills/membersim/) | Claims scenarios (professional, facility, behavioral health) |
| [skills/rxmembersim/](../skills/rxmembersim/) | Pharmacy scenarios (retail, specialty, DUR) |
| [skills/creating-skills.md](skills/creating-skills.md) | How to create new skills |
| [skills/format-specification-v2.md](skills/format-specification-v2.md) | Skills format specification |

### Output Formats

| Document | Formats Covered |
|----------|-----------------|
| [formats/fhir-r4.md](../formats/fhir-r4.md) | FHIR R4, NDJSON, Bulk Export |
| [formats/hl7v2-adt.md](../formats/hl7v2-adt.md) | HL7v2 ADT messages |
| [formats/hl7v2-orm.md](../formats/hl7v2-orm.md) | HL7v2 ORM orders |
| [formats/hl7v2-oru.md](../formats/hl7v2-oru.md) | HL7v2 ORU results |
| [formats/x12-837.md](../formats/x12-837.md) | X12 837 claims |
| [formats/x12-835.md](../formats/x12-835.md) | X12 835 remittance |
| [formats/x12-834.md](../formats/x12-834.md) | X12 834 enrollment |
| [formats/x12-270-271.md](../formats/x12-270-271.md) | X12 270/271 eligibility |
| [formats/ncpdp-d0.md](../formats/ncpdp-d0.md) | NCPDP D.0 pharmacy |
| [formats/ccda-format.md](../formats/ccda-format.md) | C-CDA clinical documents |
| [formats/csv.md](../formats/csv.md) | CSV tabular export |
| [formats/sql.md](../formats/sql.md) | SQL database loading |
| [formats/dimensional-analytics.md](../formats/dimensional-analytics.md) | Star schema for analytics |

### Reference Data

| Document | Description |
|----------|-------------|
| [references/data-models.md](../references/data-models.md) | Entity schemas and relationships |
| [references/code-systems.md](../references/code-systems.md) | ICD-10, CPT, LOINC, NDC, RxNorm |
| [references/clinical-rules.md](../references/clinical-rules.md) | Clinical business rules |
| [references/clinical-domain.md](../references/clinical-domain.md) | Domain knowledge |
| [references/oncology/](../references/oncology/) | Oncology-specific reference data |

### MCP Integration

| Document | Description |
|----------|-------------|
| [mcp/integration-guide.md](mcp/integration-guide.md) | Complete MCP integration guide |
| [mcp/development-guide.md](mcp/development-guide.md) | Developing MCP servers |
| [mcp/configuration.md](mcp/configuration.md) | MCP server configuration |

### State Management

| Document | Description |
|----------|-------------|
| [state-management/user-guide.md](state-management/user-guide.md) | Save/load scenarios and sessions |
| [state-management/specification.md](state-management/specification.md) | Technical specification |

### Extension Framework

| Document | Description |
|----------|-------------|
| [extensions/philosophy.md](extensions/philosophy.md) | Conversation-first philosophy |
| [extensions/mcp-tools.md](extensions/mcp-tools.md) | Adding MCP tools (actions) |
| [extensions/skills.md](extensions/skills.md) | Adding skills (knowledge) |
| [extensions/slash-commands.md](extensions/slash-commands.md) | Adding slash commands |
| [extensions/quick-reference.md](extensions/quick-reference.md) | Single-page quick reference |

### Architecture

| Document | Description |
|----------|-------------|
| [architecture/layered-pattern.md](architecture/layered-pattern.md) | Layered architecture overview |
| [architecture/healthsim-common-spec.md](architecture/healthsim-common-spec.md) | healthsim-common specification |
| [healthsim-common-architecture.md](healthsim-common-architecture.md) | Skills architecture |

### Contributing

| Document | Description |
|----------|-------------|
| [contributing.md](contributing.md) | Contribution guidelines |
| [testing-patterns.md](testing-patterns.md) | Testing patterns and standards |

---

## Documentation by Product

### PatientSim (Clinical Data)

| Location | Contents |
|----------|----------|
| [skills/patientsim/SKILL.md](../skills/patientsim/SKILL.md) | PatientSim skill overview |
| [PatientSim/docs/](https://github.com/mark64oswald/PatientSim/tree/main/docs) | Product documentation |
| [PatientSim/docs/user-guide/](https://github.com/mark64oswald/PatientSim/tree/main/docs/user-guide) | User guides |
| [PatientSim/docs/tutorials/](https://github.com/mark64oswald/PatientSim/tree/main/docs/tutorials) | Step-by-step tutorials |
| [PatientSim/docs/developer-guide/](https://github.com/mark64oswald/PatientSim/tree/main/docs/developer-guide) | Developer documentation |
| [PatientSim/docs/reference/](https://github.com/mark64oswald/PatientSim/tree/main/docs/reference) | API and schema reference |

### MemberSim (Claims Data)

| Location | Contents |
|----------|----------|
| [skills/membersim/SKILL.md](../skills/membersim/SKILL.md) | MemberSim skill overview |
| [MemberSim/docs/](https://github.com/mark64oswald/membersim/tree/main/docs) | Product documentation |
| [MemberSim/docs/user-guide/](https://github.com/mark64oswald/membersim/tree/main/docs/user-guide) | User guides |
| [MemberSim/docs/tutorials/](https://github.com/mark64oswald/membersim/tree/main/docs/tutorials) | Step-by-step tutorials |
| [MemberSim/docs/reference/](https://github.com/mark64oswald/membersim/tree/main/docs/reference) | API and schema reference |

### RxMemberSim (Pharmacy Data)

| Location | Contents |
|----------|----------|
| [skills/rxmembersim/SKILL.md](../skills/rxmembersim/SKILL.md) | RxMemberSim skill overview |
| [RxMemberSim/docs/](https://github.com/mark64oswald/rxmembersim/tree/main/docs) | Product documentation |
| [RxMemberSim/docs/user-guide/](https://github.com/mark64oswald/rxmembersim/tree/main/docs/user-guide) | User guides |
| [RxMemberSim/docs/tutorials/](https://github.com/mark64oswald/rxmembersim/tree/main/docs/tutorials) | Step-by-step tutorials |
| [RxMemberSim/docs/reference/](https://github.com/mark64oswald/rxmembersim/tree/main/docs/reference) | API and schema reference |

### healthsim-common (Shared Library)

| Location | Contents |
|----------|----------|
| [healthsim-common/docs/](https://github.com/mark64oswald/healthsim-common/tree/main/docs) | Core library documentation |
| [architecture/healthsim-common-spec.md](architecture/healthsim-common-spec.md) | Technical specification |

---

## Examples by Use Case

| I want to... | Example | Format |
|--------------|---------|--------|
| Generate a patient | [patientsim-examples.md](../hello-healthsim/examples/patientsim-examples.md) | JSON, FHIR |
| Generate a claim | [membersim-examples.md](../hello-healthsim/examples/membersim-examples.md) | JSON, X12 |
| Generate pharmacy data | [rxmembersim-examples.md](../hello-healthsim/examples/rxmembersim-examples.md) | JSON, NCPDP |
| Generate oncology data | [oncology-examples.md](../hello-healthsim/examples/oncology-examples.md) | JSON, FHIR |
| Generate cross-domain data | [cross-domain-examples.md](../hello-healthsim/examples/cross-domain-examples.md) | Multiple |
| Output in specific format | [format-examples.md](../hello-healthsim/examples/format-examples.md) | All formats |

---

## Navigation by Role

### For Users (generating data)

1. [Quick Start](../hello-healthsim/README.md) - Get set up
2. [SKILL.md](../SKILL.md) - Understand what you can generate
3. [Examples](../hello-healthsim/examples/) - Copy-paste prompts
4. [Troubleshooting](../hello-healthsim/TROUBLESHOOTING.md) - Fix issues

### For Developers (extending HealthSim)

1. [Extension Philosophy](extensions/philosophy.md) - Understand the approach
2. [Creating Skills](skills/creating-skills.md) - Add new scenarios
3. [MCP Tools](extensions/mcp-tools.md) - Add new actions
4. [Contributing](contributing.md) - Submit changes

### For Architects (understanding the system)

1. [Layered Architecture](architecture/layered-pattern.md) - System design
2. [healthsim-common Spec](architecture/healthsim-common-spec.md) - Core library
3. [Skills Architecture](healthsim-common-architecture.md) - Skills system
4. [Data Models](../references/data-models.md) - Entity schemas

---

## What's Shared vs. Product-Specific

| Shared (healthsim-common) | Product-Specific (product repos) |
|------------------------------|----------------------------------|
| Skills & scenarios | Python implementation |
| Output formats | API reference |
| Reference data (codes, rules) | Product tutorials |
| MCP integration docs | Product-specific validation |
| Extension framework | Product-specific use cases |
| Architecture docs | CHANGELOG |

---

## Getting Help

| Resource | Use For |
|----------|---------|
| [Troubleshooting Guide](../hello-healthsim/TROUBLESHOOTING.md) | Common issues |
| [GitHub Issues](https://github.com/mark64oswald/healthsim-common/issues) | Bug reports, feature requests |
| [GitHub Discussions](https://github.com/mark64oswald/healthsim-common/discussions) | Questions, ideas |

---

## Document Conventions

- **User prompts** shown as: `"Generate a diabetic patient with A1C of 9.5"`
- **Code examples** in fenced blocks with syntax highlighting
- **File paths** relative to repository root
- **Links** to related documents throughout

---

*HealthSim generates synthetic test data only. Never use for actual patient care or real PHI.*
