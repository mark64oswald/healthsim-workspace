"""
push-skills.py — Upload skill files to the Anthropic Skills API.

Usage:
    .venv/bin/python3 deploy/push-skills.py \\
        --path ./skills/common/ \\
        --name skill_healthsim_common_v1

    .venv/bin/python3 deploy/push-skills.py --list

Environment:
    ANTHROPIC_API_KEY must be set (via .env or shell export).
"""

import argparse
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

# Load .env from workspace root
WORKSPACE_ROOT = Path(__file__).parent.parent
load_dotenv(WORKSPACE_ROOT / ".env")

SKILL_IDS_FILE = Path(__file__).parent / "skill-ids.json"


def load_skill_ids() -> dict:
    """Load existing skill IDs from deploy/skill-ids.json."""
    if SKILL_IDS_FILE.exists():
        return json.loads(SKILL_IDS_FILE.read_text())
    return {}


def save_skill_ids(ids: dict):
    """Save skill IDs to deploy/skill-ids.json."""
    SKILL_IDS_FILE.write_text(json.dumps(ids, indent=2) + "\n")


def get_client():
    """Create an Anthropic client."""
    import anthropic

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY not set. Check .env file.", file=sys.stderr)
        sys.exit(1)
    return anthropic.Anthropic(api_key=api_key)


def upload_skill(skill_path: Path, display_name: str):
    """Upload a skill directory to the Anthropic Skills API."""
    if not skill_path.exists():
        print(f"ERROR: Skill path not found: {skill_path}", file=sys.stderr)
        sys.exit(1)

    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        print(f"ERROR: No SKILL.md found in {skill_path}", file=sys.stderr)
        sys.exit(1)

    # Collect all .md files in the skill directory
    files = sorted(skill_path.glob("*.md"))
    print(f"Uploading skill from {skill_path}")
    print(f"  Display name: {display_name}")
    print(f"  Files: {[f.name for f in files]}")

    client = get_client()

    # Upload — use tuple form (filename, file_bytes, content_type)
    # The API expects files inside a top-level directory, e.g. "skill/SKILL.md"
    dir_name = skill_path.name
    file_tuples = [
        (f"{dir_name}/{f.name}", open(f, "rb"), "text/markdown")
        for f in files
    ]
    result = client.beta.skills.create(
        display_title=display_name,
        files=file_tuples,
    )

    print(f"\n  Skill ID: {result.id}")
    print(f"  Version:  {result.latest_version}")
    print(f"  Created:  {result.created_at}")

    return result


def list_skills():
    """List all skills from the Anthropic Skills API."""
    client = get_client()
    page = client.beta.skills.list(source="custom")
    skills = list(page)

    if not skills:
        print("No custom skills found.")
        return

    print(f"Custom skills ({len(skills)}):\n")
    for skill in skills:
        print(f"  {skill.id}")
        print(f"    Title:   {skill.display_title}")
        print(f"    Version: {skill.latest_version}")
        print(f"    Created: {skill.created_at}")
        print()


def main():
    parser = argparse.ArgumentParser(description="Upload skills to Anthropic Skills API")
    parser.add_argument("--path", type=Path, help="Path to skill directory")
    parser.add_argument("--name", help="Skill identifier (for skill-ids.json)")
    parser.add_argument("--list", action="store_true", help="List existing skills")
    args = parser.parse_args()

    if args.list:
        list_skills()
        return

    if not args.path or not args.name:
        parser.error("--path and --name are required for upload")

    result = upload_skill(args.path, args.name)

    # Save to skill-ids.json
    ids = load_skill_ids()
    ids[args.name] = result.id
    save_skill_ids(ids)
    print(f"\n  Saved to {SKILL_IDS_FILE}")


if __name__ == "__main__":
    main()
