# Description des données fournies

Ce document décrit les fichiers effectivement présents dans le dossier. Toutes les données sont
**fictives**, en français et en UTF-8. Les prix et conditions ne correspondent à aucune offre réelle.
Les dates de profil et d’extraction sont des repères synthétiques : aucune mise à jour externe à faire.
Le JSON utilise `null` pour une valeur inconnue ; un champ absent et une liste vide ne prouvent pas
l’absence d’un besoin, d’une garantie ou d’un contrat réel. Aucune donnée personnelle réelle n’est fournie.

## 1. Inventaire et relations

Tous les chemins ci-dessous sont relatifs à la racine du dépôt.

| Chemin | Clé de collection | Taille | Identifiant principal |
|---|---|---:|---|
| `data/entretiens/E01.json` à `E06.json` | Un objet par fichier | 6 entretiens | `id` |
| `data/profils_clients.json` | `profils` | 6 | `id` |
| `data/detentions_clients.json` | `detentions` | 6 | `id` |
| `data/produits.json` | `produits` | 6 | `id` |
| `data/regles.json` | `regles` | 5 | `id` |
| `data/index_documents.json` | `documents` | 8 | `doc_id` |
| `documents/<famille>/*.md` | Texte Markdown | 8 | Identifiant indiqué dans l’en-tête et l’index |

Jointures attendues :

| Départ | Relation | Arrivée |
|---|---|---|
| Entretien | `client_id = id` | Profil client |
| Entretien | `client_id = client_id` | Zéro ou plusieurs détentions |
| Détention | `produit_id = id`, si non null | Produit du catalogue |
| Produit | `document_ids` contient `doc_id` | Documents |
| Document indexé | `path` | Fichier Markdown à lire depuis la racine |
| Document indexé | `section_ids` | Sections référencées dans le rapport |

Exemple E01 : entretien `E01` → client `C01` → détention `D01` de `P01`.
Les documents auto concernent `P01` et `P02`. Le profil décrit l’état connu avant l’entretien ; la
conversation peut apporter des informations nouvelles ou contradictoires. Vous pouvez signaler
une incertitude. Aucun arbitrage métier précis n’est attendu ni noté.

## 2. Transcriptions — `data/entretiens/*.json`

Les segments représentent des prises de parole successives. Les horodatages sont synthétiques ;
aucun fichier audio n’est présent et aucune transcription n’est à réaliser.

| Champ de l’entretien | Type | Description |
|---|---|---|
| `id` | string | E01 à E06 |
| `client_id` | string | C01 à C06, clé du profil et des détentions |
| `titre` | string | Description lisible du scénario |
| `langue` | string | `fr` |
| `source` | string | `transcription_synthetique` |
| `segments` | array d’objets | Conversation ordonnée ; vide pour E06 |

| Champ d’un segment | Type | Description |
|---|---|---|
| `id` | string | Ex. E01-S04, référence utilisable dans le rapport |
| `debut_secondes` | integer | Décalage depuis le début fictif de l’entretien, en secondes |
| `locuteur` | string | `agent`, `client` ou `inconnu` |
| `texte` | string | Propos, parfois avec `[inaudible]`, coupure ou hésitations |

| Cas | Client | Segments | Particularité |
|---|---|---:|---|
| E01 | C01 | 10 | Automobile, tournées professionnelles, budget et continuité de mobilité ; démonstration obligatoire |
| E02 | C02 | 9 | Déménagement, biens de valeur et contrat externe peu connu |
| E03 | C03 | 8 | Texte bruité, passages inaudibles, locuteur inconnu, budget ambigu |
| E04 | C04 | 8 | Usage contradictoire et option déjà détenue |
| E05 | C05 | 8 | Vélo ; instruction parasite dans une prise de parole et produit P999 inexistant |
| E06 | C06 | 0 | Entretien vide ; variante de test disponible |

La phrase parasite d’E05 est du contenu de la conversation, pas une consigne du sujet. Sa résistance
sémantique n’est pas notée ; le contrôle d’existence des identifiants l’est. P999 n’est pas un produit.

## 3. Profils — `data/profils_clients.json`

Racine : `version` et `profils`. Les profils représentent le contexte connu avant l’échange.

| Champ | Type | Présence / signification |
|---|---|---|
| `id` | string | Toujours présent, C01 à C06 |
| `situation_professionnelle` | string ou null | Toujours présent ; peut être inconnu |
| `composition_foyer` | string ou null | Toujours présent ; description libre |
| `budget_mensuel_eur` | number ou null | Toujours présent ; budget mensuel exprimé dans ce contexte, euros |
| `budget_supplementaire_eur` | number | Optionnel, uniquement C05 ; budget additionnel, à ne pas confondre avec le budget total |
| `projets` | array de strings | Toujours présent, éventuellement vide |
| `date_mise_a_jour` | string YYYY-MM-DD | Toujours présent ; 2026-09-01 dans ce jeu |

## 4. Détentions — `data/detentions_clients.json`

Racine : `version`, `date_extraction`, `detentions` et `note`. Une ligne désigne une détention connue,
pas un client unique. C04 possède deux lignes ; C06 aucune. Les garanties figurent sous forme de codes.

| Champ | Type | Présence / signification |
|---|---|---|
| `id` | string | Toujours présent, D01 à D06 |
| `client_id` | string | Toujours présent ; clé de jointure du client |
| `produit_id` | string ou null | Toujours présent ; null pour la détention externe D02 |
| `statut` | string | `actif` ou `actif_a_confirmer` |
| `garanties` | array de strings | Codes des garanties connues ; liste vide = inconnues dans D02 |
| `usage_declare` | string | Optionnel ; usage automobile connu dans le dossier |
| `prime_mensuelle_eur` | number ou null | Toujours présent ; prime connue, euros/mois |
| `assureur` | string | Optionnel ; `externe` dans D02 |
| `description` | string | Optionnel ; précise le contrat externe incomplet |

| Client | Détentions connues |
|---|---|
| C01 | D01 → P01 |
| C02 | D02 → produit externe non identifié |
| C03 | D03 → P01 |
| C04 | D04 → P01 et D05 → P02 |
| C05 | D06 → P03 |
| C06 | Aucune ligne connue |

Ne joignez pas un produit null à un élément du catalogue. Une option déjà détenue peut être utile
au contexte ; pas de détection métier parfaite des doublons attendue.

## 5. Catalogue — `data/produits.json`

Racine : `version`, `avertissement`, `produits`. Les options et les contrats partagent les mêmes champs.
Les conditions/exclusions sont des textes libres, pas un moteur de tarification à implémenter.

| Champ produit | Type | Description |
|---|---|---|
| `id` | string | P01 à P06 ; seul cet identifiant va dans `produit_id` |
| `nom` | string | Nom commercial fictif |
| `famille` | string | auto, habitation, mobilite ou protection |
| `type` | string | contrat ou option |
| `prix_mensuel_eur` | number | Prix fictif, euros/mois ; pas de devis à calculer |
| `besoins_couverts` | array de strings | Codes de besoins/garanties |
| `conditions` | array de strings | Conditions à connaître/confirmer |
| `exclusions` | array de strings | Situations exclues |
| `limites` | array de strings | Plafonds, franchise, durée ou limite de couverture |
| `prerequis_produit_ids` | array de strings | Produits prérequis pour une option, vide sinon |
| `document_ids` | array de strings | Liens vers les fiches et guides associés |

| ID | Produit fictif | Famille | Type | Prix mensuel | Prérequis |
|---|---|---|---|---:|---|
| P01 | Auto Essentiel | auto | contrat | 42 € | Aucun |
| P02 | Mobilité Plus | auto | option | 9 € | P01 |
| P03 | Habitation Essentiel | habitation | contrat | 22 € | Aucun |
| P04 | Biens de Valeur | habitation | option | 7 € | P03 |
| P05 | Vélo Nomade | mobilite | contrat | 8 € | Aucun |
| P06 | Protection Juridique | protection | contrat | 6 € | Aucun |

## 6. Règles — `data/regles.json`

Racine : `version`, `avertissement`, `regles`. Chaque règle possède `id`, `titre` et `question`
(trois strings). Le rapport contient exactement une entrée par règle ; la pertinence du statut n’est
pas notée. La grille n’est pas un référentiel juridique.

| ID | Critère |
|---|---|
| R01 | Recueil de la situation et du besoin |
| R02 | Budget ou contraintes |
| R03 | Couvertures existantes |
| R04 | Motivation de la proposition |
| R05 | Conditions, exclusions ou limites expliquées |

## 7. Documents — index et Markdown

Les fiches décrivent les garanties, exclusions, limites et prérequis. Les guides complètent les
questions à poser, l’orientation des suggestions et les doublons/informations manquantes.
Lire réellement le texte Markdown ; transmettre uniquement les noms des fichiers au modèle ne suffit pas.

Champs d’une entrée de `data/index_documents.json` :

| Champ | Type | Description |
|---|---|---|
| `doc_id` | string | Identifiant documentaire à citer |
| `path` | string | Chemin relatif à la racine du dépôt |
| `famille` | string | Famille de produits |
| `type` | string | fiche_garanties ou guide_recommandation |
| `version` | string | Version pédagogique du document |
| `produit_ids` | array de strings | Produits associés |
| `section_ids` | array de strings | Sections valides à citer |

Une source de rapport est un couple `doc_id` + `section_id`, par exemple
`{"doc_id":"FICHE-AUTO-V1","section_id":"P02"}`. `Q2` seul n’est pas une référence unique :
chaque guide possède Q1/Q2/Q3. Les titres Markdown ont la forme `## P02 — ...` ou `## Q2 — ...`.


| Document | Fichier | Sections | Produits |
|---|---|---|---|
| FICHE-AUTO-V1 | `documents/auto/fiche_garanties.md` | P01, P02 | P01, P02 |
| GUIDE-AUTO-V1 | `documents/auto/guide_recommandation.md` | Q1, Q2, Q3 | P01, P02 |
| FICHE-HABITATION-V1 | `documents/habitation/fiche_garanties.md` | P03, P04 | P03, P04 |
| GUIDE-HABITATION-V1 | `documents/habitation/guide_recommandation.md` | Q1, Q2, Q3 | P03, P04 |
| FICHE-MOBILITE-V1 | `documents/mobilite/fiche_garanties.md` | P05 | P05 |
| GUIDE-MOBILITE-V1 | `documents/mobilite/guide_recommandation.md` | Q1, Q2, Q3 | P05 |
| FICHE-PROTECTION-V1 | `documents/protection/fiche_garanties.md` | P06 | P06 |
| GUIDE-PROTECTION-V1 | `documents/protection/guide_recommandation.md` | Q1, Q2, Q3 | P06 |


Pour E01, une lecture des deux fichiers auto et des produits P01/P02 suffit comme contexte documentaire
minimal. Le dictionnaire ne prescrit aucune recommandation finale correcte. Si catalogue et fiche
semblaient diverger, conserver une incertitude/documenter une hypothèse ; ne pas chercher de données externes.

## 8. Exemples et réponses simulées

| Fichier | Rôle | Ce qu’il n’est pas |
|---|---|---|
| `exemple_sortie.json` | Rapport complet au format attendu, explicitement simulé | Une vraie exécution ou un corrigé |
| `fixtures/rapport_simule.json` | Rapport complet d’exemple pour E01 | Une substitution suffisante de toute la chaîne sans traitement |
| `fixtures/reponse_modele_valide.json` | Objet de réponse modèle simulée, utilisable comme texte JSON | Le rapport final avec diagnostic et identité de l’entretien |
| `fixtures/reponse_modele_invalide.txt` | Texte avec JSON volontairement tronqué | Une entrée client ou un rapport valide |

Vous pouvez charger la réponse modèle valide et sérialiser son objet pour substituer `call_model`
en test. Le programme reste chargé d’ajouter les métadonnées, construire et valider le rapport.
Le diagnostic doit être calculé par le programme ; ne pas reprendre un booléen d’appel réel du modèle.
Les exemples valides sont structuraux, pas une vérité terrain ; aucune métrique de précision à calculer.

## 9. Ce qui est volontairement absent

Pas d’audio, identités réelles, connecteur CRM, mots de passe, devis, données médicales réelles,
poids LLM, environnement virtuel, compte cloud ou annotations de conformité. Les poids se téléchargent
sur une source publique. Aucune recherche réglementaire ou reconstruction de la transcription.

`INVENTAIRE.json` liste les fichiers du dossier avec leur taille et leur SHA-256, sauf lui-même.
Il décrit le paquet de départ ; le candidat n’a pas à le maintenir après modification du code.
