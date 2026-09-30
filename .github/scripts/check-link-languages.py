#!/usr/bin/env python3
"""Audit public link language coverage against recorded evidence, without networking."""
import argparse
import html
import json
import re
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[2]
AUDIT = '.github/agents/link-language-audit.json'


def links(text):
    """Yield inline HTML/Markdown links with offsets, including balanced URL parentheses."""
    found = []
    for m in re.finditer(r'<a\b([^>]*?)>(.*?)</a>', text, re.S | re.I):
        attrs = dict(re.findall(r'([\w-]+)="([^"]*)"', m[1]))
        if 'href' in attrs:
            found.append(dict(start=m.start(), end=m.end(), kind='html', url=html.unescape(attrs['href']), label=m[2], attrs=attrs))
    for m in re.finditer(r'(?<!!)\[([^\]\n]+)\]\(', text):
        if any(x['start'] <= m.start() < x['end'] for x in found):
            continue
        pos, depth = m.end(), 1
        while pos < len(text) and depth:
            if text[pos] == '\\':
                pos += 2
                continue
            depth += (text[pos] == '(') - (text[pos] == ')')
            pos += 1
        if depth:
            continue
        raw = text[m.end():pos - 1]
        dest = re.fullmatch(r'(<[^>]*>|\S+?)(?:\s+"([^"]*)")?', raw)
        if dest:
            found.append(dict(start=m.start(), end=pos, kind='markdown', url=html.unescape(dest[1].strip('<>')), label=m[1], attrs={'title': dest[2]} if dest[2] else {}))
    return sorted(found, key=lambda x: x['start'])


def check(root=ROOT):
    audit = json.loads((root / AUDIT).read_text())
    evidence = {x['url']: x for x in audit['resources']}
    counts = {'links': 0, 'tagged': 0, 'documented_unresolved': 0, 'non_document': 0}
    errors = []
    for filename in audit['pages']:
        for link in links((root / filename).read_text()):
            counts['links'] += 1
            url, tag = link['url'], link['attrs'].get('hreflang')
            if urlsplit(url).scheme in ('mailto', 'tel'):
                counts['non_document'] += 1
                if tag:
                    errors.append(f'{filename}: language on non-document action {url}')
                continue
            record = evidence.get(url)
            if record is None:
                errors.append(f'{filename}: link needs language audit: {url}')
                continue
            expected = record['language']
            if expected:
                if tag != expected:
                    errors.append(f'{filename}: expected hreflang={expected}: {url}')
                else:
                    counts['tagged'] += 1
            else:
                counts['documented_unresolved'] += 1
                if tag or not record.get('reason'):
                    errors.append(f'{filename}: unsupported language/missing explanation: {url}')
            if tag and not re.fullmatch(r'[A-Za-z]{2,8}(?:-[A-Za-z0-9]{1,8})*', tag):
                errors.append(f'{filename}: malformed language tag {tag}')
    if errors:
        raise ValueError('\n'.join(errors))
    return counts


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    args = parser.parse_args()
    print('PASS:', check(args.root))
