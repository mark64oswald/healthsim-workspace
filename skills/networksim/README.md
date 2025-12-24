# NetworkSim

**Healthcare Network Knowledge and Entity Generation**

[![Status](https://img.shields.io/badge/status-active-green.svg)]()
[![Version](https://img.shields.io/badge/version-1.0-blue.svg)]()
[![HealthSim](https://img.shields.io/badge/healthsim-product-purple.svg)]()

---

## Overview

NetworkSim is the healthcare network infrastructure product within the HealthSim ecosystem. While other products focus on generating healthcare transactions (PatientSim for encounters, MemberSim for claims, RxMemberSim for prescriptions), NetworkSim provides the **structural foundation** that makes those transactions realistic:

- **Providers** who deliver care
- **Facilities** where care happens
- **Pharmacies** that dispense medications
- **Networks** that organize provider access
- **Benefits** that define cost sharing

NetworkSim serves two primary functions:

1. **Reference Knowledge** - Educational content about network types, plan structures, pharmacy benefits, PBM operations, and utilization management
2. **Synthetic Generation** - Creation of realistic provider, facility, pharmacy, and network entities

---

## Key Capabilities

### Reference Knowledge

NetworkSim captures deep domain knowledge about healthcare network operations:

| Domain | Topics Covered |
|--------|----------------|
| **Network Types** | HMO, PPO, EPO, POS, HDHP - definitions, tradeoffs, when to use |
| **Plan Structures** | Deductibles, copays, coinsurance, OOP max, accumulators |
| **Pharmacy Benefits** | Tier structures, formulary types, preferred networks |
| **PBM Operations** | Claims processing, BIN/PCN routing, rebates, mail order |
| **Utilization Management** | Prior authorization, step therapy, quantity limits |
| **Specialty Pharmacy** | Limited distribution, hub model, REMS programs |
| **Network Adequacy** | Time/distance standards, provider ratios, access |

### Synthetic Entity Generation

NetworkSim generates realistic synthetic entities with proper identifiers and characteristics:

| Entity | Key Attributes | Identifiers |
|--------|----------------|-------------|
| **Provider** | Name, credentials, specialty, location, affiliations | NPI (10-digit) |
| **Facility** | Name, type, beds, ownership, services | CCN (6-digit) |
| **Pharmacy** | Name, type, chain, services, hours | NCPDP (7-digit), NPI |
| **Network** | Type, geography, provider roster | Network ID |
| **Plan** | Benefits, cost sharing, network | Plan ID |

### Cross-Product Integration

NetworkSim enhances other HealthSim products with realistic network context:

```
┌─────────────────────────────────────────────────────────────────┐
│                    CROSS-PRODUCT INTEGRATION                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  PatientSim ──────► NetworkSim ──────► Provider for encounter   │
│  (needs provider)   (generates)        (with NPI, credentials)  │
│                                                                  │
│  MemberSim ───────► NetworkSim ──────► Network for member       │
│  (needs network)    (generates)        (with benefit context)   │
│                                                                  │
│  RxMemberSim ─────► NetworkSim ──────► Pharmacy for Rx          │
│  (needs pharmacy)   (generates)        (with NCPDP, type)       │
│                                                                  │
│  TrialSim ────────► NetworkSim ──────► Site/Investigator        │
│  (needs site)       (generates)        (with facility, PI)      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Quick Start

### Example 1: Network Type Reference

**Prompt:**
```
Explain the difference between HMO and PPO network types
```

**Response:**
```
HMO (Health Maintenance Organization) and PPO (Preferred Provider Organization) 
represent two fundamentally different approaches to healthcare coverage:

┌─────────────────┬──────────────────────┬──────────────────────┐
│ Characteristic  │ HMO                  │ PPO                  │
├─────────────────┼──────────────────────┼──────────────────────┤
│ Network         │ Closed - must use    │ Open - any provider  │
│                 │ in-network providers │ allowed              │
├─────────────────┼──────────────────────┼──────────────────────┤
│ PCP Required    │ Yes - gatekeeper     │ No                   │
├─────────────────┼──────────────────────┼──────────────────────┤
│ Referrals       │ Required for         │ Not required         │
│                 │ specialists          │                      │
├─────────────────┼──────────────────────┼──────────────────────┤
│ Out-of-Network  │ Not covered          │ Covered at higher    │
│                 │ (except emergency)   │ cost share           │
├─────────────────┼──────────────────────┼──────────────────────┤
│ Premiums        │ Lower                │ Higher               │
├─────────────────┼──────────────────────┼──────────────────────┤
│ Out-of-Pocket   │ Lower                │ Higher               │
├─────────────────┼──────────────────────┼──────────────────────┤
│ Best For        │ Cost-conscious,      │ Flexibility-focused, │
│                 │ coordinated care     │ specialist access    │
└─────────────────┴──────────────────────┴──────────────────────┘

Key Tradeoff: HMOs offer lower costs in exchange for less flexibility. 
PPOs offer more choice but at higher premiums and cost sharing.
```

### Example 2: Generate a Provider

**Prompt:**
```
Generate an orthopedic surgeon in Denver, Colorado
```

**Response:**
```json
{
  "npi": "1456789012",
  "entity_type": "individual",
  "provider": {
    "last_name": "Richardson",
    "first_name": "David",
    "middle_name": "James",
    "credential": "MD, FAAOS",
    "gender": "M",
    "date_of_birth": "1975-03-15"
  },
  "taxonomy": {
    "primary": {
      "code": "207X00000X",
      "classification": "Orthopaedic Surgery",
      "specialization": null,
      "display_name": "Orthopedic Surgeon",
      "is_primary": true
    },
    "secondary": [
      {
        "code": "207XS0114X",
        "classification": "Orthopaedic Surgery",
        "specialization": "Sports Medicine",
        "display_name": "Sports Medicine Orthopedist"
      }
    ]
  },
  "practice_location": {
    "address_line_1": "1601 East 19th Avenue",
    "address_line_2": "Suite 4200",
    "city": "Denver",
    "state": "CO",
    "zip": "80218",
    "county": "Denver",
    "county_fips": "08031",
    "phone": "303-555-0187",
    "fax": "303-555-0188"
  },
  "mailing_address": {
    "address_line_1": "PO Box 6510",
    "city": "Denver",
    "state": "CO",
    "zip": "80206"
  },
  "hospital_affiliations": [
    {
      "name": "UCHealth University of Colorado Hospital",
      "ccn": "060024",
      "privileges": ["Admitting", "Surgical", "Emergency"]
    },
    {
      "name": "Sky Ridge Medical Center",
      "ccn": "060114",
      "privileges": ["Surgical"]
    }
  ],
  "group_practice": {
    "name": "Colorado Orthopedic Associates",
    "npi": "1234567890",
    "tax_id": "84-1234567"
  },
  "certifications": {
    "board_certified": true,
    "board": "American Board of Orthopaedic Surgery",
    "initial_certification": "2008",
    "recertification_due": "2028"
  },
  "licenses": [
    {
      "state": "CO",
      "number": "MD.0045678",
      "status": "Active",
      "expiration": "2026-06-30"
    }
  ],
  "education": {
    "medical_school": "University of Colorado School of Medicine",
    "graduation_year": 2001,
    "residency": "University of Colorado Orthopedic Residency",
    "fellowship": "Steadman Clinic Sports Medicine Fellowship"
  },
  "accepting_new_patients": true,
  "languages": ["English"],
  "enumeration_date": "2007-05-15",
  "last_update": "2024-01-15"
}
```

### Example 3: Generate a Facility

**Prompt:**
```
Generate a 150-bed community hospital in suburban Atlanta
```

**Response:**
```json
{
  "ccn": "110234",
  "npi": "1678901234",
  "facility": {
    "name": "Northside Gwinnett Medical Center",
    "doing_business_as": "Northside Gwinnett",
    "type": "Short Term Acute Care Hospital",
    "type_code": "01",
    "subtype": "Community Hospital"
  },
  "characteristics": {
    "bed_count": 150,
    "bed_count_certified": 148,
    "operating_rooms": 8,
    "emergency_department": true,
    "trauma_level": "Level III",
    "teaching_status": "Non-Teaching"
  },
  "ownership": {
    "type": "Non-Profit",
    "subtype": "Church Operated",
    "system_affiliation": "Northside Hospital System"
  },
  "location": {
    "address_line_1": "3850 Satellite Boulevard NW",
    "city": "Duluth",
    "state": "GA",
    "zip": "30096",
    "county": "Gwinnett",
    "county_fips": "13135",
    "phone": "770-555-0100",
    "latitude": 34.0123,
    "longitude": -84.1456
  },
  "services": {
    "medical": ["Cardiology", "Oncology", "Neurology", "Pulmonology"],
    "surgical": ["General Surgery", "Orthopedics", "Cardiovascular", "Neurosurgery"],
    "women_children": ["Labor & Delivery", "NICU Level II", "Pediatrics"],
    "ancillary": ["Laboratory", "Radiology", "MRI", "CT", "Nuclear Medicine"],
    "outpatient": ["Same Day Surgery", "Infusion Center", "Rehabilitation"]
  },
  "accreditation": {
    "type": "The Joint Commission",
    "status": "Accredited",
    "last_survey": "2023-06-15",
    "specialty_certifications": [
      "Primary Stroke Center",
      "Chest Pain Center"
    ]
  },
  "medicare": {
    "provider_type": "Short Term Acute Care",
    "participation_date": "1985-01-01",
    "fiscal_year_end": "December"
  },
  "contact": {
    "administrator": "Jennifer Walsh, MHA, FACHE",
    "cno": "Patricia Morgan, RN, MSN",
    "cmo": "Robert Chen, MD, MBA"
  },
  "hours": {
    "emergency": "24/7",
    "visiting": "8:00 AM - 8:00 PM"
  }
}
```

---

## Skill Organization

NetworkSim skills are organized into four categories:

### Reference Knowledge (`reference/`)

Educational content that explains healthcare network concepts:

| Skill | File | Purpose |
|-------|------|---------|
| Network Types | `network-types.md` | HMO, PPO, EPO, POS, HDHP definitions |
| Plan Structures | `plan-structures.md` | Benefit component explanations |
| Pharmacy Benefits | `pharmacy-benefit-concepts.md` | Tier structures, formulary types |
| PBM Operations | `pbm-operations.md` | PBM role and functions |
| Utilization Management | `utilization-management.md` | PA, step therapy, QL |
| Specialty Pharmacy | `specialty-pharmacy.md` | Limited distribution, hub model |
| Network Adequacy | `network-adequacy.md` | Access standards |

### Synthetic Generation (`synthetic/`)

Generate realistic synthetic entities:

| Skill | File | Output |
|-------|------|--------|
| Synthetic Provider | `synthetic-provider.md` | Provider with NPI |
| Synthetic Facility | `synthetic-facility.md` | Facility with CCN |
| Synthetic Pharmacy | `synthetic-pharmacy.md` | Pharmacy with NCPDP |
| Synthetic Network | `synthetic-network.md` | Network configuration |
| Synthetic Plan | `synthetic-plan.md` | Plan benefit structure |
| Synthetic Pharmacy Benefit | `synthetic-pharmacy-benefit.md` | Pharmacy benefit design |

### Patterns & Templates (`patterns/`)

Reusable configuration patterns:

| Skill | File | Purpose |
|-------|------|---------|
| HMO Network | `hmo-network-pattern.md` | Typical HMO structure |
| PPO Network | `ppo-network-pattern.md` | Typical PPO structure |
| Tiered Network | `tiered-network-pattern.md` | Narrow/tiered networks |
| Pharmacy Patterns | `pharmacy-benefit-patterns.md` | Common PBM configs |
| Specialty Distribution | `specialty-distribution-pattern.md` | Hub vs retail |

### Cross-Product Integration (`integration/`)

Bridge NetworkSim to other products:

| Skill | File | Integration |
|-------|------|-------------|
| Provider for Encounter | `provider-for-encounter.md` | PatientSim |
| Network for Member | `network-for-member.md` | MemberSim |
| Pharmacy for RX | `pharmacy-for-rx.md` | RxMemberSim |
| Benefit for Claim | `benefit-for-claim.md` | MemberSim |
| Formulary Concepts | `formulary-concepts-for-rx.md` | RxMemberSim |

---

## Use Cases by Audience

### Healthcare Developers

- Generate test providers for EMR integration testing
- Create realistic facility data for claims testing
- Build pharmacy networks for PBM simulations
- Generate provider directories for member portals

### Healthcare Analysts

- Understand network type differences for reporting
- Learn pharmacy benefit structures for analysis
- Model network adequacy scenarios
- Compare plan design options

### Healthcare Educators

- Teach network type concepts with real examples
- Demonstrate prior authorization workflows
- Illustrate specialty pharmacy models
- Explain PBM operations

---

## Integration Points

### NetworkSim → PatientSim

```
PatientSim Encounter ──► NetworkSim ──► Provider Entity
                                        Facility Entity
```

**Use Case**: Generate attending physician for an encounter

```
Given this PatientSim encounter for a patient with chest pain,
generate an appropriate emergency physician.
```

### NetworkSim → MemberSim

```
MemberSim Claim ──► NetworkSim ──► Network Context
                                   Benefit Context
```

**Use Case**: Add network status to a claim

```
This member has a PPO plan. Generate network context showing
the provider is in-network with appropriate cost sharing.
```

### NetworkSim → RxMemberSim

```
RxMemberSim Prescription ──► NetworkSim ──► Pharmacy Entity
                                            Formulary Context
```

**Use Case**: Generate dispensing pharmacy for a prescription

```
Generate a specialty pharmacy for this Humira prescription.
```

### NetworkSim ← PopulationSim

```
PopulationSim Geography ──► NetworkSim ──► Provider Distribution
                                           Access Patterns
```

**Use Case**: Geographic provider generation

```
Generate cardiologists distributed across Harris County, TX
proportional to population density.
```

---

## Core Concepts

### Provider Taxonomy

NetworkSim uses the NUCC Healthcare Provider Taxonomy Code Set:

| Taxonomy Code | Classification | Specialization |
|---------------|----------------|----------------|
| 207R00000X | Internal Medicine | (none) |
| 207RC0000X | Internal Medicine | Cardiovascular Disease |
| 207RE0101X | Internal Medicine | Endocrinology |
| 208D00000X | General Practice | (none) |
| 207X00000X | Orthopaedic Surgery | (none) |
| 207XS0114X | Orthopaedic Surgery | Sports Medicine |

### Facility Types

| Type | CCN Pattern | Description |
|------|-------------|-------------|
| Short Term Acute | XX0001-0879 | General hospitals |
| Long Term Acute | XX2000-2299 | LTACH facilities |
| Rehabilitation | XX3025-3099 | Inpatient rehab |
| Psychiatric | XX4000-4499 | Psychiatric hospitals |
| SNF | XX5000-6499 | Skilled nursing |
| Home Health | XX7000-8499 | Home health agencies |
| Hospice | XX1500-1799 | Hospice providers |
| ASC | XXABCD | Ambulatory surgery centers |

### Pharmacy Types

| Type | NCPDP Class | Description |
|------|-------------|-------------|
| Community/Retail | 01 | Neighborhood pharmacies |
| Institutional | 02 | Hospital pharmacies |
| Long Term Care | 03 | LTC pharmacies |
| Mail Order | 04 | Mail service |
| Specialty | 05 | High-touch specialty |
| Compounding | 06 | Compounding services |
| Nuclear | 07 | Radiopharmacy |

---

## Output Formats

### Canonical JSON (Default)

All NetworkSim entities are generated in canonical JSON format first:

```json
{
  "npi": "1234567890",
  "entity_type": "individual",
  "provider": { ... },
  "taxonomy": { ... },
  "practice_location": { ... }
}
```

### FHIR R4

Providers can be output as FHIR Practitioner resources:

```json
{
  "resourceType": "Practitioner",
  "id": "1234567890",
  "identifier": [
    {
      "system": "http://hl7.org/fhir/sid/us-npi",
      "value": "1234567890"
    }
  ],
  "name": [
    {
      "family": "Martinez",
      "given": ["Elena"],
      "suffix": ["MD", "FACC"]
    }
  ]
}
```

### Flat/CSV

For bulk operations, entities can be output in flat format matching NPPES:

```csv
NPI,Entity Type,Last Name,First Name,Credential,Taxonomy 1,...
1234567890,1,Martinez,Elena,MD,207RC0000X,...
```

---

## What NetworkSim Does NOT Do

To maintain clear boundaries with other HealthSim products:

| Capability | Owner | Not NetworkSim |
|------------|-------|----------------|
| Process claims | MemberSim | NetworkSim generates structure, not logic |
| Adjudicate pharmacy claims | RxMemberSim | NetworkSim provides pharmacy entities |
| Determine formulary coverage | RxMemberSim | NetworkSim explains concepts |
| Generate encounters | PatientSim | NetworkSim provides providers |
| Create clinical documentation | PatientSim | NetworkSim provides facility context |
| Geographic demographics | PopulationSim | NetworkSim consumes geography |
| SDOH indicators | PopulationSim | NetworkSim focuses on network access |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2024-12 | Initial release |

### Roadmap

| Version | Planned | Features |
|---------|---------|----------|
| 1.1 | Q1 2025 | NetworkSim-Local integration (real NPPES data) |
| 1.2 | Q2 2025 | Enhanced network adequacy with PopulationSim |

---

## Related Documentation

- [SKILL.md](SKILL.md) - Master skill reference
- [Developer Guide](developer-guide.md) - Technical details
- [Prompt Guide](prompt-guide.md) - Example prompts
- [HealthSim Architecture](../../docs/HEALTHSIM-ARCHITECTURE-GUIDE.md) - Overall architecture
- [Hello HealthSim Examples](../../hello-healthsim/examples/) - Working examples

---

## Getting Started

1. **Learn the concepts** - Start with reference skills to understand network types and structures
2. **Generate entities** - Use synthetic skills to create providers, facilities, pharmacies
3. **Apply patterns** - Use pattern skills for common configurations
4. **Integrate** - Use integration skills to enhance other HealthSim products

For detailed examples, see the [Prompt Guide](prompt-guide.md).

---

*NetworkSim is part of the HealthSim ecosystem for synthetic healthcare data generation.*
