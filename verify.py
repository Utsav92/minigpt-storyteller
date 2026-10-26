import sys, json, re, torch
sys.argv=["x"]
exec(open("train.py",encoding="utf-8").read().split("model = GPT(")[0])
from tokenizers import Tokenizer
tok=Tokenizer.from_file("tokenizer_full.json")
def load(path):
    c=torch.load(path,map_location="cpu"); a=c["cfg"]
    m=GPT(a["d"],a["layers"],a["heads"],a["ctx"]); m.load_state_dict(c["model"]); return m.eval()
big=load("ckpt_big.pt"); small=load("ckpt.pt")
text="Once upon a time, there was a little bear named Tom.\nHe said, \"Hi!\""
ids=tok.encode(re.sub(r"\s*\n\s*"," \u00b6 ",text)).ids
with torch.no_grad(): lg=big(torch.tensor([ids]))[0,-1]
json.dump({"text":text,"ids":ids,"top":lg.topk(5).indices.tolist(),"l0":lg[:5].tolist()},open("ref.json","w"))
def dec(ids): return re.sub(r" ?\u00b6 ?","\n","".join(tok.id_to_token(i) for i in ids).replace("\u2581"," "))
for p in ["Once upon a time, there was a little bear named Tom.","One day, a big dog found a shiny red ball in the park.","A little robot wanted to make a friend."]:
    for name,m in (("SMALL",small),("BIG",big)):
        torch.manual_seed(1); x=tok.encode(p).ids
        for _ in range(110):
            with torch.no_grad(): l=m(torch.tensor([x[-190:]]))[0,-1]/0.7
            v,ix=l.topk(40); n=ix[torch.multinomial(torch.softmax(v,0),1)].item()
            if n==1: break
            x.append(n)
        print("-----",name); print(dec(x))
