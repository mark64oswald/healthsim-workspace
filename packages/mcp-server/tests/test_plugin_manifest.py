"""
Checks on the Claude Code plugin packaging at the repository root.

These guard the pieces that only fail after someone installs the plugin:
manifest JSON, the MCP server launch command, the generated router skill, and
the plugin commands.
"""

import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
PLUGIN_DIR = REPO_ROOT / ".claude-plugin"


@pytest.fixture(scope="module")
def plugin():
    return json.loads((PLUGIN_DIR / "plugin.json").read_text())


@pytest.fixture(scope="module")
def marketplace():
    return json.loads((PLUGIN_DIR / "marketplace.json").read_text())


def test_plugin_name_and_metadata(plugin):
    assert plugin["name"] == "healthsim"
    assert plugin["license"] == "Apache-2.0"
    assert plugin["repository"].endswith("mark64oswald/healthsim-workspace")


def test_marketplace_lists_repo_root_plugin(marketplace):
    assert marketplace["name"] == "healthsim"
    (entry,) = marketplace["plugins"]
    assert entry["name"] == "healthsim"
    assert entry["source"] == "."


def test_version_lives_in_one_place(plugin, marketplace):
    # Claude Code uses plugin.json's version and warns on a mismatch; with no
    # version, installs track commits.
    assert not ("version" in plugin and "version" in marketplace["plugins"][0])


def test_mcp_server_command_points_at_real_paths(plugin):
    server = plugin["mcpServers"]["healthsim"]
    assert server["command"] == "uv"
    args = server["args"]
    assert "--frozen" in args
    directory = args[args.index("--directory") + 1]
    assert directory.startswith("${CLAUDE_PLUGIN_ROOT}/")
    assert (REPO_ROOT / directory.removeprefix("${CLAUDE_PLUGIN_ROOT}/") / "pyproject.toml").exists()
    assert args[-1] == "healthsim-mcp"
    # The Python environment must persist outside the versioned plugin root
    assert server["env"]["UV_PROJECT_ENVIRONMENT"].startswith("${CLAUDE_PLUGIN_DATA}")
    assert (REPO_ROOT / "uv.lock").exists()


def test_no_project_mcp_json_at_root():
    # A root .mcp.json would also load as project config when working in the
    # checkout, where ${CLAUDE_PLUGIN_ROOT} doesn't resolve.
    assert not (REPO_ROOT / ".mcp.json").exists()


def test_no_top_level_bin_directory():
    # claude.ai organization sync rejects plugins with a top-level bin/
    assert not (REPO_ROOT / "bin").exists()


def test_mcp_pinned_below_2():
    pyproject = (REPO_ROOT / "packages" / "mcp-server" / "pyproject.toml").read_text()
    assert re.search(r'"mcp>=[^"]*,<2"', pyproject)


def test_router_skill_is_up_to_date():
    result = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "build_plugin_router.py"), "--check"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_every_skill_has_frontmatter():
    for skill in sorted((REPO_ROOT / "skills").glob("*/SKILL.md")):
        text = skill.read_text()
        assert text.startswith("---\n"), skill
        header = text.split("\n---\n", 1)[0]
        assert re.search(r"^name: ", header, re.M), skill
        assert re.search(r"^description: ", header, re.M), skill


@pytest.mark.parametrize("name", ["setup", "status"])
def test_commands_exist_with_description(name):
    text = (REPO_ROOT / "commands" / f"{name}.md").read_text()
    assert text.startswith("---\n")
    assert "description:" in text.split("\n---\n", 1)[0]
    assert "${CLAUDE_PLUGIN_ROOT}" in text
