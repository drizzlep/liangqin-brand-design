#!/usr/bin/env python3
import argparse
import json
import shutil
from pathlib import Path

from sync_openclaw_mirrors import sync_openclaw_mirrors


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "skills" / "public" / "liangqin-brand-openclaw"
RELEASE_METADATA = SOURCE / "skill-release.json"
FOUNDATION_DNA_SOURCE = ROOT / "foundation-dna"
DESIGN_PACKS_SOURCE = ROOT / "design-packs"
ARTIFACT_SURFACES_SOURCE = ROOT / "artifact-surfaces"
BRAND_ASSETS_SOURCE = ROOT / "assets" / "brand"
EVALUATION_SOURCE = ROOT / "evaluation"
STANDARD_MANIFEST = ROOT / "design-standard-package.json"
CONSUMER_GUIDE = ROOT / "CONSUMER-GUIDE.zh-CN.md"
EXPORTED_FOUNDATION_FILES = [
    "design-dna.zh-CN.json",
    "tokens.semantic.json",
]


def load_release_metadata() -> dict:
    if not RELEASE_METADATA.exists():
        raise SystemExit(f"release metadata missing: {RELEASE_METADATA}")
    return json.loads(RELEASE_METADATA.read_text(encoding="utf-8"))


def main() -> int:
    release_metadata = load_release_metadata()
    sync_openclaw_mirrors(ROOT)
    package_slug = release_metadata["package_slug"]
    display_name = release_metadata["display_name"]
    version = release_metadata["version"]
    entry_keyword = release_metadata["entry_keyword"]

    parser = argparse.ArgumentParser(
        description="导出良禽佳木 OpenClaw Skill 为独立可分发目录"
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        help="导出目标目录，脚本会在其下创建发行包子目录",
    )
    parser.add_argument(
        "--zip",
        action="store_true",
        help="额外输出一个适合 GitHub Release 的 zip 包",
    )
    args = parser.parse_args()

    output_root = Path(args.output_dir).resolve()
    output_root.mkdir(parents=True, exist_ok=True)
    export_dir = output_root / package_slug
    legacy_export_dir = output_root / release_metadata["source_slug"]

    if export_dir.exists():
        shutil.rmtree(export_dir)
    if legacy_export_dir.exists() and legacy_export_dir != export_dir:
        shutil.rmtree(legacy_export_dir)

    shutil.copytree(SOURCE, export_dir)
    shutil.copy2(RELEASE_METADATA, export_dir / "skill-release.json")
    shutil.copy2(ROOT / "DESIGN.md", export_dir / "DESIGN.md")
    shutil.copy2(CONSUMER_GUIDE, export_dir / "CONSUMER-GUIDE.zh-CN.md")
    shutil.copy2(ROOT / "DESIGN-GOVERNANCE.md", export_dir / "DESIGN-GOVERNANCE.md")
    shutil.copy2(ROOT / "EXECUTION-CHECKLIST.md", export_dir / "EXECUTION-CHECKLIST.md")
    shutil.copy2(STANDARD_MANIFEST, export_dir / "design-standard-package.json")
    if DESIGN_PACKS_SOURCE.exists():
        shutil.copytree(DESIGN_PACKS_SOURCE, export_dir / "design-packs")
    if ARTIFACT_SURFACES_SOURCE.exists():
        shutil.copytree(ARTIFACT_SURFACES_SOURCE, export_dir / "artifact-surfaces")
    if BRAND_ASSETS_SOURCE.exists():
        shutil.copytree(BRAND_ASSETS_SOURCE, export_dir / "assets" / "brand")
    if EVALUATION_SOURCE.exists():
        if (export_dir / "evaluation").exists():
            shutil.rmtree(export_dir / "evaluation")
        shutil.copytree(EVALUATION_SOURCE, export_dir / "evaluation")

    foundation_dir = export_dir / "foundation-dna"
    foundation_dir.mkdir(parents=True, exist_ok=True)
    for relative_name in EXPORTED_FOUNDATION_FILES:
        shutil.copy2(FOUNDATION_DNA_SOURCE / relative_name, foundation_dir / relative_name)

    readme_path = export_dir / "OPENCLAW_INSTALL.md"
    readme_path.write_text(
        "\n".join(
            [
                f"# {display_name} 安装说明",
                "",
                f"- 当前发行包：`{package_slug}`",
                f"- 对外推荐触发词：`{entry_keyword}`",
                "- 对外兼容触发词：`良禽佳木品牌体`",
                "- 对内稳定 slug：`liangqin-brand-openclaw`",
                f"- 当前版本：`{version}`",
                "- 旧名 `liangqin-brand-openclaw` 仅作迁移兼容说明，不再作为推荐入口。",
                "- 旧的公关稿、品牌通稿、`/小强体`、`/厂长模式`、`/硬核木匠` 仅保留为次级写作能力，不再作为顶层品牌入口。",
                "",
                "## 入口路由",
                "",
                "默认优先使用 `良禽品牌体 / 良禽佳木品牌体` 作为顶层品牌入口。",
                "",
                "以下请求应直接交给 `良禽品牌体 / 良禽佳木品牌体`：",
                "",
                "- 首页",
                "- 产品详情",
                "- 品牌页",
                "- `DESIGN.md` / 设计系统",
                "- 页面蓝图、模块编排、品牌视觉约束",
                "- 图片、长图、海报、视觉稿、报价卡图、图标方案",
                "- 风格切换，例如：`良禽佳木apple风`",
                "",
                "只有当用户明确要求写公关稿、品牌通稿或文章时，才应转交给次级写作能力。",
                "",
                "所有良禽视觉类请求都建议先进入 `良禽品牌体 / 良禽佳木品牌体`，先产出结构化 spec，再按渠道适配到图片、页面、长图、卡片或动效。",
                "",
                "## 安装方式",
                "",
                f"1. 将整个 `{package_slug}/` 目录复制到目标 OpenClaw skills 目录；或直接运行：",
                "```bash",
                "python3 scripts/install_into_openclaw.py",
                "```",
                "2. 确保保留 `DESIGN.md`、`CONSUMER-GUIDE.zh-CN.md`、`DESIGN-GOVERNANCE.md`、`design-standard-package.json`、`foundation-dna/design-dna.zh-CN.json`、`foundation-dna/tokens.semantic.json`、`artifact-surfaces/`、`design-packs/`、`assets/brand/asset-manifest.zh-CN.json`、`SKILL.md`、`protocols/`、`recipes/`、`examples/`、`evaluation/` 与 `skill-release.json`。",
                "3. 安装后请保留 `EXECUTION-CHECKLIST.md`、`protocols/brand-assets.zh-CN.json`、`assets/brand/asset-manifest.zh-CN.json` 与 `assets/brand/`，这是最终视觉成品的 logo 运行时依赖。",
                "4. 默认先读取 `DESIGN.md` 与 `CONSUMER-GUIDE.zh-CN.md`，再读取 `protocols/brand-boundaries.zh-CN.json`、`protocols/brand-assets.zh-CN.json` 与 `recipes/module-recipes.zh-CN.json`。",
                "5. 如果工具只支持 Tier 1，至少保住 `DESIGN.md`；如果支持 Tier 2，请同时读取 `artifact-surfaces/` 与 `assets/brand/`。",
                "6. 如果用户明确说“良禽佳木apple风”，再补读 `design-packs/liangqin-apple.json`。",
                "7. 优先按 `SKILL.md` 中的输入合同喂入品牌 brief、产品资料和参考页面；若真实 logo 资产不可读，只允许输出结构化 spec。",
            ]
        )
        + "\n"
    )

    if args.zip:
        archive_base = output_root / f"{package_slug}-{version}"
        if archive_base.with_suffix(".zip").exists():
            archive_base.with_suffix(".zip").unlink()
        shutil.make_archive(str(archive_base), "zip", root_dir=output_root, base_dir=package_slug)

    print(f"exported to {export_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
