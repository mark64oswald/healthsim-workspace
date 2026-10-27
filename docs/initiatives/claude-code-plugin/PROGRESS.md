# Claude Code Plugin - Progress

**Goal**: Install HealthSim once as a Claude Code plugin and use it from any project, not only from inside this repository.
**Branch**: `feature/claude-code-plugin`
**Started**: 2026-10-27
**Plan**: [PLAN.md](PLAN.md)

---

## Status

| Phase | Description | Status |
|-------|-------------|--------|
| 0 | Verify plugin spec, set up branch | ✅ Complete |
| 1 | Decouple data paths, split reference vs cohort data | ✅ Complete |
| 2 | Make the MCP server installable (uv workspace, pinned deps) | ✅ Complete |
| 3 | Plugin scaffold (manifest, marketplace, MCP config, router skill, commands) | ⬜ Pending |
| 4 | Reference data distribution (publish script, setup command) | ⬜ Pending |
| 5 | End-to-end test on a Mac with real data | ⬜ Pending (needs Mark) |
| 6 | Documentation, link check, pull request | ⬜ Pending |

---

## Log

### 2026-10-27: Phases 0 to 2

**Phase 0 findings** (from the Claude Code plugin docs):
- Plugin installs clone the marketplace repo and **never download Git LFS content**, so `healthsim.duckdb` arrives as a pointer. Reference data has to be installed separately.
- `${CLAUDE_PLUGIN_ROOT}` changes on every plugin update, so nothing may be written there. `${CLAUDE_PLUGIN_DATA}` persists across updates but is deleted on uninstall, so it holds only the Python environment. Cohorts and reference data live in `~/.healthsim`, which also survives an uninstall.
- A `CLAUDE.md` at the plugin root is not loaded; routing instructions must be a skill.
- A top-level `bin/` directory blocks claude.ai distribution, so scripts stay in `scripts/`.
- `mcp` 2.x renamed `FastMCP`, which broke a fresh install of the server. Pinned `mcp>=1.0.0,<2` in `packages/mcp-server/pyproject.toml` and the `Dockerfile`.

**Phase 1** (`packages/core/src/healthsim/db/paths.py`):
- One resolution order for data: `HEALTHSIM_DB_PATH`, then `~/.healthsim/reference.duckdb` (split layout), then the repo-root `healthsim.duckdb` if it's a real file, then an empty split layout.
- Split layout: `cohorts.duckdb` is the main database and `reference.duckdb` is attached read-only as `healthsim_ref`, with its schemas on the DuckDB `search_path`. Existing SQL such as `network.providers` works unchanged.
- `healthsim.db.fixtures` builds a small fixture reference database for tests.
- Tests that need the real database now skip cleanly when it's a Git LFS pointer, instead of failing.

**Phase 2** (`packages/mcp-server`):
- The server resolves its layout at startup, creates `cohorts.duckdb` on first run, and returns a setup hint from the reference tools when data isn't installed.
- New tool `healthsim_data_status`. `healthsim_tables` lists the `network` and `population` tables too.
- `healthsim-core` is a declared dependency. The uv workspace was fixed (`[tool.uv.sources]` in the root `pyproject.toml`) and `uv.lock` is committed, so `uv run --frozen` works from any directory.
- New end-to-end test (`tests/test_plugin_layout.py`) starts the server over stdio from an unrelated directory and checks reference queries, cohort saves, and persistence across restarts.

**Test results** (cloud container, no Git LFS):

| Package | Passed | Skipped | Failed |
|---------|--------|---------|--------|
| core | 1,616 | 109 | 0 |
| mcp-server | 107 | 21 | 0 |
| patientsim | 486 | 10 | 0 |
| membersim | 211 | 0 | 0 |
| rxmembersim | 234 | 0 | 0 |
| trialsim | 110 | 0 | 0 |

Before this work, core had 37 failures and 28 errors, and mcp-server had 26 failures, all caused by the LFS pointer or a missing install.
