"""Loopback-only local prototype server. No company or model connections."""
from __future__ import annotations
import argparse,json,mimetypes,secrets
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse,parse_qs
from .ledger import Ledger,Conflict
from .retrieval import Registry,Retrieval

ROOT=Path(__file__).resolve().parents[1]
class CourtServer(ThreadingHTTPServer):
    daemon_threads=True
    def __init__(self,port:int):
        self.root=ROOT; self.registry=Registry(ROOT)
        self.ledger=Ledger(ROOT/'.runtime/court.sqlite3')
        self.retrieval=Retrieval(ROOT/'.runtime/court.sqlite3',self.registry)
        self.token=secrets.token_urlsafe(32)
        super().__init__(('127.0.0.1',port),Handler)
    def state(self):
        return dict(self.ledger.state(),config=json.loads((ROOT/'config/runtime.json').read_text()),
                    artifacts=self.registry.manifest(),backend='lexical-vector-preview',
                    chunk_count=self.retrieval.count(),csrf=self.token)

class Handler(BaseHTTPRequestHandler):
    server:CourtServer
    def valid_host(self)->bool:
        return self.headers.get('Host') in {f'127.0.0.1:{self.server.server_port}',f'localhost:{self.server.server_port}'}
    def send(self,status:int,data:bytes,content_type:str):
        self.send_response(status);self.send_header('Content-Type',content_type)
        self.send_header('Content-Length',str(len(data)));self.send_header('Cache-Control','no-store')
        self.send_header('X-Content-Type-Options','nosniff');self.send_header('Referrer-Policy','no-referrer')
        self.send_header('Content-Security-Policy',"default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'")
        self.end_headers();self.wfile.write(data)
    def js(self,status:int,obj): self.send(status,json.dumps(obj).encode(),'application/json; charset=utf-8')
    def do_GET(self):
        if not self.valid_host(): return self.js(403,{'error':'Invalid local host'})
        p=urlparse(self.path);q=parse_qs(p.query)
        try:
            if p.path=='/api/state': return self.js(200,self.server.state())
            if p.path=='/api/artifact': return self.js(200,self.server.registry.read(q.get('id',[''])[0]))
            if p.path=='/api/search':
                query=q.get('q',[''])[0][:400];self.server.retrieval.refresh()
                return self.js(200,{'results':self.server.retrieval.search(query),'backend':'384d lexical-vector preview + keyword fusion','count':self.server.retrieval.count()})
            files={'/':'index.html','/index.html':'index.html','/styles.css':'styles.css','/app.js':'app.js'}
            if p.path not in files:return self.js(404,{'error':'Not found'})
            path=ROOT/'web'/files[p.path]
            typ=mimetypes.guess_type(path.name)[0] or 'application/octet-stream'
            self.send(200,path.read_bytes(),typ+'; charset=utf-8')
        except KeyError:self.js(404,{'error':'Unknown artifact'})
        except (ValueError,FileNotFoundError) as e:self.js(400,{'error':str(e)})
        except Exception:self.js(500,{'error':'Local request failed. Inspect server logs.'})
    def do_POST(self):
        if not self.valid_host():return self.js(403,{'error':'Invalid local host'})
        origin=self.headers.get('Origin')
        allowed={f'http://127.0.0.1:{self.server.server_port}',f'http://localhost:{self.server.server_port}'}
        if origin and origin not in allowed:return self.js(403,{'error':'Cross-origin write denied'})
        if not secrets.compare_digest(self.headers.get('X-Court-Token',''),self.server.token):return self.js(403,{'error':'Local session token required'})
        if self.headers.get('Content-Type','').split(';')[0]!='application/json':return self.js(415,{'error':'JSON required'})
        try:
            n=int(self.headers.get('Content-Length','0'))
            if not 0<n<=16384:raise ValueError('Request too large or empty')
            body=json.loads(self.rfile.read(n))
            if self.path=='/api/advance':
                self.server.ledger.transition(str(body['task']),int(body['version']),'advance')
                return self.js(200,self.server.state())
            if self.path=='/api/pause':
                if not isinstance(body.get('paused'),bool):raise ValueError('paused must be boolean')
                self.server.ledger.pause(body['paused']);return self.js(200,self.server.state())
            self.js(404,{'error':'Not found'})
        except Conflict as e:self.js(409,{'error':str(e)})
        except (KeyError,ValueError,TypeError) as e:self.js(400,{'error':str(e)})
        except Exception:self.js(500,{'error':'Local write failed'})
    def log_message(self,fmt,*args):
        print(f'[{self.log_date_time_string()}] local {self.command} {self.path.split("?")[0]}',flush=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--port',type=int,default=8765)
    args=parser.parse_args()
    with CourtServer(args.port) as server:
        print(f'Swarm Court: http://127.0.0.1:{args.port} · synthetic demo · Claude OFF',flush=True)
        try:server.serve_forever()
        except KeyboardInterrupt:pass
