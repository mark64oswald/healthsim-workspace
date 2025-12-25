---
name: Cross-Product Integration
description: Use NetworkSim-Local to provide real provider data to other HealthSim products. Trigger phrases include "real NPI for", "actual provider", "integrate with PatientSim", "real pharmacy for prescription"
version: 1.0.0
status: active
product: networksim-local
related_skills:
  - provider-lookup
  - specialty-search
  - facility-lookup
  - pharmacy-lookup
integration_products:
  - patientsim
  - membersim
  - rxmembersim
  - trialsim
  - populationsim
---

# Cross-Product Integration

Use NetworkSim-Local to provide real provider NPIs to other HealthSim products.

## Overview

NetworkSim-Local enhances other HealthSim products by replacing generated/synthetic provider identifiers with real NPIs from the NPPES registry. This creates more realistic synthetic healthcare data with:

- Valid NPI numbers that pass Luhn checks
- Real provider names and credentials
- Actual practice locations
- Authentic specialty classifications

## Integration Patterns

### PatientSim Integration

**Use Case**: Real attending physicians for patient encounters

```sql
-- Get physician for encounter in patient's area
SELECT npi, last_name, first_name, credential, taxonomy_code
FROM providers 
WHERE entity_type_code = '1'
  AND taxonomy_code LIKE '207%'  -- Physicians
  AND practice_state = :patient_state
ORDER BY RANDOM()
LIMIT 1;
```

**Example Output**:
```json
{
  "attending_physician": {
    "npi": "1275504409",
    "name": "Jeremy LaMotte, MD",
    "taxonomy": "207Q00000X",
    "specialty": "Family Medicine"
  }
}
```

### MemberSim Integration

**Use Case**: Real facility NPIs for claims

```sql
-- Hospital for inpatient claim
SELECT npi, organization_name, practice_city, practice_state
FROM providers 
WHERE taxonomy_code LIKE '282N%'
  AND practice_state = :member_state
ORDER BY RANDOM()
LIMIT 1;
```

**Example Output**:
```json
{
  "service_facility": {
    "npi": "1366784092",
    "name": "Memorial Hospital",
    "type": "General Acute Care Hospital",
    "location": "Houston, TX"
  }
}
```

### RxMemberSim Integration

**Use Case**: Real pharmacy NPIs for prescription fills

```sql
-- Retail pharmacy near member's ZIP
SELECT npi, organization_name, practice_address_1, 
       practice_city, practice_state, practice_zip
FROM providers 
WHERE taxonomy_code = '3336C0003X'  -- Retail pharmacy
  AND practice_zip LIKE :zip_prefix || '%'
ORDER BY RANDOM()
LIMIT 1;
```

**Example Output**:
```json
{
  "dispensing_pharmacy": {
    "npi": "1821818246",
    "name": "CVS Pharmacy #1234",
    "address": "123 Main St, San Diego, CA 92101",
    "ncpdp": null
  }
}
```

### TrialSim Integration

**Use Case**: Real investigators for clinical trial sites

```sql
-- Oncologist as potential PI
SELECT npi, last_name, first_name, credential,
       practice_city, practice_state
FROM providers 
WHERE entity_type_code = '1'
  AND taxonomy_code LIKE '207RX%'  -- Oncology
  AND practice_state = :site_state
ORDER BY RANDOM()
LIMIT 1;
```

**Example Output**:
```json
{
  "principal_investigator": {
    "npi": "1942706999",
    "name": "Katelyn Soares, MD",
    "specialty": "Medical Oncology",
    "site": "Worcester, MA"
  }
}
```

### PopulationSim Integration

**Use Case**: Provider density analysis for geographic modeling

```sql
-- Providers per 10,000 population by state
SELECT 
    p.practice_state,
    COUNT(*) as provider_count
FROM providers p
WHERE p.practice_state IS NOT NULL
GROUP BY p.practice_state
ORDER BY provider_count DESC;
```

## Entity Mapping

| HealthSim Entity | NetworkSim-Local Query | Key Fields |
|------------------|------------------------|------------|
| `Patient.attending_physician` | Physician by state | npi, name, credential |
| `Encounter.provider` | Provider by specialty + location | npi, taxonomy, city |
| `Claim.service_facility` | Facility by type + state | npi, org_name, address |
| `Prescription.pharmacy` | Pharmacy by ZIP | npi, org_name, address |
| `TrialSite.investigator` | Physician by specialty | npi, name, credential |

## Taxonomy Mappings

### Common Specialty Queries

| Specialty | Taxonomy Pattern | Use Case |
|-----------|------------------|----------|
| Family Medicine | `207Q%` | Primary care encounters |
| Internal Medicine | `207R%` | Adult medicine |
| Pediatrics | `2080%` | Pediatric encounters |
| Cardiology | `207RC%` | Cardiac encounters |
| Oncology | `207RX%` | Cancer treatment, trials |
| Surgery | `2086%` | Surgical claims |
| Emergency | `207P%` | ED encounters |
| Psychiatry | `2084P%` | Mental health |

### Facility Types

| Facility | Taxonomy Pattern | Use Case |
|----------|------------------|----------|
| Hospital | `282N%` | Inpatient claims |
| Urgent Care | `261QU%` | Outpatient urgent |
| FQHC | `261QF%` | Community health |
| SNF | `314%` | Long-term care |
| Pharmacy | `3336%` | Prescriptions |

## Validation Rules

1. Always use `ORDER BY RANDOM() LIMIT 1` for variety
2. Filter by geographic proximity to maintain realism
3. Match specialty to encounter type
4. Validate NPI format (10 digits, Luhn check)

## Sample Integration Code

```python
import duckdb

def get_provider_for_encounter(state: str, specialty_prefix: str = '207'):
    """Get a random real provider for an encounter."""
    con = duckdb.connect('data/networksim-local.duckdb', read_only=True)
    
    result = con.execute(f"""
        SELECT npi, last_name, first_name, credential, taxonomy_code
        FROM providers 
        WHERE entity_type_code = '1'
          AND taxonomy_code LIKE '{specialty_prefix}%'
          AND practice_state = ?
        ORDER BY RANDOM()
        LIMIT 1
    """, [state]).fetchone()
    
    con.close()
    
    if result:
        return {
            "npi": result[0],
            "name": f"{result[2]} {result[1]}",
            "credential": result[3],
            "taxonomy": result[4]
        }
    return None


def get_pharmacy_for_prescription(zip_prefix: str):
    """Get a random real pharmacy near a ZIP code."""
    con = duckdb.connect('data/networksim-local.duckdb', read_only=True)
    
    result = con.execute("""
        SELECT npi, organization_name, practice_address_1,
               practice_city, practice_state, practice_zip
        FROM providers 
        WHERE taxonomy_code LIKE '3336%'
          AND practice_zip LIKE ? || '%'
        ORDER BY RANDOM()
        LIMIT 1
    """, [zip_prefix]).fetchone()
    
    con.close()
    
    if result:
        return {
            "npi": result[0],
            "name": result[1],
            "address": f"{result[2]}, {result[3]}, {result[4]} {result[5]}"
        }
    return None
```

## Notes

- Real NPIs enhance data quality but are not required
- Other HealthSim products work without NetworkSim-Local
- Geographic matching improves realism
- Provider data updated monthly from NPPES

## Related Skills

- [Provider Lookup](provider-lookup.md) - Look up by NPI
- [Specialty Search](specialty-search.md) - Find by specialty
- [Facility Lookup](facility-lookup.md) - Find hospitals
- [Pharmacy Lookup](pharmacy-lookup.md) - Find pharmacies
