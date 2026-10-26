# Brag Plan: MiniGPT Storyteller

## What is this app?
A 5.31M-parameter GPT trained from scratch on TinyStories (on a laptop CPU, no GPU) that writes children's stories entirely in your browser: one offline 14 MB HTML file, no server, no network.

## The angle
Tiny model, honest brag. The flex is real: a whole GPT, trained from scratch in 3.7 hours on an i5-8250U laptop, running offline in a web page. The joke is the model itself: it writes fluent children's-story sentences and then repeats itself ("the red ball hit the ball and the red ball"). The video puts a real output line on screen and owns the flaw instead of hiding it. Specific to this project because every number and the quoted sentence are measured or sampled from the actual model (val loss 2.241 / perplexity 9.4 at step 2,800).

## Hook (first 2-3 seconds)
Giant type, typed character by character with key ticks: "I trained a GPT from scratch." Then, smaller, fading up: "On a laptop CPU. No GPU." The claim earns the next 20 seconds because it sounds like it should not be possible.

## Key moments (the middle)
- The real page UI recreated: the "MiniGPT Storyteller" header, the prompt box already holding "Once upon a time, there was a little bear named Tom.", the four sliders, and the amber "Generate story" button. A cursor clicks it.
- The story streaming in word by word in warm gold after the white prompt, with the live stats line ("Generated N tokens · ~540 tokens/s") counting up.
- Three stat cards arriving one by one: 5.31M parameters (val perplexity 9.4), 3.7 h on a laptop CPU, 14 MB one offline HTML file.

## Outro / punchline
A real sampled sentence typed out: "The red ball hit the ball and the red ball." Then the dim caption "It repeats itself. I'm leaving it in." Final card on the strong beat: "MiniGPT Storyteller" / "Runs entirely in your browser."

## User flow worth showing
1. Entry: the prompt box with a ready prompt and the sliders.
2. Key action: click "Generate story".
3. Result: the story streams in, tokens/s counter ticks, a Stop button is visible.

## Tone
- Preset: default
- Creative direction: honest tiny-model brag, a proud build with the flaw left in
- Interpretation: playful and clean with comfortable holds. The humor comes from the real repeated sentence, not from jokes added on top. No overselling. Nothing on screen claims more than the numbers support.

## Format: landscape — 1920x1080
## Duration: 25 seconds (revised from 24, see "Revision notes" at the end)

## Visual identity (from the project)
- Background: #14131a
- Panel: #1e1c27 (inputs #262434, borders #34314a)
- Accent: #ffb454 (amber), secondary accent #7ee0c3 (mint, used for slider readouts)
- Text: #ece9f7 (dim #9a96b5, generated-text gold #ffd9a0)
- Display font: Segoe UI (the page's own stack: "Segoe UI", system-ui, sans-serif)
- Body font: Segoe UI
- Strongest visual element: the dark card UI with the amber Generate button and the gold streamed text

## Share copy (draft)
I trained a 5.3M-parameter GPT from scratch on a laptop CPU in 3.7 hours. It writes children's stories in your browser, offline, in one 14 MB HTML file. It also repeats itself, and I'm leaving that in.

## Audio direction
- Role: warm bed with sparse professional accents
- Music: happy-beats-business-moves-vol-1-by-ende-dot-app.mp3 (120.19 BPM)
- Music treatment: starts at 0.0s, volume ~0.35, fade-in over the first 0.4s, fade-out from 23.0s to 24.0s; music ducks nothing (no voiceover)
- Music cue guidance: preset read (`assets/music/cues/happy-beats-business-moves-vol-1-by-ende-dot-app.music-cues.md`). Tempo 120.19 BPM, beat every ~0.5s. Strong-cue locks: 17.02s (third stat card lands), 22.01s (title card + bell). Beat-grid: UI slide-in at 3.02s; stat cards at 14.02s, 15.52s, 17.02s (every third beat, because they are text).
- Audio-reactive treatment: subtle; amber glow behind the stat cards and the final title breathes with music RMS. No waveform or equalizer visuals.
- SFX posture: moderate, motion-matched, low high-frequency-risk picks where repeated
- Audio-coupled moments: hook typing (key ticks), cursor click on "Generate story", streamed words (sparse ticks), stat cards (card sounds, third card on the 17.02s strong cue), quote typing, final title (bell on 22.01s)
- Restraint rule: no SFX over the 19.6-21.8s caption read; music never above 0.4

## Storyboard

### Scene 1 — Hook — 3.0s
Near-black field. Line 1 types out in huge text: "I trained a GPT" then the accent-colored "from scratch." (0.2–1.7s). At 1.9s the smaller line fades up: "On a laptop CPU. No GPU." Everything settled and readable from 2.4s to the cut. (Hook line read floor ~1.5s: met. Second line ~1.0s: met.)
Sequential/interaction: yes — the headline types character by character.
Audio intent: curious, confident; the music bed comes in under the typing.
Audio-coupled idea: subtle key ticks per typed character (randomized keyboard samples, quiet).
Music: warm bed fades in.
Transition mood: clean wipe → Scene 2

### Scene 2 — Reveal — 3.5s
The recreated MiniGPT Storyteller page slides up on the 3.02s beat: title "Mini**GPT** Storyteller" (GPT in amber), the subtitle verbatim ("A tiny GPT trained from scratch on TinyStories. It runs entirely in your browser, with no server and no network."), the prompt card with the real default prompt, the four sliders (Temperature 0.70, Top-k 40, Top-p 0.95, Max new tokens 150), and the amber "Generate story" button. A cursor travels to the button and clicks at ~6.0s.
Sequential/interaction: yes — simulated cursor click on "Generate story" (button press state).
Audio intent: tidy, satisfying "here it is".
Audio-coupled idea: soft click on the press at 6.0s.
Music: bed continues.
Transition mood: clean → Scene 3 (the page scrolls down to the output card, no hard cut)

### Scene 3 — The flow — 7.0s
The output card fills below the prompt: the white prompt text, then the real model continuation streams in gold, word by word: "Tom loved to play with his toy cars and trucks. One day, he went to the park and saw a big red car. Tom wanted to play with it and make it gold." A blinking amber cursor trails the text. The stats line counts up: "Generated N tokens · ~540 tokens/s", with a small dim note "(shown slowed down)". The Stop button is visible but unused. The whole sentence is fully settled for at least 1.5s before the cut. (Real copy: the continuation is an actual sampled output of this model; the page itself generates it at ~540 tokens/s, far faster than the video shows.)
Sequential/interaction: yes — words stream in one by one; tokens counter ticks up.
Audio intent: gentle, "it's alive".
Audio-coupled idea: sparse soft ticks, every third word at most.
Music: bed continues.
Transition mood: soft crossfade (page dims) → Scene 4

### Scene 4 — The numbers — 4.5s
The page recedes and dims. Three large stat cards arrive one at a time and stay: "5.31M — parameters" with the sub-label "val perplexity 9.4", "3.7 h — training on a laptop CPU", "14 MB — one offline HTML file". Each holds fully settled until the scene ends (the last one for ≥1.5s).
Sequential/interaction: yes — three cards in order, each held after arrival. Beat-grid: 14.02s, 15.52s, 17.02s (every third beat, because these are readable text). The third card lands on the 17.02s strong cue.
Audio intent: proud, building.
Audio-coupled idea: card-slide sounds on arrival; a heavier accent on the third card on the strong cue.
Music: bed continues; amber glow behind the cards breathes subtly with RMS.
Transition mood: soft crossfade → Scene 5

### Scene 5 — Punchline — 6.0s
Cards clear. A dim label "Real output from the model:" appears at 18.0s. The quote types in large gold text (18.3–19.4s): "The red ball hit the ball and the red ball." At 19.6s the dim caption fades up beneath it: "It repeats itself. I'm leaving it in." Both hold until 21.8s (quote ≥2.7s total viewing, caption ≥2.2s). On the 22.01s strong cue the final card lands with a bell: "MiniGPT Storyteller" large, with "Runs entirely in your browser." beneath. Holds for the last 2.0s; music fades out 23.0–24.0s.
Sequential/interaction: yes — the quote types out; final card lands on the strong cue.
Audio intent: warm laugh at the flaw, then a clean landing.
Audio-coupled idea: quiet key ticks on the quote typing; one bell at 22.01s; silence under the caption read.
Music: bed continues; final fade-out; amber title glow breathes subtly with RMS.
Transition mood: end card

**Music mood for this video:** upbeat, clean, corporate-adjacent warmth (Happy Beats / Business Moves vol. 1)
**Audio summary:** a warm music bed with key ticks on typing, one click on the button, card sounds on the stats, and a single bell on the final card; credit "Music: Sascha Ende, ende.app (CC BY 4.0)" goes in the share notes.

## Revision notes (after `hyperframes check`)
The storyboard above is the first draft. The shipped film differs in these ways, all driven by the check gate's reading-time floors and layout audit:
- **Film is 25.0 s (was 24).** The hook is held 1.0 s longer (4.0 s) so each typed line meets its reading floor. That is exactly two beats at 120.19 BPM, so every beat lock moved by 1.0 s and still lands on the same beats.
- **Hook sub-line is "On a laptop CPU."** ("No GPU" moved to the stat card: "Intel i5-8250U, no GPU").
- **Final timeline (film seconds):** hook 0–4.0; app UI arrives on the 4.02 s beat, click at 7.0, story streams 7.9–12.9; page clears 14.5–15.0; stat cards at 15.02 / 16.02 (every other beat) / 17.02 (strong cue); quote types 19.15–20.35; caption 20.2; final title on the 23.02 s strong cue (bell at 23.0), held to 25.0.
- **Stat cards are 1.0 s apart (every other beat), not 1.5 s,** so the third card lands on a strong cue and still holds 1.5+ s.
- **Page clears fully before the cards** instead of dimming under them: the layout audit flags text hidden under opaque cards across scenes.
- **Known, accepted warnings (3 of 3 in `check`, 0 errors):** (1) frame 0 is empty because the hook types in; the poster is baked into frame 0 at delivery. (2) The page's own 20-word subtitle is on screen 3.6 s. (3) The 44-word streamed paragraph is on screen 7.2 s, too short to read in full; the prompt line was already read in the previous scene and the point of the scene is that it writes.
