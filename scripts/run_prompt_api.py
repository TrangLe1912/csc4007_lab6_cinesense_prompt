"""Optional real API inference; requires explicit provider setup and permission."""
from pathlib import Path
import csv,json,sys,argparse,datetime
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE))
from src.llm_adapter import chat
p=argparse.ArgumentParser();p.add_argument('--version',choices=['v1','v2'],required=True);p.add_argument('--split',choices=['dev','eval'],default='eval');args=p.parse_args()
with (BASE/f'data/prompt_{args.split}.csv').open(encoding='utf-8-sig') as f:reviews=list(csv.DictReader(f))
t=(BASE/f'prompts/prompt_{args.version}.txt').read_text(encoding='utf-8')
out=BASE/f'outputs/prompt_runs_{args.version}_{args.split}_api.jsonl'
with out.open('w',encoding='utf-8') as f:
 for r in reviews:
  raw=chat('Return only the requested answer format.',t.replace('{review_text}',r['review_text']))
  result={'review_id':r['review_id'],'prompt_version':args.version,'raw_output':raw,'run_mode':'api_live_inference','timestamp':datetime.datetime.now(datetime.timezone.utc).isoformat()}
  f.write(json.dumps(result,ensure_ascii=False)+'\n')
print('Wrote',out)
