import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / "skills" / "public" / "liangqin-brand-openclaw"
STANDARD_MANIFEST = ROOT / "design-standard-package.json"
SEMANTIC_TOKENS = ROOT / "foundation-dna" / "tokens.semantic.json"
STANDARD_EVALUATION = ROOT / "evaluation"
STANDARD_EVALUATION_EXAMPLES = STANDARD_EVALUATION / "examples"
ASSET_MANIFEST = ROOT / "assets" / "brand" / "asset-manifest.zh-CN.json"


class LiangqinBrandSkillAssetsTest(unittest.TestCase):
    def test_skill_assets_exist_and_match_contract(self):
        expected_files = {
            "SKILL.md",
            "README.md",
            "skill-release.json",
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
        }
        missing = [
            relative_path
            for relative_path in expected_files
            if not (SKILL_ROOT / relative_path).exists()
        ]
        self.assertFalse(missing, f"missing skill assets: {missing}")

        input_contract = json.loads(
            (SKILL_ROOT / "protocols" / "input-contract.zh-CN.json").read_text()
        )
        release_metadata = json.loads(
            (SKILL_ROOT / "skill-release.json").read_text(encoding="utf-8")
        )
        self.assertEqual(release_metadata["display_name"], "良禽品牌体")
        self.assertEqual(release_metadata["package_slug"], "liangqin-brand-body")
        self.assertEqual(release_metadata["entry_keyword"], "良禽品牌体")
        self.assertEqual(release_metadata["package_role"], "openclaw_adapter_distribution")
        self.assertEqual(release_metadata["standard_manifest"], "design-standard-package.json")
        self.assertEqual(release_metadata["consumption_tier"], "tier_3")
        self.assertIn("foundation-dna/tokens.semantic.json", release_metadata["consumes_layers"])
        self.assertIn("artifact-surfaces/", release_metadata["consumes_layers"])
        self.assertIn("liangqin-brand-openclaw", release_metadata["legacy_keywords"])
        self.assertEqual(input_contract["primary_input"], "brand_brief")
        self.assertEqual(input_contract["skill_name"], "良禽品牌体")
        self.assertCountEqual(
            input_contract["accepted_inputs"].keys(),
            ["brand_brief", "product_data", "reference_pages"],
        )
        self.assertEqual(
            input_contract["request_normalization"]["first_output"],
            "structured_spec_only",
        )
        self.assertIn(
            "visual_delivery_spec",
            input_contract["request_normalization"]["supported_spec_types"],
        )
        self.assertEqual(
            input_contract["request_normalization"]["channel_policy"],
            "channel_adapts_delivery_not_brand",
        )
        self.assertEqual(
            len(input_contract["request_normalization"]["delivery_gates"]),
            7,
        )
        self.assertIn(
            "Context Gate",
            input_contract["request_normalization"]["delivery_gates"][0],
        )
        self.assertIn(
            "presentation_deck",
            input_contract["request_normalization"]["surface_selection"]["supported_surfaces"],
        )
        self.assertIn(
            {
                "condition": "final_visual_without_logo_asset",
                "action": "stop_final_visual_delivery",
                "reason": "未读取到真实 logo 资产时，不允许直接产出页面、图片、长图、卡片等最终视觉成品。"
            },
            input_contract["fallback_rules"],
        )

        brand_assets = json.loads(
            (
                SKILL_ROOT
                / "protocols"
                / "brand-assets.zh-CN.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual(brand_assets["consumption_tier"], "tier_2")
        self.assertTrue(brand_assets["delivery_guardrails"]["final_visual_requires_logo_asset"])
        self.assertEqual(brand_assets["source_of_truth"], "assets/brand/asset-manifest.zh-CN.json")
        self.assertEqual(brand_assets["mirror_role"], "openclaw_adapter_protocol_mirror")
        asset_ids = {asset["id"] for asset in brand_assets["required_runtime_assets"]}
        self.assertEqual(asset_ids, {"logo_horizontal_svg", "logo_vertical_svg"})
        for asset in brand_assets["required_runtime_assets"]:
            self.assertTrue((ROOT / asset["path"]).exists(), f"missing runtime asset {asset['path']}")

        self.assertTrue(STANDARD_EVALUATION.exists(), "root evaluation directory missing")
        self.assertTrue((STANDARD_EVALUATION / "manual-rubric.zh-CN.md").exists())
        self.assertTrue((STANDARD_EVALUATION / "high-risk-regression-cases.zh-CN.json").exists())
        self.assertTrue((STANDARD_EVALUATION / "human-review-protocol.zh-CN.md").exists())
        self.assertTrue((STANDARD_EVALUATION / "human-review-test-cases.zh-CN.json").exists())
        self.assertTrue((STANDARD_EVALUATION_EXAMPLES / "homepage-golden-sample.zh-CN.json").exists())
        self.assertTrue(
            (STANDARD_EVALUATION_EXAMPLES / "product-detail-golden-sample.zh-CN.json").exists()
        )
        self.assertTrue(ASSET_MANIFEST.exists(), "root asset manifest missing")
        root_asset_manifest = json.loads(ASSET_MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(root_asset_manifest["consumption_tier"], "tier_2")
        self.assertEqual(
            {asset["id"] for asset in root_asset_manifest["required_runtime_assets"]},
            asset_ids,
        )
        self.assertTrue(root_asset_manifest["delivery_guardrails"]["final_visual_requires_logo_asset"])
        root_review_cases = json.loads(
            (STANDARD_EVALUATION / "human-review-test-cases.zh-CN.json").read_text(encoding="utf-8")
        )
        self.assertIn("工具或 agent", root_review_cases["purpose"])
        root_regression_cases = json.loads(
            (STANDARD_EVALUATION / "high-risk-regression-cases.zh-CN.json").read_text(encoding="utf-8")
        )
        self.assertNotIn("良禽品牌体", json.dumps(root_regression_cases, ensure_ascii=False))

        homepage_schema = json.loads(
            (SKILL_ROOT / "protocols" / "homepage-blueprint.schema.zh-CN.json").read_text()
        )
        product_schema = json.loads(
            (
                SKILL_ROOT
                / "protocols"
                / "product-detail-blueprint.schema.zh-CN.json"
            ).read_text()
        )
        visual_schema = json.loads(
            (
                SKILL_ROOT
                / "protocols"
                / "visual-delivery-spec.schema.zh-CN.json"
            ).read_text()
        )
        required_fields = {
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
        self.assertTrue(required_fields.issubset(set(homepage_schema["required"])))
        self.assertTrue(required_fields.issubset(set(product_schema["required"])))
        self.assertTrue(
            {
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
            }.issubset(set(visual_schema["required"]))
        )
        self.assertEqual(
            visual_schema["properties"]["page_type"]["const"],
            "visual_delivery_spec",
        )

        recipes = json.loads(
            (SKILL_ROOT / "recipes" / "module-recipes.zh-CN.json").read_text()
        )
        module_ids = [module["id"] for module in recipes["modules"]]
        self.assertGreaterEqual(len(module_ids), 6)
        self.assertLessEqual(len(module_ids), 8)

        homepage_sample = json.loads(
            (SKILL_ROOT / "examples" / "homepage-golden-sample.zh-CN.json").read_text()
        )
        root_homepage_sample = json.loads(
            (STANDARD_EVALUATION_EXAMPLES / "homepage-golden-sample.zh-CN.json").read_text()
        )
        product_sample = json.loads(
            (
                SKILL_ROOT
                / "examples"
                / "product-detail-golden-sample.zh-CN.json"
            ).read_text()
        )
        root_product_sample = json.loads(
            (
                STANDARD_EVALUATION_EXAMPLES
                / "product-detail-golden-sample.zh-CN.json"
            ).read_text()
        )
        self.assertEqual(homepage_sample, root_homepage_sample)
        self.assertEqual(product_sample, root_product_sample)
        for sample in [homepage_sample, product_sample]:
            self.assertIn("delivery_context", sample)
            self.assertIn("handoff_state", sample)
            self.assertIn(
                sample["delivery_context"]["context_status"],
                {"complete", "partial", "blocked"},
            )
            self.assertEqual(sample["handoff_state"]["current_stage"], "structured_spec")
            self.assertFalse(sample["handoff_state"]["can_render_final"])
            self.assertTrue(sample["section_order"])
            self.assertTrue(
                set(sample["section_order"]).issubset(set(module_ids)),
                "sample uses modules outside whitelist",
            )

    def test_default_openclaw_core_is_explicit_and_compact(self):
        skill_md = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        readme_md = (SKILL_ROOT / "README.md").read_text(encoding="utf-8")
        recipes = json.loads(
            (SKILL_ROOT / "recipes" / "module-recipes.zh-CN.json").read_text(encoding="utf-8")
        )
        local_rubric_text = (
            SKILL_ROOT / "evaluation" / "manual-rubric.zh-CN.md"
        ).read_text(encoding="utf-8")
        local_review_protocol_text = (
            SKILL_ROOT / "evaluation" / "human-review-protocol.zh-CN.md"
        ).read_text(encoding="utf-8")

        self.assertIn("默认核心读取层固定为：", skill_md)
        self.assertIn("`良禽品牌体`", skill_md)
        self.assertIn("`design-standard-package.json`", skill_md)
        self.assertIn("`DESIGN.md`", skill_md)
        self.assertIn("`assets/brand/asset-manifest.zh-CN.json`", skill_md)
        self.assertIn("`protocols/brand-boundaries.zh-CN.json`", skill_md)
        self.assertIn("`protocols/brand-assets.zh-CN.json`", skill_md)
        self.assertIn("`recipes/module-recipes.zh-CN.json`", skill_md)
        self.assertIn("`protocols/visual-delivery-spec.schema.zh-CN.json`", skill_md)
        self.assertIn(
            "以下良禽视觉类请求，默认优先进入 `良禽品牌体 / 良禽佳木品牌体`",
            skill_md,
        )
        self.assertIn("不得被报价类 skill 抢走", skill_md)
        self.assertIn("良禽佳木apple风", skill_md)
        self.assertIn("`design-packs/liangqin-apple.json`", skill_md)
        self.assertIn("Default OpenClaw core:", readme_md)
        self.assertIn("OpenClaw 适配器层", readme_md)
        self.assertIn("`design-standard-package.json`", readme_md)
        self.assertIn("`CONSUMER-GUIDE.zh-CN.md`", readme_md)
        self.assertIn("`foundation-dna/tokens.semantic.json`", readme_md)
        self.assertIn("`assets/brand/asset-manifest.zh-CN.json`", readme_md)
        self.assertIn("`protocols/brand-assets.zh-CN.json`", readme_md)
        self.assertIn("`evaluation/examples/`", readme_md)
        self.assertIn("OpenClaw 本地兼容样例", readme_md)
        self.assertIn("不得被报价类 skill 抢走", readme_md)
        self.assertIn("对外推荐触发词：`良禽品牌体`", readme_md)
        self.assertIn("对外兼容触发词：`良禽佳木品牌体`", readme_md)
        self.assertIn("面向**所有渠道**", readme_md)
        self.assertIn("根目录 `evaluation/examples/` 是结构化黄金样例真源", skill_md)
        self.assertIn("根目录 `CONSUMER-GUIDE.zh-CN.md`", skill_md)
        self.assertIn("Root 首页黄金样例", skill_md)
        self.assertIn("OpenClaw mirror of: `evaluation/manual-rubric.zh-CN.md`", local_rubric_text)
        self.assertIn(
            "OpenClaw mirror of: `evaluation/human-review-protocol.zh-CN.md`",
            local_review_protocol_text,
        )
        self.assertTrue(STANDARD_MANIFEST.exists())
        self.assertTrue(SEMANTIC_TOKENS.exists())

        modules_by_id = {module["id"]: module for module in recipes["modules"]}
        expected_core_modules = {
            "brand-hero",
            "material-craft",
            "editorial-story",
            "consultation-promise",
            "consultation-cta",
        }
        self.assertTrue(expected_core_modules.issubset(modules_by_id.keys()))

        for module_id in expected_core_modules:
            module = modules_by_id[module_id]
            self.assertEqual(
                module["supported_pages"],
                ["homepage", "product_detail"],
                f"{module_id} should stay reusable across homepage and product detail",
            )
            for field_name, max_length in [("role", 38), ("tone_rule", 40), ("layout_rule", 44)]:
                self.assertLessEqual(
                    len(module[field_name]),
                    max_length,
                    f"{module_id}.{field_name} should stay compact enough for default AI consumption",
                )
            self.assertGreaterEqual(len(module["forbidden"]), 2)
            self.assertLessEqual(len(module["forbidden"]), 3)

    def test_human_review_cases_cover_core_acceptance_paths(self):
        case_path = (
            SKILL_ROOT
            / "evaluation"
            / "human-review-test-cases.zh-CN.json"
        )
        cases_payload = json.loads(case_path.read_text(encoding="utf-8"))
        self.assertEqual(cases_payload["brand"], "良禽佳木")
        self.assertIn("人类", cases_payload["purpose"])
        self.assertEqual(
            cases_payload["source_of_truth"],
            "evaluation/human-review-test-cases.zh-CN.json",
        )
        self.assertEqual(
            cases_payload["mirror_role"],
            "openclaw_adapter_evaluation_mirror",
        )

        cases = cases_payload["cases"]
        self.assertEqual(len(cases), 4, "expected 4 human review cases in first batch")
        root_cases_payload = json.loads(
            (
                STANDARD_EVALUATION
                / "human-review-test-cases.zh-CN.json"
            ).read_text(encoding="utf-8")
        )

        case_ids = {case["id"] for case in cases}
        self.assertEqual(
            case_ids,
            {
                "homepage-core-fit",
                "homepage-reference-boundary",
                "product-detail-factual",
                "product-detail-missing-data",
            },
        )
        self.assertEqual(
            case_ids,
            {case["id"] for case in root_cases_payload["cases"]},
        )

        page_types = {case["page_type"] for case in cases}
        self.assertEqual(page_types, {"homepage_blueprint", "product_detail_blueprint"})

        for case in cases:
            for field_name in [
                "id",
                "title",
                "page_type",
                "difficulty",
                "pass_signal",
            ]:
                self.assertTrue(str(case[field_name]).strip(), f"{case['id']} missing {field_name}")
            for list_field in ["test_focus", "human_review_checks"]:
                self.assertGreaterEqual(
                    len(case[list_field]),
                    3,
                    f"{case['id']} should provide enough human review prompts",
                )
            self.assertIn("brand_brief", case["inputs"], f"{case['id']} missing brand_brief")

        missing_data_case = next(
            case for case in cases if case["id"] == "product-detail-missing-data"
        )
        product_data = missing_data_case["inputs"]["product_data"]
        self.assertNotIn("dimensions", product_data)
        self.assertNotIn("craft_notes", product_data)

        regression_cases = json.loads(
            (
                SKILL_ROOT
                / "evaluation"
                / "high-risk-regression-cases.zh-CN.json"
            ).read_text(encoding="utf-8")
        )
        root_regression_cases = json.loads(
            (
                STANDARD_EVALUATION
                / "high-risk-regression-cases.zh-CN.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual(
            regression_cases["source_of_truth"],
            "evaluation/high-risk-regression-cases.zh-CN.json",
        )
        self.assertEqual(
            regression_cases["mirror_role"],
            "openclaw_adapter_evaluation_mirror",
        )
        self.assertTrue(8 <= len(regression_cases["cases"]) <= 10)
        regression_ids = {case["id"] for case in regression_cases["cases"]}
        root_regression_ids = {
            case["id"] for case in root_regression_cases["cases"]
        }
        self.assertIn("logo-required-long-image", regression_ids)
        self.assertIn("visual-routing-wins", regression_ids)
        self.assertIn("channel-does-not-switch-style", regression_ids)
        self.assertEqual(regression_ids, root_regression_ids)


if __name__ == "__main__":
    unittest.main()
