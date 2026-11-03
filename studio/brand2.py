"""Banner (2560x1440), avatar (800x800) and episode thumbnail (1280x720) for Space, Dino and Wild channels."""
import re, os
from art_space import SCENES3
from art_dino import SCENES4
from art_wild import SCENES5
from channel import NOVA, DASH, PIP

S = {**SCENES3, **SCENES4, **SCENES5}
font = "@font-face{font-family:Baloo;src:url(/root/zoo/vendor/f/package/files/baloo-2-latin-800-normal.woff2)}"

def animal(key):
    s = S[key]; i = s.index('<g id="animal"'); depth = 0; j = i
    for m in re.finditer(r'<g[\s>]|</g>', s[i:]):
        depth += 1 if m.group().startswith('<g') else -1
        if depth == 0: j = i + m.end(); break
    defs = "".join(re.findall(r'<defs>.*?</defs>', s, re.S))
    return defs + s[i:j]

def pet(key, x, y, h):
    w = h * 1080 / 1100
    return f'<svg viewBox="0 0 1080 1100" width="{w:.0f}" height="{h}" style="position:absolute;left:{x}px;top:{y}px">{animal(key)}</svg>'

def stars(w, h, n=160):
    import math
    r = lambda i, s: (math.sin(i * 12.9898 + s * 78.233) * 43758.5453) % 1
    return f'<svg width="{w}" height="{h}" style="position:absolute;left:0;top:0">' + "".join(
        f'<circle cx="{w*r(i,1):.0f}" cy="{h*r(i,2):.0f}" r="{1.5+3*r(i,3):.1f}" fill="#fff" opacity="{.3+.7*r(i,4):.2f}"/>' for i in range(n)) + '</svg>'

def hills(c1, c2, w=2560, h=1440, y=1020):
    return (f'<svg width="{w}" height="{h}" style="position:absolute;left:0;top:0"><path d="M0 {y} Q{w*.16} {y-120} {w*.31} {y-20} T{w*.62} {y-30} T{w} {y-60} L{w} {h} L0 {h}Z" fill="{c1}"/>'
            f'<path d="M0 {y+100} Q{w*.2} {y+20} {w*.39} {y+90} T{w*.78} {y+80} T{w} {y+60} L{w} {h} L0 {h}Z" fill="{c2}"/></svg>')

CH = {
 "space": dict(name="SPACE KIDS ACADEMY", tag="Fun space facts with Nova! 🚀🪐⭐", host=NOVA, stroke="#4b2fb5", tagc="#4b2fb5",
               bg="radial-gradient(ellipse at 50% 45%,#2d3a9a 0%,#141a4f 50%,#090d2b 100%)", extra=stars(2560, 1440),
               pets=[("saturn", -60, 380, 700), ("mars", 220, 760, 420), ("jupiter", 1960, 420, 640), ("moon", 2230, 860, 330)],
               av="radial-gradient(circle at 50% 40%,#4a5bd1 0,#28328a 55%,#141a4f 100%)",
               ep="sp_ep01_planets", t1="5 PLANET", t2="SURPRISES!", tpets=["mercury", "venus", "mars", "jupiter", "saturn"], tbg="#28328a", ground=None),
 "dino": dict(name="DINO WORLD KIDS", tag="Fun dinosaur facts with Dash! 🦕🦖", host=DASH, stroke="#8d4a1a", tagc="#8d4a1a",
              bg="linear-gradient(#ffc48a,#fff1d6)", extra=hills("#9ccc65", "#7cb342"),
              pets=[("brachiosaurus", -80, 240, 860), ("triceratops", 260, 700, 440), ("trex", 1900, 440, 640), ("stegosaurus", 2200, 760, 380)],
              av="radial-gradient(circle at 50% 40%,#ffe0b2 0,#ffb74d 55%,#f57c00 100%)",
              ep="dn_ep01_dinos", t1="5 DINO", t2="SURPRISES!", tpets=["trex", "triceratops", "stegosaurus", "brachiosaurus", "pteranodon"], tbg="#ffcc9a", ground="#7cb342"),
 "wild": dict(name="WILDKIDS DISCOVERY", tag="Fun bug facts with Pip! 🐞🐝🦋", host=PIP, stroke="#2e7d32", tagc="#2e7d32",
              bg="linear-gradient(#8fdcff,#e8f9ff)", extra=hills("#7cb342", "#558b2f"),
              pets=[("butterfly", -20, 300, 560), ("ladybug", 200, 700, 440), ("bee", 1980, 380, 560), ("snail", 2180, 780, 400)],
              av="radial-gradient(circle at 50% 40%,#dcedc8 0,#9ccc65 55%,#558b2f 100%)",
              ep="wk_ep01_bugs", t1="5 BACKYARD", t2="BUG FRIENDS!", tpets=["ladybug", "bee", "butterfly", "ant", "snail"], tbg="#9fe3ff", ground="#558b2f"),
}

def build(k):
    c = CH[k]; os.makedirs(f"brand/{k}", exist_ok=True)
    pets = "".join(pet(*p) for p in c["pets"])
    banner = f"""<html><head><style>{font}*{{margin:0}}body{{width:2560px;height:1440px;position:relative;overflow:hidden;background:{c["bg"]};font-family:Baloo}}
#t{{position:absolute;left:760px;width:1330px;top:585px;text-align:center;font-size:132px;line-height:1;color:#fff;-webkit-text-stroke:18px {c["stroke"]};paint-order:stroke fill;text-shadow:0 12px 0 rgba(0,0,0,.15)}}
#s{{position:absolute;left:760px;width:1330px;top:770px;text-align:center;font-size:56px;color:{c["tagc"]}}}
#s span{{background:#fff;border-radius:50px;padding:10px 46px 0;box-shadow:0 8px 0 rgba(0,0,0,.1)}}
#m{{position:absolute;left:480px;top:520px;transform:scale(1.3);transform-origin:0 0}}
</style></head><body>{c["extra"]}{pets}<div id="t">{c["name"]}</div><div id="s"><span>{c["tag"]}</span></div><div id="m">{c["host"]}</div></body></html>"""
    open(f"brand/{k}/banner.html", "w").write(banner)
    avatar = f"""<html><head><style>*{{margin:0}}body{{width:800px;height:800px;background:{c["av"]};display:flex;align-items:center;justify-content:center}}svg{{transform:scale(2.4) translate(0,8px)}}</style></head><body>{c["host"]}</body></html>"""
    open(f"brand/{k}/avatar.html", "w").write(avatar)
    pos = [(-60, 250, 470), (150, 330, 400), (340, 300, 430), (560, 330, 400), (770, 300, 430)]
    tp = "".join(pet(x, px, py, h) for x, (px, py, h) in zip(c["tpets"], pos))
    g = f'<div id="g" style="background:{c["ground"]}"></div>' if c["ground"] else stars(1280, 720, 70)
    thumb = f"""<html><head><style>{font}*{{margin:0}}body{{width:1280px;height:720px;overflow:hidden;position:relative;font-family:Baloo;
background:radial-gradient(circle at 70% 30%,#fff7d6 0,{c["tbg"]} 62%)}}
.t{{position:absolute;left:40px;font-size:112px;line-height:1;color:#fff;-webkit-text-stroke:14px {c["stroke"]};paint-order:stroke fill;text-shadow:0 8px 0 rgba(0,0,0,.18)}}
#m{{position:absolute;left:900px;top:220px;transform:scale(1.05);transform-origin:0 0}}
#g{{position:absolute;left:0;right:0;bottom:0;height:120px}}</style></head>
<body>{g}{tp}<div class="t" style="top:28px">{c["t1"]}</div><div class="t" style="top:140px;color:#ffe066">{c["t2"]}</div><div id="m">{c["host"]}</div></body></html>"""
    open(f"brand/{k}/thumb_{c['ep']}.html", "w").write(thumb)

for k in CH: build(k)
