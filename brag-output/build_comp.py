"""Generate the HyperFrames composition (index.html + scenes + audio) for the MiniGPT brag video.
All timings are absolute film seconds unless a name ends in _l (scene-local).
Film is 25.0 s: the hook is held 1.0 s longer than the first draft so every typed line meets its reading floor;
that is exactly two beats at 120.19 BPM, so every beat / strong-cue lock is preserved."""
import json, pathlib, html

ROOT = pathlib.Path(__file__).parent / "composition"
(ROOT / "compositions").mkdir(exist_ok=True)
D = json.load(open(pathlib.Path(__file__).parent / "data.json"))
RMS, WORDS, COUNTS = D["rms"], D["words"], D["counts"]

BG, PANEL, PANEL2, LINE = "#14131a", "#1e1c27", "#262434", "#34314a"
TEXT, DIM, AMBER, MINT, GOLD = "#ece9f7", "#9a96b5", "#ffb454", "#7ee0c3", "#ffd9a0"
TOTAL = 25.0
HOOK_END = 4.0               # app arrives on the 4.02 s beat
APP0, STATS0, OUT0 = 4.0, 14.5, 18.9
APP_DUR, STATS_DUR, OUT_DUR = 14.9, 4.4, TOTAL - OUT0

FONTS = """
@font-face { font-family: 'Segoe UI'; font-weight: 400; src: local('Segoe UI'); }
@font-face { font-family: 'Segoe UI'; font-weight: 600; src: local('Segoe UI Semibold'); }
@font-face { font-family: 'Segoe UI'; font-weight: 700; src: local('Segoe UI Bold'); }
"""
SFX_KEYS = ["keypress-003.wav", "keypress-007.wav", "keypress-012.wav", "keypress-018.wav", "keypress-024.wav", "keypress-029.wav"]
audio = []  # (id, start, dur, vol, src)
def sfx(id_, start, dur, vol, src): audio.append((id_, round(start, 3), dur, vol, src))

def rms_at(t): return RMS[min(len(RMS) - 1, int(t * 12))]
def rms_chain(glow_id, t_abs0, local0, dur, lo, hi):
    """Seek-safe music-reactive opacity: one linear tween per 1/12 s, from pre-extracted RMS (subtle)."""
    step, out = 1 / 12, []
    for k in range(int(dur / step)):
        op = round(lo + (hi - lo) * rms_at(t_abs0 + k * step), 3)
        out.append(f'tl.to("#{glow_id}", {{ opacity: {op}, duration: {step:.4f}, ease: "none" }}, {local0 + k * step:.4f});')
    return "\n    ".join(out)

def type_tween(sel, t, dur, nchars, tick_every, prefix, base_tick=0, vol=0.22):
    """Stepped clip-path reveal (reads as typing) + quiet keypress ticks, one per `tick_every` chars."""
    ticks = []
    for k in range(0, nchars, tick_every):
        sfx(f"{prefix}{k}", t + dur * k / nchars, 0.1, vol, SFX_KEYS[(base_tick + k // tick_every) % 6])
    return (f'tl.fromTo("{sel}", {{ clipPath: "inset(-24px 100% -24px -24px)" }}, '
            f'{{ clipPath: "inset(-24px -24px -24px -24px)", duration: {dur}, ease: "steps({nchars})" }}, {{T}});').replace("{T}", f"{t}")

# ------------------------------------------------------------------ HOOK (film 0.0 - 4.0)
hook_tw = [type_tween("#hook-l1", 0.15, 0.7, 15, 3, "sfx-hk1-"),
           type_tween("#hook-l2", 0.9, 0.6, 13, 3, "sfx-hk2-", base_tick=2)]
hook = f"""<template>
  <style>
    {FONTS}
    #root {{ position: absolute; inset: 0; font-family: 'Segoe UI', system-ui, sans-serif; }}
    #hook-wrap {{ position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; }}
    .big {{ font-size: 160px; line-height: 172px; font-weight: 700; color: {TEXT}; letter-spacing: -0.02em; text-align: center; white-space: nowrap; }}
    .typ {{ display: inline-block; clip-path: inset(-24px 100% -24px -24px); }}
    .amb {{ color: {AMBER}; }}
    #hook-sub {{ margin-top: 40px; font-size: 56px; font-weight: 400; color: {DIM}; opacity: 0; }}
  </style>
  <div id="root" data-composition-id="hook" data-width="1920" data-height="1080">
    <div id="hook-wrap" class="clip" data-start="0" data-duration="{HOOK_END}">
      <div class="big"><span id="hook-l1" class="typ">I trained a GPT</span></div>
      <div class="big amb"><span id="hook-l2" class="typ">from scratch.</span></div>
      <div id="hook-sub">On a laptop CPU.</div>
    </div>
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    {chr(10).join("    " + s for s in hook_tw).strip()}
    tl.fromTo("#hook-sub", {{ opacity: 0, y: 24 }}, {{ opacity: 1, y: 0, duration: 0.45, ease: "power4.out" }}, 1.5);
    tl.fromTo("#hook-wrap", {{ opacity: 1, filter: "blur(0px)" }}, {{ opacity: 0, filter: "blur(10px)", duration: 0.26, ease: "power3.in" }}, {HOOK_END - 0.28});
    window.__timelines["hook"] = tl;
  </script>
</template>
"""
(ROOT / "compositions" / "hook.html").write_text(hook, encoding="utf-8")

# ------------------------------------------------------------------ APP (film 4.0 - 18.9, local = film - 4.0)
STREAM0_l, STEP, CLICK_l = 3.9, 0.15, 3.0
BTN = (520, 640)
def slider(label, val, ratio, x):
    return f"""<div class="sl" style="left:{x}px">
        <div class="sl-top"><span>{label}</span><b>{val}</b></div>
        <div class="rail"><div class="fill" style="width:{ratio * 100:.1f}%"></div><div class="thumb" style="left:{ratio * 100:.1f}%"></div></div>
      </div>"""
sliders = "".join(slider(l, v, r, 28 + i * (281 + 20)) for i, (l, v, r) in enumerate([
    ("Temperature", "0.70", 0.467), ("Top-k", "40", 0.40), ("Top-p", "0.95", 0.944), ("Max new tokens", "150", 0.778)]))
wspans = "".join(f'<span id="app-w{i}" class="gw">{html.escape(w)}</span> ' for i, w in enumerate(WORDS))
cnt_spans = "".join(f'<span id="app-c{i}" class="cn">{c}</span>' for i, c in enumerate(COUNTS))
app_tw, prev = [], None
for i in range(len(WORDS)):
    t = STREAM0_l + i * STEP
    app_tw.append(f'tl.fromTo("#app-w{i}", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.12, ease: "power2.out" }}, {t:.3f});')
    if prev is not None: app_tw.append(f'tl.set("#app-c{prev}", {{ opacity: 0 }}, {t:.3f});')
    app_tw.append(f'tl.set("#app-c{i}", {{ opacity: 1 }}, {t:.3f});')
    prev = i
    if i % 3 == 0: sfx(f"sfx-st{i}", APP0 + t, 0.1, 0.16, SFX_KEYS[(i // 3) % 6])
sfx("sfx-click", APP0 + CLICK_l - 0.03, 0.05, 0.9, "click_003.ogg")
sfx("sfx-press", APP0 + CLICK_l - 0.01, 0.12, 0.45, "keypress-018.wav")
STREAM_END_l = STREAM0_l + (len(WORDS) - 1) * STEP + 0.12

app = f"""<template>
  <style>
    {FONTS}
    #root {{ position: absolute; inset: 0; font-family: 'Segoe UI', system-ui, sans-serif; color: {TEXT}; }}
    #app-page {{ position: absolute; left: 340px; top: 80px; width: 1240px; height: 1010px; opacity: 0; }}
    #app-h1 {{ position: absolute; left: 0; top: 0; font-size: 64px; line-height: 76px; font-weight: 600; letter-spacing: .3px; white-space: nowrap; }}
    #app-h1 span {{ color: {AMBER}; }}
    #app-sub {{ position: absolute; left: 0; top: 84px; width: 1240px; font-size: 28px; line-height: 42px; color: {DIM}; }}
    .card {{ position: absolute; left: 0; width: 1240px; background: {PANEL}; border: 1px solid {LINE}; border-radius: 22px; }}
    #app-prompt-card {{ top: 190px; height: 420px; }}
    .lab {{ position: absolute; left: 28px; font-size: 28px; line-height: 34px; color: {DIM}; }}
    #app-ta {{ position: absolute; left: 28px; top: 70px; width: 1184px; height: 104px; background: {PANEL2}; border: 1px solid {LINE}; border-radius: 14px; font-size: 32px; line-height: 102px; padding: 0 24px; white-space: nowrap; overflow: hidden; }}
    .sl {{ position: absolute; top: 204px; width: 281px; }}
    .sl-top {{ display: flex; justify-content: space-between; align-items: baseline; font-size: 28px; line-height: 36px; color: {DIM}; white-space: nowrap; }}
    .sl-top b {{ color: {MINT}; font-weight: 600; font-size: 30px; }}
    .rail {{ position: relative; margin-top: 24px; height: 8px; border-radius: 4px; background: {LINE}; }}
    .fill {{ position: absolute; left: 0; top: 0; height: 8px; border-radius: 4px; background: {AMBER}; }}
    .thumb {{ position: absolute; top: -7px; width: 22px; height: 22px; margin-left: -11px; border-radius: 11px; background: {AMBER}; }}
    #app-go {{ position: absolute; left: 28px; top: 330px; width: 300px; height: 62px; border-radius: 14px; background: {AMBER}; color: #2a1a00; font-size: 28px; font-weight: 600; line-height: 62px; text-align: center; }}
    #app-stop {{ position: absolute; left: 348px; top: 330px; width: 130px; height: 62px; border-radius: 14px; background: {PANEL2}; border: 1px solid {LINE}; color: {TEXT}; font-size: 28px; font-weight: 600; line-height: 60px; text-align: center; opacity: .45; }}
    #app-out {{ top: 640px; height: 330px; opacity: 0; }}
    #app-outtext {{ position: absolute; left: 36px; top: 30px; width: 1168px; font-size: 38px; line-height: 60px; color: {TEXT}; }}
    .gw {{ color: {GOLD}; opacity: 0; }}
    #app-stats {{ position: absolute; left: 0; top: 986px; width: 1240px; height: 44px; font-size: 28px; color: {DIM}; opacity: 0; white-space: nowrap; }}
    #app-stats b {{ color: {TEXT}; font-weight: 600; }}
    #app-cntbox {{ display: inline-block; position: relative; width: 44px; height: 34px; vertical-align: bottom; }}
    .cn {{ position: absolute; left: 0; top: 0; color: {TEXT}; font-weight: 600; opacity: 0; }}
    #app-cursor {{ position: absolute; left: 0; top: 0; width: 44px; height: 44px; opacity: 0; transform-origin: 0 0; }}
  </style>
  <div id="root" data-composition-id="app" data-width="1920" data-height="1080">
    <div id="app-wrap" class="clip" data-start="0" data-duration="{APP_DUR}" style="position:absolute;inset:0">
      <div id="app-page" data-layout-allow-occlusion>
        <div id="app-h1">Mini<span>GPT</span> Storyteller</div>
        <div id="app-sub">A tiny GPT trained from scratch on TinyStories. It runs entirely in your browser, with no server and no network.</div>
        <div id="app-prompt-card" class="card" data-layout-allow-overflow>
          <div class="lab" style="top:26px">Story prompt</div>
          <div id="app-ta">Once upon a time, there was a little bear named Tom.</div>
          {sliders}
          <div id="app-go">Generate story</div>
          <div id="app-stop">Stop</div>
        </div>
        <div id="app-out" class="card">
          <div id="app-outtext"><span>Once upon a time, there was a little bear named Tom.</span> {wspans}</div>
        </div>
        <div id="app-stats">Generated <span id="app-cntbox" data-layout-ignore>{cnt_spans}</span> <b>tokens</b> &nbsp;·&nbsp; <b>~540</b> tokens/s &nbsp;·&nbsp; (shown slowed down)</div>
      </div>
      <svg id="app-cursor" viewBox="0 0 24 24"><path d="M3 2 L3 19 L8 14.5 L11.5 22 L14.5 20.6 L11 13.2 L18 13 Z" fill="#ffffff" stroke="#14131a" stroke-width="1.6" stroke-linejoin="round"/></svg>
    </div>
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    // page arrives on the 4.02s beat (local 0.02)
    tl.fromTo("#app-page", {{ opacity: 0, y: 70, filter: "blur(8px)" }}, {{ opacity: 1, y: 0, filter: "blur(0px)", duration: 0.8, ease: "power4.out" }}, 0.02); // beat-grid: 4.02s
    // simulated cursor travels to "Generate story", clicks at local {CLICK_l}
    tl.set("#app-cursor", {{ x: 1500, y: 930 }}, 0);
    tl.fromTo("#app-cursor", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.25, ease: "power2.out" }}, 1.5);
    tl.to("#app-cursor", {{ x: {BTN[0]}, y: {BTN[1]}, duration: 1.4, ease: "power2.inOut" }}, 1.5);
    tl.fromTo("#app-cursor", {{ scale: 1 }}, {{ scale: 0.86, duration: 0.07, ease: "power2.out", immediateRender: false }}, {CLICK_l});
    tl.fromTo("#app-cursor", {{ scale: 0.86 }}, {{ scale: 1, duration: 0.18, ease: "power2.out", immediateRender: false }}, {CLICK_l + 0.07});
    tl.fromTo("#app-go", {{ opacity: 1 }}, {{ opacity: 0.55, duration: 0.08, ease: "power2.out" }}, {CLICK_l});
    tl.to("#app-stop", {{ opacity: 1, duration: 0.2, ease: "power2.out" }}, {CLICK_l + 0.05});
    tl.to("#app-cursor", {{ opacity: 0, duration: 0.3, ease: "power2.in" }}, {CLICK_l + 0.4});
    // scroll down to the output card
    tl.fromTo("#app-page", {{ y: 0 }}, {{ y: -430, duration: 0.8, ease: "power2.inOut", immediateRender: false }}, 3.3);
    tl.fromTo("#app-out", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.35, ease: "power2.out" }}, 3.5);
    tl.fromTo("#app-stats", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.35, ease: "power2.out" }}, 3.7);
    // the story streams in, word by word (real model output); the token counter ticks with it
    {chr(10).join("    " + s for s in app_tw).strip()}
    tl.to("#app-go", {{ opacity: 1, duration: 0.25, ease: "power2.out" }}, {STREAM_END_l:.3f});
    tl.to("#app-stop", {{ opacity: 0.45, duration: 0.25, ease: "power2.out" }}, {STREAM_END_l:.3f});
    // page clears just before the first stat card (film {APP0 + 10.5}s to {APP0 + 11.0}s)
    tl.to("#app-page", {{ opacity: 0, filter: "blur(6px)", duration: 0.5, ease: "power2.inOut" }}, 10.5);
    window.__timelines["app"] = tl;
  </script>
</template>
"""
(ROOT / "compositions" / "app.html").write_text(app, encoding="utf-8")

# ------------------------------------------------------------------ STATS (film 14.5 - 18.9)
cards = [("5.31M", "parameters", "val perplexity 9.4", 15.02), ("3.7 h", "training on a laptop CPU", "Intel i5-8250U, no GPU", 16.02), ("14 MB", "one offline HTML file", "no server, no network", 17.02)]
card_html, card_tw = "", []
for i, (big, lab, sub, t_abs) in enumerate(cards):
    card_html += f"""<div id="stats-c{i}" class="sc" data-layout-allow-occlusion style="left:{160 + i * 550}px"><div class="sbig" data-layout-allow-occlusion>{big}</div><div class="slab" data-layout-allow-occlusion>{lab}</div><div class="ssub" data-layout-allow-occlusion>{sub}</div></div>"""
    card_tw.append(f'tl.fromTo("#stats-c{i}", {{ opacity: 0, y: 70, filter: "blur(8px)" }}, {{ opacity: 1, y: 0, filter: "blur(0px)", duration: 0.65, ease: "power4.out" }}, {t_abs - STATS0:.3f}); // beat-{"locked" if i == 2 else "grid"}: {t_abs:.2f}s')
    sfx(f"sfx-card{i}", t_abs - 0.05, 0.6, 0.55, "card-slide-2.ogg" if i == 1 else "card-slide-1.ogg")
sfx("sfx-card-hit", 17.02, 0.19, 0.5, "impactSoft_medium_001.ogg")
stats = f"""<template>
  <style>
    {FONTS}
    #root {{ position: absolute; inset: 0; font-family: 'Segoe UI', system-ui, sans-serif; color: {TEXT}; }}
    #stats-wrap {{ position: absolute; inset: 0; }}
    #stats-glow {{ position: absolute; left: 160px; top: 140px; width: 1600px; height: 800px; background: radial-gradient(ellipse at center, rgba(255,180,84,0.9) 0%, rgba(255,180,84,0) 62%); opacity: 0.2; }}
    .sc {{ position: absolute; top: 320px; width: 500px; height: 420px; background: {PANEL}; border: 1px solid {LINE}; border-radius: 28px; opacity: 0; text-align: center; }}
    .sbig {{ margin-top: 54px; font-size: 150px; line-height: 160px; font-weight: 700; color: {AMBER}; letter-spacing: -0.02em; }}
    .slab {{ margin-top: 20px; font-size: 38px; line-height: 46px; padding: 0 24px; color: {TEXT}; }}
    .ssub {{ margin-top: 20px; font-size: 30px; color: {DIM}; }}
  </style>
  <div id="root" data-composition-id="stats" data-width="1920" data-height="1080">
    <div id="stats-wrap" class="clip" data-start="0" data-duration="{STATS_DUR}">
      <div id="stats-glow"></div>
      {card_html}
    </div>
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    tl.set("#stats-glow", {{ opacity: 0.2 }}, 0);
    {chr(10).join("    " + s for s in card_tw).strip()}
    {rms_chain("stats-glow", STATS0, 0, STATS_DUR, 0.16, 0.30)}
    tl.to("#stats-wrap", {{ opacity: 0, duration: 0.4, ease: "power2.in" }}, {STATS_DUR - 0.4});
    window.__timelines["stats"] = tl;
  </script>
</template>
"""
(ROOT / "compositions" / "stats.html").write_text(stats, encoding="utf-8")

# ------------------------------------------------------------------ OUTRO (film 18.9 - 25.0)
Q1, Q2 = "&ldquo;The red ball hit the ball", "and the red ball.&rdquo;"
Q1_T, Q1_D, Q2_D = 19.15, 0.7, 0.5
CAP_T, QUOTE_EXIT, TITLE_T = 20.2, 22.8, 22.85
q_tw = [type_tween("#out-q1", Q1_T, Q1_D, 26, 4, "sfx-q1-"),
        type_tween("#out-q2", Q1_T + Q1_D, Q2_D, 18, 4, "sfx-q2-", base_tick=2)]
q_tw = [s.replace(f", {Q1_T},", f", {Q1_T - OUT0:.3f},") if False else s for s in q_tw]
# convert absolute tween start times to scene-local
def local(tw, t_abs): return tw.rstrip(");").rsplit(", ", 1)[0] + f", {t_abs - OUT0:.3f});"
q_tw = [local(q_tw[0], Q1_T), local(q_tw[1], Q1_T + Q1_D)]
sfx("sfx-bell", 23.0, 1.5, 0.7, "impactBell_heavy_000.ogg")
land = TITLE_T - OUT0
outro = f"""<template>
  <style>
    {FONTS}
    #root {{ position: absolute; inset: 0; font-family: 'Segoe UI', system-ui, sans-serif; color: {TEXT}; }}
    #out-wrap {{ position: absolute; inset: 0; }}
    #out-quotebox {{ position: absolute; left: 160px; top: 0; width: 1600px; height: 1080px; display: flex; flex-direction: column; align-items: center; justify-content: center; }}
    #out-label {{ font-size: 34px; color: {DIM}; opacity: 0; margin-bottom: 34px; }}
    .ql {{ font-size: 92px; line-height: 112px; font-weight: 600; color: {GOLD}; text-align: center; white-space: nowrap; }}
    .typ {{ display: inline-block; clip-path: inset(-24px 100% -24px -24px); }}
    #out-cap {{ margin-top: 44px; font-size: 46px; color: {DIM}; opacity: 0; text-align: center; }}
    #out-title-box {{ position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; opacity: 0; }}
    #out-glow {{ position: absolute; left: 260px; top: 180px; width: 1400px; height: 720px; background: radial-gradient(ellipse at center, rgba(255,180,84,0.9) 0%, rgba(255,180,84,0) 60%); opacity: 0.2; }}
    #out-title {{ position: relative; font-size: 128px; line-height: 140px; font-weight: 700; letter-spacing: -0.01em; }}
    #out-title span {{ color: {AMBER}; }}
    #out-sub {{ position: relative; margin-top: 26px; font-size: 48px; color: {DIM}; }}
  </style>
  <div id="root" data-composition-id="outro" data-width="1920" data-height="1080">
    <div id="out-wrap" class="clip" data-start="0" data-duration="{OUT_DUR:.1f}">
      <div id="out-quotebox">
        <div id="out-label">Real output from the model:</div>
        <div class="ql"><span id="out-q1" class="typ">{Q1}</span></div>
        <div class="ql"><span id="out-q2" class="typ">{Q2}</span></div>
        <div id="out-cap">It repeats itself. I'm leaving it in.</div>
      </div>
      <div id="out-title-box">
        <div id="out-glow"></div>
        <div id="out-title">Mini<span>GPT</span> Storyteller</div>
        <div id="out-sub">Runs entirely in your browser.</div>
      </div>
    </div>
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    tl.fromTo("#out-label", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3, ease: "power2.out" }}, 0.05);
    {chr(10).join("    " + s for s in q_tw).strip()}
    tl.fromTo("#out-cap", {{ opacity: 0, y: 18 }}, {{ opacity: 1, y: 0, duration: 0.5, ease: "power4.out" }}, {CAP_T - OUT0:.3f});
    // quote + caption clear just before the final card
    tl.to("#out-quotebox", {{ opacity: 0, filter: "blur(8px)", duration: 0.2, ease: "power3.in" }}, {QUOTE_EXIT - OUT0:.3f});
    tl.fromTo("#out-title-box", {{ opacity: 0, filter: "blur(10px)" }}, {{ opacity: 1, filter: "blur(0px)", duration: 0.2, ease: "power4.out" }}, {land:.3f}); // beat-locked: 23.02s (bell at 23.0)
    {rms_chain("out-glow", TITLE_T, land, TOTAL - TITLE_T, 0.16, 0.30)}
    window.__timelines["outro"] = tl;
  </script>
</template>
"""
(ROOT / "compositions" / "outro.html").write_text(outro, encoding="utf-8")

# ------------------------------------------------------------------ ROOT
host = lambda id_, start, dur, z: (f'<div id="{id_}" data-composition-id="{id_}" data-composition-src="compositions/{id_}.html" '
                                  f'data-start="{start}" data-duration="{dur}" data-track-index="{z}" data-track-kind="graphics" '
                                  f'data-width="1920" data-height="1080" style="z-index:{z}"></div>')
audio_html = [f'<audio id="bg-music" data-start="0" data-duration="{TOTAL:.0f}" data-track-index="10" data-volume="0.35" data-fade-in="0.4" data-fade-out="1" src="assets/music/happy-beats-business-moves-vol-1-by-ende-dot-app.mp3"></audio>']
for n, (id_, start, dur, vol, src) in enumerate(audio):
    audio_html.append(f'<audio id="{id_}" data-start="{start}" data-duration="{dur}" data-track-index="{11 + n % 6}" data-volume="{vol}" src="assets/sfx/{src}"></audio>')
index = f"""<!doctype html>
<html lang="en" data-resolution="landscape" data-composition-variables='[
  {{"id":"color-ground","type":"color","label":"Background","default":"{BG}"}},
  {{"id":"color-ink","type":"color","label":"Text","default":"{TEXT}"}},
  {{"id":"color-accent","type":"color","label":"Accent","default":"{AMBER}"}}
]'>
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="assets/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1920px; height: 1080px; overflow: hidden; background: {BG}; }}
      #root {{ position: relative; width: 1920px; height: 1080px; background: {BG}; }}
      #bg {{ position: absolute; inset: 0; background: var(--color-ground, {BG}); z-index: 0; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1920" data-height="1080">
      <div id="bg"></div>
      {host("hook", 0, HOOK_END, 1)}
      {host("app", APP0, APP_DUR, 2)}
      {host("stats", STATS0, STATS_DUR, 3)}
      {host("outro", OUT0, f"{OUT_DUR:.1f}", 4)}
      {chr(10).join("      " + a for a in audio_html).strip()}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      tl.set("#bg", {{ opacity: 1 }}, 0);
      window.__timelines["main"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>
"""
(ROOT / "index.html").write_text(index, encoding="utf-8")
print("built; audio clips:", len(audio) + 1)
