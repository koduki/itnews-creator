"""PowerPoint only polishes existing Gemini-authored presentations."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
GEMINI = ROOT / "skills/weekly-it-news-gemini"
POLISH = ROOT / "skills/itnews-powerpoint-polish"


class PolishTests(unittest.TestCase):
    def test_two_only(self):
        self.assertIn("name: weekly-it-news-gemini", (GEMINI / "SKILL.md").read_text())
        s = (POLISH / "SKILL.md").read_text()
        for x in ("name: itnews-powerpoint-polish", "existing .pptx", "NEWS_TITLE", "Claude"):
            self.assertIn(x, s)
        self.assertNotIn("references/handoff-contract.md", s)
        self.assertNotIn("references/topic-repair.md", s)
        self.assertLess(len(s), 20_000)

    def test_current_handoff(self):
        s = (POLISH / "references/gemini-claude-handoff.md").read_text()
        self.assertIn("NEWS_TITLE", s)
        self.assertIn("assets-manifest.json", s)
        rubric = (POLISH / "references/review-rubric.md").read_text()
        self.assertIn("B0", rubric)
        self.assertIn("画像", rubric)


if __name__ == "__main__":
    unittest.main()
