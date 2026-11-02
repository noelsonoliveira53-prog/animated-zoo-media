#!/usr/bin/env python3
"""The Animated Zoo Short builder: episode JSON -> narrated, captioned 1080x1920 MP4.
Usage: python3 build.py <episode_id> [--draft]"""
import json, os, re, shutil, subprocess, sys
import numpy as np, soundfile as sf
from art import MILO, SCENES
from art2 import SCENES2
SCENES = {**SCENES, **SCENES2}

HERE = os.path.dirname(os.path.abspath(__file__))
SR = 24000
GAP = 0.35
LEAD = 0.25
VOICE = "af_heart"

def sh(cmd, **kw):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True, **kw)
    if r.returncode: raise SystemExit(f"FAILED: {cmd}\n{r.stdout[-2000:]}\n{r.stderr[-2000:]}")
    return r.stdout

def tts(text, out):
    if not os.path.exists(out):
        sh(f'hyperframes tts {json.dumps(text)} -v {VOICE} -o "{out}" --json')
    a, sr = sf.read(out, dtype="float32")
    if a.ndim > 1: a = a.mean(1)
    if sr != SR:
        a = np.interp(np.linspace(0, len(a), int(len(a) * SR / sr), endpoint=False), np.arange(len(a)), a)
    return a.astype(np.float32)

def pluck(freq, dur, amp=0.18):
    t = np.arange(int(SR * dur)) / SR
    tone = np.sin(2*np.pi*freq*t) + .35*np.sin(4*np.pi*freq*t) + .12*np.sin(6*np.pi*freq*t)
    return (amp * tone * np.exp(-t * 5.5)).astype(np.float32)

def music(total):
    # gentle ukulele-like arpeggio, C - G - Am - F at 100 bpm
    chords = [[261.6, 329.6, 392.0, 523.3], [196.0, 293.7, 392.0, 493.9],
              [220.0, 261.6, 329.6, 440.0], [174.6, 261.6, 349.2, 440.0]]
    step = 60 / 100 / 2
    out = np.zeros(int(SR * (total + 2)), np.float32)
    i, t = 0, 0.0
    while t < total:
        ch = chords[(i // 8) % 4]
        n = pluck(ch[[0, 2, 1, 3, 2, 1, 3, 2][i % 8]], 0.9)
        s = int(t * SR); out[s:s+len(n)] += n[:len(out)-s]
        if i % 8 == 0:
            b = pluck(ch[0] / 2, 1.6, .22); out[s:s+len(b)] += b[:len(out)-s]
        i += 1; t += step
    return out[:int(SR * total)]

def pop():
    t = np.arange(int(SR * .14)) / SR
    f = 500 + 900 * t / .14
    return (.35 * np.sin(2*np.pi*np.cumsum(f)/SR) * np.exp(-t*28)).astype(np.float32)

def chunks(text, n=4):
    w = text.split()
    out, cur = [], []
    for x in w:
        cur.append(x)
        if len(cur) >= n or re.search(r"[.!?,]$", x) and len(cur) >= 2:
            out.append(" ".join(cur)); cur = []
    if cur:
        if out and len(cur) == 1: out[-1] += " " + cur[0]
        else: out.append(" ".join(cur))
    return out

def act_extra(act, t, d, animal):
    known = {"tongue","tongue_long","sun","xray","coat","waddle","big","swim","hug"}
    if act in known or (act == "legs" and animal in ("penguin", "elephant")): return ""
    from long import acts_js
    return acts_js(act, "", round(t, 3), round(d, 3), animal)

def act_js(act, t, d, animal):
    J = []
    a = J.append
    if act == "hook":
        a(f'tl.fromTo("#qmark",{{scale:0,opacity:0}},{{scale:1,opacity:1,duration:.45,ease:"back.out(2.5)"}},{t+.3})')
        a(f'tl.to("#qmark",{{rotation:12,duration:.5,yoyo:true,repeat:{max(1,int(d/.5)-2)},ease:"sine.inOut"}},{t+.8})')
        a(f'tl.to("#qmark",{{scale:0,opacity:0,duration:.3}},{t+d-.1})')
    elif act == "milo_in":
        a(f'tl.fromTo("#milobox",{{x:-420,y:-120,opacity:1}},{{x:0,y:0,duration:1.2,ease:"power2.out"}},{t})')
    elif act in ("tongue", "tongue_long"):
        a(f'tl.to("#tongue",{{scaleX:{.75 if act=="tongue" else 1.0},svgOrigin:"745 281",duration:.6,ease:"back.out(1.6)"}},{t+.3})')
        a(f'tl.to("#leaves",{{rotation:3,svgOrigin:"960 420",duration:.25,yoyo:true,repeat:5}},{t+.8})')
        if act == "tongue_long":
            a(f'tl.fromTo("#badge",{{scale:0,opacity:0}},{{scale:1,opacity:1,duration:.4,ease:"back.out(2)"}},{t+.4})')
            a(f'tl.to("#badge",{{opacity:0,duration:.3}},{t+d-.1})')
        else:
            a(f'tl.to("#tongue",{{scaleX:.15,svgOrigin:"745 281",duration:.4}},{t+d-.3})')
    elif act == "sun":
        a(f'tl.to("#sunshield",{{opacity:1,duration:.5}},{t+.4})')
        a(f'tl.to("#tongue",{{scaleX:.6,svgOrigin:"745 281",duration:.5}},{t+.4})')
    elif act == "legs" and animal == "penguin":
        a(f'tl.to("#animal",{{scaleY:.96,svgOrigin:"540 1000",duration:.3,yoyo:true,repeat:3}},{t+.2})')
    elif act == "xray":
        a(f'tl.to("#xray",{{opacity:1,duration:.5}},{t+.9})')
    elif act == "coat":
        a(f'tl.to("#xray",{{opacity:0,duration:.4}},{t+.1})')
        a(f'tl.to("#coat",{{opacity:1,duration:.5}},{t+.4})')
    elif act == "waddle":
        a(f'tl.to("#animal",{{rotation:6,svgOrigin:"540 1000",duration:.35,yoyo:true,repeat:{max(1,int(d/.35)-1)},ease:"sine.inOut"}},{t})')
        a(f'tl.to("#animal",{{rotation:0,duration:.2}},{t+d})')
    elif act == "big":
        a(f'tl.to("#animal",{{scale:1.07,svgOrigin:"520 1000",duration:.5,ease:"back.out(2)"}},{t+.2})')
        a(f'tl.fromTo("#badge",{{scale:0,opacity:0}},{{scale:1,opacity:1,duration:.4,ease:"back.out(2)"}},{t+.5})')
        a(f'tl.to("#badge",{{opacity:0,duration:.3}},{t+d-.1})')
        a(f'tl.to("#animal",{{scale:1,duration:.4}},{t+d-.2})')
    elif act == "legs":
        a(f'tl.to("#legsglow",{{opacity:1,duration:.4}},{t+.5})')
        a(f'tl.to("#legsglow",{{opacity:0,duration:.3}},{t+d})')
    elif act == "swim":
        a(f'tl.to("#water",{{opacity:1,duration:.6}},{t+1.6})')
        a(f'tl.to("#animal",{{y:-30,duration:.6,yoyo:true,repeat:3,ease:"sine.inOut"}},{t+1.8})')
        a(f'tl.to("#water",{{opacity:0,duration:.5}},{t+d-.2})')
    elif act == "hug":
        a(f'tl.to("#trunk",{{rotation:-38,svgOrigin:"850 570",duration:.6,ease:"back.out(1.5)"}},{t+.4})')
        a(f'tl.fromTo("#heart",{{scale:0,opacity:0}},{{scale:1.15,opacity:1,duration:.5,ease:"back.out(3)"}},{t+1.0})')
        a(f'tl.to("#heart",{{scale:1,duration:.3,yoyo:true,repeat:5}},{t+1.5})')
    elif act not in ("hook","milo_in","outro") and act_extra(act, t, d, animal):
        a(act_extra(act, t, d, animal))
    elif act == "outro":
        a(f'tl.to("#label",{{opacity:0,scale:.8,duration:.3}},{t})')
        a(f'tl.to("#milobox",{{x:370,y:30,scale:1.15,duration:.9,ease:"power2.inOut"}},{t})')
        a(f'tl.fromTo("#outro",{{y:60,opacity:0}},{{y:0,opacity:1,duration:.6,ease:"back.out(2)"}},{t+.5})')
    return "\n".join(J)

def build(ep, draft=False):
    out = os.path.join(HERE, "out", ep["id"]); proj = os.path.join(out, "proj")
    os.makedirs(os.path.join(proj, "assets"), exist_ok=True)
    shutil.copy(os.path.join(HERE, "vendor/package/dist/gsap.min.js"), os.path.join(proj, "assets/gsap.min.js"))
    shutil.copy(os.path.join(HERE, "vendor/f/package/files/baloo-2-latin-800-normal.woff2"), os.path.join(proj, "assets/baloo.woff2"))

    # 1. narration
    t, beats, voice = LEAD, [], []
    for i, b in enumerate(ep["beats"]):
        a = tts(b["say"], os.path.join(out, f"beat{i}.wav"))
        beats.append({**b, "t": t, "d": len(a) / SR}); voice.append((t, a))
        t += len(a) / SR + GAP
    total = round(t + 1.2, 2)

    # 2. audio mix
    mix = np.zeros(int(SR * total), np.float32)
    for st, a in voice:
        s = int(st * SR); mix[s:s+len(a)] += a
    m = music(total)
    env = np.ones_like(m) * .45
    for st, a in voice:  # duck under voice
        s, e = int(st * SR), int((st + len(a) / SR) * SR); env[s:e] = .28
    env = np.convolve(env, np.ones(2400) / 2400, mode="same")
    fade = np.minimum(1, np.minimum(np.arange(len(m)) / SR / 1.0, (len(m) - np.arange(len(m))) / SR / 1.2))
    mix += m * env * fade
    p = pop()
    for b in beats:
        s = int(max(0, b["t"] - .12) * SR); mix[s:s+len(p)] += p[:len(mix)-s]
    sf.write(os.path.join(out, "mix.wav"), np.clip(mix, -1, 1), SR)

    # 3. captions
    caps, js = [], []
    for bi, b in enumerate(beats):
        cs = chunks(b["say"]); L = sum(len(c) for c in cs); ct = b["t"]
        for c in cs:
            cd = b["d"] * len(c) / L
            caps.append((ct, cd, c)); ct += cd
    cap_html = "\n".join(
        f'<div class="cap" id="c{i}"><span>{c}</span></div>' for i, (_, _, c) in enumerate(caps))
    for i, (st, d, _) in enumerate(caps):
        js.append(f'tl.set("#c{i}",{{opacity:1}},{st:.3f});tl.fromTo("#c{i} span",{{scale:.82}},{{scale:1,duration:.18,ease:"back.out(3)"}},{st:.3f});tl.set("#c{i}",{{opacity:0}},{st+d:.3f})')
    for b in beats:
        js.append(act_js(b["act"], b["t"], b["d"], ep["animal"]))

    badge = {"giraffe": "AS LONG AS YOUR ARM!", "elephant": "BIGGEST ON LAND!"}.get(ep["animal"], "")
    html = f"""<!doctype html>
<html lang="en" data-resolution="portrait"><head><meta charset="UTF-8"/>
<meta name="viewport" content="width=1080, height=1920"/>
<script src="assets/gsap.min.js"></script>
<style>
@font-face{{font-family:"Baloo";src:url(assets/baloo.woff2) format("woff2");font-weight:800}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:{ep["bg"][1]}}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;font-family:"Baloo",sans-serif;
  background:linear-gradient(180deg,{ep["bg"][0]} 0%,{ep["bg"][1]} 70%)}}
#brand{{position:absolute;top:120px;width:100%;text-align:center;font-size:44px;color:#1c5fc4;letter-spacing:.06em}}
#label{{position:absolute;top:168px;width:100%;text-align:center;font-size:150px;line-height:1;color:#fff;
  -webkit-text-stroke:14px #1c5fc4;paint-order:stroke fill;text-shadow:0 10px 0 rgba(0,0,0,.12)}}
#scene{{position:absolute;left:0;top:470px}}
#floor{{position:absolute;left:0;right:0;top:1560px;bottom:0;background:{ep.get("floor","#5fb043")}}}
#milobox{{position:absolute;left:40px;top:330px;opacity:0}}
#qmark{{position:absolute;right:70px;top:360px;width:200px;height:200px;border-radius:50%;background:#ff5c8a;color:#fff;
  font-size:170px;line-height:215px;text-align:center;box-shadow:0 12px 0 rgba(0,0,0,.15);opacity:0}}
#badge{{position:absolute;left:0;right:0;top:1290px;margin:auto;width:max-content;padding:14px 38px;border-radius:60px;
  background:#ffeb3b;color:#1a1a2e;font-size:64px;box-shadow:0 10px 0 rgba(0,0,0,.15);opacity:0}}
.cap{{position:absolute;left:60px;right:60px;top:1520px;text-align:center;opacity:0}}
.cap span{{display:inline-block;padding:10px 34px 2px;border-radius:34px;background:rgba(26,26,46,.82);color:#fff;
  font-size:84px;line-height:1.12}}
#zzz{{position:absolute;right:120px;top:520px;font-size:120px;color:#5c6bc0;opacity:0}}
#kind{{position:absolute;left:0;right:0;top:1290px;margin:auto;width:max-content;padding:12px 40px 2px;border-radius:50px;background:#fff;color:#1c5fc4;font-size:60px;opacity:0}}
#outro{{position:absolute;left:0;right:0;top:190px;text-align:center;opacity:0}}
#outro div{{display:inline-block;padding:20px 44px 10px;border-radius:44px;background:#fff;color:#1c5fc4;font-size:76px;
  box-shadow:0 12px 0 rgba(0,0,0,.12)}}
</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{total}" data-width="1080" data-height="1920">
  <div id="floor"></div>
  <div id="scene">{SCENES[ep["animal"]]}</div>
  <div id="brand">THE ANIMATED ZOO</div>
  <div id="label">{ep["top"]}</div>
  <div id="qmark">?</div>
  <div id="badge"><span>{badge}</span></div><div id="zzz">Z z z</div><div id="kind">💙 Be kind!</div>
  <div id="milobox">{MILO}</div>
  <div id="outro"><div>See you at the zoo! 💙</div></div>
  {cap_html}
</div>
<script>
window.__timelines = window.__timelines || {{}};
const tl = gsap.timeline({{paused:true}});
gsap.set("#tongue",{{scaleX:0.15,svgOrigin:"745 281"}});
tl.to("#cloud1",{{x:-160,duration:{total},ease:"none"}},0);
tl.to("#wing",{{rotation:-28,svgOrigin:"78 122",duration:.18,yoyo:true,repeat:{int(total/.18)},ease:"sine.inOut"}},0);
tl.to("#milo",{{y:-10,duration:.6,yoyo:true,repeat:{int(total/.6)},ease:"sine.inOut"}},0);
tl.fromTo("#label",{{scale:.6,opacity:0}},{{scale:1,opacity:1,duration:.4,ease:"back.out(2.5)"}},0);
{chr(10).join(js)}
tl.to({{}},{{duration:.01}},{total-.01});
window.__timelines["main"] = tl; tl.seek(0);
</script></body></html>"""
    open(os.path.join(proj, "index.html"), "w").write(html)
    json.dump({"total": total, "beats": beats, "captions": caps}, open(os.path.join(out, "timing.json"), "w"), indent=1)

    if os.environ.get('NORENDER'): print(proj, total); return
    # 4. render + mux + loudness
    q = "draft" if draft else "standard"
    sh(f'cd "{proj}" && hyperframes render -q {q} -o "{out}/silent.mp4"', timeout=1800)
    final = os.path.join(HERE, "out", f'{ep["id"]}{"_draft" if draft else ""}.mp4')
    sh(f'ffmpeg -y -i "{out}/silent.mp4" -i "{out}/mix.wav" -map 0:v -map 1:a -c:v copy '
       f'-af loudnorm=I=-16:TP=-1.5:LRA=11 -ar 48000 -c:a aac -b:a 192k -shortest "{final}"')
    print(final, total)

if __name__ == "__main__":
    eps = {e["id"]: e for f in ("episodes.json", "shorts2.json") for e in json.load(open(os.path.join(HERE, f)))}
    build(eps[sys.argv[1]], "--draft" in sys.argv)
