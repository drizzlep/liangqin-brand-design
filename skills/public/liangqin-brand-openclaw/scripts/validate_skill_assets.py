#!/usr/bin/env python3
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_json(relative_path: str):
    return json.loads((ROOT / relative_path).read_text())


def main() -> int:
    required_files = [
        "SKILL.md",
        "README.md",
        "protocols/input-contract.zh-CN.json",
        "protocols/homepage-blueprint.schema.zh-CN.json",
        "protocols/product-detail-blueprint.schema.zh-CN.json",
        "protocols/brand-boundaries.zh-CN.json",
        "recipes/module-recipes.zh-CN.json",
        "examples/homepage-golden-sample.zh-CN.json",
        "examples/product-detail-golden-sample.zh-CN.json",
        "evaluation/manual-rubric.zh-CN.md"
    ]
    missing = [path for path in required_files if not (ROOT / path).exists()]
    if missing:
        print("missing:", ", ".join(missing))
        return 1

    input_contract = load_json("protocols/input-contract.zh-CN.json")
    if input_contract.get("primary_input") != "brand_brief":
        print("invalid primary_input")
        return 1

    recipes = load_json("recipes/module-recipes.zh-CN.json")
    module_ids = [module["id"] for module in recipes["modules"]]
    if not 6 <= len(module_ids) <= 8:
        print("module count out of range")
        return 1

    for example_file in [
        "examples/homepage-golden-sample.zh-CN.json",
        "examples/product-detail-golden-sample.zh-CN.json"
    ]:
        example = load_json(example_file)
        unknown = sorted(set(example["section_order"]) - set(module_ids))
        if unknown:
            print(f"{example_file} uses unknown modules: {', '.join(unknown)}")
            return 1

    print("skill assets valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
