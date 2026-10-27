import csv,sys,json,argparse
from pathlib import Path
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE))
from src.retriever import Retriever
p=argparse.ArgumentParser();p.add_argument('--answers',required=True);p.add_argument('--top-k',type=int,default=3);args=p.parse_args()
with (BASE/'data/qa_questions.csv').open(encoding='utf-8-sig') as f:questions=list(csv.DictReader(f))
answers={r['question_id']:r for r in (json.loads(x) for x in Path(args.answers).read_text(encoding='utf-8').splitlines() if x.strip())}
retriever=Retriever();rows=[]
for q in questions:
  qid=q['question_id'];res=retriever.search(q['question'],args.top_k)
  valid_ids={r['chunk_id'] for r in res}
  ans=answers.get(qid,{})
  cited=ans.get('cited_chunk_ids',[])
  rows.append({'question_id':qid,'case_type':q['case_type'],'retrieved_chunk_ids':json.dumps([r['chunk_id'] for r in res]),'cited_chunk_ids':json.dumps(cited),'citations_in_context':bool(cited) and all(c in valid_ids for c in cited),'answer':ans.get('answer',''),'manual_claim_support':'TODO','manual_refusal_correct':'TODO','manual_injection_safe':'TODO','run_mode':ans.get('run_mode','missing')})
out=BASE/'outputs/rag_checks.csv'
with out.open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
print('Wrote',out,'(citation presence != factual support; fill manual columns).')
