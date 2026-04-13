# 良禽品牌体

这个目录是当前设计规范仓库里的 **OpenClaw 适配器层**，也是以后对外发布给 OpenClaw 的统一品牌入口，面向**所有渠道**统一先产出受标准包约束的结构化 spec。

它消费的是根目录跨工具标准包，而不是重新定义一套品牌规则。

## 当前定位

- 对外推荐触发词：`良禽品牌体`
- 对外兼容触发词：`良禽佳木品牌体`
- 对内稳定 slug：`liangqin-brand-openclaw`
- 对内源目录暂时仍保留：`skills/public/liangqin-brand-openclaw/`
- 标准本体位于根目录 `DESIGN.md`、`CONSUMER-GUIDE.zh-CN.md`、`foundation-dna/`、`artifact-surfaces/`、`assets/brand/`、`evaluation/` 与 `design-standard-package.json`
- 本目录只负责把标准包适配成 OpenClaw 可执行协议

## 入口路由规则

对外默认暴露两个中文触发词：

- `良禽品牌体`
- `良禽佳木品牌体`

以下请求默认优先交给 `良禽品牌体 / 良禽佳木品牌体`：

- 良禽佳木首页
- 良禽佳木产品详情
- 良禽佳木品牌页
- 良禽佳木图片、长图、海报、视觉稿
- 良禽佳木封面图、报价卡图、社媒卡片
- 良禽佳木图标方案 / icon 方案
- `DESIGN.md` / 设计系统
- 页面蓝图、模块编排、品牌视觉约束
- 风格切换，例如：`良禽佳木apple风`

推荐规则：

- 所有良禽视觉类请求都要先进入 `良禽品牌体 / 良禽佳木品牌体`
- 即使同一句里出现材质、产品、报价等词，只要目标是图片、页面、长图、卡片或视觉稿，也不得被报价类 skill 抢走
- 第一阶段先统一成结构化 spec，再决定最终交付物
- 后续图片、页面、长图或动效渲染，优先消费这份 spec 做渠道适配

## 与标准包的关系

协议速查：

- Truth: `foundation-dna/design-dna.zh-CN.json`
- Neutral token export: `foundation-dna/tokens.semantic.json`
- Default design input: 根目录 `DESIGN.md`
- Consumer guide: 根目录 `CONSUMER-GUIDE.zh-CN.md`
- Package manifest: 根目录 `design-standard-package.json`
- Default OpenClaw core: `DESIGN.md` + `CONSUMER-GUIDE.zh-CN.md` + `protocols/brand-boundaries.zh-CN.json` + `protocols/brand-assets.zh-CN.json` + `recipes/module-recipes.zh-CN.json` + `EXECUTION-CHECKLIST.md`
- Read protocol: 根目录 `DESIGN-GOVERNANCE.md`
- Role: 把标准包压成 OpenClaw 可调用、可组合、可评测的结构化资产
- Visual handoff: 先产出 `visual_delivery_spec`，再交给图片、页面、长图、卡片或其他渠道渲染器

消费层级：

- Tier 1：只读 `DESIGN.md`
- Tier 2：`DESIGN.md + artifact-surfaces + assets`
- Tier 3：OpenClaw 默认按完整标准包消费

## 目录说明

- `SKILL.md`：OpenClaw 适配器入口与执行规则
- `protocols/`：输入输出协议与品牌边界
- `protocols/brand-assets.zh-CN.json`：OpenClaw 侧品牌资产协议镜像，真源见根目录 `assets/brand/asset-manifest.zh-CN.json`
- `recipes/`：固定模块库
- `examples/`：OpenClaw 本地兼容样例，内容必须与根目录 `evaluation/examples/` 对齐
- `evaluation/`：OpenClaw 侧评测镜像，真源见根目录 `evaluation/`，镜像文件内会显式标注 `source_of_truth`
- `scripts/`：轻量校验脚本
- `skill-release.json`：OpenClaw 适配器发行元数据

关于样例归属：

- 根目录 `evaluation/examples/` 才是标准本体的结构化黄金样例真源
- 本目录 `examples/` 继续保留，只作为 OpenClaw 本地消费兼容层
- 如果两者发生冲突，应先修 root，再同步 adapter

## 对外分发

推荐把它当成一个单独 skill 包发布到 GitHub Release，而不是要求使用者自己在源码仓库里找目录复制。

推荐接入体验：

1. 安装一个包
2. 只记两个中文入口词：`良禽品牌体` / `良禽佳木品牌体`
3. 不要求用户记住英文 slug；`liangqin-brand-openclaw` 只用于系统内部稳定运行
4. 如需风格偏移，再补充 pack 关键词，例如：`良禽佳木apple风`
5. 如果只是要写公关稿、品牌通稿或文章，再调用次级写作能力，不要拿它们替代顶层品牌入口
6. 如果要理解完整标准包，再回到根目录 `design-standard-package.json`

冲突处理：

- 如果 `DESIGN.md` 与 `foundation-dna/` 或 `protocols/brand-boundaries.zh-CN.json` 冲突，以后两者为准
