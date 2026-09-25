"""Regression checks for sanctions consistency validation."""
from pathlib import Path
import importlib.util
import json
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('sanctions_check', Path(__file__).with_name('check-sanctions.py'))
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)

class SanctionsChecks(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        for name in ['EAA sanctions.md', 'EAA enforcement tracking.md', 'monitoring-agencies-information.md']:
            shutil.copy(ROOT / name, self.root / name)
        shutil.copytree(ROOT / '.github/agents/research/sanctions', self.root / '.github/agents/research/sanctions')
    def record(self, field, value):
        p = self.root / '.github/agents/research/sanctions/austria.json'
        data = json.loads(p.read_text())
        data[field] = value
        p.write_text(json.dumps(data))
    def test_valid_page(self):
        self.assertEqual(validator.check(self.root), 27)
    def test_mismatched_date(self):
        self.record('last_checked', '2020-01-01')
        with self.assertRaisesRegex(AssertionError, 'Record date mismatch'):
            validator.check(self.root)
    def test_missing_source(self):
        self.record('sources', [])
        with self.assertRaisesRegex(AssertionError, 'Source mismatch'):
            validator.check(self.root)
    def test_stale_record(self):
        self.record('public_row_sha256', 'stale')
        with self.assertRaisesRegex(AssertionError, 'out of sync'):
            validator.check(self.root)
    def test_research_note_in_date_cell(self):
        p = self.root / 'EAA sanctions.md'
        p.write_text(p.read_text().replace('<p>2026-09-25</p>', '<p>2026-09-25</p><p>Unfinished check</p>', 1))
        with self.assertRaisesRegex(AssertionError, 'only a date'):
            validator.check(self.root)

if __name__ == '__main__':
    unittest.main()
