"""Art for zc_ep08 "Who Lives at the Top of the Jungle?" (Nov 19 2026): the four layers of the rainforest as four places
(the dark forest floor, the shady understory, the existing canopy, the sunny emergent layer above the treetops), four new animals
(a giant anteater, a little tree frog, a scarlet macaw, a harpy eagle: one rig each), a blue butterfly, and the boards:
the layer tree cut in four floors, the sun and the leaf roof, a big leaf, the frog's wet skin, tall and short trees.
Same hand as art.py / art2.py: flat fills, one warm dark outline, big brown eyes, pink cheeks. Nothing here changes an existing character, prop or place.
Read only: art2.bg_canopy, art2._leaf, art2.fruit, art.eye, art.arrow."""
import art, art2, kit
from art import INK, eye

_ol = art2._ol


# ================================================================== the giant anteater (side view, facing right, feet on y = 0)
ANT = {"fur": "#9b8a78", "dark": "#5b4c40", "light": "#c9bba9", "stripe": "#2e2620", "white": "#f4efe6", "line": "#3a2e26"}


def anteater(pid, c=ANT):
    """A giant anteater: a long, long nose (-snout turns round where it joins the head), a big bushy tail (-tail), a black and white stripe on the
    shoulder, four legs (-fl -bl -fl2 -bl2 swing round the hip line y = -120), -eye, -brow, -jaw (the long pink tongue, hidden until it talks or licks),
    -smile / -frown (a small mouth line at the tip of the nose)."""
    ln = c["line"]
    def leg(x, col, band=False):
        b = f'<rect x="{x - 24}" y="-62" width="48" height="16" fill="{c["stripe"]}"/>' if band else ""
        return (f'<path d="M{x - 26} -130 L{x - 24} -14 Q{x} 6 {x + 28} -10 L{x + 26} -130Z" fill="{col}" stroke="{ln}" stroke-width="8" stroke-linejoin="round"/>{b}'
                f'<path d="M{x - 18} -6 l-6 10 M{x} -4 l0 12 M{x + 18} -6 l6 10" stroke="{ln}" stroke-width="6" stroke-linecap="round"/>')
    fl = f'<g id="{pid}-fl">{leg(120, c["white"], True)}</g>'; fl2 = f'<g id="{pid}-fl2">{leg(80, c["light"], True)}</g>'
    bl = f'<g id="{pid}-bl">{leg(-120, c["fur"])}</g>'; bl2 = f'<g id="{pid}-bl2">{leg(-160, c["dark"])}</g>'
    tail_sh = '<path d="M-180 -200 C-300 -260 -380 -330 -400 -250 C-420 -170 -330 -110 -190 -130Z"/>'
    tail = (f'<g id="{pid}-tail">{_ol(tail_sh, ln, 8)}<g fill="{c["dark"]}">{tail_sh}</g>'
            + "".join(f'<path d="M{x} {y} q-30 20 -50 4" stroke="{c["fur"]}" stroke-width="7" fill="none" stroke-linecap="round"/>' for x, y in ((-250, -250), (-300, -210), (-260, -170), (-330, -260)))
            + '</g>')
    body_sh = '<ellipse cx="-10" cy="-190" rx="210" ry="105"/>'
    body = (_ol(body_sh, ln, 8) + f'<ellipse cx="-10" cy="-190" rx="210" ry="105" fill="{c["fur"]}"/>'
            f'<path d="M150 -255 C80 -230 10 -190 -90 -140 L-70 -112 C30 -160 110 -196 186 -214Z" fill="{c["stripe"]}"/>'
            f'<path d="M156 -235 C96 -214 30 -180 -60 -138 L-50 -126 C40 -166 110 -198 176 -220Z" fill="{c["white"]}"/>'
            f'<ellipse cx="-60" cy="-250" rx="90" ry="22" fill="#fff" opacity=".18"/>')
    head_sh = '<ellipse cx="200" cy="-230" rx="78" ry="62"/>'
    snout_sh = '<path d="M240 -268 C330 -262 420 -232 470 -206 C478 -200 476 -186 466 -184 C410 -178 320 -190 236 -196Z"/>'
    snout = (f'<g id="{pid}-snout">{_ol(snout_sh, ln, 8)}<g fill="{c["light"]}">{snout_sh}</g>'
             f'<ellipse cx="468" cy="-196" rx="10" ry="8" fill="{c["stripe"]}"/>'
             f'<g id="{pid}-jaw" opacity="0"><path d="M468 -190 C510 -186 540 -168 560 -150" stroke="#ff7a9a" stroke-width="10" fill="none" stroke-linecap="round"/></g>'
             f'<g id="{pid}-smile"><path d="M430 -186 q14 6 28 0" stroke="{ln}" stroke-width="5" fill="none" stroke-linecap="round"/></g>'
             f'<g id="{pid}-frown" opacity="0"><path d="M430 -182 q14 -6 28 0" stroke="{ln}" stroke-width="5" fill="none" stroke-linecap="round"/></g></g>')
    head = (_ol(head_sh, ln, 8) + f'<ellipse cx="200" cy="-230" rx="78" ry="62" fill="{c["light"]}"/>'
            f'<path d="M170 -284 q-4 -40 26 -38 q16 6 6 40Z" fill="{c["fur"]}" stroke="{ln}" stroke-width="7" stroke-linejoin="round"/>'
            + eye(f"{pid}-eye", 226, -246, 17, lid=c["light"])
            + f'<path id="{pid}-brow" d="M206 -276 q20 -12 40 -2" stroke="{ln}" stroke-width="6" fill="none" stroke-linecap="round"/>'
            + f'<ellipse cx="250" cy="-214" rx="13" ry="8" fill="#ff8fb1" opacity=".7"/>')
    sh = '<ellipse cx="0" cy="4" rx="230" ry="16" fill="#000" opacity=".14"/>'
    return f'<g id="{pid}">{sh}{tail}{bl2}{fl2}<g id="{pid}-body">{body}</g>{bl}{fl}{snout}{head}</g>'


# ================================================================== the tree frog (front view, sitting, feet on y = 0)
FROG = {"skin": "#5ccf5a", "dark": "#2f9a3e", "belly": "#e9f7c9", "line": "#1d5a28", "toe": "#ff9a3c", "side": "#3f7fe0"}


def frog(pid, c=FROG):
    """A little green tree frog sitting on a leaf: big round eyes on top (-eyeL -eyeR), orange toes, blue sides, -throat puffs (ribbit),
    -jaw (open mouth), -smile / -frown, -body."""
    ln = c["line"]
    toes = lambda x, y, s: "".join(f'<path d="M{x} {y} l{dx * s} {dy}" stroke="{c["toe"]}" stroke-width="12" stroke-linecap="round"/><circle cx="{x + dx * s}" cy="{y + dy}" r="11" fill="{c["toe"]}" stroke="{ln}" stroke-width="4"/>'
                                   for dx, dy in ((-26, 4), (-8, 14), (14, 12)))
    legs_sh = '<ellipse cx="-92" cy="-46" rx="52" ry="40"/><ellipse cx="92" cy="-46" rx="52" ry="40"/>'
    body_sh = '<ellipse cx="0" cy="-90" rx="104" ry="86"/>'
    head_sh = '<circle cx="-54" cy="-176" r="44"/><circle cx="54" cy="-176" r="44"/>'
    body = (_ol(legs_sh + body_sh + head_sh, ln, 7)
            + f'<g fill="{c["dark"]}">{legs_sh}</g><ellipse cx="0" cy="-90" rx="104" ry="86" fill="{c["skin"]}"/>'
            + f'<path d="M-100 -96 q-6 40 20 70 M100 -96 q6 40 -20 70" stroke="{c["side"]}" stroke-width="16" fill="none" stroke-linecap="round"/>'
            + f'<g fill="{c["skin"]}">{head_sh}</g><ellipse cx="0" cy="-60" rx="62" ry="46" fill="{c["belly"]}"/>'
            + f'<g id="{pid}-throat" opacity="0"><ellipse cx="0" cy="-84" rx="44" ry="30" fill="#f7f2b0" stroke="{ln}" stroke-width="5"/></g>'
            + toes(-112, -14, -1) + toes(112, -14, 1) + toes(-40, -10, -1) + toes(40, -10, 1)
            + eye(f"{pid}-eyeL", -54, -178, 30, lid=c["skin"]) + eye(f"{pid}-eyeR", 54, -178, 30, lid=c["skin"])
            + f'<ellipse cx="-70" cy="-120" rx="13" ry="8" fill="#ff8fb1" opacity=".75"/><ellipse cx="70" cy="-120" rx="13" ry="8" fill="#ff8fb1" opacity=".75"/>'
            + f'<g id="{pid}-jaw" opacity="0"><path d="M-34 -124 Q0 -88 34 -124Z" fill="#8a2f3f" stroke="{ln}" stroke-width="5" stroke-linejoin="round"/></g>'
            + f'<g id="{pid}-smile"><path d="M-46 -126 Q0 -100 46 -126" stroke="{ln}" stroke-width="6" fill="none" stroke-linecap="round"/></g>'
            + f'<g id="{pid}-frown" opacity="0"><path d="M-36 -112 Q0 -128 36 -112" stroke="{ln}" stroke-width="6" fill="none" stroke-linecap="round"/></g>'
            + f'<ellipse cx="-30" cy="-150" rx="26" ry="10" fill="#fff" opacity=".25"/>')
    sh = '<ellipse cx="0" cy="4" rx="120" ry="12" fill="#000" opacity=".14"/>'
    return f'<g id="{pid}">{sh}<g id="{pid}-body">{body}</g></g>'


# ================================================================== the scarlet macaw (side view, facing right, feet on y = 0)
MAC = {"red": "#e8322e", "dark": "#b8201e", "yellow": "#ffd23f", "blue": "#2f80ed", "beak": "#f4ecd8", "beak_d": "#3a3030", "face": "#fff6ee", "line": "#6a1414"}


def macaw(pid, c=MAC):
    """A scarlet macaw on a branch: red body, a yellow and blue wing (-wing flaps), a long red and blue tail (-tail), a big curved pale beak
    (-jaw is the dark lower beak), a white face, -eye, -brow, -smile / -frown (empty: a beak does not smile)."""
    ln = c["line"]
    tail_sh = '<path d="M-60 -140 L-250 120 L-210 140 L-30 -100Z"/>'
    tail = (f'<g id="{pid}-tail">{_ol(tail_sh, ln, 7)}<g fill="{c["red"]}">{tail_sh}</g>'
            f'<path d="M-150 -10 L-236 120 L-214 132 L-130 6Z" fill="{c["blue"]}"/></g>')
    legs = "".join(f'<path d="M{x} -60 L{x} -8 M{x} -8 l-16 8 M{x} -8 l18 6" stroke="#6a6a6a" stroke-width="10" fill="none" stroke-linecap="round"/>' for x in (-14, 22))
    sil = '<ellipse cx="0" cy="-150" rx="70" ry="100" transform="rotate(18 0 -150)"/><circle cx="48" cy="-262" r="62"/>'
    body = (_ol(sil, ln, 7) + f'<g fill="{c["red"]}">{sil}</g>'
            f'<ellipse cx="62" cy="-262" rx="34" ry="30" fill="{c["face"]}"/>'
            f'<ellipse cx="20" cy="-300" rx="22" ry="10" fill="#fff" opacity=".3" transform="rotate(-24 20 -300)"/>')
    wing = (f'<g id="{pid}-wing"><path d="M-40 -220 C30 -200 50 -120 10 -40 C-30 -60 -70 -140 -40 -220Z" fill="{c["yellow"]}" stroke="{ln}" stroke-width="7" stroke-linejoin="round"/>'
            f'<path d="M-14 -130 C20 -110 26 -70 10 -40 C-14 -58 -30 -90 -14 -130Z" fill="{c["blue"]}"/>'
            f'<path d="M-30 -160 q24 6 36 24" stroke="{c["dark"]}" stroke-width="6" fill="none" stroke-linecap="round"/></g>')
    beak = (f'<g id="{pid}-jaw"><path d="M92 -236 C112 -230 120 -214 112 -204 C100 -206 92 -218 88 -228Z" fill="{c["beak_d"]}" stroke="{ln}" stroke-width="5" stroke-linejoin="round"/></g>'
            f'<path d="M84 -284 C130 -290 152 -250 132 -212 C126 -224 112 -236 90 -236Z" fill="{c["beak"]}" stroke="{ln}" stroke-width="6" stroke-linejoin="round"/>')
    face = (eye(f"{pid}-eye", 62, -270, 15, lid=c["face"])
            + f'<path id="{pid}-brow" d="M42 -298 q20 -10 40 0" stroke="{ln}" stroke-width="6" fill="none" stroke-linecap="round"/>'
            + f'<g id="{pid}-smile"></g><g id="{pid}-frown" opacity="0"></g>')
    sh = '<ellipse cx="0" cy="3" rx="70" ry="10" fill="#000" opacity=".13"/>'
    return f'<g id="{pid}">{sh}{tail}{legs}{body}{wing}{beak}{face}</g>'


# ================================================================== the harpy eagle (front view, perched, feet on y = 0)
EAG = {"grey": "#a9adb4", "dark": "#3d3f46", "light": "#dfe2e6", "white": "#fbfbf8", "beak": "#2b2b30", "foot": "#ffcf3a", "line": "#24252a"}


def eagle(pid, c=EAG):
    """A harpy eagle perched on a branch: grey head with a crest of feathers on top (-crest), a dark band across the chest, a white tummy,
    dark wings at the sides (-wl -wr open round the shoulders), big yellow feet, a dark hooked beak (-jaw is the lower part), -eyeL -eyeR, -browL -browR."""
    ln = c["line"]
    wing = lambda s: (f'<g id="{pid}-w{"lr"[s > 0]}"><path d="M{s * 70} -300 C{s * 170} -290 {s * 200} -180 {s * 170} -60 L{s * 120} -90 L{s * 110} -50 L{s * 70} -100Z" '
                      f'fill="{c["dark"]}" stroke="{ln}" stroke-width="8" stroke-linejoin="round"/>'
                      f'<path d="M{s * 110} -260 q{s * 30} 60 {s * 26} 140 M{s * 140} -230 q{s * 16} 60 {s * 14} 120" stroke="#5a5c64" stroke-width="7" fill="none" stroke-linecap="round"/></g>')
    feet = "".join(f'<path d="M{x} -40 L{x} -8 M{x} -8 l-22 10 M{x} -8 l0 14 M{x} -8 l22 10" stroke="{c["foot"]}" stroke-width="16" fill="none" stroke-linecap="round"/>' for x in (-40, 40))
    body_sh = '<ellipse cx="0" cy="-170" rx="100" ry="140"/>'
    head_sh = '<circle cx="0" cy="-350" r="86"/>'
    crest = (f'<g id="{pid}-crest"><path d="M-30 -420 L-90 -500 L-40 -440 L-60 -520 L-8 -432Z M30 -420 L90 -500 L40 -440 L60 -520 L8 -432Z" '
             f'fill="{c["dark"]}" stroke="{ln}" stroke-width="7" stroke-linejoin="round"/></g>')
    body = (_ol(body_sh + head_sh, ln, 8) + f'<ellipse cx="0" cy="-170" rx="100" ry="140" fill="{c["white"]}"/>'
            f'<path d="M-96 -232 C-40 -270 40 -270 96 -232 L96 -196 C40 -232 -40 -232 -96 -196Z" fill="{c["dark"]}"/>'
            + "".join(f'<path d="M{x} {y} l12 12" stroke="#c9ccd2" stroke-width="6" stroke-linecap="round"/>' for x, y in ((-50, -150), (10, -120), (40, -170), (-20, -90), (50, -90), (-60, -100)))
            + f'<circle cx="0" cy="-350" r="86" fill="{c["grey"]}"/><ellipse cx="0" cy="-322" rx="56" ry="44" fill="{c["light"]}"/>'
            + f'<ellipse cx="-30" cy="-400" rx="28" ry="12" fill="#fff" opacity=".3" transform="rotate(-20 -30 -400)"/>')
    face = (eye(f"{pid}-eyeL", -34, -360, 22, lid=c["grey"]) + eye(f"{pid}-eyeR", 34, -360, 22, lid=c["grey"])
            + f'<path id="{pid}-browL" d="M-60 -392 q24 -10 46 2" stroke="{c["dark"]}" stroke-width="8" fill="none" stroke-linecap="round"/>'
            + f'<path id="{pid}-browR" d="M60 -392 q-24 -10 -46 2" stroke="{c["dark"]}" stroke-width="8" fill="none" stroke-linecap="round"/>'
            + f'<ellipse cx="-58" cy="-326" rx="12" ry="8" fill="#ff8fb1" opacity=".6"/><ellipse cx="58" cy="-326" rx="12" ry="8" fill="#ff8fb1" opacity=".6"/>'
            + f'<g id="{pid}-jaw"><path d="M-14 -316 Q0 -296 14 -316Z" fill="#55565e" stroke="{ln}" stroke-width="5" stroke-linejoin="round"/></g>'
            + f'<path d="M-22 -340 C-20 -360 20 -360 22 -340 C20 -322 8 -306 0 -300 C-8 -306 -20 -322 -22 -340Z" fill="{c["beak"]}" stroke="{ln}" stroke-width="5" stroke-linejoin="round"/>'
            + f'<g id="{pid}-smile"></g><g id="{pid}-frown" opacity="0"></g>')
    sh = '<ellipse cx="0" cy="4" rx="110" ry="12" fill="#000" opacity=".13"/>'
    return f'<g id="{pid}">{sh}{wing(-1)}{wing(1)}{feet}{crest}<g id="{pid}-body">{body}{face}</g></g>'


art2.RIGS.update({
    "anteater": dict(build=lambda p: anteater(p), neck=None, tail="-190 -170", ear=None, legs={"fl": 120, "bl": -120, "fl2": 80, "bl2": -160}, hip=-130, jaw=("y", 4), eyes=["eye"], brows=["brow"]),
    "frog": dict(build=lambda p: frog(p), neck=None, tail=None, ear=None, legs=None, hip=0, jaw=("y", 4), eyes=["eyeL", "eyeR"], brows=[]),
    "macaw": dict(build=lambda p: macaw(p), neck=None, tail="-50 -120", ear=None, legs=None, hip=0, jaw=("rot", 16, "92 -232"), eyes=["eye"], brows=["brow"]),
    "eagle": dict(build=lambda p: eagle(p), neck=None, tail=None, ear=None, legs=None, hip=0, jaw=("y", 6), eyes=["eyeL", "eyeR"], brows=["browL", "browR"]),
})
kit.PT.update({"anteater": {"head": (200, -230), "body": (0, -190), "top": (200, -300), "nose": (440, -200), "feet": (0, 0), "all": (40, -190)},
               "frog": {"head": (0, -170), "body": (0, -90), "top": (0, -220), "feet": (0, 0), "all": (0, -110)},
               "macaw": {"head": (60, -262), "body": (0, -150), "top": (48, -330), "beak": (120, -250), "feet": (0, 0), "all": (0, -160)},
               "eagle": {"head": (0, -350), "body": (0, -170), "top": (0, -520), "feet": (0, 0), "all": (0, -260)}})
kit.BOX.update({"anteater": (-420, 480, -330), "frog": (-140, 140, -225), "macaw": (-250, 150, -340), "eagle": (-210, 210, -525)})


# ================================================================== places
def _crown(x, y, rx, ry, col, dark):
    """One round tree top seen from the side, with a darker lower half."""
    return (f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{col}"/><ellipse cx="{x}" cy="{y + ry * .35:.0f}" rx="{rx * .92:.0f}" ry="{ry * .6:.0f}" fill="{dark}" opacity=".55"/>'
            f'<ellipse cx="{x - rx * .3:.0f}" cy="{y - ry * .45:.0f}" rx="{rx * .35:.0f}" ry="{ry * .25:.0f}" fill="#fff" opacity=".12"/>')


def bg_floor(p):
    """The forest floor: the darkest layer. Thick trunks, roots, fallen brown leaves on the ground (y = 900), a few thin beams of light from far above."""
    far = (f'<rect x="-500" y="-1900" width="2920" height="3900" fill="#1f3b2a"/>'
           + "".join(f'<rect x="{x - w / 2}" y="-1900" width="{w}" height="2800" fill="#2c4a34"/>' for x, w in ((60, 120), (520, 90), (1000, 140), (1460, 100), (1900, 130), (-300, 110), (2250, 100)))
           + "".join(f'<path d="M{x} -900 L{x + 60} -900 L{x + 220} 900 L{x + 120} 900Z" fill="#f6f2b0" opacity=".07"/>' for x in (300, 1180, 1700)))
    roots = lambda x, w: (f'<path d="M{x - w * .9} 905 C{x - w * .6} 860 {x - w * .55} 760 {x - w / 2} 600 L{x + w / 2} 600 C{x + w * .55} 760 {x + w * .6} 860 {x + w * .9} 905Z" fill="#4a3424"/>')
    mid = ("".join(f'<rect x="{x - w / 2}" y="-1900" width="{w}" height="2600" fill="#4a3424"/>{roots(x, w)}'
                   f'<rect x="{x - w / 2 + w * .62}" y="-1900" width="{w * .2}" height="2700" fill="#3a281b" opacity=".7"/>' for x, w in ((180, 200), (1680, 230), (2300, 180), (-420, 170)))
           + "".join(f'<path d="M{x} -1900 q{dx} 900 0 {L}" stroke="#2c6a3a" stroke-width="10" fill="none" stroke-linecap="round"/>' for x, dx, L in ((720, 40, 2300), (1320, -36, 2150), (980, 30, 1900)))
           + '<path d="M-500 860 C200 830 900 870 1500 850 S2200 856 2420 866 L2420 1100 L-500 1100Z" fill="#5a4128"/>')
    lv = [(-200, 930, 1.0, 10, "#8a5a2c"), (60, 1000, .8, 70, "#a86a32"), (330, 950, .9, -30, "#7a4a22"), (560, 1010, .8, 40, "#b07a3a"), (820, 940, 1.0, 120, "#8a5a2c"),
          (1050, 1000, .9, -60, "#a86a32"), (1300, 950, .8, 20, "#7a4a22"), (1520, 1010, 1.0, 150, "#b07a3a"), (1780, 950, .9, -20, "#8a5a2c"), (2050, 1000, .8, 60, "#a86a32"),
          (2300, 940, .9, 100, "#7a4a22"), (720, 1060, 1.1, 80, "#7a4a22"), (1200, 1070, 1.0, -100, "#8a5a2c"), (400, 1080, .9, 30, "#b07a3a"), (1650, 1070, 1.0, 10, "#7a4a22")]
    near = ('<rect x="-500" y="1040" width="2920" height="1000" fill="#4e3820"/>'
            + "".join(f'<path d="M0 0 C30 -40 100 -46 150 -12 C100 18 36 22 0 0Z" fill="{c}" transform="translate({x} {y}) rotate({r}) scale({s})"/>' for x, y, s, r, c in lv)
            + "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#c9b07a" opacity=".55"/>' for x, y, r in ((470, 925, 9), (1110, 965, 7), (1880, 930, 8))))
    return far, mid, near


def bg_understory(p):
    """The understory: under the tall trees, still shady and damp. Big broad leaves at every height, thin trunks, vines, a few spots of light.
    One big flat leaf in the middle (its top at y = 640, from x = 820 to 1300) where the tree frog sits."""
    far = (f'<rect x="-500" y="-1900" width="2920" height="3900" fill="#2f6a45"/>'
           + "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#e8f7b0" opacity=".10"/>' for x, y, r in ((300, 120, 60), (1500, 60, 80), (900, -200, 50), (1880, 300, 50), (-100, 380, 70)))
           + "".join(f'<rect x="{x - w / 2}" y="-1900" width="{w}" height="3900" fill="#3d7a52"/>' for x, w in ((80, 60), (640, 46), (1240, 70), (1760, 50), (2200, 60), (-320, 50))))
    big = lambda x, y, s, r, col, vein="#2a6a3c": (f'<g transform="translate({x} {y}) rotate({r}) scale({s})"><path d="M0 0 C60 -120 260 -150 380 -40 C270 60 90 70 0 0Z" fill="{col}"/>'
                                                  f'<path d="M10 0 C120 -30 240 -40 360 -40" stroke="{vein}" stroke-width="8" fill="none"/></g>')
    mid = ("".join(f'<rect x="{x - w / 2}" y="-1900" width="{w}" height="3900" fill="#5a4630"/>' for x, w in ((330, 70), (1640, 80)))
           + "".join(f'<path d="M{x} -1900 q{dx} 1100 0 {L}" stroke="#2f8a4c" stroke-width="9" fill="none" stroke-linecap="round"/>' for x, dx, L in ((520, 40, 2400), (1460, -36, 2250), (2000, 30, 2500)))
           + big(330, 300, 1.4, -160, "#3f9e5c") + big(330, 520, 1.2, -20, "#4fb56c") + big(1640, 260, 1.5, -25, "#3f9e5c") + big(1640, 520, 1.3, -150, "#57c078")
           + big(-120, 140, 1.6, -10, "#4fb56c") + big(2160, 180, 1.5, -170, "#4fb56c") + big(900, -120, 1.3, -40, "#3f9e5c") + big(1300, -60, 1.2, -140, "#57c078")
           # the frog's big leaf, held out flat on a thin stem from the right
           + '<path d="M1420 1100 C1400 900 1380 760 1290 660" stroke="#3a7a3a" stroke-width="18" fill="none" stroke-linecap="round"/>'
           + '<path d="M820 650 C900 600 1180 590 1310 640 C1200 700 920 712 820 650Z" fill="#6fd06a" stroke="#2a6a3c" stroke-width="9" stroke-linejoin="round"/>'
           + '<path d="M840 650 C980 640 1150 634 1290 642" stroke="#2a6a3c" stroke-width="7" fill="none"/>')
    near = (big(-200, 980, 2.0, -30, "#2f8a4c") + big(2200, 1000, 2.0, -150, "#2f8a4c") + big(200, 1080, 1.6, -70, "#3f9e5c") + big(1800, 1080, 1.6, -110, "#3f9e5c")
            + '<rect x="-500" y="1060" width="2920" height="1000" fill="#2a5a3a"/>')
    return far, mid, near


def bg_emergent(p):
    """The emergent layer: above the treetops in the bright sun. A carpet of round tree tops far below (from y = 640 down), two tall trees sticking
    up out of it far away, and the top of one tall tree here: its branch at y = 430 (the same height as the canopy's branch) where the eagle perches."""
    far = (art._sky(p, "#7fd0ff", "#dff6ff", y0=-1900, y1=900) + f'<rect x="-500" y="-1900" width="2920" height="200" fill="#7fd0ff"/>'
           + art._sun(p + "sun", 1640, -60, 110) + art._cloud(p + "c1", 380, 60, 1.0) + art._cloud(p + "c2", 1200, -260, .8)
           + _crown(260, 120, 170, 90, "#4fb56c", "#2f8a4c") + '<rect x="250" y="190" width="22" height="510" fill="#7a5632"/>'
           + _crown(1560, 180, 140, 80, "#57c078", "#2f8a4c") + '<rect x="1550" y="240" width="20" height="460" fill="#7a5632"/>')
    tops = [(-400, 700, 240, 120), (-120, 680, 230, 130), (160, 720, 250, 120), (460, 690, 240, 130), (760, 730, 260, 120), (1060, 700, 240, 130), (1360, 720, 260, 125),
            (1660, 690, 240, 130), (1960, 720, 250, 120), (2260, 700, 240, 130)]
    rows = "".join(_crown(x, y, rx, ry, "#4fb56c" if k % 2 else "#3f9e5c", "#2f8a4c") for k, (x, y, rx, ry) in enumerate(tops))
    rows2 = "".join(_crown(x + 150, y + 150, rx, ry, "#3f9e5c" if k % 2 else "#57c078", "#2b7a45") for k, (x, y, rx, ry) in enumerate(tops))
    mid = rows + rows2 + '<rect x="-500" y="900" width="2920" height="1200" fill="#2f8a4c"/>'
    # the tall tree here: its trunk comes up from below, one strong branch at y = 430 and its crown above the branch
    near = ('<path d="M1040 2000 C1050 1400 1060 900 1080 470 L1180 470 C1190 900 1210 1400 1230 2000Z" fill="#8a6238"/>'
            '<path d="M-500 410 C200 396 900 436 1500 420 S2200 428 2420 412 L2420 470 C1800 480 1200 486 600 470 S-200 452 -500 462Z" fill="#8a6238"/>'
            '<path d="M-500 446 C200 438 900 468 1500 456 S2200 458 2420 448 L2420 470 C1800 480 1200 486 600 470 S-200 452 -500 462Z" fill="#735029" opacity=".7"/>'
            + art2._leaf(-80, 420, 1.5, -30, "#2f8a4c") + art2._leaf(1760, 430, 1.5, -150, "#2f8a4c") + art2._leaf(260, 404, .9, -70, "#57c078"))
    return far, mid, near


art.BG.update({"floor": bg_floor, "understory": bg_understory, "emergent": bg_emergent})
art.PLACE.update({"floor": "the forest floor", "understory": "the understory", "emergent": "the emergent layer"})


# ================================================================== props
def butterfly(pid, col="#2f80ed", dark="#1c4fa0"):
    """A blue butterfly seen from above: -wings flap (scaleX)."""
    w = (f'<path d="M0 -6 C-40 -70 -110 -60 -96 -6 C-90 20 -40 20 0 0Z M0 6 C-30 40 -76 56 -70 18 C-66 4 -30 0 0 0Z" fill="{col}" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
         f'<path d="M-70 -30 C-60 -20 -40 -14 -20 -10" stroke="{dark}" stroke-width="6" fill="none" stroke-linecap="round"/>')
    return (f'<g id="{pid}"><g id="{pid}-wings"><g>{w}</g><g transform="scale(-1 1)">{w}</g></g>'
            f'<ellipse cx="0" cy="0" rx="9" ry="34" fill="{INK}"/><path d="M-4 -30 q-14 -24 -26 -28 M4 -30 q14 -24 26 -28" stroke="{INK}" stroke-width="5" fill="none" stroke-linecap="round"/></g>')


LAYER = [("#bfe9ff", "#7fd0ff"), ("#57c078", "#3f9e5c"), ("#3f8a5a", "#2f6a45"), ("#7a5a38", "#5a4128")]     # top to bottom: emergent, canopy, understory, floor


def layer_tree(pid, numbers=True):
    """The rainforest cut open in four floors, from the top: emergent (sky, two tall trees), canopy (a thick roof of tree tops), understory (small
    trees, big leaves), forest floor (brown ground, fallen leaves). Bands -b0 (top) .. -b3 (bottom), each 210 high, the whole thing 1240 wide,
    centred on (0, 0). Each band has a number tag on the left (-n0 .. -n3: 4 at the top, 1 at the bottom) and an empty spot on the right for an animal."""
    W, H = 1240, 210; x0 = -W / 2; y0 = -2 * H; out = []
    for k in range(4):
        y = y0 + k * H; a, b = LAYER[k]
        out.append(f'<g id="{pid}-b{k}"><clipPath id="{pid}-cl{k}"><rect x="{x0}" y="{y}" width="{W}" height="{H}"/></clipPath><g clip-path="url(#{pid}-cl{k})"><rect x="{x0}" y="{y}" width="{W}" height="{H}" fill="{a}"/>')
        if k == 0:   # two trees stick up out of the roof
            out.append(_crown(-180, y + 110, 110, 70, "#4fb56c", "#2f8a4c") + f'<rect x="-190" y="{y + 160}" width="20" height="60" fill="#7a5632"/>'
                       + _crown(260, y + 130, 90, 60, "#57c078", "#2f8a4c") + f'<rect x="252" y="{y + 170}" width="18" height="40" fill="#7a5632"/>'
                       + f'<circle cx="{x0 + 1120}" cy="{y + 60}" r="40" fill="#ffe066" stroke="#f5a623" stroke-width="8"/>')
        elif k == 1:
            out.append("".join(_crown(x, y + 100, 120, 80, "#4fb56c" if n % 2 else "#3f9e5c", "#2f8a4c") for n, x in enumerate(range(-560, 640, 160))))
        elif k == 2:
            out.append("".join(f'<rect x="{x - 9}" y="{y}" width="18" height="{H}" fill="#5a4630"/><ellipse cx="{x + 40}" cy="{y + 110}" rx="70" ry="26" fill="#57c078" transform="rotate(-20 {x + 40} {y + 110})"/>'
                               for x in (-420, -150, 120, 390)))
        else:
            out.append("".join(f'<ellipse cx="{x}" cy="{y + 140 + (n % 3) * 18}" rx="34" ry="13" fill="{("#a86a32", "#8a5a2c", "#c08a4a")[n % 3]}" transform="rotate({(n * 37) % 90 - 45} {x} {y + 140 + (n % 3) * 18})"/>'
                               for n, x in enumerate(range(-560, 600, 90))))
        out.append(f'</g><rect x="{x0}" y="{y}" width="{W}" height="{H}" fill="none" stroke="{INK}" stroke-width="10"/>')
        if numbers:
            out.append(f'<g id="{pid}-n{k}"><circle cx="{x0 - 90}" cy="{y + H / 2}" r="62" fill="#ffd23f" stroke="{INK}" stroke-width="10"/>'
                       f'<text x="{x0 - 90}" y="{y + H / 2 + 30}" text-anchor="middle" font-family="Baloo,sans-serif" font-weight="800" font-size="92" fill="{INK}">{4 - k}</text></g>')
        out.append('</g>')
    return f'<g id="{pid}">{"".join(out)}</g>'


def band_y(k): return -2 * 210 + k * 210 + 105      # the middle of band k of the layer tree (k = 0 at the top)


def leaf_roof(pid):
    """The sun above a roof of leaves, a few thin rays getting through and the dark below (the light board). The roof is -roof, the rays -r0..-r2."""
    rays = "".join(f'<path id="{pid}-r{k}" d="M{x} -120 L{x + 26} -120 L{x + 60} 360 L{x + 10} 360Z" fill="#fff6a0" opacity=".85"/>' for k, x in enumerate((-280, 40, 300)))
    roof = "".join(_crown(x, -150, 130, 80, "#3f9e5c" if n % 2 else "#4fb56c", "#2f8a4c") for n, x in enumerate(range(-520, 600, 150)))
    return (f'<g id="{pid}"><rect x="-620" y="-150" width="1240" height="560" fill="#24402e" rx="24"/>{rays}'
            f'<g id="{pid}-sun"><circle cx="0" cy="-400" r="90" fill="#ffe066" stroke="#f5a623" stroke-width="10"/>'
            + "".join(f'<path d="M0 -510 V-550" stroke="#f5a623" stroke-width="14" stroke-linecap="round" transform="rotate({a} 0 -400)"/>' for a in range(0, 360, 45))
            + f'</g><g id="{pid}-roof">{roof}</g>'
            f'<path d="M-620 330 C-200 300 200 340 620 320 L620 410 L-620 410Z" fill="#5a4128"/></g>')


def big_leaf(pid, col="#6fd06a"):
    """One big broad leaf on a stem (the understory board)."""
    return (f'<g id="{pid}"><path d="M0 300 C-6 200 -4 120 0 60" stroke="#3a7a3a" stroke-width="20" fill="none" stroke-linecap="round"/>'
            f'<path d="M0 80 C-220 40 -260 -220 0 -330 C260 -220 220 40 0 80Z" fill="{col}" stroke="#2a6a3c" stroke-width="12" stroke-linejoin="round"/>'
            f'<path d="M0 70 V-300 M0 -40 L-120 -110 M0 -40 L120 -110 M0 -150 L-100 -210 M0 -150 L100 -210" stroke="#2a6a3c" stroke-width="9" fill="none" stroke-linecap="round"/></g>')


def drop(pid, col="#58b9e8"):
    return f'<g id="{pid}"><path d="M0 -60 C24 -24 38 0 38 18 C38 42 20 58 0 58 C-20 58 -38 42 -38 18 C-38 0 -24 -24 0 -60Z" fill="{col}" stroke="#2f7fb0" stroke-width="7"/><ellipse cx="-12" cy="14" rx="9" ry="16" fill="#fff" opacity=".6"/></g>'


def tree_icon(pid, h, col="#4fb56c"):
    """A simple tree h tall (feet on y = 0): trunk and a round top (the tall-trees board)."""
    return (f'<g id="{pid}"><rect x="-22" y="{-h + 120}" width="44" height="{h - 120}" fill="#8a6238" stroke="{INK}" stroke-width="8"/>'
            f'<ellipse cx="0" cy="{-h + 90}" rx="120" ry="100" fill="{col}" stroke="{INK}" stroke-width="8"/></g>')


def ant(pid):
    """A small ant seen from the side (food for the anteater: drawn without a face)."""
    legs = "".join(f'<path d="M{x} -20 l{dx} 26" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>' for x, dx in ((-10, -18), (4, 0), (18, 16)))
    return (f'<g id="{pid}">{legs}<ellipse cx="-34" cy="-26" rx="26" ry="20" fill="#7a2a1a" stroke="{INK}" stroke-width="6"/>'
            f'<ellipse cx="4" cy="-26" rx="16" ry="13" fill="#7a2a1a" stroke="{INK}" stroke-width="6"/><circle cx="34" cy="-30" r="16" fill="#7a2a1a" stroke="{INK}" stroke-width="6"/>'
            f'<path d="M42 -44 q10 -18 22 -20" stroke="{INK}" stroke-width="5" fill="none" stroke-linecap="round"/></g>')


def nose_waves(pid):
    """Three little smell lines (sniff, sniff)."""
    return f'<g id="{pid}">' + "".join(f'<path d="M{x} 0 q16 -20 0 -40 q-16 -20 0 -40" stroke="#ffd23f" stroke-width="10" fill="none" stroke-linecap="round"/>' for x in (-40, 0, 40)) + '</g>'


def icon(fn, bg="#fff"):
    """An animal in a round picture (the guesses board and the everyone-has-a-home board)."""
    def f(pid): return (f'<g id="{pid}"><clipPath id="{pid}-cl"><circle r="115"/></clipPath><circle r="120" fill="{bg}"/><g clip-path="url(#{pid}-cl)">{fn(pid + "i")}</g>'
                        f'<circle r="120" fill="none" stroke="{INK}" stroke-width="10"/></g>')
    return f


def frog_icon(p): return f'<g transform="translate(0 80) scale(.62)">{frog(p)}</g>'
def eagle_icon(p): return f'<g transform="translate(0 112) scale(.36)">{eagle(p)}</g>'
def anteater_icon(p): return f'<g transform="translate(-40 70) scale(.34)">{anteater(p)}</g>'
def macaw_icon(p): return f'<g transform="translate(14 96) scale(.52)">{macaw(p)}</g>'
