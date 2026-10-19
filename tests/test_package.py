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
    assert manifest['license'] == 'MIT'
    license_text = (ROOT / 'LICENSE').read_text(encoding='utf-8')
    assert license_text.startswith('MIT License\n')
    assert 'Copyright (c) 2026 koduki' in license_text
    assert re.fullmatch(r'\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?', manifest['version'])
    text = SKILL.read_text(encoding='utf-8')
    assert text.startswith('---\n')
    assert re.search(r'^name: weekly-it-news$', text, re.M)
    assert re.search(r'^description: \S', text, re.M)
    assert len(text) < 20_000, f'M365 skill instruction length: {len(text)}'
    for name in ('editorial-structure.md', 'style-from-samples.md', 'visual-evidence.md', 'quality-gates.md', 'platform-compatibility.md'):
        assert (SKILL_DIR / 'references' / name).is_file(), name
        assert name in text, name
    assert (SKILL_DIR / 'templates' / 'slide-plan.md').is_file()
    assert '0 is a hard reject' in text
    assert 'Never manufacture' in text
    assert '2026-01-25' in text and '2026-04-12' in text
    structure = (SKILL_DIR / 'references' / 'editorial-structure.md').read_text(encoding='utf-8')
    assert 'source' in structure.lower() and 'news' in structure.lower()
    print(f"PASS: v{manifest['version']} portable structure, canonical early-deck format and QA gates")


if __name__ == '__main__':
    check()