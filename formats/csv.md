# CSV Export Format

## Trigger Phrases

- CSV
- as CSV
- CSV file
- comma separated
- spreadsheet
- Excel
- export to CSV
- tabular format
- flat file

## Overview

This skill exports HealthSim entities to CSV (Comma-Separated Values) format for use in spreadsheets, data analysis tools, and bulk data loading. Each entity type maps to a specific CSV schema.

## Export Options

| Option | Values | Default | Description |
|--------|--------|---------|-------------|
| delimiter | `,`, `\t`, `|`, `;` | `,` | Field separator |
| quote_char | `"`, `'` | `"` | String quotation |
| header | true, false | true | Include header row |
| null_value | empty, `NULL`, `\N` | empty | How to represent nulls |
| date_format | ISO, US, EU | ISO | Date formatting |
| encoding | UTF-8, UTF-16, ASCII | UTF-8 | Character encoding |

## Entity Schemas

### patients.csv

```csv
mrn,given_name,family_name,middle_name,birth_date,gender,ssn,street_address,city,state,postal_code,country,phone_home,phone_work,email,language,marital_status,race,ethnicity,deceased,deceased_date
MRN00000001,John,Smith,Michael,1970-03-15,M,123-45-6789,123 Main St,Springfield,IL,62701,USA,555-123-4567,555-987-6543,john.smith@email.com,ENG,M,2106-3,2186-5,N,
MRN00000002,Maria,Garcia,Elena,1955-10-20,F,987-65-4321,456 Oak Ave,Springfield,IL,62702,USA,555-876-5432,,maria.garcia@email.com,SPA,W,2106-3,2135-2,N,
```

| Column | Type | Description |
|--------|------|-------------|
| mrn | string | Medical record number |
| given_name | string | First name |
| family_name | string | Last name |
| middle_name | string | Middle name (optional) |
| birth_date | date | YYYY-MM-DD |
| gender | string | M, F, O, U |
| ssn | string | Social Security Number |
| street_address | string | Street address |
| city | string | City |
| state | string | State code (2 letters) |
| postal_code | string | ZIP code |
| country | string | Country code |
| phone_home | string | Home phone |
| phone_work | string | Work phone |
| email | string | Email address |
| language | string | Preferred language code |
| marital_status | string | S, M, D, W, etc. |
| race | string | CDC race code |
| ethnicity | string | CDC ethnicity code |
| deceased | string | Y/N |
| deceased_date | date | YYYY-MM-DD if deceased |

### encounters.csv

```csv
encounter_id,patient_mrn,encounter_class,encounter_type,status,period_start,period_end,facility_code,facility_name,location_unit,location_room,location_bed,attending_npi,attending_name,admission_source,discharge_disposition,reason_code,reason_description
ENC0000000001,MRN00000001,I,inpatient,finished,2025-01-10T14:00:00,2025-01-15T10:00:00,SPRINGFIELD,Springfield Hospital,MED,201,A,1234567890,Dr. Robert Johnson,7,01,R06.00,Dyspnea
ENC0000000002,MRN00000002,O,office_visit,finished,2025-01-15T09:00:00,2025-01-15T09:30:00,CLINIC01,Main Street Clinic,,,,,9876543210,Dr. Lisa Chen,,,,
```

| Column | Type | Description |
|--------|------|-------------|
| encounter_id | string | Unique encounter identifier |
| patient_mrn | string | Patient MRN (foreign key) |
| encounter_class | string | I, O, E, U, OBS |
| encounter_type | string | inpatient, office_visit, etc. |
| status | string | planned, arrived, in-progress, finished |
| period_start | datetime | Admission/start time |
| period_end | datetime | Discharge/end time |
| facility_code | string | Facility identifier |
| facility_name | string | Facility name |
| location_unit | string | Unit/department |
| location_room | string | Room number |
| location_bed | string | Bed identifier |
| attending_npi | string | Attending physician NPI |
| attending_name | string | Attending physician name |
| admission_source | string | Admit source code |
| discharge_disposition | string | Discharge disposition code |
| reason_code | string | Primary reason ICD-10 |
| reason_description | string | Reason description |

### diagnoses.csv

```csv
diagnosis_id,patient_mrn,encounter_id,code,code_system,description,type,onset_date,abatement_date,clinical_status,verification_status,severity,diagnosed_by_npi
DX0000000001,MRN00000001,ENC0000000001,I50.23,ICD-10-CM,Acute on chronic systolic heart failure,principal,2020-03-15,,active,confirmed,moderate,1234567890
DX0000000002,MRN00000001,ENC0000000001,I10,ICD-10-CM,Essential hypertension,secondary,2015-06-20,,active,confirmed,,1234567890
DX0000000003,MRN00000001,ENC0000000001,E11.9,ICD-10-CM,Type 2 diabetes mellitus,secondary,2018-09-10,,active,confirmed,,1234567890
```

| Column | Type | Description |
|--------|------|-------------|
| diagnosis_id | string | Unique diagnosis identifier |
| patient_mrn | string | Patient MRN |
| encounter_id | string | Encounter ID |
| code | string | ICD-10-CM code |
| code_system | string | ICD-10-CM |
| description | string | Diagnosis description |
| type | string | principal, admitting, secondary, working |
| onset_date | date | When condition started |
| abatement_date | date | When condition resolved |
| clinical_status | string | active, resolved, inactive |
| verification_status | string | confirmed, provisional, differential |
| severity | string | mild, moderate, severe |
| diagnosed_by_npi | string | Diagnosing provider NPI |

### procedures.csv

```csv
procedure_id,patient_mrn,encounter_id,code,code_system,description,performed_datetime,performer_npi,performer_name,body_site,status
PX0000000001,MRN00000001,ENC0000000001,99223,CPT,Initial hospital care high severity,2025-01-10T16:00:00,1234567890,Dr. Robert Johnson,,completed
PX0000000002,MRN00000001,ENC0000000001,93000,CPT,Electrocardiogram routine,2025-01-10T15:30:00,1234567890,Dr. Robert Johnson,,completed
```

### medications.csv

```csv
medication_id,patient_mrn,encounter_id,ndc,rxnorm,drug_name,dose_value,dose_unit,route,frequency,start_date,end_date,status,prescriber_npi,prescriber_name,indication_code,refills_authorized,quantity_dispensed,days_supply
MED0000000001,MRN00000001,ENC0000000001,00093505601,314076,Lisinopril 10mg Tab,10,mg,oral,daily,2025-01-15,,active,1234567890,Dr. Robert Johnson,I10,5,30,30
MED0000000002,MRN00000001,ENC0000000001,00093085601,6809,Metformin 500mg Tab,500,mg,oral,BID,2025-01-15,,active,1234567890,Dr. Robert Johnson,E11.9,5,60,30
```

### observations.csv (Labs/Vitals)

```csv
observation_id,patient_mrn,encounter_id,code,code_system,description,value,unit,reference_low,reference_high,interpretation,effective_datetime,status,performer_npi,specimen_type
OBS0000000001,MRN00000001,ENC0000000001,2345-7,LOINC,Glucose,98,mg/dL,70,100,N,2025-01-15T15:00:00,final,9876543210,Blood
OBS0000000002,MRN00000001,ENC0000000001,2160-0,LOINC,Creatinine,1.1,mg/dL,0.7,1.3,N,2025-01-15T15:00:00,final,9876543210,Blood
OBS0000000003,MRN00000001,ENC0000000001,8480-6,LOINC,Systolic BP,128,mmHg,90,120,H,2025-01-15T14:30:00,final,1234567890,
```

### orders.csv

```csv
order_id,patient_mrn,encounter_id,order_type,code,code_system,description,priority,status,ordered_datetime,scheduled_datetime,completed_datetime,ordering_provider_npi,ordering_provider_name,performer_npi,performer_name
ORD0000000001,MRN00000001,ENC0000000001,LAB,80053,CPT,Comprehensive Metabolic Panel,R,completed,2025-01-15T14:30:00,,2025-01-15T16:00:00,1234567890,Dr. Robert Johnson,9876543210,Mary Jones MT
ORD0000000002,MRN00000001,ENC0000000001,RAD,71046,CPT,Chest X-ray 2 views,R,completed,2025-01-15T10:15:00,,2025-01-15T12:00:00,1234567890,Dr. Robert Johnson,4567890123,Dr. Sarah Williams
```

### claims.csv

```csv
claim_id,member_id,claim_type,status,service_from_date,service_to_date,facility_npi,facility_name,billing_provider_npi,rendering_provider_npi,principal_diagnosis,total_charge,total_allowed,total_paid,patient_responsibility,adjudicated_date,auth_number
CLM20250115001,MEM001234,professional,paid,2025-01-15,2025-01-15,,,,1234567890,E11.9,175.00,150.00,125.00,25.00,2025-01-16,
CLM20250115002,MEM001234,institutional,paid,2025-01-10,2025-01-15,1234567890,Springfield Hospital,1234567890,,I50.23,45000.00,38000.00,35000.00,3000.00,2025-01-20,AUTH001
```

### claim_lines.csv

```csv
claim_id,line_number,procedure_code,procedure_modifier,revenue_code,ndc,description,service_date,quantity,charge_amount,allowed_amount,paid_amount,deductible,copay,coinsurance,diagnosis_pointer,place_of_service
CLM20250115001,1,99214,,,,Office visit established,2025-01-15,1,175.00,150.00,125.00,0.00,25.00,0.00,1,11
CLM20250115002,1,99223,,0120,,Hospital initial care,2025-01-10,1,1800.00,1500.00,1400.00,100.00,0.00,0.00,1,21
CLM20250115002,2,,,0250,,Pharmacy,2025-01-12,1,450.00,400.00,400.00,0.00,0.00,0.00,,21
```

### pharmacy_claims.csv

```csv
claim_id,member_id,prescription_number,fill_date,ndc,drug_name,quantity_dispensed,days_supply,pharmacy_npi,pharmacy_name,prescriber_npi,prescriber_name,ingredient_cost,dispensing_fee,patient_pay,plan_pay,copay,coinsurance,formulary_tier,daw_code,transaction_code
RX20250115001,MEM001234,SPX001234,2025-01-15,00093505601,Lisinopril 10mg Tab,30,30,1122334455,Main Street Pharmacy,1234567890,Dr. Robert Johnson,8.50,2.00,10.00,0.50,10.00,0.00,1,0,B1
```

## Multi-File Export

When exporting a complete patient record, generate related CSV files:

```
export/
├── patients.csv
├── encounters.csv
├── diagnoses.csv
├── procedures.csv
├── medications.csv
├── observations.csv
├── orders.csv
├── allergies.csv
├── claims.csv
├── claim_lines.csv
└── pharmacy_claims.csv
```

## Example Transformations

### Single Patient Export

**Request:** "Export patient MRN00000001 to CSV"

**Output:**
```csv
mrn,given_name,family_name,birth_date,gender,street_address,city,state,postal_code
MRN00000001,John,Smith,1970-03-15,M,123 Main St,Springfield,IL,62701
```

### Batch Patient Export

**Request:** "Export 100 patients as CSV"

**Output:**
```csv
mrn,given_name,family_name,birth_date,gender,street_address,city,state,postal_code
MRN00000001,John,Smith,1970-03-15,M,123 Main St,Springfield,IL,62701
MRN00000002,Maria,Garcia,1955-10-20,F,456 Oak Ave,Springfield,IL,62702
MRN00000003,Eleanor,Thompson,1950-08-12,F,789 Elm St,Springfield,IL,62703
...
```

### Claims Export with Options

**Request:** "Export claims as pipe-delimited CSV with NULL markers"

**Output:**
```csv
claim_id|member_id|claim_type|status|service_date|total_charge|total_paid
CLM20250115001|MEM001234|professional|paid|2025-01-15|175.00|125.00
CLM20250115002|MEM001234|institutional|paid|2025-01-10|45000.00|35000.00
CLM20250115003|MEM001234|professional|denied|2025-01-16|200.00|NULL
```

## Special Handling

### Escaping Rules

| Scenario | Example Input | CSV Output |
|----------|---------------|------------|
| Comma in value | `Smith, Jr.` | `"Smith, Jr."` |
| Quote in value | `O'Brien` | `O'Brien` |
| Double quote in value | `He said "hello"` | `"He said ""hello"""` |
| Newline in value | `Line1\nLine2` | `"Line1\nLine2"` |

### Date Formats

| Format | Example | Use When |
|--------|---------|----------|
| ISO | 2025-01-15 | Default, international |
| US | 01/15/2025 | US systems |
| EU | 15/01/2025 | European systems |
| Timestamp | 2025-01-15T14:30:00 | Include time |

### Null Handling

| Option | Empty | With Value |
|--------|-------|------------|
| empty | `,,,` | Default behavior |
| NULL | `,NULL,NULL,` | Database loading |
| \N | `,\N,\N,` | MySQL LOAD DATA |

## Validation Rules

1. **Header required by default**: First row contains column names
2. **Consistent columns**: Every row same number of fields
3. **Proper quoting**: Fields with delimiters must be quoted
4. **UTF-8 encoding**: Default encoding for special characters
5. **Date consistency**: All dates in same format within file
6. **No trailing delimiters**: Lines end after last field

## Related Skills

- [sql.md](sql.md) - SQL INSERT statements
- [fhir-r4.md](fhir-r4.md) - FHIR format
- [../scenarios/patientsim/SKILL.md](../scenarios/patientsim/SKILL.md) - Patient data
- [../scenarios/membersim/SKILL.md](../scenarios/membersim/SKILL.md) - Claims data
