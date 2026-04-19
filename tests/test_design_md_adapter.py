import json
import re
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DNA_PATH = ROOT / "foundation-dna" / "design-dna.zh-CN.json"
TOKENS_CSS_PATH = ROOT / "foundation-dna" / "tokens.css"
SEMANTIC_TOKENS_PATH = ROOT / "foundation-dna" / "tokens.semantic.json"
STANDARD_PACKAGE_PATH = ROOT / "design-standard-package.json"
PACKS_DIR = ROOT / "design-packs"
ARTIFACT_SURFACES_DIR = ROOT / "artifact-surfaces"
EVALUATION_DIR = ROOT / "evaluation"
ASSET_MANIFEST_PATH = ROOT / "assets" / "brand" / "asset-manifest.zh-CN.json"

EXPECTED_PACK_SLUGS = {
    "warm-gallery",
    "liangqin-apple",
    "material-editorial",
    "architectural-minimal",
    "quiet-luxury",
    "craft-storytelling",
    "consultation-trust",
    "residence-case",
    "product-spec-premium",
    "service-faq-trust",
}

REQUIRED_PACK_FIELDS = [
    "slug",
    "sort_order",
    "title",
    "summary",
    "preview_variant",
    "mood",
    "density",
    "imagery",
    "cta_tone",
    "zh_readability",
    "best_for_pages",
    "derived_from",
    "governance_role",
    "layout_focus",
    "component_focus",
    "recommended_modules",
    "notes",
    "variation_scope",
    "tweak_axes",
    "locked_axes",
    "preview_tokens",
    "preview_content",
]

REQUIRED_PACK_TOKEN_FIELDS = [
    "background",
    "surface",
    "elevated",
    "accent",
    "line",
    "hero_glow",
    "panel_tint",
    "chip_tint",
]

REQUIRED_PACK_CONTENT_FIELDS = [
    "hero_title",
    "hero_lead",
    "hero_note",
    "primary_cta",
    "secondary_cta",
    "feature_label",
    "feature_body",
    "quote",
]

REQUIRED_PACK_MODULE_FIELDS = [
    "name",
    "purpose",
    "layout_hint",
]

EXPECTED_PACK_GOVERNANCE_ROLE = "controlled_variation_layer"

EXPECTED_ARTIFACT_SLUGS = {
    "web-brand-landing",
    "mobile-h5-consultation",
    "quote-card-editorial",
}

ALLOWED_ARTIFACT_SURFACE_TYPES = {
    "web",
    "mobile_h5",
    "quote_card",
}

REQUIRED_ARTIFACT_FIELDS = [
    "slug",
    "title",
    "surface_type",
    "source_pack",
    "primary_use_case",
    "governance_role",
    "consumption_tier",
    "allowed_adaptations",
    "forbidden_brand_overrides",
    "recommended_modules",
    "layout_rules",
    "failure_modes",
    "canvas_contract",
    "interaction_contract",
    "export_contract",
    "verification_contract",
    "preview_content",
]

REQUIRED_ARTIFACT_CONTENT_FIELDS = [
    "eyebrow",
    "hero_title",
    "hero_lead",
    "page_goal",
    "primary_cta",
    "secondary_cta",
]

REQUIRED_CANVAS_CONTRACT_FIELDS = [
    "format",
    "size_strategy",
    "safe_area",
    "responsive_behavior",
]

REQUIRED_INTERACTION_CONTRACT_FIELDS = [
    "interaction_model",
    "state_persistence",
    "input_methods",
]

REQUIRED_EXPORT_CONTRACT_FIELDS = [
    "primary_formats",
    "handoff_mode",
    "offline_expectation",
]

REQUIRED_VERIFICATION_CONTRACT_FIELDS = [
    "structure_checks",
    "runtime_checks",
    "visual_checks",
    "delivery_checks",
]

EXPECTED_ARTIFACT_GOVERNANCE_ROLE = "artifact_validation_layer"


class DesignMdAdapterTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dna = json.loads(DNA_PATH.read_text(encoding="utf-8"))

    def test_generated_assets_exist_in_repo(self):
        self.assertTrue((ROOT / "DESIGN.md").exists(), "DESIGN.md missing")
        self.assertTrue((ROOT / "DESIGN-GOVERNANCE.md").exists(), "DESIGN-GOVERNANCE.md missing")
        self.assertTrue(STANDARD_PACKAGE_PATH.exists(), "design-standard-package.json missing")
        self.assertTrue(SEMANTIC_TOKENS_PATH.exists(), "tokens.semantic.json missing")
        self.assertTrue(EVALUATION_DIR.exists(), "evaluation directory missing")
        self.assertTrue((EVALUATION_DIR / "manual-rubric.zh-CN.md").exists(), "evaluation manual rubric missing")
        self.assertTrue((EVALUATION_DIR / "human-review-protocol.zh-CN.md").exists(), "evaluation review protocol missing")
        self.assertTrue((EVALUATION_DIR / "human-review-test-cases.zh-CN.json").exists(), "evaluation review cases missing")
        self.assertTrue(ASSET_MANIFEST_PATH.exists(), "asset manifest missing")
        self.assertTrue((ROOT / "design-preview.html").exists(), "design-preview.html missing")
        self.assertTrue((ROOT / "index.html").exists(), "index.html missing")
        for slug in EXPECTED_ARTIFACT_SLUGS:
            self.assertTrue(
                (ROOT / f"artifact-{slug}.html").exists(),
                f"artifact page missing for {slug}",
            )

    def test_standard_package_manifest_is_decision_complete(self):
        manifest = json.loads(STANDARD_PACKAGE_PATH.read_text(encoding="utf-8"))
        self.assertEqual(manifest["package_name"], "良禽跨工具 DESIGN 标准包")
        self.assertEqual(manifest["source_of_truth"], "foundation-dna/design-dna.zh-CN.json")
        self.assertEqual(manifest["brand_content_version"], "2.0.0")
        self.assertEqual(
            manifest["default_conflict_resolution"],
            "Foundation DNA > DESIGN.md > artifact-surfaces > design-packs > examples",
        )
        self.assertEqual(manifest["scope"], "single_brand_first_release")
        self.assertEqual(manifest["entry_keywords"]["recommended"], ["良禽品牌体"])
        self.assertEqual(manifest["entry_keywords"]["compatible"], ["良禽佳木品牌体"])
        self.assertEqual(
            manifest["internal_slugs"]["openclaw_source_slug"],
            "liangqin-brand-openclaw",
        )
        self.assertEqual(
            manifest["internal_slugs"]["openclaw_distribution_slug"],
            "liangqin-brand-body",
        )
        compatible_tools = {
            item["tool"]: item["recommended_tier"]
            for item in manifest["compatible_tools"]
        }
        self.assertEqual(compatible_tools["Google Stitch"], "tier_1")
        self.assertEqual(compatible_tools["OpenClaw"], "tier_3")
        self.assertIn("DESIGN.md", manifest["public_interfaces"])
        self.assertIn("CONSUMER-GUIDE.zh-CN.md", manifest["public_interfaces"])
        self.assertIn("foundation-dna/tokens.semantic.json", manifest["public_interfaces"])
        self.assertIn("artifact-surfaces/*.json", manifest["public_interfaces"])
        self.assertIn("assets/brand/*", manifest["public_interfaces"])
        self.assertIn("evaluation/manual-rubric.zh-CN.md", manifest["public_interfaces"])
        self.assertIn("evaluation/examples/*.json", manifest["public_interfaces"])
        self.assertEqual(len(manifest["governance"]["delivery_gates"]), 7)
        self.assertIn("Context Gate", manifest["governance"]["delivery_gates"][0])
        self.assertIn("reference_policy", manifest["governance"])

        layers = manifest["package_layers"]
        self.assertEqual(len(layers), 7)
        layer_ids = {layer["id"] for layer in layers}
        self.assertEqual(
            layer_ids,
            {
                "foundation_dna",
                "brand_constitution",
                "controlled_variation",
                "delivery_constraints",
                "brand_assets",
                "evaluation",
                "openclaw_adapter",
            },
        )
        layer_entries = {layer["id"]: set(layer["entry_points"]) for layer in layers}
        self.assertIn("assets/brand/asset-manifest.zh-CN.json", layer_entries["brand_assets"])
        self.assertIn("evaluation/manual-rubric.zh-CN.md", layer_entries["evaluation"])
        self.assertIn("evaluation/human-review-protocol.zh-CN.md", layer_entries["evaluation"])
        self.assertIn("evaluation/human-review-test-cases.zh-CN.json", layer_entries["evaluation"])
        self.assertIn("evaluation/examples/*.json", layer_entries["evaluation"])

        tiers = manifest["consumer_tiers"]
        self.assertEqual(set(tiers.keys()), {"tier_1", "tier_2", "tier_3"})
        self.assertEqual(tiers["tier_1"]["reads"], ["DESIGN.md"])
        self.assertIn("artifact-surfaces/*.json", tiers["tier_2"]["reads"])
        self.assertIn("assets/brand/*", tiers["tier_2"]["reads"])
        self.assertIn("foundation-dna/design-dna.zh-CN.json", tiers["tier_3"]["reads"])
        self.assertIn("evaluation/*", tiers["tier_3"]["reads"])

    def test_semantic_tokens_export_matches_foundation_dna(self):
        semantic = json.loads(SEMANTIC_TOKENS_PATH.read_text(encoding="utf-8"))
        colors = self.dna["design_system"]["color"]
        typography = self.dna["design_system"]["typography"]["type_scale"]
        self.assertEqual(semantic["token_model"], "semantic_roles")
        self.assertEqual(semantic["color"]["background"], colors["surface"]["background"])
        self.assertEqual(semantic["color"]["accent"], colors["accent"]["hex"])
        self.assertEqual(semantic["color"]["brand_asset"], colors["brand_asset"]["hex"])
        self.assertEqual(semantic["typography"]["scale"]["display"]["size"], typography["display"]["size"])
        self.assertEqual(semantic["typography"]["scale"]["body"]["line_height"], typography["body"]["line_height"])

    def test_design_packs_exist_and_validate_schema(self):
        self.assertTrue(PACKS_DIR.exists(), "design-packs directory missing")

        pack_paths = sorted(PACKS_DIR.glob("*.json"))
        self.assertGreaterEqual(len(pack_paths), 9, "expected at least 9 design packs")

        found_slugs = set()
        for pack_path in pack_paths:
            pack = json.loads(pack_path.read_text(encoding="utf-8"))
            for field_name in REQUIRED_PACK_FIELDS:
                self.assertIn(field_name, pack, f"{pack_path.name} missing field: {field_name}")

            self.assertIsInstance(pack["sort_order"], int, f"{pack_path.name} sort_order must be int")
            self.assertIsInstance(pack["mood"], list, f"{pack_path.name} mood must be list")
            self.assertTrue(pack["mood"], f"{pack_path.name} mood must not be empty")
            self.assertIsInstance(
                pack["best_for_pages"],
                list,
                f"{pack_path.name} best_for_pages must be list",
            )
            self.assertTrue(
                pack["best_for_pages"],
                f"{pack_path.name} best_for_pages must not be empty",
            )
            self.assertIsInstance(
                pack["component_focus"],
                list,
                f"{pack_path.name} component_focus must be list",
            )
            self.assertTrue(
                pack["component_focus"],
                f"{pack_path.name} component_focus must not be empty",
            )
            self.assertIsInstance(
                pack["recommended_modules"],
                list,
                f"{pack_path.name} recommended_modules must be list",
            )
            self.assertGreaterEqual(
                len(pack["recommended_modules"]),
                3,
                f"{pack_path.name} recommended_modules must contain at least 3 items",
            )

            for field_name in [
                "slug",
                "title",
                "summary",
                "preview_variant",
                "density",
                "imagery",
                "cta_tone",
                "zh_readability",
                "derived_from",
                "governance_role",
                "layout_focus",
                "notes",
            ]:
                self.assertIsInstance(
                    pack[field_name],
                    str,
                    f"{pack_path.name} {field_name} must be string",
                )
                self.assertTrue(
                    pack[field_name].strip(),
                    f"{pack_path.name} {field_name} must not be empty",
                )

            self.assertEqual(
                pack["derived_from"],
                "foundation-dna/design-dna.zh-CN.json",
                f"{pack_path.name} must derive from Foundation DNA",
            )
            self.assertEqual(
                pack["governance_role"],
                EXPECTED_PACK_GOVERNANCE_ROLE,
                f"{pack_path.name} must be marked as controlled variation layer",
            )

            self.assertIsInstance(
                pack["preview_tokens"],
                dict,
                f"{pack_path.name} preview_tokens must be object",
            )
            self.assertIsInstance(
                pack["preview_content"],
                dict,
                f"{pack_path.name} preview_content must be object",
            )
            self.assertIsInstance(
                pack["variation_scope"],
                list,
                f"{pack_path.name} variation_scope must be list",
            )
            self.assertGreaterEqual(
                len(pack["variation_scope"]),
                2,
                f"{pack_path.name} variation_scope must contain at least 2 items",
            )
            for list_name in ["tweak_axes", "locked_axes"]:
                self.assertIsInstance(
                    pack[list_name],
                    list,
                    f"{pack_path.name} {list_name} must be list",
                )
                self.assertGreaterEqual(
                    len(pack[list_name]),
                    2,
                    f"{pack_path.name} {list_name} must contain at least 2 items",
                )
                for index, item in enumerate(pack[list_name]):
                    self.assertIsInstance(
                        item,
                        str,
                        f"{pack_path.name} {list_name}[{index}] must be string",
                    )
                    self.assertTrue(
                        item.strip(),
                        f"{pack_path.name} {list_name}[{index}] must not be empty",
                    )

            for index, scope_item in enumerate(pack["variation_scope"]):
                self.assertIsInstance(
                    scope_item,
                    str,
                    f"{pack_path.name} variation_scope[{index}] must be string",
                )
                self.assertTrue(
                    scope_item.strip(),
                    f"{pack_path.name} variation_scope[{index}] must not be empty",
                )

            for field_name in REQUIRED_PACK_TOKEN_FIELDS:
                self.assertIn(
                    field_name,
                    pack["preview_tokens"],
                    f"{pack_path.name} preview_tokens missing {field_name}",
                )
                self.assertTrue(
                    str(pack["preview_tokens"][field_name]).strip(),
                    f"{pack_path.name} preview_tokens.{field_name} must not be empty",
                )

            for field_name in REQUIRED_PACK_CONTENT_FIELDS:
                self.assertIn(
                    field_name,
                    pack["preview_content"],
                    f"{pack_path.name} preview_content missing {field_name}",
                )
                self.assertTrue(
                    str(pack["preview_content"][field_name]).strip(),
                    f"{pack_path.name} preview_content.{field_name} must not be empty",
                )

            for index, module in enumerate(pack["recommended_modules"]):
                self.assertIsInstance(
                    module,
                    dict,
                    f"{pack_path.name} recommended_modules[{index}] must be object",
                )
                for field_name in REQUIRED_PACK_MODULE_FIELDS:
                    self.assertIn(
                        field_name,
                        module,
                        f"{pack_path.name} recommended_modules[{index}] missing {field_name}",
                    )
                    self.assertTrue(
                        str(module[field_name]).strip(),
                        f"{pack_path.name} recommended_modules[{index}].{field_name} must not be empty",
                    )

            found_slugs.add(pack["slug"])

        self.assertTrue(
            EXPECTED_PACK_SLUGS.issubset(found_slugs),
            "missing one or more expected design pack slugs",
        )

    def test_liangqin_apple_pack_extracts_apple_signals(self):
        apple_pack = json.loads(
            (PACKS_DIR / "liangqin-apple.json").read_text(encoding="utf-8")
        )

        self.assertEqual(apple_pack["title"], "良禽佳木apple风")
        self.assertIn("无衬线", apple_pack["summary"])
        self.assertIn("整屏舞台", apple_pack["layout_focus"])
        self.assertIn("Apple 式无衬线排版", " ".join(apple_pack["variation_scope"]))
        self.assertIn("近单色结构色", apple_pack["notes"])
        self.assertEqual(apple_pack["preview_tokens"]["accent"], "#0071E3")

    def test_artifact_surfaces_exist_and_validate_schema(self):
        self.assertTrue(ARTIFACT_SURFACES_DIR.exists(), "artifact-surfaces directory missing")

        surface_paths = sorted(ARTIFACT_SURFACES_DIR.glob("*.json"))
        self.assertEqual(len(surface_paths), 3, "expected exactly 3 artifact surfaces in phase 2")

        found_slugs = set()
        for surface_path in surface_paths:
            surface = json.loads(surface_path.read_text(encoding="utf-8"))
            for field_name in REQUIRED_ARTIFACT_FIELDS:
                self.assertIn(field_name, surface, f"{surface_path.name} missing field: {field_name}")

            for field_name in [
                "slug",
                "title",
                "surface_type",
                "source_pack",
                "primary_use_case",
                "governance_role",
            ]:
                self.assertIsInstance(
                    surface[field_name],
                    str,
                    f"{surface_path.name} {field_name} must be string",
                )
                self.assertTrue(
                    surface[field_name].strip(),
                    f"{surface_path.name} {field_name} must not be empty",
                )

            self.assertEqual(
                surface["governance_role"],
                EXPECTED_ARTIFACT_GOVERNANCE_ROLE,
                f"{surface_path.name} must be marked as artifact validation layer",
            )
            self.assertEqual(
                surface["consumption_tier"],
                "tier_2",
                f"{surface_path.name} must be marked as tier_2 surface",
            )

            self.assertIn(
                surface["surface_type"],
                ALLOWED_ARTIFACT_SURFACE_TYPES,
                f"{surface_path.name} has unsupported surface_type",
            )
            self.assertIn(
                surface["source_pack"],
                EXPECTED_PACK_SLUGS,
                f"{surface_path.name} must reference an existing pack slug",
            )
            self.assertIsInstance(
                surface["recommended_modules"],
                list,
                f"{surface_path.name} recommended_modules must be list",
            )
            self.assertGreaterEqual(
                len(surface["recommended_modules"]),
                3,
                f"{surface_path.name} recommended_modules must contain at least 3 items",
            )
            self.assertIsInstance(
                surface["layout_rules"],
                list,
                f"{surface_path.name} layout_rules must be list",
            )
            self.assertGreaterEqual(
                len(surface["layout_rules"]),
                1,
                f"{surface_path.name} layout_rules must not be empty",
            )
            self.assertIsInstance(
                surface["failure_modes"],
                list,
                f"{surface_path.name} failure_modes must be list",
            )
            self.assertGreaterEqual(
                len(surface["failure_modes"]),
                2,
                f"{surface_path.name} failure_modes must contain at least 2 items",
            )
            self.assertIsInstance(
                surface["allowed_adaptations"],
                list,
                f"{surface_path.name} allowed_adaptations must be list",
            )
            self.assertGreaterEqual(
                len(surface["allowed_adaptations"]),
                2,
                f"{surface_path.name} allowed_adaptations must contain at least 2 items",
            )
            self.assertIsInstance(
                surface["forbidden_brand_overrides"],
                list,
                f"{surface_path.name} forbidden_brand_overrides must be list",
            )
            self.assertGreaterEqual(
                len(surface["forbidden_brand_overrides"]),
                2,
                f"{surface_path.name} forbidden_brand_overrides must contain at least 2 items",
            )

            for index, module in enumerate(surface["recommended_modules"]):
                self.assertIsInstance(
                    module,
                    dict,
                    f"{surface_path.name} recommended_modules[{index}] must be object",
                )
                for field_name in REQUIRED_PACK_MODULE_FIELDS:
                    self.assertIn(
                        field_name,
                        module,
                        f"{surface_path.name} recommended_modules[{index}] missing {field_name}",
                    )
                    self.assertTrue(
                        str(module[field_name]).strip(),
                        f"{surface_path.name} recommended_modules[{index}].{field_name} must not be empty",
                    )

            for index, rule in enumerate(surface["layout_rules"]):
                self.assertIsInstance(
                    rule,
                    str,
                    f"{surface_path.name} layout_rules[{index}] must be string",
                )
                self.assertTrue(
                    rule.strip(),
                    f"{surface_path.name} layout_rules[{index}] must not be empty",
                )
            for index, failure_mode in enumerate(surface["failure_modes"]):
                self.assertIsInstance(
                    failure_mode,
                    str,
                    f"{surface_path.name} failure_modes[{index}] must be string",
                )
                self.assertTrue(
                    failure_mode.strip(),
                    f"{surface_path.name} failure_modes[{index}] must not be empty",
                )

            contract_specs = {
                "canvas_contract": REQUIRED_CANVAS_CONTRACT_FIELDS,
                "interaction_contract": REQUIRED_INTERACTION_CONTRACT_FIELDS,
                "export_contract": REQUIRED_EXPORT_CONTRACT_FIELDS,
                "verification_contract": REQUIRED_VERIFICATION_CONTRACT_FIELDS,
            }
            for contract_name, required_fields in contract_specs.items():
                self.assertIsInstance(
                    surface[contract_name],
                    dict,
                    f"{surface_path.name} {contract_name} must be object",
                )
                for field_name in required_fields:
                    self.assertIn(
                        field_name,
                        surface[contract_name],
                        f"{surface_path.name} {contract_name} missing {field_name}",
                    )
                    field_value = surface[contract_name][field_name]
                    if isinstance(field_value, list):
                        self.assertTrue(
                            field_value,
                            f"{surface_path.name} {contract_name}.{field_name} must not be empty",
                        )
                        for index, item in enumerate(field_value):
                            self.assertIsInstance(
                                item,
                                str,
                                f"{surface_path.name} {contract_name}.{field_name}[{index}] must be string",
                            )
                            self.assertTrue(
                                item.strip(),
                                f"{surface_path.name} {contract_name}.{field_name}[{index}] must not be empty",
                            )
                    else:
                        self.assertIsInstance(
                            field_value,
                            str,
                            f"{surface_path.name} {contract_name}.{field_name} must be string or list",
                        )
                        self.assertTrue(
                            field_value.strip(),
                            f"{surface_path.name} {contract_name}.{field_name} must not be empty",
                        )

            self.assertIsInstance(
                surface["preview_content"],
                dict,
                f"{surface_path.name} preview_content must be object",
            )
            for field_name in REQUIRED_ARTIFACT_CONTENT_FIELDS:
                self.assertIn(
                    field_name,
                    surface["preview_content"],
                    f"{surface_path.name} preview_content missing {field_name}",
                )
                self.assertTrue(
                    str(surface["preview_content"][field_name]).strip(),
                    f"{surface_path.name} preview_content.{field_name} must not be empty",
                )

            if surface["surface_type"] == "quote_card":
                self.assertIn("quote_samples", surface, f"{surface_path.name} missing quote_samples")
                self.assertIsInstance(
                    surface["quote_samples"],
                    list,
                    f"{surface_path.name} quote_samples must be list",
                )
                self.assertGreaterEqual(
                    len(surface["quote_samples"]),
                    3,
                    f"{surface_path.name} quote_samples must contain at least 3 items",
                )
                first_sample = surface["quote_samples"][0]
                for field_name in [
                    "quote_type",
                    "badge",
                    "product_name",
                    "total_price",
                    "scenario",
                    "sections",
                ]:
                    self.assertIn(field_name, first_sample, f"{surface_path.name} quote sample missing {field_name}")
                self.assertTrue(first_sample["sections"])

            found_slugs.add(surface["slug"])

        self.assertEqual(found_slugs, EXPECTED_ARTIFACT_SLUGS)

    def test_export_script_generates_design_md_and_preview(self):
        script_path = ROOT / "scripts" / "export_design_md.py"
        self.assertTrue(script_path.exists(), "export_design_md.py missing")

        with tempfile.TemporaryDirectory() as tmp_dir:
            result = subprocess.run(
                [
                    "python3",
                    str(script_path),
                    "--output-dir",
                    tmp_dir,
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(
                result.returncode,
                0,
                f"export failed: stdout={result.stdout}\nstderr={result.stderr}",
            )

            output_root = Path(tmp_dir)
            design_md = output_root / "DESIGN.md"
            governance_md = output_root / "DESIGN-GOVERNANCE.md"
            standard_manifest = output_root / "design-standard-package.json"
            exported_dna = output_root / "foundation-dna" / "design-dna.zh-CN.json"
            exported_semantic_tokens = output_root / "foundation-dna" / "tokens.semantic.json"
            exported_artifact_surfaces = output_root / "artifact-surfaces"
            exported_evaluation = output_root / "evaluation"
            exported_asset_manifest = output_root / "assets" / "brand" / "asset-manifest.zh-CN.json"
            preview_html = output_root / "design-preview.html"
            index_html = output_root / "index.html"
            self.assertTrue(design_md.exists(), "generated DESIGN.md missing")
            self.assertTrue(
                (output_root / "CONSUMER-GUIDE.zh-CN.md").exists(),
                "generated CONSUMER-GUIDE.zh-CN.md missing",
            )
            self.assertTrue(governance_md.exists(), "generated DESIGN-GOVERNANCE.md missing")
            self.assertTrue(standard_manifest.exists(), "generated design-standard-package.json missing")
            self.assertTrue(exported_dna.exists(), "generated design DNA missing")
            self.assertTrue(exported_semantic_tokens.exists(), "generated semantic tokens missing")
            self.assertTrue(exported_artifact_surfaces.exists(), "generated artifact-surfaces missing")
            self.assertTrue(exported_evaluation.exists(), "generated evaluation missing")
            self.assertTrue(exported_asset_manifest.exists(), "generated asset manifest missing")
            self.assertTrue(preview_html.exists(), "generated design-preview.html missing")
            self.assertTrue(index_html.exists(), "generated index.html missing")
            artifact_pages = {
                slug: output_root / f"artifact-{slug}.html"
                for slug in EXPECTED_ARTIFACT_SLUGS
            }
            for slug, artifact_path in artifact_pages.items():
                self.assertTrue(artifact_path.exists(), f"generated artifact page missing for {slug}")

            design_md_text = design_md.read_text(encoding="utf-8")
            governance_md_text = governance_md.read_text(encoding="utf-8")
            standard_manifest_text = standard_manifest.read_text(encoding="utf-8")
            preview_html_text = preview_html.read_text(encoding="utf-8")
            index_html_text = index_html.read_text(encoding="utf-8")

            expected_headings = [
                "## 1. Visual Theme & Atmosphere",
                "## 2. Color Palette & Roles",
                "## 3. Typography Rules",
                "## 4. Component Stylings",
                "## 5. Layout Principles",
                "## 6. Depth & Elevation",
                "## 7. Do's and Don'ts",
                "## 8. Responsive Behavior",
                "## 9. Agent Prompt Guide",
            ]
            for heading in expected_headings:
                self.assertIn(heading, design_md_text)

            self.assertIn(
                self.dna["design_system"]["color"]["surface"]["background"],
                design_md_text,
            )
            self.assertIn(self.dna["design_system"]["color"]["accent"]["hex"], design_md_text)
            self.assertIn("Swei Sugar", design_md_text)
            self.assertIn("OPPO Sans 4.0", design_md_text)
            self.assertIn(
                self.dna["design_system"]["typography"]["type_scale"]["display"]["size"],
                design_md_text,
            )
            self.assertIn("品牌不可妥协项：", design_md_text)
            self.assertIn("Prompt checklist:", design_md_text)
            self.assertIn("Suggested prompt:", design_md_text)
            self.assertNotIn("Governance role", design_md_text)
            self.assertNotIn("默认 AI 工作流：", design_md_text)
            self.assertNotIn("artifact-surfaces", design_md_text)
            self.assertNotIn("design-packs", design_md_text)
            self.assertNotIn("examples / real cases", design_md_text)
            self.assertLessEqual(
                len(design_md_text.splitlines()),
                190,
                "DESIGN.md should stay compact enough to remain the default AI input",
            )

            self.assertIn("# DESIGN Governance", governance_md_text)
            self.assertIn("## Protocol", governance_md_text)
            self.assertIn("Default input: `DESIGN.md`", governance_md_text)
            self.assertIn(
                "Read `design-packs/*.json` only when style variation is needed",
                governance_md_text,
            )
            self.assertIn(
                "Read `artifact-surfaces/*.json` only when a concrete artifact is needed",
                governance_md_text,
            )
            self.assertIn("## Conflict Resolution", governance_md_text)
            self.assertIn(
                "Foundation DNA > DESIGN.md > artifact-surfaces > design-packs > examples",
                governance_md_text,
            )
            self.assertIn("## Delivery Gates", governance_md_text)
            self.assertIn("Context Gate", governance_md_text)
            self.assertIn("Surface Gate", governance_md_text)
            self.assertIn("Runtime Gate", governance_md_text)
            self.assertIn("## Change Map", governance_md_text)
            self.assertNotIn("## 1. Layer Roles", governance_md_text)
            self.assertNotIn("## 2. 默认 AI 读取顺序", governance_md_text)
            self.assertIn("\"package_name\": \"良禽跨工具 DESIGN 标准包\"", standard_manifest_text)
            self.assertIn("\"tier_3\"", standard_manifest_text)
            self.assertTrue(
                (exported_artifact_surfaces / "web-brand-landing.json").exists(),
                "generated raw artifact surface missing",
            )
            self.assertTrue(
                (exported_evaluation / "high-risk-regression-cases.zh-CN.json").exists(),
                "generated evaluation regression cases missing",
            )
            self.assertTrue(
                (exported_evaluation / "human-review-protocol.zh-CN.md").exists(),
                "generated evaluation review protocol missing",
            )
            self.assertTrue(
                (exported_evaluation / "human-review-test-cases.zh-CN.json").exists(),
                "generated evaluation review cases missing",
            )

            self.assertIn("Brand Surface Preview", preview_html_text)
            self.assertIn('data-pack-tab="liangqin-apple"', preview_html_text)
            quote_artifact_html = artifact_pages["quote-card-editorial"].read_text(encoding="utf-8")
            self.assertIn("真实报价样例", quote_artifact_html)
            self.assertIn("主卧通顶衣柜", quote_artifact_html)
            self.assertIn("39,529 元", quote_artifact_html)
            self.assertIn("儿童房半高床组合", quote_artifact_html)
            self.assertIn("约 24,800 元", quote_artifact_html)
            self.assertNotIn("把图文报价体从案例页升级成正式载体样例", quote_artifact_html)
            self.assertIn("Artifact Surfaces", preview_html_text)
            self.assertIn("Style Directions", preview_html_text)
            self.assertIn("当前风格方向", preview_html_text)
            self.assertIn("[hidden]", preview_html_text)
            self.assertIn('data-pack-tab="warm-gallery"', preview_html_text)
            self.assertIn('id="style-direction-note"', preview_html_text)
            self.assertIn("preview_markup", preview_html_text)
            self.assertIn("preview-layout-gallery", preview_html_text)
            self.assertIn("preview-layout-editorial", preview_html_text)
            self.assertIn("preview-layout-analytical", preview_html_text)
            self.assertNotIn("推荐模块栈", preview_html_text)
            self.assertIn("网页样例", preview_html_text)
            self.assertIn("手机 H5", preview_html_text)
            self.assertIn("图文报价体", preview_html_text)
            self.assertIn("先看最终成品，再回头看风格方向", preview_html_text)
            self.assertIn("适合场景", preview_html_text)
            self.assertIn("版式气质", preview_html_text)
            self.assertIn("行动语气", preview_html_text)
            self.assertNotIn("AI Governance", preview_html_text)
            self.assertNotIn("默认读取顺序", preview_html_text)
            self.assertIn("/artifact-web-brand-landing", preview_html_text)
            self.assertIn("/artifact-mobile-h5-consultation", preview_html_text)
            self.assertIn("/artifact-quote-card-editorial", preview_html_text)
            self.assertIn(self.dna["design_system"]["color"]["accent"]["hex"], preview_html_text)
            for pack_slug in {"warm-gallery", "consultation-trust", "product-spec-premium"}:
                self.assertIn(pack_slug, preview_html_text)
            for pack_slug in {"material-editorial", "quiet-luxury", "residence-case"}:
                self.assertNotIn(f'data-pack-tab="{pack_slug}"', preview_html_text)

            self.assertEqual(
                index_html_text,
                preview_html_text,
                "generated index.html should mirror design-preview.html",
            )

            web_html = artifact_pages["web-brand-landing"].read_text(encoding="utf-8")
            mobile_html = artifact_pages["mobile-h5-consultation"].read_text(encoding="utf-8")
            quote_html = artifact_pages["quote-card-editorial"].read_text(encoding="utf-8")

            self.assertIn("网页样例", web_html)
            self.assertIn("沉浸 Hero", web_html)
            self.assertIn("系列导览带", web_html)
            self.assertIn("案例精选区", web_html)
            self.assertIn("易失真点", web_html)

            self.assertIn("手机 H5", mobile_html)
            self.assertIn("服务边界说明", mobile_html)
            self.assertIn("流程步骤", mobile_html)
            self.assertIn("FAQ 列表", mobile_html)
            self.assertIn("易失真点", mobile_html)

            self.assertIn("图文报价体", quote_html)
            self.assertIn("报价类型标识", quote_html)
            self.assertIn("总价结论区", quote_html)
            self.assertIn("依据说明区", quote_html)
            self.assertIn("易失真点", quote_html)
            self.assertIn("#quote-samples", quote_html)
            self.assertIn("真实报价样例", quote_html)
            self.assertIn("主卧通顶衣柜", quote_html)
            self.assertIn("39,529 元", quote_html)

    def test_tokens_css_matches_foundation_dna_core_tokens(self):
        css_text = TOKENS_CSS_PATH.read_text(encoding="utf-8")
        typography = self.dna["design_system"]["typography"]["type_scale"]
        colors = self.dna["design_system"]["color"]
        shape = self.dna["design_system"]["shape"]["border_radius"]
        elevation = self.dna["design_system"]["elevation"]["levels"]

        expected_tokens = {
            "--dna-color-bg": colors["surface"]["background"],
            "--dna-color-surface": colors["surface"]["card"],
            "--dna-color-surface-elevated": colors["surface"]["elevated"],
            "--dna-color-ink-900": colors["neutral"]["scale"]["900"],
            "--dna-color-ink-800": colors["primary"]["hex"],
            "--dna-color-line": colors["neutral"]["scale"]["200"],
            "--dna-color-accent": colors["accent"]["hex"],
            "--dna-size-display": typography["display"]["size"],
            "--dna-size-h1": typography["heading_1"]["size"],
            "--dna-size-h2": typography["heading_2"]["size"],
            "--dna-size-h3": typography["heading_3"]["size"],
            "--dna-size-body": typography["body"]["size"],
            "--dna-line-display": typography["display"]["line_height"],
            "--dna-line-h1": typography["heading_1"]["line_height"],
            "--dna-line-h2": typography["heading_2"]["line_height"],
            "--dna-line-h3": typography["heading_3"]["line_height"],
            "--dna-line-body": typography["body"]["line_height"],
            "--dna-tracking-display": typography["display"]["tracking"],
            "--dna-tracking-h1": typography["heading_1"]["tracking"],
            "--dna-tracking-h2": typography["heading_2"]["tracking"],
            "--dna-tracking-h3": typography["heading_3"]["tracking"],
            "--dna-tracking-body": typography["body"]["tracking"],
            "--dna-radius-sm": shape["small"],
            "--dna-radius-md": shape["medium"],
            "--dna-radius-lg": shape["large"],
            "--dna-radius-pill": shape["pill"],
            "--dna-shadow-low": elevation["low"],
            "--dna-shadow-medium": elevation["medium"],
            "--dna-shadow-high": elevation["high"],
        }

        for token_name, expected_value in expected_tokens.items():
            match = re.search(
                rf"{re.escape(token_name)}:\s*([^;]+);",
                css_text,
            )
            self.assertIsNotNone(match, f"missing token in CSS: {token_name}")
            self.assertEqual(
                match.group(1).strip(),
                expected_value,
                f"token drift detected for {token_name}",
            )


if __name__ == "__main__":
    unittest.main()
