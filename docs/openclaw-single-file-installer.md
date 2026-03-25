# 良禽佳木品牌设计 Skill 单文件安装器说明

## 1. 这是什么

这是把整个良禽佳木品牌设计 Skill 打成一个 shell 文件的安装方案。

生成后会得到一个文件，例如：

```bash
dist/liangqin-brand-design-installer-YYYYMMDD.sh
```

## 2. 生成命令

```bash
bash scripts/build_single_file_installer.sh
```

## 3. OpenClaw 安装示例

如果环境允许 OpenClaw 执行本地 shell 命令，可以直接说：

```text
请运行 /绝对路径/liangqin-brand-design-installer-YYYYMMDD.sh，把良禽佳木品牌设计 skill 安装到 shared skills，并同步到 workspace。安装完成后再做一次 fresh 测试。
```

## 4. 可选参数

- `--skills-root`：自定义 shared skills 根目录
- `--workspace-dest`：自定义 workspace 技能目录
- `--skip-test`：安装后不自动跑 smoke test
- `--message`：自定义 smoke test 用语
