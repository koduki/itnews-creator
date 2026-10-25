"""Offline regression tests for the optional PPTX structural QA program."""
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from tempfile import TemporaryDirectory
import hashlib
import json
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
spec = spec_from_file_location("qa_pptx", ROOT / "scripts" / "qa_pptx.py")
qa = module_from_spec(spec)
spec.loader.exec_module(qa)
MEDIA = b"synthetic-image-bytes-not-a-real-png"


def fixture(path: Path, with_picture=True):
    slide = '''<?xml version="1.0"?>
<p:sld xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"
 xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
 xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
 <p:cSld><p:spTree><p:sp/><p:pic><p:blipFill><a:blip r:embed="rId2"/></p:blipFill></p:pic></p:spTree></p:cSld>
</p:sld>''' if with_picture else '''<p:sld xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"/>'''
    rel = '''<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId2" Type="image" Target="../media/image1.png"/></Relationships>'''
    with zipfile.ZipFile(path, "w") as z:
        z.writestr("[Content_Types].xml", '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"/>')
        z.writestr("ppt/presentation.xml", '<p:presentation xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"/>')
        z.writestr("ppt/slides/slide1.xml", slide)
        if with_picture:
            z.writestr("ppt/slides/_rels/slide1.xml.rels", rel)
            z.writestr("ppt/media/image1.png", MEDIA)


def ledger(path, digest=None, embedded=True):
    path.write_text(json.dumps({"schema_version": "1.0", "presentation": "test", "assets": [{
        "slide": 1, "kind": "news_photo", "purpose": "visual evidence", "source_url": "https://example.org/news",
        "publisher": "Example", "rights_status": "permitted", "embedded": embedded,
        "sha256": digest or hashlib.sha256(MEDIA).hexdigest()}
    ]}), encoding="utf-8")


class QATests(unittest.TestCase):
    def test_valid_embedded_media_and_manifest(self):
        with TemporaryDirectory() as tmp:
            p, m = Path(tmp)/"ok.pptx", Path(tmp)/"evidence.json"
            fixture(p)
            ledger(m)
            result = qa.assess(p, m, min_images=1)
            self.assertEqual(result["status"], "pass", result)
            self.assertEqual(result["stats"]["slides"], 1)
            self.assertEqual(result["stats"]["image_evidence_verified"], 1)

    def test_word_not_a_pptx(self):
        with TemporaryDirectory() as tmp:
            p = Path(tmp)/"draft.docx"
            p.write_text("A Word document")
            result = qa.assess(p)
            self.assertEqual(result["status"], "fail")
            self.assertTrue(any("extension" in e for e in result["errors"]))

    def test_no_picture_fails_requirement(self):
        with TemporaryDirectory() as tmp:
            p = Path(tmp)/"no-image.pptx"
            fixture(p, False)
            result = qa.assess(p, min_images=1)
            self.assertEqual(result["status"], "fail")
            self.assertEqual(result["stats"]["picture_shapes"], 0)

    def test_wrong_slide_hash_detected(self):
        with TemporaryDirectory() as tmp:
            p, m = Path(tmp)/"wrong.pptx", Path(tmp)/"evidence.json"
            fixture(p)
            ledger(m, digest="f" * 64)
            result = qa.assess(p, m)
            self.assertEqual(result["status"], "fail")
            self.assertTrue(any("SHA256 not found" in e for e in result["errors"]))

    def test_unembedded_planned_asset_not_claimed_valid(self):
        with TemporaryDirectory() as tmp:
            p, m = Path(tmp)/"planned.pptx", Path(tmp)/"evidence.json"
            fixture(p)
            ledger(m, embedded=False)
            result = qa.assess(p, m)
            self.assertEqual(result["status"], "pass")
            self.assertEqual(result["stats"]["image_evidence_verified"], 0)
            self.assertTrue(any("not embedded" in w for w in result["warnings"]))


if __name__ == "__main__":
    unittest.main()