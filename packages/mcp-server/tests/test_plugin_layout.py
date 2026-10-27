"""
End-to-end tests for the plugin data layout.

Starts the MCP server as a subprocess over stdio, the way Claude Code starts a
plugin's MCP server: from an unrelated working directory, with HEALTHSIM_HOME
pointing at a data directory that holds a small fixture reference database.
"""

import json
import os
import sys
from pathlib import Path

import pytest

from healthsim.db.fixtures import build_reference_fixture

mcp_client = pytest.importorskip("mcp")
from mcp import ClientSession, StdioServerParameters  # noqa: E402
from mcp.client.stdio import stdio_client  # noqa: E402

SERVER = Path(__file__).resolve().parent.parent / "healthsim_mcp.py"


def _server_env(home: Path) -> dict:
    env = {k: v for k, v in os.environ.items() if not k.startswith("HEALTHSIM_")}
    env["HEALTHSIM_HOME"] = str(home)
    return env


async def _call(session: ClientSession, tool: str, arguments: dict | None = None) -> dict:
    result = await session.call_tool(tool, arguments or {})
    return json.loads(result.content[0].text)


async def _run(home: Path, cwd: Path, steps):
    params = StdioServerParameters(
        command=sys.executable, args=[str(SERVER)], env=_server_env(home), cwd=str(cwd)
    )
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            return await steps(session)


@pytest.fixture
def plugin_home(tmp_path):
    home = tmp_path / "healthsim-home"
    build_reference_fixture(home / "reference.duckdb")
    elsewhere = tmp_path / "some-other-project"
    elsewhere.mkdir()
    return home, elsewhere


@pytest.mark.anyio
async def test_tools_work_from_another_directory(plugin_home):
    home, elsewhere = plugin_home

    async def steps(session):
        tools = {t.name for t in (await session.list_tools()).tools}
        status = await _call(session, "healthsim_data_status")
        providers = await _call(
            session, "healthsim_search_providers", {"params": {"state": "CA", "city": "San Diego"}}
        )
        svi = await _call(
            session, "healthsim_query_reference", {"params": {"table": "svi_county", "state": "TX"}}
        )
        tables = await _call(session, "healthsim_tables")
        return tools, status, providers, svi, tables

    tools, status, providers, svi, tables = await _run(home, elsewhere, steps)

    assert {"healthsim_data_status", "healthsim_search_providers", "healthsim_add_entities"} <= tools
    assert status["mode"] == "split"
    assert status["has_reference"] is True
    assert status["db_path"] == str(home / "cohorts.duckdb")
    assert "error" not in providers, providers
    assert len(providers["providers"]) == 3
    assert svi["row_count"] == 1
    assert "network.providers" in tables["reference_schema_tables"]


@pytest.mark.anyio
async def test_cohorts_persist_in_home(plugin_home):
    home, elsewhere = plugin_home

    async def save(session):
        return await _call(
            session,
            "healthsim_add_entities",
            {
                "params": {
                    "cohort_name": "plugin-smoke",
                    "entities": {
                        "patients": [
                            {
                                "patient_id": "P-1",
                                "mrn": "MRN-1",
                                "given_name": "Test",
                                "family_name": "Patient",
                                "birth_date": "1960-01-01",
                                "gender": "F",
                            }
                        ]
                    },
                }
            },
        )

    saved = await _run(home, elsewhere, save)
    assert "error" not in saved, saved

    # A new server process (a new Claude Code session) sees the cohort
    listed = await _run(home, elsewhere, lambda s: _call(s, "healthsim_list_cohorts", {"params": {}}))
    cohorts = listed["cohorts"] if isinstance(listed, dict) else listed
    names = [c["name"] for c in cohorts]
    assert "plugin-smoke" in names
    assert (home / "cohorts.duckdb").exists()
    assert not (elsewhere / "healthsim.duckdb").exists()


@pytest.mark.anyio
async def test_missing_reference_gives_setup_hint(tmp_path):
    home = tmp_path / "empty-home"
    result = await _run(
        home,
        tmp_path,
        lambda s: _call(s, "healthsim_search_providers", {"params": {"state": "CA"}}),
    )
    assert "/healthsim:setup" in result["error"]


@pytest.fixture
def anyio_backend():
    return "asyncio"
