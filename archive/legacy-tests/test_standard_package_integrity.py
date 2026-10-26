import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "design-standard-package.json"


class StandardPackageIntegrityTest(unittest.TestCase):
    def test_required_root_layers_exist(self):
        required_paths = [
            ROOT / "DESIGN.md",
            ROOT / "AGENT-PREFLIGHT.zh-CN.md",
            ROOT / "CONSUMER-GUIDE.zh-CN.md",
            ROOT / "DESIGN-GOVERNANCE.md",
            ROOT / "EXECUTION-CHECKLIST.md",
            ROOT / "foundation-dna" / "design-dna.zh-CN.json",
            ROOT / "foundation-dna" / "tokens.semantic.json",
            ROOT / "artifact-surfaces",
            ROOT / "design-packs",
            ROOT / "assets" / "brand" / "asset-manifest.zh-CN.json",
            ROOT / "evaluation" / "manual-rubric.zh-CN.md",
            ROOT / "evaluation" / "lightweight-design-md-smoke-prompts.zh-CN.md",
            ROOT / "evaluation" / "lightweight-design-md-smoke-result-2026-04-25.zh-CN.md",
            ROOT / "evaluation" / "lightweight-homepage-direction-spec-2026-04-25.zh-CN.md",
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
        self.assertNotIn("AGENT-PREFLIGHT.zh-CN.md", tiers["tier_2"]["reads"])
        self.assertIn("AGENT-PREFLIGHT.zh-CN.md", tiers["tier_3"]["reads"])
        self.assertIn("CONSUMER-GUIDE.zh-CN.md", tiers["tier_3"]["reads"])

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

    def test_lightweight_design_md_smoke_prompts_cover_core_surfaces(self):
        smoke_path = ROOT / "evaluation" / "lightweight-design-md-smoke-prompts.zh-CN.md"
        smoke_text = smoke_path.read_text(encoding="utf-8")

        self.assertIn("默认输入只给：", smoke_text)
        self.assertIn("- `DESIGN.md`", smoke_text)
        self.assertIn("不要在第一轮同时提供 preflight", smoke_text)
        self.assertIn("## Smoke 1. 品牌首页方向", smoke_text)
        self.assertIn("## Smoke 2. 产品详情页方向", smoke_text)
        self.assertIn("## Smoke 3. 客户长图方向", smoke_text)
        self.assertIn("不编造尺寸、价格、工艺和图片", smoke_text)
        self.assertIn("不输出最终图片", smoke_text)

    def test_lightweight_design_md_smoke_result_records_passed_baseline(self):
        result_path = ROOT / "evaluation" / "lightweight-design-md-smoke-result-2026-04-25.zh-CN.md"
        result_text = result_path.read_text(encoding="utf-8")

        self.assertIn("输入文件：仅使用根目录 `DESIGN.md`", result_text)
        self.assertIn("结论：3 条 smoke 均通过", result_text)
        self.assertIn("品牌首页方向", result_text)
        self.assertIn("产品详情页方向", result_text)
        self.assertIn("客户长图方向", result_text)
        self.assertIn("轻量 `DESIGN.md` 当前可以作为普通 agent 的默认入口", result_text)
        self.assertIn("先不要继续加规则", result_text)

    def test_lightweight_homepage_direction_spec_stays_design_md_only(self):
        spec_path = ROOT / "evaluation" / "lightweight-homepage-direction-spec-2026-04-25.zh-CN.md"
        spec_text = spec_path.read_text(encoding="utf-8")

        self.assertIn("默认只读取：`DESIGN.md`", spec_text)
        self.assertIn("未读取：preflight、consumer guide、design packs、artifact surfaces、assets、evaluation", spec_text)
        self.assertIn("当前阶段：方向 spec，不是最终视觉稿", spec_text)
        self.assertIn("品牌首屏", spec_text)
        self.assertIn("空间与材质引导", spec_text)
        self.assertIn("案例 / 系列浏览", spec_text)
        self.assertIn("预约咨询入口", spec_text)
        self.assertIn("不使用“立即抢购”“马上下单”等强刺激词", spec_text)
        self.assertIn("方向 spec 阶段不需要；最终视觉阶段需要补 assets", spec_text)

    def test_hermes_docs_keep_lightweight_default_input(self):
        consumer_contract = (ROOT / "HERMES-CONSUMER-CONTRACT.zh-CN.md").read_text(encoding="utf-8")
        smoke_playbook = (ROOT / "HERMES-SMOKE-PLAYBOOK.zh-CN.md").read_text(encoding="utf-8")
        smoke_prompts = (ROOT / "HERMES-SMOKE-PROMPTS.zh-CN.md").read_text(encoding="utf-8")
        adapter_memo = (ROOT / "HERMES-ADAPTER-DECISION-MEMO.zh-CN.md").read_text(encoding="utf-8")
        result_template = (ROOT / "HERMES-SMOKE-RESULT-TEMPLATE.zh-CN.md").read_text(encoding="utf-8")

        self.assertIn("Hermes 默认先按轻量 `Tier 1` 方式消费 `DESIGN.md`", consumer_contract)
        self.assertIn("### Hermes 轻量最小输入", consumer_contract)
        self.assertIn("1. `DESIGN.md`", consumer_contract)
        self.assertNotIn("Hermes 默认按 `Tier 3` 目标接入", consumer_contract)

        self.assertIn("Smoke 第一轮只把轻量品牌地图给 Hermes", smoke_playbook)
        self.assertIn("## 2. 轻量输入集", smoke_playbook)
        self.assertIn("preflight 是高保真 / adapter 接入参考，不是普通请求默认必读", smoke_playbook)
        self.assertIn("如果你现在只能读取 DESIGN.md", smoke_playbook)
        self.assertNotIn("DESIGN.md、AGENT-PREFLIGHT", smoke_playbook)

        self.assertIn("假设你现在只能读取下面这些文件：", smoke_prompts)
        self.assertIn("- DESIGN.md", smoke_prompts)
        self.assertNotIn("- AGENT-PREFLIGHT.zh-CN.md", smoke_prompts)
        self.assertNotIn("- CONSUMER-GUIDE.zh-CN.md", smoke_prompts)
        self.assertNotIn("- design-standard-package.json", smoke_prompts)

        self.assertIn("轻量 `DESIGN.md` 默认入口", adapter_memo)
        self.assertIn("preflight 高级参考", adapter_memo)
        self.assertIn("初始轻量输入是否只有 `DESIGN.md`", result_template)


if __name__ == "__main__":
    unittest.main()
