"""Coverage regressions: balanced destinations, non-document links and unknowns."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('audit', Path(__file__).with_name('check-link-languages.py'))
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


class LinkLanguageChecks(unittest.TestCase):
    def test_nested_parentheses_and_query_entities_preserved(self):
        src = '[Law](https://example.org/law_(2026)#part(1)) <a href="https://example.org/?a=1&amp;b=2" lang="de" hreflang="en">Name</a>'
        found = audit.links(src)
        self.assertEqual(found[0]['url'], 'https://example.org/law_(2026)#part(1)')
        self.assertEqual(found[1]['url'], 'https://example.org/?a=1&b=2')
        self.assertEqual(found[1]['attrs']['lang'], 'de')

    def test_unresolved_is_explicit_and_new_links_fail(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / '.github/agents').mkdir(parents=True)
            (root / audit.AUDIT).write_text(json.dumps({'pages': ['p.md'], 'resources': [{'url': 'https://example.org/', 'language': None, 'reason': 'Access failed'}]}))
            page = root / 'p.md'
            page.write_text('[Unresolved](https://example.org/) [Email](mailto:a@example.org)')
            self.assertEqual(audit.check(root)['documented_unresolved'], 1)
            page.write_text('<a href="https://example.org/" hreflang="en">Unsupported</a>')
            with self.assertRaises(ValueError): audit.check(root)
            page.write_text('[New](https://new.example.org/)')
            with self.assertRaises(ValueError): audit.check(root)


if __name__ == '__main__':
    unittest.main()
