"""Week-2 art for Gizmo Explains: body, water, simple machines, energy, animals, space, everyday tech.
Same frame/style as art_gizmo.py (1080x1100, ground ~y1000, #animal / #fx / #fx2). Keys prefixed gz2_."""
import math
from art_gizmo import svg, sky_env, lab_env, face, arrows, label, sparkles, scene, drop


def space_env():
    stars = ((60, 120), (210, 380), (330, 90), (980, 160), (880, 420), (1010, 640), (90, 700), (760, 80), (-200, 300), (1300, 260),
             (-350, 760), (1400, 820), (470, 40), (640, 980), (150, 980), (940, 900), (-120, 520), (1220, 560))
    return ('<rect x="-500" y="0" width="2200" height="1100" fill="#141a4f"/>'
            + "".join(f'<circle cx="{x}" cy="{y}" r="{5 + (x * 7 + y) % 5}" fill="#fff" opacity=".85"/>' for x, y in stars))


def water_env():
    return ('<rect x="-500" y="0" width="2200" height="1100" fill="#4fb3e8"/><rect x="-500" y="0" width="2200" height="220" fill="#7fd3ff"/>'
            '<path d="M-500 220 Q-400 200 -300 220 T-100 220 T100 220 T300 220 T500 220 T700 220 T900 220 T1100 220 T1300 220 T1500 220 T1700 220" stroke="#d6f1ff" stroke-width="12" fill="none"/>'
            '<path d="M-500 960 Q0 920 540 950 T1600 940 L1600 1110 L-500 1110Z" fill="#f2d49b"/>'
            '<g fill="#3fa35a"><path d="M-160 960 Q-200 820 -140 700 Q-120 820 -120 960Z"/><path d="M1180 950 Q1140 800 1210 680 Q1230 820 1230 950Z"/><path d="M60 960 Q20 860 80 780 Q100 870 100 960Z"/></g>')


def pond_env():
    return sky_env() + ('<ellipse cx="540" cy="900" rx="760" ry="130" fill="#4fb3e8"/><ellipse cx="540" cy="880" rx="700" ry="100" fill="#6cc4f0"/>'
                        '<path d="M-250 820 Q-260 740 -230 700 M-210 830 Q-200 750 -180 720 M1290 830 Q1300 740 1280 700" stroke="#3b8a37" stroke-width="10" fill="none" stroke-linecap="round"/>')


def ring_arrow(cx, cy, r, c="#3561d9", a0=200, a1=520):
    """Curved dashed arrow around a centre (clockwise from a0 to a1 degrees)."""
    p0 = (cx + r * math.cos(math.radians(a0)), cy + r * math.sin(math.radians(a0)))
    p1 = (cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1)))
    big = 1 if (a1 - a0) % 360 > 180 else 0
    t = math.radians(a1 + 90)
    hx, hy = p1
    return (f'<path d="M{p0[0]:.0f} {p0[1]:.0f} A{r} {r} 0 {big} 1 {p1[0]:.0f} {p1[1]:.0f}" stroke="{c}" stroke-width="14" fill="none" stroke-linecap="round" stroke-dasharray="4 22"/>'
            f'<path d="M{hx + 34 * math.cos(t):.0f} {hy + 34 * math.sin(t):.0f} L{hx - 20 * math.cos(t + 1.57):.0f} {hy - 20 * math.sin(t + 1.57):.0f} L{hx + 20 * math.cos(t + 1.57):.0f} {hy + 20 * math.sin(t + 1.57):.0f}Z" fill="{c}"/>')


def kid_head(cx=540, cy=600, hair="#5d4037", skin="#ffd6a5", shirt="#ff9f40"):
    return (f'<rect x="{cx-110}" y="{cy+120}" width="220" height="300" rx="60" fill="{shirt}"/>'
            f'<circle cx="{cx-165}" cy="{cy+10}" r="42" fill="{skin}"/><circle cx="{cx+165}" cy="{cy+10}" r="42" fill="{skin}"/>'
            f'<circle cx="{cx}" cy="{cy}" r="170" fill="{skin}"/>'
            f'<path d="M{cx-170} {cy-20} Q{cx-150} {cy-180} {cx} {cy-180} Q{cx+150} {cy-180} {cx+170} {cy-20} Q{cx+80} {cy-110} {cx-170} {cy-20}Z" fill="{hair}"/>'
            f'<circle cx="{cx-95}" cy="{cy+70}" r="22" fill="#ff8fa3" opacity=".6"/><circle cx="{cx+95}" cy="{cy+70}" r="22" fill="#ff8fa3" opacity=".6"/>'
            + face(cx, cy + 10, 1.0))


def notes(pts, c="#6a5cff"):
    return "".join(f'<g transform="translate({x} {y})"><ellipse cx="0" cy="0" rx="26" ry="20" fill="{c}" transform="rotate(-20)"/><path d="M22 -6 V-90 Q50 -80 56 -56" stroke="{c}" stroke-width="10" fill="none"/></g>' for x, y in pts)


def hexes(cx, cy, r=46, c="#ffc93c", s="#c98a00"):
    out = ""
    for i, j in ((0, 0), (1, 0), (-1, 0), (0.5, -0.87), (-0.5, -0.87), (0.5, 0.87), (-0.5, 0.87)):
        x, y = cx + i * r * 1.8, cy + j * r * 1.8 * 1.0
        pts = " ".join(f'{x + r * math.cos(math.radians(a)):.0f},{y + r * math.sin(math.radians(a)):.0f}' for a in range(30, 390, 60))
        out += f'<polygon points="{pts}" fill="{c}" stroke="{s}" stroke-width="6"/>'
    return out


LAB_TANK = ('<rect x="200" y="420" width="680" height="560" rx="30" fill="#e8f6ff" stroke="#7ec8ec" stroke-width="12"/>'
            '<rect x="212" y="560" width="656" height="408" rx="22" fill="#7fd3ff" opacity=".8"/>'
            '<path d="M212 560 Q290 540 370 560 T530 560 T690 560 T868 560" stroke="#4fa8ff" stroke-width="10" fill="none"/>')

# ======================= YOUR BODY =======================
HEART_P = "M540 880 C300 720 250 530 350 440 C430 370 520 400 540 470 C560 400 650 370 730 440 C830 530 780 720 540 880Z"
HEART = scene(f'<path d="{HEART_P}" fill="#ff5a7a" stroke="#c2185b" stroke-width="12"/><path d="M380 500 Q400 460 440 450" stroke="#ffb3c4" stroke-width="18" fill="none" stroke-linecap="round"/>'
              + face(540, 620, .95),
              f'<path d="{HEART_P}" fill="none" stroke="#ff5a7a" stroke-width="10" opacity=".5" transform="translate(540 640) scale(1.18) translate(-540 -640)"/>'
              '<path d="M470 430 Q440 300 260 260 M610 430 Q650 300 820 260" stroke="#ff5a5a" stroke-width="26" fill="none" stroke-linecap="round"/>'
              + arrows([(300, 270, 170, 240), (780, 270, 910, 240)], "#e53935") + label(540, 160, "PUMP, PUMP!", "#c2185b"),
              '<path d="M540 880 V960" stroke="#c2185b" stroke-width="0"/>' + label(540, 1050, "SIZE OF YOUR FIST", "#c2185b")
              + '<g transform="translate(880 900)"><circle r="70" fill="#fff" stroke="#c2185b" stroke-width="6"/><path d="M-30 -10 Q-30 -40 0 -30 Q30 -40 30 -10 Q30 20 0 40 Q-30 20 -30 -10Z" fill="#ff5a7a"/></g>', env=lab_env)

LUNG_L = "M500 420 Q470 400 420 430 Q300 520 300 760 Q300 880 400 880 Q480 880 500 800Z"
LUNGS = scene('<path d="M540 260 V430 M540 430 Q520 450 500 470 M540 430 Q560 450 580 470" stroke="#d45d7f" stroke-width="40" fill="none" stroke-linecap="round"/>'
              f'<path d="{LUNG_L}" fill="#ff9eb5" stroke="#d45d7f" stroke-width="12"/><path d="{LUNG_L}" fill="#ff9eb5" stroke="#d45d7f" stroke-width="12" transform="translate(1080 0) scale(-1 1)"/>'
              '<ellipse cx="540" cy="700" rx="150" ry="120" fill="#ffc2d1" stroke="#d45d7f" stroke-width="10"/>' + face(540, 690, .8),
              arrows([(540, 120, 540, 330)], "#4fa8ff") + '<g fill="#bfe3ff"><circle cx="420" cy="160" r="22"/><circle cx="660" cy="200" r="16"/><circle cx="380" cy="260" r="12"/></g>'
              + label(820, 160, "BREATHE IN", "#1d3a8a"),
              arrows([(600, 300, 800, 180)], "#9e9e9e") + label(260, 160, "BREATHE OUT", "#555"), env=lab_env)


def bone(cx, cy, w, s=1.0, rot=0):
    r = 50 * s; h = 50 * s
    return (f'<g transform="rotate({rot} {cx} {cy})"><rect x="{cx-w/2}" y="{cy-h/2}" width="{w}" height="{h}" fill="#fffaf0" stroke="#c9b99a" stroke-width="{10*s:.0f}"/>'
            + "".join(f'<circle cx="{cx+dx*w/2}" cy="{cy+dy*r*.8}" r="{r}" fill="#fffaf0" stroke="#c9b99a" stroke-width="{10*s:.0f}"/>' for dx in (-1, 1) for dy in (-1, 1))
            + f'<rect x="{cx-w/2}" y="{cy-h/2+6*s}" width="{w}" height="{h-12*s}" fill="#fffaf0"/></g>')


BONES = scene(bone(540, 640, 520, 1.7) + face(540, 630, .85),
              bone(220, 300, 120, .6, 30) + bone(860, 280, 140, .6, -20) + bone(180, 900, 110, .5, -10) + bone(900, 920, 120, .5, 15) + label(540, 200, "206 BONES"),
              '<g transform="translate(860 360)"><path d="M-60 -110 L60 -110 L48 110 L-48 110Z" fill="#fff" stroke="#8fb8de" stroke-width="8"/><path d="M-56 -40 L56 -40 L48 110 L-48 110Z" fill="#fafafa"/></g>'
              '<g transform="translate(220 380)"><ellipse rx="80" ry="40" fill="#5fae5a" transform="rotate(-30)"/><ellipse cx="40" cy="20" rx="70" ry="34" fill="#7cc576" transform="rotate(20)"/></g>'
              + label(540, 1050, "MILK + GREENS"), env=lab_env)

MUSCLES = scene('<path d="M140 760 Q140 680 220 680 L560 680 Q620 680 640 620 L660 420 Q665 390 700 390 L760 390 Q790 395 785 430 L760 700 Q740 830 600 840 L220 840 Q140 840 140 760Z" fill="#ffd6a5" stroke="#d9a066" stroke-width="10"/>'
                '<path d="M300 690 Q420 520 560 680" fill="#ffd6a5" stroke="#d9a066" stroke-width="10"/><path d="M310 690 L555 690" stroke="#ffd6a5" stroke-width="16"/>'
                '<circle cx="730" cy="370" r="70" fill="#ffd6a5" stroke="#d9a066" stroke-width="10"/><path d="M690 340 h80 M690 370 h80" stroke="#d9a066" stroke-width="6"/>'
                '<rect x="120" y="660" width="70" height="200" rx="30" fill="#ff9f40"/>' + face(430, 700, .6),
                arrows([(560, 560, 380, 560)], "#e53935") + label(450, 470, "MUSCLES PULL", "#c62828"),
                ring_arrow(640, 700, 150, "#3561d9", 200, 290) + label(540, 1040, "OVER 600 MUSCLES"), env=lab_env)

TOOTH_P = "M380 380 Q460 330 540 370 Q620 330 700 380 Q780 440 760 560 Q740 660 720 760 Q700 900 650 900 Q610 900 600 800 Q590 720 540 720 Q490 720 480 800 Q470 900 430 900 Q380 900 360 760 Q340 660 320 560 Q300 440 380 380Z"
TEETH = scene(f'<path d="{TOOTH_P}" fill="#fff" stroke="#9ec5e6" stroke-width="12"/><path d="M400 430 Q430 400 470 400" stroke="#e3f2fd" stroke-width="18" fill="none" stroke-linecap="round"/>'
              + face(540, 540, .85),
              '<g transform="translate(200 300)"><circle r="80" fill="#ff5a5a"/><path d="M0 -80 Q10 -120 40 -130" stroke="#795548" stroke-width="10" fill="none"/><ellipse cx="30" cy="-110" rx="26" ry="12" fill="#7cc576"/></g>'
              + label(780, 220, "BITE AND CHEW"),
              '<g transform="translate(860 700) rotate(-35)"><rect x="-30" y="-20" width="60" height="320" rx="24" fill="#4fa8ff"/><rect x="-36" y="-130" width="72" height="120" rx="14" fill="#fff" stroke="#4fa8ff" stroke-width="6"/>'
              + "".join(f'<path d="M{x} -130 V-200" stroke="#bfe3ff" stroke-width="10"/>' for x in (-22, -6, 10, 26)) + '</g>'
              + sparkles([(300, 820), (240, 560), (780, 380)], "#bfe3ff") + label(540, 1050, "BRUSH TWICE A DAY"), env=lab_env)

# ======================= WATER =======================
FLOAT = scene(LAB_TANK + '<path d="M360 520 L720 520 L660 620 L420 620Z" fill="#ff5a5a" stroke="#b33" stroke-width="10" stroke-linejoin="round"/>'
              '<path d="M540 520 V340" stroke="#795548" stroke-width="12"/><path d="M550 350 L680 440 L550 480Z" fill="#ffe14d" stroke="#f5a623" stroke-width="8"/>' + face(540, 560, .55),
              arrows([(420, 900, 420, 650), (660, 900, 660, 650)], "#1d3a8a") + label(540, 300, "WATER PUSHES UP"),
              sparkles([(240, 460), (840, 470)]) + label(540, 1050, "IT FLOATS!"), env=lab_env)

SINK = scene(LAB_TANK + '<path d="M400 960 Q380 860 450 820 Q540 780 630 820 Q700 860 680 960Z" fill="#9e9e9e" stroke="#616161" stroke-width="10"/>'
             '<path d="M460 850 Q490 830 520 835" stroke="#cfcfcf" stroke-width="12" fill="none" stroke-linecap="round"/>' + face(540, 885, .55)
             + '<g fill="#e3f2fd" opacity=".9"><circle cx="300" cy="700" r="14"/><circle cx="320" cy="640" r="10"/><circle cx="780" cy="760" r="12"/></g>',
             arrows([(820, 620, 820, 900)], "#e53935") + label(540, 300, "HEAVY FOR ITS SIZE"),
             '<g transform="translate(400 545)"><ellipse rx="90" ry="26" fill="#7cc576" stroke="#3b8a37" stroke-width="6"/><path d="M-80 0 H80" stroke="#3b8a37" stroke-width="5"/></g>'
             + label(540, 1050, "THE LEAF FLOATS"), env=lab_env)

STEAM = scene('<g transform="translate(220 760)"><rect x="-110" y="-110" width="220" height="220" rx="36" fill="#d6f3ff" stroke="#7ec8ec" stroke-width="10"/><path d="M-80 -70 L-20 -84" stroke="#fff" stroke-width="14" stroke-linecap="round"/></g>'
              + drop(540, 790, 2.4) + face(540, 790, .7)
              + '<g transform="translate(860 740)"><circle cx="-50" cy="20" r="70" fill="#f5f5f5"/><circle cx="40" cy="-20" r="80" fill="#f5f5f5"/><circle cx="60" cy="50" r="60" fill="#f5f5f5"/>'
                '<path d="M-60 -120 q20 -30 0 -60 M20 -140 q20 -30 0 -60" stroke="#e0e0e0" stroke-width="12" fill="none" stroke-linecap="round"/></g>',
              arrows([(320, 620, 430, 620), (650, 620, 760, 620)], "#ff8a3d") + label(540, 440, "WARM IT UP"),
              label(220, 950, "ICE") + label(540, 950, "WATER") + label(860, 950, "STEAM"), env=lab_env)

COLD_GLASS = scene('<path d="M380 420 L700 420 L660 960 L420 960Z" fill="#e8f6ff" stroke="#7ec8ec" stroke-width="12"/><path d="M392 560 L688 560 L662 950 L418 950Z" fill="#9fd8ff" opacity=".8"/>'
                   '<rect x="440" y="600" width="90" height="90" rx="16" fill="#e3f7ff" stroke="#7ec8ec" stroke-width="6" transform="rotate(12 485 645)"/>'
                   '<rect x="560" y="680" width="80" height="80" rx="14" fill="#e3f7ff" stroke="#7ec8ec" stroke-width="6" transform="rotate(-10 600 720)"/>'
                   + face(540, 820, .7),
                   "".join(f'<path d="M{x} {y} q30 -24 60 0 t60 0" stroke="#9fb1e0" stroke-width="10" fill="none" stroke-linecap="round"/>' for x, y in ((120, 520), (140, 700), (800, 560), (780, 760)))
                   + label(540, 300, "WATER IN THE AIR"),
                   "".join(drop(x, y, .3, "#4fa8ff") for x, y in ((395, 500), (700, 520), (405, 700), (680, 660), (420, 860), (668, 840), (690, 450)))
                   + label(540, 1050, "DROPS APPEAR!"), env=lab_env)

PUDDLE = scene('<ellipse cx="540" cy="930" rx="320" ry="70" fill="#4fb3e8" stroke="#2f8fc4" stroke-width="10"/><ellipse cx="460" cy="910" rx="90" ry="16" fill="#bfe3ff"/>' + face(560, 925, .55)
               + '<circle cx="840" cy="230" r="110" fill="#ffd54f"/>' + "".join(f'<path d="M{840+140*math.cos(math.radians(a)):.0f} {230+140*math.sin(math.radians(a)):.0f} L{840+190*math.cos(math.radians(a)):.0f} {230+190*math.sin(math.radians(a)):.0f}" stroke="#ffd54f" stroke-width="14" stroke-linecap="round"/>' for a in range(0, 360, 45)),
               "".join(f'<path d="M{x} 820 q-24 -40 0 -80 t0 -80 t0 -80" stroke="#9fd8ff" stroke-width="12" fill="none" stroke-linecap="round"/>' for x in (380, 540, 700))
               + label(300, 330, "WATER GOES UP"),
               '<path d="M160 260 Q120 180 220 160 Q260 90 360 130 Q440 100 470 180 Q540 200 500 260Z" fill="#fff"/>' + label(540, 1060, "IT MAKES CLOUDS"))

# ======================= SIMPLE MACHINES =======================
def wheel(cx, cy, r, c="#3d3d5c"):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{c}"/><circle cx="{cx}" cy="{cy}" r="{r*.62:.0f}" fill="#9e9e9e"/><circle cx="{cx}" cy="{cy}" r="{r*.22:.0f}" fill="#ffe14d"/>'
            + "".join(f'<path d="M{cx} {cy} L{cx + r*.6*math.cos(math.radians(a)):.0f} {cy + r*.6*math.sin(math.radians(a)):.0f}" stroke="#ffe14d" stroke-width="10"/>' for a in range(0, 360, 60)))


WHEEL = scene('<rect x="240" y="560" width="600" height="260" rx="30" fill="#ff5a5a" stroke="#b33" stroke-width="10"/><rect x="270" y="590" width="540" height="40" rx="16" fill="#ff8a8a"/>'
              '<path d="M840 640 L1000 520" stroke="#795548" stroke-width="20" stroke-linecap="round"/><circle cx="1004" cy="516" r="22" fill="#795548"/>'
              + wheel(360, 880, 110) + wheel(720, 880, 110) + face(540, 690, .75),
              ring_arrow(360, 880, 160, "#3561d9", 200, 330) + ring_arrow(720, 880, 160, "#3561d9", 200, 330) + label(540, 380, "WHEELS ROLL"),
              label(540, 260, "EASY TO PULL!"))

LEVER = scene('<path d="M600 980 L700 800 L800 980Z" fill="#ffd54f" stroke="#c99a00" stroke-width="10" stroke-linejoin="round"/>'
              '<g transform="rotate(14 700 790)"><rect x="150" y="770" width="800" height="40" rx="18" fill="#4fa8ff" stroke="#1d5fae" stroke-width="8"/></g>'
              '<rect x="790" y="680" width="150" height="130" rx="14" fill="#c68642" stroke="#8d5524" stroke-width="8" transform="rotate(14 865 745)"/>'
              + face(700, 920, .5),
              arrows([(170, 520, 170, 650)], "#e53935") + label(220, 440, "PUSH DOWN"),
              arrows([(900, 640, 900, 470)], "#3d9a3d") + label(860, 400, "LIFTS UP!", "#2e7d32"))

RAMP = scene('<path d="M120 990 L960 990 L960 560Z" fill="#c68642" stroke="#8d5524" stroke-width="10" stroke-linejoin="round"/><path d="M200 990 L960 610" stroke="#e0a96d" stroke-width="10"/>'
             '<g transform="rotate(-27 520 720)"><rect x="420" y="620" width="200" height="180" rx="24" fill="#4fa8ff" stroke="#1d5fae" stroke-width="10"/></g>' + face(520, 690, .55),
             arrows([(300, 860, 820, 600)], "#ff8a3d") + label(380, 420, "EASIER TO GO UP"),
             '<g transform="translate(860 330)">' + "".join(f'<rect x="{-120+i*60}" y="{80-i*60}" width="60" height="{60+i*60}" fill="#9fb8f5" stroke="#3561d9" stroke-width="5"/>' for i in range(4)) + '</g>'
             + label(860, 220, "NOT STAIRS"))

PULLEY = scene('<path d="M260 990 V220 H760" stroke="#795548" stroke-width="30" fill="none" stroke-linecap="round"/><path d="M740 220 V300" stroke="#795548" stroke-width="16"/>'
               '<circle cx="740" cy="360" r="70" fill="#ffd54f" stroke="#c99a00" stroke-width="10"/><circle cx="740" cy="360" r="16" fill="#795548"/>'
               '<path d="M670 360 V860 M810 360 V600" stroke="#8d6e63" stroke-width="10"/><path d="M670 360 A70 70 0 0 1 810 360" stroke="#8d6e63" stroke-width="10" fill="none"/>'
               '<path d="M730 600 L890 600 L870 760 L750 760Z" fill="#4fa8ff" stroke="#1d5fae" stroke-width="10" stroke-linejoin="round"/><path d="M740 600 Q810 520 880 600" stroke="#1d5fae" stroke-width="8" fill="none"/>'
               + face(810, 680, .5) + '<rect x="640" y="860" width="60" height="40" rx="12" fill="#ff5a5a"/>',
               arrows([(600, 700, 600, 920)], "#e53935") + label(420, 600, "PULL DOWN") + arrows([(960, 760, 960, 520)], "#3d9a3d") + label(900, 460, "UP IT GOES!", "#2e7d32"),
               '<path d="M120 990 V320" stroke="#9e9e9e" stroke-width="12"/><path d="M126 330 L240 360 L126 400Z" fill="#ff5a5a"/>' + label(260, 1060, "FLAGS USE PULLEYS"))

SCREW = scene('<rect x="380" y="300" width="320" height="90" rx="40" fill="#bdbdbd" stroke="#757575" stroke-width="10"/><path d="M490 345 H590" stroke="#616161" stroke-width="18" stroke-linecap="round"/>'
              '<path d="M450 390 L630 390 L630 820 L540 960 L450 820Z" fill="#cfd8dc" stroke="#757575" stroke-width="10" stroke-linejoin="round"/>'
              + "".join(f'<path d="M440 {y} L640 {y+50}" stroke="#90a4ae" stroke-width="16" stroke-linecap="round"/>' for y in range(420, 800, 70))
              + face(540, 560, .6).replace('fill="#fff"/><circle cx="555"', 'fill="#fff"/><circle cx="555"'),
              ring_arrow(540, 345, 230, "#3561d9", 200, 340) + label(540, 160, "TWIST, TWIST"),
              '<g transform="translate(870 760)"><rect x="-90" y="-60" width="180" height="200" rx="30" fill="#e3f2fd" stroke="#7ec8ec" stroke-width="8"/><rect x="-100" y="-110" width="200" height="60" rx="14" fill="#ff5a5a"/>'
              + "".join(f'<path d="M{x} -110 V-50" stroke="#b33" stroke-width="6"/>' for x in (-60, -20, 20, 60)) + '</g>' + label(860, 560, "JAR LIDS TOO!"), env=lab_env)

# ======================= ENERGY =======================
BATTERY = scene('<rect x="400" y="380" width="280" height="560" rx="40" fill="#3561d9" stroke="#1d3a8a" stroke-width="10"/><rect x="400" y="700" width="280" height="240" rx="40" fill="#ffd54f" stroke="#1d3a8a" stroke-width="10"/>'
                '<rect x="490" y="330" width="100" height="56" rx="14" fill="#9e9e9e" stroke="#616161" stroke-width="8"/>'
                '<path d="M520 450 h40 M540 430 v40" stroke="#fff" stroke-width="12" stroke-linecap="round"/><path d="M520 880 h40" stroke="#1d3a8a" stroke-width="12" stroke-linecap="round"/>'
                + face(540, 590, .75),
                '<path d="M540 330 V240 H200 V420" stroke="#ff5a5a" stroke-width="12" fill="none"/><path d="M540 940 V990 H200 V560" stroke="#1d3a8a" stroke-width="12" fill="none"/>'
                '<circle cx="200" cy="490" r="70" fill="#fff59d" stroke="#f5a623" stroke-width="8"/><circle cx="200" cy="490" r="120" fill="#fff59d" opacity=".35"/>' + label(820, 260, "STORED ENERGY"),
                '<g transform="translate(860 860)"><rect x="-110" y="-60" width="220" height="90" rx="30" fill="#ff9f40" stroke="#c66a00" stroke-width="8"/>'
                '<circle cx="-60" cy="40" r="34" fill="#3d3d5c"/><circle cx="60" cy="40" r="34" fill="#3d3d5c"/></g>' + label(860, 700, "TOYS GO!"), env=lab_env)

SOLAR = scene('<path d="M540 760 V990 M440 990 H640" stroke="#757575" stroke-width="24" stroke-linecap="round"/>'
              '<g transform="translate(540 600) rotate(-12)"><rect x="-320" y="-180" width="640" height="340" rx="16" fill="#1d3a8a" stroke="#c0c8d8" stroke-width="14"/>'
              + "".join(f'<path d="M{x} -170 V150" stroke="#4f74d9" stroke-width="6"/>' for x in range(-240, 320, 80))
              + "".join(f'<path d="M-310 {y} H310" stroke="#4f74d9" stroke-width="6"/>' for y in (-95, -10, 75)) + '</g>'
              + face(540, 610, .8),
              '<circle cx="150" cy="180" r="100" fill="#ffd54f"/>' + arrows([(260, 230, 400, 360), (180, 300, 260, 430), (340, 160, 520, 300)], "#ff9f40") + label(780, 180, "SUNLIGHT IN"),
              '<path d="M640 900 H900 V840" stroke="#3561d9" stroke-width="10" fill="none"/><g transform="translate(900 760)"><path d="M-90 0 L0 -80 L90 0Z" fill="#ff5a5a"/><rect x="-70" y="0" width="140" height="110" fill="#fff3e0"/><rect x="-20" y="30" width="40" height="40" fill="#ffe14d"/></g>'
              + label(820, 1060, "POWER FOR HOMES"))

TURBINE = scene('<path d="M520 990 L532 420 L548 420 L560 990Z" fill="#fafafa" stroke="#b0bec5" stroke-width="8"/>'
                + "".join(f'<path d="M540 400 Q{540+60*math.cos(math.radians(a-90)):.0f} {400+60*math.sin(math.radians(a-90)):.0f} {540+330*math.cos(math.radians(a)):.0f} {400+330*math.sin(math.radians(a)):.0f} Q{540+40*math.cos(math.radians(a+40)):.0f} {400+40*math.sin(math.radians(a+40)):.0f} 540 400Z" fill="#fafafa" stroke="#b0bec5" stroke-width="7"/>' for a in (-90, 30, 150))
                + '<rect x="470" y="360" width="140" height="80" rx="30" fill="#eceff1" stroke="#b0bec5" stroke-width="7"/><circle cx="540" cy="400" r="78" fill="#5ff3ff" stroke="#3561d9" stroke-width="8"/>'
                + face(540, 392, .62),
                ring_arrow(540, 400, 380, "#3561d9", 250, 330) + "".join(f'<path d="M{x} {y} q60 -30 120 0 t120 0" stroke="#fff" stroke-width="12" fill="none" stroke-linecap="round"/>' for x, y in ((-80, 300), (-40, 520)))
                + label(220, 180, "WIND SPINS IT"),
                '<path d="M560 960 H880 V900" stroke="#3561d9" stroke-width="10" fill="none"/><g transform="translate(880 820)"><path d="M-80 0 L0 -70 L80 0Z" fill="#ff5a5a"/><rect x="-62" y="0" width="124" height="100" fill="#fff3e0"/><rect x="-18" y="26" width="36" height="36" fill="#ffe14d"/></g>'
                + label(820, 680, "ELECTRICITY!"))

WATERWHEEL = scene('<path d="M-500 900 Q0 870 540 900 T1600 890 L1600 1110 L-500 1110Z" fill="#4fb3e8"/>'
                   '<circle cx="540" cy="640" r="280" fill="none" stroke="#8d5524" stroke-width="26"/><circle cx="540" cy="640" r="200" fill="none" stroke="#c68642" stroke-width="14"/>'
                   + "".join(f'<path d="M{540+80*math.cos(math.radians(a)):.0f} {640+80*math.sin(math.radians(a)):.0f} L{540+280*math.cos(math.radians(a)):.0f} {640+280*math.sin(math.radians(a)):.0f}" stroke="#8d5524" stroke-width="16"/>'
                             f'<rect x="-30" y="-50" width="60" height="100" rx="8" fill="#c68642" stroke="#8d5524" stroke-width="6" transform="translate({540+300*math.cos(math.radians(a)):.0f} {640+300*math.sin(math.radians(a)):.0f}) rotate({a})"/>' for a in range(0, 360, 45))
                   + '<circle cx="540" cy="640" r="110" fill="#ffd54f" stroke="#c99a00" stroke-width="10"/>' + face(540, 630, .65)
                   + '<path d="M-500 940 Q0 920 540 945 T1600 935 L1600 1110 L-500 1110Z" fill="#6cc4f0" opacity=".8"/>',
                   arrows([(80, 920, 300, 900), (880, 900, 1060, 920)], "#1d3a8a") + label(540, 220, "WATER PUSHES"),
                   ring_arrow(540, 640, 360, "#ff8a3d", 200, 320) + label(540, 1060, "SPIN = POWER"))

SWITCH = scene('<rect x="380" y="380" width="320" height="480" rx="40" fill="#fafafa" stroke="#9fb1e0" stroke-width="12"/>'
               '<rect x="490" y="470" width="100" height="160" rx="22" fill="#e0e0e0" stroke="#9e9e9e" stroke-width="8"/><rect x="500" y="480" width="80" height="80" rx="16" fill="#5ff3ff"/>'
               + face(540, 740, .65),
               '<path d="M540 380 V250 H880 V420 M540 860 V960 H880 V600" stroke="#3561d9" stroke-width="12" fill="none"/>'
               '<circle cx="880" cy="510" r="80" fill="#fff59d" stroke="#f5a623" stroke-width="8"/><circle cx="880" cy="510" r="130" fill="#fff59d" opacity=".35"/>' + label(220, 260, "ON = A LOOP"),
               label(220, 1040, "OFF = A GAP"), env=lab_env)

# ======================= ANIMALS =======================
FISH = scene('<path d="M260 620 Q420 420 680 520 Q760 550 800 620 Q760 690 680 720 Q420 820 260 620Z" fill="#ff9f40" stroke="#c66a00" stroke-width="10"/>'
             '<path d="M800 620 L960 500 L940 620 L960 740Z" fill="#ff9f40" stroke="#c66a00" stroke-width="10" stroke-linejoin="round"/>'
             '<path d="M500 500 Q560 420 640 480" fill="#ffb86b" stroke="#c66a00" stroke-width="8"/>'
             '<path d="M400 560 Q430 620 400 680 M430 550 Q460 620 430 690" stroke="#c66a00" stroke-width="8" fill="none" stroke-linecap="round"/>'
             + face(330, 610, .45).replace('cx="349"', 'cx="349"'),
             arrows([(120, 600, 260, 600), (480, 640, 600, 720)], "#fff") + "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="#fff" stroke-width="5"/>' for x, y, r in ((300, 440, 18), (330, 380, 12), (270, 330, 9)))
             + label(420, 300, "WATER IN, OVER GILLS"),
             label(540, 1050, "GILLS GET THE AIR"), env=water_env)

BIRD = scene('<ellipse cx="540" cy="680" rx="190" ry="150" fill="#ffd54f" stroke="#c99a00" stroke-width="10"/><ellipse cx="560" cy="730" rx="110" ry="80" fill="#fff3c4"/>'
             '<path d="M420 620 Q240 380 120 360 Q200 500 260 600 Q330 680 440 700Z" fill="#ff9f40" stroke="#c66a00" stroke-width="10" stroke-linejoin="round"/>'
             '<path d="M660 620 Q840 380 960 360 Q880 500 820 600 Q750 680 640 700Z" fill="#ff9f40" stroke="#c66a00" stroke-width="10" stroke-linejoin="round"/>'
             '<path d="M500 820 L470 900 L540 860 L610 900 L580 820Z" fill="#ff9f40" stroke="#c66a00" stroke-width="8"/>'
             '<path d="M520 690 L560 690 L540 720Z" fill="#ff7043"/>' + face(540, 640, .75).replace('M516 669', 'M516 669'),
             arrows([(200, 640, 200, 820), (880, 640, 880, 820)], "#3561d9") + label(540, 220, "FLAP! PUSH THE AIR"),
             '<g transform="translate(860 960) rotate(-30)"><path d="M0 -90 Q50 -40 0 90 Q-50 -40 0 -90Z" fill="#fff" stroke="#b0bec5" stroke-width="6"/><path d="M0 -80 V90" stroke="#b0bec5" stroke-width="5"/></g>'
             + label(400, 1050, "LIGHT, HOLLOW BONES"))

BEE = scene('<path d="M220 990 V760" stroke="#3b8a37" stroke-width="16"/>' + "".join(f'<ellipse cx="{220+70*math.cos(math.radians(a)):.0f}" cy="{700+70*math.sin(math.radians(a)):.0f}" rx="50" ry="32" fill="#ff8fc8" transform="rotate({a} {220+70*math.cos(math.radians(a)):.0f} {700+70*math.sin(math.radians(a)):.0f})"/>' for a in range(0, 360, 60))
            + '<circle cx="220" cy="700" r="44" fill="#ffd54f"/>'
            '<ellipse cx="580" cy="560" rx="210" ry="150" fill="#ffd54f" stroke="#5d4037" stroke-width="10"/>'
            '<path d="M560 420 Q540 560 560 700 M660 430 Q640 560 660 690" stroke="#5d4037" stroke-width="40" fill="none"/>'
            '<ellipse cx="520" cy="380" rx="110" ry="70" fill="#e3f2fd" stroke="#90caf9" stroke-width="6" opacity=".95" transform="rotate(-20 520 380)"/>'
            '<ellipse cx="660" cy="370" rx="100" ry="64" fill="#e3f2fd" stroke="#90caf9" stroke-width="6" opacity=".95" transform="rotate(20 660 370)"/>'
            '<path d="M780 560 L840 560" stroke="#5d4037" stroke-width="12" stroke-linecap="round"/><path d="M420 440 Q400 360 360 340 M450 430 Q450 350 430 320" stroke="#5d4037" stroke-width="8" fill="none" stroke-linecap="round"/>'
            '<circle cx="450" cy="580" r="110" fill="#ffd54f" stroke="#5d4037" stroke-width="10"/>' + face(450, 570, .7),
            arrows([(300, 640, 360, 600)], "#ff9f40") + drop(260, 620, .4, "#ffb74d") + label(240, 480, "NECTAR"),
            hexes(860, 880, 50) + label(860, 700, "HONEY!", "#a86b00"))

BUTTERFLY = scene('<ellipse cx="540" cy="620" rx="34" ry="190" fill="#5d4037"/>'
                  '<path d="M520 520 Q340 300 210 380 Q160 520 300 600 Q420 640 520 600Z" fill="#6a5cff" stroke="#3d2fb5" stroke-width="10"/>'
                  '<path d="M560 520 Q740 300 870 380 Q920 520 780 600 Q660 640 560 600Z" fill="#6a5cff" stroke="#3d2fb5" stroke-width="10"/>'
                  '<path d="M520 640 Q360 660 320 780 Q380 880 520 720Z" fill="#ff8fc8" stroke="#3d2fb5" stroke-width="10"/>'
                  '<path d="M560 640 Q720 660 760 780 Q700 880 560 720Z" fill="#ff8fc8" stroke="#3d2fb5" stroke-width="10"/>'
                  '<circle cx="320" cy="450" r="40" fill="#ffe14d"/><circle cx="760" cy="450" r="40" fill="#ffe14d"/>'
                  '<path d="M530 440 Q500 360 470 340 M550 440 Q580 360 610 340" stroke="#5d4037" stroke-width="8" fill="none" stroke-linecap="round"/>'
                  '<circle cx="540" cy="480" r="70" fill="#8d6e63"/>' + face(540, 475, .55),
                  '<g transform="translate(200 930)"><path d="M-130 0 Q-100 -60 -60 0 Q-30 -60 0 0 Q30 -60 60 0 Q90 -60 120 0" stroke="#7cc576" stroke-width="44" fill="none" stroke-linecap="round"/><circle cx="130" cy="-10" r="32" fill="#7cc576"/></g>'
                  '<path d="M760 940 H1000" stroke="#795548" stroke-width="16" stroke-linecap="round"/><ellipse cx="880" cy="1000" rx="38" ry="60" fill="#a5d6a7" stroke="#5fae5a" stroke-width="6"/>'
                  + arrows([(380, 930, 800, 980)], "#ff8a3d") + label(380, 200, "CATERPILLAR FIRST"),
                  sparkles([(180, 300), (900, 280), (900, 700)]) + label(780, 200, "NEW WINGS!"))

DUCK = scene('<path d="M300 760 Q300 620 460 640 L620 650 Q720 560 700 470 Q690 380 780 380 Q870 390 860 480 Q850 540 800 600 Q900 640 880 760 Q860 880 600 880 L420 880 Q300 870 300 760Z" fill="#fff8e1" stroke="#c9b99a" stroke-width="10"/>'
             '<path d="M860 450 L950 470 L860 500Z" fill="#ff9f40" stroke="#c66a00" stroke-width="6"/>'
             '<path d="M420 720 Q520 650 640 720 Q560 800 420 720Z" fill="#ffecb3" stroke="#c9b99a" stroke-width="6"/>'
             + face(785, 455, .5).replace('M761 474', 'M761 474')
             + '<path d="M180 870 Q540 850 900 870" stroke="#4fb3e8" stroke-width="20" fill="none" stroke-linecap="round"/>',
             drop(540, 560, .5, "#c68642") + arrows([(540, 600, 520, 660)], "#c66a00") + label(320, 420, "OILY FEATHERS"),
             "".join(drop(x, y, .45) for x, y in ((380, 600), (650, 580), (760, 640))) + arrows([(380, 640, 330, 760), (760, 680, 860, 780)], "#3561d9")
             + label(540, 300, "WATER ROLLS OFF!"), env=pond_env)

# ======================= SPACE =======================
def earth(cx, cy, r):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#4fa8ff" stroke="#1d5fae" stroke-width="10"/>'
            f'<path d="M{cx-r*.6:.0f} {cy-r*.5:.0f} Q{cx-r*.2:.0f} {cy-r*.8:.0f} {cx+r*.1:.0f} {cy-r*.5:.0f} Q{cx-r*.1:.0f} {cy-r*.2:.0f} {cx-r*.5:.0f} {cy-r*.1:.0f}Z" fill="#5fd36a"/>'
            f'<path d="M{cx+r*.2:.0f} {cy+r*.2:.0f} Q{cx+r*.6:.0f} {cy+r*.1:.0f} {cx+r*.7:.0f} {cy+r*.4:.0f} Q{cx+r*.4:.0f} {cy+r*.8:.0f} {cx+r*.1:.0f} {cy+r*.6:.0f}Z" fill="#5fd36a"/>')


def sun(cx, cy, r):
    rays = "".join(f'<path d="M{cx + r*1.12*math.cos(math.radians(a)):.0f} {cy + r*1.12*math.sin(math.radians(a)):.0f} L{cx + r*1.32*math.cos(math.radians(a)):.0f} {cy + r*1.32*math.sin(math.radians(a)):.0f}" stroke="#ffd54f" stroke-width="{max(8, r*.09):.0f}" stroke-linecap="round"/>' for a in range(0, 360, 30))
    return rays + f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#ffd54f" stroke="#f5a623" stroke-width="10"/>'


DAYNIGHT = scene(sun(-60, 560, 200) + earth(640, 600, 270)
                 + '<path d="M640 330 A270 270 0 0 1 640 870 A120 270 0 0 0 640 330Z" fill="#0d1240" opacity=".55"/>' + face(560, 600, .9),
                 ring_arrow(640, 600, 340, "#5ff3ff", 200, 330) + label(640, 180, "EARTH SPINS"),
                 label(400, 1000, "DAY", "#c99a00") + label(860, 1000, "NIGHT", "#1d3a8a"), env=space_env)

SEASONS = scene('<ellipse cx="540" cy="620" rx="440" ry="200" fill="none" stroke="#9fb1e0" stroke-width="6" stroke-dasharray="14 18"/>'
                + sun(540, 620, 130) + face(540, 615, .8)
                + '<g transform="rotate(-23 140 620)">' + earth(140, 620, 80) + '<path d="M140 510 V730" stroke="#fff" stroke-width="6"/></g>'
                + '<g transform="rotate(-23 940 620)">' + earth(940, 620, 80) + '<path d="M940 510 V730" stroke="#fff" stroke-width="6"/></g>',
                arrows([(840, 860, 960, 760)], "#5ff3ff") + label(540, 240, "EARTH LEANS"),
                label(540, 1000, "TILT MAKES SEASONS"), env=space_env)

MOONPHASES = scene('<circle cx="540" cy="620" r="260" fill="#eceff1" stroke="#b0bec5" stroke-width="10"/>'
                   + "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#cfd8dc"/>' for x, y, r in ((420, 480, 40), (680, 760, 50), (700, 470, 28), (380, 760, 24)))
                   + face(540, 620, 1.0),
                   "".join(f'<g transform="translate({140+i*200} 220)"><circle r="60" fill="#2a3170" stroke="#9fb1e0" stroke-width="4"/>{p}</g>' for i, p in enumerate((
                       '',
                       '<path d="M0 -60 A60 60 0 0 1 0 60 A30 60 0 0 0 0 -60Z" fill="#eceff1"/>',
                       '<path d="M0 -60 A60 60 0 0 1 0 60Z" fill="#eceff1"/>',
                       '<path d="M0 -60 A60 60 0 0 1 0 60 A30 60 0 0 1 0 -60Z" fill="#eceff1"/>',
                       '<circle r="60" fill="#eceff1"/>')))
                   + label(540, 340, "MOON PHASES"),
                   sun(-120, 620, 160) + arrows([(80, 500, 260, 540), (80, 740, 260, 700)], "#ffd54f") + label(540, 1010, "SUNLIGHT ON THE MOON"), env=space_env)

STAR_P = " ".join(f'{540 + (300 if i % 2 == 0 else 130) * math.cos(math.radians(-90 + i * 36)):.0f},{620 + (300 if i % 2 == 0 else 130) * math.sin(math.radians(-90 + i * 36)):.0f}' for i in range(10))
STARS = scene(f'<polygon points="{STAR_P}" fill="#ffe14d" stroke="#f5a623" stroke-width="12" stroke-linejoin="round"/>' + face(540, 640, .8),
              sun(200, 260, 90) + label(640, 220, "STARS ARE SUNS"),
              sparkles([(160, 860), (920, 860), (900, 360)], "#fff") + label(540, 1010, "FAR, FAR AWAY"), env=space_env)

SUN_BIG = scene(sun(420, 620, 320)
                + '<g fill="#ffb300" opacity=".5"><circle cx="300" cy="480" r="40"/><circle cx="560" cy="780" r="30"/><circle cx="560" cy="460" r="22"/></g>' + face(420, 610, 1.1),
                '<path d="M760 620 H960" stroke="#9fb1e0" stroke-width="8" stroke-dasharray="10 16"/>' + earth(1000, 620, 22) + label(780, 240, "SO FAR AWAY"),
                label(540, 1020, "109 EARTHS WIDE"), env=space_env)

# ======================= SENSES + EVERYDAY TECH =======================
EYES = scene(kid_head(560, 620, shirt="#4fa8ff"),
             '<g transform="translate(140 640)"><circle r="70" fill="#ff5a5a"/><path d="M0 -70 Q10 -110 40 -120" stroke="#795548" stroke-width="10" fill="none"/></g>'
             + arrows([(220, 610, 450, 620)], "#ffb300") + '<path d="M60 420 L140 560" stroke="#ffe14d" stroke-width="12" stroke-dasharray="14 12"/><circle cx="40" cy="380" r="50" fill="#fff59d"/>'
             + label(320, 300, "LIGHT BOUNCES IN"),
             '<path d="M720 260 Q700 180 790 170 Q830 110 900 150 Q980 140 980 220 Q1020 290 940 320 L760 320 Q690 310 720 260Z" fill="#ffc2d1" stroke="#d45d7f" stroke-width="8"/>'
             '<path d="M760 230 q30 -30 60 0 t60 0" stroke="#d45d7f" stroke-width="6" fill="none"/><circle cx="700" cy="380" r="14" fill="#ffc2d1"/><circle cx="680" cy="420" r="9" fill="#ffc2d1"/>'
             + label(540, 1060, "BRAIN SEES IT!"), env=lab_env)

EARS = scene(kid_head(540, 620, hair="#212121", shirt="#7cc576").replace('r="42" fill="#ffd6a5"', 'r="62" fill="#ffd6a5"'),
             '<g transform="translate(120 540)"><path d="M-40 -40 Q0 -90 40 -40 L50 30 L-50 30Z" fill="#ffd54f" stroke="#c99a00" stroke-width="8"/><circle cy="44" r="14" fill="#c99a00"/></g>'
             + "".join(f'<path d="M{190+i*40} {470-i*10} Q{215+i*40} 540 {190+i*40} {610+i*10}" stroke="#5ff3ff" stroke-width="12" fill="none" stroke-linecap="round"/>' for i in range(3))
             + label(300, 300, "SOUND WAVES"),
             '<circle cx="375" cy="630" r="34" fill="none" stroke="#e53935" stroke-width="8"/>' + label(540, 1060, "EARDRUM WIGGLES"), env=lab_env)

FRIDGE = scene('<rect x="330" y="240" width="420" height="750" rx="40" fill="#f5f7ff" stroke="#9fb1e0" stroke-width="12"/><path d="M330 500 H750" stroke="#9fb1e0" stroke-width="10"/>'
               '<rect x="680" y="300" width="22" height="140" rx="10" fill="#9fb1e0"/><rect x="680" y="560" width="22" height="200" rx="10" fill="#9fb1e0"/>'
               '<rect x="380" y="280" width="90" height="60" rx="10" fill="#ff8fc8"/><circle cx="430" cy="380" r="26" fill="#ffd54f"/>' + face(540, 700, .85),
               "".join(f'<g transform="translate({x} {y})"><path d="M0 -30 V30 M-26 -15 L26 15 M-26 15 L26 -15" stroke="#7fd3ff" stroke-width="9" stroke-linecap="round"/></g>' for x, y in ((420, 880), (600, 870), (520, 580)))
               + "".join(f'<path d="M{x} 900 q-20 -40 0 -80 t0 -80 t0 -80" stroke="#ff8a3d" stroke-width="10" fill="none" stroke-linecap="round"/>' for x in (820, 880, 940))
               + label(860, 220, "HEAT GOES OUT"),
               '<g transform="translate(160 820)"><rect x="-80" y="-50" width="160" height="110" rx="16" fill="#ff5a5a"/><circle cx="-30" cy="-80" r="40" fill="#7cc576"/><circle cx="40" cy="-80" r="34" fill="#ff9f40"/></g>'
               + label(220, 1060, "FOOD STAYS FRESH"), env=lab_env)

BIKE = scene('<circle cx="270" cy="800" r="170" fill="none" stroke="#3d3d5c" stroke-width="24"/><circle cx="810" cy="800" r="170" fill="none" stroke="#3d3d5c" stroke-width="24"/>'
             + "".join(f'<path d="M{cx} 800 L{cx + 150*math.cos(math.radians(a)):.0f} {800 + 150*math.sin(math.radians(a)):.0f}" stroke="#b0bec5" stroke-width="5"/>' for cx in (270, 810) for a in range(0, 360, 30))
             + '<path d="M270 800 L460 560 L760 560 L810 800 M460 560 L540 800 L270 800 M540 800 L760 560" stroke="#ff5a5a" stroke-width="22" fill="none" stroke-linejoin="round" stroke-linecap="round"/>'
             '<path d="M760 560 L740 470 L820 450" stroke="#3d3d5c" stroke-width="18" fill="none" stroke-linecap="round"/><path d="M440 520 L500 520" stroke="#3d3d5c" stroke-width="26" stroke-linecap="round"/>'
             '<path d="M540 730 L270 760 M540 870 L270 840" stroke="#616161" stroke-width="8"/>'
             '<circle cx="540" cy="800" r="74" fill="#ffd54f" stroke="#c99a00" stroke-width="10"/><circle cx="270" cy="800" r="40" fill="#ffd54f" stroke="#c99a00" stroke-width="8"/>'
             + face(540, 795, .5),
             ring_arrow(540, 800, 120, "#3561d9", 200, 330) + label(540, 380, "PEDALS TURN THE GEAR"),
             ring_arrow(270, 800, 80, "#ff8a3d", 160, 470) + label(540, 1060, "CHAIN SPINS THE WHEEL"), env=sky_env)

SCREEN = scene('<rect x="360" y="260" width="360" height="720" rx="50" fill="#3d3d5c" stroke="#1a1a2e" stroke-width="10"/><rect x="385" y="320" width="310" height="580" rx="20" fill="#7fd3ff"/>'
               '<circle cx="540" cy="940" r="20" fill="#616161"/><rect x="500" y="285" width="80" height="14" rx="7" fill="#616161"/>' + face(540, 600, .8),
               '<circle cx="860" cy="420" r="160" fill="#fff" stroke="#3561d9" stroke-width="10"/>'
               + "".join(f'<rect x="{760 + c*60 + k*18}" y="{340 + r*56}" width="14" height="44" rx="5" fill="{col}"/>' for r in range(3) for c in range(3) for k, col in enumerate(("#ff4d4d", "#5fd36a", "#4fa8ff")))
               + '<path d="M700 520 L620 580" stroke="#3561d9" stroke-width="10"/>' + label(860, 640, "TINY DOTS"),
               label(540, 1060, "RED, GREEN, BLUE"), env=lab_env)

GUITAR = scene('<rect x="510" y="140" width="60" height="460" rx="10" fill="#8d5524"/><rect x="490" y="100" width="100" height="90" rx="20" fill="#5d4037"/>'
               '<path d="M540 520 Q380 520 380 650 Q380 720 420 750 Q330 800 340 900 Q360 1000 540 1000 Q720 1000 740 900 Q750 800 660 750 Q700 720 700 650 Q700 520 540 520Z" fill="#ff9f40" stroke="#c66a00" stroke-width="10"/>'
               '<circle cx="540" cy="760" r="56" fill="#5d4037"/><rect x="480" y="900" width="120" height="24" rx="8" fill="#5d4037"/>'
               + "".join(f'<path d="M{525+i*10} 130 V912" stroke="#eee" stroke-width="{5-i*.6:.1f}"/>' for i in range(4))
               + face(540, 640, .6),
               "".join(f'<path d="M{x} 300 Q{x+14} 400 {x} 500 Q{x-14} 600 {x} 700" stroke="#5ff3ff" stroke-width="8" fill="none"/>' for x in (420, 660)) + label(540, 1060, "STRINGS WIGGLE"),
               notes([(200, 400), (860, 340), (880, 640)]) + label(220, 220, "THICK = LOW") + label(860, 160, "THIN = HIGH"), env=lab_env)

SCENES_GIZMO2 = {
    "gz2_heart": HEART, "gz2_lungs": LUNGS, "gz2_bones": BONES, "gz2_muscles": MUSCLES, "gz2_teeth": TEETH,
    "gz2_float": FLOAT, "gz2_sink": SINK, "gz2_steam": STEAM, "gz2_coldglass": COLD_GLASS, "gz2_puddle": PUDDLE,
    "gz2_wheel": WHEEL, "gz2_lever": LEVER, "gz2_ramp": RAMP, "gz2_pulley": PULLEY, "gz2_screw": SCREW,
    "gz2_battery": BATTERY, "gz2_solar": SOLAR, "gz2_turbine": TURBINE, "gz2_waterwheel": WATERWHEEL, "gz2_switch": SWITCH,
    "gz2_fish": FISH, "gz2_bird": BIRD, "gz2_bee": BEE, "gz2_butterfly": BUTTERFLY, "gz2_duck": DUCK,
    "gz2_daynight": DAYNIGHT, "gz2_seasons": SEASONS, "gz2_moonphases": MOONPHASES, "gz2_stars": STARS, "gz2_sun": SUN_BIG,
    "gz2_eyes": EYES, "gz2_ears": EARS, "gz2_fridge": FRIDGE, "gz2_bike": BIKE, "gz2_screen": SCREEN, "gz2_guitar": GUITAR,
}
NAMES_GIZMO2 = {
    "gz2_heart": "HEART", "gz2_lungs": "LUNGS", "gz2_bones": "BONES", "gz2_muscles": "MUSCLES", "gz2_teeth": "TEETH",
    "gz2_float": "FLOATING", "gz2_sink": "SINKING", "gz2_steam": "ICE, WATER, STEAM", "gz2_coldglass": "COLD GLASS", "gz2_puddle": "PUDDLE",
    "gz2_wheel": "WHEEL", "gz2_lever": "LEVER", "gz2_ramp": "RAMP", "gz2_pulley": "PULLEY", "gz2_screw": "SCREW",
    "gz2_battery": "BATTERY", "gz2_solar": "SOLAR PANEL", "gz2_turbine": "WIND TURBINE", "gz2_waterwheel": "WATER WHEEL", "gz2_switch": "LIGHT SWITCH",
    "gz2_fish": "FISH", "gz2_bird": "BIRD", "gz2_bee": "HONEYBEE", "gz2_butterfly": "BUTTERFLY", "gz2_duck": "DUCK",
    "gz2_daynight": "DAY AND NIGHT", "gz2_seasons": "SEASONS", "gz2_moonphases": "MOON PHASES", "gz2_stars": "STARS", "gz2_sun": "THE SUN",
    "gz2_eyes": "EYES", "gz2_ears": "EARS", "gz2_fridge": "FRIDGE", "gz2_bike": "BIKE GEARS", "gz2_screen": "SCREEN", "gz2_guitar": "GUITAR",
}
assert set(SCENES_GIZMO2) == set(NAMES_GIZMO2) and all(k.startswith("gz2_") for k in SCENES_GIZMO2)
