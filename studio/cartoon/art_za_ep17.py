"""Pictures for za_ep17 "How Does Hazel Find Snacks at Night?" (Nov 27 2026). New places, kit points and props only: no character, place or older prop
is drawn differently (Hazel is art2.hedgehog as it is; art2's "nightforest" is used as it is).

Places (actors stand at y 930-950 like every place; every night place is bright enough to read faces):
  "dusk_wood"   the edge of the wood at dusk: a violet sky, the moon coming up, a round bush with Hazel's leaf nest under it.
  "leafwood"    a path in the night wood carpeted with orange and brown fallen leaves (the crunchy leaves).
  "darkwood"    deep under the tall trees: thick trunks, glowing mushrooms, only a little moonlight (too dark for Milo's eyes).
  "logglade"    a moonlit clearing with ferns (the big log is a PROP, so it is drawn in front of Hazel when she snuffles under it).
  "dawn_wood"   the same edge of the wood at dawn: a pink and orange sky, the sun peeping up, Hazel's leaf nest under the bush.
Kind points: kit.PT / kit.BOX for "hedgehog" (art2 had none).
Props:
  sniff(p)      three wavy smell lines rising from the ground toward a nose. Anchored at their foot. #<p>-l1..l3 wave.
  crunch(p)     a burst of little zigzag "crunch" marks round a leaf. Anchored at the middle.
  leafpile(p)   a heap of dry autumn leaves. Anchored at its foot.
  biglog(p)     a big fallen log lying on two stones, a dark gap under it. Anchored at the middle of its foot; about 900 wide, 330 tall.
  berries(p)    a cluster of shiny blackberries on a leaf. Anchored at its foot.
  worm(p), caterpillar(p)   small and friendly (no faces that look scared), for the food board. Anchored at the middle of their foot.
  skycard(p, night)         a round picture card: a day sky with the sun, or a night sky with the moon and stars. Anchored at its middle.
  hog_lids(p)   Hazel's shut eye in hedgehog units: put it at Hazel's feet with Hazel's scale (unflipped). The idle blink would reopen the rig's own lid.
  zzz(p)        three "z" letters rising. Anchored at the bottom one.
  bigmoon(p)    a big round moon for a board. Anchored at its middle.
"""
import math, random
import art, art2, kit
from art import INK

kit.PT["hedgehog"] = {"head": (200, -130), "eye": (170, -140), "nose": (288, -80), "mouth": (236, -66), "body": (0, -120), "top": (60, -280),
                      "feet": (0, 0), "all": (30, -140)}
kit.BOX["hedgehog"] = (-250, 310, -285)

NIGHT_TINT = '<rect x="-700" y="-1100" width="3400" height="3400" fill="#1a2766" opacity=".22"/>'


def _stars(seed=17, n=40, y1=560):
    r = random.Random(seed)
    return "".join(f'<circle cx="{r.uniform(-400, 2300):.0f}" cy="{r.uniform(-700, y1):.0f}" r="{r.choice((3, 4, 5))}" fill="#fff8d6" opacity="{r.uniform(.5, 1):.2f}"/>' for _ in range(n))


def _moon(x, y, r=92):
    return (f'<circle cx="{x}" cy="{y}" r="{r * 1.6:.0f}" fill="#fff6c9" opacity=".16"/><circle cx="{x}" cy="{y}" r="{r}" fill="#fff6c9"/>'
            f'<circle cx="{x - r * .28:.0f}" cy="{y - r * .22:.0f}" r="{r * .17:.0f}" fill="#efe2a8"/><circle cx="{x + r * .32:.0f}" cy="{y + r * .3:.0f}" r="{r * .12:.0f}" fill="#efe2a8"/>')


def _pine(x, y, s=1.0, c1="#2f6a6a", c2="#3a7f7a", trunk="#4a3a5a"):
    return (f'<g transform="translate({x} {y}) scale({s})"><rect x="-18" y="-120" width="36" height="120" fill="{trunk}"/>'
            f'<path d="M-130 -100 L0 -420 L130 -100Z" fill="{c1}"/><path d="M-100 -240 L0 -500 L100 -240Z" fill="{c2}"/></g>')


def _bush(x, y, s=1.0, c=("#3f7f62", "#4c9472", "#5aa680")):
    return (f'<g transform="translate({x} {y}) scale({s})"><circle cx="-130" cy="-110" r="120" fill="{c[0]}"/><circle cx="130" cy="-110" r="120" fill="{c[0]}"/>'
            f'<circle cx="0" cy="-170" r="150" fill="{c[1]}"/><circle cx="-60" cy="-220" r="70" fill="{c[2]}"/><circle cx="80" cy="-200" r="56" fill="{c[2]}"/></g>')


def _nest(x, y, s=1.0):
    """Hazel's leaf nest: a loose heap of many separate autumn leaves (no solid dome: a solid brown dome read as a turtle shell in round 1 of the stills)
    with a round dark doorway at the front. In the ground layer, behind the actors."""
    r = random.Random(7); cols = ("#c9703a", "#e08b3c", "#b85a2e", "#d9a043", "#e6b04a")
    lv = []
    for k in range(70):
        t = k / 70; yy = -8 - t * 150 + r.uniform(-8, 8); half = 210 * (1 - t ** 1.6) + 20; xx = r.uniform(-half, half)
        if abs(xx) < 66 and yy > -60: continue                          # keep the doorway clear
        a = r.uniform(-70, 70); c = r.choice(cols)
        lv.append(f'<g transform="translate({xx:.0f} {yy:.0f}) rotate({a:.0f})"><ellipse rx="40" ry="17" fill="{c}" stroke="#5a3418" stroke-width="5"/>'
                  f'<path d="M-34 0 H34" stroke="#7a4a22" stroke-width="4"/></g>')
    door = '<path d="M-62 0 C-62 -84 62 -84 62 0Z" fill="#3a2418" stroke="#5a3418" stroke-width="6"/>'
    return f'<g transform="translate({x} {y}) scale({s})"><ellipse cx="0" cy="0" rx="230" ry="18" fill="#000" opacity=".15"/>{"".join(lv[:40])}{door}{"".join(lv[40:])}</g>'


def _fern(x, y, s=1.0, col="#3f8f6a"):
    leaves = "".join(f'<path d="M0 {-k * 34} q{side * 60} -20 {side * 90} 10" stroke="{col}" stroke-width="14" fill="none" stroke-linecap="round"/>' for k in range(1, 7) for side in (-1, 1))
    return f'<g transform="translate({x} {y}) scale({s})"><path d="M0 0 Q-10 -120 10 -240" stroke="{col}" stroke-width="12" fill="none"/>{leaves}</g>'


def _mush(x, y, s=1.0, cap="#7fe0ff"):
    return (f'<g transform="translate({x} {y}) scale({s})"><circle cx="0" cy="-60" r="70" fill="{cap}" opacity=".18"/><rect x="-12" y="-50" width="24" height="50" rx="10" fill="#f2ead2"/>'
            f'<path d="M-46 -46 Q0 -100 46 -46Z" fill="{cap}"/><circle cx="-14" cy="-62" r="6" fill="#ffffff" opacity=".8"/><circle cx="14" cy="-56" r="5" fill="#ffffff" opacity=".8"/></g>')


def _flies(pts):
    return "".join(f'<circle cx="{x}" cy="{y}" r="16" fill="#ffe98a" opacity=".25"/><circle cx="{x}" cy="{y}" r="6" fill="#ffe98a"/>' for x, y in pts)


def _leaves_ground(seed, y0=900, y1=1120, n=70):
    r = random.Random(seed); cols = ("#c9703a", "#e08b3c", "#b85a2e", "#d9a043", "#a8642f")
    return "".join(f'<ellipse cx="{r.uniform(-450, 2350):.0f}" cy="{r.uniform(y0, y1):.0f}" rx="{r.choice((22, 26, 30))}" ry="12" fill="{r.choice(cols)}" '
                   f'transform="rotate({r.uniform(-60, 60):.0f} 0 0)" opacity=".95"/>' for _ in range(0)) + \
        "".join((lambda x, y, a, c: f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="28" ry="12" fill="{c}" transform="rotate({a:.0f} {x:.0f} {y:.0f})"/>')(
            r.uniform(-450, 2350), r.uniform(y0, y1), r.uniform(-60, 60), r.choice(cols)) for _ in range(n))


def bg_dusk_wood(p, dawn=False):
    if dawn:
        sky = (art._sky(p, "#ff9fb8", "#ffe2a6") + f'<circle cx="1500" cy="700" r="260" fill="#fff3c4" opacity=".45"/>' + art._sun(p + "sun", 1500, 700, 110, "#ffb84d")
               + art._cloud(p + "c1", 700, 220, .9, "#ffd9e2", .9) + art._cloud(p + "c2", 1200, 320, .6, "#ffe6cf", .9))
    else:
        sky = art._sky(p, "#2e3f8f", "#8a78c8") + _stars(17, 30, 420) + _moon(1560, 300, 96)
    hills = '<path d="M-500 700 C0 600 500 660 900 630 S1700 600 2420 690 L2420 820 L-500 820Z" fill="%s"/>' % ("#9ccf8a" if dawn else "#4d6f9a")
    far = sky + hills + "".join(_pine(x, 780, s, *(("#5e9f78", "#6fb388", "#7a5a4a") if dawn else ())) for x, s in ((960, .7), (1140, .85), (2000, .8)))
    mid = ('<path d="M-500 800 C200 740 700 770 1200 750 S2000 740 2420 780 L2420 910 L-500 910Z" fill="%s"/>' % ("#86c870" if dawn else "#3f6f86")
           + _bush(330, 860, 1.25, ("#4f9a62", "#5caf74", "#6cc283") if dawn else ("#2f6a5a", "#3a7f6a", "#479277")) + _nest(330, 905, 1.0))
    near = ('<rect x="-500" y="860" width="2920" height="1200" fill="%s"/>' % ("#7cc95e" if dawn else "#4d7f8f")
            + _fern(1700, 1000, 1.0, "#3f9f5a" if dawn else "#3f7f7a") + _fern(-60, 1010, .9, "#3f9f5a" if dawn else "#3f7f7a"))
    if dawn: return far, mid, near
    return far + _flies(((700, 560), (1250, 620))), mid, near + _flies(((900, 720), (1500, 690)))


def bg_leafwood(p):
    far = art._sky(p, "#2b3f8f", "#5a6fc0", y1=1100) + _stars(21, 34, 380) + _moon(1640, 210, 84) + \
        "".join(f'<path d="M{x} 760 L{x + 90} {440 - h} L{x + 180} 760Z" fill="#33508f"/>' for x, h in ((-80, 0), (300, 70), (700, 30), (1150, 80), (1950, 50)))
    mid = (_pine(120, 860, 1.05, "#2f6a5a", "#3a7f6a") + _pine(1830, 860, 1.1, "#2f6a5a", "#3a7f6a")
           + '<path d="M-500 790 C200 740 700 770 1200 750 S2000 740 2420 780 L2420 910 L-500 910Z" fill="#6a5a6a"/>' + _leaves_ground(5, 780, 880, 40))
    near = ('<rect x="-500" y="860" width="2920" height="1200" fill="#8a5a3c"/>'
            '<path d="M-500 900 C200 880 900 890 1500 876 S2200 850 2420 820 L2420 990 C1900 1010 900 1020 -500 1030Z" fill="#a8693c"/>'
            + _leaves_ground(9, 870, 1120, 120) + _flies(((520, 640), (1380, 600), (980, 520))))
    return far, mid + NIGHT_TINT, near + NIGHT_TINT


def bg_darkwood(p):
    far = art._sky(p, "#1c2a6a", "#33468f", y1=1100) + _stars(33, 20, 300) + '<circle cx="1180" cy="120" r="60" fill="#fff6c9" opacity=".7"/>' + \
        '<path d="M1080 120 L760 880 L1500 880 L1260 120Z" fill="#fff6c9" opacity=".07"/>'
    trunks = "".join(f'<rect x="{x - w // 2}" y="-900" width="{w}" height="1800" rx="30" fill="{c}"/><path d="M{x - w // 2 + 20} 200 q20 60 0 120" stroke="#2a2040" stroke-width="10" fill="none"/>'
                     for x, w, c in ((-120, 220, "#3a3050"), (420, 160, "#40365a"), (1560, 200, "#3a3050"), (2060, 240, "#40365a")))
    mid = trunks + '<path d="M-500 800 C200 760 700 780 1200 770 S2000 760 2420 790 L2420 910 L-500 910Z" fill="#33505e"/>' + \
        _mush(520, 860, 1.0) + _mush(600, 870, .7, "#c4a0ff") + _mush(1480, 865, .9, "#c4a0ff") + _mush(1640, 872, .7)
    near = ('<rect x="-500" y="860" width="2920" height="1200" fill="#3d6676"/>' + _mush(140, 1040, 1.1) + _mush(1840, 1050, 1.0, "#c4a0ff")
            + _fern(1100, 1060, .8, "#3a6f70") + _flies(((760, 620), (1260, 700))))
    return far, mid, near


def bg_logglade(p):
    far = art._sky(p, "#2e4396", "#6a80cf", y1=1100) + _stars(41, 40, 420) + _moon(1500, 220, 110) + \
        "".join(_pine(x, 780, s, "#2f5a7a", "#386a8a", "#3a3050") for x, s in ((-40, .9), (260, .7), (1900, .95), (2200, .8)))
    mid = ('<path d="M-500 790 C200 730 700 770 1200 745 S2000 735 2420 780 L2420 910 L-500 910Z" fill="#457a8a"/>'
           + _fern(120, 860, 1.0, "#3f8f7a") + _fern(1820, 860, 1.1, "#3f8f7a") + _bush(1660, 850, .6, ("#2f6a5a", "#3a7f6a", "#479277")))
    near = ('<rect x="-500" y="860" width="2920" height="1200" fill="#548a8a"/><path d="M-500 862 C300 846 900 872 1500 852 S2200 866 2420 856 L2420 900 L-500 900Z" fill="#5c9590"/>'
            + _leaves_ground(13, 900, 1110, 26) + _flies(((620, 560), (1200, 520), (1700, 640), (400, 720))))
    return far, mid, near


art.BG.update({"dusk_wood": bg_dusk_wood, "dawn_wood": lambda p: bg_dusk_wood(p, True), "leafwood": bg_leafwood, "darkwood": bg_darkwood, "logglade": bg_logglade})
art.PLACE.update({"dusk_wood": "the edge of the wood at dusk", "dawn_wood": "the edge of the wood at dawn", "leafwood": "the leafy path", "darkwood": "under the tall trees",
                  "logglade": "the clearing with the big log"})


# ------------------------------------------------------------------ props
def sniff(p):
    line = lambda k, x: (f'<g id="{p}-l{k}"><path d="M{x} 0 q-30 -40 0 -80 t0 -80 t0 -80" stroke="{INK}" stroke-width="22" fill="none" stroke-linecap="round" opacity=".5"/>'
                         f'<path d="M{x} 0 q-30 -40 0 -80 t0 -80 t0 -80" stroke="#fff6c9" stroke-width="12" fill="none" stroke-linecap="round"/></g>')
    return f'<g id="{p}">{line(1, -60)}{line(2, 0)}{line(3, 60)}</g>'


def crunch(p):
    zz = "".join(f'<g transform="rotate({a}) translate(0 -130)"><path d="M-14 0 l14 -22 l14 22 l14 -22" stroke="#ffffff" stroke-width="12" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>'
                 for a in (-70, -35, 0, 35, 70))
    return (f'<g id="{p}"><g id="{p}-b">{zz}</g><ellipse cx="0" cy="0" rx="60" ry="26" fill="#e08b3c" stroke="{INK}" stroke-width="8" transform="rotate(-20)"/>'
            f'<path d="M-50 18 L50 -18" stroke="#a8642f" stroke-width="7"/></g>')


def leafpile(p):
    r = random.Random(3); cols = ("#c9703a", "#e08b3c", "#b85a2e", "#d9a043")
    lv = "".join((lambda x, y, a, c: f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="40" ry="18" fill="{c}" stroke="{INK}" stroke-width="5" transform="rotate({a:.0f} {x:.0f} {y:.0f})"/>')(
        r.uniform(-190, 190) * (1 - k / 40), -10 - k * 3.2 + r.uniform(-10, 10), r.uniform(-70, 70), r.choice(cols)) for k in range(40))
    return f'<g id="{p}"><ellipse cx="0" cy="0" rx="220" ry="20" fill="#000" opacity=".15"/>{lv}</g>'


def biglog(p):
    stone = lambda x: f'<path d="M{x - 70} 0 C{x - 80} -60 {x - 30} -90 {x} -90 C{x + 40} -90 {x + 80} -60 {x + 70} 0Z" fill="#8a8fa8" stroke="{INK}" stroke-width="8"/>'
    moss = "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>' for x, y, r, c in ((-330, -320, 50, "#6cc463"), (-220, -340, 60, "#57b04f"), (-90, -346, 56, "#6cc463"),
                                                                                      (40, -342, 62, "#57b04f"), (170, -336, 54, "#6cc463"), (290, -320, 48, "#57b04f")))
    return (f'<g id="{p}"><ellipse cx="0" cy="0" rx="470" ry="26" fill="#000" opacity=".22"/><path d="M-360 0 C-360 -60 360 -60 360 0Z" fill="#1f1a2a"/>'
            f'{stone(-300)}{stone(300)}<rect x="-430" y="-320" width="860" height="230" rx="110" fill="#9a6a3c" stroke="{INK}" stroke-width="10"/>'
            f'<ellipse cx="420" cy="-205" rx="64" ry="112" fill="#c99a62" stroke="{INK}" stroke-width="10"/><ellipse cx="420" cy="-205" rx="34" ry="60" fill="none" stroke="#9a6a3c" stroke-width="8"/>'
            f'<path d="M-340 -200 h220 M-80 -160 h260 M-20 -250 h180" stroke="#7a5030" stroke-width="9" stroke-linecap="round"/>{moss}</g>')


def berries(p):
    b = "".join(f'<g transform="translate({x} {y})"><circle r="34" fill="#3a1f5a" stroke="{INK}" stroke-width="6"/>'
                + "".join(f'<circle cx="{dx}" cy="{dy}" r="12" fill="#5b2f8a"/>' for dx, dy in ((-12, -12), (12, -12), (0, 6), (-14, 12), (14, 12)))
                + f'<circle cx="-10" cy="-14" r="5" fill="#ffffff" opacity=".8"/></g>' for x, y in ((-60, -40), (0, -60), (60, -40), (-30, -96), (30, -96), (0, -130)))
    return (f'<g id="{p}"><path d="M-130 0 Q-60 -60 0 -20 Q60 -60 130 0 Q0 30 -130 0Z" fill="#4fae4a" stroke="{INK}" stroke-width="7"/>{b}</g>')


def worm(p):
    return (f'<g id="{p}"><path d="M-110 0 q30 -60 60 0 t60 0 t60 0" stroke="{INK}" stroke-width="44" fill="none" stroke-linecap="round"/>'
            f'<path d="M-110 0 q30 -60 60 0 t60 0 t60 0" stroke="#e98a8a" stroke-width="30" fill="none" stroke-linecap="round"/>'
            f'<path d="M-60 -14 v20 M0 -6 v18 M50 -14 v20" stroke="#c96a6a" stroke-width="6"/><circle cx="72" cy="-12" r="5" fill="{INK}"/></g>')


def caterpillar(p):
    segs = "".join(f'<circle cx="{x}" cy="-34" r="30" fill="{"#7ccf4a" if k % 2 else "#94dd5e"}" stroke="{INK}" stroke-width="7"/>' for k, x in enumerate(range(-120, 60, 44)))
    legs = "".join(f'<path d="M{x} -6 v10" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>' for x in range(-120, 60, 44))
    return (f'<g id="{p}">{legs}{segs}<circle cx="90" cy="-44" r="36" fill="#94dd5e" stroke="{INK}" stroke-width="7"/><circle cx="100" cy="-52" r="6" fill="{INK}"/>'
            f'<path d="M84 -78 l-10 -26 M104 -78 l10 -26" stroke="{INK}" stroke-width="6" stroke-linecap="round"/><path d="M96 -30 q8 6 16 0" stroke="{INK}" stroke-width="5" fill="none"/></g>')


def skycard(p, night):
    if night:
        inner = ('<rect x="-200" y="-150" width="400" height="300" rx="40" fill="#2e3f8f"/>' + _moon(60, -30, 70)
                 + "".join(f'<circle cx="{x}" cy="{y}" r="7" fill="#fff8d6"/>' for x, y in ((-140, -100), (-90, -20), (-150, 60), (140, 90), (-40, -110))))
    else:
        inner = ('<rect x="-200" y="-150" width="400" height="300" rx="40" fill="#8fd8ff"/>' + art._sun(p + "sun", 40, -20, 70)
                 + art._cloud(p + "c", -110, 80, .5))
    return f'<g id="{p}">{inner}<rect x="-200" y="-150" width="400" height="300" rx="40" fill="none" stroke="{INK}" stroke-width="12"/></g>'


def hog_lids(p):
    """Over art2.hedgehog's eye (cx 170, cy -140, r 27, lid colour the face's cream)."""
    return (f'<g id="{p}"><circle cx="170" cy="-140" r="31" fill="{art2.HOG["face"]}"/>'
            f'<path d="M144 -138 Q170 -116 196 -138" stroke="{art2.HOG["line"]}" stroke-width="7" fill="none" stroke-linecap="round"/></g>')


def zzz(p):
    z = lambda x, y, s: f'<g transform="translate({x} {y}) scale({s})"><path d="M-30 -30 H30 L-30 30 H30" stroke="{INK}" stroke-width="22" fill="none" stroke-linejoin="round" stroke-linecap="round"/><path d="M-30 -30 H30 L-30 30 H30" stroke="#ffffff" stroke-width="11" fill="none" stroke-linejoin="round" stroke-linecap="round"/></g>'
    return f'<g id="{p}">{z(0, 0, .7)}{z(60, -80, .9)}{z(130, -180, 1.1)}</g>'


def bigmoon(p):
    return f'<g id="{p}">{_moon(0, 0, 120)}</g>'
