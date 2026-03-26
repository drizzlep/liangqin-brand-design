# 良禽佳木品牌设计规范与 OpenClaw Skill

这个仓库包含两层资产：

1. **设计规范层**
   - `foundation-dna/`
   - `index.html`
   - `components.html`
   - `product-detail.html`
   - `case-detail.html`

2. **OpenClaw 协议层**
   - `skills/public/liangqin-brand-openclaw/`

## 适用目标

把良禽佳木现有设计规范升级为一个**品牌专用 OpenClaw Skill**，让其他 OpenClaw 机器人可以：

- 吃品牌 brief、产品资料、参考页面
- 输出首页 / 产品详情的结构化蓝图
- 在固定模块库内继续生成页面
- 更稳定地“像良禽佳木”

## Skill 入口

- Skill 文件：`skills/public/liangqin-brand-openclaw/SKILL.md`
- 输入协议：`skills/public/liangqin-brand-openclaw/protocols/input-contract.zh-CN.json`
- 模块库：`skills/public/liangqin-brand-openclaw/recipes/module-recipes.zh-CN.json`
- 黄金样例：`skills/public/liangqin-brand-openclaw/examples/`
- 真实设计案例：`skills/public/liangqin-brand-openclaw/examples/real-cases/`

## 导出给其他 OpenClaw 使用

```bash
python3 scripts/export_openclaw_skill.py --output-dir ./dist
```

导出后会生成：

- `dist/liangqin-brand-openclaw/`

这个目录可以直接复制到其他 OpenClaw 的 skills 目录中使用。

## 本地校验

```bash
python3 -m unittest tests/test_liangqin_brand_skill_assets.py -v
python3 -m unittest tests/test_liangqin_brand_skill_distribution.py -v
python3 skills/public/liangqin-brand-openclaw/scripts/validate_skill_assets.py
```

## 当前 v1 范围

- 只服务良禽佳木
- 只覆盖首页与产品详情
- 固定模块库优先
- 先做人工评测与黄金样例
- 第一目标是“更像品牌”，不是“生成更多页面”
