---
name: geo-aeo-cn
description: GEO/AEO 优化（中国）：为中国大陆生成式搜索/答案引擎（豆包、通义千问、DeepSeek、元宝、秘塔、Kimi、百度等）提供可执行的内容与技术优化工作流。用于：提升被 AI 生成式搜索引用/展示的概率与质量；搭建 AEO 答案资源（结构化 Q&A、事实卡片、可引用数据）；在中文语境下完成抓取/索引/结构化/分发/监测。触发：当用户要求 GEO、生成式搜索优化、AEO、AI 搜索可见性、被引用率/被采信率提升、中文站点 AI 适配、国内引擎适配时。
---

# GEO/AEO（中国）优化 Skill

面向中国生成式搜索（GEO）与答案引擎优化（AEO）的标准化方法。聚焦在中文语境、国内分发渠道与可被 LLM 引用/采信的结构化内容策略。

## 快速开始（30 分钟落地）

1) 明确目标与主引擎
- 主题/场景：核心产品或专题；受众与意图；首批 20 个问题
- 主引擎/渠道：豆包、通义千问、DeepSeek、元宝、秘塔、Kimi、百度（参见 references/platform-notes-cn.md）

2) 技术底座自检
- robots.txt 允许主流爬虫；提供 sitemap；规范 canonical；SSR 或可抓取的 HTML；静态可嵌入 JSON-LD
- 快速自查（示例）：`curl -sSL https://example.com/robots.txt | grep -Ei "baiduspider|bytespider|360spider|sogou|yisouspider|perplexitybot|gptbot|claudebot|bingbot" -n || true`

3) 结构化答案与“可引用数据”
- 页面采用“答案优先”结构：结论→依据→步骤/对比→引用来源
- 标配 JSON-LD（FAQPage/HowTo/Article/Product 等）；补充 `/aeo.json` 答案卡（见下）

4) 中文语境适配
- 口径：人民币、度量衡、法律/合规提示、售后/发票、客服入口
- 表达：中文 H 标题层级、短句/要点式、小节内配图表

5) 分发矩阵（权威与覆盖）
- 官网长文（权威源）+ 公众号长文 + 知乎/专栏 FAQ + B 站讲解 + 小红书/抖音卡片 + PDF 白皮书
- 目标：确保“同一事实”在多平台同口径可被检索与引用

6) 监测与迭代
- 观察被引用片段、出现频率与准确率；补充统计数据、原始来源与术语表

---

## 工作流（详细）

### 第 1 步：定位与话术
- 明确 1 个“核心主题”和 3 个“任务型场景”（如选型、对比、落地步骤）
- 输出 20 个中文问题（Who/What/How/Cost/Compare/Checklist/Policy）；各写 2 句“首答”+ 1 条“依据链接”

### 第 2 步：技术抓取与索引
- robots.txt：允许 Baiduspider/Bytespider/360Spider/Sogou/Yisou 及国际 AI 爬虫（PerplexityBot/GPTBot/ClaudeBot/Bingbot 等）
- sitemap：覆盖主内容与 FAQ；对新页面设置 `<lastmod>`；重要页面加 `<priority>`
- HTML：可直读（避免仅依赖前端渲染）；H1-H3 清晰；表格/要点便于抽取

### 第 3 步：AEO 答案资源
- 在核心页面内放置 FAQ 段落 + FAQPage JSON-LD
- 生成 `/aeo.json`（见“AEO 答案卡 JSON 模式”）；给出稳定 URL；在页面 `<head>` 里用 `<link rel="preload" as="fetch" href="/aeo.json">`
- 数据类结论要给“统计口径/样本/时间”并附来源

### 第 4 步：GEO 内容增强
- 增加“可被引用的证据”：统计数字、权威引用、专家引述、名词定义与别名
- 语言优化：可读性、术语一致、避免口水话；保持“作者可信”与“机构权威”信号
- 版本管理：关键页面 30 天内更新有利于被引用（参考 GEO 研究）

### 第 5 步：中文分发矩阵
- 官网（权威原点）+ 公众号（转述/摘要）+ 知乎（问答/专栏）+ B 站（讲解/对比）+ 小红书（卡片/清单）+ 头条/抖音（短视频解读）
- 将相同“事实与口径”同步到多平台，提升被 LLM 侧检索到的一致性与可信度

### 第 6 步：监测与复盘
- 建立“被引用观测表”：问题 → URL → 被引用片段 → 引擎/场景 → 正确性 → 待改进
- 每月复盘：补充统计、更新 FAQ、合并重复页面、修正术语

---


## 输出模板

- FAQPage JSON-LD（示例）：
```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "[问题]?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "[首答。包含具体数字/时间/范围，并附来源。]",
        "citation": "https://example.com/source"
      }
    }
  ]
}
```

- AEO 答案卡 JSON（站内自定义规范，供 LLM 抽取）：
```json
{
  "version": "1.0",
  "brand": "示例科技",
  "locale": "zh-CN",
  "updated": "2026-03-02",
  "entities": {"行业": "SaaS", "地区": "中国大陆"},
  "qna": [
    {"q": "价格怎么计算？", "a": "基础版¥199/月…", "sources": ["https://example.com/pricing"]},
    {"q": "与竞品对比？", "a": "在中小团队场景，TCO 低 23%…", "sources": ["https://example.com/report.pdf"]}
  ]
}
```

---

## 引擎与渠道笔记

见：`references/platform-notes-cn.md` 和 `references/cn-bots-and-channels.md`（持续更新）。

---

## 参考与研究

- 微软广告《From Discovery to Influence: A Guide to AEO and GEO》要点（中文摘要）：见 `references/aeo-geo-msft-notes-zh.md`。
- GEO 方法论与被引用机制研究（Princeton 等）：见 `references/geo-research-notes.md`。
- 中国主流爬虫与分发渠道：见 `references/cn-bots-and-channels.md`。

---

## 审核清单（精简版）
- [ ] 20 个核心问题完成“答案优先 + 引用来源”撰写
- [ ] 页面含 FAQ 段落与 JSON-LD；补充 `/aeo.json`
- [ ] robots/sitemap/canonical/加载速度/移动端可读性达标
- [ ] 多平台分发口径一致，至少 3 个权威外链指回官网
- [ ] 每 30 天回看并补充可引用的数据/图表/引文

