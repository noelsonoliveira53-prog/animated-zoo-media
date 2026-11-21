"""Art for za_ep05 "Who Took Mango's Breakfast?" (Nov 19 2026): Dot the baby tapir and her mama (a new kind, "tapir": side view, a short bendy snout;
the baby is reddish-brown with white stripes and spots, the grown-up is one dark colour), the sunny hollow at the bottom of the hill (dappled light,
a little pool, leafy bushes), Mango's breakfast on a leaf, a banana and its peel, sticky drips, a leafy bush in front that can rustle, and Mango
holding a magnifying glass (a new kind, "monkey_glass": the same drawing as art2.monkey(), the glass sits in her right hand and moves with the arm).
Same hand as art.py / art2.py: flat fills, one warm dark outline. Nothing here changes an existing character, prop or place.

Facts behind the drawing (read Nov 19 2026, see the episode file): Baird's tapir calves are "born with white stripes and spots" (LA Zoo), "watermelon"
spots and stripes that fade "into a solid dark brown adult coat" (Dublin Zoo); the snout is "flexible ... made of their upper lip and nose" (Dublin Zoo)."""
import art, art2, kit
from art import eye, INK, SUN
from art2 import _ol, _brow, _mouth

BABY = {"fill": "#8f5634", "shade": "#74432a", "light": "#b07650", "line": "#3d2415", "far": "#7a482c", "mark": "#f6ecd6", "rim": "#f6ecd6", "snout": "#8f5634"}
GROWN = {"fill": "#5b4d4a", "shade": "#4a3e3c", "light": "#7a6c68", "line": "#2a2220", "far": "#4c403e", "mark": None, "rim": "#efe6dc", "snout": "#5b4d4a"}


# ------------------------------------------------------------------ the tapir
def tapir(pid, baby=True):
    """A tapir, side view, facing right: a round barrel body on short stout legs, a rounded head with a short bendy snout (-trunk, so the engine's
    "trunk" fx can wiggle it), round ears with pale rims. baby=True: Dot (reddish-brown, white stripes along her body and white spots on legs and head).
    Parts: -neck (the whole head), -trunk, -ear, -jaw, -eye, -brow, -smile / -frown, -tail, -fl -bl -fl2 -bl2. Feet on y = 0."""
    c = BABY if baby else GROWN; ln = c["line"]

    def leg(x, far, name):
        col = c["far"] if far else c["fill"]; sh = f'<rect x="{x - 38}" y="-150" width="76" height="150" rx="30"/>'
        spots = "" if (far or not baby) else "".join(f'<circle cx="{x + dx}" cy="{dy}" r="{r}" fill="{c["mark"]}"/>' for dx, dy, r in ((-12, -112, 9), (12, -84, 8), (-8, -56, 7)))
        toes = "" if far else f'<path d="M{x - 22} -4 q8 -14 16 0 M{x + 4} -4 q8 -14 16 0" stroke="{c["shade"]}" stroke-width="6" fill="none" stroke-linecap="round"/>'
        return f'<g id="{pid}-{name}">{_ol(sh, ln)}<rect x="{x - 38}" y="-150" width="76" height="150" rx="30" fill="{col}"/>{spots}{toes}</g>'
    body_e = '<ellipse cx="-20" cy="-210" rx="232" ry="122"/>'
    body = _ol(body_e, ln) + f'<ellipse cx="-20" cy="-210" rx="232" ry="122" fill="{c["fill"]}"/>'
    shade = (f'<path d="M-252 -180 A232 122 0 0 0 210 -180 A280 170 0 0 1 -252 -180Z" fill="{c["shade"]}" opacity=".6"/>'
             f'<ellipse cx="-80" cy="-300" rx="110" ry="24" fill="{c["light"]}" opacity=".55"/>')
    marks = ""
    if baby:      # the "watermelon" coat: long white stripes along the body, broken into dashes, and rows of spots
        clip = f'<clipPath id="{pid}-bc">{body_e}</clipPath>'
        stripes = "".join(f'<path d="M{x0} {y} q60 -{b} 120 0" stroke="{c["mark"]}" stroke-width="15" fill="none" stroke-linecap="round"/>'
                          for x0, y, b in ((-210, -268, 8), (-60, -276, 8), (90, -266, 6), (-230, -222, 6), (-90, -228, 6), (50, -224, 6), (-200, -176, 4), (-60, -180, 4), (80, -178, 4)))
        spots = "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c["mark"]}"/>' for x, y, r in ((-250, -246, 9), (130, -150, 9), (-130, -138, 8), (10, -134, 9), (170, -240, 8)))
        marks = clip + f'<g clip-path="url(#{pid}-bc)">{stripes}{spots}</g>'
    tail = f'<g id="{pid}-tail"><ellipse cx="-252" cy="-236" rx="20" ry="26" fill="{c["fill"]}" stroke="{ln}" stroke-width="8"/></g>'
    # the head: a rounded block, the snout reaching forward and a little down
    head_sh = '<ellipse cx="226" cy="-262" rx="112" ry="96"/>'
    snout_d = "M286 -310 C350 -314 400 -292 414 -250 C424 -220 416 -192 392 -192 C370 -192 366 -212 348 -218 C328 -224 308 -220 292 -212Z"
    trunk = (f'<g id="{pid}-trunk">{_ol(f"<path d=\"{snout_d}\"/>", ln, 8)}<path d="{snout_d}" fill="{c["snout"]}"/>'
             f'<ellipse cx="400" cy="-204" rx="16" ry="12" fill="{c["shade"]}"/><ellipse cx="404" cy="-206" rx="6" ry="5" fill="{ln}"/>'
             f'<path d="M332 -304 q8 16 0 34 M362 -296 q8 16 0 32 M388 -280 q8 14 0 28" stroke="{c["shade"]}" stroke-width="6" fill="none" stroke-linecap="round"/></g>')
    ear_sh = '<ellipse cx="166" cy="-356" rx="34" ry="46" transform="rotate(-18 166 -356)"/>'
    ear = (f'<g id="{pid}-ear">{_ol(ear_sh, ln)}<ellipse cx="166" cy="-356" rx="34" ry="46" fill="{c["rim"]}" transform="rotate(-18 166 -356)"/>'
           f'<ellipse cx="168" cy="-352" rx="22" ry="32" fill="{c["fill"]}" transform="rotate(-18 168 -352)"/><ellipse cx="170" cy="-348" rx="12" ry="18" fill="#e9a8a0" transform="rotate(-18 170 -348)"/></g>')
    hspots = "" if not baby else "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c["mark"]}"/>' for x, y, r in ((170, -300, 9), (196, -214, 8), (150, -250, 7), (230, -336, 7)))
    neck = (f'<g id="{pid}-neck">{ear}' + _ol(head_sh, ln) + f'<ellipse cx="226" cy="-262" rx="112" ry="96" fill="{c["fill"]}"/>'
            f'<ellipse cx="236" cy="-330" rx="54" ry="18" fill="{c["light"]}" opacity=".5"/>{hspots}' +
            trunk + f'<g id="{pid}-jaw" opacity="0"><path d="M292 -190 q24 22 50 2 q-4 26 -24 26 q-20 0 -26 -28Z" fill="#c9667d" stroke="{ln}" stroke-width="6" stroke-linejoin="round"/></g>'
            f'<path d="M284 -194 q32 12 64 0 l0 -10 l-64 0Z" fill="{c["fill"]}"/>' + _mouth(pid, 314, -186, 40, ln, 6)
            + eye(f"{pid}-eye", 252, -284, 26 if baby else 22, lid=c["fill"]) + _brow(pid, 252, -324, 46, ln, 7)
            + f'<ellipse cx="282" cy="-236" rx="15" ry="9" fill="#ff8fb1" opacity=".55"/></g>')
    sh = '<ellipse cx="0" cy="4" rx="250" ry="18" fill="#000" opacity=".13"/>'
    return f'<g id="{pid}">{sh}{tail}<g>{leg(-180, True, "bl2")}{leg(100, True, "fl2")}</g>{body}{shade}{marks}{leg(-130, False, "bl")}{leg(150, False, "fl")}{neck}</g>'


_RIG = dict(neck="150 -240", tail="-245 -230", ear="166 -330", legs={"fl": 150, "bl": -130, "fl2": 100, "bl2": -180}, hip=-140, jaw=("y", 10), eyes=["eye"], brows=["brow"], trunk="296 -258")
art2.RIGS["tapir"] = dict(_RIG, build=lambda p: tapir(p, True))
art2.RIGS["tapir_mama"] = dict(_RIG, build=lambda p: tapir(p, False))
kit.PT["tapir"] = {"head": (236, -262), "eye": (252, -284), "body": (-20, -210), "top": (220, -410), "trunk": (380, -240), "tip": (410, -222), "mouth": (322, -204), "feet": (0, 0), "all": (70, -220)}
kit.PT["tapir_mama"] = kit.PT["tapir"]
kit.BOX["tapir"] = (-280, 430, -410); kit.BOX["tapir_mama"] = kit.BOX["tapir"]


# ------------------------------------------------------------------ Mango with a magnifying glass in her right hand
def glass(pid=""):
    """A magnifying glass, its handle end at (0, 0), the lens up and to the right."""
    return (f'<g{f" id={chr(34)}{pid}{chr(34)}" if pid else ""}><path d="M0 0 L46 -70" stroke="{INK}" stroke-width="30" stroke-linecap="round"/><path d="M0 0 L46 -70" stroke="#c0763a" stroke-width="16" stroke-linecap="round"/>'
            f'<circle cx="74" cy="-118" r="58" fill="#dff4ff" fill-opacity=".55" stroke="{INK}" stroke-width="22"/><circle cx="74" cy="-118" r="58" fill="none" stroke="#ffd23f" stroke-width="10"/>'
            f'<path d="M48 -142 q16 -18 38 -16" stroke="#fff" stroke-width="10" fill="none" stroke-linecap="round" opacity=".9"/></g>')


def monkey_glass(pid):
    s = art2.monkey(pid)
    hand = f'<circle cx="118" cy="-62" r="22" fill="{art2.MON["dark"]}" stroke="{art2.MON["line"]}" stroke-width="7"/>'
    i = s.index(f'<g id="{pid}-ar">'); j = s.index(hand, i)
    # the glass in her hand, drawn under the fingers (the hand circle comes after it)
    return s[:j] + f'<g transform="translate(120 -60) rotate(-20)">{glass()}</g>' + s[j:]


art2.RIGS["monkey_glass"] = dict(art2.RIGS["monkey"], build=monkey_glass)
kit.PT["monkey_glass"] = kit.PT["monkey"]
kit.BOX["monkey_glass"] = (-170, 260, -430)


# ------------------------------------------------------------------ the hollow at the bottom of the hill
def bg_hollow(p):
    """The sunny hollow at the bottom of the hill: big leaves, soft patches of sunlight on the ground (dappled light, where stripes and spots blend in),
    a little pool at the back right, leafy bushes. Feet on y = 900-940."""
    far = art._sky(p, "#cdf3d6", "#f2fbdc", y1=1100) + "".join(art2._jtree(x, w, "#76a07a", 1700) for x, w in ((140, 70), (600, 54), (1180, 76), (1700, 60))) + \
        "".join(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="#94cf94"/>' for x, y, rx, ry in ((260, 110, 360, 170), (960, 50, 400, 180), (1700, 120, 380, 170)))
    rays = "".join(f'<path d="M{x} -200 L{x + 120} -200 L{x + 360} 900 L{x + 160} 900Z" fill="#fffbd0" opacity=".22"/>' for x in (300, 900, 1400))
    mid = (rays + "".join(art2._jtree(x, w) for x, w in ((380, 100), (1620, 110))) + "".join(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{c}"/>' for x, y, rx, ry, c in
           ((380, 150, 300, 150, "#3f9e5c"), (1620, 110, 340, 170, "#3f9e5c"), (980, 30, 360, 120, "#4fb56c")))
           + '<path d="M-500 760 C200 720 800 750 1300 730 S2100 730 2420 760 L2420 900 L-500 900Z" fill="#62bd6c"/>'
           # leafy bushes at the back
           + "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>' for x, y, r, c in ((60, 760, 120, "#3c9550"), (180, 730, 110, "#47a85a"), (300, 770, 100, "#3c9550"),
                                                                                         (1880, 740, 130, "#3c9550"), (2000, 770, 110, "#47a85a"))))
    pool = ('<ellipse cx="1560" cy="930" rx="300" ry="54" fill="#58b9e8"/><ellipse cx="1560" cy="920" rx="300" ry="40" fill="#7fcbf0"/>'
            '<path d="M1380 922 q30 -10 60 0 M1600 914 q30 -10 60 0" stroke="#d6f0fb" stroke-width="7" fill="none" stroke-linecap="round"/>')
    light = "".join(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="#b8ec86" opacity=".75"/>' for x, y, rx, ry in
                    ((200, 990, 90, 22), (520, 1060, 120, 26), (860, 980, 70, 18), (1100, 1080, 110, 24), (720, 1170, 90, 20), (1320, 1010, 60, 16), (1760, 1080, 100, 24), (380, 1200, 80, 18)))
    near = ('<rect x="-500" y="850" width="2920" height="1200" fill="#4aa85a"/><path d="M-500 870 C300 836 900 860 1400 846 S2100 850 2420 862 L2420 900 L-500 900Z" fill="#4aa85a"/>'
            + pool + light + art2._leaf(-40, 900, 1.5, -40, "#2f8a4c") + art2._leaf(1980, 930, 1.5, -130, "#2f8a4c")
            + "".join(f'<circle cx="{x}" cy="{y}" r="12" fill="{c}"/><circle cx="{x}" cy="{y}" r="5" fill="#fff6c0"/>' for x, y, c in ((420, 1000, "#ff7aa2"), (1240, 1040, "#ffb347"), (960, 1120, "#fff"))))
    return far, mid, near


art.BG.update({"hollow": bg_hollow})
art.PLACE.update({"hollow": "the sunny hollow at the bottom of the hill"})


# ------------------------------------------------------------------ props
def bush(pid, w=1.0):
    """A big leafy bush (drawn over the actors: whoever stands behind it is hidden). (0, 0) is the middle of its bottom. -leaves rustle."""
    blobs = [(-220, -120, 130), (-90, -210, 150), (60, -230, 150), (200, -150, 130), (-160, -50, 110), (0, -90, 140), (170, -50, 110)]
    sh = "".join(f'<circle cx="{x * w:.0f}" cy="{y}" r="{r}"/>' for x, y, r in blobs)
    leaves = "".join(f'<path d="M{x * w:.0f} {y} q22 -26 46 0 q-22 18 -46 0Z" fill="#6fd08a" opacity=".9"/>' for x, y in ((-150, -200), (40, -280), (180, -170), (-60, -120), (100, -90), (-230, -110)))
    return (f'<g id="{pid}"><g id="{pid}-leaves">{_ol(sh, "#1f6a36", 8)}<g fill="#3fa65a">{sh}</g>'
            + "".join(f'<circle cx="{x * w - r * .2:.0f}" cy="{y - r * .25:.0f}" r="{r * .55:.0f}" fill="#57c078" opacity=".8"/>' for x, y, r in blobs) + leaves + '</g></g>')


def bush_peek(pid):
    """Stripes and spots seen through a gap in the leaves (sits on the bush, shown when we look closely)."""
    return (f'<g id="{pid}"><ellipse cx="0" cy="0" rx="78" ry="54" fill="{BABY["fill"]}" stroke="{BABY["line"]}" stroke-width="7"/>'
            f'<path d="M-56 -16 q40 -8 80 0 M-50 14 q40 -8 90 0" stroke="{BABY["mark"]}" stroke-width="12" fill="none" stroke-linecap="round"/>'
            f'<circle cx="40" cy="-30" r="8" fill="{BABY["mark"]}"/><circle cx="-30" cy="34" r="7" fill="{BABY["mark"]}"/></g>')


def banana(pid):
    """A yellow banana. (0, 0) is its middle."""
    return (f'<g id="{pid}"><path d="M-120 -40 C-80 40 60 60 130 -30 C80 10 -40 20 -120 -40Z" fill="#ffd94a" stroke="#a87a10" stroke-width="9" stroke-linejoin="round"/>'
            f'<path d="M-120 -40 l-14 -16" stroke="#6a4a26" stroke-width="12" stroke-linecap="round"/><path d="M130 -30 l8 -8" stroke="#6a4a26" stroke-width="10" stroke-linecap="round"/>'
            f'<path d="M-80 -6 C-30 26 40 26 90 -6" stroke="#f0b820" stroke-width="7" fill="none" stroke-linecap="round"/></g>')


def peel(pid):
    """An empty banana peel lying on the ground: three yellow flaps. (0, 0) is where it touches the ground."""
    flap = lambda d: f'<path d="{d}" fill="#ffd94a" stroke="#a87a10" stroke-width="9" stroke-linejoin="round"/>'
    return (f'<g id="{pid}">' + flap("M-10 -40 C-80 -40 -130 -10 -150 0 C-100 6 -40 0 -6 -18Z") + flap("M10 -40 C80 -44 136 -12 152 0 C100 8 40 2 6 -18Z")
            + flap("M-6 -50 C-20 -100 0 -150 30 -170 C34 -120 24 -70 10 -40Z") + f'<ellipse cx="0" cy="-26" rx="34" ry="26" fill="#fff3c0" stroke="#a87a10" stroke-width="8"/>'
            + '<path d="M28 -170 l12 -14" stroke="#6a4a26" stroke-width="10" stroke-linecap="round"/></g>')


def drip(pid, s=1.0):
    """One sticky drop of golden fruit juice on the ground."""
    return (f'<g id="{pid}"><ellipse cx="0" cy="0" rx="{34 * s:.0f}" ry="{13 * s:.0f}" fill="#ffb81f" stroke="#a8640a" stroke-width="6"/>'
            f'<ellipse cx="{-10 * s:.0f}" cy="{-3 * s:.0f}" rx="{10 * s:.0f}" ry="{4 * s:.0f}" fill="#fff3c0"/></g>')


def drips(pid, pts):
    """A trail of drops: pts = [(x, y, s), ...] relative to the prop; each drop is -d0, -d1 ... so they can pop in one by one."""
    return f'<g id="{pid}">' + "".join(f'<g transform="translate({x} {y})">{drip(f"{pid}-d{k}", s)}</g>' for k, (x, y, s) in enumerate(pts)) + '</g>'


def breakfast(pid, n=3, nb=1):
    """Mango's breakfast on a big leaf: n golden fruits and nb bananas. (0, 0) is the middle of the leaf, on the branch."""
    leaf = (f'<path d="M-200 0 C-150 -40 150 -40 210 0 C150 30 -150 30 -200 0Z" fill="#57c078" stroke="#2f8a4c" stroke-width="8" stroke-linejoin="round"/>'
            f'<path d="M-190 0 L200 0" stroke="#2f8a4c" stroke-width="6"/>')
    fr = "".join(f'<g transform="translate({x} -6) scale(.62)">{art2.fruit(f"{pid}-f{k}")}</g>' for k, x in enumerate((-100, 0, 100)[:n]))
    bn = "".join(f'<g transform="translate({20 + 40 * k} -70) rotate(-8) scale(.55)">{banana(f"{pid}-b{k}")}</g>' for k in range(nb))
    return f'<g id="{pid}">{leaf}{fr}{bn}</g>'


def empty_leaf(pid): return breakfast(pid, 0, 0)


def note(pid, col="#ff7aa2"):
    """A music note (shows a tune that is playing: the hum is played by the instruments)."""
    return (f'<g id="{pid}"><path d="M20 -110 L20 0" stroke="{INK}" stroke-width="12" stroke-linecap="round"/><path d="M20 -110 q50 10 60 50" stroke="{INK}" stroke-width="12" fill="none" stroke-linecap="round"/>'
            f'<ellipse cx="0" cy="0" rx="30" ry="22" fill="{col}" stroke="{INK}" stroke-width="8" transform="rotate(-20)"/></g>')


def coat_board(pid):
    """Two tapirs side by side for the fact board: the striped baby and her plain mama (drawn by the engine as actors; this is only the ground line)."""
    return f'<g id="{pid}"><path d="M-700 0 H700" stroke="#c8b48a" stroke-width="10" stroke-linecap="round" opacity=".6"/></g>'
