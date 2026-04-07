import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INDEX_HTML = ROOT / "index.html"


class LiangqinIndexHomepageTest(unittest.TestCase):
    def test_homepage_now_matches_design_preview_surface(self):
        html = INDEX_HTML.read_text(encoding="utf-8")

        self.assertIn("Brand Surface Preview", html)
        self.assertIn("Artifact Surfaces", html)
        self.assertIn("Style Directions", html)
        self.assertIn("当前风格方向", html)
        self.assertIn("style-direction-note", html)
        self.assertIn("先看最终成品，再回头看风格方向", html)
        self.assertIn("/artifact-web-brand-landing", html)
        self.assertIn("/artifact-mobile-h5-consultation", html)
        self.assertIn("/artifact-quote-card-editorial", html)
        self.assertNotIn("AI Governance", html)
        self.assertNotIn("默认读取顺序", html)
        self.assertNotIn(
            "Foundation DNA > DESIGN.md > artifact-surfaces > design-packs > examples",
            html,
        )
        self.assertNotIn("推荐模块栈", html)

    def test_homepage_no_longer_uses_manual_sidebar_structure(self):
        html = INDEX_HTML.read_text(encoding="utf-8")

        self.assertNotIn("theme-toggle-button", html)
        self.assertNotIn("良禽佳木设计手册", html)
        self.assertNotIn("手册索引", html)
        self.assertNotIn("组件规范", html)
        self.assertNotIn("附录资源", html)


if __name__ == "__main__":
    unittest.main()
