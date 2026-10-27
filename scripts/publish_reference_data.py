#!/usr/bin/env python3
"""
Publish HealthSim reference data as a GitHub Release.

Claude Code never downloads Git LFS files when it installs a plugin, so the
plugin's setup command downloads reference data from a GitHub Release instead.
This script builds that release from the repo-root healthsim.duckdb:

1. Copies the network and population schemas into a standalone reference.duckdb
   (cohort tables are left behind)
2. Compresses it and writes reference-manifest.json with SHA-256 checksums
3. Creates the release with the GitHub CLI (skip with --no-release)

Run it on a machine where `git lfs pull` has fetched the real database:

    uv run --package healthsim-core python scripts/publish_reference_data.py
    uv run --package healthsim-core python scripts/publish_reference_data.py --tag data-2026.11

Requires: the GitHub CLI (`gh auth login`) for the release step.
"""

import argparse
import json
import subprocess
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "packages" / "core" / "src"))

from healthsim.db.install import (  # noqa: E402
    ASSET_NAME,
    RELEASE_PREFIX,
    extract_reference,
    package_reference,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--source", default=str(REPO_ROOT / "healthsim.duckdb"))
    parser.add_argument("--tag", default=f"{RELEASE_PREFIX}{date.today():%Y.%m}")
    parser.add_argument("--out", default=str(REPO_ROOT / "dist" / "reference-data"))
    parser.add_argument("--no-release", action="store_true", help="Build files only")
    args = parser.parse_args()

    out = Path(args.out)
    database = out / "reference.duckdb"
    print(f"Extracting reference schemas from {args.source}")
    summary = extract_reference(args.source, database)
    print(f"  {summary['table_count']} tables")
    manifest_path = package_reference(database, out, tag=args.tag, tables=summary["tables"])
    manifest = json.loads(manifest_path.read_text())
    print(f"  {ASSET_NAME}: {manifest['asset_bytes'] / 1e6:,.0f} MB")

    if args.no_release:
        print(f"Built {out / ASSET_NAME} and {manifest_path}; no release created")
        return 0

    notes = "\n".join(
        [
            "HealthSim reference data for the Claude Code plugin.",
            "",
            "Install it with `/healthsim:setup` in Claude Code, or:",
            "`python -m healthsim.db.install download --tag " + args.tag + "`",
            "",
            "| Table | Rows |",
            "| --- | --- |",
            *[f"| {t} | {n:,} |" for t, n in manifest["tables"].items()],
        ]
    )
    subprocess.run(
        [
            "gh", "release", "create", args.tag,
            str(out / ASSET_NAME), str(manifest_path),
            "--title", f"Reference data {args.tag}",
            "--notes", notes,
        ],
        check=True,
        cwd=REPO_ROOT,
    )
    print(f"Published release {args.tag}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
