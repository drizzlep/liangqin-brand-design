# 良禽品牌体 GitHub 发布手册

这份手册用于把当前仓库发布成一个**可被其他 OpenClaw 机器人直接安装的版本化技能包**。

## 当前发布定位

- GitHub 仓库：`drizzlep/liangqin-brand-design`
- 对外技能名：`良禽品牌体`
- 对外安装包 slug：`liangqin-brand-body`
- 推荐版本策略：仓库 Release Tag 与 `skill-release.json` 保持一致

这次升级建议直接发布为：

- `v2.0.0`

原因：

- 对外入口从 `liangqin-brand-openclaw` 收口为 `良禽品牌体`
- 控制面从旧协议层升级为 `DESIGN.md` 主导
- 增加了标准发行元数据、安装脚本与 zip 包交付方式
- 对其他 OpenClaw 机器人来说，这是一次明确的分发方式升级，不是小修补

## 标准发布流程

### 1. 先生成发行包

```bash
python3 scripts/prepare_openclaw_release.py
```

默认会生成：

- `dist/liangqin-brand-body/`
- `dist/liangqin-brand-body-2.0.0.zip`

### 2. 跑校验

```bash
python3 -m unittest tests/test_liangqin_brand_skill_assets.py tests/test_liangqin_brand_skill_distribution.py tests/test_design_md_adapter.py -v
python3 skills/public/liangqin-brand-openclaw/scripts/validate_skill_assets.py
```

### 3. 提交代码

```bash
git add .
git commit -m "release: ship 良禽品牌体 v2.0.0"
git push origin HEAD
```

### 4. 打 Tag 并推送

```bash
git tag v2.0.0
git push origin v2.0.0
```

### 5. 到 GitHub 创建 Release

仓库地址：

- [drizzlep/liangqin-brand-design](https://github.com/drizzlep/liangqin-brand-design)

Release 页面：

- [GitHub Releases](https://github.com/drizzlep/liangqin-brand-design/releases)

上传资产：

- `dist/liangqin-brand-body-2.0.0.zip`

## 建议的 GitHub Release 标题

```text
v2.0.0 · 良禽品牌体单入口版
```

## 建议的 GitHub Release 正文

```md
## Summary

- upgrade the Liangqin OpenClaw distribution to a single public entry: `良禽品牌体`
- switch the default design governance to `DESIGN.md`-led control
- add release metadata, packaged zip distribution, and one-command OpenClaw installer
- preserve `良禽佳木apple风` as a controlled style trigger inside the unified skill

## What Changed

- public entry keyword is now `良禽品牌体`
- packaged skill slug is now `liangqin-brand-body`
- exported bundle now includes:
  - `DESIGN.md`
  - `DESIGN-GOVERNANCE.md`
  - `foundation-dna/design-dna.zh-CN.json`
  - `design-packs/`
  - `protocols/`
  - `recipes/`
  - `examples/`
  - `evaluation/`
  - `skill-release.json`
  - `scripts/install_into_openclaw.py`

## Upgrade Notes

- old name `liangqin-brand-openclaw` is now treated as a legacy compatibility reference
- new usage pattern:
  - `请使用良禽品牌体`
  - optional style trigger: `良禽佳木apple风`
- install with:

```bash
python3 scripts/install_into_openclaw.py
```

## Verification

- `python3 -m unittest tests/test_liangqin_brand_skill_assets.py tests/test_liangqin_brand_skill_distribution.py tests/test_design_md_adapter.py -v`
- `python3 skills/public/liangqin-brand-openclaw/scripts/validate_skill_assets.py`
```

## 给其他 OpenClaw 机器人的交付说明

建议不要写得太技术化，直接告诉对方 3 件事就够了：

### 1. 这是什么

```md
`良禽品牌体` 是一个面向 OpenClaw 的品牌设计技能包。

它不是单纯的文案模板，也不是单页案例集，而是一套由 `DESIGN.md` 主导的品牌执行系统。
它会把良禽佳木的品牌 DNA、风格包和页面蓝图规则压成一个统一入口，供机器人生成更稳定的品牌页面结果。
```

### 2. 怎么安装

```md
1. 下载 Release 里的 `liangqin-brand-body-2.0.0.zip`
2. 解压后进入目录
3. 运行：

```bash
python3 scripts/install_into_openclaw.py
```

它会自动安装到：

- `~/.openclaw/skills/liangqin-brand-body`
- `~/.openclaw/workspace/skills/liangqin-brand-body`
```

### 3. 怎么使用

```md
默认入口词：

- `请使用良禽品牌体`

如果要切换风格，再补充风格词：

- `良禽佳木apple风`

推荐调用方式：

- 先说明任务类型，例如：首页 / 产品详情 / 品牌页
- 再给品牌 brief、产品资料、参考页面
- 如需风格偏移，再补充风格词
```

## 入口降级说明

为了真正做到“只剩一个品牌入口”，建议把旧的写作类 skill 统一降级成次级能力，并明确告知使用方：

- `良禽品牌体` 是唯一顶层品牌入口
- 公关稿、品牌通稿、`/小强体`、`/厂长模式`、`/硬核木匠` 这类能力只负责写作输出
- 旧写作 skill 不应用来接首页、产品详情、品牌页、`DESIGN.md`、页面蓝图、风格切换这类请求
- 只有当用户明确提出“写稿”“写文章”“写传播文案”时，才应路由到这些次级能力

你可以直接把下面这段发给其他 OpenClaw 使用方：

```md
默认只把 `良禽品牌体` 作为顶层品牌入口。

如果任务是首页、产品详情、品牌页、设计系统、页面蓝图、风格切换，请直接使用 `良禽品牌体`。

旧的公关稿、品牌通稿、`/小强体`、`/厂长模式`、`/硬核木匠` 仅保留为次级写作能力，
只在明确写稿或写文章时触发，不再承担品牌主入口职责。
```

## 对外最容易理解的一句话升级说明

你可以直接这样写：

```text
v2.0.0 把原来的良禽品牌设计能力收口成一个统一入口“良禽品牌体”，并升级为 DESIGN.md 主导的单入口分发版本；安装更简单、调用更一致、后续风格扩展也更容易。
```
