#!/usr/bin/env python3
"""Run the standard-package release checks and build the OpenClaw release bundle."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RELEASE_METADATA = (
    ROOT / "skills" / "public" / "liangqin-brand-openclaw" / "skill-release.json"
)
CORE_TEST_MODULES = [
    "tests.test_liangqin_brand_skill_assets",
    "tests.test_liangqin_brand_skill_distribution",
    "tests.test_design_md_adapter",
    "tests.test_sync_openclaw_mirrors",
    "tests.test_standard_package_integrity",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run release checks and prepare the GitHub release bundle for 良禽品牌体."
    )
    parser.add_argument(
        "--output-dir",
        default=str(ROOT / "dist"),
        help="Directory used for exported release artifacts.",
    )
    parser.add_argument(
        "--skip-tests",
        action="store_true",
        help="Skip the core unittest suite before export.",
    )
    parser.add_argument(
        "--skip-validate",
        action="store_true",
        help="Skip the OpenClaw asset validator before export.",
    )
    return parser.parse_args()


def run_step(title: str, command: list[str]) -> None:
    print(f"[run] {title}")
    print("      " + " ".join(command))
    result = subprocess.run(command, cwd=ROOT, check=False, text=True, capture_output=True)
    if result.returncode != 0:
        raise SystemExit(
            f"{title} failed:\n"
            f"command: {' '.join(command)}\n"
            f"stdout:\n{result.stdout}\n"
            f"stderr:\n{result.stderr}"
        )
    if result.stdout.strip():
        print(result.stdout.rstrip())
    if result.stderr.strip():
        print(result.stderr.rstrip())


def main() -> int:
    args = parse_args()
    metadata = json.loads(RELEASE_METADATA.read_text(encoding="utf-8"))
    package_slug = metadata["package_slug"]
    version = metadata["version"]
    output_dir = Path(args.output_dir).expanduser().resolve()

    run_step(
        "sync OpenClaw mirrors",
        ["python3", str(ROOT / "scripts" / "sync_openclaw_mirrors.py")],
    )

    if not args.skip_tests:
        run_step(
            "run core release tests",
            ["python3", "-m", "unittest", *CORE_TEST_MODULES],
        )
    if not args.skip_validate:
        run_step(
            "validate exported skill assets",
            [
                "python3",
                str(
                    ROOT
                    / "skills"
                    / "public"
                    / "liangqin-brand-openclaw"
                    / "scripts"
                    / "validate_skill_assets.py"
                ),
            ],
        )
    run_step(
        "export OpenClaw release bundle",
        [
            "python3",
            str(ROOT / "scripts" / "export_openclaw_skill.py"),
            "--output-dir",
            str(output_dir),
            "--zip",
        ],
    )

    zip_path = output_dir / f"{package_slug}-{version}.zip"
    if not zip_path.exists():
        raise SystemExit(f"expected release zip not found: {zip_path}")

    print(f"Prepared release artifact: {zip_path}")
    print("")
    print("Next steps:")
    print("1. Commit your changes:")
    print(f"   git add . && git commit -m 'release: prepare v{version}'")
    print("2. Push branch and tag:")
    print(f"   git tag v{version}")
    print("   git push origin HEAD")
    print(f"   git push origin v{version}")
    print("3. Create a GitHub Release and upload:")
    print(f"   {zip_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
