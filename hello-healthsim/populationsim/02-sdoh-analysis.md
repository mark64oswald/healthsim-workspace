# Example 02: SDOH Analysis

## Objective

Perform a detailed Social Determinants of Health (SDOH) analysis using SVI and ADI metrics, with Z-code prevalence estimation.

---

## Prompt

```
Analyze social vulnerability in Harris County census tracts, focusing on 
high-vulnerability areas (SVI ≥ 0.70). Include Z-code prevalence estimates.
```

---

## Expected Output

### SDOH Analysis Summary

```json
{
  "analysis_id": "sdoh-48201-highsvi-001",
  "geography": {
    "type": "county",
    "fips": "48201",
    "name": "Harris County, TX"
  },
  "filter": {
    "svi_min": 0.70
  },
  
  "summary": {
    "total_tracts": 871,
    "high_vulnerability_tracts": 287,
    "high_vulnerability_pct": 0.33,
    "population_in_high_svi": 1562000,
    "population_pct_in_high_svi": 0.33
  },
  
  "svi_distribution": {
    "quartile_1": {"range": "0.00-0.25", "tracts": 198, "population": 1124000},
    "quartile_2": {"range": "0.25-0.50", "tracts": 186, "population": 1089000},
    "quartile_3": {"range": "0.50-0.75", "tracts": 200, "population": 956000},
    "quartile_4": {"range": "0.75-1.00", "tracts": 287, "population": 1562000}
  },
  
  "high_vulnerability_profile": {
    "demographics": {
      "total_population": 1562000,
      "median_age": 31.2,
      "race_ethnicity": {
        "hispanic": 0.582,
        "black_nh": 0.248,
        "white_nh": 0.128,
        "asian_nh": 0.042
      }
    },
    
    "svi_themes": {
      "theme_1_socioeconomic": {
        "mean_score": 0.78,
        "key_factors": {
          "poverty_rate": 0.284,
          "unemployment_rate": 0.092,
          "no_hs_diploma": 0.318,
          "per_capita_income": 18200
        }
      },
      "theme_2_household_disability": {
        "mean_score": 0.62,
        "key_factors": {
          "age_65_plus": 0.092,
          "age_under_17": 0.288,
          "disability_rate": 0.142,
          "single_parent": 0.218
        }
      },
      "theme_3_minority_language": {
        "mean_score": 0.88,
        "key_factors": {
          "minority_pct": 0.872,
          "limited_english": 0.248
        }
      },
      "theme_4_housing_transportation": {
        "mean_score": 0.74,
        "key_factors": {
          "multi_unit_housing": 0.428,
          "mobile_homes": 0.068,
          "crowding": 0.142,
          "no_vehicle": 0.148,
          "group_quarters": 0.032
        }
      }
    },
    
    "adi_summary": {
      "mean_national_percentile": 78,
      "mean_state_decile": 8,
      "deprivation_level": "high"
    },
    
    "health_indicators": {
      "diabetes": 0.148,
      "obesity": 0.382,
      "hypertension": 0.398,
      "depression": 0.228,
      "current_smoking": 0.178,
      "physical_inactivity": 0.348
    },
    
    "healthcare_access": {
      "uninsured_rate": 0.282,
      "medicaid_rate": 0.318,
      "no_usual_source_care": 0.228
    }
  },
  
  "z_code_prevalence": {
    "methodology": "factor_based_estimation",
    "rates": {
      "Z55.0": {
        "code": "Z55.0",
        "description": "Illiteracy and low-level literacy",
        "rate": 0.064,
        "source_factor": "no_hs_diploma (0.318) × 0.2"
      },
      "Z55.9": {
        "code": "Z55.9",
        "description": "Problems related to education",
        "rate": 0.102,
        "source_factor": "no_hs_diploma (0.318) × 0.32"
      },
      "Z56.0": {
        "code": "Z56.0",
        "description": "Unemployment",
        "rate": 0.074,
        "source_factor": "unemployment_rate (0.092) × 0.8"
      },
      "Z59.41": {
        "code": "Z59.41",
        "description": "Food insecurity",
        "rate": 0.168,
        "source_factor": "food_insecurity (0.21) × 0.8"
      },
      "Z59.6": {
        "code": "Z59.6",
        "description": "Low income",
        "rate": 0.227,
        "source_factor": "poverty_rate (0.284) × 0.8"
      },
      "Z59.7": {
        "code": "Z59.7",
        "description": "Insufficient social insurance",
        "rate": 0.226,
        "source_factor": "uninsured_rate (0.282) × 0.8"
      },
      "Z59.82": {
        "code": "Z59.82",
        "description": "Transportation insecurity",
        "rate": 0.118,
        "source_factor": "no_vehicle (0.148) × 0.8"
      },
      "Z60.3": {
        "code": "Z60.3",
        "description": "Acculturation difficulty",
        "rate": 0.099,
        "source_factor": "limited_english (0.248) × 0.4"
      }
    },
    
    "summary": {
      "total_sdoh_encounter_rate": 0.48,
      "avg_z_codes_per_patient": 1.8,
      "top_z_codes": ["Z59.6", "Z59.7", "Z59.41"]
    }
  },
  
  "geographic_clusters": [
    {
      "name": "Third Ward / Sunnyside",
      "tract_count": 28,
      "svi_mean": 0.86,
      "primary_theme": "socioeconomic",
      "population": 82000
    },
    {
      "name": "East Houston / Channelview",
      "tract_count": 34,
      "svi_mean": 0.82,
      "primary_theme": "minority_language",
      "population": 124000
    },
    {
      "name": "North Houston / Greenspoint",
      "tract_count": 22,
      "svi_mean": 0.84,
      "primary_theme": "housing_transportation",
      "population": 98000
    }
  ],
  
  "metadata": {
    "created_at": "2024-12-23T10:30:00Z",
    "svi_version": "2022",
    "adi_version": "4.0"
  }
}
```

---

## Key Insights

### Vulnerability Distribution

- **33%** of tracts (287 of 871) meet high-vulnerability threshold
- **1.56 million** residents live in high-SVI areas
- Highest concentration in minority/language theme (mean 0.88)

### SDOH Factors

- **Poverty**: 28.4% in high-SVI areas (vs 15.8% county-wide)
- **No HS diploma**: 31.8% (vs ~22% county-wide)
- **Limited English**: 24.8%
- **No vehicle**: 14.8%

### Z-Code Implications

- **22.7%** estimated Z59.6 (Low income) rate
- **16.8%** estimated Z59.41 (Food insecurity) rate
- Average **1.8 Z-codes per patient** in these areas

### Health Disparities

High-SVI areas show elevated rates:
- Diabetes: 14.8% vs 11.2% county-wide (+32%)
- Obesity: 38.2% vs 32.8% county-wide (+16%)
- Uninsured: 28.2% vs 16.6% county-wide (+70%)

---

## Variations

### Theme-Specific Analysis

```
Analyze socioeconomic vulnerability (SVI Theme 1) in Dallas County tracts
```

### ADI-Focused Analysis

```
Identify block groups with ADI national percentile ≥ 80 in Harris County
```

### Comparative Analysis

```
Compare SDOH factors between highest and lowest SVI quartile tracts in Bexar County
```

---

## Next Steps

- Use these SDOH insights to [define a cohort](03-cohort-definition.md)
- Assess [trial feasibility](04-trial-feasibility.md) with SDOH considerations
- Generate patients with appropriate Z-codes using PatientSim
