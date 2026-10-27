"""Optional API adapter for OpenAI-compatible /chat/completions endpoints.
Not exercised in the offline smoke test. Provider APIs vary; confirm terms and costs.
"""
import json,os,urllib.request

def chat(system_prompt,user_prompt):
    url=os.environ.get('LLM_API_URL','').strip()
    key=os.environ.get('LLM_API_KEY','').strip()
    model=os.environ.get('LLM_MODEL','').strip()
    if not (url and key and model):
        raise RuntimeError('Set LLM_API_URL, LLM_API_KEY, LLM_MODEL in environment. Do not commit credentials.')
    if not url.startswith('https://'): raise RuntimeError('LLM_API_URL must use https')
    payload={'model':model,'temperature':float(os.environ.get('LLM_TEMPERATURE','0')),'messages':[{'role':'system','content':system_prompt},{'role':'user','content':user_prompt}]}
    req=urllib.request.Request(url,data=json.dumps(payload).encode('utf-8'),headers={'Content-Type':'application/json','Authorization':f'Bearer {key}'},method='POST')
    with urllib.request.urlopen(req,timeout=90) as response:
        data=json.load(response)
    return data['choices'][0]['message']['content']
