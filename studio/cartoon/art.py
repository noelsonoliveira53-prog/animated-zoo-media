"""The Animated Zoo cartoon art (Nov 16 2026). Every shape is drawn here as SVG; nothing is traced or taken from another show.

Style (the bible in docs/cartoon/style_bible.html shows it):
  - characters: flat fills, ONE darker shade shape and ONE light shape per body part, a thick coloured outline around the whole
    silhouette (never black), big round eyes with two glints, pink cheeks. Anchored at the feet (0,0), facing right.
  - backgrounds: no outlines, three depth layers (far / mid / near) that the camera moves at different speeds.
  - words on screen: Baloo 2 ExtraBold, white or sun-yellow with the dark-brown outline.
Every id is prefixed (pid) so one character can stand in many shots."""
import math, random

INK = "#402010"; SUN = "#ffd23f"; WHITE = "#ffffff"
MILO_BLUE = "#2f80ed"; MILO_DARK = "#1c5fc4"; MILO_LINE = "#143f8a"; MILO_BELLY = "#bfe0ff"; BEAK = "#ff9f1c"; BEAK_D = "#e07f00"; SCARF = "#e63946"; SCARF_D = "#b81f2d"
CAMEL = {"fill": "#dba56a", "shade": "#bd8348", "light": "#f0c690", "line": "#7d4a22", "far": "#c58d52", "pad": "#8f5a2b", "hair": "#a5672f"}
CAMEL_B = {"fill": "#b98a5e", "shade": "#946843", "light": "#d6ab80", "line": "#5e3a1c", "far": "#a37850", "pad": "#6e4526", "hair": "#7d5230"}   # Bactrian: darker, woolly


def outlined(shapes, line, w=9):
    """One clean outline around a whole silhouette: the shapes once as a thick stroke in the line colour, then the shapes themselves."""
    return f'<g fill="{line}" stroke="{line}" stroke-width="{w * 2}" stroke-linejoin="round" stroke-linecap="round">{shapes}</g><g>{shapes}</g>'


def eye(pid, cx, cy, r, iris="#5b3413", look=(0, 0), lashes=0, lid="#dba56a"):
    """A big round eye. Parts: #<pid>-pupil (moves to look), #<pid>-lid (scaleY 0..1 = open..shut)."""
    lx, ly = look
    la = ""
    if lashes:        # camel: two rows of long eyelashes (San Diego Zoo: "double rows of extra-long eyelashes")
        for row, (rr, ln, wd) in enumerate(((r + 2, r * 0.75, 5), (r - 3, r * 0.5, 4))):
            for k in range(5):
                a = math.radians(-155 + k * 28 + row * 9); x0, y0 = cx + rr * math.cos(a), cy + rr * math.sin(a)
                x1, y1 = cx + (rr + ln) * math.cos(a - 0.25), cy + (rr + ln) * math.sin(a - 0.25)
                la += f'<path d="M{x0:.1f} {y0:.1f} Q{(x0 + x1) / 2 - 3:.1f} {(y0 + y1) / 2 - 4:.1f} {x1:.1f} {y1:.1f}" stroke="{INK}" stroke-width="{wd}" stroke-linecap="round" fill="none"/>'
    return (f'<g id="{pid}"><circle cx="{cx}" cy="{cy}" r="{r}" fill="#fff"/>'
            f'<g id="{pid}-pupil" transform="translate({lx} {ly})"><circle cx="{cx + r * .12:.1f}" cy="{cy + r * .05:.1f}" r="{r * .62:.1f}" fill="{iris}"/><circle cx="{cx + r * .12:.1f}" cy="{cy + r * .05:.1f}" r="{r * .36:.1f}" fill="#1a1a2e"/>'
            f'<circle cx="{cx + r * .34:.1f}" cy="{cy - r * .22:.1f}" r="{r * .2:.1f}" fill="#fff"/><circle cx="{cx - r * .08:.1f}" cy="{cy + r * .3:.1f}" r="{r * .1:.1f}" fill="#fff" opacity=".8"/></g>'
            f'<g id="{pid}-lid" opacity="0"><rect x="{cx - r - 2}" y="{cy - r - 2}" width="{2 * r + 4}" height="{2 * r + 4}" rx="{r}" fill="{lid}"/>'
            f'<path d="M{cx - r} {cy + r - 3} Q{cx} {cy + r + 8} {cx + r} {cy + r - 3}" stroke="{INK}" stroke-width="5" fill="none" stroke-linecap="round"/></g>{la}</g>')


def milo(pid="milo", scarf=True):
    """Milo the bluebird, front view: round body, crest of three feathers, big brown eyes, orange beak, pale belly, red scarf.
    Parts: #<pid>-body (squash and stretch), -wl / -wr (wings), -beak (lower beak opens when he talks), -eyeL / -eyeR, -browL / -browR, -legs, -crest."""
    sil = (f'<circle cx="0" cy="-150" r="118"/>'
           f'<path d="M-34 -258 L-22 -330 L-4 -262Z"/><path d="M-10 -262 L4 -350 L20 -262Z"/><path d="M14 -260 L34 -326 L42 -254Z"/>')
    body = (f'<g id="{pid}-crest" fill="{MILO_BLUE}"><path d="M-34 -258 L-22 -330 L-4 -262Z"/><path d="M-10 -262 L4 -350 L20 -262Z" fill="{MILO_DARK}"/><path d="M14 -260 L34 -326 L42 -254Z"/></g>'
            f'<circle cx="0" cy="-150" r="118" fill="{MILO_BLUE}"/>'
            f'<path d="M-112 -112 A118 118 0 0 0 112 -112 A150 150 0 0 1 -112 -112Z" fill="{MILO_DARK}" opacity=".45"/>'
            f'<ellipse cx="0" cy="-92" rx="78" ry="56" fill="{MILO_BELLY}"/><ellipse cx="-52" cy="-222" rx="34" ry="20" fill="#fff" opacity=".28" transform="rotate(-28 -52 -222)"/>')
    wings = (f'<g id="{pid}-wl"><ellipse cx="-112" cy="-136" rx="32" ry="60" fill="{MILO_DARK}" stroke="{MILO_LINE}" stroke-width="7" transform="rotate(16 -112 -136)"/>'
             f'<path d="M-132 -96 q-2 14 6 22 M-118 -90 q-2 14 6 22" stroke="{MILO_BLUE}" stroke-width="6" fill="none" stroke-linecap="round"/></g>'
             f'<g id="{pid}-wr"><ellipse cx="112" cy="-136" rx="32" ry="60" fill="{MILO_DARK}" stroke="{MILO_LINE}" stroke-width="7" transform="rotate(-16 112 -136)"/>'
             f'<path d="M132 -96 q2 14 -6 22 M118 -90 q2 14 -6 22" stroke="{MILO_BLUE}" stroke-width="6" fill="none" stroke-linecap="round"/></g>')
    legs = (f'<g id="{pid}-legs" stroke="{BEAK}" stroke-width="10" stroke-linecap="round" fill="none"><path d="M-34 -40 L-36 -6 M-36 -6 l-18 6 M-36 -6 l2 8 M-36 -6 l18 4"/>'
            f'<path d="M34 -40 L36 -6 M36 -6 l-18 4 M36 -6 l-2 8 M36 -6 l18 6"/></g>')
    face = (eye(f"{pid}-eyeL", -46, -182, 40, lid=MILO_BLUE) + eye(f"{pid}-eyeR", 46, -182, 40, lid=MILO_BLUE)
            + f'<path id="{pid}-browL" d="M-78 -236 q30 -18 58 -4" stroke="{MILO_DARK}" stroke-width="9" fill="none" stroke-linecap="round"/>'
            + f'<path id="{pid}-browR" d="M78 -236 q-30 -18 -58 -4" stroke="{MILO_DARK}" stroke-width="9" fill="none" stroke-linecap="round"/>'
            + f'<ellipse cx="-88" cy="-128" rx="17" ry="11" fill="#ff8fb1" opacity=".8"/><ellipse cx="88" cy="-128" rx="17" ry="11" fill="#ff8fb1" opacity=".8"/>'
            + f'<g id="{pid}-beak"><path d="M-26 -128 Q0 -84 26 -128 Q0 -116 -26 -128Z" fill="{BEAK_D}"/></g>'
            + f'<path d="M-36 -136 Q0 -174 36 -136 Q0 -112 -36 -136Z" fill="{BEAK}"/><path d="M-16 -144 Q0 -156 14 -146" stroke="#ffc766" stroke-width="5" fill="none" stroke-linecap="round"/>')
    sc = ""
    if scarf:
        sc = (f'<path d="M-104 -78 Q0 -38 104 -78 L100 -52 Q0 -10 -100 -52Z" fill="{SCARF}"/><path d="M-100 -56 Q0 -16 100 -56 L100 -52 Q0 -10 -100 -52Z" fill="{SCARF_D}"/>'
              f'<g id="{pid}-scarf"><path d="M52 -52 l34 50 l-26 4 l-22 -44Z" fill="{SCARF}"/><path d="M40 -46 l8 54 l-24 -6 l-2 -46Z" fill="{SCARF_D}"/></g><circle cx="48" cy="-50" r="14" fill="{SCARF}"/>')
    return (f'<g id="{pid}"><ellipse cx="0" cy="2" rx="86" ry="13" fill="#000" opacity=".13" id="{pid}-shadow"/>{legs}'
            f'<g id="{pid}-body">{outlined(sil, MILO_LINE, 7)}{wings}{body}{sc}{face}</g></g>')


def camel(pid, humps=1, c=CAMEL, calf=False, wool=False):
    """A camel, side view facing right. humps: 0 (a calf: a little peak with a tuft of curly hair where the hump will form),
    1 (dromedary) or 2 (Bactrian). Parts: #<pid>-hump (leans over when the fat is used), -neck (head and neck: nods, bends to drink),
    -jaw (chews), -eye-lid (blinks), -nose (nostril shuts), -fl -fr -bl -br (legs, walk), -tail, -ear.
    Every part that moves carries its own outline, so a head that turns or a hump that leans takes its line with it."""
    L = 1.12 if calf else 1.0; ln = c["line"]                # a calf's legs are long for its body
    def ol(shapes, w=9): return f'<g fill="{ln}" stroke="{ln}" stroke-width="{w * 2}" stroke-linejoin="round" stroke-linecap="round">{shapes}</g>'
    def leg(x, far, name):
        col = c["far"] if far else c["fill"]; top = -262; pad = c["pad"] if not far else c["shade"]
        sh = (f'<rect x="{x - 25}" y="{top}" width="50" height="{150 * L:.0f}" rx="24"/><rect x="{x - 19}" y="{top + 132 * L:.0f}" width="38" height="{118 * L:.0f}" rx="18"/>'
              f'<ellipse cx="{x + 6}" cy="{top + 252 * L - 4:.0f}" rx="33" ry="15"/>')
        return (f'<g id="{pid}-{name}">{ol(sh)}<rect x="{x - 25}" y="{top}" width="50" height="{150 * L:.0f}" rx="24" fill="{col}"/>'
                f'<rect x="{x - 19}" y="{top + 132 * L:.0f}" width="38" height="{118 * L:.0f}" rx="18" fill="{col}"/><ellipse cx="{x + 4}" cy="{top + 132 * L:.0f}" rx="24" ry="19" fill="{col}"/>'
                f'<ellipse cx="{x + 6}" cy="{top + 252 * L - 4:.0f}" rx="33" ry="15" fill="{pad}"/></g>')
    lift = -(252 * L - 262 + 11)
    far_legs = leg(-178, True, "bl2") + leg(118, True, "fl2"); near_legs = leg(-138, False, "bl") + leg(160, False, "fl")
    hump_path = {0: "", 1: "M-170 -372 C-150 -470 -70 -590 10 -590 C90 -590 150 -470 176 -372Z",
                 2: "M-200 -372 C-190 -450 -150 -560 -96 -560 C-46 -560 -24 -470 -6 -400 C10 -470 40 -568 96 -568 C150 -568 186 -450 198 -372Z"}[humps]
    hump = ""; patch = ""
    if humps:
        hl = ('<path d="M-60 -548 C-20 -572 30 -572 64 -540" stroke="%s" stroke-width="16" fill="none" stroke-linecap="round" opacity=".9"/>' % c["light"]) if humps == 1 else \
             ('<path d="M-128 -532 C-108 -548 -86 -548 -70 -530 M62 -540 C84 -556 108 -556 126 -536" stroke="%s" stroke-width="14" fill="none" stroke-linecap="round" opacity=".9"/>' % c["light"])
        hw = ""
        if wool: hw = f'<path d="M-150 -540 q10 -18 22 0 q10 -18 22 0 M70 -548 q10 -18 22 0 q10 -18 22 0" stroke="{c["hair"]}" stroke-width="9" fill="none" stroke-linecap="round"/>'
        hump = f'<g id="{pid}-hump">{ol(f"<path d=\"{hump_path}\"/>")}<path d="{hump_path}" fill="{c["fill"]}"/>{hl}{hw}</g>'
        patch = f'<path d="M-168 -404 Q0 -462 172 -404" stroke="{c["fill"]}" stroke-width="34" fill="none" stroke-linecap="round"/>'      # the body's line under the hump
    tuft = ""; tuft_sh = ""
    if humps == 0:      # San Diego Zoo: "The calf has no humps but small peaks of hide, each topped with a tassel of curly hair"
        tuft_sh = '<path d="M-78 -398 Q0 -476 78 -398Z"/>'
        tuft = (f'<g id="{pid}-tuft"><path d="M-78 -398 Q0 -476 78 -398Z" fill="{c["fill"]}"/>'
                + "".join(f'<path d="M{x} -{y} q-16 -34 10 -46 q26 -8 18 20 q-8 18 -22 8" stroke="{c["hair"]}" stroke-width="11" fill="none" stroke-linecap="round"/>' for x, y in ((-40, 424), (-8, 440), (26, 426))) + '</g>')
    wl = ""
    if wool:            # woolly coat: a shaggy bib on the front of the neck
        wl = f'<path d="M206 -292 q-14 -74 34 -132 q34 26 44 84 q-12 12 -20 -4 q-6 18 -22 4 q-8 18 -24 6 q-4 22 -12 42Z" fill="{c["hair"]}"/>'
    neck_d = "M176 -318 C262 -340 292 -420 300 -560"
    HK = 1.22 if calf else 1.0                               # a calf's head is big for its body
    hs0, hs1 = (f'<g transform="translate(190 -330) scale({HK}) translate(-190 330)">', '</g>')
    head_sh = (f'<path d="{neck_d}" fill="none" stroke-width="{104 + 18}" stroke-linecap="round"/><ellipse cx="338" cy="-600" rx="92" ry="62" transform="rotate(-8 338 -600)"/>'
               f'<ellipse cx="412" cy="-578" rx="62" ry="46"/><path d="M262 -640 q-22 -44 16 -58 q20 26 14 60Z"/>')
    neck = (f'<g id="{pid}-neck">' + hs0 + f'<g fill="{ln}" stroke="{ln}" stroke-width="18" stroke-linejoin="round" stroke-linecap="round">{head_sh}</g>'
            f'<path d="{neck_d}" fill="none" stroke="{c["fill"]}" stroke-width="104" stroke-linecap="round"/><path d="M214 -300 C286 -330 318 -410 330 -520" fill="none" stroke="{c["shade"]}" stroke-width="30" stroke-linecap="round" opacity=".55"/>'
            + wl +
            f'<g id="{pid}-ear"><path d="M262 -640 q-22 -44 16 -58 q20 26 14 60Z" fill="{c["fill"]}"/><path d="M270 -646 q-10 -26 8 -38 q8 18 6 38Z" fill="{c["shade"]}"/></g>'
            f'<ellipse cx="338" cy="-600" rx="92" ry="62" fill="{c["fill"]}" transform="rotate(-8 338 -600)"/>'
            f'<g id="{pid}-jaw"><path d="M372 -566 q52 34 96 6 q-6 34 -50 38 q-34 2 -46 -44Z" fill="{c["shade"]}"/></g>'
            f'<ellipse cx="412" cy="-578" rx="62" ry="46" fill="{c["light"]}"/><path d="M420 -548 q26 12 48 -8" stroke="{ln}" stroke-width="6" fill="none" stroke-linecap="round"/>'
            f'<g id="{pid}-nose"><ellipse cx="452" cy="-594" rx="11" ry="7" fill="{ln}" transform="rotate(-24 452 -594)"/></g>'
            f'<path d="M300 -662 q14 -30 34 -8 q18 -24 34 2" stroke="{c["hair"]}" stroke-width="12" fill="none" stroke-linecap="round"/>'
            + eye(f"{pid}-eye", 352, -612, 27 if not calf else 31, lashes=1, lid=c["fill"])
            + f'<ellipse cx="392" cy="-560" rx="15" ry="9" fill="#ff8fb1" opacity=".55"/>' + hs1 + '</g>')
    npatch = f'<circle cx="182" cy="-322" r="58" fill="{c["fill"]}"/>'                                    # the neck's line where it joins the body
    tail = (f'<g id="{pid}-tail"><path d="M-232 -340 q-40 40 -30 110" stroke="{ln}" stroke-width="30" fill="none" stroke-linecap="round"/><ellipse cx="-262" cy="-222" rx="23" ry="31" fill="{ln}"/>'
            f'<path d="M-232 -340 q-40 40 -30 110" stroke="{c["fill"]}" stroke-width="16" fill="none" stroke-linecap="round"/><ellipse cx="-262" cy="-222" rx="16" ry="24" fill="{c["hair"]}"/></g>')
    body = ol('<ellipse cx="0" cy="-322" rx="238" ry="118"/>' + tuft_sh) + f'<ellipse cx="0" cy="-322" rx="238" ry="118" fill="{c["fill"]}"/>'
    shade = (f'<path d="M-226 -290 A238 118 0 0 0 226 -290 A300 160 0 0 1 -226 -290Z" fill="{c["shade"]}" opacity=".6"/><ellipse cx="-70" cy="-392" rx="92" ry="26" fill="{c["light"]}" opacity=".5"/>')
    sh = f'<ellipse cx="10" cy="4" rx="{250 if not calf else 230}" ry="18" fill="#000" opacity=".13"/>'
    return (f'<g id="{pid}">{sh}<g id="{pid}-all" transform="translate(0 {lift:.0f})">{tail}<g>{far_legs}</g>{hump}{body}{patch}{tuft}{neck}{npatch}{shade}{near_legs}</g></g>')


# ---------------------------------------------------------------- backgrounds: (far, mid, near) layers, drawn from x=-500 to 2420, y=-900 to 1980
def _sky(p, top, bottom, y0=-900, y1=700):
    k = p
    return (f'<defs><linearGradient id="sky{k}" gradientUnits="userSpaceOnUse" x1="0" y1="-60" x2="0" y2="{y1}"><stop offset="0" stop-color="{top}"/><stop offset="1" stop-color="{bottom}"/></linearGradient></defs>'
            f'<rect x="-500" y="{y0}" width="2920" height="{y1 - y0}" fill="url(#sky{k})"/>')


def _cloud(pid, x, y, s=1.0, col="#fff", op=.95):
    return (f'<g id="{pid}" opacity="{op}" transform="translate({x} {y}) scale({s})"><ellipse cx="0" cy="0" rx="110" ry="40" fill="{col}"/><ellipse cx="-56" cy="-22" rx="58" ry="42" fill="{col}"/>'
            f'<ellipse cx="46" cy="-28" rx="66" ry="48" fill="{col}"/></g>')


def _dune(y, amp, col, seed, x0=-500, x1=2420, bottom=1980):
    r = random.Random(seed); pts = []; x = x0
    while x <= x1 + 300: pts.append((x, y + r.uniform(-amp, amp))); x += r.uniform(380, 620)
    d = f"M{x0} {bottom} L{pts[0][0]:.0f} {pts[0][1]:.0f} "
    for (xa, ya), (xb, yb) in zip(pts, pts[1:]): d += f"C{xa + 190:.0f} {ya - amp * .5:.0f} {xb - 190:.0f} {yb - amp * .5:.0f} {xb:.0f} {yb:.0f} "
    return f'<path d="{d}L{x1 + 300} {bottom}Z" fill="{col}"/>'


def _palm(pid, x, y, s=1.0):
    fr = "".join(f'<path d="M0 -330 Q{90 * math.cos(a) :.0f} {-330 + 150 * math.sin(a) - 70:.0f} {210 * math.cos(a):.0f} {-330 + 150 * math.sin(a) + 30:.0f} Q{90 * math.cos(a):.0f} {-330 + 150 * math.sin(a) - 20:.0f} 0 -330Z" fill="{c}"/>'
                 for a, c in ((-2.8, "#2f9e5b"), (-0.35, "#2f9e5b"), (3.5, "#3fb56c"), (-0.1, "#3fb56c"), (-1.9, "#52c77e"), (-1.2, "#3fb56c")))
    return (f'<g id="{pid}" transform="translate({x} {y}) scale({s})"><path d="M-16 0 Q-34 -170 -6 -330 L14 -330 Q-2 -170 22 0Z" fill="#a8703a"/>'
            + "".join(f'<path d="M{-20 + i * 1.2:.0f} {-40 - i * 46} q18 -10 36 0" stroke="#8a5628" stroke-width="6" fill="none"/>' for i in range(6))
            + f'<g id="{pid}-fr">{fr}<circle cx="-8" cy="-318" r="13" fill="#7a4a22"/><circle cx="14" cy="-312" r="12" fill="#8a5628"/></g></g>')


def _cactus(x, y, s=1.0, col="#3fa65f", dark="#2c8048"):
    return (f'<g transform="translate({x} {y}) scale({s})"><rect x="-26" y="-210" width="52" height="210" rx="26" fill="{col}"/><path d="M-26 -90 h-34 a22 22 0 0 1 -22 -22 v-44 a14 14 0 0 1 28 0 v36 h28Z" fill="{col}"/>'
            f'<path d="M26 -120 h30 a22 22 0 0 0 22 -22 v-30 a14 14 0 0 0 -28 0 v24 h-24Z" fill="{col}"/><rect x="6" y="-200" width="14" height="190" rx="7" fill="{dark}" opacity=".5"/></g>')


def _thorn(pid, x, y, s=1.0):
    """A thorny desert bush (San Diego Zoo: tough lips "can break off and eat vegetation such as thorns or salty plants")."""
    br = "".join(f'<path d="M0 0 Q{40 * math.cos(a):.0f} {-70 + 30 * math.sin(a):.0f} {120 * math.cos(a):.0f} {-150 * abs(math.sin(a)) - 30:.0f}" stroke="#7b8f3a" stroke-width="12" fill="none" stroke-linecap="round"/>' for a in (-2.6, -2.1, -1.57, -1.0, -0.5))
    th = "".join(f'<path d="M{120 * math.cos(a) * k:.0f} {(-150 * abs(math.sin(a)) - 30) * k:.0f} l{14 * math.cos(a + 1):.0f} {-16:.0f}" stroke="#55682a" stroke-width="5" stroke-linecap="round"/>' for a in (-2.6, -2.1, -1.57, -1.0, -0.5) for k in (.45, .7, 1.0))
    lv = "".join(f'<ellipse cx="{120 * math.cos(a) * k:.0f}" cy="{(-150 * abs(math.sin(a)) - 30) * k - 6:.0f}" rx="15" ry="9" fill="#9bb24a" transform="rotate({math.degrees(a):.0f} {120 * math.cos(a) * k:.0f} {(-150 * abs(math.sin(a)) - 30) * k - 6:.0f})"/>' for a in (-2.6, -2.1, -1.57, -1.0, -0.5) for k in (.6, .9))
    return f'<g id="{pid}" transform="translate({x} {y}) scale({s})">{br}{th}{lv}</g>'


def _sun(pid, x, y, r=90, col="#ffe066"):
    return f'<g id="{pid}"><circle cx="{x}" cy="{y}" r="{r * 1.6}" fill="{col}" opacity=".25"/><circle cx="{x}" cy="{y}" r="{r}" fill="{col}"/></g>'


def bg_dunes(p):
    """Sunrise dunes: where Sandy and her mama live (dromedaries: "desert areas in North Africa and the Middle East")."""
    far = _sky(p, "#7fd0ff", "#ffe9c4") + _sun(p + "sun", 1560, 210) + _cloud(p + "c1", 420, 170) + _cloud(p + "c2", 1180, 110, .7) + _dune(560, 40, "#f7d49a", 3)
    mid = _dune(660, 50, "#f2c078", 5) + _cactus(170, 700, .8) + _cactus(1740, 690, .65)
    near = _dune(800, 30, "#eaae62", 7) + f'<rect x="-500" y="900" width="2920" height="1100" fill="#e2a258"/>' + _dune(905, 14, "#e2a258", 9) + \
        "".join(f'<ellipse cx="{x}" cy="{y}" rx="{w}" ry="6" fill="#d18f48" opacity=".6"/>' for x, y, w in ((300, 960, 90), (900, 1010, 120), (1500, 950, 80), (1250, 1040, 60), (620, 1045, 70)))
    return far, mid, near


def bg_trail(p):
    """A rocky desert trail with thorny plants."""
    far = _sky(p, "#8ad6ff", "#ffe2b8") + _sun(p + "sun", 300, 190, 80) + _cloud(p + "c1", 1300, 150, .9) + \
        '<path d="M-500 620 L80 380 L360 560 L700 300 L1040 590 L1400 360 L1800 600 L2100 420 L2420 620 L2420 760 L-500 760Z" fill="#e7b98c"/><path d="M700 300 L820 400 L760 420 L900 520 L1040 590Z" fill="#d8a473"/><path d="M1400 360 L1500 450 L1460 470 L1620 560 L1800 600Z" fill="#d8a473"/>'
    mid = _dune(700, 26, "#eec088", 11) + '<path d="M1500 720 l70 -120 l90 30 l60 -70 l110 160Z" fill="#c98f5f"/><path d="M40 730 l60 -90 l100 20 l70 70Z" fill="#c98f5f"/>'
    near = f'<rect x="-500" y="820" width="2920" height="1200" fill="#e3a866"/>' + _dune(826, 12, "#e3a866", 13) + '<path d="M-500 930 C300 880 700 990 1200 930 S2000 900 2420 950" stroke="#d09552" stroke-width="60" fill="none" opacity=".55"/>' + \
        "".join(f'<path d="M{x} {y} l18 -26 l30 4 l16 22Z" fill="#b98558"/>' for x, y in ((240, 1000), (760, 1040), (1320, 1010), (1700, 1050), (1040, 900)))
    return far, mid, near


def bg_oasis(p):
    """An oasis: palms and a pool."""
    far = _sky(p, "#79cdfb", "#fdf0cf") + _cloud(p + "c1", 300, 140, .8) + _cloud(p + "c2", 1500, 190, 1.1) + _dune(600, 36, "#f6d39b", 21)
    mid = _dune(690, 30, "#efc182", 23) + _palm(p + "p1", 250, 760, 1.25) + _palm(p + "p2", 1660, 740, 1.05) + _palm(p + "p3", 1840, 770, .8)
    near = (f'<rect x="-500" y="830" width="2920" height="1200" fill="#e6ad66"/>' + _dune(836, 12, "#e6ad66", 25)
            + f'<ellipse cx="1060" cy="960" rx="560" ry="96" fill="#58b9e8"/><ellipse cx="1060" cy="952" rx="520" ry="80" fill="#7fd3f7"/>'
            + f'<g id="{p}rip"><ellipse cx="900" cy="950" rx="120" ry="14" fill="none" stroke="#fff" stroke-width="5" opacity=".7"/><ellipse cx="1250" cy="975" rx="90" ry="10" fill="none" stroke="#fff" stroke-width="5" opacity=".6"/></g>'
            + "".join(f'<path d="M{x} {y} q8 -40 0 -70 M{x + 14} {y} q14 -30 16 -56 M{x - 12} {y} q-12 -30 -14 -50" stroke="#49a35e" stroke-width="8" fill="none" stroke-linecap="round"/>' for x, y in ((520, 930), (1610, 948), (700, 1030))))
    return far, mid, near


def bg_wind(p):
    """Windy dunes: sand blowing in the air (gentle, golden; nobody is in trouble)."""
    far = _sky(p, "#f6d28c", "#fbe6bd") + _sun(p + "sun", 1000, 240, 110, "#fff1b8") + _dune(540, 60, "#f1c47c", 31)
    mid = _dune(660, 60, "#e9b266", 33)
    near = f'<rect x="-500" y="860" width="2920" height="1200" fill="#dc9d50"/>' + _dune(866, 20, "#dc9d50", 35) + \
        f'<g id="{p}gust">' + "".join(f'<path d="M{x} {y} q120 -30 240 0 t240 0" stroke="#fff3cf" stroke-width="{w}" fill="none" stroke-linecap="round" opacity=".7"/>'
                                      for x, y, w in ((-300, 300, 10), (500, 420, 7), (1300, 260, 9), (100, 560, 6), (1000, 620, 8), (1700, 500, 7), (-200, 760, 7), (900, 820, 6))) + '</g>'
    return far, mid, near


def bg_gobi(p):
    """The cold home of the two-humped camel (Nat Geo Kids: "rocky deserts where it gets very cold in the winter"; "mountain areas where snow ... provide water")."""
    far = _sky(p, "#9db9e8", "#e9f1fb") + _cloud(p + "c1", 500, 150, 1.0, "#fff") + \
        '<path d="M-500 640 L120 300 L420 520 L760 220 L1120 560 L1480 280 L1880 580 L2420 360 L2420 760 L-500 760Z" fill="#8ea6cf"/>' + \
        '<path d="M120 300 L220 380 L170 400 L260 440 L60 420Z M760 220 L880 330 L820 350 L920 400 L640 380Z M1480 280 L1590 370 L1540 390 L1640 440 L1380 400Z" fill="#fff"/>'
    mid = _dune(690, 24, "#cdd9ec", 41) + '<path d="M1500 700 l60 -90 l100 20 l70 70Z M200 720 l50 -70 l80 14 l60 56Z" fill="#9aa8bf"/>'
    near = f'<rect x="-500" y="840" width="2920" height="1200" fill="#eef3fa"/>' + _dune(846, 14, "#eef3fa", 43) + \
        "".join(f'<ellipse cx="{x}" cy="{y}" rx="{w}" ry="8" fill="#d6e0ef"/>' for x, y, w in ((300, 950, 120), (980, 1010, 150), (1560, 940, 100)))
    return far, mid, near


def bg_night(p):
    """Night in the desert: stars, a big moon, a lantern. Bedtime, calm."""
    r = random.Random(5)
    stars = "".join(f'<circle class="{p}star" cx="{r.uniform(-400, 2300):.0f}" cy="{r.uniform(-800, 560):.0f}" r="{r.choice((3, 4, 5, 6)):.0f}" fill="#fff8d6" opacity="{r.uniform(.5, 1):.2f}"/>' for _ in range(90))
    far = _sky(p, "#18245c", "#3a4a9a") + stars + f'<circle cx="1520" cy="200" r="150" fill="#fff6c9" opacity=".2"/><circle cx="1520" cy="200" r="104" fill="#fff6c9"/><circle cx="1490" cy="176" r="18" fill="#f0e3a4"/><circle cx="1552" cy="234" r="12" fill="#f0e3a4"/>'
    far += _dune(600, 40, "#2c3a7c", 51)
    mid = _dune(700, 40, "#34449a", 53) + _palm(p + "p1", 70, 770, 1.0).replace("#2f9e5b", "#1f5c53").replace("#3fb56c", "#27705f").replace("#52c77e", "#2e8068").replace("#a8703a", "#5a4a5e")
    near = f'<rect x="-500" y="850" width="2920" height="1200" fill="#4a57a8"/>' + _dune(856, 14, "#4a57a8", 55) + \
        f'<g id="{p}lamp" transform="translate(1500 900)"><circle cx="0" cy="-60" r="150" fill="#ffd97a" opacity=".22"/><rect x="-26" y="-96" width="52" height="76" rx="12" fill="#ffd97a"/><rect x="-32" y="-104" width="64" height="14" rx="6" fill="#7a4a22"/><rect x="-32" y="-24" width="64" height="14" rx="6" fill="#7a4a22"/><path d="M-18 -104 q18 -34 36 0" stroke="#7a4a22" stroke-width="6" fill="none"/></g>'
    return far, mid, near


def bg_zoo(p):
    """The zoo gate in the morning: where every trip starts."""
    far = _sky(p, "#8fd8ff", "#eaf8ff") + _sun(p + "sun", 250, 200, 86) + _cloud(p + "c1", 900, 150) + _cloud(p + "c2", 1600, 230, .8) + \
        '<path d="M-500 720 C0 560 400 640 800 600 S1600 560 2420 680 L2420 800 L-500 800Z" fill="#a8e08a"/>'
    mid = ('<path d="M-500 780 C200 700 700 760 1200 720 S2000 720 2420 760 L2420 900 L-500 900Z" fill="#8fd470"/>'
           + "".join(f'<g transform="translate({x} {y}) scale({s})"><rect x="-14" y="-90" width="28" height="90" fill="#9a6a3a"/><circle cx="0" cy="-150" r="80" fill="#4fb565"/><circle cx="-46" cy="-110" r="52" fill="#43a559"/><circle cx="48" cy="-112" r="56" fill="#5cc473"/></g>' for x, y, s in ((180, 800, 1.2), (1760, 790, 1.0), (1500, 780, .7))))
    near = (f'<rect x="-500" y="860" width="2920" height="1200" fill="#7cc95e"/><path d="M700 1980 L860 860 L1060 860 L1220 1980Z" fill="#f2d9a6"/>'
            f'<g id="{p}gate"><rect x="640" y="430" width="56" height="450" rx="14" fill="#b9793f"/><rect x="1224" y="430" width="56" height="450" rx="14" fill="#b9793f"/>'
            f'<path d="M600 470 Q960 300 1320 470 L1320 560 Q960 400 600 560Z" fill="{MILO_BLUE}"/><path d="M600 548 Q960 388 1320 548 L1320 560 Q960 400 600 560Z" fill="{MILO_DARK}"/>'
            f'<circle cx="668" cy="420" r="34" fill="{SUN}"/><circle cx="1252" cy="420" r="34" fill="#ff7aa2"/></g>'
            + "".join(f'<circle cx="{x}" cy="{y}" r="9" fill="{c}"/><circle cx="{x + 16}" cy="{y + 6}" r="7" fill="#fff"/>' for x, y, c in ((300, 960, "#ff7aa2"), (480, 1010, SUN), (1500, 970, "#ff7aa2"), (1720, 1020, SUN), (1380, 1050, "#fff"))))
    return far, mid, near


def bg_paper(p, col="#fff6e0", grid="#f0e2c0"):
    """The picture board for diagrams and comparisons: warm paper with a soft grid, so a diagram never floats in a scene."""
    far = f'<rect x="-500" y="-900" width="2920" height="2900" fill="{col}"/>' + "".join(f'<path d="M{x} -900 V1980" stroke="{grid}" stroke-width="4"/>' for x in range(-480, 2420, 120)) + \
        "".join(f'<path d="M-500 {y} H2420" stroke="{grid}" stroke-width="4"/>' for y in range(-840, 1980, 120))
    return far, "", ""


BG = {"dunes": bg_dunes, "trail": bg_trail, "oasis": bg_oasis, "wind": bg_wind, "gobi": bg_gobi, "night": bg_night, "zoo": bg_zoo, "paper": bg_paper,
      "paper_blue": lambda p: bg_paper(p, "#e6f4ff", "#cfe6f8"), "paper_pink": lambda p: bg_paper(p, "#ffeef2", "#f8d9e0")}
PLACE = {"dunes": "the dunes at sunrise", "trail": "the rocky trail", "oasis": "the oasis", "wind": "the windy dunes", "gobi": "the snowy Gobi", "night": "the desert at night",
         "zoo": "the zoo gate", "paper": "the picture board", "paper_blue": "the picture board (blue)", "paper_pink": "the picture board (pink)"}


# ---------------------------------------------------------------- props (drawn at their own origin, placed by the shot)
def hump_cutaway(pid):
    """Inside the hump: fat (San Diego Zoo: "They store fat, not water. The fat becomes an energy source for the camel.")."""
    blobs = "".join(f'<circle class="{pid}-fat" cx="{x}" cy="{y}" r="{r}" fill="#ffe08a" stroke="#f2b84b" stroke-width="6"/>' for x, y, r in
                    ((-150, -60, 52), (-60, -70, 60), (40, -66, 58), (140, -56, 50), (-110, -160, 54), (-10, -180, 62), (90, -160, 54), (-56, -270, 52), (40, -272, 50), (-8, -350, 40)))
    return (f'<g id="{pid}"><path d="M-260 0 C-230 -150 -110 -430 0 -430 C110 -430 230 -150 260 0Z" fill="#dba56a" stroke="#7d4a22" stroke-width="16" stroke-linejoin="round"/>'
            f'<path d="M-214 -14 C-190 -140 -92 -384 0 -384 C92 -384 190 -140 214 -14Z" fill="#fff3d0"/>{blobs}</g>')


def water_drop(pid, s=1.0):
    return f'<g id="{pid}" transform="scale({s})"><path d="M0 -120 C60 -40 80 0 80 40 A80 80 0 0 1 -80 40 C-80 0 -60 -40 0 -120Z" fill="#58b9e8"/><ellipse cx="-30" cy="30" rx="16" ry="26" fill="#fff" opacity=".6"/></g>'


def lunchbox(pid):
    return (f'<g id="{pid}"><rect x="-150" y="-170" width="300" height="170" rx="26" fill="#ff7a59"/><rect x="-150" y="-170" width="300" height="60" rx="26" fill="#ff9c82"/><rect x="-28" y="-128" width="56" height="36" rx="10" fill="#fff"/>'
            f'<path d="M-70 -170 q70 -80 140 0" stroke="#c9482c" stroke-width="16" fill="none" stroke-linecap="round"/></g>')


def bolt(pid):
    return f'<path id="{pid}" d="M10 -120 L-50 10 L-6 10 L-24 110 L56 -30 L8 -30Z" fill="{SUN}" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>'


def jug(pid):
    return f'<g id="{pid}"><rect x="-34" y="-96" width="68" height="96" rx="14" fill="#7fd3f7" stroke="#2b7fb0" stroke-width="7"/><rect x="-16" y="-120" width="32" height="28" rx="6" fill="#2b7fb0"/><rect x="-22" y="-60" width="44" height="46" rx="8" fill="#fff" opacity=".5"/></g>'


def footprint(pid, wide=True):
    """A camel's foot: broad, "they expand when stepped on" (San Diego Zoo)."""
    w = 96 if wide else 44
    return (f'<g id="{pid}"><ellipse cx="0" cy="0" rx="{w}" ry="{w * .62:.0f}" fill="#8f5a2b"/><path d="M0 {-w * .62:.0f} V{w * .2:.0f}" stroke="#6e4526" stroke-width="8"/>'
            f'<ellipse cx="{-w * .42:.0f}" cy="{-w * .7:.0f}" rx="{w * .22:.0f}" ry="{w * .16:.0f}" fill="#6e4526"/><ellipse cx="{w * .42:.0f}" cy="{-w * .7:.0f}" rx="{w * .22:.0f}" ry="{w * .16:.0f}" fill="#6e4526"/></g>')


def big_eye(pid):
    """A camel's eye close up: two rows of long lashes."""
    rows = ""
    for row, (ry, ln, col) in enumerate(((150, 120, INK), (120, 90, "#6b3f1d"))):
        for k in range(9):
            a = math.radians(-160 + k * 17.5 + row * 6); x0, y0 = 250 * math.cos(a), ry * math.sin(a); x1, y1 = (250 + ln) * math.cos(a - .12), (ry + ln) * math.sin(a - .12)
            rows += f'<path class="{pid}-row{row}" d="M{x0:.0f} {y0:.0f} Q{(x0 + x1) / 2:.0f} {(y0 + y1) / 2 - 30:.0f} {x1:.0f} {y1:.0f}" stroke="{col}" stroke-width="{16 - row * 4}" stroke-linecap="round" fill="none"/>'
    return (f'<g id="{pid}"><ellipse cx="0" cy="0" rx="330" ry="230" fill="#dba56a"/><ellipse cx="0" cy="0" rx="250" ry="150" fill="#fff"/><circle cx="20" cy="6" r="118" fill="#5b3413"/><circle cx="20" cy="6" r="66" fill="#1a1a2e"/>'
            f'<circle cx="66" cy="-40" r="30" fill="#fff"/><circle cx="-14" cy="50" r="14" fill="#fff" opacity=".8"/>'
            f'<g id="{pid}-lid" opacity="0"><ellipse cx="0" cy="0" rx="256" ry="156" fill="#dba56a"/><path d="M-250 20 Q0 120 250 20" stroke="#402010" stroke-width="14" fill="none" stroke-linecap="round"/></g>{rows}</g>')


def big_nose(pid):
    """A camel's nose close up: the nostrils can shut ("camels can close their nostrils to keep sand out of their nose")."""
    return (f'<g id="{pid}"><ellipse cx="0" cy="0" rx="330" ry="250" fill="#f0c690"/><path d="M-10 60 q10 60 0 130 M-150 150 q140 80 290 0" stroke="#7d4a22" stroke-width="14" fill="none" stroke-linecap="round"/>'
            f'<g id="{pid}-nl"><ellipse cx="-110" cy="-30" rx="64" ry="40" fill="#5e3a1c" transform="rotate(24 -110 -30)"/></g>'
            f'<g id="{pid}-nr"><ellipse cx="110" cy="-30" rx="64" ry="40" fill="#5e3a1c" transform="rotate(-24 110 -30)"/></g></g>')


def sand_puffs(pid, n=26, seed=1):
    r = random.Random(seed)
    return f'<g id="{pid}">' + "".join(f'<circle class="{pid}-g" cx="{r.uniform(-900, 900):.0f}" cy="{r.uniform(-420, 420):.0f}" r="{r.uniform(6, 16):.0f}" fill="#f6dba4" opacity="{r.uniform(.5, .9):.2f}"/>' for _ in range(n)) + '</g>'


def snow(pid, n=40, seed=2):
    r = random.Random(seed)
    return f'<g id="{pid}">' + "".join(f'<circle class="{pid}-f" cx="{r.uniform(-400, 2300):.0f}" cy="{r.uniform(-900, 900):.0f}" r="{r.uniform(5, 11):.0f}" fill="#fff" opacity="{r.uniform(.6, 1):.2f}"/>' for _ in range(n)) + '</g>'


def note(pid, col="#ff7aa2"):
    return f'<g id="{pid}"><ellipse cx="-14" cy="0" rx="22" ry="16" fill="{col}" transform="rotate(-20 -14 0)"/><path d="M6 -4 V-96 q36 6 44 40" stroke="{col}" stroke-width="10" fill="none" stroke-linecap="round"/></g>'


def scale_prop(pid):
    return (f'<g id="{pid}"><rect x="-190" y="-40" width="380" height="40" rx="14" fill="#8aa0c8"/><rect x="-150" y="-70" width="300" height="34" rx="12" fill="#b7c6e4"/>'
            f'<circle cx="0" cy="-210" r="120" fill="#fff" stroke="#8aa0c8" stroke-width="16"/><path id="{pid}-hand" d="M0 -210 L0 -300" stroke="#e63946" stroke-width="12" stroke-linecap="round"/><circle cx="0" cy="-210" r="14" fill="#402010"/></g>')


def clock(pid):
    return (f'<g id="{pid}"><circle cx="0" cy="0" r="150" fill="#fff" stroke="{MILO_BLUE}" stroke-width="20"/>' + "".join(f'<circle cx="{118 * math.cos(math.radians(a)):.0f}" cy="{118 * math.sin(math.radians(a)):.0f}" r="9" fill="{MILO_DARK}"/>' for a in range(0, 360, 30))
            + f'<path d="M0 0 V-78" stroke="{INK}" stroke-width="14" stroke-linecap="round"/><path id="{pid}-min" d="M0 0 V-112" stroke="#e63946" stroke-width="10" stroke-linecap="round"/>'
            f'<path d="M0 0 L0 -112 A112 112 0 0 1 0 112Z" fill="{SUN}" opacity=".0" id="{pid}-half"/><circle cx="0" cy="0" r="14" fill="{INK}"/></g>')


def tick(pid):
    return f'<g id="{pid}"><circle cx="0" cy="0" r="74" fill="#35c46a" stroke="#fff" stroke-width="12"/><path d="M-34 2 L-8 30 L38 -26" stroke="#fff" stroke-width="20" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>'


def cross(pid):
    return f'<g id="{pid}"><path d="M-90 -90 L90 90 M90 -90 L-90 90" stroke="#e63946" stroke-width="40" stroke-linecap="round"/></g>'


def week(pid):
    return f'<g id="{pid}">' + "".join(f'<g class="{pid}-d"><rect x="{-518 + k * 150}" y="-70" width="130" height="140" rx="24" fill="#fff" stroke="{MILO_BLUE}" stroke-width="10"/><circle cx="{-453 + k * 150}" cy="0" r="34" fill="{SUN}"/></g>' for k in range(7)) + '</g>'


def arrow(pid, x1, y1, x2, y2, col=None):
    col = col or SUN; a = math.atan2(y2 - y1, x2 - x1); hx, hy = x2 - 46 * math.cos(a), y2 - 46 * math.sin(a)
    return (f'<g id="{pid}"><path d="M{x1} {y1} L{hx:.0f} {hy:.0f}" stroke="{INK}" stroke-width="34" stroke-linecap="round"/><path d="M{x1} {y1} L{hx:.0f} {hy:.0f}" stroke="{col}" stroke-width="18" stroke-linecap="round"/>'
            f'<path d="M{x2} {y2} L{hx - 40 * math.sin(a):.0f} {hy + 40 * math.cos(a):.0f} L{hx + 40 * math.sin(a):.0f} {hy - 40 * math.cos(a):.0f}Z" fill="{col}" stroke="{INK}" stroke-width="12" stroke-linejoin="round"/></g>')
