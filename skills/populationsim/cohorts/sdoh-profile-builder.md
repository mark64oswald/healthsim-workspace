---
name: sdoh-profile-builder
description: >
  Build SDOH profiles for cohorts with social factor rates and ICD-10 Z-code
  assignments. Translates SVI and population characteristics into actionable
  SDOH characteristics for synthetic patients. Triggers: "SDOH profile",
  "social factors for cohort", "Z-code rates", "social determinants profile".
---

# SDOH Profile Builder Skill

## Overview

The sdoh-profile-builder skill creates comprehensive SDOH profiles for cohorts by translating population-level indicators (SVI, economic data, community factors) into individual-level characteristics and ICD-10 Z-code assignment rates. This bridges population analysis to patient-level synthetic data generation.

**Primary Use Cases**:
- Define SDOH characteristics for cohorts
- Set realistic Z-code assignment rates
- Translate SVI to patient attributes
- Support care gap analysis

---

## Trigger Phrases

- "SDOH profile for [geography/cohort]"
- "Social determinants for [population]"
- "What Z-codes for [vulnerable population]?"
- "Build SDOH profile from SVI"
- "Social factors for Medicaid cohort"

---

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `geography` | string | Yes* | - | Geographic reference |
| `svi_score` | float | Yes* | - | Overall SVI (0-1) |
| `population_type` | string | No | "general" | "general", "medicaid", "medicare", "fqhc" |
| `condition` | string | No | - | Primary condition context |

*Either geography or svi_score required

---

## SDOH Framework

### Five SDOH Domains

| Domain | Key Factors | Z-Code Range |
|--------|-------------|--------------|
| **Economic Stability** | Income, employment, debt, expenses | Z59.4-Z59.9 |
| **Education Access** | Literacy, language, degree | Z55.x |
| **Healthcare Access** | Insurance, providers, transport | Z75.x |
| **Neighborhood** | Housing, safety, transport, food | Z59.0-Z59.3, Z59.8 |
| **Social/Community** | Isolation, discrimination, support | Z60.x, Z63.x |

### Key Z-Codes for SDOH

| Code | Description | National Rate |
|------|-------------|---------------|
| Z59.0 | Homelessness | 0.2% |
| Z59.1 | Inadequate housing | 2.4% |
| Z59.41 | Food insecurity | 10.2% |
| Z59.6 | Low income | 11.5% |
| Z59.7 | Insufficient social insurance | 8.8% |
| Z59.82 | Transportation insecurity | 5.8% |
| Z60.2 | Living alone | 14.2% |
| Z60.3 | Acculturation difficulty | 4.8% |
| Z60.4 | Social exclusion | 3.2% |
| Z62.810 | Personal history of abuse | 2.8% |
| Z63.0 | Relationship problems | 4.2% |
| Z55.0 | Illiteracy | 4.1% |
| Z56.0 | Unemployment | 3.6% |
| Z56.9 | Employment problem | 5.2% |

---

## SVI to Z-Code Mapping

### Translation Rules

| SVI Range | Vulnerability | Z-Code Multiplier |
|-----------|---------------|-------------------|
| 0.00-0.25 | Low | 0.5x |
| 0.25-0.50 | Low-Moderate | 0.8x |
| 0.50-0.75 | Moderate-High | 1.2x |
| 0.75-1.00 | High | 1.8x |

### Theme-Specific Mapping

**Socioeconomic Theme** → Economic Z-Codes
```
SVI_Theme1 > 0.75 →
  Z59.6 (Low income): base × 1.8
  Z59.41 (Food insecurity): base × 1.6
  Z56.0 (Unemployment): base × 1.5
```

**Household Composition Theme** → Social Z-Codes
```
SVI_Theme2 > 0.75 →
  Z60.2 (Living alone): base × 1.4
  Z63.0 (Relationship problems): base × 1.3
  Z62.810 (History of abuse): base × 1.5
```

**Minority/Language Theme** → Access Z-Codes
```
SVI_Theme3 > 0.75 →
  Z60.3 (Acculturation difficulty): base × 2.0
  Z60.4 (Social exclusion): base × 1.6
  Z55.0 (Illiteracy): base × 1.5
```

**Housing/Transportation Theme** → Environment Z-Codes
```
SVI_Theme4 > 0.75 →
  Z59.1 (Inadequate housing): base × 1.8
  Z59.82 (Transportation): base × 1.7
  Z59.0 (Homelessness): base × 2.0
```

---

## Output Schema

```json
{
  "sdoh_profile": {
    "source": {
      "geography": "Harris County, TX",
      "geography_type": "county",
      "fips": "48201",
      "svi_overall": 0.68,
      "population_type": "general"
    },
    
    "svi_detail": {
      "overall": 0.68,
      "theme1_socioeconomic": 0.62,
      "theme2_household": 0.58,
      "theme3_minority": 0.82,
      "theme4_housing": 0.64
    },
    
    "domain_indicators": {
      "economic_stability": {
        "poverty_rate": 0.158,
        "unemployment": 0.052,
        "no_health_insurance": 0.168,
        "food_insecurity": 0.128
      },
      "education_access": {
        "no_hs_diploma": 0.182,
        "limited_english": 0.142,
        "low_literacy_estimate": 0.068
      },
      "healthcare_access": {
        "uninsured": 0.168,
        "no_usual_source_of_care": 0.124,
        "delayed_care_cost": 0.108
      },
      "neighborhood": {
        "housing_cost_burden": 0.382,
        "no_vehicle": 0.082,
        "food_desert": 0.068
      },
      "social_community": {
        "living_alone": 0.112,
        "single_parent": 0.168,
        "limited_social_support": 0.142
      }
    },
    
    "z_code_rates": {
      "economic": {
        "Z59.6": { "name": "Low income", "rate": 0.158, "confidence": "high" },
        "Z59.41": { "name": "Food insecurity", "rate": 0.128, "confidence": "high" },
        "Z59.7": { "name": "Insufficient social insurance", "rate": 0.168, "confidence": "high" },
        "Z56.0": { "name": "Unemployment", "rate": 0.052, "confidence": "high" }
      },
      "education": {
        "Z55.0": { "name": "Illiteracy", "rate": 0.068, "confidence": "moderate" },
        "Z55.9": { "name": "Education problem", "rate": 0.182, "confidence": "high" }
      },
      "housing": {
        "Z59.0": { "name": "Homelessness", "rate": 0.008, "confidence": "moderate" },
        "Z59.1": { "name": "Inadequate housing", "rate": 0.042, "confidence": "moderate" },
        "Z59.82": { "name": "Transportation", "rate": 0.082, "confidence": "high" }
      },
      "social": {
        "Z60.2": { "name": "Living alone", "rate": 0.112, "confidence": "high" },
        "Z60.3": { "name": "Acculturation difficulty", "rate": 0.142, "confidence": "high" },
        "Z60.4": { "name": "Social exclusion", "rate": 0.048, "confidence": "moderate" }
      }
    },
    
    "z_code_summary": {
      "any_sdoh_z_code": 0.42,
      "multiple_z_codes": 0.18,
      "high_burden_3_plus": 0.08
    },
    
    "condition_interaction": {
      "condition": "E11",
      "sdoh_impact": {
        "medication_nonadherence": {
          "rate": 0.182,
          "z_code": "Z91.120",
          "drivers": ["cost", "transportation", "food_insecurity"]
        },
        "missed_appointments": {
          "rate": 0.148,
          "drivers": ["transportation", "work_schedule"]
        },
        "poor_glycemic_control": {
          "rate": 0.282,
          "drivers": ["food_insecurity", "stress", "cost"]
        }
      }
    },
    
    "population_type_adjustments": {
      "population_type": "medicaid",
      "adjustment_notes": "Medicaid population has 1.5x SDOH burden",
      "adjusted_rates": {
        "Z59.6": 0.85,
        "Z59.41": 0.28,
        "Z59.82": 0.15
      }
    },
    
    "care_gap_implications": {
      "expected_barriers": [
        { "barrier": "Cost of medications", "rate": 0.18, "intervention": "PAP referral" },
        { "barrier": "Transportation", "rate": 0.08, "intervention": "NEMT" },
        { "barrier": "Food insecurity", "rate": 0.13, "intervention": "Food pharmacy" },
        { "barrier": "Health literacy", "rate": 0.12, "intervention": "Teach-back" }
      ]
    }
  },
  
  "validation": {
    "sources": [
      "CDC_SVI_2022",
      "ACS_2022_5yr",
      "USDA_Food_Atlas"
    ],
    "confidence": "high",
    "notes": "Large county with reliable estimates"
  }
}
```

---

## Examples

### Example 1: High-Vulnerability Population

**Request**: "SDOH profile for FQHC population in South Bronx"

**Response**:

**South Bronx FQHC SDOH Profile**

**Source**: Bronx County, NY (tracts with SVI > 0.80)
**SVI Overall**: 0.92 (Very High)

**SVI Themes**:
| Theme | Score | Interpretation |
|-------|-------|----------------|
| Socioeconomic | 0.94 | Very High |
| Household Composition | 0.86 | High |
| Minority/Language | 0.96 | Very High |
| Housing/Transportation | 0.88 | High |

**Z-Code Assignment Rates**:

*Economic Domain*:
| Code | Description | Rate |
|------|-------------|------|
| Z59.6 | Low income | 42% |
| Z59.41 | Food insecurity | 32% |
| Z59.7 | Insufficient insurance | 24% |
| Z56.0 | Unemployment | 12% |

*Housing/Environment Domain*:
| Code | Description | Rate |
|------|-------------|------|
| Z59.0 | Homelessness | 2.4% |
| Z59.1 | Inadequate housing | 8.2% |
| Z59.82 | Transportation insecurity | 14% |

*Social Domain*:
| Code | Description | Rate |
|------|-------------|------|
| Z60.3 | Acculturation difficulty | 28% |
| Z60.4 | Social exclusion | 8% |
| Z60.2 | Living alone | 18% |

**SDOH Burden**:
- Any SDOH Z-code: 68%
- 2+ Z-codes: 42%
- 3+ Z-codes: 24%

---

### Example 2: Medicare Population

**Request**: "Social determinants profile for Medicare population in rural Kentucky"

**Response**:

**Rural Kentucky Medicare SDOH Profile**

**Geography**: Eastern Kentucky (Appalachian counties)
**Population**: Medicare beneficiaries 65+
**SVI Average**: 0.78

**Key SDOH Factors**:
| Factor | Rate | vs National Medicare |
|--------|------|---------------------|
| Low income | 28% | +12% |
| Transportation barrier | 18% | +10% |
| Living alone | 32% | +8% |
| Limited internet | 42% | +22% |
| Food insecurity | 18% | +6% |

**Z-Code Rates for Cohort**:
| Code | Description | Rate |
|------|-------------|------|
| Z59.6 | Low income | 28% |
| Z59.82 | Transportation | 18% |
| Z60.2 | Living alone | 32% |
| Z59.41 | Food insecurity | 18% |
| Z60.4 | Social exclusion | 12% |
| Z63.4 | Disappearance of family member | 8% |

**Health Impact**:
| SDOH Factor | Health Outcome | Correlation |
|-------------|----------------|-------------|
| Transportation | Missed dialysis | +42% |
| Food insecurity | Hypoglycemia | +28% |
| Living alone | ED utilization | +35% |
| Low income | Rx nonadherence | +48% |

---

### Example 3: Condition-Specific SDOH

**Request**: "SDOH profile for heart failure patients in urban areas"

**Response**:

**Heart Failure Urban SDOH Profile**

**Context**: I50 patients in metro areas with SVI > 0.60

**Condition-Specific SDOH Impact**:

**Medication Adherence Barriers**:
| Barrier | Rate | Z-Code |
|---------|------|--------|
| Cost | 24% | Z59.6 |
| Complex regimen | 18% | Z91.120 |
| Cognitive | 12% | Z91.19 |

**Diet Adherence Barriers**:
| Barrier | Rate | Z-Code |
|---------|------|--------|
| Food insecurity | 18% | Z59.41 |
| Limited cooking | 14% | Z59.1 |
| Cultural factors | 8% | Z60.3 |

**Care Access Barriers**:
| Barrier | Rate | Z-Code |
|---------|------|--------|
| Transportation | 15% | Z59.82 |
| Work schedule | 12% | Z56.9 |
| Caregiver burden | 18% | Z63.6 |

**Readmission Risk by SDOH**:
| SDOH Factor | Readmission RR |
|-------------|----------------|
| 0 SDOH factors | 1.0 (ref) |
| 1-2 factors | 1.4x |
| 3+ factors | 2.2x |

**Recommended Interventions**:
- CHW home visits for high-SDOH patients
- Transition care management
- NEMT for follow-up
- Medically-tailored meals

---

## Validation Rules

### Input Validation
- [ ] Geography valid or SVI provided
- [ ] SVI between 0 and 1
- [ ] Population type valid

### Output Validation
- [ ] Z-code rates ≤ 1.0
- [ ] Rates consistent with SVI level
- [ ] Domain indicators sum appropriately

---

## Related Skills

- [svi-analysis.md](../sdoh/svi-analysis.md) - SVI source
- [economic-indicators.md](../sdoh/economic-indicators.md) - Economic detail
- [community-factors.md](../sdoh/community-factors.md) - Environment detail
- [cohort-specification.md](cohort-specification.md) - Full cohort
