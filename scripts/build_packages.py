#!/usr/bin/env python3
"""Build portable ChatGPT and Microsoft 365 Copilot skills from one source tree.

Standard-library only. Outputs have fixed metadata, sorted entries and no
machine-specific paths; this intentionally does not publish/install either skill.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import stat
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / "skills" / "weekly-it-news"
MANIFEST = ROOT / "plugin.json"
SEMVER = re.compile(r"(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?\Z")
# Fixed ZIP timestamp (min supported: 1980-01-01) makes output stable.
ZIP_DATE = (2020, 1, 1, 0, 0, 0)


def validate(tag: str = "") -> tuple[str, list[Path]]:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest.get("$schema") == "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
    assert manifest.get("name") == "itnews-creator"
    version = manifest.get("version", "")
    assert isinstance(version, str) and SEMVER.fullmatch(version), f"Invalid SemVer: {version}"
    if tag and tag != f"v{version}":
        raise ValueError(f"Refusing release {tag}: plugin.json requires v{version}")
    main = SKILL_ROOT / "SKILL.md"
    skill = main.read_text(encoding="utf-8")
    assert skill.startswith("---\n"), "Missing SKILL.md YAML frontmatter"
    assert re.search(r"(?m)^name: weekly-it-news\s*$", skill)
    assert re.search(r"(?m)^description: \S", skill)
    assert len(skill) < 20_000, "M365 Copilot skill instructions exceed 20,000 characters"
    assert main.stat().st_size < 1024 * 1024, "SKILL.md exceeds 1 MiB"
    support = sorted([*SKILL_ROOT.glob("references/*.md"), *SKILL_ROOT.glob("templates/*.md")])
    assert support and all(p.is_file() for p in support)
    for required in ("editorial-structure.md", "style-from-samples.md", "visual-evidence.md", "quality-gates.md", "platform-compatibility.md", "copilot-runtime-diagnostics.md"):
        assert (SKILL_ROOT / "references" / required).is_file(), f"Missing {required}"
        assert required in skill, f"SKILL.md does not reference {required}"
    inputs = [main, *support]
    for p in [ROOT / "README.md", MANIFEST, *inputs]:
        assert p.is_file() and not p.is_symlink(), f"Missing or unsafe input: {p}"
        p.read_text(encoding="utf-8")
    return version, inputs


def create_zip(output: Path, entries: list[tuple[Path, str]]) -> None:
    names = [name for _, name in entries]
    assert len(names) == len(set(names)), "Duplicate archive member"
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for source, name in sorted(entries, key=lambda entry: entry[1]):
            assert not name.startswith("/") and ".." not in Path(name).parts
            item = zipfile.ZipInfo(name, date_time=ZIP_DATE)
            item.compress_type = zipfile.ZIP_DEFLATED
            item.external_attr = (stat.S_IFREG | 0o644) << 16
            item.create_system = 3
            z.writestr(item, source.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)


def build(out_dir: Path, tag: str = "") -> tuple[Path, Path]:
    version, inputs = validate(tag)
    shared = [(p, p.relative_to(SKILL_ROOT).as_posix()) for p in inputs]
    chatgpt = out_dir / f"itnews-creator-chatgpt-plugin-v{version}.zip"
    copilot = out_dir / f"itnews-creator-copilot-skill-v{version}.zip"
    create_zip(chatgpt, [
        (ROOT / "README.md", "README.md"),
        (MANIFEST, "plugin.json"),
        *((p, "skills/weekly-it-news/" + name) for p, name in shared),
    ])
    create_zip(copilot, shared)  # Microsoft wants SKILL.md at ZIP root.
    for archive in (chatgpt, copilot):
        with zipfile.ZipFile(archive) as z:
            assert z.testzip() is None, f"Corrupt ZIP: {archive}"
            assert all(not name.endswith("/") for name in z.namelist())
    assert copilot.stat().st_size <= 50 * 1024 * 1024, "M365 upload exceeds 50 MB"
    return chatgpt, copilot


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, default=ROOT / "dist")
    parser.add_argument("--tag", default="", help="Validate release tag (e.g., v0.3.0) against plugin.json")
    args = parser.parse_args()
    for output in build(args.out_dir, args.tag):
        print(f"Built {output} ({output.stat().st_size} bytes)")


if __name__ == "__main__":
    main()