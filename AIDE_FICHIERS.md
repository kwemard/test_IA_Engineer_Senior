# À quoi servent les fichiers de départ ?

Les fichiers de code constituent des aides facultatives. Vous pouvez les réorganiser ou les remplacer.
Les données de référence et les contrats décrits restent ceux de l’exercice.

| Fichier | État initial | Travail attendu |
|---|---|---|
| pipeline.py | Chargeur de contexte fourni ; call_model/analyze non implémentés | Pipeline et intégration locale |
| server.py | Transport HTTP minimal opérationnel | Réutiliser ou adapter ; il délègue l’analyse au pipeline |
| check_output.py | Validateur technique fourni | Réutiliser ou intégrer les contrôles |
| scripts/smoke.py | Test HTTP fourni | Appeler depuis le lanceur et la CI |
| scripts/verifier_donnees.py | Vérification du jeu fourni | Aide facultative, aucune logique IA |
| tests/test_pipeline.py | Test nominal fourni, échoue tant que le pipeline manque | Conserver/adapter et ajouter le test d’erreur |
| deploy.py | Arguments fournis ; logique non implémentée | Orchestration réelle/simulée et arrêt |
| Dockerfile | Squelette incomplet | Image applicative avec données/documents |
| compose.yaml.example | Exemple non actif | Renommer/adapter si Compose choisi, ou fournir équivalent |
| .github/workflows/ci.yml.example | Exemple non actif, TODO échouant volontairement | Renommer en ci.yml et implémenter |
| tools/prepare_hf_model.py | Téléchargement générique optionnel | Aide pour Transformers local, à intégrer/adapter si choisi |
| tools/probe_hf_local.py | Génération CPU générique optionnelle | Vérification avant T0, pas une preuve de la solution assurance |
| model_probe.py | Appel générique d’un serveur local déjà lancé | Aide ponctuelle ; le lanceur final doit lancer le serveur lui-même |
| schemas/rapport.schema.json | Contrat de structure informatif | Référence ; pas de bibliothèque JSON Schema obligatoire |

La commande `python -m unittest discover -s tests -v` échoue initialement avec NotImplementedError.
C’est attendu. Les fichiers `.example` ne sont pas pris en compte automatiquement par les outils.
Le serveur fourni est un transport de prototype ; aucune qualité de serveur de production n’est exigée.

## Paramètres d’exécution suggérés

| Paramètre | Valeur de départ | Usage |
|---|---|---|
| MODEL_MODE | reel ou simule | Choix du chemin d’inférence |
| LLM_BASE_URL | http://llm:8080/v1 dans Compose | Adresse du service local, si appel HTTP |
| LLM_MODEL | local-model | Alias du modèle local |
| PORT | 8000 | Port interne du serveur fourni |
| APP_IMAGE | assurance-local:dev | Image de l’application dans l’exemple Compose |
| MODEL_DIR | ./models | Cache local du fichier GGUF dans l’exemple Compose |

Le lanceur doit définir les valeurs nécessaires et fournir un défaut utilisable. L’évaluateur ne doit
pas créer manuellement un .env ou découvrir une clé secrète. À l’intérieur d’un conteneur, localhost
désigne ce conteneur : utiliser le nom du service du modèle si celui-ci est dans un autre conteneur.
Ne jamais faire pointer ces paramètres vers un service LLM distant dans le chemin réel.
