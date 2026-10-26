# Liangqin Brand Design Agent Rules

本仓库是良禽佳木的品牌设计规范包。`DESIGN.md` 是唯一对外规范真源，`skills/public/liangqin-brand-body/` 是把它分发给各 AI 助手的技能入口。

## 项目理解

- 理解品牌与视觉方向，只读 `DESIGN.md`。
- 理解仓库结构与分发方式，读 `README.md`。
- 需要机器可读 token 时读 `tokens/`；需要真实标志时读 `assets/brand/`。
- 需要接入某个 AI 工具时读 `skills/public/liangqin-brand-body/adapters/README.zh-CN.md`。
- 品牌名统一写 `良禽佳木` 或 `良禽`，不要写成 `梁琴` 或 `梁琴佳木`。
- `archive/` 是冻结的历史层，默认不读、不维护、不随包发行。

## 规范改动规则

- 改色彩、字体、字号、间距、圆角、阴影、标志用法时，只改 `DESIGN.md` 与 `tokens/`，并保持两处数值一致。
- 保持标准段落（Overview / Colors / Typography / Layout / Elevation & Depth / Shapes / Components / Do's and Don'ts / Responsive Behavior / Iteration Guide / Known Gaps）的名字与顺序不变；品牌扩展内容只能排在这些段落之后。
- 不要在 `DESIGN.md` 里写示例集或 demo 清单；提示词指南保持一段短提示词。
- 改完后运行 `python3 scripts/build_skill.py`，构建与校验一起完成。
- 不要在 `dist/` 里手改文件，那是生成物。
- 不要重新引入 OpenClaw / Hermes 的适配文件；将来需要时按 `adapters/` 的接入契约新增一节。

## 视觉与品牌边界

- 气质是温润、克制、专业、高级、松弛。
- 高级感来自材质、比例、留白、秩序和中文可读性，不来自夸张特效或促销色块。
- 不做电商促销风、冷感国际模板风、炫技动效风。
- 用户明确要求外部风格时（例如"喜茶风格"），按当前任务方向使用，但不要写回 `DESIGN.md`。
- 不要编造产品事实、参数、报价、图片来源或案例信息；素材不足时标成草稿、占位或待确认。

## 工作与验收

- 需要人工判断、比较或审批的产物，优先做 HTML review board，不要只给 Markdown、CSV、JSON 或命令行结果。
- 视觉或 UI 问题要验证真实页面、真实尺寸和真实可见效果；改 `preview.html` 后至少在浏览器里看过一遍。
- 改代码后运行最快、最相关的检查：`python3 scripts/build_skill.py --check` 与 `python3 -m unittest discover -s tests -p "test_*.py"`。
- 改文档时至少检查文件存在、内容完整、命名和语气一致。
