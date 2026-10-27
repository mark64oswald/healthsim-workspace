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
| 3 | Plugin scaffold (manifest, marketplace, MCP config, router skill, commands) | ✅ Complete |
| 4 | Reference data distribution (publish script, setup command) | ✅ Complete (`data-2026.10` published) |
| 5 | End-to-end test on a Mac with real data | ✅ Complete |
| 6 | Documentation, link check, pull request | ✅ Complete |

## Follow-ups

- `healthsim_search_providers` stops at 200 rows and returns no `total_count`, so it can't answer "how many" on its own
- `filters_applied` in that tool's output leaves out `county_fips`
- "Primary taxonomy" means `taxonomy_1`; the NPPES primary-taxonomy switch isn't used
- Archive the `healthsim-agent` repository

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

### 2026-10-27: Phases 3, 4 and 6

**Phase 4** (`packages/core/src/healthsim/db/install.py`):
- `package`: extracts the `network` and `population` schemas from the unified database (cohort tables stay behind), gzips them, and writes `reference-manifest.json` with SHA-256 checksums.
- `download`: finds the newest `data-*` release, downloads it, verifies both checksums, and installs it atomically into `~/.healthsim`.
- `from-file`: installs from a local `healthsim.duckdb`, optionally importing its cohorts (`import-cohorts` copies rows by column name and advances id sequences).
- `scripts/publish_reference_data.py` wraps `package` and creates the GitHub Release with `gh`.

**Phase 3** (plugin scaffold):
- `.claude-plugin/plugin.json` declares the MCP server inline rather than in a root `.mcp.json`, which would also load as project config in a checkout where `${CLAUDE_PLUGIN_ROOT}` doesn't resolve.
- The server runs with `uv run --frozen` from `${CLAUDE_PLUGIN_ROOT}/packages/mcp-server`, and its virtual environment lives in `${CLAUDE_PLUGIN_DATA}/venv`, so it survives plugin updates.
- `plugin.json` has no `version`, so installs track commits; `claude plugin validate` warns about this by design.
- `skills/healthsim/SKILL.md` is generated from the root `SKILL.md` by `scripts/build_plugin_router.py`, and a test fails if it's out of date.
- `commands/setup.md` and `commands/status.md` provide `/healthsim:setup` and `/healthsim:status`.
- The server re-attaches reference data installed while it's running, so setup needs no restart.

**Verified with the Claude Code CLI** (v2.1.311, clean config directory, cloud container):
- `claude plugin validate .` passed with two expected warnings: no `version` and no icon.
- `claude plugin marketplace add mark64oswald/healthsim-workspace#feature/claude-code-plugin` and `claude plugin install healthsim@healthsim` succeeded. Claude Code reported the LFS pointer and skipped it, as the docs describe.
- `claude mcp list` from an unrelated folder: `plugin:healthsim:healthsim ... Connected`.
- `claude -p` from that folder called `healthsim_search_providers` against a fixture reference database and listed the `healthsim:*` skills.

**Phase 6** (docs): `hello-healthsim/CLAUDE-CODE.md` rewritten for the plugin. The old version referenced the retired `healthsim-common` repository and an `npx` filesystem server. README, INSTALL, Hello HealthSim, MCP server README, and CHANGELOG were updated. `scripts/validate_links.py` reports no new broken links (170 existed before, mostly in `docs/archive/`).

**Test results**: core 1,627 passed, 109 skipped; mcp-server 119 passed, 21 skipped; product packages unchanged; `scripts/smoke_test.py` 37 passed.

### 2026-10-27: Phase 5 and release

**Release**: [`data-2026.10`](https://github.com/mark64oswald/healthsim-workspace/releases/tag/data-2026.10), with `reference.duckdb.gz` (516 MB, 10 tables, 8,925,672 providers) and `reference-manifest.json`. A fresh `/healthsim:setup download` into an empty `HEALTHSIM_HOME` verified both checksums and answered provider and population queries.

**Mac test** (Claude Code 2.1.278): installed from the marketplace, installed reference data from a local file, and confirmed from an unrelated folder that the MCP server connects and finds 1,784 family medicine providers in San Diego County.

**Fix**: with the real database present, the plugin layout tests fell back to the repo-root `healthsim.duckdb` and saved test cohorts into it. An explicitly set `HEALTHSIM_HOME` now skips that fallback. All suites pass against the real database: core 1,713 passed, mcp-server 140 passed.
