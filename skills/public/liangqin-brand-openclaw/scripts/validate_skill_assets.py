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


def resolve_standard_path(relative_path: str) -> Path | None:
    for base in [REPO_ROOT, ROOT]:
        candidate = base / relative_path
        if candidate.exists():
            return candidate
    return None


def load_json(relative_path: str):
    path = resolve_path(relative_path)
    if path is None:
        raise FileNotFoundError(relative_path)
    return json.loads(path.read_text(encoding="utf-8"))


def load_standard_json(relative_path: str):
    path = resolve_standard_path(relative_path)
    if path is None:
        raise FileNotFoundError(relative_path)
    return json.loads(path.read_text(encoding="utf-8"))


def load_local_json(relative_path: str):
    path = ROOT / relative_path
    if not path.exists():
        raise FileNotFoundError(relative_path)
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    required_files = [
        "SKILL.md",
        "README.md",
        "protocols/brand-assets.zh-CN.json",
        "protocols/input-contract.zh-CN.json",
        "protocols/homepage-blueprint.schema.zh-CN.json",
        "protocols/product-detail-blueprint.schema.zh-CN.json",
        "protocols/visual-delivery-spec.schema.zh-CN.json",
        "protocols/brand-boundaries.zh-CN.json",
        "recipes/module-recipes.zh-CN.json",
        "examples/homepage-golden-sample.zh-CN.json",
        "examples/product-detail-golden-sample.zh-CN.json",
        "evaluation/manual-rubric.zh-CN.md",
        "evaluation/human-review-protocol.zh-CN.md",
        "evaluation/human-review-test-cases.zh-CN.json",
        "evaluation/high-risk-regression-cases.zh-CN.json",
    ]
    missing = [path for path in required_files if not (ROOT / path).exists()]
    if missing:
        print("missing:", ", ".join(missing))
        return 1

    required_design_context = [
        "DESIGN.md",
        "CONSUMER-GUIDE.zh-CN.md",
        "DESIGN-GOVERNANCE.md",
        "design-standard-package.json",
        "EXECUTION-CHECKLIST.md",
        "foundation-dna/design-dna.zh-CN.json",
        "foundation-dna/tokens.semantic.json",
        "assets/brand/asset-manifest.zh-CN.json",
        "evaluation/manual-rubric.zh-CN.md",
        "evaluation/human-review-protocol.zh-CN.md",
        "evaluation/human-review-test-cases.zh-CN.json",
        "evaluation/examples/homepage-golden-sample.zh-CN.json",
        "evaluation/examples/product-detail-golden-sample.zh-CN.json",
    ]
    missing_design_context = [
        path for path in required_design_context if resolve_standard_path(path) is None
    ]
    if missing_design_context:
        print("missing design context:", ", ".join(missing_design_context))
        return 1

    input_contract = load_json("protocols/input-contract.zh-CN.json")
    if input_contract.get("primary_input") != "brand_brief":
        print("invalid primary_input")
        return 1
    normalization = input_contract.get("request_normalization", {})
    supported_spec_types = normalization.get("supported_spec_types", [])
    if "visual_delivery_spec" not in supported_spec_types:
        print("input-contract missing visual_delivery_spec routing")
        return 1
    delivery_gates = normalization.get("delivery_gates", [])
    if len(delivery_gates) != 7:
        print("input-contract delivery_gates must contain 7 stages")
        return 1
    surface_selection = normalization.get("surface_selection", {})
    if "presentation_deck" not in surface_selection.get("supported_surfaces", []):
        print("input-contract missing presentation_deck surface routing")
        return 1
    fallback_conditions = {
        rule.get("condition")
        for rule in input_contract.get("fallback_rules", [])
        if isinstance(rule, dict)
    }
    if "final_visual_without_logo_asset" not in fallback_conditions:
        print("input-contract missing logo asset stop rule")
        return 1

    design_md_path = resolve_standard_path("DESIGN.md")
    governance_path = resolve_standard_path("DESIGN-GOVERNANCE.md")
    consumer_guide_path = resolve_standard_path("CONSUMER-GUIDE.zh-CN.md")
    checklist_path = resolve_standard_path("EXECUTION-CHECKLIST.md")
    assert design_md_path is not None
    assert governance_path is not None
    assert consumer_guide_path is not None
    assert checklist_path is not None

    design_md_text = design_md_path.read_text(encoding="utf-8")
    if "## 9. Agent Prompt Guide" not in design_md_text:
        print("DESIGN.md missing agent prompt guide")
        return 1
    consumer_guide_text = consumer_guide_path.read_text(encoding="utf-8")
    if "先守住良禽，再适配渠道" not in consumer_guide_text:
        print("CONSUMER-GUIDE.zh-CN.md missing core consumption principle")
        return 1
    if "只允许输出受 `DESIGN.md` 约束的 structured spec" not in consumer_guide_text:
        print("CONSUMER-GUIDE.zh-CN.md missing logo asset degrade rule")
        return 1

    governance_text = governance_path.read_text(encoding="utf-8")
    if "Default input: `DESIGN.md`" not in governance_text:
        print("DESIGN-GOVERNANCE.md missing default input rule")
        return 1
    if "skills/public/liangqin-brand-openclaw/` is an adapter" not in governance_text:
        print("DESIGN-GOVERNANCE.md missing adapter boundary rule")
        return 1

    checklist_text = checklist_path.read_text(encoding="utf-8")
    if "图标是否符合细线、几何、克制的工艺要求" not in checklist_text:
        print("EXECUTION-CHECKLIST.md missing icon quality check")
        return 1

    standard_manifest = load_standard_json("design-standard-package.json")
    tiers = standard_manifest.get("consumer_tiers", {})
    if set(tiers.keys()) != {"tier_1", "tier_2", "tier_3"}:
        print("design-standard-package.json missing consumer tiers")
        return 1
    entry_keywords = standard_manifest.get("entry_keywords", {})
    if entry_keywords.get("recommended") != ["良禽品牌体"]:
        print("design-standard-package.json missing recommended entry keyword")
        return 1
    if entry_keywords.get("compatible") != ["良禽佳木品牌体"]:
        print("design-standard-package.json missing compatible entry keyword")
        return 1
    internal_slugs = standard_manifest.get("internal_slugs", {})
    if internal_slugs.get("openclaw_source_slug") != "liangqin-brand-openclaw":
        print("design-standard-package.json missing openclaw source slug")
        return 1
    if internal_slugs.get("openclaw_distribution_slug") != "liangqin-brand-body":
        print("design-standard-package.json missing openclaw distribution slug")
        return 1
    public_interfaces = set(standard_manifest.get("public_interfaces", []))
    required_interfaces = {
        "DESIGN.md",
        "CONSUMER-GUIDE.zh-CN.md",
        "foundation-dna/design-dna.zh-CN.json",
        "foundation-dna/tokens.semantic.json",
        "artifact-surfaces/*.json",
        "assets/brand/*",
        "EXECUTION-CHECKLIST.md",
        "evaluation/manual-rubric.zh-CN.md",
        "design-standard-package.json",
    }
    if not required_interfaces.issubset(public_interfaces):
        print("design-standard-package.json missing required public interfaces")
        return 1

    semantic_tokens = load_standard_json("foundation-dna/tokens.semantic.json")
    if semantic_tokens.get("token_model") != "semantic_roles":
        print("tokens.semantic.json missing semantic_roles model")
        return 1
    if semantic_tokens.get("color", {}).get("brand_asset") != "#9C7F66":
        print("tokens.semantic.json missing brand asset token")
        return 1

    brand_assets = load_json("protocols/brand-assets.zh-CN.json")
    asset_manifest = load_standard_json("assets/brand/asset-manifest.zh-CN.json")
    if brand_assets.get("source_of_truth") != "assets/brand/asset-manifest.zh-CN.json":
        print("brand assets missing source_of_truth pointer")
        return 1
    if brand_assets.get("mirror_role") != "openclaw_adapter_protocol_mirror":
        print("brand assets missing mirror_role")
        return 1
    if brand_assets.get("consumption_tier") != "tier_2":
        print("brand assets missing tier_2 marker")
        return 1
    if asset_manifest.get("consumption_tier") != "tier_2":
        print("asset manifest missing tier_2 marker")
        return 1
    required_assets = brand_assets.get("required_runtime_assets", [])
    manifest_assets = asset_manifest.get("required_runtime_assets", [])
    if len(required_assets) < 2:
        print("brand assets missing required logo declarations")
        return 1
    if {asset.get("id") for asset in required_assets} != {asset.get("id") for asset in manifest_assets}:
        print("brand assets and asset manifest are out of sync")
        return 1
    for asset in required_assets:
        if asset.get("type") != "logo":
            print("brand assets contain non-logo runtime asset in required set")
            return 1
        asset_path = asset.get("path")
        if not asset_path or resolve_path(asset_path) is None:
            print(f"brand asset missing path: {asset_path}")
            return 1
    guardrails = brand_assets.get("delivery_guardrails", {})
    if not guardrails.get("final_visual_requires_logo_asset"):
        print("brand assets missing final visual logo guardrail")
        return 1
    if not asset_manifest.get("delivery_guardrails", {}).get("final_visual_requires_logo_asset"):
        print("asset manifest missing final visual logo guardrail")
        return 1

    recipes = load_json("recipes/module-recipes.zh-CN.json")
    module_ids = [module["id"] for module in recipes["modules"]]
    if not 6 <= len(module_ids) <= 8:
        print("module count out of range")
        return 1

    homepage_schema = load_json("protocols/homepage-blueprint.schema.zh-CN.json")
    product_schema = load_json("protocols/product-detail-blueprint.schema.zh-CN.json")
    visual_schema = load_json("protocols/visual-delivery-spec.schema.zh-CN.json")
    blueprint_required = {
        "page_type",
        "page_goal",
        "target_audience",
        "delivery_context",
        "narrative_arc",
        "section_order",
        "sections",
        "cta_strategy",
        "brand_constraints",
        "handoff_state",
    }
    if not blueprint_required.issubset(set(homepage_schema.get("required", []))):
        print("homepage schema missing delivery protocol fields")
        return 1
    if not blueprint_required.issubset(set(product_schema.get("required", []))):
        print("product detail schema missing delivery protocol fields")
        return 1
    visual_required = {
        "page_type",
        "delivery_goal",
        "asset_form",
        "delivery_context",
        "information_priority",
        "layout_blocks",
        "visual_system",
        "image_strategy",
        "icon_strategy",
        "surface_contract_summary",
        "asset_readiness",
        "handoff_rules",
        "handoff_state",
    }
    if not visual_required.issubset(set(visual_schema.get("required", []))):
        print("visual delivery schema missing delivery protocol fields")
        return 1

    for example_file in [
        "examples/homepage-golden-sample.zh-CN.json",
        "examples/product-detail-golden-sample.zh-CN.json"
    ]:
        example = load_json(example_file)
        if "delivery_context" not in example or "handoff_state" not in example:
            print(f"{example_file} missing delivery handoff fields")
            return 1
        if example["handoff_state"].get("current_stage") != "structured_spec":
            print(f"{example_file} current_stage must stay structured_spec")
            return 1
        if example["handoff_state"].get("can_render_final") is not False:
            print(f"{example_file} can_render_final must stay false")
            return 1
        unknown = sorted(set(example["section_order"]) - set(module_ids))
        if unknown:
            print(f"{example_file} uses unknown modules: {', '.join(unknown)}")
            return 1

    review_cases = load_standard_json("evaluation/human-review-test-cases.zh-CN.json")
    cases = review_cases.get("cases", [])
    if len(cases) != 4:
        print("human review case count must be 4")
        return 1
    if "工具或 agent" not in review_cases.get("purpose", ""):
        print("root human review cases should stay tool-neutral")
        return 1
    for case in cases:
        if "brand_brief" not in case.get("inputs", {}):
            print(f"{case.get('id', 'unknown')} missing brand_brief")
            return 1

    review_protocol_path = resolve_standard_path("evaluation/human-review-protocol.zh-CN.md")
    assert review_protocol_path is not None
    review_protocol_text = review_protocol_path.read_text(encoding="utf-8")
    if "目标工具或目标 agent" not in review_protocol_text:
        print("root human review protocol should stay tool-neutral")
        return 1

    regression_cases = load_standard_json("evaluation/high-risk-regression-cases.zh-CN.json")
    if not 8 <= len(regression_cases.get("cases", [])) <= 10:
        print("high-risk regression case count must be between 8 and 10")
        return 1
    if "良禽品牌体" in json.dumps(regression_cases, ensure_ascii=False):
        print("root regression cases should stay tool-neutral")
        return 1
    golden_samples_path = resolve_standard_path("evaluation/golden-samples.zh-CN.md")
    assert golden_samples_path is not None
    golden_samples_text = golden_samples_path.read_text(encoding="utf-8")
    if "evaluation/examples/homepage-golden-sample.zh-CN.json" not in golden_samples_text:
        print("root golden samples should point to root-owned homepage example")
        return 1
    if "skills/public/liangqin-brand-openclaw/examples/" in golden_samples_text:
        print("root golden samples should not point back to openclaw examples")
        return 1

    standard_homepage_example = load_standard_json("evaluation/examples/homepage-golden-sample.zh-CN.json")
    standard_product_example = load_standard_json("evaluation/examples/product-detail-golden-sample.zh-CN.json")
    local_homepage_example = load_local_json("examples/homepage-golden-sample.zh-CN.json")
    local_product_example = load_local_json("examples/product-detail-golden-sample.zh-CN.json")
    if standard_homepage_example != local_homepage_example:
        print("local homepage golden sample drifted from root example")
        return 1
    if standard_product_example != local_product_example:
        print("local product detail golden sample drifted from root example")
        return 1

    standard_review_cases_path = resolve_standard_path("evaluation/human-review-test-cases.zh-CN.json")
    local_review_cases_path = ROOT / "evaluation" / "human-review-test-cases.zh-CN.json"
    if standard_review_cases_path is not None and standard_review_cases_path != local_review_cases_path:
        local_review_cases = load_local_json("evaluation/human-review-test-cases.zh-CN.json")
        if local_review_cases.get("source_of_truth") != "evaluation/human-review-test-cases.zh-CN.json":
            print("local human review cases missing source_of_truth")
            return 1
        if local_review_cases.get("mirror_role") != "openclaw_adapter_evaluation_mirror":
            print("local human review cases missing mirror_role")
            return 1
        if {case.get("id") for case in local_review_cases.get("cases", [])} != {
            case.get("id") for case in review_cases.get("cases", [])
        }:
            print("local human review cases drift from standard case ids")
            return 1

    standard_regression_cases_path = resolve_standard_path("evaluation/high-risk-regression-cases.zh-CN.json")
    local_regression_cases_path = ROOT / "evaluation" / "high-risk-regression-cases.zh-CN.json"
    if standard_regression_cases_path is not None and standard_regression_cases_path != local_regression_cases_path:
        local_regression_cases = load_local_json("evaluation/high-risk-regression-cases.zh-CN.json")
        if local_regression_cases.get("source_of_truth") != "evaluation/high-risk-regression-cases.zh-CN.json":
            print("local regression cases missing source_of_truth")
            return 1
        if local_regression_cases.get("mirror_role") != "openclaw_adapter_evaluation_mirror":
            print("local regression cases missing mirror_role")
            return 1
        if {case.get("id") for case in local_regression_cases.get("cases", [])} != {
            case.get("id") for case in regression_cases.get("cases", [])
        }:
            print("local regression cases drift from standard case ids")
            return 1

    standard_rubric_path = resolve_standard_path("evaluation/manual-rubric.zh-CN.md")
    local_rubric_path = ROOT / "evaluation" / "manual-rubric.zh-CN.md"
    if standard_rubric_path is not None and standard_rubric_path != local_rubric_path:
        local_rubric_text = local_rubric_path.read_text(encoding="utf-8")
        if "OpenClaw mirror of: `evaluation/manual-rubric.zh-CN.md`" not in local_rubric_text:
            print("local manual rubric missing mirror note")
            return 1

    standard_protocol_path = resolve_standard_path("evaluation/human-review-protocol.zh-CN.md")
    local_protocol_path = ROOT / "evaluation" / "human-review-protocol.zh-CN.md"
    if standard_protocol_path is not None and standard_protocol_path != local_protocol_path:
        local_protocol_text = local_protocol_path.read_text(encoding="utf-8")
        if "OpenClaw mirror of: `evaluation/human-review-protocol.zh-CN.md`" not in local_protocol_text:
            print("local human review protocol missing mirror note")
            return 1

    print("skill assets valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
