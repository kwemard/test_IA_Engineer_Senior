# À vérifier avant de lancer le chronomètre

## Prérequis système

- Python 3.11 ou plus récent, IDE et Git fonctionnels.
- Compte GitHub, capacité à créer/pousser un dépôt et Actions autorisées avec quota gratuit disponible.
  Le dépôt peut être privé si l’évaluateur y a accès ; le canal de remise des liens est celui convenu
  avec le recruteur. Ne publiez pas votre candidature uniquement pour changer de quota.
- Un moteur de conteneurs opérationnel : Docker Engine/Moby avec Compose, ou Podman et fournisseur
  Compose libre. Un seul OS/moteur documenté est accepté. Aucune installation Kubernetes.
- Accès Internet pour consulter la documentation et télécharger des fichiers publics.
- Aucun GPU, abonnement LLM, clé API d’inférence ou infrastructure cloud obligatoire.

Sous macOS/Windows, la VM éventuelle du moteur doit déjà être fonctionnelle. Aucun Docker Desktop
payant n’est imposé. Le recruteur doit permettre la résolution des problèmes de prérequis avant T0.
Les coûts du matériel/électricité ne sont pas des frais d’API demandés au candidat.

## Ce que vous pouvez préparer avant T0

Installer les prérequis, vérifier un conteneur générique, télécharger/cache un petit modèle public et
les images génériques, réaliser une génération de test générique. Aucun code de pipeline assurance,
de déploiement de la solution ou de workflow de solution ne doit être développé avant T0.
Le test de 90 minutes commence quand l’environnement est prêt et que le sujet est ouvert.

Les téléchargements peuvent être faits pendant le test, mais leur durée dépend de la connexion.
Précharger des caches génériques est autorisé pour que la bande passante n’absorbe pas l’épreuve.
La commande remise doit néanmoins savoir acquérir automatiquement tout élément applicatif manquant.

## Au moment de la remise

Après clonage, `python deploy.py` doit être la seule commande de mise en route applicative.
Les moteurs/poids ne doivent pas nécessiter de démarrage manuel. La commande d’arrêt est distincte.
Le moteur de conteneurs installé constitue un prérequis système, pas une dépendance à installer
silencieusement par le script du candidat avec des droits administrateur.

## Choisir un modèle

Lire MODELES_LOCAUX.md et RESSOURCES.md. Pour une image applicative légère, llama.cpp local avec un
fichier GGUF est une option simple. Exemple public : Qwen/Qwen3-0.6B-GGUF, Qwen3-0.6B-Q8_0.gguf.
Transformers/PyTorch local est également autorisé. Garder les contextes et générations courts.

Fixer la révision/version retenue et consigner les licences. Le sujet ne garantit pas une RAM ou une
latence identique sur tous les postes. Le recruteur doit permettre une vérification générique avant T0.
Les scripts tools/ et model_probe.py sont facultatifs ; ils ne remplacent pas l’automatisation finale.
