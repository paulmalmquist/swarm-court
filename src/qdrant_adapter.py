"""Optional LOCAL semantic candidate adapter. Integration-test at work before use.
No hosted embeddings and no automatic model download. This adapter deliberately
requires an explicit set of allowed artifact IDs and cached approved weights.
Fuse candidates with the authoritative registry/FTS service, then re-read sources.
"""
from __future__ import annotations
import uuid
from pathlib import Path
from urllib.parse import urlparse

class LocalSemanticIndex:
    def __init__(self,url:str,cache_dir:Path,collection:str='paul_os_context',
                 model_name:str='BAAI/bge-small-en-v1.5',api_key:str|None=None):
        parsed=urlparse(url)
        if parsed.scheme not in ('http','https') or parsed.hostname not in ('127.0.0.1','localhost','::1'):
            raise ValueError('Only an explicitly approved loopback Qdrant endpoint is accepted')
        if not cache_dir.exists(): raise ValueError('Provision approved model weights first; no automatic download')
        try:
            from qdrant_client import QdrantClient,models
            from fastembed import TextEmbedding
        except ImportError as exc:
            raise RuntimeError('Install optional packages from the approved work package source') from exc
        self.models=models
        self.embedder=TextEmbedding(model_name=model_name,cache_dir=str(cache_dir),
                                   local_files_only=True,threads=2)
        self.client=QdrantClient(url=url,api_key=api_key,timeout=10)
        self.collection=collection; self.model_name=model_name
        dimension=len(next(iter(self.embedder.embed(['dimension check']))))
        if not self.client.collection_exists(collection):
            self.client.create_collection(collection,vectors_config=models.VectorParams(size=dimension,distance=models.Distance.COSINE))
        else:
            info=self.client.get_collection(collection)
            config=info.config.params.vectors
            if getattr(config,'size',None)!=dimension:
                raise ValueError('Existing index dimension differs; do not overwrite it')
    def upsert(self,chunks:list[dict]):
        if not chunks: return
        required={'chunk_id','artifact','sha256','text','start','end','scope','lifecycle'}
        for c in chunks:
            if not required.issubset(c): raise ValueError('Missing provenance or scope metadata')
        vectors=self.embedder.passage_embed([c['text'] for c in chunks])
        points=[self.models.PointStruct(id=str(uuid.uuid5(uuid.NAMESPACE_URL,c['chunk_id'])),
                  vector=v.tolist(),payload=dict(c,embedding_model=self.model_name)) for c,v in zip(chunks,vectors)]
        self.client.upsert(collection_name=self.collection,points=points,wait=True)
    def delete_artifact(self,artifact_id:str):
        f=self.models.Filter(must=[self.models.FieldCondition(key='artifact',match=self.models.MatchValue(value=artifact_id))])
        self.client.delete(collection_name=self.collection,points_selector=self.models.FilterSelector(filter=f),wait=True)
    def search(self,query:str,allowed_artifacts:list[str],limit:int=12)->list[dict]:
        if not allowed_artifacts: return []
        f=self.models.Filter(must=[
            self.models.FieldCondition(key='artifact',match=self.models.MatchAny(any=allowed_artifacts)),
            self.models.FieldCondition(key='lifecycle',match=self.models.MatchValue(value='Active'))])
        vector=next(iter(self.embedder.query_embed(query))).tolist()
        result=self.client.query_points(collection_name=self.collection,query=vector,
            query_filter=f,limit=min(limit,30),with_payload=True)
        return [dict(p.payload or {},score=p.score) for p in result.points]
