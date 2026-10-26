# 良禽佳木品牌设计规范

这个仓库是良禽佳木的设计规范包：一份人类和 AI 都能读的 `DESIGN.md`，加上一个把规范分发给各 AI 助手的技能目录。

## 核心文件

| 路径 | 作用 |
|---|---|
| `DESIGN.md` | 唯一规范真源。frontmatter 是可机器读取的 token，正文是标准九段 + 标志扩展段 |
| `preview.html` | 规范的可视化对照页；标准章节与 `DESIGN.md` 一致，另有 UIkit opening |
| `kit/kit.css` | UI kit：token 变量 + 64 个组件规格（91 个 `.lq-*` 类），页面直接引入即可 |
| `kit/index.html` | 组件目录页：组件模型、导航与寻路、按钮、表单、选择器、状态与加载、提示条、图标、占位块、浮层、卡片、页面区块 |
| `kit/icons/` | 24 个 Lucide 线性图标（ISC 许可）+ 许可证文件；用 CSS mask 上色，跟随文字色 |
| `kit/templates/` | 页面骨架：官网首页、产品详情 |
| `tokens/` | token 的机器可读导出：`tokens.semantic.json` 与 `tokens.css` |
| `assets/brand/` | 真实 logo 资产与用法清单 |
| `assets/fonts/` | 标题与正文字体（woff2） |
| `skills/public/liangqin-brand-body/` | 技能源码：`SKILL.md`、`skill-release.json`、`adapters/` |
| `review-external-ui-kit.html` | 外部风格评审页；只用于参考图对照，不写回 `DESIGN.md` |
| `scripts/` | 三个轻脚本：构建发行包、校验产出页面、同步到各 runtime |
| `requirements-dev.txt` | 开发校验依赖：`PyYAML`，用于严格复核 frontmatter |
| `archive/` | 冻结的历史层，默认不读、不维护 |

`DESIGN.md` 采用 Google Stitch 提出的 DESIGN.md 格式，并按 `awesome-design-md` 收录文件的写法对齐：

- frontmatter 只放 8 个标准键：`version / name / description / colors / typography / rounded / spacing / components`
- 正文按标准段落排列：Overview / Colors / Typography / Layout / Elevation & Depth / Shapes / Components / Do's and Don'ts / Responsive Behavior / Iteration Guide / Known Gaps
- 品牌自己的内容（标志）作为扩展段排在标准段落之后
- 组件状态（`button-primary-active`、`input-focused` 等）作为 `components:` 里的独立条目维护
- 全篇使用 `{token.refs}` 引用，不内联 hex

## 怎么用

**统一产出的推荐做法（给用 AI 做网页的人）**

1. 引入 kit：`<link rel="stylesheet" href="kit/kit.css">`，页面用 `.lq-*` 类名拼装，不要自己写颜色、字号、间距、圆角。
   图标用 `<span class="lq-icon" style="--lq-icon-url:url('kit/icons/phone.svg')"></span>`，颜色自动跟随文字色。
2. 需要规格里没有的组件时，先改 `DESIGN.md` 的 `components:` 与 `## Components`，再在 `kit.css` 加对应类；不要在页面里就地发明样式。
3. 产出后跑校验：

```bash
python3 scripts/check_page.py path/to/your-page.html
```

它会报出 token 外的颜色、不在字阶上的字号、不在 8px 刻度上的间距、非法圆角、字重声明、对比度不足与拼错的 `--lq-*` 变量，有偏离时返回非零退出码。

4. 校验通过再交付。规范本身、预览页与 kit 每次构建都会跑同一套检查，所以规范与 kit 不会互相漂移。

**项目里用（不依赖任何 skill 机制）**

```bash
cp DESIGN.md /path/to/your-project/DESIGN.md
```

然后告诉 AI："按 `DESIGN.md` 做这个页面"。适合 Google Stitch、网页版 AI 工具，以及希望规范随项目走的团队。

**在 AI 助手里用**

```bash
python3 scripts/build_skill.py            # 构建 dist/liangqin-brand-body/
python3 scripts/sync_runtimes.py          # 查看会同步到哪些 runtime（dry-run）
python3 scripts/sync_runtimes.py --apply  # 真正写入
```

也可以直接把 `dist/liangqin-brand-body/` 整个目录复制到目标 runtime 的 skills 目录。安装位置见 `skills/public/liangqin-brand-body/adapters/README.zh-CN.md`。

**改规范**

1. 改 `DESIGN.md`，必要时同步 `tokens/` 的导出值
2. 跑 `python3 scripts/build_skill.py`（构建时自动校验 frontmatter、章节、资产引用）
3. 用浏览器打开根目录 `preview.html` 做人工比对
4. 跑 `python3 -m unittest discover -s tests -p "test_*.py"`

## 版本

当前 `3.0.0`。这一版按 DESIGN.md 标准重新架构，只保留长期有效的部分：标志、色彩、字体、字号、间距、圆角、阴影、组件与禁用项。

相对 2.x 的变化：

- `DESIGN.md` 重写为标准的 frontmatter token + 九段正文格式，标志作为扩展段
- 技能入口去掉 OpenClaw / Hermes 语境，改为运行时中立
- 示例目录不再随包发行，规范里的提示词指南只保留一段可复制的短提示词
- 旧 demo 页面、样式表与脚本全部退役，`preview.html` 作为规范可视化对照页；外部风格对照单独放在 `review-external-ui-kit.html`
- 六个重脚本退役，只保留构建、页面校验与同步三个轻脚本
- 旧标准层（DNA、design pack、artifact surface、蓝图 schema、模块 recipe、评测集）全部移入 `archive/`，不再参与默认读取路径
- `tokens.css` 的变量前缀由 `--dna-` 改为 `--lq-`；引用过旧前缀的工程需要同步改名
- `tokens.css` 只导出 token 变量，不再包含旧版附带的组件样式与元素选择器
- 变量名与 `DESIGN.md` 对齐：`--lq-color-primary-ink`、`--lq-color-background`、`--lq-space-section`、`--lq-radius-sm` 等
- 规范不再声明字重（随包字体各自只有一个字重）
- 两个 logo 已按图形边界裁切：横向 `678×188`、纵向 `568×419`，可直接按高度排版

## 已知待确认

- 标志的最小尺寸与安全边距正式数值待品牌方确认；确认前以可见字高不低于 24px、印刷不低于 8mm 为准。
- 本规范只定义浅色底与深色区块，没有完整的深色主题令牌。
- 随包字体各自只有一个字重；需要多字重时先补字体文件。
