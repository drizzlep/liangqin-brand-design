# Foundation DNA / 中文高端家居品牌设计规范系统 v1

本目录提供一套可直接复用的 **Foundation DNA**，用于指导后续官网、案例页、产品页、表单、内容模块与组件系统设计。

## 文件说明

- `design-dna.zh-CN.json`：完整 Design DNA / Token Contract，适合给设计、前端、生成式工作流直接消费
- `tokens.semantic.json`：工具中立的语义 token 导出层，适合给 Stitch、OpenClaw 之外的其他 agent 或脚本直接读取
- `tokens.css`：将核心 design token 映射为 CSS 自定义属性，便于原型或真实项目快速接入
- `token-table.zh-CN.md`：中文说明版 token 建议表，含原则、默认值、使用边界与落地建议
- `../design-standard-package.json`：跨工具标准包元数据、消费层级与团队治理约定
- `../skills/public/liangqin-brand-openclaw/`：将标准包适配成 OpenClaw 可消费的输入协议、蓝图 schema、模块 recipe、样例与评测清单

## 使用顺序

1. 先读 `design-dna.zh-CN.json`，确定品牌气质、系统字段与默认值
2. 在跨工具脚本或 agent 里优先读取 `tokens.semantic.json`
3. 在页面或组件实现中引入 `tokens.css`
4. 遇到中文排版、图片、CTA、表单层级等问题时，优先对照 `token-table.zh-CN.md`
5. 如果要给 OpenClaw 直接消费，再进入 `../skills/public/liangqin-brand-openclaw/` 使用适配器层

## 核心方向

- **品牌气质**：高端温润
- **风格来源**：Poliform / Flexform / Stockholm Design Lab
- **中文适配原则**：优先可读、层级清晰、克制高级、重材质与影像
- **特效原则**：默认低强度，仅保留必要的显隐、弱视差与图片过渡

## 推荐后续步骤

- 基于当前 DNA 继续扩展首页 / 产品详情的蓝图 schema 与模块 recipe
- 为标准包补齐更多工具中立的 tokens / assets / regression metadata
- 为 OpenClaw 适配器增加更多黄金样例与人工评测案例
- 将字体资源、图片规格、栅格模板与标准包层一起接入真实项目工程
