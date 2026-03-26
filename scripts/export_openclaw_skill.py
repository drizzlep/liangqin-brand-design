#!/usr/bin/env python3
import argparse
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "skills" / "public" / "liangqin-brand-openclaw"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="导出良禽佳木 OpenClaw Skill 为独立可分发目录"
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        help="导出目标目录，脚本会在其下创建 liangqin-brand-openclaw 子目录",
    )
    args = parser.parse_args()

    output_root = Path(args.output_dir).resolve()
    output_root.mkdir(parents=True, exist_ok=True)
    export_dir = output_root / "liangqin-brand-openclaw"

    if export_dir.exists():
        shutil.rmtree(export_dir)

    shutil.copytree(SOURCE, export_dir)

    readme_path = export_dir / "OPENCLAW_INSTALL.md"
    readme_path.write_text(
        "\n".join(
            [
                "# Liangqin Brand OpenClaw Skill 安装说明",
                "",
                "1. 将整个 `liangqin-brand-openclaw/` 目录复制到目标 OpenClaw skills 目录。",
                "2. 确保保留 `SKILL.md`、`protocols/`、`recipes/`、`examples/`、`evaluation/`。",
                "3. 优先按 `SKILL.md` 中的输入合同喂入品牌 brief、产品资料和参考页面。",
            ]
        )
        + "\n"
    )

    print(f"exported to {export_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
