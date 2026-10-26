#!/usr/bin/env python3
"""把 dist/ 里的发行包发布成独立的 skills 分发仓库。

默认只做预检（dry-run），加 --apply 才会写入远端。
用法：
    python3 scripts/publish_dist_repo.py --repo git@github.com:owner/repo.git
    python3 scripts/publish_dist_repo.py --repo https://github.com/owner/repo.git --apply

远端仓库需要事先创建（空仓库即可），因为创建仓库需要平台凭据。
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "dist" / "liangqin-brand-body"
PACKAGE_NAME = "liangqin-brand-body"


def run(args: list[str], cwd: Path, check: bool = True) -> subprocess.CompletedProcess:
    result = subprocess.run(args, cwd=cwd, capture_output=True, text=True, check=False)
    if check and result.returncode != 0:
        raise SystemExit(f"[FAIL] {' '.join(args)}\n{result.stderr.strip()}")
    return result


def git_env() -> dict[str, str]:
    """去掉可能指向未监听端口的代理变量，沿用 git 自身凭据。"""
    import os

    env = os.environ.copy()
    for key in ("HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy", "ALL_PROXY", "all_proxy"):
        env.pop(key, None)
    env["GIT_TERMINAL_PROMPT"] = "0"
    return env


def main() -> int:
    parser = argparse.ArgumentParser(description="发布良禽品牌体分发仓库")
    parser.add_argument("--repo", required=True, help="目标空仓库地址")
    parser.add_argument("--branch", default="main")
    parser.add_argument("--apply", action="store_true", help="真正推送到远端")
    args = parser.parse_args()

    if not SOURCE.is_dir():
        print(f"[FAIL] 发行包不存在：{SOURCE}\n先运行 python3 scripts/build_skill.py", file=sys.stderr)
        return 1

    release = json.loads((SOURCE / "skill-release.json").read_text(encoding="utf-8"))
    version = release["version"]

    files = sorted(p for p in SOURCE.rglob("*") if p.is_file())
    if not (SOURCE / "SKILL.md").is_file() or not (SOURCE / "DESIGN.md").is_file():
        print("[FAIL] 发行包缺少 SKILL.md 或 DESIGN.md", file=sys.stderr)
        return 1

    print(f"[预检] 包：{PACKAGE_NAME} v{version}，{len(files)} 个文件")
    print(f"[预检] 目标：{args.repo} → {args.branch}")
    print("[预检] 会以单次提交覆盖目标仓库历史（distribution repo 专用）")
    if not args.apply:
        print("[dry-run] 未写入远端；确认后加 --apply")
        return 0

    with tempfile.TemporaryDirectory(prefix="lq-dist-") as tmp:
        work = Path(tmp) / PACKAGE_NAME
        shutil.copytree(SOURCE, work)
        run(["git", "init", "-q", "-b", args.branch], work)
        run(["git", "config", "user.name", "liangqin-release-bot"], work)
        run(["git", "config", "user.email", "release@liangqin.local"], work)
        run(["git", "add", "-A"], work)
        run(["git", "commit", "-q", "-m", f"release: {PACKAGE_NAME} v{version}"], work)
        run(["git", "tag", "-a", f"v{version}", "-m", f"{PACKAGE_NAME} v{version}"], work)
        run(["git", "remote", "add", "origin", args.repo], work)
        push = subprocess.run(
            ["git", "push", "--force", "origin", args.branch, "--tags"],
            cwd=work,
            capture_output=True,
            text=True,
            env=git_env(),
            check=False,
        )
        if push.returncode != 0:
            print(f"[FAIL] 推送失败：\n{push.stderr.strip()}", file=sys.stderr)
            return 1
        print(f"[OK] 已推送 v{version} 到 {args.repo}")

    verify = subprocess.run(
        ["git", "ls-remote", "--heads", "--tags", args.repo],
        capture_output=True,
        text=True,
        env=git_env(),
        check=False,
    )
    if verify.returncode == 0:
        print("[校验] 远端引用：")
        for line in verify.stdout.splitlines():
            if f"refs/heads/{args.branch}" in line or f"refs/tags/v{version}" in line:
                print("  " + line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
