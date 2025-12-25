# PopulationSim

> Access real US population data including demographics, disease prevalence, social determinants of health, and geographic health intelligence.

## What PopulationSim Does

PopulationSim is the **data intelligence** engine of HealthSim. Unlike other products that generate synthetic data, PopulationSim provides **access to real CDC and Census data**—148 MB of embedded population statistics covering every US county, census tract, and block group.

This data grounds all other HealthSim products in reality. When you generate a diabetic patient in Harris County, TX, PatientSim uses PopulationSim's actual 12.1% diabetes prevalence rate instead of a generic national average.

## Quick Start

**Data Lookup:**
```
What is the diabetes prevalence in Harris County, TX?
Look up SVI vulnerability scores for San Diego census tracts
```

**Geographic Profiles:**
```
Profile the health indicators for Maricopa County, AZ
Compare chronic disease rates across California metro areas
```

**Cohort Definition:**
```
Build a cohort specification for 500 diabetic patients in Cook County, IL
```

See [hello-healthsim examples](../../hello-healthsim/examples/populationsim-examples.md) for detailed examples with expected outputs.

## Key Capabilities

| Capability | Description | Skill Reference |
|------------|-------------|-----------------|
| **Data Lookup** | Direct access to CDC PLACES, SVI, ADI | [data-access/](data-access/) |
| **County Profiles** | Comprehensive county health profiles | [geographic/county-profile.md](geographic/county-profile.md) |
| **Tract Analysis** | Census tract-level health patterns | [geographic/census-tract-analysis.md](geographic/census-tract-analysis.md) |
| **Chronic Disease** | 40 health measures from CDC PLACES | [health-patterns/](health-patterns/) |
| **SDOH Analysis** | Social vulnerability, deprivation | [sdoh/](sdoh/) |
| **Cohort Builder** | Evidence-based cohort specifications | [cohorts/](cohorts/) |
| **Trial Feasibility** | Site selection, enrollment projections | [trial-support/](trial-support/) |

## Embedded Data Sources (v2.0)

| Source | Coverage | Records | Key Measures |
|--------|----------|---------|--------------|
| **CDC PLACES 2024** | 100% US counties + tracts | 86,665 | 40 health measures (diabetes, obesity, COPD, etc.) |
| **CDC SVI 2022** | 100% US counties + tracts | 87,264 | 16 vulnerability indicators |
| **HRSA ADI 2023** | 100% US block groups | 242,336 | Area deprivation scores |

**Total**: 148 MB of real population data embedded in the skills.

## I Want To...

| Goal | Skill to Use |
|------|--------------|
| Look up a specific health measure | [data-lookup.md](data-access/data-lookup.md) |
| Get all data for a county | [county-profile.md](geographic/county-profile.md) |
| Analyze a census tract | [census-tract-analysis.md](geographic/census-tract-analysis.md) |
| Compare regions | [custom-region-builder.md](geographic/custom-region-builder.md) |
| Find disease prevalence | [chronic-disease-prevalence.md](health-patterns/chronic-disease-prevalence.md) |
| Assess social vulnerability | [svi-analysis.md](sdoh/svi-analysis.md) |
| Build a study cohort | [cohort-specification.md](cohorts/cohort-specification.md) |
| Plan trial site selection | [site-selection-support.md](trial-support/site-selection-support.md) |

## Integration with Other Products

PopulationSim provides **data grounding** for all other HealthSim products:

| Product | Integration | Data Used |
|---------|-------------|-----------|
| **PatientSim** | Demographics, condition prevalence | PLACES chronic disease rates, SVI demographics |
| **MemberSim** | Utilization patterns, risk adjustment | PLACES health measures, SVI socioeconomic |
| **RxMemberSim** | Adherence modeling, channel preferences | SVI transportation, poverty indicators |
| **TrialSim** | Feasibility, diversity planning | PLACES prevalence, SVI demographics |
| **NetworkSim** | Facility distribution, access patterns | SVI healthcare access indicators |

## Example: Data-Driven Patient Generation

**Without PopulationSim (generic):**
```
Generate 10 diabetic patients → Uses national 10.2% baseline
```

**With PopulationSim (grounded):**
```
Generate 10 diabetic patients in Harris County, TX →
  - Uses actual 12.1% diabetes rate from CDC PLACES
  - Applies 72% minority population from SVI  
  - Includes real comorbidity correlations (33% obesity, 32% HTN)
  - Tracks data provenance in output
```

## Output: CohortSpecification

PopulationSim's primary output is a **CohortSpecification**—a data structure that other products consume:

```json
{
  "cohort_id": "harris-diabetic-500",
  "geography": { "fips": "48201", "name": "Harris County, TX" },
  "size": 500,
  "conditions": {
    "diabetes": { "prevalence": 0.121, "source": "CDC_PLACES_2024" }
  },
  "demographics": {
    "age_distribution": { ... },
    "race_ethnicity": { ... }
  },
  "sdoh_profile": {
    "svi_overall": 0.68,
    "poverty_rate": 0.157
  }
}
```

## Skills Reference

For complete data access patterns, examples, and integration details, see:

- **[SKILL.md](SKILL.md)** - Full skill reference with all capabilities
- **[data/README.md](data/README.md)** - Data package documentation
- **[../../SKILL.md](../../SKILL.md)** - Master skill file (cross-product routing)

## Related Documentation

- [hello-healthsim PopulationSim Examples](../../hello-healthsim/examples/populationsim-examples.md)
- [Data Integration Guide](data-integration.md)
- [Cross-Product Integration](../../docs/HEALTHSIM-ARCHITECTURE-GUIDE.md#83-cross-product-integration)

---

*PopulationSim uses publicly available CDC and Census data. No PHI is included.*
