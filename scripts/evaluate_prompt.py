import csv,sys,json,argparse
from pathlib import Path
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE))
from src.evaluation import validate_output
p=argparse.ArgumentParser();p.add_argument('--v1',required=True);p.add_argument('--v2',required=True);args=p.parse_args()
with (BASE/'data/prompt_eval.csv').open(encoding='utf-8-sig') as f: gold={r['review_id']:r for r in csv.DictReader(f)}
def collect(path,label):
  entries=[json.loads(x) for x in Path(path).read_text(encoding='utf-8').splitlines() if x.strip()]
  pred={e['review_id']:e for e in entries};rows=[]
  for rid,g in gold.items():
    e=pred.get(rid,{});val=validate_output(e.get('raw_output',''),g['review_text'])
    rows.append({'version':label,'review_id':rid,'gold':g['gold_sentiment'],'predicted':val['predicted'] or '', 'sentiment_correct':int(val['predicted']==g['gold_sentiment']), 'schema_valid':int(val['schema_valid']), 'exact_evidence':int(val['exact_evidence']), 'run_mode':e.get('run_mode','missing'),'raw_output':e.get('raw_output','')})
  return rows
rows=collect(args.v1,'v1')+collect(args.v2,'v2')
out=BASE/'outputs/prompt_comparison.csv'
with out.open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
for v in ['v1','v2']:
  r=[x for x in rows if x['version']==v];n=len(r)
  print(v,'N=',n,'accuracy=',sum(x['sentiment_correct'] for x in r),'/',n,'json=',sum(x['schema_valid'] for x in r),'/',n,'exact_evidence=',sum(x['exact_evidence'] for x in r),'/',n)
print('Wrote',out,'(semantic support still requires human annotation)')
