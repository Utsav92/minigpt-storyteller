import sys, re, torch
sys.argv=["x"]
exec(open("train.py",encoding="utf-8").read().split("model = GPT(")[0])
from tokenizers import Tokenizer
c=torch.load("ckpt.pt",map_location="cpu"); a=c["cfg"]
m=GPT(a["d"],a["layers"],a["heads"],a["ctx"]); m.load_state_dict(c["model"]); m.eval()
tok=Tokenizer.from_file("tokenizer_full.json"); torch.manual_seed(1)
for p in ["Once upon a time, there was a little bear named Tom.","One day, a big dog found a shiny red ball in the park.","A little robot wanted to make a friend."]:
    ids=tok.encode(p.replace("\n"," ¶ ")).ids
    for _ in range(150):
        with torch.no_grad(): lg=m(torch.tensor([ids[-190:]]))[0,-1]/0.7
        v,ix=lg.topk(40); pr=torch.softmax(v,0); n=ix[torch.multinomial(pr,1)].item()
        if n==1: break
        ids.append(n)
    print("-----"); print(tok.decode(ids).replace(" ¶ ","\n"))
