#!/usr/bin/env python3
"""Reproducibly package two complementary Copilot skills and one ChatGPT plugin.

No third-party dependencies; packaging doesn't install any skill in user accounts.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import stat
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / 'skills' / 'weekly-it-news'
POLISH_ROOT = ROOT / 'skills' / 'itnews-powerpoint-polish'
COVER_ROOT = ROOT / 'assets' / 'cover'
MANIFEST = ROOT / 'plugin.json'
SEMVER = re.compile(r'(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?\Z')
ZIP_DATE = (2020, 1, 1, 0, 0, 0)


def skill_files(folder: Path, expected_name: str) -> list[Path]:
    skill = folder / 'SKILL.md'
    text = skill.read_text(encoding='utf-8')
    assert text.startswith('---\n'), f'No frontmatter: {skill}'
    assert re.search(rf'(?m)^name: {re.escape(expected_name)}\s*$', text), f'Incorrect skill name: {skill}'
    assert re.search(r'(?m)^description: \S', text), f'Missing description: {skill}'
    assert len(text) < 20_000, f'Skill must be under 20,000 chars: {skill}'
    assert skill.stat().st_size < 1024 * 1024
    resources = sorted([
        *folder.glob('references/*.md'),
        *folder.glob('templates/*.md'),
        *folder.glob('templates/*.json'),
        *folder.glob('scripts/*.py'),
    ])
    assert resources, f'No supporting resources: {folder}'
    assert all(p.is_file() and not p.is_symlink() for p in resources)
    return [skill, *resources]


def validate(tag: str = '') -> tuple[str, list[Path]]:
    manifest = json.loads(MANIFEST.read_text(encoding='utf-8'))
    assert manifest.get('$schema') == 'https://agent-plugins.org/schemas/1.0.0/plugin.schema.json'
    assert manifest.get('name') == 'itnews-creator'
    version = manifest.get('version', '')
    assert isinstance(version, str) and SEMVER.fullmatch(version), f'Invalid SemVer: {version}'
    if tag and tag != f'v{version}':
        raise ValueError(f'Refusing release {tag}: plugin.json requires v{version}')

    author = skill_files(SKILL_ROOT, 'weekly-it-news')
    polish = skill_files(POLISH_ROOT, 'itnews-powerpoint-polish')
    author_main = author[0].read_text(encoding='utf-8')
    polish_main = polish[0].read_text(encoding='utf-8')
    for req in ('editorial-structure.md', 'style-from-samples.md', 'visual-evidence.md',
                'quality-gates.md', 'platform-compatibility.md', 'copilot-runtime-diagnostics.md',
                'copilot-native-workflow.md', 'copilot-chat-workflow.md', 'production-handoff.md', 'acceptance-tests.md', 'story-continuity.md'):
        assert (SKILL_ROOT / 'references' / req).is_file()
        assert req in author_main, f'Unreferenced author resource: {req}'
    assert (SKILL_ROOT / 'scripts' / 'build_pptx.py').is_file()
    assert 'scripts/build_pptx.py' in author_main
    assert (SKILL_ROOT / 'scripts' / 'check_editorial_flow.py').is_file()
    assert 'scripts/check_editorial_flow.py' in author_main
    assert (SKILL_ROOT / 'templates' / 'editorial-storyboard.example.json').is_file()
    for req in ('handoff-contract.md', 'review-rubric.md', 'visual-repair.md', 'topic-repair.md'):
        assert (POLISH_ROOT / 'references' / req).is_file()
        assert req in polish_main, f'Unreferenced polish resource: {req}'
    assert (POLISH_ROOT / 'templates' / 'review-report.md').is_file()
    assert 'templates/review-report.md' in polish_main
    for p in (ROOT / 'README.md', MANIFEST, *author, *polish):
        assert p.is_file() and not p.is_symlink(), f'Missing or unsafe input {p}'
        p.read_text(encoding='utf-8')
    assets = cover_assets()
    return version, [*author, *polish, *assets]


def cover_assets() -> list[Path]:
    names = ('weekly-it-news-cover-20260315.pptx', 'avatar-20260315.jpg', 'cover-preview-20260315.jpg', 'README.md')
    result = [COVER_ROOT / name for name in names]
    for path in result:
        assert path.is_file() and not path.is_symlink() and path.stat().st_size > 0, f'Missing cover asset: {path}'
    with zipfile.ZipFile(result[0]) as z:
        assert z.testzip() is None and 'ppt/slides/slide1.xml' in z.namelist()
    return result


def create_zip(output: Path, entries: list[tuple[Path, str]]) -> None:
    names = [name for _, name in entries]
    assert len(names) == len(set(names)), 'Duplicate archive member'
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for source, name in sorted(entries, key=lambda e: e[1]):
            assert not name.startswith('/') and '..' not in Path(name).parts
            item = zipfile.ZipInfo(name, date_time=ZIP_DATE)
            item.compress_type = zipfile.ZIP_DEFLATED
            item.external_attr = (stat.S_IFREG | 0o644) << 16
            item.create_system = 3
            z.writestr(item, source.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)


def build(out_dir: Path, tag: str = '') -> tuple[Path, Path, Path]:
    version, _ = validate(tag)
    author_files = skill_files(SKILL_ROOT, 'weekly-it-news')
    polish_files = skill_files(POLISH_ROOT, 'itnews-powerpoint-polish')
    author = [(p, p.relative_to(SKILL_ROOT).as_posix()) for p in author_files]
    cover = [(p, 'assets/cover/' + p.name) for p in cover_assets()]
    polish = [(p, p.relative_to(POLISH_ROOT).as_posix()) for p in polish_files]
    chatgpt = out_dir / f'itnews-creator-chatgpt-plugin-v{version}.zip'
    copilot = out_dir / f'itnews-creator-copilot-skill-v{version}.zip'
    power = out_dir / f'itnews-creator-powerpoint-polish-skill-v{version}.zip'
    create_zip(chatgpt, [
        (ROOT / 'README.md', 'README.md'),
        (MANIFEST, 'plugin.json'),
        *((p, 'skills/weekly-it-news/' + name) for p, name in author),
        *((p, 'skills/weekly-it-news/' + name) for p, name in cover),
        *((p, 'skills/itnews-powerpoint-polish/' + name) for p, name in polish),
        *((p, 'skills/itnews-powerpoint-polish/' + name) for p, name in cover),
    ])
    create_zip(copilot, [*author, *cover])
    create_zip(power, [*polish, *cover])
    for archive in (chatgpt, copilot, power):
        with zipfile.ZipFile(archive) as z:
            assert z.testzip() is None, f'Corrupt ZIP: {archive}'
            assert all(not x.endswith('/') for x in z.namelist())
        assert archive.stat().st_size <= 50 * 1024 * 1024, f'Archive exceeds 50 MB: {archive}'
    return chatgpt, copilot, power


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out-dir', type=Path, default=ROOT / 'dist')
    parser.add_argument('--tag', default='', help='Validate tag e.g. v0.7.1 against plugin.json')
    a = parser.parse_args()
    for p in build(a.out_dir, a.tag):
        print(f'Built {p} ({p.stat().st_size} bytes)')


if __name__ == '__main__':
    main()