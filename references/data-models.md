# Data Models Reference

Canonical entity schemas for all HealthSim data types. Extracted from Domain Knowledge Base Section 2.

## Table of Contents

- [Core Person Model](#core-person-model)
- [PatientSim Models](#patientsim-models)
- [MemberSim Models](#membersim-models)
- [RxMemberSim Models](#rxmembersim-models)

---

## Core Person Model

The foundational person entity shared across all products:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Person",
  "type": "object",
  "required": ["id", "name", "birth_date", "gender"],
  "properties": {
    "id": {
      "type": "string",
      "description": "Unique identifier"
    },
    "name": {
      "type": "object",
      "required": ["given_name", "family_name"],
      "properties": {
        "given_name": { "type": "string" },
        "middle_name": { "type": "string" },
        "family_name": { "type": "string" },
        "suffix": { "type": "string" },
        "prefix": { "type": "string" }
      }
    },
    "birth_date": {
      "type": "string",
      "format": "date",
      "description": "YYYY-MM-DD format"
    },
    "gender": {
      "type": "string",
      "enum": ["M", "F", "O", "U"],
      "description": "M=Male, F=Female, O=Other, U=Unknown"
    },
    "address": {
      "type": "object",
      "properties": {
        "street_address": { "type": "string" },
        "street_address_2": { "type": "string" },
        "city": { "type": "string" },
        "state": { "type": "string", "pattern": "^[A-Z]{2}$" },
        "postal_code": { "type": "string" },
        "country": { "type": "string", "default": "US" }
      }
    },
    "contact": {
      "type": "object",
      "properties": {
        "phone": { "type": "string" },
        "phone_mobile": { "type": "string" },
        "email": { "type": "string", "format": "email" }
      }
    },
    "deceased": { "type": "boolean", "default": false },
    "death_date": { "type": "string", "format": "date" }
  }
}
```

---

## PatientSim Models

### Patient (extends Person)

```json
{
  "title": "Patient",
  "allOf": [{ "$ref": "#/definitions/Person" }],
  "properties": {
    "mrn": {
      "type": "string",
      "description": "Medical Record Number",
      "minLength": 1
    },
    "ssn": {
      "type": "string",
      "pattern": "^\\d{9}$",
      "description": "Social Security Number (9 digits, no dashes)"
    },
    "race": {
      "type": "string",
      "description": "Race/ethnicity"
    },
    "language": {
      "type": "string",
      "default": "en",
      "description": "Preferred language code"
    },
    "created_at": {
      "type": "string",
      "format": "date-time"
    }
  },
  "required": ["mrn"]
}
```

### Encounter

```json
{
  "title": "Encounter",
  "type": "object",
  "required": ["encounter_id", "patient_mrn", "class_code", "status", "admission_time"],
  "properties": {
    "encounter_id": { "type": "string", "minLength": 1 },
    "patient_mrn": { "type": "string", "minLength": 1 },
    "class_code": {
      "type": "string",
      "enum": ["I", "O", "E", "U", "OBS"],
      "description": "I=Inpatient, O=Outpatient, E=Emergency, U=Urgent, OBS=Observation"
    },
    "status": {
      "type": "string",
      "enum": ["planned", "arrived", "in-progress", "on-hold", "finished", "cancelled"]
    },
    "admission_time": { "type": "string", "format": "date-time" },
    "discharge_time": { "type": "string", "format": "date-time" },
    "facility": { "type": "string" },
    "department": { "type": "string" },
    "room": { "type": "string" },
    "bed": { "type": "string" },
    "chief_complaint": { "type": "string" },
    "admitting_diagnosis": { "type": "string" },
    "discharge_disposition": { "type": "string" },
    "attending_physician": { "type": "string" },
    "admitting_physician": { "type": "string" }
  }
}
```

**Encounter Class Codes:**

| Code | Description | Typical Duration |
|------|-------------|------------------|
| I | Inpatient | 1-14 days |
| O | Outpatient | 15-60 minutes |
| E | Emergency | 1-12 hours |
| U | Urgent Care | 30 min - 2 hours |
| OBS | Observation | 8-48 hours |

### Diagnosis

```json
{
  "title": "Diagnosis",
  "type": "object",
  "required": ["code", "description", "patient_mrn", "diagnosed_date"],
  "properties": {
    "code": {
      "type": "string",
      "description": "ICD-10 diagnosis code"
    },
    "description": { "type": "string" },
    "type": {
      "type": "string",
      "enum": ["admitting", "working", "final", "differential"],
      "default": "final"
    },
    "patient_mrn": { "type": "string" },
    "encounter_id": { "type": "string" },
    "diagnosed_date": { "type": "string", "format": "date" },
    "resolved_date": { "type": "string", "format": "date" }
  }
}
```

### Medication

```json
{
  "title": "Medication",
  "type": "object",
  "required": ["name", "dose", "route", "frequency", "patient_mrn", "start_date"],
  "properties": {
    "name": { "type": "string" },
    "code": { "type": "string", "description": "RxNorm or NDC code" },
    "dose": { "type": "string", "description": "e.g., '500 mg', '10 units'" },
    "route": {
      "type": "string",
      "description": "PO, IV, IM, SubQ, INH, etc."
    },
    "frequency": {
      "type": "string",
      "description": "QD, BID, TID, QID, PRN, Q8H, etc."
    },
    "patient_mrn": { "type": "string" },
    "encounter_id": { "type": "string" },
    "start_date": { "type": "string", "format": "date-time" },
    "end_date": { "type": "string", "format": "date-time" },
    "status": {
      "type": "string",
      "enum": ["active", "completed", "stopped", "on-hold"],
      "default": "active"
    },
    "prescriber": { "type": "string" },
    "indication": { "type": "string" }
  }
}
```

**Common Frequency Codes:**

| Code | Meaning |
|------|---------|
| QD | Once daily |
| BID | Twice daily |
| TID | Three times daily |
| QID | Four times daily |
| Q4H | Every 4 hours |
| Q6H | Every 6 hours |
| Q8H | Every 8 hours |
| Q12H | Every 12 hours |
| PRN | As needed |
| HS | At bedtime |
| AC | Before meals |
| PC | After meals |

### LabResult

```json
{
  "title": "LabResult",
  "type": "object",
  "required": ["test_name", "value", "patient_mrn", "collected_time"],
  "properties": {
    "test_name": { "type": "string" },
    "loinc_code": { "type": "string" },
    "value": { "type": "string" },
    "unit": { "type": "string" },
    "reference_range": { "type": "string" },
    "abnormal_flag": {
      "type": "string",
      "enum": ["H", "L", "HH", "LL", "A", "N", null],
      "description": "H=High, L=Low, HH=Critical High, LL=Critical Low, A=Abnormal, N=Normal"
    },
    "patient_mrn": { "type": "string" },
    "encounter_id": { "type": "string" },
    "collected_time": { "type": "string", "format": "date-time" },
    "resulted_time": { "type": "string", "format": "date-time" },
    "performing_lab": { "type": "string" },
    "ordering_provider": { "type": "string" }
  }
}
```

### VitalSign

```json
{
  "title": "VitalSign",
  "type": "object",
  "required": ["patient_mrn", "observation_time"],
  "properties": {
    "patient_mrn": { "type": "string" },
    "encounter_id": { "type": "string" },
    "observation_time": { "type": "string", "format": "date-time" },
    "temperature": {
      "type": "number",
      "minimum": 90,
      "maximum": 110,
      "description": "Temperature in Fahrenheit"
    },
    "heart_rate": {
      "type": "integer",
      "minimum": 0,
      "maximum": 300,
      "description": "Beats per minute"
    },
    "respiratory_rate": {
      "type": "integer",
      "minimum": 0,
      "maximum": 100,
      "description": "Breaths per minute"
    },
    "systolic_bp": {
      "type": "integer",
      "minimum": 0,
      "maximum": 300,
      "description": "mmHg"
    },
    "diastolic_bp": {
      "type": "integer",
      "minimum": 0,
      "maximum": 200,
      "description": "mmHg"
    },
    "spo2": {
      "type": "integer",
      "minimum": 0,
      "maximum": 100,
      "description": "Oxygen saturation percentage"
    },
    "height_cm": { "type": "number", "minimum": 0, "maximum": 300 },
    "weight_kg": { "type": "number", "minimum": 0, "maximum": 500 }
  }
}
```

**Vital Sign Reference Ranges (Adult):**

| Vital | Normal Min | Normal Max | Unit |
|-------|------------|------------|------|
| temperature | 97.0 | 99.5 | °F |
| heart_rate | 60 | 100 | bpm |
| respiratory_rate | 12 | 20 | /min |
| systolic_bp | 90 | 140 | mmHg |
| diastolic_bp | 60 | 90 | mmHg |
| spo2 | 95 | 100 | % |

---

## MemberSim Models

### Member (extends Person)

```json
{
  "title": "Member",
  "allOf": [{ "$ref": "#/definitions/Person" }],
  "required": ["member_id", "group_id", "coverage_start", "plan_code"],
  "properties": {
    "member_id": { "type": "string", "description": "Unique member identifier" },
    "subscriber_id": { "type": "string", "description": "For dependents, reference to subscriber" },
    "relationship_code": {
      "type": "string",
      "enum": ["18", "01", "19"],
      "default": "18",
      "description": "18=Self, 01=Spouse, 19=Child"
    },
    "group_id": { "type": "string", "description": "Employer/group identifier" },
    "coverage_start": { "type": "string", "format": "date" },
    "coverage_end": { "type": "string", "format": "date" },
    "plan_code": { "type": "string", "description": "Benefit plan identifier" },
    "pcp_npi": { "type": "string", "description": "Assigned PCP NPI (for HMO plans)" }
  }
}
```

### Claim

```json
{
  "title": "Claim",
  "type": "object",
  "required": ["claim_id", "claim_type", "member_id", "subscriber_id", "provider_npi", "service_date", "principal_diagnosis"],
  "properties": {
    "claim_id": { "type": "string" },
    "claim_type": {
      "type": "string",
      "enum": ["PROFESSIONAL", "INSTITUTIONAL", "DENTAL", "RX"]
    },
    "member_id": { "type": "string" },
    "subscriber_id": { "type": "string" },
    "provider_npi": { "type": "string", "pattern": "^\\d{10}$" },
    "facility_npi": { "type": "string" },
    "service_date": { "type": "string", "format": "date" },
    "admission_date": { "type": "string", "format": "date" },
    "discharge_date": { "type": "string", "format": "date" },
    "place_of_service": {
      "type": "string",
      "default": "11",
      "description": "11=Office, 21=Inpatient, 22=Outpatient, 23=ER"
    },
    "claim_lines": {
      "type": "array",
      "items": { "$ref": "#/definitions/ClaimLine" }
    },
    "principal_diagnosis": { "type": "string", "description": "ICD-10 code" },
    "other_diagnoses": {
      "type": "array",
      "items": { "type": "string" }
    },
    "authorization_number": { "type": "string" }
  }
}
```

### ClaimLine

```json
{
  "title": "ClaimLine",
  "type": "object",
  "required": ["line_number", "procedure_code", "service_date", "charge_amount"],
  "properties": {
    "line_number": { "type": "integer", "minimum": 1 },
    "procedure_code": { "type": "string", "description": "CPT/HCPCS code" },
    "procedure_modifiers": {
      "type": "array",
      "items": { "type": "string" },
      "maxItems": 4
    },
    "service_date": { "type": "string", "format": "date" },
    "units": { "type": "number", "default": 1 },
    "charge_amount": { "type": "number", "description": "Billed amount in dollars" },
    "diagnosis_pointers": {
      "type": "array",
      "items": { "type": "integer" },
      "default": [1]
    },
    "revenue_code": { "type": "string", "description": "For institutional claims" },
    "ndc_code": { "type": "string", "description": "Drug code if applicable" },
    "place_of_service": { "type": "string", "default": "11" }
  }
}
```

### Plan

```json
{
  "title": "Plan",
  "type": "object",
  "required": ["plan_code", "plan_name", "plan_type"],
  "properties": {
    "plan_code": { "type": "string" },
    "plan_name": { "type": "string" },
    "plan_type": {
      "type": "string",
      "enum": ["HMO", "PPO", "EPO", "POS", "HDHP"]
    },
    "coverage_type": {
      "type": "string",
      "enum": ["MEDICAL", "DENTAL", "VISION", "RX"],
      "default": "MEDICAL"
    },
    "deductible_individual": { "type": "number", "default": 500 },
    "deductible_family": { "type": "number", "default": 1500 },
    "oop_max_individual": { "type": "number", "default": 3000 },
    "oop_max_family": { "type": "number", "default": 6000 },
    "copay_pcp": { "type": "number", "default": 25 },
    "copay_specialist": { "type": "number", "default": 50 },
    "copay_er": { "type": "number", "default": 250 },
    "coinsurance": { "type": "number", "default": 0.20, "description": "0.20 = 20%" },
    "requires_pcp": { "type": "boolean", "default": false },
    "requires_referral": { "type": "boolean", "default": false }
  }
}
```

### Accumulator

```json
{
  "title": "Accumulator",
  "type": "object",
  "required": ["member_id", "plan_year", "deductible_limit", "oop_limit"],
  "properties": {
    "member_id": { "type": "string" },
    "plan_year": { "type": "integer" },
    "deductible_applied": { "type": "number", "default": 0 },
    "deductible_limit": { "type": "number" },
    "oop_applied": { "type": "number", "default": 0 },
    "oop_limit": { "type": "number" },
    "last_updated": { "type": "string", "format": "date-time" }
  }
}
```

---

## RxMemberSim Models

### Prescription

```json
{
  "title": "Prescription",
  "type": "object",
  "required": ["prescription_number", "ndc", "drug_name", "quantity_prescribed", "days_supply", "prescriber_npi", "written_date", "expiration_date"],
  "properties": {
    "prescription_number": { "type": "string" },
    "ndc": { "type": "string", "pattern": "^\\d{11}$" },
    "drug_name": { "type": "string" },
    "quantity_prescribed": { "type": "number" },
    "days_supply": { "type": "integer" },
    "refills_authorized": { "type": "integer", "default": 0 },
    "refills_remaining": { "type": "integer", "default": 0 },
    "prescriber_npi": { "type": "string", "pattern": "^\\d{10}$" },
    "prescriber_name": { "type": "string" },
    "prescriber_dea": { "type": "string" },
    "written_date": { "type": "string", "format": "date" },
    "expiration_date": { "type": "string", "format": "date" },
    "daw_code": {
      "type": "string",
      "enum": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
      "default": "0",
      "description": "Dispense As Written code"
    },
    "diagnosis_codes": {
      "type": "array",
      "items": { "type": "string" }
    },
    "directions": { "type": "string" }
  }
}
```

**DAW Codes:**

| Code | Description |
|------|-------------|
| 0 | No Product Selection Indicated |
| 1 | Substitution Not Allowed by Prescriber |
| 2 | Patient Requested Brand |
| 3 | Pharmacist Selected |
| 4 | Generic Not Available |
| 5 | Brand Dispensed as Generic |
| 6 | Override |
| 7 | Brand Mandated by Law |
| 8 | Generic Not Available in Marketplace |
| 9 | Other |

### PharmacyClaim

```json
{
  "title": "PharmacyClaim",
  "type": "object",
  "required": ["claim_id", "transaction_code", "service_date", "pharmacy_npi", "member_id", "cardholder_id", "bin", "pcn", "group_number", "prescription_number", "ndc", "quantity_dispensed", "days_supply", "prescriber_npi"],
  "properties": {
    "claim_id": { "type": "string" },
    "transaction_code": {
      "type": "string",
      "enum": ["B1", "B2", "B3"],
      "description": "B1=Billing, B2=Reversal, B3=Rebill"
    },
    "service_date": { "type": "string", "format": "date" },
    "pharmacy_npi": { "type": "string" },
    "pharmacy_ncpdp": { "type": "string" },
    "member_id": { "type": "string" },
    "cardholder_id": { "type": "string" },
    "person_code": { "type": "string" },
    "bin": { "type": "string", "pattern": "^\\d{6}$" },
    "pcn": { "type": "string" },
    "group_number": { "type": "string" },
    "prescription_number": { "type": "string" },
    "fill_number": { "type": "integer", "minimum": 0 },
    "ndc": { "type": "string" },
    "quantity_dispensed": { "type": "number" },
    "days_supply": { "type": "integer" },
    "daw_code": { "type": "string" },
    "compound_code": { "type": "string", "default": "0" },
    "prescriber_npi": { "type": "string" },
    "ingredient_cost_submitted": { "type": "number" },
    "dispensing_fee_submitted": { "type": "number" },
    "usual_customary_charge": { "type": "number" },
    "gross_amount_due": { "type": "number" },
    "prior_auth_number": { "type": "string" },
    "prior_auth_type": { "type": "string" },
    "dur_pps_code_counter": { "type": "integer", "default": 0 },
    "dur_reason_for_service": { "type": "string" },
    "dur_professional_service": { "type": "string" },
    "dur_result_of_service": { "type": "string" }
  }
}
```

### FormularyDrug

```json
{
  "title": "FormularyDrug",
  "type": "object",
  "required": ["ndc", "gpi", "drug_name", "tier", "covered"],
  "properties": {
    "ndc": { "type": "string" },
    "gpi": { "type": "string", "description": "Generic Product Identifier" },
    "drug_name": { "type": "string" },
    "tier": { "type": "integer", "minimum": 1, "maximum": 5 },
    "covered": { "type": "boolean", "default": true },
    "requires_pa": { "type": "boolean", "default": false },
    "requires_step_therapy": { "type": "boolean", "default": false },
    "step_therapy_group": { "type": "string" },
    "quantity_limit": { "type": "integer" },
    "quantity_limit_days": { "type": "integer" },
    "max_days_supply": { "type": "integer" },
    "min_age": { "type": "integer" },
    "max_age": { "type": "integer" },
    "gender_restriction": { "type": "string", "enum": ["M", "F", null] }
  }
}
```

**Formulary Tier Structure:**

| Tier | Name | Typical Copay |
|------|------|---------------|
| 1 | Preferred Generic | $10 |
| 2 | Non-Preferred Generic | $25 |
| 3 | Preferred Brand | $50 |
| 4 | Non-Preferred Brand | $80 |
| 5 | Specialty | 25% coinsurance |

---

## Required Fields Summary

| Entity | Required Fields |
|--------|-----------------|
| Person | id, name.given_name, name.family_name, birth_date, gender |
| Patient | Person fields + mrn |
| Encounter | encounter_id, patient_mrn, class_code, status, admission_time |
| Diagnosis | code, description, patient_mrn, diagnosed_date |
| Medication | name, dose, route, frequency, patient_mrn, start_date |
| LabResult | test_name, value, patient_mrn, collected_time |
| Member | Person fields + member_id, group_id, coverage_start, plan_code |
| Claim | claim_id, claim_type, member_id, provider_npi, service_date, principal_diagnosis |
| PharmacyClaim | claim_id, service_date, pharmacy_npi, member_id, ndc, quantity_dispensed |

## Referential Integrity

| Source | Target | Required |
|--------|--------|----------|
| Encounter.patient_mrn | Patient.mrn | Yes |
| Diagnosis.patient_mrn | Patient.mrn | Yes |
| Diagnosis.encounter_id | Encounter.encounter_id | No |
| Medication.patient_mrn | Patient.mrn | Yes |
| LabResult.patient_mrn | Patient.mrn | Yes |
| Claim.member_id | Member.member_id | Yes |
| Member.subscriber_id | Member.member_id | No (dependents only) |
| PharmacyClaim.member_id | Member.member_id | Yes |
