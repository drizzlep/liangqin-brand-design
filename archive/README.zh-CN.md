# 归档层

这里是冻结的历史文件。默认不读、不维护、不随技能包发行。

保留它们的目的是：需要时能查回原样，而不是让它们继续参与日常读取路径。

## 目录

| 路径 | 内容 | 为什么退役 |
|---|---|---|
| `legacy-runtimes/openclaw/` | OpenClaw 安装说明、消费指南、发布流程、本地 skill 维护流程、安装脚本 | OpenClaw 已放弃，改为运行时中立接入 |
| `legacy-runtimes/hermes/` | Hermes 决策备忘、消费契约、smoke playbook 与记录 | Hermes 已放弃 |
| `legacy-layers/` | 蓝图 schema、模块 recipe、design pack、artifact surface、评测集、旧治理文档 | 中间层过重，规范本身已足够约束日常交付 |
| `legacy-v2-pages/` | 旧 demo 页面与 `styles.css` / `app.js` | v3.0.0 起只保留 `preview.html` 作为可视化对照页 |
| `legacy-v2-standard/` | 旧示例目录、`foundation-dna/`、`.impeccable.md` | 规范真源收敛到 `DESIGN.md`，token 导出移到 `tokens/` |
| `legacy-scripts/` | 生成器、镜像同步、发布准备、本地 skill 维护等脚本 | 随模型能力提升不再需要，改为两个轻脚本 |
| `legacy-tests/` | 与上述脚本和旧结构绑定的测试 | 随被删结构一起退役 |
| `legacy-releases/` | 2.x 的发行 zip | 保留发布记录 |
| `font-subset-corpus.txt` | 字体子集化时使用的字符语料（旧命名版） | 字体子集已生成完毕，语料不再参与默认流程 |

## 恢复方式

这些文件仍在 git 历史里。需要某一份时，优先用 `git log --follow` 找到它，而不是把整个目录搬回来。

如果将来要重新接入 OpenClaw 或 Hermes，按 `skills/public/liangqin-brand-body/adapters/README.zh-CN.md` 的接入契约新增一节即可，不需要恢复旧适配文件。
