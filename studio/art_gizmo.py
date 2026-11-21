"""Original art for Gizmo Explains: how things work. Bright outdoor/workshop scenes, simple cutaway diagrams.
1080x1100 frame, ground ~y1000. Keys prefixed gz_."""
import math

def svg(body):
    return f'<svg viewBox="0 0 1080 1100" width="1080" height="1100">{body}</svg>'

def sky_env():
    return ('<circle cx="-280" cy="200" r="90" fill="#fff59d"/>'
            '<g fill="#fff" opacity=".9"><ellipse cx="1300" cy="220" rx="140" ry="50"/><ellipse cx="1240" cy="190" rx="70" ry="50"/><ellipse cx="-300" cy="420" rx="120" ry="40"/></g>'
            '<path d="M-500 940 Q-200 880 100 930 T700 920 T1600 910 L1600 1110 L-500 1110Z" fill="#7cc576"/>'
            '<path d="M-500 1000 Q0 970 540 995 T1600 990 L1600 1110 L-500 1110Z" fill="#5fae5a"/>')

def lab_env():
    return ('<rect x="-500" y="0" width="2200" height="1100" fill="#dfe9ff"/>'
            + "".join(f'<path d="M{x} 0 V1000" stroke="#c9d8fb" stroke-width="3"/>' for x in range(-480, 1600, 120))
            + "".join(f'<path d="M-500 {y} H1600" stroke="#c9d8fb" stroke-width="3"/>' for y in range(60, 1000, 120))
            + '<rect x="-500" y="990" width="2200" height="120" fill="#8a9bc7"/><rect x="-500" y="980" width="2200" height="20" fill="#6d7fb0"/>'
            '<g transform="translate(-380 700)"><rect width="180" height="280" rx="14" fill="#5a6ea8"/><circle cx="90" cy="70" r="30" fill="#5ff3ff"/><rect x="30" y="140" width="120" height="16" rx="8" fill="#9fb1e0"/></g>'
            '<g transform="translate(1280 760)"><rect width="200" height="220" rx="14" fill="#5a6ea8"/><path d="M40 60 h120 M40 110 h90 M40 160 h110" stroke="#9fb1e0" stroke-width="14" stroke-linecap="round"/></g>')

def face(cx, cy, s=1.0):
    ex = 42 * s
    return (f'<circle cx="{cx-ex:.0f}" cy="{cy:.0f}" r="{24*s:.0f}" fill="#fff"/><circle cx="{cx+ex:.0f}" cy="{cy:.0f}" r="{24*s:.0f}" fill="#fff"/>'
            f'<circle cx="{cx-ex+4*s:.0f}" cy="{cy+3*s:.0f}" r="{13*s:.0f}" fill="#1a1a2e"/><circle cx="{cx+ex+4*s:.0f}" cy="{cy+3*s:.0f}" r="{13*s:.0f}" fill="#1a1a2e"/>'
            f'<circle cx="{cx-ex+8*s:.0f}" cy="{cy-3*s:.0f}" r="{5*s:.0f}" fill="#fff"/><circle cx="{cx+ex+8*s:.0f}" cy="{cy-3*s:.0f}" r="{5*s:.0f}" fill="#fff"/>'
            f'<path d="M{cx-24*s:.0f} {cy+38*s:.0f} q{24*s:.0f} {20*s:.0f} {48*s:.0f} 0" stroke="#4a2a2a" stroke-width="{7*s:.0f}" fill="none" stroke-linecap="round"/>')

def arrows(pts, c="#3561d9"):
    out = ""
    for x1, y1, x2, y2 in pts:
        a = math.atan2(y2 - y1, x2 - x1)
        hx, hy = x2 - 30 * math.cos(a), y2 - 30 * math.sin(a)
        out += (f'<path d="M{x1} {y1} L{hx:.0f} {hy:.0f}" stroke="{c}" stroke-width="14" stroke-linecap="round" stroke-dasharray="4 22"/>'
                f'<path d="M{x2} {y2} L{hx-18*math.sin(a):.0f} {hy+18*math.cos(a):.0f} L{hx+18*math.sin(a):.0f} {hy-18*math.cos(a):.0f}Z" fill="{c}"/>')
    return out

def label(x, y, t, c="#1d3a8a"):
    w = 24 * len(t) + 40
    return f'<rect x="{x-w/2:.0f}" y="{y-34}" width="{w}" height="56" rx="28" fill="#fff" stroke="{c}" stroke-width="5"/><text x="{x}" y="{y+8}" text-anchor="middle" font-family="Baloo, sans-serif" font-weight="800" font-size="38" fill="{c}">{t}</text>'

def sparkles(pts, c="#fff59d"):
    return "".join(f'<path d="M{x} {y-30} L{x+8} {y-8} L{x+30} {y} L{x+8} {y+8} L{x} {y+30} L{x-8} {y+8} L{x-30} {y} L{x-8} {y-8}Z" fill="{c}"/>' for x, y in pts)

def scene(body, fx="", fx2="", env=sky_env):
    return svg(env() + f'<g id="animal">{body}</g><g id="fx" opacity="0">{fx}</g><g id="fx2" opacity="0">{fx2}</g>')

def drop(x, y, s=1.0, c="#4fa8ff"):
    return f'<path d="M{x} {y-60*s:.0f} Q{x+45*s:.0f} {y:.0f} {x} {y+30*s:.0f} Q{x-45*s:.0f} {y:.0f} {x} {y-60*s:.0f}Z" fill="{c}"/>'

CLOUD_P = "M260 640 Q200 520 320 480 Q330 340 480 360 Q560 240 690 340 Q840 320 840 470 Q940 520 880 640Z"

# ---------- weather ----------
RAIN = scene(f'<path d="{CLOUD_P}" fill="#cfd8e6" stroke="#8e9bb3" stroke-width="10"/>' + face(560, 500, 1.0)
             + "".join(drop(x, y, .8) for x, y in ((320, 760), (450, 840), (580, 760), (710, 850), (820, 760), (380, 930), (650, 940))),
             '<path d="M100 980 Q300 900 520 960" stroke="#4fa8ff" stroke-width="14" fill="none"/>' + arrows([(160, 300, 300, 180), (920, 300, 800, 180)], "#ff8a3d") + label(540, 160, "WATER GOES UP"),
             '<ellipse cx="540" cy="1010" rx="300" ry="40" fill="#4fa8ff" opacity=".7"/>' + label(540, 250, "DROPS FALL DOWN"))
RAINBOW = scene("".join(f'<path d="M{140+i*36} 960 A{400-i*36} {400-i*36} 0 0 1 {940-i*36} 960" stroke="{c}" stroke-width="36" fill="none"/>' for i, c in enumerate(("#ff4d4d", "#ff9f40", "#ffe14d", "#5fd36a", "#4fa8ff", "#6a5cff", "#b25cff")))
                + face(540, 840, .9),
                '<circle cx="180" cy="300" r="90" fill="#ffd54f"/>' + "".join(drop(x, 330, .6) for x in (780, 860, 940)) + label(540, 200, "SUN + RAIN"),
                '<g transform="translate(860 360)"><path d="M-90 80 L0 -80 L90 80Z" fill="#e3f2fd" stroke="#64b5f6" stroke-width="8"/>'
                + "".join(f'<path d="M40 {10+i*10} L160 {-40+i*24}" stroke="{c}" stroke-width="9"/>' for i, c in enumerate(("#ff4d4d", "#ff9f40", "#ffe14d", "#5fd36a", "#4fa8ff", "#6a5cff"))) + '<path d="M-200 30 L-30 20" stroke="#fff" stroke-width="12"/></g>')
LIGHTNING = scene(f'<path d="{CLOUD_P}" fill="#7d8aa6" stroke="#4f5b78" stroke-width="10"/>' + face(560, 500, 1.0)
                  + '<path d="M560 640 L480 820 L560 820 L500 990 L680 760 L590 760 L650 640Z" fill="#ffe14d" stroke="#f5a623" stroke-width="8" stroke-linejoin="round"/>',
                  sparkles([(300, 800), (820, 840), (420, 960)], "#fff59d") + label(540, 180, "FLASH!"),
                  '<text x="680" y="300" font-family="Baloo, sans-serif" font-weight="800" font-size="100" fill="#4f5b78">BOOM</text>' + label(260, 220, "THEN THUNDER"))
SNOW = scene('<path d="M-500 900 Q540 820 1600 900 L1600 1110 L-500 1110Z" fill="#fff"/>'
             '<circle cx="540" cy="840" r="160" fill="#fff" stroke="#c5d6ee" stroke-width="8"/><circle cx="540" cy="600" r="120" fill="#fff" stroke="#c5d6ee" stroke-width="8"/>'
             '<path d="M540 610 L620 630 L540 645Z" fill="#ff8a3d"/><path d="M420 720 Q540 760 660 720 L650 760 Q540 800 430 760Z" fill="#e53935"/>' + face(540, 580, .8)
             + '<path d="M420 820 L300 740 M660 820 L780 740" stroke="#795548" stroke-width="14" stroke-linecap="round"/>',
             "".join(f'<g transform="translate({x} {y})"><path d="M0 -40 V40 M-35 -20 L35 20 M-35 20 L35 -20" stroke="#bfe3ff" stroke-width="10" stroke-linecap="round"/></g>' for x, y in ((180, 300), (360, 220), (760, 240), (920, 380), (200, 520), (880, 560))),
             label(540, 160, "COLD = FROZEN WATER"))
WIND = scene('<rect x="530" y="560" width="20" height="440" fill="#9e9e9e"/>'
             + "".join(f'<path d="M540 560 L{540+260*math.cos(math.radians(a)):.0f} {560+260*math.sin(math.radians(a)):.0f} L{540+240*math.cos(math.radians(a+22)):.0f} {560+240*math.sin(math.radians(a+22)):.0f}Z" fill="#fafafa" stroke="#9e9e9e" stroke-width="6"/>' for a in (-90, 30, 150))
             + '<circle cx="540" cy="560" r="44" fill="#5ff3ff" stroke="#3561d9" stroke-width="8"/>' + face(540, 860, .8).replace('cy="860"', 'cy="860"'),
             "".join(f'<path d="M{x} {y} q80 -40 160 0 t160 0" stroke="#bfe3ff" stroke-width="12" fill="none" stroke-linecap="round"/>' for x, y in ((40, 300), (140, 460), (20, 640))),
             label(540, 160, "MOVING AIR"))

# ---------- flying ----------
ROCKET = scene('<path d="M540 300 Q660 420 660 640 L660 860 L420 860 L420 640 Q420 420 540 300Z" fill="#f5f7ff" stroke="#3561d9" stroke-width="10"/>'
               '<circle cx="540" cy="560" r="70" fill="#5ff3ff" stroke="#3561d9" stroke-width="10"/><path d="M420 760 L330 900 L420 870Z M660 760 L750 900 L660 870Z" fill="#ff5a5a" stroke="#b33" stroke-width="8"/>'
               '<path d="M470 300 Q540 240 610 300" fill="#ff5a5a"/>' + face(540, 560, .7),
               '<path d="M450 870 Q540 1100 630 870Z" fill="#ff9f40"/><path d="M490 870 Q540 1020 590 870Z" fill="#ffe14d"/>' + arrows([(860, 900, 860, 600)], "#ff8a3d") + label(860, 980, "PUSH DOWN"),
               arrows([(200, 700, 200, 380)], "#3561d9") + label(200, 300, "GO UP!"), env=sky_env)
PLANE = scene('<path d="M160 640 Q180 560 300 560 L860 560 Q960 570 960 640 Q960 700 860 710 L300 710 Q180 710 160 640Z" fill="#fafafa" stroke="#3561d9" stroke-width="10"/>'
              '<path d="M480 620 L640 380 L720 380 L640 620Z M480 660 L640 900 L720 900 L640 660Z" fill="#9fb8f5" stroke="#3561d9" stroke-width="8"/><path d="M820 560 L900 420 L950 420 L930 580Z" fill="#ff5a5a"/>'
              + "".join(f'<circle cx="{x}" cy="610" r="18" fill="#5ff3ff"/>' for x in (380, 440, 760, 820)) + face(250, 630, .55),
              arrows([(580, 300, 580, 160)], "#3561d9") + label(580, 110, "LIFT"), arrows([(1020, 640, 1060, 640)], "#ff8a3d") + label(860, 980, "WINGS PUSH AIR DOWN"))
BALLOON = scene('<path d="M540 260 Q800 260 800 520 Q800 700 600 800 L480 800 Q280 700 280 520 Q280 260 540 260Z" fill="#ff5a5a" stroke="#b33" stroke-width="10"/>'
                '<path d="M540 260 Q440 500 480 800 M540 260 Q640 500 600 800" stroke="#ffe14d" stroke-width="40" fill="none"/><path d="M480 800 L470 880 M600 800 L610 880" stroke="#795548" stroke-width="8"/>'
                '<rect x="450" y="880" width="180" height="110" rx="16" fill="#c68642" stroke="#8d5524" stroke-width="8"/>' + face(540, 520, .9),
                '<path d="M520 870 Q540 820 560 870 Q540 900 520 870Z" fill="#ff9f40"/>' + arrows([(540, 700, 540, 420)], "#ff8a3d") + label(540, 1060, "HOT AIR RISES"),
                label(860, 300, "UP, UP!"))
HELI = scene('<ellipse cx="540" cy="680" rx="230" ry="150" fill="#ffd54f" stroke="#c99a00" stroke-width="10"/><path d="M740 650 L980 620 L980 680 L760 720Z" fill="#ffd54f" stroke="#c99a00" stroke-width="8"/>'
             '<path d="M420 640 Q460 560 560 560 L560 700 L420 700Z" fill="#5ff3ff" stroke="#3561d9" stroke-width="6"/><rect x="530" y="500" width="20" height="40" fill="#555"/>'
             '<rect x="200" y="480" width="680" height="24" rx="12" fill="#555"/><path d="M380 830 L380 900 M700 830 L700 900 M320 900 H760" stroke="#555" stroke-width="14" stroke-linecap="round"/>' + face(480, 650, .5),
             '<ellipse cx="540" cy="492" rx="420" ry="30" fill="#bfe3ff" opacity=".6"/>' + label(540, 380, "SPINNING BLADES"),
             arrows([(540, 300, 540, 160)], "#3561d9") + label(860, 980, "STRAIGHT UP!"))
KITE = scene('<path d="M540 300 L760 560 L540 860 L320 560Z" fill="#6a5cff" stroke="#3d2fb5" stroke-width="10"/><path d="M540 300 V860 M320 560 H760" stroke="#ffe14d" stroke-width="10"/>'
             '<path d="M540 860 Q500 940 560 980 Q620 1020 580 1080" stroke="#ff5a5a" stroke-width="8" fill="none"/>' + face(540, 560, .8),
             "".join(f'<path d="M{x} {y} q80 -40 160 0 t160 0" stroke="#fff" stroke-width="12" fill="none" stroke-linecap="round"/>' for x, y in ((-60, 400), (-20, 560))) + label(220, 260, "WIND PUSHES"),
             '<path d="M540 860 L900 1080" stroke="#9e9e9e" stroke-width="5"/>' + label(860, 300, "STRING HOLDS"))

# ---------- everyday science (lab) ----------
MAGNET = scene('<path d="M340 400 L340 720 A200 200 0 0 0 740 720 L740 400 L600 400 L600 720 A60 60 0 0 1 480 720 L480 400Z" fill="#ff5a5a" stroke="#b33" stroke-width="10"/>'
               '<rect x="340" y="400" width="140" height="90" fill="#e0e0e0" stroke="#999" stroke-width="8"/><rect x="600" y="400" width="140" height="90" fill="#e0e0e0" stroke="#999" stroke-width="8"/>' + face(540, 800, .7),
               "".join(f'<g transform="translate({x} {y}) rotate({r})"><rect x="-40" y="-10" width="80" height="20" rx="10" fill="#9e9e9e"/></g>' for x, y, r in ((410, 290, 10), (670, 280, -20), (540, 230, 40)))
               + arrows([(410, 220, 410, 330), (670, 210, 670, 330)], "#3561d9"),
               label(540, 140, "PULLS METAL!"), env=lab_env)
BULB = scene('<path d="M540 300 Q740 300 740 520 Q740 620 640 700 L640 780 L440 780 L440 700 Q340 620 340 520 Q340 300 540 300Z" fill="#fff59d" stroke="#f5a623" stroke-width="10"/>'
             '<path d="M480 700 L480 560 Q540 500 600 560 L600 700" stroke="#f57c00" stroke-width="8" fill="none"/>'
             '<rect x="450" y="780" width="180" height="40" rx="10" fill="#9e9e9e"/><rect x="460" y="820" width="160" height="40" rx="10" fill="#bdbdbd"/><rect x="490" y="860" width="100" height="40" rx="14" fill="#757575"/>' + face(540, 460, .8),
             '<circle cx="540" cy="520" r="320" fill="#fff59d" opacity=".25"/>' + "".join(f'<path d="M{540+260*math.cos(math.radians(a)):.0f} {520+260*math.sin(math.radians(a)):.0f} L{540+330*math.cos(math.radians(a)):.0f} {520+330*math.sin(math.radians(a)):.0f}" stroke="#ffd54f" stroke-width="16" stroke-linecap="round"/>' for a in range(180, 361, 30)),
             '<path d="M540 900 V960 H160 V600" stroke="#3561d9" stroke-width="12" fill="none"/><rect x="100" y="520" width="120" height="80" rx="12" fill="#5ff3ff" stroke="#3561d9" stroke-width="6"/>' + label(160, 470, "ELECTRICITY"), env=lab_env)
ICE = scene('<rect x="360" y="460" width="360" height="360" rx="50" fill="#d6f3ff" stroke="#7ec8ec" stroke-width="10" opacity=".95"/><path d="M400 520 L480 500" stroke="#fff" stroke-width="16" stroke-linecap="round"/>' + face(540, 620, .9)
            + '<ellipse cx="540" cy="960" rx="300" ry="40" fill="#9fd8ff" opacity=".8"/>',
            '<circle cx="880" cy="260" r="90" fill="#ffd54f"/>' + drop(400, 880, .6, "#7ec8ec") + drop(700, 900, .5, "#7ec8ec") + label(540, 360, "WARM = MELT"),
            '<g transform="translate(200 300)"><rect x="-30" y="-140" width="60" height="240" rx="30" fill="#fff" stroke="#3561d9" stroke-width="6"/><circle cy="120" r="50" fill="#ff5a5a"/><rect x="-14" y="-60" width="28" height="160" fill="#ff5a5a"/></g>', env=lab_env)
SHADOW = scene('<path d="M540 900 L1200 1000 L1200 1060 L540 1000Z" fill="#3b4a7a" opacity=".45"/>'
               '<rect x="460" y="640" width="160" height="260" rx="40" fill="#ff9f40"/><circle cx="540" cy="540" r="120" fill="#ffd6a5"/><path d="M420 520 Q440 420 540 420 Q640 420 660 520 Q600 470 420 520Z" fill="#5d4037"/>' + face(540, 560, .7),
               '<circle cx="-100" cy="300" r="100" fill="#fff59d"/><path d="M0 330 L460 620 M0 360 L460 900" stroke="#fff59d" stroke-width="10" stroke-dasharray="20 14"/>' + label(220, 220, "LIGHT"),
               label(900, 900, "SHADOW!"))
SOUND = scene('<path d="M300 560 L420 560 L560 440 L560 860 L420 740 L300 740Z" fill="#6a5cff" stroke="#3d2fb5" stroke-width="10" stroke-linejoin="round"/>' + face(420, 650, .55),
              "".join(f'<path d="M{620+i*80} {500-i*40} Q{700+i*100} 650 {620+i*80} {800+i*40}" stroke="#5ff3ff" stroke-width="16" fill="none" stroke-linecap="round"/>' for i in range(3)),
              label(540, 260, "SOUND WAVES WIGGLE THE AIR"), env=lab_env)

# ---------- plants ----------
SEED = scene('<path d="M-500 900 L1600 900 L1600 1110 L-500 1110Z" fill="#8d6e63"/><ellipse cx="540" cy="840" rx="120" ry="80" fill="#c68642" stroke="#8d5524" stroke-width="10"/>'
             '<path d="M540 760 Q540 640 600 600 Q620 560 580 540 Q520 560 540 620" fill="#7cc576" stroke="#3b8a37" stroke-width="6"/>' + face(540, 840, .6),
             drop(380, 500, .8) + drop(700, 460, .8) + label(540, 300, "WATER"),
             '<circle cx="880" cy="240" r="90" fill="#ffd54f"/>' + label(260, 240, "WARM SUN"))
ROOTS = scene('<path d="M-500 760 L1600 760 L1600 1110 L-500 1110Z" fill="#8d6e63"/>'
              '<path d="M540 760 Q520 860 460 960 M540 760 Q560 880 640 980 M540 760 Q540 900 540 1060 M500 860 Q440 880 400 860 M580 900 Q640 900 680 880" stroke="#f5deb3" stroke-width="16" fill="none" stroke-linecap="round"/>'
              '<path d="M540 760 V520" stroke="#3b8a37" stroke-width="22"/><ellipse cx="460" cy="560" rx="90" ry="40" fill="#7cc576" transform="rotate(-25 460 560)"/><ellipse cx="620" cy="520" rx="90" ry="40" fill="#7cc576" transform="rotate(25 620 520)"/>' + face(540, 660, .5),
              arrows([(300, 1040, 460, 940), (800, 1050, 640, 980)], "#4fa8ff") + label(540, 1060, "ROOTS DRINK WATER"),
              label(540, 360, "ROOTS HOLD ON TIGHT"))
LEAF = scene('<path d="M540 960 V700" stroke="#3b8a37" stroke-width="20"/><path d="M540 700 Q260 640 300 380 Q560 360 540 700Z" fill="#7cc576" stroke="#3b8a37" stroke-width="10"/>'
             '<path d="M540 700 Q820 600 800 340 Q560 360 540 700Z" fill="#5fae5a" stroke="#3b8a37" stroke-width="10"/><path d="M540 700 L360 420 M540 700 L740 380" stroke="#3b8a37" stroke-width="6"/>' + face(540, 760, .6),
             '<circle cx="160" cy="220" r="90" fill="#ffd54f"/>' + arrows([(240, 280, 380, 420)], "#ff9f40") + label(860, 200, "SUNLIGHT = FOOD"),
             label(540, 1050, "LEAVES MAKE FOOD"))
FLOWER = scene('<path d="M540 990 V640" stroke="#3b8a37" stroke-width="20"/><ellipse cx="460" cy="820" rx="80" ry="34" fill="#7cc576" transform="rotate(-30 460 820)"/>'
               + "".join(f'<ellipse cx="{540+150*math.cos(math.radians(a)):.0f}" cy="{520+150*math.sin(math.radians(a)):.0f}" rx="90" ry="60" fill="#ffe14d" stroke="#f5a623" stroke-width="6" transform="rotate({a} {540+150*math.cos(math.radians(a)):.0f} {520+150*math.sin(math.radians(a)):.0f})"/>' for a in range(0, 360, 40))
               + '<circle cx="540" cy="520" r="110" fill="#8d5524"/>' + face(540, 510, .8),
               '<g transform="translate(860 330)"><ellipse rx="56" ry="40" fill="#ffd54f"/><path d="M-20 -38 V38 M10 -38 V38" stroke="#333" stroke-width="12"/><ellipse cx="-10" cy="-50" rx="36" ry="22" fill="#e3f2fd" opacity=".9"/></g>' + label(860, 220, "BEES VISIT"),
               "".join(f'<circle cx="{x}" cy="{y}" r="16" fill="#8d5524"/>' for x, y in ((300, 960), (360, 990), (720, 970))) + label(540, 1060, "NEW SEEDS!"))
TREE = scene('<path d="M480 990 L500 640 L580 640 L600 990Z" fill="#8d5524"/><circle cx="420" cy="520" r="170" fill="#5fae5a"/><circle cx="660" cy="520" r="170" fill="#5fae5a"/><circle cx="540" cy="380" r="190" fill="#7cc576"/>' + face(540, 480, .9),
             "".join(f'<circle cx="{x}" cy="{y}" r="28" fill="#ff5a5a"/>' for x, y in ((360, 560), (700, 600), (480, 300), (640, 340))) + label(860, 180, "FRUIT!"),
             "".join(f'<g transform="translate({x} 940)"><path d="M0 0 V-60" stroke="#3b8a37" stroke-width="8"/><ellipse cx="-18" cy="-60" rx="22" ry="10" fill="#7cc576"/></g>' for x in (200, 880)) + label(540, 1060, "FROM A TINY SEED"))

GIZMO_TITLE = svg(lab_env() + """
  <g transform="translate(-130 -40)">
    <rect x="190" y="230" width="700" height="150" rx="44" fill="#1d3a8a" stroke="#0e2366" stroke-width="10"/>
    <text x="540" y="333" text-anchor="middle" font-family="Baloo, sans-serif" font-weight="800" font-size="80" fill="#fff">GIZMO EXPLAINS</text>
    <g transform="translate(540 700)"><circle r="150" fill="#5ff3ff" opacity=".3"/><path d="M-60 60 L0 -100 L60 60Z" fill="#fff" stroke="#3561d9" stroke-width="10"/><circle cy="-20" r="26" fill="#5ff3ff"/></g>
  </g>""")

SCENES10 = {"gz_rain": RAIN, "gz_rainbow": RAINBOW, "gz_lightning": LIGHTNING, "gz_snow": SNOW, "gz_wind": WIND,
            "gz_rocket": ROCKET, "gz_plane": PLANE, "gz_balloon": BALLOON, "gz_heli": HELI, "gz_kite": KITE,
            "gz_magnet": MAGNET, "gz_bulb": BULB, "gz_ice": ICE, "gz_shadow": SHADOW, "gz_sound": SOUND,
            "gz_seed": SEED, "gz_roots": ROOTS, "gz_leaf": LEAF, "gz_flower": FLOWER, "gz_tree": TREE}
NAMES10 = {"gz_rain": "RAIN", "gz_rainbow": "RAINBOW", "gz_lightning": "LIGHTNING", "gz_snow": "SNOW", "gz_wind": "WIND", "gz_rocket": "ROCKET", "gz_plane": "AIRPLANE",
           "gz_balloon": "HOT AIR BALLOON", "gz_heli": "HELICOPTER", "gz_kite": "KITE", "gz_magnet": "MAGNET", "gz_bulb": "LIGHT BULB", "gz_ice": "MELTING ICE",
           "gz_shadow": "SHADOW", "gz_sound": "SOUND", "gz_seed": "SEED", "gz_roots": "ROOTS", "gz_leaf": "LEAVES", "gz_flower": "FLOWER", "gz_tree": "TREE"}
