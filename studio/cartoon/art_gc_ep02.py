"""Art for gc_ep02 "How Do Rockets Fly?" (Gizmo Explains, Nov 21 2026): two new places (gpad: a launch field seen from far away; gsky: high in the
sky among the clouds; gspace: space above the Earth) and the props (a cartoon rocket in three stages with its hot gas, a jet plane that takes in air,
a satellite, the Moon, a cutaway rocket with its fuel tank). Registered from here the way art_gizmo.py does: nothing that exists changes.
The rocket's exhaust is drawn as puffy hot GAS (white and cream clouds with a warm glow at the nozzle), never as a fire a child could copy.
Props are drawn around (0, 0); the rocket stands with the bottom of its engine on y = 0."""
import art, art2, kit
from art import INK, SUN
from art_gizmo import NAVY, SCREEN, CYAN, ACC, ORANGE, SILVER, STEEL, B1, B2, GREEN, _grad, _flower

RED = "#ff6b5a"; CREAM = "#fff3d6"


# ================================================================== places
def bg_gpad(p):
    """A launch field seen from far away: a wide sky, far hills, a white launch tower with the pad at (1300, 800); Gizmo watches from the grass on the left."""
    far = (_grad(f"{p}s", B2, "#bfe6ff") + f'<rect x="-600" y="-900" width="3120" height="1800" fill="url(#{p}s)"/>'
           + f'<circle cx="300" cy="150" r="80" fill="{SUN}"/><circle cx="300" cy="150" r="120" fill="{SUN}" opacity=".22"/>'
           + f'<ellipse cx="900" cy="130" rx="130" ry="40" fill="#fff"/><ellipse cx="980" cy="104" rx="80" ry="38" fill="#fff"/><ellipse cx="1750" cy="220" rx="110" ry="34" fill="#fff" opacity=".9"/>'
           + f'<path d="M-600 640 C-100 560 400 600 900 580 S1800 560 2520 600 V900 H-600Z" fill="#8fd08a"/>'
           + f'<path d="M-600 690 C200 650 900 680 1500 660 S2200 670 2520 670 V900 H-600Z" fill="#74c06f"/>')
    tower = (f'<g transform="translate(1530 800)"><rect x="-40" y="-640" width="80" height="640" fill="none" stroke="{SILVER}" stroke-width="14"/>'
             + "".join(f'<path d="M-40 {-y} L40 {-y - 80} M40 {-y} L-40 {-y - 80}" stroke="{SILVER}" stroke-width="8"/>' for y in range(0, 640, 80))
             + f'<rect x="-50" y="-660" width="100" height="24" rx="6" fill="{ORANGE}" stroke="{NAVY}" stroke-width="6"/>'
             + f'<path d="M-40 -520 H-150 M-40 -330 H-150" stroke="{SILVER}" stroke-width="12"/></g>')
    mid = (tower + f'<path d="M1060 800 h480 l40 40 h-560z" fill="#b8c2d6" stroke="{NAVY}" stroke-width="8"/>'
           + f'<path d="M-600 760 C200 720 900 750 1500 740 S2200 750 2520 750 V900 H-600Z" fill="#62b85a"/>'
           + "".join(f'<rect x="{x}" y="770" width="16" height="70" rx="6" fill="#fff" stroke="#c9d3e6" stroke-width="3"/>' for x in range(-560, 900, 70))
           + f'<rect x="-600" y="784" width="1500" height="10" fill="#fff"/>')
    near = (f'<rect x="-600" y="840" width="3120" height="1300" fill="#55ad55"/>'
            + "".join(_flower(x, y, .9, c) for x, y, c in ((-300, 1000, "#ff7aa2"), (120, 1050, SUN), (700, 1000, ACC), (1700, 1040, "#fff"), (2100, 990, "#ff7aa2")))
            + "".join(f'<path d="M{x} 1100 l-8 -34 M{x + 10} 1100 l2 -40 M{x + 20} 1100 l12 -30" stroke="#3f9e3c" stroke-width="7" stroke-linecap="round"/>' for x in range(-560, 2500, 100)))
    return far, mid, near


def bg_gsky(p):
    """High in the sky: deep blue at the top, soft clouds below, the ground far down."""
    far = (_grad(f"{p}s", "#1d3a8a", "#8fd0ff") + f'<rect x="-600" y="-900" width="3120" height="2100" fill="url(#{p}s)"/>'
           + "".join(f'<circle cx="{x}" cy="{y}" r="4" fill="#fff" opacity=".6"/>' for x, y in ((100, 40), (420, 120), (760, 30), (1180, 90), (1600, 50), (1850, 140), (300, -60), (1400, -40)))
           + f'<path d="M-600 1000 C0 960 800 990 1400 970 S2200 980 2520 980 V1300 H-600Z" fill="#7cc96f" opacity=".7"/>')
    cl = lambda x, y, s, o=1: (f'<g transform="translate({x} {y}) scale({s})" opacity="{o}"><ellipse cx="0" cy="0" rx="200" ry="60" fill="#fff"/><ellipse cx="-80" cy="-40" rx="110" ry="70" fill="#fff"/>'
                               f'<ellipse cx="70" cy="-50" rx="130" ry="80" fill="#fff"/><ellipse cx="0" cy="20" rx="210" ry="40" fill="#e6f2ff"/></g>')
    mid = cl(220, 640, 1.1, .95) + cl(1700, 560, 1.0, .95) + cl(800, 860, 1.4) + cl(-300, 900, 1.2) + cl(2200, 880, 1.3)
    near = cl(300, 1060, 1.6) + cl(1500, 1080, 1.8)
    return far, mid, near


def bg_gspace(p):
    """Space: a dark blue sky full of stars, the round edge of the Earth at the bottom (the Moon is a prop: drawn in the backdrop it showed twice, stills r1)."""
    stars = "".join(f'<circle cx="{(k * 397) % 3000 - 540}" cy="{(k * 233) % 1500 - 420}" r="{3 + k % 4}" fill="#fff" opacity="{.5 + (k % 5) / 10}"/>' for k in range(120))
    far = (f'<rect x="-600" y="-900" width="3120" height="2100" fill="#0e1a4a"/>' + stars
)
    mid = (f'<circle cx="960" cy="2700" r="1800" fill="#3d8de0" stroke="#9fd8ff" stroke-width="30"/>'
           + f'<path d="M-200 1000 C100 940 300 980 500 960 C600 1010 700 1040 760 1100 H-200Z" fill="#62b85a"/>'
           + f'<path d="M1300 980 C1450 950 1650 960 1800 1000 L1900 1100 H1250Z" fill="#62b85a"/>'
           + f'<ellipse cx="900" cy="980" rx="160" ry="22" fill="#fff" opacity=".8"/><ellipse cx="1500" cy="1040" rx="120" ry="18" fill="#fff" opacity=".8"/>')
    return far, mid, ""


art.BG.update({"gpad": bg_gpad, "gsky": bg_gsky, "gspace": bg_gspace})
art.PLACE.update({"gpad": "the launch field (far away)", "gsky": "high in the sky", "gspace": "space above the Earth"})


# ================================================================== props
def _gas(pid, y0, s=1.0, opacity="0"):
    """Hot gas rushing out of the nozzle: a warm glow at the nozzle and puffy cream and white clouds below it (no flames)."""
    return (f'<g id="{pid}" opacity="{opacity}"><g transform="translate(0 {y0}) scale({s})">'
            f'<path d="M-44 0 Q0 90 44 0Z" fill="{SUN}" stroke="#ffb020" stroke-width="6"/>'
            f'<ellipse cx="0" cy="40" rx="56" ry="34" fill="#ffd98a"/>'
            f'<g id="{pid}-p">' + "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}" stroke="#d9cbb0" stroke-width="5"/>' for x, y, r, c in
                                         ((0, 100, 70, CREAM), (-70, 150, 60, "#fff"), (70, 150, 62, "#fff"), (-20, 190, 66, CREAM), (40, 230, 56, "#fff"), (-60, 240, 48, "#fff")))
            + '</g></g></g>')


def rocket(pid, stages=True):
    """A cartoon rocket in three stages, bottom of the engine at y = 0: -s3 (bottom stage, fins, engine), -s2 (middle stage), -top (the nose with a
    round window). -g3 is the hot gas under the bottom stage, -g2 the gas under the middle stage once the bottom stage has dropped away (both opacity 0).
    -fuel lights the tank inside the bottom stage (opacity, the cutaway look)."""
    s3 = (f'<g id="{pid}-s3"><path d="M-100 -260 L-110 -40 L-170 30 L-170 70 L-86 20 H86 L170 70 L170 30 L110 -40 L100 -260Z" fill="{RED}" stroke="{NAVY}" stroke-width="10" stroke-linejoin="round"/>'
          f'<rect x="-100" y="-260" width="200" height="240" fill="{SILVER}" stroke="{NAVY}" stroke-width="10"/><rect x="-100" y="-200" width="200" height="34" fill="{ORANGE}"/>'
          f'<rect x="-80" y="-246" width="22" height="200" rx="10" fill="#fff" opacity=".6"/>'
          f'<path d="M-56 -20 L-70 30 H70 L56 -20Z" fill="{STEEL}" stroke="{NAVY}" stroke-width="9" stroke-linejoin="round"/>'
          f'<g id="{pid}-fuel" opacity="0"><rect x="-60" y="-150" width="120" height="110" rx="20" fill="{ORANGE}" stroke="{NAVY}" stroke-width="7"/>'
          f'<path d="M0 -130 C22 -100 28 -88 28 -78 A28 28 0 0 1 -28 -78 C-28 -88 -22 -100 0 -130Z" fill="#fff36b" stroke="{NAVY}" stroke-width="5"/></g></g>')
    s2 = (f'<g id="{pid}-s2"><rect x="-90" y="-460" width="180" height="200" fill="{SILVER}" stroke="{NAVY}" stroke-width="10"/><rect x="-90" y="-400" width="180" height="30" fill="{B2}"/>'
          f'<rect x="-72" y="-448" width="20" height="170" rx="9" fill="#fff" opacity=".6"/><path d="M-40 -262 L-48 -236 H48 L40 -262Z" fill="{STEEL}" stroke="{NAVY}" stroke-width="7"/></g>')
    top = (f'<g id="{pid}-top"><path d="M-90 -460 C-90 -560 -40 -640 0 -700 C40 -640 90 -560 90 -460Z" fill="#fff" stroke="{NAVY}" stroke-width="10" stroke-linejoin="round"/>'
           f'<path d="M-26 -660 C-12 -684 12 -684 26 -660 C14 -680 0 -700 0 -700 C0 -700 -14 -680 -26 -660Z" fill="{RED}" stroke="{NAVY}" stroke-width="6"/>'
           f'<path d="M-90 -480 H90" stroke="{RED}" stroke-width="16"/>'
           f'<circle cx="0" cy="-560" r="40" fill="{CYAN}" stroke="{NAVY}" stroke-width="10"/><circle cx="-12" cy="-574" r="11" fill="#fff"/></g>')
    return f'<g id="{pid}">{_gas(pid + "-g3", 30, 1.2)}{_gas(pid + "-g2", -236, .8)}{s3}{s2}{top}</g>'


def rocket_small(pid):
    """A small rocket far away (one piece), for the sky and the launch field: -g is its gas (opacity 0)."""
    return (f'<g id="{pid}">{_gas(pid + "-g", 26, .7)}'
            f'<path d="M-50 -40 L-90 20 L-50 0Z M50 -40 L90 20 L50 0Z" fill="{RED}" stroke="{NAVY}" stroke-width="8" stroke-linejoin="round"/>'
            f'<path d="M-50 0 V-260 C-50 -320 -20 -360 0 -390 C20 -360 50 -320 50 -260 V0Z" fill="#fff" stroke="{NAVY}" stroke-width="9" stroke-linejoin="round"/>'
            f'<circle cx="0" cy="-250" r="22" fill="{CYAN}" stroke="{NAVY}" stroke-width="7"/><path d="M-50 -120 H50" stroke="{RED}" stroke-width="12"/>'
            f'<path d="M-30 0 L-36 26 H36 L30 0Z" fill="{STEEL}" stroke="{NAVY}" stroke-width="7"/></g>')


def jet(pid):
    """A little jet plane flying right; -air is the air it takes in at the front of its engine (swirls, opacity 0)."""
    return (f'<g id="{pid}"><g id="{pid}-air" opacity="0">' + "".join(f'<path d="M{-40 + k * 20} {y} q40 -20 80 0 q30 14 60 0" stroke="#fff" stroke-width="12" fill="none" stroke-linecap="round" transform="translate(260 0)"/>' for k, y in enumerate((30, 70, 110))) + '</g>'
            f'<path d="M-280 -10 C-200 -50 160 -54 250 -20 C290 -6 290 20 250 30 C160 50 -200 46 -280 20Z" fill="#fff" stroke="{NAVY}" stroke-width="10"/>'
            f'<path d="M-40 10 L-140 150 H-60 L80 14Z" fill="{B2}" stroke="{NAVY}" stroke-width="9" stroke-linejoin="round"/>'
            f'<path d="M-40 -20 L-110 -120 H-60 L40 -24Z" fill="{B2}" stroke="{NAVY}" stroke-width="8" stroke-linejoin="round"/>'
            f'<path d="M-230 -20 L-290 -130 H-240 L-180 -30Z" fill="{RED}" stroke="{NAVY}" stroke-width="8" stroke-linejoin="round"/>'
            + "".join(f'<circle cx="{x}" cy="-6" r="13" fill="{CYAN}" stroke="{NAVY}" stroke-width="5"/>' for x in (-140, -90, -40, 10, 60, 110))
            + f'<path d="M190 -26 C220 -26 250 -16 262 -4 L200 -4Z" fill="{CYAN}" stroke="{NAVY}" stroke-width="6"/>'
            f'<rect x="-50" y="56" width="160" height="56" rx="26" fill="{STEEL}" stroke="{NAVY}" stroke-width="8"/><ellipse cx="110" cy="84" rx="14" ry="26" fill="{NAVY}"/></g>')


def satellite(pid):
    """A satellite with two blue solar panels and a little dish."""
    panel = lambda x: (f'<g transform="translate({x} 0)"><rect x="-90" y="-50" width="180" height="100" rx="8" fill="{B2}" stroke="{NAVY}" stroke-width="8"/>'
                       f'<path d="M-30 -50 V50 M30 -50 V50 M-90 0 H90" stroke="{ACC}" stroke-width="5"/></g>')
    return (f'<g id="{pid}">{panel(-170)}{panel(170)}<path d="M-80 0 H80" stroke="{NAVY}" stroke-width="12"/>'
            f'<rect x="-60" y="-70" width="120" height="140" rx="16" fill="{SUN}" stroke="{NAVY}" stroke-width="9"/>'
            f'<path d="M0 -70 V-110" stroke="{NAVY}" stroke-width="9"/><path d="M-36 -130 Q0 -90 36 -130Z" fill="{SILVER}" stroke="{NAVY}" stroke-width="7"/></g>')


def moon(pid):
    """The Moon, round and grey with craters."""
    return (f'<g id="{pid}"><circle r="150" fill="#e8ecf4" stroke="#b6bfd2" stroke-width="12"/><circle cx="-50" cy="-30" r="32" fill="#cfd6e4"/>'
            f'<circle cx="56" cy="40" r="24" fill="#cfd6e4"/><circle cx="30" cy="-70" r="16" fill="#cfd6e4"/><circle cx="-40" cy="70" r="18" fill="#cfd6e4"/></g>')


def updown(pid):
    """Two big arrows on the board: -dn (the gas goes down, cream) and -upa (the rocket goes up, cyan), opacity 0 each."""
    return (f'<g id="{pid}"><g id="{pid}-dn" opacity="0"><path d="M0 -60 V120" stroke="{CREAM}" stroke-width="40" stroke-linecap="round"/><path d="M-70 90 L0 170 L70 90Z" fill="{CREAM}"/></g>'
            f'<g id="{pid}-upa" opacity="0"><path d="M0 60 V-120" stroke="{ACC}" stroke-width="40" stroke-linecap="round"/><path d="M-70 -90 L0 -170 L70 -90Z" fill="{ACC}"/></g></g>')


def hands(pid):
    """Two cartoon hands pushing against each other (a push and a push back): -l and -r move toward the middle."""
    hand = lambda s, hid: (f'<g id="{pid}-{hid}"><g transform="scale({s} 1)"><path d="M-260 -40 H-110 V40 H-260Z" fill="{SILVER}" stroke="{NAVY}" stroke-width="9"/>'
                           f'<rect x="-120" y="-90" width="100" height="180" rx="40" fill="#ffd2a8" stroke="{NAVY}" stroke-width="9"/>'
                           + "".join(f'<path d="M-30 {y} h26" stroke="{NAVY}" stroke-width="7" stroke-linecap="round"/>' for y in (-50, -10, 30)) + '</g></g>')
    return f'<g id="{pid}">{hand(1, "l")}{hand(-1, "r")}</g>'


def boxload(pid, n=3):
    """Heavy boxes to load a rocket with (for 'a heavier rocket needs a bigger push'); -b0.. each box."""
    return f'<g id="{pid}">' + "".join(f'<g id="{pid}-b{k}"><rect x="{-60 + (k % 2) * 30 - 30}" y="{-110 * (k + 1)}" width="120" height="100" rx="12" fill="#c98a4a" stroke="{NAVY}" stroke-width="8"/>'
                                       f'<path d="M{-60 + (k % 2) * 30 - 30} {-110 * (k + 1) + 50} h120" stroke="#8a5a2a" stroke-width="7"/></g>' for k in range(n)) + '</g>'
