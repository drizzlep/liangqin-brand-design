# 良禽佳木品牌设计 Skill 本地部署安装说明

## 1. 适用对象

这份说明适用于：

- OpenClaw 跑在自己电脑上
- 可以直接打开终端
- 可以直接操作 `~/.openclaw/`

## 2. 从源码仓库安装

```bash
git clone <你的 GitHub 仓库地址>
cd liangqin-brand-design
python3 skill/liangqin-brand-design/scripts/publish_skill.py           --source "$PWD/skill/liangqin-brand-design"
```

执行后会同步到：

- `~/.openclaw/skills/liangqin-brand-design`
- `~/.openclaw/workspace/skills/liangqin-brand-design`

## 3. 从 zip 安装

先在仓库里打包：

```bash
bash scripts/package_openclaw_skill.sh
```

然后在目标机器上：

```bash
mkdir -p ~/.openclaw/skills
unzip dist/liangqin-brand-design-openclaw-YYYYMMDD.zip -d ~/.openclaw/skills
python3 ~/.openclaw/skills/liangqin-brand-design/scripts/publish_skill.py
```

## 4. fresh 测试

```bash
python3 ~/.openclaw/skills/liangqin-brand-design/scripts/refresh_and_test.py
```

如果要换成自己的测试语句：

```bash
python3 ~/.openclaw/skills/liangqin-brand-design/scripts/refresh_and_test.py           --message "请用良禽品牌设计体审查并纠偏这份首页方案"
```
