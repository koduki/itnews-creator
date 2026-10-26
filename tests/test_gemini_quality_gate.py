"""Regression cases from Oct 26 field deck: cookie banners, anti-bot and story loops.

No claim is made that filename/hash checks recognize the content of PNG pixels.
Visual approval is a separately recorded step after opening the real image.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
GEN=ROOT/'skills/weekly-it-news-gemini/scripts/build_pptx.py'
TEMPLATE=ROOT/'assets/templates/weekly-it-news-design-template.pptx'
spec=importlib.util.spec_from_file_location('gemini_quality',GEN)
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def plot():
    return {'status':'approved','edition_date':'2026-10-26',
            'slides':[
                {'slide_id':'s01','story_id':'front','layout_id':'COVER','title':'Weekly IT News','on_slide':['News']},
                {'slide_id':'s02','story_id':'front','layout_id':'AGENDA','title':'今週のトピック','on_slide':['A']},
                {'slide_id':'s03','story_id':'a','layout_id':'SOURCE_IMAGE','title':'記事画面','asset_ids':['news1'],
                 'on_slide':['写真の役割','写真の説明']}],
            'assets':[{'id':'news1','file':'news1.png','source_url':'https://example.com/news',
                       'status':'captured','review_status':'approved',
                       'review_notes':'view_fileで記事見出しと本文を確認、遮蔽なし'}]}


class QualityGateTest(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.dir=Path(self.tmp.name)
        Image.new('RGB',(1280,853),'white').save(self.dir/'news1.png')

    def tearDown(self):self.tmp.cleanup()

    def test_reviewed_real_image_can_build_and_report(self):
        data=plot(); inp=self.dir/'plot.json'; inp.write_text(json.dumps(data,ensure_ascii=False))
        out=self.dir/'presentation.pptx';qa=self.dir/'qa.json'
        result=module.build_deck(TEMPLATE,inp,out,assets_dir=self.dir,
                                 strict_assets=True,qa_report_path=qa)
        self.assertTrue(out.is_file())
        self.assertEqual(result['preflight']['assets_inspected'],1)
        report=json.loads(qa.read_text())
        self.assertTrue(report['passed'])
        self.assertEqual(report['visual_qa'],'must manually inspect all slide previews; not auto-certified')

    def test_unreviewed_asset_blocks_even_if_png_exists(self):
        data=plot();data['assets'][0]['review_status']='pending'
        p=self.dir/'plot.json';p.write_text(json.dumps(data))
        out=self.dir/'deck.pptx';report=self.dir/'report.json'
        with self.assertRaisesRegex(ValueError,'no explicit visual approval'):
            module.build_deck(TEMPLATE,p,out,assets_dir=self.dir,strict_assets=True,qa_report_path=report)
        self.assertFalse(out.exists())
        self.assertFalse(json.loads(report.read_text())['passed'])

    def test_bot_and_cookie_flags_are_hard_errors(self):
        for flag in ('bot_challenge','cookie_overlay','ad_dominant','wrong_article'):
            data=plot();data['assets'][0]['quality_flags']=[flag]
            pre=module.preflight_plot(data,self.dir,strict_assets=True)
            self.assertFalse(pre['passed'])
            self.assertIn('rejected screenshot',str(pre['errors']))

    def test_missing_media_and_conflicting_source_block(self):
        data=plot();data['assets'][0]['file']='missing.png'
        # Intentionally no fallback file in separate directory.
        with tempfile.TemporaryDirectory() as empty:
            pre=module.preflight_plot(data,Path(empty),strict_assets=True)
            self.assertIn('missing file',str(pre['errors']))
        manifest=self.dir/'assets-manifest.json'
        manifest.write_text(json.dumps({'assets':[{'asset_id':'news1','source_url':'https://other.test'}]}))
        with self.assertRaisesRegex(ValueError,'source_url differs'):
            module.merge_asset_manifest(plot(),manifest)

    def test_signed_manifest_merges_approved_review(self):
        data=plot();data['assets'][0].pop('review_status')
        manifest=self.dir/'assets-manifest.json'
        manifest.write_text(json.dumps({'assets':[{'asset_id':'news1',
            'review_status':'approved','review_notes':'画像を開き記事本文を確認',
            'sha256':__import__('hashlib').sha256((self.dir/'news1.png').read_bytes()).hexdigest()}]}))
        merged=module.merge_asset_manifest(data,manifest)
        self.assertTrue(module.preflight_plot(merged,self.dir,True)['passed'])
        merged['assets'][0]['sha256']='0'*64
        self.assertIn('SHA-256 mismatch',str(module.preflight_plot(merged,self.dir,True)['errors']))

    def test_repeated_story_and_invalid_table_are_rejected(self):
        data=plot();data['slides'] += [
            {'slide_id':'s04','story_id':'b','layout_id':'NEWS','on_slide':['B']},
            {'slide_id':'s05','story_id':'a','layout_id':'NEWS','on_slide':['Back to A']},
            {'slide_id':'s06','story_id':'b','layout_id':'COMPARE',
             'table':{'headers':['比較','A','B'],'rows':[['missing column','x']]}}]
        pre=module.preflight_plot(data,self.dir,True)
        self.assertIn('reopens',str(pre['errors']))
        self.assertIn('invalid COMPARE',str(pre['errors']))

    def test_declared_image_missing_strict_mode_but_legacy_still_drafts(self):
        data=plot();data['slides'][2]['asset_ids']=[]
        self.assertFalse(module.preflight_plot(data,self.dir,True)['passed'])
        self.assertTrue(module.preflight_plot(data,self.dir,False)['passed'])


if __name__=='__main__':unittest.main()