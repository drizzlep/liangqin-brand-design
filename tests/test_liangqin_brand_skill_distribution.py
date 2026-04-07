import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / "skills" / "public" / "liangqin-brand-openclaw"


class LiangqinBrandSkillDistributionTest(unittest.TestCase):
    def test_real_design_cases_exist(self):
        real_case_dir = SKILL_ROOT / "examples" / "real-cases"
        self.assertTrue(real_case_dir.exists(), "real case directory missing")
        cases = sorted(real_case_dir.glob("*.md"))
        self.assertGreaterEqual(len(cases), 3, "need at least 3 real design cases")

    def test_export_script_can_build_standalone_skill_folder(self):
        script_path = ROOT / "scripts" / "export_openclaw_skill.py"
        self.assertTrue(script_path.exists(), "export script missing")

        with tempfile.TemporaryDirectory() as tmp_dir:
            output_dir = Path(tmp_dir) / "dist"
            result = subprocess.run(
                [
                    "python3",
                    str(script_path),
                    "--output-dir",
                    str(output_dir),
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(
                result.returncode,
                0,
                f"export failed: stdout={result.stdout}\nstderr={result.stderr}",
            )
            exported_skill = output_dir / "liangqin-brand-body"
            self.assertTrue(exported_skill.exists(), "standalone skill folder missing")
            self.assertTrue((exported_skill / "DESIGN.md").exists())
            self.assertTrue((exported_skill / "DESIGN-GOVERNANCE.md").exists())
            self.assertTrue((exported_skill / "SKILL.md").exists())
            self.assertTrue((exported_skill / "skill-release.json").exists())
            self.assertTrue((exported_skill / "foundation-dna").exists())
            self.assertTrue((exported_skill / "foundation-dna" / "design-dna.zh-CN.json").exists())
            self.assertTrue((exported_skill / "design-packs").exists())
            self.assertTrue((exported_skill / "design-packs" / "liangqin-apple.json").exists())
            self.assertTrue((exported_skill / "protocols").exists())
            self.assertTrue((exported_skill / "recipes").exists())
            self.assertTrue((exported_skill / "examples").exists())
            self.assertTrue((exported_skill / "evaluation").exists())
            self.assertTrue((exported_skill / "scripts" / "install_into_openclaw.py").exists())
            install_text = (exported_skill / "OPENCLAW_INSTALL.md").read_text(encoding="utf-8")
            self.assertIn("`良禽品牌体`", install_text)
            self.assertIn("`liangqin-brand-body`", install_text)
            self.assertIn("默认先读取 `DESIGN.md`", install_text)
            self.assertIn("`protocols/brand-boundaries.zh-CN.json`", install_text)
            self.assertIn("`recipes/module-recipes.zh-CN.json`", install_text)
            self.assertIn("良禽佳木apple风", install_text)
            self.assertIn("默认只使用 `良禽品牌体` 作为顶层品牌入口", install_text)
            self.assertIn("次级写作能力", install_text)

    def test_exported_installer_can_publish_to_openclaw_skill_stores(self):
        script_path = ROOT / "scripts" / "export_openclaw_skill.py"

        with tempfile.TemporaryDirectory() as tmp_dir:
            output_dir = Path(tmp_dir) / "dist"
            export = subprocess.run(
                [
                    "python3",
                    str(script_path),
                    "--output-dir",
                    str(output_dir),
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(export.returncode, 0, export.stderr)

            exported_skill = output_dir / "liangqin-brand-body"
            installer = exported_skill / "scripts" / "install_into_openclaw.py"
            active_dest = Path(tmp_dir) / "openclaw" / "skills" / "liangqin-brand-body"
            workspace_dest = (
                Path(tmp_dir) / "openclaw" / "workspace" / "skills" / "liangqin-brand-body"
            )

            install = subprocess.run(
                [
                    "python3",
                    str(installer),
                    "--source",
                    str(exported_skill),
                    "--dest",
                    str(active_dest),
                    "--workspace-dest",
                    str(workspace_dest),
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(install.returncode, 0, install.stderr)
            self.assertTrue((active_dest / "SKILL.md").exists())
            self.assertTrue((workspace_dest / "SKILL.md").exists())
            self.assertTrue((active_dest / "DESIGN.md").exists())
            self.assertTrue((workspace_dest / "skill-release.json").exists())


if __name__ == "__main__":
    unittest.main()
