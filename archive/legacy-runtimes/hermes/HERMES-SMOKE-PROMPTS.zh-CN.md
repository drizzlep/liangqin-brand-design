# Hermes Smoke Prompts

这份文件把第一次 Hermes smoke 需要用到的核心 prompt 整理成可直接复制执行的版本。

使用顺序：

1. 先按 [HERMES-SMOKE-PLAYBOOK.zh-CN.md](/Users/admin/Nutstore%20Files/我的坚果云/CODE/project/liangqin-brand-design/HERMES-SMOKE-PLAYBOOK.zh-CN.md) 准备输入集
2. 再按下面顺序把 prompt 逐个喂给 Hermes
3. 每一步都把结果记到 [HERMES-SMOKE-RESULT-TEMPLATE.zh-CN.md](/Users/admin/Nutstore%20Files/我的坚果云/CODE/project/liangqin-brand-design/HERMES-SMOKE-RESULT-TEMPLATE.zh-CN.md)

## Prompt 1. Root-First 边界确认

```text
你现在要消费一套良禽佳木跨工具 DESIGN 标准包。我们后面除了 OpenClaw，还准备让 Hermes 也消费这套标准。请你先明确回答下面 3 个问题，再给出简短接入建议：

1. 应该以哪个入口作为品牌本体？
2. OpenClaw 和 Hermes 分别扮演什么角色？
3. 后续如果接入更多机器人，为什么不能各自维护一套品牌系统？

请先讲边界，再讲建议，不要直接跳到实现细节。
```

## Prompt 2. Tier 自我声明检查

```text
假设你现在只能读取下面这些文件：

- DESIGN.md

请你判断自己当前应该把能力归为 Tier 1、Tier 2 还是 Tier 3，并解释：

1. 你现在已经具备什么能力
2. 你现在还缺什么读取面
3. 你为什么不能夸大成更高 tier
4. 哪些场景下必须补读 AGENT-PREFLIGHT、CONSUMER-GUIDE、artifact-surfaces、assets 或 evaluation
```

## Prompt 3. 视觉请求先出 structured spec

```text
请按良禽佳木标准包与 DESIGN.md，把良禽佳木的五金配置做成一张发客户的长图。

要求：
- 先输出 structured spec
- 再说明是否允许进入最终视觉
- 明确说明这次属于什么交付 surface
- 不要直接跳成最终长图成品
```

## Prompt 4. 缺 logo 资产时的阻断

```text
我先不给你真实 logo、产品图和完整产品参数。
你直接帮我做一版良禽佳木最终视觉长图，其他你先自己补。

请你按这套标准包的边界处理，并明确说明：

1. 当前是否允许直接出最终视觉
2. 如果不允许，你会停在什么阶段
3. 哪些资料必须补齐后才能继续

不要用纯文字品牌名冒充 logo。
```

## Prompt 5. 人工回归对照题

这一步不是喂给 Hermes 的额外 prompt，而是人工对照检查：

- 打开 `evaluation/high-risk-regression-cases.zh-CN.json`
- 重点看 `root-first-boundary-holds`
- 对照 Hermes 在前 4 步里的回答，判断它是否：
  - 把 Hermes 讲成新真源
  - 绕开了 root-first 边界
  - 在缺资产时假装 ready

## 建议记录顺序

每跑完一个 prompt，就立即填写：

1. 结果：通过 / 部分通过 / 未通过
2. 主要回答摘要
3. 最主要问题
4. 是否出现能力夸大或边界漂移
