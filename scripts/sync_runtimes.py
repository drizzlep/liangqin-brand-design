#!/usr/bin/env python3
"""把构建好的品牌体发行包同步到各 runtime 的 skills 目录。

默认只做 dry-run，加 --apply 才写入。
写入时会清空目标包目录（保留 .git），完成后逐文件比对哈希，确认装进去的和 dist/ 一致。
"""

from __future__ import annotations

import argparse
import hashlib
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGE_NAME = "liangqin-brand-body"
SOURCE = ROOT / "dist" / PACKAGE_NAME
HOME = Path.home()
MIN_EXPECTED_FILES = 12

TARGETS = {
    "cc-switch": HOME / ".cc-switch" / "skills",
    "claude": HOME / ".claude" / "skills",
    "codex": HOME / ".codex" / "skills",
    "workbuddy": HOME / ".workbuddy" / "skills",
    "codebuddy": HOME / ".codebuddy" / "skills",
    "qoder": HOME / ".qoder" / "skills",
    "cursor": HOME / ".cursor" / "skills",
    "gemini": HOME / ".gemini" / "skills",
    "agents": HOME / ".agents" / "skills",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="同步品牌体到各 runtime")
    parser.add_argument(
        "--target",
        action="append",
        choices=sorted(TARGETS),
        help="只同步指定 runtime，可重复；默认全部已存在的 runtime",
    )
    parser.add_argument("--apply", action="store_true", help="真正写入，默认 dry-run")
    parser.add_argument("--create", action="store_true", help="skills 目录不存在时一并创建")
    return parser.parse_args()


def digest_tree(root: Path) -> dict[str, str]:
    digests: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root)
        if path.is_dir() or path.name == ".DS_Store" or ".git" in relative.parts:
            continue
        digests[str(relative)] = hashlib.sha256(path.read_bytes()).hexdigest()
    return digests


def replace_package(destination: Path, source: Path) -> int:
    """替换目标目录内容，保留 .git（CC Switch 副本自带版本库）。返回被清掉的条目数。"""
    if destination.is_symlink():
        raise ValueError("目标是指向别处的符号链接，请同步它指向的真实目录")
    destination.mkdir(parents=True, exist_ok=True)
    removed = 0
    for entry in destination.iterdir():
        if entry.name == ".git":
            continue
        if entry.is_dir() and not entry.is_symlink():
            shutil.rmtree(entry)
        else:
            entry.unlink()
        removed += 1
    for entry in source.iterdir():
        target = destination / entry.name
        if entry.is_dir():
            shutil.copytree(entry, target)
        else:
            shutil.copy2(entry, target)
    return removed


def verify(destination: Path, source: Path) -> list[str]:
    expected = digest_tree(source)
    actual = digest_tree(destination)
    problems: list[str] = []
    for relative, digest in expected.items():
        if relative not in actual:
            problems.append(f"缺少 {relative}")
        elif actual[relative] != digest:
            problems.append(f"内容不一致 {relative}")
    for relative in actual:
        if relative not in expected:
            problems.append(f"多出 {relative}")
    return problems


def main() -> int:
    args = parse_args()

    if not SOURCE.is_dir():
        print(f"[FAIL] 发行包不存在：{SOURCE}\n先运行 python3 scripts/build_skill.py", file=sys.stderr)
        return 1
    source_files = digest_tree(SOURCE)
    if len(source_files) < MIN_EXPECTED_FILES:
        print(f"[FAIL] 发行包只有 {len(source_files)} 个文件，疑似构建不完整", file=sys.stderr)
        return 1

    names = args.target or sorted(TARGETS)
    planned: list[tuple[str, Path]] = []
    skipped: list[tuple[str, Path, str]] = []

    for name in names:
        skills_dir = TARGETS[name]
        destination = skills_dir / PACKAGE_NAME
        if destination.is_symlink():
            skipped.append((name, destination, "符号链接，随目标目录一起更新"))
            continue
        if not skills_dir.is_dir() and not args.create:
            skipped.append((name, skills_dir, "skills 目录不存在"))
            continue
        planned.append((name, destination))

    if not planned:
        print("没有可同步的目标。用 --create 创建缺失的 skills 目录。")
        for name, path, reason in skipped:
            print(f"  skip {name}: {reason} ({path})")
        return 0

    failures = 0
    for name, destination in planned:
        mode = "写入" if args.apply else "dry-run"
        print(f"[{mode}] {name}: {destination}")
        if not args.apply:
            continue
        removed = replace_package(destination, SOURCE)
        problems = verify(destination, SOURCE)
        if problems:
            failures += 1
            print(f"  [FAIL] 校验不通过：{problems[:3]}")
        else:
            print(f"  [OK] 已替换 {removed} 个旧条目，{len(source_files)} 个文件哈希一致")

    for name, path, reason in skipped:
        print(f"  skip {name}: {reason} ({path})")

    if not args.apply:
        print("\n以上为 dry-run，加 --apply 才会写入。")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
