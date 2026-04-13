#!/usr/bin/env python3
"""Sync root standard-package files into the OpenClaw adapter mirror."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STANDARD_EVALUATION_DIR = ROOT / "evaluation"
STANDARD_EVALUATION_EXAMPLES_DIR = STANDARD_EVALUATION_DIR / "examples"
OPENCLAW_EVALUATION_DIR = (
    ROOT / "skills" / "public" / "liangqin-brand-openclaw" / "evaluation"
)
OPENCLAW_EXAMPLES_DIR = (
    ROOT / "skills" / "public" / "liangqin-brand-openclaw" / "examples"
)
STANDARD_ASSET_MANIFEST_PATH = ROOT / "assets" / "brand" / "asset-manifest.zh-CN.json"
OPENCLAW_BRAND_ASSET_PROTOCOL_PATH = (
    ROOT
    / "skills"
    / "public"
    / "liangqin-brand-openclaw"
    / "protocols"
    / "brand-assets.zh-CN.json"
)

MIRROR_ROLE = "openclaw_adapter_evaluation_mirror"
MIRROR_NOTE = "仅补充 OpenClaw 落地语境，不反向覆盖根层标准评测规则。"
PROTOCOL_MIRROR_ROLE = "openclaw_adapter_protocol_mirror"


def build_markdown_mirror(source_relative_path: str, source_text: str) -> str:
    return (
        f"> OpenClaw mirror of: `{source_relative_path}`\n"
        f"> {MIRROR_NOTE}\n\n"
        f"{source_text.lstrip()}"
    )


def build_json_mirror(source_relative_path: str, payload: dict) -> dict:
    adapter_scope = "OpenClaw 镜像可补充适配器语境，但不得改变根层标准的核心 case id 与检查目标。"
    mirrored: dict = {}

    for key in ["version", "brand"]:
        if key in payload:
            mirrored[key] = payload[key]

    mirrored["source_of_truth"] = source_relative_path
    mirrored["mirror_role"] = MIRROR_ROLE
    mirrored["adapter_scope"] = adapter_scope

    for key, value in payload.items():
        if key not in mirrored:
            mirrored[key] = value

    return mirrored


def build_brand_assets_protocol_mirror(payload: dict) -> dict:
    mirrored: dict = {
        "version": payload["version"],
        "brand": payload["brand"],
        "source_of_truth": "assets/brand/asset-manifest.zh-CN.json",
        "mirror_role": PROTOCOL_MIRROR_ROLE,
        "package_role": "openclaw_adapter_brand_assets_protocol_mirror",
        "adapter_scope": "OpenClaw 协议镜像可补充适配器执行语境，但不得改变根层资产清单与阻断规则。",
        "purpose": "声明良禽品牌体在 OpenClaw 运行时必须可读取的品牌识别资产，避免视觉交付退化成纯文字品牌名或误判 logo 缺失。",
        "consumption_tier": payload["consumption_tier"],
        "required_runtime_assets": payload["required_runtime_assets"],
        "delivery_guardrails": payload["delivery_guardrails"],
        "icon_relationship": payload["icon_relationship"],
        "adapter_notes": {
            "cross_tool_role": "为 Tier 2 及以上消费层提供稳定品牌资产约束。",
            "missing_asset_default": "无真实 logo 资产时停在结构化 spec，不直出成品。"
        },
    }
    return mirrored


def sync_openclaw_mirrors(root: Path = ROOT) -> list[Path]:
    standard_dir = root / "evaluation"
    mirror_dir = root / "skills" / "public" / "liangqin-brand-openclaw" / "evaluation"

    if not standard_dir.exists():
        raise FileNotFoundError(f"missing standard evaluation directory: {standard_dir}")

    mirror_dir.mkdir(parents=True, exist_ok=True)
    written_paths: list[Path] = []

    for source_path in sorted(standard_dir.glob("*")):
        if not source_path.is_file():
            continue

        source_relative_path = f"evaluation/{source_path.name}"
        mirror_path = mirror_dir / source_path.name

        if source_path.suffix == ".md":
            source_text = source_path.read_text(encoding="utf-8")
            mirror_text = build_markdown_mirror(source_relative_path, source_text)
            mirror_path.write_text(mirror_text, encoding="utf-8")
            written_paths.append(mirror_path)
            continue

        if source_path.suffix == ".json":
            payload = json.loads(source_path.read_text(encoding="utf-8"))
            mirrored_payload = build_json_mirror(source_relative_path, payload)
            mirror_path.write_text(
                json.dumps(mirrored_payload, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            written_paths.append(mirror_path)

    return written_paths


def sync_openclaw_brand_assets(root: Path = ROOT) -> list[Path]:
    asset_manifest_path = root / "assets" / "brand" / "asset-manifest.zh-CN.json"
    protocol_path = (
        root
        / "skills"
        / "public"
        / "liangqin-brand-openclaw"
        / "protocols"
        / "brand-assets.zh-CN.json"
    )

    if not asset_manifest_path.exists():
        raise FileNotFoundError(f"missing asset manifest: {asset_manifest_path}")

    protocol_path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.loads(asset_manifest_path.read_text(encoding="utf-8"))
    mirrored_payload = build_brand_assets_protocol_mirror(payload)
    protocol_path.write_text(
        json.dumps(mirrored_payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return [protocol_path]


def sync_openclaw_examples(root: Path = ROOT) -> list[Path]:
    examples_dir = root / "evaluation" / "examples"
    mirror_dir = root / "skills" / "public" / "liangqin-brand-openclaw" / "examples"

    if not examples_dir.exists():
        raise FileNotFoundError(f"missing standard evaluation examples directory: {examples_dir}")

    mirror_dir.mkdir(parents=True, exist_ok=True)
    written_paths: list[Path] = []

    for source_path in sorted(examples_dir.glob("*.json")):
        payload = json.loads(source_path.read_text(encoding="utf-8"))
        mirror_path = mirror_dir / source_path.name
        mirror_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        written_paths.append(mirror_path)

    return written_paths


def main() -> int:
    written_paths = []
    written_paths.extend(sync_openclaw_mirrors())
    written_paths.extend(sync_openclaw_brand_assets())
    written_paths.extend(sync_openclaw_examples())
    print(f"synced {len(written_paths)} OpenClaw mirror files")
    for path in written_paths:
        print(path.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
