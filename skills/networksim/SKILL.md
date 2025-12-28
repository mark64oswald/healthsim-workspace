---
name: healthsim-networksim
description: >
  NetworkSim provides provider network intelligence using real NPPES data (8.9M providers).
  Use this skill for ANY request involving: (1) provider search by specialty or location,
  (2) facility search (hospitals, nursing homes, clinics), (3) NPI validation,
  (4) network adequacy assessment against CMS/NCQA standards, (5) healthcare desert
  identification, (6) provider density analysis, (7) network roster generation,
  (8) hospital or physician quality metrics, (9) cross-product provider assignment,
  (10) pharmacy network analysis.
---

# NetworkSim - Provider Network Intelligence & Analytics

## Overview

NetworkSim provides provider network intelligence using real NPPES provider data (8.9M records), CMS facility data (60K+ facilities), and quality metrics integrated with PopulationSim demographics. Unlike synthetic generation, NetworkSim queries **actual registered providers** to enable:

1. **Provider Discovery**: Search providers by specialty, location, credentials, quality
2. **Network Analysis**: Assess adequacy against regulatory standards (CMS MA, NCQA, Medicaid)
3. **Healthcare Access**: Identify deserts combining access gaps, health needs, and vulnerability
4. **Cross-Product Integration**: Provide authentic providers for PatientSim, MemberSim, TrialSim

**Key Differentiator**: NetworkSim uses real NPPES registry data, not synthetic generation. Every NPI returned is a real, registered healthcare provider.

## Quick Reference

| I want to... | Use This Skill | Key Triggers |
|--------------|----------------|--------------|
| **Provider Search** | | |
| Find providers by specialty | `query/provider-search.md` | "find cardiologists", "search for PCPs", "providers in" |
| Search hospitals/facilities | `query/facility-search.md` | "hospitals in", "find nursing homes", "clinics near" |
| Find pharmacies | `query/pharmacy-search.md` | "pharmacies in", "retail pharmacy", "specialty pharmacy" |
| **Validation & Roster** | | |
| Validate an NPI | `query/npi-validation.md` | "is NPI valid", "validate NPI", "check NPI" |
| Generate network roster | `query/network-roster.md` | "create roster", "export providers", "network list" |
| **Density & Coverage** | | |
| Calculate provider density | `query/provider-density.md` | "providers per 100K", "density analysis", "HRSA benchmark" |
| Assess network coverage | `query/coverage-analysis.md` | "network coverage", "geographic coverage", "specialty gaps" |
| **Quality Metrics** | | |
| Filter by hospital quality | `query/hospital-quality-search.md` | "4-star hospitals", "high quality", "CMS ratings" |
| Filter by physician credentials | `query/physician-quality-search.md` | "MD only", "board certified", "credentials" |
| **Advanced Analytics** | | |
| Assess network adequacy | `analytics/network-adequacy-analysis.md` | "adequacy assessment", "CMS standards", "NCQA requirements" |
| Identify healthcare deserts | `analytics/healthcare-deserts.md` | "healthcare deserts", "underserved areas", "access gaps" |
| **Synthetic Generation** | | |
| Generate synthetic provider | `synthetic/synthetic-provider.md` | "generate a provider", "create physician" |
| Generate synthetic facility | `synthetic/synthetic-facility.md` | "generate hospital", "create facility" |
| Generate synthetic pharmacy | `synthetic/synthetic-pharmacy.md` | "generate pharmacy", "create pharmacy" |
| Generate synthetic network | `synthetic/synthetic-network.md` | "generate network", "create provider network" |
| Generate synthetic plan | `synthetic/synthetic-plan.md` | "generate plan", "create health plan" |
| **Integration** | | |
| Assign provider to encounter | `integration/provider-for-encounter.md` | "provider for patient", "attending physician" |
| Determine network status | `integration/network-for-member.md` | "in-network check", "network status" |
| Route prescription | `integration/pharmacy-for-rx.md` | "pharmacy for prescription", "dispense at" |

## Trigger Phrases

### Provider Search
- "Find [specialty] in [location]"
- "Search for primary care providers in [county]"
- "Show me cardiologists within 10 miles of [zip]"
- "List all orthopedic surgeons in Texas"
- "Find providers with NPI starting with [prefix]"

### Facility Search
- "Find hospitals in [county/state]"
- "Show me 4-star hospitals in California"
- "List nursing homes in [city]"
- "Find trauma centers near [location]"
- "Search for ambulatory surgery centers"

### Validation & Roster
- "Is NPI 1234567890 valid?"
- "Validate this NPI: [number]"
- "Create a network roster for [specialty] in [geography]"
- "Export provider list to CSV"
- "Generate directory of PCPs for [county]"

### Density & Coverage
- "What's the provider density in [county]?"
- "Providers per 100K population in Texas"
- "Compare density to HRSA benchmarks"
- "Which specialties have gaps in [region]?"
- "Assess geographic coverage for [state]"

### Quality Filtering
- "Show only 5-star hospitals"
- "Find MD/DO providers only"
- "Filter by board certification"
- "High-quality providers in [area]"
- "Premium tier hospitals"

### Network Adequacy
- "Assess PCP adequacy for California"
- "Does this network meet CMS standards?"
- "NCQA specialty coverage check"
- "Provider-to-enrollee ratio analysis"
- "Time/distance access assessment"

### Healthcare Deserts
- "Identify healthcare deserts in Texas"
- "Show underserved counties"
- "Find areas with low access + high disease burden"
- "Critical shortage areas for primary care"
- "Equity analysis for vulnerable populations"

## Skill Inventory

### Query Skills (9 skills)

| Skill | File | Lines | Purpose |
|-------|------|-------|---------|
| Provider Search | `query/provider-search.md` | 450 | Search 8.9M providers by specialty, location |
| Facility Search | `query/facility-search.md` | 380 | Search hospitals, nursing homes, clinics |
| Pharmacy Search | `query/pharmacy-search.md` | 320 | Search retail, specialty, mail pharmacies |
| NPI Validation | `query/npi-validation.md` | 280 | Validate NPIs with Luhn checksums |
| Network Roster | `query/network-roster.md` | 350 | Generate rosters in CSV/JSON/Excel |
| Provider Density | `query/provider-density.md` | 400 | Calculate density vs HRSA benchmarks |
| Coverage Analysis | `query/coverage-analysis.md` | 380 | Assess geographic/specialty coverage |
| Hospital Quality | `query/hospital-quality-search.md` | 320 | Filter by CMS star ratings |
| Physician Quality | `query/physician-quality-search.md` | 290 | Filter by credentials (MD/DO/NP/PA) |

### Analytics Skills (2 skills)

| Skill | File | Lines | Purpose |
|-------|------|-------|---------|
| Network Adequacy | `analytics/network-adequacy-analysis.md` | 653 | CMS/NCQA regulatory compliance |
| Healthcare Deserts | `analytics/healthcare-deserts.md` | 757 | Access + health needs + vulnerability |

### Synthetic Skills (6 skills)

| Skill | File | Lines | Purpose |
|-------|------|-------|---------|
| Synthetic Provider | `synthetic/synthetic-provider.md` | 400 | Generate providers with valid NPI format |
| Synthetic Facility | `synthetic/synthetic-facility.md` | 350 | Generate hospitals, ASCs, clinics |
| Synthetic Pharmacy | `synthetic/synthetic-pharmacy.md` | 320 | Generate pharmacies with NCPDP IDs |
| Synthetic Network | `synthetic/synthetic-network.md` | 450 | Generate complete network configurations |
| Synthetic Plan | `synthetic/synthetic-plan.md` | 380 | Generate health plan structures |
| Synthetic Pharmacy Benefit | `synthetic/synthetic-pharmacy-benefit.md` | 350 | Generate PBM configurations |

### Integration Skills (5 skills)

| Skill | File | Lines | Purpose |
|-------|------|-------|---------|
| Provider for Encounter | `integration/provider-for-encounter.md` | 280 | Assign providers to PatientSim |
| Network for Member | `integration/network-for-member.md` | 300 | Network status for MemberSim |
| Pharmacy for Rx | `integration/pharmacy-for-rx.md` | 260 | Pharmacy routing for RxMemberSim |
| Formulary for Rx | `integration/formulary-for-rx.md` | 290 | Formulary checks for RxMemberSim |
| Benefit for Claim | `integration/benefit-for-claim.md` | 270 | Benefit lookup for MemberSim |

### Reference Skills (7 skills)

| Skill | File | Purpose |
|-------|------|---------|
| Network Types | `reference/network-types.md` | HMO, PPO, EPO, POS structures |
| Plan Structures | `reference/plan-structures.md` | Cost sharing, benefit design |
| Pharmacy Benefits | `reference/pharmacy-benefit-concepts.md` | PBM, formulary, tiers |
| Network Adequacy | `reference/network-adequacy.md` | CMS/NCQA standards |
| PBM Operations | `reference/pbm-operations.md` | Claims processing, rebates |
| Specialty Pharmacy | `reference/specialty-pharmacy.md` | Limited distribution, hubs |
| Utilization Management | `reference/utilization-management.md` | PA, step therapy, QL |

### Pattern Skills (5 skills)

| Skill | File | Purpose |
|-------|------|---------|
| HMO Network | `patterns/hmo-network-pattern.md` | Closed network, gatekeeper model |
| PPO Network | `patterns/ppo-network-pattern.md` | Open access, tiered cost sharing |
| Tiered Network | `patterns/tiered-network-pattern.md` | Quality-based tier assignment |
| Specialty Distribution | `patterns/specialty-distribution-pattern.md` | Specialty mix by geography |
| Pharmacy Benefit | `patterns/pharmacy-benefit-patterns.md` | PBM network configurations |

---

## Output Types

### ProviderSearchResult

Provider records from NPPES database:

```json
{
  "npi": "1234567890",
  "entity_type": "individual",
  "name": {
    "last": "Johnson",
    "first": "Sarah",
    "credential": "MD, FACC"
  },
  "taxonomy": {
    "code": "207RC0000X",
    "classification": "Internal Medicine",
    "specialization": "Cardiovascular Disease"
  },
  "practice_location": {
    "address": "123 Medical Center Dr",
    "city": "Houston",
    "state": "TX",
    "zip": "77030",
    "county_fips": "48201"
  },
  "enumeration_date": "2015-03-15",
  "last_update": "2024-11-01"
}
```

### AdequacyAssessment

Network adequacy evaluation against standards:

```json
{
  "geography": {
    "type": "state",
    "code": "CA",
    "name": "California"
  },
  "standard": "CMS_MA",
  "assessment_date": "2025-01-15",
  "metrics": {
    "pcp_ratio": {
      "actual": 85.3,
      "required": 83.3,
      "adequacy_pct": 102.4,
      "status": "ADEQUATE"
    },
    "specialist_coverage": {
      "ncqa_13_specialties": 13,
      "covered": 13,
      "status": "COMPLETE"
    }
  },
  "overall_status": "COMPLIANT"
}
```

### HealthcareDesert

Desert identification with severity scoring:

```json
{
  "geography": {
    "fips": "48001",
    "county": "Anderson County",
    "state": "Texas"
  },
  "desert_type": "primary_care",
  "severity": "critical",
  "scores": {
    "access_gap": 0.85,
    "health_burden": 0.72,
    "social_vulnerability": 0.68,
    "quality_gap": 0.45,
    "composite": 0.73
  },
  "indicators": {
    "providers_per_100k": 12.3,
    "hrsa_benchmark": 60.0,
    "diabetes_prevalence": 0.142,
    "svi_percentile": 0.78
  },
  "intervention_priority": 1
}
```

### NetworkRoster

Exportable provider roster:

```json
{
  "roster_id": "ROSTER-CA-PCP-2025-001",
  "generated_at": "2025-01-15T10:30:00Z",
  "criteria": {
    "specialty": "Primary Care",
    "geography": "San Diego County, CA",
    "quality_filter": "MD/DO only"
  },
  "summary": {
    "total_providers": 2847,
    "by_taxonomy": {
      "207Q00000X": 1523,
      "207R00000X": 892,
      "363L00000X": 432
    }
  },
  "export_formats": ["csv", "json", "xlsx"]
}
```

---

## Data Sources

### Provider Data (network.providers)

| Attribute | Value |
|-----------|-------|
| Source | NPPES (National Plan and Provider Enumeration System) |
| Records | 8,925,672 |
| Update Frequency | Monthly CMS releases |
| Coverage | All active US healthcare providers with NPIs |
| County FIPS | 97.77% coverage (3,213 of 3,286 counties) |

**Key Columns**: npi, entity_type_code, last_name, first_name, credential, taxonomy_1-4, practice_state, practice_city, practice_zip, county_fips

### Facility Data (network.facilities)

| Attribute | Value |
|-----------|-------|
| Source | CMS Provider of Services (POS) file |
| Records | 77,302 |
| Types | Hospitals (01), SNFs (05), HHAs (07), Hospice (13) |
| Coverage | All CMS-certified healthcare facilities |

### Hospital Quality (network.hospital_quality)

| Attribute | Value |
|-----------|-------|
| Source | CMS Hospital Compare |
| Records | 5,421 hospitals |
| Metrics | Overall rating (1-5 stars), mortality, readmission, safety |

### Physician Quality (network.physician_quality)

| Attribute | Value |
|-----------|-------|
| Source | CMS Physician Compare |
| Records | 1,478,309 physicians |
| Metrics | Quality measures, Medicare participation |

### AHRF County Data (network.ahrf_county)

| Attribute | Value |
|-----------|-------|
| Source | HRSA Area Health Resources File |
| Records | 3,235 counties |
| Metrics | Provider counts, hospital beds, health workforce |

---

## Regulatory Standards

### CMS Medicare Advantage

**Provider-to-Enrollee Ratios**:
| Specialty | Ratio | Example (10K enrollees) |
|-----------|-------|------------------------|
| Primary Care | 1:1,200 | 8.3 providers minimum |
| OB/GYN | 1:2,000 | 5.0 providers |
| Mental Health | 1:3,000 | 3.3 providers |
| General Surgery | 1:5,000 | 2.0 providers |

**Time/Distance Standards**:
| Geography | Primary Care | Specialists | Hospitals |
|-----------|--------------|-------------|-----------|
| Urban (>50K) | 10 miles | 15 miles | 15 miles |
| Suburban | 20 miles | 30 miles | 30 miles |
| Rural (<10K) | 30 miles | 60 miles | 60 miles |

### NCQA 13 Essential Specialties

Must have at least one contracted provider in each:
1. Primary Care
2. Cardiology
3. Dermatology
4. Endocrinology
5. Gastroenterology
6. General Surgery
7. Neurology
8. OB/GYN
9. Ophthalmology
10. Orthopedic Surgery
11. Otolaryngology (ENT)
12. Psychiatry
13. Urology

### HRSA Benchmarks

| Metric | Threshold | Classification |
|--------|-----------|----------------|
| PCPs per 100K | <60 | Health Professional Shortage Area |
| PCPs per 100K | 60-80 | Adequate |
| PCPs per 100K | >80 | Well-served |

---

## Performance Benchmarks

| Query Type | Target | Actual | Status |
|------------|--------|--------|--------|
| Provider search | <100ms | 13.8ms | ✅ Excellent |
| NPI validation | <50ms | 18.8ms | ✅ Excellent |
| Provider density | <100ms | 46.9ms | ✅ Good |
| Network adequacy | <300ms | ~200ms | ✅ Good |
| Healthcare deserts | <500ms | ~400ms | ✅ Good |
| Cross-product JOIN | <500ms | ~300ms | ✅ Good |

**Database**: healthsim.duckdb (1.7 GB)
**Indexes**: county_fips, taxonomy_1, practice_state

---

## Cross-Product Integration

### NetworkSim → PatientSim

Assign providers to clinical encounters:

```sql
-- Find cardiologist for heart failure patient
SELECT npi, first_name, last_name, credential
FROM network.providers
WHERE taxonomy_1 LIKE '207RC%'  -- Cardiovascular
  AND practice_state = 'TX'
  AND county_fips = '48201'     -- Harris County
LIMIT 1;
```

### NetworkSim → MemberSim

Determine network status for claims:

```sql
-- Check if provider is in network
SELECT 
  CASE WHEN p.npi IS NOT NULL THEN 'IN_NETWORK' 
       ELSE 'OUT_OF_NETWORK' END as network_status
FROM network.providers p
WHERE p.npi = '1234567890';
```

### NetworkSim + PopulationSim

Equity analysis combining provider access with vulnerability:

```sql
-- Provider access in vulnerable communities
SELECT 
    sv.county,
    sv.rpl_themes as svi_percentile,
    COUNT(DISTINCT p.npi) as provider_count,
    sv.e_totpop as population,
    ROUND(COUNT(DISTINCT p.npi) * 100000.0 / sv.e_totpop, 1) as per_100k
FROM population.svi_county sv
LEFT JOIN network.providers p ON sv.stcnty = p.county_fips
WHERE sv.rpl_themes > 0.75  -- Most vulnerable quartile
GROUP BY sv.county, sv.rpl_themes, sv.e_totpop
ORDER BY per_100k ASC;
```

---

## Development Status

### Phase 1: Data Infrastructure ✅
- [x] NPPES data import (8.9M providers)
- [x] Geographic enrichment (97.77% county FIPS)
- [x] Quality metrics integration (CMS Hospital Compare)
- [x] Test framework (18 tests passing)

### Phase 2: Query Skills ✅
- [x] 9 query skills (provider, facility, pharmacy, NPI, roster, density, coverage, quality)
- [x] 4,069 lines documentation

### Phase 3: Advanced Analytics 🎯 (Current)
- [x] Network adequacy analysis
- [x] Healthcare deserts identification
- [ ] Specialty distribution analysis
- [ ] Provider demographics analysis

**Progress**: 8 of 12 sessions complete (66%)

---

## Validation Rules

### NPI Validation
- 10 digits exactly
- Luhn algorithm checksum
- Prefix 1 or 2 (individual vs organization)
- Active status in NPPES

### Taxonomy Validation
- Valid NUCC taxonomy codes
- Matches provider specialty claim
- Primary taxonomy switch indicator

### Geographic Validation
- Valid state abbreviation (2 letters)
- Valid county FIPS (5 digits)
- ZIP code format (5 or 9 digits)

---

## Related Documentation

- **Examples**: [hello-healthsim/examples/networksim-examples.md](../../hello-healthsim/examples/networksim-examples.md)
- **Developer Guide**: [developer-guide.md](developer-guide.md)
- **Prompt Guide**: [prompt-guide.md](prompt-guide.md)
- **Data Architecture**: [docs/healthsim-duckdb-schema.md](../../docs/healthsim-duckdb-schema.md)
- **Master SKILL.md**: [SKILL.md](../../SKILL.md)

---

*Last Updated: December 28, 2025*
*Version: 2.0.0*
*Status: Active (Phase 3)*
