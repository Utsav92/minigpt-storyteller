import os, sys, time, math, json, argparse
import numpy as np, torch, torch.nn as nn, torch.nn.functional as F

p = argparse.ArgumentParser()
p.add_argument("--d", type=int, default=256)
p.add_argument("--layers", type=int, default=6)
p.add_argument("--heads", type=int, default=8)
p.add_argument("--ctx", type=int, default=256)
p.add_argument("--bs", type=int, default=32)
p.add_argument("--steps", type=int, default=4000)
p.add_argument("--lr", type=float, default=2e-3)
p.add_argument("--threads", type=int, default=8)
p.add_argument("--bench", type=int, default=0)
p.add_argument("--out", default="ckpt.pt")
p.add_argument("--init", default="")
a = p.parse_args()
torch.set_num_threads(a.threads)
torch.manual_seed(0); np.random.seed(0)
V = 2048

class Block(nn.Module):
    def __init__(s, d, h):
        super().__init__()
        s.h = h
        s.ln1 = nn.LayerNorm(d); s.qkv = nn.Linear(d, 3 * d); s.proj = nn.Linear(d, d)
        s.ln2 = nn.LayerNorm(d); s.fc = nn.Linear(d, 4 * d); s.out = nn.Linear(4 * d, d)
    def forward(s, x):
        B, T, C = x.shape
        q, k, v = s.qkv(s.ln1(x)).split(C, dim=2)
        q, k, v = [t.view(B, T, s.h, C // s.h).transpose(1, 2) for t in (q, k, v)]
        y = F.scaled_dot_product_attention(q, k, v, is_causal=True)
        x = x + s.proj(y.transpose(1, 2).reshape(B, T, C))
        return x + s.out(F.gelu(s.fc(s.ln2(x))))

class GPT(nn.Module):
    def __init__(s, d, L, h, ctx):
        super().__init__()
        s.tok = nn.Embedding(V, d); s.pos = nn.Embedding(ctx, d)
        s.blocks = nn.ModuleList([Block(d, h) for _ in range(L)])
        s.lnf = nn.LayerNorm(d)
        s.apply(s._init)
        for n, p_ in s.named_parameters():
            if n.endswith("proj.weight") or n.endswith("out.weight"):
                nn.init.normal_(p_, std=0.02 / math.sqrt(2 * L))
    def _init(s, m):
        if isinstance(m, (nn.Linear, nn.Embedding)):
            nn.init.normal_(m.weight, std=0.02)
            if getattr(m, "bias", None) is not None: nn.init.zeros_(m.bias)
    def forward(s, idx, targets=None):
        T = idx.shape[1]
        x = s.tok(idx) + s.pos(torch.arange(T))
        for b in s.blocks: x = b(x)
        logits = s.lnf(x) @ s.tok.weight.T          # tied output head
        if targets is None: return logits
        return F.cross_entropy(logits.view(-1, V), targets.view(-1))

model = GPT(a.d, a.layers, a.heads, a.ctx)
if a.init:
    model.load_state_dict(torch.load(a.init)["model"]); print("resumed from", a.init)
print("params: %.2fM" % (sum(p_.numel() for p_ in model.parameters()) / 1e6), flush=True)

tr = np.memmap("train.bin", dtype=np.uint16, mode="r")
va = np.memmap("val.bin", dtype=np.uint16, mode="r")
def batch(data, bs):
    ix = np.random.randint(0, len(data) - a.ctx - 1, bs)
    x = np.stack([data[i:i + a.ctx] for i in ix]).astype(np.int64)
    y = np.stack([data[i + 1:i + a.ctx + 1] for i in ix]).astype(np.int64)
    return torch.from_numpy(x), torch.from_numpy(y)

decay = [p_ for n, p_ in model.named_parameters() if p_.dim() >= 2]
nodecay = [p_ for n, p_ in model.named_parameters() if p_.dim() < 2]
opt = torch.optim.AdamW([{"params": decay, "weight_decay": 0.1}, {"params": nodecay, "weight_decay": 0}],
                        lr=a.lr, betas=(0.9, 0.95))
warm = max(50, a.steps // 40)
def lr_at(i):
    if i < warm: return a.lr * (i + 1) / warm
    r = (i - warm) / max(1, a.steps - warm)
    return a.lr * (0.05 + 0.95 * 0.5 * (1 + math.cos(math.pi * r)))

@torch.no_grad()
def evaluate():
    model.eval(); ls = []
    for _ in range(20):
        x, y = batch(va, 32); ls.append(model(x, y).item())
    model.train(); return float(np.mean(ls))

if a.bench:
    t = time.time()
    for i in range(a.bench):
        x, y = batch(tr, a.bs); loss = model(x, y); loss.backward(); opt.step(); opt.zero_grad()
    dt = (time.time() - t) / a.bench
    print("%.2fs/step, %d tok/s" % (dt, a.bs * a.ctx / dt)); sys.exit()

t0 = time.time()
for i in range(a.steps):
    for g in opt.param_groups: g["lr"] = lr_at(i)
    x, y = batch(tr, a.bs)
    loss = model(x, y); loss.backward()
    torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
    opt.step(); opt.zero_grad(set_to_none=True)
    if i % 50 == 0:
        print("step %d/%d loss %.3f lr %.2e  %.0fs" % (i, a.steps, loss.item(), lr_at(i), time.time() - t0), flush=True)
    if (i + 1) % 250 == 0 or i + 1 == a.steps:
        vl = evaluate()
        print("== step %d val_loss %.4f (ppl %.2f)" % (i + 1, vl, math.exp(vl)), flush=True)
        torch.save({"cfg": vars(a), "model": model.state_dict(), "step": i + 1, "val": vl}, a.out)
print("done", time.time() - t0)
