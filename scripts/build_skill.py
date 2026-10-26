#!/usr/bin/env python3
"""构建良禽佳木品牌体发行包（v3.0.0）。

做三件事：
1. 校验 SKILL.md / DESIGN.md 的 frontmatter、章节与引用
2. 交叉核对 DESIGN.md 与 tokens/ 下的 token 导出
3. 把规范文件组装到 dist/liangqin-brand-body/

刻意不做的事：不生成 HTML、不渲染预览、不做运行时适配。
frontmatter 采用受约束的 YAML 子集（2 空格缩进映射 + 引号标量 + 行内列表），
解析器只接受这个子集，越界写法直接报错，而不是被静默忽略。
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGE_NAME = "liangqin-brand-body"
SKILL_SRC = ROOT / "skills" / "public" / PACKAGE_NAME
OUTPUT_DIR = ROOT / "dist" / PACKAGE_NAME
TOKENS_PATH = ROOT / "tokens" / "tokens.semantic.json"

# 标准段落，顺序即规范顺序；扩展段必须排在标准段落之后。
DESIGN_SECTIONS = [
    "## Overview",
    "## Colors",
    "## Typography",
    "## Layout",
    "## Elevation & Depth",
    "## Shapes",
    "## Components",
    "## Do's and Don'ts",
    "## Responsive Behavior",
    "## Iteration Guide",
    "## Known Gaps",
]

EXTENSION_SECTIONS = ["## Brand Mark & Logo"]

DESIGN_FRONTMATTER_KEYS = [
    "version",
    "name",
    "description",
    "colors",
    "typography",
    "rounded",
    "spacing",
    "components",
]

LEGACY_NAME_PATTERN = re.compile(r"openclaw|hermes", re.IGNORECASE)
ASSET_REFERENCE = re.compile(r"assets/[A-Za-z0-9._/-]+\.(?:svg|png|woff2|css)")
TOKEN_REFERENCE = re.compile(r"\{([a-z0-9.\-]+)\}")
QUOTED = re.compile(r"^'[^']*'$|^\"[^\"]*\"$")
PLAIN_NUMBER = re.compile(r"^-?\d+(?:\.\d+)?$")
FLOW_LIST = re.compile(r"^\[(.*)\]$")
YAML_SPECIAL = set('{}[]"\'#,&:*!|>%@`')

PACKAGE_FILES = [
    ("DESIGN.md", ROOT / "DESIGN.md"),
    ("preview.html", ROOT / "preview.html"),
    ("kit/kit.css", ROOT / "kit" / "kit.css"),
    ("kit/index.html", ROOT / "kit" / "index.html"),
    ("kit/templates/homepage.html", ROOT / "kit" / "templates" / "homepage.html"),
    (
        "kit/templates/product-detail.html",
        ROOT / "kit" / "templates" / "product-detail.html",
    ),
    ("kit/templates/README.zh-CN.md", ROOT / "kit" / "templates" / "README.zh-CN.md"),
    ("tokens/tokens.semantic.json", TOKENS_PATH),
    ("tokens/tokens.css", ROOT / "tokens" / "tokens.css"),
    ("scripts/check_page.py", ROOT / "scripts" / "check_page.py"),
]

FONT_FILES = [
    "SweiSugarCJKtc-ExtraLight.woff2",
    "OPPO-Sans-4.0.woff2",
]


class FrontmatterError(ValueError):
    pass


def split_frontmatter(path: Path) -> tuple[list[str], str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise FrontmatterError(f"{path.name} 缺少 YAML frontmatter")
    end = text.find("\n---\n", 3)
    if end == -1:
        raise FrontmatterError(f"{path.name} 的 frontmatter 没有结束标记")
    return text[4:end].splitlines(), text


def parse_scalar(raw: str, context: str) -> object:
    value = raw.strip()
    flow = FLOW_LIST.match(value)
    if flow:
        items = [item.strip() for item in flow.group(1).split(",") if item.strip()]
        return [parse_scalar(item, context) for item in items]
    if QUOTED.match(value):
        return value[1:-1]
    if PLAIN_NUMBER.match(value):
        return int(value) if "." not in value else float(value)
    if value and not (set(value) & YAML_SPECIAL) and not value.startswith(("- ", "? ")):
        return value
    raise FrontmatterError(
        f"{context} 的标量包含 YAML 特殊字符，必须加引号，当前为：{value!r}"
    )


def parse_frontmatter(path: Path) -> tuple[dict, str]:
    """只接受受约束的 YAML 子集：2 空格缩进映射、引号标量、行内列表。"""
    lines, text = split_frontmatter(path)
    root: dict = {}
    stack: list[tuple[int, dict]] = [(-1, root)]
    for number, line in enumerate(lines, start=2):
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip(" "))
        if indent % 2:
            raise FrontmatterError(f"{path.name}:{number} 缩进必须是 2 的倍数")
        if line.lstrip().startswith("- "):
            raise FrontmatterError(f"{path.name}:{number} 不接受块状列表，请用 [a, b] 行内写法")
        body = line.strip()
        if ":" not in body:
            raise FrontmatterError(f"{path.name}:{number} 不是 key: value 形式")
        key, _, raw_value = body.partition(":")
        key = key.strip()
        if not key or " " in key:
            raise FrontmatterError(f"{path.name}:{number} 的键名非法：{key!r}")
        while stack and indent <= stack[-1][0]:
            stack.pop()
        if not stack:
            raise FrontmatterError(f"{path.name}:{number} 缩进层级无法归属")
        parent = stack[-1][1]
        if raw_value.strip() == "":
            node: dict = {}
            parent[key] = node
            stack.append((indent, node))
        else:
            parent[key] = parse_scalar(raw_value, f"{path.name}:{number} {key}")
    return root, text


def walk_values(node, prefix="") -> dict[str, object]:
    found: dict[str, object] = {}
    if isinstance(node, dict):
        for key, value in node.items():
            found.update(walk_values(value, f"{prefix}.{key}" if prefix else key))
    else:
        found[prefix] = node
    return found


def resolve_refs(frontmatter: dict, block: str, label: str, errors: list[str]) -> None:
    for ref in sorted(set(TOKEN_REFERENCE.findall(block))):
        node: object = frontmatter
        for part in ref.split("."):
            if isinstance(node, dict) and part in node:
                node = node[part]
            else:
                errors.append(f"{label} 的引用 {{{ref}}} 无法解析")
                break


def check_skill(errors: list[str]) -> None:
    skill_path = SKILL_SRC / "SKILL.md"
    try:
        fields, text = parse_frontmatter(skill_path)
    except FrontmatterError as exc:
        errors.append(str(exc))
        return

    name = str(fields.get("name", ""))
    if name != PACKAGE_NAME:
        errors.append(f"SKILL.md 的 name 必须是 {PACKAGE_NAME}，当前为 {name!r}")
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name):
        errors.append(f"SKILL.md 的 name 不符合 Agent Skills 规范：{name!r}")

    description = str(fields.get("description", ""))
    if not description:
        errors.append("SKILL.md 缺少 description")
    elif len(description) > 1024:
        errors.append(f"SKILL.md 的 description 超过 1024 字符（当前 {len(description)}）")
    if "良禽" not in description:
        errors.append("SKILL.md 的 description 缺少中文触发词")
    if "Liangqin" not in description:
        errors.append("SKILL.md 的 description 缺少英文触发词")

    metadata = fields.get("metadata")
    if not isinstance(metadata, dict):
        errors.append("SKILL.md 缺少 metadata 映射")
    else:
        for key, value in metadata.items():
            if not isinstance(value, str):
                errors.append(f"SKILL.md metadata.{key} 必须是字符串")

    if LEGACY_NAME_PATTERN.search(text):
        errors.append("SKILL.md 仍然提到已归档的旧运行时")


def check_design(errors: list[str]) -> None:
    design_path = ROOT / "DESIGN.md"
    try:
        fields, text = parse_frontmatter(design_path)
    except FrontmatterError as exc:
        errors.append(str(exc))
        return

    for key in DESIGN_FRONTMATTER_KEYS:
        if key not in fields:
            errors.append(f"DESIGN.md frontmatter 缺少 {key}")
    extra_keys = sorted(set(fields) - set(DESIGN_FRONTMATTER_KEYS))
    if extra_keys:
        errors.append(
            f"DESIGN.md frontmatter 只允许标准 8 个键，多出：{extra_keys}"
            "（elevation / motion / responsive / logo 应写进正文）"
        )
    for section in DESIGN_SECTIONS:
        if section not in text:
            errors.append(f"DESIGN.md 缺少章节 {section}")
    positions = [text.find(section) for section in DESIGN_SECTIONS]
    if positions != sorted(positions) or -1 in positions:
        errors.append("DESIGN.md 的标准段落没有按规范顺序出现")
    first_extension = min(
        (text.find(section) for section in EXTENSION_SECTIONS if text.find(section) != -1),
        default=len(text),
    )
    if first_extension < positions[-1]:
        errors.append("DESIGN.md 的扩展段必须排在标准段落之后")

    block = "\n".join(split_frontmatter(design_path)[0])
    resolve_refs(fields, block, "DESIGN.md", errors)
    if "fontWeight" in block or "font-weight" in block:
        errors.append("DESIGN.md frontmatter 不应声明字重（随包字体只有单一字重）")

    for reference in sorted(set(ASSET_REFERENCE.findall(text))):
        if not (ROOT / reference).exists():
            errors.append(f"DESIGN.md 引用了不存在的资产 {reference}")

    tokens = json.loads(TOKENS_PATH.read_text(encoding="utf-8"))
    token_values = {str(value).upper() for value in walk_values(tokens["color"]).values()}
    if fields.get("colors") != tokens["color"]:
        errors.append("DESIGN.md 的 colors 与 tokens.semantic.json 的 color 不一致")

    css_path = ROOT / "tokens" / "tokens.css"
    if not css_path.exists():
        errors.append("缺少 tokens/tokens.css")
    else:
        css_text = css_path.read_text(encoding="utf-8")
        if "--dna-" in css_text:
            errors.append("tokens.css 仍在使用已退役的 --dna- 前缀")
        for value in re.findall(r"--lq-color-[a-z0-9-]+:\s*(#[0-9A-Fa-f]{3,6})", css_text):
            if value.upper() not in token_values:
                errors.append(f"tokens.css 的颜色 {value} 不在 tokens.semantic.json 中")
        for line in css_text.splitlines():
            stripped = line.strip()
            if stripped.startswith("."):
                errors.append(f"tokens.css 只应导出 token，不应包含组件样式：{stripped[:40]}")
                break

    token_sizes = {v["size"] for v in tokens["typography"]["scale"].values()}
    design_sizes = {
        str(entry["fontSize"])
        for entry in fields.get("typography", {}).values()
        if isinstance(entry, dict) and "fontSize" in entry
    }
    if design_sizes != token_sizes:
        errors.append(
            f"DESIGN.md 字阶 {sorted(design_sizes)} 与 token 导出 {sorted(token_sizes)} 不一致"
        )

    if fields.get("rounded") != tokens["rounded"] or tokens["rounded"] != tokens["shape"]["radius"]:
        errors.append("DESIGN.md 的 rounded 与 tokens.semantic.json 的 rounded / shape.radius 不一致")

    if fields.get("spacing") != tokens["spacing"]:
        errors.append("DESIGN.md 的 spacing 与 tokens.semantic.json 的 spacing 不一致")

    components = fields.get("components", {})
    if not isinstance(components, dict) or len(components) < 20:
        errors.append(f"components 层过薄（当前 {len(components)} 条，至少 20 条）")
    hover_keys = [name for name in components if name.endswith("-hover")]
    if hover_keys:
        errors.append(f"components 不应记录 hover 状态：{hover_keys}")
    components_section = text[text.find("## Components") : text.find("## Do's and Don'ts")]
    for name in components:
        if f"`{name}`" not in components_section:
            errors.append(f"组件 {name} 只在 frontmatter 里，Components 正文缺少逐条解释")

    for value in tokens["elevation"].values():
        if value not in text:
            errors.append(f"正文缺少阴影值 {value}")
    if tokens["motion"]["easing"] not in text:
        errors.append("正文缺少动效缓动值")
    for value in tokens["motion"]["duration"].values():
        if value not in text:
            errors.append(f"正文缺少动效时长 {value}")


def check_optional_strict_yaml(errors: list[str]) -> None:
    """有 PyYAML 时用真实解析器复核一次；没有则明确提示，不静默跳过。"""
    try:
        import yaml  # type: ignore
    except ImportError:
        print("[NOTE] 未检测到 PyYAML，跳过真实 YAML 解析复核（子集语法校验仍然执行）")
        return
    for name in ("DESIGN.md", f"skills/public/{PACKAGE_NAME}/SKILL.md"):
        path = ROOT / name
        block, _ = split_frontmatter(path)
        try:
            yaml.safe_load("\n".join(block))
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{name} 不是合法 YAML：{exc}")


def expected_class(component: str) -> str:
    """组件条目 → kit 里的类名前缀。状态条目复用宿主组件的类。"""
    name = component
    for suffix in ("-active", "-disabled", "-focused", "-error"):
        if name.endswith(suffix):
            name = name[: -len(suffix)]
            break
    if name.startswith("button-"):
        name = "btn-" + name[len("button-") :]
    return f"lq-{name}"


def check_kit(errors: list[str]) -> None:
    kit_path = ROOT / "kit" / "kit.css"
    index_path = ROOT / "kit" / "index.html"
    if not kit_path.exists() or not index_path.exists():
        errors.append("缺少 kit/kit.css 或 kit/index.html")
        return

    kit_text = kit_path.read_text(encoding="utf-8")
    tokens = json.loads(TOKENS_PATH.read_text(encoding="utf-8"))

    def collect(prefix: str) -> dict[str, str]:
        return dict(re.findall(rf"(--lq-{prefix}[a-z0-9-]+):\s*([^;]+);", kit_text))

    kit_colors = {key.replace("--lq-color-", ""): value.strip() for key, value in collect("color-").items()}
    if kit_colors != tokens["color"]:
        errors.append("kit.css 的颜色变量与 tokens.semantic.json 不一致")
    kit_spacing = {key.replace("--lq-space-", ""): value.strip() for key, value in collect("space-").items()}
    if kit_spacing != tokens["spacing"]:
        errors.append("kit.css 的间距变量与 tokens.semantic.json 不一致")
    kit_radius = {key.replace("--lq-radius-", ""): value.strip() for key, value in collect("radius-").items()}
    if kit_radius != tokens["rounded"]:
        errors.append("kit.css 的圆角变量与 tokens.semantic.json 不一致")

    design_fields, _ = parse_frontmatter(ROOT / "DESIGN.md")
    for component in design_fields.get("components", {}):
        if f".{expected_class(component)}" not in kit_text and f".{expected_class(component)}:" not in kit_text:
            errors.append(f"kit.css 缺少组件 {component} 对应的类 .{expected_class(component)}")

    if "font-weight" in kit_text.replace("@font-face", "", 1).split(":root")[-1] and re.search(
        r"font-weight\s*:\s*(?!400|normal)\d+", kit_text.split(":root")[-1]
    ):
        errors.append("kit.css 不应声明 400 以外的字重")


def check_pages(errors: list[str]) -> None:
    """用 check_page 的规则扫自家产物，产物跑偏时构建直接失败。"""
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "liangqin_check_page", ROOT / "scripts" / "check_page.py"
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)

    tokens = json.loads(TOKENS_PATH.read_text(encoding="utf-8"))
    scales = module.build_scales(tokens)
    for relative in (
        "preview.html",
        "kit/index.html",
        "kit/kit.css",
        "kit/templates/homepage.html",
        "kit/templates/product-detail.html",
        "tokens/tokens.css",
    ):
        path = ROOT / relative
        if not path.exists():
            errors.append(f"缺少待检文件 {relative}")
            continue
        for finding in module.check_text(path, path.read_text(encoding="utf-8"), tokens, scales):
            errors.append(
                f"{relative}:{finding['line']} {finding['rule']} {finding['value']}"
            )


def validate() -> list[str]:
    errors: list[str] = []
    check_skill(errors)
    check_design(errors)
    check_kit(errors)
    check_pages(errors)
    check_optional_strict_yaml(errors)
    for name in FONT_FILES:
        if not (ROOT / "assets" / "fonts" / name).exists():
            errors.append(f"缺少字体文件 assets/fonts/{name}")
    return errors


def copy_file(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def copy_tree(source_dir: Path, target_dir: Path) -> list[Path]:
    written: list[Path] = []
    for path in sorted(source_dir.rglob("*")):
        if path.is_dir() or path.name == ".DS_Store":
            continue
        target = target_dir / path.relative_to(source_dir)
        copy_file(path, target)
        written.append(target)
    return written


def build(output_dir: Path) -> list[Path]:
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True)

    written: list[Path] = []
    for relative, source in PACKAGE_FILES:
        copy_file(source, output_dir / relative)
        written.append(output_dir / relative)

    for name in ("SKILL.md", "skill-release.json"):
        copy_file(SKILL_SRC / name, output_dir / name)
        written.append(output_dir / name)

    copy_file(
        SKILL_SRC / "adapters" / "README.zh-CN.md",
        output_dir / "adapters" / "README.zh-CN.md",
    )
    written.append(output_dir / "adapters" / "README.zh-CN.md")

    written.extend(copy_tree(ROOT / "assets" / "brand", output_dir / "assets" / "brand"))
    written.extend(copy_tree(ROOT / "kit" / "icons", output_dir / "kit" / "icons"))

    for name in FONT_FILES:
        target = output_dir / "assets" / "fonts" / name
        copy_file(ROOT / "assets" / "fonts" / name, target)
        written.append(target)

    for path in written:
        if LEGACY_NAME_PATTERN.search(path.name):
            raise SystemExit(f"[FAIL] 发行包文件名残留旧运行时：{path.name}")
    return written


def main() -> int:
    parser = argparse.ArgumentParser(description="构建良禽佳木品牌体发行包")
    parser.add_argument("--output-dir", default=str(OUTPUT_DIR))
    parser.add_argument("--check", action="store_true", help="只校验，不写文件")
    args = parser.parse_args()

    errors = validate()
    if errors:
        for error in errors:
            print(f"[FAIL] {error}", file=sys.stderr)
        return 1
    print("[OK] 校验通过：frontmatter 子集语法、章节、引用、token 交叉核对、旧运行时残留")

    if args.check:
        return 0

    written = build(Path(args.output_dir).resolve())
    total = sum(path.stat().st_size for path in written)
    print(f"[OK] 已构建 {len(written)} 个文件，共 {total / 1024:.0f} KB → {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
