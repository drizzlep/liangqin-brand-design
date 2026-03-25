# 良禽佳木品牌设计 Skill 设计文档

**日期：** 2026-03-25

## 目标

构建一个可独立发布到 GitHub、可被其他 OpenClaw 安装的良禽佳木品牌设计 Skill。

## 定位

- 品牌专用：只服务良禽佳木品牌语境
- 使用场景：通用品牌设计执行 + 设计审查/纠偏
- 默认流程：先审查，再改写

## 仓库形态

采用独立仓库 + Skill 子目录 + 打包脚本的模式，兼容：

- GitHub 源码安装
- zip 打包交付
- 单文件安装器交付

## Skill 核心职责

1. 按良禽佳木品牌 DNA 执行设计
2. 审查已有视觉是否偏离品牌规范
3. 先指出偏差，再给纠偏方案与修正版

## references 拆分

- `brand-dna.md`：品牌气质与设计锚点
- `execution-rules.md`：任务执行流程与输出约束
- `review-checklist.md`：审查维度与输出格式
- `anti-patterns.md`：禁止滑向的错误风格
- `page-and-poster-patterns.md`：常见载体的落地模式

## 交付要求

- 提供可发布到 `~/.openclaw/skills/liangqin-brand-design` 的 Skill 本体
- 提供发布脚本，同步到 workspace
- 提供最小 smoke test
- 提供仓库 README 与安装文档
