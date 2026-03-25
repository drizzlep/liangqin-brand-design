#!/usr/bin/env python3
"""Validate and publish the Liangqin brand design skill into OpenClaw skill stores."""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

ALLOWED_FRONTMATTER_KEYS = {"name", "description"}
IGNORE_NAMES = {"__pycache__", ".DS_Store"}
DEFAULT_ACTIVE_DEST = Path.home() / ".openclaw" / "skills" / "liangqin-brand-design"
DEFAULT_WORKSPACE_DEST = Path.home() / ".openclaw" / "workspace" / "skills" / "liangqin-brand-design"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate and publish the Liangqin brand design skill to OpenClaw skill stores.")
    parser.add_argument("--source", default=str(Path(__file__).resolve().parent.parent), help="Shared skill source directory.")
    parser.add_argument("--dest", default=str(DEFAULT_ACTIVE_DEST), help="Primary OpenClaw skill destination directory.")
    parser.add_argument(
        "--workspace-dest",
        default=str(DEFAULT_WORKSPACE_DEST),
        help="Workspace mirror destination directory. Pass empty string to skip.",
    )
    return parser.parse_args()


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        raise SystemExit("No YAML frontmatter found at the top of SKILL.md")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise SystemExit("Invalid frontmatter format in SKILL.md")
    raw = text[4:end].splitlines()
    result: dict[str, str] = {}
    for line in raw:
        stripped = line.strip()
        if not stripped:
            continue
        if ":" not in stripped:
            raise SystemExit(f"Invalid frontmatter line: {line}")
        key, value = stripped.split(":", 1)
        result[key.strip()] = value.strip().strip('"').strip("'")
    return result


def validate_skill_dir(skill_dir: Path) -> None:
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        raise SystemExit(f"SKILL.md not found: {skill_md}")

    frontmatter = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
    unexpected = set(frontmatter) - ALLOWED_FRONTMATTER_KEYS
    if unexpected:
        raise SystemExit(f"Unexpected frontmatter keys: {', '.join(sorted(unexpected))}")

    name = frontmatter.get("name", "").strip()
    description = frontmatter.get("description", "").strip()
    if not name or not description:
        raise SystemExit("Frontmatter requires non-empty name and description")
    if not re.fullmatch(r"[a-z0-9-]+", name):
        raise SystemExit("Frontmatter name must be kebab-case")
    if "<" in description or ">" in description:
        raise SystemExit("Frontmatter description cannot contain angle brackets")
    if not (skill_dir / "references").exists():
        raise SystemExit("references directory is required for this skill")


def ignore_filter(_dir: str, names: list[str]) -> set[str]:
    return {name for name in names if name in IGNORE_NAMES}


def publish(source: Path, dest: Path) -> None:
    if dest.exists():
        shutil.rmtree(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, dest, ignore=ignore_filter)


def main() -> int:
    args = parse_args()
    source = Path(args.source).expanduser().resolve()
    dest = Path(args.dest).expanduser().resolve()
    workspace_dest = Path(args.workspace_dest).expanduser().resolve() if args.workspace_dest else None

    destinations = [dest]
    if workspace_dest and workspace_dest not in destinations:
        destinations.append(workspace_dest)

    if any(source == candidate for candidate in destinations):
        raise SystemExit("Source and destination must be different.")

    validate_skill_dir(source)
    for candidate in destinations:
        publish(source, candidate)
        validate_skill_dir(candidate)
        print(f"Published skill to {candidate}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
