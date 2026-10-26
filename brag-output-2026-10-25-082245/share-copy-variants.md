# Share copy variants (research-demo cut)

## Short (X / Bluesky)
MiniGPT Storyteller: a 5.31M-parameter LM trained from scratch to write children's stories. Runs entirely in the browser, one 14 MB file. Val perplexity 9.4. Samples are picked from 5; it repeats itself.

## Project-page / LinkedIn
**MiniGPT Storyteller** is a small decoder-only transformer trained from scratch on TinyStories to continue a story from its first sentence.

- 5.31M parameters: 6 layers, width 256, 8 heads, 192-token context
- Custom 2,048-token BPE vocabulary; about 194k training stories
- Validation loss 3.85 -> 2.24 over 2,800 steps (perplexity 9.4)
- Runs entirely in the browser as a single 14 MB HTML file: no server, no network

The three samples in the video are real outputs (temperature 0.7, top-k 40), first sentences only, each picked from five samples for the most coherent opening. It repeats itself and only knows simple children's stories.

## Facts to keep accurate in any post
- Samples are selected, not random: 6 prompts x 5 samples were generated, 3 prompts shown, best of 5 each, truncated at a sentence boundary (`samples_ex.json` holds all 30).
- Figure 1 is the real validation-loss log (12 evaluation points), not a smoothed or illustrative curve.
- Music is CC BY 4.0 and the credit is on the end card; keep it if you re-cut the video.
