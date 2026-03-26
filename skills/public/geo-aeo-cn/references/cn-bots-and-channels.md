# 中国常见抓取器（User-Agent）与内容分发渠道

> 用于 robots.txt 放行、抓取可读性优化与分发计划参考。列表非穷尽；以公开资料为准并随版本更新。

## 抓取器（User-Agent 关键词）

- Baiduspider（百度搜索）
- Bytespider（字节系；今日头条/抖音内容抓取）
- 360Spider（360 搜索）
- Sogou web spider / Sogou spider（搜狗）
- YisouSpider（神马搜索，UC 旗下）
-（跨境/AI）PerplexityBot、GPTBot、ChatGPT-User、ClaudeBot、bingbot、Googlebot 等

参考：
- Shift Inc.《Bots and crawler management》：包含 Bytespider、ToutiaoSpider、Sogou、360Spider 等示例 UA 与 robots 规则。证据性资料，建议优先允许而非屏蔽。citeturn3search2
- KDocs《User Agents》：列出 YisouSpider（神马）等 UA。citeturn3search18

### robots.txt 基本范式（示例）

```txt
User-agent: *
Allow: /

# 显式列出重要 AI/中文抓取器（可选）
User-agent: Baiduspider
Allow: /
User-agent: Bytespider
Allow: /
User-agent: 360Spider
Allow: /
User-agent: Sogou web spider
Allow: /
User-agent: YisouSpider
Allow: /
# 国际 AI
User-agent: PerplexityBot
Allow: /
User-agent: GPTBot
Allow: /
User-agent: ClaudeBot
Allow: /
User-agent: bingbot
Allow: /
```

> 提醒：如需屏蔽敏感目录，请用 `Disallow` 精确指定；避免全局屏蔽导致无法被引用。

## 常见中文内容渠道（建议同步“同口径事实”）

- 官网（权威原点）
- 微信公众号（长文/白皮书复述）
- 知乎（问答/专栏）
- B 站（讲解/评测/对比）
- 小红书（卡片/清单）
- 今日头条/抖音（短视频/图文）
- 技术社区：掘金、CSDN、少数派等

> 这些渠道可被中文 LLM 或其上游搜索收录，形成跨源一致性与权威信号。

EOF
