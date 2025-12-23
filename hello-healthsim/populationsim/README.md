# Hello PopulationSim

Welcome to PopulationSim! This directory contains example prompts and outputs to help you get started with population demographics, health indicators, and SDOH analysis.

## Examples

| Example | Description | Key Concepts |
|---------|-------------|--------------|
| [01-basic-profile](01-basic-profile.md) | County population profile | Demographics, health indicators |
| [02-sdoh-analysis](02-sdoh-analysis.md) | Social vulnerability analysis | SVI, ADI, Z-codes |
| [03-cohort-definition](03-cohort-definition.md) | Define target population | Clinical + SDOH criteria |
| [04-trial-feasibility](04-trial-feasibility.md) | Trial site assessment | Catchment, diversity planning |

## Quick Start

### Your First Population Profile

```
User: Create a population profile for Harris County, Texas

Claude: I'll generate a comprehensive population profile for Harris County 
(FIPS 48201), the most populous county in Texas and home to Houston.

[PopulationProfile output with demographics, health indicators, SDOH]
```

### Your First SDOH Analysis

```
User: Analyze social vulnerability in Harris County census tracts

Claude: I'll analyze the CDC/ATSDR Social Vulnerability Index (SVI) 
for census tracts in Harris County, breaking down vulnerability 
by theme and identifying high-risk areas.

[Tract-level SVI analysis with theme scores]
```

### Your First Cohort

```
User: Define a cohort of 1,000 diabetic patients from high-vulnerability 
      areas for a health equity study

Claude: I'll create a CohortSpecification targeting diabetic adults 
in high-SDOH census tracts (SVI ≥ 0.70) of Harris County.

[CohortSpecification with clinical and SDOH requirements]
```

## Key Concepts

### Geographic Levels

PopulationSim works at multiple geographic scales:

- **State** (2-digit FIPS): Broad analysis
- **County** (5-digit FIPS): Primary analysis unit
- **Census Tract** (11-digit FIPS): SDOH detail
- **Block Group** (12-digit FIPS): Finest granularity (ADI)
- **MSA/CBSA**: Metropolitan areas

### Data Sources

PopulationSim synthesizes from authoritative sources:

- **Census ACS**: Demographics, income, education, housing
- **CDC PLACES**: Health indicators and behaviors
- **CDC SVI**: Social vulnerability (4 themes, 16 variables)
- **ADI**: Area deprivation (17 variables)

### SDOH Z-Codes

PopulationSim estimates ICD-10-CM Z-code prevalence:

| Code | Description | Typical Rate |
|------|-------------|--------------|
| Z59.6 | Low income | 8-20% |
| Z59.41 | Food insecurity | 8-15% |
| Z56.0 | Unemployment | 4-10% |
| Z59.82 | Transportation insecurity | 5-12% |

## Next Steps

1. Try the [basic profile example](01-basic-profile.md)
2. Explore [SDOH analysis](02-sdoh-analysis.md)
3. Learn [cohort definition](03-cohort-definition.md)
4. See [trial feasibility](04-trial-feasibility.md)

## Related Resources

- [PopulationSim SKILL.md](../../skills/populationsim/SKILL.md)
- [Developer Guide](../../skills/populationsim/developer-guide.md)
- [Prompt Guide](../../skills/populationsim/prompt-guide.md)
