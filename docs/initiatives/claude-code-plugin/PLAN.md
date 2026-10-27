# Claude Code Plugin - Plan

**Approved**: 2026-10-27
**Progress**: [PROGRESS.md](PROGRESS.md)

---

## Why

HealthSim only works when Claude Code is started inside this repository. Three things depend on that working directory: the routing instructions in `.claude/CLAUDE.md`, the MCP server's import path, and the location of `healthsim.duckdb`. Packaging HealthSim as a Claude Code plugin removes that limit: install it once and use it from any project.

## What

This repository becomes both the plugin and its own marketplace:

```
/plugin marketplace add mark64oswald/healthsim-workspace
/plugin install healthsim@healthsim
```

| Part | Where | Notes |
|------|-------|-------|
| Plugin manifest | `.claude-plugin/plugin.json` | Name `healthsim` |
| Marketplace | `.claude-plugin/marketplace.json` | One entry, source `./` |
| MCP server | `.mcp.json` | `uv run --frozen` with `${CLAUDE_PLUGIN_ROOT}`; Python env in `${CLAUDE_PLUGIN_DATA}` |
| Skills | `skills/` | Existing product skills plus a `healthsim` router skill |
| Setup and status | `skills/setup`, `skills/status` | Install reference data, show where data lives |
| Data | `~/.healthsim/` | `reference.duckdb` (read-only, downloaded once) and `cohorts.duckdb` (your cohorts) |

```
Any project (Claude Code) ──> healthsim plugin ──> skills
                                    │
                                    └─> MCP server ──> ~/.healthsim/reference.duckdb  (read-only)
                                                   ──> ~/.healthsim/cohorts.duckdb    (read-write)
                                                   ──> MotherDuck                     (optional)
```

## How

### Data location

Resolved once in `healthsim.db.paths`:

1. `HEALTHSIM_DB_PATH`: one database at that path, or MotherDuck when it starts with `md:`
2. `~/.healthsim/reference.duckdb` exists: split layout under `~/.healthsim` (`HEALTHSIM_HOME` overrides)
3. Repo-root `healthsim.duckdb` is a real file, not an LFS pointer: the developer layout, unchanged
4. Otherwise: split layout with no reference data; the reference tools return a setup hint

### Reference data distribution

Claude Code never downloads Git LFS content when it installs a plugin, so the reference database ships separately as a GitHub Release asset (`data-YYYY.MM`). The setup skill downloads it, checks its SHA-256, and installs it in `~/.healthsim`. MotherDuck remains an alternative that needs no download.

`healthsim.duckdb` stays in Git LFS for development. Plugin installs only ever see the pointer, which the resolver ignores.

### Phases

| Phase | Work |
|-------|------|
| 0 | Verify the plugin spec; feature branch |
| 1 | `healthsim.db.paths`, split layout, fixture database, tests |
| 2 | MCP server as an installable uv package; pinned dependencies |
| 3 | Manifest, marketplace, `.mcp.json`, router skill, setup and status skills |
| 4 | `scripts/publish_reference_data.py`, `scripts/install_reference_data.py` |
| 5 | End-to-end check on a Mac with the real data |
| 6 | README, Hello HealthSim guide, link check, pull request |

### Decisions

| Decision | Choice |
|----------|--------|
| Repository for the plugin | healthsim-workspace |
| Default data mode | Release asset to `~/.healthsim`; MotherDuck optional |
| Split reference and cohort databases | Yes |
| Python runner | `uv` |
| healthsim-agent repository | Archive with a pointer to this repository |
