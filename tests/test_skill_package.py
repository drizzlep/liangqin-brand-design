"""技能入口合规性、发行包结构与仓库卫生检查。"""

import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "public" / "liangqin-brand-body"
PACKAGE_NAME = "liangqin-brand-body"


def load_build_script():
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "liangqin_build_skill", ROOT / "scripts" / "build_skill.py"
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


build_skill = load_build_script()


class SkillEntryTest(unittest.TestCase):
    def setUp(self):
        self.path = SKILL_DIR / "SKILL.md"
        self.fields, _ = build_skill.parse_frontmatter(self.path)
        self.text = self.path.read_text(encoding="utf-8")

    def test_name_matches_directory_and_spec(self):
        name = str(self.fields["name"])
        self.assertEqual(name, PACKAGE_NAME)
        self.assertEqual(SKILL_DIR.name, name)
        self.assertRegex(name, r"^[a-z0-9]+(-[a-z0-9]+)*$")

    def test_description_within_limit_and_bilingual(self):
        description = str(self.fields["description"])
        self.assertLessEqual(len(description), 1024)
        self.assertIn("良禽佳木", description)
        self.assertIn("Liangqin", description)

    def test_metadata_values_are_strings(self):
        for key, value in self.fields["metadata"].items():
            self.assertIsInstance(value, str, f"metadata.{key} 不是字符串")

    def test_entry_has_no_legacy_runtime_language(self):
        self.assertIsNone(re.search(r"openclaw|hermes", self.text, re.IGNORECASE))

    def test_entry_points_to_current_structure(self):
        self.assertIn("`DESIGN.md`（唯一默认必读）", self.text)
        self.assertIn("tokens/tokens.css", self.text)
        self.assertNotIn("foundation-dna", self.text)
        self.assertNotIn("examples/", self.text)


class PackageBuildTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.output = Path(cls.tmp.name) / PACKAGE_NAME
        result = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "build_skill.py"),
                "--output-dir",
                str(cls.output),
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == 0, f"构建失败：{result.stdout}\n{result.stderr}"

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_package_contains_standard_and_entry(self):
        for relative in [
            "SKILL.md",
            "DESIGN.md",
            "preview.html",
            "skill-release.json",
            "adapters/README.zh-CN.md",
            "kit/kit.css",
            "kit/index.html",
            "kit/templates/homepage.html",
            "kit/templates/product-detail.html",
            "kit/templates/README.zh-CN.md",
            "tokens/tokens.css",
            "tokens/tokens.semantic.json",
            "scripts/check_page.py",
            "assets/brand/liangqinjiamu-logo-horizontal.svg",
            "assets/brand/asset-manifest.zh-CN.json",
            "assets/fonts/OPPO-Sans-4.0.woff2",
        ]:
            self.assertTrue((self.output / relative).exists(), f"发行包缺少 {relative}")

    def test_package_ships_no_examples_or_legacy_layers(self):
        self.assertFalse((self.output / "examples").exists(), "发行包不应再带示例目录")

    def test_entry_documents_kit_workflow(self):
        text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        for marker in ["kit/kit.css", "check_page.py", ".lq-*", "kit/templates/homepage.html"]:
            self.assertIn(marker, text, f"SKILL.md 缺少 {marker}")

    def test_templates_use_kit_classes_and_keep_placeholders(self):
        kit = (ROOT / "kit" / "kit.css").read_text(encoding="utf-8")
        for name in ["homepage.html", "product-detail.html"]:
            text = (ROOT / "kit" / "templates" / name).read_text(encoding="utf-8")
            self.assertIn('href="../kit.css"', text, f"{name} 没有引入 kit.css")
            classes = set(re.findall(r'class="([^"]+)"', text))
            used = {c for group in classes for c in group.split()}
            lq_classes = {c for c in used if c.startswith("lq-")}
            self.assertGreaterEqual(len(lq_classes), 10, f"{name} 用的 kit 类太少")
            self.assertIn("待确认", text, f"{name} 缺少占位标记")
            missing = sorted(
                cls for cls in lq_classes if f".{cls}" not in kit and f".{cls}" not in text
            )
            self.assertEqual(missing, [], f"{name} 用了未定义的类：{missing}")

    def test_every_referenced_icon_exists(self):
        icons_dir = ROOT / "kit" / "icons"
        self.assertTrue((icons_dir / "LICENSE.txt").exists(), "缺少图标许可文件")
        for page in ["index.html", "templates/homepage.html", "templates/product-detail.html"]:
            text = (ROOT / "kit" / page).read_text(encoding="utf-8")
            referenced = set(re.findall(r"icons/([a-z0-9-]+)\.svg", text))
            for name in sorted(referenced):
                self.assertTrue((icons_dir / f"{name}.svg").exists(), f"{page} 引用了缺失图标 {name}")

    def test_kit_sheet_keeps_the_style_guide_sections(self):
        """kit/index.html 是「一页铺开」的样式手册，分节名与顺序固定。"""
        text = (ROOT / "kit" / "index.html").read_text(encoding="utf-8")
        sections = re.findall(r'<h2 class="sheet-label[^"]*">([^<]+)</h2>', text)
        expected = [
            "Headlines",
            "Sub-headlines",
            "Paragraphs",
            "Display",
            "Buttons",
            "Dropdowns",
            "Input Fields",
            "Input Field Styles",
            "Text Areas &amp; Upload",
            "Checkboxes",
            "Misc",
            "Icons",
            "Sliders &amp; Progress",
            "Selectors",
            "Alerts",
            "Placeholders",
            "Page Blocks",
        ]
        self.assertEqual(sections, expected, f"样式手册分节与预期不符：{sections}")

    def test_new_form_controls_are_shipped(self):
        kit = (ROOT / "kit" / "kit.css").read_text(encoding="utf-8")
        for cls in [
            "lq-select",
            "lq-textarea",
            "lq-checkbox",
            "lq-radio",
            "lq-slider",
            "lq-segmented",
            "lq-stepper",
            "lq-alert",
            "lq-icon",
            "lq-placeholder",
            "lq-breadcrumb",
            "lq-tabs",
            "lq-pagination",
            "lq-search-field",
            "lq-toggle",
            "lq-choice-card",
            "lq-status-badge",
            "lq-skeleton",
            "lq-empty-state",
            "lq-tooltip",
            "lq-accordion",
            "lq-modal",
            "lq-drawer",
            "lq-divider",
        ]:
            self.assertIn(f".{cls}", kit, f"kit.css 缺少 {cls}")
        index = (ROOT / "kit" / "index.html").read_text(encoding="utf-8")
        self.assertIn("Component model · 10 categories", index)
        for marker in ["lq-breadcrumb", "lq-toggle", "lq-status-badge", "lq-modal"]:
            self.assertIn(marker, index, f"kit/index.html 缺少 {marker} 示例")
        for relative in ["design-packs", "artifact-surfaces", "protocols", "recipes", "foundation-dna"]:
            self.assertFalse((self.output / relative).exists(), f"发行包残留旧层 {relative}")
        for path in self.output.rglob("*"):
            self.assertIsNone(
                re.search(r"openclaw|hermes", path.name, re.IGNORECASE),
                f"发行包残留旧运行时文件 {path}",
            )

    def test_package_preview_is_the_repo_preview(self):
        self.assertEqual(
            (self.output / "preview.html").read_bytes(),
            (ROOT / "preview.html").read_bytes(),
            "发行包的 preview.html 必须与仓库 preview.html 一致",
        )

    def test_release_metadata_is_v3(self):
        release = json.loads((self.output / "skill-release.json").read_text(encoding="utf-8"))
        self.assertEqual(release["version"], "3.0.0")
        self.assertEqual(release["package_slug"], PACKAGE_NAME)
        self.assertIn("scripts/check_page.py", release["optional_context"])
        self.assertTrue((self.output / "scripts" / "check_page.py").exists())

    def test_no_shipped_file_points_at_archived_paths(self):
        archived = [
            "foundation-dna",
            "design-packs/",
            "artifact-surfaces/",
            "design-standard-package.json",
            "token-table",
        ]
        for path in self.output.rglob("*"):
            if path.is_dir() or path.suffix not in {".md", ".html", ".json", ".css"}:
                continue
            if path.name == "README.zh-CN.md":
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            for token in archived:
                for line in text.splitlines():
                    if token in line and "archive/" not in line:
                        self.fail(
                            f"{path.relative_to(self.output)} 仍引用已归档路径 {token}：{line.strip()[:80]}"
                        )


class RepositoryHygieneTest(unittest.TestCase):
    def test_kit_matches_token_export(self):
        tokens = json.loads((ROOT / "tokens" / "tokens.semantic.json").read_text(encoding="utf-8"))
        kit = (ROOT / "kit" / "kit.css").read_text(encoding="utf-8")
        for key, value in tokens["color"].items():
            self.assertIn(f"--lq-color-{key}: {value};", kit, f"kit.css 缺少颜色 {key}")
        for key, value in tokens["spacing"].items():
            self.assertIn(f"--lq-space-{key}: {value};", kit, f"kit.css 缺少间距 {key}")
        for key, value in tokens["rounded"].items():
            self.assertIn(f"--lq-radius-{key}: {value};", kit, f"kit.css 缺少圆角 {key}")

    def test_every_component_has_a_kit_class(self):
        fields, _ = build_skill.parse_frontmatter(ROOT / "DESIGN.md")
        kit = (ROOT / "kit" / "kit.css").read_text(encoding="utf-8")
        for component in fields["components"]:
            self.assertIn(
                f".{build_skill.expected_class(component)}",
                kit,
                f"kit.css 缺少 {component} 对应的类",
            )

    def test_check_page_passes_on_own_artifacts(self):
        result = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "check_page.py"),
                "preview.html",
                "kit/index.html",
                "kit/kit.css",
                "kit/templates/homepage.html",
                "kit/templates/product-detail.html",
                "tokens/tokens.css",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, f"自有产物未通过校验：{result.stdout}")

    def test_check_page_catches_drift(self):
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / "bad.html"
            bad.write_text(
                '<div style="color:#123456;font-size:19px;padding:20px;'
                'border-radius:8px;font-weight:700">x</div>',
                encoding="utf-8",
            )
            result = subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "check_page.py"), str(bad)],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 1, "校验器没有拦住明显偏离")
            for rule in ["color-off-token", "font-size-off-scale", "spacing-off-scale", "radius-off-scale", "font-weight-declared"]:
                self.assertIn(rule, result.stdout, f"未报出 {rule}")

    def test_only_light_scripts_remain(self):
        scripts = sorted(p.name for p in (ROOT / "scripts").glob("*.py"))
        self.assertEqual(scripts, ["build_skill.py", "check_page.py", "sync_runtimes.py"])

    def test_root_has_single_standard_and_preview(self):
        self.assertTrue((ROOT / "DESIGN.md").is_file())
        self.assertTrue((ROOT / "preview.html").is_file())
        self.assertFalse((ROOT / "index.html").exists(), "index.html 应已并入 preview.html")
        self.assertFalse((ROOT / "styles.css").exists(), "旧 demo 样式应已归档")

    def test_legacy_assets_are_archived(self):
        for name in ["styles.css", "components.html", "artifact-web-brand-landing.html"]:
            self.assertTrue((ROOT / "archive" / "legacy-v2-pages" / name).exists(), f"{name} 未归档")
        for name in ["examples", "foundation-dna", ".impeccable.md"]:
            self.assertTrue((ROOT / "archive" / "legacy-v2-standard" / name).exists(), f"{name} 未归档")

    def test_no_default_path_file_points_at_archived_layers(self):
        offenders = []
        skip = {"archive", "dist", "tmp", ".git", ".planning", "__pycache__"}
        for path in ROOT.rglob("*"):
            if path.is_dir() or path.suffix not in {".md", ".html", ".json", ".py", ".css"}:
                continue
            if skip & set(path.relative_to(ROOT).parts):
                continue
            if path.name in {"test_skill_package.py", "test_design_standard.py", "build_skill.py"}:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            for token in ["foundation-dna", "token-table.zh-CN.md", "design-standard-package.json", "styles.css"]:
                for line in text.splitlines():
                    if token in line and "archive/" not in line:
                        offenders.append(f"{path.relative_to(ROOT)} -> {token}")
        self.assertEqual(offenders, [], f"仍有指向已归档内容的引用：{offenders}")


if __name__ == "__main__":
    unittest.main()
