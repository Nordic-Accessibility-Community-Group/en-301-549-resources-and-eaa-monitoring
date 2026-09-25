"""Enforcement record consistency, not legal or linguistic verification (stdlib only)."""
import argparse
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
import country_records
from collections import Counter
from datetime import date
import hashlib
import json
import re
from urllib.parse import urlparse

REGISTRY = json.loads((Path(__file__).resolve().parents[1] / 'registry.json').read_text())
EU = [j['name'] for j in REGISTRY['jurisdictions'] if j['group'] == 'EU']
SECTORS = REGISTRY['sectors']
SOURCE_TYPES = ['official_law', 'official_authority_publication', 'official_court_decision', 'european_commission_publication', 'external_legal_analysis', 'external_party_statement', 'external_news_report', 'contributor_correspondence', 'other_unverified']
SOURCE_TYPES.append('official_authority_correspondence')
STAGES = ['announced_monitoring', 'ongoing_monitoring', 'complaint_lodged', 'investigation', 'warning', 'order_issued', 'conditional_penalty', 'penalty_imposed', 'appeal_pending', 'final_judgment', 'closed', 'unknown']
PAGE = 'EAA enforcement tracking.md'
# Frozen setup map; changes require explicit baseline migration review.
BASELINE_SHA256 = '2ece63c50c290efb0da2e301f45a177176d39376a8da519953037aca0242daeb'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def fields(value, template, label):
    require(isinstance(value, dict), label + ': expected object')
    require(set(value) == set(template), label + ': unexpected or missing fields')
    for key, expected in template.items():
        if expected is not None:
            require(type(value[key]) is type(expected), label + ': wrong type for ' + key)


def checked_date(value, label):
    if value is not None:
        require(isinstance(value, str) and bool(re.fullmatch(r'\d{4}-\d{2}-\d{2}', value)), label + ': ISO date required')
        require(date.fromisoformat(value) <= date.today(), label + ': future observation date')


def digest(text):
    return hashlib.sha256(text.encode()).hexdigest()


def public_rows(page):
    """Extract current raw-HTML data rows without imposing a new public layout."""
    result = []
    for section in re.split(r'(?m)^## ', page)[1:]:
        heading = section.splitlines()[0].strip()
        for match in re.finditer(r'<tr\b[^>]*>.*?</tr>', section, re.S | re.I):
            row = match.group()
            if re.search(r'<td\b', row, re.I):
                result.append((heading, row))
    return result


def check(root):
    folder = root / '.github/agents/enforcement'
    read = lambda name: json.loads((folder / name).read_text())
    template = read('record-template.json')
    claim_template = read('claim-template.json')
    source_template = claim_template['sources'][0]
    current_map = read('public-map.json')
    baseline = read('baseline-map.json')
    require(hashlib.sha256((folder / 'baseline-map.json').read_bytes()).hexdigest() == BASELINE_SHA256, 'Frozen baseline-map changed; do not rehash inherited changes')
    require(current_map['schema_version'] == baseline['schema_version'] == 1, 'Map version')
    page = (root / PAGE).read_text()
    actual = Counter((heading, digest(row)) for heading, row in public_rows(page))
    mapped = Counter((entry['section'], entry['row_sha256']) for entry in current_map['entries'])
    require(actual == mapped, 'Public rows changed or missing from public-map.json; review and map each row')
    ids = [entry['id'] for entry in current_map['entries']]
    require(len(ids) == len(set(ids)), 'Duplicate public entry ID')
    baseline_ids = {entry['id']: entry for entry in baseline['entries']}
    records = {}
    claims = {}
    for path, record in country_records.records(root, 'enforcement'):
        name = record.get('country', path.stem)
        fields(record, template, name)
        require(record['schema_version'] == 1, name + ': schema version')
        require(path.stem == name.lower(), name + ': filename mismatch')
        require(name not in records, 'Duplicate country: ' + name)
        records[name] = record
        require(record['jurisdiction_group'] in ['EU', 'EU territory', 'non-EU'], name + ': jurisdiction group')
        require((name in EU) == (record['jurisdiction_group'] == 'EU'), name + ': EU membership mismatch')
        require((name == 'Åland') == (record['jurisdiction_group'] == 'EU territory'), name + ': EU territory mismatch')
        require(record['research_state'] in ['not_yet_researched', 'partially_researched', 'bounded_pass_completed'], name + ': research state')
        require(record['search_result'] in ['not_assessed', 'reportable_activity_found', 'no_reportable_activity_found_in_checked_sources'], name + ': search result')
        for key in ['created_on', 'attempted_on', 'verified_on']:
            checked_date(record[key], name + '.' + key)
        require(record['created_on'] is not None, name + ': creation date missing')
        require(all(isinstance(note, str) and note.strip() for note in record['knowledge_notes']), name + ': knowledge notes')
        require(all(isinstance(ref, str) for ref in record['public_entry_ids']), name + ': public references')
        require(len(record['public_entry_ids']) == len(set(record['public_entry_ids'])), name + ': duplicate public references')
        if record['research_state'] == 'not_yet_researched':
            require(record['attempted_on'] is None and record['verified_on'] is None and not record['attempts'] and not record['claims'], name + ': unresearched record has research results')
            require(record['search_result'] == 'not_assessed', name + ': unresearched result')
        else:
            require(record['attempts'] and record['attempted_on'], name + ': research requires attempt history')
        for attempt in record['attempts']:
            fields(attempt, {'attempted_on': '', 'scope': '', 'sources_checked': [], 'limitations': '', 'next_check': ''}, name + ': attempt')
            checked_date(attempt['attempted_on'], name + ': attempt date')
            require(attempt['scope'].strip() and attempt['limitations'].strip(), name + ': attempt scope and limits required')
            require(all(isinstance(url, str) and urlparse(url).scheme in ['http', 'https'] and urlparse(url).netloc for url in attempt['sources_checked']), name + ': attempt source URLs')
        if record['attempts']:
            require(record['attempted_on'] == max(a['attempted_on'] for a in record['attempts']), name + ': latest attempt date mismatch')
        if record['search_result'] == 'no_reportable_activity_found_in_checked_sources':
            require(record['research_state'] == 'bounded_pass_completed' and any(a['sources_checked'] for a in record['attempts']), name + ': no-findings result requires completed scoped source check')
        for question in record['questions']:
            fields(question, {'priority': '', 'question': '', 'owner': '', 'resolved_when': ''}, name + ': question')
            require(question['priority'] in ['Before PR', 'Before merge', 'Follow-up'], name + ': question priority')
            require(all(question[key].strip() for key in ['question', 'owner', 'resolved_when']), name + ': incomplete question')
        for claim in record['claims']:
            fields(claim, claim_template, name + ': claim')
            cid = claim['id']
            require(bool(re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', cid)), 'Invalid claim ID')
            require(cid not in claims, 'Duplicate claim ID: ' + cid)
            claims[cid] = (name, claim)
            require(claim['kind'] in ['case', 'monitoring_activity', 'statistics', 'commission_proceeding'], cid + ': kind')
            require(claim['status'] in ['verified', 'disputed', 'unknown', 'unverified_source'], cid + ': evidence status')
            require(claim['procedural_stage'] in STAGES, cid + ': stage')
            require(all(sector in SECTORS for sector in claim['sectors']), cid + ': sector')
            require(claim['sectors'] == sorted(set(claim['sectors']), key=SECTORS.index), cid + ': sector order/duplicates')
            require(claim['applicability'] in ['EAA', 'other_law', 'unknown'], cid + ': applicability')
            for key in ['event_on', 'published_on', 'verified_on']:
                checked_date(claim[key], cid + '.' + key)
            require(isinstance(claim['case_identifier'], (str, type(None))), cid + ': case identifier')
            for source in claim['sources']:
                fields({k: v for k, v in source.items() if k != 'correspondence_review'}, source_template, cid + ': source')
                require(source['source_type'] in SOURCE_TYPES, cid + ': source type')
                if source['source_type'] == 'official_authority_correspondence':
                    review = source.get('correspondence_review')
                    fields(review, {'authority': '', 'source_date': '', 'document_sha256': '', 'reviewed_by': '', 'reviewed_on': '', 'scope_limit': ''}, cid + ': correspondence review')
                    require(all(review.values()), cid + ': incomplete correspondence review')
                    checked_date(review['source_date'], cid + ': correspondence date')
                    checked_date(review['reviewed_on'], cid + ': correspondence review date')
                    require(review['source_date'] <= review['reviewed_on'], cid + ': correspondence chronology')
                    require(bool(re.fullmatch(r'[a-f0-9]{64}', review['document_sha256'])), cid + ': correspondence digest')
                    require(source['provenance_note'].strip(), cid + ': correspondence provenance')
                    require(source['retrieved_on'] is not None and source['retrieved_on'] <= review['reviewed_on'], cid + ': correspondence must be read before review')
                    if claim['status'] == 'verified':
                        require(claim['verified_on'] is not None and review['reviewed_on'] <= claim['verified_on'], cid + ': verification predates correspondence review')
                else:
                    require('correspondence_review' not in source, cid + ': review metadata only for official correspondence')
                require(source['access_result'] in ['not_attempted', 'reachable', 'unreachable', 'unknown'], cid + ': access result')
                for key in ['attempted_on', 'retrieved_on']:
                    checked_date(source[key], cid + '.' + key)
                if source['url'] is not None:
                    require(isinstance(source['url'], str) and urlparse(source['url']).scheme in ['http', 'https'] and urlparse(source['url']).netloc, cid + ': source URL')
                else:
                    require(source['source_type'] in ['contributor_correspondence', 'official_authority_correspondence'] and source['reference'].strip(), cid + ': source needs URL or correspondence reference')
                if source['access_result'] == 'not_attempted':
                    require(source['attempted_on'] is None and source['retrieved_on'] is None, cid + ': unattempted source has dates')
                else:
                    require(source['attempted_on'] is not None, cid + ': attempted source lacks date')
                if source['retrieved_on'] is not None:
                    require(source['access_result'] == 'reachable' and source['attempted_on'] is not None and source['retrieved_on'] <= source['attempted_on'], cid + ': invalid retrieval date')
            if claim['status'] == 'verified':
                require(claim['verified_on'] is not None and claim['text'].strip() and claim['authority_or_court'].strip() and claim['legal_basis'].strip(), cid + ': verified claim lacks details')
                require(any(s['source_type'] in SOURCE_TYPES[:4] + ['official_authority_correspondence'] and s['passage'].strip() and s['reference'].strip() and s['retrieved_on'] and s['retrieved_on'] <= claim['verified_on'] for s in claim['sources']), cid + ': verified claim requires retrieved primary passage')
            else:
                require(claim['verified_on'] is None, cid + ': unverified claim has verification date')
            if claim['kind'] == 'statistics':
                fields(claim['statistics'], {'as_of': '', 'period': '', 'units': '', 'counting_basis': '', 'overlap_note': ''}, cid + ': statistics')
                checked_date(claim['statistics']['as_of'], cid + ': statistics date')
                require(all(claim['statistics'].values()), cid + ': incomplete statistics metadata')
            else:
                require(claim['statistics'] is None, cid + ': statistics only for aggregate claims')
        verified = [c['verified_on'] for c in record['claims'] if c['status'] == 'verified']
        require(record['verified_on'] == (max(verified) if verified else None), name + ': verification roll-up mismatch')
        if record['search_result'] == 'reportable_activity_found':
            require(verified, name + ': reportable finding requires verified claim')
    require(set(EU).issubset(records), 'Missing EU research records: ' + ', '.join(sorted(set(EU) - set(records))))
    require('Norway' in records, 'Preserve the existing Norway research record')
    for entry in current_map['entries']:
        require(entry['countries'] and len(entry['countries']) == len(set(entry['countries'])), entry['id'] + ': country mapping')
        require(all(name in records for name in entry['countries']), entry['id'] + ': missing country record')
        if entry['state'] == 'inherited_unreviewed':
            require(entry == baseline_ids.get(entry['id']), entry['id'] + ': inherited entry changed without review')
        else:
            require(entry['state'] == 'reviewed' and entry['claim_ids'], entry['id'] + ': new/changed public entry needs claims')
            for cid in entry['claim_ids']:
                require(cid in claims and claims[cid][0] in entry['countries'] and claims[cid][1]['status'] == 'verified', entry['id'] + ': unsupported public claim reference')
        for name in entry['countries']:
            require(entry['id'] in records[name]['public_entry_ids'], name + ': missing public back-reference')
    for name, record in records.items():
        expected = {e['id'] for e in current_map['entries'] if name in e['countries']}
        require(set(record['public_entry_ids']) == expected, name + ': stale public reference')
    return len(records), len(ids)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', nargs='?', type=Path, default=Path(__file__).resolve().parents[3])
    args = parser.parse_args()
    try:
        countries, entries = check(args.root)
    except (ValueError, KeyError, TypeError, OSError) as error:
        parser.exit(1, 'FAIL: ' + str(error) + '\n')
    print(f'PASS: {countries} research records; {entries} public entries mapped. No legal, language or live-source verification performed.')
