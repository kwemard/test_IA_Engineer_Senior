# Ressources publiques utilisables pendant l’épreuve

Documentation Internet et téléchargements autorisés. Aucun achat ni service d’inférence hébergé requis.

| Besoin | Ressource officielle |
|---|---|
| Workflow GitHub Actions | https://docs.github.com/en/actions/writing-workflows |
| Artefacts de CI | https://docs.github.com/en/actions/using-workflows/storing-workflow-data-as-artifacts |
| Conditions d’usage gratuit | https://docs.github.com/en/billing/concepts/product-billing/github-actions |
| Docker Engine Linux | https://docs.docker.com/engine/install/ |
| Compose | https://docs.docker.com/compose/gettingstarted/ |
| Podman | https://podman.io/docs/installation |
| Fournisseur Compose Podman | https://docs.podman.io/en/latest/markdown/podman-compose.1.html |
| llama.cpp conteneur CPU | https://github.com/ggml-org/llama.cpp/blob/master/docs/docker.md |
| API du serveur local | https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md |
| Poids GGUF officiels Qwen | https://huggingface.co/Qwen/Qwen3-0.6B-GGUF |
| Transformers local/hors ligne | https://huggingface.co/docs/transformers/installation |

Exemple de fichier public pour le téléchargement automatique :
https://huggingface.co/Qwen/Qwen3-0.6B-GGUF/resolve/main/Qwen3-0.6B-Q8_0.gguf

Cette URL de découverte utilise main. Dans la remise, remplacer main par une révision immuable et
consigner le checksum. De même, fixer la version/digest du moteur : une étiquette server/latest
facilite la découverte mais ne garantit pas une reproduction à l’identique dans le temps.

Les moteurs et poids du chemin proposé sont sous licences libres/permissives. GitHub et Hugging Face
sont des plateformes de distribution/hébergement autorisées ; ne pas les qualifier de plateformes
intégralement open source. Aucun service HF Inference Providers/Endpoints ne doit générer la réponse.
