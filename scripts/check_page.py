#!/usr/bin/env python3
"""按 DESIGN.md 扫描页面或样式表，报出偏离规范的地方，并给出改法。

   python3 scripts/check_page.py path/to/page.html path/to/style.css

每条发现按 What / Why / Fix 三段输出：
  What  问题与实测值
  Why   依据，引用 DESIGN.md 的章节
  Fix   可执行的改法（最接近的 token、允许的刻度值）

检查项：
  color-off-token       颜色不在 token 内
  font-size-off-scale   字号不在字阶内
  spacing-off-scale     间距不在 8px 刻度内
  radius-off-scale      圆角不在 token 内
  font-weight-declared  声明了 400 以外的字重（@font-face 除外）
  text-contrast-low     文字色对比度低于 4.5:1
  unknown-token         用了未定义的 --lq-* 变量

退出码：0 全部通过；1 有 FAIL。
"""

from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOKENS_PATH = ROOT / "tokens" / "tokens.semantic.json"

HEX = re.compile(r"#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b")
VAR_USE = re.compile(r"var\(\s*(--lq-[a-z0-9-]+)")
VAR_DEF = re.compile(r"(--lq-[a-z0-9-]+)\s*:")
# 值必须以 ；} > " 或换行结束，避免把 HTML 正文吞进 CSS 值里
VALUE = r'([^;}>\n"]+)'
FONT_SIZE = re.compile(r"font-size\s*:\s*" + VALUE)
FONT_WEIGHT = re.compile(r"font-weight\s*:\s*" + VALUE)
RADIUS = re.compile(r"border-radius\s*:\s*" + VALUE)
SPACING = re.compile(r"\b(?:margin|padding|gap|row-gap|column-gap)\s*:\s*" + VALUE)
TEXT_COLOR = re.compile(r"(?<![-\w])color\s*:\s*" + VALUE)
PX_VALUE = re.compile(r"(-?\d+(?:\.\d+)?)px")
PX = re.compile(r"^(-?\d+(?:\.\d+)?)px$")

ALLOWED_WEIGHTS = {"400", "normal"}

RULE_SECTION = {
    "color-off-token": "Colors",
    "font-size-off-scale": "Typography",
    "spacing-off-scale": "Layout",
    "radius-off-scale": "Shapes",
    "font-weight-declared": "Typography",
    "text-contrast-low": "Colors",
    "unknown-token": "Colors / Shapes / Layout",
}

RULE_WHY = {
    "color-off-token": "页面颜色必须取自 token，规范只定义有角色的颜色。",
    "font-size-off-scale": "字号只能取字阶里的档位，避免出现 14px、19px 这类随手值。",
    "spacing-off-scale": "间距只能取 8px 基准刻度，保证版式节奏一致。",
    "radius-off-scale": "圆角只能取 token 里的四个档位。",
    "font-weight-declared": "随包字体各自只有一个字重，声明 500/600/700 不会生效。",
    "text-contrast-low": "正文与背景对比度需达到 4.5:1，保证中文可读性。",
    "unknown-token": "变量名必须是 token 里定义过的，避免拼错后静默失效。",
}


def hex_to_rgb(value: str) -> tuple[int, int, int]:
    raw = value.lstrip("#")
    if len(raw) == 3:
        raw = "".join(ch * 2 for ch in raw)
    return int(raw[0:2], 16), int(raw[2:4], 16), int(raw[4:6], 16)


def luminance(value: str) -> float:
    channels = [c / 255 for c in hex_to_rgb(value)]
    linear = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in channels]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def contrast(foreground: str, background: str) -> float:
    a, b = luminance(foreground), luminance(background)
    high, low = max(a, b), min(a, b)
    return (high + 0.05) / (low + 0.05)


def load_tokens() -> dict:
    return json.loads(TOKENS_PATH.read_text(encoding="utf-8"))


def build_scales(tokens: dict) -> dict[str, set[float]]:
    """刻度全部来自 token 导出，避免校验器和规范各写一套。"""

    def to_px(values) -> set[float]:
        result = {0.0}
        for value in values:
            match = PX.match(str(value))
            if match:
                result.add(float(match.group(1)))
        return result

    return {
        "font": to_px(entry["size"] for entry in tokens["typography"]["scale"].values()),
        "spacing": to_px(tokens["spacing"].values()),
        "radius": to_px(tokens["rounded"].values()) | {9999.0},
    }


def legal_vars(tokens: dict) -> set[str]:
    """从 token 导出推出全部合法的 --lq-* 变量名。"""
    names = {f"--lq-color-{key}" for key in tokens["color"]}
    names |= {f"--lq-space-{key}" for key in tokens["spacing"]}
    names |= {f"--lq-radius-{key}" for key in tokens["rounded"]}
    names |= {"--lq-font-heading", "--lq-font-body", "--lq-font-mono"}
    for key in tokens["typography"]["scale"]:
        names |= {f"--lq-size-{key}", f"--lq-line-{key}", f"--lq-tracking-{key}"}
    names |= {f"--lq-shadow-{key}" for key in tokens["elevation"]}
    names |= {f"--lq-duration-{key}" for key in tokens["motion"]["duration"]}
    names |= {"--lq-ease", "--lq-max-content-width"}
    names |= {
        "--lq-gutter-desktop",
        "--lq-gutter-tablet",
        "--lq-gutter-mobile",
    }
    names |= {"--lq-divider-thickness", "--lq-divider-color"}
    names |= {"--lq-icon-url"}
    return names


def fmt(value: float) -> str:
    return str(int(value)) if float(value).is_integer() else str(value)


def nearest_number(value: float, allowed: set[float]) -> str:
    ordered = sorted(allowed)
    below = [v for v in ordered if v <= value]
    above = [v for v in ordered if v >= value]
    options = []
    if below:
        options.append(fmt(below[-1]))
    if above:
        options.append(fmt(above[0]))
    return " 或 ".join(dict.fromkeys(options)) if options else "—"


def nearest_color(value: str, token_colors: dict[str, str]) -> tuple[str, str, int]:
    target = hex_to_rgb(value)
    best = ("", "", 10**9)
    for name, token_value in token_colors.items():
        if not str(token_value).startswith("#"):
            continue
        candidate = hex_to_rgb(str(token_value))
        distance = sum((a - b) ** 2 for a, b in zip(target, candidate))
        if distance < best[2]:
            best = (name, str(token_value), int(distance**0.5))
    return best


def rule_spans(text: str) -> list[tuple[int, str]]:
    """按行切分，跳过 @font-face 块（那里的 font-weight 是字体描述，不是样式声明）。"""
    spans: list[tuple[int, str]] = []
    font_face_depth = 0
    for number, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if "@font-face" in stripped:
            font_face_depth += stripped.count("{") - stripped.count("}")
            continue
        if font_face_depth:
            font_face_depth += stripped.count("{") - stripped.count("}")
            continue
        spans.append((number, line))
    return spans


def check_text(path: Path, text: str, tokens: dict, scales: dict[str, set[float]]) -> list[dict]:
    findings: list[dict] = []
    token_colors = {key: str(value) for key, value in tokens["color"].items()}
    allowed_colors = {value.upper() for value in token_colors.values()}
    backgrounds = [
        str(tokens["color"]["background"]).upper(),
        str(tokens["color"]["surface"]).upper(),
        str(tokens["color"]["surface-elevated"]).upper(),
    ]
    safe_text_colors = [
        (name, value)
        for name, value in token_colors.items()
        if all(contrast(value, bg) >= 4.5 for bg in backgrounds)
    ]
    defined_vars = set(VAR_DEF.findall(text)) | legal_vars(tokens)

    def add(line: int, rule: str, what: str, fix: str) -> None:
        findings.append(
            {
                "file": str(path),
                "line": line,
                "rule": rule,
                "what": what,
                "why": f"DESIGN.md › {RULE_SECTION[rule]} — {RULE_WHY[rule]}",
                "fix": fix,
            }
        )

    for number, line in rule_spans(text):
        for value in HEX.findall(line):
            if value.upper() not in allowed_colors:
                name, nearest, distance = nearest_color(value, token_colors)
                add(
                    number,
                    "color-off-token",
                    f"{value} 不在 token 内",
                    f"最近的 token 是 --lq-color-{name} {nearest}（RGB 距离 {distance}）；"
                    "如果确实是新颜色，先在 DESIGN.md › Colors 里新增 token",
                )

        for match in FONT_SIZE.findall(line):
            for px in PX_VALUE.findall(match):
                if float(px) not in scales["font"]:
                    add(
                        number,
                        "font-size-off-scale",
                        f"font-size: {px}px 不在字阶内",
                        f"改用 {nearest_number(float(px), scales['font'])}px；"
                        "对应 token 见 --lq-size-*",
                    )

        for match in SPACING.findall(line):
            for px in PX_VALUE.findall(match):
                if float(px) not in scales["spacing"]:
                    add(
                        number,
                        "spacing-off-scale",
                        f"间距 {px}px 不在 8px 刻度内",
                        f"改用 {nearest_number(float(px), scales['spacing'])}px；对应 token 见 --lq-space-*",
                    )

        for match in RADIUS.findall(line):
            if "%" in match:
                continue
            for px in PX_VALUE.findall(match):
                if float(px) not in scales["radius"]:
                    add(
                        number,
                        "radius-off-scale",
                        f"border-radius: {px}px 不在 token 内",
                        f"改用 {nearest_number(float(px), scales['radius'])}px，"
                        "或 --lq-radius-xs/sm/md/pill",
                    )

        for match in FONT_WEIGHT.findall(line):
            value = match.strip()
            if value not in ALLOWED_WEIGHTS:
                add(
                    number,
                    "font-weight-declared",
                    f"font-weight: {value}",
                    "删掉这行（默认字重即可）；需要强调时改字号或颜色",
                )

        for match in TEXT_COLOR.findall(line):
            for value in HEX.findall(match):
                worst = min(contrast(value, bg) for bg in backgrounds)
                if worst < 4.5:
                    suggestion = "、".join(f"--lq-color-{name}" for name, _ in safe_text_colors[:3])
                    add(
                        number,
                        "text-contrast-low",
                        f"{value} 最低对比度 {worst:.2f}:1（需 ≥ 4.5:1）",
                        f"正文改用 {suggestion}；该色只用于边框、图标或 ≥18px 文字",
                    )

        for name in VAR_USE.findall(line):
            if name in defined_vars:
                continue
            close = difflib.get_close_matches(name, sorted(defined_vars), n=2, cutoff=0.7)
            add(
                number,
                "unknown-token",
                f"{name} 未定义",
                ("是不是 " + " 或 ".join(close) + "？") if close else "检查拼写，或先在 token 里定义",
            )

    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="按 DESIGN.md 校验页面样式")
    parser.add_argument("files", nargs="+", help="要检查的 HTML 或 CSS 文件")
    parser.add_argument("--json", action="store_true", help="输出 JSON")
    args = parser.parse_args()

    tokens = load_tokens()
    scales = build_scales(tokens)
    findings: list[dict] = []
    for name in args.files:
        path = Path(name)
        if not path.exists():
            print(f"[FAIL] 文件不存在：{path}", file=sys.stderr)
            return 1
        findings.extend(check_text(path, path.read_text(encoding="utf-8"), tokens, scales))

    if args.json:
        print(json.dumps(findings, ensure_ascii=False, indent=2))
        return 1 if findings else 0

    if not findings:
        print(f"[OK] {len(args.files)} 个文件未发现偏离规范的地方")
        return 0

    for item in findings:
        print(f"[FAIL] {item['file']}:{item['line']}  {item['rule']}")
        print(f"       What: {item['what']}")
        print(f"       Why:  {item['why']}")
        print(f"       Fix:  {item['fix']}")
    print(f"\n合计 {len(findings)} 处需要处理")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
