# State Management Technical Specification

This document defines the MCP tool interfaces and data formats for the State Management capability.

## Overview

State Management enables users to save and load workspace scenarios - complete snapshots of all patients and clinical data with full provenance tracking.

**Storage Location**: `~/.healthsim/scenarios/`
**File Format**: JSON
**File Naming**: `{scenario_id}.json` where scenario_id is a UUID

## MCP Tool Specifications

### healthsim.save_scenario

Saves the current workspace as a named scenario.

#### Input Schema

```json
{
  "type": "object",
  "properties": {
    "name": {
      "type": "string",
      "description": "Human-readable name for the scenario (kebab-case recommended)",
      "minLength": 1,
      "maxLength": 100,
      "pattern": "^[a-zA-Z0-9][a-zA-Z0-9-_]*$"
    },
    "description": {
      "type": "string",
      "description": "Optional description of the scenario contents and purpose",
      "maxLength": 500
    },
    "tags": {
      "type": "array",
      "description": "Optional tags for filtering and organization",
      "items": {
        "type": "string",
        "minLength": 1,
        "maxLength": 50
      },
      "maxItems": 20
    },
    "scope": {
      "type": "string",
      "description": "What to save: 'all' for entire workspace, 'patients' for selected patients",
      "enum": ["all", "patients"],
      "default": "all"
    },
    "patient_ids": {
      "type": "array",
      "description": "Patient IDs to save (required when scope='patients')",
      "items": {
        "type": "string"
      }
    }
  },
  "required": ["name"]
}
```

#### Output Schema

```json
{
  "type": "object",
  "properties": {
    "success": {
      "type": "boolean",
      "description": "Whether the save operation succeeded"
    },
    "scenario_id": {
      "type": "string",
      "description": "UUID of the saved scenario"
    },
    "saved_at": {
      "type": "string",
      "format": "date-time",
      "description": "ISO 8601 timestamp of when scenario was saved"
    },
    "file_path": {
      "type": "string",
      "description": "Path to the saved scenario file"
    },
    "summary": {
      "type": "object",
      "description": "Summary of what was saved",
      "properties": {
        "patient_count": { "type": "integer" },
        "encounter_count": { "type": "integer" },
        "diagnosis_count": { "type": "integer" },
        "lab_count": { "type": "integer" },
        "medication_count": { "type": "integer" },
        "vital_count": { "type": "integer" },
        "procedure_count": { "type": "integer" },
        "note_count": { "type": "integer" },
        "provenance_summary": {
          "type": "object",
          "properties": {
            "generated": { "type": "integer" },
            "loaded": { "type": "integer" },
            "derived": { "type": "integer" }
          }
        }
      }
    },
    "error": {
      "type": "string",
      "description": "Error message if success is false"
    }
  },
  "required": ["success"]
}
```

#### Behavior

1. Generate a UUID for the scenario
2. Collect all entities from the workspace (or filtered by patient_ids)
3. Serialize to JSON preserving all provenance
4. Create `~/.healthsim/scenarios/` directory if needed
5. Write to `{scenario_id}.json`
6. Return summary of saved contents

#### Error Conditions

- Empty workspace (nothing to save)
- Invalid patient_ids (patients not found)
- File system errors (permissions, disk full)
- Invalid name (empty or bad characters)

---

### healthsim.load_scenario

Loads a previously saved scenario into the workspace.

#### Input Schema

```json
{
  "type": "object",
  "properties": {
    "scenario_id": {
      "type": "string",
      "description": "UUID of the scenario to load"
    },
    "name": {
      "type": "string",
      "description": "Name to search for (fuzzy matching supported)"
    },
    "scope": {
      "type": "string",
      "description": "What to load: 'all' for entire scenario, 'patients' for selected patients",
      "enum": ["all", "patients"],
      "default": "all"
    },
    "patient_ids": {
      "type": "array",
      "description": "Patient IDs to load from scenario (when scope='patients')",
      "items": {
        "type": "string"
      }
    },
    "mode": {
      "type": "string",
      "description": "How to handle existing workspace: 'replace' clears first, 'merge' adds to existing",
      "enum": ["replace", "merge"],
      "default": "replace"
    },
    "conflict_resolution": {
      "type": "string",
      "description": "How to handle MRN conflicts during merge",
      "enum": ["skip", "overwrite", "duplicate"],
      "default": "skip"
    }
  },
  "oneOf": [
    { "required": ["scenario_id"] },
    { "required": ["name"] }
  ]
}
```

#### Output Schema

```json
{
  "type": "object",
  "properties": {
    "success": {
      "type": "boolean",
      "description": "Whether the load operation succeeded"
    },
    "scenario_id": {
      "type": "string",
      "description": "UUID of the loaded scenario"
    },
    "scenario_name": {
      "type": "string",
      "description": "Name of the loaded scenario"
    },
    "loaded_at": {
      "type": "string",
      "format": "date-time",
      "description": "ISO 8601 timestamp of load operation"
    },
    "summary": {
      "type": "object",
      "description": "Summary of what was loaded",
      "properties": {
        "patients_loaded": { "type": "integer" },
        "patients_skipped": { "type": "integer" },
        "patients_overwritten": { "type": "integer" },
        "total_entities": { "type": "integer" }
      }
    },
    "workspace_state": {
      "type": "object",
      "description": "Current workspace state after load",
      "properties": {
        "total_patients": { "type": "integer" },
        "total_encounters": { "type": "integer" }
      }
    },
    "conflicts": {
      "type": "array",
      "description": "MRN conflicts encountered during merge",
      "items": {
        "type": "object",
        "properties": {
          "mrn": { "type": "string" },
          "workspace_patient": { "type": "string" },
          "scenario_patient": { "type": "string" },
          "resolution": { "type": "string" }
        }
      }
    },
    "error": {
      "type": "string",
      "description": "Error message if success is false"
    }
  },
  "required": ["success"]
}
```

#### Behavior

1. Find scenario by ID or fuzzy match on name
2. If mode='replace', clear current workspace
3. Read and parse scenario JSON
4. For each patient:
   - If mode='merge', check for MRN conflicts
   - Apply conflict_resolution strategy
   - Add patient and associated clinical data to workspace
5. Restore all provenance exactly as saved
6. Return summary of load operation

#### Error Conditions

- Scenario not found (ID or name)
- Multiple matches for name (ambiguous)
- Corrupted scenario file (invalid JSON)
- Incompatible version (future consideration)

---

### healthsim.list_scenarios

Lists saved scenarios with optional filtering.

#### Input Schema

```json
{
  "type": "object",
  "properties": {
    "search": {
      "type": "string",
      "description": "Search string to filter by name or description"
    },
    "tags": {
      "type": "array",
      "description": "Filter to scenarios with ALL specified tags",
      "items": {
        "type": "string"
      }
    },
    "limit": {
      "type": "integer",
      "description": "Maximum number of scenarios to return",
      "default": 20,
      "minimum": 1,
      "maximum": 100
    },
    "sort_by": {
      "type": "string",
      "description": "Sort order for results",
      "enum": ["saved_at", "name", "patient_count"],
      "default": "saved_at"
    },
    "sort_order": {
      "type": "string",
      "enum": ["asc", "desc"],
      "default": "desc"
    }
  }
}
```

#### Output Schema

```json
{
  "type": "object",
  "properties": {
    "success": {
      "type": "boolean"
    },
    "scenarios": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "scenario_id": { "type": "string" },
          "name": { "type": "string" },
          "description": { "type": "string" },
          "tags": {
            "type": "array",
            "items": { "type": "string" }
          },
          "saved_at": {
            "type": "string",
            "format": "date-time"
          },
          "patient_count": { "type": "integer" },
          "entity_count": { "type": "integer" },
          "file_size_bytes": { "type": "integer" }
        }
      }
    },
    "total_count": {
      "type": "integer",
      "description": "Total matching scenarios (may be more than returned due to limit)"
    },
    "error": {
      "type": "string"
    }
  },
  "required": ["success"]
}
```

#### Behavior

1. Scan `~/.healthsim/scenarios/` directory
2. Read metadata from each scenario file (not full content)
3. Apply search filter (case-insensitive substring match on name/description)
4. Apply tag filter (AND logic - must have all specified tags)
5. Sort by specified field
6. Return limited results with total count

#### Error Conditions

- Scenarios directory doesn't exist (return empty list, not error)
- Corrupted scenario files (skip with warning)

---

### healthsim.delete_scenario

Deletes a saved scenario.

#### Input Schema

```json
{
  "type": "object",
  "properties": {
    "scenario_id": {
      "type": "string",
      "description": "UUID of the scenario to delete"
    },
    "confirm": {
      "type": "boolean",
      "description": "Must be true to actually delete (safety check)",
      "const": true
    }
  },
  "required": ["scenario_id", "confirm"]
}
```

#### Output Schema

```json
{
  "type": "object",
  "properties": {
    "success": {
      "type": "boolean"
    },
    "deleted_scenario": {
      "type": "object",
      "properties": {
        "scenario_id": { "type": "string" },
        "name": { "type": "string" },
        "patient_count": { "type": "integer" }
      }
    },
    "error": {
      "type": "string"
    }
  },
  "required": ["success"]
}
```

#### Behavior

1. Verify confirm=true (reject if false or missing)
2. Find scenario by ID
3. Read scenario metadata for response
4. Delete the scenario file
5. Return deleted scenario info

#### Error Conditions

- confirm is not true
- Scenario not found
- File system errors (permissions)

---

## Scenario JSON Schema

The complete schema for a saved scenario file.

### Schema Definition

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://healthsim.io/schemas/scenario/v1",
  "title": "HealthSim Scenario",
  "description": "A saved workspace scenario containing patients and clinical data",
  "type": "object",
  "properties": {
    "schema_version": {
      "type": "string",
      "const": "1.0",
      "description": "Schema version for forward compatibility"
    },
    "scenario_id": {
      "type": "string",
      "format": "uuid",
      "description": "Unique identifier for this scenario"
    },
    "name": {
      "type": "string",
      "description": "Human-readable scenario name"
    },
    "description": {
      "type": "string",
      "description": "Optional description"
    },
    "tags": {
      "type": "array",
      "items": { "type": "string" },
      "description": "Organization tags"
    },
    "created_at": {
      "type": "string",
      "format": "date-time",
      "description": "When scenario was saved"
    },
    "created_by": {
      "type": "string",
      "description": "User or system that created the scenario"
    },
    "healthsim_version": {
      "type": "string",
      "description": "Version of HealthSim that created this scenario"
    },
    "provenance_summary": {
      "$ref": "#/$defs/ProvenanceSummary"
    },
    "entities": {
      "$ref": "#/$defs/Entities"
    }
  },
  "required": ["schema_version", "scenario_id", "name", "created_at", "entities"]
}
```

For the complete schema definition including all entity types (Patient, Encounter, Diagnosis, Medication, LabResult, VitalSign, Procedure, ClinicalNote), see the full specification.

---

## Implementation Notes

### File System Operations

- Use atomic writes (write to temp file, then rename)
- Create directories with appropriate permissions (0700 for ~/.healthsim)
- Handle concurrent access gracefully (file locking if needed)

### Performance Considerations

- For list_scenarios, read only metadata section (first ~1KB)
- Consider indexing if scenario count exceeds 100
- Large scenarios (1000+ patients) may need streaming JSON

### Versioning Strategy

- `schema_version` enables forward compatibility
- Older versions should be loadable by newer HealthSim
- Include `healthsim_version` for debugging

### Security

- Validate scenario files on load (don't trust arbitrary JSON)
- Sanitize file names to prevent path traversal
- No execution of arbitrary code from scenarios

## See Also

- [State Management User Guide](user-guide.md)
- [MCP Configuration](../mcp/configuration.md)
