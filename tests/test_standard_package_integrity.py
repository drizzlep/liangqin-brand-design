import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "design-standard-package.json"


class StandardPackageIntegrityTest(unittest.TestCase):
    def test_required_root_layers_exist(self):
        required_paths = [
            ROOT / "DESIGN.md",
            ROOT / "CONSUMER-GUIDE.zh-CN.md",
            ROOT / "DESIGN-GOVERNANCE.md",
            ROOT / "EXECUTION-CHECKLIST.md",
            ROOT / "foundation-dna" / "design-dna.zh-CN.json",
            ROOT / "foundation-dna" / "tokens.semantic.json",
            ROOT / "artifact-surfaces",
            ROOT / "design-packs",
            ROOT / "assets" / "brand" / "asset-manifest.zh-CN.json",
            ROOT / "evaluation" / "manual-rubric.zh-CN.md",
            ROOT / "evaluation" / "human-review-protocol.zh-CN.md",
            ROOT / "evaluation" / "human-review-test-cases.zh-CN.json",
            ROOT / "evaluation" / "high-risk-regression-cases.zh-CN.json",
            ROOT / "evaluation" / "examples" / "homepage-golden-sample.zh-CN.json",
            ROOT / "evaluation" / "examples" / "product-detail-golden-sample.zh-CN.json",
            ROOT / "skills" / "public" / "liangqin-brand-openclaw" / "SKILL.md",
        ]

        for path in required_paths:
            self.assertTrue(path.exists(), f"missing standard package path: {path}")

    def test_manifest_entry_points_resolve(self):
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        layers = manifest["package_layers"]

        for layer in layers:
            for entry in layer["entry_points"]:
                if "*" in entry:
                    matches = list(ROOT.glob(entry))
                    self.assertTrue(matches, f"manifest glob has no matches: {entry}")
                else:
                    self.assertTrue((ROOT / entry).exists(), f"manifest entry missing: {entry}")

    def test_consumer_tiers_point_to_real_consumption_surfaces(self):
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        tiers = manifest["consumer_tiers"]

        self.assertEqual(tiers["tier_1"]["reads"], ["DESIGN.md"])

        for entry in tiers["tier_2"]["reads"] + tiers["tier_3"]["reads"]:
            if "*" in entry:
                matches = list(ROOT.glob(entry))
                self.assertTrue(matches, f"tier read glob has no matches: {entry}")
            else:
                self.assertTrue((ROOT / entry).exists(), f"tier read entry missing: {entry}")

    def test_openclaw_mirrors_point_back_to_standard_truth(self):
        brand_assets = json.loads(
            (
                ROOT
                / "skills"
                / "public"
                / "liangqin-brand-openclaw"
                / "protocols"
                / "brand-assets.zh-CN.json"
            ).read_text(encoding="utf-8")
        )
        review_cases = json.loads(
            (
                ROOT
                / "skills"
                / "public"
                / "liangqin-brand-openclaw"
                / "evaluation"
                / "human-review-test-cases.zh-CN.json"
            ).read_text(encoding="utf-8")
        )
        regression_cases = json.loads(
            (
                ROOT
                / "skills"
                / "public"
                / "liangqin-brand-openclaw"
                / "evaluation"
                / "high-risk-regression-cases.zh-CN.json"
            ).read_text(encoding="utf-8")
        )

        self.assertEqual(
            brand_assets["source_of_truth"],
            "assets/brand/asset-manifest.zh-CN.json",
        )
        self.assertEqual(
            review_cases["source_of_truth"],
            "evaluation/human-review-test-cases.zh-CN.json",
        )
        self.assertEqual(
            regression_cases["source_of_truth"],
            "evaluation/high-risk-regression-cases.zh-CN.json",
        )


if __name__ == "__main__":
    unittest.main()
