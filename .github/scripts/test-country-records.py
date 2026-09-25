"""Migration and boundary regression tests using canonical country storage."""
import copy
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from jsonschema import ValidationError
import country_records as cr

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('country_check', Path(__file__).with_name('check-country-records.py'))
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)

class UnifiedRecords(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        shutil.copytree(ROOT / '.github', self.root / '.github')
        for p in ROOT.glob('*.md'):
            shutil.copy(p, self.root / p.name)
    def read(self, country):
        return json.loads((cr.folder(self.root) / (country.lower() + '.json')).read_text())
    def write(self, data):
        (cr.folder(self.root) / (data['country'].lower() + '.json')).write_text(json.dumps(data))
    def test_lossless_all_domains(self):
        self.assertEqual(checker.check(self.root, migration=True), (36, 651, 16))
    def test_missing_evidence_reference_rejected(self):
        d = self.read('Estonia')
        d['domains']['monitoring']['claims'][0]['source_refs'] = ['source-' + '0' * 24]
        self.write(d)
        with self.assertRaisesRegex(AssertionError, 'Missing evidence reference'):
            checker.check(self.root)
    def test_evidence_mutation_rejected(self):
        d = self.read('Estonia')
        next(iter(d['evidence'].values()))['unexpected'] = 'changed'
        self.write(d)
        with self.assertRaisesRegex(AssertionError, 'Evidence fingerprint'):
            checker.check(self.root)
    def test_duplicate_claim_id_rejected(self):
        d = self.read('Estonia')
        d['domains']['monitoring']['claims'][1]['id'] = d['domains']['monitoring']['claims'][0]['id']
        self.write(d)
        with self.assertRaisesRegex(AssertionError, 'Duplicate claim ID'):
            checker.check(self.root)
    def test_legacy_exception_does_not_cover_changed_claim(self):
        d = self.read('Greece')
        d['domains']['monitoring']['claims'][6]['assertion'] += ' Changed assertion.'
        self.write(d)
        with self.assertRaises(ValidationError):
            checker.check(self.root)
    def test_wrong_destination_domain_rejected(self):
        d = self.read('Estonia')
        d['deliveries'][0]['destinations'][0]['domain'] = 'sanctions'
        self.write(d)
        with self.assertRaisesRegex(AssertionError, 'Destination/domain'):
            checker.check(self.root)
    def test_stale_routing_projection_rejected(self):
        p = self.root / '.github/agents/evidence-routing/events.json'
        d = json.loads(p.read_text());d['events'].pop();p.write_text(json.dumps(d))
        with self.assertRaisesRegex(AssertionError, 'routing index is stale'):
            checker.check(self.root)
    def test_single_domain_edit_preserves_other_domains(self):
        d = self.read('Estonia');before = copy.deepcopy(d)
        view = cr.expand(d, 'enforcement');view['knowledge_notes'].append('Fixture note')
        cr.put_domain(d, 'enforcement', view)
        self.assertEqual(d['domains']['monitoring'], before['domains']['monitoring'])
        self.assertEqual(d['domains']['sanctions'], before['domains']['sanctions'])
        self.assertEqual(d['deliveries'], before['deliveries'])
    def test_same_url_different_passages_not_coalesced(self):
        d = self.read('Estonia');view = cr.expand(d, 'enforcement')
        source = copy.deepcopy(view['claims'][0]['sources'][0])
        source['passage'] += ' Distinct evidence.'
        view['claims'][0]['sources'].append(source)
        cr.put_domain(d, 'enforcement', view)
        refs = d['domains']['enforcement']['claims'][0]['source_refs']
        self.assertNotEqual(refs[0], refs[-1])
        self.assertEqual(cr.expand(d, 'enforcement'), view)

if __name__ == '__main__':
    unittest.main()
