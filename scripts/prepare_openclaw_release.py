#!/usr/bin/env python3
"""Build the OpenClaw release bundle and print the next GitHub release steps."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RELEASE_METADATA = (
    ROOT / "skills" / "public" / "liangqin-brand-openclaw" / "skill-release.json"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Prepare the GitHub release bundle for 良禽品牌体.")
    parser.add_argument(
        "--output-dir",
        default=str(ROOT / "dist"),
        help="Directory used for exported release artifacts.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    metadata = json.loads(RELEASE_METADATA.read_text(encoding="utf-8"))
    package_slug = metadata["package_slug"]
    version = metadata["version"]
    output_dir = Path(args.output_dir).expanduser().resolve()

    command = [
        "python3",
        str(ROOT / "scripts" / "export_openclaw_skill.py"),
        "--output-dir",
        str(output_dir),
        "--zip",
    ]
    result = subprocess.run(command, cwd=ROOT, check=False, text=True, capture_output=True)
    if result.returncode != 0:
        raise SystemExit(
            "release bundle export failed:\n"
            f"stdout:\n{result.stdout}\n"
            f"stderr:\n{result.stderr}"
        )

    zip_path = output_dir / f"{package_slug}-{version}.zip"
    if not zip_path.exists():
        raise SystemExit(f"expected release zip not found: {zip_path}")

    print(f"Prepared release artifact: {zip_path}")
    print("")
    print("Next steps:")
    print("1. Run tests:")
    print(
        "   python3 -m unittest tests/test_liangqin_brand_skill_assets.py "
        "tests/test_liangqin_brand_skill_distribution.py tests/test_design_md_adapter.py -v"
    )
    print("2. Commit your changes:")
    print(f"   git add . && git commit -m 'release: prepare v{version}'")
    print("3. Push branch and tag:")
    print(f"   git tag v{version}")
    print("   git push origin HEAD")
    print(f"   git push origin v{version}")
    print("4. Create a GitHub Release and upload:")
    print(f"   {zip_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
