# Share copy variants

All numbers are measured from the actual run (train_big.log, export output). Nothing here claims more than that.

## Short (X / Bluesky)
Trained a tiny GPT from scratch on a laptop CPU (3.7 h, no GPU). It writes kids' stories offline in one 14 MB HTML file. Val perplexity 9.4. It repeats itself and I'm leaving that in.

## LinkedIn
I wanted to see how small a GPT can be and still write something readable, so I trained one from scratch on an Intel i5-8250U laptop with no GPU.

- 5.31M parameters (6 layers, width 256), custom 2,048-token BPE
- Trained on about 194k TinyStories stories, 2,800 steps in 3.7 hours
- Validation loss 2.241 (perplexity 9.4)
- Runs entirely in the browser as a single 14 MB HTML file: no server, no network

It writes fluent children's-story sentences, then repeats itself ("The red ball hit the ball and the red ball."). That sentence is real model output and it is in the video.

## Honest caveats to keep in any post
- It is a toy: it can only write simple children's stories (TinyStories), not answer questions.
- The "~540 tokens/s" figure was measured in headless Chrome on the same laptop; the video shows streaming slowed down.
- The story shown streaming is a real sample from the model (temperature 0.7, top-k 40), cut to its first three sentences.

## Required credit (music is CC BY 4.0)
Music: Sascha Ende, ende.app (CC BY 4.0) — "Happy Beats / Business Moves Vol. 1". Put this in the post, the video description, or the video itself. The bundled SFX are CC0.
