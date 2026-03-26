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
            exported_skill = output_dir / "liangqin-brand-openclaw"
            self.assertTrue(exported_skill.exists(), "standalone skill folder missing")
            self.assertTrue((exported_skill / "SKILL.md").exists())
            self.assertTrue((exported_skill / "protocols").exists())
            self.assertTrue((exported_skill / "recipes").exists())
            self.assertTrue((exported_skill / "examples").exists())
            self.assertTrue((exported_skill / "evaluation").exists())


if __name__ == "__main__":
    unittest.main()
