import json, re, subprocess, numpy as np
log = open("../train_big.log", encoding="utf-8", errors="replace").read()
val = [(int(a), float(b)) for a, b in re.findall(r"^== step (\d+) val_loss ([\d.]+)", log, re.M)]
S = json.load(open("../samples_ex.json", encoding="utf-8"))
def first_sentences(text, n):
    parts = re.findall(r"[^.!?\"]+[.!?]+\"?", text.replace("\n", " "))
    return " ".join(p.strip() for p in parts[:n])
pick = [  # (prompt, sample index, sentences kept): chosen from 5 samples per prompt for the most coherent opening
    ("Once upon a time, there was a little bear named Tom.", 3, 3),
    ("Lily and her mom went to the garden to plant flowers.", 2, 3),
    ("One day, a girl named Mia found a magic door in the forest.", 0, 4)]
samples = [{"prompt": p, "answer": first_sentences(S[p][i], k)} for p, i, k in pick]
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", "composition/assets/music/happy-beats-business-moves-vol-12-by-ende-dot-app.mp3",
                      "-t", "25", "-ac", "1", "-ar", "22050", "-f", "f32le", "-"], capture_output=True).stdout
x = np.frombuffer(raw, dtype=np.float32); sr = 22050; hop = sr // 12
rms = np.array([np.sqrt(np.mean(x[i:i+hop] ** 2)) for i in range(0, 25 * sr, hop)])[:300]
rms = np.convolve(rms, np.ones(3) / 3, mode="same"); rms = np.clip(rms / np.percentile(rms, 95), 0, 1)
json.dump({"val": val, "samples": samples, "rms": [round(float(v), 3) for v in rms]}, open("data.json", "w", encoding="utf-8"))
print("val points:", val[0], "...", val[-1], len(val))
for s in samples: print(len(s["answer"].split()), "words |", s["prompt"], "=>", s["answer"])
