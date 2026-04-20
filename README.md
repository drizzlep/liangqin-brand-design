# 良禽佳木跨工具 DESIGN 标准包

这个仓库不再只被视为一个 OpenClaw 品牌 skill，而是一个以良禽佳木为样板的**跨工具 DESIGN 标准包**。

它的目标是：

- 让 `DESIGN.md` 成为人类和弱能力 agent 都能理解的主入口
- 让更强的链路继续读取 DNA、assets、artifact surfaces、checklist 和 evaluation
- 让 OpenClaw 只作为一个消费这套标准的适配器，而不是标准本体

## 固定分层

当前标准包固定分成 7 层：

1. **Foundation DNA 真源层**
   - `foundation-dna/design-dna.zh-CN.json`
   - `foundation-dna/tokens.semantic.json`
   - `foundation-dna/tokens.css`
   - `foundation-dna/token-table.zh-CN.md`

2. **品牌宪法主入口**
   - `DESIGN.md`
   - `CONSUMER-GUIDE.zh-CN.md`
   - `DESIGN-GOVERNANCE.md`
   - `EXECUTION-CHECKLIST.md`

3. **Design Pack 受控变化层**
   - `design-packs/`

4. **Artifact Surface 载体约束层**
   - `artifact-surfaces/`
   - `artifact-web-brand-landing.html`
   - `artifact-mobile-h5-consultation.html`
   - `artifact-quote-card-editorial.html`

5. **品牌资产与阻断层**
   - `assets/brand/`
   - `assets/brand/asset-manifest.zh-CN.json`

6. **评测与回归层**
   - `evaluation/`

7. **OpenClaw 适配器层**
   - `skills/public/liangqin-brand-openclaw/`
   - `scripts/export_openclaw_skill.py`
   - `design-standard-package.json`

## 适用目标

把良禽佳木现有设计规范升级为一个**团队可维护、跨工具可消费、但先用良禽佳木验证的标准底座**。

这套标准允许：

- 弱能力工具只读取 `DESIGN.md`
- 中等能力工具读取 `DESIGN.md + artifact-surfaces + assets`
- 高保真链路读取完整标准包

同时，它也让 OpenClaw 机器人可以：

- 吃品牌 brief、产品资料、参考页面
- 输出首页 / 产品详情的结构化蓝图
- 在固定模块库内继续生成页面
- 更稳定地“像良禽佳木”

## 对外入口

- 对外推荐入口词：`良禽品牌体`
- 对外兼容入口词：`良禽佳木品牌体`
- 内部源目录：`skills/public/liangqin-brand-openclaw/`
- 标准包元数据：`design-standard-package.json`
- Skill 文件：`skills/public/liangqin-brand-openclaw/SKILL.md`
- 输入协议：`skills/public/liangqin-brand-openclaw/protocols/input-contract.zh-CN.json`
- 模块库：`skills/public/liangqin-brand-openclaw/recipes/module-recipes.zh-CN.json`
- OpenClaw 本地兼容样例：`skills/public/liangqin-brand-openclaw/examples/`
- 真实设计案例：`skills/public/liangqin-brand-openclaw/examples/real-cases/`
- Root 黄金样例：`evaluation/examples/`

命名策略：

- 仓库内部暂时保留旧源目录名，避免一次性打碎路径与测试
- 对外发行包继续使用 `liangqin-brand-body`
- 对话里推荐使用 `良禽品牌体` 或 `良禽佳木品牌体`
- `liangqin-brand-openclaw` 只保留为历史兼容说明

## 系统层级关系

- `foundation-dna/`：品牌真源
- `DESIGN.md`：人类与弱能力 agent 的唯一主入口
- `CONSUMER-GUIDE.zh-CN.md`：跨渠道、跨 agent 的统一消费说明
- `DESIGN-GOVERNANCE.md`：读取顺序、冲突优先级与层级职责
- `EXECUTION-CHECKLIST.md`：统一生成自检
- `design-packs/`：受控变化层
- `artifact-surfaces/`：具体交付物约束层
- `assets/brand/` 与 `assets/brand/asset-manifest.zh-CN.json`：最终成品阻断层
- `evaluation/`：人工评审、黄金样例索引与回归题
- `skills/public/liangqin-brand-openclaw/`：OpenClaw 适配器层
- `design-standard-package.json`：标准包元数据、消费层级与团队治理策略

默认优先级：

- `Foundation DNA > DESIGN.md > artifact-surfaces > design-packs > examples`

补充约定：

- `design-packs/` 只负责受控偏移，不替代真源
- `artifact-surfaces/` 只负责交付约束，不重定义品牌
- `examples/` 与真实案例只作验收基准
- `skills/public/liangqin-brand-openclaw/` 只负责消费标准，不再定义标准本身

## 跨工具消费层级

- `Tier 1`
  - 只读 `DESIGN.md`
  - 适合 Stitch、弱能力 agent、公开传播
  - 能保住品牌基调，但不保证图标、logo、成品细节工艺

- `Tier 2`
  - 读取 `DESIGN.md + artifact-surfaces + assets`
  - 适合页面、长图、海报、H5 等成品交付
  - 能较稳定保住 logo、版式、信息密度

- `Tier 3`
  - 读取完整标准包：`DESIGN.md + DNA + assets + checklist + evaluation`
  - 适合你自己的机器人链路与团队内高保真生成

所有工具都允许“只读自己吃得动的层”，但不允许低层覆盖高层。

## DESIGN.md 导出与验收

```bash
python3 scripts/export_design_md.py
```

默认会把下面这些文件写到目标目录：

- `DESIGN.md`
- `CONSUMER-GUIDE.zh-CN.md`
- `DESIGN-GOVERNANCE.md`
- `design-standard-package.json`
- `artifact-surfaces/`
- `assets/brand/`
- `evaluation/`
- `design-preview.html`
- `index.html`
- `artifact-web-brand-landing.html`
- `artifact-mobile-h5-consultation.html`
- `artifact-quote-card-editorial.html`
- `foundation-dna/design-dna.zh-CN.json`
- `foundation-dna/tokens.semantic.json`

推荐执行顺序：

1. 先修改 `foundation-dna/design-dna.zh-CN.json`
2. 如需工具中立 token，再同步 `foundation-dna/tokens.semantic.json`
3. 如需风格偏移，再改 `design-packs/*.json`
4. 如需具体载体，再改 `artifact-surfaces/*.json`
5. 运行 `python3 scripts/export_design_md.py`
6. 打开 `DESIGN.md`、`CONSUMER-GUIDE.zh-CN.md`、`DESIGN-GOVERNANCE.md`、`design-standard-package.json`、`design-preview.html` 与 3 个 `artifact-*` 页面做人工验收
7. 运行测试确认没有回归

## 扩展 Design Packs

当你觉得现有变化空间不够时，优先扩展 `design-packs/`，而不是引入外部样式仓库依赖。

- 每个 pack 都是一份 JSON，描述适用页面、信息密度、CTA 语气、图像策略和预览文案
- pack 只表达“同一品牌 DNA 下的不同页面气质”，不重新定义品牌真源
- pack 的职责是打开**受控变化空间**，不是再造第二套设计系统

## 扩展 Artifact Surfaces

当你觉得“风格有了，但还看不出具体成品长什么样”时，优先扩展 `artifact-surfaces/`。

- 每个 surface 都是一份 JSON，固定描述载体类型、推荐模块、版式规则和易失真点
- surface 只表达“同一品牌 DNA 落到具体交付物时的模块顺序与版式约束”，不重定义品牌规则
- surface 的职责是做**具体交付物校验**

## 案例与回归

`skills/public/liangqin-brand-openclaw/examples/` 与真实案例继续保留，但默认角色已经调整为：

- 人工验收对照
- 回归测试基准
- 品牌边界校准样本
- OpenClaw 本地兼容层，不再是黄金样例真源

人类在环验收题库：

- 评审协议：`evaluation/human-review-protocol.zh-CN.md`
- 验收题库：`evaluation/human-review-test-cases.zh-CN.json`
- 基础清单：`evaluation/manual-rubric.zh-CN.md`
- 黄金样例索引：`evaluation/golden-samples.zh-CN.md`
- Root 结构化样例：`evaluation/examples/`
- 失败样例类型：`evaluation/failure-samples.zh-CN.md`
- 高风险回归题：`evaluation/high-risk-regression-cases.zh-CN.json`

## 导出给其他 OpenClaw 使用

```bash
python3 scripts/export_openclaw_skill.py --output-dir ./dist --zip
```

导出后会生成：

- `dist/liangqin-brand-body/`
- `dist/liangqin-brand-body-2.2.0.zip`

推荐安装方式：

```bash
python3 dist/liangqin-brand-body/scripts/install_into_openclaw.py
```

导出包内已包含：

- `DESIGN.md`
- `CONSUMER-GUIDE.zh-CN.md`
- `DESIGN-GOVERNANCE.md`
- `design-standard-package.json`
- `EXECUTION-CHECKLIST.md`
- `foundation-dna/design-dna.zh-CN.json`
- `foundation-dna/tokens.semantic.json`
- `artifact-surfaces/`
- `assets/brand/`
- `SKILL.md`
- `protocols/`
- `recipes/`
- `examples/`
- `evaluation/`
- `skill-release.json`

## 本地校验

```bash
python3 scripts/prepare_openclaw_release.py --output-dir ./dist
```

如果你只想手动逐步检查，也可以使用：

```bash
python3 scripts/sync_openclaw_mirrors.py
python3 scripts/export_design_md.py
python3 -m unittest tests/test_liangqin_brand_skill_assets.py -v
python3 -m unittest tests/test_liangqin_brand_skill_distribution.py -v
python3 -m unittest tests/test_design_md_adapter.py -v
python3 -m unittest tests/test_sync_openclaw_mirrors.py -v
python3 -m unittest tests/test_standard_package_integrity.py -v
python3 skills/public/liangqin-brand-openclaw/scripts/validate_skill_assets.py
```

## 当前第一版范围

- 只服务良禽佳木
- 先做良禽先行样板，不直接抽成多品牌框架
- 团队协作与你自己的机器人链路优先
- 不新增“渠道专属风格包”作为主控方式
- 第一目标是“更像品牌且可稳定交付”，不是“堆更多风格”
