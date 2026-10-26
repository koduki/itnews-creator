"""Only the two active skills are packaged, reproducibly."""
import importlib.util
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("packages", ROOT / "scripts/build_packages.py")
packages = importlib.util.module_from_spec(spec)
spec.loader.exec_module(packages)


class PackageTests(unittest.TestCase):
    def test_two_reproducible_skill_packages(self):
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        with TemporaryDirectory() as first, TemporaryDirectory() as second:
            a = packages.build(Path(first), tag="v" + version)
            b = packages.build(Path(second), tag="v" + version)
            self.assertEqual([p.name for p in a], [
                f"itnews-creator-gemini-task-skill-v{version}.zip",
                f"itnews-creator-powerpoint-polish-skill-v{version}.zip",
            ])
            self.assertEqual(len(a), 2)
            for p, q in zip(a, b):
                self.assertEqual(p.read_bytes(), q.read_bytes())
                with zipfile.ZipFile(p) as z:
                    self.assertIsNone(z.testzip())
                    self.assertFalse(any(n.endswith((".gs", ".pptx", ".png", ".jpg")) for n in z.namelist()))
            with zipfile.ZipFile(a[0]) as z:
                self.assertIn("scripts/build_pptx.py", z.namelist())
                self.assertIn("scripts/screenshot_relay.js", z.namelist())
                self.assertIn("templates/assets-manifest.example.json", z.namelist())
            with zipfile.ZipFile(a[1]) as z:
                self.assertIn("references/gemini-claude-handoff.md", z.namelist())
                self.assertNotIn("references/handoff-contract.md", z.namelist())
                self.assertNotIn("references/topic-repair.md", z.namelist())

    def test_release_tag_guard(self):
        with TemporaryDirectory() as dest:
            with self.assertRaisesRegex(ValueError, "Refusing release"):
                packages.build(Path(dest), tag="v999.999.999")

    def test_legacy_is_gone(self):
        for path in ("plugin.json", "skills/weekly-it-news", "scripts/qa_pptx.py",
                     "schemas", "examples/handoff"):
            self.assertFalse((ROOT / path).exists(), path)


if __name__ == "__main__":
    unittest.main()
