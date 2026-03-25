# liangqin-brand-design

良禽佳木 OpenClaw 品牌设计 Skill 独立仓库。

这个仓库面向两类用途：

- 安装可直接使用的良禽佳木品牌设计 Skill
- 维护品牌设计 DNA、审查规则、发布脚本和安装器

## 适用场景

这个 Skill 适合下面这类任务：

- 请用良禽品牌设计体重做这份视觉
- 改成良禽佳木品牌设计
- 审查当前页面 / 海报 / 内容图是否符合良禽佳木品牌规范
- 先指出偏差，再按良禽佳木品牌气质纠偏

默认工作流：**先审查，再改写**。

## 仓库结构

- `skill/liangqin-brand-design/`：可发布到 OpenClaw 的 Skill 本体
- `scripts/`：打包 zip、生成单文件安装器等仓库级脚本
- `docs/`：安装说明、设计说明、实现计划
- `dist/`：打包产物目录

## 最常用的两件事

### 1. 打包 zip

```bash
bash scripts/package_openclaw_skill.sh
```

### 2. 生成单文件安装器

```bash
bash scripts/build_single_file_installer.sh
```

## 安装到另一个 OpenClaw

### 方式一：从源码仓库安装

```bash
git clone <你的 GitHub 仓库地址>
cd liangqin-brand-design
python3 skill/liangqin-brand-design/scripts/publish_skill.py           --source "$PWD/skill/liangqin-brand-design"
```

### 方式二：先生成单文件安装器，再交给 OpenClaw 安装

```bash
bash scripts/build_single_file_installer.sh
```

生成后会得到一个文件，例如：

```bash
dist/liangqin-brand-design-installer-YYYYMMDD.sh
```

可以把下面这段话直接发给 OpenClaw：

```text
请运行 /绝对路径/liangqin-brand-design-installer-YYYYMMDD.sh，把良禽佳木品牌设计 skill 安装到 shared skills，并同步到 workspace。安装完成后再做一次 fresh 测试，确认 skill 已经生效。
```

## 推荐 GitHub 发布方式

远程仓库名建议直接使用：`liangqin-brand-design`

本地若为避免与现有设计项目目录重名，可使用其他本地目录名；真正发布到 GitHub 时再使用上面的仓库名即可。
