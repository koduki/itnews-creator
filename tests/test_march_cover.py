"""Cover fidelity and bundled source-image tests without optional packages."""
from pathlib import Path
import importlib.util
import json
import subprocess
import sys
import unittest
import xml.etree.ElementTree as ET
from tempfile import TemporaryDirectory
from zipfile import ZipFile

ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/'assets'/'cover'
AVATAR=ASSETS/'avatar-20260315.jpg'
TEMPLATE=ASSETS/'weekly-it-news-cover-20260315.pptx'

class MarchCoverTest(unittest.TestCase):
    def test_single_slide_original_avatar_and_editable_topic(self):
        avatar=AVATAR.read_bytes()
        self.assertTrue(avatar.startswith(b'\xff\xd8\xff'))
        with ZipFile(TEMPLATE) as z:
            self.assertIsNone(z.testzip())
            pres=ET.fromstring(z.read('ppt/presentation.xml'))
            ns={'p':'http://schemas.openxmlformats.org/presentationml/2006/main'}
            self.assertEqual(len(pres.findall('.//p:sldId',ns)),1)
            pic_files=[x for x in z.namelist() if x.startswith('ppt/media/')]
            self.assertEqual(len(pic_files),1)
            self.assertEqual(z.read(pic_files[0]),avatar)
            text=''.join(ET.fromstring(z.read('ppt/slides/slide1.xml')).itertext())
            for value in ('Weekly','IT','News','今週のトピック'):
                self.assertIn(value,text)
            self.assertNotIn('ppt/slides/slide2.xml', z.namelist())

    def test_copilot_chat_gen_changes_cover_but_keeps_agenda(self):
        script=ROOT/'skills'/'weekly-it-news'/'scripts'/'build_pptx.py'
        with TemporaryDirectory() as td:
            wd=Path(td)
            plan=wd/'plan.json'
            plan.write_text(json.dumps({'edition_date':'2026-10-25','slides':[
                {'layout':'cover','title':'Weekly IT News！','cover_teaser':'今週の検証'},
                {'layout':'agenda','title':'今週のトピック','bullets':['Meta Muse','PHP2Shell','GMO侵害']}
            ]},ensure_ascii=False),encoding='utf-8')
            pptx=wd/'deck.pptx'
            p=subprocess.run([sys.executable,str(script),str(plan),str(pptx)],capture_output=True,text=True)
            self.assertEqual(p.returncode,0,p.stderr)
            with ZipFile(pptx) as z:
                self.assertIsNone(z.testzip())
                slide1=ET.fromstring(z.read('ppt/slides/slide1.xml'))
                slide2=ET.fromstring(z.read('ppt/slides/slide2.xml'))
                head=''.join(slide1.itertext())
                agenda=''.join(slide2.itertext())
                self.assertIn('2026年',head)
                self.assertIn('10月',head)
                self.assertIn('25',head)
                self.assertIn('今週の検証',head)
                self.assertIn('今週のトピック',agenda)
                for title in ('Meta Muse','PHP2Shell','GMO侵害'):
                    self.assertIn(title,agenda)
                pics=[x for x in z.namelist() if x.startswith('ppt/media/')]
                self.assertEqual(len(pics),1)
                self.assertEqual(z.read(pics[0]),AVATAR.read_bytes())
                self.assertNotIn('今週の検証',agenda)

    def test_cover_avatar_is_not_counted_as_documentary_evidence(self):
        script=ROOT/'skills'/'weekly-it-news'/'scripts'/'build_pptx.py'
        with TemporaryDirectory() as td:
            wd=Path(td)
            plan=wd/'plan.json'
            plan.write_text(json.dumps({'edition_date':'2026-10-25','min_evidence_images':1,
                'slides':[{'layout':'cover','title':'Weekly IT News！','teaser':'検証'}]},ensure_ascii=False),encoding='utf-8')
            p=subprocess.run([sys.executable,str(script),str(plan),str(wd/'out.pptx')],capture_output=True,text=True)
            self.assertNotEqual(p.returncode,0)
            self.assertIn('Image requirement unmet',p.stderr)

    def test_packages_ship_all_cover_resources(self):
        spec=importlib.util.spec_from_file_location('build_packages',ROOT/'scripts'/'build_packages.py')
        m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
        with TemporaryDirectory() as tmp:
            archives=m.build(Path(tmp))
            for i,zfile in enumerate(archives):
                prefix='assets/cover/' if i else 'skills/weekly-it-news/assets/cover/'
                with ZipFile(zfile) as z:
                    for filename in ('avatar-20260315.jpg','weekly-it-news-cover-20260315.pptx','cover-preview-20260315.jpg','README.md'):
                        self.assertIn(prefix+filename,z.namelist())
                    self.assertEqual(z.read(prefix+'avatar-20260315.jpg'),AVATAR.read_bytes())
                if i==0:
                    with ZipFile(zfile) as z:
                        self.assertIn('skills/itnews-powerpoint-polish/assets/cover/avatar-20260315.jpg',z.namelist())

if __name__=='__main__':unittest.main()