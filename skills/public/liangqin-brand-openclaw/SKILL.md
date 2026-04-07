---
name: 良禽品牌体
description: 良禽佳木品牌专用的统一 OpenClaw 入口。默认由 DESIGN.md 主导，负责把品牌 brief、产品资料、参考页面转成结构化首页/产品详情蓝图；旧名为 liangqin-brand-openclaw，迁移期仅作兼容参考。
---

# 良禽品牌体

这是一个**品牌专用 Skill**，不是通用家居品牌模板。  
目标不是“生成得更多”，而是“生成得更像良禽佳木”。

对外只保留这一个入口词：

- `良禽品牌体`

迁移说明：

- 新体系已接管旧的顶层品牌入口
- `liangqin-brand-openclaw` 现在只保留为历史目录名与兼容说明，不再作为推荐调用名
- 如果用户明确说 `良禽佳木apple风`，继续在这个统一入口内切换对应 pack

## 适用范围

- 良禽佳木首页蓝图生成
- 良禽佳木产品详情蓝图生成
- 同品牌下的轻量变体探索
- 对现有页面方案做品牌一致性反审
- 对品牌风格词进行受控切换，例如 `良禽佳木apple风`

## 输入规则

默认接收三类输入，优先级固定：

1. **品牌 brief（主输入）**
2. **产品资料（辅输入）**
3. **参考页面（辅输入）**

输入说明见：

- `protocols/input-contract.zh-CN.json`

如果缺少品牌 brief，不要直接输出最终蓝图。  
如果缺少产品资料，可输出低细节蓝图。  
如果缺少参考页面，回退到良禽佳木 DNA 默认风格。

## 输出规则

第一阶段只允许输出两类结构化蓝图：

- `homepage_blueprint`
- `product_detail_blueprint`

蓝图 schema 见：

- `protocols/homepage-blueprint.schema.zh-CN.json`
- `protocols/product-detail-blueprint.schema.zh-CN.json`

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

边界定义见：

- `protocols/brand-boundaries.zh-CN.json`

## 补充外观上下文

OpenClaw 的默认核心读取层固定为：

- 根目录 `DESIGN.md`
- `protocols/brand-boundaries.zh-CN.json`
- `recipes/module-recipes.zh-CN.json`

如果执行环境可读取仓库根目录 `DESIGN.md`，应默认先读取这 3 份核心资产，再按需要补读 `design-packs/` 与 `artifact-surfaces/`。
默认读取顺序、层级职责与冲突优先级统一以根目录 `DESIGN-GOVERNANCE.md` 为准。

如果用户明确说“良禽佳木apple风”，应补读 `design-packs/liangqin-apple.json`，把它视为受控变化层，而不是替代品牌真源。

如果 `DESIGN.md` 与 `foundation-dna/` 或 `protocols/brand-boundaries.zh-CN.json` 冲突，以后两者为准。

## 推荐工作流

1. 读取输入合同，判断信息完整度
2. 根据页面类型选择对应蓝图 schema
3. 只从白名单模块库中选模块
4. 按品牌边界约束结构、语气、CTA
5. 仅把黄金样例与人工评测清单作为验收基准，而不是主控制来源
6. 如与品牌边界冲突，回退到 Foundation DNA 与 DESIGN.md

## 黄金样例与评测

- 首页黄金样例：`examples/homepage-golden-sample.zh-CN.json`
- 产品详情黄金样例：`examples/product-detail-golden-sample.zh-CN.json`
- 人工评测清单：`evaluation/manual-rubric.zh-CN.md`

## 禁止事项

- 不把参考页当作直接模仿对象
- 不输出白名单外模块
- 不以强刺激文案替代品牌信任感
- 不为了“高级感”牺牲中文可读性
- 不用复杂特效掩盖信息结构
