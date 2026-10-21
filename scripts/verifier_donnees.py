"""Vérifie les données pédagogiques et les exemples ; aucune inférence et aucune dépendance tierce."""
from pathlib import Path
import json, sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from check_output import validate, validate_documents

def load(relative): return json.loads((ROOT/relative).read_text(encoding='utf-8'))
def require(condition,message):
    if not condition: raise ValueError(message)

def main():
    profiles=load('data/profils_clients.json')['profils']
    holdings=load('data/detentions_clients.json')['detentions']
    products=load('data/produits.json')
    rules=load('data/regles.json')
    index=load('data/index_documents.json')
    profile_ids={p['id'] for p in profiles}
    product_ids={p['id'] for p in products['produits']}
    docs={d['doc_id']:d for d in index['documents']}
    require(len(profile_ids)==len(profiles),'Profil dupliqué')
    require(len(product_ids)==len(products['produits']),'Produit dupliqué')
    require(len(docs)==len(index['documents']),'Document dupliqué')
    segments=set(); interviews=[]
    for path in sorted((ROOT/'data/entretiens').glob('*.json')):
        e=json.loads(path.read_text(encoding='utf-8')); interviews.append(e)
        require(path.stem==e['id'],'ID entretien / fichier incohérent')
        require(e['client_id'] in profile_ids,'Profil client absent')
        for segment in e['segments']:
            require(segment['id'] not in segments,'Segment dupliqué')
            segments.add(segment['id'])
            require(segment['locuteur'] in {'agent','client','inconnu'},'Locuteur inconnu')
    for h in holdings:
        require(h['client_id'] in profile_ids,'Détention sans client')
        require(h['produit_id'] is None or h['produit_id'] in product_ids,'Détention sans produit')
    for p in products['produits']:
        require(set(p['prerequis_produit_ids'])<=product_ids,'Prérequis produit inexistant')
        require(set(p['document_ids'])<=set(docs),'Document produit inexistant')
    for d in index['documents']:
        body=(ROOT/d['path']).read_text(encoding='utf-8')
        require(set(d['produit_ids'])<=product_ids,'Document lié à un produit absent')
        for section in d['section_ids']:
            require(f'## {section} —' in body,'Section Markdown absente')
    e01=next(e for e in interviews if e['id']=='E01')
    for name in ['exemple_sortie.json','fixtures/rapport_simule.json']:
        report=load(name)
        validate(report,e01,products,rules)
        validate_documents(report,index)
        require(report['diagnostic']['mode']=='simule','Exemple annoncé réel')
        require(not report['diagnostic']['appel_modele_effectue'],'Exemple avec faux appel réel')
    try:
        json.loads((ROOT/'fixtures/reponse_modele_invalide.txt').read_text(encoding='utf-8'))
    except json.JSONDecodeError: pass
    else: raise ValueError('La fixture invalide est devenue valide')
    print(f'OK : {len(interviews)} entretiens, {len(segments)} segments, {len(profiles)} profils, '
          f'{len(holdings)} détentions, {len(product_ids)} produits, {len(rules["regles"])} règles, '
          f'{len(docs)} documents ; références et exemples cohérents.')

if __name__=='__main__':
    try: main()
    except (ValueError,KeyError,OSError) as exc:
        print('ERREUR : '+str(exc)); raise SystemExit(1)
