"""Conservative handling of additive destination-language presentation metadata."""
import hashlib
import re


def additive_language_digest(row, original_hashes):
    """Retain a known hash only if removing added hreflang restores exact bytes.

    This does not excuse href, label, lang, other attribute or content changes,
    nor establish destination language. Separate audit evidence validates tags.
    """
    raw = hashlib.sha256(row.encode()).hexdigest()
    stripped = re.sub(r'(<a\b[^>]*?)\s+hreflang="[A-Za-z]{2,8}(?:-[A-Za-z0-9]{1,8})*"', r'\1', row)
    original = hashlib.sha256(stripped.encode()).hexdigest()
    return original if original in original_hashes else raw
