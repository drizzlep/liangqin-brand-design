# 运行时接入

本技能遵循 Agent Skills 约定，接入任何 runtime 都只需要同一件事：**把 `liangqin-brand-body/` 整个目录放进该 runtime 的 skills 目录。**

不需要为单个 runtime 改 `SKILL.md`，也不需要额外脚本。只有接入一个全新 runtime 时，才在这里补一节说明。

## 接入契约

| 项 | 要求 |
|---|---|
| 目录名 | `liangqin-brand-body`，必须与 `SKILL.md` frontmatter 的 `name` 一致 |
| 入口 | `SKILL.md`，含 `name` 与 `description` |
| 触发 | 由 `description` 决定，包含中文与英文触发词 |
| 默认上下文 | `DESIGN.md` |
| 可选资源 | `assets/brand/`、`tokens/`、`preview.html` |
| 外部依赖 | 无。不要求 node、python、网络或任何 CLI |

## 常见安装位置

| Runtime | skills 目录 |
|---|---|
| Claude Code | `~/.claude/skills/liangqin-brand-body/` |
| Codex | `~/.codex/skills/liangqin-brand-body/` |
| WorkBuddy | `~/.workbuddy/skills/liangqin-brand-body/` |
| CodeBuddy | `~/.codebuddy/skills/liangqin-brand-body/` |
| Qoder | `~/.qoder/skills/liangqin-brand-body/` |
| Cursor | `~/.cursor/skills/liangqin-brand-body/` |
| Gemini CLI | `~/.gemini/skills/liangqin-brand-body/` |
| 通用 agent skills | `~/.agents/skills/liangqin-brand-body/` |
| CC Switch（本机分发源） | `~/.cc-switch/skills/liangqin-brand-body/` |

批量同步用仓库里的 `scripts/sync_runtimes.py`，默认只做 dry-run。

## 能力分级

| 级别 | runtime 特征 | 期望行为 |
|---|---|---|
| **L1** | 只把 `SKILL.md` 正文注入上下文，不能读文件 | 依据 `SKILL.md` 内嵌的品牌摘要输出结构化方向与规格，明确说明没有读取完整规范 |
| **L2** | 能读技能目录内的文件 | 读 `DESIGN.md`，必要时读 `assets/brand/` 与 `examples/`，产出可交付内容 |
| **L3** | 能跑脚本、开浏览器、做视觉验收 | 在 L2 基础上补真实渲染与响应式检查，并给出验收证据 |

如果 runtime 只支持单文件注入，把 `DESIGN.md` 的正文一并注入即可获得接近 L2 的效果。

## 项目级接入（不使用 skill 机制时）

Google Stitch 与 `awesome-design-md` 生态的用法是：**把 `DESIGN.md` 复制到项目根目录，然后要求 AI 按它做。**

```bash
cp DESIGN.md /path/to/your-project/DESIGN.md
```

适合以下情况：

- 目标工具不读 skills 目录，只读项目文件（Stitch、部分网页版 AI 工具）
- 希望规范随项目走，而不是跟着某个 runtime 走
- 需要团队在代码评审里同时评审视觉规范

如果项目同时使用 `AGENTS.md` / `CLAUDE.md`，在其中一个文件里加一行指向 `DESIGN.md` 即可，不必复制规范正文。

## 已停止维护的适配

OpenClaw 与 Hermes 的适配说明、安装脚本和 smoke 记录已移出本技能，归档在仓库 `archive/legacy-runtimes/`。它们不再随包发行，也不参与默认读取路径。将来需要重新接入时，按上面的接入契约新增一节即可，不需要恢复旧文件。
