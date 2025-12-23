# Example 01: Basic Population Profile

## Objective

Generate a comprehensive population profile for a county, demonstrating PopulationSim's core demographic and health indicator capabilities.

---

## Prompt

```
Create a population profile for Harris County, Texas
```

---

## Expected Output

### PopulationProfile

```json
{
  "profile_id": "pop-48201-2024-001",
  
  "geography": {
    "type": "county",
    "fips": "48201",
    "geoid": "48201",
    "name": "Harris County",
    "full_name": "Harris County, Texas",
    "state_fips": "48",
    "state_abbr": "TX",
    "cbsa_code": "26420",
    "cbsa_name": "Houston-The Woodlands-Sugar Land, TX"
  },
  
  "demographics": {
    "total_population": 4731145,
    
    "age_distribution": {
      "0_4": 0.068,
      "5_17": 0.172,
      "18_24": 0.092,
      "25_34": 0.158,
      "35_44": 0.142,
      "45_54": 0.128,
      "55_64": 0.112,
      "65_74": 0.078,
      "75_plus": 0.050
    },
    
    "sex_distribution": {
      "male": 0.498,
      "female": 0.502
    },
    
    "race_ethnicity": {
      "white_nh": 0.288,
      "black_nh": 0.198,
      "hispanic": 0.438,
      "asian_nh": 0.078,
      "aian_nh": 0.003,
      "nhpi_nh": 0.001,
      "multiracial_nh": 0.014
    },
    
    "median_age": 33.4,
    
    "household_composition": {
      "average_household_size": 2.78,
      "family_households": 0.682,
      "single_person": 0.242
    }
  },
  
  "health_indicators": {
    "source": "CDC_PLACES_2024",
    "data_year": 2022,
    
    "chronic_conditions": {
      "diabetes": 0.112,
      "obesity": 0.328,
      "hypertension": 0.342,
      "chd": 0.058,
      "copd": 0.062,
      "depression": 0.188,
      "asthma": 0.098,
      "ckd": 0.032,
      "stroke": 0.034,
      "arthritis": 0.248
    },
    
    "health_behaviors": {
      "current_smoking": 0.142,
      "physical_inactivity": 0.268,
      "binge_drinking": 0.172,
      "short_sleep": 0.378
    },
    
    "prevention": {
      "annual_checkup": 0.768,
      "cholesterol_screening": 0.872,
      "dental_visit": 0.642
    }
  },
  
  "sdoh_profile": {
    "svi": {
      "overall": 0.58,
      "theme_1_socioeconomic": 0.54,
      "theme_2_household_disability": 0.48,
      "theme_3_minority_language": 0.72,
      "theme_4_housing_transportation": 0.62
    },
    
    "economic": {
      "median_household_income": 58100,
      "poverty_rate": 0.158,
      "unemployment_rate": 0.058,
      "uninsured_rate": 0.168
    }
  },
  
  "healthcare_access": {
    "insurance_coverage": {
      "commercial": 0.508,
      "medicare": 0.138,
      "medicaid": 0.188,
      "uninsured": 0.166
    }
  },
  
  "metadata": {
    "created_at": "2024-12-23T10:30:00Z",
    "version": "1.0",
    "data_sources": {
      "demographics": {"source": "ACS_5YR", "vintage": "2018-2022"},
      "health": {"source": "CDC_PLACES", "data_year": 2022},
      "svi": {"source": "CDC_ATSDR_SVI", "version": "2022"}
    }
  }
}
```

---

## Key Insights from Output

### Demographics

- **Population**: Nearly 4.8 million - largest county in Texas
- **Young population**: Median age 33.4 years
- **Diverse**: 43.8% Hispanic, 19.8% Black, 28.8% White non-Hispanic
- **Family-oriented**: 68% family households

### Health Indicators

- **Diabetes**: 11.2% prevalence (above national average of 10.1%)
- **Obesity**: 32.8% (slightly above national 32.1%)
- **Hypertension**: 34.2% (above national 32.4%)
- **Smoking**: 14.2% (below national 16.0%)

### SDOH

- **Overall SVI**: 0.58 (moderate-high vulnerability)
- **Highest theme**: Minority/Language (0.72)
- **Poverty rate**: 15.8%
- **Uninsured**: 16.6% (higher than national average)

---

## Variations

### Different County

```
Create a population profile for Los Angeles County, California
```

### State Level

```
Create a state-level population profile for Texas
```

### MSA Level

```
Create a population profile for the Houston-The Woodlands-Sugar Land MSA
```

---

## Next Steps

- Try [SDOH Analysis](02-sdoh-analysis.md) for deeper vulnerability assessment
- Define a [cohort](03-cohort-definition.md) based on this profile
- See [trial feasibility](04-trial-feasibility.md) for clinical research use
