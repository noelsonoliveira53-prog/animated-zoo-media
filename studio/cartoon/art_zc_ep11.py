"""Art for zc_ep11 "Whose Feet Are These? Guess With Milo" (Nov 20 2026): a giraffe and a zebra (new rigs, registered here the way
art_zc_ep07.py registers its elephants), three footprints in the sand (elephant: big and round with nail marks; giraffe: two halves side by side;
zebra: one smooth hoof), close-ups of each foot for the fact boards (the elephant's foot from the front with five toenails, the elephant's foot cut
open: toe bones standing on tiptoe over a soft cushion; the giraffe's foot with its two hooves; the zebra's foot cut open: one toe inside one hoof),
a dinner plate, a hand with one finger up, a second zebra with other stripes, and the place `sandtrail` (the savanna with a wide sandy path).
Same hand as art.py / art2.py: flat fills, one warm dark outline round every moving part. Nothing here changes an existing character, prop or place."""
import random
import art, art2, kit
from art import eye, INK

GIR = {"fill": "#f6c04e", "spot": "#b8692a", "spot_l": "#cf8240", "shade": "#dda43a", "light": "#ffe08a", "line": "#7a4318", "far": "#e2ab40", "hoof": "#5a3418", "mane": "#9a5422", "horn": "#8a4a1e"}
ZEB = {"fill": "#fbfaf6", "stripe": "#26232e", "shade": "#dedbd2", "light": "#ffffff", "line": "#26232e", "far": "#e6e3da", "hoof": "#3a3440", "muzzle": "#4a4452", "mane": "#26232e"}


def _ol(shapes, ln, w=9): return f'<g fill="{ln}" stroke="{ln}" stroke-width="{w * 2}" stroke-linejoin="round" stroke-linecap="round">{shapes}</g>'


# ================================================================== giraffe
def giraffe(pid, c=GIR):
    """A giraffe, side view facing right, feet at y = 0 (about 1120 tall). Parts: -neck (neck and head: nods, looks), -jaw, -eye, -brow, -smile / -frown,
    -ear, -tail, -fl -bl (near legs) -fl2 -bl2 (far legs). Every foot ends in TWO hooves with a split between them (Live Science: "two weight-bearing hooves on each foot")."""
    ln = c["line"]; top = -470

    def leg(x, far, name):
        col = c["far"] if far else c["fill"]; h = -top - 46
        sh = f'<path d="M{x - 26} {top} L{x - 18} {top + h} L{x + 18} {top + h} L{x + 26} {top}Z"/><ellipse cx="{x}" cy="{top + h * .55:.0f}" rx="22" ry="20"/>'
        hooves = (f'<path d="M{x - 26} {top + h - 4} L{x - 30} -2 Q{x - 15} 6 {x - 2} -2 L{x - 2} {top + h - 4}Z" fill="{c["hoof"]}"/>'
                  f'<path d="M{x + 2} {top + h - 4} L{x + 2} -2 Q{x + 15} 6 {x + 30} -2 L{x + 26} {top + h - 4}Z" fill="{c["hoof"]}"/>')
        hsh = f'<path d="M{x - 26} {top + h - 4} L{x - 30} -2 Q{x} 8 {x + 30} -2 L{x + 26} {top + h - 4}Z"/>'
        spots = "" if far else (f'<ellipse cx="{x - 4}" cy="{top + 70}" rx="14" ry="20" fill="{c["spot_l"]}"/>')
        return (f'<g id="{pid}-{name}">{_ol(sh + hsh, ln, 8)}<path d="M{x - 26} {top} L{x - 18} {top + h} L{x + 18} {top + h} L{x + 26} {top}Z" fill="{col}"/>'
                f'<ellipse cx="{x}" cy="{top + h * .55:.0f}" rx="22" ry="20" fill="{col}"/>{spots}{hooves}</g>')
    far_legs = leg(-176, True, "bl2") + leg(92, True, "fl2"); near_legs = leg(-128, False, "bl") + leg(134, False, "fl")
    body_sh = '<path d="M-210 -520 C-200 -620 40 -660 190 -600 C250 -570 250 -470 190 -430 C80 -390 -160 -390 -210 -450Z"/>'
    body = _ol(body_sh, ln) + f'<g fill="{c["fill"]}">{body_sh}</g>'
    r = random.Random(5)
    bspots = "".join(f'<path d="M{x} {y} l{r.randint(28, 40)} {-r.randint(6, 14)} l{r.randint(8, 16)} {r.randint(24, 34)} l{-r.randint(30, 40)} {r.randint(8, 14)}Z" fill="{c["spot"]}" stroke="{c["spot"]}" stroke-width="10" stroke-linejoin="round"/>'
                     for x, y in ((-170, -540), (-110, -580), (-40, -600), (40, -604), (110, -590), (-140, -480), (-70, -520), (10, -540), (80, -530), (150, -520), (-30, -460), (50, -470), (120, -460)))
    shade = f'<path d="M-205 -460 C-150 -410 80 -400 190 -436 C150 -400 -120 -390 -205 -460Z" fill="{c["shade"]}" opacity=".7"/>'
    tail = (f'<g id="{pid}-tail"><path d="M-205 -510 q-34 70 -26 190" stroke="{ln}" stroke-width="22" fill="none" stroke-linecap="round"/>'
            f'<path d="M-205 -510 q-34 70 -26 190" stroke="{c["fill"]}" stroke-width="10" fill="none" stroke-linecap="round"/>'
            f'<path d="M-231 -330 q-18 34 0 60 q18 -26 0 -60Z" fill="{c["mane"]}" stroke="{ln}" stroke-width="6"/></g>')
    neck_d = "M150 -540 C200 -700 250 -860 300 -990"
    head_sh = (f'<path d="{neck_d}" fill="none" stroke-width="{110 + 18}" stroke-linecap="round"/>'
               '<ellipse cx="350" cy="-1010" rx="86" ry="56" transform="rotate(18 350 -1010)"/><ellipse cx="420" cy="-970" rx="54" ry="44"/>'
               '<path d="M300 -1056 l-6 -54 l26 -2 l2 52Z"/><path d="M340 -1060 l4 -56 l26 4 l-8 54Z"/>'
               '<path d="M282 -1030 q-56 -26 -70 -6 q30 24 72 22Z"/>')
    nspots = "".join(f'<path d="M{x} {y} l26 -8 l8 24 l-28 8Z" fill="{c["spot"]}" stroke="{c["spot"]}" stroke-width="8" stroke-linejoin="round"/>'
                     for x, y in ((150, -620), (196, -700), (168, -760), (220, -800), (240, -880), (204, -660), (262, -920), (186, -560)))
    mane = "".join(f'<path d="M{x} {y} l-26 -14 l14 -22Z" fill="{c["mane"]}"/>' for x, y in ((150, -580), (164, -640), (182, -700), (198, -760), (216, -820), (234, -880), (252, -940)))
    neck = (f'<g id="{pid}-neck">' + _ol(head_sh, ln) + mane +
            f'<path d="{neck_d}" fill="none" stroke="{c["fill"]}" stroke-width="110" stroke-linecap="round"/>{nspots}'
            f'<path d="M206 -560 C250 -700 296 -840 334 -960" fill="none" stroke="{c["light"]}" stroke-width="22" stroke-linecap="round" opacity=".6"/>'
            f'<g id="{pid}-ear"><path d="M282 -1030 q-56 -26 -70 -6 q30 24 72 22Z" fill="{c["fill"]}"/><path d="M270 -1026 q-30 -12 -42 -4 q18 12 42 12Z" fill="#f4a9b8"/></g>'
            f'<path d="M300 -1056 l-6 -54 l26 -2 l2 52Z" fill="{c["fill"]}"/><circle cx="306" cy="-1112" r="16" fill="{c["horn"]}"/>'
            f'<path d="M340 -1060 l4 -56 l26 4 l-8 54Z" fill="{c["fill"]}"/><circle cx="358" cy="-1114" r="16" fill="{c["horn"]}"/>'
            f'<ellipse cx="350" cy="-1010" rx="86" ry="56" fill="{c["fill"]}" transform="rotate(18 350 -1010)"/>'
            f'<g id="{pid}-jaw" opacity="0"><path d="M410 -946 q30 18 56 0 q-4 26 -28 28 q-22 0 -28 -28Z" fill="#c9667d" stroke="{ln}" stroke-width="6" stroke-linejoin="round"/></g>'
            f'<ellipse cx="420" cy="-970" rx="54" ry="44" fill="{c["light"]}"/><ellipse cx="452" cy="-986" rx="9" ry="6" fill="{ln}" transform="rotate(-20 452 -986)"/>'
            + art2._mouth(pid, 430, -948, 44, ln, 6) + eye(f"{pid}-eye", 352, -1026, 25, lashes=1, lid=c["fill"]) + art2._brow(pid, 352, -1064, 44, ln, 7)
            + f'<ellipse cx="392" cy="-990" rx="13" ry="8" fill="#ff8fb1" opacity=".55"/></g>')
    npatch = f'<circle cx="160" cy="-540" r="58" fill="{c["fill"]}"/><path d="M130 -560 l26 -8 l8 24 l-28 8Z" fill="{c["spot"]}"/>'
    sh = '<ellipse cx="0" cy="4" rx="250" ry="18" fill="#000" opacity=".13"/>'
    return f'<g id="{pid}">{sh}<g id="{pid}-all">{tail}<g>{far_legs}</g>{neck}{body}{bspots}{shade}{near_legs}</g></g>'


# ================================================================== zebra
def zebra(pid, c=ZEB, seed=3):
    """A plains zebra, side view facing right, feet at y = 0 (about 640 tall). Parts: -neck, -jaw, -eye, -brow, -smile / -frown, -ear, -tail,
    -fl -bl -fl2 -bl2. Each leg ends in ONE smooth hoof (SDZWA: "Single toe at terminus of each limb"). seed: another stripe pattern (every zebra's own)."""
    ln = c["line"]; top = -350; r = random.Random(seed)

    def leg(x, far, name):
        col = c["far"] if far else c["fill"]; h = -top - 40
        sh = f'<rect x="{x - 24}" y="{top}" width="48" height="{h}" rx="20"/><path d="M{x - 24} {top + h - 6} L{x - 28} -2 Q{x} 8 {x + 28} -2 L{x + 24} {top + h - 6}Z"/>'
        stripes = "".join(f'<path d="M{x - 24} {top + yy} q24 {8 + r.randint(-3, 3)} 48 0 l0 13 q-24 {8 + r.randint(-3, 3)} -48 0Z" fill="{c["stripe"]}" opacity="{.75 if far else 1}"/>'
                          for yy in range(60, h - 30, 38))
        return (f'<g id="{pid}-{name}">{_ol(sh, ln, 7)}<rect x="{x - 24}" y="{top}" width="48" height="{h}" rx="20" fill="{col}"/>{stripes}'
                f'<path d="M{x - 24} {top + h - 6} L{x - 28} -2 Q{x} 8 {x + 28} -2 L{x + 24} {top + h - 6}Z" fill="{c["hoof"]}"/>'
                f'<path d="M{x - 16} {top + h + 4} q16 6 32 0" stroke="#6a6474" stroke-width="5" fill="none" stroke-linecap="round"/></g>')
    far_legs = leg(-170, True, "bl2") + leg(100, True, "fl2"); near_legs = leg(-126, False, "bl") + leg(142, False, "fl")
    body_sh = '<ellipse cx="0" cy="-360" rx="214" ry="108"/>'
    clip = f'<clipPath id="{pid}-bc"><ellipse cx="0" cy="-360" rx="214" ry="108"/></clipPath>'
    bstr = "".join(f'<path d="M{x} -472 q{r.randint(-22, 22)} 50 {r.randint(-10, 10)} 100 q{r.randint(-18, 18)} 40 {r.randint(-8, 8)} {r.randint(70, 110)}" stroke="{c["stripe"]}" stroke-width="{r.randint(16, 22)}" fill="none" stroke-linecap="round"/>'
                   for x in range(-150, 200, 44))
    rump = "".join(f'<path d="M-214 {y} q60 {r.randint(-16, -6)} 110 {r.randint(4, 14)} l-6 14 q-50 -12 -104 0Z" fill="{c["stripe"]}"/>' for y in (-420, -388, -356, -324))
    body = _ol(body_sh, ln) + clip + f'<g clip-path="url(#{pid}-bc)"><ellipse cx="0" cy="-360" rx="214" ry="108" fill="{c["fill"]}"/>{bstr}{rump}' \
        f'<path d="M-214 -320 A214 108 0 0 0 214 -320 L214 -252 L-214 -252Z" fill="{c["shade"]}" opacity=".35"/></g>'
    tail = (f'<g id="{pid}-tail"><path d="M-208 -390 q-30 50 -22 150" stroke="{ln}" stroke-width="22" fill="none" stroke-linecap="round"/>'
            f'<path d="M-208 -390 q-30 50 -22 150" stroke="{c["fill"]}" stroke-width="10" fill="none" stroke-linecap="round"/>'
            f'<path d="M-230 -250 q-20 40 0 70 q20 -30 0 -70Z" fill="{c["stripe"]}"/></g>')
    neck_d = "M160 -400 C210 -460 250 -520 280 -580"
    head_sh = (f'<path d="{neck_d}" fill="none" stroke-width="{120 + 16}" stroke-linecap="round"/>'
               '<path d="M250 -640 C300 -660 360 -600 420 -540 C450 -510 440 -470 400 -470 C350 -472 290 -520 250 -560Z"/>'
               '<path d="M262 -630 l-12 -64 l34 22Z"/>')
    nclip = f'<clipPath id="{pid}-nc"><path d="{neck_d}" fill="none" stroke="#000" stroke-width="120" stroke-linecap="round"/><path d="M250 -640 C300 -660 360 -600 420 -540 C450 -510 440 -470 400 -470 C350 -472 290 -520 250 -560Z"/></clipPath>'
    nstr = "".join(f'<path d="M{160 + t * 120 - 50 * .83:.0f} {-400 - t * 180 - 50 * .55:.0f} L{160 + t * 120 + 50 * .83:.0f} {-400 - t * 180 + 50 * .55:.0f}" stroke="{c["stripe"]}" stroke-width="18" stroke-linecap="round"/>'
                   for t in (.05, .3, .55, .8, 1.02))
    hstr = "".join(f'<path d="M{276 + k * 24} -646 q-8 20 -2 44" stroke="{c["stripe"]}" stroke-width="10" fill="none" stroke-linecap="round"/>' for k in range(2))
    mane = "".join(f'<path d="M{x} {y} l-20 -30 l30 -6Z" fill="{c["mane"]}"/><path d="M{x - 4} {y - 4} l-8 -14 l14 -2Z" fill="#fff"/>' for x, y in ((150, -440), (176, -480), (200, -520), (224, -560), (248, -600), (270, -640)))
    neck = (f'<g id="{pid}-neck">' + _ol(head_sh, ln) + nclip +
            f'<g><path d="{neck_d}" fill="none" stroke="{c["fill"]}" stroke-width="120" stroke-linecap="round"/>'
            f'<path d="M250 -640 C300 -660 360 -600 420 -540 C450 -510 440 -470 400 -470 C350 -472 290 -520 250 -560Z" fill="{c["fill"]}"/>{nstr}{hstr}</g>' + mane +
            f'<path d="M386 -566 C420 -540 444 -510 432 -486 C420 -466 380 -470 352 -490Z" fill="{c["muzzle"]}"/>'
            f'<ellipse cx="420" cy="-520" rx="8" ry="5" fill="#16141c" transform="rotate(40 420 -520)"/>'
            f'<g id="{pid}-ear"><path d="M262 -630 l-12 -64 l34 22Z" fill="{c["fill"]}"/><path d="M264 -640 l-6 -36 l16 12Z" fill="#f4a9b8"/></g>'
            f'<g id="{pid}-jaw" opacity="0"><path d="M380 -476 q24 14 46 0 q-4 22 -24 24 q-18 0 -22 -24Z" fill="#c9667d" stroke="{ln}" stroke-width="6" stroke-linejoin="round"/></g>'
            + art2._mouth(pid, 396, -478, 36, "#fff", 5) + f'<circle cx="330" cy="-586" r="34" fill="#fff"/>' + eye(f"{pid}-eye", 330, -586, 24, lashes=1, lid=c["fill"])
            + art2._brow(pid, 330, -622, 40, ln, 6) + f'<ellipse cx="350" cy="-548" rx="12" ry="7" fill="#ff8fb1" opacity=".6"/></g>')
    npatch = f'<circle cx="166" cy="-392" r="56" fill="{c["fill"]}"/><path d="M128 -420 l60 -20 l0 14 l-60 20Z" fill="{c["stripe"]}"/>'
    sh = '<ellipse cx="0" cy="4" rx="240" ry="18" fill="#000" opacity=".13"/>'
    return f'<g id="{pid}">{sh}<g id="{pid}-all">{tail}<g>{far_legs}</g>{neck}{body}{near_legs}</g></g>'


def zebra2(pid): return zebra(pid, seed=11)


art2.RIGS["giraffe"] = dict(build=lambda p: giraffe(p), neck="150 -540", tail="-205 -510", ear="282 -1030",
                            legs={"fl": 134, "bl": -128, "fl2": 92, "bl2": -176}, hip=-470, jaw=("y", 12), eyes=["eye"], brows=["brow"])
art2.RIGS["zebra"] = dict(build=lambda p: zebra(p), neck="160 -400", tail="-208 -390", ear="262 -630",
                          legs={"fl": 142, "bl": -126, "fl2": 100, "bl2": -170}, hip=-350, jaw=("y", 10), eyes=["eye"], brows=["brow"])
art2.RIGS["zebra2"] = dict(art2.RIGS["zebra"], build=zebra2)
kit.PT["giraffe"] = {"head": (370, -1010), "eye": (352, -1026), "body": (0, -500), "top": (350, -1130), "neck": (230, -800), "legs": (0, -230), "hoof": (134, -20),
                     "feet": (0, 0), "all": (90, -560)}
kit.BOX["giraffe"] = (-260, 480, -1140)
kit.PT["zebra"] = {"head": (350, -560), "eye": (330, -586), "body": (0, -360), "top": (280, -700), "legs": (0, -170), "hoof": (142, -20), "feet": (0, 0), "all": (90, -330)}
kit.BOX["zebra"] = (-260, 460, -710)
kit.PT["zebra2"] = kit.PT["zebra"]; kit.BOX["zebra2"] = kit.BOX["zebra"]


# ================================================================== footprints in the sand (drawn flat, seen from above; a soft rim of pushed-up sand)
SAND_D = "#b8893e"; SAND_DD = "#9a6f2c"; RIM = "#f2d78f"


def print_elephant(pid, s=1.0):
    """The elephant's print: big and round, with little toenail marks at the front."""
    nails = "".join(f'<ellipse cx="{x}" cy="{y}" rx="20" ry="13" fill="{SAND_DD}" transform="rotate({a} {x} {y})"/>'
                    for x, y, a in ((-92, -96, -30), (-44, -128, -12), (12, -136, 0), (64, -122, 14), (106, -88, 32)))
    return (f'<g id="{pid}" transform="scale({s})"><ellipse cx="0" cy="0" rx="150" ry="132" fill="{RIM}"/><ellipse cx="0" cy="4" rx="132" ry="114" fill="{SAND_D}"/>'
            f'<ellipse cx="-20" cy="20" rx="80" ry="60" fill="{SAND_DD}" opacity=".35"/>{nails}</g>')


def print_giraffe(pid, s=1.0):
    """The giraffe's print: two halves side by side, with a gap between (two hooves on each foot)."""
    half = lambda k: (f'<path d="M{k * 10} -96 C{k * 70} -96 {k * 84} -10 {k * 66} 60 C{k * 54} 100 {k * 24} 104 {k * 10} 90Z" fill="{SAND_D}" stroke="{RIM}" stroke-width="16" stroke-linejoin="round"/>'
                      f'<path d="M{k * 22} -60 C{k * 50} -50 {k * 56} 10 {k * 44} 50" stroke="{SAND_DD}" stroke-width="10" fill="none" stroke-linecap="round" opacity=".5"/>')
    return f'<g id="{pid}" transform="scale({s})"><g id="{pid}-a">{half(-1)}</g><g id="{pid}-b">{half(1)}</g></g>'


def print_zebra(pid, s=1.0):
    """The zebra's print: one smooth, round hoof (one toe inside one hoof)."""
    return (f'<g id="{pid}" transform="scale({s})"><path d="M0 -92 C70 -92 92 -20 84 40 C78 84 40 96 0 96 C-40 96 -78 84 -84 40 C-92 -20 -70 -92 0 -92Z" fill="{SAND_D}" stroke="{RIM}" stroke-width="16"/>'
            f'<path d="M-24 70 L0 10 L24 70" stroke="{SAND_DD}" stroke-width="12" fill="none" stroke-linecap="round" stroke-linejoin="round" opacity=".55"/></g>')


# ================================================================== close-ups for the fact boards
def ele_foot_front(pid, c=art2.ELE):
    """An elephant's front foot, seen from the front: a round pillar on a flat sole, five toenails in a row (#<pid>-n0..n4: to count)."""
    ln = c["line"]
    sh = '<path d="M-150 -360 L-150 -60 Q-150 0 -90 0 L90 0 Q150 0 150 -60 L150 -360Z"/>'
    nails = "".join(f'<g id="{pid}-n{k}"><path d="M{x - 26} -6 Q{x - 26} -56 {x} -58 Q{x + 26} -56 {x + 26} -6Z" fill="{c["nail"]}" stroke="{ln}" stroke-width="7" stroke-linejoin="round"/></g>'
                    for k, x in enumerate((-104, -52, 0, 52, 104)))
    wr = "".join(f'<path d="M{-110 + k * 10} {-300 + k * 60} q110 18 220 0" stroke="{c["shade"]}" stroke-width="8" fill="none" stroke-linecap="round"/>' for k in range(3))
    return (f'<g id="{pid}"><ellipse cx="0" cy="6" rx="190" ry="20" fill="#000" opacity=".13"/>{_ol(sh, ln)}<g fill="{c["fill"]}">{sh}</g>{wr}'
            f'<path d="M-150 -360 L-110 -360 L-110 -10 Q-130 -6 -150 -40Z" fill="{c["light"]}" opacity=".5"/>{nails}</g>')


def ele_foot_cut(pid, c=art2.ELE):
    """An elephant's foot cut open, side view facing right: the toe bones slope down to the front, standing on tiptoe (#<pid>-bones),
    over a big soft cushion (#<pid>-pad: squishes). SDZWA: walk "on tiptoes"; "fat pads" cushion bottoms of feet."""
    ln = c["line"]
    sh = '<path d="M-130 -380 L-150 -80 Q-160 0 -80 0 L120 0 Q176 0 170 -60 L130 -380Z"/>'
    bones = (f'<g id="{pid}-bones" fill="#fffaf0" stroke="#7a6a4c" stroke-width="8" stroke-linejoin="round">'
             f'<rect x="-40" y="-380" width="70" height="150" rx="26"/>'
             f'<path d="M-6 -240 L30 -232 L100 -96 L72 -82Z"/><circle cx="86" cy="-80" r="20"/>'
             f'<path d="M-30 -238 L0 -230 L58 -110 L32 -100Z"/><circle cx="44" cy="-96" r="17"/></g>')
    pad = (f'<g id="{pid}-pad"><path d="M-140 -40 C-150 -170 -60 -230 10 -170 C50 -130 70 -80 70 -50 C70 -14 30 -6 -40 -6 C-110 -6 -138 -14 -140 -40Z" fill="#ffd9a0" stroke="#e8a85a" stroke-width="8"/>'
           f'<ellipse cx="-70" cy="-90" rx="30" ry="18" fill="#fff" opacity=".55"/></g>')
    nail = f'<path d="M150 -10 Q176 -40 160 -70 Q132 -48 120 -8Z" fill="{c["nail"]}" stroke="{ln}" stroke-width="7"/>'
    return (f'<g id="{pid}"><ellipse cx="10" cy="6" rx="200" ry="20" fill="#000" opacity=".13"/>{_ol(sh, ln)}<g fill="{c["light"]}">{sh}</g>'
            f'{pad}{bones}{nail}</g>')


def gir_foot(pid, c=GIR):
    """A giraffe's foot close up, side view facing right: the lower leg and TWO big hooves side by side (#<pid>-h0, #<pid>-h1: they pulse)."""
    ln = c["line"]
    sh = '<path d="M-60 -420 L-56 -200 L56 -200 L60 -420Z"/>'
    h0 = f'<g id="{pid}-h0"><path d="M-64 -210 L-10 -210 L-10 0 L-84 0 Q-96 -60 -64 -210Z" fill="{c["hoof"]}" stroke="{ln}" stroke-width="9" stroke-linejoin="round"/><path d="M-52 -180 L-56 -30" stroke="#8a5a34" stroke-width="10" stroke-linecap="round"/></g>'
    h1 = f'<g id="{pid}-h1"><path d="M10 -210 L64 -210 Q100 -60 90 0 L10 0Z" fill="{c["hoof"]}" stroke="{ln}" stroke-width="9" stroke-linejoin="round"/><path d="M34 -180 L40 -30" stroke="#8a5a34" stroke-width="10" stroke-linecap="round"/></g>'
    return (f'<g id="{pid}"><ellipse cx="0" cy="6" rx="130" ry="16" fill="#000" opacity=".13"/>{_ol(sh, ln)}<g fill="{c["fill"]}">{sh}</g>'
            f'<ellipse cx="-10" cy="-340" rx="22" ry="30" fill="{c["spot_l"]}"/>{h0}{h1}</g>')


def zeb_foot_cut(pid, c=ZEB):
    """A zebra's foot cut open, side view facing right: ONE toe bone (#<pid>-toe) inside ONE hoof (#<pid>-hoof) that wraps round it.
    SDZWA: "Single toe at terminus of each limb"; "Hooves enclose and protect the toe"."""
    ln = c["line"]
    sh = '<path d="M-50 -420 L-50 -170 L50 -170 L50 -420Z"/>'
    stripes = "".join(f'<path d="M-50 {y} q50 10 100 0 l0 18 q-50 10 -100 0Z" fill="{c["stripe"]}"/>' for y in (-400, -350, -300, -250))
    hoof = (f'<g id="{pid}-hoof"><path d="M-60 -190 L60 -190 Q96 -60 104 0 L-104 0 Q-96 -60 -60 -190Z" fill="{c["hoof"]}" stroke="{ln}" stroke-width="9" stroke-linejoin="round"/>'
            f'<path d="M-44 -170 L44 -170 Q70 -70 74 -26 L-74 -26 Q-70 -70 -44 -170Z" fill="#6a6474"/></g>')
    toe = (f'<g id="{pid}-toe" fill="#fffaf0" stroke="#b9a98c" stroke-width="7" stroke-linejoin="round"><rect x="-22" y="-330" width="44" height="130" rx="18"/>'
           f'<path d="M-30 -196 L30 -196 Q46 -110 50 -50 L-50 -50 Q-46 -110 -30 -196Z"/></g>')
    return (f'<g id="{pid}"><ellipse cx="0" cy="6" rx="150" ry="16" fill="#000" opacity=".13"/>{_ol(sh, ln)}<g fill="{c["fill"]}">{sh}</g>{stripes}{hoof}{toe}</g>')


def plate(pid, s=1.0):
    """A big round dinner plate, seen a little from above (SDZWA: a giraffe's feet are "the size of a dinner plate")."""
    return (f'<g id="{pid}" transform="scale({s})"><ellipse cx="0" cy="8" rx="200" ry="70" fill="#000" opacity=".12"/><ellipse cx="0" cy="0" rx="200" ry="70" fill="#ffffff" stroke="#8aa1b8" stroke-width="9"/>'
            f'<ellipse cx="0" cy="0" rx="140" ry="46" fill="#eef4fb" stroke="#bcd0e2" stroke-width="6"/><path d="M-170 -10 q170 -60 340 0" stroke="#7fb3e6" stroke-width="7" fill="none" opacity=".6"/></g>')


def plate_top(pid, s=1.0):
    """A dinner plate seen from straight above, so a footprint can lie on it to compare the size."""
    return (f'<g id="{pid}" transform="scale({s})"><circle cx="8" cy="12" r="230" fill="#000" opacity=".1"/><circle r="230" fill="#ffffff" stroke="#8aa1b8" stroke-width="10"/>'
            f'<circle r="170" fill="#f3f8fd" stroke="#bcd0e2" stroke-width="7"/><path d="M-150 -120 a200 200 0 0 1 120 -70" stroke="#7fb3e6" stroke-width="10" fill="none" stroke-linecap="round" opacity=".6"/></g>')


def hand_one(pid, s=1.0):
    """A child's hand holding up one finger (for one zebra toe), with a little fingernail."""
    sk = "#f6c9a4"; ln = "#9a5a34"
    sh = ('<rect x="-90" y="-120" width="180" height="170" rx="70"/><rect x="-28" y="-330" width="56" height="240" rx="28"/>'
          '<path d="M-90 -60 q-70 -30 -60 -90 q30 0 70 50Z"/><rect x="-80" y="40" width="160" height="120" rx="30"/>')
    folded = "".join(f'<path d="M{x} -120 q12 -30 30 0" stroke="{ln}" stroke-width="7" fill="none" stroke-linecap="round"/>' for x in (-80, 34))
    return (f'<g id="{pid}" transform="scale({s})">{_ol(sh, ln, 8)}<g fill="{sk}">{sh}</g>{folded}'
            f'<path d="M-16 -318 Q0 -334 16 -318 L16 -286 Q0 -278 -16 -286Z" fill="#ffe9de" stroke="{ln}" stroke-width="5"/></g>')


def bump(pid):
    """Three little curved lines: a soft bump (the cushion soaks it up)."""
    return f'<g id="{pid}">' + "".join(f'<path d="M{-60 + k * 60} 0 q-20 -26 0 -52" stroke="#3d6fb0" stroke-width="12" fill="none" stroke-linecap="round"/>' for k in range(3)) + '</g>'


def rumble(pid):
    """Little wavy lines in the ground: tiny rumbles."""
    return f'<g id="{pid}">' + "".join(f'<path id="{pid}-w{k}" d="M-160 {k * 26} q20 -14 40 0 q20 14 40 0 q20 -14 40 0 q20 14 40 0 q20 -14 40 0 q20 14 40 0 q20 -14 40 0 q20 14 40 0" stroke="#8a5a2c" stroke-width="8" fill="none" stroke-linecap="round" opacity="{.9 - k * .25}"/>' for k in range(3)) + '</g>'


def side_arrow(pid, col="#ff5a5f"):
    """A short curved arrow pointing forward: 'this side moves'."""
    return (f'<g id="{pid}"><path d="M-80 0 Q0 -50 80 0" stroke="{INK}" stroke-width="26" fill="none" stroke-linecap="round"/><path d="M-80 0 Q0 -50 80 0" stroke="{col}" stroke-width="14" fill="none" stroke-linecap="round"/>'
            f'<path d="M58 -30 L96 8 L46 22Z" fill="{col}" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/></g>')


def qmark(pid, col="#ffd23f"):
    """A big question mark on a disc (the mystery)."""
    return (f'<g id="{pid}"><circle r="110" fill="#ffffff" stroke="{INK}" stroke-width="10"/><text x="0" y="8" text-anchor="middle" dominant-baseline="central" font-family="Fredoka, Baloo, sans-serif" '
            f'font-weight="800" font-size="190" fill="{col}" stroke="{INK}" stroke-width="12" paint-order="stroke">?</text></g>')


# ================================================================== the sandy path on the savanna
def bg_sandtrail(p):
    """The sunny savanna with a wide sandy path across the front, soft and smooth: footprints show well on it."""
    far, mid, _ = art2.bg_savanna(p)
    near = ('<rect x="-500" y="840" width="2920" height="1200" fill="#e0bf5c"/>'
            '<path d="M-500 880 C300 850 900 870 1400 856 S2100 864 2420 874 L2420 1980 L-500 1980Z" fill="#e0bf5c"/>'
            '<path d="M-500 930 C300 900 1000 920 1500 906 S2100 912 2420 920 L2420 1300 C1800 1280 1000 1300 -500 1290Z" fill="#f3d68c"/>'
            '<path d="M-500 940 C300 912 1000 930 1500 918 S2100 922 2420 930" stroke="#e8c573" stroke-width="10" fill="none"/>'
            + "".join(art2._grass(x, y, 1.0) for x, y in ((40, 900), (1880, 905), (1300, 1330), (300, 1340), (900, 1360)))
            + "".join(f'<ellipse cx="{x}" cy="{y}" rx="{w}" ry="5" fill="#e3bf6c" opacity=".7"/>' for x, y, w in ((220, 1180, 60), (1620, 1120, 80), (1040, 1250, 50), (560, 1020, 40))))
    return far, mid, near


art.BG.update({"sandtrail": bg_sandtrail})
art.PLACE.update({"sandtrail": "the sandy path"})
