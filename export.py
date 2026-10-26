"""Bake a checkpoint + tokenizer into one self-contained HTML file; also dump a reference for JS validation."""
import sys, json, base64, math, numpy as np, torch
ck = sys.argv[1] if len(sys.argv) > 1 else "ckpt.pt"
out = sys.argv[2] if len(sys.argv) > 2 else "minigpt_storyteller.html"
c = torch.load(ck, map_location="cpu")
a = c["cfg"]; sd = c["model"]
order = ["tok.weight", "pos.weight"]
for l in range(a["layers"]):
    for n in ["ln1.weight", "ln1.bias", "qkv.weight", "qkv.bias", "proj.weight", "proj.bias",
              "ln2.weight", "ln2.bias", "fc.weight", "fc.bias", "out.weight", "out.bias"]:
        order.append(f"blocks.{l}.{n}")
order += ["lnf.weight", "lnf.bias"]
flat = np.concatenate([sd[k].numpy().astype(np.float16).ravel() for k in order])
nparams = sum(v.numel() for v in sd.values())
cfg = {"d": a["d"], "layers": a["layers"], "heads": a["heads"], "ctx": a["ctx"], "vocab": 2048,
       "params": "%.2fM" % (nparams / 1e6), "val": "%.3f" % c["val"], "ppl": "%.1f" % math.exp(c["val"]), "step": c["step"]}
tok = open("tok_web.json", encoding="utf-8").read()
html = open("template.html", encoding="utf-8").read()
html = html.replace("__CFG__", json.dumps(cfg)).replace("__TOK__", tok) \
           .replace("__WEIGHTS__", base64.b64encode(flat.tobytes()).decode())
open(out, "w", encoding="utf-8").write(html)
print("wrote", out, "%.1f MB" % (len(html) / 1e6), cfg)
