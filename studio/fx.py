"""Animation-quality layer shared by build.py (Shorts) and long.py (episodes).
Adds: outlines + ground shadows, blink, breathing/idle sway, Milo beak talk,
confetti bursts, flying birds, sparkles, camera moves."""
import math, re

NO_SHADOW = _NS2 = {"monkey", "owl", "sloth", "koala", "octopus", "turtle", "seaotter", "venus", "jupiter", "saturn", "moon", "mercury", "mars", "sun", "pteranodon", "bee", "butterfly", "ladybug", "ant", "snail", "firetruck", "excavator", "bulldozer", "dumptruck", "mixer", "crane", "ambulance", "policecar", "garbage", "schoolbus", "train", "tractor", "red", "blue", "yellow", "green", "orange", "purple", "pink", "brown", "gray", "black", "circle", "square", "triangle", "star", "heart", "rectangle", "oval", "diamond", "crescent", "hexagon", "n1", "n2", "n3", "n4", "n5", "apple", "banana", "orangefruit", "watermelon", "blueberry", "carrot", "broccoli", "peas", "corn", "pumpkin", "handwash", "toothbrush", "water", "sleep", "share", "plate", "mb_bunny", "mb_bear", "mb_kitten", "mb_duck", "mb_lamb", "mb_moon", "mb_stars", "mb_cloud", "mb_firefly", "mb_sunset", "mb_bath", "mb_pajamas", "mb_book", "mb_teddy", "mb_nightlight", "mb_whale", "mb_seahorse", "mb_fish", "mb_turtle", "mb_jelly", "mb_cow", "mb_pig", "mb_horse", "mb_hen", "mb_puppy", "gz_rain", "gz_rainbow", "gz_lightning", "gz_snow", "gz_wind", "gz_rocket", "gz_plane", "gz_balloon", "gz_heli", "gz_kite", "gz_magnet", "gz_bulb", "gz_ice", "gz_shadow", "gz_sound", "gz_seed", "gz_roots", "gz_leaf", "gz_flower", "gz_tree"}

OUTLINE = """<defs><filter id="ol" x="-10%" y="-10%" width="120%" height="120%">
<feMorphology in="SourceAlpha" operator="dilate" radius="4" result="d"/>
<feFlood flood-color="#2b2540" flood-opacity=".9"/><feComposite in2="d" operator="in" result="o"/>
<feMerge><feMergeNode in="o"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>"""

def _close_of(s, i):
    depth = 0
    for m in re.finditer(r'<g[\s>]|</g>', s[i:]):
        depth += 1 if m.group().startswith('<g') else -1
        if depth == 0:
            return i + m.start()
    return -1

def enhance(svg, key):
    """Wrap the #animal group's content in a .breathe group, add outline filter + shadow, tag eyes."""
    i = svg.find('<g id="animal"')
    if i < 0:
        return svg
    j = svg.index('>', i) + 1
    k = _close_of(svg, i)
    inner = svg[j:k]
    inner = re.sub(r'<circle([^>]*fill="#1a1a2e"[^>]*)/>', r'<circle class="pupil"\1/>', inner)
    inner = re.sub(r'<circle([^>]*r="[3-7]"[^>]*fill="#fff"[^>]*)/>', r'<circle class="glint"\1/>', inner)
    head = svg[i:j].replace('<g id="animal"', '<g id="animal" filter="url(#ol)"')
    shadow = '' if key in NO_SHADOW else '<ellipse cx="540" cy="1002" rx="250" ry="22" fill="#1b2a10" opacity=".18" filter="none"/>'
    out = svg[:i] + head + shadow + '<g class="breathe">' + inner + '</g>' + svg[k:]
    return out.replace('<svg ', '<svg ', 1).replace('>', '>' + OUTLINE, 1)

# Milo with a two-part beak (lower beak opens while he talks) and tagged eyes
def milo_talking(milo):
    milo = milo.replace('<polygon points="164,98 202,110 164,124" fill="#ff9f1c"/>',
                        '<polygon points="164,98 204,110 164,112" fill="#ff9f1c"/>'
                        '<polygon id="beaklow" points="164,111 198,112 164,124" fill="#f08a00"/>')
    milo = milo.replace('<circle cx="133" cy="90" r="9" fill="#1a1a2e"/>', '<circle class="mpupil" cx="133" cy="90" r="9" fill="#1a1a2e"/>')
    return milo

def rnd(n, seed):
    x = math.sin(n * 12.9898 + seed * 78.233) * 43758.5453
    return x - math.floor(x)

def ambient_js(total, scene_sel, origin="540 1000", seed=1):
    """Blink + breathe + sparkle twinkle + Milo blink for a whole film."""
    J = [f'tl.to("{scene_sel} .breathe",{{scaleY:1.022,scaleX:.992,svgOrigin:"{origin}",duration:1.4,yoyo:true,repeat:{int(total/1.4)//2*2+1},ease:"sine.inOut"}},0);',
         f'tl.to("{scene_sel} .breathe",{{rotation:1.2,svgOrigin:"{origin}",duration:2.3,yoyo:true,repeat:{int(total/2.3)//2*2+1},ease:"sine.inOut"}},0);']
    t, n = 1.2, 0
    while t < total - 1:
        J.append(f'tl.to("{scene_sel} .pupil, .mpupil",{{scaleY:.08,transformOrigin:"50% 50%",duration:.07,yoyo:true,repeat:1}},{t:.2f});'
                 f'tl.to("{scene_sel} .glint",{{opacity:0,duration:.05,yoyo:true,repeat:1}},{t:.2f});')
        n += 1; t += 2.2 + 2.2 * rnd(n, seed)
    return "\n".join(J)

def talk_js(beats, mode="rot"):
    """Milo's lower beak flaps while each line is spoken."""
    J = []
    for b in beats:
        reps = max(1, int(b["d"] / .13)) // 2 * 2 + 1
        if mode == "scale":
            J.append(f'tl.to("#beaklow",{{scaleY:4,svgOrigin:"110 117",duration:.12,yoyo:true,repeat:{reps},ease:"sine.inOut"}},{b["t"]:.2f});')
        else:
            J.append(f'tl.to("#beaklow",{{rotation:22,svgOrigin:"164 111",duration:.13,yoyo:true,repeat:{reps},ease:"sine.inOut"}},{b["t"]:.2f});')
    return "\n".join(J)

def confetti_html(n=28):
    cols = ["#ff5c8a", "#ffca28", "#4fc3f7", "#66bb6a", "#ab47bc", "#ff7043"]
    return '<div id="confetti">' + "".join(
        f'<i class="cf" style="background:{cols[i % len(cols)]};{"border-radius:50%;" if i % 3 == 0 else ""}"></i>' for i in range(n)) + '</div>'

CONFETTI_CSS = "#confetti{position:absolute;left:50%;top:34%;width:0;height:0;pointer-events:none}.cf{position:absolute;width:30px;height:18px;opacity:0;border-radius:3px}"

def confetti_js(t, n=28, spread=520, seed=0):
    J = []
    for i in range(n):
        a = rnd(i, seed + 7) * math.pi * 2; r = spread * (.45 + .55 * rnd(i, seed + 3))
        x, y = math.cos(a) * r, math.sin(a) * r * .7 - 120
        J.append(f'tl.fromTo("#confetti .cf:nth-child({i+1})",{{x:0,y:0,rotation:0,opacity:1,scale:1,immediateRender:false}},'
                 f'{{x:{x:.0f},y:{y+260:.0f},rotation:{int(360*rnd(i,seed+9))+180},opacity:0,scale:.6,duration:1.4,ease:"power2.out",immediateRender:false}},{t:.2f});')
    return "".join(J)

BIRDS_HTML = ('<svg id="birds" width="160" height="60" viewBox="0 0 160 60" style="position:absolute;left:-200px;top:120px">'
              '<path d="M10 30 q15 -18 30 0 q15 -18 30 0" stroke="#37474f" stroke-width="5" fill="none" stroke-linecap="round"/>'
              '<path d="M90 18 q12 -14 24 0 q12 -14 24 0" stroke="#37474f" stroke-width="4" fill="none" stroke-linecap="round"/></svg>')

def birds_js(total, width):
    J, t = [], 4.0
    while t < total - 8:
        J.append(f'tl.fromTo("#birds",{{x:0,y:0}},{{x:{width+400},y:-40,duration:9,ease:"none"}},{t:.1f});')
        t += 26
    return "".join(J)

SPARKLE_HTML = "".join(
    f'<svg class="spk" viewBox="0 0 40 40" width="46" height="46" style="position:absolute;left:{x}%;top:{y}%"><path d="M20 0 L24 16 L40 20 L24 24 L20 40 L16 24 L0 20 L16 16Z" fill="#fff59d"/></svg>'
    for x, y in ((14, 40), (82, 34), (70, 62), (24, 66)))

def sparkle_js(total):
    return (f'tl.fromTo(".spk",{{scale:.2,opacity:.2}},{{scale:1,opacity:.95,duration:.8,yoyo:true,repeat:{int(total/.8)//2*2+1},'
            f'stagger:{{each:.35}},ease:"sine.inOut"}},0);')

import glob as _g, importlib as _i, os as _o
for _p in _g.glob(_o.path.join(_o.path.dirname(_o.path.abspath(__file__)), "art_*2.py")):
    _mm = _i.import_module(_o.path.basename(_p)[:-3])
    for _a in dir(_mm):
        if _a.startswith("SCENES_") and _a.endswith("2"): NO_SHADOW.update(getattr(_mm, _a).keys())
