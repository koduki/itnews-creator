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

    def test_backported_workflow_and_gas_relay_script(self):
        s = GEMINI.read_text(encoding='utf-8')
        plot_ref = (ROOT / 'skills/weekly-it-news-gemini/references/plot-and-layout.md').read_text(encoding='utf-8')
        assets_ref = (ROOT / 'skills/weekly-it-news-gemini/references/assets-and-handoff.md').read_text(encoding='utf-8')
        relay_js = ROOT / 'skills/weekly-it-news-gemini/scripts/screenshot_relay.js'
        self.assertTrue(relay_js.is_file())
        self.assertIn('常駐型AIエージェント', s)
        self.assertIn('1ページ1スクショ', s)
        self.assertIn('itnews-screenshot-queue', s)
        self.assertIn('パターンA', plot_ref)
        self.assertIn('パターンB', plot_ref)
        self.assertIn('パターンC', plot_ref)
        self.assertIn('Meiryo UI', plot_ref)
        self.assertIn('screenshot_relay.js', assets_ref)
        js = relay_js.read_text(encoding='utf-8')
        self.assertIn('PageSpeed', js)
        self.assertIn('/width/1280/crop/853/noanimate/', js)
        self.assertIn('Missing required queue columns', js)
        self.assertIn('status', js)

    def test_packaged_gemini_skill_contains_js_but_no_gs_or_binary(self):
        import importlib.util
        from tempfile import TemporaryDirectory
        spec=importlib.util.spec_from_file_location('packages',ROOT/'scripts/build_packages.py')
        m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
        with TemporaryDirectory() as td:
            archive=m.build(Path(td))[-1]
            with zipfile.ZipFile(archive) as z:
                self.assertIn('scripts/screenshot_relay.js',z.namelist())
                self.assertFalse(any(n.endswith(('.gs','.pptx','.png','.jpg','.jpeg')) for n in z.namelist()))
        r=(ROOT/'README.md').read_text(encoding='utf-8')
        self.assertIn('drive:download_file_content',r)
        self.assertIn('GAS',r)

if __name__=='__main__':
    unittest.main()