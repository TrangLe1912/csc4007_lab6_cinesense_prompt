"""Guided TF-IDF + cosine retriever. Provided by instructor; edit not required."""
from pathlib import Path
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

BASE=Path(__file__).resolve().parents[1]

def load_chunks(path=None):
    path=Path(path or BASE/'knowledge_base/chunks.jsonl')
    records=[json.loads(s) for s in path.read_text(encoding='utf-8').splitlines() if s.strip()]
    ids=[r['chunk_id'] for r in records]
    if len(set(ids))!=len(ids): raise ValueError('Duplicate chunk_id')
    return records

class Retriever:
    def __init__(self,chunks=None):
        self.chunks=chunks if chunks is not None else load_chunks()
        self.vectorizer=TfidfVectorizer(lowercase=True,ngram_range=(1,2),stop_words='english')
        self.matrix=self.vectorizer.fit_transform([r['text']+' '+r['doc_id'] for r in self.chunks])
    def search(self,question,top_k=3):
        if top_k<1: raise ValueError('top_k must be >=1')
        scores=cosine_similarity(self.vectorizer.transform([question]),self.matrix).ravel()
        inds=sorted(range(len(scores)),key=lambda i:(-scores[i],i))[:top_k]
        return [{**self.chunks[i],'score':round(float(scores[i]),6)} for i in inds]

def make_context(results):
    return '\n\n'.join(f"[{r['chunk_id']}] (source: {r['source_file']}) {r['text']}" for r in results)
