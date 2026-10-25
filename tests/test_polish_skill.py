"""Portable PowerPoint polish skill release contract and cross-host handoff tests."""
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from tempfile import TemporaryDirectory
import json
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
POLISH = ROOT / 'skills' / 'itnews-powerpoint-polish'
AUTHOR = ROOT / 'skills' / 'weekly-it-news'
spec = spec_from_file_location('polish_builder', ROOT / 'scripts' / 'build_packages.py')
mod = module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(mod)


class PowerPointPolishSkillTest(unittest.TestCase):
    def test_two_distinct_skills(self):
        author = (AUTHOR / 'SKILL.md').read_text(encoding='utf-8')
        polish = (POLISH / 'SKILL.md').read_text(encoding='utf-8')
        self.assertIn('name: weekly-it-news', author)
        self.assertIn('name: itnews-powerpoint-polish', polish)
        self.assertIn('Copilot Chat', author)
        self.assertIn('existing .pptx', polish)
        self.assertIn('BASE DRAFT', author)
        self.assertIn('Copilot in PowerPoint', polish)
        self.assertLess(len(polish), 20000)
        self.assertNotIn('python scripts/qa_pptx.py', polish)

    def test_release_contains_three_separate_packages(self):
        version = json.loads((ROOT / 'plugin.json').read_text(encoding='utf-8'))['version']
        with TemporaryDirectory() as f1, TemporaryDirectory() as f2:
            archives1 = mod.build(Path(f1), tag='v' + version)
            archives2 = mod.build(Path(f2), tag='v' + version)
            self.assertEqual(len(archives1), 3)
            self.assertEqual([a.name for a in archives1], [a.name for a in archives2])
            for a, b in zip(archives1, archives2):
                self.assertEqual(a.read_bytes(), b.read_bytes())
            with zipfile.ZipFile(archives1[0]) as z:
                names = set(z.namelist())
                self.assertIn('skills/weekly-it-news/SKILL.md', names)
                self.assertIn('skills/itnews-powerpoint-polish/SKILL.md', names)
            with zipfile.ZipFile(archives1[1]) as z:
                names = set(z.namelist())
                self.assertIn('SKILL.md', names)
                self.assertIn('scripts/build_pptx.py', names)
                self.assertNotIn('references/review-rubric.md', names)
                self.assertIn('name: weekly-it-news', z.read('SKILL.md').decode())
            with zipfile.ZipFile(archives1[2]) as z:
                names = set(z.namelist())
                expected = {'SKILL.md', 'references/handoff-contract.md',
                            'references/review-rubric.md', 'references/visual-repair.md', 'references/topic-repair.md',
                            'templates/review-report.md'}
                self.assertEqual(names, expected)
                self.assertIn('name: itnews-powerpoint-polish', z.read('SKILL.md').decode())
                self.assertFalse(any(n.endswith(('.png', '.pdf', '.pptx', '.docx')) for n in names))

    def test_review_contract_preserves_story_and_truth(self):
        s = (POLISH / 'SKILL.md').read_text(encoding='utf-8')
        handoff = (POLISH / 'references' / 'handoff-contract.md').read_text(encoding='utf-8')
        rubric = (POLISH / 'references' / 'review-rubric.md').read_text(encoding='utf-8')
        self.assertIn('2026-01-25', s)
        self.assertIn('2026-04-12', s)
        self.assertIn('Do not restart news selection', s)
        self.assertIn('Do not call the whole job completed yet', handoff)
        self.assertIn('cannot automatically read', handoff)
        self.assertIn('base acceptable', rubric)
        self.assertIn('final incomplete', rubric)


if __name__ == '__main__':
    unittest.main()