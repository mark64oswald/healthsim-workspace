# Auto-Persist Examples

_Token-efficient scenario management for large batch operations._

## Overview

The auto-persist pattern enables generating and persisting large batches of synthetic healthcare data without filling the context window. Instead of echoing back all generated data, it returns a compact summary (~500 tokens).

**When to Use Auto-Persist**:
- Generating 50+ entities at once
- Building large cohorts for training or testing
- Batch generation workflows
- Avoiding context overflow in long sessions

**Traditional vs Auto-Persist**:

| Approach | Use Case | Context Impact |
|----------|----------|----------------|
| Traditional `save_scenario` | Small scenarios (<50 entities) | Returns all data (~1K-50K tokens) |
| Auto-Persist `persist()` | Large batches (50+ entities) | Returns summary (~500 tokens) |

---

## Example 1: Generate 100 Medicare Members

### User Prompt
```
Generate 100 Medicare Advantage members over 65 years old in California
```

### Claude Response (using auto-persist)
```
I'll generate 100 Medicare Advantage members for you.

[Generates members using MemberSim skill...]
[Auto-persists to database...]

**Saved "medicare-advantage-20241227"**

| Metric | Value |
|--------|-------|
| Members | 100 |
| Age Range | 65-89 |
| Gender | 48 male, 52 female |
| Geographic | California (Los Angeles, San Diego, San Francisco, etc.) |
| Plan Types | HMO (40), PPO (35), PFFS (25) |

The data is persisted and ready for use. Would you like to:
- Query specific subsets ("show members in San Diego")
- See sample members ("show me 3 example members")
- Generate claims for these members
```

---

## Example 2: Query Saved Scenario Data

### User Prompt
```
From my medicare scenario, show female members over 75 with diabetes
```

### Claude Response
```
[Queries scenario with SQL...]

Found 12 female members over 75 with diabetes:

| Name | Age | City | Plan | Risk Score |
|------|-----|------|------|------------|
| Margaret Wilson | 78 | San Diego | HMO | 1.85 |
| Dorothy Chen | 82 | Los Angeles | PPO | 2.12 |
| Patricia Johnson | 76 | San Francisco | HMO | 1.45 |
| Betty Martinez | 79 | Sacramento | PFFS | 1.92 |
| Ruth Anderson | 81 | Fresno | PPO | 2.34 |
...

Showing 5 of 12 results. Say "show more" to see the rest.

These high-risk members may benefit from care management programs.
```

---

## Example 3: Resume Work with Summary

### User Prompt
```
Load my diabetes cohort from yesterday
```

### Claude Response (loading summary only)
```
[Loading summary for "diabetes-cohort-20241226"...]

**diabetes-cohort-20241226** Summary:

| Entity Type | Count |
|-------------|-------|
| Patients | 150 |
| Encounters | 425 |
| Lab Results | 890 |
| Medications | 320 |

**Patient Demographics**:
- Age range: 35-78 years
- Gender: 72 male, 78 female
- Race: White (45%), Hispanic (28%), Black (18%), Asian (9%)

**Clinical Characteristics**:
- Average A1C: 7.8% (range: 6.1-12.4%)
- With complications: 67 (45%)
- On insulin: 43 (29%)

What would you like to do with this cohort?
- Query specific patients
- Generate additional data (encounters, labs)
- Export for analysis
```

---

## Example 4: Get Sample Entities

### User Prompt
```
Show me a few example patients from that cohort
```

### Claude Response
```
Here are 3 representative patients from "diabetes-cohort-20241226":

---

**1. Maria Gonzalez** (Female, 58)
- MRN: P-2024-00847
- Diagnosis: E11.65 - Type 2 DM with hyperglycemia
- Latest A1C: 8.2% (2024-02-15)
- Medications: Metformin 1000mg BID, Jardiance 10mg daily
- Comorbidities: Hypertension (I10), Obesity (E66.9)
- Last Visit: 2024-02-15 (routine follow-up)

---

**2. James Thompson** (Male, 67)
- MRN: P-2024-01234
- Diagnosis: E11.9 - Type 2 DM without complications
- Latest A1C: 6.8% (2024-01-20) - well controlled
- Medications: Metformin 500mg BID
- Comorbidities: None
- Last Visit: 2024-01-20 (annual wellness)

---

**3. Patricia Lee** (Female, 72)
- MRN: P-2024-00623
- Diagnosis: E11.40 - Type 2 DM with DKA
- Latest A1C: 10.1% (2024-03-01) - poor control
- Medications: Insulin glargine 30u qHS, Humalog sliding scale
- Comorbidities: CKD Stage 3 (N18.3), Retinopathy (E11.319)
- Last Visit: 2024-03-01 (urgent, post-hospitalization)

---

Want to see more samples or query for specific criteria?
```

---

## Example 5: Batch Generation Workflow

### User Prompt
```
Generate a complete clinical trial scenario with 200 subjects
```

### Claude Response
```
I'll generate a Phase 3 oncology trial with 200 subjects. This will use 
auto-persist to manage the large volume of data.

[Generating study and sites...]
[Generating subjects in batches of 50...]
[Generating visits and adverse events...]
[Auto-persisting...]

**Saved "oncology-phase3-20241227"**

**Study Overview**:
| Attribute | Value |
|-----------|-------|
| Protocol | ONCO-2024-001 |
| Phase | 3 |
| Indication | NSCLC |
| Sites | 8 |
| Subjects | 200 |

**Subject Breakdown**:
| Treatment Arm | N | % |
|---------------|---|---|
| Active (Drug A + SOC) | 100 | 50% |
| Control (SOC only) | 100 | 50% |

**Visit Statistics**:
- Scheduled visits: 2,400 (12 per subject)
- Completed visits: 1,847 (77%)
- Adverse events: 89 (32 subjects affected)

**Data Generated**:
| Entity | Count |
|--------|-------|
| Subjects | 200 |
| Treatment Arms | 2 |
| Scheduled Visits | 2,400 |
| Actual Visits | 1,847 |
| Adverse Events | 89 |
| Disposition Events | 200 |

Would you like to:
- Query subjects by arm or site
- View adverse event details
- Export to CDISC SDTM format
```

---

## Example 6: Cross-Product Query

### User Prompt
```
For my diabetes cohort, show patients who also have claims over $10,000
```

### Claude Response
```
[Running cross-product query...]

Found 23 patients with both diabetes diagnosis AND claims over $10,000:

| Patient | Total Claims | Highest Claim | Primary Payer |
|---------|-------------|---------------|---------------|
| Robert Wilson | $45,230 | $28,500 (inpatient) | Medicare |
| Linda Martinez | $32,100 | $15,200 (surgery) | BCBS PPO |
| Michael Chen | $28,750 | $12,400 (ED) | Aetna HMO |
| Barbara Johnson | $24,300 | $11,800 (inpatient) | UHC |
| Thomas Brown | $19,450 | $10,500 (procedure) | Medicare |
...

Showing 5 of 23 results.

**Key Insights**:
- Average total claims: $18,420
- Most common high-cost service: Inpatient hospitalization
- Average age of high-cost patients: 68 years

Would you like to see the claim details for any specific patient?
```

---

## Example 7: Rename and Tag Scenarios

### User Prompt
```
Rename my medicare scenario to "ca-medicare-q4-2024" and tag it with 
"training", "california", "medicare-advantage"
```

### Claude Response
```
[Renaming scenario...]
[Adding tags...]

Updated scenario:
- **Old name**: medicare-advantage-20241227
- **New name**: ca-medicare-q4-2024
- **Tags**: training, california, medicare-advantage

You can now find this scenario with:
- `list scenarios tagged training`
- `load ca-medicare-q4-2024`
```

---

## Technical Details

### Auto-Persist Functions

```python
from healthsim.state import persist, get_summary, query_scenario

# Persist entities - returns summary, not full data
result = persist(
    entities={'patients': [...], 'encounters': [...]},
    context='diabetes cohort for training',
    tags=['diabetes', 'training']
)
# result.summary contains ~500 tokens

# Load summary only
summary = get_summary('scenario-name')
# summary.entity_counts, summary.statistics, summary.samples

# Query with pagination
results = query_scenario(
    'scenario-name',
    "SELECT * FROM patients WHERE gender = 'F'",
    limit=20
)
# results.rows, results.has_more
```

### Token Budget

| Component | Approximate Tokens |
|-----------|-------------------|
| Scenario metadata | ~100 |
| Entity counts | ~50 |
| Statistics summary | ~150 |
| Sample entities (3 per type) | ~200 per type |
| **Total (without samples)** | **~300** |
| **Total (with 3 samples × 5 types)** | **~1,300** |

### Query Security

All queries are validated to ensure they are SELECT-only:
- ✅ `SELECT * FROM patients WHERE...`
- ✅ `SELECT COUNT(*) FROM encounters`
- ❌ `DELETE FROM patients` (blocked)
- ❌ `DROP TABLE scenarios` (blocked)
- ❌ `UPDATE members SET...` (blocked)

---

## Example 8: Tag Management

### User Prompt
```
What tags do I have across my scenarios?
```

### Claude Response
```
[Listing all tags...]

**Your scenario tags**:

| Tag | Usage Count |
|-----|-------------|
| training | 5 scenarios |
| production | 3 scenarios |
| california | 3 scenarios |
| diabetes | 2 scenarios |
| validated | 2 scenarios |
| testing | 1 scenario |

To find scenarios with a specific tag: "show scenarios tagged production"
To add a tag: "tag my-scenario with validated"
```

---

## Example 9: Clone Scenario for A/B Testing

### User Prompt
```
Clone my diabetes-cohort scenario so I can test a different cohort definition
```

### Claude Response
```
[Cloning scenario...]

**Cloned "diabetes-cohort-20241227" → "diabetes-cohort-20241227-copy"**

| Entity Type | Copied |
|-------------|--------|
| Patients | 150 |
| Encounters | 425 |
| Lab Results | 890 |
| Medications | 320 |
| **Total** | **1,785 entities** |

All entities have new unique IDs. The clone is completely independent - 
changes to either scenario won't affect the other.

Would you like to rename the clone to something more descriptive?
```

---

## Example 10: Merge Multiple Cohorts

### User Prompt
```
Merge my diabetes, heart-failure, and copd scenarios into a combined 
training dataset
```

### Claude Response
```
[Merging 3 scenarios...]

**Created "merged-training-20241227"** from 3 sources:

| Source | Patients | Encounters | Labs |
|--------|----------|------------|------|
| diabetes-cohort | 150 | 425 | 890 |
| heart-failure-cohort | 120 | 380 | 720 |
| copd-training | 75 | 210 | 450 |
| **Total** | **345** | **1,015** | **2,060** |

- Conflicts resolved: 0 (no duplicate IDs)
- Tags inherited: training, chronic-disease, validated

All source scenarios remain unchanged. Would you like to:
- View samples from the merged set
- Query specific patient subsets
- Export for external analysis
```

---

## Example 11: Export to CSV for Analysis

### User Prompt
```
Export my merged training dataset to CSV for analysis in Python
```

### Claude Response
```
[Exporting to CSV...]

**Exported "merged-training-20241227" to CSV**

| File | Rows | Size |
|------|------|------|
| patients.csv | 345 | 312 KB |
| encounters.csv | 1,015 | 548 KB |
| lab_results.csv | 2,060 | 1.2 MB |
| diagnoses.csv | 892 | 124 KB |
| medications.csv | 1,240 | 186 KB |

**Location**: `~/Downloads/merged-training-20241227/`
**Total Size**: 2.3 MB

Load in Python:
```python
import pandas as pd

patients = pd.read_csv('~/Downloads/merged-training-20241227/patients.csv')
encounters = pd.read_csv('~/Downloads/merged-training-20241227/encounters.csv')
labs = pd.read_csv('~/Downloads/merged-training-20241227/lab_results.csv')

print(f"Loaded {len(patients)} patients with {len(encounters)} encounters")
```
```

---

## Example 12: Export to Parquet for Big Data

### User Prompt
```
Export as Parquet for loading into Databricks
```

### Claude Response
```
[Exporting to Parquet...]

**Exported "merged-training-20241227" to Parquet**

| File | Rows | Size |
|------|------|------|
| patients.parquet | 345 | 89 KB |
| encounters.parquet | 1,015 | 142 KB |
| lab_results.parquet | 2,060 | 285 KB |
| diagnoses.parquet | 892 | 38 KB |
| medications.parquet | 1,240 | 52 KB |

**Location**: `~/Downloads/merged-training-20241227-parquet/`
**Total Size**: 606 KB (74% smaller than CSV!)

Load in Databricks:
```python
# Upload to DBFS first
dbutils.fs.cp(
    'file:///Users/.../merged-training-20241227-parquet/',
    'dbfs:/FileStore/healthsim-training/',
    recurse=True
)

# Read with Spark
patients = spark.read.parquet('dbfs:/FileStore/healthsim-training/patients.parquet')
patients.display()
```

Or query directly:
```sql
CREATE TABLE healthsim.patients
USING PARQUET
LOCATION 'dbfs:/FileStore/healthsim-training/patients.parquet';

SELECT * FROM healthsim.patients WHERE gender = 'F';
```
```

---

## Related Examples

- [Cross-Domain Examples](cross-domain-examples.md) - **Cross-product auto-persist workflow** (PopulationSim → PatientSim → TrialSim)
- [PatientSim Examples](patientsim-examples.md)
- [MemberSim Examples](membersim-examples.md)
- [TrialSim Examples](trialsim-examples.md)

---

*Version: 2.0 | December 27, 2024 | Phase 2 Enhancements: Tags, Cloning, Merging, Export*
