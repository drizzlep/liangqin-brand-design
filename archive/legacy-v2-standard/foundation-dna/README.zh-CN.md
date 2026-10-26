# Foundation DNA

这里是 `DESIGN.md` 背后的机器可读层与理由层。

## 文件说明

- `design-dna.zh-CN.json`：品牌内核真源。包含品牌原则、设计系统、视觉特效策略、中文适配与投放准则，用于解释"为什么这样定"。
- `tokens.semantic.json`：工具中立的语义 token 导出，供脚本和 agent 直接读取，不必解析 YAML。
- `tokens.css`：核心 token 的 CSS 自定义属性，前端可直接引用。

## 使用顺序

1. 人和 agent 默认读仓库根目录 `DESIGN.md`
2. 脚本或需要结构化数据时读 `tokens.semantic.json`
3. 前端工程引用 `tokens.css`
4. 需要理解取值理由时再读 `design-dna.zh-CN.json`

## 一致性

`DESIGN.md` 的 frontmatter 是面向 agent 的对外表达，`tokens.semantic.json` 与 `tokens.css` 是它的导出。两者是**包含关系而不是相等关系**：

- `DESIGN.md` 只列 agent 需要按角色使用的颜色；`tokens.semantic.json` 保留完整中性色阶与全部语义色。
- 反过来必须成立：`DESIGN.md` 里出现的每个颜色、字号、圆角、间距、阴影、缓动值都必须能在 token 导出里找到同值。

这条不变式由 `python3 scripts/build_skill.py --check` 强制检查，`python3 -m unittest discover -s tests -p "test_*.py"` 会再跑一遍。
