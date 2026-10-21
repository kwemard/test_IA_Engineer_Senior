# Exemples vérifiés de modèles locaux — 20 octobre 2026

Ces dépôts éditeurs publient leurs poids sous **Apache-2.0** et permettent une utilisation locale sans
facturation à la requête. Nous décrivons précisément des poids sous licence permissive ; cela ne
constitue pas une certification d’ouverture de toutes les données et méthodes d’entraînement.

| Modèle | Taille approximative | Intérêt pour cet exercice |
|---|---:|---|
| Qwen/Qwen2.5-0.5B-Instruct | 0,49 milliard de paramètres | Choix de départ proposé : petit modèle instruction, famille multilingue incluant le français |
| Qwen/Qwen3-0.6B | 0,6 milliard | Autre petit modèle multilingue ; désactiver le mode thinking pour limiter la génération |
| HuggingFaceTB/SmolLM2-360M-Instruct | 360 millions | Option compacte ; principalement anglophone, donc moins adaptée aux échanges français mais recevable pour évaluer l’intégration |

Les petits modèles peuvent produire une analyse médiocre ; elle n’est pas notée. Ils peuvent fonctionner
sur CPU via un moteur adapté, sans garantie de latence ou de mémoire identique sur tous les postes.
Ne pas choisir un grand modèle simplement pour améliorer la synthèse au détriment des 90 minutes.

## Utiliser Hugging Face sans API payante

Hugging Face Hub sert au **téléchargement des poids**. La bibliothèque open source Transformers permet
ensuite de les charger et de générer sur la machine avec PyTorch. Le téléchargement préalable utilise
Internet ; l’inférence finale n’a pas besoin de joindre Hugging Face. Préférer une révision immuable.
Les trois modèles sont publics ; aucune offre d’inférence hébergée n’est nécessaire.

Les services Hugging Face Inference Providers/Endpoints, une application web ou un notebook exécutant
le modèle sur une machine distante ne satisfont pas l’exigence d’inférence locale, même avec un quota
gratuit. Ne pas utiliser InferenceClient pour une inférence distante dans cette épreuve.

Autre option : des poids GGUF compatibles avec llama.cpp/llama-server, obtenus auprès d’une source
identifiée. Consigner le modèle d’origine, la révision, la quantification, la licence et le checksum.
Une distribution quantifiée ne doit pas être présumée libre simplement parce qu’elle est téléchargeable.

## Références officielles

- https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct
- https://huggingface.co/Qwen/Qwen3-0.6B
- https://huggingface.co/HuggingFaceTB/SmolLM2-360M-Instruct
- https://huggingface.co/docs/transformers/installation
- https://github.com/huggingface/transformers/blob/main/LICENSE
- https://github.com/ggml-org/llama.cpp/blob/master/LICENSE

Les licences des versions réellement utilisées doivent être consignées. L’absence de coût d’inférence
ne supprime pas les obligations de licence ou les coûts du matériel/électricité. Aucune facturation de
service ni souscription payante n’est requise pour ce chemin local.

## Option prête à télécharger pour Compose

Le dépôt éditeur https://huggingface.co/Qwen/Qwen3-0.6B-GGUF fournit notamment
Qwen3-0.6B-Q8_0.gguf sous Apache-2.0. Il peut être utilisé avec llama.cpp local. La commande de déploiement
doit acquérir les poids manquants, les mettre en cache et démarrer le moteur automatiquement. Consigner
révision du dépôt et checksum ; ne pas imposer de conversion manuelle des poids pendant le test.
