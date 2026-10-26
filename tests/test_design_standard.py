"""DESIGN.md 标准结构与 token 一致性检查。"""

import importlib.util
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESIGN_MD = ROOT / "DESIGN.md"
PREVIEW_HTML = ROOT / "preview.html"
TOKENS = json.loads((ROOT / "tokens" / "tokens.semantic.json").read_text(encoding="utf-8"))

CANONICAL_SECTIONS = [
    "## Overview",
    "## Colors",
    "## Typography",
    "## Layout",
    "## Elevation & Depth",
    "## Shapes",
    "## Components",
    "## Do's and Don'ts",
    "## Responsive Behavior",
    "## Iteration Guide",
    "## Known Gaps",
]

EXTENSION_SECTIONS = ["## Brand Mark & Logo"]

STANDARD_FRONTMATTER_KEYS = [
    "version",
    "name",
    "description",
    "colors",
    "typography",
    "rounded",
    "spacing",
    "components",
]


def load_build_script():
    spec = importlib.util.spec_from_file_location(
        "liangqin_build_skill", ROOT / "scripts" / "build_skill.py"
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


build_skill = load_build_script()


def token_color_values() -> set[str]:
    return {
        str(value).upper() for value in build_skill.walk_values(TOKENS["color"]).values()
    }


def luminance(value: str) -> float:
    raw = value.lstrip("#")
    channels = [int(raw[i : i + 2], 16) / 255 for i in (0, 2, 4)]
    linear = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in channels]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def contrast(foreground: str, background: str) -> float:
    a, b = luminance(foreground), luminance(background)
    high, low = max(a, b), min(a, b)
    return (high + 0.05) / (low + 0.05)


class DesignMdStructureTest(unittest.TestCase):
    def setUp(self):
        self.text = DESIGN_MD.read_text(encoding="utf-8")
        self.fields, _ = build_skill.parse_frontmatter(DESIGN_MD)

    def test_canonical_sections_appear_in_order(self):
        positions = [self.text.find(section) for section in CANONICAL_SECTIONS]
        self.assertNotIn(-1, positions, f"缺少标准章节：{[s for s in CANONICAL_SECTIONS if s not in self.text]}")
        self.assertEqual(positions, sorted(positions), "标准九段没有按规范顺序出现")

    def test_extension_sections_come_last(self):
        last_canonical = self.text.find(CANONICAL_SECTIONS[-1])
        for section in EXTENSION_SECTIONS:
            position = self.text.find(section)
            self.assertNotEqual(position, -1, f"缺少扩展章节 {section}")
            self.assertGreater(position, last_canonical, "扩展段必须排在标准九段之后")

    def test_frontmatter_has_standard_token_blocks(self):
        for key in STANDARD_FRONTMATTER_KEYS:
            self.assertIn(key, self.fields, f"frontmatter 缺少标准字段 {key}")

    def test_frontmatter_has_no_extra_keys(self):
        extra = sorted(set(self.fields) - set(STANDARD_FRONTMATTER_KEYS))
        self.assertEqual(extra, [], f"frontmatter 多出非标准键：{extra}")

    def test_frontmatter_declares_no_font_weight(self):
        block = "\n".join(build_skill.split_frontmatter(DESIGN_MD)[0])
        self.assertNotIn("fontWeight", block)
        self.assertNotIn("font-weight", block)

    def test_frontmatter_follows_constrained_grammar(self):
        block = "\n".join(build_skill.split_frontmatter(DESIGN_MD)[0])
        self.assertTrue(block.strip(), "frontmatter 为空")
        errors: list[str] = []
        build_skill.resolve_refs(self.fields, block, "DESIGN.md", errors)
        self.assertEqual(errors, [], "存在无法解析的 token 引用")
        self.assertGreater(len(set(build_skill.TOKEN_REFERENCE.findall(block))), 8)


class DesignTokenConsistencyTest(unittest.TestCase):
    def setUp(self):
        self.fields, _ = build_skill.parse_frontmatter(DESIGN_MD)

    def test_colors_exist_in_token_export(self):
        allowed = token_color_values()
        for role, value in build_skill.walk_values(self.fields["colors"]).items():
            self.assertIn(str(value).upper(), allowed, f"颜色 {role}={value} 不在 token 导出中")

    def test_colors_rounded_spacing_match_token_export_exactly(self):
        self.assertEqual(self.fields["colors"], TOKENS["color"])
        self.assertEqual(self.fields["rounded"], TOKENS["rounded"])
        self.assertEqual(self.fields["rounded"], TOKENS["shape"]["radius"])
        self.assertEqual(self.fields["spacing"], TOKENS["spacing"])

    def test_type_scale_matches_token_export(self):
        token_sizes = {entry["size"] for entry in TOKENS["typography"]["scale"].values()}
        design_sizes = {
            str(entry["fontSize"])
            for entry in self.fields["typography"].values()
            if isinstance(entry, dict) and "fontSize" in entry
        }
        self.assertEqual(design_sizes, token_sizes)

    def test_elevation_and_motion_values_appear_in_body(self):
        text = DESIGN_MD.read_text(encoding="utf-8")
        for value in TOKENS["elevation"].values():
            self.assertIn(value, text, f"正文缺少阴影值 {value}")
        self.assertIn(TOKENS["motion"]["easing"], text)
        for value in TOKENS["motion"]["duration"].values():
            self.assertIn(value, text, f"正文缺少动效时长 {value}")

    def test_components_layer_is_dense_enough(self):
        components = self.fields["components"]
        self.assertIsInstance(components, dict)
        self.assertGreaterEqual(len(components), 20, "components 层过薄")
        for name, spec in components.items():
            self.assertIsInstance(spec, dict, f"{name} 不是映射")
            self.assertTrue(spec, f"{name} 没有字段")

    def test_every_component_is_explained_in_prose(self):
        section = DESIGN_MD.read_text(encoding="utf-8")
        for name in self.fields["components"]:
            self.assertIn(f"`{name}`", section, f"{name} 缺少正文解释")

    def test_components_do_not_document_hover_states(self):
        for name in self.fields["components"]:
            self.assertFalse(name.endswith("-hover"), f"{name} 不应作为组件条目")


class DesignFactsTest(unittest.TestCase):
    def setUp(self):
        self.text = DESIGN_MD.read_text(encoding="utf-8")

    def test_documented_contrast_ratios_match_colors(self):
        checked = 0
        for line in self.text.splitlines():
            if not line.startswith("|"):
                continue
            hexes = re.findall(r"#[0-9A-Fa-f]{6}", line)
            documented = re.findall(r"(\d+\.\d+):1", line)
            if len(hexes) != 2 or len(documented) != 1:
                continue
            actual = contrast(hexes[0], hexes[1])
            self.assertAlmostEqual(actual, float(documented[0]), delta=0.01, msg=line)
            checked += 1
        self.assertGreaterEqual(checked, 5, "对比度表没有被解析到")

    def test_logo_references_exist(self):
        for reference in sorted(set(re.findall(r"assets/brand/[A-Za-z0-9._-]+", self.text))):
            self.assertTrue((ROOT / reference).exists(), f"缺少资产 {reference}")

    def test_standard_covers_logo_geometry_and_open_questions(self):
        for marker in ["678×188", "568×419", "#9E7F63", "Swei Sugar"]:
            self.assertIn(marker, self.text, f"DESIGN.md 缺少事实记录 {marker}")


class PreviewPageTest(unittest.TestCase):
    def setUp(self):
        self.html = PREVIEW_HTML.read_text(encoding="utf-8")
        self.style = re.search(r"<style>(.*?)</style>", self.html, re.S).group(1)

    def test_preview_mirrors_standard_sections(self):
        for marker in [
            "Overview 概览",
            "Colors 色彩",
            "Typography 字号",
            "Layout 布局",
            "Elevation &amp; Depth 阴影与动效",
            "Shapes 形状",
            "Components 组件",
            "Do's and Don'ts 该做与不该做",
            "Responsive Behavior 响应式",
            "Iteration Guide 迭代指南",
            "Known Gaps 已知缺口",
            "Brand Mark &amp; Logo 标志",
        ]:
            self.assertIn(marker, self.html, f"预览页缺少 {marker}")

    def test_preview_shows_component_catalog(self):
        for marker in [
            "Navigation",
            "Buttons",
            "Forms",
            "Content cards",
            "Page blocks",
            "Marks &amp; tags",
            "Component model",
            "Wayfinding",
            "Extended forms",
            "Feedback &amp; overlays",
        ]:
            self.assertIn(marker, self.html, f"预览页缺少组件分组 {marker}")
        for name in [
            "button-primary",
            "text-input",
            "card-case",
            "consultation-cta",
            "pill-tag",
            "breadcrumb",
            "toggle",
            "choice-card",
            "status-badge",
            "skeleton",
            "empty-state",
            "tooltip",
            "accordion",
            "modal",
            "drawer",
            "divider",
        ]:
            self.assertIn(name, self.html, f"预览页缺少组件 {name}")
        self.assertIn("64 条规格、91 个类名", self.html)

    def test_preview_css_stays_on_brand_palette(self):
        hexes = {value.upper() for value in re.findall(r"#(?:[0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b", self.style)}
        off_palette = sorted(hexes - token_color_values())
        self.assertEqual(off_palette, [], f"预览页 CSS 用了 token 外的颜色：{off_palette}")

    def test_preview_avoids_low_contrast_text_colors(self):
        for banned in ["color: var(--ink-500)", "color: var(--warning)"]:
            self.assertNotIn(banned, self.style, f"预览页用 {banned} 作正文色，低于 AA 4.5:1")

    def test_preview_assets_exist(self):
        for reference in sorted(set(re.findall(r'(?:src|url\()"?\.?/?(assets/[A-Za-z0-9._/-]+)"?', self.html))):
            self.assertTrue((ROOT / reference).exists(), f"预览页引用缺失资产 {reference}")


if __name__ == "__main__":
    unittest.main()
