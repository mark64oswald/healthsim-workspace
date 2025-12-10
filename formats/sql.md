# SQL Export Format

## Trigger Phrases

- SQL
- INSERT statements
- SQL INSERT
- database insert
- as SQL
- load to database
- SQL script
- database export

## Overview

This skill exports HealthSim entities as SQL INSERT statements for direct database loading. Supports multiple SQL dialects and batch operations.

## Export Options

| Option | Values | Default | Description |
|--------|--------|---------|-------------|
| dialect | postgresql, mysql, sqlserver, oracle, sqlite | postgresql | SQL dialect |
| batch_size | 1-1000 | 100 | Rows per INSERT (multi-row) |
| include_schema | true, false | false | Include CREATE TABLE |
| transaction | true, false | true | Wrap in transaction |
| on_conflict | ignore, update, error | error | Conflict handling |
| null_style | NULL, DEFAULT | NULL | How to handle nulls |

## Table Schemas

### patients

```sql
CREATE TABLE patients (
    mrn VARCHAR(20) PRIMARY KEY,
    given_name VARCHAR(50) NOT NULL,
    family_name VARCHAR(50) NOT NULL,
    middle_name VARCHAR(50),
    birth_date DATE NOT NULL,
    gender CHAR(1) NOT NULL,
    ssn VARCHAR(11),
    street_address VARCHAR(100),
    city VARCHAR(50),
    state CHAR(2),
    postal_code VARCHAR(10),
    country VARCHAR(3) DEFAULT 'USA',
    phone_home VARCHAR(20),
    phone_work VARCHAR(20),
    email VARCHAR(100),
    language_code VARCHAR(3),
    marital_status CHAR(1),
    race_code VARCHAR(10),
    ethnicity_code VARCHAR(10),
    deceased BOOLEAN DEFAULT FALSE,
    deceased_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### encounters

```sql
CREATE TABLE encounters (
    encounter_id VARCHAR(20) PRIMARY KEY,
    patient_mrn VARCHAR(20) NOT NULL REFERENCES patients(mrn),
    encounter_class CHAR(3) NOT NULL,
    encounter_type VARCHAR(50),
    status VARCHAR(20) NOT NULL,
    period_start TIMESTAMP NOT NULL,
    period_end TIMESTAMP,
    facility_code VARCHAR(20),
    facility_name VARCHAR(100),
    location_unit VARCHAR(20),
    location_room VARCHAR(10),
    location_bed VARCHAR(5),
    attending_npi VARCHAR(10),
    attending_name VARCHAR(100),
    admission_source VARCHAR(5),
    discharge_disposition VARCHAR(5),
    reason_code VARCHAR(10),
    reason_description VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### diagnoses

```sql
CREATE TABLE diagnoses (
    diagnosis_id VARCHAR(20) PRIMARY KEY,
    patient_mrn VARCHAR(20) NOT NULL REFERENCES patients(mrn),
    encounter_id VARCHAR(20) REFERENCES encounters(encounter_id),
    code VARCHAR(10) NOT NULL,
    code_system VARCHAR(20) DEFAULT 'ICD-10-CM',
    description VARCHAR(200),
    diagnosis_type VARCHAR(20),
    onset_date DATE,
    abatement_date DATE,
    clinical_status VARCHAR(20),
    verification_status VARCHAR(20),
    severity VARCHAR(20),
    diagnosed_by_npi VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### procedures

```sql
CREATE TABLE procedures (
    procedure_id VARCHAR(20) PRIMARY KEY,
    patient_mrn VARCHAR(20) NOT NULL REFERENCES patients(mrn),
    encounter_id VARCHAR(20) REFERENCES encounters(encounter_id),
    code VARCHAR(10) NOT NULL,
    code_system VARCHAR(20) NOT NULL,
    description VARCHAR(200),
    performed_datetime TIMESTAMP,
    performer_npi VARCHAR(10),
    performer_name VARCHAR(100),
    body_site VARCHAR(50),
    status VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### medications

```sql
CREATE TABLE medications (
    medication_id VARCHAR(20) PRIMARY KEY,
    patient_mrn VARCHAR(20) NOT NULL REFERENCES patients(mrn),
    encounter_id VARCHAR(20) REFERENCES encounters(encounter_id),
    ndc VARCHAR(11),
    rxnorm_code VARCHAR(10),
    drug_name VARCHAR(200) NOT NULL,
    dose_value DECIMAL(10,2),
    dose_unit VARCHAR(20),
    route VARCHAR(20),
    frequency VARCHAR(50),
    start_date DATE,
    end_date DATE,
    status VARCHAR(20),
    prescriber_npi VARCHAR(10),
    prescriber_name VARCHAR(100),
    indication_code VARCHAR(10),
    refills_authorized INT,
    quantity_dispensed INT,
    days_supply INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### observations

```sql
CREATE TABLE observations (
    observation_id VARCHAR(20) PRIMARY KEY,
    patient_mrn VARCHAR(20) NOT NULL REFERENCES patients(mrn),
    encounter_id VARCHAR(20) REFERENCES encounters(encounter_id),
    code VARCHAR(20) NOT NULL,
    code_system VARCHAR(20) NOT NULL,
    description VARCHAR(200),
    value_numeric DECIMAL(12,4),
    value_string VARCHAR(500),
    value_code VARCHAR(20),
    unit VARCHAR(20),
    reference_low DECIMAL(10,2),
    reference_high DECIMAL(10,2),
    interpretation VARCHAR(5),
    effective_datetime TIMESTAMP,
    status VARCHAR(20),
    performer_npi VARCHAR(10),
    specimen_type VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### orders

```sql
CREATE TABLE orders (
    order_id VARCHAR(20) PRIMARY KEY,
    patient_mrn VARCHAR(20) NOT NULL REFERENCES patients(mrn),
    encounter_id VARCHAR(20) REFERENCES encounters(encounter_id),
    order_type VARCHAR(20) NOT NULL,
    code VARCHAR(20),
    code_system VARCHAR(20),
    description VARCHAR(200),
    priority CHAR(1),
    status VARCHAR(20),
    ordered_datetime TIMESTAMP,
    scheduled_datetime TIMESTAMP,
    completed_datetime TIMESTAMP,
    ordering_provider_npi VARCHAR(10),
    ordering_provider_name VARCHAR(100),
    performer_npi VARCHAR(10),
    performer_name VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### claims

```sql
CREATE TABLE claims (
    claim_id VARCHAR(20) PRIMARY KEY,
    member_id VARCHAR(20) NOT NULL,
    claim_type VARCHAR(20) NOT NULL,
    status VARCHAR(20) NOT NULL,
    service_from_date DATE NOT NULL,
    service_to_date DATE,
    facility_npi VARCHAR(10),
    facility_name VARCHAR(100),
    billing_provider_npi VARCHAR(10),
    rendering_provider_npi VARCHAR(10),
    principal_diagnosis VARCHAR(10),
    total_charge DECIMAL(12,2),
    total_allowed DECIMAL(12,2),
    total_paid DECIMAL(12,2),
    patient_responsibility DECIMAL(12,2),
    adjudicated_date DATE,
    auth_number VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### claim_lines

```sql
CREATE TABLE claim_lines (
    claim_id VARCHAR(20) NOT NULL REFERENCES claims(claim_id),
    line_number INT NOT NULL,
    procedure_code VARCHAR(10),
    procedure_modifier VARCHAR(10),
    revenue_code VARCHAR(4),
    ndc VARCHAR(11),
    description VARCHAR(200),
    service_date DATE,
    quantity DECIMAL(10,3),
    charge_amount DECIMAL(12,2),
    allowed_amount DECIMAL(12,2),
    paid_amount DECIMAL(12,2),
    deductible DECIMAL(10,2),
    copay DECIMAL(10,2),
    coinsurance DECIMAL(10,2),
    diagnosis_pointer VARCHAR(10),
    place_of_service VARCHAR(2),
    PRIMARY KEY (claim_id, line_number)
);
```

## Example INSERT Statements

### Single Patient Insert

```sql
INSERT INTO patients (
    mrn, given_name, family_name, middle_name, birth_date, gender,
    ssn, street_address, city, state, postal_code, country,
    phone_home, email, language_code, marital_status
) VALUES (
    'MRN00000001', 'John', 'Smith', 'Michael', '1970-03-15', 'M',
    '123-45-6789', '123 Main St', 'Springfield', 'IL', '62701', 'USA',
    '555-123-4567', 'john.smith@email.com', 'ENG', 'M'
);
```

### Multi-Row Insert (PostgreSQL/MySQL)

```sql
INSERT INTO patients (mrn, given_name, family_name, birth_date, gender, city, state) VALUES
    ('MRN00000001', 'John', 'Smith', '1970-03-15', 'M', 'Springfield', 'IL'),
    ('MRN00000002', 'Maria', 'Garcia', '1955-10-20', 'F', 'Springfield', 'IL'),
    ('MRN00000003', 'Eleanor', 'Thompson', '1950-08-12', 'F', 'Springfield', 'IL'),
    ('MRN00000004', 'James', 'Wilson', '1965-07-10', 'M', 'Springfield', 'IL'),
    ('MRN00000005', 'Carlos', 'Martinez', '1968-02-20', 'M', 'Springfield', 'IL');
```

### Complete Patient with Related Data

```sql
BEGIN;

-- Insert patient
INSERT INTO patients (mrn, given_name, family_name, birth_date, gender, city, state)
VALUES ('MRN00000001', 'John', 'Smith', '1970-03-15', 'M', 'Springfield', 'IL');

-- Insert encounter
INSERT INTO encounters (encounter_id, patient_mrn, encounter_class, encounter_type, status, period_start, period_end, attending_npi, attending_name)
VALUES ('ENC0000000001', 'MRN00000001', 'I', 'inpatient', 'finished', '2025-01-10 14:00:00', '2025-01-15 10:00:00', '1234567890', 'Dr. Robert Johnson');

-- Insert diagnoses
INSERT INTO diagnoses (diagnosis_id, patient_mrn, encounter_id, code, code_system, description, diagnosis_type, clinical_status)
VALUES
    ('DX0000000001', 'MRN00000001', 'ENC0000000001', 'I50.23', 'ICD-10-CM', 'Acute on chronic systolic heart failure', 'principal', 'active'),
    ('DX0000000002', 'MRN00000001', 'ENC0000000001', 'I10', 'ICD-10-CM', 'Essential hypertension', 'secondary', 'active'),
    ('DX0000000003', 'MRN00000001', 'ENC0000000001', 'E11.9', 'ICD-10-CM', 'Type 2 diabetes mellitus', 'secondary', 'active');

-- Insert medications
INSERT INTO medications (medication_id, patient_mrn, encounter_id, ndc, drug_name, dose_value, dose_unit, route, frequency, status, prescriber_npi)
VALUES
    ('MED0000000001', 'MRN00000001', 'ENC0000000001', '00093505601', 'Lisinopril 10mg Tab', 10, 'mg', 'oral', 'daily', 'active', '1234567890'),
    ('MED0000000002', 'MRN00000001', 'ENC0000000001', '00093085601', 'Metformin 500mg Tab', 500, 'mg', 'oral', 'BID', 'active', '1234567890');

-- Insert observations (labs)
INSERT INTO observations (observation_id, patient_mrn, encounter_id, code, code_system, description, value_numeric, unit, reference_low, reference_high, interpretation, status)
VALUES
    ('OBS0000000001', 'MRN00000001', 'ENC0000000001', '2345-7', 'LOINC', 'Glucose', 98, 'mg/dL', 70, 100, 'N', 'final'),
    ('OBS0000000002', 'MRN00000001', 'ENC0000000001', '2160-0', 'LOINC', 'Creatinine', 1.1, 'mg/dL', 0.7, 1.3, 'N', 'final'),
    ('OBS0000000003', 'MRN00000001', 'ENC0000000001', '4548-4', 'LOINC', 'HbA1c', 7.8, '%', 4.0, 5.6, 'H', 'final');

COMMIT;
```

### Claims Insert

```sql
-- Insert claim
INSERT INTO claims (
    claim_id, member_id, claim_type, status, service_from_date, service_to_date,
    rendering_provider_npi, principal_diagnosis, total_charge, total_allowed,
    total_paid, patient_responsibility, adjudicated_date
) VALUES (
    'CLM20250115001', 'MEM001234', 'professional', 'paid', '2025-01-15', '2025-01-15',
    '1234567890', 'E11.9', 175.00, 150.00, 125.00, 25.00, '2025-01-16'
);

-- Insert claim lines
INSERT INTO claim_lines (
    claim_id, line_number, procedure_code, description, service_date,
    quantity, charge_amount, allowed_amount, paid_amount, deductible, copay,
    coinsurance, diagnosis_pointer, place_of_service
) VALUES (
    'CLM20250115001', 1, '99214', 'Office visit established', '2025-01-15',
    1, 175.00, 150.00, 125.00, 0.00, 25.00, 0.00, '1', '11'
);
```

## Dialect-Specific Syntax

### PostgreSQL

```sql
-- Use ON CONFLICT for upsert
INSERT INTO patients (mrn, given_name, family_name, birth_date, gender)
VALUES ('MRN00000001', 'John', 'Smith', '1970-03-15', 'M')
ON CONFLICT (mrn) DO UPDATE SET
    given_name = EXCLUDED.given_name,
    family_name = EXCLUDED.family_name,
    updated_at = CURRENT_TIMESTAMP;
```

### MySQL

```sql
-- Use INSERT ... ON DUPLICATE KEY UPDATE
INSERT INTO patients (mrn, given_name, family_name, birth_date, gender)
VALUES ('MRN00000001', 'John', 'Smith', '1970-03-15', 'M')
ON DUPLICATE KEY UPDATE
    given_name = VALUES(given_name),
    family_name = VALUES(family_name),
    updated_at = CURRENT_TIMESTAMP;
```

### SQL Server

```sql
-- Use MERGE for upsert
MERGE INTO patients AS target
USING (VALUES ('MRN00000001', 'John', 'Smith', '1970-03-15', 'M'))
    AS source (mrn, given_name, family_name, birth_date, gender)
ON target.mrn = source.mrn
WHEN MATCHED THEN
    UPDATE SET given_name = source.given_name, family_name = source.family_name
WHEN NOT MATCHED THEN
    INSERT (mrn, given_name, family_name, birth_date, gender)
    VALUES (source.mrn, source.given_name, source.family_name, source.birth_date, source.gender);
```

### Oracle

```sql
-- Use MERGE for upsert
MERGE INTO patients target
USING (SELECT 'MRN00000001' AS mrn, 'John' AS given_name, 'Smith' AS family_name,
       TO_DATE('1970-03-15', 'YYYY-MM-DD') AS birth_date, 'M' AS gender FROM dual) source
ON (target.mrn = source.mrn)
WHEN MATCHED THEN
    UPDATE SET target.given_name = source.given_name, target.family_name = source.family_name
WHEN NOT MATCHED THEN
    INSERT (mrn, given_name, family_name, birth_date, gender)
    VALUES (source.mrn, source.given_name, source.family_name, source.birth_date, source.gender);
```

### SQLite

```sql
-- Use INSERT OR REPLACE
INSERT OR REPLACE INTO patients (mrn, given_name, family_name, birth_date, gender)
VALUES ('MRN00000001', 'John', 'Smith', '1970-03-15', 'M');
```

## Batch Loading Script

**Request:** "Generate SQL load script for 100 patients"

**Output:**
```sql
-- HealthSim Data Load Script
-- Generated: 2025-01-15T14:30:00
-- Dialect: PostgreSQL
-- Records: 100 patients with related data

BEGIN;

-- Patients (batch 1 of 1)
INSERT INTO patients (mrn, given_name, family_name, birth_date, gender, city, state) VALUES
    ('MRN00000001', 'John', 'Smith', '1970-03-15', 'M', 'Springfield', 'IL'),
    ('MRN00000002', 'Maria', 'Garcia', '1955-10-20', 'F', 'Springfield', 'IL'),
    -- ... 98 more rows ...
    ('MRN00000100', 'Robert', 'Taylor', '1982-11-30', 'M', 'Springfield', 'IL');

-- Verify count
DO $$
BEGIN
    IF (SELECT COUNT(*) FROM patients) < 100 THEN
        RAISE EXCEPTION 'Expected 100 patients, found %', (SELECT COUNT(*) FROM patients);
    END IF;
END $$;

COMMIT;
```

## String Escaping

| Character | Escaped As |
|-----------|------------|
| Single quote | `''` |
| Backslash | `\\` (MySQL) |
| NULL value | `NULL` keyword |
| Unicode | Native UTF-8 |

**Example:**
```sql
-- Name with apostrophe
INSERT INTO patients (mrn, family_name)
VALUES ('MRN00000001', 'O''Brien');

-- Address with special characters
INSERT INTO patients (mrn, street_address)
VALUES ('MRN00000001', '123 Main St, Apt #5');
```

## Validation Rules

1. **Foreign keys**: Referenced records must exist
2. **NOT NULL constraints**: Required fields must have values
3. **Data types**: Values must match column types
4. **Unique constraints**: No duplicate primary keys
5. **Check constraints**: Values within valid ranges

## Related Skills

- [csv.md](csv.md) - CSV export
- [../scenarios/patientsim/SKILL.md](../scenarios/patientsim/SKILL.md) - Patient data
- [../scenarios/membersim/SKILL.md](../scenarios/membersim/SKILL.md) - Claims data
- [../references/code-systems.md](../references/code-systems.md) - Code systems
