"""Fruity Friends, week 2: 25 NEW fruit, veggie and healthy-habit scenes.
Same 1080x1100 kitchen frame as art_fruity.py (counter/floor at ~y1000). Every key starts with "fr2_"."""
import math
from art_fruity import svg, kitchen_env, face, scene, sparkles, bubbles, leaf, kid


def stem(x, y, h=90, c="#795548", w=20):
    return f'<rect x="{x - w // 2}" y="{y - h}" width="{w}" height="{h}" rx="8" fill="{c}"/>'


def shine(x, y, rx=46, ry=24, rot=-35):
    return f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="#fff" opacity=".4" transform="rotate({rot} {x} {y})"/>'


def heart(x, y, s=1.0, c="#fb7185"):
    return (f'<path d="M{x} {y + 40 * s:.0f} C{x - 70 * s:.0f} {y:.0f} {x - 40 * s:.0f} {y - 50 * s:.0f} {x} {y - 20 * s:.0f} '
            f'C{x + 40 * s:.0f} {y - 50 * s:.0f} {x + 70 * s:.0f} {y:.0f} {x} {y + 40 * s:.0f}Z" fill="{c}"/>')


def drops(pts, c="#38bdf8"):
    return "".join(f'<path d="M{x} {y} q18 40 0 70 q-18 -30 0 -70z" fill="{c}"/>' for x, y in pts)


def sun(x, y, r=80):
    rays = "".join(f'<path d="M{x + (r + 20) * math.cos(math.radians(a)):.0f} {y + (r + 20) * math.sin(math.radians(a)):.0f} '
                   f'L{x + (r + 60) * math.cos(math.radians(a)):.0f} {y + (r + 60) * math.sin(math.radians(a)):.0f}" stroke="#fbbf24" stroke-width="16" stroke-linecap="round"/>'
                   for a in range(0, 360, 45))
    return f'{rays}<circle cx="{x}" cy="{y}" r="{r}" fill="#fde047" stroke="#f59e0b" stroke-width="8"/>'


def closed_face(cx, cy, s=1.0, mouth="#7a2b2b"):
    ex = int(46 * s)
    return (f'<path d="M{cx - ex - 22 * s:.0f} {cy} q{22 * s:.0f} {16 * s:.0f} {44 * s:.0f} 0 M{cx + ex - 22 * s:.0f} {cy} q{22 * s:.0f} {16 * s:.0f} {44 * s:.0f} 0" '
            f'stroke="#1a1a2e" stroke-width="{max(5, int(8 * s))}" fill="none" stroke-linecap="round"/>'
            f'<path d="M{cx - 30 * s:.0f} {cy + 46 * s:.0f} q{30 * s:.0f} {26 * s:.0f} {60 * s:.0f} 0" stroke="{mouth}" stroke-width="{max(5, int(8 * s))}" fill="none" stroke-linecap="round"/>'
            f'<ellipse cx="{cx - ex - 24 * s:.0f}" cy="{cy + 40 * s:.0f}" rx="{20 * s:.0f}" ry="{11 * s:.0f}" fill="#ff8fab" opacity=".6"/>'
            f'<ellipse cx="{cx + ex + 24 * s:.0f}" cy="{cy + 40 * s:.0f}" rx="{20 * s:.0f}" ry="{11 * s:.0f}" fill="#ff8fab" opacity=".6"/>')


def mini_tree(x, y, fruit, s=1.0):
    """Little tree with fruit dots, trunk base at (x, y)."""
    f = "".join(f'<circle cx="{x + dx * s:.0f}" cy="{y - 230 * s + dy * s:.0f}" r="{16 * s:.0f}" fill="{fruit}"/>' for dx, dy in ((-60, -10), (-10, -50), (50, -20), (20, 30), (-40, 40), (70, 30)))
    return (f'<rect x="{x - 18 * s:.0f}" y="{y - 140 * s:.0f}" width="{36 * s:.0f}" height="{140 * s:.0f}" rx="10" fill="#8d6e63"/>'
            f'<circle cx="{x}" cy="{y - 230 * s:.0f}" r="{120 * s:.0f}" fill="#4ade80" stroke="#15803d" stroke-width="8"/>' + f)


# ================= FRUITS =================
_grapes = [(400, 520), (540, 520), (680, 520), (330, 630), (470, 630), (610, 630), (750, 630), (400, 740), (540, 740), (680, 740), (470, 850), (610, 850), (540, 950)]
GRAPES = scene(stem(540, 470, 80) + leaf(620, 430, -20, s=1.3) + leaf(460, 440, 200, c="#4ade80")
               + "".join(f'<circle cx="{x}" cy="{y}" r="78" fill="#8b5cf6" stroke="#5b21b6" stroke-width="8"/><circle cx="{x - 24}" cy="{y - 26}" r="14" fill="#fff" opacity=".45"/>' for x, y in _grapes)
               + face(540, 650, 1.1, "#fff"),
               '<g transform="translate(880 320)">' + "".join(f'<circle cx="{dx}" cy="{dy}" r="30" fill="#a3e635" stroke="#4d7c0f" stroke-width="5"/>' for dx, dy in ((-40, -40), (0, -40), (40, -40), (-20, 0), (20, 0), (0, 40))) + '<rect x="-6" y="-100" width="12" height="44" fill="#795548"/></g>',
               sparkles([(200, 330), (880, 520), (260, 520)]))

PEAR = scene('<path d="M540 420 C470 420 450 520 440 600 C300 680 290 965 540 972 C790 965 780 680 640 600 C630 520 610 420 540 420Z" fill="#a3d65c" stroke="#65a30d" stroke-width="10"/>'
             + stem(545, 430, 80) + leaf(620, 380, -25) + shine(430, 700, 40, 70, 20) + face(540, 760, 1.15),
             mini_tree(880, 480, "#a3d65c", 1.0),
             '<g transform="translate(180 360)"><path d="M0 -110 C-40 -110 -50 -50 -55 -10 C-130 30 -130 140 0 140 C130 140 130 30 55 -10 C50 -50 40 -110 0 -110Z" fill="#fefce8" stroke="#a3d65c" stroke-width="12"/>'
             '<ellipse cx="-14" cy="60" rx="9" ry="16" fill="#5d4037"/><ellipse cx="14" cy="60" rx="9" ry="16" fill="#5d4037"/></g>')

_hatch = "".join(f'<path d="M{x} 470 L{x + 520} 990" stroke="#d97706" stroke-width="7"/><path d="M{x + 520} 470 L{x} 990" stroke="#d97706" stroke-width="7"/>' for x in range(-80, 760, 80))
PINEAPPLE = scene('<defs><clipPath id="fr2-pine-clip"><ellipse cx="540" cy="735" rx="210" ry="245"/></clipPath></defs>'
                  + "".join(f'<path d="M540 520 Q{540 + dx * .5:.0f} {430 + abs(dx) * .3:.0f} {540 + dx} {300 + abs(dx) * .9:.0f} Q{540 + dx * .2:.0f} 470 540 520Z" fill="{c}" stroke="#15803d" stroke-width="6"/>'
                            for dx, c in ((-170, "#22c55e"), (170, "#22c55e"), (-100, "#4ade80"), (100, "#4ade80"), (-40, "#22c55e"), (40, "#22c55e"), (0, "#4ade80")))
                  + '<ellipse cx="540" cy="735" rx="210" ry="245" fill="#fbbf24" stroke="#b45309" stroke-width="10"/>'
                  + f'<g clip-path="url(#fr2-pine-clip)" opacity=".7">{_hatch}</g>'
                  + '<ellipse cx="540" cy="735" rx="140" ry="120" fill="#fbbf24" opacity=".85"/>' + face(540, 720, 1.05),
                  ('<g transform="translate(880 480)">' + "".join(f'<path d="M0 0 L{120*math.cos(math.radians(a))-14:.0f} {120*math.sin(math.radians(a)):.0f} L{120*math.cos(math.radians(a))+14:.0f} {120*math.sin(math.radians(a)):.0f}Z" fill="{c}"/>' for a, c in ((-170, "#22c55e"), (-145, "#4ade80"), (-120, "#22c55e"), (-60, "#22c55e"), (-35, "#4ade80"), (-10, "#22c55e")))
                  + '<rect x="-6" y="-80" width="12" height="80" fill="#15803d"/><ellipse cx="0" cy="-125" rx="44" ry="58" fill="#fbbf24" stroke="#b45309" stroke-width="6"/><path d="M-22 -180 L0 -230 L22 -180Z" fill="#22c55e"/></g>'),
                  "".join(f'<g transform="translate({x} {y})"><circle r="70" fill="#fde68a" stroke="#f59e0b" stroke-width="10"/><circle r="24" fill="#fef9c3" stroke="#f59e0b" stroke-width="6"/></g>' for x, y in ((150, 330), (230, 470))))

KIWI = scene('<ellipse cx="540" cy="730" rx="290" ry="240" fill="#a16207" stroke="#713f12" stroke-width="10"/>'
             + "".join(f'<path d="M{540 + 240 * math.cos(a):.0f} {730 + 200 * math.sin(a):.0f} l{6 * math.cos(a):.0f} {6 * math.sin(a):.0f}" stroke="#d6a35c" stroke-width="5" stroke-linecap="round"/>' for a in [i * .3 for i in range(21)])
             + "".join(f'<circle cx="{x}" cy="{y}" r="3" fill="#d6a35c"/>' for x, y in ((380, 620), (700, 600), (360, 820), (720, 840), (460, 900), (620, 910), (440, 560), (650, 540)))
             + '<path d="M810 700 l30 -10 -4 30z" fill="#713f12"/>' + face(540, 720, 1.15, "#fff"),
             '<g transform="translate(870 320)"><circle r="120" fill="#a16207"/><circle r="108" fill="#84cc16"/><ellipse rx="40" ry="34" fill="#f7fee7"/>'
             + "".join(f'<ellipse cx="{62 * math.cos(math.radians(a)):.0f}" cy="{62 * math.sin(math.radians(a)):.0f}" rx="5" ry="10" fill="#1a1a2e" transform="rotate({a + 90} {62 * math.cos(math.radians(a)):.0f} {62 * math.sin(math.radians(a)):.0f})"/>' for a in range(0, 360, 24))
             + '</g>',
             sparkles([(190, 340), (250, 520)]))

MANGO = scene('<defs><linearGradient id="fr2-mango-g" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="#ef4444"/><stop offset=".45" stop-color="#fb923c"/><stop offset=".8" stop-color="#facc15"/><stop offset="1" stop-color="#84cc16"/></linearGradient></defs>'
              '<path d="M300 770 C280 570 440 440 620 465 C800 495 845 690 765 840 C690 975 425 985 345 905 C312 868 302 820 300 770Z" fill="url(#fr2-mango-g)" stroke="#c2410c" stroke-width="10"/>'
              + stem(640, 470, 50) + leaf(720, 430, -15, s=1.2) + shine(420, 640, 40, 26, -45) + face(555, 720, 1.1),
              '<g transform="translate(880 330)"><ellipse rx="70" ry="120" fill="#fef3c7" stroke="#d97706" stroke-width="10" transform="rotate(20)"/>'
              '<path d="M-30 -80 q20 80 0 160 M10 -90 q20 90 0 180" stroke="#f59e0b" stroke-width="5" fill="none" transform="rotate(20)"/></g>',
              "".join(f'<rect x="{x}" y="{y}" width="64" height="64" rx="12" fill="#fb923c" stroke="#ea580c" stroke-width="5"/>' for x, y in ((120, 300), (200, 300), (160, 380), (240, 380), (120, 460))))

CHERRIES = scene('<path d="M380 640 Q420 460 560 400" stroke="#4d7c0f" stroke-width="18" fill="none" stroke-linecap="round"/><path d="M700 640 Q660 470 560 400" stroke="#4d7c0f" stroke-width="18" fill="none" stroke-linecap="round"/>'
                 + leaf(640, 380, -20, s=1.3)
                 + "".join(f'<circle cx="{x}" cy="800" r="175" fill="#dc2626" stroke="#991b1b" stroke-width="10"/>' + shine(x - 80, 720, 40, 22) for x in (365, 715))
                 + face(365, 790, .75) + face(715, 790, .75),
                 '<g transform="translate(880 320)"><circle r="110" fill="#dc2626" stroke="#991b1b" stroke-width="10"/><circle r="84" fill="#fca5a5"/><ellipse rx="36" ry="46" fill="#fef3c7" stroke="#d6a35c" stroke-width="6"/></g>',
                 '<g>' + "".join(f'<g transform="translate({x} {y})">' + "".join(f'<ellipse cx="{18 * math.cos(math.radians(a)):.0f}" cy="{18 * math.sin(math.radians(a)):.0f}" rx="16" ry="11" fill="#fbcfe8" transform="rotate({a} {18 * math.cos(math.radians(a)):.0f} {18 * math.sin(math.radians(a)):.0f})"/>' for a in range(0, 360, 72)) + '<circle r="8" fill="#fde047"/></g>' for x, y in ((160, 330), (240, 420), (130, 480))) + '</g>')

LEMON = scene('<path d="M230 720 Q240 690 270 680 C300 520 440 470 540 470 C640 470 780 520 810 680 Q840 690 850 720 Q840 750 810 760 C780 920 640 970 540 970 C440 970 300 920 270 760 Q240 750 230 720Z" fill="#fde047" stroke="#ca8a04" stroke-width="10"/>'
              + leaf(600, 470, -20) + shine(390, 600, 50, 24, -30)
              + "".join(f'<circle cx="{540 + 220 * math.cos(a):.0f}" cy="{720 + 190 * math.sin(a):.0f}" r="5" fill="#eab308" opacity=".6"/>' for a in [i * .5 for i in range(13)])
              + face(540, 700, 1.15),
              '<g transform="translate(880 320)"><circle r="110" fill="#fef9c3" stroke="#facc15" stroke-width="16"/>' + "".join(f'<path d="M0 0 L{92 * math.cos(math.radians(a)):.0f} {92 * math.sin(math.radians(a)):.0f}" stroke="#fde047" stroke-width="9"/>' for a in range(0, 360, 45)) + '<circle r="14" fill="#fef9c3"/></g>',
              '<g transform="translate(170 400)"><path d="M-80 -110 L80 -110 L60 140 L-60 140Z" fill="#e0f2fe" stroke="#7dd3fc" stroke-width="10"/><path d="M-74 -40 L74 -40 L60 134 L-60 134Z" fill="#bae6fd"/>'
              '<circle cx="50" cy="-110" r="46" fill="#fef9c3" stroke="#facc15" stroke-width="10"/></g>')

PEACH = scene('<defs><radialGradient id="fr2-peach-g" cx=".35" cy=".35" r=".8"><stop offset="0" stop-color="#fed7aa"/><stop offset=".55" stop-color="#fdba74"/><stop offset="1" stop-color="#fb7185"/></radialGradient></defs>'
              '<path d="M540 470 C360 420 240 560 260 740 C280 920 420 985 540 960 C660 985 800 920 820 740 C840 560 720 420 540 470Z" fill="url(#fr2-peach-g)" stroke="#f97316" stroke-width="10"/>'
              '<path d="M540 480 Q500 700 540 950" stroke="#f97316" stroke-width="7" fill="none" opacity=".5"/>'
              + stem(545, 480, 50) + leaf(620, 440, -25, s=1.2) + face(560, 720, 1.15),
              '<g transform="translate(880 320)"><circle r="115" fill="#fdba74" stroke="#f97316" stroke-width="10"/><circle r="90" fill="#fde68a"/><ellipse rx="40" ry="52" fill="#b45309" stroke="#7c2d12" stroke-width="6"/>'
              '<path d="M-14 -36 q10 36 0 72 M10 -34 q10 34 0 68" stroke="#7c2d12" stroke-width="4" fill="none"/></g>',
              sparkles([(180, 330), (250, 470), (150, 560)], "#fff"))

# ================= VEGGIES =================
TOMATO = scene('<ellipse cx="540" cy="720" rx="290" ry="250" fill="#ef4444" stroke="#b91c1c" stroke-width="10"/>'
               '<path d="M540 480 L500 430 L520 490 L440 470 L500 510 L430 540 L520 530 L540 590 L560 530 L650 540 L580 510 L640 470 L560 490 L580 430Z" fill="#22c55e" stroke="#15803d" stroke-width="6" stroke-linejoin="round"/>'
               + stem(540, 480, 50, "#15803d", 16) + shine(380, 620, 50, 26) + face(540, 740, 1.2),
               '<g><rect x="870" y="160" width="14" height="420" rx="6" fill="#a16207"/><path d="M877 560 Q820 470 880 400 Q940 330 870 250" stroke="#15803d" stroke-width="12" fill="none"/>'
               + leaf(830, 440, 30, s=.8) + leaf(930, 330, -30, s=.8)
               + '<circle cx="820" cy="490" r="38" fill="#ef4444"/><circle cx="935" cy="390" r="34" fill="#22c55e"/><circle cx="845" cy="290" r="32" fill="#fb923c"/></g>',
               '<g transform="translate(180 360)"><circle r="100" fill="#ef4444" stroke="#b91c1c" stroke-width="8"/><circle r="82" fill="#fca5a5"/>'
               + "".join(f'<ellipse cx="{48 * math.cos(math.radians(a)):.0f}" cy="{48 * math.sin(math.radians(a)):.0f}" rx="20" ry="28" fill="#ef4444" transform="rotate({a} {48 * math.cos(math.radians(a)):.0f} {48 * math.sin(math.radians(a)):.0f})"/>' for a in range(0, 360, 90))
               + '<circle r="18" fill="#fecaca"/></g>')

CUCUMBER = scene('<rect x="410" y="380" width="260" height="600" rx="130" fill="#16a34a" stroke="#14532d" stroke-width="10"/>'
                 + "".join(f'<path d="M{x} 430 Q{x + 6} 680 {x} 930" stroke="#4ade80" stroke-width="12" fill="none" opacity=".6"/>' for x in (470, 540, 610))
                 + "".join(f'<circle cx="{x}" cy="{y}" r="7" fill="#bbf7d0"/>' for x, y in ((450, 500), (630, 520), (440, 820), (640, 800), (500, 900), (590, 910), (460, 660), (625, 680)))
                 + '<rect x="525" y="350" width="30" height="40" rx="8" fill="#4d7c0f"/>' + face(540, 620, 1.0, "#fff"),
                 "".join(f'<g transform="translate({x} {y})"><circle r="62" fill="#bbf7d0" stroke="#16a34a" stroke-width="10"/>' + "".join(f'<ellipse cx="{24 * math.cos(math.radians(a)):.0f}" cy="{24 * math.sin(math.radians(a)):.0f}" rx="5" ry="9" fill="#ecfccb" stroke="#86efac" stroke-width="2"/>' for a in range(0, 360, 60)) + '</g>' for x, y in ((830, 300), (950, 360), (870, 440))),
                 '<path d="M80 600 Q140 480 100 400 Q60 320 160 260" stroke="#15803d" stroke-width="10" fill="none"/>' + leaf(150, 470, 30, s=.9) + leaf(80, 330, -20, s=.8)
                 + '<g transform="translate(170 260)">' + "".join(f'<ellipse cx="{18 * math.cos(math.radians(a)):.0f}" cy="{18 * math.sin(math.radians(a)):.0f}" rx="18" ry="12" fill="#fde047" transform="rotate({a} {18 * math.cos(math.radians(a)):.0f} {18 * math.sin(math.radians(a)):.0f})"/>' for a in range(0, 360, 72)) + '<circle r="9" fill="#f59e0b"/></g>')

POTATO = scene('<path d="M290 700 C270 560 400 480 540 500 C700 470 830 560 815 720 C840 860 720 965 560 955 C400 975 260 880 290 700Z" fill="#d6a35c" stroke="#92400e" stroke-width="10"/>'
               + "".join(f'<ellipse cx="{x}" cy="{y}" rx="12" ry="7" fill="#a16207" opacity=".7"/>' for x, y in ((360, 620), (740, 640), (340, 820), (760, 840), (470, 910), (640, 920), (690, 540)))
               + shine(400, 580, 40, 20) + face(545, 720, 1.15),
               '<g transform="translate(880 330)"><rect x="-150" y="0" width="300" height="160" rx="20" fill="#8d6e63"/>'
               '<path d="M0 0 V-60 M0 -40 Q-60 -90 -90 -60 M0 -50 Q60 -110 90 -70" stroke="#15803d" stroke-width="10" fill="none"/>' + leaf(-80, -80, 20, s=.6) + leaf(80, -90, -20, s=.6) + leaf(0, -100, -90, s=.6)
               + '<path d="M0 0 Q-40 50 -70 90 M0 0 Q30 60 70 100" stroke="#d6a35c" stroke-width="5" fill="none"/>'
               + "".join(f'<ellipse cx="{x}" cy="{y}" rx="30" ry="22" fill="#d6a35c" stroke="#92400e" stroke-width="4"/>' for x, y in ((-80, 100), (75, 110), (0, 60))) + '</g>',
               '<g transform="translate(170 420)"><path d="M-110 0 Q-110 110 0 110 Q110 110 110 0Z" fill="#60a5fa" stroke="#1d4ed8" stroke-width="8"/>'
               '<path d="M-90 0 Q-60 -60 0 -50 Q60 -70 90 0Z" fill="#fef3c7"/>'
               '<path d="M-40 -90 q-20 -30 0 -60 M0 -100 q-20 -30 0 -60 M40 -90 q-20 -30 0 -60" stroke="#cbd5e1" stroke-width="8" fill="none" stroke-linecap="round"/></g>')

_lettuce_leaves = [(540, 520, 240, 150, "#86efac"), (360, 690, 170, 200, "#4ade80"), (720, 690, 170, 200, "#4ade80"), (540, 830, 260, 150, "#22c55e"), (420, 850, 150, 120, "#4ade80"), (660, 850, 150, 120, "#4ade80")]
LETTUCE = scene("".join(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{c}" stroke="#15803d" stroke-width="8"/>' for x, y, rx, ry, c in _lettuce_leaves)
                + '<ellipse cx="540" cy="690" rx="220" ry="200" fill="#bbf7d0" stroke="#15803d" stroke-width="8"/>'
                + '<path d="M540 520 V880 M540 650 L430 560 M540 650 L650 560 M540 780 L410 700 M540 780 L670 700" stroke="#86efac" stroke-width="10" fill="none" stroke-linecap="round" opacity=".9"/>'
                + face(540, 700, 1.05),
                '<g transform="translate(880 350)"><path d="M-140 -10 Q-140 120 0 120 Q140 120 140 -10Z" fill="#fde68a" stroke="#d97706" stroke-width="8"/>'
                '<ellipse cx="-60" cy="-20" rx="60" ry="34" fill="#4ade80"/><ellipse cx="40" cy="-30" rx="60" ry="34" fill="#86efac"/><circle cx="-10" cy="-30" r="22" fill="#ef4444"/><circle cx="80" cy="-10" r="18" fill="#ef4444"/>'
                '<rect x="-110" y="-30" width="60" height="16" rx="8" fill="#fb923c" transform="rotate(-20 -80 -22)"/></g>',
                drops([(170, 300), (240, 420), (130, 480), (210, 560)], "#7dd3fc"))

BELLPEPPER = scene('<path d="M540 480 C620 440 760 470 790 600 C820 760 780 930 680 955 C620 970 590 940 540 950 C490 940 460 970 400 955 C300 930 260 760 290 600 C320 470 460 440 540 480Z" fill="#ef4444" stroke="#991b1b" stroke-width="10"/>'
                   '<path d="M540 500 Q520 720 540 945" stroke="#b91c1c" stroke-width="7" fill="none" opacity=".5"/>'
                   '<path d="M520 490 Q510 420 570 390" stroke="#15803d" stroke-width="30" fill="none" stroke-linecap="round"/><ellipse cx="540" cy="485" rx="70" ry="22" fill="#22c55e"/>'
                   + shine(380, 620, 44, 22, -60) + face(540, 720, 1.1),
                   '<g>' + "".join(f'<g transform="translate({x} 330) scale(.26) translate(-540 -720)"><path d="M540 480 C620 440 760 470 790 600 C820 760 780 930 680 955 C620 970 590 940 540 950 C490 940 460 970 400 955 C300 930 260 760 290 600 C320 470 460 440 540 480Z" fill="{c}" stroke="#334155" stroke-width="14"/><ellipse cx="540" cy="485" rx="70" ry="24" fill="#15803d"/></g>' for x, c in ((760, "#22c55e"), (870, "#facc15"), (980, "#fb923c"))) + '</g>',
                   '<g transform="translate(180 380)"><path d="M-110 -100 Q0 -140 110 -100 Q130 60 0 120 Q-130 60 -110 -100Z" fill="#fff7ed" stroke="#ef4444" stroke-width="16"/>'
                   + "".join(f'<ellipse cx="{dx}" cy="{dy}" rx="9" ry="14" fill="#fef3c7" stroke="#d6a35c" stroke-width="3"/>' for dx, dy in ((-20, -20), (10, -30), (25, 0), (-10, 10), (0, -50), (-30, -45), (30, -55))) + '</g>')

AVOCADO = scene('<path d="M540 400 C460 400 420 500 400 580 C300 660 280 960 540 970 C800 960 780 660 680 580 C660 500 620 400 540 400Z" fill="#3f6212" stroke="#1a2e05" stroke-width="10"/>'
                '<path d="M540 430 C480 430 450 520 432 595 C345 670 330 935 540 940 C750 935 735 670 648 595 C630 520 600 430 540 430Z" fill="#d9f99d"/>'
                '<path d="M540 470 C500 470 480 540 466 600 C400 660 390 910 540 912 C690 910 680 660 614 600 C600 540 580 470 540 470Z" fill="#ecfccb" opacity=".8"/>'
                '<circle cx="540" cy="790" r="105" fill="#a16207" stroke="#713f12" stroke-width="8"/><ellipse cx="505" cy="755" rx="30" ry="18" fill="#fff" opacity=".35" transform="rotate(-35 505 755)"/>'
                + face(540, 590, .85),
                '<g transform="translate(880 340)"><rect x="-130" y="-110" width="260" height="220" rx="60" fill="#e8b07a" stroke="#b45309" stroke-width="10"/><rect x="-100" y="-80" width="200" height="160" rx="40" fill="#fde68a"/>'
                '<path d="M-90 -40 Q0 -80 90 -40 Q100 40 0 70 Q-100 40 -90 -40Z" fill="#a3e635"/></g>',
                '<g transform="translate(180 380)"><path d="M0 -120 C-40 -120 -60 -60 -70 -20 C-130 20 -130 140 0 140 C130 140 130 20 70 -20 C60 -60 40 -120 0 -120Z" fill="#365314" stroke="#1a2e05" stroke-width="8"/>'
                + "".join(f'<circle cx="{dx}" cy="{dy}" r="5" fill="#4d7c0f"/>' for dx, dy in ((-30, 0), (20, 30), (-50, 80), (40, 90), (0, 60), (10, -50), (-20, -80))) + '</g>')

SWEETPOTATO = scene('<path d="M190 760 C200 640 340 560 540 570 C740 560 880 640 890 760 C880 880 740 950 540 945 C340 950 200 880 190 760Z" fill="#c2410c" stroke="#7c2d12" stroke-width="10"/>'
                    '<path d="M190 760 l-60 10 M890 760 l60 -16" stroke="#7c2d12" stroke-width="10" stroke-linecap="round"/>'
                    + "".join(f'<path d="M{x} {y} q30 6 60 0" stroke="#9a3412" stroke-width="5" fill="none"/>' for x, y in ((300, 680), (700, 690), (290, 850), (720, 860), (480, 900)))
                    + shine(360, 650, 50, 20, -10) + face(540, 740, 1.1),
                    '<g transform="translate(880 330)"><ellipse rx="130" ry="80" fill="#c2410c"/><ellipse cx="40" rx="96" ry="72" fill="#fb923c" stroke="#ea580c" stroke-width="6"/><ellipse cx="40" rx="50" ry="36" fill="#fdba74" opacity=".7"/></g>',
                    '<g transform="translate(180 360)"><rect x="-130" y="20" width="260" height="140" rx="20" fill="#8d6e63"/>' + leaf(-40, -10, -60, s=.8) + leaf(40, -10, -120, s=.8) + leaf(0, -30, -90, s=.9)
                    + '<path d="M-20 100 Q0 60 30 90 Q60 120 20 140 Q-30 140 -20 100Z" fill="#c2410c"/></g>')

MUSHROOM = scene('<path d="M450 980 C440 860 450 760 470 680 L610 680 C630 760 640 860 630 980Z" fill="#fef3c7" stroke="#d6a35c" stroke-width="10"/>'
                 '<path d="M220 700 C220 470 380 380 540 380 C700 380 860 470 860 700 C860 740 820 750 540 750 C260 750 220 740 220 700Z" fill="#c08457" stroke="#7c4a21" stroke-width="10"/>'
                 '<path d="M260 712 C380 700 700 700 820 712" stroke="#fde68a" stroke-width="10" fill="none" opacity=".6"/>'
                 + shine(400, 500, 70, 30, -25) + face(540, 840, .8),
                 '<g transform="translate(930 230) scale(.8)">' + "".join(f'<g transform="translate({dx} {dy}) scale({s})"><rect x="-22" y="0" width="44" height="70" rx="16" fill="#fef3c7" stroke="#d6a35c" stroke-width="5"/><path d="M-70 10 C-70 -50 -30 -70 0 -70 C30 -70 70 -50 70 10Z" fill="#c08457" stroke="#7c4a21" stroke-width="5"/></g>' for dx, dy, s in ((-70, 20, 1), (60, 0, 1.2), (0, 60, .8))) + '</g>',
                 "".join(f'<g transform="translate({x} {y})"><path d="M-70 0 C-70 -60 70 -60 70 0Z" fill="#c08457" stroke="#7c4a21" stroke-width="6"/><rect x="-18" y="-4" width="36" height="60" rx="12" fill="#fef3c7" stroke="#d6a35c" stroke-width="5"/></g>' for x, y in ((110, 290), (200, 400))))

# ================= HABITS =================
def table(y=780):
    return f'<rect x="120" y="{y}" width="840" height="40" rx="14" fill="#e8b07a" stroke="#b45309" stroke-width="6"/><rect x="180" y="{y + 40}" width="34" height="160" fill="#b45309"/><rect x="866" y="{y + 40}" width="34" height="160" fill="#b45309"/>'


BREAKFAST = scene(kid(540, 500, shirt="#facc15") + table(760)
                  + '<path d="M330 700 Q330 780 430 780 Q530 780 530 700Z" fill="#60a5fa" stroke="#1d4ed8" stroke-width="7"/><ellipse cx="430" cy="702" rx="100" ry="20" fill="#fef3c7"/>'
                  + "".join(f'<circle cx="{x}" cy="{y}" r="13" fill="#4f46e5"/>' for x, y in ((395, 696), (430, 690), (465, 698)))
                  + '<ellipse cx="680" cy="752" rx="120" ry="24" fill="#fff" stroke="#e2e8f0" stroke-width="6"/><rect x="610" y="700" width="90" height="56" rx="14" fill="#f6c992" stroke="#b45309" stroke-width="5"/>'
                  + "".join(f'<circle cx="{x}" cy="738" r="16" fill="#fef08a" stroke="#eab308" stroke-width="4"/>' for x in (722, 756)),
                  sun(880, 300, 75),
                  '<g transform="translate(170 400)"><path d="M-60 -90 L60 -90 L50 110 L-50 110Z" fill="#fff" stroke="#cbd5e1" stroke-width="8"/><path d="M-56 -30 L56 -30 L50 104 L-50 104Z" fill="#fef3c7"/></g>')

LUNCHBOX = scene('<path d="M260 640 L320 420 L760 420 L820 640Z" fill="#7dd3fc" stroke="#0369a1" stroke-width="10"/>'
                 '<rect x="240" y="640" width="600" height="340" rx="40" fill="#38bdf8" stroke="#0369a1" stroke-width="10"/>'
                 '<rect x="270" y="610" width="540" height="60" rx="20" fill="#e0f2fe" stroke="#0369a1" stroke-width="6"/>'
                 '<path d="M300 640 L380 580 L460 640Z" fill="#fde68a" stroke="#d97706" stroke-width="6"/><path d="M308 636 L380 596 L452 636Z" fill="#86efac"/>'
                 '<path d="M500 640 a40 40 0 0 1 80 0Z" fill="#ef4444"/><path d="M590 640 a40 40 0 0 1 80 0Z" fill="#a3e635"/>'
                 + "".join(f'<rect x="{x}" y="560" width="16" height="80" rx="8" fill="#fb923c"/>' for x in (690, 715, 740, 765))
                 + '<rect x="500" y="440" width="80" height="80" rx="14" fill="#0369a1"/>' + face(540, 800, 1.05),
                 '<g transform="translate(900 360)"><rect x="-50" y="-110" width="100" height="220" rx="30" fill="#bae6fd" stroke="#0369a1" stroke-width="8"/><rect x="-30" y="-140" width="60" height="40" rx="10" fill="#3aa856"/><path d="M-50 0 H50" stroke="#38bdf8" stroke-width="40" opacity=".5"/></g>',
                 sparkles([(180, 330), (250, 470), (150, 540)]))

TRYNEW = scene(kid(540, 520, c="#c68642", hair="#1a1a2e", shirt="#a78bfa") + table(800)
               + '<ellipse cx="540" cy="790" rx="190" ry="34" fill="#fff" stroke="#e2e8f0" stroke-width="6"/>'
               + '<circle cx="480" cy="770" r="34" fill="#a16207"/><circle cx="480" cy="770" r="28" fill="#84cc16"/><circle cx="480" cy="770" r="10" fill="#f7fee7"/>'
               + '<circle cx="600" cy="772" r="30" fill="#ef4444"/>'
               + '<path d="M700 760 L760 560" stroke="#94a3b8" stroke-width="14" stroke-linecap="round"/><path d="M745 575 l10 -40 M760 580 l12 -40 M775 585 l12 -40" stroke="#94a3b8" stroke-width="7" stroke-linecap="round"/><circle cx="768" cy="532" r="20" fill="#22c55e"/>',
               '<g transform="translate(880 330)"><circle r="100" fill="#3aa856" stroke="#15803d" stroke-width="10"/>' + sparkles([(0, 0)], "#fff") + '</g>' + heart(180, 360, 1.2) + heart(260, 480, .8, "#f472b6"),
               sparkles([(200, 600), (880, 560), (740, 300)]))

WASHPRODUCE = scene('<rect x="230" y="800" width="620" height="180" rx="30" fill="#e0f2fe" stroke="#7dd3fc" stroke-width="10"/><ellipse cx="540" cy="806" rx="270" ry="40" fill="#bae6fd"/>'
                    '<path d="M640 430 L640 520 Q640 550 610 550 L560 550" stroke="#94a3b8" stroke-width="30" fill="none" stroke-linecap="round"/><rect x="620" y="400" width="60" height="40" rx="10" fill="#94a3b8"/>'
                    + "".join(f'<path d="M{x} 580 L{x - 6} 660" stroke="#7dd3fc" stroke-width="10" stroke-linecap="round" opacity=".8"/>' for x in (520, 545, 570))
                    + '<path d="M330 680 L750 680 L700 820 L380 820Z" fill="#fde68a" stroke="#d97706" stroke-width="8"/>'
                    + "".join(f'<circle cx="{x}" cy="{y}" r="5" fill="#d97706"/>' for x in range(400, 720, 40) for y in (720, 770))
                    + '<circle cx="440" cy="660" r="50" fill="#ef4444"/><circle cx="530" cy="650" r="44" fill="#fb923c"/><circle cx="620" cy="660" r="48" fill="#a3d65c"/><circle cx="560" cy="690" r="30" fill="#8b5cf6"/>'
                    + face(540, 900, .8),
                    bubbles([(420, 590, 22), (650, 610, 18)]) + drops([(380, 560), (700, 540), (460, 520)], "#7dd3fc"),
                    sparkles([(200, 330), (880, 320), (900, 520)]))

HARVEST = scene('<rect x="-500" y="880" width="2200" height="100" fill="#8d6e63"/>'
                + "".join(f'<path d="M{x} 880 Q{x - 40} 800 {x - 60} 780 M{x} 880 Q{x + 40} 800 {x + 60} 780 M{x} 880 V760" stroke="#22c55e" stroke-width="12" fill="none" stroke-linecap="round"/>' for x in (100, 980))
                + '<path d="M330 640 Q540 560 750 640" stroke="#a16207" stroke-width="16" fill="none"/>'
                + '<circle cx="410" cy="640" r="60" fill="#ef4444"/><circle cx="500" cy="610" r="56" fill="#22c55e"/><path d="M560 640 L620 560 L650 650Z" fill="#fb923c"/><circle cx="660" cy="630" r="54" fill="#8b5cf6"/>' + leaf(620, 540, -60, s=.7)
                + '<path d="M300 650 L780 650 L730 960 L350 960Z" fill="#d6a35c" stroke="#92400e" stroke-width="10"/>'
                + "".join(f'<path d="M{310 + i * 12} {700 + i * 60} H{770 - i * 12}" stroke="#a16207" stroke-width="6"/>' for i in range(4))
                + face(540, 760, .95),
                '<g transform="translate(170 380)"><path d="M-80 -40 L60 -40 L50 80 L-70 80Z" fill="#60a5fa" stroke="#1d4ed8" stroke-width="8"/><path d="M60 -20 L140 -80" stroke="#1d4ed8" stroke-width="16" stroke-linecap="round"/>'
                '<path d="M-60 -40 Q-10 -110 40 -40" stroke="#1d4ed8" stroke-width="10" fill="none"/></g>' + drops([(320, 330), (350, 410)], "#7dd3fc"),
                sun(880, 280, 70))

MARKET = scene(kid(540, 470, c="#ffd6a5", hair="#a16207", shirt="#3aa856")
               + "".join(f'<path d="M{x} 250 L{x + 100} 250 L{x + 100} 340 Q{x + 50} 380 {x} 340Z" fill="{c}"/>' for x, c in zip(range(140, 940, 100), ("#ef4444", "#fff") * 4))
               + '<rect x="130" y="230" width="820" height="30" rx="10" fill="#b91c1c"/><rect x="150" y="260" width="22" height="720" fill="#a16207"/><rect x="908" y="260" width="22" height="720" fill="#a16207"/>'
               + '<rect x="160" y="700" width="760" height="40" rx="10" fill="#c08457" stroke="#7c4a21" stroke-width="6"/>'
               + "".join(f'<rect x="{x}" y="740" width="230" height="200" rx="14" fill="#e8b07a" stroke="#b45309" stroke-width="8"/><path d="M{x} 810 H{x + 230} M{x} 870 H{x + 230}" stroke="#b45309" stroke-width="5"/>' for x in (190, 425, 660))
               + "".join(f'<circle cx="{x}" cy="{y}" r="34" fill="{c}"/>' for x, y, c in ((230, 680, "#ef4444"), (290, 670, "#ef4444"), (350, 680, "#ef4444"), (470, 680, "#fb923c"), (540, 670, "#fb923c"), (610, 680, "#fb923c"), (700, 680, "#a3e635"), (770, 670, "#a3e635"), (840, 680, "#a3e635"))),
               '<path d="M-100 150 Q270 230 540 160 Q810 230 1180 150" stroke="#7a2b2b" stroke-width="5" fill="none"/>' + "".join(f'<path d="M{x} {170 + 20 * math.sin(i)} l40 0 -20 50z" fill="{c}"/>' for i, (x, c) in enumerate(zip(range(-40, 1120, 110), ("#ef4444", "#facc15", "#3aa856", "#60a5fa", "#f472b6") * 3))),
               '<g transform="translate(990 820)"><path d="M-70 -60 L70 -60 L60 100 L-60 100Z" fill="#fef3c7" stroke="#a16207" stroke-width="8"/><path d="M-40 -60 Q0 -130 40 -60" stroke="#a16207" stroke-width="10" fill="none"/>'
               '<circle cx="-20" cy="-70" r="26" fill="#ef4444"/>' + leaf(30, -80, -70, s=.6) + '</g>')


def jumper(cx, cy):
    """A kid with arms up, jumping. Head center (cx, cy)."""
    return (f'<path d="M{cx - 60} {cy + 140} L{cx - 160} {cy - 10} M{cx + 60} {cy + 140} L{cx + 160} {cy - 10}" stroke="#ffd6a5" stroke-width="40" stroke-linecap="round"/>'
            f'<path d="M{cx - 40} {cy + 300} L{cx - 100} {cy + 400} M{cx + 40} {cy + 300} L{cx + 100} {cy + 400}" stroke="#1d4ed8" stroke-width="44" stroke-linecap="round"/>'
            f'<ellipse cx="{cx - 110}" cy="{cy + 420}" rx="40" ry="20" fill="#ef4444"/><ellipse cx="{cx + 110}" cy="{cy + 420}" rx="40" ry="20" fill="#ef4444"/>'
            + kid(cx, cy, c="#ffd6a5", hair="#f59e0b", shirt="#f472b6"))


PLAY = scene(jumper(540, 440),
             '<g transform="translate(880 820)"><circle r="90" fill="#facc15" stroke="#ca8a04" stroke-width="8"/><path d="M-90 0 Q0 -40 90 0 M0 -90 Q-40 0 0 90" stroke="#ef4444" stroke-width="10" fill="none"/></g>'
             '<g stroke="#7a2b2b" stroke-width="8" stroke-linecap="round" opacity=".5"><path d="M330 320 l-50 -30 M320 400 l-60 0 M750 320 l50 -30 M760 400 l60 0"/></g>',
             heart(180, 340, 1.4) + sparkles([(880, 300), (240, 500)]))

SUNSCREEN = scene('<rect x="400" y="460" width="280" height="520" rx="70" fill="#fde68a" stroke="#d97706" stroke-width="10"/>'
                  '<rect x="460" y="380" width="160" height="100" rx="20" fill="#3aa856" stroke="#15803d" stroke-width="8"/><rect x="510" y="340" width="60" height="50" rx="10" fill="#15803d"/>'
                  '<rect x="400" y="800" width="280" height="80" fill="#fb923c" opacity=".85"/>'
                  + '<g transform="translate(540 840) scale(.35)">' + sun(0, 0, 70) + '</g>' + shine(450, 560, 20, 60, 0) + face(540, 640, .85),
                  sun(880, 290, 80),
                  '<g transform="translate(180 400)"><ellipse cx="0" cy="30" rx="140" ry="40" fill="#fbbf24" stroke="#b45309" stroke-width="8"/><path d="M-80 30 Q-80 -80 0 -80 Q80 -80 80 30Z" fill="#fde68a" stroke="#b45309" stroke-width="8"/><rect x="-80" y="0" width="160" height="22" fill="#f472b6"/></g>'
                  '<g transform="translate(200 560)"><circle cx="-50" cy="0" r="40" fill="#1a1a2e" opacity=".85"/><circle cx="50" cy="0" r="40" fill="#1a1a2e" opacity=".85"/><path d="M-10 -5 h20" stroke="#1a1a2e" stroke-width="8"/></g>')

SNEEZE = scene('<rect x="450" y="610" width="180" height="200" rx="70" fill="#60a5fa"/>'
               '<circle cx="540" cy="520" r="120" fill="#ffd6a5"/><path d="M420 500 Q440 370 540 390 Q650 370 660 500 Q600 430 420 500Z" fill="#5d4037"/>'
               '<path d="M470 500 q22 -14 44 0 M566 500 q22 -14 44 0" stroke="#1a1a2e" stroke-width="8" fill="none" stroke-linecap="round"/>'
               '<path d="M620 690 Q580 600 480 580 Q420 540 400 450" stroke="#60a5fa" stroke-width="64" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
               '<circle cx="396" cy="420" r="32" fill="#ffd6a5"/>'
               '<ellipse cx="440" cy="540" rx="20" ry="11" fill="#ff8fab" opacity=".6"/><ellipse cx="640" cy="530" rx="20" ry="11" fill="#ff8fab" opacity=".6"/>'
               '<path d="M450 810 L430 960 M630 810 L650 960" stroke="#1d4ed8" stroke-width="44" stroke-linecap="round"/>',
               '<g transform="translate(880 400)"><rect x="-110" y="-40" width="220" height="140" rx="16" fill="#a78bfa" stroke="#6d28d9" stroke-width="8"/><ellipse cx="0" cy="-40" rx="60" ry="14" fill="#6d28d9"/>'
               '<path d="M-40 -40 Q-50 -110 0 -100 Q50 -120 40 -40" fill="#fff" stroke="#cbd5e1" stroke-width="5"/></g>',
               bubbles([(170, 330, 40), (240, 440, 28), (150, 520, 34), (900, 620, 30), (960, 540, 22)]))

SCENES_FRUITY2 = {
    "fr2_grapes": GRAPES, "fr2_pear": PEAR, "fr2_pineapple": PINEAPPLE, "fr2_kiwi": KIWI, "fr2_mango": MANGO,
    "fr2_cherries": CHERRIES, "fr2_lemon": LEMON, "fr2_peach": PEACH,
    "fr2_tomato": TOMATO, "fr2_cucumber": CUCUMBER, "fr2_potato": POTATO, "fr2_lettuce": LETTUCE, "fr2_bellpepper": BELLPEPPER,
    "fr2_avocado": AVOCADO, "fr2_sweetpotato": SWEETPOTATO, "fr2_mushroom": MUSHROOM,
    "fr2_breakfast": BREAKFAST, "fr2_lunchbox": LUNCHBOX, "fr2_trynew": TRYNEW, "fr2_washproduce": WASHPRODUCE,
    "fr2_harvest": HARVEST, "fr2_market": MARKET, "fr2_play": PLAY, "fr2_sunscreen": SUNSCREEN, "fr2_sneeze": SNEEZE,
}
NAMES_FRUITY2 = {
    "fr2_grapes": "GRAPES", "fr2_pear": "PEAR", "fr2_pineapple": "PINEAPPLE", "fr2_kiwi": "KIWI", "fr2_mango": "MANGO",
    "fr2_cherries": "CHERRIES", "fr2_lemon": "LEMON", "fr2_peach": "PEACH",
    "fr2_tomato": "TOMATO", "fr2_cucumber": "CUCUMBER", "fr2_potato": "POTATO", "fr2_lettuce": "LETTUCE", "fr2_bellpepper": "BELL PEPPER",
    "fr2_avocado": "AVOCADO", "fr2_sweetpotato": "SWEET POTATO", "fr2_mushroom": "MUSHROOMS",
    "fr2_breakfast": "BREAKFAST", "fr2_lunchbox": "PACK A LUNCH", "fr2_trynew": "TRY NEW FOODS", "fr2_washproduce": "WASH YOUR FOOD",
    "fr2_harvest": "GARDEN HARVEST", "fr2_market": "FARMERS MARKET", "fr2_play": "MOVE AND PLAY", "fr2_sunscreen": "SUNSCREEN", "fr2_sneeze": "COVER YOUR SNEEZE",
}
