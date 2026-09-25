"""Canonical country storage with lossless projections for domain validators.

Evidence objects are shared only when every recorded field is identical. They
are not merged merely because URLs match. Loading never changes verification.
"""
import copy
import hashlib
import json
from pathlib import Path

DOMAINS = ('monitoring', 'sanctions', 'enforcement')

def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))

def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()

def folder(root):
    return Path(root) / '.github/agents/research/countries'

def expand(country, domain):
    """Return the exact former domain record, not a second writable file."""
    pool = country['evidence']
    def unpack(value):
        if isinstance(value, list):
            return [unpack(v) for v in value]
        if not isinstance(value, dict):
            return value
        result = {k: unpack(v) for k, v in value.items() if k != 'source_refs'}
        if 'source_refs' in value:
            result['sources'] = [copy.deepcopy(pool[s]) for s in value['source_refs']]
        return result
    result = unpack(country['domains'][domain])
    result['country'] = country['country']
    if domain == 'monitoring':
        for claim in result['claims']:
            claim.pop('id')
    return result

def load(root, country, domain):
    return expand(json.loads((folder(root) / (country.lower() + '.json')).read_text()), domain)

def records(root, domain):
    for path in sorted(folder(root).glob('*.json')):
        data = json.loads(path.read_text())
        if domain in data['domains']:
            yield path, expand(data, domain)

def put_domain(country, domain, record):
    """Replace one domain in memory, retaining other domains and stable IDs."""
    assert domain in DOMAINS and record['country'] == country['country']
    pool = country['evidence']
    previous = country['domains'].get(domain, {})
    if domain == 'monitoring' and previous:
        raise ValueError('Edit existing monitoring claims canonically to preserve their IDs')
    old_ids = []
    def pack(value):
        if isinstance(value, list):
            return [pack(v) for v in value]
        if not isinstance(value, dict):
            return value
        result = {k: pack(v) for k, v in value.items() if k != 'sources'}
        if 'sources' in value:
            refs = []
            for source in value['sources']:
                sid = 'source-' + digest(source)[:24]
                assert sid not in pool or pool[sid] == source, 'Evidence ID collision'
                pool[sid] = copy.deepcopy(source)
                refs.append(sid)
            result['source_refs'] = refs
        return result
    data = pack(record)
    data.pop('country')
    if domain == 'monitoring':
        for i, claim in enumerate(data['claims']):
            claim['id'] = old_ids[i] if i < len(old_ids) else 'monitoring-' + digest([country['country'], i, record['claims'][i]])[:24]
    country['domains'][domain] = data
    return country

def save_domain(root, record, domain):
    """Used by fixtures and explicit migration tools; no network side effects."""
    path = folder(root) / (record['country'].lower() + '.json')
    if path.exists():
        country = json.loads(path.read_text())
    else:
        country = {'schema_version': 2, 'country': record['country'],
                   'jurisdiction_group': record.get('jurisdiction_group', 'EU'),
                   'evidence': {}, 'domains': {}, 'deliveries': []}
    put_domain(country, domain, record)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(country, ensure_ascii=False, indent=2) + '\n')

def routing_projection(root):
    events = []
    for path in sorted(folder(root).glob('*.json')):
        events.extend(json.loads(path.read_text())['deliveries'])
    return {'version': 1, 'events': events}

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('country')
    parser.add_argument('domain', choices=DOMAINS)
    args = parser.parse_args()
    print(json.dumps(load(Path(__file__).resolve().parents[2], args.country, args.domain), ensure_ascii=False, indent=2))
