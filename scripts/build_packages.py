#!/usr/bin/env python3
"""Build the only two supported skills reproducibly: Gemini Tasks and PowerPoint."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import stat
import zipfile

ROOT = Path(__file__).resolve().parents[1]
GEMINI = ROOT / "skills/weekly-it-news-gemini"
POWERPOINT = ROOT / "skills/itnews-powerpoint-polish"
TEMPLATE = ROOT / "assets/templates/weekly-it-news-design-template.pptx"
MANIFEST = ROOT / "assets/templates/template-manifest.json"
ZIP_DATE = (2020, 1, 1, 0, 0, 0)
SEMVER = re.compile(r"(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)(?:-[0-9A-Za-z.-]+)?\Z")
ALLOWED = {".md", ".json", ".py", ".js"}


def skill_files(folder: Path, expected: str) -> list[Path]:
    skill = folder / "SKILL.md"
    content = skill.read_text(encoding="utf-8")
    if not content.startswith("---\n") or not re.search(rf"(?m)^name: {re.escape(expected)}\s*$", content):
        raise ValueError(f"Invalid skill frontmatter: {skill}")
    if not re.search(r"(?m)^description: \S", content) or len(content) >= 20_000:
        raise ValueError(f"Invalid skill description or length: {skill}")
    result = [skill]
    for subdir in ("references", "templates", "scripts"):
        directory = folder / subdir
        if not directory.exists():
            continue
        for path in sorted(directory.rglob("*")):
            if path.is_dir():
                continue
            if path.is_symlink() or path.suffix.lower() not in ALLOWED:
                raise ValueError(f"Disallowed skill resource: {path}")
            result.append(path)
    if len(result) == 1:
        raise ValueError(f"No supporting resources: {folder}")
    return result


def validate(tag: str = "") -> tuple[str, list[Path], list[Path]]:
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    if not SEMVER.fullmatch(version):
        raise ValueError(f"Invalid VERSION: {version}")
    if tag and tag != "v" + version:
        raise ValueError(f"Refusing release {tag}: VERSION requires v{version}")
    gemini = skill_files(GEMINI, "weekly-it-news-gemini")
    powerpoint = skill_files(POWERPOINT, "itnews-powerpoint-polish")
    for required in (
        GEMINI / "scripts/build_pptx.py",
        GEMINI / "scripts/screenshot_relay.js",
        GEMINI / "references/plot-and-layout.md",
        GEMINI / "references/assets-and-handoff.md",
        GEMINI / "templates/plot.example.json",
        GEMINI / "templates/assets-manifest.example.json",
        POWERPOINT / "references/gemini-claude-handoff.md",
        TEMPLATE,
        MANIFEST,
        ROOT / "assets/cover/avatar-20260315.jpg",
        ROOT / "README.md",
    ):
        if not required.is_file():
            raise ValueError(f"Required project resource missing: {required}")
    spec = json.loads(MANIFEST.read_text(encoding="utf-8"))
    data = TEMPLATE.read_bytes()
    if spec["sha256"] != hashlib.sha256(data).hexdigest():
        raise ValueError("Template SHA-256 mismatch")
    if spec["size_bytes"] != len(data) or spec["slides"] != 8:
        raise ValueError("Unexpected template manifest")
    return version, gemini, powerpoint


def create_zip(output: Path, base: Path, files: list[Path]) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for source in sorted(files, key=lambda f: f.relative_to(base).as_posix()):
            info = zipfile.ZipInfo(source.relative_to(base).as_posix(), date_time=ZIP_DATE)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (stat.S_IFREG | 0o644) << 16
            info.create_system = 3
            z.writestr(info, source.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)


def build(out_dir: Path, tag: str = "") -> tuple[Path, Path]:
    version, gemini, powerpoint = validate(tag)
    gemini_zip = out_dir / f"itnews-creator-gemini-task-skill-v{version}.zip"
    polish_zip = out_dir / f"itnews-creator-powerpoint-polish-skill-v{version}.zip"
    create_zip(gemini_zip, GEMINI, gemini)
    create_zip(polish_zip, POWERPOINT, powerpoint)
    for result in (gemini_zip, polish_zip):
        with zipfile.ZipFile(result) as z:
            members = z.namelist()
            if z.testzip() is not None or len(members) != len(set(members)):
                raise ValueError(f"Corrupt or duplicate ZIP contents: {result}")
            if any(name.lower().endswith((".gs", ".pptx", ".png", ".jpg", ".jpeg")) for name in members):
                raise ValueError(f"Disallowed Gemini/PowerPoint skill file type: {result}")
        if result.stat().st_size > 50 * 1024 * 1024:
            raise ValueError(f"Too-large skill package: {result}")
    return gemini_zip, polish_zip


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, default=ROOT / "dist")
    parser.add_argument("--tag", default="")
    args = parser.parse_args()
    for path in build(args.out_dir, args.tag):
        print(f"Built {path} ({path.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
