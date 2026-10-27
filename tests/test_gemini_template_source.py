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
    def test_template_is_real_editable_8_slide_pptx(self):
        spec=json.loads(MANIFEST.read_text(encoding='utf-8'))
        data=TEMPLATE.read_bytes()
        self.assertEqual(spec['size_bytes'],len(data))
        self.assertEqual(spec['sha256'],hashlib.sha256(data).hexdigest())
        self.assertEqual(spec['slides'],8)
        self.assertEqual(spec['raw_url'],
            'https://raw.githubusercontent.com/koduki/itnews-creator/main/'
            'assets/templates/weekly-it-news-design-template.pptx')
        with zipfile.ZipFile(TEMPLATE) as z:
            self.assertIsNone(z.testzip())
            pres=ET.fromstring(z.read('ppt/presentation.xml'))
            self.assertEqual(len(pres.findall('.//'+P+'sldId')),8)
            text1=''.join(ET.fromstring(z.read('ppt/slides/slide1.xml')).itertext())
            text2=''.join(ET.fromstring(z.read('ppt/slides/slide2.xml')).itertext())
            self.assertIn('Weekly IT News',text1)
            self.assertIn('今週のトピック',text2)
            text3=''.join(ET.fromstring(z.read('ppt/slides/slide3.xml')).itertext())
            self.assertIn('NEWS 01',text3)
            self.assertIn('ニュースのタイトル',text3)
            self.assertEqual(spec['layouts'][2], 'NEWS_TITLE')
            self.assertTrue(any(n.startswith('ppt/media/') for n in z.namelist()))

    def test_task_skill_has_url_and_explicit_fallback(self):
        s=GEMINI.read_text(encoding='utf-8')
        spec=json.loads(MANIFEST.read_text(encoding='utf-8'))
        self.assertIn(spec['raw_url'],s)
        self.assertIn(spec['sha256'],s)
        self.assertIn('Google Drive',s)
        self.assertIn('取得できない',s)

    def test_backported_workflow_and_gas_relay_script(self):
        s = GEMINI.read_text(encoding='utf-8')
        plot_ref = (ROOT / 'skills/weekly-it-news-gemini/references/plot-and-layout.md').read_text(encoding='utf-8')
        assets_ref = (ROOT / 'skills/weekly-it-news-gemini/references/assets-and-handoff.md').read_text(encoding='utf-8')
        relay_js = ROOT / 'skills/weekly-it-news-gemini/scripts/screenshot_relay.js'
        self.assertTrue(relay_js.is_file())
        self.assertIn('デザインの唯一の正本', s)
        self.assertIn('1ページ1スクショ', s)
        self.assertIn('itnews-screenshot-queue', s)
        self.assertIn('デザインの唯一の正本', plot_ref)
        self.assertIn('色', plot_ref)
        self.assertIn('screenshot_relay.js', assets_ref)
        self.assertIn('PageSpeed', relay_js.read_text(encoding='utf-8'))

if __name__=='__main__':
    unittest.main()