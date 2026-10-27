---
description: Install HealthSim reference data (NPPES providers, CDC PLACES, SVI, ADI) into ~/.healthsim
argument-hint: "[download | path/to/healthsim.duckdb | motherduck]"
---

# HealthSim setup

Set up HealthSim's data so it works from any project. Work through these steps in order, report each result briefly, and stop at the first failure with a clear fix.

The user's argument, if any: `$ARGUMENTS`

## 1. Check uv

Run `uv --version`. If uv is missing, stop and give the install command: `brew install uv` on macOS, or `curl -LsSf https://astral.sh/uv/install.sh | sh`. After installing uv the user must restart Claude Code so the HealthSim MCP server can start.

## 2. Prepare the Python environment

Run this once; it can take a minute the first time:

```bash
UV_PROJECT_ENVIRONMENT="${CLAUDE_PLUGIN_DATA}/venv" uv sync --frozen --quiet --package healthsim-mcp --directory "${CLAUDE_PLUGIN_ROOT}"
```

## 3. Show the current data location

```bash
UV_PROJECT_ENVIRONMENT="${CLAUDE_PLUGIN_DATA}/venv" uv run --frozen --quiet --directory "${CLAUDE_PLUGIN_ROOT}/packages/mcp-server" python -m healthsim.db.install status
```

If `has_reference` is already `true`, say where the data is and ask whether to replace it before going on.

## 4. Install reference data

Pick the source from the argument. With no argument, ask the user which one they want, recommending the download.

**download** (default): fetch the newest published release from GitHub (several hundred MB compressed). Confirm the download with the user first, then run:

```bash
UV_PROJECT_ENVIRONMENT="${CLAUDE_PLUGIN_DATA}/venv" uv run --frozen --quiet --directory "${CLAUDE_PLUGIN_ROOT}/packages/mcp-server" python -m healthsim.db.install download
```

**A path to a `healthsim.duckdb`** (for example a healthsim-workspace checkout after `git lfs pull`): copy its reference schemas into `~/.healthsim`. Ask whether to also import the cohorts saved in that file; if yes, add `--import-cohorts`.

```bash
UV_PROJECT_ENVIRONMENT="${CLAUDE_PLUGIN_DATA}/venv" uv run --frozen --quiet --directory "${CLAUDE_PLUGIN_ROOT}/packages/mcp-server" python -m healthsim.db.install from-file "<path>"
```

**motherduck**: no download. Explain that the user sets two environment variables in `~/.claude/settings.json` under `"env"`, then restarts Claude Code:

```json
{
  "env": {
    "HEALTHSIM_DB_PATH": "md:healthsim_ref",
    "MOTHERDUCK_TOKEN": "<their token>"
  }
}
```

Never ask the user to paste a token into the chat.

## 5. Confirm

Run the status command from step 3 again and call the `healthsim_data_status` tool. Tell the user where reference data and cohorts now live. The MCP server picks up newly installed reference data without a restart; for MotherDuck or after installing uv, they need to restart Claude Code.
