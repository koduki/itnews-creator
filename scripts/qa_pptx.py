#!/usr/bin/env python3
"""Dependency-free structural QA for Copilot/ChatGPT-created PowerPoint files.

This does NOT render slides, inspect visual legibility, verify image copyright,
or generate PowerPoint presentations. It reports unverified issues truthfully.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

P = "http://schemas.openxmlformats.org/presentationml/2006/main"
A = "http://schemas.openxmlformats.org/drawingml/2006/main"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
REL = "http://schemas.openxmlformats.org/package/2006/relationships"
CT = "http://schemas.openxmlformats.org/package/2006/content-types"
SLIDE_RE = re.compile(r"^ppt/slides/slide([1-9][0-9]*)\.xml$")
MAX_FILE = 150 * 1024 * 1024


def assess(path: Path, manifest: Path | None = None, min_images: int = 0) -> dict:
    errors, warnings = [], []
    stats = {"slides": 0, "picture_shapes": 0, "picture_slides": [], "embedded_images": 0,
             "native_shapes": 0, "native_charts": 0, "image_evidence_verified": 0}
    if not path.exists():
        return {"status": "fail", "errors": ["PPTX file is missing"], "warnings": [], "stats": stats}
    if path.suffix.lower() != ".pptx":
        errors.append("PowerPoint requested, but the extension is not .pptx")
    if path.stat().st_size > MAX_FILE:
        errors.append("PPTX exceeds structural QA 150 MiB size limit")
        return {"status": "fail", "errors": errors, "warnings": warnings, "stats": stats}
    try:
        with zipfile.ZipFile(path) as z:
            bad = z.testzip()
            if bad:
                errors.append("Corrupt ZIP member: " + bad)
            names = set(z.namelist())
            if "ppt/presentation.xml" not in names or "[Content_Types].xml" not in names:
                errors.append("Not a valid PPTX package: missing presentation/content types")
            slides = sorted((int(m.group(1)), name) for name in names if (m := SLIDE_RE.fullmatch(name)))
            stats["slides"] = len(slides)
            if not slides:
                errors.append("No PowerPoint slides in file")
            stats["embedded_images"] = len([n for n in names if n.startswith("ppt/media/") and not n.endswith("/")])
            media_hashes = {n: hashlib.sha256(z.read(n)).hexdigest() for n in names if n.startswith("ppt/media/") and not n.endswith("/")}
            slide_picture_hashes = {}
            for num, slide_path in slides:
                try:
                    root = ET.fromstring(z.read(slide_path))
                    pictures = list(root.iter(f"{{{P}}}pic"))
                    stats["picture_shapes"] += len(pictures)
                    stats["native_shapes"] += len(list(root.iter(f"{{{P}}}sp")))
                    stats["native_charts"] += sum(1 for e in root.iter() if e.tag.endswith("}chart"))
                    if pictures:
                        stats["picture_slides"].append(num)
                    rels_path = f"ppt/slides/_rels/slide{num}.xml.rels"
                    relmap = {}
                    if rels_path in names:
                        relroot = ET.fromstring(z.read(rels_path))
                        for e in relroot.findall(f"{{{REL}}}Relationship"):
                            target = e.get("Target", "")
                            if target.startswith("../media/"):
                                relmap[e.get("Id")] = "ppt/media/" + target.split("../media/", 1)[1]
                            elif target.startswith("/ppt/media/"):
                                relmap[e.get("Id")] = target.lstrip("/")
                    used_hashes = set()
                    for pic in pictures:
                        for blip in pic.iter(f"{{{A}}}blip"):
                            loc = relmap.get(blip.get(f"{{{R}}}embed"))
                            if loc in media_hashes:
                                used_hashes.add(media_hashes[loc])
                    slide_picture_hashes[num] = used_hashes
                except ET.ParseError:
                    errors.append(f"Slide {num} contains malformed XML")
            if min_images > stats["picture_shapes"]:
                errors.append(f"Required {min_images} actual picture shapes; found {stats['picture_shapes']}")
            if manifest:
                try:
                    ledger = json.loads(manifest.read_text(encoding="utf-8"))
                    if ledger.get("schema_version") != "1.0" or not isinstance(ledger.get("assets"), list):
                        raise ValueError("Unsupported evidence manifest format")
                    for i, asset in enumerate(ledger["assets"], 1):
                        if not isinstance(asset, dict):
                            errors.append(f"Evidence {i} must be an object")
                            continue
                        needed = ("slide", "kind", "purpose", "source_url", "publisher", "rights_status", "embedded")
                        if any(k not in asset for k in needed):
                            errors.append(f"Evidence {i} lacks required metadata")
                            continue
                        num = asset["slide"]
                        if not isinstance(num, int) or num not in [n for n, _ in slides]:
                            errors.append(f"Evidence {i} refers to missing slide {num}")
                            continue
                        if asset["rights_status"] in ("unknown", "restricted") and asset["embedded"]:
                            warnings.append(f"Evidence {i}: reuse rights not confirmed")
                        if not str(asset["source_url"]).startswith(("https://", "http://")):
                            errors.append(f"Evidence {i} lacks source HTTP URL")
                        if asset["embedded"]:
                            digest = asset.get("sha256", "").lower()
                            if not re.fullmatch(r"[0-9a-f]{64}", digest):
                                errors.append(f"Evidence {i} marked embedded without 64-char media SHA256")
                            elif digest not in slide_picture_hashes.get(num, set()):
                                errors.append(f"Evidence {i}: claimed media SHA256 not found on slide {num}")
                            else:
                                stats["image_evidence_verified"] += 1
                    if any(not a.get("embedded", False) for a in ledger["assets"] if isinstance(a, dict)):
                        warnings.append("Some planned documentary assets were not embedded")
                except (ValueError, OSError, json.JSONDecodeError) as ex:
                    errors.append("Invalid/unreadable evidence manifest: " + str(ex))
            else:
                warnings.append("No evidence manifest: photo provenance and correspondence unverified")
            warnings.append("Structural QA only: visual rendering, factual accuracy and licensing remain unverified")
    except (zipfile.BadZipFile, OSError) as ex:
        errors.append("Cannot open PPTX archive: " + str(ex))
    return {"status": "fail" if errors else "pass", "errors": errors, "warnings": warnings, "stats": stats}


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("pptx", type=Path)
    p.add_argument("--manifest", type=Path, default=None, help="Optional evidence provenance JSON")
    p.add_argument("--min-images", type=int, default=0, help="Minimum count of real picture shapes; only when requested")
    p.add_argument("--json", action="store_true", help="Emit JSON (otherwise also JSON, for stable automation)")
    a = p.parse_args(argv)
    if a.min_images < 0:
        p.error("--min-images must not be negative")
    report = assess(a.pptx, a.manifest, a.min_images)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())