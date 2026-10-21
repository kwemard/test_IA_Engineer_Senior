# À lire en premier — Test technique AI Engineer senior

**Durée : 90 minutes de travail. Remise : dépôt GitHub + SHA final + lien vers le run GitHub Actions.**

Vous allez réaliser un prototype d’assistant de conseil en assurance à partir de transcriptions,
de profils clients, de contrats déjà détenus et de documents produits. Le résultat doit être
déployable sur votre machine en une commande, avec un modèle local gratuit.

## Cloner et commencer

```bash
git clone https://github.com/kwemard/test_IA_Engineer_Senior.git
cd test_IA_Engineer_Senior
python scripts/verifier_donnees.py
```

Lisez ensuite les consignes ci-dessous. Le chronomètre commence à l’ouverture du sujet, une fois
les prérequis système vérifiés. Ce dépôt fournit le sujet et les squelettes : `deploy.py` et le
pipeline sont volontairement à compléter.

Pour la remise, publiez votre travail dans votre propre dépôt GitHub et donnez l’accès à l’évaluateur,
avec le SHA final et le lien Actions. Ne modifiez pas le dépôt de référence partagé. La connexion à
votre compte GitHub et la création du dépôt vide peuvent être préparées avant le test.

Le contrôle Actions « Vérification du sujet » valide seulement l’intégrité des données et la syntaxe
des scripts de départ. Il ne remplace pas la CI/CD que vous devez réaliser dans votre dépôt.

## Ordre de lecture

1. [PREPARATION.md](PREPARATION.md) — prérequis à vérifier avant le chronomètre.
2. [INSTRUCTIONS_CANDIDAT.md](INSTRUCTIONS_CANDIDAT.md) — travail demandé, limites, temps et remise.
3. [DESCRIPTION_DONNEES.md](DESCRIPTION_DONNEES.md) — fichiers, champs, jointures et cas disponibles.
4. [FORMAT_RAPPORT.md](FORMAT_RAPPORT.md) — contrat de sortie et commandes de vérification.

Pendant le développement : [RESSOURCES.md](RESSOURCES.md), [MODELES_LOCAUX.md](MODELES_LOCAUX.md),
[AIDE_FICHIERS.md](AIDE_FICHIERS.md) et les fichiers des dossiers `data/` et `documents/`.
Avant la remise : compléter [MODELE_ET_LICENCES.md](MODELE_ET_LICENCES.md) et s’aider de
[README_SOLUTION_TEMPLATE.md](README_SOLUTION_TEMPLATE.md) pour documenter sa solution.

## Résultat attendu

Après clonage, depuis la racine du dépôt et avec les prérequis système prêts :

```bash
python deploy.py
```

Cette commande doit installer/construire les dépendances applicatives, acquérir les poids manquants,
exécuter les tests, démarrer application et modèle local, vérifier l’API puis afficher son URL.
Les squelettes de départ sont volontairement incomplets : leur réalisation constitue l’exercice.

Toutes les données sont fictives et déjà présentes dans ce dossier. Aucun audio à transcrire,
aucun accès CRM, aucun service LLM payant, aucun serveur cloud à fournir.
La justesse métier des conclusions et la qualité rédactionnelle du modèle ne sont pas notées.

## Vérification initiale des fichiers — facultative

Depuis la racine du dossier :

```bash
python scripts/verifier_donnees.py
```

Cette commande utilise uniquement la bibliothèque standard et vérifie le jeu fourni. Elle ne réalise
pas le pipeline IA et ne remplace pas vos tests. Vous pouvez modifier l’organisation du code, à
condition de conserver les données de référence et de respecter les interfaces décrites.
