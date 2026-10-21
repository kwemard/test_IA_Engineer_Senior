"""Contrôle technique sans aucune évaluation de la pertinence métier."""
import argparse
import json
import math
from pathlib import Path

def require(condition, message):
    if not condition:
        raise ValueError(message)

def text(value):
    return isinstance(value, str)

def text_list(value):
    return isinstance(value, list) and all(text(v) for v in value)

def validate(report, entretien, produits, regles):
    require(isinstance(report, dict), 'Le rapport doit être un objet')
    require(report.get('entretien_id') == entretien['id'], 'entretien_id incorrect')
    require(report.get('statut_execution') in {'ok','degrade','erreur'}, 'statut_execution incorrect')
    require(text(report.get('synthese')), 'synthese doit être du texte')
    segment_ids = {s['id'] for s in entretien['segments']}
    def refs(item):
        values = item.get('segment_ids')
        require(text_list(values), 'segment_ids doit être une liste de textes')
        require(set(values) <= segment_ids, 'Référence à un segment inexistant')
    needs = report.get('besoins')
    require(isinstance(needs, list), 'besoins doit être une liste')
    for item in needs:
        require(isinstance(item, dict) and text(item.get('description')), 'Besoin mal formé')
        refs(item)
    checks = report.get('controles')
    require(isinstance(checks, list), 'controles doit être une liste')
    for item in checks:
        require(isinstance(item, dict), 'Contrôle mal formé')
        require(text(item.get('regle_id')), 'regle_id doit être du texte')
        require(item.get('statut') in {'observe','a_completer','non_verifiable','non_applicable'}, 'Statut de contrôle incorrect')
        require(text(item.get('justification')), 'Justification manquante')
        refs(item)
    wanted = {r['id'] for r in regles['regles']}
    require(len(checks) == len(wanted) and {x['regle_id'] for x in checks} == wanted,
            'Chaque règle doit apparaître exactement une fois')
    recs = report.get('recommandations')
    require(isinstance(recs, list), 'recommandations doit être une liste')
    known = {p['id'] for p in produits['produits']}
    for item in recs:
        require(isinstance(item, dict), 'Recommandation mal formée')
        require(text(item.get('produit_id')) and item['produit_id'] in known, 'Produit inconnu')
        require(text(item.get('motif')) and text_list(item.get('a_confirmer')), 'Motif ou a_confirmer mal formé')
    require(text_list(report.get('questions_a_poser')), 'questions_a_poser doit être une liste de textes')
    diag = report.get('diagnostic')
    require(isinstance(diag, dict), 'diagnostic doit être un objet')
    require(diag.get('mode') in {'reel','simule','sans_modele'}, 'Mode incorrect')
    require(text(diag.get('modele')), 'Identifiant du modèle manquant')
    require(isinstance(diag.get('appel_modele_effectue'), bool), 'appel_modele_effectue doit être booléen')
    ms = diag.get('duree_ms')
    require(type(ms) in (int, float) and math.isfinite(ms) and ms >= 0, 'duree_ms incorrect')
    require(text_list(diag.get('avertissements')), 'avertissements doit être une liste de textes')
    if report['statut_execution'] != 'ok':
        require(len(diag['avertissements']) > 0, 'Un échec doit être explicité')
    if diag['mode'] in {'simule', 'sans_modele'}:
        require(not diag['appel_modele_effectue'], 'Mode et appel réel contradictoires')

def validate_documents(report, index):
    allowed = {(d['doc_id'], sid) for d in index['documents'] for sid in d['section_ids']}
    def check_refs(refs):
        require(isinstance(refs, list), 'Sources documentaires : liste attendue')
        for ref in refs:
            require(isinstance(ref, dict), 'Source documentaire mal formée')
            require((ref.get('doc_id'), ref.get('section_id')) in allowed, 'Document ou section inconnu')
    check_refs(report.get('sources_documentaires'))
    for rec in report['recommandations']:
        check_refs(rec.get('sources'))
        require(len(rec['sources']) > 0, 'Une recommandation doit référencer une source')

def main():
    p = argparse.ArgumentParser()
    p.add_argument('rapport')
    p.add_argument('--entretien', required=True)
    p.add_argument('--data-dir', default=str(Path(__file__).parent / 'data'))
    a = p.parse_args()
    def load(path):
        return json.loads(Path(path).read_text(encoding='utf-8'))
    try:
        validate(load(a.rapport), load(a.entretien), load(Path(a.data_dir)/'produits.json'),
                 load(Path(a.data_dir)/'regles.json'))
        validate_documents(load(a.rapport), load(Path(a.data_dir)/'index_documents.json'))
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print(f'ECHEC TECHNIQUE : {exc}')
        raise SystemExit(1)
    print('FORMAT OK — aucune conclusion sur la pertinence métier ni preuve d’inférence réelle.')

if __name__ == '__main__':
    main()
