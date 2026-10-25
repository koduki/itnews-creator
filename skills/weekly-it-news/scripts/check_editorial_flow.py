#!/usr/bin/env python3
"""Validate planned Weekly IT News topic continuity and actionable visual handoff.

Standalone stdlib script. This validates a JSON *storyboard*, NOT the final slides,
image rights, correctness of claims, or URL authenticity. No external network.

Usage: python check_editorial_flow.py plan.json [--final]
"""
import argparse
import json
from pathlib import Path
from urllib.parse import urlparse

TOPIC_ROLES = {"explanation", "evidence", "analysis", "technical", "context"}
ROOT_ROLES = {"cover", "agenda", "summary"}
ASSET_STATES = {"embedded", "pending", "unavailable", "rights-unverified"}


def validate_plan(deck, final=False):
    errors = []
    slides = deck.get('slides', []) if isinstance(deck, dict) else []
    if not isinstance(slides, list) or not slides:
        return ['Plan must contain a nonempty slides list']
    agenda = deck.get('agenda_topic_ids')
    if agenda is not None and (not isinstance(agenda, list) or not all(isinstance(x, str) and x.strip() for x in agenda) or len(agenda) != len(set(agenda))):
        errors.append('agenda_topic_ids must be a list of unique nonblank IDs')
    begun, seen_closed, current, seen_explanations = [], set(), None, set()
    summary_started = False
    for number, slide in enumerate(slides, 1):
        label = 'slide ' + str(number)
        if not isinstance(slide, dict):
            errors.append(label + ': slide must be an object'); continue
        role, topic = slide.get('role'), slide.get('topic_id')
        if role in ROOT_ROLES:
            if role == 'summary': summary_started = True
            elif begun: errors.append(label + ': cover/agenda cannot interrupt news topics')
            continue
        if role not in TOPIC_ROLES:
            errors.append(label + ': unknown slide role ' + repr(role)); continue
        if not isinstance(topic, str) or not topic.strip():
            errors.append(label + ': topic_id is mandatory for news slides'); continue
        if summary_started: errors.append(label + ': cannot reopen topic after closing summary')
        if current != topic:
            if current is not None: seen_closed.add(current)
            if topic in seen_closed:
                errors.append(label + ': reopened topic ' + topic + ' after another topic; group all slides contiguously')
            else: begun.append(topic)
            current = topic
            if role != 'explanation':
                errors.append(label + ': each topic must start with an explanation slide')
        if role == 'explanation': seen_explanations.add(topic)
        if role == 'evidence':
            purpose=slide.get('evidence_purpose','')
            if not isinstance(purpose,str) or not purpose.strip():
                errors.append(label + ': evidence_purpose must say what image proves')
            status=slide.get('asset_status')
            if status not in ASSET_STATES:
                errors.append(label + ': asset_status must be embedded/pending/unavailable/rights-unverified')
            url=slide.get('source_url')
            gap=slide.get('source_gap')
            if url:
                if not isinstance(url,str) or urlparse(url).scheme not in ('http','https') or not urlparse(url).netloc:
                    errors.append(label + ': source_url must be a valid actual http(s) URL')
            elif not isinstance(gap,str) or not gap.strip():
                errors.append(label + ': no source_url; provide honest source_gap, never fabricate URL')
            if status == 'embedded' and not url:
                errors.append(label + ': embedded image requires source_url provenance')
            if not slide.get('intended_after'):
                errors.append(label + ': intended_after explanation slide is required for the polish handoff')
            if not slide.get('rights_status'):
                errors.append(label + ': rights_status required (may be unverified)')
            if final and status != 'embedded':
                errors.append(label + ': final requires authentic embedded evidence (unresolved ' + str(status) + ')')
    if agenda is not None and begun != agenda:
        errors.append('agenda_topic_ids order differs from actual contiguous topic order: agenda=' + repr(agenda) + '; slides=' + repr(begun))
    return errors


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('plan',type=Path)
    parser.add_argument('--final',action='store_true',help='Reject unembedded documentary evidence')
    options=parser.parse_args()
    try: deck=json.loads(options.plan.read_text('utf-8'))
    except (OSError,ValueError) as exc: parser.error(str(exc))
    errors=validate_plan(deck,final=options.final)
    if errors:
        for issue in errors: print('FAIL:',issue)
        raise SystemExit(1)
    print('PASS: storyboard topic-contiguous; evidence handoff fields present')


if __name__=='__main__': main()