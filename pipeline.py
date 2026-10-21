"""Partie à compléter. La couche HTTP est déjà fournie dans server.py."""
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'))

def load_context(entretien_id):
    """Charge les données du sujet ; le candidat choisit les documents à exploiter."""
    available = {p.stem: p for p in (ROOT/'data/entretiens').glob('*.json')}
    if entretien_id not in available:
        raise ValueError('Entretien inconnu')
    entretien = read_json(available[entretien_id])
    profils = read_json(ROOT/'data/profils_clients.json')['profils']
    detentions = read_json(ROOT/'data/detentions_clients.json')['detentions']
    index = read_json(ROOT/'data/index_documents.json')
    documents = [{**doc, 'texte': (ROOT/doc['path']).read_text(encoding='utf-8')}
                 for doc in index['documents']]
    return {'entretien': entretien,
            'profil': next(p for p in profils if p['id'] == entretien['client_id']),
            'detentions': [d for d in detentions if d['client_id'] == entretien['client_id']],
            'produits': read_json(ROOT/'data/produits.json'),
            'regles': read_json(ROOT/'data/regles.json'),
            'index_documents': index, 'documents': documents}

def call_model(prompt):
    """À implémenter : appel HTTP au moteur local, timeout et extraction du texte."""
    # LLM_BASE_URL, ex. http://127.0.0.1:8081/v1 ; LLM_MODEL, ex. local-model.
    raise NotImplementedError('Appel du modèle local à implémenter')

def analyze(entretien_id, mode=None):
    """À implémenter : contexte, prompt, modèle/simulation, parsing, validation, rapport.

    mode = reel ou simule ; sinon utiliser MODEL_MODE (défaut : reel).
    Le mode simulé ne doit appeler aucun modèle ni télécharger de poids.
    Les modes doivent partager la construction et la validation du rapport.
    """
    raise NotImplementedError('Pipeline à implémenter')
