"""Pictures for za_ep16 "Can Little Clover Lead the Sheep Home?" (Nov 27 2026). New places, kinds and props only: no character, place or older prop
is drawn differently (Clover is art2.lamb as it is; the big sheep are the same drawing with other colours and one small mark each, used at a bigger
scale; art2's "farm" is used as it is and once more under a sunset sky).

Places:
  "meadow"       the green meadow up the hill in the afternoon: rolling grass, a round tree, flowers, the red barn small and far away on the right.
  "meadow_gold"  the same meadow when the sun is low: a golden sky, a big orange sun near the hills.
  "lane"         the lane home at sunset: a sandy path along a fence, the barn closer on the right.
  "farm_gold"    art2's farm (barn, fence, fields) under the sunset sky.
  "barn"         inside the barn in the evening: plank walls, a window with the evening sky, a lantern, hay bales, straw on the floor.
Kinds (registered into art2.RIGS, kit.PT, kit.BOX; art2.lamb had no kit entries):
  "lamb" points and box; "sheep_mama" (Clover's colours, a blue collar with a gold bell), "sheep_woolly" (grey wool, dark grey face),
  "sheep_daisy" (cream, a daisy in her wool), "sheep_bramble" (brown face and legs).
Props:
  tuft(p)        a tuft of long grass with a clover flower (what the sheep munch). Anchored at its foot.
  dizzy(p)       three little stars on a ring (Clover is dizzy). Anchored at the ring's middle; #<p>-spin turns.
  hay(p)         a heap of fresh hay. Anchored at its foot.
  arrow(p)       a fat orange arrow pointing right. Anchored at its middle.
  sock(p)        one striped sock (the wrong answer's picture). Anchored at its middle.
"""
import art, art2, kit

INK = art.INK
GOLD = '<rect x="-700" y="-1100" width="3400" height="3400" fill="#ff9a3c" opacity=".13"/>'


# ------------------------------------------------------------------ kinds
def _sheep(pal, mark=""):
    c = dict(art2.LAMB, **pal)

    def build(p):
        s = art2.lamb(p, c)
        return s.replace(f'<g id="{p}-neck">', f'<g id="{p}-neck">' + mark.replace("{p}", p), 1) if mark and mark.startswith("<!--under-->") else \
            (s[:s.rindex("</g></g>")] + mark.replace("{p}", p) + "</g></g>" if mark else s)
    return build


BELL = ('<!--under--><path d="M150 -262 Q214 -222 286 -262" stroke="#2f7fd0" stroke-width="26" fill="none" stroke-linecap="round"/>'
        f'<circle cx="214" cy="-222" r="26" fill="#ffd23f" stroke="{INK}" stroke-width="7"/><circle cx="214" cy="-210" r="7" fill="{INK}"/>')
DAISY = ('<g transform="translate(206 -446)">' + "".join(f'<ellipse cx="0" cy="-20" rx="11" ry="18" fill="#ffffff" stroke="{INK}" stroke-width="4" transform="rotate({a})"/>' for a in range(0, 360, 60))
         + f'<circle r="12" fill="#ffd23f" stroke="{INK}" stroke-width="4"/></g>')
_Q = art2.RIGS["lamb"]
for _k, _pal, _mark in (("sheep_mama", {}, BELL),
                        ("sheep_woolly", {"wool": "#e3e1dc", "shade": "#c4c0b8", "face": "#8d8782", "leg": "#77716c", "far": "#625d59", "line": "#4a4541"}, ""),
                        ("sheep_daisy", {"wool": "#fff4dc", "shade": "#ecd9b4"}, DAISY),
                        ("sheep_bramble", {"face": "#a9805f", "leg": "#8a6548", "far": "#70523a", "line": "#5a4030"}, "")):
    art2.RIGS[_k] = dict(_Q, build=_sheep(_pal, _mark))
for _k in ("lamb", "sheep_mama", "sheep_woolly", "sheep_daisy", "sheep_bramble"):
    kit.PT[_k] = {"head": (222, -340), "eye": (232, -346), "body": (-10, -236), "top": (222, -470), "mouth": (290, -292), "feet": (0, 0), "all": (30, -240)}
    kit.BOX[_k] = (-260, 330, -470)


# ------------------------------------------------------------------ places
def _flowers(pts):
    return "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/><circle cx="{x}" cy="{y}" r="{r * .4:.0f}" fill="#ffd23f"/>' for x, y, r, c in pts)


def _blades(x, y, s=1.0, col="#5fae48"):
    return (f'<g transform="translate({x} {y}) scale({s})"><path d="M-22 0 Q-30 -40 -40 -58 M-8 0 Q-8 -50 -4 -76 M8 0 Q14 -44 28 -64 M20 0 Q30 -26 46 -36" '
            f'stroke="{col}" stroke-width="10" fill="none" stroke-linecap="round"/></g>')


def _tree(x, y, s=1.0):
    return (f'<g transform="translate({x} {y}) scale({s})"><rect x="-26" y="-230" width="52" height="240" rx="16" fill="#8a5a34"/>'
            '<circle cx="-90" cy="-300" r="110" fill="#4f9a3c"/><circle cx="80" cy="-310" r="120" fill="#5aaa46"/><circle cx="-10" cy="-400" r="130" fill="#66b850"/>'
            '<circle cx="-40" cy="-420" r="16" fill="#ff6b6b"/><circle cx="60" cy="-340" r="16" fill="#ff6b6b"/><circle cx="-110" cy="-300" r="16" fill="#ff6b6b"/></g>')


def _far_barn(x, y, s=1.0):
    return (f'<g transform="translate({x} {y}) scale({s})"><path d="M-190 0 V-210 L0 -340 L190 -210 V0Z" fill="#e2574c"/><path d="M-210 -200 L0 -350 L210 -200 L190 -186 L0 -322 L-190 -186Z" fill="#fff"/>'
            '<rect x="-60" y="-150" width="120" height="150" fill="#b83b34"/><path d="M-60 -150 L60 0 M60 -150 L-60 0" stroke="#fff" stroke-width="10"/><rect x="-36" y="-262" width="72" height="56" rx="8" fill="#fff"/></g>')


def _sky_day(p): return art._sky(p, "#8fd8ff", "#eaf8ff") + art._sun(p + "sun", 1560, 190, 84) + art._cloud(p + "c1", 520, 170) + art._cloud(p + "c2", 1140, 260, .7)


def _sky_gold(p, sun=(420, 560)):
    return (art._sky(p, "#ffb45e", "#ffe9a8") + f'<circle cx="{sun[0]}" cy="{sun[1]}" r="230" fill="#fff3c4" opacity=".45"/>' + art._sun(p + "sun", sun[0], sun[1], 120, "#ff8a3d")
            + art._cloud(p + "c1", 1100, 190, 1.0, "#ffd9c2", .9) + art._cloud(p + "c2", 1680, 300, .7, "#ffc9b0", .9))


def bg_meadow(p, gold=False):
    hills = ('<path d="M-500 660 C-100 520 300 600 700 560 S1500 500 2420 640 L2420 820 L-500 820Z" fill="#a8e08a"/>'
             '<path d="M-500 720 C100 640 600 700 1100 660 S1900 640 2420 700 L2420 860 L-500 860Z" fill="#96d67a"/>')
    far = (_sky_gold(p) if gold else _sky_day(p)) + hills + _far_barn(1660, 668, .34)
    mid = ('<path d="M-500 800 C200 730 700 780 1200 750 S2000 740 2420 790 L2420 920 L-500 920Z" fill="#8fd470"/>' + _tree(170, 800, .9)
           + _flowers(((560, 800, 9, "#fff"), (760, 790, 9, "#ff7aa2"), (1300, 790, 9, "#fff"), (1560, 800, 9, "#ffd23f"))))
    near = ('<rect x="-500" y="860" width="2920" height="1200" fill="#7cc95e"/><path d="M-500 862 C300 846 900 872 1500 852 S2200 866 2420 856 L2420 900 L-500 900Z" fill="#86d066"/>'
            + "".join(_blades(x, y, s) for x, y, s in ((90, 1010, 1.2), (470, 1040, 1.0), (1010, 1050, 1.1), (1530, 1040, 1.0), (1870, 1010, 1.2), (-200, 1030, 1.1), (2150, 1040, 1.1)))
            + _flowers(((300, 990, 11, "#fff"), (700, 1030, 11, "#ff7aa2"), (1260, 1010, 11, "#fff"), (1720, 1050, 11, "#ffd23f"), (40, 1060, 11, "#ff7aa2"))))
    return (far, mid + GOLD, near + GOLD) if gold else (far, mid, near)


def bg_lane(p):
    far = (_sky_gold(p, (300, 540)) + '<path d="M-500 680 C0 560 500 640 900 600 S1700 560 2420 660 L2420 820 L-500 820Z" fill="#a8e08a"/>' + _far_barn(1640, 730, .62))
    fence = ("".join(f'<rect x="{x}" y="716" width="18" height="100" rx="6" fill="#f2e6c8"/>' for x in range(-460, 1300, 130))
             + '<rect x="-480" y="736" width="1760" height="16" rx="6" fill="#f2e6c8"/><rect x="-480" y="778" width="1760" height="16" rx="6" fill="#f2e6c8"/>')
    mid = '<path d="M-500 790 C200 740 700 770 1200 750 S2000 740 2420 780 L2420 910 L-500 910Z" fill="#8fd470"/>' + fence
    near = ('<rect x="-500" y="860" width="2920" height="1200" fill="#7cc95e"/>'
            '<path d="M-500 900 C200 880 900 890 1500 876 S2200 850 2420 820 L2420 960 C1900 990 900 1000 -500 1010Z" fill="#e8cf96"/>'
            '<path d="M-500 906 C200 886 900 896 1500 882 S2200 856 2420 826" stroke="#d2b678" stroke-width="10" fill="none"/>'
            + "".join(_blades(x, y, s) for x, y, s in ((120, 1060, 1.1), (640, 1064, 1.0), (1240, 1056, 1.1), (1800, 1040, 1.0)))
            + _flowers(((380, 1050, 11, "#fff"), (900, 1066, 11, "#ff7aa2"), (1540, 1050, 11, "#fff"))))
    return far, mid + GOLD, near + GOLD


def bg_farm_gold(p):
    far, mid, near = art2.bg_farm(p)
    far = _sky_gold(p, (340, 520)) + '<path d="M-500 700 C0 580 500 640 900 610 S1700 580 2420 680 L2420 800 L-500 800Z" fill="#a8e08a"/>'
    return far, mid + GOLD, near + GOLD


def bg_barn(p):
    planks = "".join(f'<rect x="{x}" y="-900" width="150" height="1760" fill="{"#b9814f" if k % 2 else "#c18a57"}"/><rect x="{x}" y="-900" width="8" height="1760" fill="#9a6a3e"/>' for k, x in enumerate(range(-500, 2440, 150)))
    win = (f'<g transform="translate(1460 330)"><rect x="-170" y="-150" width="340" height="300" rx="24" fill="#ffb45e" stroke="#7a4f2a" stroke-width="26"/>'
           '<circle cx="60" cy="40" r="60" fill="#ff8a3d"/><path d="M-170 70 Q0 20 170 80 L170 150 L-170 150Z" fill="#8fd470"/>'
           '<path d="M0 -150 V150 M-170 0 H170" stroke="#7a4f2a" stroke-width="18"/></g>')
    lamp = (f'<g transform="translate(560 250)"><path d="M0 -330 V-90" stroke="#5a3a20" stroke-width="10"/><circle cx="0" cy="0" r="190" fill="#ffe9a8" opacity=".35"/>'
            f'<rect x="-50" y="-90" width="100" height="130" rx="22" fill="#ffd23f" stroke="{INK}" stroke-width="10"/><rect x="-62" y="-104" width="124" height="26" rx="10" fill="#5a3a20"/>'
            '<rect x="-62" y="34" width="124" height="22" rx="10" fill="#5a3a20"/><path d="M0 -50 q26 34 0 62 q-26 -28 0 -62Z" fill="#ff8a3d"/></g>')
    far = planks + '<rect x="-500" y="-60" width="2940" height="46" fill="#8a5a34"/>' + win + lamp
    bale = lambda x, y, s: (f'<g transform="translate({x} {y}) scale({s})"><rect x="-190" y="-220" width="380" height="220" rx="26" fill="#f0cf6a" stroke="#b08a2c" stroke-width="12"/>'
                            '<path d="M-190 -150 H190 M-190 -76 H190" stroke="#d9b24a" stroke-width="10"/><path d="M-70 -220 V0 M70 -220 V0" stroke="#b08a2c" stroke-width="12"/></g>')
    mid = '<rect x="-500" y="800" width="2940" height="120" fill="#9a6a3e"/>' + bale(1760, 850, 1.0) + bale(1700, 640, .8) + bale(40, 850, 1.0)
    near = ('<rect x="-500" y="860" width="2940" height="1200" fill="#f1d683"/><path d="M-500 862 C300 846 900 874 1500 852 S2200 866 2440 856 L2440 900 L-500 900Z" fill="#f6e09a"/>'
            + "".join(f'<path d="M{x} {y} l{dx} -16 M{x + 30} {y + 14} l{dx} -12" stroke="#d9b24a" stroke-width="8" stroke-linecap="round"/>'
                      for x, y, dx in ((60, 960, 70), (420, 1010, -60), (800, 980, 70), (1180, 1020, -64), (1560, 970, 70), (1900, 1020, -60), (240, 1060, 66), (1360, 1064, 60))))
    return far, mid, near


art.BG.update({"meadow": bg_meadow, "meadow_gold": lambda p: bg_meadow(p, True), "lane": bg_lane, "farm_gold": bg_farm_gold, "barn": bg_barn})
art.PLACE.update({"meadow": "the green meadow", "meadow_gold": "the meadow when the sun is low", "lane": "the lane home at sunset", "farm_gold": "the farm at sunset",
                  "barn": "inside the cosy barn"})


# ------------------------------------------------------------------ props
def tuft(p):
    return (f'<g id="{p}"><path d="M-40 0 Q-54 -70 -80 -110 M-16 0 Q-18 -90 -10 -140 M10 0 Q18 -84 40 -128 M34 0 Q52 -52 84 -76" stroke="{INK}" stroke-width="30" fill="none" stroke-linecap="round"/>'
            '<path d="M-40 0 Q-54 -70 -80 -110 M-16 0 Q-18 -90 -10 -140 M10 0 Q18 -84 40 -128 M34 0 Q52 -52 84 -76" stroke="#4fae4a" stroke-width="18" fill="none" stroke-linecap="round"/>'
            f'<circle cx="-10" cy="-150" r="24" fill="#ff8fc0" stroke="{INK}" stroke-width="7"/></g>')


def dizzy(p):
    star = lambda a: (f'<g transform="rotate({a}) translate(0 -110)"><path d="M0 -34 L10 -10 L36 -10 L15 6 L23 32 L0 16 L-23 32 L-15 6 L-36 -10 L-10 -10Z" fill="#ffd23f" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/></g>')
    return (f'<g id="{p}"><g transform="scale(1 .42)"><g id="{p}-spin"><circle r="110" fill="none" stroke="#ffffff" stroke-width="10" stroke-dasharray="26 22" opacity=".9"/>'
            f'{star(0)}{star(120)}{star(240)}</g></g></g>')


def hay(p):
    return (f'<g id="{p}"><path d="M-220 0 Q-200 -150 -60 -170 Q0 -230 80 -176 Q210 -150 220 0Z" fill="#f0cf6a" stroke="{INK}" stroke-width="10" stroke-linejoin="round"/>'
            '<path d="M-150 -40 q40 -50 90 -60 M-30 -60 q40 -60 100 -70 M60 -30 q40 -40 100 -40 M-90 -110 q30 -20 70 -20" stroke="#b08a2c" stroke-width="9" fill="none" stroke-linecap="round"/></g>')


def arrow(p):
    return (f'<g id="{p}"><path d="M-120 -30 H30 V-76 L130 0 L30 76 V30 H-120Z" fill="#ff8a3d" stroke="{INK}" stroke-width="12" stroke-linejoin="round"/></g>')


def sock(p):
    return (f'<g id="{p}"><path d="M-60 -170 H60 V40 Q60 80 110 96 Q170 116 150 160 Q130 190 40 180 Q-60 170 -60 80Z" fill="#ff7aa2" stroke="{INK}" stroke-width="12" stroke-linejoin="round"/>'
            '<path d="M-54 -120 H54 M-54 -70 H54 M-54 -20 H54" stroke="#ffffff" stroke-width="18"/><rect x="-66" y="-190" width="132" height="44" rx="14" fill="#ffffff" stroke="#402010" stroke-width="10"/></g>')
