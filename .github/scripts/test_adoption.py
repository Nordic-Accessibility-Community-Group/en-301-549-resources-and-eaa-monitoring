"""Adoption regression checks: preserve uncertainty, scope and review boundaries."""
import copy
import json
from unittest.mock import patch
from datetime import date
from pathlib import Path
import tempfile
import unittest
import check_adoption as a
import country_records as cr

class AdoptionChecks(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.root=Path(self.tmp.name)
        self.row='<tr><td>Example</td><td>Adopted</td><td></td><td></td><td></td></tr>'
        self.claim={'id':'adoption-example-inherited','aspect':'adoption','statement':'Adopted','scope':'Inherited; scope unresolved','stage':'unknown','status':'unknown','source_refs':[],'event_dates':[],'attempted_on':None,'verified_on':None,'next_review_due':'2026-09-27','existing_text':'Adopted','review_note':'Preserved pending evidence'}
        self.domain={'claims':[self.claim],'questions':[],'attempts':[],'last_monthly_review':None,'last_full_review':None,'public_row_sha256':a.row_digest(self.row),'public_claim_ids':[self.claim['id']],'review_report':None}
        self.domain['public_cells']={str(i):[self.claim['id']] for i in range(5)}
        self.baseline_patch=patch.object(a,'inherited_rows',return_value={'Example':self.row}); self.baseline_patch.start()
        self.pool={}; self.today=date(2026,9,27)
    def tearDown(self): self.baseline_patch.stop(); self.tmp.cleanup()
    def check(self): return a.check_domain('Example',self.domain,self.pool,self.root,self.row,self.today)
    def test_current_filename_preferred_and_legacy_fallback(self):
        (self.root/a.PAGE).write_text('<table>'+self.row+'</table>')
        self.assertIn('Example',a.rows(self.root))
        current=self.root/'EN 301 549 adoption.md'
        current.write_text('<table>'+self.row.replace('Example','Current')+'</table>')
        self.assertEqual({'Current'},set(a.rows(self.root)))
        (self.root/a.PAGE).unlink()
        self.assertEqual({'Current'},set(a.rows(self.root)))
    def test_inherited_unknown_preserved(self): self.check()
    def test_new_unsupported_public_assertion_rejected(self):
        self.claim['existing_text']=None
        with self.assertRaisesRegex(ValueError,'lacks verified'): self.check()
    def test_missing_evidence_rejected(self):
        self.claim['source_refs']=['source-missing']
        with self.assertRaisesRegex(ValueError,'Missing evidence'): self.check()
    def test_future_achieved_rejected_but_target_allowed(self):
        self.claim['event_dates']=[{'kind':'target','value':'2026-12-16'}]; self.check()
        self.claim['event_dates'][0]['kind']='achieved'
        with self.assertRaisesRegex(ValueError,'Future event'): self.check()
    def test_verification_cannot_be_future(self):
        self.claim['verified_on']='2026-09-28'
        with self.assertRaisesRegex(ValueError,'Future observation'): self.check()
    def test_failed_source_cannot_verify(self):
        s={'issuer':'Agency','url':'https://example.org','source_type':'official_government','language':'en','passage':'Adopted','publication_date':None,'accessed_on':'2026-09-27','access':'unreachable','method':'reader'}
        sid='source-'+cr.digest(s)[:24]; self.pool[sid]=s
        self.claim.update(status='verified',verified_on='2026-09-27',attempted_on='2026-09-27',source_refs=[sid])
        with self.assertRaisesRegex(ValueError,'retrieved primary'): self.check()
    def test_changed_row_requires_new_mapping(self):
        self.row=self.row.replace('Adopted','Mandatory')
        with self.assertRaisesRegex(ValueError,'row changed'): self.check()
    def test_failed_attempt_keeps_claim_due(self):
        self.domain['attempts']=[{'url':'https://example.org','on':'2026-09-27','method':'reader','outcome':'unreachable'}]
        self.check()
        self.assertIn(('2026-09-27','Example',self.claim['id']),a.due_reviews({'Example':(self.domain,self.pool)},self.today))
    def test_missing_coverage_rejected(self):
        (self.root/a.PAGE).write_text('<table>'+self.row+'</table>')
        with self.assertRaisesRegex(ValueError,'Baseline missing'): a.check(self.root,True,self.today)
    def test_inherited_flag_cannot_bypass_changed_cell_review(self):
        self.row=self.row.replace('Adopted','Mandatory')
        self.domain['public_row_sha256']=a.row_digest(self.row)
        with self.assertRaisesRegex(ValueError,'Changed public cell lacks verified'): self.check()
    def test_empty_claim_mapping_rejected(self):
        self.domain['public_claim_ids']=[]
        with self.assertRaisesRegex(ValueError,'needs claim mappings'): self.check()
    def test_populated_cell_cannot_omit_mapping(self):
        self.domain['public_cells']['1']=[]
        with self.assertRaisesRegex(ValueError,'Populated factual cell'): self.check()
    def test_global_events_reject_duplicates_and_missing_destinations(self):
        (self.root/a.PAGE).write_text('<table>'+self.row.replace('Example','Europe')+'</table>')
        folder=self.root/'.github/agents/adoption'; folder.mkdir(parents=True)
        d=copy.deepcopy(self.domain); row=self.row.replace('Example','Europe'); d['public_row_sha256']=a.row_digest(row)
        record={'subject':'European Union','evidence':{},'adoption':d,'deliveries':[{'id':'one','destinations':[]}]}
        path=folder/'european-standard.json'
        path.write_text(json.dumps(record))
        with self.assertRaisesRegex(ValueError,'all destinations'): a.check(self.root,True,self.today)
        targets=[{'page':p,'domain':domain,'record':'.github/agents/adoption/european-standard.json' if domain=='adoption' else None,'reason':'No relevant finding','disposition':'research_only' if domain=='adoption' else 'not_applicable'} for p,domain in [(a.PAGE,'adoption'),('monitoring-agencies-information.md','monitoring'),('EAA sanctions.md','sanctions'),('EAA enforcement tracking.md','enforcement')]]
        record['deliveries']=[{'id':'one','destinations':targets}]*2; path.write_text(json.dumps(record))
        with self.assertRaisesRegex(ValueError,'ID missing/duplicate'): a.check(self.root,True,self.today)
        record['deliveries']=['garbage']; path.write_text(json.dumps(record))
        with self.assertRaisesRegex(ValueError,'must be an object'): a.check(self.root,True,self.today)
    def test_changed_link_requires_evidence(self):
        original=self.row.replace('<td>Adopted</td>','<td><a href="https://example.org/original">Adopted</a></td>')
        self.baseline_patch.stop(); self.baseline_patch=patch.object(a,'inherited_rows',return_value={'Example':original}); self.baseline_patch.start()
        self.row=original.replace('https://example.org/original','https://other.example/new')
        self.domain['public_row_sha256']=a.row_digest(self.row)
        with self.assertRaisesRegex(ValueError,'Changed public cell lacks verified'): self.check()
    def test_global_handoff_cannot_point_to_arbitrary_file(self):
        (self.root/a.PAGE).write_text('<table>'+self.row.replace('Example','Europe')+'</table>')
        folder=self.root/'.github/agents/adoption'; folder.mkdir(parents=True)
        (self.root/'unrelated.txt').write_text('not a country record')
        targets=[{'page':p,'domain':d,'record':'.github/agents/adoption/european-standard.json' if d=='adoption' else 'unrelated.txt' if d=='monitoring' else None,'reason':'Fixture','disposition':'research_only' if d in ('adoption','monitoring') else 'not_applicable'} for p,d in [(a.PAGE,'adoption'),('monitoring-agencies-information.md','monitoring'),('EAA sanctions.md','sanctions'),('EAA enforcement tracking.md','enforcement')]]
        (folder/'european-standard.json').write_text(json.dumps({'subject':'European Union','evidence':{},'adoption':self.domain,'deliveries':[{'id':'one','destinations':targets}]}))
        with self.assertRaisesRegex(ValueError,'canonical country record'): a.check(self.root,True,self.today)
    def sixth(self, text, mapped):
        self.row=self.row.replace('</tr>','<td>'+text+'</td></tr>')
        self.domain['public_row_sha256']=a.row_digest(self.row)
        self.domain['public_cells']['5']=mapped
    def record_update(self, date):
        p=self.root/'.github/agents/adoption/row-updates.json';p.parent.mkdir(parents=True,exist_ok=True)
        p.write_text(json.dumps({'Example':{'updated_on':date,'reason':'Public link label edited'}}))
    def test_unknown_updated_date_is_blank(self):
        self.sixth('',[]);self.check()
    def test_editorial_update_does_not_imply_verification(self):
        self.record_update('2026-09-27');self.sixth('2026-09-27',[]);self.check()
        self.assertIsNone(self.claim['verified_on'])
    def test_updated_date_requires_record(self):
        self.sixth('2026-09-27',[])
        with self.assertRaisesRegex(ValueError,'row update record'):self.check()
    def test_updated_date_rejects_scope_text(self):
        self.record_update('2026-09-27 — verified');self.sixth('2026-09-27 — verified',[])
        with self.assertRaisesRegex(ValueError,'date only'):self.check()
    def test_updated_date_cannot_be_future(self):
        self.record_update('2026-09-28');self.sixth('2026-09-28',[])
        with self.assertRaisesRegex(ValueError,'Future observation'):self.check()
    def test_adoption_adapter_preserves_other_domains(self):
        c={'country':'Example','evidence':{},'domains':{'enforcement':{'unchanged':[1,2]}}}
        old=copy.deepcopy(c['domains']['enforcement'])
        record=copy.deepcopy(self.domain); record['country']='Example'
        cr.put_domain(c,'adoption',record)
        self.assertEqual(old,c['domains']['enforcement'])
        self.assertEqual(self.claim['id'],c['domains']['adoption']['claims'][0]['id'])

if __name__=='__main__': unittest.main()
