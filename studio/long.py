#!/usr/bin/env python3
"""The Animated Zoo long-form builder (1920x1080, ~8 min). Usage: python3 long.py <episode.json> [--norender]"""
import json, os, re, shutil, subprocess, sys
import numpy as np, soundfile as sf
from art import MILO, SCENES
from art2 import SCENES2
import fx
from channel import C, NAME as CHANNEL
from art_space import SCENES3, SPACE_TITLE
from art_dino import SCENES4, DINO_TITLE, NAMES4
from art_wild import SCENES5, WILD_TITLE, NAMES5
from art_truck import SCENES6, TRUCK_TITLE, NAMES6
from art_bloop import SCENES7, BLOOP_TITLE, NAMES7
from art_fruity import SCENES8, FRUITY_TITLE, NAMES8
from art_moon import SCENES9, MOON_TITLE, NAMES9
from art_gizmo import SCENES10, GIZMO_TITLE, NAMES10
from build import tts as _tts, music, pop, chunks, sh, SR

HERE = os.path.dirname(os.path.abspath(__file__))
ALL = {**SCENES, **SCENES2, **SCENES3, **SCENES4, **SCENES5, **SCENES6, **SCENES7, **SCENES8, **SCENES9, **SCENES10}
ALL["title"] = {"gizmo": GIZMO_TITLE if os.environ.get("GZTITLE") == "lab" else SPACE_TITLE.replace("SPACE KIDS ACADEMY", "GIZMO EXPLAINS").replace('fill="#6c4cd6"', 'fill="#3561d9"'), "space": SPACE_TITLE, "dino": DINO_TITLE, "wild": WILD_TITLE, "truck": TRUCK_TITLE, "bloop": BLOOP_TITLE, "fruity": FRUITY_TITLE, "moon": MOON_TITLE}.get(CHANNEL, ALL["title"])
GAP, SEG_GAP, SPEED, THINK = 0.7, 1.4, C.get("speed", 0.85), 2.6
NAMES = {"polarbear": "POLAR BEAR", "turtle": "SEA TURTLE", "monkey": "SPIDER MONKEY", "redpanda": "RED PANDA", "seaotter": "SEA OTTER", **NAMES4, **NAMES5, **NAMES6, **NAMES7, **NAMES8, **NAMES9, **NAMES10}
ORIGIN = {"monkey": "640 430", "owl": "540 500", "sloth": "545 350", "koala": "435 600"}

def tts(text, out):
    if not os.path.exists(out):
        sh(f'hyperframes tts {json.dumps(text)} -v {C["voice"]} -s {SPEED} -o "{out}" --json')
    return _tts(text, out)

def prep_scene(key, i):
    s = fx.enhance(ALL[key], key)
    s = s.replace('viewBox="0 0 1080 1100" width="1080" height="1100"', 'viewBox="-420 0 1920 1080" width="1920" height="1080"', 1)
    s = re.sub(r'id="([\w-]+)"', lambda m: f'id="s{i}-{m.group(1)}"', s)
    s = re.sub(r'url\(#([\w-]+)\)', lambda m: f'url(#s{i}-{m.group(1)})', s)
    return s

def acts_js(acts, p, t, d, key):
    """acts: '+'-joined list. p = scene id prefix like 's3-'. Returns JS lines."""
    J = []; a = J.append
    A = f'"#{p}animal"'
    for act in acts.split("+"):
        name, _, arg = act.partition(":")
        if name == "enter":
            a(f'tl.fromTo({A},{{x:-1500,svgOrigin:"540 1000"}},{{x:0,svgOrigin:"540 1000",duration:.9,ease:"back.out(1.4)"}},{t})')
            a(f'tl.fromTo({A},{{scaleY:.8,scaleX:1.15,svgOrigin:"540 1000"}},{{scaleY:1,scaleX:1,duration:.5,ease:"elastic.out(1,.4)"}},{t+.8})')
        elif name == "bob":
            a(f'tl.to({A},{{y:-14,duration:.5,yoyo:true,repeat:{max(1, int(d/.5)//2*2-1)},ease:"sine.inOut"}},{t})')
        elif name == "zoom":
            a(f'tl.to({A},{{scale:1.08,svgOrigin:"540 1000",duration:.5,ease:"back.out(2)"}},{t+.2})')
            a(f'tl.to({A},{{scale:1,svgOrigin:"540 1000",duration:.4}},{t+d})')
        elif name == "wiggle":
            a(f'tl.to({A},{{rotation:3,svgOrigin:"540 1000",duration:.3,yoyo:true,repeat:{max(1, int(d/.3)//2*2-1)},ease:"sine.inOut"}},{t})')
        elif name == "hop":
            a(f'tl.to({A},{{y:-90,duration:.32,yoyo:true,repeat:{max(1, int(d/.32)//2*2-1)},ease:"power1.out"}},{t})')
        elif name == "swing":
            a(f'tl.to({A},{{rotation:8,svgOrigin:"{ORIGIN.get(key, "540 1000")}",duration:.6,yoyo:true,repeat:{max(1, int(d/.6)//2*2-1)},ease:"sine.inOut"}},{t})')
        elif name == "q":
            a(f'tl.fromTo("#qmark",{{scale:0,opacity:0}},{{scale:1,opacity:1,duration:.4,ease:"back.out(2.5)"}},{t+.2})')
            a(f'tl.to("#qmark",{{rotation:12,duration:.5,yoyo:true,repeat:{max(1, int(d/.5)-2)},ease:"sine.inOut"}},{t+.6})')
            a(f'tl.to("#qmark",{{scale:0,opacity:0,duration:.25}},{t+d+.3})')
        elif name == "badge":
            a(f'tl.set("#badge span",{{textContent:{json.dumps(arg)}}},{t})')
            a(fx.confetti_js(t + .35, n=36, spread=700, seed=int(t)))
            a(f'tl.fromTo("#badge",{{scale:0,opacity:0}},{{scale:1,opacity:1,duration:.4,ease:"back.out(2)"}},{t+.3})')
            a(f'tl.to("#badge",{{opacity:0,duration:.3}},{t+d+.3})')
        elif name in ("fx", "fx2"):
            a(f'tl.to("#{p}{name}",{{opacity:1,duration:.5}},{t+.3})')
        elif name in ("fxoff", "fx2off"):
            a(f'tl.to("#{p}{name[:-3]}",{{opacity:0,duration:.4}},{t})')
        elif name == "zzz":
            a(f'tl.fromTo("#zzz",{{opacity:0,y:30}},{{opacity:1,y:0,duration:.5}},{t+.2})')
            a(f'tl.to("#zzz",{{opacity:0,duration:.4}},{t+d+.2})')
        elif name == "kind":
            a(f'tl.fromTo("#kind",{{scale:0,opacity:0}},{{scale:1,opacity:1,duration:.4,ease:"back.out(2)"}},{t+.2})')
            a(f'tl.to("#kind",{{opacity:0,duration:.3}},{t+d+.2})')
        elif name == "color":   # octopus camouflage
            a(f'tl.to("#{p}animal .ocf",{{attr:{{fill:"#26a69a"}},duration:1}},{t+.4})')
            a(f'tl.to("#{p}animal .ocf2",{{attr:{{fill:"#4db6ac"}},duration:1}},{t+.4})')
            a(f'tl.to("#{p}animal .ocs",{{attr:{{stroke:"#26a69a"}},duration:1}},{t+.4})')
            a(f'tl.to("#{p}animal .ocf",{{attr:{{fill:"#ff7043"}},duration:.8}},{t+d+1.5})')
            a(f'tl.to("#{p}animal .ocf2",{{attr:{{fill:"#ff8a65"}},duration:.8}},{t+d+1.5})')
            a(f'tl.to("#{p}animal .ocs",{{attr:{{stroke:"#ff7043"}},duration:.8}},{t+d+1.5})')
        elif name == "headturn":
            a(f'tl.to("#{p}head",{{scaleX:.2,svgOrigin:"540 470",duration:.45,yoyo:true,repeat:5,ease:"sine.inOut"}},{t+.3})')
            a(f'tl.to("#{p}head",{{rotation:14,svgOrigin:"540 470",duration:.6,yoyo:true,repeat:3,ease:"sine.inOut"}},{t+.3})')
        elif name == "sink":
            a(f'tl.to("#{p}fx2",{{opacity:1,duration:.6}},{t+.2})')
            a(f'tl.to({A},{{y:70,duration:.6,yoyo:true,repeat:3,ease:"sine.inOut"}},{t+.6})')
            a(f'tl.to("#{p}fx2",{{opacity:0,duration:.5}},{t+d+.2})')
        elif name == "tail":   # monkey tail glow
            a(f'tl.to("#{p}fx",{{attr:{{stroke:"#ffca28"}},duration:.4,yoyo:true,repeat:5}},{t+.3})')
        # giraffe / penguin / elephant specials
        elif name in ("tongue", "tongue_long"):
            a(f'tl.to("#{p}tongue",{{scaleX:{.75 if name=="tongue" else 1.0},svgOrigin:"745 281",duration:.6,ease:"back.out(1.6)"}},{t+.3})')
            a(f'tl.to("#{p}leaves",{{rotation:3,svgOrigin:"960 420",duration:.25,yoyo:true,repeat:5}},{t+.8})')
        elif name == "sun":
            a(f'tl.to("#{p}sunshield",{{opacity:1,duration:.5}},{t+.4})')
            a(f'tl.to("#{p}sunshield",{{opacity:0,duration:.4}},{t+d+.3})')
        elif name == "xray":
            a(f'tl.to("#{p}xray",{{opacity:1,duration:.5}},{t+.6})')
            a(f'tl.to("#{p}xray",{{opacity:0,duration:.4}},{t+d+.6})')
        elif name == "waddle":
            a(f'tl.to({A},{{rotation:6,svgOrigin:"540 1000",duration:.35,yoyo:true,repeat:{max(1, int(d/.35)//2*2-1)},ease:"sine.inOut"}},{t})')
        elif name == "legs":
            a(f'tl.to("#{p}legsglow",{{opacity:1,duration:.4}},{t+.5})')
            a(f'tl.to("#{p}legsglow",{{opacity:0,duration:.3}},{t+d+.3})')
        elif name == "swim":
            a(f'tl.to("#{p}water",{{opacity:1,duration:.6}},{t+.8})')
            a(f'tl.to({A},{{y:-30,duration:.6,yoyo:true,repeat:3,ease:"sine.inOut"}},{t+1})')
            a(f'tl.to("#{p}water",{{opacity:0,duration:.5}},{t+d+.3})')
        elif name == "hug":
            a(f'tl.to("#{p}trunk",{{rotation:-38,svgOrigin:"850 570",duration:.6,ease:"back.out(1.5)"}},{t+.4})')
            a(f'tl.fromTo("#{p}heart",{{scale:0,opacity:0}},{{scale:1.15,opacity:1,svgOrigin:"930 360",duration:.5,ease:"back.out(3)"}},{t+1})')
            a(f'tl.to("#{p}trunk",{{rotation:0,svgOrigin:"850 570",duration:.5}},{t+d+.3})')
            a(f'tl.to("#{p}heart",{{opacity:0,duration:.4}},{t+d+.3})')
        elif name == "trunk":
            a(f'tl.to("#{p}trunk",{{rotation:-14,svgOrigin:"850 570",duration:.45,yoyo:true,repeat:3,ease:"sine.inOut"}},{t+.3})')
    return "\n".join(J)

def build(ep_path, norender=False):
    ep = json.load(open(ep_path))
    eid = ep["id"]; out = os.path.join(HERE, "out", eid); proj = os.path.join(out, "proj")
    os.makedirs(os.path.join(proj, "assets"), exist_ok=True)
    shutil.copy(os.path.join(HERE, "vendor/package/dist/gsap.min.js"), os.path.join(proj, "assets/gsap.min.js"))
    shutil.copy(os.path.join(HERE, "vendor/f/package/files/baloo-2-latin-800-normal.woff2"), os.path.join(proj, "assets/baloo.woff2"))

    # segments: intro(title) + animals + recap + outro(title)
    segs = [{"scene": "title", "label": "", "lines": ep["intro"]}]
    for a in ep["animals"]:
        segs.append({"scene": a["key"], "label": NAMES.get(a["key"], a["key"].upper()), "lines": a["lines"]})
    segs.append({"scene": "recap", "label": "LET'S REMEMBER!", "lines": ep["recap"]})
    segs.append({"scene": "title", "label": "", "lines": ep["outro"]})

    scene_keys = ["title"] + [a["key"] for a in ep["animals"]]
    sidx = {k: i for i, k in enumerate(scene_keys)}

    t, voice, beats, n = 0.6, [], [], 0
    for si, s in enumerate(segs):
        s["t0"] = t
        for li, (say, act) in enumerate(s["lines"]):
            a = tts(say, os.path.join(out, f"v{si:02d}_{li:02d}.wav")); d = len(a) / SR
            scene = act.split("@")[1] if "@" in act else s["scene"]
            beats.append({"seg": si, "t": t, "d": d, "say": say, "act": act.split("@")[0], "scene": scene})
            voice.append((t, a)); t += d + GAP + (THINK if 'q' in act.split('@')[0].split('+') else 0)
        s["t1"] = t; t += SEG_GAP
    total = round(t + 1.5, 2)
    print("duration", total)

    mix = np.zeros(int(SR * total), np.float32)
    for st, a in voice: s0 = int(st * SR); mix[s0:s0+len(a)] += a
    m = music(total); env = np.full(len(m), .42, np.float32)
    for st, a in voice: env[int(st*SR):int((st+len(a)/SR)*SR)] = .24
    env = np.convolve(env, np.ones(2400)/2400, mode="same")
    fade = np.minimum(1, np.minimum(np.arange(len(m))/SR/1.5, (len(m)-np.arange(len(m)))/SR/2))
    mix += m * env * fade
    p = pop()
    for s in segs[1:]:
        s0 = int(max(0, s["t0"] - .3) * SR); mix[s0:s0+len(p)] += p[:len(mix)-s0]
    sf.write(os.path.join(out, "mix.wav"), np.clip(mix, -1, 1), SR)

    # scene visibility windows
    js, windows = [], []
    for b in beats:
        sc = "title" if b["scene"] == "title" else b["scene"]
        if windows and windows[-1][0] == sc: windows[-1][2] = b["t"] + b["d"]
        else: windows.append([sc, b["t"], b["t"] + b["d"]])
    for wi, (sc, st, en) in enumerate(windows):
        i = sidx[sc]; start = 0 if wi == 0 else st - .45
        end = total if wi == len(windows) - 1 else windows[wi+1][1] - .45
        js.append(f'tl.set("#scene{i}",{{opacity:0}},0);' if wi == 0 else '')
        js.append(f'tl.to("#scene{i}",{{opacity:1,duration:.45}},{max(0,start-.001):.3f});')
        if wi < len(windows) - 1:
            nxt = windows[wi+1][0]
            if nxt != sc: js.append(f'tl.to("#scene{i}",{{opacity:0,duration:.45}},{end+.45:.3f});')
    # labels per segment
    labels = ""
    for si, s in enumerate(segs):
        if s["label"]:
            labels += f'<div class="label" id="lab{si}">{s["label"]}</div>'
            js.append(f'tl.fromTo("#lab{si}",{{opacity:0,x:-40}},{{opacity:1,x:0,duration:.45,ease:"back.out(2)"}},{s["t0"]:.3f});tl.to("#lab{si}",{{opacity:0,duration:.3}},{s["t1"]:.3f});')
    # milo: big centre on title segments, corner otherwise
    js.append(f'tl.set("#milobox",{{x:1250,y:110,scale:1.5}},0);tl.fromTo("#milobox",{{opacity:0}},{{opacity:1,duration:.6}},.2);')
    js.append(f'tl.to("#milobox",{{x:0,y:0,scale:1,duration:1,ease:"power2.inOut"}},{segs[1]["t0"]-1:.3f});')
    js.append(f'tl.to("#milobox",{{x:1250,y:110,scale:1.5,duration:1,ease:"power2.inOut"}},{segs[-1]["t0"]-.8:.3f});')
    js.append(f'tl.fromTo("#eptitle",{{opacity:0,y:30}},{{opacity:1,y:0,duration:.6}},.4);tl.to("#eptitle",{{opacity:0,duration:.4}},{segs[0]["t1"]:.3f});')
    js.append(f'tl.fromTo("#bye",{{opacity:0,y:30}},{{opacity:1,y:0,duration:.6}},{segs[-1]["t0"]+.5:.3f});')
    # captions + acts
    caps = []
    for b in beats:
        cs = chunks(b["say"], 5); L = sum(len(c) for c in cs); ct = b["t"]
        for c in cs:
            cd = b["d"] * len(c) / L; caps.append((ct, cd, c)); ct += cd
        sc = b["scene"]
        if sc != "title" and b["act"]:
            js.append(acts_js(b["act"], f's{sidx[sc]}-', round(b["t"], 3), round(b["d"], 3), sc))
    extra = ""
    for s_ in segs[1:]:
        w0 = s_["t0"] - .95
        extra += f'tl.fromTo("#wipe",{{scale:0}},{{scale:1,duration:.4,ease:"power2.in"}},{w0:.2f});tl.to("#wipe",{{scale:0,duration:.45,ease:"power2.out"}},{w0+.5:.2f});'
    for (sc_, st_, en_) in windows:
        extra += f'tl.fromTo("#scene{sidx[sc_]}",{{scale:1}},{{scale:1.05,duration:{max(1,en_-st_+.5):.2f},ease:"none"}},{st_:.2f});'
    cap_html = "".join(f'<div class="cap" id="c{i}"><span>{c}</span></div>' for i, (_, _, c) in enumerate(caps))
    for i, (st, d, _) in enumerate(caps):
        js.append(f'tl.set("#c{i}",{{opacity:1}},{st:.3f});tl.fromTo("#c{i} span",{{scale:.85}},{{scale:1,duration:.18,ease:"back.out(3)"}},{st:.3f});tl.set("#c{i}",{{opacity:0}},{st+d:.3f});')

    scenes_html = "".join(
        f'<div class="scene" id="scene{i}" style="opacity:{1 if i==0 else 0}">{prep_scene(k, i)}</div>' for i, k in enumerate(scene_keys))
    html = f"""<!doctype html><html lang="en"><head><meta charset="UTF-8"/>
<meta name="viewport" content="width=1920, height=1080"/><script src="assets/gsap.min.js"></script>
<style>
@font-face{{font-family:"Baloo";src:url(assets/baloo.woff2) format("woff2");font-weight:800}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1920px;height:1080px;overflow:hidden;background:#8fd3ff}}
#root{{position:relative;width:1920px;height:1080px;overflow:hidden;font-family:"Baloo",sans-serif;background:{C["root_bg"]}}}
.scene{{position:absolute;inset:0;transform-origin:50% 70%}}
{fx.CONFETTI_CSS}
#wipe{{position:absolute;left:50%;top:50%;width:2400px;height:2400px;margin:-1200px;border-radius:50%;background:radial-gradient(circle,#ffe066 0 18%,#2f80ed 19%);transform:scale(0)}}
.label{{position:absolute;left:60px;top:40px;font-size:110px;line-height:1;color:#fff;-webkit-text-stroke:12px #1c5fc4;paint-order:stroke fill;opacity:0}}
#brand{{position:absolute;right:50px;top:36px;font-size:34px;color:#1c5fc4;letter-spacing:.06em;background:rgba(255,255,255,.75);padding:6px 22px 0;border-radius:24px}}
#milobox{{position:absolute;left:60px;top:180px;opacity:0}}
#qmark{{position:absolute;right:160px;top:150px;width:180px;height:180px;border-radius:50%;background:#ff5c8a;color:#fff;font-size:150px;line-height:195px;text-align:center;box-shadow:0 10px 0 rgba(0,0,0,.15);opacity:0}}
#badge{{position:absolute;right:120px;top:360px;opacity:0}}
#badge span{{display:inline-block;padding:12px 40px 2px;border-radius:50px;background:#ffeb3b;color:#1a1a2e;font-size:66px;box-shadow:0 10px 0 rgba(0,0,0,.15)}}
#zzz{{position:absolute;right:300px;top:200px;font-size:120px;color:#5c6bc0;opacity:0}}
#kind{{position:absolute;right:120px;top:380px;padding:12px 40px 2px;border-radius:50px;background:#fff;color:#1c5fc4;font-size:60px;box-shadow:0 10px 0 rgba(0,0,0,.12);opacity:0}}
.cap{{position:absolute;left:160px;right:160px;bottom:40px;text-align:center;opacity:0}}
.cap span{{display:inline-block;padding:8px 36px 0;border-radius:30px;background:rgba(26,26,46,.82);color:#fff;font-size:70px;line-height:1.15}}
#eptitle,#bye{{position:absolute;left:0;right:0;top:{"690px" if CHANNEL=="zoo" else "820px"};text-align:center;opacity:0}}
#eptitle div,#bye div{{display:inline-block;padding:14px 50px 4px;border-radius:44px;background:#fff;color:#1c5fc4;font-size:76px;box-shadow:0 12px 0 rgba(0,0,0,.12)}}
</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{total}" data-width="1920" data-height="1080">
{scenes_html}
<div id="brand">{C["brand"]}</div>{labels}
<div id="qmark">?</div><div id="badge"><span></span></div><div id="zzz">Z z z</div><div id="kind">{C["kind"]}</div>
<div id="eptitle"><div>{ep["title"]}</div></div><div id="bye"><div>{C["bye"]}</div></div>
<div id="milobox">{C["host"] or fx.milo_talking(MILO)}</div>{fx.confetti_html(36)}{C["birds_html"] or fx.BIRDS_HTML}<div id="wipe"></div>
{cap_html}
</div>
<script>
window.__timelines = window.__timelines || {{}};
const tl = gsap.timeline({{paused:true}});
gsap.utils.toArray('[id$="-tongue"]').forEach(e=>gsap.set(e,{{scaleX:.15,svgOrigin:"745 281"}}));
{C["wing"](total, True)}
tl.to("#milo",{{y:-10,duration:.6,yoyo:true,repeat:{int(total/.6)//2*2-1},ease:"sine.inOut"}},0);
tl.to('[id$="-cloud1"]',{{x:-200,duration:{total},ease:"none"}},0);
tl.to('[id$="-bubbles"]',{{y:-120,duration:3,repeat:{int(total/3)},ease:"none"}},0);
{chr(10).join(js)}
{fx.ambient_js(total, "")}
{fx.talk_js(beats, C["talk"])}
{fx.birds_js(total, 1920)}
{extra}
tl.to({{}},{{duration:.01}},{total-.01});
window.__timelines["main"] = tl; tl.seek(0);
</script></body></html>"""
    open(os.path.join(proj, "index.html"), "w").write(html)
    json.dump({"total": total, "segments": [{k: s[k] for k in ("scene", "t0", "t1")} for s in segs]}, open(os.path.join(out, "timing.json"), "w"), indent=1)
    if norender: return proj, total
    sh(f'cd "{proj}" && hyperframes render -f 24 -q standard --crf 24 -o "{out}/silent.mp4"', timeout=7000)
    final = os.path.join(HERE, "out", f"{eid}.mp4")
    sh(f'ffmpeg -y -i "{out}/silent.mp4" -i "{out}/mix.wav" -map 0:v -map 1:a -c:v copy -af loudnorm=I=-16:TP=-1.5:LRA=11 -ar 48000 -c:a aac -b:a 160k -shortest "{final}"', timeout=1200)
    print(final, total)
    return final, total

if __name__ == "__main__":
    build(sys.argv[1], "--norender" in sys.argv)
