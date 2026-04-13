import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class PrepareOpenclawReleaseTest(unittest.TestCase):
    def test_prepare_release_script_builds_zip_bundle(self):
        script_path = ROOT / "scripts" / "prepare_openclaw_release.py"
        self.assertTrue(script_path.exists(), "prepare release script missing")

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
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("[run] sync OpenClaw mirrors", result.stdout)
            self.assertIn("[run] run core release tests", result.stdout)
            self.assertIn("[run] validate exported skill assets", result.stdout)
            self.assertIn("[run] export OpenClaw release bundle", result.stdout)
            self.assertIn("Prepared release artifact:", result.stdout)
            self.assertTrue((output_dir / "liangqin-brand-body-2.1.0.zip").exists())


if __name__ == "__main__":
    unittest.main()
