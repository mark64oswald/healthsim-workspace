---
description: Show where HealthSim keeps reference data and cohorts, and whether reference data is installed
---

# HealthSim status

Call the `healthsim_data_status` tool and summarize the result for the user in a few lines:

- Data layout (`split` means `~/.healthsim`, `single` means one database file, `motherduck` means the cloud)
- Where cohorts are saved and how many there are
- Whether reference data (NPPES, CDC PLACES, SVI, ADI) is installed, and which release

If the tool isn't available, the HealthSim MCP server didn't start. Check that `uv --version` works, then suggest `/healthsim:setup`. If reference data is missing, suggest `/healthsim:setup`.

For the installed release tag, also run:

```bash
UV_PROJECT_ENVIRONMENT="${CLAUDE_PLUGIN_DATA}/venv" uv run --frozen --quiet --directory "${CLAUDE_PLUGIN_ROOT}/packages/mcp-server" python -m healthsim.db.install status
```
