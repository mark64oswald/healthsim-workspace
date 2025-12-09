# Data Models Reference

Canonical entity schemas for all HealthSim data types. All scenarios use these models to ensure consistency.

## Table of Contents

- [Clinical Entities](#clinical-entities)
  - [Person](#person)
  - [Patient](#patient)
  - [Encounter](#encounter)
  - [Diagnosis](#diagnosis)
  - [Procedure](#procedure)
  - [Medication](#medication)
  - [LabResult](#labresult)
  - [VitalSign](#vitalsign)
- [Insurance Entities](#insurance-entities)
  - [Member](#member)
  - [Plan](#plan)
  - [Claim](#claim)
  - [ClaimLine](#claimline)
  - [Payment](#payment)
  - [Accumulator](#accumulator)
- [Pharmacy Entities](#pharmacy-entities)
  - [Prescription](#prescription)
  - [PharmacyClaim](#pharmacyclaim)
  - [ClaimResponse](#claimresponse)
  - [FormularyDrug](#formularydrug)

---

## Clinical Entities

### Person

Base demographic entity inherited by Patient and Member.

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["id", "name", "birth_date", "gender"],
  "properties": {
    "id": {
      "type": "string",
      "description": "Unique identifier",
      "pattern": "^[A-Z0-9]{8,12}$"
    },
    "name": {
      "type": "object",
      "required": ["family", "given"],
      "properties": {
        "family": { "type": "string", "minLength": 1 },
        "given": {
          "type": "array",
          "items": { "type": "string" },
          "minItems": 1
        },
        "prefix": { "type": "string" },
        "suffix": { "type": "string" }
      }
    },
    "birth_date": {
      "type": "string",
      "format": "date",
      "description": "YYYY-MM-DD format"
    },
    "gender": {
      "type": "string",
      "enum": ["male", "female", "other", "unknown"]
    },
    "address": {
      "type": "object",
      "properties": {
        "line": { "type": "array", "items": { "type": "string" } },
        "city": { "type": "string" },
        "state": { "type": "string", "pattern": "^[A-Z]{2}$" },
        "postal_code": { "type": "string", "pattern": "^[0-9]{5}(-[0-9]{4})?$" },
        "country": { "type": "string", "default": "US" }
      }
    },
    "phone": {
      "type": "string",
      "pattern": "^[0-9]{3}-[0-9]{3}-[0-9]{4}$"
    },
    "email": {
      "type": "string",
      "format": "email"
    },
    "ssn": {
      "type": "string",
      "pattern": "^[0-9]{3}-[0-9]{2}-[0-9]{4}$",
      "description": "Social Security Number (synthetic)"
    },
    "race": {
      "type": "string",
      "enum": ["white", "black", "asian", "native", "pacific", "other", "unknown"]
    },
    "ethnicity": {
      "type": "string",
      "enum": ["hispanic", "non-hispanic", "unknown"]
    },
    "language": {
      "type": "string",
      "default": "en"
    }
  }
}
```

### Patient

Clinical patient entity extending Person with medical context.

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "allOf": [{ "$ref": "#/definitions/Person" }],
  "required": ["mrn", "id", "name", "birth_date", "gender"],
  "properties": {
    "mrn": {
      "type": "string",
      "description": "Medical Record Number",
      "pattern": "^MRN[0-9]{8}$"
    },
    "identifiers": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "system": { "type": "string", "format": "uri" },
          "value": { "type": "string" }
        }
      }
    },
    "active": {
      "type": "boolean",
      "default": true
    },
    "deceased": {
      "type": "boolean",
      "default": false
    },
    "deceased_date": {
      "type": "string",
      "format": "date"
    },
    "marital_status": {
      "type": "string",
      "enum": ["single", "married", "divorced", "widowed", "unknown"]
    },
    "primary_care_provider": {
      "type": "object",
      "properties": {
        "npi": { "type": "string", "pattern": "^[0-9]{10}$" },
        "name": { "type": "string" }
      }
    },
    "emergency_contact": {
      "type": "object",
      "properties": {
        "name": { "type": "string" },
        "relationship": { "type": "string" },
        "phone": { "type": "string" }
      }
    }
  }
}
```

### Encounter

A clinical interaction between patient and provider.

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["id", "patient_id", "type", "status", "period"],
  "properties": {
    "id": {
      "type": "string",
      "pattern": "^ENC[0-9]{10}$"
    },
    "patient_id": {
      "type": "string",
      "description": "Reference to Patient.mrn"
    },
    "type": {
      "type": "string",
      "enum": ["ambulatory", "emergency", "inpatient", "observation", "virtual"],
      "description": "Encounter class"
    },
    "status": {
      "type": "string",
      "enum": ["planned", "arrived", "in-progress", "finished", "cancelled"]
    },
    "period": {
      "type": "object",
      "required": ["start"],
      "properties": {
        "start": { "type": "string", "format": "date-time" },
        "end": { "type": "string", "format": "date-time" }
      }
    },
    "reason": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "code": { "type": "string" },
          "system": { "type": "string" },
          "display": { "type": "string" }
        }
      }
    },
    "location": {
      "type": "object",
      "properties": {
        "facility_name": { "type": "string" },
        "facility_npi": { "type": "string", "pattern": "^[0-9]{10}$" },
        "department": { "type": "string" },
        "room": { "type": "string" },
        "bed": { "type": "string" }
      }
    },
    "provider": {
      "type": "object",
      "properties": {
        "npi": { "type": "string", "pattern": "^[0-9]{10}$" },
        "name": { "type": "string" },
        "specialty": { "type": "string" }
      }
    },
    "service_type": {
      "type": "string",
      "description": "Service category code"
    },
    "place_of_service": {
      "type": "string",
      "pattern": "^[0-9]{2}$",
      "description": "CMS Place of Service code"
    },
    "admission": {
      "type": "object",
      "description": "For inpatient encounters",
      "properties": {
        "admit_source": { "type": "string" },
        "admit_type": { "type": "string" },
        "discharge_disposition": { "type": "string" },
        "drg": {
          "type": "object",
          "properties": {
            "code": { "type": "string" },
            "description": { "type": "string" },
            "weight": { "type": "number" }
          }
        }
      }
    },
    "diagnoses": {
      "type": "array",
      "items": { "$ref": "#/definitions/Diagnosis" }
    },
    "procedures": {
      "type": "array",
      "items": { "$ref": "#/definitions/Procedure" }
    }
  }
}
```

### Diagnosis

A clinical diagnosis assigned to a patient.

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["code", "system", "display"],
  "properties": {
    "id": {
      "type": "string",
      "pattern": "^DX[0-9]{10}$"
    },
    "patient_id": { "type": "string" },
    "encounter_id": { "type": "string" },
    "code": {
      "type": "string",
      "description": "ICD-10-CM code",
      "pattern": "^[A-Z][0-9]{2}(\\.[0-9A-Z]{1,4})?$"
    },
    "system": {
      "type": "string",
      "const": "http://hl7.org/fhir/sid/icd-10-cm"
    },
    "display": {
      "type": "string",
      "description": "Human-readable diagnosis name"
    },
    "type": {
      "type": "string",
      "enum": ["principal", "admitting", "secondary", "working", "billing"],
      "default": "secondary"
    },
    "rank": {
      "type": "integer",
      "minimum": 1,
      "description": "Diagnosis sequence number"
    },
    "onset_date": {
      "type": "string",
      "format": "date"
    },
    "abatement_date": {
      "type": "string",
      "format": "date",
      "description": "Resolution date if resolved"
    },
    "status": {
      "type": "string",
      "enum": ["active", "resolved", "inactive", "recurrence"]
    },
    "verification": {
      "type": "string",
      "enum": ["confirmed", "provisional", "differential", "refuted"]
    },
    "poa": {
      "type": "string",
      "enum": ["Y", "N", "U", "W", "1"],
      "description": "Present on Admission indicator"
    }
  }
}
```

### Procedure

A clinical procedure performed on a patient.

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["code", "system", "display", "performed_date"],
  "properties": {
    "id": {
      "type": "string",
      "pattern": "^PRC[0-9]{10}$"
    },
    "patient_id": { "type": "string" },
    "encounter_id": { "type": "string" },
    "code": {
      "type": "string",
      "description": "CPT or ICD-10-PCS code"
    },
    "system": {
      "type": "string",
      "enum": [
        "http://www.ama-assn.org/go/cpt",
        "http://hl7.org/fhir/sid/icd-10-pcs",
        "http://snomed.info/sct"
      ]
    },
    "display": { "type": "string" },
    "performed_date": {
      "type": "string",
      "format": "date-time"
    },
    "performer": {
      "type": "object",
      "properties": {
        "npi": { "type": "string" },
        "name": { "type": "string" },
        "role": { "type": "string" }
      }
    },
    "body_site": {
      "type": "object",
      "properties": {
        "code": { "type": "string" },
        "display": { "type": "string" }
      }
    },
    "outcome": {
      "type": "string",
      "enum": ["successful", "unsuccessful", "partial"]
    },
    "modifiers": {
      "type": "array",
      "items": {
        "type": "string",
        "pattern": "^[0-9A-Z]{2}$"
      },
      "description": "CPT modifier codes"
    },
    "units": {
      "type": "integer",
      "minimum": 1,
      "default": 1
    }
  }
}
```

### Medication

A medication prescribed or administered to a patient.

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["patient_id", "medication", "status"],
  "properties": {
    "id": {
      "type": "string",
      "pattern": "^MED[0-9]{10}$"
    },
    "patient_id": { "type": "string" },
    "encounter_id": { "type": "string" },
    "medication": {
      "type": "object",
      "required": ["name"],
      "properties": {
        "name": { "type": "string" },
        "rxnorm": {
          "type": "string",
          "pattern": "^[0-9]+$"
        },
        "ndc": {
          "type": "string",
          "pattern": "^[0-9]{11}$"
        },
        "strength": { "type": "string" },
        "form": {
          "type": "string",
          "enum": ["tablet", "capsule", "liquid", "injection", "patch", "inhaler", "cream", "drops"]
        }
      }
    },
    "status": {
      "type": "string",
      "enum": ["active", "completed", "stopped", "on-hold", "cancelled"]
    },
    "intent": {
      "type": "string",
      "enum": ["order", "plan", "proposal"]
    },
    "dosage": {
      "type": "object",
      "properties": {
        "text": { "type": "string" },
        "dose_quantity": { "type": "number" },
        "dose_unit": { "type": "string" },
        "frequency": { "type": "string" },
        "route": {
          "type": "string",
          "enum": ["oral", "intravenous", "intramuscular", "subcutaneous", "topical", "inhalation", "ophthalmic", "otic"]
        },
        "as_needed": { "type": "boolean", "default": false },
        "max_dose_per_period": { "type": "string" }
      }
    },
    "prescriber": {
      "type": "object",
      "properties": {
        "npi": { "type": "string" },
        "name": { "type": "string" }
      }
    },
    "dispense": {
      "type": "object",
      "properties": {
        "quantity": { "type": "number" },
        "days_supply": { "type": "integer" },
        "refills_allowed": { "type": "integer" },
        "refills_remaining": { "type": "integer" }
      }
    },
    "effective_period": {
      "type": "object",
      "properties": {
        "start": { "type": "string", "format": "date" },
        "end": { "type": "string", "format": "date" }
      }
    },
    "reason": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "code": { "type": "string" },
          "display": { "type": "string" }
        }
      }
    },
    "substitution": {
      "type": "object",
      "properties": {
        "allowed": { "type": "boolean" },
        "reason": { "type": "string" }
      }
    }
  }
}
```

### LabResult

A laboratory test result.

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["patient_id", "code", "status", "effective_date"],
  "properties": {
    "id": {
      "type": "string",
      "pattern": "^LAB[0-9]{10}$"
    },
    "patient_id": { "type": "string" },
    "encounter_id": { "type": "string" },
    "code": {
      "type": "object",
      "required": ["code", "display"],
      "properties": {
        "code": { "type": "string" },
        "system": {
          "type": "string",
          "default": "http://loinc.org"
        },
        "display": { "type": "string" }
      }
    },
    "status": {
      "type": "string",
      "enum": ["registered", "preliminary", "final", "amended", "corrected", "cancelled"]
    },
    "effective_date": {
      "type": "string",
      "format": "date-time"
    },
    "issued": {
      "type": "string",
      "format": "date-time"
    },
    "value": {
      "oneOf": [
        {
          "type": "object",
          "properties": {
            "type": { "const": "quantity" },
            "value": { "type": "number" },
            "unit": { "type": "string" },
            "system": { "type": "string" },
            "code": { "type": "string" }
          }
        },
        {
          "type": "object",
          "properties": {
            "type": { "const": "string" },
            "value": { "type": "string" }
          }
        },
        {
          "type": "object",
          "properties": {
            "type": { "const": "codeable" },
            "code": { "type": "string" },
            "display": { "type": "string" }
          }
        }
      ]
    },
    "reference_range": {
      "type": "object",
      "properties": {
        "low": { "type": "number" },
        "high": { "type": "number" },
        "unit": { "type": "string" },
        "text": { "type": "string" }
      }
    },
    "interpretation": {
      "type": "string",
      "enum": ["N", "L", "H", "LL", "HH", "A", "AA"],
      "description": "N=Normal, L=Low, H=High, LL=Critical Low, HH=Critical High, A=Abnormal, AA=Critical Abnormal"
    },
    "specimen": {
      "type": "object",
      "properties": {
        "type": { "type": "string" },
        "collected_date": { "type": "string", "format": "date-time" }
      }
    },
    "performer": {
      "type": "object",
      "properties": {
        "lab_name": { "type": "string" },
        "npi": { "type": "string" }
      }
    },
    "note": { "type": "string" }
  }
}
```

### VitalSign

A patient vital sign measurement.

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["patient_id", "type", "value", "effective_date"],
  "properties": {
    "id": {
      "type": "string",
      "pattern": "^VIT[0-9]{10}$"
    },
    "patient_id": { "type": "string" },
    "encounter_id": { "type": "string" },
    "type": {
      "type": "string",
      "enum": ["blood_pressure", "heart_rate", "respiratory_rate", "temperature", "oxygen_saturation", "height", "weight", "bmi"]
    },
    "code": {
      "type": "object",
      "properties": {
        "code": { "type": "string" },
        "system": { "type": "string", "default": "http://loinc.org" },
        "display": { "type": "string" }
      }
    },
    "value": {
      "oneOf": [
        {
          "type": "object",
          "description": "Single value vital",
          "properties": {
            "value": { "type": "number" },
            "unit": { "type": "string" }
          }
        },
        {
          "type": "object",
          "description": "Blood pressure (systolic/diastolic)",
          "properties": {
            "systolic": { "type": "number" },
            "diastolic": { "type": "number" },
            "unit": { "type": "string", "const": "mmHg" }
          }
        }
      ]
    },
    "effective_date": {
      "type": "string",
      "format": "date-time"
    },
    "status": {
      "type": "string",
      "enum": ["final", "amended", "entered-in-error"],
      "default": "final"
    },
    "method": {
      "type": "string",
      "description": "Measurement method"
    },
    "body_site": {
      "type": "string",
      "description": "Where measurement was taken"
    },
    "interpretation": {
      "type": "string",
      "enum": ["normal", "low", "high", "critical"]
    }
  }
}
```

**Vital Sign LOINC Codes:**

| Type | LOINC | Display | Unit |
|------|-------|---------|------|
| blood_pressure | 85354-9 | Blood pressure panel | mmHg |
| systolic | 8480-6 | Systolic blood pressure | mmHg |
| diastolic | 8462-4 | Diastolic blood pressure | mmHg |
| heart_rate | 8867-4 | Heart rate | /min |
| respiratory_rate | 9279-1 | Respiratory rate | /min |
| temperature | 8310-5 | Body temperature | Cel |
| oxygen_saturation | 2708-6 | Oxygen saturation | % |
| height | 8302-2 | Body height | cm |
| weight | 29463-7 | Body weight | kg |
| bmi | 39156-5 | Body mass index | kg/m2 |

---

## Insurance Entities

### Member

An insured individual (subscriber or dependent).

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "allOf": [{ "$ref": "#/definitions/Person" }],
  "required": ["member_id", "plan_id", "relationship", "coverage_start"],
  "properties": {
    "member_id": {
      "type": "string",
      "pattern": "^[A-Z0-9]{9,12}$",
      "description": "Unique member identifier"
    },
    "subscriber_id": {
      "type": "string",
      "description": "Subscriber's member_id (same as member_id for subscriber)"
    },
    "plan_id": {
      "type": "string",
      "description": "Reference to Plan.id"
    },
    "group_number": {
      "type": "string",
      "description": "Employer group number"
    },
    "relationship": {
      "type": "string",
      "enum": ["self", "spouse", "child", "other"],
      "description": "Relationship to subscriber"
    },
    "coverage_start": {
      "type": "string",
      "format": "date"
    },
    "coverage_end": {
      "type": "string",
      "format": "date"
    },
    "status": {
      "type": "string",
      "enum": ["active", "terminated", "pending"]
    },
    "pcp": {
      "type": "object",
      "description": "Primary Care Physician (for HMO)",
      "properties": {
        "npi": { "type": "string" },
        "name": { "type": "string" }
      }
    },
    "cobra": {
      "type": "boolean",
      "default": false,
      "description": "COBRA continuation coverage"
    },
    "medicare": {
      "type": "object",
      "description": "Medicare coordination info",
      "properties": {
        "hic_number": { "type": "string" },
        "part_a_date": { "type": "string", "format": "date" },
        "part_b_date": { "type": "string", "format": "date" },
        "msp_type": { "type": "string" }
      }
    }
  }
}
```

### Plan

An insurance benefit plan.

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["id", "name", "type", "effective_date"],
  "properties": {
    "id": {
      "type": "string",
      "pattern": "^PLN[0-9]{6}$"
    },
    "name": { "type": "string" },
    "type": {
      "type": "string",
      "enum": ["HMO", "PPO", "EPO", "POS", "HDHP", "Medicare", "Medicaid"]
    },
    "effective_date": {
      "type": "string",
      "format": "date"
    },
    "termination_date": {
      "type": "string",
      "format": "date"
    },
    "benefits": {
      "type": "object",
      "properties": {
        "individual_deductible": { "type": "number" },
        "family_deductible": { "type": "number" },
        "individual_oop_max": { "type": "number" },
        "family_oop_max": { "type": "number" },
        "coinsurance_in_network": { "type": "number" },
        "coinsurance_out_network": { "type": "number" }
      }
    },
    "copays": {
      "type": "object",
      "properties": {
        "pcp_visit": { "type": "number" },
        "specialist_visit": { "type": "number" },
        "urgent_care": { "type": "number" },
        "emergency_room": { "type": "number" },
        "generic_rx": { "type": "number" },
        "brand_rx": { "type": "number" },
        "specialty_rx": { "type": "number" }
      }
    },
    "pharmacy_benefit": {
      "type": "object",
      "properties": {
        "pbm_id": { "type": "string" },
        "formulary_id": { "type": "string" },
        "rx_bin": { "type": "string" },
        "rx_pcn": { "type": "string" },
        "rx_group": { "type": "string" }
      }
    },
    "network_id": { "type": "string" },
    "metal_level": {
      "type": "string",
      "enum": ["bronze", "silver", "gold", "platinum"]
    }
  }
}
```

### Claim

An insurance claim for healthcare services.

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["id", "member_id", "type", "status", "service_date", "lines"],
  "properties": {
    "id": {
      "type": "string",
      "pattern": "^CLM[0-9]{12}$"
    },
    "member_id": { "type": "string" },
    "patient_account_number": { "type": "string" },
    "type": {
      "type": "string",
      "enum": ["professional", "institutional", "dental", "pharmacy"]
    },
    "status": {
      "type": "string",
      "enum": ["submitted", "pending", "processing", "adjudicated", "paid", "denied", "appealed"]
    },
    "service_date": {
      "type": "string",
      "format": "date"
    },
    "service_end_date": {
      "type": "string",
      "format": "date"
    },
    "received_date": {
      "type": "string",
      "format": "date"
    },
    "billing_provider": {
      "type": "object",
      "properties": {
        "npi": { "type": "string", "pattern": "^[0-9]{10}$" },
        "name": { "type": "string" },
        "tax_id": { "type": "string" },
        "address": { "$ref": "#/definitions/Address" }
      }
    },
    "rendering_provider": {
      "type": "object",
      "properties": {
        "npi": { "type": "string" },
        "name": { "type": "string" },
        "specialty": { "type": "string" }
      }
    },
    "facility": {
      "type": "object",
      "properties": {
        "npi": { "type": "string" },
        "name": { "type": "string" },
        "type_code": { "type": "string" }
      }
    },
    "place_of_service": {
      "type": "string",
      "pattern": "^[0-9]{2}$"
    },
    "diagnoses": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "code": { "type": "string" },
          "type": { "type": "string", "enum": ["principal", "admitting", "secondary"] },
          "poa": { "type": "string" }
        }
      }
    },
    "drg": {
      "type": "object",
      "description": "For institutional claims",
      "properties": {
        "code": { "type": "string" },
        "description": { "type": "string" },
        "weight": { "type": "number" }
      }
    },
    "lines": {
      "type": "array",
      "items": { "$ref": "#/definitions/ClaimLine" },
      "minItems": 1
    },
    "totals": {
      "type": "object",
      "properties": {
        "billed": { "type": "number" },
        "allowed": { "type": "number" },
        "paid": { "type": "number" },
        "member_liability": { "type": "number" }
      }
    },
    "prior_auth_number": { "type": "string" },
    "referral_number": { "type": "string" },
    "original_claim_id": {
      "type": "string",
      "description": "For adjustments/voids"
    },
    "frequency_code": {
      "type": "string",
      "enum": ["1", "7", "8"],
      "description": "1=Original, 7=Replacement, 8=Void"
    }
  }
}
```

### ClaimLine

A single service line item on a claim.

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["line_number", "procedure_code", "service_date", "billed_amount"],
  "properties": {
    "line_number": {
      "type": "integer",
      "minimum": 1
    },
    "procedure_code": {
      "type": "string",
      "description": "CPT/HCPCS code"
    },
    "procedure_code_type": {
      "type": "string",
      "enum": ["CPT", "HCPCS", "ICD10PCS", "CDT", "NDC"]
    },
    "modifiers": {
      "type": "array",
      "items": { "type": "string" },
      "maxItems": 4
    },
    "revenue_code": {
      "type": "string",
      "pattern": "^[0-9]{4}$",
      "description": "For institutional claims"
    },
    "service_date": {
      "type": "string",
      "format": "date"
    },
    "service_end_date": {
      "type": "string",
      "format": "date"
    },
    "place_of_service": { "type": "string" },
    "units": {
      "type": "number",
      "minimum": 0.01
    },
    "diagnosis_pointers": {
      "type": "array",
      "items": { "type": "integer", "minimum": 1, "maximum": 12 }
    },
    "rendering_provider_npi": { "type": "string" },
    "billed_amount": { "type": "number" },
    "allowed_amount": { "type": "number" },
    "paid_amount": { "type": "number" },
    "deductible": { "type": "number" },
    "coinsurance": { "type": "number" },
    "copay": { "type": "number" },
    "cob_amount": { "type": "number" },
    "adjustment_reason_codes": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "group": { "type": "string", "enum": ["CO", "PR", "OA", "PI", "CR"] },
          "code": { "type": "string" },
          "amount": { "type": "number" }
        }
      }
    },
    "remark_codes": {
      "type": "array",
      "items": { "type": "string" }
    },
    "status": {
      "type": "string",
      "enum": ["paid", "denied", "adjusted", "pending"]
    },
    "denial_reason": { "type": "string" },
    "ndc": {
      "type": "string",
      "description": "NDC for drug claims"
    },
    "drug_quantity": { "type": "number" },
    "drug_unit": { "type": "string" }
  }
}
```

### Payment

A payment record for a processed claim.

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["id", "claim_id", "payment_date", "amount"],
  "properties": {
    "id": {
      "type": "string",
      "pattern": "^PMT[0-9]{12}$"
    },
    "claim_id": { "type": "string" },
    "check_number": { "type": "string" },
    "payment_date": {
      "type": "string",
      "format": "date"
    },
    "payment_method": {
      "type": "string",
      "enum": ["check", "eft", "virtual_card"]
    },
    "amount": { "type": "number" },
    "payee": {
      "type": "object",
      "properties": {
        "npi": { "type": "string" },
        "name": { "type": "string" },
        "tax_id": { "type": "string" }
      }
    },
    "remittance_id": {
      "type": "string",
      "description": "835 transaction ID"
    },
    "trace_number": { "type": "string" }
  }
}
```

### Accumulator

Member cost-sharing accumulator tracking.

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["member_id", "plan_year", "type", "amount"],
  "properties": {
    "id": { "type": "string" },
    "member_id": { "type": "string" },
    "plan_year": {
      "type": "integer",
      "description": "Benefit year"
    },
    "type": {
      "type": "string",
      "enum": ["individual_deductible", "family_deductible", "individual_oop", "family_oop"]
    },
    "network": {
      "type": "string",
      "enum": ["in_network", "out_of_network", "combined"]
    },
    "limit": {
      "type": "number",
      "description": "Annual maximum"
    },
    "amount": {
      "type": "number",
      "description": "Current accumulated amount"
    },
    "remaining": {
      "type": "number",
      "description": "Remaining until limit met"
    },
    "met_date": {
      "type": "string",
      "format": "date",
      "description": "Date limit was met"
    },
    "last_updated": {
      "type": "string",
      "format": "date-time"
    }
  }
}
```

---

## Pharmacy Entities

### Prescription

A medication prescription order.

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["id", "patient_id", "prescriber", "medication", "written_date"],
  "properties": {
    "id": {
      "type": "string",
      "pattern": "^RX[0-9]{10}$"
    },
    "patient_id": { "type": "string" },
    "prescriber": {
      "type": "object",
      "required": ["npi"],
      "properties": {
        "npi": { "type": "string", "pattern": "^[0-9]{10}$" },
        "name": { "type": "string" },
        "dea": { "type": "string", "pattern": "^[A-Z]{2}[0-9]{7}$" }
      }
    },
    "medication": {
      "type": "object",
      "required": ["name", "ndc"],
      "properties": {
        "name": { "type": "string" },
        "ndc": { "type": "string", "pattern": "^[0-9]{11}$" },
        "rxnorm": { "type": "string" },
        "gpi": { "type": "string" },
        "strength": { "type": "string" },
        "form": { "type": "string" },
        "brand_generic": { "type": "string", "enum": ["brand", "generic"] }
      }
    },
    "written_date": {
      "type": "string",
      "format": "date"
    },
    "directions": {
      "type": "string",
      "description": "SIG - dosing instructions"
    },
    "quantity": { "type": "number" },
    "days_supply": { "type": "integer" },
    "refills_authorized": { "type": "integer" },
    "refills_remaining": { "type": "integer" },
    "daw_code": {
      "type": "string",
      "enum": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
      "description": "Dispense As Written code"
    },
    "diagnosis": {
      "type": "object",
      "properties": {
        "code": { "type": "string" },
        "display": { "type": "string" }
      }
    },
    "prior_auth": {
      "type": "object",
      "properties": {
        "required": { "type": "boolean" },
        "number": { "type": "string" },
        "status": { "type": "string", "enum": ["approved", "denied", "pending"] },
        "expires": { "type": "string", "format": "date" }
      }
    },
    "status": {
      "type": "string",
      "enum": ["active", "completed", "cancelled", "expired"]
    },
    "controlled_substance_schedule": {
      "type": "string",
      "enum": ["II", "III", "IV", "V"]
    }
  }
}
```

### PharmacyClaim

A pharmacy claim submitted for adjudication.

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["id", "prescription_id", "member_id", "pharmacy", "fill_date"],
  "properties": {
    "id": {
      "type": "string",
      "pattern": "^RXCLM[0-9]{12}$"
    },
    "prescription_id": { "type": "string" },
    "member_id": { "type": "string" },
    "cardholder_id": { "type": "string" },
    "pharmacy": {
      "type": "object",
      "required": ["ncpdp_id", "npi"],
      "properties": {
        "ncpdp_id": { "type": "string", "pattern": "^[0-9]{7}$" },
        "npi": { "type": "string", "pattern": "^[0-9]{10}$" },
        "name": { "type": "string" },
        "chain_code": { "type": "string" },
        "pharmacy_type": { "type": "string", "enum": ["retail", "mail", "specialty", "ltc"] }
      }
    },
    "fill_date": {
      "type": "string",
      "format": "date"
    },
    "fill_number": {
      "type": "integer",
      "description": "0=new, 1+=refill"
    },
    "ndc": { "type": "string", "pattern": "^[0-9]{11}$" },
    "quantity_dispensed": { "type": "number" },
    "days_supply": { "type": "integer" },
    "compound_code": {
      "type": "string",
      "enum": ["0", "1", "2"],
      "description": "0=not compound, 1=compound, 2=not specified"
    },
    "daw_code": { "type": "string" },
    "pricing": {
      "type": "object",
      "properties": {
        "ingredient_cost": { "type": "number" },
        "dispensing_fee": { "type": "number" },
        "sales_tax": { "type": "number" },
        "usual_customary": { "type": "number" },
        "gross_amount_due": { "type": "number" },
        "patient_pay": { "type": "number" },
        "plan_pay": { "type": "number" },
        "copay": { "type": "number" },
        "coinsurance": { "type": "number" },
        "deductible": { "type": "number" }
      }
    },
    "prescriber_npi": { "type": "string" },
    "diagnosis_code": { "type": "string" },
    "prior_auth_number": { "type": "string" },
    "submission_clarification_code": { "type": "string" },
    "other_coverage_code": {
      "type": "string",
      "enum": ["0", "1", "2", "3", "4", "8"]
    },
    "dur": {
      "type": "array",
      "description": "Drug Utilization Review results",
      "items": {
        "type": "object",
        "properties": {
          "reason_code": { "type": "string" },
          "response_code": { "type": "string" },
          "clinical_significance": { "type": "string" },
          "other_prescriber_npi": { "type": "string" },
          "other_pharmacy_ncpdp": { "type": "string" },
          "previous_fill_date": { "type": "string", "format": "date" }
        }
      }
    },
    "bin": { "type": "string", "pattern": "^[0-9]{6}$" },
    "pcn": { "type": "string" },
    "group_id": { "type": "string" }
  }
}
```

### ClaimResponse

Response from pharmacy benefit adjudication.

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["claim_id", "response_status", "transaction_date"],
  "properties": {
    "claim_id": { "type": "string" },
    "transaction_code": {
      "type": "string",
      "enum": ["B1", "B2", "B3"],
      "description": "B1=billing, B2=reversal, B3=rebill"
    },
    "response_status": {
      "type": "string",
      "enum": ["paid", "rejected", "duplicate", "captured"]
    },
    "transaction_date": {
      "type": "string",
      "format": "date-time"
    },
    "authorization_number": { "type": "string" },
    "reject_codes": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "code": { "type": "string" },
          "field": { "type": "string" },
          "description": { "type": "string" }
        }
      }
    },
    "approved_message_code": { "type": "string" },
    "additional_messages": {
      "type": "array",
      "items": { "type": "string" }
    },
    "pricing": {
      "type": "object",
      "properties": {
        "ingredient_cost_paid": { "type": "number" },
        "dispensing_fee_paid": { "type": "number" },
        "total_amount_paid": { "type": "number" },
        "patient_pay_amount": { "type": "number" },
        "amount_of_copay": { "type": "number" },
        "amount_of_coinsurance": { "type": "number" },
        "amount_applied_to_deductible": { "type": "number" },
        "basis_of_cost": { "type": "string" },
        "accumulated_deductible": { "type": "number" },
        "remaining_deductible": { "type": "number" },
        "remaining_benefit": { "type": "number" }
      }
    },
    "dur_response": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "reason_for_service_code": { "type": "string" },
          "clinical_significance_code": { "type": "string" },
          "other_pharmacy_indicator": { "type": "string" },
          "previous_fill_date": { "type": "string", "format": "date" },
          "quantity_of_previous_fill": { "type": "number" },
          "database_indicator": { "type": "string" },
          "free_text_message": { "type": "string" }
        }
      }
    },
    "preferred_product": {
      "type": "object",
      "description": "Suggested alternative if applicable",
      "properties": {
        "ndc": { "type": "string" },
        "name": { "type": "string" },
        "price": { "type": "number" }
      }
    }
  }
}
```

### FormularyDrug

A drug in the plan formulary.

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["ndc", "formulary_id", "tier", "status"],
  "properties": {
    "ndc": {
      "type": "string",
      "pattern": "^[0-9]{11}$"
    },
    "formulary_id": { "type": "string" },
    "gpi": {
      "type": "string",
      "description": "Generic Product Identifier"
    },
    "rxnorm": { "type": "string" },
    "drug_name": { "type": "string" },
    "generic_name": { "type": "string" },
    "brand_generic": {
      "type": "string",
      "enum": ["brand", "generic"]
    },
    "tier": {
      "type": "integer",
      "minimum": 1,
      "maximum": 6,
      "description": "Formulary tier (1=generic, 2=preferred brand, etc.)"
    },
    "status": {
      "type": "string",
      "enum": ["formulary", "non_formulary", "excluded"]
    },
    "quantity_limit": {
      "type": "object",
      "properties": {
        "applies": { "type": "boolean" },
        "amount": { "type": "number" },
        "days": { "type": "integer" }
      }
    },
    "step_therapy": {
      "type": "object",
      "properties": {
        "required": { "type": "boolean" },
        "step_drugs": {
          "type": "array",
          "items": { "type": "string" }
        }
      }
    },
    "prior_auth": {
      "type": "object",
      "properties": {
        "required": { "type": "boolean" },
        "criteria": { "type": "string" }
      }
    },
    "specialty": {
      "type": "boolean",
      "description": "Specialty pharmacy required"
    },
    "maintenance": {
      "type": "boolean",
      "description": "Maintenance medication"
    },
    "dea_schedule": {
      "type": "string",
      "enum": ["II", "III", "IV", "V"]
    },
    "effective_date": {
      "type": "string",
      "format": "date"
    },
    "termination_date": {
      "type": "string",
      "format": "date"
    }
  }
}
```

---

## Field Naming Conventions

| Convention | Example | Usage |
|------------|---------|-------|
| snake_case | `member_id` | All field names |
| Singular | `diagnosis` | Single value fields |
| Plural | `diagnoses` | Array fields |
| _id suffix | `patient_id` | Foreign key references |
| _date suffix | `service_date` | Date fields |
| _code suffix | `procedure_code` | Code values |

## Common Field Patterns

### Identifiers
- Internal IDs: `{PREFIX}{DIGITS}` (e.g., `MRN00001234`, `CLM000000001234`)
- External IDs: Standard formats (NPI: 10 digits, NDC: 11 digits)

### Dates
- Date only: `YYYY-MM-DD` (ISO 8601)
- DateTime: `YYYY-MM-DDTHH:MM:SSZ` (ISO 8601 with timezone)

### Money
- All monetary values are `number` type
- Always in USD
- Two decimal precision (stored as float)

### Codes
- Always paired with `system` URI when standard terminology
- Include `display` for human readability
