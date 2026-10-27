import csv,sys,json,argparse
from pathlib import Path
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE))
from src.retriever import Retriever
p=argparse.ArgumentParser();p.add_argument('--top-k',type=int,default=3);args=p.parse_args()
with (BASE/'data/qa_questions.csv').open(encoding='utf-8-sig') as f:qa=list(csv.DictReader(f))
r=Retriever();rows=[]
for q in qa:
  result=r.search(q['question'],args.top_k)
  rows.append({'question_id':q['question_id'],'case_type':q['case_type'],'top_k':args.top_k,'retrieved_chunk_ids':json.dumps([x['chunk_id'] for x in result]),'scores':json.dumps([x['score'] for x in result])})
out=BASE/f'outputs/retrieval_top{args.top_k}.csv';out.parent.mkdir(parents=True,exist_ok=True)
with out.open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
print('Wrote',out)
