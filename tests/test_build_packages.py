"""Run packaging tests without third-party dependencies or GitHub credentials."""
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from tempfile import TemporaryDirectory
import json
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
spec = spec_from_file_location("build_packages", ROOT / "scripts" / "build_packages.py")
build_packages = module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(build_packages)


class BuildPackagesTest(unittest.TestCase):
    def test_both_formats_and_deterministic_content(self):
        version = json.loads((ROOT / "plugin.json").read_text(encoding="utf-8"))["version"]
        with TemporaryDirectory() as first, TemporaryDirectory() as second:
            first_archives = build_packages.build(Path(first), tag=f"v{version}")
            second_archives = build_packages.build(Path(second), tag=f"v{version}")
            for a, b in zip(first_archives, second_archives):
                self.assertEqual(a.read_bytes(), b.read_bytes(), a.name)
                with zipfile.ZipFile(a) as z:
                    self.assertIsNone(z.testzip())
                    self.assertEqual(len(z.namelist()), len(set(z.namelist())))
            with zipfile.ZipFile(first_archives[0]) as z:
                members = set(z.namelist())
                self.assertIn("plugin.json", members)
                self.assertIn("README.md", members)
                self.assertIn("skills/weekly-it-news/SKILL.md", members)
                self.assertNotIn("tests/test_package.py", members)
                self.assertEqual(json.loads(z.read("plugin.json"))["version"], version)
            with zipfile.ZipFile(first_archives[1]) as z:
                members = set(z.namelist())
                self.assertIn("SKILL.md", members)
                self.assertIn("references/editorial-structure.md", members)
                self.assertIn("templates/slide-plan.md", members)
                self.assertNotIn("plugin.json", members)
                self.assertFalse(any(name.startswith("skills/") for name in members))

    def test_release_must_match_manifest(self):
        with TemporaryDirectory() as dest:
            with self.assertRaisesRegex(ValueError, "Refusing release"):
                build_packages.build(Path(dest), tag="v999.999.999")


if __name__ == "__main__":
    unittest.main()