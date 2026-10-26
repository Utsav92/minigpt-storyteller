import json, subprocess, numpy as np, re
from tokenizers import Tokenizer
tok = Tokenizer.from_file("tokenizer_full.json")
prompt = "Once upon a time, there was a little bear named Tom."
cont = "Tom loved to play with his toy cars and trucks. One day, he went to the park and saw a big red car. Tom wanted to play with it and make it gold."
words = cont.split(" ")
base = len(tok.encode(prompt).ids)
counts = [len(tok.encode(prompt + " " + " ".join(words[:i+1])).ids) - base for i in range(len(words))]
# music RMS, 12 samples/s over 24 s
ff = "ffmpeg"
raw = subprocess.run([ff, "-v", "error", "-i", "brag-output/composition/assets/music/happy-beats-business-moves-vol-1-by-ende-dot-app.mp3",
                      "-t", "25", "-ac", "1", "-ar", "22050", "-f", "f32le", "-"], capture_output=True).stdout
x = np.frombuffer(raw, dtype=np.float32); sr = 22050; hop = sr // 12
rms = np.array([np.sqrt(np.mean(x[i:i+hop] ** 2)) for i in range(0, 25 * sr, hop)])[:300]
rms = np.convolve(rms, np.ones(3) / 3, mode="same")
rms = np.clip(rms / np.percentile(rms, 95), 0, 1)
json.dump({"words": words, "counts": counts, "rms": [round(float(v), 3) for v in rms]}, open("brag-output/data.json", "w"))
print(len(words), "words;", counts[-1], "tokens;", len(rms), "rms samples; min/max", rms.min().round(2), rms.max().round(2))
