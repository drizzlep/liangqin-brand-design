# 本机 Skill 维护流程

这个流程用于维护 `良禽品牌体`、`Impeccable` 以及它们在 CC Switch、Codex、Claude、OpenClaw、Hermes 里的运行副本。默认原则是：自动发现、自动出计划、人工确认后再应用。

## 为什么不是全自动覆盖

Skill 不是普通依赖包。它会影响触发词、模型可见指令、Hermes snapshot、OpenClaw discovery 和 CC Switch DB。上游新增 `SKILL.md`、命令、参考文件或兼容 wrapper 时，必须先判断它属于核心入口、兼容 wrapper、可选参考还是外部依赖，不能直接写进良禽品牌真源。

## 日常检查

```bash
python3 scripts/maintain_local_skills.py check
```

检查内容：

- `liangqin-brand-body` 的仓库源版本、CC Switch、Codex、Claude、OpenClaw、Hermes 是否一致。
- 默认只检查各运行副本之间是否一致；不会把仓库里的 `dist/` 当作真源，因为 `dist/` 是可重新生成的发行产物。
- 旧入口 `liangqin-brand-openclaw` 是否又出现在活跃 roots。
- `impeccable` 是否仍解析到 `~/.cc-switch/skills/impeccable`，并保持新版主入口。
- CC Switch DB 是否有对应记录。
- Hermes prompt snapshot 是否还缓存旧入口。

如果已经通过 `export_openclaw_skill.py` 或 `prepare_openclaw_release.py` 生成了新的候选包，再显式指定候选包做对照：

```bash
python3 scripts/maintain_local_skills.py check \
  --candidate liangqin-brand-body=/path/to/liangqin-brand-body
```

只有这种情况下，脚本才会判断运行副本是否已经同步到该候选发行包。

## 检查上游新增内容

如果已经拉取或下载了上游候选目录，使用：

```bash
python3 scripts/maintain_local_skills.py check-upstream \
  --upstream impeccable=/path/to/upstream/impeccable \
  --upstream-only
```

报告会比较：

- 新增或删除的 `SKILL.md`。
- 新增或删除的 `reference/`、`references/`、`commands/`、`protocols/`、`recipes/`、`examples/`、`evaluation/`、`scripts/` 等文件。
- 新增或删除的 `command-metadata.json` 与命令名。
- 版本变化。

新增入口、命令和 command metadata 默认进入 `manual_review`，新增普通参考文件进入 `report_only`。这样可以发现新能力，但不会自动把外部规则合进良禽品牌真源。

如果你同时想看本机运行副本状态，可以去掉 `--upstream-only`；但做上游差异判断时建议保留它，避免临时目录或测试目录中的本地安装缺失噪声混入报告。

## 生成维护计划

```bash
python3 scripts/maintain_local_skills.py plan \
  --upstream impeccable=/path/to/upstream/impeccable
```

计划里的动作分三类：

- `repair_candidate`：本机安装层可修的问题，例如旧入口复活、版本不一致、Hermes snapshot 污染。
- `manual_review`：需要人工判断的问题，例如上游新增子 skill、命令、删除已有参考。
- `report_only`：只提示，不建议立即应用，例如上游新增普通参考文件。

## 推荐维护节奏

- 每周或每次升级前跑一次 `check`。
- 上游有新 release 时，先拉到临时目录，再跑 `check-upstream`。
- 只有当计划报告确认无品牌真源污染风险后，再执行导出、覆盖、DB 更新和运行时验证。
- 更新后重启 Codex、OpenClaw、Hermes 相关会话，清掉已加载进程的 skill 缓存。
