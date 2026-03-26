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
            "protocols/input-contract.zh-CN.json",
            "protocols/homepage-blueprint.schema.zh-CN.json",
            "protocols/product-detail-blueprint.schema.zh-CN.json",
            "protocols/brand-boundaries.zh-CN.json",
            "recipes/module-recipes.zh-CN.json",
            "examples/homepage-golden-sample.zh-CN.json",
            "examples/product-detail-golden-sample.zh-CN.json",
            "evaluation/manual-rubric.zh-CN.md",
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
        self.assertEqual(input_contract["primary_input"], "brand_brief")
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


if __name__ == "__main__":
    unittest.main()
