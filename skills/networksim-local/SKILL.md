---
name: NetworkSim-Local Master Skill
description: Real provider data integration using NPPES NPI Registry. Lookup providers, facilities, and pharmacies by NPI, geography, or specialty. Trigger phrases include "lookup NPI", "find provider", "real provider data", "NPPES lookup", "actual NPI"
version: 0.1.0
status: development
product: networksim-local
---

# NetworkSim-Local

> Real provider data from NPPES NPI Registry for authentic healthcare simulations.

## Overview

NetworkSim-Local provides **actual provider, facility, and pharmacy data** from public CMS sources. Unlike NetworkSim (which synthesizes data), NetworkSim-Local returns real NPIs, addresses, and specialties from the NPPES registry.

## Trigger Phrases

- "Look up NPI [number]"
- "Find real provider for..."
- "What actual providers are in [location]?"
- "NPPES lookup for..."
- "Find cardiologists in [city/state]"
- "Real pharmacy near [location]"
- "Actual hospital in [area]"

## Capabilities

| Capability | Description |
|------------|-------------|
| **Provider Lookup** | Find provider by NPI, name, or specialty |
| **Geographic Search** | Find providers in city, state, or ZIP |
| **Specialty Search** | Find providers by taxonomy code |
| **Facility Lookup** | Find hospitals, ASCs, SNFs by location |
| **Pharmacy Lookup** | Find pharmacies by location or type |

## Data Coverage

- **Provider Types**: Physicians, NPs, PAs, pharmacies, facilities
- **Geographic**: Top 10 US states (CA, TX, NY, FL, IL, PA, OH, GA, NC, MI)
- **Records**: ~3 million active providers
- **Source**: NPPES NPI Registry (updated monthly)

## Response Format

All responses include **provenance tracking**:

```
Provider: John Smith, MD
NPI: 1234567890
Specialty: Internal Medicine (207R00000X)
Address: 123 Medical Center Dr, San Diego, CA 92101

Source: NPPES Registry, November 2025
```

## Skills

### Provider Skills
- [provider-lookup](skills/provider-lookup.md) - Lookup by NPI or name
- [specialty-search](skills/specialty-search.md) - Search by taxonomy code
- [geographic-search](skills/geographic-search.md) - Search by location

### Facility Skills
- [facility-lookup](skills/facility-lookup.md) - Hospitals and facilities
- [pharmacy-lookup](skills/pharmacy-lookup.md) - Pharmacies by location

## Cross-Product Integration

| Product | Use Case |
|---------|----------|
| **PatientSim** | Real attending physician NPIs |
| **MemberSim** | Actual provider network data |
| **RxMemberSim** | Real pharmacy NPIs and addresses |
| **PopulationSim** | Provider density by geography |

## Prerequisites

NetworkSim-Local requires local data setup:

1. Download NPPES data: `python setup/download-nppes.py`
2. Build database: `python setup/build-local-db.py`
3. Verify: `python setup/validate-db.py`

See [developer-guide.md](developer-guide.md) for complete setup instructions.

## Examples

### Example 1: NPI Lookup

**User**: Look up NPI 1234567890

**Response**:
```
Provider: Jane Doe, MD, FACC
NPI: 1234567890
Entity Type: Individual
Specialty: Cardiovascular Disease (207RC0000X)
Practice Location: 456 Heart Center Blvd, Los Angeles, CA 90001
Phone: (310) 555-1234

Source: NPPES Registry, November 2025
```

### Example 2: Geographic Search

**User**: Find orthopedic surgeons in Houston, TX

**Response**:
```
Found 847 orthopedic surgeons in Houston, TX

Top Results:
1. Robert Johnson, MD - NPI: 1122334455
   Texas Orthopedic Associates, 789 Spine Way, Houston, TX 77001
   
2. Maria Garcia, DO - NPI: 2233445566
   Houston Sports Medicine, 321 Joint Dr, Houston, TX 77002
   
[... additional results available]

Source: NPPES Registry, November 2025
```

### Example 3: Facility Search

**User**: What hospitals are in Cook County, IL?

**Response**:
```
Found 52 hospitals in Cook County, IL

Major Facilities:
1. Northwestern Memorial Hospital
   NPI: 1234567890 | CCN: 140281
   Beds: 894 | Type: General Acute Care
   
2. Rush University Medical Center
   NPI: 2345678901 | CCN: 140119
   Beds: 671 | Type: Academic Medical Center

[... additional facilities]

Source: NPPES Registry + CMS Provider of Services, November 2025
```

## Validation Rules

1. NPIs must be 10-digit numbers passing Luhn check
2. Taxonomy codes must exist in NUCC code set
3. State codes must be valid 2-letter abbreviations
4. Results limited to active providers (no deactivation date)

## Related Skills

- [NetworkSim](../networksim/SKILL.md) - Synthetic provider generation
- [PopulationSim](../populationsim/SKILL.md) - Geographic demographics

## Notes

- **Data is local only** - requires setup before use
- **Updates manually** - download new NPPES monthly as needed
- **Experimental** - parallel implementation to NetworkSim v1.0
