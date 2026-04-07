# 良禽佳木品牌设计规范与 良禽品牌体

这个仓库包含五层资产：

1. **Foundation DNA 真源层**
   - `foundation-dna/`
   - `components.html`
   - `product-detail.html`
   - `case-detail.html`
   - `quote-card-detail.html`

2. **Design Pack 风格层**
   - `design-packs/`

3. **AI 设计消费层**
   - `DESIGN.md`
   - `DESIGN-GOVERNANCE.md`
   - `design-preview.html`
   - `index.html`
   - `scripts/export_design_md.py`

4. **Artifact Surface 载体层**
   - `artifact-surfaces/`
   - `artifact-web-brand-landing.html`
   - `artifact-mobile-h5-consultation.html`
   - `artifact-quote-card-editorial.html`

5. **OpenClaw 协议层**
   - `skills/public/liangqin-brand-openclaw/`

## 适用目标

把良禽佳木现有设计规范升级为一个**品牌专用 OpenClaw Skill**，让其他 OpenClaw 机器人可以：

- 吃品牌 brief、产品资料、参考页面
- 输出首页 / 产品详情的结构化蓝图
- 在固定模块库内继续生成页面
- 更稳定地“像良禽佳木”

## 对外入口

- 对外唯一入口词：`良禽品牌体`
- 内部源目录：`skills/public/liangqin-brand-openclaw/`
- Skill 文件：`skills/public/liangqin-brand-openclaw/SKILL.md`
- 输入协议：`skills/public/liangqin-brand-openclaw/protocols/input-contract.zh-CN.json`
- 模块库：`skills/public/liangqin-brand-openclaw/recipes/module-recipes.zh-CN.json`
- 黄金样例：`skills/public/liangqin-brand-openclaw/examples/`
- 真实设计案例：`skills/public/liangqin-brand-openclaw/examples/real-cases/`

命名策略：

- 仓库内部暂时保留旧源目录名，避免一次性打碎路径与测试
- 对外发行包统一改为 `liangqin-brand-body`
- 对话里只推荐使用 `良禽品牌体`
- `liangqin-brand-openclaw` 只保留为历史兼容说明

## 系统层级关系

- `foundation-dna/`：品牌真源
- `DESIGN.md`：AI 默认设计输入
- `DESIGN-GOVERNANCE.md`：AI 读取协议
- `design-preview.html` / `index.html`：人工预览层
- `design-packs/`：受控变化层
- `artifact-surfaces/` 与 `artifact-*.html`：具体载体校验层
- `skills/public/liangqin-brand-openclaw/`：结构化执行层

读取顺序、层级职责与冲突处理统一以根目录 `DESIGN-GOVERNANCE.md` 为准。

默认优先级：`Foundation DNA > DESIGN.md > artifact-surfaces > design-packs > examples`

补充约定：
- `design-packs/` 只负责风格偏移，不替代真源
- `artifact-surfaces/` 只负责具体交付物验证，不重定义品牌
- `examples/` 与真实案例只作验收基准

## DESIGN.md 导出与验收

```bash
python3 scripts/export_design_md.py
```

默认会把下面这些文件写到仓库根目录：

- `DESIGN.md`
- `DESIGN-GOVERNANCE.md`
- `design-preview.html`
- `index.html`
- `artifact-web-brand-landing.html`
- `artifact-mobile-h5-consultation.html`
- `artifact-quote-card-editorial.html`

其中 `index.html` 会与 `design-preview.html` 保持同步，让生产根地址 `/` 直接展示最新设计预览面；3 个 `artifact-*.html` 则对应网页、手机 H5、图文报价体三个载体样例。

推荐执行顺序：

1. 先修改 `foundation-dna/design-dna.zh-CN.json`
2. 如需风格偏移，再改 `design-packs/*.json`
3. 如需具体载体，再改 `artifact-surfaces/*.json`
4. 运行 `python3 scripts/export_design_md.py`
5. 打开 `DESIGN.md`、`DESIGN-GOVERNANCE.md`、`design-preview.html`、首页 `/` 与 3 个 `artifact-*` 页面做人工验收
6. 运行测试确认没有回归

## 扩展 Design Packs

当你觉得现有类目不够时，优先扩展 `design-packs/`，而不是引入外部样式仓库依赖。

- 每个 pack 都是一份 JSON，描述适用页面、信息密度、CTA 语气、图像策略和预览文案
- pack 只表达“同一品牌 DNA 下的不同页面气质”，不重新定义品牌真源
- pack 的职责是打开**受控变化空间**，不是再造第二套设计系统
- 新增 pack 后，重新运行导出脚本，`design-preview.html` 与 `index.html` 会自动出现新的筛选项和预览卡片

## 扩展 Artifact Surfaces

当你觉得“风格有了，但还看不出具体成品长什么样”时，优先扩展 `artifact-surfaces/`。

- 每个 surface 都是一份 JSON，固定描述 `surface_type / source_pack / primary_use_case / recommended_modules / layout_rules / preview_content`
- surface 只表达“同一品牌 DNA 落到具体交付物时的模块顺序与版式约束”，不重新定义品牌规则
- surface 的职责是做**具体交付物校验**，帮助发现网页、H5、报价体这类载体最容易失真的地方
- Phase 2 默认只内建 3 个高价值载体：网页、手机 H5、图文报价体

## 案例与真实样例

`skills/public/liangqin-brand-openclaw/examples/` 与真实案例继续保留，但默认角色已经调整为：

- 人工验收对照
- 回归测试基准
- 品牌边界校准样本

不再默认承担主要控制职责，也不以“继续堆更多案例”作为主要演进方向。

## 人类在环验收题库

如果要验证“这套东西给别的 OpenClaw 用到底行不行”，不要只跑机器测试，还要跑人类验收题。

- 题库：`skills/public/liangqin-brand-openclaw/evaluation/human-review-test-cases.zh-CN.json`
- 评审协议：`skills/public/liangqin-brand-openclaw/evaluation/human-review-protocol.zh-CN.md`
- 基础清单：`skills/public/liangqin-brand-openclaw/evaluation/manual-rubric.zh-CN.md`

推荐顺序：

1. 先做 schema / 白名单 / 资产完整性校验
2. 再用题库逐题让目标 OpenClaw 生成首页或产品详情蓝图
3. 最后由人类判断是否真的适合良禽佳木品牌交付

## 导出给其他 OpenClaw 使用

```bash
python3 scripts/export_openclaw_skill.py --output-dir ./dist --zip
```

导出后会生成：

- `dist/liangqin-brand-body/`
- `dist/liangqin-brand-body-2.0.0.zip`

推荐安装方式：

```bash
python3 dist/liangqin-brand-body/scripts/install_into_openclaw.py
```

这个发行包可以直接复制到其他 OpenClaw 的 skills 目录中使用。导出包内已包含：

- `DESIGN.md`
- `DESIGN-GOVERNANCE.md`
- `foundation-dna/design-dna.zh-CN.json`
- `SKILL.md`
- `protocols/`
- `recipes/`
- `examples/`
- `evaluation/`
- `skill-release.json`

如果你想在 OpenClaw 里测试新的 Apple 方法论分支，可直接在对话中明确说：

- `请使用良禽品牌体`
- `良禽佳木apple风`

## 发布新版本到 GitHub

当前公开仓库：

- [drizzlep/liangqin-brand-design](https://github.com/drizzlep/liangqin-brand-design)

当前线上已发布统一入口版本：

- `v2.0.0`

推荐流程：

```bash
python3 scripts/prepare_openclaw_release.py
python3 -m unittest tests/test_liangqin_brand_skill_assets.py tests/test_liangqin_brand_skill_distribution.py tests/test_design_md_adapter.py tests/test_prepare_openclaw_release.py -v
python3 skills/public/liangqin-brand-openclaw/scripts/validate_skill_assets.py
git add .
git commit -m "release: ship 良禽品牌体 v2.0.0"
git push origin HEAD
git tag v2.0.0
git push origin v2.0.0
```

然后到 GitHub Release 页面上传：

- `dist/liangqin-brand-body-2.0.0.zip`

更完整的话术、交付说明和 Release 正文模板见：

- `docs/openclaw-release-playbook.zh-CN.md`

## 本地校验

```bash
python3 scripts/export_design_md.py
python3 -m unittest tests/test_liangqin_brand_skill_assets.py -v
python3 -m unittest tests/test_liangqin_brand_skill_distribution.py -v
python3 -m unittest tests/test_design_md_adapter.py -v
python3 skills/public/liangqin-brand-openclaw/scripts/validate_skill_assets.py
```

## 当前 v1 范围

- 只服务良禽佳木
- 只覆盖首页与产品详情
- 固定模块库优先
- 先做人工评测与黄金样例
- 第一目标是“更像品牌”，不是“生成更多页面”
