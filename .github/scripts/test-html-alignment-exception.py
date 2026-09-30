#!/usr/bin/env python3
import importlib.util
import unittest
import os
import subprocess
import tempfile
from pathlib import Path

spec = importlib.util.spec_from_file_location("alignment", Path(__file__).with_name("prepare-html-validation.py"))
alignment = importlib.util.module_from_spec(spec)
spec.loader.exec_module(alignment)


class AlignmentTests(unittest.TestCase):
    def test_approved_cells(self):
        text = '<table><tr><th align="left" valign="top">Header</th><td align="left">Cell</td></tr></table>'
        result, count = alignment.prepare(text)
        self.assertEqual(count, 3)
        self.assertEqual(len(result), len(text))
        self.assertNotIn('align=', result)
        self.assertIn('Header</th>', result)

    def test_non_exempt_markup_preserved(self):
        for text in [
            '<th align="left"foo="bad">Text</th>',
            '<div align="left">Text</div>',
            '<th align="right" valign="middle">Text</th>',
            '<th align="left" align="right">Text</th>',
            "<th title='example align=\"left\"'>Text</th>",
            '<!-- <td align="left"> -->',
            "<script>const x = '<td align=\"left\">';</script>",
            '<th align="leftish">Text</th>',
        ]:
            with self.subTest(text=text):
                self.assertEqual(alignment.prepare(text), (text, 0))

    def test_unicode_separators_preserve_offsets(self):
        for separator in ["\u2028", "\u2029", "\r", "\v", "\f"]:
            text = '<p>one' + separator + 'two</p>\n<table><tr><td align="left">Cell</td></tr></table>'
            with self.subTest(separator=separator):
                result, count = alignment.prepare(text)
                self.assertEqual(count, 1)
                self.assertEqual(result, text.replace(' align="left"', ' ' * len(' align="left"')))

    def test_other_errors_remain(self):
        text = '<table>\n<tr><th align="left" bogus="bad"><unknown>text</table>'
        result, count = alignment.prepare(text)
        self.assertEqual(count, 1)
        self.assertIn('bogus="bad"><unknown>text</table>', result)
        self.assertEqual(result.count('\n'), text.count('\n'))


@unittest.skipUnless(os.environ.get("HTML5_TIDY"), "Set HTML5_TIDY to run real-validator tests")
class TidyIntegrationTests(unittest.TestCase):
    def validate(self, content):
        document = '<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Test</title></head><body>' + content + '</body></html>'
        prepared, _ = alignment.prepare(document)
        with tempfile.NamedTemporaryFile(mode="w", suffix=".html") as f:
            f.write(prepared)
            f.flush()
            return subprocess.run([os.environ["HTML5_TIDY"], "-errors", "-quiet", "-utf8", f.name], capture_output=True).returncode

    def test_approved_alignment_passes(self):
        self.assertEqual(self.validate('<table><tr><th align="left" valign="top">Header</th><td align="left" valign="top">Value</td></tr></table>'), 0)

    def test_unrelated_failures_are_not_suppressed(self):
        for content in [
            '<table><tr><th align="right">Header</th></tr></table>',
            '<div align="left">Text</div>',
            '<table><tr><th align="left" bogus="bad">Header</th></tr></table>',
            '<table><tr><th align="left" align="left">Header</th></tr></table>',
            '<table><tr><th align="left"><unknown>Header</unknown></th></tr></table>',
        ]:
            with self.subTest(content=content):
                self.assertNotEqual(self.validate(content), 0)


if __name__ == "__main__":
    unittest.main()
