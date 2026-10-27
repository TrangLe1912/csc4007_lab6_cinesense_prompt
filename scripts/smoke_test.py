from pathlib import Path
import sys,csv
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE))
from src.retriever import Retriever,load_chunks

def rows(p):
    with p.open(encoding='utf-8-sig',newline='') as f: return list(csv.DictReader(f))
for part,n in [('dev',5),('eval',10),('stress',5)]:
    data=rows(BASE/f'data/prompt_{part}.csv')
    assert len(data)==n, (part,len(data))
    assert all(r['gold_sentiment'] in {'positive','negative'} for r in data)
    assert all(r['source_type']=='synthetic_teaching_example' for r in data)
chunks=load_chunks();assert len(chunks)==20
qa=rows(BASE/'data/qa_questions.csv');assert len(qa)==12
r=Retriever(chunks)
top=r.search('What does RP01 say about slow pacing?',3)
assert len(top)==3
print('PASS: 5 dev + 10 eval + 5 stress; 12 QA; 10 packs/20 chunks; TF-IDF retrieval works')
print('Top chunks:',[(e['chunk_id'],e['score']) for e in top])
