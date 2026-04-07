#!/usr/bin/env python3
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = Path(__file__).resolve().parents[4]


def resolve_path(relative_path: str) -> Path | None:
    for base in [ROOT, REPO_ROOT]:
        candidate = base / relative_path
        if candidate.exists():
            return candidate
    return None


def load_json(relative_path: str):
    path = resolve_path(relative_path)
    if path is None:
        raise FileNotFoundError(relative_path)
    return json.loads(path.read_text(encoding="utf-8"))


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
        "evaluation/manual-rubric.zh-CN.md",
        "evaluation/human-review-protocol.zh-CN.md",
        "evaluation/human-review-test-cases.zh-CN.json",
    ]
    missing = [path for path in required_files if not (ROOT / path).exists()]
    if missing:
        print("missing:", ", ".join(missing))
        return 1

    required_design_context = [
        "DESIGN.md",
        "DESIGN-GOVERNANCE.md",
        "foundation-dna/design-dna.zh-CN.json",
    ]
    missing_design_context = [
        path for path in required_design_context if resolve_path(path) is None
    ]
    if missing_design_context:
        print("missing design context:", ", ".join(missing_design_context))
        return 1

    input_contract = load_json("protocols/input-contract.zh-CN.json")
    if input_contract.get("primary_input") != "brand_brief":
        print("invalid primary_input")
        return 1

    design_md_path = resolve_path("DESIGN.md")
    governance_path = resolve_path("DESIGN-GOVERNANCE.md")
    assert design_md_path is not None
    assert governance_path is not None

    design_md_text = design_md_path.read_text(encoding="utf-8")
    if "## 9. Agent Prompt Guide" not in design_md_text:
        print("DESIGN.md missing agent prompt guide")
        return 1

    governance_text = governance_path.read_text(encoding="utf-8")
    if "Default input: `DESIGN.md`" not in governance_text:
        print("DESIGN-GOVERNANCE.md missing default input rule")
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

    review_cases = load_json("evaluation/human-review-test-cases.zh-CN.json")
    cases = review_cases.get("cases", [])
    if len(cases) != 4:
        print("human review case count must be 4")
        return 1
    for case in cases:
        if "brand_brief" not in case.get("inputs", {}):
            print(f"{case.get('id', 'unknown')} missing brand_brief")
            return 1

    print("skill assets valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
