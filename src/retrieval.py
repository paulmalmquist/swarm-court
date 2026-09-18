"""Persistent lexical-vector PREVIEW. Not pretrained semantic embeddings."""
from __future__ import annotations
import hashlib, json, math, re, sqlite3
from pathlib import Path

DIM=384

def tokens(text:str)->list[str]:
    return re.findall(r'[a-zA-Z0-9_]{2,}',text.lower())

def embedding(text:str)->list[float]:
    v=[0.0]*DIM
    for token in tokens(text):
        h=hashlib.blake2b(token.encode(),digest_size=8).digest()
        v[int.from_bytes(h[:4],'little')%DIM]+=1 if h[4]%2 else -1
    n=math.sqrt(sum(x*x for x in v)) or 1
    return [x/n for x in v]

class Registry:
    def __init__(self,root:Path):
        self.root=root.resolve()
        data=json.loads((root/'config/artifacts.json').read_text())
        self.items={a['id']:a for a in data}
    def resolve(self,aid:str)->Path:
        if aid not in self.items: raise KeyError('Unknown artifact')
        path=(self.root/self.items[aid]['path']).resolve()
        if not path.is_relative_to(self.root) or not path.is_file(): raise ValueError('Artifact missing or outside approved root')
        return path
    def read(self,aid:str)->dict:
        path=self.resolve(aid)
        if path.stat().st_size>1_000_000: raise ValueError('Artifact exceeds preview size cap')
        text=path.read_text(encoding='utf-8')
        return dict(self.items[aid],text=text,sha256=hashlib.sha256(text.encode()).hexdigest())
    def manifest(self)->list[dict]:
        out=[]
        for aid in self.items:
            try:
                a=self.read(aid); del a['text']; a['available']=True
            except (ValueError,FileNotFoundError): a=dict(self.items[aid],available=False)
            out.append(a)
        return out

class Retrieval:
    def __init__(self,path:Path,registry:Registry):
        self.path=path; self.registry=registry
        with sqlite3.connect(path) as c:
            c.execute('CREATE TABLE IF NOT EXISTS chunks(id TEXT PRIMARY KEY,artifact TEXT,sha TEXT,start INTEGER,end INTEGER,text TEXT,vec TEXT)')
        self.refresh()
    def refresh(self):
        with sqlite3.connect(self.path) as c:
            old={r[0]:r[1] for r in c.execute('SELECT artifact,sha FROM chunks')}
            valid=set()
            for aid in self.registry.items:
                try: a=self.registry.read(aid)
                except (ValueError,FileNotFoundError): continue
                valid.add(aid)
                if old.get(aid)==a['sha256']: continue
                c.execute('DELETE FROM chunks WHERE artifact=?',(aid,))
                lines=a['text'].splitlines()
                for start in range(0,len(lines),18):
                    text='\n'.join(lines[start:start+22]); end=min(start+22,len(lines))
                    c.execute('INSERT OR REPLACE INTO chunks VALUES(?,?,?,?,?,?,?)',
                              (f'{aid}:{start+1}',aid,a['sha256'],start+1,end,text,json.dumps(embedding(text))))
            for aid in set(old)-valid: c.execute('DELETE FROM chunks WHERE artifact=?',(aid,))
    def count(self)->int:
        with sqlite3.connect(self.path) as c: return c.execute('SELECT COUNT(*) FROM chunks').fetchone()[0]
    def search(self,query:str,limit:int=6)->list[dict]:
        if not query.strip(): return []
        q=embedding(query); qt=set(tokens(query)); candidates=[]
        with sqlite3.connect(self.path) as c:
            c.row_factory=sqlite3.Row
            for row in c.execute('SELECT * FROM chunks'):
                lexical=len(qt&set(tokens(row['text'])))/max(1,len(qt))
                cosine=sum(a*b for a,b in zip(q,json.loads(row['vec'])))
                if lexical==0: continue
                candidates.append((dict(row),cosine,lexical))
        dense=sorted(candidates,key=lambda x:x[1],reverse=True)
        sparse=sorted(candidates,key=lambda x:x[2],reverse=True)
        scores={}
        for ranked in [dense,sparse]:
            for rank,(row,_,_) in enumerate(ranked,1): scores[row['id']]=scores.get(row['id'],0)+1/(60+rank)
        out=[]; per_source={}
        for row,cosine,lexical in sorted(candidates,key=lambda x:scores[x[0]['id']],reverse=True):
            if per_source.get(row['artifact'],0)>=2: continue
            try: a=self.registry.read(row['artifact'])
            except (KeyError,ValueError,FileNotFoundError): continue
            if a['sha256']!=row['sha']: continue
            per_source[row['artifact']]=per_source.get(row['artifact'],0)+1
            out.append(dict(artifact=row['artifact'],path=a['path'],title=a['title'],start=row['start'],end=row['end'],
                            text=row['text'],sha256=row['sha'],score=round(scores[row['id']],5),
                            backend='lexical-vector-preview',similarity=round(cosine,3)))
            if len(out)>=limit: break
        return out
