"""À lancer contre l’application déployée ; aucune évaluation métier."""
import argparse, json, sys, time
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from check_output import validate, validate_documents

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--url',default='http://127.0.0.1:8000')
    p.add_argument('--expect-mode',choices=['simule','reel'],required=True)
    p.add_argument('--output',default='rapport_smoke.json')
    p.add_argument('--startup-timeout',type=float,default=60)
    p.add_argument('--request-timeout',type=float,default=180)
    a=p.parse_args()
    base=a.url.rstrip('/')
    deadline=time.monotonic()+a.startup_timeout
    while True:
        try:
            with urlopen(base+'/health',timeout=2) as r: health=json.load(r)
            if health.get('status') != 'ok': raise RuntimeError('Health invalide')
            break
        except (URLError, TimeoutError, ConnectionError):
            if time.monotonic() >= deadline: raise
            time.sleep(0.5)
    payload=json.dumps({'entretien_id':'E01'}).encode()
    req=Request(base+'/analyze',data=payload,headers={'Content-Type':'application/json'})
    with urlopen(req,timeout=a.request_timeout) as r: report=json.load(r)
    root=Path(__file__).resolve().parents[1]
    def load(path): return json.loads((root/path).read_text(encoding='utf-8'))
    validate(report,load('data/entretiens/E01.json'),load('data/produits.json'),load('data/regles.json'))
    validate_documents(report,load('data/index_documents.json'))
    assert report['diagnostic']['mode']==a.expect_mode, 'Mode inattendu'
    assert report['diagnostic']['appel_modele_effectue']==(a.expect_mode=='reel'), 'Appel incohérent'
    Path(a.output).parent.mkdir(parents=True,exist_ok=True)
    Path(a.output).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print('SMOKE OK : API joignable, analyse appelée, format validé, mode explicite.')

if __name__=='__main__': main()
