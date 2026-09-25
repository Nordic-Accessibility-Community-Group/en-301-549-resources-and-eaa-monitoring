"""Regression tests for publication/research boundaries; no external evidence checks."""
import copy
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location('enforcement_check', HERE / 'check.py')
CHECK = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECK)


class RecordChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.folder = self.root / '.github/agents/enforcement'
        self.folder.mkdir(parents=True)
        (self.folder / 'research').mkdir()
        for filename in ['record-template.json', 'claim-template.json']:
            shutil.copy2(HERE / filename, self.folder / filename)
        section = 'Fixture enforcement section'
        definitions = [
            ('austria-1', ['Austria'], '<tr><td>Austria</td><td>Actively testing.</td></tr>'),
            ('commission-1', ['Croatia', 'Germany'], '<tr><td>Croatia and Germany</td><td>Fixture Commission entry</td></tr>'),
            ('norway-1', ['Norway'], '<tr><td>Norway</td><td>Fixture entry</td></tr>'),
        ]
        page = '# Fixture\n\n## ' + section + '\n<table>\n' + '\n'.join(row for _, _, row in definitions) + '\n</table>\n'
        (self.root / CHECK.PAGE).write_text(page)
        entries = [{'id': eid, 'countries': countries, 'section': section, 'row_sha256': CHECK.digest(row), 'state': 'inherited_unreviewed', 'claim_ids': [], 'snapshot_url': 'https://example.org/fixture'} for eid, countries, row in definitions]
        mapping = {'schema_version': 1, 'baseline_commit': 'fixture', 'baseline_page_sha256': CHECK.digest(page), 'entries': entries}
        self.write('baseline-map.json', mapping)
        self.write('public-map.json', mapping)
        baseline_patch = patch.object(CHECK, 'BASELINE_SHA256', CHECK.digest((self.folder / 'baseline-map.json').read_text()))
        baseline_patch.start()
        self.addCleanup(baseline_patch.stop)
        for country in CHECK.EU + ['Norway']:
            record = self.read('record-template.json')
            record.update(country=country, jurisdiction_group='EU' if country in CHECK.EU else 'non-EU', public_entry_ids=[entry['id'] for entry in entries if country in entry['countries']])
            self.write('research/' + country.lower() + '.json', record)

    def read(self, path):
        return json.loads((self.folder / path).read_text())

    def write(self, path, value):
        (self.folder / path).write_text(json.dumps(value))

    def rejects(self, fragment):
        with self.assertRaisesRegex(ValueError, fragment):
            CHECK.check(self.root)

    def test_sparse_public_page_and_full_research_coverage(self):
        self.assertEqual(CHECK.check(self.root), (28, 3))
        self.assertEqual(self.read('research/belgium.json')['public_entry_ids'], [])

    def test_missing_eu_record_fails_even_without_public_entry(self):
        (self.folder / 'research/belgium.json').unlink()
        self.rejects('Missing EU research')

    def test_public_change_cannot_keep_stale_mapping(self):
        page = self.root / CHECK.PAGE
        page.write_text(page.read_text().replace('Actively testing.', 'All companies fined.'))
        self.rejects('Public rows changed')

    def test_rehash_does_not_verify_inherited_entry(self):
        page = self.root / CHECK.PAGE
        page.write_text(page.read_text().replace('Actively testing.', 'All companies fined.'))
        mapping = self.read('public-map.json')
        mapping['entries'][0]['row_sha256'] = CHECK.digest(CHECK.public_rows(page.read_text())[0][1])
        self.write('public-map.json', mapping)
        self.rejects('inherited entry changed')

    def test_rewriting_both_maps_cannot_bypass_inherited_review(self):
        page = self.root / CHECK.PAGE
        page.write_text(page.read_text().replace('Actively testing.', 'All companies fined.'))
        mapping = self.read('public-map.json')
        mapping['entries'][0]['row_sha256'] = CHECK.digest(CHECK.public_rows(page.read_text())[0][1])
        self.write('public-map.json', mapping)
        self.write('baseline-map.json', mapping)
        self.rejects('Frozen baseline-map changed')

    def test_duplicate_public_id_fails(self):
        mapping = self.read('public-map.json')
        mapping['entries'][1]['id'] = mapping['entries'][0]['id']
        self.write('public-map.json', mapping)
        self.rejects('Duplicate public entry')

    def test_setup_date_is_not_verification(self):
        record = self.read('research/belgium.json')
        record['verified_on'] = record['created_on']
        self.write('research/belgium.json', record)
        self.rejects('unresearched record has research results')

    def test_no_findings_requires_a_completed_scoped_check(self):
        record = self.read('research/belgium.json')
        record['search_result'] = 'no_reportable_activity_found_in_checked_sources'
        self.write('research/belgium.json', record)
        self.rejects('unresearched result')

    def researched_record(self):
        record = self.read('research/belgium.json')
        record.update(research_state='partially_researched', attempted_on='2026-09-25')
        record['attempts'] = [{'attempted_on': '2026-09-25', 'scope': 'Synthetic test only', 'sources_checked': ['https://example.org/decision'], 'limitations': 'Fixture, not evidence', 'next_check': 'None'}]
        claim = copy.deepcopy(self.read('claim-template.json'))
        claim.update(id='belgium-test', text='Fixture claim', authority_or_court='Fixture authority', legal_basis='Fixture law')
        claim['sources'][0].update(url='https://example.org/decision', reference='Fixture section', passage='Fixture passage', source_type='official_authority_publication')
        record['claims'] = [claim]
        return record, claim

    def test_partial_attempt_with_unknown_claim_is_valid(self):
        record, claim = self.researched_record()
        self.write('research/belgium.json', record)
        self.assertEqual(CHECK.check(self.root), (28, 3))

    def test_official_url_alone_cannot_verify(self):
        record, claim = self.researched_record()
        claim.update(status='verified', verified_on='2026-09-25')
        record['verified_on'] = '2026-09-25'
        self.write('research/belgium.json', record)
        self.rejects('retrieved primary passage')

    def test_verified_case_can_add_public_entry_without_other_countries(self):
        record, claim = self.researched_record()
        claim.update(status='verified', verified_on='2026-09-25')
        claim['sources'][0].update(attempted_on='2026-09-25', retrieved_on='2026-09-25', access_result='reachable')
        record.update(verified_on='2026-09-25', search_result='reportable_activity_found', public_entry_ids=['belgium-1'])
        self.write('research/belgium.json', record)
        page = self.root / CHECK.PAGE
        row = '<tr><td>Belgium</td><td>Fixture claim</td></tr>'
        page.write_text(page.read_text().replace('</table>', row + '\n</table>', 1))
        mapping = self.read('public-map.json')
        entry = copy.deepcopy(mapping['entries'][0])
        entry.update(id='belgium-1', countries=['Belgium'], row_sha256=CHECK.digest(row), state='reviewed', claim_ids=['belgium-test'])
        mapping['entries'].append(entry)
        self.write('public-map.json', mapping)
        self.assertEqual(CHECK.check(self.root), (28, 4))

    def test_bounded_no_findings_does_not_add_a_public_entry(self):
        record, claim = self.researched_record()
        record.update(research_state='bounded_pass_completed', search_result='no_reportable_activity_found_in_checked_sources', claims=[])
        self.write('research/belgium.json', record)
        self.assertEqual(CHECK.check(self.root), (28, 3))

    def test_failed_retrieval_cannot_have_retrieved_date(self):
        record, claim = self.researched_record()
        claim['sources'][0].update(attempted_on='2026-09-25', retrieved_on='2026-09-25', access_result='unreachable')
        self.write('research/belgium.json', record)
        self.rejects('invalid retrieval date')

    def test_secondary_source_cannot_verify(self):
        record, claim = self.researched_record()
        claim.update(status='verified', verified_on='2026-09-25')
        claim['sources'][0].update(source_type='external_news_report', attempted_on='2026-09-25', retrieved_on='2026-09-25', access_result='reachable')
        record['verified_on'] = '2026-09-25'
        self.write('research/belgium.json', record)
        self.rejects('retrieved primary passage')

    def test_noncanonical_sector_order_fails(self):
        record, claim = self.researched_record()
        claim['sectors'] = ['Banking', 'Products']
        self.write('research/belgium.json', record)
        self.rejects('sector order')

    def test_statistics_need_counting_basis(self):
        record, claim = self.researched_record()
        claim['kind'] = 'statistics'
        claim['statistics'] = {'as_of': '2026-09-25', 'period': 'Fixture', 'units': 'Complaints', 'counting_basis': '', 'overlap_note': 'Unknown'}
        self.write('research/belgium.json', record)
        self.rejects('incomplete statistics')

    def test_commission_entry_is_shared_not_duplicated(self):
        mapping = self.read('public-map.json')
        shared = [e for e in mapping['entries'] if e['id'].startswith('commission-')]
        self.assertEqual(len(shared), 1)
        for country in ['croatia', 'germany']:
            self.assertIn(shared[0]['id'], self.read('research/' + country + '.json')['public_entry_ids'])

    def test_missing_country_back_reference_fails(self):
        record = self.read('research/croatia.json')
        record['public_entry_ids'] = []
        self.write('research/croatia.json', record)
        self.rejects('missing public back-reference')

    def test_new_public_country_requires_verified_claims(self):
        page = self.root / CHECK.PAGE
        row = '<tr><td>Belgium</td><td>Placeholder</td></tr>'
        page.write_text(page.read_text().replace('</table>', row + '\n</table>', 1))
        mapping = self.read('public-map.json')
        entry = copy.deepcopy(mapping['entries'][0])
        entry.update(id='belgium-1', countries=['Belgium'], row_sha256=CHECK.digest(row), state='reviewed', claim_ids=[])
        mapping['entries'].append(entry)
        self.write('public-map.json', mapping)
        self.rejects('new/changed public entry needs claims')


if __name__ == '__main__':
    unittest.main()
