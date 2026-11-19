"""Art for zc_ep09 "What Do Camels Eat in the Desert?" (Nov 19 2026): the boards of a camel's lunch.
A camel's face from the front with the split top lip (each half -lipL / -lipR moves on its own), the inside of the mouth with its hard
little bumps (cone shapes that point down the throat), a fingertip with its nail, food pictures (a grass tuft, a leaf, a twig, a thorny
branch, a salty bush), a leafy bush whose leaves can be eaten one by one, a round loop arrow (chew, swallow, chew again) and a food icon frame.
Same hand as art.py / art2.py: flat fills, one warm dark outline. Nothing here changes an existing character, prop or place.
Read only: art.CAMEL, art.eye, art.INK, art._thorn."""
import math
import art
from art import INK, eye

C = art.CAMEL


def muzzle(pid):
    """A camel's face from the front, big (the lips board). Anchored at the middle of the face; about 760 wide, 900 tall.
    Parts: -lipL, -lipR (the two halves of the split top lip; rotate round their top corner), -lipD (the bottom lip), -nose (both nostrils), -eyeL, -eyeR."""
    ln = C["line"]
    head = (f'<path d="M-250 -420 C-260 -560 -120 -640 0 -640 C120 -640 260 -560 250 -420 C240 -260 230 -60 200 80 L-200 80 C-230 -60 -240 -260 -250 -420Z" '
            f'fill="{C["fill"]}" stroke="{ln}" stroke-width="14" stroke-linejoin="round"/>')
    ears = (f'<path d="M-210 -540 q-90 -60 -60 -150 q70 30 110 110Z" fill="{C["fill"]}" stroke="{ln}" stroke-width="12" stroke-linejoin="round"/>'
            f'<path d="M210 -540 q90 -60 60 -150 q-70 30 -110 110Z" fill="{C["fill"]}" stroke="{ln}" stroke-width="12" stroke-linejoin="round"/>')
    tuft = f'<path d="M-90 -630 q20 -50 50 -16 q24 -44 50 -4 q28 -40 50 10" stroke="{C["hair"]}" stroke-width="18" fill="none" stroke-linecap="round"/>'
    eyes = (f'<g id="{pid}-eyeL">' + eye(f"{pid}-eL", -118, -400, 56, lashes=1, lid=C["fill"]) + '</g>'
            f'<g id="{pid}-eyeR">' + eye(f"{pid}-eR", 118, -400, 56, lashes=1, lid=C["fill"]) + '</g>')
    snout = (f'<path d="M-230 -120 C-240 -230 -130 -270 0 -270 C130 -270 240 -230 230 -120 C230 0 180 90 0 100 C-180 90 -230 0 -230 -120Z" '
             f'fill="{C["light"]}" stroke="{ln}" stroke-width="12"/>')
    nose = (f'<g id="{pid}-nose"><path d="M-110 -200 q30 -24 66 -10" stroke="{ln}" stroke-width="16" fill="none" stroke-linecap="round"/>'
            f'<path d="M110 -200 q-30 -24 -66 -10" stroke="{ln}" stroke-width="16" fill="none" stroke-linecap="round"/></g>')
    cheeks = f'<ellipse cx="-190" cy="-250" rx="40" ry="22" fill="#ff8fb1" opacity=".5"/><ellipse cx="190" cy="-250" rx="40" ry="22" fill="#ff8fb1" opacity=".5"/>'
    # the split top lip: two round halves meeting at a notch in the middle
    lipL = (f'<g id="{pid}-lipL"><path d="M-6 -140 C-40 -150 -170 -140 -190 -60 C-200 0 -120 30 -60 20 C-20 14 -6 -20 -6 -60Z" '
            f'fill="{C["shade"]}" stroke="{ln}" stroke-width="12" stroke-linejoin="round"/>'
            f'<path d="M-150 -70 q40 -40 110 -40" stroke="{C["light"]}" stroke-width="10" fill="none" stroke-linecap="round" opacity=".8"/></g>')
    lipR = (f'<g id="{pid}-lipR"><path d="M6 -140 C40 -150 170 -140 190 -60 C200 0 120 30 60 20 C20 14 6 -20 6 -60Z" '
            f'fill="{C["shade"]}" stroke="{ln}" stroke-width="12" stroke-linejoin="round"/>'
            f'<path d="M150 -70 q-40 -40 -110 -40" stroke="{C["light"]}" stroke-width="10" fill="none" stroke-linecap="round" opacity=".8"/></g>')
    lipD = (f'<g id="{pid}-lipD"><path d="M-150 30 C-120 110 120 110 150 30 C110 60 -110 60 -150 30Z" fill="{C["shade"]}" stroke="{ln}" stroke-width="12" stroke-linejoin="round"/></g>')
    return f'<g id="{pid}">{ears}{head}{tuft}{eyes}{cheeks}{snout}{nose}{lipD}{lipL}{lipR}</g>'


def inside_mouth(pid):
    """The inside of a camel's mouth (a friendly diagram): a pink mouth, a dark round throat at the bottom, rows of little hard cone bumps (.{pid}-cone)
    that all point down to the throat, and an arrow -arrow (hidden until shown by the episode) running down into the throat. Anchored at the middle; about 900 x 760."""
    ln = INK
    rim = (f'<path d="M-500 -330 C-500 -450 500 -450 500 -330 L440 280 C400 420 -400 420 -440 280Z" fill="{C["light"]}" stroke="{C["line"]}" stroke-width="14" stroke-linejoin="round"/>')      # the camel's lips around the open mouth
    mouth = (f'<path d="M-440 -300 C-440 -380 440 -380 440 -300 L380 260 C340 360 -340 360 -380 260Z" fill="#f28aa0" stroke="{ln}" stroke-width="14" stroke-linejoin="round"/>'
             f'<path d="M-400 -300 C-400 -350 400 -350 400 -300 L400 -250 C200 -290 -200 -290 -400 -250Z" fill="#fff4ea" stroke="{ln}" stroke-width="10"/>'      # top teeth row
             f'<ellipse cx="0" cy="250" rx="110" ry="70" fill="#7a2a3e" stroke="{ln}" stroke-width="10"/>')                                                          # the throat
    cones = ""
    for row, (y, n, w) in enumerate(((-170, 7, 330), (-50, 6, 300), (70, 5, 260), (170, 3, 180))):
        for k in range(n):
            x = -w + 2 * w * k / max(1, n - 1)
            if row == 3 and k == 1: continue          # the throat sits there
            a = math.degrees(math.atan2(x, 250 - y))        # point at the throat (a path pointing down, turned clockwise by a)
            cones += (f'<g transform="translate({x:.0f} {y}) rotate({a:.0f})"><path class="{pid}-cone" d="M-14 -22 L0 40 L14 -22Z" fill="#ffd2dc" stroke="#c4566e" stroke-width="6" stroke-linejoin="round"/></g>')
    arrow = (f'<g id="{pid}-arrow"><path d="M0 -200 V150" stroke="#2f80ed" stroke-width="26" stroke-linecap="round" stroke-dasharray="40 30"/>'
             f'<path d="M-50 120 L0 196 L50 120Z" fill="#2f80ed"/></g>')
    return f'<g id="{pid}">{rim}{mouth}{cones}{arrow}</g>'


def fingertip(pid):
    """A child's fingertip with its nail, pointing up (the 'hard like your fingernails' picture). Anchored at the bottom middle; about 220 x 420."""
    return (f'<g id="{pid}"><path d="M-90 0 L-90 -300 C-90 -400 90 -400 90 -300 L90 0Z" fill="#f6c9a0" stroke="{INK}" stroke-width="12" stroke-linejoin="round"/>'
            f'<path d="M-58 -300 C-58 -360 58 -360 58 -300 L58 -230 C20 -216 -20 -216 -58 -230Z" fill="#fff0f2" stroke="#d98a9a" stroke-width="9"/>'
            f'<path d="M-36 -320 q20 -18 40 -12" stroke="#fff" stroke-width="10" fill="none" stroke-linecap="round"/>'
            f'<path d="M-60 -120 q60 20 120 0 M-60 -80 q60 18 120 0" stroke="#d99a72" stroke-width="7" fill="none" stroke-linecap="round"/></g>')


def grass(pid):
    """A tuft of desert grass. Bottom middle on (0, 0); about 300 x 280."""
    blades = "".join(f'<path d="M{x0} 0 Q{(x0 + x1) / 2 + b} {-h * .6:.0f} {x1} {-h}" stroke="{col}" stroke-width="18" fill="none" stroke-linecap="round"/>'
                     for x0, x1, h, b, col in ((-50, -140, 200, -20, "#8fb34a"), (-28, -70, 260, -10, "#a9c95a"), (-6, -8, 290, 0, "#8fb34a"),
                                               (16, 60, 260, 10, "#c2d46a"), (40, 140, 210, 20, "#8fb34a")))
    return f'<g id="{pid}">{blades}<ellipse cx="0" cy="-4" rx="80" ry="18" fill="#6f8f3a"/></g>'


def leaf(pid, col="#7cc35a"):
    """One small green leaf. Anchored at its middle; about 260 x 150."""
    return (f'<g id="{pid}"><path d="M-130 0 C-60 -90 70 -90 130 0 C70 90 -60 90 -130 0Z" fill="{col}" stroke="#3a7a3a" stroke-width="10" stroke-linejoin="round"/>'
            f'<path d="M-130 0 H120 M-40 0 L0 -40 M30 0 L70 -36 M-40 0 L0 40 M30 0 L70 36" stroke="#3a7a3a" stroke-width="7" fill="none" stroke-linecap="round"/></g>')


def twig(pid):
    """A small brown twig with two buds. Anchored at its middle; about 320 x 160."""
    return (f'<g id="{pid}"><path d="M-160 50 L150 -40 M10 10 L90 -70 M-60 30 L-110 -40" stroke="#8a5a2e" stroke-width="22" fill="none" stroke-linecap="round"/>'
            f'<ellipse cx="96" cy="-76" rx="20" ry="14" fill="#9bc45a"/><ellipse cx="-114" cy="-46" rx="20" ry="14" fill="#9bc45a"/><ellipse cx="156" cy="-42" rx="20" ry="14" fill="#9bc45a"/></g>')


def thorn_branch(pid):
    """A thorny branch, big (the thorns close-up): a brown stem with long pale thorns and a few small leaves. Anchored at its middle; about 760 x 340."""
    th = ""
    for k, x in enumerate(range(-300, 320, 90)):
        up = k % 2 == 0; y = -0.12 * x
        th += f'<path d="M{x} {y:.0f} L{x + 34} {y + (-96 if up else 96):.0f} L{x + 22} {y:.0f}Z" fill="#f4ead2" stroke="#8a6a3a" stroke-width="6" stroke-linejoin="round"/>'
    lv = "".join(f'<ellipse cx="{x}" cy="{y}" rx="34" ry="17" fill="#9bb24a" stroke="#55682a" stroke-width="6" transform="rotate({r} {x} {y})"/>'
                 for x, y, r in ((-240, 60, 30), (-60, -40, -30), (120, 10, 30), (300, -80, -30)))
    return (f'<g id="{pid}"><path d="M-370 44 L370 -44" stroke="#7a5230" stroke-width="30" stroke-linecap="round"/>{th}{lv}</g>')


def saltbush(pid):
    """A salty desert bush (saltbush): a round silvery grey-green bush with little white salt sparkles (.{pid}-salt). Bottom middle on (0, 0); about 520 x 340."""
    blobs = "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{col}" stroke="#5e7a64" stroke-width="8"/>'
                    for x, y, r, col in ((-160, -110, 110, "#a9c4a8"), (160, -110, 110, "#a9c4a8"), (-70, -200, 120, "#b9d2b6"), (90, -210, 120, "#b9d2b6"), (0, -120, 140, "#c4dbc0")))
    salt = "".join(f'<g transform="translate({x} {y})"><path class="{pid}-salt" d="M0 -14 L4 -4 L14 0 L4 4 L0 14 L-4 4 L-14 0 L-4 -4Z" fill="#fff"/></g>'
                   for x, y in ((-170, -150), (-60, -260), (70, -270), (180, -150), (0, -150), (-100, -90), (110, -80), (30, -210)))
    return f'<g id="{pid}"><rect x="-14" y="-40" width="28" height="40" fill="#7a5230"/>{blobs}{salt}</g>'


def leafy_bush(pid, n=7):
    """A small desert shrub with n leaves (-l0 ... -l{n-1}) that can be eaten one by one. Bottom middle on (0, 0); about 420 x 360."""
    stems = "".join(f'<path d="M0 0 Q{40 * math.cos(a):.0f} {-90:.0f} {160 * math.cos(a):.0f} {-300 * abs(math.sin(a)) - 30:.0f}" stroke="#7a5a30" stroke-width="14" fill="none" stroke-linecap="round"/>'
                    for a in (-2.7, -2.2, -1.57, -0.94, -0.44))
    pts = [(-150, -100), (-120, -230), (-30, -300), (40, -250), (120, -300), (160, -150), (60, -150), (-60, -170), (-180, -170)]
    lv = "".join(f'<ellipse id="{pid}-l{k}" cx="{x}" cy="{y}" rx="46" ry="24" fill="#7cc35a" stroke="#3a7a3a" stroke-width="7" transform="rotate({(-30 if k % 2 else 30)} {x} {y})"/>'
                 for k, (x, y) in enumerate(pts[:n]))
    return f'<g id="{pid}">{stems}{lv}</g>'


def loop_arrow(pid):
    """A round arrow that goes down and comes back up (chew, swallow, chew again). Anchored at its middle; about 420 x 420."""
    return (f'<g id="{pid}"><path d="M-60 -170 A170 170 0 1 0 120 -120" stroke="#2f80ed" stroke-width="30" fill="none" stroke-linecap="round"/>'
            f'<path d="M80 -190 L170 -110 L66 -70Z" fill="#2f80ed"/></g>')


def food_icon(fn, s=1.0, dy=0, bg="#fff"):
    """A food picture in a round frame (the guesses board and the lunch board)."""
    def f(pid): return (f'<g id="{pid}"><circle r="120" fill="{bg}"/><g transform="translate(0 {dy}) scale({s})">{fn(pid + "i")}</g>'
                        f'<circle r="120" fill="none" stroke="{INK}" stroke-width="10"/></g>')
    return f
