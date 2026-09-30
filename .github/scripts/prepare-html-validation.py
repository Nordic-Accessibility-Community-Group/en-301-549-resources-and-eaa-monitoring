#!/usr/bin/env python3
"""Apply the GitHub table-alignment exception to a temporary validation copy.

This is repository policy, not a claim that legacy attributes conform to HTML5.
Only align="left" and valign="top" on th/td are exempt. Other values, elements,
duplicate attributes and all other markup remain available to HTML Tidy.
"""
import re
import sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path

# Tokenize complete attributes so alignment-like text inside another quoted
# attribute cannot be mistaken for an attribute of its own.
ATTRIBUTE = re.compile(r"""\s+([^\s=/>]+)(?:\s*=\s*(?:"[^"]*"|'[^']*'|[^\s>]+))?""")
APPROVED = {"align": "left", "valign": "top"}


class AlignmentException(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=False)
        # HTMLParser advances line numbers on LF only.
        self.offsets = [0] + [match.end() for match in re.finditer("\n", source)]
        self.edits = []

    def handle_starttag(self, tag, attrs):
        if tag not in {"th", "td"}:
            return
        counts = Counter(name for name, _ in attrs)
        raw = self.get_starttag_text()
        line, column = self.getpos()
        offset = self.offsets[line - 1] + column
        # Refuse malformed spacing/syntax instead of accidentally repairing it.
        position = re.match(r"<[^\s/>]+", raw).end()
        tokens = []
        while not re.fullmatch(r"\s*/?>", raw[position:]):
            token = ATTRIBUTE.match(raw, position)
            if token is None:
                return
            tokens.append(token)
            position = token.end()
        for match in tokens:
            name = match.group(1).lower()
            if name not in APPROVED or counts[name] != 1:
                continue
            # Deliberately accept only the exact double-quoted syntax we emit.
            if match.group(0).strip() == f'{name}="{APPROVED[name]}"':
                self.edits.append((offset + match.start(), offset + match.end()))

    handle_startendtag = handle_starttag


def prepare(source):
    parser = AlignmentException(source)
    parser.feed(source)
    parser.close()
    for start, end in reversed(parser.edits):
        # Preserve line/column positions for Tidy diagnostics.
        source = source[:start] + re.sub(r"[^\r\n]", " ", source[start:end]) + source[end:]
    return source, len(parser.edits)


if __name__ == "__main__":
    path = Path(sys.argv[1])
    source, count = prepare(path.read_text(encoding="utf-8"))
    path.write_text(source, encoding="utf-8")
    print(f"HTML validation exception: {count} approved table alignment attributes (temporary copy only).")
