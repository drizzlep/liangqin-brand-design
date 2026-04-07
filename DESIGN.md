# DESIGN.md: Liangqin Ji Mu

> Source of truth: `foundation-dna/design-dna.zh-CN.json`
>
> Generated from `miten-foundation-dna-zh-cn-v2` (`v2.0.0`) as the default AI-facing design brief.

## 1. Visual Theme & Atmosphere

良禽佳木的界面气质应围绕“温润 / 克制 / 高定 / 理性 / 安静 / 耐看”展开。先建立信任与审美判断，再承接咨询或产品理解。锚点句：**以温润克制的高级感与理性秩序感，服务中文语境下重视品质、可信度与审美耐久度的客户。**

视觉隐喻：如同进入光线柔和、材质克制的高端家居展厅：有秩序、有空气感、可被慢慢观看。

品牌不可妥协项：
- 中文优先，允许完整导航、按钮与标签表达
- CTA 必须礼貌、稳妥、非强刺激推销口吻
- 材质、摄影、留白和信息秩序优先于装饰性表现
- 不能滑向电商促销页、通用 SaaS 模板或欧美极简冷感语气

设计风格：
- Mood: calm, premium, tactile, rational, warm
- Genre / Personality: luxury editorial / confident, meticulous, cultured, restrained, trustworthy
- Texture / Whitespace: 纹理主要来自真实摄影中的木、石、布、皮革；UI 结构本身保持平整简洁。 / generous and directional

## 2. Color Palette & Roles

### Primary

- **Primary Ink** (`#2B2926`): 主文本、品牌锚点、深色分隔面与高对比标题
- **Background** (`#F8F5F0`): 页面主背景
- **Surface** (`#F2EEE8`): 卡片 / 次级背景
- **Elevated Surface** (`#FFFCF8`): 浮层 / 强调区块
- **Accent** (`#8B6A4E`): CTA、悬停、重点链接与少量状态强调
- **Brand Asset** (`#9C7F66`): 类目品牌资产专用色，用于良禽佳木 logo、标准字、品牌签名区与少量品牌识别强调，不替代通用 CTA accent。

### Neutral Scale

| Level | Value |
|---|---|
| 0 | `#F8F5F0` |
| 50 | `#F2EEE8` |
| 100 | `#E7E1D8` |
| 200 | `#D8D0C4` |
| 300 | `#C6BDAF` |
| 400 | `#A99F92` |
| 500 | `#888075` |
| 600 | `#6A635B` |
| 700 | `#4B4640` |
| 800 | `#36322E` |
| 900 | `#1F1D1B` |

### Semantic

- **Success** (`#567A62`)
- **Warning** (`#A0743C`)
- **Error** (`#A04F46`)
- **Info** (`#5E7A8E`)

配色策略：
- Palette / Contrast: analogous / dark-on-light dominant with subtle layers
- Accent / Neutral usage: 通用界面 CTA 继续使用 #8B6A4E；品牌识别与 logo 资产允许使用 #9C7F66 作为品牌 taupe。 / 以暖白、石灰、烟灰、炭黑构成主中性色阶；大面积使用浅阶，信息和标题使用 700-900 深阶。

## 3. Typography Rules

字体策略：
- **Heading**: `"Swei Sugar", "Noto Serif SC", "Source Han Serif SC", "Songti SC", serif`
- **Body**: `"OPPO Sans 4.0", "PingFang SC", "Hiragino Sans GB", "Noto Sans SC", sans-serif`
- **Mono**: `"SFMono-Regular", "SF Mono", "Menlo", "Consolas", monospace`
- Notes: 中文大标题默认使用 Swei Sugar（狮尾宋体）ExtraLight 方向营造高级、安静、带文化感的品牌气质；正文、摘要、导航、按钮与表单默认使用 OPPO Sans 4.0，保证中文界面的清晰度、稳定性与现代感。

| Role | Size | Weight | Line Height | Tracking | Font Family | Usage |
|---|---:|---:|---:|---:|---|---|
| Display | 72px | 500 | 1.08 | -0.03em | "Swei Sugar", "Noto Serif SC", "Source Han Serif SC", "Songti SC", serif | 首屏主标题 |
| Heading 1 | 48px | 500 | 1.18 | -0.025em | "Swei Sugar", "Noto Serif SC", "Source Han Serif SC", "Songti SC", serif | 一级标题 |
| Heading 2 | 36px | 500 | 1.24 | -0.02em | "Swei Sugar", "Noto Serif SC", "Source Han Serif SC", "Songti SC", serif | 二级标题 |
| Heading 3 | 28px | 500 | 1.32 | -0.015em | "Swei Sugar", "Noto Serif SC", "Source Han Serif SC", "Songti SC", serif | 三级标题 |
| Body | 17px | 400 | 1.82 | 0 | "OPPO Sans 4.0", "PingFang SC", "Hiragino Sans GB", "Noto Sans SC", sans-serif | 正文与摘要 |
| Body Small | 15px | 400 | 1.72 | 0 | "OPPO Sans 4.0", "PingFang SC", "Hiragino Sans GB", "Noto Sans SC", sans-serif | 次正文与表单说明 |
| Caption | 13px | 400 | 1.6 | 0.01em | "OPPO Sans 4.0", "PingFang SC", "Hiragino Sans GB", "Noto Sans SC", sans-serif | 注释与元信息 |
| Overline | 12px | 500 | 1.4 | 0.12em | "OPPO Sans 4.0", "PingFang SC", "Hiragino Sans GB", "Noto Sans SC", sans-serif | 标签与分组标题 |

中文排版默认规则：
- 标题：大标题优先使用 Swei Sugar（狮尾宋体），控制单行长度与换行位置，避免依靠过强字距制造高级感。
- 正文：正文、摘要、导航、按钮、表单统一使用 OPPO Sans 4.0，默认不少于 16px，并保持较宽松行高。
- 标签：导航、按钮、标签与表单字段名称允许更完整的中文表达，不以极短英文式标签为目标。
- 回退：当自定义字体加载失败时，正文优先回退到 PingFang SC / Noto Sans SC，标题优先回退到 Source Han Serif SC / Songti SC。

## 4. Component Stylings

- **Buttons**: 以实底深色按钮和浅底描边按钮为主，默认高度 44-48px，文案礼貌直接，不使用高饱和色块。
- **Inputs**: 白底或浅石色底，1px 边框，内边距充足，标签与帮助信息层级必须清晰。
- **Cards**: 更像信息版块而不是电商卡片；弱边框、弱阴影、大图或大留白优先。
- **Navigation**: 顶部主导航保持稀疏与明确，一级层级少而准；移动端优先保证检索与路径理解。
- **Modal / Drawer**: 采用安静的居中浮层或抽屉，背景遮罩偏轻，避免玻璃与重模糊。
- **Lists**: 采用节奏稳定的纵向列表，标题、摘要、元信息和辅助标签之间关系明确。
- **Component rule**: 组件继承品牌秩序而非自我表现：按钮、导航、表单、卡片都必须让位于内容、摄影与材质表达。

## 5. Layout Principles

- Base unit: `8px`
- Spacing scale: `4px, 8px, 12px, 16px, 24px, 32px, 48px, 64px, 96px, 128px`
- Section rhythm: 以 96px / 128px 为主节奏，长页面用 64px 作为次节奏，模块内部保持 16px / 24px / 32px 的递进关系。
- Grid: `12-column modular grid`
- Max content width: `1440px`
- Columns: desktop `12` / tablet `8` / mobile `4`
- Gutters: desktop `32px` / tablet `24px` / mobile `16px`
- Alignment / Balance: strict grid with selective centered hero compositions / asymmetric
- Negative space role: 留白是高端感的主要组成，不只是空出来，而是用来给摄影、文字和品牌留呼吸。

Shape system：
- Radius: small `2px` / medium `6px` / large `12px` / pill `999px`
- Border / Divider: subtle 1px / 1px 实线细分隔，优先使用 #D8D0C4；必要时用图像留白和版心对齐替代分割线。

## 6. Depth & Elevation

| Level | Value | Usage |
|---|---|---|
| Low | `0 8px 24px rgba(31, 29, 27, 0.04)` | 轻层级卡片与弱强调区 |
| Medium | `0 18px 44px rgba(31, 29, 27, 0.08)` | 浮层与重点信息块 |
| High | `0 28px 72px rgba(31, 29, 27, 0.12)` | 强强调层与高优先级内容 |

深度与动效规则：
- Shadow style: soft diffused
- Depth cues: 主要通过色面层差、图文叠放和克制阴影表达深度，不采用厚重投影。
- Easing: `cubic-bezier(0.22, 1, 0.36, 1)`
- Duration scale: micro `140ms` / normal `280ms` / macro `520ms`
- Entrance: fade-up with slight translateY(12px)
- Exit: fade-out with slight translateY(-8px)
- Composite / Image / Background: 整体特效策略应以'几乎感觉不到特效存在，但能感到页面很顺'为原则。首屏允许极轻微视频或弱视差，其余区域以摄影、留白、排版节奏为主，确保中文客户不会因过度实验性动效而产生距离感。 / 图片进入视口时可做轻微裁切揭示与弱缩放，悬停时只允许细微位移或亮度变化。 / 仅在首页或品牌级首屏可选用静音、缓慢、材质导向的视频背景；其余页面默认使用静态摄影。

## 7. Do's and Don'ts

### Do

- 高级但不疏离：气质来自材质、比例、留白与影像，不来自夸张修饰。
- 温润且安静：避免情绪过热与强刺激配色，让用户感到稳妥、松弛、可信。
- 秩序清晰：信息层级、栅格、对齐与节奏必须清楚，支撑品牌专业度。
- 强调触感与材质：通过摄影、文字与色彩去传达木、石、布、皮革等真实触感。
- 中文优先可读：中文正文字重、字号、行高与标签长度必须优先于西文美感。
- 按钮、主要链接与表单控件的有效点击高度不低于 44px。
- 所有动效遵守 `minimal functional`，并支持 reduced motion 降级
- 把摄影、材质、留白和结构层级放在所有视觉修饰之前

### Don't

- 高饱和品牌主色占据大面积界面
- 复杂粒子、炫光、液态变形等喧宾夺主特效
- 过度纤细且不适合中文的标题排版
- 英文式超短导航和按钮文案
- 为追求高级感而牺牲导航、表单与信息可理解性
- 不使用粒子系统、shader 扭曲、默认 3D 语言或自定义鼠标特效
- 不为了“高级感”牺牲中文可读性、路径理解和表单说明
- 不让 accent 长时间、大面积占据视觉中心

## 8. Responsive Behavior

| Breakpoint | Range / Strategy |
|---|---|
| Mobile | `0-767px` / 优先保证中文阅读、导航理解与 CTA 易点按；首屏允许更集中，但不能拥挤。 |
| Tablet | `768-1199px` / 缩减为 8 栏，保留图文层级与卡片模组，不简单等比压缩桌面版。 |
| Desktop | `1200px+` / 以 12 栏与宽留白建立高端秩序，可局部使用偏移构图和编辑式断行。 |

响应式要求：
- Navigation: 移动端导航可采用横向滑动目录或折叠目录，但命名必须完整、层级必须明确。
- Section density: 移动端区块间距可从 96px 收束到 64px，但模块内部呼吸感不能被牺牲。
- Contrast / Focus visibility: 正文与背景保持稳定高对比，浅色背景上的正文优先使用 700-900 深阶；禁止浅灰正文落在暖灰背景上。 / 键盘焦点必须可见，建议使用 1px 深色描边加低强度外发光或底线增强。
- Motion safety / Content clarity: 所有 reveal、hover 与滚动动效都必须支持 prefers-reduced-motion 降级。 / 错误、成功、帮助与空状态信息必须直接说明问题与下一步，不使用隐喻或玩笑化表达。

## 9. Agent Prompt Guide

Use this DESIGN.md to lock the non-negotiable brand feel before exploring layout or style variation.

Prompt checklist:
- 优先中文，导航、按钮、标签允许完整表达
- 先用摄影、材质说明、留白和结构建立信任，再谈装饰
- CTA 语气使用 `subtle suggestion`，避免命令式压迫感
- 交互反馈保持 `quiet and precise`，hover 只做微弱变化
- 如果与品牌边界冲突，永远回到 `foundation-dna/design-dna.zh-CN.json` 里的规则

Suggested prompt:

```text
Build a Chinese premium home furnishing page for Liangqin Ji Mu.
Use a calm, tactile, editorial visual language with generous whitespace,
warm neutral surfaces, serif-led headlines, and restrained interactions.
Keep copy polite and trustworthy. Prefer “查看 / 了解 / 预约 / 咨询”
style CTAs. Avoid e-commerce promo styling, loud gradients, glassmorphism,
particle effects, and experimental motion that harms readability.
```
