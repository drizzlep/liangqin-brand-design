import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "maintain_local_skills.py"


class MaintainLocalSkillsTest(unittest.TestCase):
    def write_skill(self, root: Path, name: str = "demo", version: str = "1.0.0") -> None:
        root.mkdir(parents=True, exist_ok=True)
        (root / "SKILL.md").write_text(
            "\n".join(
                [
                    "---",
                    f"name: {name}",
                    f"version: {version}",
                    "description: Demo skill.",
                    "---",
                    "",
                    "# Demo",
                    "",
                ]
            ),
            encoding="utf-8",
        )

    def run_script(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            ["python3", str(SCRIPT), *args],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_check_upstream_reports_added_skill_reference_and_command(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp = Path(tmp_dir)
            authority = tmp / "authority"
            candidate = tmp / "candidate"
            self.write_skill(authority, name="impeccable", version="3.1.1")
            self.write_skill(candidate, name="impeccable", version="3.1.2")

            (authority / "reference").mkdir()
            (authority / "reference" / "audit.md").write_text("audit\n", encoding="utf-8")

            (candidate / "reference").mkdir()
            (candidate / "reference" / "audit.md").write_text("audit\n", encoding="utf-8")
            (candidate / "reference" / "new-mode.md").write_text("new\n", encoding="utf-8")
            (candidate / "commands").mkdir()
            (candidate / "commands" / "new-command.md").write_text("command\n", encoding="utf-8")
            (candidate / "extra-wrapper").mkdir()
            (candidate / "extra-wrapper" / "SKILL.md").write_text(
                "---\nname: extra-wrapper\ndescription: New wrapper.\n---\n",
                encoding="utf-8",
            )
            (candidate / "scripts").mkdir()
            (candidate / "scripts" / "command-metadata.json").write_text(
                json.dumps({"commands": [{"name": "new-command"}]}),
                encoding="utf-8",
            )

            result = self.run_script(
                "check-upstream",
                "--repo-root",
                str(tmp),
                "--home",
                str(tmp),
                "--skill",
                "impeccable",
                "--upstream",
                f"impeccable={candidate}",
                "--json",
            )

            self.assertEqual(result.returncode, 1, result.stderr)
            payload = json.loads(result.stdout)
            actions = payload["plan"]["actions"]
            action_codes = {action["code"] for action in actions}
            self.assertIn("upstream_version_changed", action_codes)
            self.assertIn("upstream_added_skill_files", action_codes)
            self.assertIn("upstream_added_reference_files", action_codes)
            self.assertIn("upstream_added_commands", action_codes)
            self.assertIn("upstream_added_command_metadata_files", action_codes)

            skill_file_actions = [
                action for action in actions if action["code"] == "upstream_added_skill_files"
            ]
            self.assertEqual(skill_file_actions[0]["type"], "manual_review")
            reference_actions = [
                action for action in actions if action["code"] == "upstream_added_reference_files"
            ]
            self.assertEqual(reference_actions[0]["type"], "report_only")

    def test_check_upstream_reports_changed_existing_skill_reference_and_metadata(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp = Path(tmp_dir)
            authority = tmp / ".cc-switch" / "skills" / "impeccable"
            candidate = tmp / "candidate"
            self.write_skill(authority, name="impeccable", version="3.1.1")
            self.write_skill(candidate, name="impeccable", version="3.1.1")

            (authority / "reference").mkdir()
            (candidate / "reference").mkdir()
            (authority / "reference" / "audit.md").write_text("old audit\n", encoding="utf-8")
            (candidate / "reference" / "audit.md").write_text("new audit\n", encoding="utf-8")

            (authority / "scripts").mkdir()
            (candidate / "scripts").mkdir()
            (authority / "scripts" / "command-metadata.json").write_text(
                json.dumps({"commands": ["audit"]}),
                encoding="utf-8",
            )
            (candidate / "scripts" / "command-metadata.json").write_text(
                json.dumps({"commands": ["audit", "shape"]}),
                encoding="utf-8",
            )

            result = self.run_script(
                "check-upstream",
                "--repo-root",
                str(tmp),
                "--home",
                str(tmp),
                "--skill",
                "impeccable",
                "--upstream",
                f"impeccable={candidate}",
                "--json",
            )

            self.assertEqual(result.returncode, 1, result.stderr)
            payload = json.loads(result.stdout)
            actions = payload["plan"]["actions"]
            action_codes = {action["code"] for action in actions}
            self.assertIn("upstream_changed_reference_files", action_codes)
            self.assertIn("upstream_changed_command_metadata_files", action_codes)
            self.assertIn("upstream_added_commands", action_codes)

    def test_check_upstream_only_omits_local_install_noise(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp = Path(tmp_dir)
            authority = tmp / ".cc-switch" / "skills" / "impeccable"
            candidate = tmp / "candidate"
            self.write_skill(authority, name="impeccable", version="3.1.1")
            self.write_skill(candidate, name="impeccable", version="3.1.2")

            result = self.run_script(
                "check-upstream",
                "--repo-root",
                str(tmp),
                "--home",
                str(tmp),
                "--skill",
                "impeccable",
                "--upstream",
                f"impeccable={candidate}",
                "--upstream-only",
                "--json",
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["local"], [])
            action_codes = {action["code"] for action in payload["plan"]["actions"]}
            self.assertIn("upstream_version_changed", action_codes)
            self.assertNotIn("missing_active_path", action_codes)

    def test_local_check_fails_when_runtime_copy_content_differs_even_same_version(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp = Path(tmp_dir)
            source = tmp / "skills" / "public" / "liangqin-brand-openclaw"
            runtime_authority = tmp / "dist" / "liangqin-brand-body"
            self.write_skill(source, name="良禽品牌体", version="2.2.0")
            self.write_skill(runtime_authority, name="良禽品牌体", version="2.2.0")
            (source / "skill-release.json").write_text(
                json.dumps({"version": "2.2.0"}),
                encoding="utf-8",
            )
            (runtime_authority / "skill-release.json").write_text(
                json.dumps({"version": "2.2.0"}),
                encoding="utf-8",
            )
            (runtime_authority / "DESIGN.md").write_text("fresh design\n", encoding="utf-8")

            active_paths = [
                ".cc-switch/skills/liangqin-brand-body",
                ".codex/skills/liangqin-brand-body",
                ".claude/skills/liangqin-brand-body",
                ".openclaw/skills/liangqin-brand-body",
                ".openclaw/workspace/skills/liangqin-brand-body",
                ".hermes/skills/openclaw-imports/liangqin-brand-body",
            ]
            for path in active_paths:
                self.write_skill(tmp / path, name="良禽品牌体", version="2.2.0")
                (tmp / path / "skill-release.json").write_text(
                    json.dumps({"version": "2.2.0"}),
                    encoding="utf-8",
                )
                (tmp / path / "DESIGN.md").write_text("stale design\n", encoding="utf-8")

            result = self.run_script(
                "check",
                "--repo-root",
                str(tmp),
                "--home",
                str(tmp),
                "--skill",
                "liangqin-brand-body",
                "--candidate",
                f"liangqin-brand-body={runtime_authority}",
                "--json",
            )

            self.assertEqual(result.returncode, 1, result.stderr)
            payload = json.loads(result.stdout)
            issue_codes = {
                issue["code"]
                for local_result in payload["local"]
                for issue in local_result["issues"]
            }
            self.assertIn("content_mismatch", issue_codes)

    def test_local_check_passes_when_runtime_copies_match_without_candidate(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp = Path(tmp_dir)
            source = tmp / "skills" / "public" / "liangqin-brand-openclaw"
            self.write_skill(source, name="良禽品牌体", version="2.2.0")
            (source / "skill-release.json").write_text(
                json.dumps({"version": "2.2.0"}),
                encoding="utf-8",
            )

            for path in [
                ".cc-switch/skills/liangqin-brand-body",
                ".codex/skills/liangqin-brand-body",
                ".claude/skills/liangqin-brand-body",
                ".openclaw/skills/liangqin-brand-body",
                ".openclaw/workspace/skills/liangqin-brand-body",
                ".hermes/skills/openclaw-imports/liangqin-brand-body",
            ]:
                self.write_skill(tmp / path, name="良禽品牌体", version="2.2.0")
                (tmp / path / "skill-release.json").write_text(
                    json.dumps({"version": "2.2.0"}),
                    encoding="utf-8",
                )
                (tmp / path / "DESIGN.md").write_text("same design\n", encoding="utf-8")

            result = self.run_script(
                "check",
                "--repo-root",
                str(tmp),
                "--home",
                str(tmp),
                "--skill",
                "liangqin-brand-body",
                "--json",
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["status"], "PASS")
            self.assertEqual(payload["local"][0]["runtime_authority_kind"], "active_baseline")

    def test_local_check_fails_when_active_skill_release_json_is_invalid(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp = Path(tmp_dir)
            source = tmp / "skills" / "public" / "liangqin-brand-openclaw"
            runtime_authority = tmp / "dist" / "liangqin-brand-body"
            self.write_skill(source, name="良禽品牌体", version="2.2.0")
            self.write_skill(runtime_authority, name="良禽品牌体", version="2.2.0")
            (source / "skill-release.json").write_text(
                json.dumps({"version": "2.2.0"}),
                encoding="utf-8",
            )
            (runtime_authority / "skill-release.json").write_text(
                json.dumps({"version": "2.2.0"}),
                encoding="utf-8",
            )

            for path in [
                ".cc-switch/skills/liangqin-brand-body",
                ".codex/skills/liangqin-brand-body",
                ".claude/skills/liangqin-brand-body",
                ".openclaw/skills/liangqin-brand-body",
                ".openclaw/workspace/skills/liangqin-brand-body",
                ".hermes/skills/openclaw-imports/liangqin-brand-body",
            ]:
                self.write_skill(tmp / path, name="良禽品牌体", version="2.2.0")
                (tmp / path / "skill-release.json").write_text("{invalid", encoding="utf-8")

            result = self.run_script(
                "check",
                "--repo-root",
                str(tmp),
                "--home",
                str(tmp),
                "--skill",
                "liangqin-brand-body",
                "--json",
            )

            self.assertEqual(result.returncode, 1, result.stderr)
            payload = json.loads(result.stdout)
            issue_codes = {
                issue["code"]
                for local_result in payload["local"]
                for issue in local_result["issues"]
            }
            self.assertIn("active_version_unreadable", issue_codes)

    def test_local_check_reports_deprecated_hermes_snapshot_entry(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp = Path(tmp_dir)
            source = tmp / "skills" / "public" / "liangqin-brand-openclaw"
            runtime_authority = tmp / "dist" / "liangqin-brand-body"
            self.write_skill(source, name="良禽品牌体", version="2.2.0")
            self.write_skill(runtime_authority, name="良禽品牌体", version="2.2.0")
            (source / "skill-release.json").write_text(
                json.dumps({"version": "2.2.0"}),
                encoding="utf-8",
            )
            (runtime_authority / "skill-release.json").write_text(
                json.dumps({"version": "2.2.0"}),
                encoding="utf-8",
            )
            hermes_snapshot = tmp / ".hermes" / ".skills_prompt_snapshot.json"
            hermes_snapshot.parent.mkdir(parents=True)
            hermes_snapshot.write_text(
                json.dumps({"skills": [{"skill_name": "liangqin-brand-openclaw"}]}),
                encoding="utf-8",
            )

            for path in [
                ".cc-switch/skills/liangqin-brand-body",
                ".codex/skills/liangqin-brand-body",
                ".claude/skills/liangqin-brand-body",
                ".openclaw/skills/liangqin-brand-body",
                ".openclaw/workspace/skills/liangqin-brand-body",
                ".hermes/skills/openclaw-imports/liangqin-brand-body",
            ]:
                self.write_skill(tmp / path, name="良禽品牌体", version="2.2.0")
                (tmp / path / "skill-release.json").write_text(
                    json.dumps({"version": "2.2.0"}),
                    encoding="utf-8",
                )

            result = self.run_script(
                "check",
                "--repo-root",
                str(tmp),
                "--home",
                str(tmp),
                "--skill",
                "liangqin-brand-body",
                "--json",
            )

            self.assertEqual(result.returncode, 1, result.stderr)
            payload = json.loads(result.stdout)
            issue_codes = {
                issue["code"]
                for local_result in payload["local"]
                for issue in local_result["issues"]
            }
            self.assertIn("hermes_snapshot_deprecated_entry", issue_codes)


if __name__ == "__main__":
    unittest.main()
