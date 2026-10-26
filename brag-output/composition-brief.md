# Hyperframes Composition Brief: MiniGPT Storyteller

## Objective
Create a short launch-style brag video for MiniGPT Storyteller.

## Output
- Composition directory: `brag-output/composition/`
- Rendered video: `brag-output/brag.mp4`
- Format: landscape — 1920x1080
- Duration: 24 seconds

## Source Material
- Project root: `C:\Users\Utsav\minigpt-stories`
- Primary files read: `template.html` (the page's markup, CSS variables and copy), `minigpt_storyteller_big.html` (the shipped page, same UI), `train_big.log` / `export.py` output (model facts)
- Product name: MiniGPT Storyteller
- Tagline / strongest claim: "A tiny GPT trained from scratch on TinyStories. It runs entirely in your browser, with no server and no network."
- Key UI or visual moment to recreate: the prompt card (textarea, four sliders, amber "Generate story" button) and the output card with gold streamed text and the stats line
- Copy that must appear verbatim:
  - "MiniGPT Storyteller"
  - "A tiny GPT trained from scratch on TinyStories. It runs entirely in your browser, with no server and no network."
  - "Once upon a time, there was a little bear named Tom."
  - "Generate story"
  - Real model continuation: "Tom loved to play with his toy cars and trucks. One day, he went to the park and saw a big red car. Tom wanted to play with it and make it gold."
  - Real model sentence for the punchline: "The red ball hit the ball and the red ball."
- Numbers that may appear (all measured): 5.31M parameters; validation perplexity 9.4 (loss 2.241, step 2,800); 3.7 h training on an Intel i5-8250U laptop CPU (no GPU); 14 MB single offline HTML file; ~540 tokens/s generation in the browser (543.7 measured in headless Chrome)

## Creative Direction
- Tone preset: default
- Creative direction: honest tiny-model brag, a proud build with the flaw left in
- Interpretation: playful and clean, comfortable holds, humor from the real repeated sentence. No claim on screen exceeds the numbers above.
- Angle: See `brag-plan.md`. The flex is real (a whole GPT trained from scratch on a laptop CPU, running offline in a web page) and the flaw is shown, not hidden.
- Hook: giant typed line "I trained a GPT from scratch." then "On a laptop CPU. No GPU."
- Outro / punchline: the real repeated sentence, the caption "It repeats itself. I'm leaving it in.", then the final card "MiniGPT Storyteller / Runs entirely in your browser."
- Avoid:
  - Generic SaaS language
  - Abstract filler visuals
  - Unrelated visual redesign
  - Any claim not in the lists above (no "state of the art", no "GPT-4 level", no speed claims beyond ~540 tokens/s)

## Visual Identity
- Background: #14131a
- Text: #ece9f7 (dim #9a96b5)
- Accent: #ffb454 (amber); secondary #7ee0c3 (mint); generated text gold #ffd9a0
- Panels: #1e1c27, inputs #262434, borders #34314a
- Display font: Segoe UI (the page's stack: "Segoe UI", system-ui, sans-serif)
- Body font: Segoe UI
- Visual references from the project: dark card UI, amber Generate button, mint slider readouts, gold streamed text with blinking amber cursor, uppercase letter-spaced field labels

## Storyboard
Use the storyboard in `brag-output/brag-plan.md` as the creative contract.

Scene summary:
1. Hook — 3.0s — typed "I trained a GPT from scratch." then "On a laptop CPU. No GPU."
2. Reveal — 3.5s — recreated page UI slides up on the 3.02s beat; cursor clicks "Generate story" at ~6.0s
3. The flow — 7.0s — gold story streams word by word; tokens counter ticks; "(shown slowed down)" note
4. The numbers — 4.5s — three stat cards at 14.02s, 15.52s, 17.02s (third on the strong cue)
5. Punchline — 6.0s — typed real sentence, honest caption, final title card landing on the 22.01s strong cue

## Audio
- Audio role: warm bed with sparse professional accents
- Audio arc: music fades in under the typing, stays steady as a bed, one bell on the final card, fade-out in the last second
- Music: `happy-beats-business-moves-vol-1-by-ende-dot-app.mp3` (credit: "Music: Sascha Ende, ende.app (CC BY 4.0)")
- Music treatment: starts at 0.0s, volume ~0.35, fade-in 0.4s, fade-out 23.0–24.0s
- Music cue guidance: bundled preset at `C:\Users\Utsav\.claude\skills\brag\assets\music\cues\happy-beats-business-moves-vol-1-by-ende-dot-app.music-cues.md` (and `.json`). 120.19 BPM, beat ≈ 0.5s. Strong-cue locks: 17.02s, 22.01s. Beat-grid: 3.02s; stat cards 14.02s / 15.52s / 17.02s. Mark with `// beat-locked` and `// beat-grid` comments.
- Audio-reactive treatment: subtle; the amber glow behind the stat cards and final title breathes with music RMS (pre-extracted per-frame, seek-safe). No waveform/equalizer visuals. If extraction is unavailable, skip and say so.
- Audio-coupled moments:
  - Hook typing — quiet randomized keyboard ticks
  - Button press at ~6.0s — soft click
  - Stat cards — card-slide sounds; third card gets a slightly heavier accent on the strong cue
  - Quote typing — quiet keyboard ticks
  - Final title at 22.01s — one bell
- SFX selection guidance: low high-frequency-risk files for repeated sounds (typing, clicks); medium-risk card-slide for three card arrivals; one bell for the logo payoff. Silence under the caption read (19.6–21.8s).
- SFX analysis guidance: `C:\Users\Utsav\.claude\skills\brag\assets\sfx\sfx-analysis.md`
- Exact SFX choice: chosen after the animation exists, by timing and character.
- Audio files: copy the chosen music and SFX into `brag-output/composition/assets/`

## Hyperframes Instructions
Build in `brag-output/composition/` using HyperFrames conventions (paused GSAP timeline registered on `window.__timelines`, `data-start`/`data-duration`, `class="clip"`, deterministic logic only). The Hyperframes skills are not installed in this environment, so the CLI docs (`npx hyperframes docs ...`) and the scaffold's `AGENTS.md` are the contract. Skip storyline/SPEC steps; the brag plan and this brief replace them.

Requirements:
- Show at least one real UI, copy, or visual element from the source project.
- Keep all text readable in the final render.
- Keep the video at 24 seconds (within 15-25).
- Include the planned music/SFX layer.
- Treat music cue metadata as optional timing hints; ignore cues that hurt readability.
- Run `npx hyperframes check` before render — it is the single gate.
- Keep creation and rendering local. No publishing.
