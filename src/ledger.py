"""Durable synthetic task ledger. Production ownership must come from real events."""
from __future__ import annotations
import json
import sqlite3
import time
from pathlib import Path
from contextlib import contextmanager
from typing import Any, Iterator

NODES = [
    dict(id='signals', title='Signal watch', role='Deterministic observers', x=115, y=195, symbol='⌁'),
    dict(id='router', title='Dispatcher', role='Dedupe · budget · routing', x=320, y=195, symbol='◇'),
    dict(id='memory', title='Local memory', role='Source-backed retrieval', x=325, y=385, symbol='▤'),
    dict(id='pipeline', title='Pipeline Sentinel', role='Freshness & incidents', x=555, y=90, symbol='⌁'),
    dict(id='governance', title='Governance Agent', role='Contracts & certification', x=555, y=235, symbol='⬡'),
    dict(id='librarian', title='Knowledge Librarian', role='Plans · code · evidence', x=555, y=385, symbol='▤'),
    dict(id='critic', title='Verifier', role='Tests before second opinions', x=800, y=195, symbol='✓'),
    dict(id='paul', title='Paul', role='Accountable human', x=1025, y=195, symbol='P'),
    dict(id='features', title='System features', role='Linked implementation', x=1025, y=385, symbol='↗'),
]
EDGES = [('signals','router'),('router','pipeline'),('router','governance'),('router','librarian'),
         ('router','memory'),('memory','librarian'),('memory','governance'),('pipeline','critic'),
         ('governance','critic'),('librarian','critic'),('critic','paul'),('paul','features')]
FEATURES = [
 dict(id='certification',title='Governed metric certification',subtitle='Definition → evidence → approval',
      plan='plan-001',code='ledger',task='GOV-027',status='Demo surface',
      checks=['Versioned definitions','Evidence links','Named approver','No autonomous certification']),
 dict(id='memory',title='Paul OS context retrieval',subtitle='Local files → local vectors → exact citations',
      plan='plan-002',code='retrieval',task='KB-012',status='Local preview working',
      checks=['Local persistent index','Real source links','Content hashes','Semantic adapter requires validation']),
 dict(id='query-audit',title='Application query audit',subtitle='Feature → SQL → governed source',
      plan='plan-003',code='worker',task='APP-009',status='Work adapter not connected',
      checks=['Declared data contract','Actual execution identity','Read-only metadata','Explicit permission gaps']),
 dict(id='pipeline-health',title='Pipeline health',subtitle='Deterministic signals → bounded investigation',
      plan='plan-004',code='observer',task='PIPE-041',status='Work adapter not connected',
      checks=['Freshness detector','Incident deduplication','Runbook evidence','Human-gated remediation']),
]

def fixtures() -> list[dict[str,Any]]:
    now=time.time()
    common=dict(accountable='Paul',version=1,source='Synthetic scenario',hops=0)
    return [dict(common,id='GOV-027',title='Review metric-contract change',project='Governed data',
                 status='WAITING_HUMAN',owner='Paul',node='paul',pending_owner='System features',
                 reason='Evidence is assembled; a named decision is needed.',
                 next_action='Approve or reject the read-only review scope.',age_start=now-1320,
                 plan='plan-001',code='ledger',feature='certification',priority='High',
                 route=['signals','router','governance','critic','paul','features'],
                 evidence=['plan-001','architecture','budget']),
            dict(common,id='KB-012',title='Refresh changed skill context',project='Paul OS knowledge',
                 status='RUNNING',owner='Knowledge Librarian',node='librarian',pending_owner='Verifier',
                 reason='Synthetic run: index only content-hash changes.',
                 next_action='Validate citations for changed skill files.',age_start=now-360,
                 plan='plan-002',code='retrieval',feature='memory',priority='Normal',
                 route=['signals','router','memory','librarian','critic','paul'],
                 evidence=['plan-002','vector-memory','retrieval']),
            dict(common,id='APP-009',title='Verify app uses governed sources',project='Application governance',
                 status='WAITING_PERMISSION',owner='Access approver · unassigned',node='router',pending_owner='Governance Agent',
                 reason='Approved BigQuery metadata access has not been configured.',
                 next_action='Name the access approver and register a read-only adapter.',age_start=now-5580,
                 plan='plan-003',code='worker',feature='query-audit',priority='High',
                 route=['signals','router','governance','critic','paul'],
                 evidence=['plan-003','security','connections']),
            dict(common,id='PIPE-041',title='Investigate freshness breach',project='Data reliability',
                 status='WAITING_CAPACITY',owner='Pipeline Sentinel',node='pipeline',pending_owner='Verifier',
                 reason='Claude execution is disabled until billing and egress are verified.',
                 next_action='Verify work-seat billing mode; then take a bounded queue slot.',age_start=now-660,
                 plan='plan-004',code='observer',feature='pipeline-health',priority='Normal',
                 route=['signals','router','pipeline','critic','paul'],
                 evidence=['plan-004','budget','runtime'])]

class Conflict(ValueError):
    """A task changed after the caller read it."""

class Ledger:
    def __init__(self,path:Path):
        self.path=path; path.parent.mkdir(parents=True,exist_ok=True)
        with self.db() as c:
            c.executescript('''
            CREATE TABLE IF NOT EXISTS tasks(id TEXT PRIMARY KEY, payload TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS events(id INTEGER PRIMARY KEY AUTOINCREMENT, at REAL, kind TEXT, payload TEXT);
            CREATE TABLE IF NOT EXISTS settings(key TEXT PRIMARY KEY,value TEXT);
            CREATE TABLE IF NOT EXISTS dispatches(id INTEGER PRIMARY KEY AUTOINCREMENT,at REAL,status TEXT,until REAL);
            ''')
            c.execute("INSERT OR IGNORE INTO settings VALUES('paused','false')")
            if c.execute('SELECT COUNT(*) FROM tasks').fetchone()[0]==0:
                for t in fixtures(): c.execute('INSERT INTO tasks VALUES(?,?)',(t['id'],json.dumps(t)))
                self._event(c,'DEMO_LOADED',{'note':'Synthetic scenario initialized. No systems or Claude connected.'})
    @contextmanager
    def db(self)->Iterator[sqlite3.Connection]:
        c=sqlite3.connect(self.path,timeout=10); c.row_factory=sqlite3.Row
        c.execute('PRAGMA journal_mode=WAL'); c.execute('PRAGMA busy_timeout=10000')
        try:
            yield c; c.commit()
        except BaseException:
            c.rollback(); raise
        finally: c.close()
    def _event(self,c,kind,payload):
        c.execute('INSERT INTO events(at,kind,payload) VALUES(?,?,?)',(time.time(),kind,json.dumps(payload)))
    def state(self)->dict:
        with self.db() as c:
            tasks=[json.loads(r['payload']) for r in c.execute('SELECT payload FROM tasks ORDER BY id')]
            events=[dict(id=r['id'],at=r['at'],kind=r['kind'],**json.loads(r['payload'])) for r in c.execute('SELECT * FROM events ORDER BY id DESC LIMIT 24')]
            paused=json.loads(c.execute("SELECT value FROM settings WHERE key='paused'").fetchone()[0])
            today=time.time()//86400*86400
            dispatches=c.execute('SELECT COUNT(*) FROM dispatches WHERE at>=?',(today,)).fetchone()[0]
        return dict(tasks=tasks,events=events,paused=paused,dispatches=dispatches,nodes=NODES,edges=EDGES,features=FEATURES)
    def pause(self,paused:bool)->dict:
        with self.db() as c:
            c.execute('UPDATE settings SET value=? WHERE key=?',(json.dumps(paused),'paused'))
            self._event(c,'DEMO_PAUSED' if paused else 'DEMO_RESUMED',{'note':'Local simulation only; model execution remains disabled.'})
        return self.state()
    def transition(self,task_id:str,version:int,action:str)->dict:
        with self.db() as c:
            c.execute('BEGIN IMMEDIATE')
            if json.loads(c.execute("SELECT value FROM settings WHERE key='paused'").fetchone()[0]):
                raise ValueError('Simulation is paused.')
            row=c.execute('SELECT payload FROM tasks WHERE id=?',(task_id,)).fetchone()
            if not row: raise KeyError(task_id)
            t=json.loads(row[0])
            if t['version']!=version: raise Conflict('Task changed; refresh before acting.')
            previous=t['node']
            if action=='advance':
                if t['status']=='COMPLETED': raise ValueError('Task is already completed.')
                route=t['route']; idx=route.index(t['node'])
                if idx>=len(route)-1:
                    t.update(status='COMPLETED',reason='Synthetic route completed.',next_action='Review linked artifacts; no production changes were made.',pending_owner=None)
                else:
                    node=route[idx+1]; title=next(n['title'] for n in NODES if n['id']==node)
                    status='WAITING_HUMAN' if node=='paul' else ('COMPLETED' if node=='features' else 'RUNNING')
                    t.update(node=node,owner=title,status=status,reason='Accepted handoff recorded by the synthetic demo.',
                             next_action='Inspect the linked plan and evidence before the next handoff.',pending_owner=None)
            else: raise ValueError('Unsupported demo action.')
            t.update(version=version+1,age_start=time.time(),hops=t['hops']+1)
            c.execute('UPDATE tasks SET payload=? WHERE id=?',(json.dumps(t),task_id))
            self._event(c,'DEMO_HANDOFF_ACCEPTED',{'task':task_id,'from_node':previous,'to_node':t['node'],'owner':t['owner'],'note':'Simulation only; no external side effect.'})
        return self.state()
    def reserve_dispatch(self,limit:int,seconds:int)->int:
        with self.db() as c:
            c.execute('BEGIN IMMEDIATE'); now=time.time()
            if json.loads(c.execute("SELECT value FROM settings WHERE key='paused'").fetchone()[0]): raise ValueError('Paused')
            if c.execute("SELECT COUNT(*) FROM dispatches WHERE status='running' AND until>?",(now,)).fetchone()[0]: raise ValueError('Worker slot occupied')
            if c.execute('SELECT COUNT(*) FROM dispatches WHERE at>=?',(now//86400*86400,)).fetchone()[0]>=limit: raise ValueError('Daily dispatch cap reached')
            cur=c.execute('INSERT INTO dispatches(at,status,until) VALUES(?,?,?)',(now,'running',now+seconds+30))
            return cur.lastrowid
    def finish_dispatch(self,run_id:int,status:str):
        with self.db() as c:
            c.execute('UPDATE dispatches SET status=?,until=0 WHERE id=?',(status,run_id))
            self._event(c,'DISPATCH_FINISHED',{'run_id':run_id,'status':status})
