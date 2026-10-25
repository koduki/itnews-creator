"""Real PPTX generation regressions, entirely offline with standard Python."""
import base64
import importlib.util
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from zipfile import ZipFile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'skills' / 'weekly-it-news' / 'scripts' / 'build_pptx.py'
spec = importlib.util.spec_from_file_location('chat_builder', SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
# A tiny genuine local PNG file; synthetic test asset, not publication evidence.
PNG = base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQIHWP4z8DwHwAFgAI/ScL/nwAAAABJRU5ErkJggg==')

class ChatPptxTest(unittest.TestCase):
    def write_plan(self, base, slides, min_evidence_images=0):
        path = base / 'plan.json'
        path.write_text(json.dumps({'min_evidence_images':min_evidence_images,'slides':slides},ensure_ascii=False),encoding='utf-8')
        return path

    def test_real_editable_pptx_and_embedded_image(self):
        with TemporaryDirectory() as td:
            base=Path(td)
            (base/'actual.png').write_bytes(PNG)
            plan=self.write_plan(base,[
                {'layout':'cover','date':'2026-10-25','title':'Weekly IT News！'},
                {'layout':'agenda','title':'今週のトピック','bullets':['ニュースA','ニュースB']},
                {'layout':'evidence','title':'ソース図','image':'actual.png','caption':'デモ画像でニュースの証拠ではない'}
            ],min_evidence_images=1)
            target=base/'result.pptx'
            count,n_images=mod.build(plan,target)
            self.assertEqual((count,n_images),(3,1))
            self.assertTrue(target.is_file())
            with ZipFile(target) as z:
                self.assertIsNone(z.testzip())
                self.assertIn('ppt/presentation.xml',z.namelist())
                self.assertIn('ppt/slides/slide3.xml',z.namelist())
                self.assertEqual(z.read('ppt/media/image2.png'),PNG)
                slide=ET.fromstring(z.read('ppt/slides/slide3.xml'))
                ns={'a':mod.A,'p':mod.P}
                vals=[x.text for x in slide.findall('.//a:t',ns)]
                self.assertIn('ソース図',vals)
                self.assertTrue(slide.findall('.//p:pic',ns))
                self.assertIn(b'image2.png',z.read('ppt/slides/_rels/slide3.xml.rels'))

    def test_missing_evidence_is_not_silent_success(self):
        with TemporaryDirectory() as td:
            base=Path(td)
            plan=self.write_plan(base,[{'title':'文章のみ','bullets':['スクショは存在しない']}],min_evidence_images=1)
            output=base/'missing.pptx'
            with self.assertRaisesRegex(ValueError,'Image requirement unmet'):
                mod.build(plan,output)
            self.assertFalse(output.exists())

    def test_word_output_and_fake_images_are_rejected(self):
        with TemporaryDirectory() as td:
            base=Path(td)
            plan=self.write_plan(base,[{'title':'テスト'}])
            with self.assertRaisesRegex(ValueError,'Output must be a .pptx'):
                mod.build(plan,base/'out.docx')
            (base/'fake.png').write_text('not actual image bytes')
            plan=self.write_plan(base,[{'title':'Fake','image':'fake.png'}])
            with self.assertRaisesRegex(ValueError,'genuine local PNG'):
                mod.build(plan,base/'nope.pptx')

if __name__=='__main__': unittest.main()