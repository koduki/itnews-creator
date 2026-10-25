"""PPTX source-of-truth checks for the Gemini Tasks template (stdlib only)."""
from pathlib import Path
import hashlib
import json
import unittest
import zipfile
from xml.etree import ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
TEMPLATE=ROOT/'assets/templates/weekly-it-news-design-template.pptx'
MANIFEST=ROOT/'assets/templates/template-manifest.json'
GEMINI=ROOT/'skills/weekly-it-news-gemini/SKILL.md'
P='{http://schemas.openxmlformats.org/presentationml/2006/main}'

class GeminiTemplateSourceTest(unittest.TestCase):
    def test_template_is_real_editable_7_slide_pptx(self):
        spec=json.loads(MANIFEST.read_text(encoding='utf-8'))
        data=TEMPLATE.read_bytes()
        self.assertEqual(spec['size_bytes'],len(data))
        self.assertEqual(spec['sha256'],hashlib.sha256(data).hexdigest())
        self.assertEqual(spec['slides'],7)
        self.assertEqual(spec['raw_url'],
            'https://raw.githubusercontent.com/koduki/itnews-creator/main/'
            'assets/templates/weekly-it-news-design-template.pptx')
        with zipfile.ZipFile(TEMPLATE) as z:
            self.assertIsNone(z.testzip())
            pres=ET.fromstring(z.read('ppt/presentation.xml'))
            self.assertEqual(len(pres.findall('.//'+P+'sldId')),7)
            text1=''.join(ET.fromstring(z.read('ppt/slides/slide1.xml')).itertext())
            text2=''.join(ET.fromstring(z.read('ppt/slides/slide2.xml')).itertext())
            self.assertIn('Weekly IT News',text1)
            self.assertIn('今週のトピック',text2)
            self.assertTrue(any(n.startswith('ppt/media/') for n in z.namelist()))

    def test_task_skill_has_url_and_explicit_fallback(self):
        s=GEMINI.read_text(encoding='utf-8')
        spec=json.loads(MANIFEST.read_text(encoding='utf-8'))
        self.assertIn(spec['raw_url'],s)
        self.assertIn(spec['sha256'],s)
        self.assertIn('Google Drive',s)
        self.assertIn('取得できない',s)

if __name__=='__main__':
    unittest.main()
