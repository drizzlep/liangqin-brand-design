---
name: 良禽品牌体
description: 良禽佳木品牌专用的统一 OpenClaw 入口。默认由 DESIGN.md 主导，负责把品牌 brief、产品资料、参考页面转成结构化 spec，再按不同渠道适配页面、图片、长图、卡片或其他视觉交付；旧名为 liangqin-brand-openclaw，迁移期仅作兼容参考。
---

# 良禽品牌体

这是一个**品牌专用 Skill**，不是通用家居品牌模板。  
目标不是“生成得更多”，而是“生成得更像良禽佳木”。
它首先是一个**品牌治理执行器**，也是一个**OpenClaw 消费适配器**，不是标准本体。

对外保留两个中文入口词：

- `良禽品牌体`
- `良禽佳木品牌体`

迁移说明：

- 新体系已接管旧的顶层品牌入口
- `liangqin-brand-openclaw` 现在只保留为历史目录名与兼容说明，不再作为推荐调用名
- 如果用户明确说 `良禽佳木apple风`，继续在这个统一入口内切换对应 pack
- 真正的跨工具标准包元数据位于根目录 `design-standard-package.json`
- 根目录 `evaluation/examples/` 是结构化黄金样例真源，本目录 `examples/` 仅保留本地兼容副本

## 适用范围

- 良禽佳木首页蓝图生成
- 良禽佳木产品详情蓝图生成
- 良禽佳木图片、长图、海报、视觉稿、封面图、卡片图的结构化 spec 生成
- 良禽佳木不同渠道下的同一品牌表达适配
- 同品牌下的轻量变体探索
- 对现有页面方案做品牌一致性反审
- 对品牌风格词进行受控切换，例如 `良禽佳木apple风`

## 默认路由

以下良禽视觉类请求，默认优先进入 `良禽品牌体 / 良禽佳木品牌体`：

- 图片
- 长图
- 海报
- 页面视觉稿
- 社媒封面
- 报价卡图
- 图标方案 / icon 方案

推荐做法是先产出受 `DESIGN.md` 约束的结构化 spec，再交给后续渲染方。
如果下游渠道能力足够，也可以直接消费这份 spec 做最终交付；重点是先统一品牌规则，再做渠道适配，而不是按渠道切换品牌风格。
如果同一句请求里同时出现产品、材质、报价等词，但目标仍是图片、页面、长图、卡片或视觉稿，优先级仍然是 `良禽品牌体`，不得被报价类 skill 抢走。

## 输入规则

默认接收三类输入，优先级固定：

1. **品牌 brief（主输入）**
2. **产品资料（辅输入）**
3. **参考页面（辅输入）**

输入说明见：

- `protocols/input-contract.zh-CN.json`
- `protocols/brand-assets.zh-CN.json`

如果缺少品牌 brief，不要直接输出最终蓝图。  
如果缺少产品资料，可输出低细节蓝图。  
如果缺少参考页面，回退到良禽佳木 DNA 默认风格。

## 输出规则

第一阶段默认先输出结构化 spec，再按需要交给下游产出成品：

- `homepage_blueprint`
- `product_detail_blueprint`
- `visual_delivery_spec`

蓝图 schema 见：

- `protocols/homepage-blueprint.schema.zh-CN.json`
- `protocols/product-detail-blueprint.schema.zh-CN.json`
- `protocols/visual-delivery-spec.schema.zh-CN.json`

## 固定模块库

只允许使用白名单模块，不允许自由发明新模块：

- `brand-hero`
- `trust-intro`
- `material-craft`
- `product-highlight`
- `product-specs`
- `editorial-story`
- `consultation-promise`
- `consultation-cta`

模块 recipe 见：

- `recipes/module-recipes.zh-CN.json`

## 品牌边界

生成时必须遵守：

- 中文优先
- 礼貌 CTA
- 温润、克制、可信
- 结构稳定，允许有限变化
- 不得滑向促销页、电商页、欧美极简模板腔
- 品类变化只影响内容事实与重点，不改写品牌表达
- 承载变化只影响信息压缩与交付方式，不切换风格家族

边界定义见：

- `protocols/brand-boundaries.zh-CN.json`

## 补充外观上下文

OpenClaw 的默认核心读取层固定为：

- 根目录 `DESIGN.md`
- 根目录 `CONSUMER-GUIDE.zh-CN.md`
- 根目录 `design-standard-package.json`
- 根目录 `assets/brand/asset-manifest.zh-CN.json`
- `protocols/brand-boundaries.zh-CN.json`
- `protocols/brand-assets.zh-CN.json`
- `recipes/module-recipes.zh-CN.json`
- 根目录 `EXECUTION-CHECKLIST.md`

如果执行环境可读取仓库根目录 `DESIGN.md`，应默认先读取这 8 份核心资产，再按需要补读 `design-packs/` 与 `artifact-surfaces/`。
默认读取顺序、层级职责与冲突优先级统一以根目录 `DESIGN-GOVERNANCE.md` 为准。

如果任务要直接落成图片、页面、长图、卡片等最终视觉成品，必须同时确认 `protocols/brand-assets.zh-CN.json` 中声明的真实 logo 资产可读；若不可读，只允许停在结构化 spec，不允许直接出最终成品。

如果用户明确说“良禽佳木apple风”，应补读 `design-packs/liangqin-apple.json`，把它视为受控变化层，而不是替代品牌真源。

如果 `DESIGN.md` 与 `foundation-dna/` 或 `protocols/brand-boundaries.zh-CN.json` 冲突，以后两者为准。

## 推荐工作流

1. 读取输入合同，判断信息完整度
2. 先读取 `DESIGN.md`，提取不可协商的品牌规则
3. 再读取 `design-standard-package.json`，确认当前消费层级与适用边界
4. 先判断这次请求属于页面蓝图还是视觉交付 spec，再选择对应 schema
5. 页面类请求只从白名单模块库中选模块；视觉类请求先定义信息主次、构图、图像角色与图标降级策略
6. 再判断这次变化属于“内容变化”“承载变化”还是“渠道变化”，三者都不得被理解成风格切换
7. 按品牌边界约束结构、语气、CTA、中文表达和图标工艺
8. 先确认 `protocols/brand-assets.zh-CN.json` 中的真实 logo 资产已可读；若不可读，停止在结构化 spec
9. 用 `EXECUTION-CHECKLIST.md` 做生成前 / 生成中 / 生成后自检
10. 如需落到具体渠道，优先调整信息密度、画幅、交付形式，不切换品牌真源
11. OpenClaw 默认按 Tier 3 消费标准包；如果上下文不足，至少保住 Tier 1 或 Tier 2 的边界
12. 如与品牌边界冲突，回退到 Foundation DNA 与 DESIGN.md；如图标或复杂细节无法稳定成立，优先降级而不是自由发挥

## 黄金样例与评测

- Root 首页黄金样例：根目录 `evaluation/examples/homepage-golden-sample.zh-CN.json`
- Root 产品详情黄金样例：根目录 `evaluation/examples/product-detail-golden-sample.zh-CN.json`
- OpenClaw 本地兼容样例：`examples/homepage-golden-sample.zh-CN.json`
- OpenClaw 本地兼容样例：`examples/product-detail-golden-sample.zh-CN.json`
- 人工评测清单：`evaluation/manual-rubric.zh-CN.md`
- 高风险回归题：`evaluation/high-risk-regression-cases.zh-CN.json`

## 禁止事项

- 不把参考页当作直接模仿对象
- 不输出白名单外模块
- 不以强刺激文案替代品牌信任感
- 不为了“高级感”牺牲中文可读性
- 不用复杂特效掩盖信息结构
- 不把渠道约束误当成风格切换理由
- 不在成品中泄漏 `Pack`、`Page Goal`、`Preview` 等系统说明词
- 不因为渠道不同，就切换成另一套品牌语言
- 不在未读取真实 logo 资产时，拿纯文字品牌名冒充品牌标志
