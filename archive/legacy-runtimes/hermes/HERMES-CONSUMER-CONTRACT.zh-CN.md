# Hermes 消费合同（草案）

这份文档用于约束 Hermes 未来如何消费这套良禽佳木跨工具标准包。

它不是 Hermes adapter，也不是新的品牌入口。
它只回答一件事：
Hermes 如果要接入，必须按什么边界读取、降级、交付，才不会把项目重新带偏。

## 1. 角色定义

- root package 仍是品牌本体
- 轻量 `DESIGN.md` 仍是默认主入口
- `AGENT-PREFLIGHT.zh-CN.md` 是高保真 / adapter 接入参考，不是普通请求默认必读
- Hermes 只能被定义为消费者 / 适配器候选，不是第二品牌系统
- Hermes 不得反向定义品牌规则、资产规则、pack 语义或交付 gate

一句话：

`root 定义标准，Hermes 只负责消费标准。`

## 2. 最小读取集

Hermes 默认先按轻量 `Tier 1` 方式消费 `DESIGN.md`。只有当任务需要高保真交付、adapter 接入、资产校验或回归验收时，才逐步补读更深层文件；不能把“目标可升级到 Tier 3”说成“当前已经满足 Tier 3”。

### Hermes 轻量最小输入

1. `DESIGN.md`

只读这一项时，Hermes 应明确自己处于轻量品牌地图消费状态。

### Hermes 做 adapter / 跨工具接入时追加

2. `AGENT-PREFLIGHT.zh-CN.md`
3. `CONSUMER-GUIDE.zh-CN.md`
4. `design-standard-package.json`

### Hermes 做视觉交付时追加

5. `artifact-surfaces/*.json`
6. `assets/brand/asset-manifest.zh-CN.json`
7. `EXECUTION-CHECKLIST.md`

### Hermes 做高保真或回归验收时追加

8. `foundation-dna/design-dna.zh-CN.json`
9. `foundation-dna/tokens.semantic.json`
10. `evaluation/manual-rubric.zh-CN.md`
11. `evaluation/human-review-protocol.zh-CN.md`
12. `evaluation/high-risk-regression-cases.zh-CN.json`

## 3. 读取顺序

Hermes 的默认读取顺序是：

`DESIGN.md -> 按任务需要补读 preflight / consumer guide / artifact-surfaces / assets / evaluation`

内部治理和冲突优先级仍保持：

`Foundation DNA > DESIGN.md > artifact-surfaces > design-packs > examples`

补充说明：

- `design-packs/` 只在确有探索需求时打开
- `artifact-surfaces/` 只负责载体约束，不负责重定义品牌
- `examples/` 只做验收与边界校准，不做直接模板复制

## 4. 交付纪律

普通轻量请求不需要把所有 delivery gates 都显式展开。高保真、分发或回归验收时，Hermes 必须复用根层既有 delivery gates：

1. `Context Gate`
2. `Surface Gate`
3. `Variation Gate`
4. `Material Gate`
5. `Runtime Gate`
6. `Verification Gate`
7. `Handoff Gate`

不能自创一套“更快的 Hermes 流程”绕开这些 gate。

## 5. 降级规则

如果 Hermes 不具备完整理解或执行能力，必须显式降级：

- 只读 `DESIGN.md` 时，只能按轻量 `Tier 1` 自居
- 只读 `DESIGN.md + AGENT-PREFLIGHT.zh-CN.md` 时，仍不能越级宣称自己已满足 `Tier 2` 或 `Tier 3`
- 未读取 `artifact-surfaces/` 与 `assets/brand/` 时，不得产出最终视觉成品
- 未读取真实 logo 资产时，只能停在 structured spec、placeholder 或 blocked state
- 无法稳定控制图标、中文 UI、交付载体时，应减少细节，而不是自由发挥
- 无法完成高保真链路时，应明确说自己当前停在 `partial`，而不是假装已经满足 `Tier 3`

## 6. Hermes 不得做的事

- 不得把自己声明为新的品牌入口
- 不得维护独立于 root package 的品牌边界文档
- 不得为了适应 Hermes 运行限制而切换品牌语言
- 不得在缺少真实资产或产品事实时直出高保真成品
- 不得把参考页、黄金样例或 adapter 文档当成新真源

## 7. 建议的 smoke path

Hermes 真正接入前，先只跑一个最小 smoke path，不要一开始就做完整 adapter：

### Smoke 目标

验证 Hermes 能否在不偏离 root-first 边界的前提下，稳定消费同一套标准包。

### 建议步骤

1. 先只读取 `DESIGN.md`
2. 明确声明自己当前属于 `Tier 1`、`Tier 2` 还是 `Tier 3`
3. 说明哪些任务需要补读 preflight、consumer guide、surfaces、assets 或 evaluation
4. 对一个视觉请求先输出 structured spec
5. 对一个缺 logo 资产的请求正确停在 blocked / spec
6. 对一个多机器人边界问题明确回答：
   `root 是品牌本体，Hermes 只是消费者`
7. 用 `evaluation/high-risk-regression-cases.zh-CN.json` 中的 `root-first-boundary-holds` 回归题做一次人工检查

### Smoke 通过标准

- 没有把 Hermes 说成新真源
- 没有把 preflight 与 delivery gates 当成普通请求默认负担，也没有在高保真时绕过它们
- 没有在缺资产时假装能出最终视觉
- 没有把多机器人扩展讲成“各自一套品牌系统”

## 8. 当前状态声明

截至 2026-04-24，这份文档只是消费合同草案，不代表：

- Hermes adapter 已存在
- Hermes runtime 已验证
- 多机器人接入已经完成

当前更准确的说法是：

`Hermes 接入边界已经定义，runtime smoke 仍待补证据。`
