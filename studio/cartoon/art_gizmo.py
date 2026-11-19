"""Art for Gizmo Explains' cartoon test (gc_ep01, Nov 19 2026): Gizmo the robot as a toon.py rig, his lab and outdoor places in the
channel's colours (#1d3a8a to #3561d9, accent #5ff3ff), and the props of "How Does a Seed Grow Into a Plant?".
Gizmo is drawn from studio/cartoon/gizmo/gizmo_flat.svg.part (the drawing used for the channel banner), in the engine's style: flat fills,
a thick dark-navy outline, nothing traced. Registered from here the way art3.py registers its places: no Zoo character, prop or place changes.
Props are drawn around (0, 0); a rig stands with its feet (here: the tips of the jets) on y = 0."""
import art, art2, kit
from art import INK, SUN

NAVY = "#1b2550"; SCREEN = "#16204a"; CYAN = "#9ff6ff"; ACC = "#5ff3ff"; ORANGE = "#f08a24"; SILVER = "#e3e9f4"; STEEL = "#c9d3e6"
B1, B2 = "#1d3a8a", "#3561d9"          # the channel's blues
SOIL = ("#8a5a32", "#6e4526", "#a8743f")
GREEN = ("#57c078", "#2f8a4a", "#9be08a")


# ================================================================== Gizmo
def _eye(pid, cx, cy):
    """A screen eye: a cyan oval with a glint; -lid covers it with the screen colour and draws a closed-eye curve (a blink)."""
    return (f'<g id="{pid}"><ellipse cx="{cx}" cy="{cy}" rx="34" ry="42" fill="{CYAN}"/><circle cx="{cx + 12}" cy="{cy - 16}" r="11" fill="#fff"/>'
            f'<g id="{pid}-lid" opacity="0"><ellipse cx="{cx}" cy="{cy}" rx="40" ry="48" fill="{SCREEN}"/>'
            f'<path d="M{cx - 32} {cy + 2} Q{cx} {cy + 22} {cx + 32} {cy + 2}" stroke="{CYAN}" stroke-width="10" fill="none" stroke-linecap="round"/></g></g>')


def gizmo(pid):
    """Gizmo (gizmo_flat.svg.part, both arms down). Parts the engine moves: -hover (the floating bob), -body, -al / -ar (arms, shoulders at
    (-120 120) / (120 120) in the drawing's own units), -glow (the antenna bulb lit, opacity), -eyeL / -eyeR with -lid (blinks), -smile, -jaw (the
    open talking mouth over the smile), -frown, -jets (the little flames)."""
    arm = lambda s, aid: (f'<g id="{pid}-{aid}"><path d="M{120 * s} 120 C{190 * s} 130 {220 * s} 175 {240 * s} 215" stroke="{NAVY}" stroke-width="30" fill="none" stroke-linecap="round"/>'
                          f'<path d="M{120 * s} 120 C{190 * s} 130 {220 * s} 175 {240 * s} 215" stroke="{STEEL}" stroke-width="16" fill="none" stroke-linecap="round"/>'
                          f'<circle cx="{244 * s}" cy="225" r="34" fill="{ORANGE}" stroke="{NAVY}" stroke-width="9"/></g>')
    rays = "".join(f'<path d="M0 -245 m0 -48 v-30" stroke="#fff36b" stroke-width="10" stroke-linecap="round" transform="rotate({a} 0 -245)"/>' for a in range(0, 360, 45))
    inner = (f'<g id="{pid}-jets"><path d="M-55 300 l18 70 l18 -70z" fill="{SUN}" stroke="#e8a000" stroke-width="6"/><path d="M37 300 l18 70 l18 -70z" fill="{SUN}" stroke="#e8a000" stroke-width="6"/></g>'
             f'<ellipse cx="0" cy="285" rx="150" ry="38" fill="{ORANGE}" stroke="{NAVY}" stroke-width="10"/><ellipse cx="0" cy="275" rx="120" ry="24" fill="{STEEL}"/>'
             + arm(-1, "al") + arm(1, "ar")
             + f'<path d="M-120 70 h240 q20 0 18 20 l-22 170 q-3 22 -25 22 h-182 q-22 0 -25 -22 l-22 -170 q-2 -20 18 -20z" fill="{SILVER}" stroke="{NAVY}" stroke-width="10"/>'
             f'<path d="M-104 92 h40 l-16 150 h-26z" fill="#fff" opacity=".55"/>'
             f'<rect x="-62" y="130" width="124" height="56" rx="12" fill="{ORANGE}" stroke="{NAVY}" stroke-width="8"/>'
             f'<path d="M0 140 l9 18 l20 2 l-15 13 l5 20 l-19 -11 l-19 11 l5 -20 l-15 -13 l20 -2z" fill="{CYAN}" stroke="{NAVY}" stroke-width="4"/>'
             f'<rect x="-8" y="-230" width="16" height="60" fill="#8b97b0" stroke="{NAVY}" stroke-width="6"/>'
             f'<circle cx="0" cy="-245" r="30" fill="{ACC}" stroke="{NAVY}" stroke-width="9"/><circle cx="-9" cy="-254" r="9" fill="#fff"/>'
             f'<g id="{pid}-glow" opacity="0"><circle cx="0" cy="-245" r="62" fill="#fff36b" opacity=".45"/>{rays}<circle cx="0" cy="-245" r="30" fill="#fff36b" stroke="{NAVY}" stroke-width="9"/><circle cx="-9" cy="-254" r="10" fill="#fff"/></g>'
             f'<rect x="-205" y="-120" width="40" height="120" rx="14" fill="{ORANGE}" stroke="{NAVY}" stroke-width="9"/><rect x="165" y="-120" width="40" height="120" rx="14" fill="{ORANGE}" stroke="{NAVY}" stroke-width="9"/>'
             f'<rect x="-150" y="-195" width="300" height="34" rx="12" fill="{ORANGE}" stroke="{NAVY}" stroke-width="9"/>'
             f'<rect x="-175" y="-170" width="350" height="250" rx="34" fill="{SILVER}" stroke="{NAVY}" stroke-width="11"/>'
             f'<rect x="-145" y="-142" width="290" height="194" rx="24" fill="{SCREEN}"/>'
             + _eye(f"{pid}-eyeL", -58, -62) + _eye(f"{pid}-eyeR", 58, -62)
             + f'<g id="{pid}-smile"><path d="M-50 0 Q0 45 50 0 Z" fill="{CYAN}"/></g>'
             f'<g id="{pid}-jaw" opacity="0"><path d="M-53 -3 Q0 74 53 -3 Z" fill="{CYAN}"/><path d="M-28 26 Q0 46 28 26 Q0 34 -28 26Z" fill="#ff8fb1"/></g>'
             f'<g id="{pid}-frown" opacity="0"><path d="M-40 26 Q0 -2 40 26" stroke="{CYAN}" stroke-width="12" fill="none" stroke-linecap="round"/></g>'
             f'<ellipse cx="-108" cy="-6" rx="20" ry="11" fill="#ff8fb1" opacity=".9"/><ellipse cx="108" cy="-6" rx="20" ry="11" fill="#ff8fb1" opacity=".9"/>')
    return (f'<g id="{pid}"><ellipse cx="0" cy="6" rx="130" ry="20" fill="#000" opacity=".16"/>'
            f'<g id="{pid}-hover"><g id="{pid}-body"><g transform="translate(0 -370)">{inner}</g></g></g></g>')


art2.RIGS.update({"gizmo": dict(build=lambda p: gizmo(p), neck=None, tail=None, ear=None, legs=None, hip=0, jaw=("y", 3), eyes=["eyeL", "eyeR"], brows=[], hover=16)})
kit.PT.update({"gizmo": {"head": (0, -415), "screen": (0, -420), "body": (0, -200), "top": (0, -650), "feet": (0, 0), "all": (0, -320)}})
kit.BOX.update({"gizmo": (-290, 290, -660)})


# ================================================================== places
def _grad(gid, c0, c1):
    return f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c0}"/><stop offset="1" stop-color="{c1}"/></linearGradient></defs>'


def _jar(x, y, s, inside=""):
    return (f'<g transform="translate({x} {y}) scale({s})"><rect x="-44" y="-96" width="88" height="96" rx="18" fill="{ACC}" opacity=".35" stroke="#bff9ff" stroke-width="6"/>'
            f'<rect x="-50" y="-116" width="100" height="24" rx="8" fill="{ORANGE}"/>{inside}<rect x="-30" y="-84" width="12" height="60" rx="6" fill="#fff" opacity=".6"/></g>')


def _seeds_in(n=5):
    return "".join(f'<ellipse cx="{-24 + (k % 3) * 22}" cy="{-14 - (k // 3) * 16}" rx="11" ry="8" fill="#b07a42"/>' for k in range(n))


def _sprout_in():
    return f'<path d="M0 -6 V-60" stroke="{GREEN[1]}" stroke-width="7"/><ellipse cx="-14" cy="-62" rx="16" ry="8" fill="{GREEN[0]}"/><ellipse cx="14" cy="-62" rx="16" ry="8" fill="{GREEN[0]}"/><rect x="-40" y="-20" width="80" height="20" fill="{SOIL[0]}"/>'


def _pot(x, y, s, plant=0):
    """A small clay pot (decoration): plant 0 = soil, 1 = a sprout, 2 = a leafy plant."""
    pl = ""
    if plant >= 1: pl += f'<path d="M0 -92 V-170" stroke="{GREEN[1]}" stroke-width="10"/><ellipse cx="-26" cy="-172" rx="28" ry="13" fill="{GREEN[0]}"/><ellipse cx="26" cy="-172" rx="28" ry="13" fill="{GREEN[0]}"/>'
    if plant >= 2: pl += f'<path d="M0 -170 V-250" stroke="{GREEN[1]}" stroke-width="10"/><ellipse cx="-34" cy="-230" rx="36" ry="16" fill="{GREEN[0]}" transform="rotate(-20 -34 -230)"/><ellipse cx="34" cy="-250" rx="36" ry="16" fill="{GREEN[0]}" transform="rotate(20 34 -250)"/>'
    return (f'<g transform="translate({x} {y}) scale({s})">{pl}<path d="M-70 -92 L-54 0 H54 L70 -92Z" fill="#d9773f" stroke="#8a4320" stroke-width="7" stroke-linejoin="round"/>'
            f'<rect x="-80" y="-112" width="160" height="28" rx="8" fill="#e8894f" stroke="#8a4320" stroke-width="7"/><ellipse cx="0" cy="-112" rx="68" ry="10" fill="{SOIL[1]}"/></g>')


def bg_glab(p):
    """Gizmo's lab: the channel's blue wall, a round window, shelves of seed jars and sprouts, a long counter, a tiled floor."""
    far = (_grad(f"{p}g", B1, B2) + f'<rect x="-600" y="-900" width="3120" height="1900" fill="url(#{p}g)"/>'
           + "".join(f'<path d="M{x} -900 V860" stroke="#ffffff" stroke-width="3" opacity=".06"/>' for x in range(-560, 2500, 160))
           + f'<circle cx="1480" cy="300" r="200" fill="#bfe6ff" stroke="{SILVER}" stroke-width="26"/><circle cx="1480" cy="300" r="200" fill="none" stroke="{NAVY}" stroke-width="8"/>'
           + f'<path d="M1280 300 H1680 M1480 100 V500" stroke="{SILVER}" stroke-width="16"/><ellipse cx="1420" cy="360" rx="90" ry="34" fill="#fff" opacity=".9"/><circle cx="1560" cy="210" r="46" fill="{SUN}"/>'
           + f'<rect x="60" y="250" width="560" height="22" rx="8" fill="{SILVER}"/><rect x="60" y="460" width="560" height="22" rx="8" fill="{SILVER}"/>'
           + _jar(140, 250, 1, _seeds_in(5)) + _jar(270, 250, 1, _seeds_in(3)) + _jar(400, 250, 1, _sprout_in()) + _jar(530, 250, 1, _seeds_in(6))
           + _pot(160, 460, .9, 1) + _pot(320, 460, .9, 2) + _pot(480, 460, .9, 0)
           + f'<g transform="translate(-260 360)"><rect x="-120" y="-150" width="240" height="300" rx="20" fill="{B1}" stroke="{ACC}" stroke-width="8"/>'
           f'<path d="M0 120 V-40" stroke="{ACC}" stroke-width="8"/><ellipse cx="-40" cy="-40" rx="40" ry="18" fill="none" stroke="{ACC}" stroke-width="8"/><ellipse cx="40" cy="-70" rx="40" ry="18" fill="none" stroke="{ACC}" stroke-width="8"/>'
           f'<path d="M0 120 q-30 30 -60 20 M0 120 q30 30 60 24" stroke="{ACC}" stroke-width="8" fill="none"/></g>')
    mid = (f'<rect x="-600" y="640" width="3120" height="40" fill="{SILVER}"/><rect x="-600" y="680" width="3120" height="200" fill="#9fb0d4"/>'
           + "".join(f'<rect x="{x}" y="700" width="230" height="160" rx="14" fill="#b6c4e2" stroke="#8496bf" stroke-width="5"/><circle cx="{x + 115}" cy="780" r="10" fill="{NAVY}"/>' for x in range(-560, 2500, 260))
           + _pot(1900, 640, .8, 2) + _pot(-200, 640, .8, 1)
           + f'<g transform="translate(1100 640)"><rect x="-60" y="-34" width="120" height="34" rx="8" fill="{NAVY}"/><circle cx="20" cy="-80" r="44" fill="none" stroke="{SILVER}" stroke-width="14"/><path d="M-10 -50 L-60 -10" stroke="{SILVER}" stroke-width="16" stroke-linecap="round"/></g>')
    near = (f'<rect x="-600" y="870" width="3120" height="1200" fill="#142c6e"/>'
            + "".join(f'<path d="M{x} 870 L{x + (x - 960) * .6:.0f} 1400" stroke="#2a4a9c" stroke-width="5"/>' for x in range(-560, 2500, 180))
            + "".join(f'<path d="M-600 {y} H2520" stroke="#2a4a9c" stroke-width="5"/>' for y in (930, 1010, 1110, 1240))
            + f'<ellipse cx="960" cy="1000" rx="700" ry="60" fill="{ACC}" opacity=".08"/>')
    return far, mid, near


def bg_gbench(p):
    """Gizmo's work bench: a big science screen on the wall (a seed on it), a pegboard with tools, the white bench top in front."""
    far = (_grad(f"{p}g", B1, B2) + f'<rect x="-600" y="-900" width="3120" height="1900" fill="url(#{p}g)"/>'
           + f'<rect x="660" y="90" width="600" height="380" rx="30" fill="{SILVER}" stroke="{NAVY}" stroke-width="10"/><rect x="690" y="120" width="540" height="320" rx="18" fill="{SCREEN}"/>'
           + f'<g transform="translate(960 280)"><ellipse cx="0" cy="0" rx="120" ry="80" fill="none" stroke="{ACC}" stroke-width="10"/><path d="M-30 30 q0 -60 40 -70" stroke="{ACC}" stroke-width="10" fill="none"/></g>'
           + "".join(f'<rect x="{690 + k * 60}" y="410" width="40" height="12" rx="6" fill="{ACC}" opacity="{.3 + .1 * k}"/>' for k in range(6))
           + f'<rect x="-420" y="80" width="760" height="460" rx="24" fill="#2a4fb8"/>'
           + "".join(f'<circle cx="{x}" cy="{y}" r="7" fill="{B1}"/>' for x in range(-380, 320, 50) for y in range(110, 520, 50))
           + f'<path d="M-260 160 v190" stroke="{SILVER}" stroke-width="22" stroke-linecap="round"/><circle cx="-260" cy="380" r="34" fill="none" stroke="{SILVER}" stroke-width="12"/>'
           + f'<rect x="-120" y="150" width="40" height="220" rx="12" fill="{ORANGE}"/><path d="M60 160 q40 40 0 80 q-40 40 0 80" stroke="{ACC}" stroke-width="14" fill="none"/>'
           + f'<rect x="1600" y="120" width="520" height="22" rx="8" fill="{SILVER}"/>' + _jar(1680, 120, 1, _seeds_in(4)) + _jar(1820, 120, 1, _sprout_in()) + _jar(1960, 120, 1, _seeds_in(6))
           + _pot(1720, 400, .9, 2) + _pot(1920, 400, .9, 1) + f'<rect x="1600" y="400" width="520" height="22" rx="8" fill="{SILVER}"/>')
    mid = ""
    near = (f'<rect x="-600" y="760" width="3120" height="1300" fill="#8a9cc6"/><rect x="-600" y="740" width="3120" height="50" rx="10" fill="{SILVER}" stroke="{NAVY}" stroke-width="8"/>'
            + f'<rect x="-600" y="790" width="3120" height="18" fill="#6f82b0"/>'
            + "".join(f'<rect x="{x}" y="830" width="300" height="200" rx="16" fill="#9aabd2" stroke="#7184b4" stroke-width="5"/><rect x="{x + 110}" y="860" width="80" height="14" rx="7" fill="{NAVY}"/>' for x in range(-560, 2500, 340)))
    return far, mid, near


def bg_gwindow(p):
    """The lab's big sunny window with a wide sill for pots."""
    far = (_grad(f"{p}g", B1, B2) + f'<rect x="-600" y="-900" width="3120" height="1900" fill="url(#{p}g)"/>'
           + _grad(f"{p}s", "#7cc4ff", "#d8f0ff") + f'<rect x="380" y="-40" width="1160" height="780" fill="url(#{p}s)"/>'
           + f'<circle cx="1320" cy="160" r="90" fill="{SUN}"/><circle cx="1320" cy="160" r="130" fill="{SUN}" opacity=".25"/>'
           + f'<ellipse cx="640" cy="200" rx="130" ry="44" fill="#fff"/><ellipse cx="720" cy="170" rx="80" ry="40" fill="#fff"/>'
           + f'<path d="M380 600 C600 520 800 560 1000 540 S1400 520 1540 560 V740 H380Z" fill="#7fcf7a"/>'
           + f'<rect x="360" y="-60" width="1200" height="820" fill="none" stroke="{SILVER}" stroke-width="40"/><path d="M960 -60 V760 M360 340 H1560" stroke="{SILVER}" stroke-width="24"/>'
           + f'<path d="M1300 200 L900 760 L1180 760Z" fill="#fff6b0" opacity=".18"/>')
    mid = (f'<rect x="200" y="740" width="1520" height="44" rx="12" fill="{SILVER}" stroke="{NAVY}" stroke-width="8"/>'
           + _pot(330, 740, .85, 2) + _pot(1600, 740, .85, 1))
    near = (f'<rect x="-600" y="784" width="3120" height="1300" fill="#2a4fb8"/>' + "".join(f'<path d="M-600 {y} H2520" stroke="{B1}" stroke-width="6"/>' for y in (860, 960, 1080))
            + f'<rect x="-600" y="784" width="3120" height="16" fill="{B1}"/>')
    return far, mid, near


def bg_gsoil(p):
    """Under the ground (a cutaway, like a picture of a garden cut open): a strip of sky and grass on top, soil in layers with pebbles below."""
    far = (_grad(f"{p}s", "#5a8ef0", "#bfe4ff") + f'<rect x="-600" y="-900" width="3120" height="1300" fill="url(#{p}s)"/>'
           + f'<circle cx="1700" cy="80" r="80" fill="{SUN}"/><ellipse cx="420" cy="120" rx="120" ry="40" fill="#fff"/><ellipse cx="490" cy="96" rx="70" ry="34" fill="#fff"/>'
           + f'<path d="M-600 330 C0 280 500 300 960 290 S1800 300 2520 280 V420 H-600Z" fill="#7fcf7a"/>')
    soil = (f'<rect x="-600" y="380" width="3120" height="1700" fill="{SOIL[0]}"/><path d="M-600 640 C200 610 900 660 1500 630 S2200 640 2520 620 V2100 H-600Z" fill="#7a4d2b"/>'
            f'<path d="M-600 900 C300 880 1000 920 1700 890 S2300 900 2520 890 V2100 H-600Z" fill="{SOIL[1]}"/>'
            + "".join(f'<ellipse cx="{x}" cy="{y}" rx="{r}" ry="{r * .7:.0f}" fill="#b49a7a" stroke="#7a6248" stroke-width="5"/>' for x, y, r in
                      ((120, 520, 26), (360, 760, 18), (620, 980, 30), (1500, 520, 20), (1760, 800, 28), (1980, 560, 16), (260, 1040, 22), (1880, 1060, 24), (820, 470, 14)))
            + "".join(f'<circle cx="{x}" cy="{y}" r="5" fill="#5a3a20"/>' for x, y in ((200, 600), (500, 700), (700, 560), (1400, 760), (1650, 640), (1300, 980), (900, 1050), (1580, 1000), (420, 900))))
    grass = (f'<rect x="-600" y="360" width="3120" height="30" fill="#4fae4a"/>'
             + "".join(f'<path d="M{x} 372 l-10 -40 M{x + 12} 372 l4 -48 M{x + 24} 372 l14 -36" stroke="#3f9e3c" stroke-width="8" stroke-linecap="round"/>' for x in range(-560, 2500, 70))
             + "".join(f'<path d="M{x} 388 q-10 50 -30 80 M{x} 388 q8 60 24 90" stroke="#c9a06a" stroke-width="5" fill="none" stroke-linecap="round"/>' for x in range(-500, 2500, 210)))
    return far, soil, grass


def _flower(x, y, s, col):
    return (f'<g transform="translate({x} {y}) scale({s})"><path d="M0 0 V-90" stroke="{GREEN[1]}" stroke-width="9"/><ellipse cx="18" cy="-40" rx="20" ry="9" fill="{GREEN[0]}" transform="rotate(-30 18 -40)"/>'
            + "".join(f'<ellipse cx="0" cy="-118" rx="14" ry="26" fill="{col}" transform="rotate({a} 0 -96)"/>' for a in range(0, 360, 60)) + f'<circle cx="0" cy="-96" r="14" fill="{SUN}"/></g>')


def bg_ggarden(p):
    """Gizmo's garden outside: a blue sky in the channel's colours, green hills, a white fence, two beds of brown soil."""
    far = (_grad(f"{p}s", B2, "#a9dcff") + f'<rect x="-600" y="-900" width="3120" height="1700" fill="url(#{p}s)"/>'
           + f'<circle cx="1640" cy="150" r="96" fill="{SUN}"/><circle cx="1640" cy="150" r="140" fill="{SUN}" opacity=".22"/>'
           + f'<ellipse cx="380" cy="170" rx="140" ry="46" fill="#fff"/><ellipse cx="460" cy="140" rx="86" ry="44" fill="#fff"/><ellipse cx="1100" cy="90" rx="100" ry="34" fill="#fff" opacity=".9"/>'
           + f'<path d="M-600 600 C-100 470 400 520 800 560 S1700 470 2520 540 V800 H-600Z" fill="#6cc070"/>')
    mid = (f'<path d="M-600 680 C200 620 900 660 1500 640 S2200 650 2520 650 V900 H-600Z" fill="#57b05e"/>'
           + "".join(f'<rect x="{x}" y="600" width="26" height="140" rx="10" fill="#fff" stroke="#c9d3e6" stroke-width="4"/>' for x in range(-560, 2500, 90))
           + f'<rect x="-600" y="630" width="3120" height="18" fill="#fff"/><rect x="-600" y="690" width="3120" height="18" fill="#fff"/>'
           + "".join(_flower(x, 760, .8, c) for x, c in ((-200, "#ff7aa2"), (140, ACC), (1700, "#ff7aa2"), (2000, SUN), (2250, ACC))))
    near = (f'<rect x="-600" y="760" width="3120" height="1300" fill="#5fb85f"/>'
            + f'<path d="M780 930 C900 880 1500 880 1640 930 V990 H780Z" fill="{SOIL[1]}"/><path d="M800 930 C920 892 1500 892 1620 930" stroke="{SOIL[2]}" stroke-width="10" fill="none"/>'
            + f'<path d="M-500 1010 C-380 960 200 960 330 1010 V1070 H-500Z" fill="{SOIL[1]}"/>'
            + "".join(f'<path d="M{x} 1080 l-8 -34 M{x + 10} 1080 l2 -40 M{x + 20} 1080 l12 -30" stroke="#3f9e3c" stroke-width="7" stroke-linecap="round"/>' for x in range(-560, 2500, 110))
            + _flower(400, 1060, 1.0, SUN) + _flower(1800, 1050, 1.0, "#ff7aa2"))
    return far, mid, near


def bg_gmeadow(p):
    """A sunny meadow full of flowers on a hill, a little later in the year."""
    far = (_grad(f"{p}s", B2, "#bfe8ff") + f'<rect x="-600" y="-900" width="3120" height="1700" fill="url(#{p}s)"/>'
           + f'<circle cx="320" cy="150" r="100" fill="{SUN}"/><circle cx="320" cy="150" r="150" fill="{SUN}" opacity=".2"/>'
           + f'<ellipse cx="1300" cy="140" rx="140" ry="44" fill="#fff"/><ellipse cx="1380" cy="110" rx="80" ry="40" fill="#fff"/>'
           + f'<path d="M-600 560 C0 440 600 600 1100 520 S2000 470 2520 560 V800 H-600Z" fill="#7cc96f"/>')
    mid = (f'<path d="M-600 700 C300 640 900 690 1500 660 S2200 680 2520 670 V900 H-600Z" fill="#62b85a"/>'
           + "".join(_flower(x, y, .7, c) for x, y, c in ((-300, 720, SUN), (-60, 700, "#ff7aa2"), (180, 730, ACC), (420, 700, "#fff"), (1500, 690, SUN), (1760, 710, "#ff7aa2"), (2020, 690, ACC), (2300, 720, "#fff"))))
    near = (f'<rect x="-600" y="780" width="3120" height="1300" fill="#55ad55"/>'
            + "".join(_flower(x, y, 1.0, c) for x, y, c in ((-400, 1000, "#ff7aa2"), (60, 1060, SUN), (260, 990, ACC), (1640, 1040, "#fff"), (1900, 990, "#ff7aa2"), (2200, 1060, SUN)))
            + "".join(f'<path d="M{x} 1100 l-8 -34 M{x + 10} 1100 l2 -40 M{x + 20} 1100 l12 -30" stroke="#3f9e3c" stroke-width="7" stroke-linecap="round"/>' for x in range(-560, 2500, 100)))
    return far, mid, near


def bg_paper_gz(p):
    """Gizmo's picture board: a blueprint (the channel's blue, a fine grid), so a diagram never floats in a scene. A 'paper' place: not counted as a place."""
    far = (f'<rect x="-600" y="-900" width="3120" height="2900" fill="{B1}"/>'
           + "".join(f'<path d="M{x} -900 V2000" stroke="{B2}" stroke-width="4"/>' for x in range(-560, 2520, 120))
           + "".join(f'<path d="M-600 {y} H2520" stroke="{B2}" stroke-width="4"/>' for y in range(-840, 2000, 120))
           + "".join(f'<path d="M{x} -900 V2000" stroke="{ACC}" stroke-width="2" opacity=".18"/>' for x in range(-560, 2520, 480)))
    return far, "", ""


art.BG.update({"glab": bg_glab, "gbench": bg_gbench, "gwindow": bg_gwindow, "gsoil": bg_gsoil, "ggarden": bg_ggarden, "gmeadow": bg_gmeadow, "paper_gz": bg_paper_gz})
art.PLACE.update({"glab": "Gizmo's lab", "gbench": "Gizmo's work bench", "gwindow": "the sunny lab window", "gsoil": "under the ground (cutaway)", "ggarden": "Gizmo's garden",
                  "gmeadow": "the flower meadow", "paper_gz": "the picture board (blueprint)"})


# ================================================================== props
def seed(pid):
    """A big bean seed lying on its side (closed). -coat is the whole seed."""
    return (f'<g id="{pid}"><g id="{pid}-coat"><path d="M-150 10 C-160 -90 -40 -120 30 -96 C110 -70 170 -40 160 30 C150 100 40 110 -30 92 C-100 76 -146 60 -150 10Z" fill="#b07a42" stroke="#6e4526" stroke-width="10"/>'
            f'<path d="M-40 -60 C20 -80 90 -60 120 -20" stroke="#d6a26a" stroke-width="16" fill="none" stroke-linecap="round" opacity=".8"/><ellipse cx="0" cy="80" rx="26" ry="9" fill="#6e4526"/></g></g>')


def seed_open(pid):
    """The same seed cut open: the seed coat (-coat, the brown rim), the food store (-food, two cream halves) and the baby plant (-baby: a tiny
    root -broot pointing down and a tiny shoot -bshoot with two folded leaves pointing up)."""
    shape = "M-210 14 C-224 -126 -56 -168 42 -134 C154 -98 238 -56 224 42 C210 140 56 154 -42 128 C-140 106 -204 84 -210 14Z"
    return (f'<g id="{pid}"><g id="{pid}-coat"><path d="{shape}" fill="#b07a42" stroke="#6e4526" stroke-width="12"/></g>'
            f'<g id="{pid}-food"><path d="M-180 14 C-190 -100 -60 -132 20 -108 C30 -40 20 40 0 104 C-110 90 -176 70 -180 14Z" fill="#f3e3b0" stroke="#d1b87a" stroke-width="6"/>'
            f'<path d="M30 -106 C130 -76 200 -40 190 40 C180 112 70 120 10 104 C40 40 46 -40 30 -106Z" fill="#f6e8bf" stroke="#d1b87a" stroke-width="6"/>'
            f'<ellipse cx="-100" cy="-20" rx="40" ry="18" fill="#fff6d8" opacity=".8"/></g>'
            f'<g id="{pid}-baby"><g id="{pid}-broot"><path d="M14 0 C16 30 8 60 -6 86" stroke="#7a5a2a" stroke-width="22" fill="none" stroke-linecap="round"/><path d="M14 0 C16 30 8 60 -6 86" stroke="#f4ead0" stroke-width="10" fill="none" stroke-linecap="round"/></g>'
            f'<g id="{pid}-bshoot"><path d="M14 0 C14 -30 20 -52 26 -66" stroke="{GREEN[1]}" stroke-width="14" fill="none" stroke-linecap="round"/>'
            f'<ellipse cx="6" cy="-74" rx="24" ry="12" fill="{GREEN[0]}" stroke="{GREEN[1]}" stroke-width="5" transform="rotate(-30 6 -74)"/><ellipse cx="44" cy="-76" rx="24" ry="12" fill="{GREEN[0]}" stroke="{GREEN[1]}" stroke-width="5" transform="rotate(30 44 -76)"/></g></g></g>')


def growth(pid, seed_scale=1.0, root=True):
    """A seed in the soil and everything that grows out of it, each part shown by the episode: -seed, -crack (the coat opens), -root (grows DOWN from
    the seed; scaleY from the top), -hairs, -shoot (grows UP; scaleY from the bottom), -sl (the two seed leaves), -leaves (true leaves), -stem2 and
    -flower (a sunflower-like head) at the top. The seed sits at (0, 0); the root reaches y = 300, the shoot y = -330, the flower y = -700."""
    return (f'<g id="{pid}">'
            f'<g id="{pid}-root"{"" if root else ' opacity="0"'}><path d="M0 20 C10 90 -14 170 6 300" stroke="#efe6c4" stroke-width="20" fill="none" stroke-linecap="round"/>'
            f'<path d="M0 20 C10 90 -14 170 6 300" stroke="#cbb98a" stroke-width="7" fill="none" stroke-linecap="round"/>'
            f'<g id="{pid}-hairs">' + "".join(f'<path d="M{x} {y} l{dx} 30" stroke="#efe6c4" stroke-width="8" stroke-linecap="round"/>' for x, y, dx in ((2, 120, -44), (-4, 170, 46), (-6, 220, -40), (0, 260, 40), (6, 90, 40))) + '</g></g>'
            f'<g id="{pid}-stem2" opacity="0"><path d="M0 -330 C-6 -440 10 -560 0 -660" stroke="{GREEN[1]}" stroke-width="22" fill="none" stroke-linecap="round"/>'
            f'<ellipse cx="-70" cy="-470" rx="70" ry="26" fill="{GREEN[0]}" stroke="{GREEN[1]}" stroke-width="7" transform="rotate(-24 -70 -470)"/>'
            f'<ellipse cx="74" cy="-560" rx="70" ry="26" fill="{GREEN[0]}" stroke="{GREEN[1]}" stroke-width="7" transform="rotate(24 74 -560)"/></g>'
            f'<g id="{pid}-shoot"><path d="M0 -10 C-8 -100 12 -220 0 -330" stroke="{GREEN[1]}" stroke-width="20" fill="none" stroke-linecap="round"/>'
            f'<path d="M0 -10 C-8 -100 12 -220 0 -330" stroke="{GREEN[2]}" stroke-width="6" fill="none" stroke-linecap="round" opacity=".7"/></g>'
            f'<g id="{pid}-sl"><ellipse cx="-50" cy="-336" rx="56" ry="24" fill="{GREEN[0]}" stroke="{GREEN[1]}" stroke-width="7" transform="rotate(-18 -50 -336)"/>'
            f'<ellipse cx="50" cy="-336" rx="56" ry="24" fill="{GREEN[0]}" stroke="{GREEN[1]}" stroke-width="7" transform="rotate(18 50 -336)"/></g>'
            f'<g id="{pid}-leaves"><ellipse cx="-74" cy="-240" rx="74" ry="28" fill="{GREEN[0]}" stroke="{GREEN[1]}" stroke-width="7" transform="rotate(-28 -74 -240)"/>'
            f'<ellipse cx="78" cy="-190" rx="74" ry="28" fill="{GREEN[0]}" stroke="{GREEN[1]}" stroke-width="7" transform="rotate(26 78 -190)"/>'
            f'<path d="M-40 -230 l-60 -12 M44 -182 l62 -10" stroke="{GREEN[1]}" stroke-width="5" stroke-linecap="round"/></g>'
            f'<g id="{pid}-flower" opacity="0"><g transform="translate(0 -700)">' + "".join(f'<ellipse cx="0" cy="-104" rx="30" ry="56" fill="{SUN}" stroke="#e8a000" stroke-width="6" transform="rotate({a})"/>' for a in range(0, 360, 30))
            + f'<circle r="74" fill="#7a4a22" stroke="#4e2c12" stroke-width="8"/>' + "".join(f'<ellipse cx="{x}" cy="{y}" rx="9" ry="6" fill="#3a2010"/>' for x in range(-50, 60, 25) for y in range(-50, 60, 25) if x * x + y * y < 3400) + '</g></g>'
            f'<g transform="scale({seed_scale})"><g id="{pid}-seed"><path d="M-70 4 C-74 -42 -18 -56 14 -46 C52 -34 80 -20 76 14 C70 48 18 52 -14 44 C-48 36 -68 28 -70 4Z" fill="#b07a42" stroke="#6e4526" stroke-width="8"/>'
            f'<path d="M-20 -28 C10 -38 44 -28 58 -10" stroke="#d6a26a" stroke-width="9" fill="none" stroke-linecap="round" opacity=".8"/></g>'
            f'<g id="{pid}-crack" opacity="0"><path d="M-40 -40 l14 20 l-10 16 l14 18" stroke="#3a2010" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g></g></g>')


def drop(pid, col="#7fd0f5"):
    """One drop of water."""
    return f'<g id="{pid}"><path d="M0 -70 C34 -24 46 0 46 22 A46 46 0 0 1 -46 22 C-46 0 -34 -24 0 -70Z" fill="{col}" stroke="#2f80c0" stroke-width="8"/><ellipse cx="-16" cy="16" rx="10" ry="16" fill="#fff" opacity=".75"/></g>'


def puff(pid):
    """Air: three soft swirls."""
    return f'<g id="{pid}">' + "".join(f'<path d="M-120 {y} q60 -36 120 0 q60 36 120 0 q40 -24 70 -8" stroke="#fff" stroke-width="16" fill="none" stroke-linecap="round" opacity=".95"/>' for y in (-70, 0, 70)) + '</g>'


def warm_sun(pid):
    """A friendly warm sun (rays group -rays)."""
    rays = "".join(f'<path d="M0 -140 L0 -196" stroke="#ffb020" stroke-width="18" stroke-linecap="round" transform="rotate({k * 30})"/>' for k in range(12))
    return (f'<g id="{pid}"><g id="{pid}-rays">{rays}</g><circle r="112" fill="{SUN}" stroke="#ffb020" stroke-width="12"/>'
            f'<circle cx="-36" cy="-14" r="11" fill="{INK}"/><circle cx="36" cy="-14" r="11" fill="{INK}"/><path d="M-40 30 Q0 62 40 30" stroke="{INK}" stroke-width="10" fill="none" stroke-linecap="round"/>'
            f'<ellipse cx="-62" cy="22" rx="16" ry="9" fill="#ff8fb1" opacity=".8"/><ellipse cx="62" cy="22" rx="16" ry="9" fill="#ff8fb1" opacity=".8"/></g>')


def pot(pid):
    """A clay pot of soil (the growth prop stands in it at (0, -112))."""
    return (f'<g id="{pid}"><path d="M-130 -170 L-100 0 H100 L130 -170Z" fill="#d9773f" stroke="#8a4320" stroke-width="10" stroke-linejoin="round"/>'
            f'<rect x="-150" y="-210" width="300" height="50" rx="12" fill="#e8894f" stroke="#8a4320" stroke-width="10"/><ellipse cx="0" cy="-210" rx="128" ry="18" fill="{SOIL[1]}"/>'
            f'<path d="M-90 -150 L-70 -30" stroke="#f0a070" stroke-width="12" stroke-linecap="round" opacity=".6"/></g>')


def can(pid):
    """A small blue watering can, spout to the right; -water is the little stream of drops (opacity)."""
    return (f'<g id="{pid}"><g id="{pid}-water" opacity="0">' + "".join(f'<path d="M{x} {y} q8 14 0 22 q-8 -8 0 -22Z" fill="#7fd0f5" stroke="#2f80c0" stroke-width="3"/>' for x, y in ((212, -40), (226, 0), (206, 30), (230, 56)))
            + f'</g><path d="M60 -80 L210 -150 L222 -132 L80 -40Z" fill="{B2}" stroke="{NAVY}" stroke-width="8" stroke-linejoin="round"/>'
            f'<ellipse cx="216" cy="-142" rx="22" ry="12" fill="{ACC}" stroke="{NAVY}" stroke-width="6" transform="rotate(-24 216 -142)"/>'
            f'<rect x="-110" y="-150" width="190" height="150" rx="28" fill="{B2}" stroke="{NAVY}" stroke-width="9"/><path d="M-80 -150 C-80 -230 50 -230 50 -150" stroke="{NAVY}" stroke-width="22" fill="none"/>'
            f'<path d="M-80 -150 C-80 -230 50 -230 50 -150" stroke="{STEEL}" stroke-width="10" fill="none"/><rect x="-80" y="-110" width="30" height="80" rx="12" fill="#fff" opacity=".35"/></g>')


def sunflower(pid, h=520):
    """A tall sunflower with its seed head (-head; the seeds -s0.. -s2 can drop out). Feet at y = 0."""
    return (f'<g id="{pid}"><path d="M0 0 C-10 {-h * .4:.0f} 14 {-h * .7:.0f} 0 {-h}" stroke="{GREEN[1]}" stroke-width="22" fill="none" stroke-linecap="round"/>'
            f'<ellipse cx="-70" cy="{-h * .35:.0f}" rx="76" ry="28" fill="{GREEN[0]}" stroke="{GREEN[1]}" stroke-width="7" transform="rotate(-24 -70 {-h * .35:.0f})"/>'
            f'<ellipse cx="74" cy="{-h * .55:.0f}" rx="76" ry="28" fill="{GREEN[0]}" stroke="{GREEN[1]}" stroke-width="7" transform="rotate(24 74 {-h * .55:.0f})"/>'
            f'<g id="{pid}-head" transform="translate(0 {-h})">' + "".join(f'<ellipse cx="0" cy="-118" rx="32" ry="60" fill="{SUN}" stroke="#e8a000" stroke-width="6" transform="rotate({a})"/>' for a in range(0, 360, 30))
            + f'<circle r="84" fill="#7a4a22" stroke="#4e2c12" stroke-width="8"/>' + "".join(f'<ellipse cx="{x}" cy="{y}" rx="10" ry="7" fill="#3a2010"/>' for x in range(-60, 70, 24) for y in range(-60, 70, 24) if x * x + y * y < 4400)
            + '</g></g>')


def seed_small(pid):
    """One sunflower seed (striped), for counting."""
    return (f'<g id="{pid}"><path d="M0 -50 C30 -30 34 20 0 50 C-34 20 -30 -30 0 -50Z" fill="#3a2a20" stroke="#1c120c" stroke-width="6"/>'
            f'<path d="M-10 -30 C-14 0 -10 26 -4 40 M10 -30 C14 0 10 26 4 40" stroke="#e8e0d0" stroke-width="5" fill="none" stroke-linecap="round"/></g>')


def magnifier(pid):
    """A big magnifying glass, handle down-left."""
    return (f'<g id="{pid}"><path d="M-60 60 L-190 190" stroke="{NAVY}" stroke-width="44" stroke-linecap="round"/><path d="M-60 60 L-190 190" stroke="{ORANGE}" stroke-width="26" stroke-linecap="round"/>'
            f'<circle r="120" fill="#bff9ff" fill-opacity=".25" stroke="{NAVY}" stroke-width="34"/><circle r="120" fill="none" stroke="{SILVER}" stroke-width="18"/>'
            f'<path d="M-60 -60 Q-20 -96 30 -90" stroke="#fff" stroke-width="14" fill="none" stroke-linecap="round" opacity=".8"/></g>')


def label(pid, text, col=ACC, w=None):
    """A little label tag with a word (for the parts of a seed)."""
    w = w or 40 + 34 * len(text)
    return (f'<g id="{pid}"><rect x="{-w / 2}" y="-44" width="{w}" height="88" rx="22" fill="#fff" stroke="{NAVY}" stroke-width="8"/>'
            f'<text x="0" y="22" text-anchor="middle" font-family="Baloo" font-size="62" fill="{B1}">{text}</text></g>')


def kitchen_leaf(pid):
    """A big leaf, the plant's little kitchen, with a glowing food cube on it (the food it makes): -food (opacity)."""
    return (f'<g id="{pid}"><path d="M-260 40 C-160 -160 140 -200 280 -40 C140 120 -120 160 -260 40Z" fill="{GREEN[0]}" stroke="{GREEN[1]}" stroke-width="12" stroke-linejoin="round"/>'
            f'<path d="M-240 36 Q0 -40 260 -38" stroke="{GREEN[1]}" stroke-width="10" fill="none" stroke-linecap="round"/>'
            + "".join(f'<path d="M{x} {-10 - k * 8} q34 -44 80 -56" stroke="{GREEN[1]}" stroke-width="7" fill="none" stroke-linecap="round"/>' for k, x in enumerate((-140, -40, 60, 150)))
            + f'<g id="{pid}-food" opacity="0"><circle cx="20" cy="-10" r="70" fill="#fff36b" opacity=".45"/><rect x="-24" y="-54" width="88" height="88" rx="16" fill="#fff" stroke="{B1}" stroke-width="8"/>'
            f'<path d="M-24 -20 h88 M20 -54 v88" stroke="#dce6f8" stroke-width="6"/></g></g>')


def cycle(pid):
    """The circle of a plant's life: seed (top), sprout (right), plant (bottom), flower (left), arrows between. -k0..-k3 are the four pictures."""
    pos = ((0, -300), (330, 0), (0, 300), (-330, 0))
    ring = "".join(f'<path d="M{a[0] * .7 + b[0] * .3:.0f} {a[1] * .7 + b[1] * .3:.0f} Q{(a[0] + b[0]) * .62:.0f} {(a[1] + b[1]) * .62:.0f} {a[0] * .3 + b[0] * .7:.0f} {a[1] * .3 + b[1] * .7:.0f}" stroke="{ACC}" stroke-width="16" fill="none" stroke-linecap="round"/>'
                   for a, b in zip(pos, pos[1:] + pos[:1]))
    heads = "".join(f'<circle cx="{a[0] * .3 + b[0] * .7:.0f}" cy="{a[1] * .3 + b[1] * .7:.0f}" r="16" fill="{ACC}"/>' for a, b in zip(pos, pos[1:] + pos[:1]))
    pics = [f'<g transform="scale(.55)">{seed(pid + "a")}</g>', f'<g transform="translate(0 60)"><ellipse cx="0" cy="0" rx="80" ry="20" fill="{SOIL[1]}"/><path d="M0 0 V-120" stroke="{GREEN[1]}" stroke-width="12"/><ellipse cx="-34" cy="-118" rx="36" ry="15" fill="{GREEN[0]}" stroke="{GREEN[1]}" stroke-width="5"/><ellipse cx="34" cy="-118" rx="36" ry="15" fill="{GREEN[0]}" stroke="{GREEN[1]}" stroke-width="5"/></g>',
            f'<g transform="translate(0 110) scale(.5)">{_pot(0, 0, 1.6, 2)}</g>', f'<g transform="translate(0 130) scale(.32)">{sunflower(pid + "d", 420)}</g>']
    body = "".join(f'<g id="{pid}-k{k}" transform="translate({x} {y})"><circle r="128" fill="#fff" stroke="{NAVY}" stroke-width="10"/>{pics[k]}</g>' for k, (x, y) in enumerate(pos))
    return f'<g id="{pid}">{ring}{heads}{body}</g>'


def arrow(pid, x1, y1, x2, y2, col=ACC): return art.arrow(pid, x1, y1, x2, y2, col)
