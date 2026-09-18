"""Local HTTP checks in an isolated temporary ledger. No model/network provider calls."""
import json,sys,tempfile,threading,urllib.request,urllib.error
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from src.server import CourtServer
from src.ledger import Ledger
from src.retrieval import Retrieval
checks=[]
with tempfile.TemporaryDirectory() as tmp:
    server=CourtServer(0)
    server.ledger=Ledger(Path(tmp)/'state.db')
    server.retrieval=Retrieval(Path(tmp)/'state.db',server.registry)
    thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
    base=f'http://127.0.0.1:{server.server_port}'
    def call(path,body=None,token=True,origin=None):
        headers={}
        if body is not None:
            headers['Content-Type']='application/json'
            if token:headers['X-Court-Token']=server.token
            if origin:headers['Origin']=origin
        request=urllib.request.Request(base+path,data=None if body is None else json.dumps(body).encode(),headers=headers)
        try:
            with urllib.request.urlopen(request,timeout=10) as response:
                raw=response.read();return response.status,json.loads(raw) if 'application/json' in response.headers.get('Content-Type','') else raw
        except urllib.error.HTTPError as e:return e.code,json.loads(e.read())
    try:
        code,s=call('/api/state');assert code==200 and s['dispatches']==0;checks.append('state API available with zero model calls')
        for path in ['/','/styles.css','/app.js']: assert call(path)[0]==200
        checks.append('HTML CSS and JavaScript served')
        for a in s['artifacts']:
            code,content=call('/api/artifact?id='+a['id']);assert code==200 and content['sha256']==a['sha256']
        checks.append(f'all {len(s["artifacts"])} allowlisted artifacts resolve with matching hashes')
        assert call('/api/artifact?id=../etc/passwd')[0]==404;checks.append('arbitrary source path rejected')
        code,result=call('/api/search?q=vector%20source%20hash');assert code==200 and result['results'];checks.append('persistent vector-plus-keyword retrieval returns evidence')
        assert call('/api/advance',{'task':'PIPE-041','version':1},token=False)[0]==403;checks.append('write without token rejected')
        assert call('/api/advance',{'task':'PIPE-041','version':1},origin='https://untrusted.invalid')[0]==403;checks.append('cross-origin write rejected')
        code,s=call('/api/advance',{'task':'PIPE-041','version':1});assert code==200
        t=next(t for t in s['tasks'] if t['id']=='PIPE-041');assert t['owner']=='Verifier';checks.append('accepted handoff persisted over HTTP')
        assert call('/api/advance',{'task':'PIPE-041','version':1})[0]==409;checks.append('stale write rejected with conflict')
        reloaded=Ledger(Path(tmp)/'state.db').state();assert next(t for t in reloaded['tasks'] if t['id']=='PIPE-041')['owner']=='Verifier';checks.append('fresh ledger instance reads persisted ownership')
        assert call('/api/pause',{'paused':True})[0]==200
        assert call('/api/advance',{'task':'KB-012','version':1})[0]==400;checks.append('pause blocks subsequent mutation')
        assert call('/api/state')[1]['dispatches']==0;checks.append('full HTTP test made zero model calls')
    finally:
        server.shutdown();server.server_close();thread.join()
report={'passed':len(checks),'checks':checks}
print(json.dumps(report,indent=2))
