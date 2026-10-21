"""Téléchargement générique AVANT le test ; aucun appel d’inférence hébergé."""
import argparse, json
from pathlib import Path

MODELS = ['Qwen/Qwen2.5-0.5B-Instruct', 'Qwen/Qwen3-0.6B',
          'HuggingFaceTB/SmolLM2-360M-Instruct']

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--model', choices=MODELS, default=MODELS[0])
    parser.add_argument('--manifest', default='modele_local.json')
    args=parser.parse_args()
    from huggingface_hub import HfApi, snapshot_download
    info=HfApi().model_info(args.model)
    revision=info.sha
    if not revision: raise RuntimeError('Révision du modèle introuvable')
    local=snapshot_download(repo_id=args.model, revision=revision,
        allow_patterns=['*.json','*.safetensors','tokenizer.model','*.txt','LICENSE*','README.md'])
    manifest={'model_id':args.model,'revision':revision,'local_path':str(Path(local).resolve()),
              'license':'Apache-2.0','source':'https://huggingface.co/'+args.model}
    Path(args.manifest).write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    print('Poids téléchargés. Manifeste : '+args.manifest)
    print('Aucune génération ni API d’inférence distante utilisée.')

if __name__=='__main__': main()
