---
name: liangqin-brand-openclaw
description: 良禽佳木品牌专用的 OpenClaw 页面蓝图 Skill。用于把品牌 brief、产品资料、参考页面转成结构化首页/产品详情蓝图，并在固定模块库内继续生成更像良禽佳木的页面方案。
---

# 良禽佳木页面蓝图 Skill

这是一个**品牌专用 Skill**，不是通用家居品牌模板。  
目标不是“生成得更多”，而是“生成得更像良禽佳木”。

## 适用范围

- 良禽佳木首页蓝图生成
- 良禽佳木产品详情蓝图生成
- 同品牌下的轻量变体探索
- 对现有页面方案做品牌一致性反审

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

## 推荐工作流

1. 读取输入合同，判断信息完整度
2. 根据页面类型选择对应蓝图 schema
3. 只从白名单模块库中选模块
4. 按品牌边界约束结构、语气、CTA
5. 对照黄金样例与人工评测清单做自检

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
