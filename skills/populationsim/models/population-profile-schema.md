---
name: population-profile-schema
description: >
  Complete schema definition for PopulationProfile - the core model representing
  geographic population characteristics in PopulationSim.
---

# PopulationProfile Schema

## Overview

PopulationProfile is the foundational model for PopulationSim, representing the complete demographic, health, and social characteristics of a geographic area. It combines data from Census ACS, CDC PLACES, CDC SVI, and other sources into a unified structure.

---

## Complete Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://healthsim.io/schemas/population-profile-v1",
  "title": "PopulationProfile",
  "description": "Complete population characteristics for a geographic area",
  "type": "object",
  "required": ["profile_id", "geography", "demographics", "metadata"],
  
  "properties": {
    "profile_id": {
      "type": "string",
      "description": "Unique identifier for this profile",
      "pattern": "^[a-z0-9_-]+$"
    },
    
    "geography": {
      "type": "object",
      "required": ["type", "name"],
      "properties": {
        "type": {
          "type": "string",
          "enum": ["nation", "region", "division", "state", "county", "tract", "block_group", "msa", "custom"]
        },
        "fips": { "type": "string" },
        "name": { "type": "string" },
        "state": { "type": "string" },
        "state_fips": { "type": "string", "pattern": "^[0-9]{2}$" },
        "county_fips": { "type": "string", "pattern": "^[0-9]{5}$" },
        "tract_fips": { "type": "string", "pattern": "^[0-9]{11}$" },
        "cbsa_code": { "type": "string", "pattern": "^[0-9]{5}$" },
        "cbsa_name": { "type": "string" },
        "cbsa_type": { "type": "string", "enum": ["metro", "micro"] },
        "population": { "type": "integer", "minimum": 0 },
        "households": { "type": "integer", "minimum": 0 },
        "land_area_sq_mi": { "type": "number", "minimum": 0 },
        "population_density": { "type": "number", "minimum": 0 },
        "urban_rural": { "type": "string", "enum": ["urban", "suburban", "rural"] }
      }
    },
    
    "demographics": {
      "type": "object",
      "properties": {
        "total_population": { "type": "integer", "minimum": 0 },
        "age": {
          "type": "object",
          "properties": {
            "min": { "type": "integer", "minimum": 0 },
            "max": { "type": "integer", "maximum": 120 },
            "mean": { "type": "number" },
            "median": { "type": "number" },
            "distribution": {
              "type": "object",
              "additionalProperties": { "type": "number", "minimum": 0, "maximum": 1 }
            }
          }
        },
        "sex": {
          "type": "object",
          "properties": {
            "male": { "type": "number", "minimum": 0, "maximum": 1 },
            "female": { "type": "number", "minimum": 0, "maximum": 1 }
          }
        },
        "race_ethnicity": {
          "type": "object",
          "properties": {
            "white_nh": { "type": "number" },
            "black": { "type": "number" },
            "hispanic": { "type": "number" },
            "asian": { "type": "number" },
            "aian": { "type": "number" },
            "nhpi": { "type": "number" },
            "two_or_more": { "type": "number" },
            "other": { "type": "number" }
          }
        }
      }
    },
    
    "health_indicators": {
      "type": "object",
      "properties": {
        "source": { "type": "string" },
        "source_year": { "type": "integer" },
        "outcomes": {
          "type": "object",
          "properties": {
            "diabetes": { "$ref": "#/$defs/healthMeasure" },
            "obesity": { "$ref": "#/$defs/healthMeasure" },
            "hypertension": { "$ref": "#/$defs/healthMeasure" },
            "chd": { "$ref": "#/$defs/healthMeasure" },
            "stroke": { "$ref": "#/$defs/healthMeasure" },
            "copd": { "$ref": "#/$defs/healthMeasure" },
            "asthma": { "$ref": "#/$defs/healthMeasure" },
            "cancer": { "$ref": "#/$defs/healthMeasure" },
            "kidney": { "$ref": "#/$defs/healthMeasure" },
            "depression": { "$ref": "#/$defs/healthMeasure" },
            "disability": { "$ref": "#/$defs/healthMeasure" }
          }
        },
        "behaviors": {
          "type": "object",
          "properties": {
            "smoking": { "$ref": "#/$defs/healthMeasure" },
            "obesity": { "$ref": "#/$defs/healthMeasure" },
            "physical_inactivity": { "$ref": "#/$defs/healthMeasure" },
            "binge_drinking": { "$ref": "#/$defs/healthMeasure" },
            "short_sleep": { "$ref": "#/$defs/healthMeasure" }
          }
        },
        "prevention": {
          "type": "object",
          "properties": {
            "checkup": { "$ref": "#/$defs/healthMeasure" },
            "dental": { "$ref": "#/$defs/healthMeasure" },
            "cholesterol_screening": { "$ref": "#/$defs/healthMeasure" },
            "mammography": { "$ref": "#/$defs/healthMeasure" },
            "colorectal_screening": { "$ref": "#/$defs/healthMeasure" },
            "bp_medication": { "$ref": "#/$defs/healthMeasure" }
          }
        }
      }
    },
    
    "sdoh_indices": {
      "type": "object",
      "properties": {
        "svi": {
          "type": "object",
          "properties": {
            "overall": { "type": "number", "minimum": 0, "maximum": 1 },
            "theme1_socioeconomic": { "type": "number", "minimum": 0, "maximum": 1 },
            "theme2_household": { "type": "number", "minimum": 0, "maximum": 1 },
            "theme3_minority": { "type": "number", "minimum": 0, "maximum": 1 },
            "theme4_housing": { "type": "number", "minimum": 0, "maximum": 1 }
          }
        },
        "adi": {
          "type": "object",
          "properties": {
            "national_percentile": { "type": "integer", "minimum": 1, "maximum": 100 },
            "state_decile": { "type": "integer", "minimum": 1, "maximum": 10 }
          }
        },
        "economic": {
          "type": "object",
          "properties": {
            "median_household_income": { "type": "number" },
            "per_capita_income": { "type": "number" },
            "poverty_rate": { "type": "number", "minimum": 0, "maximum": 1 },
            "unemployment_rate": { "type": "number", "minimum": 0, "maximum": 1 },
            "gini_coefficient": { "type": "number", "minimum": 0, "maximum": 1 }
          }
        },
        "education": {
          "type": "object",
          "properties": {
            "no_hs_diploma": { "type": "number", "minimum": 0, "maximum": 1 },
            "bachelors_or_higher": { "type": "number", "minimum": 0, "maximum": 1 }
          }
        },
        "housing": {
          "type": "object",
          "properties": {
            "owner_occupied": { "type": "number" },
            "median_home_value": { "type": "number" },
            "median_rent": { "type": "number" },
            "cost_burden": { "type": "number" },
            "no_vehicle": { "type": "number" }
          }
        }
      }
    },
    
    "healthcare_access": {
      "type": "object",
      "properties": {
        "insurance_coverage": {
          "type": "object",
          "properties": {
            "total_insured": { "type": "number" },
            "uninsured": { "type": "number" },
            "employer": { "type": "number" },
            "medicaid": { "type": "number" },
            "medicare": { "type": "number" },
            "individual": { "type": "number" }
          }
        },
        "provider_availability": {
          "type": "object",
          "properties": {
            "pcp_per_100k": { "type": "number" },
            "specialist_per_100k": { "type": "number" },
            "hospital_beds_per_100k": { "type": "number" },
            "mental_health_per_100k": { "type": "number" }
          }
        },
        "hpsa_status": {
          "type": "object",
          "properties": {
            "primary_care": { "type": "boolean" },
            "mental_health": { "type": "boolean" },
            "dental": { "type": "boolean" }
          }
        }
      }
    },
    
    "comparison": {
      "type": "object",
      "properties": {
        "benchmark": { "type": "string" },
        "benchmark_type": { "type": "string", "enum": ["state", "national", "peer"] },
        "metrics": {
          "type": "object",
          "additionalProperties": {
            "type": "object",
            "properties": {
              "value": { "type": "number" },
              "benchmark_value": { "type": "number" },
              "difference": { "type": "number" },
              "percentile": { "type": "number" }
            }
          }
        }
      }
    },
    
    "metadata": {
      "type": "object",
      "required": ["generated_at", "version"],
      "properties": {
        "generated_at": { "type": "string", "format": "date-time" },
        "version": { "type": "string" },
        "data_sources": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "name": { "type": "string" },
              "version": { "type": "string" },
              "reference_year": { "type": "integer" }
            }
          }
        },
        "reliability": { "type": "string", "enum": ["high", "moderate", "low"] },
        "notes": { "type": "string" }
      }
    }
  },
  
  "$defs": {
    "healthMeasure": {
      "type": "object",
      "properties": {
        "rate": { "type": "number", "minimum": 0, "maximum": 1 },
        "ci_low": { "type": "number" },
        "ci_high": { "type": "number" },
        "reliable": { "type": "boolean" }
      }
    }
  }
}
```

---

## Example Instance

```json
{
  "profile_id": "harris_county_tx_2024",
  "geography": {
    "type": "county",
    "fips": "48201",
    "name": "Harris County",
    "state": "TX",
    "state_fips": "48",
    "cbsa_code": "26420",
    "cbsa_name": "Houston-The Woodlands-Sugar Land, TX",
    "population": 4731145,
    "households": 1672845,
    "land_area_sq_mi": 1729.2,
    "urban_rural": "urban"
  },
  "demographics": {
    "total_population": 4731145,
    "age": {
      "mean": 34.2,
      "median": 33.5,
      "distribution": {
        "0-17": 0.24,
        "18-44": 0.38,
        "45-64": 0.24,
        "65+": 0.14
      }
    },
    "sex": { "male": 0.49, "female": 0.51 },
    "race_ethnicity": {
      "white_nh": 0.28,
      "black": 0.20,
      "hispanic": 0.44,
      "asian": 0.07,
      "other": 0.01
    }
  },
  "health_indicators": {
    "source": "CDC_PLACES_2024",
    "outcomes": {
      "diabetes": { "rate": 0.108, "reliable": true },
      "obesity": { "rate": 0.328, "reliable": true },
      "hypertension": { "rate": 0.324, "reliable": true }
    }
  },
  "sdoh_indices": {
    "svi": { "overall": 0.68, "theme1_socioeconomic": 0.62 },
    "economic": {
      "median_household_income": 62320,
      "poverty_rate": 0.158
    }
  },
  "metadata": {
    "generated_at": "2024-12-23T10:00:00Z",
    "version": "1.0",
    "reliability": "high"
  }
}
```

---

## Related Schemas

- [CohortSpecification](cohort-specification-schema.md) - Uses PopulationProfile as input
- [CrossProductIntegration](cross-product-integration.md) - Product mapping
