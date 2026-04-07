# 良禽品牌体

这个目录是当前设计规范仓库里的**品牌专用协议层**，也是以后对外发布给 OpenClaw 的**唯一品牌入口**。

它把现有的：

- `foundation-dna/design-dna.zh-CN.json`
- `foundation-dna/tokens.css`
- `foundation-dna/token-table.zh-CN.md`
- `DESIGN.md`

进一步翻译成 OpenClaw 可消费的资产：

- 输入协议
- 页面蓝图 schema
- 固定模块库 recipe
- 黄金样例
- 人工评测清单

## 当前定位

- 对外唯一入口词：`良禽品牌体`
- 对内源目录暂时仍保留：`skills/public/liangqin-brand-openclaw/`
- 新体系由 `DESIGN.md` 主导，旧的良禽品牌文案类能力应降级为内部子能力，不再作为顶层品牌入口

## 入口路由规则

对外默认只暴露一个顶层品牌入口：

- `良禽品牌体`

以下请求应直接交给 `良禽品牌体`：

- 良禽佳木首页
- 良禽佳木产品详情
- 良禽佳木品牌页
- `DESIGN.md` / 设计系统
- 页面蓝图、模块编排、品牌视觉约束
- 风格切换，例如：`良禽佳木apple风`

旧的公关稿、品牌通稿、`/小强体`、`/厂长模式`、`/硬核木匠` 这类能力，只应视为次级写作能力：

- 只在用户明确要求写稿、写文章、写传播文案时触发
- 不再承担顶层品牌入口职责
- 不应拦截页面生成、设计治理或风格控制请求

## v1 范围

- 只服务**良禽佳木**
- 只支持**首页**与**产品详情**
- 只允许**固定模块库优先**
- 默认**文字为主，图片辅助**
- 第一优先级是**更像品牌**

## 目录说明

- `SKILL.md`：Skill 入口与执行规则
- `protocols/`：输入输出协议与品牌边界
- `recipes/`：固定模块库
- `examples/`：黄金样例
- `evaluation/`：人工评测清单
- `scripts/`：轻量校验脚本
- `skill-release.json`：对外发行元数据

## 与 Foundation DNA 的关系

本目录是 OpenClaw 的品牌执行层，不替代 Foundation DNA，也不重定义品牌规则。

协议速查：

- Truth: `foundation-dna/design-dna.zh-CN.json`
- Default design input: 根目录 `DESIGN.md`
- Default OpenClaw core: `DESIGN.md` + `protocols/brand-boundaries.zh-CN.json` + `recipes/module-recipes.zh-CN.json`
- Read protocol: 根目录 `DESIGN-GOVERNANCE.md`
- OpenClaw boundary: `protocols/brand-boundaries.zh-CN.json`
- Role: 把品牌规则压成可调用、可组合、可评测的首页 / 产品详情蓝图资产

## 对外分发

推荐把它当成一个单独 skill 包发布到 GitHub Release，而不是要求使用者自己在源码仓库里找目录复制。

推荐接入体验：

1. 安装一个包
2. 只记一个入口词：`良禽品牌体`
3. 如需风格偏移，再补充 pack 关键词，例如：`良禽佳木apple风`
4. 如果只是要写公关稿、品牌通稿或文章，再调用次级写作能力，不要拿它们替代顶层品牌入口

冲突处理：

- 如果 `DESIGN.md` 与 `foundation-dna/` 或 `protocols/brand-boundaries.zh-CN.json` 冲突，以后两者为准
