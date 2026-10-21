"""Génération générique CPU sur fichiers locaux ; pas de logique assurance."""
import argparse, json, os, time
from pathlib import Path

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--manifest',default='modele_local.json')
    args=parser.parse_args()
    cfg=json.loads(Path(args.manifest).read_text(encoding='utf-8'))
    local=Path(cfg['local_path'])
    if not local.is_dir(): raise FileNotFoundError('Télécharger le modèle avant cette étape')
    os.environ['HF_HUB_OFFLINE']='1'
    os.environ['TRANSFORMERS_OFFLINE']='1'
    import torch, transformers
    from transformers import AutoTokenizer, AutoModelForCausalLM
    start=time.perf_counter()
    tokenizer=AutoTokenizer.from_pretrained(str(local), local_files_only=True, trust_remote_code=False)
    model=AutoModelForCausalLM.from_pretrained(str(local), local_files_only=True,
        trust_remote_code=False, torch_dtype=torch.float32).to('cpu').eval()
    prompt=tokenizer.apply_chat_template(
        [{'role':'user','content':'Explique en une phrase à quoi sert Python.'}],
        tokenize=False,add_generation_prompt=True,enable_thinking=False)
    batch=tokenizer(prompt,return_tensors='pt')
    with torch.inference_mode():
        output=model.generate(**batch,max_new_tokens=64,do_sample=False,
                              pad_token_id=tokenizer.eos_token_id)
    generated=output[0,batch['input_ids'].shape[-1]:]
    print(tokenizer.decode(generated,skip_special_tokens=True))
    print(json.dumps({'model_id':cfg['model_id'],'revision':cfg['revision'],
        'device':'cpu','local_files_only':True,'torch':torch.__version__,
        'transformers':transformers.__version__,'duration_s':round(time.perf_counter()-start,2)}))

if __name__=='__main__': main()
