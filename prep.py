"""Build tokenizer + tokenized train/val arrays from TinyStories text."""
import re, json, numpy as np
from tokenizers import Tokenizer, models, trainers, pre_tokenizers

EOS = "<eos>"

def clean(story):
    s = story.strip()
    s = re.sub(r"\s*\n\s*", " ¶ ", s)   # newline -> pilcrow word
    s = re.sub(r"[ \t]+", " ", s)
    return s

def load(path, drop_last):
    txt = open(path, encoding="utf-8", errors="replace").read()
    parts = txt.split("<|endoftext|>")
    if drop_last:
        parts = parts[:-1]
    out = [clean(p) for p in parts if p.strip()]
    return out

stories = load("valid.txt", False) + load("train_part.txt", True)
print("stories", len(stories))

tok = Tokenizer(models.BPE(unk_token="<unk>"))
tok.pre_tokenizer = pre_tokenizers.Metaspace(replacement="▁", prepend_scheme="always")
trainer = trainers.BpeTrainer(vocab_size=2048, special_tokens=["<unk>", EOS], min_frequency=2)
tok.train_from_iterator(stories[:150000], trainer)
tok.save("tokenizer_full.json")
print("vocab", tok.get_vocab_size())

ids = []
B = 5000
for i in range(0, len(stories), B):
    for e in tok.encode_batch(stories[i:i+B]):
        ids.extend(e.ids); ids.append(1)
arr = np.array(ids, dtype=np.uint16)
print("tokens", len(arr), "unk frac", float((arr == 0).mean()))
nval = 400_000
arr[:-nval].tofile("train.bin"); arr[-nval:].tofile("val.bin")

# compact tokenizer for the browser
d = json.load(open("tokenizer_full.json", encoding="utf-8"))
vocab = d["model"]["vocab"]
inv = [None] * len(vocab)
for t, i in vocab.items(): inv[i] = t
merges = [m if isinstance(m, str) else " ".join(m) for m in d["model"]["merges"]]
json.dump({"vocab": inv, "merges": merges}, open("tok_web.json", "w", encoding="utf-8"), ensure_ascii=False)
print("sample:", tok.encode(stories[0][:120]).tokens[:20])
