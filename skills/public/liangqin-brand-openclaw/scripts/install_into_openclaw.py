#!/usr/bin/env python3
"""Install the exported Liangqin Brand Body skill into OpenClaw skill stores."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Install 良禽品牌体 into OpenClaw skill stores.")
    parser.add_argument(
        "--source",
        default=str(Path(__file__).resolve().parents[1]),
        help="Exported skill package directory.",
    )
    parser.add_argument(
        "--dest",
        default="",
        help="Primary destination. Defaults to ~/.openclaw/skills/<package_slug>.",
    )
    parser.add_argument(
        "--workspace-dest",
        default="",
        help="Workspace mirror destination. Defaults to ~/.openclaw/workspace/skills/<package_slug>.",
    )
    return parser.parse_args()


def load_manifest(source: Path) -> dict:
    manifest_path = source / "skill-release.json"
    if not manifest_path.exists():
        raise SystemExit(f"skill-release.json not found: {manifest_path}")
    return json.loads(manifest_path.read_text(encoding="utf-8"))


def validate_exported_package(source: Path) -> None:
    expected = [
        source / "SKILL.md",
        source / "DESIGN.md",
        source / "CONSUMER-GUIDE.zh-CN.md",
        source / "DESIGN-GOVERNANCE.md",
        source / "design-standard-package.json",
        source / "EXECUTION-CHECKLIST.md",
        source / "evaluation" / "manual-rubric.zh-CN.md",
        source / "protocols" / "brand-assets.zh-CN.json",
        source / "assets" / "brand" / "asset-manifest.zh-CN.json",
        source / "assets" / "brand" / "liangqinjiamu-logo-horizontal.svg",
        source / "assets" / "brand" / "liangqinjiamu-logo-vertical.svg",
        source / "foundation-dna" / "design-dna.zh-CN.json",
        source / "foundation-dna" / "tokens.semantic.json",
        source / "artifact-surfaces",
        source / "design-packs",
    ]
    missing = [str(path) for path in expected if not path.exists()]
    if missing:
        raise SystemExit(f"Exported package is incomplete: {missing}")


def install_tree(source: Path, dest: Path) -> None:
    if dest.exists():
        shutil.rmtree(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, dest, ignore=shutil.ignore_patterns("__pycache__", ".DS_Store"))


def main() -> int:
    args = parse_args()
    source = Path(args.source).expanduser().resolve()
    if not source.exists():
        raise SystemExit(f"Source package not found: {source}")

    manifest = load_manifest(source)
    package_slug = manifest["package_slug"]
    validate_exported_package(source)

    primary_dest = (
        Path(args.dest).expanduser().resolve()
        if args.dest
        else (Path.home() / ".openclaw" / "skills" / package_slug)
    )
    workspace_dest = (
        Path(args.workspace_dest).expanduser().resolve()
        if args.workspace_dest
        else (Path.home() / ".openclaw" / "workspace" / "skills" / package_slug)
    )

    for dest in [primary_dest, workspace_dest]:
        install_tree(source, dest)
        print(f"Installed 良禽品牌体 to {dest}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
