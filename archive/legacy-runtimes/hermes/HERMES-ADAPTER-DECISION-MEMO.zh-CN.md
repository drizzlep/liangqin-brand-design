# Hermes Adapter Decision Memo

这份 memo 用来回答一个具体问题：

`后面如果继续推进 Hermes，到底什么时候应该起独立 adapter，什么时候不应该起？`

它不是 adapter 实现文档。
它只负责给团队一个稳定的决策框架，避免还没跑通 consumer contract 和 smoke，就过早扩成第二套系统。

## 当前结论

截至 2026-04-24：

- 不建议立即起独立 Hermes adapter
- 更合适的顺序是：
  1. 先确认 root-first 组织口径
  2. 先按 `HERMES-CONSUMER-CONTRACT.zh-CN.md` 跑 smoke
  3. 先拿到最小 runtime 证据
  4. 再决定是否需要独立 adapter 形态

一句话：

`先证明 Hermes 能稳定消费同一套 root package，再讨论要不要给它单独外壳。`

## 为什么现在不建议立刻起 adapter

### 1. 当前最大缺口不是“没有壳”，而是“没有证据”

现在仓库已经有：

- root package
- 轻量 `DESIGN.md` 默认入口
- preflight 高级参考
- tier 边界
- delivery gates
- 高层治理回归题
- Hermes smoke playbook

现在缺的是：

- Hermes runtime smoke proof
- Hermes 真实消费行为证据
- Hermes 是否真的需要独立协议镜像或安装形态的判断

所以现在直接起 adapter，很容易把“还没验证的接入假设”误包装成“已经成立的产品结构”。

### 2. 过早起 adapter，最容易带来第二真源风险

一旦太早起独立 adapter，最常见的问题是：

- 在 adapter 文档里先补规则
- 在 adapter 目录里先做运行时妥协
- 最后 root 反而变成追认者

这和当前项目一直在防的风险完全相反。

### 3. OpenClaw 的 adapter 条件目前并不自动适用于 Hermes

OpenClaw 之所以已经适合有独立 adapter，是因为它已经具备：

- 清晰的分发目标
- 明确的安装方式
- 可运行的镜像同步链
- validator 与 release tests
- 对外稳定的 package slug

Hermes 目前这些都还没有 runtime 证据支撑。

## 什么时候“不该”起独立 adapter

只要出现下面任一情况，就不该起：

- 还没跑完第一次 Hermes smoke
- 还没有最小 runtime 证据
- 还无法证明 Hermes 会稳定遵守 root-first 边界
- 还不清楚 Hermes 是否真的需要独立安装包、镜像协议或发布链
- 团队还在把“消费合同”和“adapter 实现”混着说

这几个条件下，继续留在 consumer contract 阶段更安全。

## 什么时候“可以考虑”起独立 adapter

只有下面条件大体同时成立，才值得进入 adapter 决策：

### A. smoke 已通过

- 已按 `HERMES-SMOKE-PLAYBOOK.zh-CN.md` 跑完
- 结果已记录到 `HERMES-SMOKE-RESULT-TEMPLATE.zh-CN.md`
- 结论不是空泛的“差不多可以”，而是有明确通过/partial/未通过

### B. Hermes 有稳定的独特运行需求

例如：

- 需要独立安装路径
- 需要独立协议镜像
- 需要 Hermes 专用运行时元数据
- 需要独立导出或发布链

如果只是“也能读 root package”，那还不构成必须起 adapter 的理由。

### C. 可以明确证明 adapter 只是消费层

准备起 adapter 时，必须能先回答清楚：

- 它消费哪些 root 文件
- 它为什么不能反向定义标准
- 它的镜像或协议哪些是 runtime 语境，哪些绝不是新真源

### D. 能给 adapter 配套治理保护

至少要能预想到这些保护面：

- source_of_truth 回指
- mirror_role / package_role 声明
- 最小 validator
- 最小 smoke 或回归检查
- 文档里明确写清 “adapter != truth”

如果这些都还说不清，就还不该起。

## 推荐决策树

### 路径 A：先不建 adapter

适用条件：

- 还在第一次 smoke 阶段
- 目标只是验证 Hermes 能不能稳定消费 root package
- 还没有独立安装/分发需求

结论：

继续保留：

- consumer contract
- smoke playbook
- result template

不要过早扩目录结构。

### 路径 B：进入 adapter 评估

适用条件：

- smoke 已经通过
- Hermes 有稳定独特 runtime 需求
- 团队能清楚说出 adapter 的消费边界与非真源边界

结论：

可以进入“是否起独立 adapter”的详细设计阶段，但仍不等于马上实现。

### 路径 C：明确起 adapter

适用条件：

- smoke 已通过
- 有独立分发/安装/协议需求
- 有办法建立最小 validator 和回指 root 的约束
- 团队已经接受 root-first 不可动摇

结论：

这时才适合进入真正的 adapter 规划。

## 当前建议动作

当前最推荐的动作仍然是：

1. 先确认 root-first 组织口径
2. 先跑 Hermes smoke
3. 先拿到真实结果记录
4. 再开一次小会，只讨论：
   `Hermes 是否已经满足进入 adapter 评估的条件`

## 默认结论模板

如果你们会里要快速落一句话，建议直接用这句：

`当前先不立刻起 Hermes adapter；先证明 Hermes 能稳定消费同一套 root package，等 smoke 和 runtime 证据成立后，再决定是否需要独立 adapter 形态。`
