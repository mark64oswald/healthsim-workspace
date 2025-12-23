# Example 03: Cohort Definition

## Objective

Define a target population cohort with specific clinical conditions, demographic requirements, and SDOH characteristics for synthetic data generation.

---

## Prompt

```
Define a cohort of 1,000 patients for a diabetes health equity study with:
- Type 2 diabetes diagnosis
- Age 35-70
- From high-vulnerability areas (SVI ≥ 0.65) in Harris County
- At least 40% Hispanic representation
- Include hypertension comorbidity at 50% rate
- Enable PatientSim integration with Z-codes
```

---

## Expected Output

### CohortSpecification

```json
{
  "cohort_id": "cohort-dm-equity-harris-001",
  "name": "Diabetes Health Equity Cohort - Harris County",
  "description": "Adults with Type 2 diabetes in high-vulnerability census tracts for health equity analysis",
  
  "geography": {
    "type": "county",
    "identifiers": {
      "fips": "48201",
      "name": "Harris County",
      "state": "TX"
    },
    "filters": {
      "svi_min": 0.65,
      "urban_rural": "any"
    },
    "filtered_tracts": {
      "count": 342,
      "population": 1824000
    }
  },
  
  "demographics": {
    "age": {
      "min": 35,
      "max": 70,
      "distribution": "population_based"
    },
    "sex": {
      "distribution": "population_based",
      "expected": {
        "male": 0.48,
        "female": 0.52
      }
    },
    "race_ethnicity": {
      "distribution": "population_based",
      "minimum_diversity": {
        "hispanic_pct": 0.40
      },
      "expected": {
        "hispanic": 0.54,
        "black_nh": 0.24,
        "white_nh": 0.15,
        "asian_nh": 0.05,
        "other_nh": 0.02
      }
    }
  },
  
  "clinical_profile": {
    "conditions": {
      "type_2_diabetes": {
        "icd10": ["E11.9", "E11.65", "E11.21", "E11.22", "E11.40"],
        "prevalence": 1.0,
        "required": true,
        "onset_range_years": {"min": 1, "max": 15}
      },
      "hypertension": {
        "icd10": ["I10", "I11.9"],
        "prevalence": 0.50,
        "required": false
      },
      "obesity": {
        "icd10": ["E66.01", "E66.9"],
        "prevalence": 0.45,
        "required": false
      },
      "hyperlipidemia": {
        "icd10": ["E78.5", "E78.00"],
        "prevalence": 0.55,
        "required": false
      }
    },
    
    "comorbidity_rules": {
      "diabetes_hypertension": 0.50,
      "diabetes_obesity": 0.45,
      "diabetes_hyperlipidemia": 0.55,
      "hypertension_obesity": 0.40
    },
    
    "exclusions": [
      {
        "condition": "type_1_diabetes",
        "icd10": ["E10.x"],
        "reason": "Wrong diabetes type"
      },
      {
        "condition": "esrd",
        "icd10": ["N18.6"],
        "reason": "End-stage renal disease"
      },
      {
        "condition": "pregnancy",
        "icd10": ["Z33.x", "O00-O9A"],
        "reason": "Pregnancy exclusion"
      }
    ],
    
    "labs": {
      "hba1c": {
        "loinc": "4548-4",
        "range": {"min": 6.5, "max": 12.0},
        "distribution": "normal",
        "mean": 8.2,
        "sd": 1.4
      }
    }
  },
  
  "sdoh_requirements": {
    "vulnerability_level": "high",
    
    "svi_thresholds": {
      "overall_min": 0.65
    },
    
    "expected_sdoh_profile": {
      "poverty_rate": 0.26,
      "uninsured_rate": 0.25,
      "limited_english": 0.22,
      "no_vehicle": 0.13
    },
    
    "z_code_prevalence": {
      "Z59.6": {
        "target_rate": 0.21,
        "description": "Low income"
      },
      "Z59.41": {
        "target_rate": 0.16,
        "description": "Food insecurity"
      },
      "Z59.7": {
        "target_rate": 0.20,
        "description": "Insufficient social insurance"
      },
      "Z59.82": {
        "target_rate": 0.10,
        "description": "Transportation insecurity"
      },
      "Z60.3": {
        "target_rate": 0.09,
        "description": "Acculturation difficulty"
      }
    }
  },
  
  "size": {
    "target": 1000,
    "type": "exact",
    "tolerance": 0.02,
    
    "stratification": {
      "by": "age_sex_ethnicity",
      "ensure_minimum": 30
    }
  },
  
  "integration": {
    "patientsim": {
      "enabled": true,
      "generate_clinical_data": true,
      "encounter_density": "moderate",
      "encounter_types": ["ambulatory", "ed", "inpatient"],
      "include_labs": true,
      "include_vitals": true,
      "sdoh_z_codes": true,
      "timeframe": {
        "history_years": 3
      }
    },
    "membersim": {
      "enabled": true,
      "plan_distribution": "population_based",
      "generate_claims": true
    },
    "identity_correlation": {
      "ssn_as_correlator": true,
      "generate_mrns": true,
      "mrn_format": "MRN-{sequence:06d}"
    }
  },
  
  "metadata": {
    "created_at": "2024-12-23T10:30:00Z",
    "created_by": "health_equity_researcher",
    "version": "1.0",
    "purpose": "health_equity_analysis",
    "project": "DM-EQUITY-2024",
    "tags": ["diabetes", "health_equity", "high_sdoh", "hispanic"]
  }
}
```

---

### Cohort Summary

```json
{
  "cohort_summary": {
    "cohort_id": "cohort-dm-equity-harris-001",
    
    "population_sourcing": {
      "source_geography": "Harris County, TX",
      "eligible_tracts": 342,
      "tract_population": 1824000,
      "age_eligible": 892000,
      "diabetes_prevalent": 132000,
      "after_exclusions": 118000,
      "meets_sdoh_criteria": 98000
    },
    
    "target_composition": {
      "total": 1000,
      
      "by_age": {
        "35_44": 220,
        "45_54": 280,
        "55_64": 320,
        "65_70": 180
      },
      
      "by_sex": {
        "male": 480,
        "female": 520
      },
      
      "by_ethnicity": {
        "hispanic": 540,
        "black_nh": 240,
        "white_nh": 150,
        "asian_nh": 50,
        "other_nh": 20
      },
      
      "by_insurance": {
        "commercial": 320,
        "medicare": 180,
        "medicaid": 320,
        "uninsured": 180
      }
    },
    
    "clinical_distribution": {
      "diabetes_only": 250,
      "diabetes_hypertension": 350,
      "diabetes_obesity": 280,
      "diabetes_multiple_comorbid": 420
    },
    
    "sdoh_distribution": {
      "with_z_code": 680,
      "avg_z_codes": 1.6,
      "z59_6_low_income": 210,
      "z59_41_food_insecurity": 160,
      "z59_7_uninsured_related": 200
    }
  }
}
```

---

## Key Elements

### Geographic Targeting

- **County**: Harris County (48201)
- **Filter**: SVI ≥ 0.65 (moderate-high to high vulnerability)
- **342 tracts** meet criteria with 1.8M population

### Clinical Criteria

- **Required**: Type 2 diabetes (100%)
- **Common**: Hypertension (50%), Obesity (45%), Hyperlipidemia (55%)
- **Excluded**: Type 1 diabetes, ESRD, Pregnancy

### Diversity Achievement

- **Hispanic**: 54% (exceeds 40% minimum)
- **Black**: 24%
- **Reflects** high-SVI area demographics

### SDOH Integration

- **68%** will have at least one Z-code
- **Average 1.6** Z-codes per patient
- Top codes: Z59.6, Z59.7, Z59.41

---

## Variations

### Trial-Focused Cohort

```
Define a cohort of 500 patients for a diabetes cardiovascular outcomes trial:
- Type 2 diabetes with HbA1c 7.0-10.5%
- Age 40-75
- No heart failure or ESRD
- 40% minority enrollment requirement
- Multi-site: Houston, Dallas, San Antonio
```

### Pediatric Cohort

```
Define a cohort of 200 pediatric asthma patients:
- Age 5-17
- Asthma diagnosis
- From low-income areas (poverty rate ≥ 20%)
- Include Medicaid enrollment
```

### Elderly Cohort

```
Define a cohort of 1,500 Medicare beneficiaries:
- Age 65+
- Multiple chronic conditions (≥3)
- Include dual-eligible at population rate
- High utilization risk
```

---

## Next Steps

- Generate patients using PatientSim with this cohort
- Create claims data using MemberSim integration
- Assess [trial feasibility](04-trial-feasibility.md) for clinical research
