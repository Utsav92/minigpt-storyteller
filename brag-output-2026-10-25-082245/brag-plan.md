# Brag Plan: MiniGPT Storyteller (research-demo cut)

## What is this app?
A 5.31M-parameter decoder-only language model, trained from scratch on TinyStories, that continues a children's story from its first sentence. It runs entirely in the browser as one 14 MB HTML file.

## The angle
Present it the way a research project page does: title, model card, one honest figure, qualitative samples, limitations. The credibility comes from showing real things: the real parameter count, the real validation-loss curve from the training log, three real samples (labelled as picked from 5), and a plain limitations line. No hype claims. Specific to this project because every number comes from `train_big.log` / the exported model and every sentence on screen is actual model output.

## Hook (first 2-3 seconds)
A paper-white title card that is already fully on screen at frame 0: "MiniGPT Storyteller" in a serif, then the line "A 5.31M-parameter language model that writes children's stories." fades in. The parameter count is in the first line.

## Key moments (the middle)
- **Model card:** "5.31M parameters" counting up in huge type, the purpose line ("Continue a story from its first sentence."), a four-row spec table that fills one row at a time, and Figure 1, the validation-loss curve drawing itself from 3.85 to 2.24.
- **Three examples with big answers:** three different prompts (a bear named Tom, Lily's garden, Mia's magic door). Each prompt types in monospace, then the model's answer streams in at large size in blue. Each carries the honest tag "one of 5 samples".

## Outro / punchline
Limitations stated plainly ("Repeats itself. Simple stories only.") under the title lockup "MiniGPT Storyteller / Runs entirely in your browser." with the music credit.

## User flow worth showing
Entry: a prompt (first sentence of a story). Key action: the model continues it. Result: a multi-sentence story. Shown three times with three different prompts.

## Tone
- Preset: polished
- Creative direction: research demo / project page: calm, exact, understated
- Interpretation: fewer, longer holds, serif title + monospace data, no jokes, no hype. The honesty (samples picked from 5, limitations) is the point.

## Format: landscape — 1920x1080
## Duration: 25 seconds

## Visual identity
- Background: #f7f5ef (paper)
- Ink: #17171c; dim text #5f5f6b; rules #d6d2c6
- Accent: #1d3fcf (model output, curve)
- Display font: EB Garamond (titles, answers); body Inter; data/prompts JetBrains Mono (all bundled by Hyperframes)
- Strongest visual element: Figure 1 (the real loss curve) and the large blue model output on paper

## Share copy (draft)
A 5.31M-parameter language model, trained from scratch to write children's stories. Runs entirely in your browser, one 14 MB file. Validation perplexity 9.4. It repeats itself and only knows simple stories; the samples in the video are picked from 5.

## Audio direction
- Role: calm bed with sparse professional accents
- Music: happy-beats-business-moves-vol-12-by-ende-dot-app.mp3 (109.96 BPM; "steady and clean", suits polished)
- Music treatment: from 0.0s, volume ~0.30, fade-in 0.4s, fade-out over the last second
- Music cue guidance: preset read (vol-12 cues). Strong cues 8.74, 13.11, 17.47 (8 beats apart), 22.37, 22.93. Locks: the three sample cards start on 8.74 / 13.11 / 17.47; limitations land on 22.37.
- Audio-reactive treatment: subtle; a small accent "running" dot beside each sample's tag breathes with music RMS. No waveform visuals.
- SFX posture: sparse; keypress ticks on prompt typing, soft drops on table rows, one soft bong when the limitations land
- Audio-coupled moments: prompt typing, table rows, curve reveal, limitations
- Restraint rule: nothing loud; no SFX during the streamed answers

## Storyboard

### Scene 1 — Title — 3.27s
Title "MiniGPT Storyteller" already on screen at frame 0. Fades in: "TECHNICAL DEMO · decoder-only transformer" (mono) then "A 5.31M-parameter language model that writes children's stories."
Sequential/interaction: none (frame 0 is complete by design).
Audio intent: calm entrance. Music: bed fades in.
Transition mood: soft crossfade → Scene 2

### Scene 2 — Model card — 5.47s
Left: "5.31M" counts up, "parameters", then the purpose block. Right: spec rows (Layers / width / heads: 6 · 256 · 8; Context: 192 tokens; Vocabulary: 2,048 BPE; Training data: 194k stories), then Figure 1 draws: validation loss 3.85 → 2.24.
Sequential/interaction: yes — count-up, four table rows one by one, curve reveal.
Audio intent: precise, informative. Audio-coupled idea: soft drop per table row.
Transition mood: clean → Scene 3 (lands on the 8.74s strong cue)

### Scene 3 — Samples — 13.1s (three panels of 4.37s)
Each panel: "SAMPLE n / 3" tag with the breathing dot, prompt typed in monospace, "Model output" label, then the answer streaming in large blue serif type. Footer: "temperature 0.7 · top-k 40 · one of 5 samples".
Sequential/interaction: yes — typing prompt, streaming answer.
Audio intent: quiet attention. Audio-coupled idea: key ticks on the prompt.
Transition mood: crossfade between panels, panels start on 8.74 / 13.11 / 17.47.

### Scene 4 — Limitations and close — 3.16s
Title lockup, "Runs entirely in your browser.", "Limitations: Repeats itself. Simple stories only." (lands on 22.37), credit line.
Audio intent: honest landing. Audio-coupled idea: one soft bong at 22.37.

**Music mood for this video:** steady, clean, quiet
**Audio summary:** a quiet bed, typing ticks on prompts, soft drops on table rows, one soft bong on the limitations; credit baked into the end card.
