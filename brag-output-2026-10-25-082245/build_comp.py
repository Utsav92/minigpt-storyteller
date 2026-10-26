"""Build the research-demo composition. Templates use %%NAME%% placeholders (no brace escaping).
Film seconds: title 0-3.27 | model card 3.27-8.74 | samples 8.74-21.84 (3 x 4.37) | close 21.84-25.0.
Beat sources: vol-12 preset (109.96 BPM): strong cues 8.74, 13.11, 17.47, 22.37."""
import json, pathlib, html, re

HERE = pathlib.Path(__file__).parent
ROOT = HERE / "composition"; (ROOT / "compositions").mkdir(exist_ok=True)
D = json.load(open(HERE / "data.json", encoding="utf-8"))
RMS, VAL, SAMPLES = D["rms"], D["val"], D["samples"]

PAPER, INK, DIM, RULE, ACC = "#f7f5ef", "#17171c", "#5f5f6b", "#d6d2c6", "#1d3fcf"
TOTAL = 25.0
T_TITLE, T_MODEL, T_SAMP, T_CLOSE = 0.0, 3.27, 8.74, 21.84
PANEL = 4.37
D_TITLE, D_MODEL, D_SAMP, D_CLOSE = T_MODEL - T_TITLE, T_SAMP - T_MODEL, T_CLOSE - T_SAMP, TOTAL - T_CLOSE

SFX_KEYS = ["keypress-003.wav", "keypress-007.wav", "keypress-012.wav", "keypress-018.wav", "keypress-024.wav", "keypress-029.wav"]
audio = []
def sfx(id_, start, dur, vol, src): audio.append((id_, round(start, 3), dur, vol, src))
def fill(tpl, **kw):
    for k, v in kw.items(): tpl = tpl.replace(f"%%{k}%%", str(v))
    return tpl
def rms_chain(sel, t_abs0, dur, lo=0.45, hi=1.0, local0=0.0):
    step, out = 1 / 12, []
    for k in range(int(dur / step)):
        v = RMS[min(len(RMS) - 1, int((t_abs0 + k * step) * 12))]
        out.append(f'tl.to("{sel}", {{ opacity: {round(lo + (hi - lo) * v, 3)}, duration: {step:.4f}, ease: "none" }}, {local0 + k * step:.4f});')
    return "\n    ".join(out)
def type_tween(sel, t_local, dur, nchars):
    return (f'tl.fromTo("{sel}", {{ clipPath: "inset(-12px 100% -12px -12px)" }}, '
            f'{{ clipPath: "inset(-12px -12px -12px -12px)", duration: {dur}, ease: "steps({nchars})" }}, {t_local:.3f});')
def ticks(prefix, t_abs, dur, nchars, every, base=0, vol=0.2):
    for k in range(0, nchars, every):
        sfx(f"{prefix}{k}", t_abs + dur * k / nchars, 0.1, vol, SFX_KEYS[(base + k // every) % 6])

COMMON_CSS = """
    #root { position: absolute; inset: 0; font-family: 'Inter', system-ui, sans-serif; color: %%INK%%; }
    .mono { font-family: 'JetBrains Mono', monospace; }
    .serif { font-family: 'EB Garamond', serif; }
    .typ { display: inline-block; clip-path: inset(-12px 100% -12px -12px); }
""".replace("%%INK%%", INK)

# ---------------------------------------------------------------- TITLE
title = fill("""<template>
  <style>
    %%COMMON%%
    #t-wrap { position: absolute; inset: 0; }
    #t-rule { position: absolute; left: 200px; top: 330px; width: 1520px; height: 4px; background: %%ACC%%; }
    #t-meta { position: absolute; left: 200px; top: 366px; font-size: 30px; letter-spacing: .08em; text-transform: uppercase; color: %%DIM%%; opacity: 0; }
    #t-title { position: absolute; left: 196px; top: 430px; font-size: 168px; line-height: 180px; font-weight: 700; letter-spacing: -0.01em; white-space: nowrap; }
    #t-sub { position: absolute; left: 200px; top: 650px; width: 1500px; font-size: 50px; line-height: 66px; color: %%DIM%%; opacity: 0; text-wrap: balance; }
  </style>
  <div id="root" data-composition-id="title" data-width="1920" data-height="1080">
    <div id="t-wrap" class="clip" data-start="0" data-duration="%%DUR%%">
      <div id="t-rule"></div>
      <div id="t-meta" class="mono">Technical demo &middot; decoder-only transformer</div>
      <div id="t-title" class="serif">MiniGPT Storyteller</div>
      <div id="t-sub">A 5.31M-parameter language model that writes children&rsquo;s stories.</div>
    </div>
  </div>
  <script>
    const tl = gsap.timeline({ paused: true });
    tl.fromTo("#t-meta", { opacity: 0 }, { opacity: 1, duration: 0.4, ease: "power2.out" }, 0.15);
    tl.fromTo("#t-sub", { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: 0.5, ease: "power4.out" }, 0.2);
    tl.to("#t-wrap", { opacity: 0, duration: 0.25, ease: "power2.in" }, %%FADE%%);
    window.__timelines["title"] = tl;
  </script>
</template>
""", COMMON=COMMON_CSS, ACC=ACC, DIM=DIM, DUR=f"{D_TITLE:.2f}", FADE=f"{D_TITLE - 0.25:.2f}")
(ROOT / "compositions" / "title.html").write_text(title, encoding="utf-8")

# ---------------------------------------------------------------- MODEL CARD
# count-up spans (ease-out) for 5.31M
N = 18; cnt_html, cnt_tw = "", []
for k in range(N + 1):
    v = 5.31 * (1 - (1 - k / N) ** 2.6)
    cnt_html += f'<span id="m-c{k}" class="cn">{v:.2f}M</span>'
    t = 0.25 + k * (1.3 / N)
    if k: cnt_tw.append(f'tl.set("#m-c{k-1}", {{ opacity: 0 }}, {t:.3f});')
    cnt_tw.append(f'tl.set("#m-c{k}", {{ opacity: 1 }}, {t:.3f});')
rows = [("Layers &middot; width &middot; heads", "6 &middot; 256 &middot; 8"), ("Context", "192 tokens"), ("Vocabulary", "2,048 (BPE)"), ("Training data", "194k stories")]
row_t = [1.12, 1.66, 2.20, 2.74]   # beat-grid: abs 4.39, 4.93, 5.47, 6.01
rows_html = "".join(f'<div id="m-r{i}" class="row"><span class="rk mono">{k}</span><span class="rv mono">{v}</span></div>' for i, (k, v) in enumerate(rows))
rows_tw = "\n    ".join(f'tl.fromTo("#m-r{i}", {{ opacity: 0, y: 14 }}, {{ opacity: 1, y: 0, duration: 0.4, ease: "power4.out" }}, {t:.2f});' for i, t in enumerate(row_t))
for i, t in enumerate(row_t): sfx(f"sfx-row{i}", T_MODEL + t - 0.03, 0.11, 0.5, "drop_001.ogg")
# Figure 1: real validation loss
X0, X1, Y0, Y1, LMIN, LMAX = 70, 770, 40, 270, 2.0, 4.0
px = lambda s: X0 + (X1 - X0) * s / 2800
py = lambda l: Y0 + (Y1 - Y0) * (LMAX - l) / (LMAX - LMIN)
pts = [(px(s), py(l)) for s, l in VAL]
poly = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
dots = "".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="7" fill="{ACC}"/>' for x, y in pts)
grid = "".join(f'<line x1="{X0}" y1="{py(l):.1f}" x2="{X1}" y2="{py(l):.1f}" stroke="{RULE}" stroke-width="2"/>' for l in (3.0, 2.0))
svg = (f'<svg viewBox="0 0 800 300" width="800" height="300"><line x1="{X0}" y1="{Y1}" x2="{X1}" y2="{Y1}" stroke="{INK}" stroke-width="3"/>'
       f'<line x1="{X0}" y1="{Y0-10}" x2="{X0}" y2="{Y1}" stroke="{INK}" stroke-width="3"/>{grid}'
       f'<polyline points="{poly}" fill="none" stroke="{ACC}" stroke-width="5" stroke-linejoin="round" stroke-linecap="round"/>{dots}'
       f'<text x="{pts[0][0]+16:.0f}" y="{pts[0][1]+4:.0f}" font-family="JetBrains Mono" font-size="28" fill="{ACC}">{VAL[0][1]:.2f}</text>'
       f'<text x="{pts[-1][0]:.0f}" y="{pts[-1][1]-18:.0f}" text-anchor="end" font-family="JetBrains Mono" font-size="28" font-weight="700" fill="{ACC}">{VAL[-1][1]:.2f}</text></svg>')
model = fill("""<template>
  <style>
    %%COMMON%%
    #m-wrap { position: absolute; inset: 0; }
    #m-lab { position: absolute; left: 140px; top: 120px; font-size: 28px; letter-spacing: .08em; text-transform: uppercase; color: %%DIM%%; }
    #m-numbox { position: absolute; left: 132px; top: 150px; width: 780px; height: 280px; }
    .cn { position: absolute; left: 0; top: 0; font-family: 'EB Garamond', serif; font-weight: 700; font-size: 250px; line-height: 270px; color: %%ACC%%; opacity: 0; white-space: nowrap; }
    #m-par { position: absolute; left: 140px; top: 440px; font-size: 56px; line-height: 64px; opacity: 0; }
    #m-rule { position: absolute; left: 140px; top: 590px; width: 740px; height: 2px; background: %%RULE%%; }
    #m-plab { position: absolute; left: 140px; top: 620px; font-size: 28px; letter-spacing: .08em; text-transform: uppercase; color: %%DIM%%; opacity: 0; }
    #m-purp { position: absolute; left: 140px; top: 672px; width: 740px; font-size: 46px; line-height: 62px; opacity: 0; text-wrap: balance; }
    #m-tab { position: absolute; left: 980px; top: 130px; width: 800px; }
    .row { display: flex; justify-content: space-between; align-items: baseline; height: 84px; border-bottom: 2px solid %%RULE%%; opacity: 0; }
    .rk { font-size: 28px; color: %%DIM%%; } .rv { font-size: 34px; font-weight: 700; }
    #m-fig { position: absolute; left: 980px; top: 520px; width: 800px; height: 300px; clip-path: inset(0 100% 0 0); }
    #m-cap { position: absolute; left: 980px; top: 840px; font-size: 28px; color: %%DIM%%; opacity: 0; white-space: nowrap; }
  </style>
  <div id="root" data-composition-id="model" data-width="1920" data-height="1080">
    <div id="m-wrap" class="clip" data-start="0" data-duration="%%DUR%%">
      <div id="m-lab" class="mono">Model</div>
      <div id="m-numbox" data-layout-ignore>%%CNT%%</div>
      <div id="m-par">parameters</div>
      <div id="m-rule"></div>
      <div id="m-plab" class="mono">Purpose</div>
      <div id="m-purp">Continue a story from its first sentence.</div>
      <div id="m-tab">%%ROWS%%</div>
      <div id="m-fig">%%SVG%%</div>
      <div id="m-cap" class="mono">Figure 1. Validation loss: 3.85 &rarr; 2.24</div>
    </div>
  </div>
  <script>
    const tl = gsap.timeline({ paused: true });
    tl.fromTo("#m-wrap", { opacity: 0 }, { opacity: 1, duration: 0.3, ease: "power2.out" }, 0);
    %%CNTTW%%
    tl.fromTo("#m-par", { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: 0.5, ease: "power4.out" }, 0.45);
    tl.fromTo("#m-plab", { opacity: 0 }, { opacity: 1, duration: 0.3, ease: "power2.out" }, 1.9);
    tl.fromTo("#m-purp", { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: 0.5, ease: "power4.out" }, 2.0);
    // beat-grid: rows at abs 4.39, 4.93, 5.47, 6.01
    %%ROWSTW%%
    tl.fromTo("#m-fig", { clipPath: "inset(0 100% 0 0)" }, { clipPath: "inset(0 0% 0 0)", duration: 1.4, ease: "power2.inOut" }, 3.0);
    tl.fromTo("#m-cap", { opacity: 0 }, { opacity: 1, duration: 0.4, ease: "power2.out" }, 2.9);
    tl.to("#m-wrap", { opacity: 0, duration: 0.25, ease: "power2.in" }, %%FADE%%);
    window.__timelines["model"] = tl;
  </script>
</template>
""", COMMON=COMMON_CSS, ACC=ACC, DIM=DIM, RULE=RULE, DUR=f"{D_MODEL:.2f}", FADE=f"{D_MODEL - 0.25:.2f}",
     CNT=cnt_html, ROWS=rows_html, SVG=svg, CNTTW="\n    ".join(cnt_tw), ROWSTW=rows_tw)
(ROOT / "compositions" / "model.html").write_text(model, encoding="utf-8")

# ---------------------------------------------------------------- SAMPLES (3 panels)
panels_html, panels_tw = "", []
for p, s in enumerate(SAMPLES):
    t0 = p * PANEL                      # local start of panel; abs = T_SAMP + t0 (8.74 / 13.11 / 17.47 strong cues)
    words = s["answer"].split(" "); n = len(words)
    wspans = " ".join(f'<span id="s{p}-w{i}" class="w">{html.escape(w)}</span>' for i, w in enumerate(words))
    panels_html += f"""
      <div id="s{p}" class="panel clip" data-start="{t0:.2f}" data-duration="{PANEL:.2f}">
        <div class="tag mono"><span id="s{p}-dot" class="dot"></span>SAMPLE {p + 1} / 3</div>
        <div class="meta mono">temperature 0.7 &middot; top-k 40 &middot; one of 5 samples</div>
        <div class="lab mono" style="top:230px">Prompt</div>
        <div class="prompt mono"><span id="s{p}-p" class="typ">{html.escape(s["prompt"])}</span></div>
        <div class="hr" style="top:410px"></div>
        <div class="lab mono" id="s{p}-ol" style="top:440px">Model output</div>
        <div class="ans serif">{wspans}</div>
      </div>"""
    nch = len(s["prompt"])
    ticks(f"sfx-s{p}-", T_SAMP + t0 + 0.2, 0.65, nch, 8, base=p * 2)
    step = 2.3 / n
    tws = [f'tl.fromTo("#s{p}", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.25, ease: "power2.out" }}, {t0:.2f}); // beat-locked: abs {T_SAMP + t0:.2f}s',
           type_tween(f"#s{p}-p", t0 + 0.2, 0.65, nch),
           f'tl.fromTo("#s{p}-ol", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3, ease: "power2.out" }}, {t0 + 0.9:.2f});']
    for i in range(n):
        tws.append(f'tl.fromTo("#s{p}-w{i}", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.1, ease: "power2.out" }}, {t0 + 1.05 + i * step:.3f});')
    tws.append(f'tl.to("#s{p}", {{ opacity: 0, duration: 0.2, ease: "power2.in" }}, {t0 + PANEL - 0.22:.2f});')
    tws.append(rms_chain(f"#s{p}-dot", T_SAMP + t0, PANEL, local0=t0))
    panels_tw += tws
samples = fill("""<template>
  <style>
    %%COMMON%%
    .panel { position: absolute; inset: 0; opacity: 0; }
    .tag { position: absolute; left: 200px; top: 110px; display: flex; align-items: center; gap: 14px; font-size: 28px; font-weight: 700; color: %%ACC%%; border: 3px solid %%ACC%%; border-radius: 999px; padding: 6px 24px; letter-spacing: .04em; }
    .dot { display: inline-block; width: 16px; height: 16px; border-radius: 8px; background: %%ACC%%; opacity: .7; }
    .meta { position: absolute; right: 200px; top: 120px; font-size: 28px; color: %%DIM%%; white-space: nowrap; }
    .lab { position: absolute; left: 200px; font-size: 28px; letter-spacing: .08em; text-transform: uppercase; color: %%DIM%%; }
    .prompt { position: absolute; left: 200px; top: 290px; font-size: 38px; line-height: 56px; white-space: nowrap; }
    .hr { position: absolute; left: 200px; width: 1520px; height: 2px; background: %%RULE%%; }
    .ans { position: absolute; left: 200px; top: 500px; width: 1520px; font-size: 64px; line-height: 84px; color: %%ACC%%; }
    .w { opacity: 0; }
  </style>
  <div id="root" data-composition-id="samples" data-width="1920" data-height="1080">
    <div id="smp-wrap" class="clip" data-start="0" data-duration="%%DUR%%" style="position:absolute;inset:0">
      %%PANELS%%
    </div>
  </div>
  <script>
    const tl = gsap.timeline({ paused: true });
    %%TW%%
    window.__timelines["samples"] = tl;
  </script>
</template>
""", COMMON=COMMON_CSS, ACC=ACC, DIM=DIM, RULE=RULE, DUR=f"{D_SAMP:.2f}", PANELS=panels_html, TW="\n    ".join(panels_tw))
(ROOT / "compositions" / "samples.html").write_text(samples, encoding="utf-8")

# ---------------------------------------------------------------- CLOSE
LIM = 22.37 - T_CLOSE
sfx("sfx-bong", 22.37, 0.12, 0.6, "bong_001.ogg")
close = fill("""<template>
  <style>
    %%COMMON%%
    #c-wrap { position: absolute; inset: 0; }
    #c-rule { position: absolute; left: 200px; top: 230px; width: 1520px; height: 4px; background: %%ACC%%; opacity: 0; }
    #c-title { position: absolute; left: 196px; top: 270px; font-size: 140px; line-height: 150px; font-weight: 700; white-space: nowrap; opacity: 0; }
    #c-sub { position: absolute; left: 200px; top: 450px; font-size: 54px; line-height: 64px; color: %%DIM%%; opacity: 0; }
    #c-hr { position: absolute; left: 200px; top: 590px; width: 1520px; height: 2px; background: %%RULE%%; opacity: 0; }
    #c-llab { position: absolute; left: 200px; top: 620px; font-size: 28px; letter-spacing: .08em; text-transform: uppercase; color: %%DIM%%; opacity: 0; }
    #c-lim { position: absolute; left: 200px; top: 668px; font-size: 52px; line-height: 64px; opacity: 0; }
    #c-credit { position: absolute; left: 200px; top: 890px; font-size: 28px; color: %%DIM%%; opacity: 0; }
  </style>
  <div id="root" data-composition-id="close" data-width="1920" data-height="1080">
    <div id="c-wrap" class="clip" data-start="0" data-duration="%%DUR%%">
      <div id="c-rule"></div>
      <div id="c-title" class="serif">MiniGPT Storyteller</div>
      <div id="c-sub">Runs entirely in your browser.</div>
      <div id="c-hr"></div>
      <div id="c-llab" class="mono">Limitations</div>
      <div id="c-lim">Repeats itself. Simple stories only.</div>
      <div id="c-credit" class="mono">Music: Sascha Ende, ende.app (CC BY 4.0)</div>
    </div>
  </div>
  <script>
    const tl = gsap.timeline({ paused: true });
    tl.fromTo("#c-rule", { opacity: 0 }, { opacity: 1, duration: 0.3, ease: "power2.out" }, 0.0);
    tl.fromTo("#c-title", { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: 0.5, ease: "power4.out" }, 0.05);
    tl.fromTo("#c-sub", { opacity: 0, y: 12 }, { opacity: 1, y: 0, duration: 0.45, ease: "power4.out" }, 0.3);
    tl.fromTo("#c-hr", { opacity: 0 }, { opacity: 1, duration: 0.3, ease: "power2.out" }, 0.45);
    tl.fromTo("#c-llab", { opacity: 0 }, { opacity: 1, duration: 0.3, ease: "power2.out" }, %%LIM%%);
    tl.fromTo("#c-lim", { opacity: 0, y: 12 }, { opacity: 1, y: 0, duration: 0.45, ease: "power4.out" }, %%LIM%%); // beat-locked: abs 22.37s
    tl.fromTo("#c-credit", { opacity: 0 }, { opacity: 1, duration: 0.4, ease: "power2.out" }, 0.55);
    window.__timelines["close"] = tl;
  </script>
</template>
""", COMMON=COMMON_CSS, ACC=ACC, DIM=DIM, RULE=RULE, DUR=f"{D_CLOSE:.2f}", LIM=f"{LIM:.2f}")
(ROOT / "compositions" / "close.html").write_text(close, encoding="utf-8")

# ---------------------------------------------------------------- ROOT
host = lambda id_, start, dur, z: (f'<div id="{id_}" data-composition-id="{id_}" data-composition-src="compositions/{id_}.html" '
                                  f'data-start="{start:.2f}" data-duration="{dur:.2f}" data-track-index="{z}" data-track-kind="graphics" '
                                  f'data-width="1920" data-height="1080" style="z-index:{z}"></div>')
aud = [f'<audio id="bg-music" data-start="0" data-duration="{TOTAL:.0f}" data-track-index="10" data-volume="0.30" data-fade-in="0.4" data-fade-out="1" src="assets/music/happy-beats-business-moves-vol-12-by-ende-dot-app.mp3"></audio>']
for n, (id_, start, dur, vol, src) in enumerate(audio):
    aud.append(f'<audio id="{id_}" data-start="{start}" data-duration="{dur}" data-track-index="{11 + n % 6}" data-volume="{vol}" src="assets/sfx/{src}"></audio>')
index = fill("""<!doctype html>
<html lang="en" data-resolution="landscape" data-composition-variables='[
  {"id":"color-ground","type":"color","label":"Background","default":"%%PAPER%%"},
  {"id":"color-ink","type":"color","label":"Text","default":"%%INK%%"},
  {"id":"color-accent","type":"color","label":"Accent","default":"%%ACC%%"}
]'>
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="assets/gsap.min.js"></script>
    <style>
      * { margin: 0; padding: 0; box-sizing: border-box; }
      html, body { margin: 0; width: 1920px; height: 1080px; overflow: hidden; background: %%PAPER%%; }
      #root { position: relative; width: 1920px; height: 1080px; background: %%PAPER%%; }
      #bg { position: absolute; inset: 0; background: var(--color-ground, %%PAPER%%); z-index: 0; }
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="%%TOTAL%%" data-width="1920" data-height="1080">
      <div id="bg"></div>
      %%HOSTS%%
      %%AUDIO%%
    </div>
    <script>
      const tl = gsap.timeline({ paused: true });
      tl.set("#bg", { opacity: 1 }, 0);
      window.__timelines["main"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>
""", PAPER=PAPER, INK=INK, ACC=ACC, TOTAL=TOTAL,
     HOSTS="\n      ".join([host("title", T_TITLE, D_TITLE, 1), host("model", T_MODEL, D_MODEL, 2), host("samples", T_SAMP, D_SAMP, 3), host("close", T_CLOSE, D_CLOSE, 4)]),
     AUDIO="\n      ".join(aud))
(ROOT / "index.html").write_text(index, encoding="utf-8")
print("built; audio clips:", len(audio) + 1)
