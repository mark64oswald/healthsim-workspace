#!/usr/bin/env python3
"""
Build the plugin's router skill from the root SKILL.md.

The root SKILL.md is the master HealthSim skill: the entry point in a checkout,
the file uploaded to claude.ai, and the page linked from the README. The Claude
Code plugin loads skills only from skills/<name>/SKILL.md, so this script writes
skills/healthsim/SKILL.md from it, adds a short section on how the plugin finds
its data, and rewrites relative links for the new location.

Edit the root SKILL.md (or PLUGIN_SECTION below), then run:

    python scripts/build_plugin_router.py          # write skills/healthsim/SKILL.md
    python scripts/build_plugin_router.py --check  # exit 1 if it is out of date
"""

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCE = REPO_ROOT / "SKILL.md"
TARGET = REPO_ROOT / "skills" / "healthsim" / "SKILL.md"

NOTICE = (
    "<!-- Generated from /SKILL.md by scripts/build_plugin_router.py. "
    "Edit the root SKILL.md and re-run the script. -->"
)

PLUGIN_SECTION = """## Using HealthSim as a Claude Code Plugin

When HealthSim is installed as a plugin, it works from any project. Product skills are namespaced under the plugin:

| Request Type | Skill |
|--------------|-------|
| Patients, clinical data, diagnoses, labs, EMR | `healthsim:patientsim` |
| Claims, members, enrollment, benefits | `healthsim:membersim` |
| Pharmacy, prescriptions, formulary, DUR | `healthsim:rxmembersim` |
| Clinical trials, subjects, CDISC | `healthsim:trialsim` |
| Demographics, SDOH, SVI, ADI, county/tract profiles | `healthsim:populationsim` |
| Provider networks, facilities, NPPES | `healthsim:networksim` |
| Profiles, journeys, large-scale generation | `healthsim:generation` |
| Saving/loading cohorts, identity correlation, SQL | `healthsim:common` |

**Data access goes through the HealthSim MCP tools**, never through files in the current project:

- `healthsim_query_reference` for CDC PLACES, SVI and ADI
- `healthsim_search_providers` for real NPPES providers
- `healthsim_add_entities`, `healthsim_list_cohorts`, `healthsim_load_cohort`, `healthsim_query` for cohorts
- `healthsim_data_status` to see where data lives

Reference data and saved cohorts live in `~/.healthsim`, not in the project you are working in. If a reference tool reports that data is missing, tell the user to run `/healthsim:setup`. Synthetic generation and cohort tools work without it.

Format and reference documents ship with the plugin under `${CLAUDE_PLUGIN_ROOT}/formats/` and `${CLAUDE_PLUGIN_ROOT}/references/`.

"""

# Root-relative link prefixes and where they live relative to skills/healthsim/
LINK_PREFIXES = {
    "skills/": "../",
    "formats/": "../../formats/",
    "references/": "../../references/",
    "docs/": "../../docs/",
    "hello-healthsim/": "../../hello-healthsim/",
}

_LINK = re.compile(r"\]\((?!https?://|#|/)([^)]+)\)")


def _rewrite_link(match: re.Match) -> str:
    target = match.group(1)
    for prefix, replacement in LINK_PREFIXES.items():
        if target.startswith(prefix):
            return f"]({replacement}{target[len(prefix):]})"
    return f"](../../{target})"


def build() -> str:
    text = SOURCE.read_text()
    if not text.startswith("---\n"):
        raise ValueError("Root SKILL.md must start with YAML frontmatter")
    end = text.index("\n---\n", 4) + len("\n---\n")
    frontmatter, body = text[:end], text[end:]

    body = _LINK.sub(_rewrite_link, body)
    # Insert the plugin section before the first second-level heading after the title
    first_h2 = body.index("\n## ")
    body = body[: first_h2 + 1] + PLUGIN_SECTION + body[first_h2 + 1 :]
    return f"{frontmatter}\n{NOTICE}\n{body}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--check", action="store_true", help="Fail if the router skill is out of date")
    args = parser.parse_args()

    expected = build()
    if args.check:
        if not TARGET.exists() or TARGET.read_text() != expected:
            print(f"{TARGET.relative_to(REPO_ROOT)} is out of date; run scripts/build_plugin_router.py")
            return 1
        print(f"{TARGET.relative_to(REPO_ROOT)} is up to date")
        return 0

    TARGET.parent.mkdir(parents=True, exist_ok=True)
    TARGET.write_text(expected)
    print(f"Wrote {TARGET.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
