"""Art for zc_ep14 "Whose Egg Is This? Guess With Milo" (Nov 27 2026): an ostrich (dad and mom), an ostrich chick, an emperor penguin (dad with
an egg on his feet under his brood pouch, mom with a chick), a penguin chick, a baby sea turtle (art2.turtle in hatchling colours), the eggs
(a big ostrich egg that can crack and open, small round sea turtle eggs, a penguin egg), the nests (a shallow scrape in the dirt, a hole in the
sand), a chicken egg and a ping-pong ball for the size boards, a day / night board.
The mama sea turtle is the existing Tula rig ("turtle", art2.py). Same hand as art.py / art2.py: flat fills, one warm dark outline round every
moving part. Nothing here changes an existing character, prop or place."""
import art, art2, kit
from art import eye, INK

OST_DAD = {"body": "#2e2a30", "shade": "#1c191e", "plume": "#fbf8f2", "plume2": "#e6e0d6", "skin": "#f2b7a6", "skin2": "#dd9a88", "line": "#2a1a14", "beak": "#f6c79a"}
OST_MOM = {"body": "#9a8774", "shade": "#7f6d5c", "plume": "#d9cbb8", "plume2": "#c4b4a0", "skin": "#e9c3a8", "skin2": "#d2a98e", "line": "#3d2a1c", "beak": "#f1cfa4"}
PEN = {"back": "#26303e", "back2": "#3a4658", "belly": "#fdfbf4", "belly2": "#e9e6dc", "gold": "#ffc94a", "gold2": "#ffe9a3", "beak": "#ff8a3d", "foot": "#4a4a52", "line": "#141a24"}
EGG_OST = ("#fbf1d8", "#e9d8b0")       # fill, shade (the drawing only: the episode says nothing about colour)
EGG_TUR = ("#fffdf6", "#e4ded0")
EGG_PEN = ("#f6f4ec", "#dcd8cc")


def _ol(shapes, ln, w=9): return f'<g fill="{ln}" stroke="{ln}" stroke-width="{w * 2}" stroke-linejoin="round" stroke-linecap="round">{shapes}</g>'


# ================================================================== ostrich (side view, facing right, feet at y = 0, about 1000 tall)
def ostrich(pid, c=OST_DAD, chick=False):
    """Parts: -neck (the long neck and the head: nods, looks; turns round 150 -560), -eye, -brow, -smile / -frown, -wing (the white wing plumes:
    it opens over the chicks), -tail, -fl (near leg), -fl2 (far leg)."""
    ln = c["line"]

    def leg(x, far, name):
        col = c["skin2"] if far else c["skin"]
        sh = (f'<path d="M{x - 34} -470 C{x - 40} -380 {x - 20} -320 {x - 8} -290 L{x + 8} -290 C{x + 26} -330 {x + 34} -400 {x + 30} -470Z"/>'
              f'<rect x="{x - 13}" y="-300" width="26" height="290" rx="12"/><path d="M{x - 18} -14 L{x + 70} -14 Q{x + 86} -6 {x + 70} 4 L{x - 22} 4Z"/>')
        return (f'<g id="{pid}-{name}">{_ol(sh, ln, 6)}<g fill="{col}">{sh}</g>'
                f'<path d="M{x - 10} -250 h20 M{x - 10} -200 h20 M{x - 10} -150 h20 M{x - 10} -100 h20" stroke="{c["skin2"] if not far else c["shade"]}" stroke-width="5" opacity=".7"/></g>')
    legs_far = leg(-30, True, "fl2"); legs_near = leg(40, False, "fl")
    body_d = "M-250 -560 C-250 -680 -60 -730 100 -680 C210 -640 250 -560 220 -480 C190 -410 60 -390 -60 -400 C-180 -410 -250 -470 -250 -560Z"
    body = _ol(f'<path d="{body_d}"/>', ln, 8) + f'<path d="{body_d}" fill="{c["body"]}"/><path d="M-230 -500 C-120 -420 80 -410 210 -470 C150 -400 -100 -390 -230 -500Z" fill="{c["shade"]}" opacity=".7"/>'
    tail_d = "M-240 -600 C-320 -640 -360 -600 -340 -560 C-370 -540 -350 -490 -300 -500 C-290 -470 -240 -480 -230 -520Z"
    tail = f'<g id="{pid}-tail">{_ol(f"<path d=\"{tail_d}\"/>", ln, 7)}<path d="{tail_d}" fill="{c["plume"]}"/><path d="M-330 -566 q30 6 60 -6 M-320 -530 q30 0 56 -10" stroke="{c["plume2"]}" stroke-width="8" fill="none" stroke-linecap="round"/></g>'
    wing_d = "M-150 -600 C-60 -660 90 -650 150 -590 C120 -540 40 -520 -40 -526 C-110 -530 -150 -560 -150 -600Z"
    wing = (f'<g id="{pid}-wing">{_ol(f"<path d=\"{wing_d}\"/>", ln, 7)}<path d="{wing_d}" fill="{c["plume"]}"/>'
            f'<path d="M-110 -570 q60 26 130 10 M-90 -545 q60 18 120 4 M-120 -600 q70 20 160 4" stroke="{c["plume2"]}" stroke-width="9" fill="none" stroke-linecap="round"/></g>')
    neck_d = "M120 -640 C150 -720 170 -820 190 -900 L232 -900 C222 -820 214 -730 196 -620Z"
    head_d = "M180 -930 C186 -985 262 -1000 290 -960 C306 -940 300 -906 270 -896 C240 -888 196 -890 180 -930Z"
    beak_d = "M276 -948 C320 -948 360 -936 372 -926 C360 -914 320 -906 276 -910Z"
    neck = (f'<g id="{pid}-neck">' + _ol(f'<path d="{neck_d}"/><path d="{head_d}"/><path d="{beak_d}"/>', ln, 7)
            + f'<path d="{neck_d}" fill="{c["skin"]}"/><path d="M196 -620 C214 -730 222 -820 232 -900 L222 -900 C206 -820 196 -720 176 -630Z" fill="{c["skin2"]}"/>'
            f'<path d="M110 -650 C130 -690 200 -690 216 -636 C190 -610 140 -612 110 -650Z" fill="{c["plume"]}"/>'
            f'<path d="{head_d}" fill="{c["skin"]}"/><path d="M190 -950 q30 -30 70 -24" stroke="{c["body"]}" stroke-width="10" fill="none" stroke-linecap="round" opacity=".5"/>'
            f'<path d="{beak_d}" fill="{c["beak"]}"/><path d="M280 -928 q44 4 88 0" stroke="{ln}" stroke-width="5" fill="none" stroke-linecap="round"/>'
            + art2._mouth(pid, 300, -918, 1, ln, 1).replace('stroke-width="1"', 'stroke-width="0"')
            + eye(f"{pid}-eye", 252, -946, 22, lashes=1, lid=c["skin"]) + art2._brow(pid, 252, -978, 34, ln, 6)
            + f'<ellipse cx="270" cy="-918" rx="12" ry="7" fill="#ff8fb1" opacity=".55"/></g>')
    sh = '<ellipse cx="10" cy="4" rx="230" ry="18" fill="#000" opacity=".13"/>'
    return f'<g id="{pid}">{sh}<g id="{pid}-all">{legs_far}{tail}{body}{wing}{legs_near}{neck}</g></g>'


def ostrich_chick(pid):
    """A fluffy ostrich chick, side view facing right, feet at y = 0 (about 300 tall): striped down, little wings. Parts: -neck, -eye, -brow,
    -smile / -frown, -wing, -fl, -fl2."""
    ln = "#4a3018"; fill = "#e8cfa0"; dark = "#b8925a"

    def leg(x, far, name):
        col = "#d9a98e" if far else "#f0c0a6"
        sh = f'<rect x="{x - 9}" y="-110" width="18" height="104" rx="8"/><path d="M{x - 12} -10 L{x + 36} -10 Q{x + 44} -4 {x + 36} 4 L{x - 14} 4Z"/>'
        return f'<g id="{pid}-{name}">{_ol(sh, ln, 5)}<g fill="{col}">{sh}</g></g>'
    body = (_ol('<ellipse cx="-10" cy="-150" rx="100" ry="70"/>', ln, 7) + f'<ellipse cx="-10" cy="-150" rx="100" ry="70" fill="{fill}"/>'
            + "".join(f'<path d="M{x} -205 q-8 50 4 110" stroke="{dark}" stroke-width="12" fill="none" stroke-linecap="round" opacity=".8"/>' for x in (-70, -30, 10))
            + f'<path d="M-100 -170 q-30 -20 -24 -50 q20 10 30 30" fill="{fill}" stroke="{ln}" stroke-width="6" stroke-linejoin="round"/>')
    wing = f'<g id="{pid}-wing"><path d="M-50 -170 q40 -30 80 0 q-30 30 -80 0Z" fill="{dark}" stroke="{ln}" stroke-width="6" stroke-linejoin="round"/></g>'
    neck_d = "M50 -190 C60 -230 70 -260 80 -280 L110 -280 C104 -250 100 -220 90 -180Z"
    head = '<circle cx="104" cy="-300" r="42"/><path d="M134 -312 C156 -312 174 -304 178 -298 C172 -290 154 -286 134 -288Z"/>'
    neck = (f'<g id="{pid}-neck">' + _ol(f'<path d="{neck_d}"/>{head}', ln, 6) + f'<path d="{neck_d}" fill="{fill}"/><g fill="{fill}">{head}</g>'
            f'<path d="M134 -312 C156 -312 174 -304 178 -298 C172 -290 154 -286 134 -288Z" fill="#f6c79a"/>'
            f'<path d="M82 -336 q10 -16 4 -30 M100 -340 q4 -16 -2 -30 M118 -336 q8 -14 6 -26" stroke="{dark}" stroke-width="7" fill="none" stroke-linecap="round"/>'
            f'<path d="M70 -290 q20 6 34 -4" stroke="{dark}" stroke-width="8" fill="none" stroke-linecap="round" opacity=".8"/>'
            + art2._mouth(pid, 150, -294, 1, ln, 1).replace('stroke-width="1"', 'stroke-width="0"')
            + eye(f"{pid}-eye", 112, -308, 17, lid=fill) + art2._brow(pid, 112, -334, 26, ln, 5)
            + '<ellipse cx="126" cy="-282" rx="9" ry="6" fill="#ff8fb1" opacity=".6"/></g>')
    sh = '<ellipse cx="0" cy="4" rx="110" ry="12" fill="#000" opacity=".13"/>'
    return f'<g id="{pid}">{sh}<g id="{pid}-all">{leg(-24, True, "fl2")}{body}{wing}{leg(16, False, "fl")}{neck}</g></g>'


# ================================================================== emperor penguin (side view facing right, feet at y = 0, about 700 tall)
def penguin(pid, c=PEN, egg=False, chick=False):
    """An emperor penguin standing up. Parts: -neck (head: nods, looks; round 60 -520), -eye, -brow, -smile / -frown, -ff (flipper), -fl / -fl2
    (feet), -pouch (the fold of feathered skin low on the belly, the brood pouch: it lifts a little to show what it keeps warm), -egg (an egg on
    the feet, under the pouch; egg=True), -chick (a chick's head peeking out of the pouch; chick=True). SeaWorld: the male "incubates a single
    egg on top of its feet under a loose fold of abdominal skin"."""
    ln = c["line"]
    feet = (f'<g id="{pid}-fl2"><path d="M-40 -18 L40 -18 Q60 -6 40 6 L-44 6Z" fill="{c["foot"]}" stroke="{ln}" stroke-width="7" stroke-linejoin="round"/></g>'
            f'<g id="{pid}-fl"><path d="M0 -14 L96 -14 Q118 -2 96 8 L-4 8Z" fill="{c["foot"]}" stroke="{ln}" stroke-width="7" stroke-linejoin="round"/></g>')
    body_d = "M-120 -60 C-190 -200 -170 -440 -60 -540 C20 -600 120 -560 140 -470 C170 -340 190 -170 120 -40 C60 10 -70 10 -120 -60Z"
    belly_d = "M20 -470 C110 -420 160 -260 140 -120 C126 -40 80 -10 20 -8 C60 -100 70 -300 20 -470Z"
    body = (_ol(f'<path d="{body_d}"/>', ln, 8) + f'<path d="{body_d}" fill="{c["back"]}"/>'
            f'<path d="M-40 -470 C70 -470 170 -300 150 -120 C140 -30 80 0 0 -2 C-80 -4 -110 -60 -110 -120 C-110 -260 -110 -420 -40 -470Z" fill="{c["belly"]}"/>'
            f'<path d="{belly_d}" fill="{c["belly2"]}" opacity=".6"/>'
            f'<path d="M-30 -470 C30 -480 90 -450 110 -400 C70 -420 20 -430 -30 -430Z" fill="{c["gold2"]}" opacity=".9"/>')
    egg_g = (f'<g id="{pid}-egg" opacity="{1 if egg else 0}"><ellipse cx="78" cy="-64" rx="54" ry="64" fill="{EGG_PEN[0]}" stroke="{ln}" stroke-width="7"/>'
             f'<path d="M40 -40 q38 32 80 0" stroke="{EGG_PEN[1]}" stroke-width="10" fill="none" stroke-linecap="round"/><ellipse cx="60" cy="-92" rx="10" ry="16" fill="#fff" opacity=".8"/></g>')
    chick_g = (f'<g id="{pid}-chick" opacity="{1 if chick else 0}"><g transform="translate(10 56)"><circle cx="70" cy="-120" r="58" fill="#b9bcc4" stroke="{ln}" stroke-width="7"/>'
               f'<path d="M24 -152 C34 -194 112 -194 124 -140 C104 -166 50 -168 24 -152Z" fill="#1d2430"/><path d="M36 -140 C46 -96 104 -92 118 -132 C104 -152 50 -154 36 -140Z" fill="#fff"/>'
               f'<circle cx="94" cy="-128" r="9" fill="#1d2430"/><circle cx="97" cy="-131" r="3" fill="#fff"/><path d="M118 -122 l20 6 l-20 5Z" fill="#2a2a2a"/></g></g>')
    pouch_d = "M-20 -200 C40 -220 120 -200 150 -150 C150 -126 120 -112 84 -114 C40 -118 0 -140 -20 -200Z"
    pouch = (f'<g id="{pid}-pouch">{_ol(f"<path d=\"{pouch_d}\"/>", ln, 6)}<path d="{pouch_d}" fill="{c["belly"]}"/>'
             f'<path d="M10 -170 q60 20 120 -10" stroke="{c["belly2"]}" stroke-width="9" fill="none" stroke-linecap="round"/></g>')
    ff_d = "M-60 -400 C-120 -360 -150 -240 -130 -160 C-110 -200 -70 -300 -30 -360Z"
    ff = f'<g id="{pid}-ff">{_ol(f"<path d=\"{ff_d}\"/>", ln, 7)}<path d="{ff_d}" fill="{c["back2"]}"/></g>'
    head_d = "M-50 -560 C-60 -660 60 -700 120 -640 C160 -600 150 -530 100 -500 C40 -470 -40 -490 -50 -560Z"
    beak_d = "M120 -600 C170 -600 214 -586 226 -574 C210 -566 170 -560 124 -566Z"
    neck = (f'<g id="{pid}-neck">' + _ol(f'<path d="{head_d}"/><path d="{beak_d}"/>', ln, 7) + f'<path d="{head_d}" fill="{c["back"]}"/>'
            f'<path d="M10 -540 C40 -560 70 -540 70 -500 C50 -480 20 -490 10 -540Z" fill="{c["gold"]}"/>'
            f'<path d="{beak_d}" fill="#1e2430"/><path d="M128 -580 C160 -578 190 -574 210 -572 C190 -568 160 -566 130 -568Z" fill="{c["beak"]}"/>'
            + art2._mouth(pid, 150, -568, 1, ln, 1).replace('stroke-width="1"', 'stroke-width="0"')
            + eye(f"{pid}-eye", 72, -606, 22, lid=c["back"]) + art2._brow(pid, 72, -638, 34, "#8a95a8", 6)
            + '<ellipse cx="100" cy="-560" rx="12" ry="7" fill="#ff8fb1" opacity=".5"/></g>')
    sh = '<ellipse cx="10" cy="4" rx="170" ry="16" fill="#000" opacity=".13"/>'
    return f'<g id="{pid}">{sh}<g id="{pid}-all">{feet}{body}{ff}{egg_g}{chick_g}{pouch}{neck}</g></g>'


def penguin_chick(pid):
    """A fluffy grey emperor penguin chick with a black cap and a white face, standing, facing right (about 320 tall). Parts: -neck, -eye,
    -brow, -smile / -frown, -ff."""
    ln = "#141a24"
    body_d = "M-90 -30 C-130 -120 -110 -220 -20 -240 C70 -250 110 -170 100 -90 C94 -30 60 0 0 0 C-40 0 -70 -10 -90 -30Z"
    body = _ol(f'<path d="{body_d}"/>', ln, 7) + f'<path d="{body_d}" fill="#b9bcc4"/><path d="M-80 -60 C-40 -10 50 -6 90 -60" stroke="#a3a7b0" stroke-width="14" fill="none" stroke-linecap="round"/>'
    ff = f'<g id="{pid}-ff"><path d="M-50 -170 C-90 -140 -100 -90 -90 -60 C-70 -90 -50 -130 -30 -150Z" fill="#a3a7b0" stroke="{ln}" stroke-width="6" stroke-linejoin="round"/></g>'
    head = ('<circle cx="10" cy="-290" r="80"/>')
    neck = (f'<g id="{pid}-neck">' + _ol(head, ln, 7) + f'<circle cx="10" cy="-290" r="80" fill="#1d2430"/>'
            f'<path d="M-40 -280 C-30 -220 70 -214 88 -270 C80 -300 50 -310 20 -300 C0 -320 -40 -310 -40 -280Z" fill="#fff"/>'
            f'<path d="M84 -286 l30 10 l-30 8Z" fill="#2a2a2a"/>'
            + art2._mouth(pid, 90, -276, 1, ln, 1).replace('stroke-width="1"', 'stroke-width="0"')
            + eye(f"{pid}-eye", 46, -282, 16, lid="#fff") + art2._brow(pid, 46, -306, 24, "#8a95a8", 5) + '</g>')
    feet = f'<path d="M-30 -8 L30 -8 Q44 0 30 6 L-34 6Z M10 -8 L66 -8 Q80 0 66 6 L6 6Z" fill="#4a4a52" stroke="{ln}" stroke-width="5" stroke-linejoin="round"/>'
    sh = '<ellipse cx="0" cy="4" rx="100" ry="12" fill="#000" opacity=".13"/>'
    return f'<g id="{pid}">{sh}<g id="{pid}-all">{feet}{body}{ff}{neck}</g></g>'


TUR_BABY = {"shell": "#4b5a46", "dark": "#2c3a2a", "skin": "#7c8a6e", "line": "#1d281b", "belly": "#e6dfc0"}

art2.RIGS["ostrich"] = dict(build=lambda p: ostrich(p), neck="150 -580", tail="-240 -560", ear=None, legs={"fl": 40, "fl2": -30}, hip=-420, jaw=("y", 4), eyes=["eye"], brows=["brow"])
art2.RIGS["ostrich_mom"] = dict(build=lambda p: ostrich(p, OST_MOM), neck="150 -580", tail="-240 -560", ear=None, legs={"fl": 40, "fl2": -30}, hip=-420, jaw=("y", 4), eyes=["eye"], brows=["brow"])
art2.RIGS["ostrich_chick"] = dict(build=lambda p: ostrich_chick(p), neck="70 -190", tail=None, ear=None, legs={"fl": 16, "fl2": -24}, hip=-110, jaw=("y", 3), eyes=["eye"], brows=["brow"])
art2.RIGS["penguin"] = dict(build=lambda p: penguin(p), neck="40 -500", tail=None, ear=None, legs=None, hip=0, jaw=("y", 3), eyes=["eye"], brows=["brow"])
art2.RIGS["penguin_egg"] = dict(build=lambda p: penguin(p, egg=True), neck="40 -500", tail=None, ear=None, legs=None, hip=0, jaw=("y", 3), eyes=["eye"], brows=["brow"])
art2.RIGS["penguin_chick_pouch"] = dict(build=lambda p: penguin(p, chick=True), neck="40 -500", tail=None, ear=None, legs=None, hip=0, jaw=("y", 3), eyes=["eye"], brows=["brow"])
art2.RIGS["penguin_chick"] = dict(build=lambda p: penguin_chick(p), neck="10 -230", tail=None, ear=None, legs=None, hip=0, jaw=("y", 3), eyes=["eye"], brows=["brow"])
art2.RIGS["turtle_baby"] = dict(build=lambda p: art2.turtle(p, TUR_BABY), neck="180 -170", tail=None, ear=None, legs=None, hip=0, jaw=("y", 9), eyes=["eye"], brows=["brow"])

kit.PT["ostrich"] = {"head": (250, -940), "eye": (252, -946), "neck": (190, -760), "body": (-20, -560), "top": (250, -1000), "wing": (0, -590), "legs": (10, -200),
                     "feet": (0, 0), "all": (40, -500)}
kit.PT["ostrich_mom"] = kit.PT["ostrich"]
kit.BOX["ostrich"] = (-370, 380, -1010); kit.BOX["ostrich_mom"] = kit.BOX["ostrich"]
kit.PT["ostrich_chick"] = {"head": (104, -300), "eye": (112, -308), "body": (-10, -150), "top": (104, -360), "feet": (0, 0), "all": (30, -180)}
kit.BOX["ostrich_chick"] = (-130, 180, -370)
_PP = {"head": (60, -590), "eye": (72, -606), "body": (0, -300), "top": (60, -690), "belly": (60, -200), "pouch": (60, -150), "feet": (30, 0), "all": (20, -340)}
for _k in ("penguin", "penguin_egg", "penguin_chick_pouch"): kit.PT[_k] = _PP; kit.BOX[_k] = (-180, 230, -700)
kit.PT["penguin_chick"] = {"head": (10, -290), "eye": (46, -282), "body": (0, -120), "top": (10, -370), "feet": (0, 0), "all": (0, -180)}
kit.BOX["penguin_chick"] = (-130, 120, -370)
kit.PT["turtle_baby"] = {"head": (258, -182), "eye": (272, -186), "body": (0, -200), "top": (0, -350), "feet": (0, 0), "all": (60, -170)}
kit.BOX["turtle_baby"] = (-260, 350, -360)


# ================================================================== eggs and nests (props: drawn IN FRONT of the actors)
def big_egg(pid, w=300, h=380, col=EGG_OST, crack=True):
    """One egg standing up, bottom at y = 0. Parts: -whole (the egg in one piece, shown until it hatches), -top (the top of the shell above the zigzag: it lifts off when the egg hatches), -bot,
    -crack (a crack line, hidden until shown: ("to", at, "#{p}NAME-crack", {"opacity": 1})). The wobble is done on NAME_w by the episode."""
    a, b = w / 2, h / 2; cy = -b
    zig = " ".join(f"L{-a + k * w / 8:.0f} {cy - 10 + (24 if k % 2 else -18):.0f}" for k in range(9))
    clip_top = f'M{-a - 20} {cy - b - 20} L{a + 20} {cy - b - 20} L{a + 20} {cy - 28} ' + " ".join(f"L{a - k * w / 8:.0f} {cy - 10 + (24 if (8 - k) % 2 else -18):.0f}" for k in range(9)) + f' L{-a - 20} {cy - 28}Z'
    clip_bot = f'M{-a - 20} {cy - 28} {zig} L{a + 20} {cy - 28} L{a + 20} 20 L{-a - 20} 20Z'
    shape = f'<path d="M0 {-h} C{a * 1.15:.0f} {-h} {a * 1.05:.0f} 0 0 0 C{-a * 1.05:.0f} 0 {-a * 1.15:.0f} {-h} 0 {-h}Z"/>'
    full = (_ol(shape, INK, 6) + f'<g fill="{col[0]}">{shape}</g>'
            f'<path d="M{-a * .7:.0f} {-h * .25:.0f} C{-a * .3:.0f} {-h * .02:.0f} {a * .4:.0f} {-h * .03:.0f} {a * .75:.0f} {-h * .3:.0f}" stroke="{col[1]}" stroke-width="{w * .08:.0f}" fill="none" stroke-linecap="round"/>'
            f'<ellipse cx="{-a * .4:.0f}" cy="{-h * .68:.0f}" rx="{w * .07:.0f}" ry="{h * .11:.0f}" fill="#fff" opacity=".85" transform="rotate(18 {-a * .4:.0f} {-h * .68:.0f})"/>')
    crk = (f'<g id="{pid}-crack" opacity="0"><path d="M{-a * .55:.0f} {cy - 16:.0f} l{w * .12:.0f} {28} l{w * .1:.0f} {-34} l{w * .12:.0f} {30} l{w * .1:.0f} {-26}" stroke="{INK}" stroke-width="{max(5, w * .022):.0f}" fill="none" stroke-linejoin="round" stroke-linecap="round"/></g>') if crack else ""
    if not crack: return f'<g id="{pid}">{full}</g>'
    return (f'<g id="{pid}"><defs><clipPath id="{pid}-ct"><path d="{clip_top}"/></clipPath><clipPath id="{pid}-cb"><path d="{clip_bot}"/></clipPath></defs>'
            f'<g id="{pid}-whole">{full}</g><g id="{pid}-bot" opacity="0"><g clip-path="url(#{pid}-cb)">{full}</g></g><g id="{pid}-top" opacity="0"><g clip-path="url(#{pid}-ct)">{full}</g></g>{crk}</g>')


def small_egg(x, y, r=40, col=EGG_TUR):
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="{col[0]}" stroke="{INK}" stroke-width="6"/><path d="M{x - r * .6:.0f} {y + r * .3:.0f} q{r * .6:.0f} {r * .45:.0f} {r * 1.2:.0f} 0" stroke="{col[1]}" stroke-width="{r * .2:.0f}" fill="none" stroke-linecap="round"/>'
            f'<ellipse cx="{x - r * .35:.0f}" cy="{y - r * .35:.0f}" rx="{r * .18:.0f}" ry="{r * .26:.0f}" fill="#fff" opacity=".9"/>')


def scrape_back(pid, w=760):
    """The back of a shallow scrape in the dirt (the ostrich nest), drawn behind the egg; base at y = 0."""
    return (f'<g id="{pid}"><ellipse cx="0" cy="-10" rx="{w / 2}" ry="{w * .11:.0f}" fill="#a77a44"/><ellipse cx="0" cy="-4" rx="{w * .44:.0f}" ry="{w * .08:.0f}" fill="#8e6436"/></g>')


def scrape_front(pid, w=760):
    """The front lip of the scrape: a low bank of dirt with pebbles, in front of the egg's bottom, tapering into the ground at both ends (no hard
    edge in a tall 9:16 view); base at y = 0."""
    L, R = -w / 2 - 300, w / 2 + 300
    return (f'<g id="{pid}"><path d="M{L} 60 Q{-w / 2 - 60} -10 {-w / 2} -8 C{-w * .3:.0f} {-w * .08:.0f} {w * .3:.0f} {-w * .08:.0f} {w / 2} -8 Q{w / 2 + 60} -10 {R} 60 Q0 110 {L} 60Z" fill="#c99a5a"/>'
            f'<path d="M{-w / 2 - 50} -4 C{-w * .3:.0f} {-w * .075:.0f} {w * .3:.0f} {-w * .075:.0f} {w / 2 + 50} -4" stroke="#b5844a" stroke-width="12" fill="none" stroke-linecap="round"/>'
            + "".join(f'<ellipse cx="{x * w:.0f}" cy="{y}" rx="{r}" ry="{r * .6:.0f}" fill="#9c8a74" stroke="#00000022" stroke-width="4"/>' for x, y, r in ((-.38, 20, 22), (-.12, 34, 16), (.2, 28, 20), (.42, 16, 14))) + '</g>')


def turtle_nest(pid, w=820, n=17, covered=False):
    """A hole in the sand full of small round eggs (the eggs are a group -eggs); the front sand lip in front; base at y = 0. A sand heap
    -cover (hidden unless covered) covers the eggs."""
    import random
    r = random.Random(4); eggs = []
    rows = ((-150, 6), (-95, 6), (-40, 5))
    k = 0
    for y, m in rows:
        for j in range(m):
            if k >= n: break
            x = (j - (m - 1) / 2) * 76 + r.uniform(-6, 6); eggs.append(small_egg(round(x), y + r.randint(-6, 6), 38)); k += 1
    hole = f'<ellipse cx="0" cy="-90" rx="{w / 2 - 40}" ry="120" fill="#c79a52"/><ellipse cx="0" cy="-70" rx="{w / 2 - 70}" ry="96" fill="#b0843f"/>'
    L, R = -w / 2 - 340, w / 2 + 340
    lip = (f'<path d="M{L} 70 Q{-w / 2 - 80} -44 {-w / 2 + 20} -36 C{-w * .3:.0f} 10 {w * .3:.0f} 10 {w / 2 - 20} -36 Q{w / 2 + 80} -44 {R} 70 Q0 120 {L} 70Z" fill="#f2d48c"/>'
           f'<path d="M{-w / 2 - 70} -36 C{-w * .3:.0f} 12 {w * .3:.0f} 12 {w / 2 + 70} -36" stroke="#e0bd6e" stroke-width="12" fill="none" stroke-linecap="round"/>')
    cover = f'<g id="{pid}-cover" opacity="{1 if covered else 0}"><path d="M{-w / 2 + 10} -30 C{-w * .32:.0f} -340 {w * .32:.0f} -340 {w / 2 - 10} -30Z" fill="#f2d48c"/><path d="M{-w * .3:.0f} -170 q{w * .3:.0f} -70 {w * .6:.0f} 0" stroke="#e0bd6e" stroke-width="10" fill="none" stroke-linecap="round"/></g>'
    return f'<g id="{pid}">{hole}<g id="{pid}-eggs">{"".join(eggs)}</g>{lip}{cover}</g>'


def egg_trio_turtle(pid):
    """Three small round eggs in a little sand pile (the turtle clue on the game board), base y = 0."""
    return (f'<g id="{pid}"><ellipse cx="0" cy="-20" rx="230" ry="60" fill="#c79a52"/>' + small_egg(-80, -60, 46) + small_egg(10, -78, 46) + small_egg(90, -54, 46)
            + '<path d="M-300 400 L-300 -10 C-150 30 150 30 300 -10 L300 400Z" fill="#f2d48c"/></g>')


def ice_floor(pid, w=1200):
    """A patch of blue-white ice in front (the penguin egg sits on feet above it); base y = 0, solid 500 down."""
    return f'<g id="{pid}"><path d="M{-w / 2} 500 L{-w / 2} -10 C{-w * .2:.0f} -40 {w * .2:.0f} -30 {w / 2} -10 L{w / 2} 500Z" fill="#eaf6ff"/><path d="M{-w * .4:.0f} 30 l120 -10 M{w * .1:.0f} 50 l160 -14" stroke="#bfe0f4" stroke-width="10" stroke-linecap="round"/></g>'


def chicken_egg(pid, s=1.0):
    return big_egg(pid, 90 * s, 116 * s, ("#f7e6cf", "#e2c9a6"), crack=False)


def egg_grid(pid, cols=6, rows=4, gap=96):
    """24 small chicken eggs in rows (each its own -e<k> group, so they can pop in one by one); centred at 0 0."""
    out = []
    for k in range(cols * rows):
        cx = (k % cols - (cols - 1) / 2) * gap; cy = (k // cols - (rows - 1) / 2) * gap * 1.18 + 56
        out.append(f'<g id="{pid}-e{k}" transform="translate({cx:.0f} {cy:.0f})">{big_egg(f"{pid}-x{k}", 80, 104, ("#f7e6cf", "#e2c9a6"), crack=False)}</g>')
    return f'<g id="{pid}">{"".join(out)}</g>'


def pingpong(pid):
    """A white ping-pong ball (round, a little seam)."""
    return (f'<g id="{pid}"><circle r="60" fill="#ffffff" stroke="{INK}" stroke-width="7"/><path d="M-50 -20 q50 30 100 0" stroke="#d8d8d8" stroke-width="6" fill="none"/>'
            f'<ellipse cx="-22" cy="-24" rx="12" ry="16" fill="#eef4ff"/></g>')


def day_night(pid):
    """Two cards side by side: a sunny day (left) and a starry night (right), each with a dirt scrape and a big egg, centred at 0 0 (1400 wide).
    Parts -day, -night (the card), -mom (the mom ostrich sitting in the day card), -dad (the dad sitting at night)."""
    def card(x, sky, deco, sitter, name):
        return (f'<g id="{pid}-{name}" transform="translate({x} 0)"><rect x="-330" y="-300" width="660" height="600" rx="50" fill="{sky}" stroke="{INK}" stroke-width="12"/>'
                f'{deco}<rect x="-318" y="110" width="636" height="178" rx="0" fill="#c99a5a"/><path d="M-318 110 h636" stroke="#b5844a" stroke-width="10"/>{sitter}</g>')
    sun = '<circle cx="200" cy="-180" r="70" fill="#ffd23f" stroke="#f4a52a" stroke-width="10"/>' + "".join(f'<path d="M{200 + 100 * __import__("math").cos(a / 8 * 6.283):.0f} {-180 + 100 * __import__("math").sin(a / 8 * 6.283):.0f} l{22 * __import__("math").cos(a / 8 * 6.283):.0f} {22 * __import__("math").sin(a / 8 * 6.283):.0f}" stroke="#f4a52a" stroke-width="12" stroke-linecap="round"/>' for a in range(8))
    moon = '<path d="M230 -230 a80 80 0 1 0 0 120 a60 60 0 1 1 0 -120Z" fill="#fff4c2" stroke="#e8d07a" stroke-width="8"/>' + "".join(f'<circle cx="{x}" cy="{y}" r="7" fill="#fff8d6"/>' for x, y in ((-220, -200), (-120, -240), (-30, -170), (60, -230), (-200, -90)))
    sit = lambda c, nm: (f'<g id="{pid}-{nm}" transform="translate(-10 150) scale(.42)"><ellipse cx="0" cy="-160" rx="300" ry="180" fill="{c["body"]}" stroke="{INK}" stroke-width="14"/>'
                         f'<path d="M-150 -200 C-60 -260 90 -250 150 -190 C120 -140 40 -120 -40 -126 C-110 -130 -150 -160 -150 -200Z" fill="{c["plume"]}" stroke="{INK}" stroke-width="12"/>'
                         f'<path d="M180 -260 C200 -360 210 -460 220 -560 L262 -560 C256 -460 250 -360 232 -240Z" fill="{c["skin"]}" stroke="{INK}" stroke-width="12"/>'
                         f'<path d="M210 -590 C216 -645 292 -660 320 -620 C336 -600 330 -566 300 -556 C270 -548 226 -550 210 -590Z" fill="{c["skin"]}" stroke="{INK}" stroke-width="12"/>'
                         f'<path d="M306 -608 C350 -608 390 -596 402 -586 C390 -574 350 -566 306 -570Z" fill="{c["beak"]}" stroke="{INK}" stroke-width="10"/>'
                         f'<circle cx="282" cy="-606" r="20" fill="#fff"/><circle cx="286" cy="-604" r="12" fill="#1a1a2e"/></g>')
    return (f'<g id="{pid}">' + card(-370, "#9fdcff", sun, sit(OST_MOM, "mom"), "day") + card(370, "#1f2f72", moon, sit(OST_DAD, "dad"), "night") + '</g>')


def baby_hello(pid):
    """Little hearts that pop up round a family (the babies are safe with their family)."""
    return f'<g id="{pid}">' + "".join(f'<g transform="translate({x} {y}) scale({s})">{art2.heart(f"{pid}-h{k}")}</g>' for k, (x, y, s) in enumerate(((-120, 0, 1.0), (0, -70, .8), (120, 0, .9)))) + '</g>'


def sea_line(pid, w=2600):
    """A wet band of shiny sand and a little white wave edge at the front (the sea is close), base y = 0."""
    return f'<g id="{pid}"><path d="M{-w / 2} 600 L{-w / 2} 0 C{-w * .2:.0f} -30 {w * .2:.0f} 20 {w / 2} -10 L{w / 2} 600Z" fill="#e6c27a"/></g>'


# thumbnail pieces
def thumb_egg(pid):
    """The thumbnail's one big egg with a crack (crack visible)."""
    return big_egg(pid, 300, 380, EGG_OST, crack=True).replace(f'id="{pid}-crack" opacity="0"', f'id="{pid}-crack" opacity="1"')


# ================================================================== the beach at night (the hatchlings come out mostly at night: NSU)
import art_za_ep13 as _A13, art_za_ep14 as _A14
def bg_shore_night(p):
    far, mid, near = _A13._shore(p)
    return far + _A14.TINT + _A14.TINT + _A14._stars(p, 70, 5, 420) + _A14._moon(1620, 150), mid + _A14.TINT + _A14.TINT, near + _A14.TINT
art.BG["shore_night"] = bg_shore_night
art.PLACE["shore_night"] = "the beach at night"


def plain_dirt(pid, w=420):
    """A low oval of dirt (the ostrich egg's spot on the game board)."""
    return f'<g id="{pid}"><ellipse cx="0" cy="0" rx="{w / 2}" ry="{w * .12:.0f}" fill="#a77a44"/><ellipse cx="0" cy="4" rx="{w * .42:.0f}" ry="{w * .08:.0f}" fill="#8e6436"/></g>'


def plain_ice(pid, w=360):
    return f'<g id="{pid}"><ellipse cx="0" cy="0" rx="{w / 2}" ry="{w * .12:.0f}" fill="#d6ecfa" stroke="#a9d2ee" stroke-width="8"/></g>'


def sand_pile_eggs(pid):
    """Three small round eggs in a little hollow of sand (the turtle clue on the game board), no hard edges; base y = 0."""
    return (f'<g id="{pid}"><ellipse cx="0" cy="-10" rx="250" ry="62" fill="#e9c77e"/><ellipse cx="0" cy="-16" rx="200" ry="46" fill="#c79a52"/>' + small_egg(-80, -50, 46) + small_egg(10, -68, 46) + small_egg(90, -44, 46)
            + '<path d="M-250 -10 C-150 40 150 40 250 -10 C200 60 -200 60 -250 -10Z" fill="#f2d48c"/></g>')


def finger_down(pid):
    """A child's fingertip pointing down (it presses the soft egg)."""
    import art_zc_ep09 as _A9
    return f'<g id="{pid}"><g transform="rotate(180)">{_A9.fingertip(pid + "-f")}</g></g>'
