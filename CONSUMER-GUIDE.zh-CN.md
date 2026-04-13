# 良禽跨工具标准包消费指南

这份指南用于说明任意渠道、任意 agent、任意生成工具该如何消费这套标准包。

核心原则只有三条：

1. 先对齐良禽品牌标准，再谈渠道和承载。
2. 品类只改内容事实，渠道只改信息密度与交付形式。
3. 低层不能覆盖高层，工具吃不动时要降级，不能自由发挥。

## 1. 适用范围

这套标准默认面向：

- 页面生成
- 长图 / 海报 / 卡片生成
- H5 / 品牌页 / 产品页生成
- 结构化 spec 生产
- 人工评审与回归

它不区分具体渠道，也不要求先声明某个 agent 专属风格。

## 2. 消费层级

### Tier 1

适用：弱能力工具、公开传播、只支持单文件输入的 agent。

最小读取集：

- `DESIGN.md`

允许产出：

- 品牌基调明确的结构化 spec
- 低保真页面说明
- 方向性版式建议

不保证：

- logo 稳定落地
- 图标精度
- 具体承载约束
- 最终视觉成品工艺

### Tier 2

适用：页面、长图、海报、H5 等可直接产出视觉稿的工具。

最小读取集：

- `DESIGN.md`
- `artifact-surfaces/*.json`
- `assets/brand/*`

建议同时读取：

- `CONSUMER-GUIDE.zh-CN.md`
- `EXECUTION-CHECKLIST.md`

保证重点：

- logo 运行时资产
- 承载约束
- 信息密度与基础版式稳定性

### Tier 3

适用：团队内部机器人链路、高保真生成、回归验收。

最小读取集：

- `DESIGN.md`
- `CONSUMER-GUIDE.zh-CN.md`
- `foundation-dna/design-dna.zh-CN.json`
- `foundation-dna/tokens.semantic.json`
- `artifact-surfaces/*.json`
- `assets/brand/*`
- `EXECUTION-CHECKLIST.md`
- `evaluation/*`

保证重点：

- 品牌一致性
- 承载一致性
- logo 与图标降级策略
- 人工评审与回归挂钩

## 3. 推荐读取顺序

默认读取顺序固定为：

`Foundation DNA > DESIGN.md > artifact-surfaces > design-packs > examples`

如果是人类或工具接入，建议按下面顺序消费：

1. 读 `DESIGN.md`，先锁品牌宪法。
2. 读本指南，确认自己属于 Tier 1 / 2 / 3 哪一档。
3. 如果要做具体交付，再读 `artifact-surfaces/*.json`。
4. 如果要产出最终视觉，再校验 `assets/brand/asset-manifest.zh-CN.json`。
5. 如果是高保真链路，再补读 DNA、checklist、evaluation。

## 4. 渠道与品类边界

所有工具都必须遵守：

- 品类变化只改变内容事实、内容重点、叙事顺序。
- 渠道变化只改变画幅、信息密度、交互能力、交付形式。
- 不允许因为“钉钉”“朋友圈”“海报”“H5”而切换成另一套品牌风格。
- 不允许因为“衣柜页”“五金页”“品牌页”而重新发明视觉语言。

## 5. 降级与阻断规则

以下情况必须降级，不能硬出成品：

### 缺少真实 logo 资产

- 只允许输出受 `DESIGN.md` 约束的 structured spec。
- 禁止直接输出页面视觉稿、长图、海报、hero 图、多卡片成品。
- 禁止用纯文字品牌名冒充 logo。

### 图标精度不足

- 优先减少图标数量。
- 必要时取消图标装饰。
- 不允许硬塞粗糙、风格不统一、线条工艺不稳的图标。

### 产品事实不足

- 允许输出低细节结构化方案。
- 不允许用装饰、材质词、情绪词去伪造“完成感”。
- 不允许编造参数、工艺、服务承诺。

### 工具只能读取低层

- 明确停在 Tier 1 或 Tier 2 能力边界。
- 不要伪装成已经满足 Tier 3。

## 6. 最低交付约束

所有视觉请求默认先产出 structured spec，再决定是否进入最终成品阶段。

最终成品至少要满足：

- 仍然明显像良禽佳木
- 中文表达完整自然
- 没有系统说明词泄漏
- logo 没有丢失或被文本替代
- 图标若存在，必须精致且统一

## 7. 什么时候必须停在 spec

只要出现以下任一情况，就应停止在 spec：

- 未读取到真实 logo 资产
- 请求事实明显不足
- 工具无法稳定控制图标工艺
- 工具无法理解对应 artifact surface
- 结果开始泄漏系统说明词
- 结果已经偏成渠道模板，而不是良禽品牌表达

## 8. 人工验收入口

需要人工验收时，优先使用：

- `EXECUTION-CHECKLIST.md`
- `evaluation/manual-rubric.zh-CN.md`
- `evaluation/human-review-protocol.zh-CN.md`
- `evaluation/high-risk-regression-cases.zh-CN.json`

## 9. 一句话原则

先守住良禽，再适配渠道；宁可降级到 spec，也不要脱离 `DESIGN.md` 自由发挥。
