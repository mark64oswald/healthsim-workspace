# PopulationSim Integration for RxMemberSim

PopulationSim v2.0 provides **embedded real-world data** for realistic medication utilization modeling. When a geography is specified, RxMemberSim uses actual CDC PLACES, SVI, and ADI data to ground prescribing patterns, adherence behaviors, and formulary utilization.

## Data-Driven Generation Pattern

**Step 1: Look up real population data**
```
# For rural Appalachian county - Pike County, KY (FIPS: 21195)
Read from: skills/populationsim/data/county/places_county_2024.csv
-> DIABETES_CrudePrev: 16.8%
-> BPMED_CrudePrev: 62.1% (on BP medication)
-> ACCESS2_CrudePrev: 9.1% (uninsured)

Read from: skills/populationsim/data/county/svi_county_2022.csv
-> RPL_THEMES (overall SVI): 0.91 (very high vulnerability)
-> EP_POV150: 38.2% (below 150% poverty)
-> EP_NOVEH: 8.4% (no vehicle - affects pharmacy access)
```

**Step 2: Apply rates to pharmacy generation**
```json
{
  "cohort_parameters": {
    "geography": { "county_fips": "21195", "name": "Pike County, KY" },
    "expected_drug_classes": {
      "antidiabetics": 0.168,
      "antihypertensives": 0.621
    },
    "adherence_context": {
      "svi_overall": 0.91,
      "transportation_barrier": 0.084,
      "poverty_rate": 0.382
    },
    "data_provenance": {
      "source": "CDC_PLACES_2024",
      "data_year": 2022
    }
  }
}
```

**Step 3: Generate pharmacy claims matching real patterns**
- ~17% of members on antidiabetics (not generic 10%)
- High SVI -> higher generic utilization (cost sensitivity)
- Transportation barriers -> more mail-order, 90-day fills
- Lower adherence rates (MPR ~0.70 vs 0.80 baseline)

## Embedded Data Sources for Rx Patterns

| Source | File | Use in RxMemberSim |
|--------|------|-------------------|
| CDC PLACES County | `populationsim/data/county/places_county_2024.csv` | Medication class utilization (BPMED, etc.) |
| CDC PLACES Tract | `populationsim/data/tract/places_tract_2024.csv` | Neighborhood prescribing patterns |
| SVI County | `populationsim/data/county/svi_county_2022.csv` | Adherence modeling, generic preference |
| SVI Tract | `populationsim/data/tract/svi_tract_2022.csv` | Pharmacy access patterns |
| ADI Block Group | `populationsim/data/block_group/adi_blockgroup_2023.csv` | Deprivation -> adherence correlation |

## SDOH Impact on Pharmacy Utilization

| SDOH Factor | Pharmacy Impact | Data Source |
|-------------|-----------------|-------------|
| High SVI (>0.75) | +15% generic utilization, -15% adherence | SVI RPL_THEMES |
| No vehicle (EP_NOVEH) | +20% mail-order preference | SVI tract data |
| High poverty (EP_POV150) | Higher copay card utilization | SVI county data |
| High ADI (>75 percentile) | More early refill rejections | ADI block group |

## Example: Data-Grounded Diabetic Pharmacy Claims

**Request:** "Generate pharmacy claims for a diabetic population in Pike County, KY"

**Data Lookup:**
```
From places_county_2024.csv (FIPS 21195):
  DIABETES_CrudePrev: 16.8%
  OBESITY_CrudePrev: 41.2%
  BPMED_CrudePrev: 62.1%

From svi_county_2022.csv (FIPS 21195):
  RPL_THEMES: 0.91 (very high vulnerability)
  EP_POV150: 38.2%
  EP_NOVEH: 8.4%
```

**Applied to Generation:**
- Drug mix: 70% metformin (generic), 20% sulfonylureas, 10% GLP-1/SGLT2
- Adherence: MPR ~0.68 (below national average due to high SVI)
- Channel: 65% retail, 35% mail-order (transport barriers)
- Copay programs: 25% utilizing manufacturer assistance

**Output with Provenance:**
```json
{
  "pharmacy_claims": [ ... ],
  "generation_context": {
    "geography": "Pike County, KY (21195)",
    "data_sources": ["CDC_PLACES_2024", "CDC_SVI_2022"],
    "rates_applied": {
      "diabetes_prevalence": 0.168,
      "svi_adherence_modifier": -0.15
    }
  }
}
```

> **Key Principle:** When geography is specified, ground pharmacy claims in real PopulationSim data. This enables realistic medication adherence modeling, generic utilization patterns, and SDOH-influenced pharmacy access behaviors.
