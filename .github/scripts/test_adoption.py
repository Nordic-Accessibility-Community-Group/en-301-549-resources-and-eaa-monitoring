"""Adoption regression checks: preserve uncertainty, scope and review boundaries."""
import copy
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
        self.pool={}; self.today=date(2026,9,27)
    def tearDown(self): self.tmp.cleanup()
    def check(self): return a.check_domain('Example',self.domain,self.pool,self.root,self.row,self.today)
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
    def test_adoption_adapter_preserves_other_domains(self):
        c={'country':'Example','evidence':{},'domains':{'enforcement':{'unchanged':[1,2]}}}
        old=copy.deepcopy(c['domains']['enforcement'])
        record=copy.deepcopy(self.domain); record['country']='Example'
        cr.put_domain(c,'adoption',record)
        self.assertEqual(old,c['domains']['enforcement'])
        self.assertEqual(self.claim['id'],c['domains']['adoption']['claims'][0]['id'])

if __name__=='__main__': unittest.main()
