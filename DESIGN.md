---
version: "3.0.0"
name: 良禽佳木 DESIGN.md
description: "良禽佳木品牌设计规范。温润、克制、专业、高级、松弛：暖中性色底 + 低饱和 taupe 强调，宋体方向标题 + 现代中文无衬线正文，8px 基准间距，12 栏宽留白，低噪声组件与礼貌 CTA。供 AI agent、设计工具与前端工程共同读取。"

colors:
  primary-ink: "#2B2926"
  background: "#F8F5F0"
  surface: "#F2EEE8"
  surface-elevated: "#FFFCF8"
  accent: "#8B6A4E"
  brand-asset: "#9E7F63"
  line: "#D8D0C4"
  ink-900: "#1F1D1B"
  ink-700: "#4B4640"
  ink-500: "#888075"
  on-dark: "#F8F5F0"
  success: "#567A62"
  warning: "#A0743C"
  error: "#A04F46"
  info: "#5E7A8E"

typography:
  heading-family: '"Swei Sugar", "Noto Serif SC", "Source Han Serif SC", "Songti SC", serif'
  body-family: '"OPPO Sans 4.0", "PingFang SC", "Hiragino Sans GB", "Noto Sans SC", sans-serif'
  mono-family: '"SFMono-Regular", "SF Mono", "Menlo", "Consolas", monospace'
  display:
    fontFamily: '{typography.heading-family}'
    fontSize: 72px
    lineHeight: 1.08
    letterSpacing: -0.03em
  heading-1:
    fontFamily: '{typography.heading-family}'
    fontSize: 48px
    lineHeight: 1.18
    letterSpacing: -0.025em
  heading-2:
    fontFamily: '{typography.heading-family}'
    fontSize: 36px
    lineHeight: 1.24
    letterSpacing: -0.02em
  heading-3:
    fontFamily: '{typography.heading-family}'
    fontSize: 28px
    lineHeight: 1.32
    letterSpacing: -0.015em
  heading-4:
    fontFamily: '{typography.heading-family}'
    fontSize: 22px
    lineHeight: 1.4
    letterSpacing: -0.01em
  body:
    fontFamily: '{typography.body-family}'
    fontSize: 17px
    lineHeight: 1.82
    letterSpacing: 0
  body-small:
    fontFamily: '{typography.body-family}'
    fontSize: 15px
    lineHeight: 1.72
    letterSpacing: 0
  caption:
    fontFamily: '{typography.body-family}'
    fontSize: 13px
    lineHeight: 1.6
    letterSpacing: 0.01em
  overline:
    fontFamily: '{typography.body-family}'
    fontSize: 12px
    lineHeight: 1.4
    letterSpacing: 0.12em

rounded:
  xs: 2px
  sm: 6px
  md: 12px
  pill: 999px

spacing:
  xxs: 4px
  xs: 8px
  sm: 12px
  md: 16px
  lg: 24px
  xl: 32px
  xxl: 48px
  xxxl: 64px
  section: 96px
  section-lg: 128px

components:
  nav-bar:
    backgroundColor: '{colors.background}'
    textColor: '{colors.ink-700}'
    border: '1px solid {colors.line}'
    typography: '{typography.body-small}'
    height: 72px
  nav-link:
    textColor: '{colors.ink-700}'
    typography: '{typography.body-small}'
    padding: 8px 12px
    rounded: '{rounded.xs}'
  nav-cta:
    backgroundColor: '{colors.primary-ink}'
    textColor: '{colors.background}'
    typography: '{typography.body-small}'
    rounded: '{rounded.sm}'
    padding: 12px 24px
    height: 44px
  breadcrumb:
    textColor: '{colors.ink-700}'
    typography: '{typography.caption}'
    padding: 8px 0
  tabs:
    backgroundColor: transparent
    textColor: '{colors.ink-700}'
    border: '1px solid {colors.line}'
    typography: '{typography.body-small}'
    padding: 8px 16px
    height: 40px
  pagination:
    textColor: '{colors.ink-700}'
    typography: '{typography.body-small}'
    border: '1px solid {colors.line}'
    rounded: '{rounded.xs}'
    size: 40px
  button-primary:
    backgroundColor: '{colors.primary-ink}'
    textColor: '{colors.background}'
    typography: '{typography.body-small}'
    rounded: '{rounded.sm}'
    padding: 16px 32px
    height: 48px
  button-primary-active:
    backgroundColor: '{colors.ink-900}'
    textColor: '{colors.background}'
    rounded: '{rounded.sm}'
  button-primary-disabled:
    backgroundColor: '{colors.line}'
    textColor: '{colors.ink-700}'
    rounded: '{rounded.sm}'
  button-secondary:
    backgroundColor: transparent
    textColor: '{colors.primary-ink}'
    border: '1px solid {colors.line}'
    typography: '{typography.body-small}'
    rounded: '{rounded.sm}'
    padding: 16px 32px
    height: 48px
  button-secondary-active:
    backgroundColor: '{colors.surface}'
    textColor: '{colors.primary-ink}'
    border: '1px solid {colors.accent}'
    rounded: '{rounded.sm}'
  button-sm:
    height: 40px
    padding: 8px 24px
    typography: '{typography.body-small}'
    rounded: '{rounded.sm}'
  button-lg:
    height: 56px
    padding: 16px 32px
    typography: '{typography.body}'
    rounded: '{rounded.sm}'
  button-on-dark:
    backgroundColor: '{colors.background}'
    textColor: '{colors.primary-ink}'
    typography: '{typography.body-small}'
    rounded: '{rounded.sm}'
    padding: 16px 32px
    height: 48px
  button-text-link:
    backgroundColor: transparent
    textColor: '{colors.accent}'
    typography: '{typography.body-small}'
    rounded: '{rounded.xs}'
    padding: 4px 0
  text-input:
    backgroundColor: '{colors.surface-elevated}'
    textColor: '{colors.primary-ink}'
    border: '1px solid {colors.line}'
    typography: '{typography.body-small}'
    rounded: '{rounded.sm}'
    padding: 12px 16px
    height: 48px
  text-input-focused:
    border: '2px solid {colors.accent}'
    rounded: '{rounded.sm}'
  text-input-error:
    border: '1px solid {colors.error}'
    textColor: '{colors.error}'
    rounded: '{rounded.sm}'
  text-input-sm:
    height: 40px
    padding: 8px 12px
    typography: '{typography.body-small}'
    rounded: '{rounded.sm}'
  search-field:
    backgroundColor: '{colors.surface-elevated}'
    border: '1px solid {colors.line}'
    typography: '{typography.body-small}'
    rounded: '{rounded.sm}'
    padding: 0 16px
    height: 48px
  select:
    backgroundColor: '{colors.surface-elevated}'
    textColor: '{colors.primary-ink}'
    border: '1px solid {colors.line}'
    typography: '{typography.body-small}'
    rounded: '{rounded.sm}'
    padding: 0 48px 0 16px
    height: 48px
  textarea:
    backgroundColor: '{colors.surface-elevated}'
    textColor: '{colors.primary-ink}'
    border: '1px solid {colors.line}'
    typography: '{typography.body-small}'
    rounded: '{rounded.sm}'
    padding: 12px 16px
    minHeight: 128px
  select-on-dark:
    backgroundColor: '{colors.primary-ink}'
    textColor: '{colors.on-dark}'
    border: '1px solid {colors.primary-ink}'
    typography: '{typography.body-small}'
    rounded: '{rounded.sm}'
    padding: 0 48px 0 16px
    height: 48px
  checkbox:
    textColor: '{colors.primary-ink}'
    typography: '{typography.body-small}'
    size: 20px
  checkbox-disabled:
    textColor: '{colors.ink-700}'
    opacity: 0.45
  radio:
    textColor: '{colors.primary-ink}'
    typography: '{typography.body-small}'
    size: 20px
  slider:
    height: 24px
  segmented:
    backgroundColor: '{colors.surface}'
    textColor: '{colors.ink-700}'
    border: '1px solid {colors.line}'
    typography: '{typography.body-small}'
    rounded: '{rounded.pill}'
    padding: 8px 16px
  stepper:
    backgroundColor: '{colors.surface-elevated}'
    textColor: '{colors.primary-ink}'
    border: '1px solid {colors.line}'
    typography: '{typography.body-small}'
    rounded: '{rounded.sm}'
    height: 40px
  toggle:
    backgroundColor: '{colors.line}'
    textColor: '{colors.primary-ink}'
    rounded: '{rounded.pill}'
    width: 44px
    height: 24px
  choice-card:
    backgroundColor: '{colors.surface-elevated}'
    textColor: '{colors.primary-ink}'
    border: '1px solid {colors.line}'
    rounded: '{rounded.md}'
    padding: 24px
  form-label:
    textColor: '{colors.ink-700}'
    typography: '{typography.body-small}'
    padding: 0 0 8px
  form-helper:
    textColor: '{colors.ink-700}'
    typography: '{typography.caption}'
    padding: 8px 0 0
  card-base:
    backgroundColor: '{colors.surface}'
    textColor: '{colors.primary-ink}'
    border: '1px solid {colors.line}'
    rounded: '{rounded.md}'
    padding: 32px
  card-material:
    backgroundColor: '{colors.surface-elevated}'
    textColor: '{colors.primary-ink}'
    border: '1px solid {colors.line}'
    rounded: '{rounded.md}'
    padding: 32px
  card-case:
    backgroundColor: '{colors.surface}'
    textColor: '{colors.primary-ink}'
    border: '1px solid {colors.line}'
    rounded: '{rounded.md}'
    padding: 0
  card-product:
    backgroundColor: '{colors.surface-elevated}'
    textColor: '{colors.primary-ink}'
    border: '1px solid {colors.line}'
    rounded: '{rounded.md}'
    padding: 24px
  card-quote:
    backgroundColor: '{colors.surface-elevated}'
    textColor: '{colors.primary-ink}'
    border: '1px solid {colors.line}'
    rounded: '{rounded.sm}'
    padding: 24px
  hero-band:
    backgroundColor: '{colors.background}'
    textColor: '{colors.primary-ink}'
    typography: '{typography.display}'
    padding: 96px 32px
    rounded: '{rounded.xs}'
  section-header:
    textColor: '{colors.primary-ink}'
    typography: '{typography.heading-2}'
    padding: 0 0 32px
  media-frame:
    backgroundColor: '{colors.surface}'
    border: '1px solid {colors.line}'
    rounded: '{rounded.md}'
    padding: 0
  spec-table:
    backgroundColor: '{colors.surface-elevated}'
    textColor: '{colors.ink-700}'
    border: '1px solid {colors.line}'
    typography: '{typography.body-small}'
    rounded: '{rounded.sm}'
    padding: 16px
  consultation-cta:
    backgroundColor: '{colors.primary-ink}'
    textColor: '{colors.background}'
    typography: '{typography.heading-3}'
    rounded: '{rounded.md}'
    padding: 48px
  footer:
    backgroundColor: '{colors.surface}'
    textColor: '{colors.ink-700}'
    border: '1px solid {colors.line}'
    typography: '{typography.caption}'
    padding: 64px 32px
  logo-lockup:
    textColor: '{colors.brand-asset}'
    height: 24px
    padding: 0
  pill-tag:
    backgroundColor: '{colors.surface}'
    textColor: '{colors.ink-700}'
    border: '1px solid {colors.line}'
    typography: '{typography.caption}'
    rounded: '{rounded.pill}'
    padding: 8px 16px
  status-badge:
    backgroundColor: '{colors.surface}'
    textColor: '{colors.ink-700}'
    border: '1px solid {colors.line}'
    typography: '{typography.caption}'
    rounded: '{rounded.pill}'
    padding: 4px 12px
  eyebrow:
    textColor: '{colors.ink-700}'
    typography: '{typography.overline}'
    padding: 0 0 16px
  icon:
    color: '{colors.primary-ink}'
    size: 24px
    strokeWidth: 1.5
  icon-sm:
    size: 16px
  icon-lg:
    size: 32px
  placeholder:
    backgroundColor: '{colors.surface}'
    textColor: '{colors.ink-700}'
    border: '1px solid {colors.line}'
    rounded: '{rounded.md}'
  alert:
    backgroundColor: '{colors.surface}'
    textColor: '{colors.ink-700}'
    border: '1px solid {colors.line}'
    typography: '{typography.body-small}'
    rounded: '{rounded.sm}'
    padding: 16px 24px
  alert-on-dark:
    backgroundColor: '{colors.primary-ink}'
    textColor: '{colors.on-dark}'
    rounded: '{rounded.sm}'
  upload:
    backgroundColor: '{colors.surface}'
    textColor: '{colors.ink-700}'
    border: '1px dashed {colors.line}'
    typography: '{typography.body-small}'
    rounded: '{rounded.sm}'
    padding: 32px
    minHeight: 128px
  progress:
    backgroundColor: '{colors.line}'
    textColor: '{colors.primary-ink}'
    rounded: '{rounded.pill}'
    height: 4px
  tooltip:
    backgroundColor: '{colors.primary-ink}'
    textColor: '{colors.on-dark}'
    typography: '{typography.caption}'
    rounded: '{rounded.sm}'
    padding: 8px 12px
  accordion:
    backgroundColor: '{colors.surface-elevated}'
    textColor: '{colors.primary-ink}'
    border: '1px solid {colors.line}'
    typography: '{typography.body-small}'
    rounded: '{rounded.sm}'
    padding: 16px 24px
  modal:
    backgroundColor: '{colors.surface-elevated}'
    textColor: '{colors.primary-ink}'
    border: '1px solid {colors.line}'
    typography: '{typography.body-small}'
    rounded: '{rounded.md}'
    padding: 32px
  drawer:
    backgroundColor: '{colors.surface-elevated}'
    textColor: '{colors.primary-ink}'
    border: '1px solid {colors.line}'
    typography: '{typography.body-small}'
    padding: 32px
  empty-state:
    backgroundColor: transparent
    textColor: '{colors.ink-700}'
    border: '1px solid {colors.line}'
    typography: '{typography.body-small}'
    rounded: '{rounded.md}'
    padding: 48px 32px
  skeleton:
    backgroundColor: '{colors.surface}'
    rounded: '{rounded.sm}'
    height: 16px
  divider:
    backgroundColor: '{colors.line}'
    height: 1px
  section:
    backgroundColor: '{colors.background}'
    paddingY: '{spacing.section}'
    maxWidth: 1440px
---

# DESIGN.md: 良禽佳木

> 这是良禽佳木的默认视觉地图。agent 先读这一份；标志与资产的完整规则见文末扩展段。

## Overview

品牌锚点：**以温润克制的高级感与理性秩序感，服务中文语境下重视品质、可信度与审美耐久度的客户。**

- 气质关键词：温润 / 克制 / 高定 / 理性 / 安静 / 耐看
- 视觉隐喻：光线柔和、材质克制的高端家居展厅，有秩序、有空气感、可被慢慢观看
- 整体方向：安静、克制、画册感强；先建立审美高度与信任，再承接产品理解、案例浏览或咨询动作
- 纹理来自真实摄影中的木、石、布、皮革；UI 结构本身保持平整简洁
- 留白充足且有方向感，不做均匀铺满

外部参考（Poliform / Flexform 等）只提取方法：留白比例、影像节奏、材质表达、信息克制。不要复制其页面结构、模块顺序、品类形态或交互签名。

用户明确要求外部风格（例如"喜茶风格"）时，按该风格完成本次产物，不要强行转译回木作风格，也不要写回本文件。

## Colors

| 角色 | 值 | 用途 |
|---|---|---|
| `{colors.primary-ink}` | `#2B2926` | 主文本、品牌锚点、深色分隔面 |
| `{colors.background}` | `#F8F5F0` | 页面主背景 |
| `{colors.surface}` | `#F2EEE8` | 卡片与次级背景 |
| `{colors.surface-elevated}` | `#FFFCF8` | 浮层与强调区块 |
| `{colors.accent}` | `#8B6A4E` | CTA、选中态、重点链接 |
| `{colors.brand-asset}` | `#9E7F63` | logo、标准字与品牌签名区，不替代 CTA accent |
| `{colors.line}` | `#D8D0C4` | 低噪声分隔线与边框 |
| `{colors.ink-900}` | `#1F1D1B` | 最深正文、深色区块底 |
| `{colors.ink-700}` | `#4B4640` | 次级正文与说明 |
| `{colors.ink-500}` | `#888075` | 仅装饰性文字 |
| `{colors.on-dark}` | `#F8F5F0` | 深色区块上的正文 |

状态色：`success` / `warning` / `error` / `info`，只用于状态表达，不承担品牌识别。

使用规则：

- 大面积使用暖白、石灰、烟灰、炭黑等中性色；accent 只用于引导与确认，不允许长时间大面积占据视觉中心。
- 不使用高饱和色块制造注意力，让材质、图像与版式承担高级感。
- 浅色背景上的正文只使用 `ink-900` / `ink-700` / `primary-ink`，禁止浅灰正文落在暖灰背景上。

对比度（按 WCAG 2.1 计算，改色时必须重新核算）：

| 组合 | 比值 | 结论 |
|---|---|---|
| `#1F1D1B` on `#F8F5F0` | 15.45:1 | `ink-900` 作正文与标题首选 |
| `#2B2926` on `#F8F5F0` | 13.34:1 | `primary-ink` 作标题与主文本 |
| `#4B4640` on `#F8F5F0` | 8.59:1 | `ink-700` 作次级正文与说明 |
| `#4B4640` on `#F2EEE8` | 8.08:1 | `ink-700` 在卡片内作正文 |
| `#8B6A4E` on `#F8F5F0` | 4.52:1 | `accent` 作链接与 CTA 文字，刚好达到 AA 正文 |
| `#888075` on `#F8F5F0` | 3.58:1 | `ink-500` 不达 AA 正文，只允许 ≥18px 或纯装饰文字 |
| `#A0743C` on `#F2EEE8` | 3.59:1 | `warning` 不达 AA 正文，只用于边框、图标或大字号 |
| `#F8F5F0` on `#1F1D1B` | 15.45:1 | `on-dark` 在深色区块作正文 |

落地要求：小字说明、表单帮助信息、图注、页脚一律使用 `ink-700` 或更深；状态色只用边框、图标或 ≥18px 文本表达。

## Typography

- **Heading**：`{typography.heading-family}`，宋体方向营造安静与文化感，但不牺牲可读性
- **Body**：`{typography.body-family}`，正文、导航、按钮、表单使用清晰现代的中文无衬线
- **Mono**：`{typography.mono-family}`，数据、编号、工程信息

| Token | 字号 | 行高 | 字距 | 用途 |
|---|---|---|---|---|
| `{typography.display}` | 72px | 1.08 | -0.03em | 首屏主标题 |
| `{typography.heading-1}` | 48px | 1.18 | -0.025em | 一级标题 |
| `{typography.heading-2}` | 36px | 1.24 | -0.02em | 二级标题 |
| `{typography.heading-3}` | 28px | 1.32 | -0.015em | 三级标题 |
| `{typography.heading-4}` | 22px | 1.4 | -0.01em | 卡片标题、列表标题 |
| `{typography.body}` | 17px | 1.82 | 0 | 主正文 |
| `{typography.body-small}` | 15px | 1.72 | 0 | 次正文、表单说明 |
| `{typography.caption}` | 13px | 1.6 | 0.01em | 注释与元信息 |
| `{typography.overline}` | 12px | 1.4 | 0.12em | 分组标签 |

规则：

- 本规范不声明字重。随包字体各自只有一个字重，声明 500 / 600 不会生效；需要强调时用字号、颜色或留白，不要用字重。
- 正文默认 `17px / 1.82`，不得小于 `16px / 1.7`。
- 中文标签可以完整表达，不追求英文式极短导航；一级导航优先 2-6 个中文字符，必要时可更长但必须清楚。
- 负字距只用于大字号标题，正文和按钮字距保持 0。
- `caption` 与 `overline` 属于小字，颜色必须用 `ink-700` 或更深。

## Layout

间距刻度：`{spacing.xxs}` 4px / `{spacing.xs}` 8px / `{spacing.sm}` 12px / `{spacing.md}` 16px / `{spacing.lg}` 24px / `{spacing.xl}` 32px / `{spacing.xxl}` 48px / `{spacing.xxxl}` 64px / `{spacing.section}` 96px / `{spacing.section-lg}` 128px。

- **基准**：8px。不要在刻度之外随手取值。
- **Section rhythm**：常规区块纵向 96px，品牌级大区块 128px。
- 相邻区块之间的间隔由两个 section 各自的内边距叠加形成；不要额外再写 margin，也不要只给单边内边距，否则节奏会和其它页面不一致。
- **Grid**：桌面 12 栏、平板 8 栏、移动 4 栏；内容最大宽度 1440px，槽宽 32 / 24 / 16px。
- **Whitespace**：留白是结构而不是剩余空间；允许局部偏移构图与编辑式断行，不做均匀网格铺满。
- **Density**：spacious。宁可减少信息量，也不要压缩行高与模块间距。
- 组件内边距必须取间距刻度上的值；14px、20px 这类刻度外数值一律不接受。

## Elevation & Depth

| 层级 | 值 | 用途 |
|---|---|---|
| Level 0 | 无阴影 | 默认状态，靠边框与背景差建立层次 |
| Level 1 | `0 8px 24px rgba(31, 29, 27, 0.04)` | 轻浮层、抬起的卡片 |
| Level 2 | `0 18px 44px rgba(31, 29, 27, 0.08)` | 下拉、弹层 |
| Level 3 | `0 28px 72px rgba(31, 29, 27, 0.12)` | 模态、抽屉 |

规则：阴影只表达层级，不用于装饰；同一屏内不要出现两个以上层级的阴影。不使用玻璃拟态、霓虹辉光与彩色阴影。

动效：缓动 `cubic-bezier(0.22, 1, 0.36, 1)`，时长三档：`140ms` / `280ms` / `520ms`。入场为轻微上移淡入（位移不超过 12px），退场为淡出（位移不超过 8px）。视差只允许 2 层、4%-8% 深度。禁止粒子、3D、shader 扭曲、自定义光标与拆字动画，所有动效必须支持 `prefers-reduced-motion` 降级。

## Shapes

| Token | 值 | 用途 |
|---|---|---|
| `{rounded.xs}` | 2px | 分隔条、小标签 |
| `{rounded.sm}` | 6px | 按钮、输入框 |
| `{rounded.md}` | 12px | 卡片、面板 |
| `{rounded.pill}` | 999px | 胶囊标签、圆形头像 |

边框与分隔线：1px 实线，颜色 `{colors.line}`。不使用双线、虚线装饰或粗边框。

## Components

> 不记录 hover 状态：按下与选中态已经表达了交互反馈，hover 属于实现细节。

组件模型按用途分为 10 类：基础内容、导航与寻路、操作按钮、表单输入、选择与确认、反馈与状态、披露与浮层、内容卡片、页面区块、标记与工具。每一类都同时给出 default / active / focus-visible / disabled / error 中适用的状态；不是每个组件都必须出现全部状态。

### Navigation

**`nav-bar`** — 顶部主导航容器。Background `{colors.background}`，text `{colors.ink-700}`，border `1px solid {colors.line}`，typography `{typography.body-small}`，height 72px。一级层级少而准。
**`nav-link`** — 导航项。Text `{colors.ink-700}`，typography `{typography.body-small}`，padding `8px 12px`，rounded `{rounded.xs}`。选中态用 `{colors.accent}` 文字或 2px 下划线表达。
**`nav-cta`** — 导航右侧的咨询入口。Background `{colors.primary-ink}`，text `{colors.background}`，rounded `{rounded.sm}`，height 44px。
**`breadcrumb`** — 面包屑寻路。Text `{colors.ink-700}`，typography `{typography.caption}`，条目间距 8px；只展示真实层级，不把面包屑当装饰。
**`tabs`** — 页内视图切换。底边 1px `{colors.line}`，选中项用 2px `{colors.accent}` 下划线；用于同一内容层的并列视图，不替代主导航。
**`pagination`** — 分页。每页按钮 40×40px，border `{colors.line}`，rounded `{rounded.xs}`，当前页反白；只在真实多页内容中使用。

### Buttons

**`button-primary`** — 主操作按钮，实底深色。Background `{colors.primary-ink}`，text `{colors.background}`，typography `{typography.body-small}`，padding `16px 32px`，rounded `{rounded.sm}`，height 48px。
**`button-primary-active`** — 按下态，背景加深到 `{colors.ink-900}`。
**`button-primary-disabled`** — 禁用态，背景 `{colors.line}`，文字 `{colors.ink-700}`，降低对比而不改变色相。
**`button-secondary`** — 次操作按钮，浅底描边。Background transparent，text `{colors.primary-ink}`，border `1px solid {colors.line}`，height 48px。
**`button-secondary-active`** — 按下态，填充 `{colors.surface}`，边框转为 `{colors.accent}`。
**`button-sm`** — 小尺寸按钮，height 40px、padding `8px 24px`，用于导航、卡片内操作与密集列表。
**`button-lg`** — 大尺寸按钮，height 56px、padding `16px 32px`，typography `{typography.body}`，用于首屏与咨询入口。
**`button-on-dark`** — 深色区块上的按钮。Background `{colors.background}`，text `{colors.primary-ink}`，height 48px；用于 `consultation-cta` 这类深底区块，不要在页面里临时覆盖按钮颜色。
**`button-text-link`** — 内联文字链接。Text `{colors.accent}`，typography `{typography.body-small}`，padding `4px 0`。

### Forms

**`text-input`** — 输入框。Background `{colors.surface-elevated}`，text `{colors.primary-ink}`，border `1px solid {colors.line}`，rounded `{rounded.sm}`，height 48px。
**`text-input-focused`** — 焦点态，边框换成 2px `{colors.accent}`；不允许移除键盘焦点提示。
**`text-input-error`** — 错误态，边框与文字转为 `{colors.error}`。
**`text-input-sm`** — 小尺寸输入框，height 40px、padding `8px 12px`，用于筛选、搜索与紧凑表单。
**`select`** — 下拉选择。Background `{colors.surface-elevated}`，border `1px solid {colors.line}`，height 48px，右侧固定 20px 的 chevron 图标；不要用浏览器默认外观。
**`select-on-dark`** — 深色区块内使用的下拉，Background `{colors.primary-ink}`，text `{colors.on-dark}`；规格同 `select`。
**`textarea`** — 多行输入。最小高度 128px，padding `12px 16px`，只允许纵向拉伸。
**`checkbox`** — 复选。20px 方框，选中态用 `{colors.primary-ink}`；标签文字 `{typography.body-small}`。
**`checkbox-disabled`** — 禁用态，文字降到 `{colors.ink-700}`，控件透明度 0.45。
**`radio`** — 单选。规格同 `checkbox`，用于互斥选项。
**`slider`** — 滑杆。轨道与手柄用 `{colors.primary-ink}`，行高 24px；只在真正需要连续取值时使用。
**`segmented`** — 分段选择器。容器 pill 圆角 + `{colors.surface}` 底，选中项反白；用于 2-4 个互斥视图切换，不要用于导航。
**`stepper`** — 数字步进器。height 40px，两侧按钮各 40px 宽，中间数值居中。
**`form-label`** — 字段标签。Text `{colors.ink-700}`，typography `{typography.body-small}`，padding `0 0 8px`。
**`form-helper`** — 帮助与校验说明。Text `{colors.ink-700}`，typography `{typography.caption}`，padding `8px 0 0`。
**`search-field`** — 搜索输入组合。外层 height 48px，左侧 16px Lucide 搜索图标，内部复用 `text-input`；图标只表达动作，不承担状态。
**`toggle`** — 二元开关。轨道 44×24px，rounded `{rounded.pill}`，关闭 `{colors.line}`、开启 `{colors.primary-ink}`，手柄 `{colors.surface-elevated}`；只用于立即生效的设置。
**`choice-card`** — 卡片式单选。Background `{colors.surface-elevated}`，border `{colors.line}`，rounded `{rounded.md}`，padding 24px，选中态边框 `{colors.accent}`；适合材质、空间或方案选择。

### Content cards

**`card-base`** — 通用信息版块。Background `{colors.surface}`，border `1px solid {colors.line}`，rounded `{rounded.md}`，padding 32px。是信息版块而不是电商卡片。
**`card-material`** — 材质说明卡。Background `{colors.surface-elevated}`，padding 32px，强调真实材质摄影与短说明。
**`card-case`** — 案例卡。Background `{colors.surface}`，padding 0，影像贴顶上、文字在下，影像与卡片圆角一致。
**`card-product`** — 产品卡。Background `{colors.surface-elevated}`，padding 24px；产品图与规格短表并列，不做价格促销块。
**`card-quote`** — 报价卡。Background `{colors.surface-elevated}`，rounded `{rounded.sm}`，padding 24px；总价是唯一主焦点，确认条件次之。

### Page blocks

**`hero-band`** — 品牌首屏区块。Background `{colors.background}`，typography `{typography.display}`，padding `96px 32px`；用摄影与留白建立气质，不堆卖点。
**`section-header`** — 区块标题组。Text `{colors.primary-ink}`，typography `{typography.heading-2}`，padding `0 0 32px`，可配 `eyebrow`。
**`media-frame`** — 图片容器。Background `{colors.surface}`，border `1px solid {colors.line}`，rounded `{rounded.md}`，padding 0；图片不加复杂边框或阴影。
**`spec-table`** — 规格表。Background `{colors.surface-elevated}`，text `{colors.ink-700}`，typography `{typography.body-small}`，padding 16px；用分隔线而不是斑马纹。
**`consultation-cta`** — 咨询入口区块。Background `{colors.primary-ink}`，text `{colors.background}`，typography `{typography.heading-3}`，rounded `{rounded.md}`，padding 48px；文案礼貌邀请，不制造紧迫感。
**`footer`** — 页脚。Background `{colors.surface}`，text `{colors.ink-700}`，typography `{typography.caption}`，padding `64px 32px`；放品牌落款、主要栏目与联系信息。
**`section`** — 页面区块容器。Padding 纵向 `{spacing.section}`，内容宽度上限 1440px；品牌级大区块用 `{spacing.section-lg}`。

### Marks & tags

**`logo-lockup`** — 品牌落款，使用 `assets/brand/` 的真实资产，height 24px，四周净空不小于可见高度的 1/4。
**`pill-tag`** — 胶囊标签，用于材质、工艺、服务标签。Background `{colors.surface}`，text `{colors.ink-700}`，rounded `{rounded.pill}`，padding `8px 16px`。
**`eyebrow`** — 分组小标题。Text `{colors.ink-700}`，typography `{typography.overline}`，uppercase，padding `0 0 16px`。
**`icon`** — 图标。统一使用 Lucide 线性图标（ISC 许可，随包放在 `kit/icons/`），24px 网格，stroke 1.5，颜色跟随文字色；只允许 `icon-sm`(16px) / `icon`(24px) / `icon-lg`(32px) 三个尺寸。无法保证工艺时宁可去掉图标，也不要换一套。
**`icon-sm`** — 16px，用于行内提示、按钮内文字前的小图标。
**`icon-lg`** — 32px，用于空状态或区块入口。
**`placeholder`** — 图片占位块。Background `{colors.surface}`，border `1px solid {colors.line}`，rounded `{rounded.md}`；按 16:10 或 4:3 出图，不要用色块冒充成品图。
**`alert`** — 提示条。Background `{colors.surface}`，text `{colors.ink-700}`，padding `16px 24px`，右侧可带关闭按钮。
**`alert-on-dark`** — 深色提示条，Background `{colors.primary-ink}`，text `{colors.on-dark}`；用于首屏或深底区块内的提示。
**`upload`** — 上传 / 拖拽区。Background `{colors.surface}`，边框 `1px dashed {colors.line}`，最小高度 128px，图标居中；用于资料收集与方案确认阶段。
**`progress`** — 进度条。轨道 `{colors.line}`，已完成段 `{colors.primary-ink}`，高度 4px，pill 圆角；只表达真实进度，不做装饰性动画。

### Feedback & overlays

**`status-badge`** — 状态徽标。Background `{colors.surface}`，text `{colors.ink-700}`，border `{colors.line}`，rounded `{rounded.pill}`，padding `4px 12px`；状态色只用于边框与 8px 状态点，小字保持可读。
**`tooltip`** — 补充提示。Background `{colors.primary-ink}`，text `{colors.on-dark}`，typography `{typography.caption}`，rounded `{rounded.sm}`，padding `8px 12px`；悬停或键盘聚焦出现，不承载必读信息。
**`accordion`** — 折叠披露。Background `{colors.surface-elevated}`，border `{colors.line}`，rounded `{rounded.sm}`，标题 padding `16px 24px`；默认收起，最多展开一项时由页面控制。
**`modal`** — 模态对话框。Background `{colors.surface-elevated}`，border `{colors.line}`，rounded `{rounded.md}`，padding 32px，Level 3 阴影；必须有明确关闭方式，不用于普通说明。
**`drawer`** — 侧边抽屉。Background `{colors.surface-elevated}`，border `{colors.line}`，padding 32px，Level 3 阴影；适合筛选、目录与次要详情，不替代页面导航。
**`empty-state`** — 空状态。Background transparent，text `{colors.ink-700}`，border `{colors.line}`，rounded `{rounded.md}`，padding `48px 32px`；说明为什么为空以及下一步，不用插画硬填版面。
**`skeleton`** — 加载骨架。Background `{colors.surface}`，rounded `{rounded.sm}`，height 16px；只表达真实加载，不循环装饰，`prefers-reduced-motion` 下停用动效。

### Utilities

**`divider`** — 水平分隔线。Background `{colors.line}`，height 1px；用于切断信息组，不使用虚线、双线或粗边框。

### 通用规则

- **Lists**：纵向节奏稳定，标题、摘要、元信息与辅助标签之间关系明确。
- **Iconography**：细线、几何、克制，线宽约 1.25px；无法保证图标工艺时减少或取消图标，而不是用劣质图标填充。
- **状态**：default / active / focus-visible / disabled / error 必须齐全；hover 不记录。
- 组件服务内容、摄影与材质，不让组件自己抢戏。

## Do's and Don'ts

### Do

- 先建立品牌气质与信任，再谈产品、案例与咨询入口
- 用真实摄影、材质、比例与留白表达高级感
- 保持中文可读性优先：字号、行高、标签完整度
- 结构稳定、允许有限变化；换承载方式不换风格语言
- 信息不足时给出结构化 spec、占位或待补资料清单

### Don't

- 不做电商促销风、倒计时、夸张稀缺文案与高饱和色块
- 不做冷感国际模板腔、玻璃拟态、假奢华与炫技动效
- 不用低质量图标、假数据或编造的参数、案例、图片来源
- 不把参考页当模板复制，不照搬其他品牌识别、具体形态、文案或交互签名
- 不把系统说明词、控制面术语、英文元标签泄漏到最终成品
- 不在用户未明确要求时插入 logo，也不用纯文字品牌名冒充标志

## Responsive Behavior

- **Mobile `0-767px`**：4 栏，槽宽 16px。优先保证中文阅读、导航理解与 CTA 易点按；首屏可以更集中，但不能拥挤。
- **Tablet `768-1199px`**：8 栏，槽宽 24px。保留图文层级与卡片模组，不简单等比压缩桌面版。
- **Desktop `1200px+`**：12 栏，槽宽 32px。以宽留白建立高端秩序，可局部使用偏移构图。
- 触控目标不小于 44×44px；正文行宽建议控制在 28-38 个中文字符。
- 移动端标题降一级：`display` 降为 `heading-1`，`heading-1` 降为 `heading-2`，避免大字号撑破版心。
- 区块间距可以收束，但模块内部呼吸感不能被牺牲。

## Iteration Guide

1. 一次只改一个组件，引用它的 YAML 键（如 `{components.card-base}`）。
2. 新增组件必须同时写进 frontmatter 的 `components:` 和本节正文，两边名字一一对应。
3. 状态作为独立条目维护，例如 `button-primary-active`、`text-input-focused`，不要写进正文描述。
4. 不记录 hover 状态；只写 default / active / focus-visible / disabled / error。
5. 任何地方都用 `{token.refs}`，不要内联 hex。
6. 需要强调时先放大字号，再考虑颜色；本规范不提供字重变化。
7. 颜色只用暖中性底 + 低饱和 taupe 这一组关系，不要引入第四种面层色调。
8. 需要生图时把规范压缩成一段短提示词，不要把整份文件塞进提示词。

```text
为良禽佳木生成一版高端中文家居视觉方向：quiet luxury，暖中性色底，低饱和 taupe 强调，编辑式留白，
克制的宋体标题配现代中文无衬线正文，真实木 / 石 / 布 / 皮革材质，低文字密度。
避免电商促销感、高饱和色块、玻璃拟态、假奢华与英文优先的模板腔。
```

## Known Gaps

- 两个 logo 已按图形边界裁切（横向 678×188，纵向 568×419），但最小尺寸与安全边距的正式数值仍待品牌方确认；确认前以"可见字高不低于 24px、印刷不低于 8mm"为准。
- 本规范只定义浅色底与深色区块，没有完整的深色主题令牌。需要深色主题时先补一套令牌，不要临时调色。
- 随包字体各自只有一个字重（Swei Sugar 为 ExtraLight，OPPO Sans 为 Regular），因此本规范不声明字重；需要多字重时先补字体文件。
- 图标、插画与摄影素材没有独立资产规范，只有 Do / Don't 层面的约束。
- 本规范本体是 Markdown；配套代码 UI kit 在 `kit/`。当前没有 Figma 导出或 Storybook，新增可复用代码组件应维护在 `kit/`，不要塞回本文件。

## Brand Mark & Logo

> 扩展段。品牌名统一写 `良禽佳木` 或 `良禽`，不要写成 `梁琴` 或 `梁琴佳木`。

- **横向标志**：页头、页尾、品牌签名区、横向落款的默认选择，文件为 `assets/brand/liangqinjiamu-logo-horizontal.svg`
- **纵向标志**：仅用于竖版品牌页、封面或纵向识别的签名场景，文件为 `assets/brand/liangqinjiamu-logo-vertical.svg`，不要替代横向标志在导航中的位置
- **PNG 降级**：`assets/brand/liangqinjiamu-logo-horizontal.png`、`assets/brand/liangqinjiamu-logo-vertical.png`
- **默认不插 logo**：只有用户明确说"加入 logo / 使用真实标志 / 放横版 logo / 品牌落款"时才使用
- **必须用真实资产**：不得凭记忆重绘字形，也不得用纯文字品牌名冒充标志；读不到资产就停在结构化 spec
- **颜色**：标志自身填充色为 `{colors.brand-asset}`，直接使用文件颜色，不要重新上色
- **最小尺寸**：可见字高不低于 24px（横向按高度直接排版即可，文件已裁切）
- **保护空间**：四周净空不小于标志可见高度的 1/4
- **禁止**：拉伸、描边、加浮雕、加发光、改字距、旋转、叠加在高噪声图像上
