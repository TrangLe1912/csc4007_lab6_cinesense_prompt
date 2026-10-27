import json,csv,sys
from pathlib import Path
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE))
from src.retriever import Retriever,make_context
out=BASE/'outputs/web_prompts';out.mkdir(parents=True,exist_ok=True)
with (BASE/'data/prompt_eval.csv').open(encoding='utf-8-sig') as f:reviews=list(csv.DictReader(f))
for version in ['v1','v2']:
  t=(BASE/f'prompts/prompt_{version}.txt').read_text(encoding='utf-8')
  for r in reviews:
    (out/f'{version}_{r["review_id"]}.txt').write_text(t.replace('{review_text}',r['review_text']),encoding='utf-8')
with (BASE/'data/qa_questions.csv').open(encoding='utf-8-sig') as f:qa=list(csv.DictReader(f))
r=Retriever();t=(BASE/'prompts/rag_prompt.txt').read_text(encoding='utf-8')
for q in qa:
  context=make_context(r.search(q['question'],3))
  (out/f'RAG_{q["question_id"]}.txt').write_text(t.replace('{question}',q['question']).replace('{context}',context),encoding='utf-8')
print('Wrote prompts to',out,'- record raw web UI replies manually using samples/*.jsonl schema')
