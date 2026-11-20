"""Art for zc_ep10 "One Hump or Two? Meet the Camels" (Nov 20 2026): Sandy's two-humped camel cousin in her thick winter coat
(shaggy patches that can fall off one by one: the spring shed), the same cousin in her thinner summer coat, the Gobi in spring,
a big letter B, a snowflake, a sun, a little sign of each season, and a loose patch of shed hair on the ground.
Same hand as art.py: flat fills, one warm dark outline. Nothing here changes an existing character, prop or place
("bactrian" in toon.py stays as it is; the two new kinds are registered here, the way art_zc_ep07.py registers its elephants)."""
import random
import art, art2, kit
from art import INK, CAMEL_B

SHAG = "#8a5c34"; SHAG_L = "#a6774a"; SHAG_D = "#5e3a1c"
# where the winter patches sit on the camel (its own units: facing right, feet at 0), and how big each is
PATCHES = [(-112, -500, 1.0), (98, -506, 1.0), (-176, -350, 1.15), (-30, -330, 1.25), (126, -344, 1.05), (-92, -246, .95), (64, -244, .95), (210, -318, .8)]


def _patch(pid, x, y, s, seed, cls=""):
    """One shaggy patch: a soft blob with a ragged fringe at the bottom and a few strands."""
    r = random.Random(seed); w = 92 * s; h = 66 * s
    top = f"M{-w:.0f} 0 C{-w:.0f} {-h:.0f} {w:.0f} {-h:.0f} {w:.0f} 0"
    fr = ""; n = 6
    for k in range(n):                      # the ragged fringe: little points hanging down
        x0 = w - 2 * w * k / n; x1 = w - 2 * w * (k + 1) / n; xm = (x0 + x1) / 2
        fr += f" L{xm:.0f} {h * r.uniform(.45, .75):.0f} L{x1:.0f} {h * r.uniform(.05, .2):.0f}"
    d = top + fr + "Z"
    strands = "".join(f'<path d="M{r.uniform(-w * .6, w * .6):.0f} {-h * r.uniform(.2, .55):.0f} q{r.uniform(-14, 14):.0f} 22 {r.uniform(-8, 8):.0f} 44" stroke="{SHAG_L}" stroke-width="{8 * s:.0f}" fill="none" stroke-linecap="round"/>'
                      for _ in range(3))
    return (f'<g transform="translate({x} {y})"><g class="{cls}" id="{pid}"><path d="{d}" fill="{SHAG_D}" stroke="{SHAG_D}" stroke-width="16" stroke-linejoin="round"/>'
            f'<path d="{d}" fill="{SHAG}"/>{strands}</g></g>')


def bactrian_winter(pid):
    """Sandy's cousin in winter: two humps, the woolly bib, and eight shaggy patches #<pid>-sh0..7 (class <pid>-shag) over the humps and body.
    A patch falls with a tween on its y: it lands on the ground at y = -(patch y) in the camel's units."""
    base = art.camel(pid, 2, c=CAMEL_B, wool=True)
    assert base.endswith("</g></g>")
    sh = "".join(_patch(f"{pid}-sh{k}", x, y, s, 11 + k, f"{pid}-shag") for k, (x, y, s) in enumerate(PATCHES))
    return base[:-len("</g></g>")] + f'<g id="{pid}-coat">{sh}</g></g></g>'


def bactrian_summer(pid):
    """Sandy's cousin after the spring shed: two humps, a smooth, thinner coat (no bib, no patches)."""
    return art.camel(pid, 2, c=CAMEL_B, wool=False)


_RIG = dict(neck="190 -330", tail="-232 -340", ear="284 -640", legs={"fl": 160, "bl": -138, "fl2": 118, "bl2": -178}, hip=-262, jaw=("rot", 9, "372 -560"), eyes=["eye"], brows=[])
art2.RIGS["bac_winter"] = dict(build=bactrian_winter, **_RIG)
art2.RIGS["bac_summer"] = dict(build=bactrian_summer, **_RIG)
CAMEL_PT = {"head": (345, -601), "eye": (352, -613), "nose": (452, -595), "mouth": (440, -549), "hump": (0, -501), "humptop": (0, -601), "back": (0, -441),
            "body": (0, -323), "feet": (0, 0), "legs": (10, -131), "all": (60, -330), "top": (345, -700), "hump1": (-96, -520), "hump2": (96, -528)}
for _k in ("camel", "bactrian", "bac_winter", "bac_summer"):
    kit.PT[_k] = dict(CAMEL_PT); kit.BOX[_k] = (-340, 490, -660)


# ------------------------------------------------------------------ props
def letter_b(pid, col="#ff7aa2"):
    """A big letter B (the Denver Zoo's "two humps - like the letter B"). Turn it -90 degrees and its two bumps point up, like two humps."""
    return (f'<g id="{pid}"><text x="0" y="0" text-anchor="middle" dominant-baseline="central" font-family="Fredoka, Baloo, sans-serif" font-weight="800" font-size="420" '
            f'fill="{col}" stroke="{INK}" stroke-width="18" paint-order="stroke" stroke-linejoin="round">B</text></g>')


def snowflake(pid, s=1.0, col="#ffffff"):
    """A six-armed snowflake on a soft blue disc."""
    def arms(c, w): return "".join(f'<g transform="rotate({a})"><path d="M0 0 V-92 M0 -52 l-24 -22 M0 -52 l24 -22 M0 -76 l-14 -14 M0 -76 l14 -14" stroke="{c}" stroke-width="{w}" stroke-linecap="round" fill="none"/></g>'
                                   for a in range(0, 360, 60))
    return (f'<g id="{pid}" transform="scale({s})"><circle r="120" fill="#7fb3e6"/>{arms("#2e5a8c", 26)}{arms(col, 14)}'
            f'<circle r="120" fill="none" stroke="{INK}" stroke-width="10"/></g>')


def sun_disc(pid, s=1.0):
    """A hot sun on a warm orange disc."""
    rays = "".join(f'<path d="M0 -62 V-96" stroke="#fff3b0" stroke-width="16" stroke-linecap="round" transform="rotate({a})"/>' for a in range(0, 360, 45))
    return (f'<g id="{pid}" transform="scale({s})"><circle r="120" fill="#ff9f43"/>{rays}<circle r="50" fill="#ffe066" stroke="#e08a1e" stroke-width="8"/>'
            f'<circle r="120" fill="none" stroke="{INK}" stroke-width="10"/></g>')


def flower_disc(pid, s=1.0):
    """Spring: a little pink flower on a green disc."""
    pet = "".join(f'<ellipse cx="0" cy="-40" rx="24" ry="36" fill="#ff9ec4" stroke="#c2577f" stroke-width="6" transform="rotate({a})"/>' for a in range(0, 360, 72))
    return (f'<g id="{pid}" transform="scale({s})"><circle r="120" fill="#9ed67a"/>{pet}<circle r="22" fill="#ffd23f" stroke="#c99a12" stroke-width="6"/>'
            f'<circle r="120" fill="none" stroke="{INK}" stroke-width="10"/></g>')


def hair_clump(pid, s=1.0):
    """A loose patch of shed camel hair lying on the ground."""
    return f'<g id="{pid}" transform="scale({s})">{_patch(pid + "c", 0, 0, 1.1, 7)}</g>'


def height_line(pid, w=360, col="#ff5a5f"):
    """A dashed line across the top of a camel, to compare how tall two camels are."""
    return f'<g id="{pid}"><path d="M{-w / 2:.0f} 0 H{w / 2:.0f}" stroke="{col}" stroke-width="12" stroke-dasharray="30 20" stroke-linecap="round"/></g>'


# ------------------------------------------------------------------ the Gobi in spring
def bg_gobi_spring(p):
    """The cousin's home in spring: the snow is gone from the ground, only a little is left on the mountain tops; pale green grass, a blue sky."""
    far = art._sky(p, "#7fc3f0", "#e3f4fd") + art._cloud(p + "c1", 520, 160, 1.0, "#fff") + art._cloud(p + "c2", 1600, 110, .8, "#fff") + \
        '<path d="M-500 640 L120 300 L420 520 L760 220 L1120 560 L1480 280 L1880 580 L2420 360 L2420 760 L-500 760Z" fill="#9a9fb8"/>' + \
        '<path d="M120 300 L200 366 L140 372Z M760 220 L850 302 L700 296Z M1480 280 L1560 346 L1420 344Z" fill="#fff"/>'
    mid = art._dune(690, 24, "#c8d49a", 41) + '<path d="M1500 700 l60 -90 l100 20 l70 70Z M200 720 l50 -70 l80 14 l60 56Z" fill="#a39a86"/>'
    near = f'<rect x="-500" y="840" width="2920" height="1200" fill="#b9cc84"/>' + art._dune(846, 14, "#b9cc84", 43) + \
        "".join(f'<path d="M{x} {y} q-8 -30 -2 -46 M{x + 10} {y} q4 -34 14 -44 M{x + 20} {y} q10 -24 24 -30" stroke="#7fa652" stroke-width="7" fill="none" stroke-linecap="round"/>'
                for x, y in ((240, 960), (620, 1010), (1500, 950), (1820, 1000), (980, 1040), (-200, 980), (2100, 970)))
    return far, mid, near


art.BG.update({"gobi_spring": bg_gobi_spring})
art.PLACE.update({"gobi_spring": "the Gobi in spring"})
