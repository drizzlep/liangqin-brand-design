import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class SyncOpenclawMirrorsTest(unittest.TestCase):
    def test_sync_script_rebuilds_openclaw_evaluation_mirrors(self):
        script_path = ROOT / "scripts" / "sync_openclaw_mirrors.py"
        self.assertTrue(script_path.exists(), "sync script missing")

        with tempfile.TemporaryDirectory() as tmp_dir:
            repo_root = Path(tmp_dir) / "repo"
            (repo_root / "scripts").mkdir(parents=True, exist_ok=True)
            shutil.copy2(script_path, repo_root / "scripts" / script_path.name)

            standard_evaluation = repo_root / "evaluation"
            standard_evaluation.mkdir(parents=True, exist_ok=True)
            for filename in [
                "manual-rubric.zh-CN.md",
                "human-review-protocol.zh-CN.md",
                "human-review-test-cases.zh-CN.json",
                "high-risk-regression-cases.zh-CN.json",
            ]:
                shutil.copy2(ROOT / "evaluation" / filename, standard_evaluation / filename)
            standard_examples = standard_evaluation / "examples"
            standard_examples.mkdir(parents=True, exist_ok=True)
            shutil.copy2(
                ROOT / "evaluation" / "examples" / "homepage-golden-sample.zh-CN.json",
                standard_examples / "homepage-golden-sample.zh-CN.json",
            )
            shutil.copy2(
                ROOT / "evaluation" / "examples" / "product-detail-golden-sample.zh-CN.json",
                standard_examples / "product-detail-golden-sample.zh-CN.json",
            )

            standard_assets = repo_root / "assets" / "brand"
            standard_assets.mkdir(parents=True, exist_ok=True)
            shutil.copy2(
                ROOT / "assets" / "brand" / "asset-manifest.zh-CN.json",
                standard_assets / "asset-manifest.zh-CN.json",
            )

            mirror_dir = repo_root / "skills" / "public" / "liangqin-brand-openclaw" / "evaluation"
            mirror_dir.mkdir(parents=True, exist_ok=True)
            (mirror_dir / "manual-rubric.zh-CN.md").write_text("broken", encoding="utf-8")
            (mirror_dir / "human-review-test-cases.zh-CN.json").write_text(
                json.dumps({"cases": [{"id": "wrong"}]}, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            examples_dir = repo_root / "skills" / "public" / "liangqin-brand-openclaw" / "examples"
            examples_dir.mkdir(parents=True, exist_ok=True)
            (examples_dir / "homepage-golden-sample.zh-CN.json").write_text(
                json.dumps({"page_type": "wrong"}, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            protocol_dir = repo_root / "skills" / "public" / "liangqin-brand-openclaw" / "protocols"
            protocol_dir.mkdir(parents=True, exist_ok=True)
            (protocol_dir / "brand-assets.zh-CN.json").write_text("{}", encoding="utf-8")

            result = subprocess.run(
                ["python3", str(repo_root / "scripts" / "sync_openclaw_mirrors.py")],
                cwd=repo_root,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("synced", result.stdout)

            rubric_text = (mirror_dir / "manual-rubric.zh-CN.md").read_text(encoding="utf-8")
            self.assertIn("OpenClaw mirror of: `evaluation/manual-rubric.zh-CN.md`", rubric_text)
            self.assertIn("良禽佳木跨工具生成人工评测清单", rubric_text)

            protocol_text = (mirror_dir / "human-review-protocol.zh-CN.md").read_text(encoding="utf-8")
            self.assertIn(
                "OpenClaw mirror of: `evaluation/human-review-protocol.zh-CN.md`",
                protocol_text,
            )

            root_review_cases = json.loads(
                (standard_evaluation / "human-review-test-cases.zh-CN.json").read_text(encoding="utf-8")
            )
            mirror_review_cases = json.loads(
                (mirror_dir / "human-review-test-cases.zh-CN.json").read_text(encoding="utf-8")
            )
            self.assertEqual(
                mirror_review_cases["source_of_truth"],
                "evaluation/human-review-test-cases.zh-CN.json",
            )
            self.assertEqual(
                mirror_review_cases["mirror_role"],
                "openclaw_adapter_evaluation_mirror",
            )
            self.assertEqual(
                {case["id"] for case in mirror_review_cases["cases"]},
                {case["id"] for case in root_review_cases["cases"]},
            )

            root_regression_cases = json.loads(
                (standard_evaluation / "high-risk-regression-cases.zh-CN.json").read_text(encoding="utf-8")
            )
            mirror_regression_cases = json.loads(
                (mirror_dir / "high-risk-regression-cases.zh-CN.json").read_text(encoding="utf-8")
            )
            self.assertEqual(
                mirror_regression_cases["source_of_truth"],
                "evaluation/high-risk-regression-cases.zh-CN.json",
            )
            self.assertEqual(
                {case["id"] for case in mirror_regression_cases["cases"]},
                {case["id"] for case in root_regression_cases["cases"]},
            )

            root_asset_manifest = json.loads(
                (standard_assets / "asset-manifest.zh-CN.json").read_text(encoding="utf-8")
            )
            mirror_brand_assets = json.loads(
                (protocol_dir / "brand-assets.zh-CN.json").read_text(encoding="utf-8")
            )
            self.assertEqual(
                mirror_brand_assets["source_of_truth"],
                "assets/brand/asset-manifest.zh-CN.json",
            )
            self.assertEqual(
                mirror_brand_assets["mirror_role"],
                "openclaw_adapter_protocol_mirror",
            )
            self.assertEqual(
                mirror_brand_assets["package_role"],
                "openclaw_adapter_brand_assets_protocol_mirror",
            )
            self.assertEqual(
                {asset["id"] for asset in mirror_brand_assets["required_runtime_assets"]},
                {asset["id"] for asset in root_asset_manifest["required_runtime_assets"]},
            )
            self.assertTrue(mirror_brand_assets["delivery_guardrails"]["final_visual_requires_logo_asset"])

            root_homepage_example = json.loads(
                (
                    standard_examples / "homepage-golden-sample.zh-CN.json"
                ).read_text(encoding="utf-8")
            )
            mirrored_homepage_example = json.loads(
                (examples_dir / "homepage-golden-sample.zh-CN.json").read_text(encoding="utf-8")
            )
            root_product_example = json.loads(
                (
                    standard_examples / "product-detail-golden-sample.zh-CN.json"
                ).read_text(encoding="utf-8")
            )
            mirrored_product_example = json.loads(
                (
                    examples_dir / "product-detail-golden-sample.zh-CN.json"
                ).read_text(encoding="utf-8")
            )
            self.assertEqual(mirrored_homepage_example, root_homepage_example)
            self.assertEqual(mirrored_product_example, root_product_example)


if __name__ == "__main__":
    unittest.main()
