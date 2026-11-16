"""The cartoon engine for The Animated Zoo explainers and Shorts (Nov 16 2026).
Noelson: "move back to the cartoon style ... with better animation than we had then"; "a new shot or visual change every 4 to 6
seconds"; "at least 6 different locations"; "every fact is shown with a matching image"; "all narration and on-screen words in sync".

  python3 toon.py <episode module> [--short <part>] [--plan] [--stills t1,t2,...] [--draft] [--from a --to b]

An episode is a Python module in episodes/ with EP (title, ids, packaging), STAGES (who stands where in each place) and SHOTS.
A SHOT is one camera set-up on one place, with one spoken line and the things that happen on its words:
  shot(place, cam, say, fx=[...], pcam=..., cam2=..., trans=..., pause=..., who=..., props=[...], part=...)
Every shot is a cut, so the picture changes with every line; fx add words, pictures and actions between the cuts.
--plan    only voices the lines, builds the timing and prints the plan gate (no render): longest stretch without a visual change,
          places, questions, length. The gate fails over 6 s (the finished video is checked again by pace_check.py at 8 s).
--stills  PNG frames at those seconds of the film (to LOOK at before a render).
--short N the 9:16 version of part N: the same shots, each re-framed by its own "pcam" (a new framing, not a crop), with a title
          band, bigger captions and the watermark above the title.
Output: out/<id>/<id>.mp4 (3840x2160) or out/<id>/<id>_short<N>.mp4 (2160x3840), <id>_timing.json, and the packaging files."""
import json, os, sys, re, subprocess, shutil, importlib, random, math, hashlib
import numpy as np, soundfile as sf

HERE = os.path.dirname(os.path.abspath(__file__)); STUDIO = os.path.dirname(HERE); REPO = os.path.dirname(STUDIO)
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(STUDIO, "sing")); sys.path.insert(0, os.path.join(STUDIO, "zoo3d"))
import art, art2
SR = 24000; FPS = 24
CHROME = "/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell"
GAP = 0.32          # silence between two lines
LEAD = 0.12         # the picture cuts a moment before the voice
MAXGAP = 6.0        # plan gate: no stretch without a visual change longer than this


def arg(k, d=None): return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


def shot(place, cam, say="", fx=(), pcam=None, cam2=None, pcam2=None, trans="cut", pause=0.0, who="milo", props=(), part=0, actors=None, q=False, hide=(), fly=None, tag="", speak=None,
         beat="", sing=None, move=None):
    """who: the one who speaks the line (their voice from EP["cast"], their mouth moves when they are in the picture).
    beat: the story beat this shot belongs to (hook, goal, obstacle1..3, low, solution, ending, fact, song) - the story gate counts them.
    sing: a sung line instead of a spoken one: {"lines": [{"text", "notes"}], "bpm", "chords", ...} (sing.py); the caption follows the sung words.
    move: {actor: (x, y, scale[, flip])} - where an actor of the stage stands in this shot."""
    return dict(place=place, cam=cam, say=say, fx=list(fx), pcam=pcam, cam2=cam2, pcam2=pcam2, trans=trans, pause=pause, who=who, props=list(props), part=part,
                actors=actors, q=q, hide=list(hide), fly=fly, tag=tag, speak=speak, beat=beat, sing=sing, move=move or {})


# ------------------------------------------------------------------ sound
def tone(f, d, amp=.25, decay=6.0, kind="sin"):
    t = np.arange(int(SR * d)) / SR
    w = np.sin(2 * np.pi * f * t) + (.3 * np.sin(4 * np.pi * f * t) if kind == "bell" else 0)
    return (amp * w * np.exp(-t * decay)).astype(np.float32)


def sfx(name):
    if name == "pop":
        t = np.arange(int(SR * .13)) / SR; f = 520 + 900 * t / .13
        return (.30 * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 26)).astype(np.float32)
    if name == "ding": return np.concatenate([tone(1046, .16, .22, 9, "bell"), tone(1568, .5, .24, 5, "bell")])
    if name == "tick": return tone(880, .07, .16, 40)
    if name == "whoosh":
        n = int(SR * .5); r = np.random.RandomState(3).randn(n).astype(np.float32); k = np.hanning(260); r = np.convolve(r, k / k.sum(), "same")
        return (r * np.hanning(n) * 1.6).astype(np.float32)
    if name == "boing":
        t = np.arange(int(SR * .3)) / SR; f = 300 + 500 * np.exp(-t * 9)
        return (.22 * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7)).astype(np.float32)
    if name == "hum":      # the mama and her calf hum to each other (a soft low tone, two notes)
        a = np.concatenate([tone(196, .55, .2, 1.6), tone(233, .7, .2, 1.4)]); n = len(a); e = np.minimum(1, np.arange(n) / (SR * .08))
        return (a * e).astype(np.float32)
    raise KeyError(name)


def music(total, bpm=96):
    """A soft plucked loop under the voice: C - Am - F - G, one bar each."""
    chords = [[261.6, 329.6, 392.0, 523.3], [220.0, 261.6, 329.6, 440.0], [174.6, 261.6, 349.2, 440.0], [196.0, 293.7, 392.0, 493.9]]
    step = 60 / bpm / 2; out = np.zeros(int(SR * (total + 3)), np.float32); i = 0; t = 0.0
    while t < total:
        ch = chords[(i // 8) % 4]; f = ch[(0, 2, 1, 3, 2, 1, 3, 2)[i % 8]]; n = tone(f, .9, .16, 4.2, "bell") + tone(f / 2, .9, .05, 3.0)
        s0 = int(t * SR); out[s0:s0 + len(n)] += n[:len(out) - s0]; i += 1; t += step
    return out[:int(SR * total)]


# ------------------------------------------------------------------ voice + timing
def shift(a, semis=0.0, formant=1.0):
    """A character's own voice from one of the engine's voices: the pitch moved by semitones, the mouth made smaller (formant > 1) or bigger. Same length."""
    if not semis and formant == 1.0: return a
    import sing, pyworld as pw
    h = hashlib.md5(a.tobytes() + f"{semis}|{formant}".encode()).hexdigest()[:16]; f = os.path.join(sing.CACHE, f"sh_{h}.npy")
    if os.path.exists(f): return np.load(f)
    x = a.astype(np.float64); f0, t = pw.harvest(x, SR, f0_floor=70, f0_ceil=700, frame_period=5.0); sp = pw.cheaptrick(x, f0, t, SR); ap = pw.d4c(x, f0, t, SR)
    if formant != 1.0:
        fr = np.arange(sp.shape[1]); src = np.clip(fr / formant, 0, sp.shape[1] - 1); sp = np.array([np.interp(src, fr, row) for row in sp])
    y = pw.synthesize(f0 * 2 ** (semis / 12), np.ascontiguousarray(sp), np.ascontiguousarray(ap), SR, frame_period=5.0)[:len(a)].astype(np.float32)
    y *= float(np.sqrt(np.mean(a ** 2)) / (np.sqrt(np.mean(y ** 2)) + 1e-9)); np.save(f, y); return y


def sung(ep, s):
    """A sung line (sing.py): the vocal with its own little band; returns (mix, vocal, words)."""
    import sing
    sp = dict(s["sing"]); lines = sp.pop("lines"); c = ep.get("cast", {}).get(s["who"], {})
    spec = {"bpm": sp.get("bpm", 108), "voice": sp.get("voice", c.get("voice", ep.get("voice", "af_heart"))), "formant": sp.get("formant", 1.1), "chords": sp.get("chords", "C G Am F"),
            "style": sp.get("style", "pop"), "intro_bars": 0, "outro_bars": sp.get("outro_bars", 1), "parts": [{"section": "refrain", "who": "host", "group": sp.get("group", True), "lines": lines}]}
    h = hashlib.md5(json.dumps(spec, sort_keys=True).encode()).hexdigest()[:12]; d = os.path.join(sing.CACHE, "refrain_" + h)
    if not os.path.exists(os.path.join(d, "timing.json")): sing.build(spec, d)
    tm = json.load(open(os.path.join(d, "timing.json"))); mix, _ = sf.read(os.path.join(d, "song.wav")); voc, _ = sf.read(os.path.join(d, "vocal.wav"))
    return mix.astype(np.float32), voc.astype(np.float32), [(w["w"], round(w["start"], 3), round(w["end"], 3)) for w in tm["words"]]


def voice_lines(ep, shots):
    import sing, wordsync
    v0_ = ep.get("voice", "af_heart"); sp0 = ep.get("speed", 0.9); t = ep.get("lead_in", 0.4); miss = 0; tot = 0; GAP_ = ep.get("gap", GAP); cast = ep.get("cast", {})
    for s in shots:
        s["t0"] = t; s["sung"] = False
        if s.get("sing"):
            mix, voc, words = sung(ep, s); s["say"] = " ".join(w[0] for w in words); s["audio"] = mix * .9; s["dur"] = len(mix) / SR; s["words"] = words; s["sung"] = True
            hop = SR // 12; env = np.array([np.sqrt(np.mean(voc[i:i + hop] ** 2)) for i in range(0, len(voc) - hop, hop)]); env = np.clip(env / (np.percentile(env, 92) + 1e-6), 0, 1)
            s["env"] = [round(float(x), 2) for x in env]; s["v0"] = t + LEAD; t = s["v0"] + s["dur"] + s["pause"]; s["t1"] = t; continue
        if s["say"]:
            spoken = s.get("speak") or s["say"]; c = cast.get(s["who"], {}); v = c.get("voice", v0_); sp = c.get("speed", sp0)
            a = sing.say(spoken, v, sp).astype(np.float32); al, got, n = wordsync.align(a, spoken); miss += n - got; tot += n
            if c.get("pitch") or c.get("formant", 1.0) != 1.0:
                a = shift(a, c.get("pitch", 0), c.get("formant", 1.0)); pk = float(np.abs(a).max())
                if pk > .9: a = a * (.9 / pk)          # a pitched voice can peak above full scale: bring the whole line down, never clip it
            if c.get("gain"): a = a * c["gain"]        # the voices of the cast at the same loudness as the storyteller
            toks = s["say"].split()
            if len(al) != len(toks):        # "speak" differs from the caption text: spread the times over the caption's words
                d = len(a) / SR; al = [(d * k / len(toks), d * (k + 1) / len(toks)) for k in range(len(toks))]
            s["audio"] = a; s["dur"] = len(a) / SR; s["words"] = [(toks[k], round(al[k][0], 3), round(al[k][1], 3)) for k in range(len(toks))]
            hop = SR // 12; env = np.array([np.sqrt(np.mean(a[i:i + hop] ** 2)) for i in range(0, len(a) - hop, hop)]); env = np.clip(env / (np.percentile(env, 92) + 1e-6), 0, 1)
            s["env"] = [round(float(x), 2) for x in env]
            s["v0"] = t + LEAD; t = s["v0"] + s["dur"] + GAP_ + s["pause"]
        else:
            s["audio"] = None; s["dur"] = 0; s["words"] = []; s["env"] = []; s["v0"] = t; t += max(0.6, s["pause"])
        s["t1"] = t
    return t, miss, tot


def when(s, at):
    """A moment inside a shot -> seconds of the film. at: seconds from the shot's start (number), "w:word" (when that word starts;
    "w:word:2" the second time it is said), "e:word" (when it ends), "end" (the end of the line), "end+1.2", "wait:0.5" (into the pause)."""
    if isinstance(at, (int, float)): return s["t0"] + at
    if at.startswith(("w:", "e:")):
        parts = at.split(":"); key = re.sub(r"[^a-z0-9']", "", parts[1].lower()); nth = int(parts[2]) if len(parts) > 2 else 1; k = 0
        for w, a, b in s["words"]:
            if re.sub(r"[^a-z0-9']", "", w.lower()) == key:
                k += 1
                if k == nth: return s["v0"] + (a if at[0] == "w" else b)
        raise KeyError(f"word '{parts[1]}' is not in the line: {s['say']}")
    if at.startswith("end"): return s["v0"] + s["dur"] + (float(at[3:]) if len(at) > 3 else 0)
    if at.startswith("wait:"): return s["v0"] + s["dur"] + GAP + float(at[5:])
    raise KeyError(at)


# ------------------------------------------------------------------ the page
CSS = """
@font-face{font-family:"Baloo";src:url(assets/baloo.woff2) format("woff2");font-weight:800}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:VWpx;height:VHpx;overflow:hidden;background:#fff}
#root{position:relative;width:VWpx;height:VHpx;overflow:hidden;font-family:"Baloo",sans-serif;background:#8fd8ff}
.shot{position:absolute;inset:0;display:none;overflow:hidden}
.cam{position:absolute;left:0;top:0;width:1920px;height:1080px;transform-origin:0 0}
.cam svg{position:absolute;left:0;top:0;overflow:visible}
.w{position:absolute;white-space:nowrap;color:#fff;-webkit-text-stroke:14px #402010;paint-order:stroke fill;line-height:1;transform:translate(-50%,-50%);opacity:0;letter-spacing:.01em}
.w.sun{color:#ffd23f}.w.pill{-webkit-text-stroke:0;color:#402010;background:#ffd23f;padding:14px 34px 4px;border-radius:999px;box-shadow:0 10px 0 rgba(64,32,16,.22)}
.w.note{-webkit-text-stroke:0;color:#1c5fc4;background:#fff;padding:12px 30px 2px;border-radius:26px;box-shadow:0 10px 0 rgba(28,95,196,.2)}
#hud{position:absolute;inset:0;pointer-events:none}
.cap{position:absolute;left:CAPLpx;right:CAPLpx;bottom:CAPBpx;text-align:center;opacity:0;font-size:CAPSpx;line-height:1.12;color:#fff;-webkit-text-stroke:CAPOpx #402010;paint-order:stroke fill}
.cap b{font-weight:800}.cap b.on{color:#ffd23f}
.sign{position:absolute;opacity:0;transform:translate(-50%,-50%);font-size:SIGNSpx;line-height:1;color:#fff;padding:22px 44px 8px;border-radius:30px;border:10px solid #fff;box-shadow:0 14px 0 rgba(64,32,16,.25);white-space:nowrap;-webkit-text-stroke:0}
.sign.a{background:#2f80ed}.sign.b{background:#ff7a59}.sign .ck{position:absolute;right:-46px;top:-46px;width:96px;height:96px;opacity:0}
.dots{position:absolute;opacity:0;transform:translate(-50%,-50%);display:flex;gap:26px}.dots i{width:44px;height:44px;border-radius:50%;background:#fff;border:8px solid #402010;opacity:.25}
#iris{position:absolute;left:50%;top:50%;width:3000px;height:3000px;margin:-1500px;border-radius:50%;background:radial-gradient(circle,#ffd23f 0 30%,#2f80ed 31%);transform:scale(0)}
#wm{position:absolute;opacity:.88}
#qcount{position:absolute;opacity:0;transform:translate(-50%,-50%);font-size:230px;color:#ffd23f;-webkit-text-stroke:20px #402010;paint-order:stroke fill;line-height:1}
#band{position:absolute;left:0;right:0;top:0;text-align:center}
#band .l1{position:absolute;left:0;right:0;top:206px;white-space:nowrap;font-size:104px;color:#fff;-webkit-text-stroke:16px #402010;paint-order:stroke fill;line-height:1}
#band .l2{position:absolute;left:0;right:0;top:310px;white-space:nowrap;font-size:150px;color:#ffd23f;-webkit-text-stroke:20px #402010;paint-order:stroke fill;line-height:1}
"""


class Film:
    def __init__(self, ep, stages, shots, portrait=False):
        self.ep, self.stages, self.shots, self.portrait = ep, stages, shots, portrait
        self.VW, self.VH = (1080, 1920) if portrait else (1920, 1080)
        self.js = []; self.hud = []; self.events = []; self.snd = []; self.uid = 0; self.rnd = random.Random(7); self.kinds = {}

    CAMEL_RIG = {"neck": "190 -330", "tail": "-232 -340", "ear": "284 -640", "legs": {"fl": 160, "bl": -138, "fl2": 118, "bl2": -178}, "hip": -262, "jaw": ("rot", 9, "372 -560"), "eyes": ["eye"], "brows": []}

    def rig(self, pid):
        k = self.kinds.get(pid, "camel"); return art2.RIGS.get(k, self.CAMEL_RIG)

    # camera: a landscape rect is (cx, cy, w); a portrait rect is (cx, cy, h)
    def cam_t(self, r):
        cx, cy, z = r; s = (self.VH / z) if self.portrait else (self.VW / z)
        return round(self.VW / 2 - cx * s, 2), round(self.VH / 2 - cy * s, 2), round(s, 4)

    def ev(self, t, kind, what=""): self.events.append((round(t, 2), kind, what))

    def add(self, code): self.js.append(code)

    def actor_svg(self, i, a):
        aid, kind, x, y, sc = a[:5]; flip = len(a) > 5 and a[5]; pid = f"s{i}_{aid}"
        self.kinds[pid] = kind
        if kind == "milo": inner = art.milo(pid)
        elif kind == "calf": inner = art.camel(pid, 0, calf=True)
        elif kind == "camel": inner = art.camel(pid, 1)
        elif kind == "bactrian": inner = art.camel(pid, 2, c=art.CAMEL_B, wool=True)
        elif kind in art2.RIGS: inner = art2.RIGS[kind]["build"](pid)
        else: raise KeyError(kind)
        if self.ep.get("kind") == "story" or self.ep.get("nest"):      # the part the engine moves carries a plain translate; the size and the mirror sit inside it.
            # (GSAP's x and y on a scaled SVG group are measured from the group's bounding box, so a tween to x = 300 on "translate(250 500) scale(.78)" stops at 257.)
            return f'<g id="{pid}_w" transform="translate({x} {y})"><g transform="scale({-sc if flip else sc} {sc})">{inner}</g></g>'
        return f'<g id="{pid}_w" transform="translate({x} {y}) scale({-sc if flip else sc} {sc})">{inner}</g>'

    def idle(self, i, a, s, fly):
        aid, kind = a[0], a[1]; p = f"s{i}_{aid}"; t0, d = s["t0"], s["t1"] - s["t0"]; r = self.rnd; js = []
        busy = any((f[0] in ("drink", "lookat", "nod") and f[2] == aid) or (f[0] in ("to", "fromto") and f"{aid}-neck" in f[2]) for f in s["fx"])   # the head is acting: no idle sway on top of it
        n = max(1, int(d / .5) | 1)
        if kind == "milo":
            js.append(f'tl.to("#{p}-body",{{scaleY:1.035,scaleX:.98,svgOrigin:"0 0",duration:.42,yoyo:true,repeat:{n},ease:"sine.inOut"}},{t0:.2f});')
            if fly:
                js.append(f'tl.set("#{p}-shadow",{{opacity:0}},0);tl.set("#{p}-legs",{{y:-14}},0);')
                js.append(f'tl.fromTo("#{p}",{{y:10}},{{y:-22,duration:.5,yoyo:true,repeat:{n},ease:"sine.inOut"}},{t0:.2f});')
                m = max(1, int(d / .11) | 1)
                js.append(f'tl.fromTo("#{p}-wl",{{rotation:-8,svgOrigin:"-96 -182"}},{{rotation:46,duration:.11,yoyo:true,repeat:{m},ease:"sine.inOut"}},{t0:.2f});')
                js.append(f'tl.fromTo("#{p}-wr",{{rotation:8,svgOrigin:"96 -182"}},{{rotation:-46,duration:.11,yoyo:true,repeat:{m},ease:"sine.inOut"}},{t0:.2f});')
            js.append(f'tl.to("#{p}-scarf",{{rotation:9,svgOrigin:"48 -50",duration:.6,yoyo:true,repeat:{max(1, int(d / .6) | 1)},ease:"sine.inOut"}},{t0:.2f});')
            eyes = [f"{p}-eyeL", f"{p}-eyeR"]
        elif kind in art2.RIGS:
            R = art2.RIGS[kind]; busy = busy or any(f[0] in ("face",) and f[2] == aid and False for f in s["fx"])
            js.append(f'tl.to("#{p}",{{scaleY:1.014,svgOrigin:"0 0",duration:.8,yoyo:true,repeat:{max(1, int(d / .8) | 1)},ease:"sine.inOut"}},{t0:.2f});')
            if R.get("tail"): js.append(f'tl.fromTo("#{p}-tail",{{rotation:-6,svgOrigin:"{R["tail"]}"}},{{rotation:8,duration:.7,yoyo:true,repeat:{max(1, int(d / .7) | 1)},ease:"sine.inOut"}},{t0:.2f});')
            if R.get("ear") and not any(f[0] == "face" and f[2] == aid for f in s["fx"]):
                tt = t0 + r.uniform(.5, 1.4)
                while tt < s["t1"] - .5: js.append(f'tl.to("#{p}-ear",{{rotation:-9,svgOrigin:"{R["ear"]}",duration:.14,yoyo:true,repeat:3}},{tt:.2f});'); tt += r.uniform(2.0, 3.6)
            if R.get("neck") and not busy: js.append(f'tl.fromTo("#{p}-neck",{{rotation:-1.2,svgOrigin:"{R["neck"]}"}},{{rotation:1.8,duration:1.2,yoyo:true,repeat:{max(1, int(d / 1.2) | 1)},ease:"sine.inOut"}},{t0:.2f});')
            if kind == "monkey_hang": js.append(f'tl.fromTo("#{p}-swing",{{rotation:-5,svgOrigin:"0 0"}},{{rotation:5,duration:1.0,yoyo:true,repeat:{max(1, int(d / 1.0) | 1)},ease:"sine.inOut"}},{t0:.2f});')
            eyes = [f"{p}-{e}" for e in R["eyes"]]
            tb = t0 + r.uniform(.5, 1.8)
            while tb < s["t1"] - .3:
                for e in eyes: js.append(f'tl.set("#{e}-lid",{{opacity:1}},{tb:.2f});tl.set("#{e}-lid",{{opacity:0}},{tb + .13:.2f});')
                tb += r.uniform(1.9, 3.6)
            return "".join(js)
        else:
            js.append(f'tl.to("#{p}",{{scaleY:1.012,svgOrigin:"0 0",duration:.9,yoyo:true,repeat:{max(1, int(d / .9) | 1)},ease:"sine.inOut"}},{t0:.2f});')
            js.append(f'tl.fromTo("#{p}-tail",{{rotation:-7,svgOrigin:"-232 -340"}},{{rotation:9,duration:.7,yoyo:true,repeat:{max(1, int(d / .7) | 1)},ease:"sine.inOut"}},{t0:.2f});')
            tt = t0 + r.uniform(.6, 1.6)
            while tt < s["t1"] - .5:
                js.append(f'tl.to("#{p}-ear",{{rotation:-18,svgOrigin:"284 -640",duration:.09,yoyo:true,repeat:3}},{tt:.2f});'); tt += r.uniform(2.2, 4.0)
            if not busy: js.append(f'tl.fromTo("#{p}-neck",{{rotation:-1.5,svgOrigin:"190 -330"}},{{rotation:2,duration:1.3,yoyo:true,repeat:{max(1, int(d / 1.3) | 1)},ease:"sine.inOut"}},{t0:.2f});')
            eyes = [f"{p}-eye"]
        tb = t0 + r.uniform(.5, 1.8)
        while tb < s["t1"] - .3:
            for e in eyes: js.append(f'tl.set("#{e}-lid",{{opacity:1}},{tb:.2f});tl.set("#{e}-lid",{{opacity:0}},{tb + .13:.2f});')
            tb += r.uniform(1.9, 3.6)
        return "".join(js)

    def talk(self, i, s, who):
        if not s["env"]: return ""
        p = f"s{i}_{who}"; js = []; v0 = s["v0"]; last = -1; kind = self.kinds.get(p, "milo")
        if kind != "milo":          # the jaw drops with the voice (hidden when the mouth is shut)
            R = self.rig(p); jw = R["jaw"]
            for k, e in enumerate(s["env"]):
                o = 0 if e < .12 else round(.35 + e * .65, 2)
                if o != last:
                    js.append(f'tl.set("#{p}-jaw",{{rotation:{o * jw[1]:.1f},svgOrigin:"{jw[2]}"}},{v0 + k / 12:.3f});' if jw[0] == "rot" else f'tl.set("#{p}-jaw",{{opacity:{1 if o else 0},y:{o * jw[1]:.1f}}},{v0 + k / 12:.3f});'); last = o
            js.append(f'tl.set("#{p}-jaw",{{rotation:0,svgOrigin:"{jw[2]}"}},{v0 + s["dur"] + .02:.3f});' if jw[0] == "rot" else f'tl.set("#{p}-jaw",{{opacity:0,y:0}},{v0 + s["dur"] + .02:.3f});')
            return "".join(js)
        for k, e in enumerate(s["env"]):
            o = 0 if e < .12 else round(6 + e * 22)
            if o != last: js.append(f'tl.set("#{p}-beak",{{y:{o}}},{v0 + k / 12:.3f});'); last = o
        js.append(f'tl.set("#{p}-beak",{{y:0}},{v0 + s["dur"] + .02:.3f});')
        ups = [w for w in s["words"] if w[0].endswith("?")]
        if ups: js.append(f'tl.to("#{p}-browL,#{p}-browR",{{y:-12,duration:.18,yoyo:true,repeat:1,repeatDelay:.5}},{v0 + ups[0][1]:.2f});')
        return "".join(js)

    # ---- things that happen in a shot
    def word(self, i, s, at, text, x, y, size=120, cls="", hold=None, space="stage", rot=-4):
        t = when(s, at); self.uid += 1; wid = f"w{self.uid}"; end = min(s["t1"] - .05, t + hold) if hold else s["t1"] - .05
        tgt = self.stage_html[i] if space == "stage" else self.hud
        if self.portrait and space == "hud": x, y = x * 1080 / 1920, y * 1920 / 1080 * .72 + 300
        tgt.append(f'<div class="w {cls}" id="{wid}" style="left:{x}px;top:{y}px;font-size:{size}px">{text}</div>')
        self.add(f'tl.fromTo("#{wid}",{{opacity:0,scale:.3,rotation:{rot - 10}}},{{opacity:1,scale:1,rotation:{rot},duration:.32,ease:"back.out(2.4)"}},{t:.2f});'
                 f'tl.to("#{wid}",{{scale:1.06,duration:.4,yoyo:true,repeat:{max(1, int((end - t - .4) / .4) | 1)},ease:"sine.inOut"}},{t + .34:.2f});tl.set("#{wid}",{{opacity:0}},{end:.2f});')
        self.ev(t, "word", text); self.snd.append((t, "pop"))

    def prop_show(self, i, s, at, pid, hold=None, pop=True):
        t = when(s, at); q = f"#s{i}_{pid}_w"
        self.add(f'tl.fromTo("{q}",{{opacity:0,scale:.2,transformOrigin:"50% 50%"}},{{opacity:1,scale:1,duration:.34,ease:"back.out(2)"}},{t:.2f});')
        if hold: self.add(f'tl.to("{q}",{{opacity:0,scale:.6,duration:.2}},{min(s["t1"] - .22, t + hold):.2f});')
        self.ev(t, "picture", pid)
        if pop: self.snd.append((t, "pop"))

    def signs(self, i, s, at, options, correct, reveal_at):
        t = when(s, at); tr = when(s, reveal_at); self.uid += 1; u = self.uid
        if self.portrait: pos = [(540, 570), (540, 725)]; dp = (540, 850)      # right under the title band, above the animals
        else: pos = [(600, 178), (1320, 178)]; dp = (960, 180)
        for k, o in enumerate(options):
            self.hud.append(f'<div class="sign {"ab"[k]}" id="sg{u}_{k}" style="left:{pos[k][0]}px;top:{pos[k][1]}px">{o}<svg class="ck" id="ck{u}_{k}" viewBox="-80 -80 160 160">{art.tick("x")}</svg></div>')
            self.add(f'tl.fromTo("#sg{u}_{k}",{{opacity:0,y:-80,rotation:{(-5, 5)[k]}}},{{opacity:1,y:0,rotation:{(-3, 3)[k]},duration:.4,ease:"back.out(2)"}},{t + k * .35:.2f});')
            self.add(f'tl.to("#sg{u}_{k}",{{y:-14,duration:.5,yoyo:true,repeat:{max(1, int((tr - t) / .5) | 1)},ease:"sine.inOut"}},{t + .8:.2f});')
            self.ev(t + k * .35, "sign", o); self.snd.append((t + k * .35, "pop"))
        self.hud.append(f'<div class="dots" id="dt{u}" style="left:{dp[0]}px;top:{dp[1]}px"><i></i><i></i><i></i></div>')
        think = tr - (s["v0"] + s["dur"])
        if think > 1.2:        # thinking time: three dots fill up, one a second
            td = s["v0"] + s["dur"] + .15; self.add(f'tl.set("#dt{u}",{{opacity:1}},{td:.2f});')
            for k in range(3):
                tk = td + (think - .3) * (k + .5) / 3
                self.add(f'tl.to("#dt{u} i:nth-child({k + 1})",{{opacity:1,scale:1.25,backgroundColor:"#ffd23f",duration:.2}},{tk:.2f});'); self.ev(tk, "thinking dot", str(k + 1)); self.snd.append((tk, "tick"))
            self.add(f'tl.set("#dt{u}",{{opacity:0}},{tr - .05:.2f});')
        w = 1 - correct
        self.add(f'tl.to("#sg{u}_{correct}",{{scale:1.25,rotation:0,duration:.3,ease:"back.out(3)"}},{tr:.2f});tl.set("#ck{u}_{correct}",{{opacity:1}},{tr:.2f});'
                 f'tl.fromTo("#ck{u}_{correct}",{{scale:0}},{{scale:1,duration:.3,ease:"back.out(3)"}},{tr:.2f});tl.to("#sg{u}_{w}",{{opacity:.0,scale:.7,duration:.3}},{tr:.2f});')
        self.add(f'tl.to("#sg{u}_0,#sg{u}_1",{{opacity:0,duration:.2}},{s["t1"] - .22:.2f});')
        self.ev(tr, "answer", options[correct]); self.snd.append((tr, "ding"))

    def count(self, i, s, at, n, dur, x=960, y=330, suffix=""):
        t = when(s, at); self.uid += 1; u = self.uid
        if self.portrait: x, y = 540, 760
        self.hud.append(f'<div id="qcount" class="qc{u}" style="left:{x}px;top:{y}px"></div>')
        for k in range(1, n + 1):
            tk = t + dur * (k - 1) / max(1, n - 1)
            self.add(f'tl.set(".qc{u}",{{opacity:1,innerText:"{k}{suffix}"}},{tk:.3f});tl.fromTo(".qc{u}",{{scale:1.25}},{{scale:1,duration:{min(.18, dur / n * .8):.3f}}},{tk:.3f});')
            if n <= 8 or k % max(1, n // 8) == 0: self.ev(tk, "count", str(k)); self.snd.append((tk, "tick"))
        self.add(f'tl.set(".qc{u}",{{opacity:0}},{s["t1"] - .05:.2f});')

    def fx(self, i, s, f):
        k = f[0]; P = lambda a: f"s{i}_{a}"
        if k == "word": self.word(i, s, f[1], f[2], **(f[3] if len(f) > 3 else {}))
        elif k == "show": self.prop_show(i, s, f[1], f[2], *(f[3:]))
        elif k == "hide": self.add(f'tl.to("#{P(f[2])}_w",{{opacity:0,duration:.2}},{when(s, f[1]):.2f});')
        elif k == "signs": self.signs(i, s, f[1], f[2], f[3], f[4])
        elif k == "count": self.count(i, s, f[1], f[2], f[3], **(f[4] if len(f) > 4 else {}))
        elif k == "hop":
            t = when(s, f[1]); n = f[3] if len(f) > 3 else 1
            self.add(f'tl.to("#{P(f[2])}",{{y:"-=70",duration:.2,yoyo:true,repeat:{2 * n - 1},ease:"power2.out"}},{t:.2f});'); self.ev(t, "action", f"{f[2]} hops"); self.snd.append((t, "boing"))
        elif k == "nod":
            t = when(s, f[1]); self.add(f'tl.to("#{P(f[2])}-neck",{{rotation:{14 if self.kinds.get(P(f[2]), "camel") not in art2.RIGS else 9},svgOrigin:"{self.rig(P(f[2]))["neck"]}",duration:.22,yoyo:true,repeat:3,ease:"sine.inOut"}},{t:.2f});'); self.ev(t, "action", f"{f[2]} nods")
        elif k == "lookat":         # a camel turns its head: up (-) or down (+) degrees, and holds
            t = when(s, f[1]); self.add(f'tl.to("#{P(f[2])}-neck",{{rotation:{f[3]},svgOrigin:"{self.rig(P(f[2]))["neck"]}",duration:.5,ease:"power2.inOut"}},{t:.2f});'); self.ev(t, "action", f"{f[2]} looks")
        elif k == "chew":
            t = when(s, f[1]); d = f[3]; self.add(f'tl.to("#{P(f[2])}-jaw",{{rotation:9,x:6,svgOrigin:"372 -560",duration:.17,yoyo:true,repeat:{int(d / .17) | 1},ease:"sine.inOut"}},{t:.2f});'); self.ev(t, "action", f"{f[2]} chews")
        elif k == "drink":
            t = when(s, f[1]); d = f[3]
            self.add(f'tl.to("#{P(f[2])}-neck",{{rotation:{f[4] if len(f) > 4 else 62},svgOrigin:"190 -330",duration:.6,ease:"power2.inOut"}},{t:.2f});'
                     f'tl.to("#{P(f[2])}-neck",{{rotation:0,duration:.6,ease:"power2.inOut"}},{t + d:.2f});'); self.ev(t, "action", f"{f[2]} bends down to drink")
        elif k == "droop":          # the hump leans over and droops (the fat was used)
            t = when(s, f[1]); self.add(f'tl.to("#{P(f[2])}-hump",{{rotation:{f[3] if len(f) > 3 else 28},scaleY:.72,scaleX:.94,svgOrigin:"0 -372",duration:1.1,ease:"power2.inOut"}},{t:.2f});'); self.ev(t, "action", f"{f[2]}'s hump leans over")
        elif k == "perk":
            t = when(s, f[1]); self.add(f'tl.to("#{P(f[2])}-hump",{{rotation:0,scaleY:1,scaleX:1,svgOrigin:"0 -372",duration:.9,ease:"back.out(2)"}},{t:.2f});'); self.ev(t, "action", f"{f[2]}'s hump stands up")
        elif k == "grow":           # a hump grows from the tuft (time passing)
            t = when(s, f[1]); self.add(f'tl.fromTo("#{P(f[2])}-hump",{{scaleY:.12,scaleX:.5,svgOrigin:"0 -372"}},{{scaleY:{f[3] if len(f) > 3 else .7},scaleX:.8,duration:1.6,ease:"power1.inOut"}},{t:.2f});'); self.ev(t, "action", "a hump grows")
        elif k == "walk":
            t = when(s, f[1]); dx, d = f[3], f[4]; n = int(d / .3) | 1
            self.add(f'tl.to("#{P(f[2])}_w",{{x:"+={dx}",duration:{d},ease:"none"}},{t:.2f});')
            R = self.rig(P(f[2])); LG = R.get("legs") or {}
            if not LG: self.add(f'tl.to("#{P(f[2])}",{{y:"-=26",duration:.15,yoyo:true,repeat:{int(d / .15) | 1},ease:"sine.inOut"}},{t:.2f});')      # no legs to swing: a bouncy walk
            for leg, ph in (("fl", 1), ("bl", -1), ("fl2", -1), ("bl2", 1)):
                if leg not in LG: continue
                ox = LG[leg]
                self.add(f'tl.fromTo("#{P(f[2])}-{leg}",{{rotation:{-13 * ph},svgOrigin:"{ox} {R["hip"]}"}},{{rotation:{13 * ph},duration:.3,yoyo:true,repeat:{n},ease:"sine.inOut"}},{t:.2f});'
                         f'tl.to("#{P(f[2])}-{leg}",{{rotation:0,duration:.15}},{t + d:.2f});')
            self.ev(t, "action", f"{f[2]} walks")
        elif k == "fly":            # Milo flies to a new spot in the shot
            t = when(s, f[1]); self.add(f'tl.to("#{P(f[2])}_w",{{x:{f[3]},y:{f[4]},duration:{f[5] if len(f) > 5 else .8},ease:"power2.inOut"}},{t:.2f});'); self.ev(t, "action", f"{f[2]} flies")
        elif k == "blinkslow":      # a slow, long blink (eyelashes)
            t = when(s, f[1])
            for q in range(f[3] if len(f) > 3 else 2): self.add(f'tl.set("#{P(f[2])}-lid",{{opacity:1}},{t + q * .7:.2f});tl.set("#{P(f[2])}-lid",{{opacity:0}},{t + q * .7 + .32:.2f});'); self.ev(t + q * .7, "action", "blink")
        elif k == "to":             # anything else: (to, at, "#selector with {p}", {gsap vars}, what)
            t = when(s, f[1]); self.add(f'tl.to("{f[2].replace("{p}", f"s{i}_")}",{json.dumps(f[3])},{t:.2f});')
            if len(f) > 4 and f[4]: self.ev(t, "action", f[4])
        elif k == "fromto":
            t = when(s, f[1]); self.add(f'tl.fromTo("{f[2].replace("{p}", f"s{i}_")}",{json.dumps(f[3])},{json.dumps(f[4])},{t:.2f});')
            if len(f) > 5 and f[5]: self.ev(t, "action", f[5])
        elif k == "face":           # how a character feels: ("face", at, who, "sad" | "happy" | "wow" | "sleepy")
            t = when(s, f[1]); p = P(f[2]); kind = self.kinds.get(p, "camel"); R = self.rig(p); mood = f[3]; br = R.get("brows", [])
            tilt = {"sad": 16, "happy": 0, "wow": 0, "sleepy": 6}[mood]; lift = {"sad": -4, "happy": 0, "wow": -14, "sleepy": 6}[mood]
            for b in br:
                sign = 1 if b.endswith("R") else -1            # the inner end of the brow goes up when worried
                self.add(f'tl.to("#{p}-{b}",{{rotation:{sign * tilt},y:{lift},transformOrigin:"50% 50%",duration:.25}},{t:.2f});')
            if kind in art2.RIGS:
                self.add(f'tl.set("#{p}-smile",{{opacity:{0 if mood == "sad" else 1}}},{t:.2f});tl.set("#{p}-frown",{{opacity:{1 if mood == "sad" else 0}}},{t:.2f});')
                if R.get("ear"): self.add(f'tl.to("#{p}-ear",{{rotation:{ {"sad": 12, "happy": 0, "wow": -10, "sleepy": 8}[mood] },svgOrigin:"{R["ear"]}",duration:.35}},{t:.2f});')
                if R.get("neck") and mood in ("sad", "sleepy", "happy"): self.add(f'tl.to("#{p}-neck",{{rotation:{ {"sad": 9, "sleepy": 7, "happy": 0}[mood] },svgOrigin:"{R["neck"]}",duration:.4,ease:"power2.inOut"}},{t:.2f});')
            elif kind == "milo": self.add(f'tl.to("#{p}-body",{{scaleY:{ {"sad": .95, "happy": 1, "wow": 1.05, "sleepy": .96}[mood] },svgOrigin:"0 0",duration:.3}},{t:.2f});')
            else: self.add(f'tl.to("#{p}-neck",{{rotation:{ {"sad": 14, "happy": 0, "wow": -8, "sleepy": 12}[mood] },svgOrigin:"190 -330",duration:.4,ease:"power2.inOut"}},{t:.2f});')
            for e in R.get("eyes", []) if kind != "milo" else ["eyeL", "eyeR"]:
                if mood == "wow": self.add(f'tl.to("#{p}-{e}",{{scale:1.14,transformOrigin:"50% 50%",duration:.15,yoyo:true,repeat:1,repeatDelay:.6}},{t:.2f});')
            self.ev(t, "action", f"{f[2]} looks {mood}")
        elif k == "trunk":          # the elephant's trunk turns: ("trunk", at, who, degrees[, seconds])  -100 = straight up (the snorkel), -40 = a reach
            t = when(s, f[1]); p = P(f[2]); self.add(f'tl.to("#{p}-trunk",{{rotation:{f[3]},svgOrigin:"{self.rig(p)["trunk"]}",duration:{f[4] if len(f) > 4 else .5},ease:"power2.inOut"}},{t:.2f});'); self.ev(t, "action", f"{f[2]}'s trunk moves")
        elif k == "arm":            # the monkey's arm: ("arm", at, who, "l" | "r", degrees)
            t = when(s, f[1]); p = P(f[2]); ox = -58 if f[3] == "l" else 58
            self.add(f'tl.to("#{p}-a{f[3]}",{{rotation:{f[4]},svgOrigin:"{ox} -206",duration:.35,ease:"back.out(1.6)"}},{t:.2f});'); self.ev(t, "action", f"{f[2]} moves an arm")
        elif k == "snd": self.snd.append((when(s, f[1]), f[2]))
        else: raise KeyError(k)

    def captions(self, i, s):
        if not s["words"]: return
        words = s["words"]; mx = 5 if self.portrait else 9; chunks = []; cur = []
        for w in words:
            cur.append(w)
            if len(cur) >= mx or (re.search(r"[.!?]$", w[0]) and len(cur) >= 2) or (re.search(r",$", w[0]) and len(cur) >= mx - 2): chunks.append(cur); cur = []
        if cur:
            if chunks and len(cur) == 1: chunks[-1] += cur
            else: chunks.append(cur)
        for ci, ch in enumerate(chunks):
            self.uid += 1; cid = f"c{self.uid}"; a = s["v0"] + ch[0][1] - .06; b = (s["v0"] + chunks[ci + 1][0][1] - .06) if ci + 1 < len(chunks) else min(s["t1"] - .02, s["v0"] + s["dur"] + .5)
            self.hud.append(f'<div class="cap" id="{cid}">' + " ".join(f'<b id="{cid}_{k}">{w[0]}</b>' for k, w in enumerate(ch)) + '</div>')
            self.add(f'tl.set("#{cid}",{{opacity:1}},{max(0, a):.3f});tl.set("#{cid}",{{opacity:0}},{b:.3f});' + "".join(f'tl.set("#{cid}_{k}",{{color:"#ffd23f"}},{s["v0"] + w[1]:.3f});' for k, w in enumerate(ch)))

    def build_html(self, total, title_band=None):
        VW, VH = self.VW, self.VH; shots_html = []; self.stage_html = {}
        self.add(f'tl.set("#s0",{{display:"block"}},0);')
        for i, s in enumerate(self.shots):
            self.stage_html[i] = []; p = f"s{i}"; far, mid, near = art.BG[s["place"]](p)
            actors = s["actors"] if s["actors"] is not None else self.stages.get(s["place"], [])
            actors = [a for a in actors if a[0] not in s["hide"]]
            actors = [((a[0], a[1]) + tuple(s["move"][a[0]]) + tuple(a[len(s["move"][a[0]]) + 2:])) if a[0] in s.get("move", {}) else a for a in actors]
            fly = s["fly"] if s["fly"] is not None else [a[0] for a in actors if a[1] == "milo" and (len(a) > 6 and a[6])]
            asvg = "".join(self.actor_svg(i, a) for a in sorted(actors, key=lambda a: a[3]))
            def _pp(pr): return pr[6] if (self.portrait and len(pr) > 6 and pr[6]) else (pr[2], pr[3], pr[4] if len(pr) > 4 else 1)   # a prop may sit elsewhere in the 9:16 picture
            story = self.ep.get("kind") == "story" or self.ep.get("nest")      # "nest": a lesson built with the translate-only wrappers (every episode after zc_ep01)
            def _pw(pr):
                x_, y_, sc_ = _pp(pr); op = 0 if (len(pr) > 5 and pr[5] == "hidden") else 1; inner = pr[1](f"{p}_{pr[0]}") if callable(pr[1]) else pr[1]
                if story: return f'<g id="{p}_{pr[0]}_w" transform="translate({x_} {y_})" opacity="{op}"><g transform="scale({sc_})">{inner}</g></g>'
                return f'<g id="{p}_{pr[0]}_w" transform="translate({x_} {y_}) scale({sc_})" opacity="{op}">{inner}</g>'
            psvg = "".join(_pw(pr) for pr in s["props"])
            c0 = (s["pcam"] if self.portrait else s["cam"]); c1 = (s["pcam2"] if self.portrait else s["cam2"])
            if self.portrait and c0 is None: c0 = (s["cam"][0], s["cam"][1], s["cam"][2] * 9 / 16 * 1.5); c1 = None
            if c1 is None: c1 = (c0[0], c0[1] - (6 if i % 2 else -6), c0[2] * (.93 if i % 2 == 0 else 1.07))        # every shot drifts a little: slow push in or pull out
            x0, y0, z0 = self.cam_t(c0); x1, y1, z1 = self.cam_t(c1); d = s["t1"] - s["t0"]
            self.add(f'tl.set("#{p}",{{display:"block"}},{s["t0"]:.3f});' + (f'tl.set("#{p}",{{display:"none"}},{s["t1"]:.3f});' if i < len(self.shots) - 1 else ""))
            self.add(f'tl.fromTo("#{p}c",{{x:{x0},y:{y0},scale:{z0}}},{{x:{x1},y:{y1},scale:{z1},duration:{d:.3f},ease:"sine.inOut"}},{s["t0"]:.3f});')
            px = (c1[0] - c0[0]); self.add(f'tl.fromTo("#{p}f",{{x:{-px * .0:.1f}}},{{x:{px * .35:.1f},duration:{d:.3f},ease:"sine.inOut"}},{s["t0"]:.3f});tl.fromTo("#{p}m",{{x:0}},{{x:{px * .15:.1f},duration:{d:.3f},ease:"sine.inOut"}},{s["t0"]:.3f});')
            self.add(f'tl.to("#{p}c1,#{p}c2",{{x:"+=60",duration:{d:.2f},ease:"none"}},{s["t0"]:.3f});')
            self.ev(s["t0"], "new place" if (i == 0 or self.shots[i - 1]["place"] != s["place"]) else "new shot", f'{art.PLACE[s["place"]]} {s["tag"]}'.strip())
            for a in actors: self.add(self.idle(i, a, s, a[0] in fly))
            if s["who"] and any(a[0] == s["who"] for a in actors): self.add(self.talk(i, s, s["who"]))
            if s["trans"] == "iris" and i:
                t = s["t0"]; self.add(f'tl.fromTo("#iris",{{scale:0}},{{scale:1,duration:.34,ease:"power2.in"}},{t - .36:.2f});tl.to("#iris",{{scale:0,duration:.4,ease:"power2.out"}},{t + .02:.2f});'); self.snd.append((t - .3, "whoosh"))
            for f in s["fx"]:
                if self.portrait and f[0] in ("word",) and len(f) > 3 and f[3].get("landscape_only"): continue
                ff = f
                if f[0] == "word" and len(f) > 3:
                    o = dict(f[3]); o.pop("landscape_only", None)
                    if self.portrait and "p" in o: o.update(o.pop("p"))
                    o.pop("p", None); ff = (f[0], f[1], f[2], o)
                self.fx(i, s, ff)
            self.captions(i, s)
            shots_html.append((p, far, mid, near, asvg, psvg))
        body = ""
        for (p, far, mid, near, asvg, psvg) in shots_html:
            i = int(p[1:])
            body += (f'<div class="shot" id="{p}"><div class="cam" id="{p}c"><svg width="1920" height="1080" viewBox="0 0 1920 1080"><g id="{p}f">{far}</g><g id="{p}m">{mid}</g><g id="{p}n">{near}</g>{asvg}{psvg}</svg>'
                     + "".join(self.stage_html[i]) + '</div></div>')
        css = CSS.replace("VW", str(VW)).replace("VH", str(VH))
        if self.portrait: css = css.replace("CAPL", "70").replace("CAPB", "330").replace("CAPS", "84").replace("CAPO", "15").replace("SIGNS", "92")
        else: css = css.replace("CAPL", "150").replace("CAPB", "44").replace("CAPS", "62").replace("CAPO", "12").replace("SIGNS", "96")
        if self.portrait: wm = '<img id="wm" src="assets/watermark_short.png" style="left:273px;top:116px;width:533px;height:85px">'
        else: wm = '<img id="wm" src="assets/watermark.png" style="left:20px;top:18px;width:387px;height:68px">'
        band = ""
        if self.portrait and title_band: band = f'<div id="band"><div class="l1">{title_band[0]}</div><div class="l2">{title_band[1]}</div></div>'
        return f"""<!doctype html><html lang="en"><head><meta charset="UTF-8"/><meta name="viewport" content="width={VW}, height={VH}"/><script src="assets/gsap.min.js"></script>
<style>{css}</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{total:.3f}" data-width="{VW}" data-height="{VH}">
{body}<div id="hud">{"".join(self.hud)}{band}{wm}</div><div id="iris"></div></div>
<script>window.__timelines=window.__timelines||{{}};const tl=gsap.timeline({{paused:true}});
{chr(10).join(self.js)}
tl.to({{}},{{duration:.01}},{total - .01:.3f});window.__timelines["main"]=tl;tl.seek(0);</script></body></html>"""


def plan_gate(film, total, ep):
    ev = sorted(film.events); ts = [e[0] for e in ev] + [total]; gaps = [(ts[k], ts[k + 1]) for k in range(len(ts) - 1)]
    worst = max(gaps, key=lambda g: g[1] - g[0]); over = [g for g in gaps if g[1] - g[0] > MAXGAP]
    places = []
    for s in film.shots:
        if s["place"] not in places: places.append(s["place"])
    real = [p for p in places if not p.startswith("paper")]
    qs = [s["t0"] for s in film.shots if s["q"]]; qg = [b - a for a, b in zip([0] + qs, qs + [total])]
    cuts = sum(1 for e in ev if e[1] in ("new shot", "new place"))
    res = {"length": round(total, 1), "shots": len(film.shots), "visual_changes": len(ev), "mean_gap": round(total / max(1, len(ev)), 2), "longest_gap": round(worst[1] - worst[0], 2),
           "longest_gap_at": round(worst[0], 1), "over_6s": [(round(a, 1), round(b, 1)) for a, b in over], "places": real, "picture_boards": [p for p in places if p.startswith("paper")],
           "questions": len(qs), "longest_without_question": round(max(qg), 1) if qg else None, "first_words_at": round(film.shots[0]["v0"], 2), "shot_mean": round(total / max(1, cuts), 2)}
    fails = []
    if over: fails.append(f"{len(over)} stretches over {MAXGAP:g} s without a visual change: {res['over_6s']}")
    if not film.portrait:
        if len(real) < 6: fails.append(f"only {len(real)} places (need 6)")
        if total < 300: fails.append(f"only {total:.0f} s long (need 300)")
        if total > 390: fails.append(f"{total:.0f} s long (at most 390)")
        if ep.get("kind") == "story":
            beats = [s.get("beat", "") for s in film.shots]; res["beats"] = {b: beats.count(b) for b in dict.fromkeys(beats) if b}
            for b in ("hook", "goal", "obstacle1", "obstacle2", "obstacle3", "low", "solution", "ending"):
                if b not in beats: fails.append(f"the story has no '{b}' beat")
            if beats.count("fact") < 2: fails.append(f"only {beats.count('fact')} animal facts shown (2 or 3)")
            if not any(s.get("sung") for s in film.shots): fails.append("no song moment")
            if film.shots[0]["v0"] > 1.0 or film.shots[0].get("beat") != "hook": fails.append("the first shot must be the hook, spoken in the first 5 seconds")
            if beats and "ending" in beats and "low" in beats and not (beats.index("low") < beats.index("solution") < len(beats) - beats[::-1].index("ending")): fails.append("the beats are out of order (low moment, then the solution, then the ending)")
        else:
            if qg and max(qg) > 60: fails.append(f"{max(qg):.0f} s without a question to the viewer (about every 45 s)")
            if film.shots[0]["v0"] > 1.0 or not film.shots[0]["q"]: fails.append("the first shot must be the hook question, spoken in the first 5 seconds")
    res["fails"] = fails
    return res, ev


def mix_audio(film, total, ep):
    m = np.zeros(int(SR * (total + .5)), np.float32); env = np.full(len(m), 1.0, np.float32)
    for s in film.shots:
        if s["audio"] is not None:
            a0 = int(s["v0"] * SR); m[a0:a0 + len(s["audio"])] += s["audio"][:len(m) - a0] * 0.95; env[max(0, a0 - 2400):a0 + len(s["audio"]) + 2400] = 0.0 if s.get("sung") else 0.42
    env = np.convolve(env, np.ones(3600) / 3600, mode="same")
    mu = music(total + .5); fade = np.minimum(1, np.minimum(np.arange(len(mu)) / SR / 1.0, (len(mu) - np.arange(len(mu))) / SR / 2.0)); n = min(len(m), len(mu))
    m[:n] += mu[:n] * env[:n] * fade[:n] * ep.get("music", 0.5)
    for t, name in film.snd:
        x = sfx(name) * (0.5 if name in ("pop", "tick") else 0.7); a0 = int(max(0, t) * SR); m[a0:a0 + len(x)] += x[:len(m) - a0]
    return np.clip(m, -1, 1)


def need_4k(path, portrait):
    """Noelson, Nov 16: 4K is the minimum for every video on the channel. A finished cartoon file that is not 3840x2160 (2160x3840 for a Short) is refused."""
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0", path], capture_output=True, text=True).stdout.strip()
    want = "2160,3840" if portrait else "3840,2160"
    if r != want:
        bad = path.replace(".mp4", "_NOT_4K.mp4"); os.replace(path, bad); sys.exit(f"NOT 4K: {bad} is {r.replace(',', 'x')}, it must be {want.replace(',', 'x')}. Not a finished file.")
    print("4K", r.replace(",", "x"), path)


def main():
    if len(sys.argv) > 2 and sys.argv[1] == "--check4k":
        for f in sys.argv[2:]: need_4k(f, "short" in os.path.basename(f))
        return
    mod = importlib.import_module("episodes." + sys.argv[1]); ep = mod.EP; short = arg("--short")
    shots = [dict(s) for s in mod.SHOTS]; portrait = short is not None; band = None; sid = ep["id"]
    if portrait:
        sp = mod.SHORTS[int(short)]; shots = [dict(s) for s in mod.SHOTS if s["part"] == sp["part"]] if "part" in sp else [dict(mod.SHOTS[k]) for k in sp["shots"]]
        for s in sp.get("extra_first", []): shots.insert(0, dict(s))
        for s in sp.get("extra_last", []): shots.append(dict(s))
        shots[0]["trans"] = "cut"; band = sp["band"]; sid = sp["id"]
        if len(band[0]) > 15 or len(band[1]) > 10: sys.exit(f"the Short's title band is too long for two lines (15 and 10 letters at most): {band}")      # a third line sat on the picture's words (Nov 16)
    out = os.path.join(HERE, "out", ep["id"]); proj = os.path.join(out, "proj_" + ("p" if portrait else "l")); os.makedirs(os.path.join(proj, "assets"), exist_ok=True)
    total, miss, tot = voice_lines(ep, shots); total += ep.get("tail", 0.6) if not portrait else 0.4
    shots[0]["t0"] = 0.0      # the first shot owns the lead-in too: until Nov 16 the first 0.3 s of every video had no camera at all (the whole stage, or its left half in a Short), then jumped to the framing
    film = Film(ep, mod.STAGES, shots, portrait); html = film.build_html(total, band)
    res, ev = plan_gate(film, total, ep); res["words_placed"] = f"{tot - miss}/{tot}"
    if miss: res["fails"].append(f"word sync: {miss} of {tot} words could not be placed from the audio")
    json.dump({"id": sid, "total": total, "plan": res, "events": ev,
               "shots": [{k: s.get(k) for k in ("place", "say", "t0", "t1", "v0", "dur", "words", "part", "q", "tag", "who", "beat", "sung")} for s in shots]}, open(os.path.join(out, sid + "_timing.json"), "w"), indent=1)
    print(json.dumps(res, indent=1))
    if "--plan" in sys.argv: sys.exit(1 if res["fails"] else 0)
    for f, d in ((os.path.join(STUDIO, "vendor/package/dist/gsap.min.js"), "gsap.min.js"), (os.path.join(STUDIO, "vendor/f/package/files/baloo-2-latin-800-normal.woff2"), "baloo.woff2"),
                 (os.path.join(REPO, "brand/zoo/watermark.png"), "watermark.png"), (os.path.join(REPO, "brand/zoo/watermark_short.png"), "watermark_short.png")):
        shutil.copy(f, os.path.join(proj, "assets", d))
    for f in ("hyperframes.json", "meta.json", "package.json"): shutil.copy(os.path.join(STUDIO, "base", f), os.path.join(proj, f))
    open(os.path.join(proj, "index.html"), "w").write(html)
    env = dict(os.environ, HYPERFRAMES_BROWSER_PATH=CHROME)
    if arg("--stills"):
        r = subprocess.run(["hyperframes", "snapshot", "--at", arg("--stills"), "--json"], cwd=proj, env=env, capture_output=True, text=True)
        print(r.stdout[-1500:], r.stderr[-800:]); return
    wav = os.path.join(out, sid + ".wav"); sf.write(wav, mix_audio(film, total, ep), SR)
    silent = os.path.join(out, sid + "_silent.mp4"); res_flag = "portrait-4k" if portrait else "landscape-4k"
    cmd = ["hyperframes", "render", "-f", str(FPS), "-q", "standard", "--crf", "17", "-o", silent, "--quiet"]
    if "--draft" not in sys.argv: cmd += ["--resolution", res_flag]
    if arg("--from"): cmd += ["--start", arg("--from"), "--end", arg("--to")]
    if "--audio" not in sys.argv: subprocess.run(cmd, cwd=proj, env=env, check=True)      # --audio: new sound on the picture that is already rendered
    final = os.path.join(out, sid + ("_draft" if "--draft" in sys.argv else "") + ".mp4")
    a_in = ["-i", wav] if not arg("--from") else ["-ss", arg("--from"), "-to", arg("--to"), "-i", wav]
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", silent] + a_in + ["-map", "0:v", "-map", "1:a", "-c:v", "copy", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000",
                    "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", final], check=True)
    if "--draft" not in sys.argv: need_4k(final, portrait)
    print("FILM", final, round(total, 1), "s")


if __name__ == "__main__":
    main()
