---
name: liangqin-brand-body
description: "良禽佳木品牌设计规范与 UI kit。当用户要求做良禽佳木 / 良禽的网页、官网、落地页、H5、活动页、首页、产品详情、品牌页、海报、长图、封面、报价卡、图标方案或视觉稿，或要求按品牌规范给出色彩、字体、字号、间距、圆角、阴影、组件与标志用法时使用。Use when the user asks for Liangqin Ji Mu (良禽佳木) web pages, landing pages, H5 pages, brand sites, posters, long images, cover images, quote cards, icon sets, or the brand design tokens and UI kit for color, typography, spacing, radius, elevation, components and logo usage."
metadata:
  display_name: "良禽品牌体"
  aliases: "良禽佳木品牌体, liangqin-brand-body"
  version: "3.0.0"
  brand: "良禽佳木"
  spec: "DESIGN.md (Google Stitch format)"
---

# 良禽品牌体

良禽佳木的品牌设计规范技能。目标不是"生成得更多"，而是"生成得更像良禽佳木"。

一句话工作方式：**先读 `DESIGN.md`，按里面的色彩、字体、字号、间距、圆角和标志规则出方案；素材不够就降级，不编造。**

## 何时使用

用户提到以下任一方向时进入本技能：

- 良禽佳木 / 良禽的品牌页、首页、产品详情、H5、落地页
- 海报、长图、封面、报价卡、社媒图、图标方案、视觉稿
- 品牌色彩、字体、字号、间距、圆角、阴影、标志用法
- 设计系统、`DESIGN.md`、design token、组件规范
- 现有方案与良禽品牌的一致性反审

## 何时不要抢单

- 用户要的是**报价数字、材质参数、产品事实**：先由报价或产品资料能力给出事实，本技能只负责视觉表达。
- 用户要的是**纯文案**（公关稿、文章、详情描述）：交给写作能力，本技能只提供语气与视觉约束。
- 用户要的是**工程实现**（改代码、修 bug、性能）：本技能只提供规范输入，不接管实现。

同一条请求里同时出现产品、材质、报价词，但目标仍是图片、页面、长图或卡片时，仍由本技能主导，不要被报价类技能抢走。

## 30 秒品牌摘要

- **气质**：温润、克制、专业、高级、松弛。高级感来自材质、比例、留白、秩序和中文可读性。
- **颜色**：暖白 `#F8F5F0` 打底，石灰 `#F2EEE8` 作次级面，炭墨 `#2B2926` 作主文本，低饱和 taupe `#8B6A4E` 作强调；标志色 `#9E7F63`。不使用高饱和色块。
- **字体**：标题宋体方向（Swei Sugar / Noto Serif SC / Songti SC），正文现代中文无衬线（OPPO Sans 4.0 / PingFang SC）。正文 `17px / 1.82`，不得小于 `16px / 1.7`。
- **字重**：不声明字重。随包字体各自只有一个字重，声明 500 / 600 不会生效，需要强调时用字号、颜色或留白。
- **间距**：8px 基准，刻度 `4 / 8 / 12 / 16 / 24 / 32 / 48 / 64 / 96 / 128`；区块纵向 96px，品牌级大区块 128px。
- **形状**：圆角 2 / 6 / 12px 与 pill；阴影只表达层级，同一屏不超过两个层级。
- **语气**：礼貌邀请式 CTA，不命令、不制造焦虑、不用倒计时和夸张稀缺文案。

完整定义以 `DESIGN.md` 为准，本摘要只用于快速判断方向。

## 交付分级

先判断当前 runtime 能做到哪一级，再决定产出形态。不要承诺做不到的事。

| 级别 | 能力 | 交付形态 |
|---|---|---|
| **L1** | 只能读 markdown，不能读文件或跑工具 | 依据本文件与 `DESIGN.md` 的正文，输出结构化的视觉方向、文案与规格说明 |
| **L2** | 能读文件、能写代码或生成图片 | 读取 `DESIGN.md`、`assets/brand/`、`tokens/`，产出可交付的页面、图片或组件 |
| **L3** | 能跑脚本、开浏览器、做视觉验收 | 在 L2 基础上补做真实渲染、尺寸与响应式检查，并给出验收证据 |

只有 L1 时不要假装已经渲染或校验过；L2/L3 也不要跳过 `DESIGN.md` 直接凭审美发挥。

## 默认读取顺序

1. `DESIGN.md`（唯一默认必读）
2. 要写页面或 HTML 时读 `kit/kit.css`，用里面的 `.lq-*` 类名
3. 需要真实标志时读 `assets/brand/` 与其中的 `asset-manifest.zh-CN.json`
4. 需要工程接入时读 `tokens/tokens.css`；需要组件可视目录时打开 `kit/index.html`
5. 需要规范对照或人工验收时打开 `preview.html`

`adapters/` 只在接入某个具体 runtime 时才读，默认跳过。

## 交付流程（必须遵守）

1. 先读 `DESIGN.md`，确认这次交付属于哪类承载（网页 / 卡片 / 长图 / 海报 / 组件）。
2. 做整页时先套模板：官网首页用 `kit/templates/homepage.html`，产品详情用 `kit/templates/product-detail.html`，替换内容但保留结构与流转。
3. 没有模板可套时引入 `kit/kit.css`，用 `.lq-*` 类名拼装；**不要自己写颜色、字号、间距、圆角，也不要声明字重**。
4. 需要规格里没有的组件时，先在 `DESIGN.md` 的 `components:` 加条目并在 `## Components` 写清规格，再在 `kit.css` 加对应类，不要在页面里就地发明样式。
5. 产出后运行 `python3 scripts/check_page.py <产出文件>`；报告会按 What / Why / Fix 三段给出问题、依据章节和改法，有 FAIL 必须修掉再交付。
6. 环境不能读文件或不能跑脚本时，按 `DESIGN.md` 正文输出结构化规格，并明确说明"未经过 kit 与 check_page 校验"。

## 标志与资产纪律

- **默认不插 logo**。只有用户明确说"加入 logo / 使用真实标志 / 放横版 logo / 品牌落款"时才使用。
- 用户要求 logo 时，必须读到 `assets/brand/` 中的真实 SVG（PNG 仅降级）。读不到就停在结构化 spec，并说明缺什么，**不允许用纯文字品牌名冒充标志**。
- 直接使用文件本身的颜色，**不要按 token 重新上色**：标志填充色是 `#9E7F63`，token `brand-asset` 已与它对齐。
- 两个标志文件已按图形边界裁切（横向 678×188，纵向 568×419），可以直接按高度排版；横向可见字高不低于 24px。
- 不重绘字形、不拉伸、不描边、不加浮雕发光、不叠在高噪声图像上。
- 品牌名统一写 `良禽佳木` 或 `良禽`；不要写成 `梁琴` 或 `梁琴佳木`。
- 产品参数、报价、案例、图片来源一律不得编造；不足时标成占位或待确认。

## 硬约束

必须：

- 中文优先，先保证中文阅读的字号、行高与标签完整度
- 先用摄影、材质、留白和结构建立信任，再谈装饰或动效
- 结构稳定、允许有限变化；换承载方式不换风格语言
- 交付前自检：颜色是否落在 token 内、字号是否落在字阶内、间距是否落在刻度内、标志是否符合用法、事实是否有来源

禁止：

- 电商促销风、倒计时、夸张稀缺文案、高饱和色块
- 冷感国际模板腔、玻璃拟态、假奢华、炫技动效、粒子与 3D 默认装饰
- 用低质量图标或假数据把版面填满
- 把参考页（Poliform / Flexform 等）当模板复制，照搬其结构、形态、文案或交互签名
- 把 `Pack`、`Page Goal`、`Preview` 等系统说明词泄漏到成品里
- 把 deck、报价卡、H5、设计画布统一套成网页落地页

## 外部风格请求

用户明确要求外部风格（例如"喜茶风格"）时，按该风格方向完成本次产物，不要强行转译回木作风格；但不要把它写回 `DESIGN.md` 或任何品牌真源文件。

## 信息不足时

按下面顺序降级，并明确写出当前状态：

1. `structured_spec`：只有规范与结构，没有成品
2. `visual_draft`：有视觉方向，但素材或事实不完整
3. `blocked_pending_assets`：缺少必要素材或事实，无法继续

不要为了交付完整感而编造。缺什么就写清楚缺什么、需要谁来补。

## 文件地图

```text
liangqin-brand-body/
├── SKILL.md                     # 本文件：入口与工作方式
├── DESIGN.md                    # 品牌设计规范（默认必读，含 token frontmatter）
├── preview.html                 # 色板 / 字阶 / 间距 / 组件的人工预览页
├── skill-release.json           # 包元数据与版本
├── kit/
│   ├── kit.css                  # token + 组件类，页面直接引入
│   ├── index.html               # 组件目录（样式手册），含可复制的类名
│   ├── icons/                   # 24 个 Lucide 图标 + 许可证
│   └── templates/               # 页面骨架：homepage.html / product-detail.html
├── assets/brand/                # logo 真实资产与用法清单
├── assets/fonts/                # 标题与正文字体（woff2）
├── tokens/
│   ├── tokens.css               # 前端可直接引用的 CSS 变量
│   └── tokens.semantic.json     # 不解析 YAML 时读这份 token 导出
├── scripts/check_page.py        # 发行包内的页面校验脚本
└── adapters/README.zh-CN.md     # 接入某个 runtime 时才读
```

交付前的校验脚本：`scripts/check_page.py <文件>`（默认按 token 与刻度检查，有偏离返回非零退出码）。

## 运行时接入

本技能遵循 Agent Skills 约定：一个目录一个 skill，`SKILL.md` 带 `name` 与 `description` frontmatter，目录名与 `name` 一致。

各 runtime 的安装位置见 `adapters/README.zh-CN.md`。默认只需要把整个目录放进对应 runtime 的 skills 目录，不需要额外脚本。
