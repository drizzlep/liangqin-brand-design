#!/usr/bin/env python3
"""Audit local skill installs and detect upstream skill graph drift.

This tool is intentionally read-only. It reports what changed, what is safe to
sync, and what needs human review before any local runtime entry is modified.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

WATCH_DIRS = (
    "reference",
    "references",
    "commands",
    "protocols",
    "recipes",
    "examples",
    "evaluation",
    "design-packs",
    "artifact-surfaces",
    "assets/brand",
    "scripts",
)


@dataclass(frozen=True)
class SkillSpec:
    name: str
    authority_kind: str
    authority_path: str
    canonical_entry: str
    public_name: str
    expected_version_path: str | None
    expected_version_key: str
    runtime_authority_path: str | None
    active_paths: tuple[str, ...]
    deprecated_entries: tuple[str, ...]
    cc_switch_id: str | None = None
    hermes_snapshot: str | None = None
    allow_new_wrappers: str = "review"


SKILLS: dict[str, SkillSpec] = {
    "liangqin-brand-body": SkillSpec(
        name="liangqin-brand-body",
        authority_kind="repo-export",
        authority_path="skills/public/liangqin-brand-openclaw",
        canonical_entry="良禽品牌体",
        public_name="良禽品牌体",
        expected_version_path="skills/public/liangqin-brand-openclaw/skill-release.json",
        expected_version_key="version",
        runtime_authority_path=None,
        active_paths=(
            "~/.cc-switch/skills/liangqin-brand-body",
            "~/.codex/skills/liangqin-brand-body",
            "~/.claude/skills/liangqin-brand-body",
            "~/.openclaw/skills/liangqin-brand-body",
            "~/.openclaw/workspace/skills/liangqin-brand-body",
            "~/.hermes/skills/openclaw-imports/liangqin-brand-body",
        ),
        deprecated_entries=("liangqin-brand-openclaw",),
        cc_switch_id="local:liangqin-brand-body",
        hermes_snapshot="~/.hermes/.skills_prompt_snapshot.json",
        allow_new_wrappers="report-only",
    ),
    "impeccable": SkillSpec(
        name="impeccable",
        authority_kind="cc-switch",
        authority_path="~/.cc-switch/skills/impeccable",
        canonical_entry="impeccable",
        public_name="impeccable",
        expected_version_path=None,
        expected_version_key="version",
        runtime_authority_path=None,
        active_paths=(
            "~/.cc-switch/skills/impeccable",
            "~/.codex/skills/impeccable",
            "~/.claude/skills/impeccable",
            "~/.agents/skills/impeccable",
            "~/.openclaw/skills/impeccable",
            "~/.openclaw/workspace/skills/impeccable",
            "~/.openclaw/workspace/.agents/skills/impeccable",
            "~/.hermes/skills/impeccable",
        ),
        deprecated_entries=(),
        cc_switch_id="pbakaus/impeccable:impeccable",
        allow_new_wrappers="report-only",
    ),
}

IGNORED_TREE_NAMES = {".DS_Store"}
IGNORED_TREE_DIRS = {".git", "__pycache__", "node_modules", ".venv"}


def expand_path(path: str, home: Path, repo_root: Path) -> Path:
    if path.startswith("~/"):
        return home / path[2:]
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    return repo_root / candidate


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def try_read_json(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    try:
        return read_json(path), None
    except (OSError, json.JSONDecodeError) as exc:
        return None, str(exc)


def parse_frontmatter(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8", errors="ignore")
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    data: dict[str, str] = {}
    for line in parts[1].splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"')
    return data


def version_from_skill_dir(path: Path) -> str | None:
    return skill_version_info(path)["version"]


def skill_version_info(path: Path) -> dict[str, str | None]:
    release = path / "skill-release.json"
    if release.exists():
        payload, error = try_read_json(release)
        if error:
            return {"version": None, "source": str(release), "error": error}
        return {
            "version": str(payload.get("version", "") or "") or None,
            "source": str(release),
            "error": None,
        }
    frontmatter = parse_frontmatter(path / "SKILL.md")
    return {
        "version": frontmatter.get("version"),
        "source": str(path / "SKILL.md"),
        "error": None,
    }


def iter_tree_files(path: Path) -> list[Path]:
    if not path.exists():
        return []
    root = path.resolve(strict=False)
    files: list[Path] = []
    for child in sorted(root.rglob("*")):
        if any(part in IGNORED_TREE_DIRS for part in child.relative_to(root).parts):
            continue
        if child.name in IGNORED_TREE_NAMES:
            continue
        if child.is_file():
            files.append(child)
    return files


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def tree_file_hashes(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    root = path.resolve(strict=False)
    return {
        child.relative_to(root).as_posix(): file_hash(child)
        for child in iter_tree_files(root)
    }


def tree_hash(path: Path) -> str | None:
    if not path.exists():
        return None
    root = path.resolve(strict=False)
    digest = hashlib.sha256()
    for child in iter_tree_files(root):
        rel_path = child.relative_to(root).as_posix()
        digest.update(rel_path.encode("utf-8"))
        digest.update(b"\0")
        digest.update(child.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def collect_skill_graph(path: Path) -> dict[str, Any]:
    """Collect entry points and dependency/reference files for one skill tree."""
    graph: dict[str, Any] = {
        "root": str(path),
        "exists": path.exists(),
        "version": version_from_skill_dir(path) if path.exists() else None,
        "skill_files": [],
        "frontmatter_names": [],
        "reference_files": [],
        "command_metadata_files": [],
        "commands": [],
        "watch_dirs": [],
        "file_hash": tree_hash(path) if path.exists() else None,
        "file_hashes": tree_file_hashes(path) if path.exists() else {},
    }
    if not path.exists():
        return graph

    for skill_path in sorted(path.rglob("SKILL.md")):
        rel = skill_path.relative_to(path).as_posix()
        graph["skill_files"].append(rel)
        name = parse_frontmatter(skill_path).get("name")
        if name:
            graph["frontmatter_names"].append(name)

    for watch_dir in WATCH_DIRS:
        directory = path / watch_dir
        if not directory.exists():
            continue
        graph["watch_dirs"].append(watch_dir)
        for child in sorted(directory.rglob("*")):
            if child.is_file():
                graph["reference_files"].append(child.relative_to(path).as_posix())

    for metadata_path in sorted(path.rglob("command-metadata.json")):
        rel = metadata_path.relative_to(path).as_posix()
        graph["command_metadata_files"].append(rel)
        try:
            payload = read_json(metadata_path)
        except json.JSONDecodeError:
            graph.setdefault("invalid_command_metadata", []).append(rel)
            continue
        commands = payload.get("commands", payload if isinstance(payload, list) else [])
        if isinstance(commands, dict):
            command_names = sorted(str(key) for key in commands)
        elif isinstance(commands, list):
            command_names = []
            for item in commands:
                if isinstance(item, dict):
                    command_names.append(str(item.get("name") or item.get("command") or item))
                else:
                    command_names.append(str(item))
            command_names = sorted(command_names)
        else:
            command_names = []
        graph["commands"].extend(command_names)

    for key in ("skill_files", "frontmatter_names", "reference_files", "command_metadata_files", "commands", "watch_dirs"):
        graph[key] = sorted(set(graph[key]))
    return graph


def compare_graphs(authority: dict[str, Any], candidate: dict[str, Any]) -> dict[str, Any]:
    comparisons: dict[str, Any] = {
        "authority_root": authority["root"],
        "candidate_root": candidate["root"],
        "authority_version": authority.get("version"),
        "candidate_version": candidate.get("version"),
        "version_changed": authority.get("version") != candidate.get("version"),
        "added": {},
        "removed": {},
        "changed": {},
    }
    for key in ("skill_files", "frontmatter_names", "reference_files", "command_metadata_files", "commands", "watch_dirs"):
        authority_set = set(authority.get(key, []))
        candidate_set = set(candidate.get(key, []))
        comparisons["added"][key] = sorted(candidate_set - authority_set)
        comparisons["removed"][key] = sorted(authority_set - candidate_set)
        if key in {"skill_files", "reference_files", "command_metadata_files"}:
            authority_hashes = authority.get("file_hashes", {})
            candidate_hashes = candidate.get("file_hashes", {})
            comparisons["changed"][key] = sorted(
                rel
                for rel in authority_set & candidate_set
                if authority_hashes.get(rel) != candidate_hashes.get(rel)
            )
    return comparisons


def load_expected_version(spec: SkillSpec, repo_root: Path) -> tuple[str | None, str | None]:
    if not spec.expected_version_path:
        return None, None
    path = expand_path(spec.expected_version_path, Path.home(), repo_root)
    if not path.exists():
        return None, f"expected version file missing: {path}"
    payload, error = try_read_json(path)
    if error:
        return None, f"expected version file invalid: {path}: {error}"
    return str(payload.get(spec.expected_version_key, "") or "") or None, None


def check_cc_switch_db(spec: SkillSpec, home: Path) -> dict[str, Any]:
    db_path = home / ".cc-switch" / "cc-switch.db"
    result: dict[str, Any] = {"path": str(db_path), "exists": db_path.exists()}
    if not db_path.exists() or not spec.cc_switch_id:
        return result
    try:
        con = sqlite3.connect(db_path)
        con.row_factory = sqlite3.Row
        row = con.execute(
            "select id,name,directory,enabled_claude,enabled_codex,enabled_hermes,content_hash "
            "from skills where id = ?",
            (spec.cc_switch_id,),
        ).fetchone()
        con.close()
    except sqlite3.Error as exc:
        result["error"] = str(exc)
        return result
    result["row"] = dict(row) if row else None
    return result


def first_existing_active_path(spec: SkillSpec, home: Path, repo_root: Path) -> Path | None:
    for configured_path in spec.active_paths:
        path = expand_path(configured_path, home, repo_root)
        if path.exists() or path.is_symlink():
            return path
    return None


def audit_local_skill(
    spec: SkillSpec,
    home: Path,
    repo_root: Path,
    candidate_runtime_path: str | None = None,
) -> dict[str, Any]:
    authority_path = expand_path(spec.authority_path, home, repo_root)
    runtime_authority_kind = "configured"
    if candidate_runtime_path:
        runtime_authority_path = expand_path(candidate_runtime_path, home, repo_root)
        runtime_authority_kind = "candidate"
    elif spec.runtime_authority_path:
        runtime_authority_path = expand_path(spec.runtime_authority_path, home, repo_root)
    else:
        runtime_authority_path = first_existing_active_path(spec, home, repo_root)
        runtime_authority_kind = "active_baseline" if runtime_authority_path else "none"
    expected_hash = tree_hash(runtime_authority_path) if runtime_authority_path else None
    expected_version, expected_version_error = load_expected_version(spec, repo_root)
    if expected_version is None:
        expected_version = version_from_skill_dir(authority_path)

    active_paths: list[dict[str, Any]] = []
    issues: list[dict[str, str]] = []
    if not authority_path.exists():
        issues.append(
            {
                "severity": "fail",
                "code": "authority_missing",
                "message": f"{spec.name} authority path missing: {authority_path}",
            }
        )
    if runtime_authority_path is None or not runtime_authority_path.exists():
        issues.append(
            {
                "severity": "fail",
                "code": "runtime_authority_missing",
                "message": f"{spec.name} runtime authority path missing",
            }
        )
    if expected_version_error:
        issues.append(
            {
                "severity": "fail",
                "code": "expected_version_unreadable",
                "message": expected_version_error,
            }
        )
    for configured_path in spec.active_paths:
        path = expand_path(configured_path, home, repo_root)
        exists = path.exists() or path.is_symlink()
        resolved = path.resolve(strict=False) if exists else None
        version_info = skill_version_info(path) if exists else {"version": None, "source": None, "error": None}
        version = version_info["version"]
        content_hash = tree_hash(path) if exists else None
        entry = {
            "configured_path": configured_path,
            "path": str(path),
            "exists": exists,
            "is_symlink": path.is_symlink(),
            "resolved": str(resolved) if resolved else None,
            "version": version,
            "version_source": version_info["source"],
            "version_error": version_info["error"],
            "content_hash": content_hash,
            "content_matches_runtime_authority": content_hash == expected_hash if exists and expected_hash else None,
        }
        active_paths.append(entry)
        if not exists:
            issues.append(
                {
                    "severity": "fail",
                    "code": "missing_active_path",
                    "message": f"{spec.name} missing active path: {configured_path}",
                }
            )
        elif version_info["error"]:
            issues.append(
                {
                    "severity": "fail",
                    "code": "active_version_unreadable",
                    "message": f"{configured_path} version source is unreadable: {version_info['error']}",
                }
            )
        elif expected_version and not version:
            issues.append(
                {
                    "severity": "fail",
                    "code": "missing_version",
                    "message": f"{configured_path} has no detectable version, expected {expected_version}",
                }
            )
        elif expected_version and version != expected_version:
            issues.append(
                {
                    "severity": "fail",
                    "code": "version_mismatch",
                    "message": f"{configured_path} has {version}, expected {expected_version}",
                }
            )
        if exists and expected_hash and content_hash != expected_hash:
            issues.append(
                {
                    "severity": "fail",
                    "code": "content_mismatch",
                    "message": f"{configured_path} content hash differs from runtime authority {runtime_authority_path}",
                }
            )

    deprecated_hits: list[str] = []
    search_roots = {Path(entry["path"]).parent for entry in active_paths}
    for root in sorted(search_roots):
        if not root.exists():
            continue
        for deprecated in spec.deprecated_entries:
            candidate = root / deprecated
            if candidate.exists() or candidate.is_symlink():
                deprecated_hits.append(str(candidate))
                issues.append(
                    {
                        "severity": "fail",
                        "code": "deprecated_entry_active",
                        "message": f"deprecated entry is active: {candidate}",
                    }
                )

    db = check_cc_switch_db(spec, home)
    if db.get("exists") and spec.cc_switch_id and not db.get("row"):
        issues.append(
            {
                "severity": "warn",
                "code": "cc_switch_row_missing",
                "message": f"CC Switch DB row missing: {spec.cc_switch_id}",
            }
        )
    elif db.get("row"):
        row = db["row"]
        cc_switch_active = next(
            (entry for entry in active_paths if entry["configured_path"].startswith("~/.cc-switch/")),
            None,
        )
        if cc_switch_active and row.get("content_hash") and cc_switch_active.get("content_hash") != row["content_hash"]:
            issues.append(
                {
                    "severity": "fail",
                    "code": "cc_switch_db_hash_mismatch",
                    "message": f"CC Switch DB hash differs from disk for {cc_switch_active['configured_path']}",
                }
            )

    snapshot_result: dict[str, Any] | None = None
    if spec.hermes_snapshot:
        snapshot_path = expand_path(spec.hermes_snapshot, home, repo_root)
        snapshot_text = snapshot_path.read_text(encoding="utf-8", errors="ignore") if snapshot_path.exists() else ""
        snapshot_result = {
            "path": str(snapshot_path),
            "exists": snapshot_path.exists(),
            "deprecated_counts": {
                name: snapshot_text.count(name) for name in spec.deprecated_entries
            },
            "canonical_count": snapshot_text.count(spec.canonical_entry),
        }
        for name, count in snapshot_result["deprecated_counts"].items():
            if count:
                issues.append(
                    {
                        "severity": "fail",
                        "code": "hermes_snapshot_deprecated_entry",
                        "message": f"Hermes snapshot still contains {name} ({count})",
                    }
                )

    severity_order = {"fail": 3, "warn": 2, "info": 1}
    worst = max((severity_order[item["severity"]] for item in issues), default=0)
    status = "FAIL" if worst == 3 else "WARN" if worst == 2 else "PASS"

    return {
        "skill": spec.name,
        "status": status,
        "public_name": spec.public_name,
        "authority_kind": spec.authority_kind,
        "authority_path": str(authority_path),
        "authority_exists": authority_path.exists(),
        "runtime_authority_kind": runtime_authority_kind,
        "runtime_authority_path": str(runtime_authority_path) if runtime_authority_path else None,
        "runtime_authority_exists": runtime_authority_path.exists() if runtime_authority_path else False,
        "runtime_authority_hash": expected_hash,
        "expected_version": expected_version,
        "active_paths": active_paths,
        "deprecated_hits": deprecated_hits,
        "cc_switch_db": db,
        "hermes_snapshot": snapshot_result,
        "issues": issues,
        "graph": collect_skill_graph(authority_path),
    }


def build_plan(local_results: list[dict[str, Any]], upstream_results: list[dict[str, Any]]) -> dict[str, Any]:
    actions: list[dict[str, str]] = []
    for result in local_results:
        for issue in result["issues"]:
            action_type = "manual_review"
            if issue["code"] in {
                "authority_missing",
                "runtime_authority_missing",
                "expected_version_unreadable",
                "missing_active_path",
                "missing_version",
                "active_version_unreadable",
                "version_mismatch",
                "content_mismatch",
                "cc_switch_db_hash_mismatch",
                "deprecated_entry_active",
                "hermes_snapshot_deprecated_entry",
            }:
                action_type = "repair_candidate"
            actions.append(
                {
                    "skill": result["skill"],
                    "type": action_type,
                    "severity": issue["severity"],
                    "code": issue["code"],
                    "message": issue["message"],
                }
            )

    for result in upstream_results:
        skill = result["skill"]
        comparison = result["comparison"]
        if comparison.get("version_changed"):
            actions.append(
                {
                    "skill": skill,
                    "type": "manual_review",
                    "severity": "warn",
                    "code": "upstream_version_changed",
                    "message": (
                        f"{skill} upstream version {comparison.get('candidate_version')} "
                        f"differs from authority {comparison.get('authority_version')}"
                    ),
                }
            )
        for key, values in comparison["added"].items():
            if not values:
                continue
            action_type = "manual_review" if key in {"skill_files", "commands", "command_metadata_files"} else "report_only"
            actions.append(
                {
                    "skill": skill,
                    "type": action_type,
                    "severity": "warn" if action_type == "manual_review" else "info",
                    "code": f"upstream_added_{key}",
                    "message": f"{skill} upstream added {len(values)} {key}: {', '.join(values[:5])}",
                }
            )
        for key, values in comparison["changed"].items():
            if not values:
                continue
            action_type = "manual_review" if key in {"skill_files", "command_metadata_files"} else "report_only"
            actions.append(
                {
                    "skill": skill,
                    "type": action_type,
                    "severity": "warn" if action_type == "manual_review" else "info",
                    "code": f"upstream_changed_{key}",
                    "message": f"{skill} upstream changed {len(values)} {key}: {', '.join(values[:5])}",
                }
            )
        for key, values in comparison["removed"].items():
            if not values:
                continue
            actions.append(
                {
                    "skill": skill,
                    "type": "manual_review",
                    "severity": "warn",
                    "code": f"upstream_removed_{key}",
                    "message": f"{skill} upstream removed {len(values)} {key}: {', '.join(values[:5])}",
                }
            )

    return {"actions": actions, "action_count": len(actions)}


def render_markdown(report: dict[str, Any]) -> str:
    lines = ["# Local Skill Maintenance Report", ""]
    for result in report["local"]:
        lines.append(f"## {result['skill']} - {result['status']}")
        lines.append(f"- Public entry: `{result['public_name']}`")
        lines.append(f"- Expected version: `{result.get('expected_version') or 'unknown'}`")
        lines.append(f"- Authority: `{result['authority_path']}`")
        if result["issues"]:
            lines.append("- Issues:")
            for issue in result["issues"]:
                lines.append(f"  - [{issue['severity']}] `{issue['code']}` {issue['message']}")
        else:
            lines.append("- Issues: none")
        lines.append("")

    if report["upstream"]:
        lines.append("## Upstream Drift")
        for result in report["upstream"]:
            comparison = result["comparison"]
            lines.append(f"- `{result['skill']}` candidate: `{comparison['candidate_root']}`")
            if comparison["version_changed"]:
                lines.append(
                    f"  - version: `{comparison['authority_version']}` -> `{comparison['candidate_version']}`"
                )
            for key in ("skill_files", "commands", "command_metadata_files", "reference_files", "watch_dirs"):
                added = comparison["added"].get(key, [])
                removed = comparison["removed"].get(key, [])
                if added:
                    lines.append(f"  - added {key}: `{', '.join(added[:8])}`")
                if removed:
                    lines.append(f"  - removed {key}: `{', '.join(removed[:8])}`")
        lines.append("")

    lines.append("## Plan")
    actions = report["plan"]["actions"]
    if not actions:
        lines.append("- No action required.")
    else:
        for action in actions:
            lines.append(
                f"- [{action['severity']}] `{action['skill']}` `{action['type']}` "
                f"`{action['code']}`: {action['message']}"
            )
    lines.append("")
    lines.append(
        "Boundary: this report is read-only. Apply steps should be run separately with backups and runtime verification."
    )
    return "\n".join(lines) + "\n"


def parse_upstream(value: str) -> tuple[str, str]:
    if "=" not in value:
        raise argparse.ArgumentTypeError("expected SKILL_NAME=/path/to/candidate")
    skill, path = value.split("=", 1)
    if skill not in SKILLS:
        raise argparse.ArgumentTypeError(f"unknown skill: {skill}")
    return skill, path


def build_report(args: argparse.Namespace) -> dict[str, Any]:
    home = Path(args.home).expanduser().resolve()
    repo_root = Path(args.repo_root).resolve()
    skill_names = args.skill or sorted(SKILLS)
    candidate_paths = dict(args.candidate or [])
    local_results = [] if args.upstream_only else [
        audit_local_skill(SKILLS[name], home, repo_root, candidate_paths.get(name))
        for name in skill_names
    ]

    upstream_results: list[dict[str, Any]] = []
    for skill_name, candidate_path in args.upstream or []:
        spec = SKILLS[skill_name]
        authority = collect_skill_graph(expand_path(spec.authority_path, home, repo_root))
        candidate = collect_skill_graph(expand_path(candidate_path, home, repo_root))
        upstream_results.append(
            {
                "skill": skill_name,
                "comparison": compare_graphs(authority, candidate),
            }
        )

    plan = build_plan(local_results, upstream_results)
    return {
        "status": "FAIL"
        if any(result["status"] == "FAIL" for result in local_results)
        else "WARN"
        if plan["actions"]
        else "PASS",
        "local": local_results,
        "upstream": upstream_results,
        "plan": plan,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Read-only local skill maintenance audit and upstream drift planner"
    )
    parser.add_argument(
        "command",
        nargs="?",
        default="check",
        choices=("check", "check-upstream", "plan"),
        help="check local installs, compare upstream candidates, or render a combined plan",
    )
    parser.add_argument("--repo-root", default=str(ROOT))
    parser.add_argument("--home", default=str(Path.home()))
    parser.add_argument("--skill", action="append", choices=sorted(SKILLS))
    parser.add_argument(
        "--upstream",
        action="append",
        type=parse_upstream,
        help="Compare a candidate skill tree, e.g. impeccable=/tmp/impeccable",
    )
    parser.add_argument(
        "--candidate",
        action="append",
        type=parse_upstream,
        help="Compare local runtime installs against an explicit release candidate, e.g. liangqin-brand-body=/tmp/liangqin-brand-body",
    )
    parser.add_argument(
        "--upstream-only",
        action="store_true",
        help="Skip local runtime checks and report only upstream candidate drift",
    )
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    args = parser.parse_args()

    if args.command == "check-upstream" and not args.upstream:
        parser.error("check-upstream requires at least one --upstream SKILL=PATH")

    report = build_report(args)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(render_markdown(report), end="")
    return 1 if report["status"] == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
