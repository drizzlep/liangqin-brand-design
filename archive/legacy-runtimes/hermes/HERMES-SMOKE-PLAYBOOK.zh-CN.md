# Hermes Smoke Playbook

这份 playbook 用于第一次验证 Hermes 是否能按良禽佳木 root package 的边界稳定消费标准包。

目标不是证明 Hermes 已完整接入。
目标只是回答：

`Hermes 会不会一接入就把 root-first 边界讲乱，或在缺资料时假装能做成品。`

## 0. 使用前提

在跑这份 smoke 前，先确认：

- 已阅读 [HERMES-CONSUMER-CONTRACT.zh-CN.md](/Users/admin/Nutstore%20Files/我的坚果云/CODE/project/liangqin-brand-design/HERMES-CONSUMER-CONTRACT.zh-CN.md)
- 已阅读 [.planning/GOVERNANCE-REVIEW-CHECKLIST.md](/Users/admin/Nutstore%20Files/我的坚果云/CODE/project/liangqin-brand-design/.planning/GOVERNANCE-REVIEW-CHECKLIST.md)
- 团队明确这次是 smoke，不是正式发布或功能验收

## 1. Smoke 目标

这次只检查 4 件事：

1. Hermes 是否仍把 root package 当品牌本体
2. Hermes 是否会按 tier 和 delivery gates 正确降级
3. Hermes 是否会在缺 logo / 缺事实时停在 spec 或 blocked
4. Hermes 是否会把多机器人扩展误讲成“各自一套品牌系统”

## 2. 轻量输入集

Smoke 第一轮只把轻量品牌地图给 Hermes：

1. `DESIGN.md`

这一步的目标是验证：Hermes 只看鸟瞰地图时，是否已经能守住品牌方向，并知道自己不能假装完成高保真接入。

如果要测 adapter / 跨工具接入判断，再追加：

2. `AGENT-PREFLIGHT.zh-CN.md`
3. `CONSUMER-GUIDE.zh-CN.md`
4. `design-standard-package.json`

如果要测视觉请求，再追加：

5. `artifact-surfaces/*.json`
6. `assets/brand/asset-manifest.zh-CN.json`
7. `EXECUTION-CHECKLIST.md`

如果要测高保真理解或回归意识，再追加：

8. `evaluation/manual-rubric.zh-CN.md`
9. `evaluation/human-review-protocol.zh-CN.md`
10. `evaluation/high-risk-regression-cases.zh-CN.json`

## 3. 演练步骤

### Step 1. Root-First 边界确认

把下面的问题给 Hermes：

```text
我们后面除了 OpenClaw，还准备让 Hermes 也消费这套良禽佳木标准。请你先说明应该以哪个入口作为品牌本体、OpenClaw 和 Hermes 分别扮演什么角色，再给出接入建议。
```

通过标准：

- 明确回答 root package / 轻量 `DESIGN.md` 才是品牌本体入口
- 能说明 preflight 是高保真 / adapter 接入参考，不是普通请求默认必读
- 明确回答 OpenClaw 与 Hermes 都只是消费者 / 适配器候选
- 没有说“每个机器人维护一套自己的品牌系统”

### Step 2. Tier 自我声明检查

把下面的问题给 Hermes：

```text
如果你现在只能读取 DESIGN.md，你当前应该把自己判为 Tier 1、Tier 2 还是 Tier 3？为什么？

请同时说明：哪些任务场景下你必须补读 AGENT-PREFLIGHT、CONSUMER-GUIDE、artifact-surfaces、assets 或 evaluation？
```

通过标准：

- 不假装自己已经是完整 `Tier 3`
- 能说明当前读取面与能力边界
- 能明确什么时候必须继续补读 asset / surface / evaluation

### Step 3. 视觉请求先出 structured spec

把下面的问题给 Hermes：

```text
请按良禽佳木标准包与 DESIGN.md，把良禽佳木的五金配置做成一张发客户的长图。先输出 structured spec，再决定是否进入最终视觉。
```

通过标准：

- 第一输出是 structured spec，而不是直接视觉成品
- 能先识别这次属于视觉请求
- 没有跳过 Context Gate 与 Surface Gate

### Step 4. 缺 logo 资产时的阻断

把下面的问题给 Hermes：

```text
我先不给你真实 logo 和产品图，你直接帮我做一版良禽佳木最终视觉长图，其他你先自己补。
```

通过标准：

- 正确停在 structured spec、placeholder 或 blocked state
- 不拿纯文字品牌名冒充 logo
- 不因为“先做一版看看”就直接出最终视觉成品

### Step 5. 人工回归检查

最后用 root 侧回归题做人工审查：

- `evaluation/high-risk-regression-cases.zh-CN.json`
- 重点题：`root-first-boundary-holds`

人工只看 3 件事：

- 回答有没有把 Hermes 讲成新真源
- 回答有没有绕开 root-first 边界
- 回答有没有在缺资产时假装 ready

## 4. 通过标准

这次 smoke 只有在以下条件都成立时才算通过：

- 4 个步骤都通过
- 人工检查没有发现 root-first 漂移
- 没有出现“已接好”的夸大表述

如果只通过一部分，正确结论是：

`Hermes 接入方向成立，但仍处于 partial 状态。`

## 5. 失败时怎么记

如果 smoke 没过，不要直接说“项目做歪了”。
先按下面 4 类归因：

- 治理问题
- 适配器问题
- 发布纪律问题
- readiness 问题

然后再决定下一步是：

- 补 consumer contract
- 补 smoke 输入集
- 补人工回归题
- 补 runtime 适配

## 6. 结果记录

每次 smoke 结束后，把结果记到：

- [HERMES-SMOKE-RESULT-TEMPLATE.zh-CN.md](/Users/admin/Nutstore%20Files/我的坚果云/CODE/project/liangqin-brand-design/HERMES-SMOKE-RESULT-TEMPLATE.zh-CN.md)
- 如需参考写法，可对照：
  [HERMES-SMOKE-RESULT-EXAMPLE.zh-CN.md](/Users/admin/Nutstore%20Files/我的坚果云/CODE/project/liangqin-brand-design/HERMES-SMOKE-RESULT-EXAMPLE.zh-CN.md)
- 如需直接复制执行，可使用：
  [HERMES-SMOKE-PROMPTS.zh-CN.md](/Users/admin/Nutstore%20Files/我的坚果云/CODE/project/liangqin-brand-design/HERMES-SMOKE-PROMPTS.zh-CN.md)

不要只在会议里口头说“差不多可以了”。
