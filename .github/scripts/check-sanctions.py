#!/usr/bin/env python3
"""Check sanctions publication/record consistency; does not verify legal claims."""
from pathlib import Path
from html import unescape
from html.parser import HTMLParser
from datetime import date
import hashlib
import json
import re
import sys

COUNTRIES = 'Austria Belgium Bulgaria Croatia Cyprus Czechia Denmark Estonia Finland France Germany Greece Hungary Ireland Italy Latvia Lithuania Luxembourg Malta Netherlands Poland Portugal Romania Slovakia Slovenia Spain Sweden'.split()
AREAS = ['Products', 'E-commerce', 'Banking', 'Electronic communications', 'Transport', 'Audiovisual access', 'E-books', '112 emergency calls']

class BalancedHTML(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
    def handle_starttag(self, tag, attrs):
        self.stack.append(tag)
    def handle_endtag(self, tag):
        assert self.stack and self.stack.pop() == tag, 'Unbalanced HTML: ' + tag

def check(root):
    page = (root / 'EAA sanctions.md').read_text()
    folder = root / '.github/agents/research/sanctions'
    tables = re.findall(r'<table>.*?</table>', page, re.S)
    assert len(tables) == 1, 'Expected one country table'
    parser = BalancedHTML()
    parser.feed(tables[0])
    assert not parser.stack, 'Unclosed HTML tags'
    assert len(re.findall(r'<th scope="col">', tables[0])) == 7, 'Expected seven column headers'
    rows = re.findall(r'<tr>\s*<th scope="row".*?</tr>', tables[0], re.S)
    names = []
    for row in rows:
        slug, name = re.search(r'<th scope="row" id="([^"]+)">([^<]+)</th>', row).groups()
        names.append(name)
        assert slug == name.lower(), 'Country ID mismatch: ' + name
        cells = re.findall(r'<td>(.*?)</td>', row, re.S)
        assert len(cells) == 6, 'Wrong cell count: ' + name
        assert all(area in cells[0] for area in AREAS), 'Missing EAA area: ' + name
        match = re.fullmatch(r'<p>(\d{4}-\d{2}-\d{2})</p>', cells[5])
        assert match, 'Last checked must contain only a date: ' + name
        assert date.fromisoformat(match[1]) <= date.today(), 'Future review date: ' + name
        record = json.loads((folder / (slug + '.json')).read_text())
        assert record['country'] == name, 'Record country mismatch: ' + name
        assert record['last_checked'] == match[1], 'Record date mismatch: ' + name
        assert record['review_note'].strip(), 'Missing retained review note: ' + name
        urls = {unescape(url) for url in re.findall(r'href="([^"]+)"', cells[4])}
        assert urls and all(url.startswith('https://') for url in urls), 'Invalid source URL: ' + name
        assert urls == {source['url'] for source in record['sources']}, 'Source mismatch: ' + name
        assert record['public_row_sha256'] == hashlib.sha256(row.encode()).hexdigest(), 'Record/public row out of sync: ' + name
    assert names == COUNTRIES, 'Countries must appear once each in alphabetical order'
    assert page.index('## Reading the table') > page.index('</table>'), 'Reading guide must follow table'
    for target in re.findall(r'\]\(([^)]+)\)', page):
        if not re.match(r'\w+://', target):
            from urllib.parse import unquote
            assert (root / unquote(target.split('#')[0])).exists(), 'Broken local link: ' + target
    return len(rows)

if __name__ == '__main__':
    try:
        root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[2]
        count = check(root)
    except (AssertionError, KeyError, ValueError, OSError, IndexError) as exc:
        print('FAIL: ' + str(exc), file=sys.stderr)
        sys.exit(1)
    print(f'PASS: {count} countries; table, dates, source links and record fingerprints agree. Legal claims not checked.')
