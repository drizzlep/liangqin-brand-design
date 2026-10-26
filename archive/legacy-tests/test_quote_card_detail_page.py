import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUOTE_CARD_HTML = ROOT / "quote-card-detail.html"


class LiangqinQuoteCardDetailPageTest(unittest.TestCase):
    def test_quote_card_detail_page_exists_with_core_sections(self):
        html = QUOTE_CARD_HTML.read_text(encoding="utf-8")

        self.assertIn("图文报价体模板", html)
        self.assertIn("图文报价体，是一种很常规、但必须足够专业的报价呈现方案", html)
        self.assertIn("案例预览", html)
        self.assertIn("正式单品报价卡", html)
        self.assertIn("儿童房组合报价卡", html)
        self.assertIn("多品汇总报价卡", html)
        self.assertIn("参考报价卡", html)
        self.assertIn("无图回退报价卡", html)
        self.assertIn("场景覆盖", html)
        self.assertIn("参考报价", html)
        self.assertIn("超长明细", html)
        self.assertIn("无图回退", html)
        self.assertIn("生成规则摘要", html)
        self.assertIn("总价唯一主焦点", html)
        self.assertIn("先看产品与总价，再看确认条件，最后看必要依据", html)
        self.assertIn("轻图像、强排版、长图阅读", html)
        self.assertIn("回到卡片规范", html)


if __name__ == "__main__":
    unittest.main()
