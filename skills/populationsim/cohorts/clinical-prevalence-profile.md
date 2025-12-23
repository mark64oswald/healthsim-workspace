---
name: clinical-prevalence-profile
description: >
  Build clinical profiles with disease prevalence, comorbidity patterns, and
  severity distributions for cohorts. Combines CDC PLACES data with clinical
  evidence for realistic disease patterns. Triggers: "clinical profile",
  "comorbidity rates", "disease prevalence for cohort", "condition patterns".
---

# Clinical Prevalence Profile Skill

## Overview

The clinical-prevalence-profile skill creates comprehensive clinical characterizations for cohorts, including primary condition prevalence, comorbidity patterns, severity distributions, and expected medication use. It draws from CDC PLACES data and clinical literature to produce realistic disease patterns.

**Primary Use Cases**:
- Define disease cohort clinical characteristics
- Set realistic comorbidity rates
- Establish severity distributions
- Guide medication assignment

---

## Trigger Phrases

- "Clinical profile for [condition] cohort"
- "What comorbidities for diabetics?"
- "Comorbidity rates for [condition]"
- "Severity distribution for [disease]"
- "Disease patterns in [geography]"

---

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `primary_condition` | string | Yes | - | ICD-10 code or condition name |
| `geography` | string | No | "national" | Geographic context |
| `age_range` | array | No | [18, 100] | Age range for rates |
| `severity_detail` | bool | No | true | Include severity breakdown |

---

## Common Condition Profiles

### Type 2 Diabetes (E11)

**Comorbidity Rates**:
| Condition | ICD-10 | Rate | Correlation |
|-----------|--------|------|-------------|
| Hypertension | I10 | 71% | Very High |
| Hyperlipidemia | E78 | 68% | Very High |
| Obesity | E66 | 62% | Very High |
| CKD | N18 | 25% | High |
| Depression | F32 | 28% | Moderate |
| CAD | I25 | 18% | Moderate |
| Neuropathy | G62 | 22% | High |
| Retinopathy | H35.0 | 18% | High |
| Heart Failure | I50 | 12% | Moderate |

**Severity Distribution**:
| Severity | ICD-10 Codes | Rate |
|----------|--------------|------|
| Without complications | E11.9 | 35% |
| With kidney | E11.2x | 18% |
| With ophthalmic | E11.3x | 12% |
| With neurological | E11.4x | 15% |
| With circulatory | E11.5x | 8% |
| With multiple | E11.65 | 12% |

### Heart Failure (I50)

**Comorbidity Rates**:
| Condition | ICD-10 | Rate | Correlation |
|-----------|--------|------|-------------|
| Hypertension | I10 | 82% | Very High |
| CAD | I25 | 58% | Very High |
| Atrial Fibrillation | I48 | 42% | High |
| Diabetes | E11 | 42% | High |
| CKD | N18 | 48% | Very High |
| COPD | J44 | 28% | Moderate |
| Depression | F32 | 24% | Moderate |
| Anemia | D64 | 32% | High |

**Severity Distribution**:
| Type | ICD-10 | Rate |
|------|--------|------|
| HFrEF (systolic) | I50.2x | 45% |
| HFpEF (diastolic) | I50.3x | 40% |
| Combined | I50.4x | 10% |
| Unspecified | I50.9 | 5% |

### COPD (J44)

**Comorbidity Rates**:
| Condition | ICD-10 | Rate |
|-----------|--------|------|
| Hypertension | I10 | 52% |
| CAD | I25 | 28% |
| Heart Failure | I50 | 24% |
| Diabetes | E11 | 22% |
| Depression | F32 | 38% |
| Anxiety | F41 | 32% |
| Osteoporosis | M81 | 28% |
| Lung Cancer | C34 | 8% |

### Depression (F32)

**Comorbidity Rates**:
| Condition | ICD-10 | Rate |
|-----------|--------|------|
| Anxiety | F41 | 62% |
| Chronic Pain | G89 | 45% |
| Insomnia | G47 | 48% |
| Diabetes | E11 | 18% |
| CAD | I25 | 12% |
| Obesity | E66 | 28% |
| Substance Use | F10-F19 | 22% |

---

## Output Schema

```json
{
  "clinical_profile": {
    "primary_condition": {
      "code": "E11",
      "name": "Type 2 Diabetes Mellitus",
      "category": "endocrine",
      "prevalence_source": 1.0
    },
    
    "severity_distribution": {
      "mild": {
        "codes": ["E11.9"],
        "rate": 0.35,
        "description": "Without complications, controlled"
      },
      "moderate": {
        "codes": ["E11.21", "E11.311", "E11.42"],
        "rate": 0.45,
        "description": "Single organ involvement"
      },
      "severe": {
        "codes": ["E11.65", "E11.52"],
        "rate": 0.20,
        "description": "Multiple complications"
      }
    },
    
    "comorbidities": {
      "very_high_correlation": [
        {
          "code": "I10",
          "name": "Essential Hypertension",
          "rate": 0.71,
          "evidence": "NHANES, Framingham"
        },
        {
          "code": "E78.5",
          "name": "Hyperlipidemia, unspecified",
          "rate": 0.68,
          "evidence": "NHANES, ADA guidelines"
        }
      ],
      "high_correlation": [
        {
          "code": "E66.9",
          "name": "Obesity, unspecified",
          "rate": 0.62,
          "evidence": "CDC obesity-diabetes link"
        },
        {
          "code": "N18.3",
          "name": "CKD Stage 3",
          "rate": 0.18,
          "evidence": "USRDS, diabetic nephropathy"
        }
      ],
      "moderate_correlation": [
        {
          "code": "F32.9",
          "name": "Major depressive disorder",
          "rate": 0.28,
          "evidence": "Depression-diabetes bidirectional"
        },
        {
          "code": "I25.10",
          "name": "CAD without angina",
          "rate": 0.14,
          "evidence": "Cardiovascular risk"
        }
      ]
    },
    
    "multimorbidity_distribution": {
      "primary_only": 0.12,
      "plus_1_comorbidity": 0.24,
      "plus_2_comorbidities": 0.28,
      "plus_3_comorbidities": 0.22,
      "plus_4_or_more": 0.14
    },
    
    "expected_medications": {
      "diabetes_specific": {
        "metformin": 0.72,
        "sulfonylurea": 0.28,
        "sglt2_inhibitor": 0.22,
        "glp1_agonist": 0.18,
        "dpp4_inhibitor": 0.14,
        "insulin_basal": 0.28,
        "insulin_bolus": 0.12
      },
      "comorbidity_related": {
        "ace_inhibitor_arb": 0.68,
        "statin": 0.72,
        "aspirin": 0.42,
        "beta_blocker": 0.24
      }
    },
    
    "lab_patterns": {
      "hba1c": {
        "mean": 7.8,
        "controlled_under_7": 0.42,
        "moderate_7_9": 0.38,
        "uncontrolled_over_9": 0.20
      },
      "egfr": {
        "normal_over_90": 0.45,
        "mild_60_89": 0.30,
        "moderate_30_59": 0.18,
        "severe_under_30": 0.07
      }
    },
    
    "geographic_variation": {
      "geography": "Harris County, TX",
      "vs_national": {
        "diabetes_prevalence": "+2.4%",
        "hypertension_comorbidity": "+3.2%",
        "obesity_comorbidity": "+4.8%"
      }
    }
  },
  
  "validation": {
    "sources": [
      "CDC_PLACES_2024",
      "NHANES_2017-2020",
      "ADA_Standards_2024"
    ],
    "confidence": "high"
  }
}
```

---

## Examples

### Example 1: Diabetes Clinical Profile

**Request**: "Clinical profile for diabetics in South Texas"

**Response**:

**Type 2 Diabetes Clinical Profile - South Texas**

**Primary Condition**: E11 - Type 2 Diabetes Mellitus

**Severity Distribution**:
| Severity | Rate | Typical Codes |
|----------|------|---------------|
| Controlled, no complications | 30% | E11.9 |
| Single complication | 45% | E11.2x, E11.3x, E11.4x |
| Multiple complications | 25% | E11.65 |

*Note: South Texas has higher complication rates than national average (+5%)*

**Top Comorbidities**:
| Condition | Rate | vs National |
|-----------|------|-------------|
| Hypertension (I10) | 74% | +3% |
| Hyperlipidemia (E78) | 68% | - |
| Obesity (E66) | 72% | +10% ⚠️ |
| CKD (N18) | 28% | +3% |
| Depression (F32) | 26% | -2% |
| Retinopathy (H35.0) | 22% | +4% |

**Multimorbidity**:
- Average comorbidities: 3.2
- 4+ conditions: 42% of patients

**Expected Medications**:
| Class | Rate |
|-------|------|
| Metformin | 72% |
| Insulin (any) | 38% |
| SGLT2i | 18% |
| GLP1-RA | 14% |
| ACE/ARB | 72% |
| Statin | 68% |

---

### Example 2: Heart Failure Profile

**Request**: "Comorbidity patterns for heart failure"

**Response**:

**Heart Failure (I50) Comorbidity Profile**

**HF Type Distribution**:
| Type | Rate | Description |
|------|------|-------------|
| HFrEF (I50.2x) | 45% | EF ≤ 40% |
| HFpEF (I50.3x) | 40% | EF ≥ 50% |
| HFmrEF (I50.4x) | 10% | EF 41-49% |
| Unspecified | 5% | I50.9 |

**Comorbidity Cascade**:
```
Heart Failure (I50)
├── Hypertension (I10): 82% ────────────────▶ Near universal
├── CAD (I25): 58% ─────────────────────────▶ Ischemic HF driver
├── CKD (N18): 48% ─────────────────────────▶ Cardiorenal syndrome
├── Atrial Fibrillation (I48): 42% ─────────▶ Rhythm complication
├── Diabetes (E11): 42% ────────────────────▶ Metabolic overlap
├── Anemia (D64): 32% ──────────────────────▶ Outcome modifier
├── COPD (J44): 28% ────────────────────────▶ Shared risk factors
└── Depression (F32): 24% ──────────────────▶ Quality of life
```

**Medication Profile**:
| Category | Medications | Rate |
|----------|-------------|------|
| RAAS inhibition | ACEi/ARB/ARNI | 78% |
| Beta blocker | Carvedilol, metoprolol | 82% |
| Diuretic | Furosemide, bumetanide | 72% |
| MRA | Spironolactone | 42% |
| SGLT2i | Dapagliflozin, empagliflozin | 28% |

---

### Example 3: Multimorbidity Pattern

**Request**: "Generate multimorbidity profile for elderly Medicare population"

**Response**:

**Medicare 65+ Multimorbidity Profile**

**Condition Prevalence** (Medicare 65+):
| Condition | Prevalence |
|-----------|------------|
| Hypertension | 62% |
| Hyperlipidemia | 52% |
| Diabetes | 28% |
| Ischemic Heart Disease | 24% |
| Heart Failure | 14% |
| COPD | 12% |
| CKD | 18% |
| Depression | 16% |
| Atrial Fibrillation | 11% |
| Alzheimer's/Dementia | 12% |

**Multimorbidity Distribution**:
| Conditions | Rate | Cumulative |
|------------|------|------------|
| 0 | 8% | 8% |
| 1 | 14% | 22% |
| 2 | 18% | 40% |
| 3 | 20% | 60% |
| 4 | 16% | 76% |
| 5+ | 24% | 100% |

**Common Clusters**:
1. **Cardiovascular** (42%): HTN + HLD + CAD
2. **Cardiometabolic** (28%): HTN + HLD + DM
3. **Cardiopulmonary** (12%): HTN + HF + COPD
4. **Mental-Physical** (18%): Depression + Chronic Pain + DM

---

## Validation Rules

### Rate Checks
- [ ] All rates between 0 and 1
- [ ] Severity distribution sums to ~1.0
- [ ] Primary condition rate = 1.0 for disease cohort

### Clinical Plausibility
- [ ] Comorbidity rates consistent with literature
- [ ] Medication rates match condition guidelines
- [ ] Geographic variations reasonable

---

## Related Skills

- [cohort-specification.md](cohort-specification.md) - Full cohort
- [chronic-disease-prevalence.md](../health-patterns/chronic-disease-prevalence.md) - Geographic rates
- [demographic-distribution.md](demographic-distribution.md) - Age effects
