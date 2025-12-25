---
name: NetworkSim-Local
description: Real provider network data integration using local NPPES registry. Provides actual NPIs, provider names, specialties, and locations for cross-product integration.
version: 1.1.0
status: active
product: networksim-local
data_source: NPPES NPI Registry (CMS)
record_count: 8,937,975
last_updated: 2024-12-25
---

# NetworkSim-Local

Real provider network data from NPPES NPI Registry for HealthSim cross-product integration.

## Overview

NetworkSim-Local provides access to **8.9 million real healthcare providers** from the CMS NPPES registry, enabling realistic provider data in synthetic healthcare scenarios. Unlike NetworkSim v1.0 (which generates synthetic providers), NetworkSim-Local uses actual registered providers.

## Quick Start

```
"Find cardiologists in California"
"Look up NPI 1234567890"
"Pharmacies near ZIP 92101"
"Hospitals in Texas"
"Get a random physician for a patient encounter in NY"
```

## Trigger Phrases

| Category | Example Phrases |
|----------|-----------------|
| **Provider Lookup** | "lookup NPI", "find provider", "who is NPI" |
| **Geographic Search** | "providers in [city]", "doctors in [state]", "near ZIP" |
| **Specialty Search** | "find cardiologists", "primary care in", "specialists" |
| **Facility Search** | "hospitals in", "clinics near", "urgent care" |
| **Pharmacy Search** | "pharmacies in", "drugstore near", "retail pharmacy" |
| **Integration** | "real NPI for", "actual provider for PatientSim" |

## Skills

| Skill | Description | Status |
|-------|-------------|--------|
| [Provider Lookup](skills/provider-lookup.md) | Look up by NPI or name | ✅ Active |
| [Geographic Search](skills/geographic-search.md) | Find by city, state, ZIP | ✅ Active |
| [Specialty Search](skills/specialty-search.md) | Find by taxonomy code | ✅ Active |
| [Facility Lookup](skills/facility-lookup.md) | Find hospitals, clinics | ✅ Active |
| [Pharmacy Lookup](skills/pharmacy-lookup.md) | Find pharmacies | ✅ Active |
| [Cross-Product Integration](skills/cross-product-integration.md) | Integration with other HealthSim products | ✅ Active |

## Database Statistics

| Metric | Value |
|--------|-------|
| **Total Providers** | 8,937,975 |
| **Individuals** | 7,063,800 (79%) |
| **Organizations** | 1,874,175 (21%) |
| **States/Territories** | 56 |
| **Database Size** | 1.7 GB |
| **Source Date** | December 2024 |

### Top Provider Categories

| Category | Count |
|----------|-------|
| Physicians (Allopathic) | 1,475,196 |
| Physical Therapists | 680,315 |
| Nurse Practitioners | 477,961 |
| Psychologists | 451,029 |
| Pharmacists | 319,976 |
| Clinics | 270,523 |
| Physician Assistants | 211,133 |

## Cross-Product Integration

NetworkSim-Local enhances other HealthSim products:

| Product | Integration Use Case |
|---------|---------------------|
| **PatientSim** | Real attending physician NPIs for encounters |
| **MemberSim** | Actual facility NPIs for claims |
| **RxMemberSim** | Real pharmacy NPIs for prescriptions |
| **TrialSim** | Real investigator NPIs for trial sites |
| **PopulationSim** | Provider density analysis by geography |

## Data Sources

| Source | Description | Size |
|--------|-------------|------|
| **NPPES Registry** | National Plan and Provider Enumeration System | 8.9M records |
| **NUCC Taxonomy** | Provider taxonomy code reference | 900+ codes |

## Setup Requirements

```bash
# Install dependencies
pip install duckdb pandas

# Run setup (downloads and builds database)
cd skills/networksim-local/setup
python setup-all.py
```

## File Structure

```
networksim-local/
├── SKILL.md              # This file
├── README.md             # Product overview
├── developer-guide.md    # Developer documentation
├── data/                 # Local data (not in git)
│   ├── nppes/            # NPPES CSV files
│   ├── taxonomy/         # Taxonomy reference
│   └── networksim-local.duckdb  # Built database
├── setup/                # Setup scripts
│   ├── download-nppes.py
│   ├── build-database.py
│   └── validate-db.py
├── skills/               # Skill definitions
│   ├── provider-lookup.md
│   ├── geographic-search.md
│   ├── specialty-search.md
│   ├── facility-lookup.md
│   ├── pharmacy-lookup.md
│   └── cross-product-integration.md
└── queries/              # SQL templates
    └── provider-queries.sql
```

## Comparison: NetworkSim vs NetworkSim-Local

| Feature | NetworkSim v1.0 | NetworkSim-Local |
|---------|-----------------|------------------|
| **Data Source** | Generated/Synthetic | Real NPPES data |
| **NPIs** | Synthetic (valid format) | Actual registered |
| **Provider Names** | Generated | Real names |
| **Locations** | Based on PopulationSim | Actual addresses |
| **Use Case** | Full synthetic data | Real data integration |
| **Setup** | None (on-demand) | Requires data download |
| **Size** | N/A | 1.7 GB database |

## Related Products

- [NetworkSim](../networksim/SKILL.md) - Synthetic provider generation
- [PatientSim](../patientsim/SKILL.md) - Patient and EMR data
- [MemberSim](../membersim/SKILL.md) - Health plan claims
- [RxMemberSim](../rxmembersim/SKILL.md) - Pharmacy claims
- [TrialSim](../trialsim/SKILL.md) - Clinical trial data
- [PopulationSim](../populationsim/SKILL.md) - Demographics and SDOH

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.1.0 | 2024-12-25 | Added cross-product integration skill |
| 1.0.0 | 2024-12-24 | Initial release with 8.9M providers |
