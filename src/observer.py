"""Hash changes in explicitly registered artifacts. No LLM and no system polling."""
from __future__ import annotations
import json
from pathlib import Path
from .retrieval import Registry

def observe(registry:Registry,snapshot:Path)->list[dict]:
    old=json.loads(snapshot.read_text()) if snapshot.exists() else {}
    new={a['id']:a['sha256'] for a in registry.manifest() if a['available']}
    events=[dict(kind='ARTIFACT_CHANGED',artifact=k,old_hash=old.get(k),new_hash=v,
                 idempotency_key=f'{k}:{v}') for k,v in new.items() if old.get(k)!=v]
    events.extend(dict(kind='ARTIFACT_REMOVED',artifact=k,idempotency_key=f'{k}:removed:{v}') for k,v in old.items() if k not in new)
    snapshot.parent.mkdir(parents=True,exist_ok=True)
    tmp=snapshot.with_suffix('.tmp'); tmp.write_text(json.dumps(new)); tmp.replace(snapshot)
    return events

if __name__=='__main__':
    root=Path(__file__).resolve().parents[1]
    print(json.dumps(observe(Registry(root),root/'.runtime/observer.json'),indent=2))
