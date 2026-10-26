# MiniGPT Storyteller

A 5.31M-parameter decoder-only GPT (6 layers, width 256, 8 heads, 192-token context) trained from scratch on TinyStories with a custom 2,048-token BPE. Validation loss 2.24 (perplexity 9.4). It continues a children's story from its first sentence. It repeats itself and only knows simple stories.

`minigpt_storyteller_big.html` is the whole model in one 14 MB file: open it in a browser, no server needed.

## Files
- `prep.py`: builds the tokenizer and the token files from TinyStories
- `train.py`: model and training loop (PyTorch, CPU)
- `export.py` + `template.html`: bake a checkpoint into the self-contained HTML
- `verify.py`: checks the JS model against PyTorch
- `ckpt_big.pt`: trained 5.31M checkpoint
- `train_big.log`: training log
- `samples_ex.json`: 30 real samples (6 prompts x 5)
- `brag-output-2026-10-25-082245/`: research-demo video (`brag.mp4`) and its Hyperframes project

## Data
Download TinyStories (valid and train) and run `prep.py`. The data files are not in this repo.

Demo video music: Sascha Ende, ende.app (CC BY 4.0).
