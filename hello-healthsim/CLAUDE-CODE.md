# Claude Code Setup

Use HealthSim from any project in Claude Code by installing it as a plugin. Install it once and it works in every folder you open.

---

## Prerequisites

| Requirement | Check | Install |
|-------------|-------|---------|
| Claude Code | `claude --version` | [Claude Code docs](https://code.claude.com/docs) |
| uv (runs the HealthSim MCP server) | `uv --version` | `brew install uv`, or `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| Git | `git --version` | Needed to add the plugin marketplace |

You don't need to clone the repository, install Git LFS, or set up a Python environment. uv downloads the right Python and packages the first time the plugin's MCP server starts.

---

## Step 1: Install the Plugin

In a Claude Code session:

```
/plugin marketplace add mark64oswald/healthsim-workspace
/plugin install healthsim@healthsim
```

Or from your shell:

```bash
claude plugin marketplace add mark64oswald/healthsim-workspace
claude plugin install healthsim@healthsim
```

The plugin adds:

| Component | Name | What it does |
|-----------|------|--------------|
| Router skill | `healthsim:healthsim` | Routes requests to the right product |
| Product skills | `healthsim:patientsim`, `healthsim:membersim`, `healthsim:rxmembersim`, `healthsim:trialsim`, `healthsim:populationsim`, `healthsim:networksim`, `healthsim:generation`, `healthsim:common` | Domain knowledge for each product |
| MCP server | `healthsim` | Cohort storage, reference data queries, NPPES provider search |
| Commands | `/healthsim:setup`, `/healthsim:status` | Install reference data; show where data lives |

---

## Step 2: Install Reference Data

Synthetic generation works right away. PopulationSim and NetworkSim also use real reference data (8.9M NPPES providers, CDC PLACES, SVI, ADI), which you install once per machine:

```
/healthsim:setup
```

The command offers three sources:

| Source | Command | When to use it |
|--------|---------|----------------|
| **Download** (recommended) | `/healthsim:setup download` | Fetches the latest published release into `~/.healthsim` |
| **Local file** | `/healthsim:setup ~/Developer/projects/healthsim-workspace/healthsim.duckdb` | You already have a checkout with `git lfs pull` done. It can also import the cohorts saved in that file |
| **MotherDuck** | `/healthsim:setup motherduck` | Cloud data with no download; needs a MotherDuck token |

---

## Step 3: Verify

From any folder:

```
/healthsim:status
```

Then try a few requests:

```
Generate a 65-year-old diabetic patient with hypertension in Houston, TX
```

```
Find 5 family medicine providers in San Diego County
```

```
What is the diabetes rate and SVI for Harris County, Texas?
```

---

## Where Your Data Lives

HealthSim keeps data outside your projects, in `~/.healthsim`:

| File | Contents | Written by |
|------|----------|------------|
| `~/.healthsim/reference.duckdb` | Reference data (read-only) | `/healthsim:setup` |
| `~/.healthsim/cohorts.duckdb` | Your saved cohorts | The MCP server, when you save a cohort |
| `~/.healthsim/reference-manifest.json` | Installed release and checksums | `/healthsim:setup download` |

Cohorts you save in one project are available in every other project. Reinstalling or updating the plugin doesn't touch this folder.

The location is resolved in this order:

1. `HEALTHSIM_DB_PATH`: one database at that path, or MotherDuck when it starts with `md:`
2. `~/.healthsim/reference.duckdb` exists: the plugin layout above (`HEALTHSIM_HOME` changes the folder)
3. The repo-root `healthsim.duckdb` is a real file: the developer layout in a checkout
4. Otherwise: the plugin layout, with no reference data yet

To set an environment variable for HealthSim, add it to `~/.claude/settings.json`:

```json
{
  "env": {
    "HEALTHSIM_HOME": "/Volumes/Data/healthsim"
  }
}
```

---

## Updating

```
/plugin marketplace update healthsim
```

The plugin tracks the repository's main branch, so an update picks up the latest skills and server code. Reference data updates separately: run `/healthsim:setup download` when a new data release is announced.

---

## Developing HealthSim

To work on HealthSim itself, use a checkout:

```bash
git lfs install
git clone https://github.com/mark64oswald/healthsim-workspace.git
cd healthsim-workspace
uv sync --all-packages
claude
```

In a checkout, the repo-root `healthsim.duckdb` is used, and `.claude/CLAUDE.md` routes requests to the skills, as before.

To try your changes as a plugin before pushing them, load the checkout directly:

```bash
claude --plugin-dir /path/to/healthsim-workspace
```

After editing the root `SKILL.md`, regenerate the plugin's router skill:

```bash
python scripts/build_plugin_router.py
```

To publish new reference data from a checkout with the real database:

```bash
uv run --package healthsim-core python scripts/publish_reference_data.py
```

---

## Automation

HealthSim works in non-interactive mode too:

```bash
claude -p "Generate 10 Medicare members with Type 2 diabetes as CSV" > members.csv
```

```bash
claude -p "Generate an X12 837P claim for a 99214 office visit" > claim.837
```

---

## Troubleshooting

### The HealthSim tools aren't available

Run `/mcp` and look for `plugin:healthsim:healthsim`.

- **Failed**: check `uv --version`. If uv was just installed, restart Claude Code.
- **Timed out on first start**: the first start downloads Python packages. Run `/healthsim:setup`, which prepares the environment, then reconnect from `/mcp`.

### "Reference data is not installed"

Run `/healthsim:setup`. Generation and cohort tools work without reference data; provider search and population queries need it.

### A checkout shows a ~130-byte `healthsim.duckdb`

That file is a Git LFS pointer. Run `git lfs pull` in the checkout, or install reference data with `/healthsim:setup` instead. The plugin ignores pointer files.

### Two HealthSim skills appear

If you also uploaded HealthSim's `SKILL.md` to claude.ai, it syncs into Claude Code as a separate skill. Turn it off in claude.ai settings so the plugin's skills are the only ones in use.

---

## Next Steps

- [Hello HealthSim](README.md): first steps and examples
- [Examples by Product](examples/): ready-to-use prompts
- [Extending HealthSim](EXTENDING.md): add cohorts, skills, and formats
