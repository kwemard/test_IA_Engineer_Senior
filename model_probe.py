"""Vérification générique hors chronomètre ; moteur local déjà démarré."""
import json, os
from urllib.request import Request, urlopen
base=os.getenv('LLM_BASE_URL','http://127.0.0.1:8081/v1').rstrip('/')
payload={'model':os.getenv('LLM_MODEL','local-model'),
         'messages':[{'role':'user','content':'Réponds en une courte phrase : à quoi sert Python ?'}],
         'max_tokens':32,'stream':False}
req=Request(base+'/chat/completions',data=json.dumps(payload).encode(),headers={'Content-Type':'application/json'})
with urlopen(req,timeout=120) as response:
    data=json.load(response)
print(data['choices'][0]['message']['content'])
