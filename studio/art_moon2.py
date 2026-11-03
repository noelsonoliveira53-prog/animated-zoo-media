"""Moonbeam Bedtime week-2 art: forest, snowy, garden, toys, rainy night, dream train + wind-down extras.
Same 1080x1100 frame / floor ~y1000 / <g id="animal"> + fx + fx2 layout as art_moon.py. Keys are prefixed mb2_."""
import math
from art_moon import svg, scene, critter, snout, zzz, twinkles, night_env, MOON_FX, _r

def face(cx, cy, s=1.0, awake=False, mouth=True, cheeks=True, ex=44, col="#1a1a2e", mdy=40):
    """Like art_moon.sleepy_face, but the mouth can be moved or dropped (for beaks / snouts)."""
    e = ex * s
    if awake:
        out = "".join(f'<circle cx="{x:.0f}" cy="{cy:.0f}" r="{16*s:.0f}" fill="{col}"/><circle cx="{x+5*s:.0f}" cy="{cy-5*s:.0f}" r="{max(3,5*s):.0f}" fill="#fff"/>' for x in (cx - e, cx + e))
    else:
        out = "".join(f'<path d="M{x-18*s:.0f} {cy:.0f} q{18*s:.0f} {14*s:.0f} {36*s:.0f} 0" stroke="{col}" stroke-width="{max(3,7*s):.0f}" fill="none" stroke-linecap="round"/>' for x in (cx - e, cx + e))
    if mouth:
        out += f'<path d="M{cx-16*s:.0f} {cy+mdy*s:.0f} q{16*s:.0f} {12*s:.0f} {32*s:.0f} 0" stroke="#6b2b3a" stroke-width="{max(3,6*s):.0f}" fill="none" stroke-linecap="round"/>'
    if cheeks:
        out += "".join(f'<ellipse cx="{x:.0f}" cy="{cy+30*s:.0f}" rx="{18*s:.0f}" ry="{10*s:.0f}" fill="#ff9ab0" opacity=".55"/>' for x in (cx - e - 22 * s, cx + e + 22 * s))
    return out

def g(body, tx, ty, sc):
    return f'<g transform="translate({tx} {ty}) scale({sc})">{body}</g>'

def leaves(pts, cols=("#e08a3c", "#c9653a", "#e6b34a")):
    return "".join(f'<ellipse cx="{x}" cy="{y}" rx="34" ry="16" fill="{cols[i % 3]}" transform="rotate({(i * 47) % 180 - 90} {x} {y})"/>' for i, (x, y) in enumerate(pts))

def snowflakes(n=26, seed=11):
    return "".join(f'<circle cx="{-420+1900*_r(i,seed):.0f}" cy="{60+800*_r(i,seed+1):.0f}" r="{4+7*_r(i,seed+2):.0f}" fill="#ffffff" opacity="{.35+.5*_r(i,seed+3):.2f}"/>' for i in range(n))

def drops(pts, c="#9fd0ff"):
    return "".join(f'<path d="M{x} {y-26} Q{x+16} {y} {x+14} {y+8} A15 15 0 1 1 {x-14} {y+8} Q{x-16} {y} {x} {y-26}Z" fill="{c}"/>' for x, y in pts)

def notes(x, y, c="#c7d2fe"):
    return f'<text x="{x}" y="{y}" font-family="Baloo, sans-serif" font-weight="800" font-size="70" fill="{c}">♪ ♫</text>'

# ---------- environments ----------
def env_scene(env, body, fx="", fx2=""):
    """night_env + extra scenery OUTSIDE the #animal group (so only the subject breathes / gets the shadow)."""
    return svg(night_env() + env + f'<g id="animal">{body}</g><g id="fx" opacity="0">{fx}</g><g id="fx2" opacity="0">{fx2}</g>')

def _pine(x, base, h, c):
    w = h * .42
    return "".join(f'<path d="M{x} {base-h+i*h*.28:.0f} L{x+w*(.6+i*.2):.0f} {base-h*.45+i*h*.22:.0f} L{x-w*(.6+i*.2):.0f} {base-h*.45+i*h*.22:.0f}Z" fill="{c}"/>' for i in range(3)) + f'<rect x="{x-14}" y="{base-h*.2:.0f}" width="28" height="{h*.2:.0f}" fill="{c}"/>'

def forest_scene(body, fx="", fx2=""):
    trees = "".join(_pine(x, b, h, c) for x, b, h, c in ((-420, 940, 520, "#1b2452"), (-250, 960, 400, "#202a5e"), (-110, 970, 300, "#26316a"),
                                                          (1190, 970, 300, "#26316a"), (1330, 960, 420, "#202a5e"), (1490, 940, 520, "#1b2452")))
    return env_scene(trees + '<ellipse cx="540" cy="1010" rx="420" ry="40" fill="#1e2a5a" opacity=".6"/>', body, fx, fx2)

def arctic_scene(body, fx="", fx2=""):
    snow = ('<path d="M-500 880 Q-100 820 300 870 T1100 860 T1600 850 L1600 1110 L-500 1110Z" fill="#dfe8fb"/>'
            '<path d="M-500 970 Q100 930 540 960 T1600 950 L1600 1110 L-500 1110Z" fill="#c9d6f2"/>'
            '<path d="M-470 880 L-400 700 L-330 760 L-260 640 L-170 880Z" fill="#b8cdf2"/><path d="M1260 880 L1330 690 L1400 750 L1470 620 L1560 880Z" fill="#b8cdf2"/>')
    return svg(night_env() + snow + snowflakes() + f'<g id="animal">{body}</g><g id="fx" opacity="0">{fx}</g><g id="fx2" opacity="0">{fx2}</g>')

def icesea_scene(body, fx="", fx2=""):
    bub = "".join(f'<circle cx="{-400+1900*_r(i,5):.0f}" cy="{220+660*_r(i,6):.0f}" r="{6+14*_r(i,7):.0f}" fill="none" stroke="#bfe3ff" stroke-width="4" opacity=".45"/>' for i in range(26))
    ice = ('<path d="M-500 0 H1600 V110 Q1400 150 1200 120 Q1000 170 800 125 Q600 160 400 120 Q200 165 0 120 Q-250 160 -500 120Z" fill="#e6f0ff"/>'
           '<path d="M-500 110 Q-250 150 0 112 Q200 155 400 112 Q600 150 800 117 Q1000 160 1200 112 Q1400 140 1600 102 V125 Q1400 165 1200 135 Q1000 185 800 140 Q600 175 400 135 Q200 180 0 135 Q-250 175 -500 135Z" fill="#b9d3f5"/>')
    rocks = '<path d="M-500 1000 Q-200 940 100 990 T700 980 T1600 975 L1600 1110 L-500 1110Z" fill="#26407a"/>'
    return svg('<rect x="-500" y="0" width="2200" height="1100" fill="#163677"/>' + bub + ice + rocks + f'<g id="animal">{body}</g><g id="fx" opacity="0">{fx}</g><g id="fx2" opacity="0">{fx2}</g>')

def garden_scene(body, fx="", fx2=""):
    def flower(x, y, c, s=1):
        return (f'<path d="M{x} 1000 Q{x-10} {(y+1000)/2:.0f} {x} {y}" stroke="#3f7a5c" stroke-width="{10*s:.0f}" fill="none"/>'
                + "".join(f'<circle cx="{x+26*s*math.cos(math.radians(a)):.0f}" cy="{y+26*s*math.sin(math.radians(a)):.0f}" r="{20*s:.0f}" fill="{c}"/>' for a in range(0, 360, 72))
                + f'<circle cx="{x}" cy="{y}" r="{16*s:.0f}" fill="#ffe082"/>')
    grass = "".join(f'<path d="M{x} 1010 q{8+6*_r(i,8):.0f} -{50+40*_r(i,9):.0f} {22:.0f} -{90+50*_r(i,10):.0f} q-2 {60:.0f} 14 {90+50*_r(i,10):.0f}Z" fill="#2f6655"/>' for i, x in enumerate(range(-480, 1600, 70)))
    fl = flower(-300, 700, "#f8bbd0") + flower(-140, 780, "#d1c4e9", .8) + flower(40, 860, "#fff9c4", .6) + flower(1040, 860, "#f8bbd0", .6) + flower(1220, 780, "#fff9c4", .8) + flower(1380, 700, "#d1c4e9")
    return env_scene('<path d="M-500 990 Q540 950 1600 990 L1600 1110 L-500 1110Z" fill="#244a52"/>' + fl + grass, body, fx, fx2)

def room_scene(body, fx="", fx2="", window=True):
    paper = "".join(f'<path d="M{x} {y-10} l3 7 8 1 -6 5 2 8 -7 -4 -7 4 2 -8 -6 -5 8 -1z" fill="#4b4f9a"/>' for x in range(-460, 1600, 120) for y in range(80, 900, 140))
    win = ('<rect x="80" y="130" width="270" height="290" rx="20" fill="#141a48" stroke="#c9b98f" stroke-width="16"/><path d="M215 130 V420 M80 275 H350" stroke="#c9b98f" stroke-width="10"/>'
           '<path d="M270 170 A40 40 0 1 0 300 240 A32 32 0 1 1 270 170Z" fill="#fff3c4"/>' + "".join(f'<circle cx="{x}" cy="{y}" r="4" fill="#fff8e1"/>' for x, y in ((120, 180), (160, 330), (300, 360), (130, 250), (250, 320)))
           + '<path d="M50 110 Q110 260 60 440 L20 440 L20 110Z M380 110 Q320 260 370 440 L410 440 L410 110Z" fill="#7e6bb8"/>') if window else ""
    return svg('<rect x="-500" y="0" width="2200" height="1100" fill="#2e3170"/>' + paper + win
               + '<rect x="-500" y="955" width="2200" height="160" fill="#463c7a"/><rect x="-500" y="945" width="2200" height="14" fill="#5b4f96"/>'
               + '<ellipse cx="540" cy="1010" rx="440" ry="55" fill="#7e6bb8" opacity=".55"/>'
               + f'<g id="animal">{body}</g><g id="fx" opacity="0">{fx}</g><g id="fx2" opacity="0">{fx2}</g>')

def rain_scene(body, fx="", fx2=""):
    clouds = "".join(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="#4a4f8f" opacity=".9"/>' for x, y, rx, ry in
                     ((-380, 40, 260, 120), (-60, 10, 300, 130), (300, 30, 280, 120), (640, 0, 320, 130), (980, 30, 280, 120), (1340, 10, 300, 130)))
    rain = "".join(f'<path d="M{x:.0f} {y:.0f} l-12 46" stroke="#a9bcff" stroke-width="5" stroke-linecap="round" opacity=".35"/>' for x, y in ((-480 + 2080 * _r(i, 21), 150 + 780 * _r(i, 22)) for i in range(90)))
    ground = ('<path d="M-500 900 Q-200 820 100 880 T700 870 T1600 860 L1600 1110 L-500 1110Z" fill="#2c3570"/>'
              '<path d="M-500 980 Q0 930 540 970 T1600 960 L1600 1110 L-500 1110Z" fill="#232a5c"/>')
    return svg('<rect x="-500" y="0" width="2200" height="1100" fill="#1f2556"/>' + rain + clouds + ground + f'<g id="animal">{body}</g><g id="fx" opacity="0">{fx}</g><g id="fx2" opacity="0">{fx2}</g>')

def track(y=990):
    return ('<rect x="-500" y="%d" width="2200" height="16" fill="#8d6e63"/>' % (y - 8)
            + "".join(f'<rect x="{x}" y="{y-2}" width="34" height="22" rx="4" fill="#5d4037"/>' for x in range(-480, 1600, 70))
            + f'<rect x="-500" y="{y-14}" width="2200" height="10" fill="#b0bec5"/>')

def train_scene(body, fx="", fx2=""):
    return env_scene(track(), body, fx, fx2)

def wheel(x, y, r, c="#3d3466"):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}" stroke="#1f1a3a" stroke-width="8"/><circle cx="{x}" cy="{y}" r="{r*.35:.0f}" fill="#ffd94a"/>'

# ---------- goodnight forest ----------
DEER = forest_scene('<ellipse cx="370" cy="500" rx="90" ry="38" fill="#c68a55" stroke="#7a4e2a" stroke-width="8" transform="rotate(-28 370 500)"/><ellipse cx="370" cy="500" rx="56" ry="18" fill="#ffc6d3" transform="rotate(-28 370 500)"/>'
                    '<ellipse cx="710" cy="500" rx="90" ry="38" fill="#c68a55" stroke="#7a4e2a" stroke-width="8" transform="rotate(28 710 500)"/><ellipse cx="710" cy="500" rx="56" ry="18" fill="#ffc6d3" transform="rotate(28 710 500)"/>'
                    + critter("#c68a55", "#7a4e2a", "none", "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff6e8"/>' for x, y, r in ((480, 505, 13), (540, 485, 15), (600, 505, 13), (330, 800, 18), (370, 760, 14), (750, 800, 18), (710, 760, 14), (320, 870, 14), (760, 870, 14)))
                              + snout("#f3dcc0", "#7a4e2a", False) + '<ellipse cx="540" cy="702" rx="24" ry="16" fill="#3e2723"/>', belly="#f3dcc0"),
                    zzz(), MOON_FX + leaves([(180, 420), (300, 300), (880, 520)]))
FOX = forest_scene('<path d="M700 960 Q990 990 970 760 Q960 620 860 620 Q930 760 850 880 Q790 930 690 925Z" fill="#f08a3c" stroke="#a8521c" stroke-width="10"/><path d="M860 620 Q935 640 950 700 Q900 690 870 660Z" fill="#fff6ec"/>'
                   + critter("#f08a3c", "#a8521c", "cat", '<path d="M390 380 L382 440 L425 418Z M690 380 L698 440 L655 418Z" fill="#5a2e10"/>'
                             '<path d="M380 700 Q460 650 540 690 Q620 650 700 700 Q660 820 540 825 Q420 820 380 700Z" fill="#fff6ec"/><ellipse cx="540" cy="672" rx="16" ry="11" fill="#3e2723"/>', belly="#fff6ec"),
                   zzz(), MOON_FX + leaves([(200, 400), (860, 300)]))
_sp = []
for i, a in enumerate(range(150, 391, 8)):
    rr = 330 if i % 2 == 0 else 270
    _sp.append(f"{540+rr*math.cos(math.radians(a)):.0f},{760+rr*math.sin(math.radians(a)):.0f}")
HEDGEHOG = forest_scene(f'<polygon points="{" ".join(_sp)} 540,960" fill="#8d6748" stroke="#5b3f28" stroke-width="10" stroke-linejoin="round"/>'
                        '<ellipse cx="540" cy="880" rx="240" ry="120" fill="#8d6748" stroke="#5b3f28" stroke-width="10"/><ellipse cx="540" cy="900" rx="150" ry="80" fill="#f3dcc0"/>'
                        '<circle cx="430" cy="545" r="34" fill="#f3dcc0" stroke="#5b3f28" stroke-width="7"/><circle cx="650" cy="545" r="34" fill="#f3dcc0" stroke="#5b3f28" stroke-width="7"/>'
                        '<circle cx="540" cy="680" r="170" fill="#f3dcc0" stroke="#5b3f28" stroke-width="10"/><ellipse cx="540" cy="688" rx="16" ry="11" fill="#3e2723"/>' + face(540, 660, 1.0, mdy=46),
                        zzz(), leaves([(250, 990), (330, 1010), (760, 1000), (830, 985), (420, 1015), (680, 1015)]))
SQUIRREL = forest_scene('<path d="M690 950 Q1010 900 965 600 Q935 380 760 400 Q650 420 700 510 Q800 470 830 570 Q860 770 680 860Z" fill="#a19bb3" stroke="#5f5a6e" stroke-width="10"/>'
                        + '<ellipse cx="430" cy="470" rx="38" ry="62" fill="#a19bb3" stroke="#5f5a6e" stroke-width="8" transform="rotate(-18 430 470)"/><ellipse cx="430" cy="478" rx="18" ry="36" fill="#ffc6d3" transform="rotate(-18 430 478)"/>'
                        '<ellipse cx="650" cy="470" rx="38" ry="62" fill="#a19bb3" stroke="#5f5a6e" stroke-width="8" transform="rotate(18 650 470)"/><ellipse cx="650" cy="478" rx="18" ry="36" fill="#ffc6d3" transform="rotate(18 650 478)"/>'
                        + critter("#a19bb3", "#5f5a6e", "none", '<ellipse cx="540" cy="676" rx="13" ry="9" fill="#ff8fab"/>'
                                  '<ellipse cx="540" cy="895" rx="48" ry="56" fill="#c58b4a" stroke="#7b5232" stroke-width="6"/><path d="M488 870 Q540 810 592 870Z" fill="#7b5232"/><path d="M540 828 v-18" stroke="#7b5232" stroke-width="8"/>'
                                  '<ellipse cx="482" cy="880" rx="30" ry="22" fill="#a19bb3" stroke="#5f5a6e" stroke-width="6"/><ellipse cx="598" cy="880" rx="30" ry="22" fill="#a19bb3" stroke="#5f5a6e" stroke-width="6"/>', belly="#f2eef6"),
                        zzz(), leaves([(200, 300), (300, 420), (870, 260)], ("#c58b4a", "#e08a3c", "#7b5232")))
RACCOON = forest_scene('<path d="M720 930 Q900 910 920 770 Q930 690 880 650" stroke="#8f8b99" stroke-width="80" fill="none" stroke-linecap="round"/>'
                       '<path d="M720 930 Q900 910 920 770 Q930 690 880 650" stroke="#4b4756" stroke-width="80" fill="none" stroke-dasharray="34 38" stroke-dashoffset="10"/>'
                       + critter("#8f8b99", "#4b4756", "cat", '<path d="M405 470 L398 430 L440 460Z M675 470 L682 430 L640 460Z" fill="#f5f3f8"/>'
                                 '<ellipse cx="482" cy="572" rx="50" ry="20" fill="#f5f3f8"/><ellipse cx="598" cy="572" rx="50" ry="20" fill="#f5f3f8"/>'
                                 '<path d="M370 640 Q400 585 470 598 Q540 625 610 598 Q680 585 710 640 Q680 700 610 684 Q540 664 470 684 Q400 700 370 640Z" fill="#4b4756"/>'
                                 '<circle cx="492" cy="640" r="25" fill="#f5f3f8"/><circle cx="588" cy="640" r="25" fill="#f5f3f8"/>'
                                 '<ellipse cx="540" cy="735" rx="95" ry="58" fill="#f5f3f8"/><ellipse cx="540" cy="694" rx="20" ry="13" fill="#2b2733"/>', awake=True, belly="#e8e4ee"),
                       twinkles([(180, 300), (900, 280)]), MOON_FX)

# ---------- snowy dreams ----------
def _noface_mouth(body):
    return body
PENGUIN = arctic_scene('<ellipse cx="350" cy="760" rx="50" ry="130" fill="#2b2f4a" stroke="#151829" stroke-width="8" transform="rotate(20 350 760)"/><ellipse cx="730" cy="760" rx="50" ry="130" fill="#2b2f4a" stroke="#151829" stroke-width="8" transform="rotate(-20 730 760)"/>'
                       '<ellipse cx="480" cy="1000" rx="60" ry="24" fill="#ff9f43"/><ellipse cx="600" cy="1000" rx="60" ry="24" fill="#ff9f43"/>'
                       '<ellipse cx="540" cy="740" rx="210" ry="275" fill="#2b2f4a" stroke="#151829" stroke-width="10"/><ellipse cx="540" cy="800" rx="150" ry="205" fill="#fdfdff"/>'
                       '<circle cx="488" cy="615" r="78" fill="#fdfdff"/><circle cx="592" cy="615" r="78" fill="#fdfdff"/><ellipse cx="540" cy="660" rx="120" ry="70" fill="#fdfdff"/>'
                       '<ellipse cx="400" cy="610" rx="22" ry="34" fill="#ffc94a" opacity=".85"/><ellipse cx="680" cy="610" rx="22" ry="34" fill="#ffc94a" opacity=".85"/>'
                       + face(540, 615, .85, mouth=False) + '<path d="M512 652 L568 652 L540 690Z" fill="#ff9f43" stroke="#e07b1a" stroke-width="4" stroke-linejoin="round"/>',
                       zzz(), '<g transform="translate(830 260)"><path d="M0 -60 A60 60 0 1 0 40 40 A48 48 0 1 1 0 -60Z" fill="#fff3c4"/></g>')
POLARCUB = arctic_scene(critter("#f7f9ff", "#aab8d6", "bear", snout("#ffffff", "#aab8d6", False) + '<ellipse cx="540" cy="702" rx="26" ry="18" fill="#2b2733"/>', belly="#e3eaf8"),
                        zzz(), '<path d="M120 1000 Q120 700 300 700 Q480 700 480 1000Z" fill="#eef4ff" opacity="0"/>' + twinkles([(180, 300), (900, 260)], "#ffffff"))
SEAL = arctic_scene('<path d="M300 760 Q360 940 600 960 Q860 980 960 900 Q1010 870 1040 820 Q980 840 960 880 Q960 830 1000 790 Q930 810 900 860 Q760 840 640 760 Q560 650 470 620 Z" fill="#a9b4c8" stroke="#6c7891" stroke-width="10" stroke-linejoin="round"/>'
                    '<path d="M420 880 Q560 950 760 930 Q600 900 520 840Z" fill="#d7deea"/>'
                    '<ellipse cx="560" cy="930" rx="80" ry="34" fill="#8e9ab3" stroke="#6c7891" stroke-width="7" transform="rotate(-15 560 930)"/>'
                    '<circle cx="440" cy="660" r="160" fill="#a9b4c8" stroke="#6c7891" stroke-width="10"/>'
                    '<ellipse cx="415" cy="715" rx="38" ry="30" fill="#d7deea"/><ellipse cx="465" cy="715" rx="38" ry="30" fill="#d7deea"/><ellipse cx="440" cy="694" rx="17" ry="12" fill="#2b2733"/>'
                    '<path d="M380 715 h-80 M380 730 h-74 M500 715 h80 M500 730 h74" stroke="#6c7891" stroke-width="4"/>' + face(440, 650, .85, mouth=False) + '<path d="M428 744 q12 9 24 0" stroke="#6b2b3a" stroke-width="5" fill="none" stroke-linecap="round"/>',
                    zzz(720, 420), twinkles([(180, 300), (920, 300)], "#ffffff"))
SNOWYOWL = arctic_scene('<ellipse cx="335" cy="760" rx="70" ry="160" fill="#eef2fa" stroke="#b9c3d9" stroke-width="8" transform="rotate(14 335 760)"/><ellipse cx="745" cy="760" rx="70" ry="160" fill="#eef2fa" stroke="#b9c3d9" stroke-width="8" transform="rotate(-14 745 760)"/>'
                        '<ellipse cx="540" cy="730" rx="230" ry="270" fill="#fbfcff" stroke="#b9c3d9" stroke-width="10"/>'
                        + "".join(f'<path d="M{x-14} {y} q14 12 28 0" stroke="#5d6680" stroke-width="6" fill="none" stroke-linecap="round"/>' for x, y in ((420, 800), (480, 860), (600, 860), (660, 800), (540, 910), (440, 920), (640, 920), (360, 700), (720, 700)))
                        + '<ellipse cx="470" cy="610" rx="78" ry="74" fill="#ffffff" stroke="#d5dcea" stroke-width="5"/><ellipse cx="610" cy="610" rx="78" ry="74" fill="#ffffff" stroke="#d5dcea" stroke-width="5"/>'
                        '<circle cx="470" cy="612" r="38" fill="#ffd54f"/><circle cx="610" cy="612" r="38" fill="#ffd54f"/><circle cx="470" cy="618" r="17" fill="#1a1a2e"/><circle cx="610" cy="618" r="17" fill="#1a1a2e"/>'
                        '<path d="M428 612 A42 42 0 0 1 512 612Z M568 612 A42 42 0 0 1 652 612Z" fill="#fbfcff" stroke="#b9c3d9" stroke-width="4"/>'
                        '<path d="M520 650 L560 650 L540 690Z" fill="#5d6680"/><ellipse cx="400" cy="660" rx="18" ry="10" fill="#ff9ab0" opacity=".5"/><ellipse cx="680" cy="660" rx="18" ry="10" fill="#ff9ab0" opacity=".5"/>'
                        '<ellipse cx="480" cy="995" rx="55" ry="30" fill="#ffffff" stroke="#c7d0e2" stroke-width="5"/><ellipse cx="600" cy="995" rx="55" ry="30" fill="#ffffff" stroke="#c7d0e2" stroke-width="5"/>'
                        '<path d="M455 1000 v14 M480 1003 v14 M505 1000 v14 M575 1000 v14 M600 1003 v14 M625 1000 v14" stroke="#c7d0e2" stroke-width="5" stroke-linecap="round"/>',
                        zzz(), '<path d="M880 180 A110 110 0 1 0 960 360 A90 90 0 1 1 880 180Z" fill="#fff3c4"/>')
BELUGA = icesea_scene('<path d="M860 690 Q960 600 1010 540 Q990 650 1050 720 Q960 720 880 760Z" fill="#eef3fb" stroke="#9fb1cf" stroke-width="8"/>'
                      '<path d="M200 700 Q190 520 380 480 Q470 420 570 470 Q800 470 890 660 Q910 770 790 820 Q600 880 360 860 Q210 840 200 700Z" fill="#eef3fb" stroke="#9fb1cf" stroke-width="10"/>'
                      '<path d="M500 840 Q560 930 470 960 Q450 900 440 850Z" fill="#dfe8f6" stroke="#9fb1cf" stroke-width="7"/>'
                      + face(340, 640, .8, mouth=False) + '<path d="M232 720 Q300 770 400 738" stroke="#6b7fa3" stroke-width="7" fill="none" stroke-linecap="round"/>',
                      notes(640, 400), twinkles([(200, 260), (920, 280)], "#ffffff"))

# ---------- garden at night ----------
SNAIL = garden_scene('<path d="M180 990 Q160 900 230 860 Q240 780 260 730 Q300 650 360 700 Q390 780 400 880 Q470 905 900 915 Q970 955 900 992Z" fill="#d7c4a3" stroke="#9c8562" stroke-width="10" stroke-linejoin="round"/>'
                     '<path d="M280 670 Q260 600 240 560 M330 668 Q350 600 370 556" stroke="#9c8562" stroke-width="12" fill="none" stroke-linecap="round"/><circle cx="240" cy="556" r="18" fill="#d7c4a3" stroke="#9c8562" stroke-width="6"/><circle cx="370" cy="552" r="18" fill="#d7c4a3" stroke="#9c8562" stroke-width="6"/>'
                     '<circle cx="305" cy="740" r="82" fill="#d7c4a3"/>' + face(305, 735, .55)
                     + '<circle cx="610" cy="740" r="210" fill="#c98b5e" stroke="#8a5532" stroke-width="10"/><path d="M590 740 a20 20 0 1 1 40 0 a50 50 0 1 1 -100 0 a90 90 0 1 1 180 0 a130 130 0 1 1 -260 0 a170 170 0 1 1 340 0" stroke="#8a5532" stroke-width="12" fill="none" stroke-linecap="round"/>',
                     '<path d="M900 1000 Q1000 1000 1100 990" stroke="#e8f4ff" stroke-width="10" opacity=".7" fill="none"/>' + twinkles([(950, 960), (1050, 950)], "#e8f4ff"), MOON_FX)
MOTH = garden_scene('<path d="M510 560 Q470 470 420 420 M570 560 Q610 470 660 420" stroke="#a89572" stroke-width="7" fill="none"/>'
                    + "".join(f'<path d="M{x} {y} l{d*18} -10" stroke="#a89572" stroke-width="5"/>' for x, y, d in ((480, 510, -1), (462, 485, -1), (445, 462, -1), (600, 510, 1), (618, 485, 1), (635, 462, 1)))
                    + '<path d="M520 620 Q300 420 200 560 Q160 700 500 720Z M560 620 Q780 420 880 560 Q920 700 580 720Z" fill="#cdb8e6" stroke="#8a72b5" stroke-width="10" stroke-linejoin="round"/>'
                    '<path d="M510 720 Q300 760 330 900 Q420 960 520 790Z M570 720 Q780 760 750 900 Q660 960 560 790Z" fill="#b8a0dc" stroke="#8a72b5" stroke-width="10" stroke-linejoin="round"/>'
                    '<circle cx="320" cy="590" r="44" fill="#fff3c4" opacity=".9"/><circle cx="320" cy="590" r="20" fill="#8a72b5"/><circle cx="760" cy="590" r="44" fill="#fff3c4" opacity=".9"/><circle cx="760" cy="590" r="20" fill="#8a72b5"/>'
                    '<circle cx="410" cy="850" r="24" fill="#fff3c4" opacity=".8"/><circle cx="670" cy="850" r="24" fill="#fff3c4" opacity=".8"/>'
                    '<ellipse cx="540" cy="770" rx="70" ry="170" fill="#e8dcc4" stroke="#a89572" stroke-width="10"/>' + "".join(f'<path d="M490 {y} q50 18 100 0" stroke="#cbb994" stroke-width="6" fill="none"/>' for y in (760, 810, 860))
                    + '<circle cx="540" cy="600" r="86" fill="#f1e8d6" stroke="#a89572" stroke-width="10"/>' + face(540, 595, .6, awake=True),
                    '<circle cx="880" cy="250" r="150" fill="#fff3c4" opacity=".15"/><circle cx="880" cy="250" r="80" fill="#fff3c4"/>', twinkles([(180, 300), (300, 200)]))
FROG = garden_scene('<path d="M210 960 A330 70 0 1 0 870 960 A330 70 0 1 0 210 960Z" fill="#3f8f5a" stroke="#2c6b41" stroke-width="8"/><path d="M540 960 L700 910 L720 930Z" fill="#244a52"/>'
                    '<ellipse cx="380" cy="930" rx="80" ry="30" fill="#7cc96b" stroke="#3e7d3a" stroke-width="7"/><ellipse cx="700" cy="930" rx="80" ry="30" fill="#7cc96b" stroke="#3e7d3a" stroke-width="7"/>'
                    '<ellipse cx="540" cy="830" rx="230" ry="140" fill="#7cc96b" stroke="#3e7d3a" stroke-width="10"/><ellipse cx="540" cy="860" rx="140" ry="90" fill="#e6f5c9"/>'
                    '<circle cx="410" cy="530" r="78" fill="#7cc96b" stroke="#3e7d3a" stroke-width="10"/><circle cx="670" cy="530" r="78" fill="#7cc96b" stroke="#3e7d3a" stroke-width="10"/>'
                    '<ellipse cx="540" cy="650" rx="240" ry="150" fill="#7cc96b" stroke="#3e7d3a" stroke-width="10"/><ellipse cx="410" cy="545" rx="58" ry="50" fill="#7cc96b"/><ellipse cx="670" cy="545" rx="58" ry="50" fill="#7cc96b"/>'
                    '<circle cx="410" cy="525" r="44" fill="#fffde7"/><circle cx="670" cy="525" r="44" fill="#fffde7"/>'
                    '<path d="M384 528 q26 18 52 0 M644 528 q26 18 52 0" stroke="#1a1a2e" stroke-width="8" fill="none" stroke-linecap="round"/>'
                    '<path d="M410 690 Q540 770 670 690" stroke="#2c6b41" stroke-width="9" fill="none" stroke-linecap="round"/><circle cx="510" cy="620" r="6" fill="#2c6b41"/><circle cx="570" cy="620" r="6" fill="#2c6b41"/>'
                    '<ellipse cx="350" cy="680" rx="26" ry="14" fill="#ff9ab0" opacity=".6"/><ellipse cx="730" cy="680" rx="26" ry="14" fill="#ff9ab0" opacity=".6"/>',
                    notes(760, 400, "#c8f7c5") + '<ellipse cx="540" cy="770" rx="70" ry="40" fill="#e6f5c9" opacity=".9"/>',
                    '<ellipse cx="540" cy="975" rx="420" ry="60" fill="none" stroke="#9fd8ff" stroke-width="5" opacity=".6"/><ellipse cx="540" cy="975" rx="500" ry="80" fill="none" stroke="#9fd8ff" stroke-width="4" opacity=".4"/>')
LADYBUG = garden_scene('<ellipse cx="540" cy="930" rx="400" ry="110" fill="#5aa06a" stroke="#2f6b45" stroke-width="10"/><path d="M160 930 Q540 900 920 930" stroke="#2f6b45" stroke-width="7" fill="none"/>'
                       '<circle cx="540" cy="760" r="225" fill="#e53935" stroke="#a31515" stroke-width="10"/><path d="M540 560 V980" stroke="#3b3550" stroke-width="10"/>'
                       + "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#3b3550"/>' for x, y, r in ((430, 690, 38), (650, 690, 38), (400, 830, 32), (680, 830, 32), (480, 920, 24), (600, 920, 24)))
                       + '<path d="M500 450 Q470 380 430 360 M580 450 Q610 380 650 360" stroke="#3b3550" stroke-width="9" fill="none" stroke-linecap="round"/><circle cx="430" cy="358" r="16" fill="#3b3550"/><circle cx="650" cy="358" r="16" fill="#3b3550"/>'
                       '<circle cx="540" cy="550" r="125" fill="#4a4363" stroke="#2b2538" stroke-width="10"/><ellipse cx="475" cy="505" rx="24" ry="16" fill="#fff8e1"/><ellipse cx="605" cy="505" rx="24" ry="16" fill="#fff8e1"/>'
                       + face(540, 555, .85, col="#fff8e1", mouth=False) + '<path d="M526 595 q14 11 28 0" stroke="#fff8e1" stroke-width="6" fill="none" stroke-linecap="round"/>',
                       twinkles([(200, 320), (880, 300)]), MOON_FX)
TULIP = garden_scene('<path d="M540 1000 Q530 820 540 690" stroke="#3f7a5c" stroke-width="22" fill="none"/>'
                     '<path d="M535 960 Q380 900 360 760 Q470 800 535 900Z" fill="#5aa06a" stroke="#2f6b45" stroke-width="7"/><path d="M545 930 Q700 880 730 740 Q610 780 545 870Z" fill="#5aa06a" stroke="#2f6b45" stroke-width="7"/>'
                     '<path d="M390 470 Q380 650 460 700 Q540 730 620 700 Q700 650 690 470 Q650 540 615 480 Q580 380 540 360 Q500 380 465 480 Q430 540 390 470Z" fill="#f48fb1" stroke="#c2185b" stroke-width="10" stroke-linejoin="round"/>'
                     '<path d="M465 480 Q500 600 540 610 Q580 600 615 480" stroke="#c2185b" stroke-width="6" fill="none" opacity=".6"/>' + face(540, 610, .62),
                     zzz(720, 420), MOON_FX + twinkles([(200, 300), (320, 200)]))

# ---------- toys go to sleep ----------
def _cube(x, y, s, c, side, top, sym):
    sy = {"moon": f'<path d="M{x+46} {y+28} A26 26 0 1 0 {x+62} {y+72} A21 21 0 1 1 {x+46} {y+28}Z" fill="#fff8e1"/>',
          "star": f'<path d="M{x+46} {y+24} l8 18 20 2 -15 13 5 20 -18 -11 -18 11 5 -20 -15 -13 20 -2z" fill="#fff8e1"/>',
          "heart": f'<path d="M{x+46} {y+70} q-34 -22 -22 -40 q12 -14 22 2 q10 -16 22 -2 q12 18 -22 40z" fill="#fff8e1"/>'}[sym]
    return (f'<path d="M{x} {y} L{x+40} {y-40} L{x+s+40} {y-40} L{x+s} {y}Z" fill="{top}" stroke="#2b2560" stroke-width="7" stroke-linejoin="round"/>'
            f'<path d="M{x+s} {y} L{x+s+40} {y-40} L{x+s+40} {y+s-40} L{x+s} {y+s}Z" fill="{side}" stroke="#2b2560" stroke-width="7" stroke-linejoin="round"/>'
            f'<rect x="{x}" y="{y}" width="{s}" height="{s}" rx="10" fill="{c}" stroke="#2b2560" stroke-width="8"/>' + sy + face(x + s / 2, y + s / 2 + 10, .6))
BLOCKS = room_scene(_cube(290, 770, 220, "#7aa7f0", "#5a86cf", "#a8c6f7", "star") + _cube(550, 770, 220, "#f7a8c4", "#d9849f", "#fbc9da", "heart") + _cube(420, 545, 220, "#ffd76a", "#e0b545", "#ffe7a6", "moon"),
                    zzz(), twinkles([(880, 300), (760, 200)]))
DOLL = room_scene('<circle cx="430" cy="470" r="50" fill="#ff8a50"/><circle cx="650" cy="470" r="50" fill="#ff8a50"/><circle cx="400" cy="560" r="48" fill="#ff8a50"/><circle cx="680" cy="560" r="48" fill="#ff8a50"/><circle cx="410" cy="650" r="44" fill="#ff8a50"/><circle cx="670" cy="650" r="44" fill="#ff8a50"/>'
                  '<rect x="400" y="930" width="70" height="60" rx="20" fill="#fff" stroke="#7e6bb8" stroke-width="6"/><rect x="610" y="930" width="70" height="60" rx="20" fill="#fff" stroke="#7e6bb8" stroke-width="6"/>'
                  '<path d="M405 945 h60 M405 965 h60 M615 945 h60 M615 965 h60" stroke="#7e6bb8" stroke-width="8"/>'
                  '<path d="M470 700 L610 700 L740 950 Q540 990 340 950Z" fill="#b39ddb" stroke="#5e35b1" stroke-width="10" stroke-linejoin="round"/>'
                  '<rect x="500" y="820" width="80" height="70" rx="10" fill="#f8bbd0" stroke="#5e35b1" stroke-width="5" stroke-dasharray="10 8"/>'
                  '<path d="M480 730 Q380 800 400 880 M600 730 Q700 800 680 880" stroke="#ffd6b0" stroke-width="44" fill="none" stroke-linecap="round"/>'
                  '<circle cx="540" cy="570" r="140" fill="#ffd6b0" stroke="#c48a62" stroke-width="10"/>'
                  '<path d="M420 520 Q440 420 540 425 Q640 420 660 520 Q620 470 580 495 Q560 460 540 490 Q520 460 500 495 Q460 470 420 520Z" fill="#ff8a50"/>' + face(540, 580, .8),
                  zzz(), twinkles([(880, 300), (760, 200)]))
ROCKHORSE = room_scene('<path d="M170 920 Q540 1060 910 920" stroke="#8d5a32" stroke-width="36" fill="none" stroke-linecap="round"/>'
                       '<path d="M380 760 L330 960 M460 770 L440 985 M660 770 L680 985 M740 760 L790 960" stroke="#c68a55" stroke-width="30" stroke-linecap="round"/>'
                       '<path d="M780 700 Q900 720 900 860 Q860 800 800 790Z" fill="#e57373" stroke="#b23b3b" stroke-width="6"/>'
                       '<ellipse cx="560" cy="720" rx="250" ry="110" fill="#f6c28b" stroke="#a8693a" stroke-width="10"/>'
                       '<path d="M470 620 Q560 600 640 640 L640 740 Q560 770 470 740Z" fill="#e57373" stroke="#b23b3b" stroke-width="7"/>'
                       '<path d="M330 720 Q320 600 300 540 L420 500 Q450 620 440 700Z" fill="#f6c28b" stroke="#a8693a" stroke-width="10" stroke-linejoin="round"/>'
                       '<ellipse cx="300" cy="480" rx="120" ry="82" fill="#f6c28b" stroke="#a8693a" stroke-width="10" transform="rotate(-20 300 480)"/>'
                       '<path d="M330 390 L345 320 L385 380Z" fill="#f6c28b" stroke="#a8693a" stroke-width="8"/>'
                       '<path d="M370 400 Q420 440 440 520 Q450 590 450 680" stroke="#e57373" stroke-width="34" fill="none" stroke-linecap="round"/>'
                       '<path d="M290 470 q22 16 44 0" stroke="#1a1a2e" stroke-width="7" fill="none" stroke-linecap="round"/><circle cx="200" cy="520" r="8" fill="#a8693a"/>'
                       '<path d="M220 560 q24 16 48 0" stroke="#6b2b3a" stroke-width="6" fill="none" stroke-linecap="round"/><ellipse cx="320" cy="520" rx="18" ry="10" fill="#ff9ab0" opacity=".6"/>',
                       zzz(), twinkles([(880, 300), (760, 200)]))
BOAT = room_scene('<ellipse cx="540" cy="960" rx="420" ry="70" fill="#7fb8ef" stroke="#4f86c6" stroke-width="7"/><path d="M200 960 q40 -16 80 0 M760 960 q40 -16 80 0" stroke="#d5ecff" stroke-width="6" fill="none"/>'
                  '<path d="M540 820 V420" stroke="#8d5a32" stroke-width="14" stroke-linecap="round"/>'
                  '<path d="M555 440 L555 800 L800 800Z" fill="#fff8e1" stroke="#c9b98f" stroke-width="7" stroke-linejoin="round"/><path d="M525 490 L525 800 L330 800Z" fill="#a8d4ff" stroke="#6aa2db" stroke-width="7" stroke-linejoin="round"/>'
                  '<path d="M540 420 L620 440 L540 460Z" fill="#ffd94a"/>'
                  '<path d="M250 820 L830 820 L750 950 L330 950Z" fill="#ef6c6c" stroke="#b23b3b" stroke-width="10" stroke-linejoin="round"/><path d="M290 860 H790" stroke="#fff8e1" stroke-width="10"/>' + face(540, 900, .6),
                  zzz(), twinkles([(880, 300), (200, 560)]))
TOYBOX = room_scene('<path d="M290 700 L330 560 L820 560 L790 700Z" fill="#a8693a" stroke="#6d4123" stroke-width="10" stroke-linejoin="round"/>'
                    '<circle cx="420" cy="680" r="70" fill="#ef6c6c" stroke="#b23b3b" stroke-width="8"/><path d="M360 650 Q420 690 480 650" stroke="#fff8e1" stroke-width="10" fill="none"/>'
                    '<circle cx="570" cy="620" r="30" fill="#c58b5a" stroke="#7b5232" stroke-width="6"/><circle cx="650" cy="620" r="30" fill="#c58b5a" stroke="#7b5232" stroke-width="6"/><circle cx="610" cy="670" r="62" fill="#c58b5a" stroke="#7b5232" stroke-width="8"/>' + face(610, 668, .45)
                    + '<rect x="690" y="610" width="90" height="90" rx="8" fill="#7aa7f0" stroke="#2b2560" stroke-width="6" transform="rotate(12 735 655)"/>'
                    '<rect x="280" y="700" width="520" height="280" rx="18" fill="#c68a55" stroke="#7b4e2a" stroke-width="10"/><path d="M280 790 H800 M280 880 H800" stroke="#a8693a" stroke-width="6"/>'
                    '<rect x="270" y="690" width="540" height="34" rx="12" fill="#a8693a" stroke="#7b4e2a" stroke-width="6"/>'
                    + "".join(f'<path d="M{x} {y-18} l5 13 14 1 -11 9 4 14 -12 -8 -12 8 4 -14 -11 -9 14 -1z" fill="#ffd94a"/>' for x, y in ((340, 760), (740, 940), (740, 770)))
                    + face(540, 840, .9),
                    zzz(), twinkles([(880, 300), (760, 200)]))

# ---------- rainy night ----------
RAINDROP = rain_scene('<circle cx="540" cy="760" r="240" fill="#8ec5ff" opacity=".18"/><path d="M540 380 Q720 620 720 760 A180 180 0 1 1 360 760 Q360 620 540 380Z" fill="#8ec5ff" stroke="#3f7fd0" stroke-width="10"/>'
                      '<ellipse cx="460" cy="700" rx="26" ry="60" fill="#ffffff" opacity=".55" transform="rotate(20 460 700)"/>' + face(540, 780, .9),
                      drops([(220, 420), (320, 300), (820, 330), (900, 470), (180, 640), (880, 650)]),
                      '<path d="M170 1000 Q160 900 180 860" stroke="#5aa06a" stroke-width="10" fill="none"/><circle cx="180" cy="850" r="24" fill="#f8bbd0"/><path d="M900 1000 Q910 920 890 880" stroke="#5aa06a" stroke-width="10" fill="none"/><circle cx="890" cy="870" r="24" fill="#fff9c4"/>')
_win_rain = "".join(f'<path d="M{x:.0f} {y:.0f} l-8 30" stroke="#a9bcff" stroke-width="4" stroke-linecap="round" opacity=".5"/>' for x, y in ((320 + 420 * _r(i, 31), 420 + 380 * _r(i, 32)) for i in range(26)))
WINDOW = room_scene('<rect x="250" y="360" width="580" height="560" rx="16" fill="#1d2a66"/>' + _win_rain
                    + drops([(330, 470), (470, 560), (640, 450), (740, 620), (380, 760), (600, 800), (720, 860), (420, 880)], "#cfe6ff")
                    + '<rect x="250" y="360" width="580" height="560" rx="16" fill="none" stroke="#c9b98f" stroke-width="24"/><path d="M540 360 V920 M250 640 H830" stroke="#c9b98f" stroke-width="16"/>'
                    '<path d="M180 330 Q280 620 200 960 L130 960 L130 330Z M900 330 Q800 620 880 960 L950 960 L950 330Z" fill="#7e6bb8" stroke="#5e35b1" stroke-width="6"/>'
                    '<rect x="200" y="915" width="680" height="40" rx="10" fill="#c9b98f"/>'
                    + g(critter("#b8b4c8", "#77738a", "cat", '<path d="M540 690 l-14 -12 h28z" fill="#ff8fab"/>', belly="#ece9f4"), 370, 590, .32),
                    '<circle cx="540" cy="500" r="0"/>' + drops([(330, 500), (700, 520), (460, 700)], "#e3f1ff"), twinkles([(80, 200), (1000, 220)], "#cfe6ff"), window=False)
UMBRELLA = rain_scene('<ellipse cx="540" cy="1000" rx="260" ry="34" fill="#4f86c6" opacity=".55"/>'
                      '<path d="M540 620 V940" stroke="#5d4037" stroke-width="18"/><path d="M540 940 q0 55 -45 55 q-40 0 -40 -38" stroke="#5d4037" stroke-width="18" fill="none" stroke-linecap="round"/>'
                      '<path d="M200 640 Q230 330 540 320 Q850 330 880 640 Q827 595 773 640 Q720 595 667 640 Q613 595 560 640 Q507 595 453 640 Q400 595 347 640 Q293 595 240 640Z" fill="#b39ddb" stroke="#5e35b1" stroke-width="10" stroke-linejoin="round"/>'
                      '<path d="M540 320 Q450 450 453 640 M540 320 Q630 450 627 640 M540 320 Q300 420 280 640 M540 320 Q780 420 800 640" stroke="#7e57c2" stroke-width="6" fill="none"/>'
                      '<circle cx="540" cy="310" r="16" fill="#5e35b1"/>' + face(540, 500, .8),
                      drops([(230, 700), (850, 690), (180, 840), (900, 860)]), drops([(300, 230), (780, 220), (540, 150)]))
WORM = garden_scene('<ellipse cx="820" cy="1000" rx="150" ry="50" fill="#6d4c41"/>'
                    '<path d="M800 1000 Q800 860 660 860 Q500 860 480 740 Q470 640 360 625" stroke="#f4a3b5" stroke-width="100" fill="none" stroke-linecap="round"/>'
                    '<path d="M800 1000 Q800 860 660 860 Q500 860 480 740 Q470 640 360 625" stroke="#d97a92" stroke-width="100" fill="none" stroke-dasharray="5 46" opacity=".55"/>'
                    '<path d="M720 870 Q780 880 790 950" stroke="#e98da5" stroke-width="40" fill="none" opacity=".0"/>'
                    '<circle cx="345" cy="622" r="78" fill="#f4a3b5"/>' + face(345, 618, .58),
                    drops([(200, 400), (330, 300), (800, 360), (900, 500), (650, 260)]), '<ellipse cx="540" cy="1000" rx="200" ry="22" fill="#5a7fb8" opacity=".7"/>')
_bow = ["#f6c9cf", "#f8dcc0", "#f6efc4", "#cfeccd", "#c9dcf6", "#dccff3"]
MOONBOW = rain_scene("".join(f'<path d="M{540-r} 1000 A{r} {r} 0 0 1 {540+r} 1000" stroke="{c}" stroke-width="34" fill="none" opacity=".85"/>' for r, c in zip(range(440, 230, -36), _bow))
                     + '<path d="M60 1000 Q30 900 120 880 Q130 800 220 820 Q280 770 330 840 Q400 850 380 940 Q420 1000 360 1000Z" fill="#e8eaf6" stroke="#b0b6dd" stroke-width="8"/>' + face(230, 905, .55)
                     + '<path d="M1020 1000 Q1050 900 960 880 Q950 800 860 820 Q800 770 750 840 Q680 850 700 940 Q660 1000 720 1000Z" fill="#e8eaf6" stroke="#b0b6dd" stroke-width="8"/>' + face(850, 905, .55),
                     twinkles([(540, 420), (300, 500), (780, 500)]), '<path d="M880 120 A90 90 0 1 0 950 270 A72 72 0 1 1 880 120Z" fill="#fff3c4"/>')

# ---------- sleepy train to dreamland ----------
ENGINE = train_scene('<path d="M220 880 L280 760 L300 880Z" fill="#7e6bb8" stroke="#4a3d82" stroke-width="7"/>'
                     '<rect x="330" y="520" width="90" height="140" rx="12" fill="#5c6bc0" stroke="#283593" stroke-width="8"/><rect x="315" y="505" width="120" height="34" rx="10" fill="#3949ab" stroke="#283593" stroke-width="7"/>'
                     '<rect x="260" y="640" width="500" height="230" rx="90" fill="#9b8bd6" stroke="#4a3d82" stroke-width="10"/><rect x="420" y="640" width="30" height="230" fill="#b9acec"/><rect x="580" y="640" width="30" height="230" fill="#b9acec"/>'
                     '<circle cx="270" cy="740" r="34" fill="#fff59d" stroke="#f9a825" stroke-width="6"/>'
                     '<rect x="700" y="500" width="230" height="370" rx="16" fill="#7e6bb8" stroke="#4a3d82" stroke-width="10"/><rect x="680" y="480" width="270" height="44" rx="14" fill="#5c6bc0" stroke="#283593" stroke-width="8"/>'
                     '<rect x="740" y="560" width="150" height="120" rx="16" fill="#ffe9a8" stroke="#4a3d82" stroke-width="7"/>'
                     + wheel(360, 910, 62) + wheel(520, 910, 62) + wheel(810, 900, 80) + face(520, 735, .8),
                     "".join(f'<ellipse cx="{x}" cy="{y}" rx="{r}" ry="{r*.7:.0f}" fill="#e8eaf6" opacity="{o}"/>' for x, y, r, o in ((375, 440, 60, .9), (300, 340, 80, .75), (200, 220, 100, .55))),
                     twinkles([(880, 300), (640, 260)]))
def _head(x, y, c, dark, kind):
    ears = {"bunny": f'<ellipse cx="{x-22}" cy="{y-60}" rx="14" ry="44" fill="{c}" stroke="{dark}" stroke-width="4"/><ellipse cx="{x+22}" cy="{y-60}" rx="14" ry="44" fill="{c}" stroke="{dark}" stroke-width="4"/>',
            "bear": f'<circle cx="{x-40}" cy="{y-36}" r="20" fill="{c}" stroke="{dark}" stroke-width="4"/><circle cx="{x+40}" cy="{y-36}" r="20" fill="{c}" stroke="{dark}" stroke-width="4"/>',
            "lamb": "".join(f'<circle cx="{x+50*math.cos(math.radians(a)):.0f}" cy="{y+46*math.sin(math.radians(a)):.0f}" r="22" fill="#fff" stroke="#d6d3e8" stroke-width="3"/>' for a in range(180, 361, 36))}[kind]
    return ears + f'<circle cx="{x}" cy="{y}" r="52" fill="{c}" stroke="{dark}" stroke-width="5"/>' + face(x, y, .38)
SLEEPCAR = train_scene('<path d="M150 600 Q540 500 930 600 L930 620 L150 620Z" fill="#3949ab" stroke="#1a237e" stroke-width="8"/>'
                       '<rect x="160" y="600" width="760" height="300" rx="24" fill="#5c6bc0" stroke="#283593" stroke-width="10"/><rect x="160" y="840" width="760" height="22" fill="#3949ab"/>'
                       + "".join(f'<rect x="{x}" y="640" width="200" height="170" rx="20" fill="#ffe9a8" stroke="#283593" stroke-width="8"/>' for x in (200, 440, 680))
                       + _head(300, 730, "#f1eef9", "#b9b2d6", "bunny") + _head(540, 730, "#a97c50", "#6d4c2f", "bear") + _head(780, 730, "#fdfbff", "#d6d3e8", "lamb")
                       + "".join(f'<path d="M{x} 810 Q{x+100} 760 {x+200} 810Z" fill="{c}"/>' for x, c in ((200, "#f48fb1"), (440, "#90caf9"), (680, "#c5e1a5")))
                       + wheel(280, 920, 54) + wheel(420, 920, 54) + wheel(660, 920, 54) + wheel(800, 920, 54),
                       zzz(700, 470), twinkles([(200, 300), (880, 260)]))
BRIDGE = svg(night_env() + '<path d="M-500 860 Q540 820 1600 860 L1600 1110 L-500 1110Z" fill="#2a4a8a"/>'
             + "".join(f'<path d="M{x} {y} h{w}" stroke="#7fa6e6" stroke-width="6" stroke-linecap="round" opacity=".55"/>' for x, y, w in ((-300, 920, 160), (100, 960, 120), (700, 940, 180), (1100, 990, 140), (300, 1040, 200)))
             + '<rect x="-500" y="610" width="2200" height="60" fill="#7a6aa8" stroke="#4a3d82" stroke-width="8"/>'
             + "".join(f'<path d="M{x} 670 L{x} 940 L{x+70} 940 L{x+70} 670Z" fill="#7a6aa8" stroke="#4a3d82" stroke-width="8"/>' for x in (-330, 70, 470, 870, 1270))
             + "".join(f'<path d="M{x+70} 940 Q{x+235} 720 {x+400} 940" stroke="#4a3d82" stroke-width="8" fill="none"/>' for x in (-330, 70, 470, 870))
             + "".join(f'<path d="M{x} 600 V560" stroke="#4a3d82" stroke-width="8"/>' for x in range(-480, 1600, 80)) + '<path d="M-500 560 H1600" stroke="#4a3d82" stroke-width="8"/><g id="animal">'
             + g('<rect x="0" y="0" width="200" height="110" rx="40" fill="#9b8bd6" stroke="#4a3d82" stroke-width="8"/><rect x="160" y="-50" width="100" height="160" rx="10" fill="#7e6bb8" stroke="#4a3d82" stroke-width="8"/><rect x="180" y="-30" width="60" height="50" rx="8" fill="#ffe9a8"/><rect x="40" y="-50" width="40" height="60" fill="#5c6bc0"/>'
                 + face(110, 50, .5) + '<rect x="290" y="-20" width="220" height="130" rx="14" fill="#5c6bc0" stroke="#283593" stroke-width="8"/><rect x="310" y="5" width="80" height="60" rx="8" fill="#ffe9a8"/><rect x="410" y="5" width="80" height="60" rx="8" fill="#ffe9a8"/>'
                 '<rect x="540" y="-20" width="220" height="130" rx="14" fill="#5c6bc0" stroke="#283593" stroke-width="8"/><rect x="560" y="5" width="80" height="60" rx="8" fill="#ffe9a8"/><rect x="660" y="5" width="80" height="60" rx="8" fill="#ffe9a8"/>'
                 + "".join(f'<circle cx="{x}" cy="115" r="22" fill="#3d3466"/>' for x in (50, 150, 220, 340, 460, 590, 710)), 160, 470, 1)
             + '</g><g id="fx" opacity="0">' + "".join(f'<ellipse cx="{x}" cy="{y}" rx="{r}" ry="{r*.7:.0f}" fill="#e8eaf6" opacity="{o}"/>' for x, y, r, o in ((230, 360, 50, .9), (160, 280, 70, .7), (90, 190, 90, .5)))
             + '</g><g id="fx2" opacity="0"><ellipse cx="540" cy="1000" rx="90" ry="24" fill="#fff3c4" opacity=".6"/>' + twinkles([(760, 240), (900, 380)]) + '</g>')
CABOOSE = train_scene('<rect x="250" y="590" width="580" height="290" rx="20" fill="#e57373" stroke="#b23b3b" stroke-width="10"/><rect x="230" y="570" width="620" height="40" rx="14" fill="#c62828" stroke="#8e1b1b" stroke-width="8"/>'
                      '<rect x="430" y="460" width="220" height="120" rx="14" fill="#e57373" stroke="#b23b3b" stroke-width="10"/><rect x="410" y="440" width="260" height="34" rx="12" fill="#c62828" stroke="#8e1b1b" stroke-width="7"/>'
                      '<rect x="470" y="490" width="60" height="60" rx="8" fill="#ffe9a8"/><rect x="550" y="490" width="60" height="60" rx="8" fill="#ffe9a8"/>'
                      '<rect x="290" y="640" width="100" height="100" rx="14" fill="#ffe9a8" stroke="#b23b3b" stroke-width="6"/><rect x="690" y="640" width="100" height="100" rx="14" fill="#ffe9a8" stroke="#b23b3b" stroke-width="6"/>'
                      '<path d="M830 700 H900 M900 600 V860 M180 700 H250 M180 600 V860" stroke="#5d4037" stroke-width="10" stroke-linecap="round"/>'
                      '<path d="M900 640 v30" stroke="#5d4037" stroke-width="6"/><circle cx="940" cy="700" r="70" fill="#ffd94a" opacity=".25"/><rect x="915" y="670" width="50" height="64" rx="10" fill="#fff59d" stroke="#5d4037" stroke-width="6"/><path d="M915 670 Q940 645 965 670" stroke="#5d4037" stroke-width="6" fill="none"/>'
                      + wheel(360, 910, 60) + wheel(720, 910, 60) + face(540, 720, .85),
                      twinkles([(200, 300), (900, 260)]), '<path d="M120 200 A70 70 0 1 0 170 320 A55 55 0 1 1 120 200Z" fill="#fff3c4"/>')
STATION = train_scene('<rect x="230" y="930" width="2200" height="40" fill="#6f6496" transform="translate(-730 0)"/>'
                      '<rect x="270" y="600" width="540" height="330" rx="12" fill="#c5b8ea" stroke="#5e35b1" stroke-width="10"/>'
                      '<path d="M200 620 L540 400 L880 620Z" fill="#7e57c2" stroke="#4a2d8a" stroke-width="10" stroke-linejoin="round"/>'
                      '<rect x="460" y="760" width="160" height="170" rx="70" fill="#5e35b1"/><rect x="310" y="680" width="110" height="110" rx="16" fill="#ffe9a8" stroke="#5e35b1" stroke-width="7"/><rect x="660" y="680" width="110" height="110" rx="16" fill="#ffe9a8" stroke="#5e35b1" stroke-width="7"/>'
                      '<circle cx="540" cy="540" r="70" fill="#fff3c4" stroke="#4a2d8a" stroke-width="8"/>' + face(540, 535, .55)
                      + '<path d="M960 930 V560" stroke="#3d3466" stroke-width="16"/><circle cx="960" cy="540" r="90" fill="#fff59d" opacity=".22"/><rect x="930" y="510" width="60" height="70" rx="12" fill="#fff59d" stroke="#3d3466" stroke-width="7"/>'
                      '<rect x="100" y="860" width="140" height="22" rx="6" fill="#8d5a32"/><path d="M115 882 v40 M225 882 v40 M100 830 h140" stroke="#8d5a32" stroke-width="10"/>',
                      zzz(700, 380), twinkles([(160, 300), (880, 200)]))

# ---------- wind-down extras (Shorts) ----------
COUNTSTARS = scene('<path d="M540 420 L605 590 L785 598 L645 712 L695 885 L540 785 L385 885 L435 712 L295 598 L475 590Z" fill="#ffe082" stroke="#f9a825" stroke-width="12" stroke-linejoin="round"/>' + face(540, 670, .8),
                   "".join(f'<text x="{x}" y="{y+90}" text-anchor="middle" font-family="Baloo, sans-serif" font-weight="800" font-size="54" fill="#fff3c4">{i+1}</text>' for i, (x, y) in enumerate(((150, 260), (330, 180), (750, 180), (930, 260), (180, 620)))),
                   twinkles([(150, 260), (330, 180), (750, 180), (930, 260), (180, 620)]))
BALLOON = scene('<path d="M540 870 Q510 930 560 980 Q600 1010 560 1040" stroke="#e8eaf6" stroke-width="6" fill="none"/>'
                '<path d="M540 380 Q760 380 760 620 Q760 820 560 860 L575 885 L505 885 L520 860 Q320 820 320 620 Q320 380 540 380Z" fill="#b39ddb" stroke="#5e35b1" stroke-width="10" stroke-linejoin="round"/>'
                '<ellipse cx="440" cy="520" rx="34" ry="64" fill="#ffffff" opacity=".45" transform="rotate(20 440 520)"/>' + face(540, 640, .9),
                '<circle cx="540" cy="630" r="300" fill="none" stroke="#d1c4e9" stroke-width="8" stroke-dasharray="20 18" opacity=".8"/><circle cx="540" cy="630" r="360" fill="none" stroke="#d1c4e9" stroke-width="6" stroke-dasharray="14 18" opacity=".5"/>',
                '<path d="M180 640 q40 -40 80 0 q40 40 80 0" stroke="#c7d2fe" stroke-width="10" fill="none" stroke-linecap="round"/><path d="M740 640 q40 -40 80 0 q40 40 80 0" stroke="#c7d2fe" stroke-width="10" fill="none" stroke-linecap="round"/>')
_arm = []
for i in range(10):
    a = math.radians(-90 + i * 36); rr = 330 if i % 2 == 0 else 140
    _arm.append(f"{540+rr*math.cos(a):.0f},{700+rr*math.sin(a):.0f}")
STARFISH = svg(night_env() + '<path d="M-500 920 Q540 880 1600 920 L1600 1110 L-500 1110Z" fill="#cdb48a"/><path d="M-500 880 Q0 850 540 875 T1600 870" stroke="#9fd8ff" stroke-width="8" fill="none" opacity=".6"/>'
               + f'<g id="animal"><polygon points="{" ".join(_arm)}" fill="#ff9e80" stroke="#d8603e" stroke-width="12" stroke-linejoin="round"/>'
               + "".join(f'<circle cx="{540+(rr)*math.cos(math.radians(-90+k*72)):.0f}" cy="{700+(rr)*math.sin(math.radians(-90+k*72)):.0f}" r="10" fill="#ffd0bf"/>' for k in range(5) for rr in (200, 260))
               + face(540, 690, .75) + '</g><g id="fx" opacity="0">'
               + "".join(f'<path d="M{540+380*math.cos(math.radians(-90+k*72)):.0f} {700+380*math.sin(math.radians(-90+k*72)):.0f} L{540+440*math.cos(math.radians(-90+k*72)):.0f} {700+440*math.sin(math.radians(-90+k*72)):.0f}" stroke="#fff3c4" stroke-width="14" stroke-linecap="round" stroke-dasharray="4 22"/>' for k in range(5))
               + '</g><g id="fx2" opacity="0">' + twinkles([(180, 260), (900, 260)]) + '</g>')
FORT = room_scene('<path d="M160 960 L330 520 L750 520 L920 960Z" fill="#9fa8da" stroke="#5c6bc0" stroke-width="10" stroke-linejoin="round"/>'
                  + "".join(f'<path d="M{x} {y-14} l4 10 11 1 -8 7 3 11 -10 -6 -10 6 3 -11 -8 -7 11 -1z" fill="#fff3c4"/>' for x, y in ((300, 700), (380, 600), (700, 600), (790, 720), (260, 860), (820, 880)))
                  + '<path d="M540 560 L400 960 L680 960Z" fill="#ffe9a8"/><ellipse cx="540" cy="930" rx="120" ry="34" fill="#f48fb1"/>'
                  + g(critter("#c58b5a", "#7b5232", "bear", snout("#f1d3b0", "#7b5232", False) + '<ellipse cx="540" cy="700" rx="24" ry="16" fill="#3e2723"/>', belly="#f1d3b0"), 435, 700, .2)
                  + '<path d="M540 560 Q470 760 430 960 L400 960 Z M540 560 Q610 760 650 960 L680 960Z" fill="#7986cb"/>'
                  + '<path d="M330 520 Q540 470 750 520" stroke="#3d3466" stroke-width="4" fill="none"/>' + "".join(f'<circle cx="{x}" cy="{y}" r="12" fill="{c}"/>' for x, y, c in ((380, 508, "#fff59d"), (450, 497, "#f8bbd0"), (540, 494, "#b3e5fc"), (630, 497, "#fff59d"), (700, 508, "#f8bbd0")))
                  + '<path d="M120 960 Q100 900 150 880 L260 880 Q290 900 280 960Z" fill="#c5cae9"/>',
                  "".join(f'<circle cx="{x}" cy="{y}" r="26" fill="{c}" opacity=".35"/>' for x, y, c in ((380, 508, "#fff59d"), (450, 497, "#f8bbd0"), (540, 494, "#b3e5fc"), (630, 497, "#fff59d"), (700, 508, "#f8bbd0"))),
                  zzz())

SCENES_MOON2 = {
    "mb2_deer": DEER, "mb2_fox": FOX, "mb2_hedgehog": HEDGEHOG, "mb2_squirrel": SQUIRREL, "mb2_raccoon": RACCOON,
    "mb2_penguin": PENGUIN, "mb2_polarbear": POLARCUB, "mb2_seal": SEAL, "mb2_snowyowl": SNOWYOWL, "mb2_beluga": BELUGA,
    "mb2_snail": SNAIL, "mb2_moth": MOTH, "mb2_frog": FROG, "mb2_ladybug": LADYBUG, "mb2_tulip": TULIP,
    "mb2_blocks": BLOCKS, "mb2_doll": DOLL, "mb2_rockhorse": ROCKHORSE, "mb2_boat": BOAT, "mb2_toybox": TOYBOX,
    "mb2_raindrop": RAINDROP, "mb2_window": WINDOW, "mb2_umbrella": UMBRELLA, "mb2_worm": WORM, "mb2_moonbow": MOONBOW,
    "mb2_engine": ENGINE, "mb2_sleepcar": SLEEPCAR, "mb2_bridge": BRIDGE, "mb2_caboose": CABOOSE, "mb2_station": STATION,
    "mb2_countstars": COUNTSTARS, "mb2_balloon": BALLOON, "mb2_starfish": STARFISH, "mb2_fort": FORT,
}
NAMES_MOON2 = {
    "mb2_deer": "DEER", "mb2_fox": "FOX", "mb2_hedgehog": "HEDGEHOG", "mb2_squirrel": "SQUIRREL", "mb2_raccoon": "RACCOON",
    "mb2_penguin": "PENGUIN", "mb2_polarbear": "POLAR BEAR", "mb2_seal": "SEAL", "mb2_snowyowl": "SNOWY OWL", "mb2_beluga": "BELUGA WHALE",
    "mb2_snail": "SNAIL", "mb2_moth": "MOTH", "mb2_frog": "FROG", "mb2_ladybug": "LADYBUG", "mb2_tulip": "TULIP",
    "mb2_blocks": "BLOCKS", "mb2_doll": "RAG DOLL", "mb2_rockhorse": "ROCKING HORSE", "mb2_boat": "TOY BOAT", "mb2_toybox": "TOY BOX",
    "mb2_raindrop": "RAINDROP", "mb2_window": "RAINY WINDOW", "mb2_umbrella": "UMBRELLA", "mb2_worm": "EARTHWORM", "mb2_moonbow": "MOONBOW",
    "mb2_engine": "DREAM TRAIN", "mb2_sleepcar": "SLEEPING CAR", "mb2_bridge": "BRIDGE", "mb2_caboose": "CABOOSE", "mb2_station": "STATION",
    "mb2_countstars": "COUNT THE STARS", "mb2_balloon": "BALLOON BREATH", "mb2_starfish": "STARFISH STRETCH", "mb2_fort": "BLANKET FORT",
}
