# Test technique — AI Engineer senior

**Temps de travail : 90 minutes après vérification des prérequis.**
**Livrable : dépôt GitHub accessible à l’évaluateur, SHA du commit remis et lien vers son run Actions.**

## 1. Contexte

Un agent d’assurance échange avec un client. Nous souhaitons prototyper un assistant qui utilise
la transcription de cet échange pour décrire les besoins du client, examiner des critères de conseil
et suggérer des produits ou garanties à partir d’un catalogue et de documents fournis.

Vous construisez la chaîne technique complète : lecture des données → contexte documentaire → appel
à un modèle local → rapport JSON → API → tests → conteneur → déploiement local automatisé.
Les cinq critères du sujet sont pédagogiques : aucun travail de recherche juridique n’est demandé.

**Nous évaluons l’intégration et la livraison. Nous ne notons ni la justesse métier, ni le français
du modèle, ni l’exactitude des recommandations.** Un petit modèle produisant une analyse imparfaite
convient. Le résultat doit néanmoins respecter le contrat technique : types, identifiants et erreurs.

## 2. Données disponibles

Le dossier contient réellement les ensembles suivants, en UTF-8 :

| Ensemble | Volume | Utilité |
|---|---:|---|
| Transcriptions JSON | 6 entretiens, 43 segments | Source de la conversation, avec locuteurs et horodatages |
| Profils clients | 6 profils | Situation, projets et budgets connus avant l’entretien |
| Détentions clients | 6 enregistrements | Produits et garanties déjà détenus, dont un contrat externe incomplet |
| Catalogue produits | 6 produits/options | Identifiants, garanties, conditions, exclusions et prix fictifs |
| Critères de conseil | 5 règles | Grille simplifiée à représenter dans le rapport |
| Documents Markdown | 8 documents | Une fiche et un guide pour chacune des 4 familles de produits |
| Index documentaire | 8 entrées | Chemins, produits liés, versions et sections des documents |
| Réponses simulées | 3 fichiers | Aide aux tests nominaux et aux sorties mal formées |

Les chemins, champs et relations sont détaillés dans DESCRIPTION_DONNEES.md.
**E01 est le scénario obligatoire de démonstration.** E02 à E06 sont des variantes disponibles :
vous n’avez pas à démontrer leur analyse métier ni à créer un benchmark. Le code doit sélectionner
l’entretien par identifiant ; ne codez pas en dur un rapport final propre à E01.

## 3. Partie A — Réaliser le pipeline IA

Complétez le squelette ou remplacez-le par votre propre organisation.

1. Charger l’entretien demandé, retrouver son profil et filtrer ses détentions via `client_id`.
2. Construire un contexte contenant ces données, les produits, les cinq règles et le texte d’au moins
   **une fiche de garanties et un guide de recommandation** adaptés à la famille retenue. Pour E01,
   les deux documents auto constituent un choix simple. Une lecture directe ou sélection par famille
   suffit ; aucune base vectorielle ou recherche sémantique n’est imposée.
3. Effectuer au moins un véritable appel à un modèle local et **utiliser le résultat** dans l’analyse.
   Le modèle peut faire uniquement l’extraction des besoins ; les contrôles et recommandations peuvent
   ensuite être produits par du code déterministe. Un appel dont le résultat est ignoré ne suffit pas.
4. Construire et valider le rapport de FORMAT_RAPPORT.md. Référencer les segments et sections par leurs
   identifiants existants ; ne pas copier un nom de produit inventé dans `produit_id`.
5. Prévoir une substitution de la réponse du modèle pour les tests/CI. Ce mode doit réutiliser la même
   construction et validation du rapport, avec un diagnostic honnête `mode=simule`.
6. Gérer une réponse modèle mal formée : rapport `degrade` avec avertissement ou erreur applicative
   explicite. Pas de réparation automatique, de retry ou d’amélioration du prompt exigés.

L’API fournie peut être conservée :

| Requête | Résultat |
|---|---|
| `GET /health` | HTTP 200 et objet contenant `status: "ok"` quand l’application répond |
| `POST /analyze` avec `{"entretien_id":"E01"}` | HTTP 200 et rapport respectant FORMAT_RAPPORT.md |

Le service tourne par défaut sur `http://127.0.0.1:8000`. Un autre port local est accepté si le
lanceur l’affiche et le transmet au smoke test. `/health` seul ne prouve pas que le modèle fonctionne :
le test de bout en bout appelle aussi `/analyze`.

Pour le test de sortie modèle invalide, une réponse JSON dégradée en HTTP 200 ou une erreur HTTP
documentée avec corps JSON est recevable. Le test doit vérifier le comportement choisi, et non
seulement constater que `json.loads` échoue. Les cas HTTP avancés et l’entretien vide ne demandent
pas de développement supplémentaire obligatoire dans les 90 minutes ; documentez leurs limites.

## 4. Partie B — Utiliser un modèle local et gratuit

Le modèle de la démonstration doit s’exécuter sur votre machine : directement dans Python ou dans un
service local/conteneur. Aucun appel à un fournisseur LLM distant, même avec un quota gratuit, n’est
autorisé dans l’application. Aucun fallback cloud. Les poids doivent être utilisables gratuitement
sous une licence libre/permissive identifiée.

Exemples disponibles publiquement :
- `Qwen/Qwen2.5-0.5B-Instruct` avec Transformers/PyTorch local ;
- `Qwen/Qwen3-0.6B-GGUF` avec llama.cpp local, par exemple en Q8_0 ;
- `HuggingFaceTB/SmolLM2-360M-Instruct`, compact et principalement anglophone, également accepté.

Ces exemples publient leurs poids sous Apache-2.0. Vous pouvez choisir une alternative en indiquant
son URL, sa révision et sa licence. Aucun GPU obligatoire ; n’optimisez pas la précision du modèle.
Hugging Face est autorisé pour télécharger les poids. Ses services d’inférence hébergée ne satisfont
pas l’exigence locale. MODELES_LOCAUX.md et RESSOURCES.md donnent les liens et les options.

Après mise en cache des poids, images et dépendances, la génération et le redémarrage doivent fonctionner
sans accès réseau externe. Les échanges entre services locaux restent autorisés. Consignez le modèle,
sa révision, le moteur/version et le checksum du GGUF dans MODELE_ET_LICENCES.md.

## 5. Partie C — Déployer localement en une commande

Depuis un clone du dépôt, avec Python/Git/moteur de conteneurs déjà installés, l’évaluateur doit lancer :

```bash
python deploy.py
```

La commande doit automatiquement :
1. Vérifier les prérequis et signaler clairement une absence.
2. Acquérir les poids publics et images manquants, puis les conserver dans un cache local.
3. Construire l’image applicative et exécuter les tests ; les tests peuvent tourner dans l’image.
4. Démarrer l’application et le moteur du modèle. Aucun `llama-server`, `model pull`, `pip install`
   applicatif ou édition de fichier à effectuer manuellement avant cette commande.
5. Attendre avec un délai maximal documenté que les services soient disponibles.
6. Appeler `/analyze` sur E01, valider le rapport, l’enregistrer et afficher l’URL de l’API.

Après succès, les services restent démarrés et la commande peut rendre la main. En cas d’échec,
elle termine avec un code non nul et des logs utiles. Prévoir :

```bash
python deploy.py --stop
```

Cette commande arrête seulement les ressources du projet et conserve les poids en cache. Une relance
ne doit pas créer de conflit de ports ou de services. Une seule combinaison OS/moteur documentée suffit.
Docker Engine/Moby + Compose ou Podman + fournisseur Compose libre conviennent.

Une commande unique équivalente est acceptée si son mode réel, son mode CI et son arrêt sont documentés.
Une architecture à deux services Compose (application + llama.cpp) constitue une option, sans obligation.

## 6. Partie D — Automatiser avec GitHub Actions

Fournissez un workflow actif sur pull request et sur push vers `main`, qui :
1. Installe les dépendances nécessaires et exécute les tests. Un échec bloque la suite.
2. Construit l’image applicative identifiée par le commit.
3. Lance cette image avec le même mécanisme de déploiement, par exemple :

```bash
python deploy.py --ci --image assurance-ci:<SHA>
```

4. Démarre réellement le conteneur, vérifie `/health`, appelle `/analyze` et valide son JSON.
5. Retourne un échec si une vérification échoue et nettoie les services, même en échec.
6. Sur `main`, après succès, conserve l’image exacte testée, son identifiant/commit et les traces utiles
   en artefacts Actions à rétention courte. Un export OCI ou `docker save` compressé convient.

Le mode CI utilise une réponse de modèle simulée, **sans télécharger de poids**. Il partage l’orchestration
et le traitement du rapport avec le mode réel ; il peut omettre le service du modèle. Avec `--image`,
utilisez l’image indiquée déjà construite, sans reconstruire un autre artefact. GHCR est facultatif.

La CI valide le déploiement sur le runner GitHub ; elle ne déploie pas directement sur votre ordinateur.
La commande locale est la preuve du déploiement réel. La CI simulée ne remplace pas le vrai appel local.
GitHub et GitHub Actions sont les services hébergés autorisés, dans les quotas gratuits disponibles.
Les composants applicatifs, d’inférence et de déploiement choisis doivent être open source et gratuits.

## 7. Vérifications minimales à fournir

| Vérification | Attendu |
|---|---|
| Test nominal automatisé | E01 simulé produit un rapport valide ; aucun modèle/poids requis |
| Test d’erreur automatisé | Une réponse modèle mal formée déclenche le comportement explicite prévu |
| Déploiement CI | Conteneur réellement lancé et requête `/analyze` validée |
| Démonstration locale réelle | Commande unique exécutée avec vrai modèle ; prompt, brut et rapport conservés |

Le test nominal et le smoke test fournis sont des aides. Ajoutez le test de réponse modèle invalide.
La pertinence des textes générés n’est pas évaluée. Les identifiants inventés, JSON non maîtrisés,
erreurs silencieuses ou modes d’exécution mal déclarés sont des défauts techniques évaluables.

## 8. Organisation des 90 minutes

| Activité indicative | Minutes |
|---|---:|
| Lire le sujet et parcourir les données | 10 |
| Pipeline, modèle, rapport et test d’erreur | 25 |
| Conteneur et lanceur local | 20 |
| Workflow et vérification Actions | 20 |
| Démonstration réelle et preuves | 10 |
| README et remise | 5 |
| Total | 90 |

Lancez la CI tôt. À T+90, cessez les modifications et remettez l’état obtenu avec ses limites.
Un run déjà lancé peut terminer après. Les prérequis système et caches génériques peuvent être
préparés avant T0 ; aucun code de solution assurance ne doit être développé à ce stade.

## 9. Remise attendue

Placez le contenu de ce dossier à la racine du dépôt, en conservant les données de référence.
Le dépôt peut être privé si l’évaluateur y a accès. Dans votre README final, fournissez :
- commandes de déploiement réel, de test, de CI et d’arrêt ; OS/moteur pris en charge ;
- modèle, version, licence et fonctionnement du cache ;
- lien vers le run Actions et explication de la récupération/réutilisation de l’image livrée ;
- fichiers de preuve du véritable appel : prompt/contexte utile, sortie brute et rapport ;
- limites, points inachevés et usage éventuel d’assistants de code.

Conservez MODELE_ET_LICENCES.md complété. Excluez poids, caches, `.venv`, secrets et clés API.
Communiquez à l’évaluateur **URL du dépôt + SHA final + URL du run** dans le canal de remise convenu.
Vous pouvez utiliser README_SOLUTION_TEMPLATE.md pour documenter votre résultat.

## 10. Ce qui est évalué

| Dimension | Points |
|---|---:|
| Pipeline et exploitation des données/documents | 20 |
| Intégration du modèle local | 15 |
| Contrat de sortie et erreurs | 10 |
| CI GitHub Actions | 15 |
| Image et reproductibilité | 10 |
| Déploiement local automatisé | 20 |
| Qualité de la remise GitHub | 10 |
| Exactitude métier et qualité rédactionnelle du modèle | 0 |

## 11. Réponses aux questions courantes

**Faut-il une interface web ?** Non, l’API et les rapports JSON suffisent.

**Faut-il du speech-to-text, un RAG vectoriel ou du fine-tuning ?** Non. Les transcriptions existent.
Une sélection de documents par famille est suffisante et ne retire aucun point.

**Dois-je analyser les six entretiens dans les preuves ?** Non. E01 suffit pour le chemin complet.
Les autres entrées sont disponibles ; sélectionnez l’entretien par identifiant, sans figer le résultat.

**Puis-je modifier les squelettes ?** Oui, y compris l’organisation et le moteur. Conservez les
contrats ou documentez clairement les commandes équivalentes. Ne modifiez pas les données pour réussir.

**Puis-je retourner une recommandation vide ?** Oui. La liste peut être vide ; les cinq contrôles et
le reste du contrat restent présents. Un vrai appel utilisé dans le traitement demeure obligatoire.

**Et si le modèle ne produit pas le JSON demandé ?** Gérez la dégradation ou l’erreur ; pas de pénalité
sur la qualité de génération. Le cas E01 simulé doit rester valide pour tester le déploiement.

**Dois-je démontrer une connexion Internet coupée pendant les 90 minutes ?** Non, une trace réelle
et une relance hors accès externe possible suffisent à la remise. L’évaluateur pourra vérifier ensuite.

**Faut-il une image publiée dans un registre ou un déploiement cloud ?** Non. L’artefact Actions suffit.

**Internet et les assistants de code sont-ils autorisés ?** Oui. Déclarez leur usage ; l’application
livrée doit utiliser le modèle local requis et vous devez pouvoir expliquer le code.

**Si je manque de temps ?** Remettez le dépôt à T+90 et documentez ce qui fonctionne et ce qui manque.
