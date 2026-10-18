"""Dependency-free structural checks for portable skill source."""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / 'skills' / 'weekly-it-news'
SKILL = SKILL_DIR / 'SKILL.md'


def check():
    manifest = json.loads((ROOT / 'plugin.json').read_text(encoding='utf-8'))
    assert manifest['$schema'] == 'https://agent-plugins.org/schemas/1.0.0/plugin.schema.json'
    assert manifest['name'] == 'itnews-creator'
    text = SKILL.read_text(encoding='utf-8')
    assert text.startswith('---\n')
    assert re.search(r'^name: weekly-it-news$', text, re.M)
    assert re.search(r'^description: \S', text, re.M)
    assert len(text) < 20_000, f'M365 skill instruction length: {len(text)}'
    for name in ('style-from-samples.md', 'visual-evidence.md', 'quality-gates.md', 'platform-compatibility.md'):
        assert (SKILL_DIR / 'references' / name).is_file(), name
        assert name in text, name
    assert (SKILL_DIR / 'templates' / 'slide-plan.md').is_file()
    assert '0 is a hard reject' in text
    assert 'Never manufacture' in text
    print('PASS: plugin manifest + skill frontmatter + skill length + references + core evidence gates')


if __name__ == '__main__':
    check()