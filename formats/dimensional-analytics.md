# Dimensional Analytics Format

## Trigger Phrases

- dimensional
- star schema
- analytics
- data warehouse
- fact table
- dimension table
- DuckDB
- Databricks
- BI export
- reporting database

## Overview

This skill transforms HealthSim entities into dimensional (star schema) format optimized for analytics and business intelligence. The dimensional model separates data into:

- **Dimension Tables**: Descriptive attributes (who, what, where, when)
- **Fact Tables**: Measurable events and metrics (how much, how many)

## When to Use

Use dimensional output when:
- Building BI dashboards (Tableau, Power BI, Looker)
- Running SQL-based population health analytics
- Computing quality measures and KPIs
- Creating data warehouses for reporting
- Loading to analytics databases (DuckDB, Databricks, Snowflake)

## Conversation-First Approach

Generate dimensional data through natural conversation. Claude generates SQL directly - no scripts, no code generation.

### Quick Start Examples

**Local Analytics (DuckDB):**
```
Generate 10 diabetic patients in star schema format for DuckDB
```

**Enterprise Analytics (Databricks):**
```
Generate 10 patients in dimensional format and load to Databricks
```

## Target Databases

### DuckDB (Local Development)

- **Use case**: Local development, testing, demos
- **Schema**: `analytics`
- **Connection**: In-memory or file-based (no auth needed)

**Example conversation:**
```
User: Generate 5 patients with encounters as star schema for DuckDB

Claude: I'll generate the dimensional model. Here are the CREATE TABLE
and INSERT statements for DuckDB...

[Generates SQL DDL + INSERT statements]
```

### Databricks (Enterprise)

- **Use case**: Production analytics, team collaboration, large-scale testing
- **Catalog**: User-specified (e.g., `healthsim`, `dev_catalog`)
- **Schema**: User-specified (e.g., `gold`, `analytics`)

**Prerequisites**: You must be authenticated via Databricks CLI:
```bash
# Check your authentication
databricks auth profiles

# Expected output showing valid auth:
# Name     Host                                     Valid
# DEFAULT  https://your-workspace.cloud.databricks.com  YES

# Find your warehouse ID
databricks warehouses list
```

**Example conversation:**
```
User: Generate 10 patients in dimensional format for Databricks.
      Use catalog 'dev_catalog' and schema 'gold'

Claude: I see you're authenticated to Databricks. Let me:
1. Generate the dimensional data
2. Create the tables (if needed)
3. Load the data via SQL Statements API

[Generates SQL and executes via databricks api post]
```

## Products and Their Star Schemas

### PatientSim (Clinical Analytics)

**Dimensions:**
| Table | Description | Key Columns |
|-------|-------------|-------------|
| `dim_patient` | Patient demographics | patient_key, mrn, age, age_band, gender |
| `dim_facility` | Healthcare facilities | facility_key, facility_code, facility_name |
| `dim_provider` | Healthcare providers | provider_key, npi, provider_name, specialty |
| `dim_diagnosis` | ICD-10 codes | diagnosis_key, icd10_code, description, category |
| `dim_procedure` | Procedure codes | procedure_key, cpt_code, description |
| `dim_medication` | Medications | medication_key, rxnorm_code, drug_name, therapeutic_class |
| `dim_lab_test` | Lab definitions | lab_test_key, loinc_code, test_name, unit |
| `dim_date` | Calendar | date_key, full_date, year, quarter, month, day_name, is_holiday |

**Facts:**
| Table | Grain | Key Metrics |
|-------|-------|-------------|
| `fact_encounters` | One row per encounter | length_of_stay_hours, length_of_stay_days, is_readmission_7_day, is_readmission_30_day |
| `fact_diagnoses` | One row per diagnosis | is_primary, is_admitting, onset_date_key |
| `fact_procedures` | One row per procedure | performed_date_key, procedure_count |
| `fact_medications` | One row per medication | start_date_key, end_date_key, is_active |
| `fact_lab_results` | One row per result | result_numeric, is_abnormal, is_critical |
| `fact_vitals` | One row per vital set | is_febrile, is_tachycardic, is_hypotensive, is_hypertensive |

### MemberSim (Payer Analytics)

**Dimensions:**
| Table | Description | Key Columns |
|-------|-------------|-------------|
| `dim_member` | Member demographics | member_key, member_id, age_band, relationship |
| `dim_plan` | Plan details | plan_key, plan_code, plan_type, network_type |
| `dim_provider` | Billing/rendering | provider_key, npi, provider_type |
| `dim_facility` | Place of service | facility_key, pos_code, facility_type |
| `dim_diagnosis` | ICD-10 codes | diagnosis_key, icd10_code, category |
| `dim_procedure` | CPT/HCPCS | procedure_key, cpt_code, description |
| `dim_service_category` | Service groupings | service_category_key, category_name |

**Facts:**
| Table | Grain | Key Metrics |
|-------|-------|-------------|
| `fact_claims` | One row per claim line | charge_amount, allowed_amount, paid_amount, member_responsibility, deductible, copay, coinsurance |
| `fact_eligibility_spans` | One row per coverage period | start_date_key, end_date_key, coverage_days |

### RxMemberSim (Pharmacy Analytics)

**Dimensions:**
| Table | Description | Key Columns |
|-------|-------------|-------------|
| `dim_rx_member` | Pharmacy member | rx_member_key, member_id, age_band, plan_phase |
| `dim_medication` | NDC/drug details | medication_key, ndc, gpi, therapeutic_class, is_brand, is_specialty |
| `dim_pharmacy` | Pharmacy info | pharmacy_key, ncpdp_id, pharmacy_type, in_network |
| `dim_prescriber` | Prescriber info | prescriber_key, npi, specialty, dea_number |
| `dim_formulary` | Tier assignments | formulary_key, tier, requires_pa, step_therapy |

**Facts:**
| Table | Grain | Key Metrics |
|-------|-------|-------------|
| `fact_prescription_fills` | One row per fill | quantity_dispensed, days_supply, ingredient_cost, dispensing_fee, total_paid, patient_pay |
| `fact_prior_auth` | One row per PA | request_date_key, decision_date_key, status, approved_quantity |
| `fact_rx_eligibility_spans` | One row per coverage | deductible_remaining, oop_remaining, part_d_phase |

## Shared Date Dimension

All products share a common date dimension:

```sql
CREATE TABLE dim_date (
    date_key INT PRIMARY KEY,           -- YYYYMMDD format
    full_date DATE NOT NULL,
    year INT,
    quarter INT,
    quarter_name VARCHAR(2),            -- Q1, Q2, Q3, Q4
    month INT,
    month_name VARCHAR(20),
    week_of_year INT,
    day_of_month INT,
    day_of_week INT,
    day_name VARCHAR(20),
    is_weekend BOOLEAN,
    is_us_federal_holiday BOOLEAN,
    holiday_name VARCHAR(50)
);
```

US Federal Holidays included:
- New Year's Day, MLK Day, Presidents Day, Memorial Day
- Juneteenth, Independence Day, Labor Day, Columbus Day
- Veterans Day, Thanksgiving, Christmas

## Common Analytics Queries

### PatientSim: 30-Day Readmission Rate

```sql
SELECT
    d.category as diagnosis_category,
    COUNT(*) as encounters,
    SUM(CASE WHEN f.is_readmission_30_day THEN 1 ELSE 0 END) as readmissions,
    ROUND(100.0 * SUM(CASE WHEN f.is_readmission_30_day THEN 1 ELSE 0 END) / COUNT(*), 2) as readmit_rate
FROM fact_encounters f
JOIN fact_diagnoses fd ON f.encounter_key = fd.encounter_key
JOIN dim_diagnosis d ON fd.icd10_code = d.icd10_code
WHERE fd.is_primary = true
GROUP BY d.category
ORDER BY readmit_rate DESC;
```

### MemberSim: Cost by Service Category

```sql
SELECT
    sc.category_name as service_category,
    COUNT(*) as claim_lines,
    SUM(f.charge_amount) as total_charged,
    SUM(f.allowed_amount) as total_allowed,
    SUM(f.paid_amount) as plan_paid,
    SUM(f.member_responsibility) as member_paid
FROM fact_claims f
JOIN dim_service_category sc ON f.service_category_key = sc.service_category_key
GROUP BY sc.category_name
ORDER BY plan_paid DESC;
```

### RxMemberSim: Generic Dispensing Rate

```sql
SELECT
    m.therapeutic_class,
    COUNT(*) as total_fills,
    SUM(CASE WHEN NOT m.is_brand THEN 1 ELSE 0 END) as generic_fills,
    ROUND(100.0 * SUM(CASE WHEN NOT m.is_brand THEN 1 ELSE 0 END) / COUNT(*), 2) as gdr
FROM fact_prescription_fills f
JOIN dim_medication m ON f.medication_key = m.medication_key
GROUP BY m.therapeutic_class
ORDER BY gdr;
```

### Cross-Product: Total Member Spend

```sql
-- Requires both MemberSim and RxMemberSim data
SELECT
    m.age_band,
    COUNT(DISTINCT m.member_key) as members,
    COALESCE(SUM(mc.paid_amount), 0) as medical_spend,
    COALESCE(SUM(rx.total_paid), 0) as pharmacy_spend,
    COALESCE(SUM(mc.paid_amount), 0) + COALESCE(SUM(rx.total_paid), 0) as total_spend
FROM dim_member m
LEFT JOIN fact_claims mc ON m.member_key = mc.member_key
LEFT JOIN dim_rx_member rm ON m.person_id = rm.person_id
LEFT JOIN fact_prescription_fills rx ON rm.rx_member_key = rx.rx_member_key
GROUP BY m.age_band
ORDER BY total_spend DESC;
```

## Derived Metrics

The dimensional model pre-calculates useful derived metrics:

### Patient Dimensions
- `age_band`: 0-17, 18-34, 35-44, 45-54, 55-64, 65-74, 75-84, 85+
- `gender_description`: Male, Female, Other, Unknown

### Encounter Facts
- `length_of_stay_hours`: Calculated from admission/discharge
- `length_of_stay_days`: Rounded LOS in days
- `is_readmission_7_day`: True if readmitted within 7 days
- `is_readmission_30_day`: True if readmitted within 30 days

### Lab Result Facts
- `is_abnormal`: Outside reference range
- `is_critical`: Significantly outside range (panic value)

### Vital Sign Facts
- `is_febrile`: Temperature > 100.4F
- `is_tachycardic`: Heart rate > 100
- `is_hypotensive`: Systolic BP < 90
- `is_hypertensive`: Systolic BP > 140

### Claim Facts
- `member_responsibility`: deductible + copay + coinsurance
- Service category derived from CPT code ranges

## Example: Complete Workflow

### DuckDB Local Workflow

**User request:**
```
Generate 5 patients with encounters in star schema format for DuckDB analytics
```

**Claude generates:**
1. CREATE TABLE statements for dimensions and facts
2. INSERT statements with realistic healthcare data
3. Sample analytics queries to verify the data

```sql
-- Dimension: dim_patient
CREATE TABLE IF NOT EXISTS analytics.dim_patient (
    patient_key INT PRIMARY KEY,
    mrn VARCHAR(20),
    given_name VARCHAR(50),
    family_name VARCHAR(50),
    birth_date DATE,
    age INT,
    age_band VARCHAR(10),
    gender CHAR(1),
    gender_description VARCHAR(10),
    city VARCHAR(50),
    state CHAR(2)
);

-- Insert patients
INSERT INTO analytics.dim_patient VALUES
(1, 'MRN100001', 'John', 'Smith', '1960-03-15', 65, '65-74', 'M', 'Male', 'Springfield', 'IL'),
(2, 'MRN100002', 'Maria', 'Garcia', '1955-08-22', 69, '65-74', 'F', 'Female', 'Chicago', 'IL'),
-- ... more rows
```

### Databricks Enterprise Workflow

**User request:**
```
Load 10 patients to Databricks. Use catalog 'dev_catalog', schema 'gold'.
Start the warehouse if needed.
```

**Claude workflow:**
1. Confirms Databricks CLI authentication
2. Checks/starts the SQL warehouse
3. Generates CREATE TABLE and INSERT statements
4. Executes via `databricks api post /api/2.0/sql/statements`
5. Reports success with table counts

**Example execution:**
```bash
# Claude uses Databricks SQL Statements API
databricks api post /api/2.0/sql/statements --json '{
  "warehouse_id": "YOUR_WAREHOUSE_ID",
  "statement": "CREATE SCHEMA IF NOT EXISTS dev_catalog.gold",
  "wait_timeout": "30s"
}'
```

## Reproducibility

For consistent results across sessions:

**Request:** "Generate 10 patients using seed 42"

Claude will:
1. Use seed 42 for all random selections
2. Generate identical output if same parameters used
3. Note the seed in output for reference

## Related Skills

- [../scenarios/patientsim/SKILL.md](../scenarios/patientsim/SKILL.md) - Clinical data generation
- [../scenarios/membersim/SKILL.md](../scenarios/membersim/SKILL.md) - Claims data generation
- [../scenarios/rxmembersim/SKILL.md](../scenarios/rxmembersim/SKILL.md) - Pharmacy data generation
- [sql.md](sql.md) - SQL INSERT format (transactional, not dimensional)
- [csv.md](csv.md) - CSV export format
