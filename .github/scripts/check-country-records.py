"""Validate unified storage, stable references and domain-specific contracts."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
from jsonschema import Draft202012Validator, FormatChecker
import country_records as cr

def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def check(root, migration=False):
    agents = root / '.github/agents'
    registry = json.loads((agents / 'registry.json').read_text())
    groups = {j['name']: j['group'] for j in registry['jurisdictions']}
    validator = Draft202012Validator(json.loads((agents / 'research/country.schema.json').read_text()), format_checker=FormatChecker())
    monitor = Draft202012Validator(json.loads((agents / 'country-record.schema.json').read_text()), format_checker=FormatChecker())
    exception_bytes = (agents / 'research/legacy-schema-exceptions.json').read_bytes()
    assert hashlib.sha256(exception_bytes).hexdigest() == '170afe7f9ebf5cd1fbb633baeb9bbf7341fb776f967717ee457b6c1e1bfe1305', 'Frozen legacy exceptions changed'
    exceptions = json.loads(exception_bytes)['exceptions']
    names, ids, events = set(), set(), set()
    for path in sorted(cr.folder(root).glob('*.json')):
        country = json.loads(path.read_text())
        validator.validate(country)
        name = country['country']
        assert name not in names and path.stem == name.lower(), 'Duplicate or mismatched country'
        names.add(name)
        assert groups[name] == country['jurisdiction_group'], 'Jurisdiction classification mismatch'
        pool = country['evidence']
        for sid, source in pool.items():
            assert sid == 'source-' + cr.digest(source)[:24], 'Evidence fingerprint mismatch'
        def refs(value):
            if isinstance(value, dict):
                assert 'sources' not in value, 'Inline sources must use shared evidence references'
                if 'source_refs' in value:
                    assert isinstance(value['source_refs'], list) and all(isinstance(s, str) and s in pool for s in value['source_refs']), 'Missing evidence reference'
                for v in value.values(): refs(v)
            elif isinstance(value, list):
                for v in value: refs(v)
        refs(country['domains'])
        for domain, data in country['domains'].items():
            for claim in data.get('claims', []):
                assert claim['id'] not in ids, 'Duplicate claim ID'
                ids.add(claim['id'])
            if domain == 'monitoring':
                expanded = cr.expand(country, domain)
                for error in monitor.iter_errors(expanded):
                    path_parts = list(error.absolute_path)
                    allowed = False
                    if len(path_parts) >= 2 and path_parts[0] == 'claims':
                        index = path_parts[1]
                        signature = {'country': name, 'claim_id': data['claims'][index]['id'],
                                     'claim_sha256': cr.digest(expanded['claims'][index]),
                                     'relative_path': path_parts[2:], 'validator': error.validator,
                                     'message': error.message}
                        allowed = signature in exceptions
                    if not allowed:
                        raise error
        for event in country['deliveries']:
            assert event['id'] not in events and event['country'] == name, 'Duplicate/misfiled delivery event'
            events.add(event['id'])
            for target in event['destinations']:
                domain = {'monitoring-agencies-information.md':'monitoring','EAA sanctions.md':'sanctions','EAA enforcement tracking.md':'enforcement'}[target['page']]
                assert target['domain'] == domain, 'Destination/domain mismatch'
                if target['record'] is None:
                    assert target['disposition'] == 'not_applicable' and domain not in country['domains'], 'Missing applicable destination'
                else:
                    assert target['record'] == str(path.relative_to(root)) and domain in country['domains'], 'Wrong destination record'
    assert names == set(groups), 'Jurisdiction coverage differs from registry'
    ledger = json.loads((agents / 'evidence-routing/events.json').read_text())
    assert ledger == cr.routing_projection(root), 'Generated routing index is stale'
    module(agents / 'enforcement/check.py', 'enforcement_validation').check(root)
    module(root / '.github/scripts/check-sanctions.py', 'sanctions_validation').check(root)
    if migration:
        manifest = json.loads((agents / 'research/migration-manifest.json').read_text())
        for item in manifest['records']:
            assert cr.digest(cr.load(root, item['country'], item['domain'])) == item['sha256'], 'Migration changed original domain values: ' + item['original_path']
            assert not (root / item['original_path']).exists(), 'Duplicate writable legacy record'
    return len(names), len(ids), len(events)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--migration', action='store_true', help='Compare against frozen migration fingerprints; only for migration acceptance, not future research')
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[2])
    args = parser.parse_args()
    print('PASS: countries, claims, delivery events =', check(args.root, args.migration))
