#!/usr/bin/env python3
"""Refresh the Liangqin brand design skill and run one fresh-session smoke test."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

DEFAULT_MESSAGE = "请用良禽品牌设计体审查并纠偏这份首页方案。"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Refresh the shared skill and run a fresh-session test.")
    parser.add_argument("--message", default=DEFAULT_MESSAGE, help="Smoke test message.")
    parser.add_argument("--session-id", help="Optional explicit session id.")
    parser.add_argument("--skill-dir", default=str(Path(__file__).resolve().parent.parent), help="Skill root directory.")
    parser.add_argument("--timeout", type=int, default=120, help="Agent timeout in seconds.")
    parser.add_argument("--thinking", default="minimal", help="Agent thinking level.")
    return parser.parse_args()


def run_step(command: list[str], *, capture: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, check=False, text=True, capture_output=capture)


def extract_json_payload(raw: str) -> dict[str, object]:
    lines = [line for line in raw.splitlines() if line.strip()]
    for start in range(len(lines)):
        candidate = "\n".join(lines[start:])
        try:
            parsed = json.loads(candidate)
        except json.JSONDecodeError:
            continue
        if isinstance(parsed, dict):
            return parsed
    raise SystemExit("未能从 OpenClaw 输出里解析到 JSON 结果，请稍后重试。")


def print_header(title: str) -> None:
    print(f"\n=== {title} ===")


def main() -> int:
    args = parse_args()
    skill_dir = Path(args.skill_dir).expanduser().resolve()
    scripts_dir = skill_dir / "scripts"
    session_id = args.session_id or f"liangqin-brand-design-test-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

    print_header("发布当前 skill")
    publish = run_step([sys.executable, str(scripts_dir / "publish_skill.py"), "--source", str(skill_dir)])
    if publish.returncode != 0:
        return publish.returncode

    print_header("开始 fresh session 测试")
    print(f"session-id: {session_id}")
    print(f"message: {args.message}")

    result = run_step(
        [
            "openclaw",
            "agent",
            "--session-id",
            session_id,
            "--message",
            args.message,
            "--json",
            "--thinking",
            args.thinking,
            "--timeout",
            str(args.timeout),
        ],
        capture=True,
    )
    if result.returncode != 0:
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        return result.returncode

    if result.stderr:
        print(result.stderr, file=sys.stderr)

    payload = extract_json_payload(result.stdout)
    texts = [item.get("text", "") for item in payload.get("result", {}).get("payloads", []) if item.get("text")]

    print_header("测试结果")
    print(texts[-1] if texts else result.stdout)
    print_header("后续可复用命令")
    print(f"python3 ~/.openclaw/skills/liangqin-brand-design/scripts/refresh_and_test.py --message '{args.message}'")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
