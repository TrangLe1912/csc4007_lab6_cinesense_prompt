import csv,sys,json,argparse
from pathlib import Path
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE))
from src.retriever import Retriever,make_context
p=argparse.ArgumentParser();p.add_argument('--top-k',type=int,default=3);args=p.parse_args()
with (BASE/'data/qa_questions.csv').open(encoding='utf-8-sig') as f:qa=list(csv.DictReader(f))
r=Retriever()
out=BASE/'outputs/rag_contexts.jsonl'
with out.open('w',encoding='utf-8') as f:
  for q in qa:
    hits=r.search(q['question'],args.top_k)
    entry={'question_id':q['question_id'],'question':q['question'],'case_type':q['case_type'],'retrieved_chunk_ids':[h['chunk_id'] for h in hits],'context':make_context(hits),'run_mode':'retrieval_only'}
    f.write(json.dumps(entry,ensure_ascii=False)+'\n')
print('Wrote',out)
