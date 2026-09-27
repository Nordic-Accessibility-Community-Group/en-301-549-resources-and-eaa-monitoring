"""Validate adoption evidence and report due reviews; never fetch or publish."""
import argparse
from datetime import date, timedelta
import hashlib
from html import unescape
import json
from pathlib import Path
import re
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import country_records as cr

PAGE = 'EN 301 549 adoptation.md'
BASELINE_SHA256 = '24e9b1a65aa55f415e7d1e0dfbdf0d189842d3677fdc6c1d9da57bbcfbd9024b'
DOMAIN_KEYS = {'claims', 'questions', 'attempts', 'last_monthly_review', 'last_full_review',
               'public_row_sha256', 'public_claim_ids', 'public_cells', 'review_report'}
CLAIM_KEYS = {'id', 'aspect', 'statement', 'scope', 'stage', 'status', 'source_refs',
              'event_dates', 'attempted_on', 'verified_on', 'next_review_due',
              'existing_text', 'review_note'}

def require(ok, message):
    if not ok:
        raise ValueError(message)

def day(value, today, future=False):
    if value is None:
        return None
    require(isinstance(value, str) and re.fullmatch(r'\d{4}-\d{2}-\d{2}', value), 'ISO date required')
    d = date.fromisoformat(value)
    require(future or d <= today, 'Future observation/verification date')
    return d

def event_date(value):
    require(isinstance(value, str) and re.fullmatch(r'\d{4}(-\d{2}){0,2}', value), 'Typed event date required')
    return date.fromisoformat(value + {4:'-01-01',7:'-01',10:''}[len(value)])

def rows(root):
    text = (root / PAGE).read_text()
    result = {}
    for row in re.findall(r'<tr\b[^>]*>.*?</tr>', text, re.S | re.I):
        cells = re.findall(r'<td\b[^>]*>(.*?)</td>', row, re.S | re.I)
        if cells:
            require(len(cells) in (5, 6), 'Adoption table must have five legacy or six current cells per row')
            name = re.sub('<[^>]+>', '', cells[0]).strip()
            require(name not in result, 'Duplicate adoption row')
            result[name] = row
    return result

def cell_texts(row):
    return [' '.join(unescape(re.sub('<[^>]+>', '', c)).split()) for c in re.findall(r'<td\b[^>]*>(.*?)</td>', row, re.S | re.I)]

def cell_links(row):
    return [[unescape(url) for url in re.findall(r'href=["\']([^"\']+)["\']', cell, re.I)] for cell in re.findall(r'<td\b[^>]*>(.*?)</td>', row, re.S | re.I)]

def inherited_rows(root):
    raw = (root / '.github/agents/adoption/inherited-rows.json').read_bytes()
    require(hashlib.sha256(raw).hexdigest() == BASELINE_SHA256, 'Frozen adoption baseline changed')
    return json.loads(raw)['rows']

def row_digest(row):
    return hashlib.sha256(row.encode()).hexdigest()

def check_domain(name, domain, pool, root, row, today):
    require(set(domain) == DOMAIN_KEYS, name + ': missing/unexpected domain fields')
    for key in ('last_monthly_review', 'last_full_review'):
        day(domain[key], today)
    require(isinstance(domain['questions'], list) and all(isinstance(q,str) for q in domain['questions']), 'Questions must be strings')
    require(isinstance(domain['attempts'], list), 'Attempt history missing')
    for attempt in domain['attempts']:
        require(attempt.get('outcome') in ('reachable','unreachable','unknown','search_lead','deferred'), 'Attempt outcome')
        require(bool(attempt.get('url') or attempt.get('query')) and bool(attempt.get('method')), 'Attempt provenance')
        day(attempt['on'], today)
    claims = {}
    for c in domain['claims']:
        require(set(c) == CLAIM_KEYS, name + ': missing/unexpected claim fields')
        require(re.fullmatch(r'adoption-[a-z0-9-]+', c['id']) and c['id'] not in claims, 'Duplicate/invalid adoption claim ID')
        claims[c['id']] = c
        require(c['aspect'] in ('adoption','edition','date','scope','publication','citation','reference','source_correction'), 'Claim aspect')
        require(c['stage'] in ('draft','final','withdrawn','planned','unknown'), 'Claim stage')
        require(c['status'] in ('verified','disputed','unknown','unverified_source'), 'Evidence status')
        require(all(isinstance(c[k],str) and c[k].strip() for k in ('statement','scope','review_note')), 'Claim wording/scope/note required')
        require(c['existing_text'] is None or isinstance(c['existing_text'],str), 'Inherited text must be string or null')
        attempted = day(c['attempted_on'], today)
        verified = day(c['verified_on'], today)
        due = day(c['next_review_due'], today, future=True)
        require(due is not None, 'Next review date required')
        require(verified is None or (attempted is not None and verified <= attempted and verified <= due), 'Verification chronology')
        require(isinstance(c['source_refs'],list) and all(s in pool for s in c['source_refs']), 'Missing evidence reference')
        for sid in c['source_refs']:
            source = pool[sid]
            require(sid == 'source-' + cr.digest(source)[:24], 'Evidence fingerprint mismatch')
            require(all(k in source for k in ('issuer','url','source_type','language','passage','publication_date','accessed_on','access','method')), 'Source metadata missing')
            require(source['access'] in ('reachable','unreachable','unknown'), 'Source access outcome')
            require(source['url'].startswith(('https://','http://')), 'Source URL')
            day(source['accessed_on'],today)
            if source['publication_date']:
                require(event_date(source['publication_date']) <= today, 'Future source publication')
        for e in c['event_dates']:
            require(set(e) == {'kind','value'}, 'Typed event fields')
            require(e['kind'] in ('publication','adoption','effective','citation','target','achieved','consultation_start','consultation_end','page_updated'), 'Event kind')
            require(e['kind'] == 'target' or event_date(e['value']) <= today, 'Future event must be a target')
            event_date(e['value'])
        if c['status'] == 'verified':
            require(verified is not None and c['source_refs'], 'Verified claim needs evidence and date')
            require(any(pool[s]['source_type'] in ('official_standard_body','official_government','official_law') and pool[s]['access'] == 'reachable' and pool[s]['passage'].strip() and pool[s]['accessed_on'] and day(pool[s]['accessed_on'],today) >= verified for s in c['source_refs']), 'Verified claim needs retrieved primary evidence')
        else:
            require(verified is None, 'Unverified claim has verification date')
    require(len(domain['public_claim_ids']) == len(set(domain['public_claim_ids'])) and all(i in claims for i in domain['public_claim_ids']), 'Public claim mapping')
    require(row_digest(row) == domain['public_row_sha256'], name + ': public row changed without evidence mapping')
    require(domain['public_claim_ids'], 'Public row needs claim mappings')
    baseline = inherited_rows(root)
    old_name = 'Europe' if name == 'European Union' else name
    old_row = baseline.get(old_name)
    actual_cells = cell_texts(row)
    old_cells = cell_texts(old_row) if old_row else [''] * 5
    old_cells += [''] * (len(actual_cells) - len(old_cells))
    actual_links = cell_links(row)
    old_links = cell_links(old_row) if old_row else [[] for _ in range(5)]
    old_links += [[] for _ in range(len(actual_cells) - len(old_links))]
    require(set(domain['public_cells']) == {str(i) for i in range(len(actual_cells))}, 'All public cells need mappings')
    new = []
    for i, text in enumerate(actual_cells):
        mapped = domain['public_cells'][str(i)]
        require(isinstance(mapped,list) and all(cid in domain['public_claim_ids'] for cid in mapped), 'Cell claim mapping invalid')
        if i == 5:
            require(not actual_links[i] and not mapped, 'Updated date is editorial metadata, not a claim')
            updates_path = root / '.github/agents/adoption/row-updates.json'
            updates = json.loads(updates_path.read_text()) if updates_path.exists() else {}
            update = updates.get(name)
            expected = update['updated_on'] if update else ''
            require(text == expected, 'Updated date must match row update record')
            if text:
                require(bool(re.fullmatch(r'\d{4}-\d{2}-\d{2}', text)), 'Updated date must be a date only')
                day(text, today)
                require(bool(update.get('reason')), 'Row update needs a reason')
            continue
        require(i == 0 or not text or mapped, 'Populated factual cell needs claim mapping')
        editorial = (i == 0 and name == 'European Union' and old_name == 'Europe')
        if i == 4 and old_row and old_cells[i] == '' and text == 'Source document (PDF)':
            editorial = re.findall(r'href="([^"]+)"',old_row) == re.findall(r'href="([^"]+)"',row) and bool(re.findall(r'href="([^"]+)"',old_row))
        if (text != old_cells[i] or actual_links[i] != old_links[i]) and not editorial:
            require(mapped, 'Changed public cell lacks evidence mapping')
            require(all(claims[cid]['status'] == 'verified' for cid in mapped), 'Changed public cell lacks verified evidence')
            new.extend(mapped)
    new.extend(i for i in domain['public_claim_ids'] if claims[i]['existing_text'] is None)
    new = list(set(new))
    require(all(claims[i]['status'] == 'verified' for i in new), 'New public assertion lacks verified evidence')
    if new:
        require(bool(domain['review_report']), 'New public wording needs isolated review report')
        p = (root / domain['review_report']).resolve()
        require(root.resolve() in p.parents, 'Review report outside repository')
        report = json.loads(p.read_text())
        require(report['isolation'] == 'no_history' and bool(report['reviewer']), 'Isolated reviewer missing')
        day(report['reviewed_on'],today)
        reviewed = report['rows'][name]
        require(reviewed['verdict'] == 'Supported' and reviewed['row_sha256'] == domain['public_row_sha256'] and set(new).issubset(reviewed['claim_ids']), 'Review does not cover final public wording')
    return claims

def check(root, require_coverage=False, today=None):
    today = today or date.today()
    public = rows(root)
    domains = {}
    country_event_ids = set()
    for path in cr.folder(root).glob('*.json'):
        c = json.loads(path.read_text())
        country_event_ids.update(e['id'] for e in c['deliveries'])
        if 'adoption' in c['domains']:
            domains[c['country']] = (c['domains']['adoption'],c['evidence'])
    global_path = root / '.github/agents/adoption/european-standard.json'
    if global_path.exists():
        g = json.loads(global_path.read_text())
        require(g['subject'] == 'European Union', 'Global subject')
        require(set(g) == {'subject','evidence','adoption','deliveries'}, 'Global record keys')
        require(isinstance(g['deliveries'],list), 'Global deliveries')
        event_ids = set(country_event_ids)
        pages = {PAGE:'adoption','monitoring-agencies-information.md':'monitoring','EAA sanctions.md':'sanctions','EAA enforcement tracking.md':'enforcement'}
        for event in g['deliveries']:
            require(isinstance(event,dict), 'Global event must be an object')
            require(bool(event.get('id')) and event['id'] not in event_ids, 'Global event ID missing/duplicate')
            event_ids.add(event['id'])
            targets = event['destinations']
            require(isinstance(targets,list) and all(isinstance(t,dict) for t in targets), 'Global destinations must be objects')
            require(len(targets) == 4 and {t['page'] for t in targets} == set(pages), 'Global event needs all destinations')
            for target in targets:
                require(target['domain'] == pages[target['page']] and bool(target['reason']), 'Global destination metadata')
                require(target['disposition'] in ('proposed','already_present','research_only','needs_evidence','blocked_by_open_pr','not_applicable'), 'Global disposition')
                if target['page'] == PAGE:
                    require(target['record'] == str(global_path.relative_to(root)), 'Global adoption record path')
                else:
                    if target['disposition'] == 'not_applicable':
                        require(target['record'] is None, 'Inapplicable global handoff must have null record')
                    else:
                        require(isinstance(target['record'],str), 'Applicable global handoff record missing')
                        destination = (root / target['record']).resolve()
                        require(destination.parent == cr.folder(root).resolve() and destination.suffix == '.json' and destination.is_file(), 'Global handoff must use canonical country record')
                        country = json.loads(destination.read_text())
                        require(target['domain'] in country['domains'], 'Global handoff domain missing')
        domains['European Union' if 'European Union' in public else 'Europe'] = (g['adoption'],g['evidence'])
    require(set(domains).issubset(public), 'Research row missing from page')
    if require_coverage:
        require(set(domains) == set(public), 'Baseline missing adoption records')
    ids = set()
    for name,(domain,pool) in domains.items():
        claims = check_domain(name,domain,pool,root,public[name],today)
        require(not ids.intersection(claims), 'Duplicate cross-country claim ID')
        ids.update(claims)
    return domains

def due_reviews(domains, today):
    result=[]
    for name,(d,_) in domains.items():
        for c in d['claims']:
            if date.fromisoformat(c['next_review_due']) <= today:
                result.append((c['next_review_due'],name,c['id']))
        for key,days in [('last_monthly_review',30),('last_full_review',90)]:
            due = date.min if d[key] is None else date.fromisoformat(d[key]) + timedelta(days=days)
            if due <= today:
                result.append((str(due),name,key))
    return sorted(result)

if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[2])
    p.add_argument('--require-coverage',action='store_true')
    p.add_argument('--due',action='store_true')
    a=p.parse_args()
    domains=check(a.root,a.require_coverage)
    print('PASS: adoption records =',len(domains))
    if a.due:
        for due,name,item in due_reviews(domains,date.today()):
            print(due,name,item)
