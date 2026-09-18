import hashlib,json,math,tempfile,unittest
from pathlib import Path
from src.ledger import Ledger,Conflict
from src.retrieval import Registry,Retrieval,embedding
from src.worker import gate
from src.observer import observe
ROOT=Path(__file__).resolve().parents[1]

class LedgerTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name);self.l=Ledger(self.root/'state.db')
    def tearDown(self):self.tmp.cleanup()
    def test_synthetic_baseline_and_no_calls(self):
        self.assertEqual(len(self.l.state()['tasks']),4);self.assertEqual(self.l.state()['dispatches'],0)
    def test_state_persists(self):
        self.l.transition('GOV-027',1,'advance')
        t=next(t for t in Ledger(self.root/'state.db').state()['tasks'] if t['id']=='GOV-027')
        self.assertEqual(t['node'],'features');self.assertEqual(t['version'],2)
    def test_pending_owner_is_not_current_owner(self):
        t=next(t for t in self.l.state()['tasks'] if t['id']=='GOV-027')
        self.assertEqual(t['owner'],'Paul');self.assertEqual(t['pending_owner'],'System features')
    def test_stale_handoff_rejected(self):
        self.l.transition('GOV-027',1,'advance')
        with self.assertRaises(Conflict):self.l.transition('GOV-027',1,'advance')
    def test_pause_blocks_simulation(self):
        self.l.pause(True)
        with self.assertRaises(ValueError):self.l.transition('GOV-027',1,'advance')
    def test_dispatch_cap(self):
        rid=self.l.reserve_dispatch(1,60);self.l.finish_dispatch(rid,'done')
        with self.assertRaises(ValueError):self.l.reserve_dispatch(1,60)
    def test_single_slot(self):
        self.l.reserve_dispatch(12,60)
        with self.assertRaises(ValueError):self.l.reserve_dispatch(12,60)
    def test_handoff_has_audit_event(self):
        s=self.l.transition('PIPE-041',1,'advance')
        self.assertEqual(s['events'][0]['kind'],'DEMO_HANDOFF_ACCEPTED')
        self.assertEqual(s['events'][0]['from_node'],'pipeline')
        self.assertEqual(s['events'][0]['to_node'],'critic')

class RegistryRetrievalTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
        (self.root/'config').mkdir();(self.root/'plan.md').write_text('# Approval\nPaul approves certification before release.\nLocal vector retrieval verifies source hashes.\n')
        (self.root/'config/artifacts.json').write_text(json.dumps([dict(id='plan',path='plan.md',title='Plan',kind='plan')]))
        self.registry=Registry(self.root);self.r=Retrieval(self.root/'db.sqlite',self.registry)
    def tearDown(self):self.tmp.cleanup()
    def test_hash_and_exact_source(self):
        a=self.registry.read('plan');self.assertEqual(a['sha256'],hashlib.sha256(a['text'].encode()).hexdigest())
        hits=self.r.search('certification approval');self.assertTrue(hits)
        self.assertEqual(hits[0]['artifact'],'plan');self.assertEqual(hits[0]['start'],1)
    def test_unknown_id_cannot_read_arbitrary_path(self):
        with self.assertRaises(KeyError):self.registry.read('../etc/passwd')
    def test_symlink_escape_rejected(self):
        self.registry.items['escape']=dict(id='escape',path='outside',title='bad')
        (self.root/'outside').symlink_to('/etc/passwd')
        with self.assertRaises(ValueError):self.registry.read('escape')
    def test_stale_source_rejected(self):
        (self.root/'plan.md').write_text('Replacement source.')
        self.assertEqual(self.r.search('certification'),[])
    def test_incremental_update(self):
        (self.root/'plan.md').write_text('Calibration lineage is the new plan.')
        self.r.refresh();self.assertTrue(self.r.search('calibration lineage'));self.assertEqual(self.r.search('certification'),[])
    def test_deleted_source_removed(self):
        (self.root/'plan.md').unlink();self.r.refresh();self.assertEqual(self.r.count(),0)
    def test_empty_query(self):self.assertEqual(self.r.search(''),[])
    def test_embedding_stable_and_normalized(self):
        a=embedding('source verification');self.assertEqual(a,embedding('source verification'));self.assertEqual(len(a),384)
        self.assertAlmostEqual(sum(x*x for x in a),1)
    def test_observer_dedupe(self):
        snapshot=self.root/'snapshot.json';self.assertEqual(len(observe(self.registry,snapshot)),1)
        self.assertEqual(observe(self.registry,snapshot),[])
    def test_packaged_artifacts_resolve(self):
        r=Registry(ROOT)
        for aid in r.items:self.assertTrue(r.resolve(aid).is_file())

class BudgetTests(unittest.TestCase):
    def test_default_is_fail_closed(self):
        p=json.loads((ROOT/'config/runtime.json').read_text());self.assertGreaterEqual(len(gate(p,{})),4)
    def allowed(self):
        return dict(execution_enabled=True,admin_verified=True,egress_approved=True,billing_mode='included_allowance',usage_credits_disabled=True,approved_model='approved-test-model',automatic_api_fallback=False)
    def test_explicit_allowance_policy(self):self.assertEqual(gate(self.allowed(),{}),[])
    def test_provider_override_blocks(self):self.assertTrue(gate(self.allowed(),{'ANTHROPIC_API_KEY':'TEST_ONLY_NOT_REAL'}))
    def test_consumption_requires_spend_controls(self):
        p=self.allowed();p['billing_mode']='consumption';self.assertTrue(gate(p,{}))
    def test_paid_fallback_forbidden(self):
        p=self.allowed();p['automatic_api_fallback']=True;self.assertTrue(gate(p,{}))

if __name__=='__main__':unittest.main()
