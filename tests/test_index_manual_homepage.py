import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INDEX_HTML = ROOT / "index.html"


class LiangqinIndexManualHomepageTest(unittest.TestCase):
    def test_homepage_keeps_manual_structure_and_theme_toggle(self):
        html = INDEX_HTML.read_text(encoding="utf-8")

        self.assertIn("theme-toggle-button", html)
        self.assertIn("设计手册", html)
        self.assertIn("手册索引", html)
        self.assertIn("品牌资产", html)
        self.assertIn("基础规范", html)
        self.assertIn("组件规范", html)
        self.assertIn("附录资源", html)

    def test_homepage_no_longer_uses_editorial_intro_copy(self):
        html = INDEX_HTML.read_text(encoding="utf-8")

        self.assertNotIn("Editorial Intro", html)
        self.assertNotIn("良禽佳木的规范首页，不只是目录，更像品牌系统进入前的前言。", html)
        self.assertNotIn("Who It Serves", html)
        self.assertNotIn("What It Values", html)
        self.assertNotIn("How To Use", html)


if __name__ == "__main__":
    unittest.main()
