# Example 04: Trial Feasibility Assessment

## Objective

Assess clinical trial feasibility using PopulationSim to analyze catchment areas, estimate eligible populations, plan for diversity requirements, and model enrollment.

---

## Prompt

```
Assess feasibility for a Phase 3 Type 2 diabetes cardiovascular outcomes trial:
- Target enrollment: 500 subjects
- Sites: Houston (Texas Medical Center), Dallas (UT Southwestern), San Antonio (UT Health)
- Eligibility: Type 2 diabetes, age 40-75, HbA1c 7.0-10.5%
- Exclusions: Heart failure NYHA IV, ESRD, active cancer
- Diversity: 40% minority, 25% age 65+, 50% female
- Include SDOH diversity targets: 25% from high-vulnerability areas
```

---

## Expected Output

### Feasibility Assessment

```json
{
  "assessment_id": "feasibility-dm-cv-001",
  "protocol_id": "DM-CARDIO-2024-001",
  "assessment_date": "2024-12-23",
  
  "protocol_summary": {
    "title": "Cardiovascular Outcomes in Type 2 Diabetes",
    "phase": "3",
    "target_enrollment": 500,
    "enrollment_window_months": 18,
    
    "eligibility": {
      "inclusion": {
        "diagnosis": "Type 2 diabetes (E11.x)",
        "age": {"min": 40, "max": 75},
        "hba1c": {"min": 7.0, "max": 10.5}
      },
      "exclusion": [
        "Heart failure NYHA Class IV",
        "ESRD (eGFR < 15 or dialysis)",
        "Active malignancy"
      ]
    },
    
    "diversity_requirements": {
      "minority": 0.40,
      "elderly_65_plus": 0.25,
      "female": 0.50,
      "high_sdoh": 0.25
    }
  },
  
  "site_assessments": [
    {
      "site_id": "SITE-001",
      "name": "Texas Medical Center - Houston",
      "geography": {
        "fips": "48201",
        "county": "Harris County",
        "catchment_radius_miles": 30
      },
      
      "catchment_profile": {
        "total_population": 4731145,
        "age_eligible_40_75": 1842000,
        "with_diabetes": 206300,
        "hba1c_in_range_estimate": 123800,
        "after_exclusions": 111400,
        "final_eligible_pool": 111400
      },
      
      "diversity_profile": {
        "race_ethnicity": {
          "white_nh": 0.288,
          "black_nh": 0.198,
          "hispanic": 0.438,
          "asian_nh": 0.078
        },
        "minority_pct": 0.712,
        "age_65_plus_in_eligible": 0.32,
        "female_pct": 0.52,
        "high_sdoh_pct": 0.33
      },
      
      "enrollment_projection": {
        "monthly_screening_capacity": 45,
        "screen_fail_rate": 0.35,
        "expected_enrollment_per_month": 29,
        "projected_enrollment_18mo": 522,
        "contribution_to_total": 0.44
      },
      
      "feasibility_score": 0.92,
      "feasibility_rating": "HIGH",
      "notes": [
        "Large eligible pool supports strong enrollment",
        "Excellent diversity profile exceeds all targets",
        "High SDOH population may require retention support"
      ]
    },
    {
      "site_id": "SITE-002",
      "name": "UT Southwestern - Dallas",
      "geography": {
        "fips": "48113",
        "county": "Dallas County",
        "catchment_radius_miles": 30
      },
      
      "catchment_profile": {
        "total_population": 2613539,
        "age_eligible_40_75": 1024000,
        "with_diabetes": 112640,
        "hba1c_in_range_estimate": 67584,
        "after_exclusions": 60826,
        "final_eligible_pool": 60826
      },
      
      "diversity_profile": {
        "race_ethnicity": {
          "white_nh": 0.298,
          "black_nh": 0.238,
          "hispanic": 0.402,
          "asian_nh": 0.062
        },
        "minority_pct": 0.702,
        "age_65_plus_in_eligible": 0.28,
        "female_pct": 0.51,
        "high_sdoh_pct": 0.28
      },
      
      "enrollment_projection": {
        "monthly_screening_capacity": 35,
        "screen_fail_rate": 0.32,
        "expected_enrollment_per_month": 24,
        "projected_enrollment_18mo": 432,
        "contribution_to_total": 0.36
      },
      
      "feasibility_score": 0.85,
      "feasibility_rating": "HIGH",
      "notes": [
        "Strong eligible pool",
        "Good diversity profile",
        "Academic center provides research infrastructure"
      ]
    },
    {
      "site_id": "SITE-003",
      "name": "UT Health San Antonio",
      "geography": {
        "fips": "48029",
        "county": "Bexar County",
        "catchment_radius_miles": 30
      },
      
      "catchment_profile": {
        "total_population": 2009324,
        "age_eligible_40_75": 782000,
        "with_diabetes": 93840,
        "hba1c_in_range_estimate": 56304,
        "after_exclusions": 50674,
        "final_eligible_pool": 50674
      },
      
      "diversity_profile": {
        "race_ethnicity": {
          "white_nh": 0.268,
          "black_nh": 0.068,
          "hispanic": 0.612,
          "asian_nh": 0.028
        },
        "minority_pct": 0.732,
        "age_65_plus_in_eligible": 0.26,
        "female_pct": 0.52,
        "high_sdoh_pct": 0.25
      },
      
      "enrollment_projection": {
        "monthly_screening_capacity": 25,
        "screen_fail_rate": 0.30,
        "expected_enrollment_per_month": 18,
        "projected_enrollment_18mo": 324,
        "contribution_to_total": 0.27
      },
      
      "feasibility_score": 0.78,
      "feasibility_rating": "MODERATE-HIGH",
      "notes": [
        "Excellent Hispanic representation",
        "Smaller but sufficient eligible pool",
        "Strong community engagement history"
      ]
    }
  ],
  
  "aggregate_assessment": {
    "total_eligible_pool": 222900,
    "combined_enrollment_projection": 1278,
    "enrollment_target_achievable": true,
    "projected_time_to_target": 14,
    
    "diversity_achievability": {
      "minority": {
        "target": 0.40,
        "projected": 0.71,
        "achievable": true,
        "status": "EXCEEDS"
      },
      "elderly_65_plus": {
        "target": 0.25,
        "projected": 0.29,
        "achievable": true,
        "status": "MEETS"
      },
      "female": {
        "target": 0.50,
        "projected": 0.52,
        "achievable": true,
        "status": "MEETS"
      },
      "high_sdoh": {
        "target": 0.25,
        "projected": 0.29,
        "achievable": true,
        "status": "MEETS"
      }
    },
    
    "overall_feasibility": "HIGH",
    "confidence_score": 0.88
  },
  
  "sdoh_considerations": {
    "high_vulnerability_enrollment": {
      "target_subjects": 125,
      "available_pool": 64500,
      "feasibility": "HIGH"
    },
    
    "retention_risk_factors": {
      "transportation_insecurity": {
        "prevalence": 0.11,
        "impact": "Missed visits",
        "mitigation": "Transportation stipend ($50/visit)"
      },
      "food_insecurity": {
        "prevalence": 0.14,
        "impact": "Protocol adherence",
        "mitigation": "Meal provision at visits"
      },
      "employment_constraints": {
        "prevalence": 0.38,
        "impact": "Scheduling conflicts",
        "mitigation": "Weekend/evening availability"
      },
      "limited_english": {
        "prevalence": 0.19,
        "impact": "Informed consent, compliance",
        "mitigation": "Bilingual coordinators, translated materials"
      }
    },
    
    "retention_projection": {
      "baseline_12mo_retention": 0.85,
      "sdoh_adjusted_retention": 0.78,
      "recommended_over_enrollment": 1.28
    }
  },
  
  "enrollment_timeline": {
    "months": [
      {"month": 1, "screened": 105, "enrolled": 68},
      {"month": 3, "screened": 315, "enrolled": 204, "cumulative": 204},
      {"month": 6, "screened": 630, "enrolled": 409, "cumulative": 409},
      {"month": 9, "screened": 945, "enrolled": 614, "cumulative": 500},
      {"month": 12, "screened": 1260, "enrolled": 819, "cumulative": 500},
      {"month": 14, "screened": 1470, "enrolled": 955, "cumulative": 500}
    ],
    "target_met_month": 9,
    "buffer_subjects": 114
  },
  
  "recommendations": [
    {
      "priority": "HIGH",
      "recommendation": "Proceed with all three sites",
      "rationale": "Combined eligible pool and enrollment capacity exceed requirements"
    },
    {
      "priority": "HIGH",
      "recommendation": "Implement enhanced retention program",
      "rationale": "29% high-SDOH population requires proactive support",
      "actions": [
        "Transportation reimbursement ($50/visit)",
        "Flexible scheduling (evenings/weekends)",
        "Reminder calls in preferred language"
      ]
    },
    {
      "priority": "MEDIUM",
      "recommendation": "Deploy bilingual study coordinators",
      "rationale": "19% limited English speakers across catchment",
      "actions": [
        "Spanish-speaking coordinator at each site",
        "Translated consent forms and materials"
      ]
    },
    {
      "priority": "MEDIUM",
      "recommendation": "Consider mobile/home visit option",
      "rationale": "11% transportation insecure population",
      "actions": [
        "Home visit capability for select assessments",
        "Partnership with community health workers"
      ]
    },
    {
      "priority": "LOW",
      "recommendation": "Budget for retention incentives",
      "rationale": "Improve completion rates in high-SDOH subjects",
      "actions": [
        "Completion bonuses at milestones",
        "Gift cards for visit attendance"
      ]
    }
  ],
  
  "metadata": {
    "generated_at": "2024-12-23T10:30:00Z",
    "populationsim_version": "1.0",
    "data_sources": {
      "demographics": "ACS 2018-2022",
      "health": "CDC PLACES 2024",
      "sdoh": "SVI 2022"
    }
  }
}
```

---

## Key Findings

### Overall Feasibility: HIGH (88% confidence)

- **Target**: 500 subjects
- **Combined eligible pool**: 222,900
- **Projected enrollment capacity**: 1,278 (18 months)
- **Time to target**: ~9 months (well within 18-month window)

### Site Comparison

| Site | Eligible Pool | Monthly Enrollment | Diversity Score |
|------|---------------|-------------------|-----------------|
| Houston TMC | 111,400 | 29 | 0.92 |
| Dallas UTSW | 60,826 | 24 | 0.85 |
| San Antonio UTH | 50,674 | 18 | 0.78 |

### Diversity Achievement

| Metric | Target | Projected | Status |
|--------|--------|-----------|--------|
| Minority | 40% | 71% | ✅ Exceeds |
| Age 65+ | 25% | 29% | ✅ Meets |
| Female | 50% | 52% | ✅ Meets |
| High-SDOH | 25% | 29% | ✅ Meets |

### SDOH Considerations

- **29%** of potential enrollees from high-vulnerability areas
- **Key risks**: Transportation (11%), Food (14%), Language (19%)
- **Recommended over-enrollment**: 28% to account for retention challenges

---

## Variations

### Single-Site Assessment

```
Assess trial feasibility for a diabetes study at Houston Methodist Hospital 
with 25-mile catchment radius
```

### Multi-State Trial

```
Assess feasibility for a national diabetes trial with sites in 
TX, CA, FL, NY, and IL - target 2,000 subjects
```

### Rare Disease

```
Assess feasibility for a rare disease trial (prevalence 1:50,000) 
across Texas academic medical centers
```

---

## Next Steps

- Use TrialSim to simulate screening and enrollment
- Generate synthetic subject demographics
- Model retention scenarios with SDOH adjustments
