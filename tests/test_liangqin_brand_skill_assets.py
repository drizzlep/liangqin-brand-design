import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / "skills" / "public" / "liangqin-brand-openclaw"


class LiangqinBrandSkillAssetsTest(unittest.TestCase):
    def test_skill_assets_exist_and_match_contract(self):
        expected_files = {
            "SKILL.md",
            "README.md",
            "skill-release.json",
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
        self.assertIn("liangqin-brand-openclaw", release_metadata["legacy_keywords"])
        self.assertEqual(input_contract["primary_input"], "brand_brief")
        self.assertEqual(input_contract["skill_name"], "良禽品牌体")
        self.assertCountEqual(
            input_contract["accepted_inputs"].keys(),
            ["brand_brief", "product_data", "reference_pages"],
        )

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
        required_fields = {
            "page_type",
            "page_goal",
            "target_audience",
            "narrative_arc",
            "section_order",
            "sections",
            "cta_strategy",
            "brand_constraints",
        }
        self.assertTrue(required_fields.issubset(set(homepage_schema["required"])))
        self.assertTrue(required_fields.issubset(set(product_schema["required"])))

        recipes = json.loads(
            (SKILL_ROOT / "recipes" / "module-recipes.zh-CN.json").read_text()
        )
        module_ids = [module["id"] for module in recipes["modules"]]
        self.assertGreaterEqual(len(module_ids), 6)
        self.assertLessEqual(len(module_ids), 8)

        homepage_sample = json.loads(
            (SKILL_ROOT / "examples" / "homepage-golden-sample.zh-CN.json").read_text()
        )
        product_sample = json.loads(
            (
                SKILL_ROOT
                / "examples"
                / "product-detail-golden-sample.zh-CN.json"
            ).read_text()
        )
        for sample in [homepage_sample, product_sample]:
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

        self.assertIn("默认核心读取层固定为：", skill_md)
        self.assertIn("`良禽品牌体`", skill_md)
        self.assertIn("`DESIGN.md`", skill_md)
        self.assertIn("`protocols/brand-boundaries.zh-CN.json`", skill_md)
        self.assertIn("`recipes/module-recipes.zh-CN.json`", skill_md)
        self.assertIn("良禽佳木apple风", skill_md)
        self.assertIn("`design-packs/liangqin-apple.json`", skill_md)
        self.assertIn("Default OpenClaw core:", readme_md)
        self.assertIn("对外唯一入口词：`良禽品牌体`", readme_md)

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

        cases = cases_payload["cases"]
        self.assertEqual(len(cases), 4, "expected 4 human review cases in first batch")

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


if __name__ == "__main__":
    unittest.main()
