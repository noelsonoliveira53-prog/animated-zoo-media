"""Original art for Moonbeam Bedtime: calm night scenes, sleepy friends, soft colors. 1080x1100 frame, floor ~y1000.
Scene keys are prefixed mb_ so they never collide with other channels."""
import math

def svg(body):
    return f'<svg viewBox="0 0 1080 1100" width="1080" height="1100">{body}</svg>'

def _r(i, s):
    return (math.sin(i * 12.9898 + s * 78.233) * 43758.5453) % 1

def night_env():
    stars = "".join(f'<circle cx="{-480+2040*_r(i,1):.0f}" cy="{40+520*_r(i,2):.0f}" r="{2+4*_r(i,3):.1f}" fill="#fff8e1" opacity="{.4+.6*_r(i,4):.2f}"/>' for i in range(70))
    return (stars + '<circle cx="1300" cy="180" r="90" fill="#fff3c4" opacity=".25"/><circle cx="1300" cy="180" r="60" fill="#fff3c4"/>'
            '<path d="M-500 900 Q-200 820 100 880 T700 870 T1600 860 L1600 1110 L-500 1110Z" fill="#2c3570"/>'
            '<path d="M-500 980 Q0 930 540 970 T1600 960 L1600 1110 L-500 1110Z" fill="#232a5c"/>')

def sleepy_face(cx, cy, s=1.0, awake=False):
    ex = 44 * s
    if awake:
        eyes = (f'<circle cx="{cx-ex:.0f}" cy="{cy:.0f}" r="{16*s:.0f}" fill="#1a1a2e"/><circle cx="{cx+ex:.0f}" cy="{cy:.0f}" r="{16*s:.0f}" fill="#1a1a2e"/>'
                f'<circle cx="{cx-ex+5*s:.0f}" cy="{cy-5*s:.0f}" r="{5*s:.0f}" fill="#fff"/><circle cx="{cx+ex+5*s:.0f}" cy="{cy-5*s:.0f}" r="{5*s:.0f}" fill="#fff"/>')
    else:
        eyes = (f'<path d="M{cx-ex-18*s:.0f} {cy:.0f} q{18*s:.0f} {14*s:.0f} {36*s:.0f} 0" stroke="#1a1a2e" stroke-width="{7*s:.0f}" fill="none" stroke-linecap="round"/>'
                f'<path d="M{cx+ex-18*s:.0f} {cy:.0f} q{18*s:.0f} {14*s:.0f} {36*s:.0f} 0" stroke="#1a1a2e" stroke-width="{7*s:.0f}" fill="none" stroke-linecap="round"/>')
    return (eyes + f'<path d="M{cx-16*s:.0f} {cy+40*s:.0f} q{16*s:.0f} {12*s:.0f} {32*s:.0f} 0" stroke="#6b2b3a" stroke-width="{6*s:.0f}" fill="none" stroke-linecap="round"/>'
            f'<ellipse cx="{cx-ex-22*s:.0f}" cy="{cy+30*s:.0f}" rx="{18*s:.0f}" ry="{10*s:.0f}" fill="#ff9ab0" opacity=".55"/>'
            f'<ellipse cx="{cx+ex+22*s:.0f}" cy="{cy+30*s:.0f}" rx="{18*s:.0f}" ry="{10*s:.0f}" fill="#ff9ab0" opacity=".55"/>')

def zzz(x=760, y=330):
    return (f'<text x="{x}" y="{y}" font-family="Baloo, sans-serif" font-weight="800" font-size="90" fill="#c7d2fe">Z</text>'
            f'<text x="{x+70}" y="{y-70}" font-family="Baloo, sans-serif" font-weight="800" font-size="66" fill="#c7d2fe" opacity=".8">z</text>'
            f'<text x="{x+120}" y="{y-130}" font-family="Baloo, sans-serif" font-weight="800" font-size="48" fill="#c7d2fe" opacity=".6">z</text>')

def twinkles(pts, c="#fff3c4"):
    return "".join(f'<path d="M{x} {y-30} L{x+8} {y-8} L{x+30} {y} L{x+8} {y+8} L{x} {y+30} L{x-8} {y+8} L{x-30} {y} L{x-8} {y-8}Z" fill="{c}"/>' for x, y in pts)

def scene(body, fx="", fx2=""):
    return svg(night_env() + f'<g id="animal">{body}</g><g id="fx" opacity="0">{fx}</g><g id="fx2" opacity="0">{fx2}</g>')

def critter(c, dark, ears, extra="", awake=False, belly="#fff7ef"):
    """Round sleepy critter sitting on the ground. ears: bunny|bear|cat|lamb|none|pig|cow|horse"""
    E = {"bunny": f'<ellipse cx="460" cy="380" rx="44" ry="140" fill="{c}" stroke="{dark}" stroke-width="8" transform="rotate(-12 460 380)"/><ellipse cx="460" cy="390" rx="20" ry="100" fill="#ffc6d3" transform="rotate(-12 460 390)"/>'
                  f'<ellipse cx="620" cy="380" rx="44" ry="140" fill="{c}" stroke="{dark}" stroke-width="8" transform="rotate(12 620 380)"/><ellipse cx="620" cy="390" rx="20" ry="100" fill="#ffc6d3" transform="rotate(12 620 390)"/>',
         "bear": f'<circle cx="390" cy="470" r="60" fill="{c}" stroke="{dark}" stroke-width="8"/><circle cx="690" cy="470" r="60" fill="{c}" stroke="{dark}" stroke-width="8"/><circle cx="390" cy="470" r="28" fill="{belly}"/><circle cx="690" cy="470" r="28" fill="{belly}"/>',
         "cat": f'<path d="M370 520 L390 380 L480 470Z" fill="{c}" stroke="{dark}" stroke-width="8"/><path d="M710 520 L690 380 L600 470Z" fill="{c}" stroke="{dark}" stroke-width="8"/>',
         "lamb": "".join(f'<circle cx="{540+190*math.cos(math.radians(a)):.0f}" cy="{640+170*math.sin(math.radians(a)):.0f}" r="70" fill="#fff" stroke="#d6d3e8" stroke-width="6"/>' for a in range(180, 361, 30)),
         "pig": f'<path d="M390 500 L380 410 L460 460Z" fill="{c}" stroke="{dark}" stroke-width="8"/><path d="M690 500 L700 410 L620 460Z" fill="{c}" stroke="{dark}" stroke-width="8"/>',
         "cow": f'<ellipse cx="350" cy="510" rx="70" ry="30" fill="{c}" stroke="{dark}" stroke-width="8"/><ellipse cx="730" cy="510" rx="70" ry="30" fill="{c}" stroke="{dark}" stroke-width="8"/>'
                f'<path d="M430 470 q-20 -60 10 -90 M650 470 q20 -60 -10 -90" stroke="#f5e6c8" stroke-width="22" fill="none" stroke-linecap="round"/>',
         "horse": f'<path d="M420 500 L440 400 L500 470Z" fill="{c}" stroke="{dark}" stroke-width="8"/><path d="M660 500 L640 400 L580 470Z" fill="{c}" stroke="{dark}" stroke-width="8"/><path d="M500 440 Q540 380 600 440 Q560 470 500 440Z" fill="{dark}"/>',
         "none": ""}[ears]
    return (E + f'<ellipse cx="540" cy="860" rx="250" ry="150" fill="{c}" stroke="{dark}" stroke-width="10"/><ellipse cx="540" cy="880" rx="150" ry="100" fill="{belly}"/>'
            f'<circle cx="540" cy="640" r="190" fill="{c}" stroke="{dark}" stroke-width="10"/>' + extra + sleepy_face(540, 640, 1.1, awake))

def snout(c, dark, nost=True):
    return (f'<ellipse cx="540" cy="720" rx="80" ry="55" fill="{c}" stroke="{dark}" stroke-width="6"/>' +
            (f'<ellipse cx="515" cy="720" rx="11" ry="15" fill="{dark}"/><ellipse cx="565" cy="720" rx="11" ry="15" fill="{dark}"/>' if nost else ""))

MOON_FX = '<path d="M880 180 A110 110 0 1 0 960 360 A90 90 0 1 1 880 180Z" fill="#fff3c4"/>'
BED_FX = '<path d="M120 1000 Q540 940 960 1000 L960 1060 L120 1060Z" fill="#9fa8da"/><path d="M200 960 Q540 900 880 960 L880 1000 L200 1000Z" fill="#c5cae9"/>'

# ---------- goodnight animals ----------
BUNNY = scene(critter("#f1eef9", "#b9b2d6", "bunny") + '<ellipse cx="540" cy="690" rx="16" ry="11" fill="#ff8fab"/>', zzz(), MOON_FX + twinkles([(760, 120), (650, 220)]))
BEAR = scene(critter("#a97c50", "#6d4c2f", "bear", snout("#e7c9a2", "#6d4c2f", False) + '<ellipse cx="540" cy="700" rx="26" ry="18" fill="#3e2723"/>', belly="#e7c9a2"),
             zzz(), '<g transform="translate(830 330)"><circle r="70" fill="#ffd54f"/><circle cx="-50" cy="-50" r="30" fill="#ffd54f"/><circle cx="50" cy="-50" r="30" fill="#ffd54f"/><text y="20" text-anchor="middle" font-size="60" font-family="Baloo, sans-serif" font-weight="800" fill="#8d6e63">♥</text></g>')
KITTEN = scene(critter("#ffb74d", "#c77c1e", "cat", '<path d="M540 690 l-14 -12 h28z" fill="#ff8fab"/><path d="M430 700 h-120 M430 720 h-110 M650 700 h120 M650 720 h110" stroke="#c77c1e" stroke-width="5"/>', belly="#ffe0b2")
               + '<path d="M780 900 Q900 860 880 760" stroke="#ffb74d" stroke-width="40" fill="none" stroke-linecap="round"/>',
               zzz(), '<g transform="translate(850 330)"><circle r="80" fill="#f48fb1"/><path d="M-70 -20 Q0 40 70 -20 M-60 30 Q0 -30 60 30" stroke="#ad1457" stroke-width="8" fill="none"/></g>')
DUCK = scene('<ellipse cx="540" cy="860" rx="240" ry="140" fill="#fff176" stroke="#f9a825" stroke-width="10"/><path d="M740 820 Q840 760 820 860Z" fill="#fff176" stroke="#f9a825" stroke-width="8"/>'
             '<circle cx="540" cy="620" r="170" fill="#fff176" stroke="#f9a825" stroke-width="10"/><path d="M530 470 q10 -50 40 -30" stroke="#f9a825" stroke-width="10" fill="none"/>'
             '<path d="M480 690 Q540 660 600 690 Q540 740 480 690Z" fill="#ff9800" stroke="#e65100" stroke-width="6"/>' + sleepy_face(540, 610, 1.0).split('<path d="M524')[0],
             zzz(), '<ellipse cx="540" cy="1000" rx="360" ry="50" fill="#5c6bc0" opacity=".7"/>' + "".join(f'<path d="M{x} 990 q30 -20 60 0" stroke="#9fa8da" stroke-width="6" fill="none"/>' for x in (260, 420, 640, 780)))
LAMB = scene(critter("#fdfbff", "#d6d3e8", "lamb", '<ellipse cx="360" cy="600" rx="50" ry="26" fill="#5d5470" transform="rotate(-25 360 600)"/><ellipse cx="720" cy="600" rx="50" ry="26" fill="#5d5470" transform="rotate(25 720 600)"/>'),
             zzz(), "".join(f'<g transform="translate({x} {y}) scale(.3)"><ellipse cx="0" cy="0" rx="150" ry="100" fill="#fff"/><circle cx="-110" cy="-30" r="60" fill="#5d5470"/><rect x="-90" y="70" width="20" height="70" fill="#5d5470"/><rect x="60" y="70" width="20" height="70" fill="#5d5470"/></g>'
                                     + f'<text x="{x}" y="{y-60}" text-anchor="middle" font-family="Baloo, sans-serif" font-weight="800" font-size="56" fill="#fff3c4">{i+1}</text>' for i, (x, y) in enumerate(((160, 380), (330, 300), (750, 300), (920, 380)))))

# ---------- night sky ----------
MOON = scene('<circle cx="540" cy="620" r="300" fill="#fff3c4" opacity=".25"/><circle cx="540" cy="620" r="250" fill="#fff3c4" stroke="#f0d98a" stroke-width="10"/>'
             '<circle cx="420" cy="500" r="40" fill="#f0d98a" opacity=".6"/><circle cx="680" cy="760" r="30" fill="#f0d98a" opacity=".6"/><circle cx="650" cy="480" r="22" fill="#f0d98a" opacity=".6"/>' + sleepy_face(540, 620, 1.2),
             twinkles([(160, 200), (920, 220), (200, 880), (880, 860)]), '<path d="M120 400 A70 70 0 1 0 170 520 A55 55 0 1 1 120 400Z" fill="#fff3c4"/><path d="M960 420 A70 70 0 1 1 910 540 A55 55 0 1 0 960 420Z" fill="#fff3c4"/>')
STARS = scene('<path d="M540 330 L620 540 L840 550 L670 690 L730 900 L540 780 L350 900 L410 690 L240 550 L460 540Z" fill="#ffe082" stroke="#f9a825" stroke-width="12" stroke-linejoin="round"/>' + sleepy_face(540, 640, .95, awake=True),
              twinkles([(150, 250), (930, 260), (180, 760), (900, 760), (300, 160), (780, 160)]),
              '<path d="M150 250 L300 160 L540 120 L780 160 L930 260" stroke="#fff3c4" stroke-width="4" stroke-dasharray="10 10" fill="none"/>')
CLOUD = scene('<path d="M260 820 Q200 700 320 660 Q330 520 480 540 Q560 420 690 520 Q840 500 840 650 Q940 700 880 820Z" fill="#e8eaf6" stroke="#b0b6dd" stroke-width="10"/>' + sleepy_face(560, 690, 1.0),
              '<path d="M300 900 q20 40 0 70 M460 900 q20 40 0 70 M640 900 q20 40 0 70 M800 900 q20 40 0 70" stroke="#90caf9" stroke-width="10" fill="none" stroke-linecap="round"/>',
              MOON_FX)
FIREFLY = scene('<ellipse cx="540" cy="700" rx="130" ry="160" fill="#7e57c2" stroke="#4527a0" stroke-width="10"/><circle cx="540" cy="900" r="110" fill="#fff59d" opacity=".5"/><ellipse cx="540" cy="880" rx="100" ry="80" fill="#fff59d"/>'
                '<ellipse cx="400" cy="600" rx="120" ry="60" fill="#d1c4e9" opacity=".7" transform="rotate(-30 400 600)"/><ellipse cx="680" cy="600" rx="120" ry="60" fill="#d1c4e9" opacity=".7" transform="rotate(30 680 600)"/>'
                '<path d="M510 560 q-30 -80 -70 -90 M570 560 q30 -80 70 -90" stroke="#4527a0" stroke-width="8" fill="none"/>' + sleepy_face(540, 660, .85, awake=True),
                "".join(f'<circle cx="{x}" cy="{y}" r="14" fill="#fff59d"/><circle cx="{x}" cy="{y}" r="34" fill="#fff59d" opacity=".3"/>' for x, y in ((180, 300), (300, 460), (860, 340), (940, 560), (220, 700), (820, 760))))
SUNSET = svg('<rect x="-500" y="0" width="2200" height="1100" fill="#ffb199" opacity=".55"/>' + night_env() + '<g id="animal"><circle cx="540" cy="860" r="260" fill="#ffb74d" stroke="#f57c00" stroke-width="10"/>'
             '<path d="M-500 900 Q-200 820 100 880 T700 870 T1600 860 L1600 1110 L-500 1110Z" fill="#2c3570"/>' + sleepy_face(540, 770, 1.1) + '</g>'
             '<g id="fx" opacity="0">' + "".join(f'<path d="M{540+300*math.cos(math.radians(a)):.0f} {860+300*math.sin(math.radians(a)):.0f} L{540+380*math.cos(math.radians(a)):.0f} {860+380*math.sin(math.radians(a)):.0f}" stroke="#ffcc80" stroke-width="14" stroke-linecap="round"/>' for a in range(200, 341, 28)) + '</g><g id="fx2" opacity="0">' + twinkles([(200, 200), (880, 180)]) + '</g>')

# ---------- bedtime routine ----------
BATH = scene('<path d="M200 760 L880 760 L840 960 Q830 990 800 990 L280 990 Q250 990 240 960Z" fill="#e1f5fe" stroke="#81d4fa" stroke-width="10"/><rect x="180" y="730" width="720" height="40" rx="20" fill="#b3e5fc"/>'
             '<circle cx="540" cy="640" r="130" fill="#ffd6a5"/><path d="M420 600 Q440 500 540 510 Q650 500 660 600 Q600 550 420 600Z" fill="#5d4037"/>' + sleepy_face(540, 650, .75, awake=True)
             + "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff" stroke="#b3e5fc" stroke-width="4"/>' for x, y, r in ((300, 720, 50), (380, 700, 40), (700, 715, 55), (780, 700, 38), (240, 700, 30))),
             "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#e3f2fd" stroke="#90caf9" stroke-width="5" opacity=".9"/>' for x, y, r in ((300, 420, 40), (420, 340, 30), (700, 360, 46), (820, 450, 26))),
             '<g transform="translate(860 640)"><ellipse rx="60" ry="44" fill="#ffeb3b"/><circle cx="-40" cy="-40" r="30" fill="#ffeb3b"/><path d="M-70 -40 l-24 8 24 8z" fill="#ff9800"/></g>')
PAJAMAS = scene('<path d="M340 520 L460 470 Q540 520 620 470 L740 520 L820 680 L740 720 L720 640 L720 960 L360 960 L360 640 L340 720 L260 680Z" fill="#9fa8da" stroke="#5c6bc0" stroke-width="10" stroke-linejoin="round"/>'
                + "".join(f'<path d="M{x} {y-18} l5 13 14 1 -11 9 4 14 -12 -8 -12 8 4 -14 -11 -9 14 -1z" fill="#fff3c4"/>' for x, y in ((430, 600), (620, 620), (520, 720), (440, 860), (640, 860), (540, 560)))
                + '<circle cx="540" cy="760" r="0"/>' + sleepy_face(540, 780, .8, awake=True),
                zzz(), MOON_FX)
STORYBOOK = scene('<path d="M540 560 Q380 500 220 540 L220 920 Q380 880 540 940 Q700 880 860 920 L860 540 Q700 500 540 560Z" fill="#fff8e1" stroke="#a1887f" stroke-width="10"/><path d="M540 560 L540 940" stroke="#a1887f" stroke-width="8"/>'
                  + "".join(f'<path d="M{x} {y} h{w}" stroke="#bcaaa4" stroke-width="10" stroke-linecap="round"/>' for x, y, w in ((270, 620, 200), (270, 670, 180), (270, 720, 210), (600, 620, 200), (600, 670, 170)))
                  + '<path d="M650 780 A50 50 0 1 0 690 860 A40 40 0 1 1 650 780Z" fill="#ffd54f"/>' + sleepy_face(380, 820, .6, awake=True),
                  twinkles([(240, 380), (540, 330), (840, 380)]), '<g transform="translate(860 300)">' + '<circle r="60" fill="#ffe082"/><rect x="-20" y="50" width="40" height="40" fill="#bdbdbd"/></g><path d="M860 360 L760 560 L960 560Z" fill="#fff59d" opacity=".35"/>')
TEDDY = scene(critter("#c58b5a", "#7b5232", "bear", snout("#f1d3b0", "#7b5232", False) + '<ellipse cx="540" cy="700" rx="24" ry="16" fill="#3e2723"/><path d="M500 800 q40 30 80 0" stroke="#e57373" stroke-width="0"/>', belly="#f1d3b0")
              + '<path d="M470 800 L540 840 L610 800 L610 860 L540 830 L470 860Z" fill="#e57373"/>',
              BED_FX, '<g transform="translate(850 330)"><text text-anchor="middle" font-size="140" fill="#f48fb1">♥</text></g><g transform="translate(220 360)"><text text-anchor="middle" font-size="110" fill="#f48fb1">♥</text></g>')
NIGHTLIGHT = scene('<rect x="470" y="880" width="140" height="100" rx="20" fill="#9fa8da"/><circle cx="540" cy="700" r="300" fill="#fff59d" opacity=".18"/><circle cx="540" cy="700" r="200" fill="#fff59d" opacity=".22"/>'
                   '<path d="M380 880 Q380 560 540 520 Q700 560 700 880Z" fill="#fff9c4" stroke="#fdd835" stroke-width="10"/>' + sleepy_face(540, 720, .9, awake=True),
                   twinkles([(200, 300), (880, 300), (160, 640), (920, 640)], "#fff59d"), MOON_FX)

# ---------- ocean dreams ----------
def ocean_scene(body, fx="", fx2=""):
    bubbles = "".join(f'<circle cx="{-400+1900*_r(i,5):.0f}" cy="{80+800*_r(i,6):.0f}" r="{6+14*_r(i,7):.0f}" fill="none" stroke="#9fd8ff" stroke-width="4" opacity=".5"/>' for i in range(30))
    return svg('<rect x="-500" y="0" width="2200" height="1100" fill="#14306b"/>' + bubbles + '<path d="M-500 960 Q0 900 540 950 T1600 940 L1600 1110 L-500 1110Z" fill="#e0c68f" opacity=".85"/>'
               + "".join(f'<path d="M{x} 960 q-30 -120 10 -200 q30 -60 0 -140" stroke="#2e7d6b" stroke-width="22" fill="none" stroke-linecap="round"/>' for x in (-300, 1300))
               + f'<g id="animal">{body}</g><g id="fx" opacity="0">{fx}</g><g id="fx2" opacity="0">{fx2}</g>')
WHALE = ocean_scene('<path d="M180 720 Q200 460 520 460 Q860 460 880 700 Q880 860 600 880 L300 880 Q180 860 180 720Z" fill="#5c8de0" stroke="#2f5fae" stroke-width="10"/>'
                    '<path d="M300 820 Q540 900 800 800 Q760 880 600 880 L300 880Z" fill="#c9dcff"/><path d="M860 640 Q980 560 1000 480 Q960 600 1020 680 Q940 680 870 700Z" fill="#5c8de0" stroke="#2f5fae" stroke-width="8"/>' + sleepy_face(420, 660, 1.0),
                    '<path d="M500 450 q-30 -80 -10 -140 M520 450 q10 -100 60 -150 M540 450 q40 -70 100 -100" stroke="#bfe3ff" stroke-width="12" fill="none" stroke-linecap="round"/>',
                    '<text x="760" y="400" font-family="Baloo, sans-serif" font-weight="800" font-size="70" fill="#bfe3ff">♪ ♫</text>')
SEAHORSE = ocean_scene('<path d="M560 420 Q700 420 680 540 Q660 620 600 640 Q700 720 640 820 Q600 900 640 960 Q560 960 560 880 Q540 800 580 740 Q480 720 480 620 Q440 600 400 610 Q380 560 470 540 Q470 440 560 420Z" fill="#f48fb1" stroke="#c2185b" stroke-width="10"/>'
                       + "".join(f'<path d="M{680+5*i} {470+60*i} l30 -10 -20 30z" fill="#c2185b"/>' for i in range(4)) + sleepy_face(560, 520, .55, awake=True),
                       '<g fill="#ff8a80">' + "".join(f'<circle cx="{x}" cy="{y}" r="16"/>' for x, y in ((240, 860), (280, 820), (310, 880), (820, 860), (850, 820))) + '</g>',
                       twinkles([(240, 300), (860, 300)], "#bfe3ff"))
FISH = ocean_scene('<path d="M260 700 Q420 470 700 600 L900 480 L880 700 L900 920 L700 800 Q420 930 260 700Z" fill="#ffb74d" stroke="#e65100" stroke-width="10"/>'
                   '<path d="M470 540 Q500 700 470 860 M590 560 Q620 700 590 840" stroke="#fff" stroke-width="30" fill="none" opacity=".85"/>' + sleepy_face(380, 680, .7),
                   "".join(f'<g transform="translate({x} {y}) scale(.3)"><path d="M260 700 Q420 470 700 600 L900 480 L880 700 L900 920 L700 800 Q420 930 260 700Z" fill="{c}"/></g>' for x, y, c in ((60, 100, "#4fc3f7"), (640, 60, "#81c784"), (700, 300, "#ba68c8"))))
SEATURTLE = ocean_scene('<ellipse cx="540" cy="700" rx="280" ry="190" fill="#81c784" stroke="#2e7d32" stroke-width="10"/>'
                        + "".join(f'<path d="M{x} {y} l50 -30 50 30 0 60 -50 30 -50 -30z" fill="#a5d6a7" stroke="#2e7d32" stroke-width="5"/>' for x, y in ((390, 620), (490, 580), (590, 620), (440, 700), (540, 680)))
                        + '<ellipse cx="320" cy="560" rx="90" ry="40" fill="#c5e1a5" transform="rotate(-30 320 560)"/><ellipse cx="760" cy="560" rx="90" ry="40" fill="#c5e1a5" transform="rotate(30 760 560)"/>'
                        '<circle cx="240" cy="720" r="100" fill="#c5e1a5" stroke="#2e7d32" stroke-width="8"/>' + sleepy_face(240, 710, .6),
                        zzz(700, 380), '<path d="M120 1000 Q540 940 960 1000" stroke="#fff" stroke-width="8" fill="none" stroke-dasharray="14 14"/>')
JELLY = ocean_scene('<path d="M330 640 Q330 400 540 400 Q750 400 750 640 Q700 610 660 650 Q610 610 540 650 Q470 610 420 650 Q380 610 330 640Z" fill="#ce93d8" stroke="#8e24aa" stroke-width="10" opacity=".95"/>'
                    + "".join(f'<path d="M{x} 650 q-30 80 0 160 q30 80 0 160" stroke="#ce93d8" stroke-width="16" fill="none" stroke-linecap="round"/>' for x in (390, 470, 540, 610, 690)) + sleepy_face(540, 540, .8),
                    '<circle cx="540" cy="540" r="260" fill="#f3e5f5" opacity=".18"/><circle cx="540" cy="540" r="330" fill="#f3e5f5" opacity=".1"/>', twinkles([(180, 240), (900, 260)], "#f3e5f5"))

# ---------- farm goodnight ----------
def farm_scene(body, fx="", fx2=""):
    return scene('<path d="M-460 1000 L-460 620 L-300 500 L-140 620 L-140 1000Z" fill="#8e3b46" opacity=".8"/><path d="M1220 1000 L1220 700 H1560 V1000Z" fill="#5d4037" opacity=".6"/>' + body, fx, fx2)
COW = farm_scene(critter("#fafafa", "#9e9e9e", "cow", '<ellipse cx="430" cy="560" rx="60" ry="45" fill="#424242"/><ellipse cx="680" cy="620" rx="40" ry="55" fill="#424242"/>' + snout("#f8bbd0", "#c2185b")), zzz(), MOON_FX)
PIG = farm_scene(critter("#f8bbd0", "#d17a99", "pig", snout("#f48fb1", "#ad1457"), belly="#fce4ec"), zzz(),
                 '<ellipse cx="540" cy="1010" rx="380" ry="50" fill="#6d4c41" opacity=".7"/>')
HORSE = farm_scene(critter("#bc8f6f", "#6d4c41", "horse", '<path d="M540 450 Q600 520 560 620 Q620 560 640 470Z" fill="#4e342e"/>' + snout("#e0cbb8", "#6d4c41"), belly="#e0cbb8"),
                   zzz(), '<g fill="#ffe082">' + "".join(f'<rect x="{x}" y="930" width="120" height="70" rx="10"/>' for x in (120, 840)) + '</g>')
HEN = farm_scene('<ellipse cx="540" cy="800" rx="230" ry="190" fill="#fff" stroke="#bdbdbd" stroke-width="10"/><path d="M740 720 Q860 640 820 820Z" fill="#fff" stroke="#bdbdbd" stroke-width="8"/>'
                 '<circle cx="480" cy="600" r="140" fill="#fff" stroke="#bdbdbd" stroke-width="10"/><path d="M430 470 q20 -50 40 0 q20 -50 40 0 q20 -50 40 0" fill="#e53935"/>'
                 '<path d="M380 620 L320 640 L380 660Z" fill="#ffb300"/><path d="M380 670 q-10 30 10 50 q20 -20 0 -50" fill="#e53935"/>' + sleepy_face(490, 590, .7),
                 zzz(), '<path d="M300 1000 Q540 920 780 1000Z" fill="#ffe082"/>' + "".join(f'<ellipse cx="{x}" cy="975" rx="30" ry="38" fill="#fff8e1" stroke="#d7ccc8" stroke-width="4"/>' for x in (460, 540, 620)))
PUPPY = farm_scene(critter("#d7a86e", "#8d6239", "none", '<ellipse cx="370" cy="620" rx="60" ry="120" fill="#8d6239" transform="rotate(15 370 620)"/><ellipse cx="710" cy="620" rx="60" ry="120" fill="#8d6239" transform="rotate(-15 710 620)"/>'
                   + '<ellipse cx="540" cy="700" rx="26" ry="18" fill="#3e2723"/>', belly="#f3dcb8"),
                   zzz(), '<g transform="translate(860 920)"><path d="M-120 0 Q-120 -80 0 -80 Q120 -80 120 0Z" fill="#c62828"/><text y="-20" text-anchor="middle" font-family="Baloo, sans-serif" font-weight="800" font-size="40" fill="#fff">ZZZ</text></g>')

MOON_TITLE = svg(night_env() + """
  <g transform="translate(-130 -40)">
    <rect x="190" y="230" width="700" height="150" rx="44" fill="#3949ab" stroke="#1a237e" stroke-width="10"/>
    <text x="540" y="333" text-anchor="middle" font-family="Baloo, sans-serif" font-weight="800" font-size="70" fill="#fff3c4">MOONBEAM BEDTIME</text>
    <path d="M500 520 A170 170 0 1 0 620 800 A140 140 0 1 1 500 520Z" fill="#fff3c4"/>
  </g>""" + twinkles([(820, 500), (900, 700), (720, 820)]))

SCENES9 = {"mb_bunny": BUNNY, "mb_bear": BEAR, "mb_kitten": KITTEN, "mb_duck": DUCK, "mb_lamb": LAMB,
           "mb_moon": MOON, "mb_stars": STARS, "mb_cloud": CLOUD, "mb_firefly": FIREFLY, "mb_sunset": SUNSET,
           "mb_bath": BATH, "mb_pajamas": PAJAMAS, "mb_book": STORYBOOK, "mb_teddy": TEDDY, "mb_nightlight": NIGHTLIGHT,
           "mb_whale": WHALE, "mb_seahorse": SEAHORSE, "mb_fish": FISH, "mb_turtle": SEATURTLE, "mb_jelly": JELLY,
           "mb_cow": COW, "mb_pig": PIG, "mb_horse": HORSE, "mb_hen": HEN, "mb_puppy": PUPPY}
NAMES9 = {k: v for k, v in {"mb_bunny": "BUNNY", "mb_bear": "BEAR", "mb_kitten": "KITTEN", "mb_duck": "DUCKLING", "mb_lamb": "LAMB", "mb_moon": "MOON", "mb_stars": "STAR",
          "mb_cloud": "CLOUD", "mb_firefly": "FIREFLY", "mb_sunset": "SUNSET", "mb_bath": "BATH TIME", "mb_pajamas": "PAJAMAS", "mb_book": "STORY TIME", "mb_teddy": "TEDDY",
          "mb_nightlight": "NIGHT LIGHT", "mb_whale": "WHALE", "mb_seahorse": "SEAHORSE", "mb_fish": "FISH", "mb_turtle": "SEA TURTLE", "mb_jelly": "JELLYFISH",
          "mb_cow": "COW", "mb_pig": "PIG", "mb_horse": "HORSE", "mb_hen": "HEN", "mb_puppy": "PUPPY"}.items()}

LUNA = """<svg id="milo" viewBox="0 0 220 200" width="260" height="236">
  <g id="wing"><path d="M40 100 Q10 140 40 175 Q60 150 62 115Z" fill="#7e6bb8" stroke="#4a3d82" stroke-width="4"/></g>
  <path d="M180 100 Q210 140 180 175 Q160 150 158 115Z" fill="#7e6bb8" stroke="#4a3d82" stroke-width="4"/>
  <ellipse cx="110" cy="122" rx="66" ry="72" fill="#9b8bd6" stroke="#4a3d82" stroke-width="5"/>
  <ellipse cx="110" cy="148" rx="40" ry="38" fill="#e8e1ff"/>
  <path d="M90 140 q6 6 12 0 M110 152 q6 6 12 0 M95 164 q6 6 12 0" stroke="#b9acec" stroke-width="3" fill="none"/>
  <path d="M58 62 L66 30 L84 56Z M162 62 L154 30 L136 56Z" fill="#7e6bb8" stroke="#4a3d82" stroke-width="4"/>
  <circle cx="86" cy="92" r="22" fill="#fff8e1" stroke="#4a3d82" stroke-width="3"/><circle cx="134" cy="92" r="22" fill="#fff8e1" stroke="#4a3d82" stroke-width="3"/>
  <ellipse class="mpupil" cx="88" cy="95" rx="8" ry="9" fill="#1a1a2e"/><ellipse class="mpupil" cx="136" cy="95" rx="8" ry="9" fill="#1a1a2e"/>
  <circle class="glint" cx="91" cy="90" r="3.5" fill="#fff"/><circle class="glint" cx="139" cy="90" r="3.5" fill="#fff"/>
  <path d="M66 80 Q86 70 106 82 L106 76 Q86 62 66 74Z" fill="#7e6bb8"/><path d="M154 80 Q134 70 114 82 L114 76 Q134 62 154 74Z" fill="#7e6bb8"/>
  <path d="M102 108 L110 122 L118 108Z" fill="#ffb74d" stroke="#e08a1e" stroke-width="2"/>
  <ellipse id="beaklow" cx="110" cy="124" rx="6" ry="2" fill="#e08a1e"/>
  <path d="M60 40 Q110 -6 160 40 Q110 30 60 40Z" fill="#5c6bc0"/><circle cx="162" cy="34" r="9" fill="#fff3c4"/>
  <circle cx="70" cy="112" r="7" fill="#ff9ab0" opacity=".7"/><circle cx="150" cy="112" r="7" fill="#ff9ab0" opacity=".7"/>
</svg>"""
