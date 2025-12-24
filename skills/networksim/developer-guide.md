---
name: networksim-developer-guide
description: |
  Developer guide for NetworkSim covering quick start, core concepts,
  skill reference, workflows, output formats, integration points, and
  best practices for working with healthcare network data.
---

# NetworkSim Developer Guide

## Overview

NetworkSim provides healthcare network knowledge and synthetic entity generation for the HealthSim ecosystem. This guide covers technical details for developers integrating NetworkSim into their workflows.

**Key Principle**: NetworkSim generates the *structural entities* (providers, facilities, pharmacies, networks) that other HealthSim products use for realistic data generation.

---

## Quick Start

### 1. Network Type Reference

```
User: Explain the difference between HMO and PPO networks

Claude: 
HMO (Health Maintenance Organization) and PPO (Preferred Provider Organization) 
differ primarily in flexibility and cost:

| Aspect | HMO | PPO |
|--------|-----|-----|
| Network | Must use in-network | Can use any provider |
| Referrals | Required for specialists | Not required |
| PCP Required | Yes | No |
| Out-of-Network | Not covered (except emergency) | Covered at higher cost |
| Premiums | Lower | Higher |

HMOs emphasize coordinated care through a gatekeeper model.
PPOs prioritize member flexibility with broader access.
```

### 2. Synthetic Provider Generation

```
User: Generate a cardiologist in Houston, Texas

Claude:
{
  "npi": "1234567890",
  "entity_type": "individual",
  "provider": {
    "last_name": "Nguyen",
    "first_name": "David",
    "credential": "MD, FACC"
  },
  "taxonomy": {
    "code": "207RC0000X",
    "classification": "Internal Medicine",
    "specialization": "Cardiovascular Disease"
  },
  "practice_location": {
    "city": "Houston",
    "state": "TX",
    "county_fips": "48201"
  }
}
```

### 3. Cross-Product Integration

```
User: Generate a provider for this heart failure patient's cardiology referral

Claude:
Based on the patient's diagnosis (I50.9) and location, generating 
an appropriate heart failure specialist:

{
  "npi": "1987654321",
  "provider": {
    "last_name": "Patel",
    "first_name": "Vikram",
    "credential": "MD, FACC, FHFSA"
  },
  "taxonomy": {
    "code": "207RC0001X",
    "specialization": "Advanced Heart Failure and Transplant Cardiology"
  },
  "integration_context": {
    "source_product": "patientsim",
    "matched_on": ["diagnosis_category", "geography"]
  }
}
```

---

## Core Concepts

### Network Types
[To be completed in Phase 5 - see reference/network-types.md]

Summary:
- **HMO** - Closed network, gatekeeper model, lowest cost
- **PPO** - Open network, no referrals, higher cost
- **EPO** - Closed network like HMO, but no PCP requirement
- **POS** - Hybrid HMO/PPO, choose at point of service
- **HDHP** - High deductible, HSA-eligible

### Provider Taxonomy
[To be completed in Phase 5 - NUCC taxonomy codes, specialty distribution]

Key taxonomy code patterns:
- `207R%` - Internal Medicine subspecialties
- `207X%` - Orthopedic Surgery subspecialties
- `208D%` - General Practice
- `363L%` - Nurse Practitioners
- `363A%` - Physician Assistants

### Facility Types
[To be completed in Phase 5 - Hospital, ambulatory, post-acute categories]

Major categories:
- Short Term Acute Care Hospitals
- Long Term Acute Care Hospitals
- Skilled Nursing Facilities
- Ambulatory Surgery Centers
- Home Health Agencies

### Pharmacy Classification
[To be completed in Phase 5 - Retail, mail order, specialty]

Types:
- Community/Retail Pharmacy
- Mail Order Pharmacy
- Specialty Pharmacy
- Long Term Care Pharmacy
- Compounding Pharmacy

---

## Skill Reference

| Skill | Category | Purpose | Trigger Phrases |
|-------|----------|---------|-----------------|
| network-types | reference | Network type definitions | "explain HMO", "difference between PPO and EPO" |
| plan-structures | reference | Benefit design concepts | "plan structure", "deductible vs copay" |
| pharmacy-benefit-concepts | reference | Pharmacy benefit design | "tier structure", "formulary" |
| pbm-operations | reference | PBM functions | "what is a PBM", "BIN PCN" |
| utilization-management | reference | UM programs | "prior authorization", "step therapy" |
| specialty-pharmacy | reference | Specialty distribution | "specialty pharmacy", "hub model" |
| network-adequacy | reference | Access standards | "network adequacy", "time distance" |
| synthetic-provider | synthetic | Generate providers | "generate provider", "create physician" |
| synthetic-facility | synthetic | Generate facilities | "generate hospital", "create ASC" |
| synthetic-pharmacy | synthetic | Generate pharmacies | "generate pharmacy", "specialty pharmacy" |
| synthetic-network | synthetic | Generate networks | "generate network", "build roster" |
| synthetic-plan | synthetic | Generate plans | "generate plan", "benefit design" |
| synthetic-pharmacy-benefit | synthetic | Generate Rx benefits | "pharmacy benefit design" |

---

## Common Workflows

### Workflow 1: Provider for Clinical Encounter
[To be completed in Phase 5]

```
PatientSim Encounter → NetworkSim → Provider Entity
```

### Workflow 2: Network for Member Plan
[To be completed in Phase 5]

```
MemberSim Member → NetworkSim → Network + Benefit Context
```

### Workflow 3: Pharmacy for Prescription
[To be completed in Phase 5]

```
RxMemberSim Prescription → NetworkSim → Pharmacy Entity
```

### Workflow 4: Site for Clinical Trial
[To be completed in Phase 5]

```
TrialSim Protocol → NetworkSim → Facility + Investigator
```

---

## Output Formats

### Provider Entity (Canonical JSON)
[To be completed in Phase 5 - full schema]

```json
{
  "npi": "string (10 digits)",
  "entity_type": "individual | organization",
  "provider": {
    "last_name": "string",
    "first_name": "string",
    "credential": "string"
  },
  "taxonomy": {
    "code": "string (10 char)",
    "classification": "string",
    "specialization": "string"
  },
  "practice_location": {
    "address_line_1": "string",
    "city": "string",
    "state": "string (2 char)",
    "zip": "string (5 or 9 digits)",
    "county_fips": "string (5 digits)"
  }
}
```

### Facility Entity (Canonical JSON)
[To be completed in Phase 5 - full schema]

```json
{
  "ccn": "string (6 digits)",
  "facility": {
    "name": "string",
    "type": "string",
    "subtype": "string"
  },
  "characteristics": {
    "bed_count": "integer",
    "emergency_department": "boolean"
  }
}
```

### Pharmacy Entity (Canonical JSON)
[To be completed in Phase 5 - full schema]

```json
{
  "ncpdp_id": "string (7 digits)",
  "npi": "string (10 digits)",
  "pharmacy": {
    "name": "string",
    "type": "string",
    "chain_name": "string"
  }
}
```

---

## Integration Points

### To PatientSim
[To be completed in Phase 5]

NetworkSim provides:
- Attending physician for encounters
- Referring physician for referrals
- Facility for admissions

### To MemberSim
[To be completed in Phase 5]

NetworkSim provides:
- Network configuration for member
- Rendering provider for claims
- Facility for institutional claims

### To RxMemberSim
[To be completed in Phase 5]

NetworkSim provides:
- Dispensing pharmacy for claims
- Prescriber for prescriptions
- Pharmacy network context

### To TrialSim
[To be completed in Phase 5]

NetworkSim provides:
- Site facility for trials
- Principal investigator
- Sub-investigators

### From PopulationSim
[To be completed in Phase 5]

PopulationSim provides:
- Geographic context (county, ZCTA)
- Population density
- HPSA/MUA designations
- Provider-to-population ratios

---

## Best Practices

1. **Be Specific About Geography** - Include city, county, or state for provider generation
   ```
   ✅ "Generate a cardiologist in Harris County, Texas"
   ❌ "Generate a cardiologist in Texas"
   ```

2. **Specify Specialty When Relevant** - Use specific specialty names, not generic terms
   ```
   ✅ "Generate an interventional cardiologist"
   ❌ "Generate a heart doctor"
   ```

3. **Include Context for Integration** - Provide encounter/claim context for cross-product use
   ```
   ✅ "Generate a provider for this heart failure patient's cardiology referral"
   ❌ "Generate a provider"
   ```

4. **Request Specific Output When Needed** - Ask for taxonomy codes, credentials if required
   ```
   ✅ "Generate a provider with full taxonomy codes and board certifications"
   ❌ "Generate a provider" (may omit optional fields)
   ```

5. **Use Reference Skills First** - Understand concepts before generating data
   ```
   ✅ "Explain specialty pharmacy concepts" → then "Generate a specialty pharmacy"
   ❌ Jump straight to generation without understanding
   ```

6. [Additional best practices to be added in Phase 5]

---

## Troubleshooting

[To be completed in Phase 5]

### Common Issues

| Issue | Cause | Resolution |
|-------|-------|------------|
| Missing taxonomy code | Specialty not recognized | Use NUCC taxonomy lookup |
| Invalid NPI format | Not 10 digits | NPIs are always 10 digits |
| County not found | Misspelled or wrong state | Use county FIPS code |
| [More to be added] | | |

---

## Related Documentation

- [SKILL.md](SKILL.md) - Main skill reference with routing
- [Prompt Guide](prompt-guide.md) - Example prompts by category
- [README](README.md) - Product overview
- [HealthSim Architecture](../../docs/HEALTHSIM-ARCHITECTURE-GUIDE.md) - Overall architecture

---

*Developer Guide will be expanded in Phase 5 with complete workflows, schemas, and examples.*
