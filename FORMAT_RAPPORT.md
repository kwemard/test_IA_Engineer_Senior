# Contrat technique du rapport

Tous les champs ci-dessous sont requis dans un rapport. Des champs supplémentaires sont acceptés.
Référence lisible : `exemple_sortie.json`. Schéma de structure : `schemas/rapport.schema.json`.
Validateur fourni : `check_output.py`, qui vérifie aussi les références aux données.
Le schéma est informatif : vous pouvez réutiliser le validateur sans installer jsonschema.

## 1. Objet racine

| Champ | Type | Contrainte |
|---|---|---|
| entretien_id | string | Identifiant de l’entretien demandé |
| statut_execution | string | ok, degrade ou erreur |
| synthese | string | Texte libre ; pas de longueur imposée |
| besoins | array d’objets | Liste éventuellement vide, voir ci-dessous |
| controles | array de 5 objets | Une fois chacune des règles R01 à R05 |
| recommandations | array d’objets | Liste éventuellement vide |
| sources_documentaires | array d’objets | Sections des documents exploitées, couples existants |
| questions_a_poser | array de strings | Liste éventuellement vide |
| diagnostic | objet | Métadonnées calculées par le programme |

`ok` : traitement terminé avec rapport exploitable ; `degrade` : résultat partiel ou fallback
technique explicité ; `erreur` : rapport d’échec structuré si ce choix d’API est retenu.
Les statuts techniques ne sont pas des verdicts de conformité.

## 2. Sous-objets

| Liste / objet | Champs requis | Contraintes |
|---|---|---|
| besoins[] | description: string ; segment_ids: array de strings | Les segments cités existent dans l’entretien |
| controles[] | regle_id: string ; statut: string ; justification: string ; segment_ids: array de strings | Chaque règle exactement une fois, segments existants |
| recommandations[] | produit_id: string ; motif: string ; a_confirmer: array de strings ; sources: array d’objets | Produit du catalogue ; au moins une source par recommandation |
| sources[] et sources_documentaires[] | doc_id: string ; section_id: string | Couple présent dans l’index documentaire |

Les listes `segment_ids` peuvent être vides quand aucune preuve n’est disponible. Les listes de
besoins, recommandations et questions peuvent être vides ; les cinq contrôles restent présents.

Statuts autorisés des contrôles :
- `observe` : élément considéré comme présent dans l’échange ;
- `a_completer` : information ou étape à compléter ;
- `non_verifiable` : éléments insuffisants pour conclure ;
- `non_applicable` : critère considéré non applicable au cas analysé.

Ce sont des statuts pédagogiques ; leur justesse n’est pas évaluée. La structure et les références le sont.

## 3. Diagnostic

| Champ | Type | Règle |
|---|---|---|
| mode | string | reel, simule ou sans_modele |
| modele | string | Identifiant réel du modèle, ou nom explicite de fixture ; peut être vide sans modèle |
| appel_modele_effectue | boolean | true seulement si un appel d’inférence réel a effectivement été tenté |
| duree_ms | number | Durée mesurée de l’analyse, >= 0 ; zéro autorisé dans un exemple |
| avertissements | array de strings | Au moins un message si statut_execution n’est pas ok |

`reel` : chemin d’inférence réelle sélectionné. Un timeout tenté peut produire un rapport dégradé
avec appel_modele_effectue=true, mais ne remplace pas une génération réellement obtenue dans la
démonstration. `simule` : réponse substituée, appel_modele_effectue=false. `sans_modele` : aucun appel,
par exemple entrée refusée, appel_modele_effectue=false. Ne pas faire remplir ce booléen par le LLM.

## 4. Sources documentaires

Le contexte du cas nominal doit comprendre une fiche et un guide réellement lus. Consigner les
sections exploitées dans sources_documentaires et garder le prompt/contexte utile dans les preuves.
Une recommandation a ses propres sources. Aucun score de pertinence de citation n’est calculé.
L’existence du couple doc_id/section_id est contrôlée ; l’identifiant d’un fichier seul ne suffit pas.

Exemple de source valide :

```json
{"doc_id": "FICHE-AUTO-V1", "section_id": "P02"}
```

## 5. Erreurs

Le chemin nominal E01 simulé retourne HTTP 200 et un rapport conforme. Pour la réponse modèle invalide,
vous pouvez produire un rapport dégradé conforme ou une erreur HTTP avec corps JSON et comportement
documenté/testé. Une erreur silencieuse ou un succès CI malgré l’échec du smoke n’est pas acceptable.
Si une erreur HTTP est retournée, elle n’a pas à respecter le schéma du rapport de succès.

## 6. Commandes de vérification

Depuis la racine du dépôt, sur un rapport enregistré :

```bash
python check_output.py exemple_sortie.json --entretien data/entretiens/E01.json
python check_output.py preuves/rapport_reel.json --entretien data/entretiens/E01.json
```

Le validateur n’atteste ni une inférence réelle ni une conclusion métier correcte.
Sur une API déjà démarrée :

```bash
python scripts/smoke.py --expect-mode reel --output preuves/rapport_reel.json
python scripts/smoke.py --expect-mode simule --output preuves/rapport_ci.json
```

Choisir la commande correspondant au mode actif. Le smoke appelle /health et /analyze, vérifie la
structure, les références et le mode annoncé. Le lanceur final doit appeler cette vérification
automatiquement ; la commande manuelle ci-dessus sert au diagnostic. Options --url, --startup-timeout
et --request-timeout disponibles pour adapter port et délais à la machine.
