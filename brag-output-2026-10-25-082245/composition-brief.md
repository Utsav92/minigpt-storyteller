# Hyperframes Composition Brief: MiniGPT Storyteller (research-demo cut)

## Objective
Create a short research-demo-style video for MiniGPT Storyteller: model card, one real figure, three real samples, limitations.

## Output
- Composition directory: `brag-output-2026-10-25-082245/composition/`
- Rendered video: `brag-output-2026-10-25-082245/brag.mp4`
- Format: landscape — 1920x1080, 30 fps
- Duration: 25 seconds

## Source Material
- Project root: `C:\Users\Utsav\minigpt-stories`
- Primary files read: `train_big.log` (validation-loss points), `samples_ex.json` (30 real samples: 6 prompts x 5), `export.py` output / `train.py` (architecture), `template.html` (product copy)
- Product name: MiniGPT Storyteller
- Strongest claim: "A tiny GPT trained from scratch on TinyStories. It runs entirely in your browser, with no server and no network."
- Key visual moments: Figure 1 (real validation-loss curve), three large model answers
- Copy that must appear verbatim (all real model output, first sentences only, picked from 5 samples each):
  - Prompt 1 "Once upon a time, there was a little bear named Tom." -> "Tom was a very curious boy who liked to explore new places in the woods. One day, Tom found a big tree. He knew it was a good spot to watch."
  - Prompt 2 "Lily and her mom went to the garden to plant flowers." -> "Lily saw a big pile of flowers and squirrels. She wanted to pick them, but her mom said no. Lily was sad and hurt."
  - Prompt 3 "One day, a girl named Mia found a magic door in the forest." -> "She was so excited and wanted to open it. But she couldn't find it anywhere. Mia asked her mom if she could. Her mom said no."
- Numbers (all measured): 5.31M parameters; 6 layers, width 256, 8 heads, context 192 tokens; vocabulary 2,048 (BPE); about 194k TinyStories stories; validation loss 3.85 (step 250) -> 2.24 (step 2,800), perplexity 9.4; 14 MB single HTML file; sampling settings temperature 0.7, top-k 40

## Creative Direction
- Tone preset: polished
- Creative direction: research demo / project page — calm, exact, understated
- Hook: title card complete at frame 0; the parameter count is in the first line of text
- Outro: limitations stated plainly, then the title lockup
- Avoid: hype, comparisons to other models, any mention of the hardware it was trained on, claims beyond the numbers above

## Visual Identity
- Background #f7f5ef, ink #17171c, dim #5f5f6b, rules #d6d2c6, accent #1d3fcf
- Display EB Garamond; body Inter; data JetBrains Mono (bundled)
- Visual references: paper-white project page, hairline rules, monospace prompts, blue model output, a plain line chart with dots

## Storyboard
See `brag-plan.md`.
1. Title — 3.27s
2. Model card — 5.47s (count-up, spec rows, Figure 1)
3. Samples — 13.1s (three 4.37s panels starting on the 8.74 / 13.11 / 17.47 strong cues)
4. Limitations + close — 3.16s (limitations land on 22.37)

## Audio
- Role: calm bed with sparse accents
- Music: `happy-beats-business-moves-vol-12-by-ende-dot-app.mp3`, credit "Music: Sascha Ende, ende.app (CC BY 4.0)" shown on the end card
- Music treatment: volume 0.30, fade-in 0.4s, fade-out 1s
- Cue guidance: `C:\Users\Utsav\.claude\skills\brag\assets\music\cues\happy-beats-business-moves-vol-12-by-ende-dot-app.music-cues.md` (strong cues 8.74, 13.11, 17.47, 22.37). Mark `// beat-locked` / `// beat-grid`.
- Audio-reactive: subtle breathing "running" dot beside each sample tag, from pre-extracted RMS
- SFX: keypress ticks (prompt typing), soft drop (table rows), one soft bong (22.37). Copy to `composition/assets/sfx/`.

## Hyperframes Instructions
Build with HyperFrames conventions (paused GSAP timeline per composition on `window.__timelines`, deterministic only, one scene per sub-composition). The Hyperframes skills are read from the cloned repo rather than installed. `npx hyperframes check` is the gate; keep creation and rendering local, no publishing, and pass `--describe false` to `snapshot` (it otherwise uploads frames to Gemini when `GEMINI_API_KEY` is set).
