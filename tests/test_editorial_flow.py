"""v0.5 field-test regressions: topic order and evidence handoff are behavioral rules."""
import copy
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from tempfile import TemporaryDirectory
import json
import unittest

ROOT=Path(__file__).resolve().parents[1]
CODE=ROOT/'skills'/'weekly-it-news'/'scripts'/'check_editorial_flow.py'
EXAMPLE=ROOT/'skills'/'weekly-it-news'/'templates'/'editorial-storyboard.example.json'
spec=spec_from_file_location('flow_validator',CODE)
validator=module_from_spec(spec);spec.loader.exec_module(validator)

class FlowTests(unittest.TestCase):
    def setUp(self):
        self.plan=json.loads(EXAMPLE.read_text('utf-8'))

    def test_base_handoff_accepts_explicit_pending_media_without_fake_urls(self):
        self.assertEqual(validator.validate_plan(self.plan), [])
        self.assertGreater(sum(s.get('asset_status')=='pending' for s in self.plan['slides']), 0)

    def test_real_v05_round_robin_topic_blocks_are_rejected(self):
        slides=[{'role':'cover'},{'role':'agenda'}]
        for topic in ['meta','php','gmo']:
            slides.append({'role':'explanation','topic_id':topic,'title':topic})
        for topic in ['meta','php','gmo']:
            slides.append({'role':'analysis','topic_id':topic,'title':'followup'})
        plan={'agenda_topic_ids':['meta','php','gmo'],'slides':slides}
        errs=validator.validate_plan(plan)
        self.assertTrue(any('reopened topic' in e for e in errs), errs)

    def test_news_evidence_must_have_actionable_handoff(self):
        plan=copy.deepcopy(self.plan)
        asset=next(s for s in plan['slides'] if s.get('role')=='evidence')
        del asset['source_gap'];del asset['intended_after'];del asset['rights_status']
        errs=validator.validate_plan(plan)
        self.assertTrue(any('source_gap' in e for e in errs))
        self.assertTrue(any('intended_after' in e for e in errs))
        self.assertTrue(any('rights_status' in e for e in errs))

    def test_final_requires_embedded_evidence(self):
        self.assertEqual(validator.validate_plan(self.plan),[])
        self.assertTrue(any('final requires' in s for s in validator.validate_plan(self.plan,final=True)))

    def test_correct_contiguous_order_has_no_false_quota(self):
        p=copy.deepcopy(self.plan)
        p['slides']=[s for s in p['slides'] if s.get('role')!='evidence']
        self.assertEqual(validator.validate_plan(p),[])

    def test_staged_plan_runs_in_offline_pptx_builder(self):
        from importlib.util import spec_from_file_location, module_from_spec
        builder_file=ROOT/'skills'/'weekly-it-news'/'scripts'/'build_pptx.py'
        spec=spec_from_file_location('itnews_base_builder',builder_file)
        builder=module_from_spec(spec);spec.loader.exec_module(builder)
        with TemporaryDirectory() as tmp:
            target=Path(tmp)/'story.pptx'
            slides, images=builder.build(EXAMPLE,target)
            self.assertEqual(slides,len(self.plan['slides']))
            self.assertEqual(images,0)  # explicit pending imagery is not fabricated
            import zipfile
            with zipfile.ZipFile(target) as archive:
                self.assertIsNone(archive.testzip())
                self.assertIn('ppt/slides/slide3.xml',archive.namelist())

    def test_package_references_present(self):
        author=(ROOT/'skills'/'weekly-it-news'/'SKILL.md').read_text('utf-8')
        polish=(ROOT/'skills'/'itnews-powerpoint-polish'/'SKILL.md').read_text('utf-8')
        self.assertIn('story-continuity.md',author)
        self.assertIn('check_editorial_flow.py',author)
        self.assertIn('topic-repair.md',polish)
        self.assertIn('reopened',polish)
        self.assertLess(len(author),20000)
        self.assertLess(len(polish),20000)

if __name__=='__main__': unittest.main()