import json
VALID_SENTIMENT={'positive','negative'}
VALID_CONF={'low','medium','high'}

def validate_output(raw,review_text):
    try:
        p=json.loads(raw)
    except (ValueError,TypeError): return {'schema_valid':False,'exact_evidence':False,'predicted':None}
    valid=(isinstance(p,dict) and set(['sentiment','evidence','short_explanation','confidence']).issubset(p)
           and p.get('sentiment') in VALID_SENTIMENT and p.get('confidence') in VALID_CONF
           and isinstance(p.get('short_explanation'),str)
           and isinstance(p.get('evidence'),list) and len(p['evidence'])>0
           and all(isinstance(e,str) and e.strip() for e in p['evidence']))
    exact=valid and all(e in review_text for e in p['evidence'])
    return {'schema_valid':bool(valid),'exact_evidence':bool(exact),'predicted':p.get('sentiment') if valid else None}
