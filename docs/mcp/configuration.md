# MCP Server Configuration

This guide explains how to set up HealthSim MCP servers for use with Claude Desktop, Claude Code, and other MCP-compatible clients.

## Overview

HealthSim products provide MCP servers that expose capabilities as tools for Claude:

1. **Generation Server** - Create synthetic patients, members, or prescriptions
2. **Export Server** - Transform data to healthcare formats (FHIR, HL7v2, X12, NCPDP, MIMIC)
3. **Validation Server** - Validate clinical plausibility and data integrity

## Quick Start

### Prerequisites

- Python 3.10 or higher
- Product installed: `pip install -e .`
- Virtual environment activated (recommended)

### Configuration File

Each product includes a pre-configured MCP configuration file at `.claude/mcp-config.json`:

```json
{
  "mcpServers": {
    "patientsim-generation": {
      "command": "python",
      "args": ["-m", "patientsim.mcp.generation_server"],
      "description": "Generate synthetic patients and cohorts",
      "cwd": "${workspaceFolder}"
    },
    "patientsim-export": {
      "command": "python",
      "args": ["-m", "patientsim.mcp.export_server"],
      "description": "Export patients to healthcare data formats",
      "cwd": "${workspaceFolder}"
    },
    "patientsim-validation": {
      "command": "python",
      "args": ["-m", "patientsim.mcp.validation_server"],
      "description": "Validate patient data for clinical plausibility",
      "cwd": "${workspaceFolder}"
    }
  }
}
```

## Setup for Claude Desktop

### macOS/Linux

1. **Locate Claude Desktop Config**:
   ```bash
   # macOS
   ~/Library/Application Support/Claude/claude_desktop_config.json

   # Linux
   ~/.config/Claude/claude_desktop_config.json
   ```

2. **Add Server Configurations**:
   ```bash
   # Copy the server configurations
   cat .claude/mcp-config.json
   ```

3. **Edit claude_desktop_config.json**:
   ```json
   {
     "mcpServers": {
       "patientsim-generation": {
         "command": "/path/to/your/venv/bin/python",
         "args": ["-m", "patientsim.mcp.generation_server"],
         "cwd": "/path/to/patientsim"
       },
       "patientsim-export": {
         "command": "/path/to/your/venv/bin/python",
         "args": ["-m", "patientsim.mcp.export_server"],
         "cwd": "/path/to/patientsim"
       },
       "patientsim-validation": {
         "command": "/path/to/your/venv/bin/python",
         "args": ["-m", "patientsim.mcp.validation_server"],
         "cwd": "/path/to/patientsim"
       }
     }
   }
   ```

4. **Replace Paths**:
   - Replace `/path/to/your/venv/bin/python` with your virtual environment's Python path
   - Replace `/path/to/patientsim` with your product directory path

5. **Restart Claude Desktop**:
   - Quit Claude Desktop completely
   - Relaunch Claude Desktop
   - MCP servers will start automatically

### Windows

1. **Locate Claude Desktop Config**:
   ```powershell
   %APPDATA%\Claude\claude_desktop_config.json
   ```

2. **Edit Configuration**:
   ```json
   {
     "mcpServers": {
       "patientsim-generation": {
         "command": "C:\\path\\to\\venv\\Scripts\\python.exe",
         "args": ["-m", "patientsim.mcp.generation_server"],
         "cwd": "C:\\path\\to\\patientsim"
       }
     }
   }
   ```

3. **Restart Claude Desktop**

## Setup for Claude Code

Claude Code automatically discovers MCP configuration in `.claude/mcp-config.json` within your workspace.

### Automatic Setup

1. **Open Project in Claude Code**:
   ```bash
   code /path/to/patientsim
   ```

2. **Verify Configuration**:
   - Claude Code reads `.claude/mcp-config.json`
   - Servers start automatically when needed

### Manual Path Configuration

If using a specific Python interpreter:

1. **Edit `.claude/mcp-config.json`**:
   ```json
   {
     "mcpServers": {
       "patientsim-generation": {
         "command": "/absolute/path/to/venv/bin/python",
         "args": ["-m", "patientsim.mcp.generation_server"],
         "cwd": "${workspaceFolder}"
       }
     }
   }
   ```

2. **Use `${workspaceFolder}` variable** - Claude Code expands this automatically

## Available Tools

### Generation Server Tools

**Patient/Member Generation:**
- **`generate_patient`** / **`generate_member`** - Generate a single entity
- **`generate_cohort`** - Generate multiple entities
- **`list_scenarios`** - Show available clinical scenarios
- **`describe_scenario`** - Get scenario details
- **`modify_patient`** - Modify existing entity
- **`get_patient_details`** - View entity information

**State Management (Save/Load Scenarios):**
- **`save_scenario`** - Save current workspace to a named scenario
- **`load_scenario`** - Load a saved scenario
- **`list_saved_scenarios`** - List all saved scenarios
- **`delete_scenario`** - Delete a saved scenario
- **`workspace_summary`** - View current workspace state

### Export Server Tools

- **`export_fhir`** - Export to FHIR R4 Bundle
- **`export_hl7v2`** - Export to HL7v2 messages (ADT^A01, ORU^R01)
- **`export_x12`** - Export to X12 837/835 format (claims)
- **`export_ncpdp`** - Export to NCPDP D.0 format (pharmacy)
- **`export_mimic`** - Export to MIMIC-III CSV/Parquet format
- **`export_json`** - Export to native JSON format
- **`list_export_formats`** - Show available export formats

### Validation Server Tools

- **`validate_patients`** - Validate clinical plausibility
- **`validate_for_export`** - Validate for specific export format
- **`fix_validation_issues`** - Auto-fix common validation issues
- **`explain_validation_rule`** - Get explanation for validation rules

## Testing MCP Servers

### Manual Testing

Test each server independently before configuring Claude:

```bash
# Activate virtual environment
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate     # Windows

# Test generation server
python -m patientsim.mcp.generation_server
# Should output: "INFO:patientsim.mcp:Starting PatientSim MCP Generation Server"
# Press Ctrl+C to stop

# Test export server
python -m patientsim.mcp.export_server
# Should output: "INFO:patientsim.mcp.export:Starting PatientSim MCP Export Server"

# Test validation server
python -m patientsim.mcp.validation_server
# Should output: "INFO:patientsim.mcp.validation:Starting PatientSim MCP Validation Server"
```

### Testing with MCP Inspector

The [MCP Inspector](https://github.com/modelcontextprotocol/inspector) is a debugging tool for MCP servers:

```bash
# Install MCP Inspector
npm install -g @modelcontextprotocol/inspector

# Test a server
mcp-inspector python -m patientsim.mcp.generation_server
```

This opens a web UI showing:
- Available tools
- Tool schemas
- Request/response inspection
- Error debugging

## Troubleshooting

### Servers Not Appearing in Claude

**Symptom**: MCP tools don't appear in Claude's tool list

**Solutions**:
1. **Verify Python path** - Use absolute path to Python interpreter:
   ```bash
   which python  # macOS/Linux
   where python  # Windows
   ```

2. **Check working directory** - Ensure `cwd` points to product root:
   ```json
   {
     "cwd": "/absolute/path/to/patientsim"
   }
   ```

3. **Restart Claude Desktop** - Completely quit and relaunch

4. **Check Claude logs**:
   ```bash
   # macOS
   ~/Library/Logs/Claude/

   # Linux
   ~/.config/Claude/logs/

   # Windows
   %APPDATA%\Claude\logs\
   ```

### Import Errors

**Symptom**: Server starts but shows `ModuleNotFoundError`

**Solutions**:
1. **Install product**:
   ```bash
   pip install -e .
   ```

2. **Verify installation**:
   ```bash
   python -c "import patientsim; print(patientsim.__file__)"
   ```

3. **Use correct Python interpreter** - Ensure MCP config uses the same Python where product is installed

### Server Crashes

**Symptom**: MCP server starts but crashes immediately

**Solutions**:
1. **Check dependencies**:
   ```bash
   pip install -e ".[dev]"
   ```

2. **View server logs** - Run server manually to see error messages

3. **Check Python version**:
   ```bash
   python --version  # Should be 3.10+
   ```

## Advanced Configuration

### Environment Variables

Pass environment variables to MCP servers:

```json
{
  "mcpServers": {
    "patientsim-generation": {
      "command": "python",
      "args": ["-m", "patientsim.mcp.generation_server"],
      "env": {
        "PATIENTSIM_LOG_LEVEL": "DEBUG",
        "PATIENTSIM_OUTPUT_DIR": "/custom/export/path"
      }
    }
  }
}
```

### Multiple Instances

Run separate instances for different projects:

```json
{
  "mcpServers": {
    "patientsim-dev": {
      "command": "python",
      "args": ["-m", "patientsim.mcp.generation_server"],
      "cwd": "/path/to/dev/patientsim"
    },
    "patientsim-prod": {
      "command": "python",
      "args": ["-m", "patientsim.mcp.generation_server"],
      "cwd": "/path/to/prod/patientsim"
    }
  }
}
```

## Session Management

MCP servers share session state:
- **Generation server** creates entities and stores them in session
- **Export server** exports entities from the same session
- **Validation server** validates entities in the session

**Example workflow**:
```text
1. User: "Generate 5 diabetic patients"
   → generation_server creates patients, stores in session

2. User: "Validate them"
   → validation_server reads patients from session, validates

3. User: "Export to FHIR"
   → export_server reads patients from session, exports to FHIR

4. User: "Clear the session"
   → Session cleared, start fresh
```

## Security Considerations

### Data Privacy

- **All data is synthetic** - MCP servers generate fictional data only
- **No PHI** - Servers refuse requests that could create PHI lookalikes
- **Local execution** - Servers run locally, no cloud uploads

### File System Access

MCP servers can:
- ✅ Write exports to designated output directory
- ✅ Read scenario skills from `skills/` directory
- ❌ **Cannot** read arbitrary files outside product directory
- ❌ **Cannot** modify source code

### Network Access

- ❌ MCP servers do **not** make network requests
- ❌ MCP servers do **not** upload data
- ✅ All processing is local-only

## See Also

- [MCP Integration Guide](integration-guide.md)
- [State Management](../state-management/user-guide.md)
- [MCP Protocol Specification](https://spec.modelcontextprotocol.io/)
