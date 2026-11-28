"""Art for gc_ep04 "How Does Your Heart Work?" (Gizmo Explains, Nov 28 2026, catch-up run A): the props of the heart (a friendly heart that squeezes,
a child's body outline with the heart in the chest a little to the left of the middle and the blood's way out and back, a fist the size of the heart,
the lungs where the blood picks up oxygen, the heart's four rooms with the little doors (valves) that close, a heartbeat line slow and fast, a bed
with a sleeping child, a moon, a ball). No new place. Registered nothing: props only, drawn around (0, 0); nothing that exists changes."""
import art
from art import INK, SUN
from art_gizmo import NAVY, ACC, SILVER, STEEL, B1, B2

RED = "#e8475a"; REDD = "#a8283a"; REDL = "#ff8a96"; BLUE = "#4f86e8"; BLUED = "#2a55a8"; PINK = "#ffb3c1"; PINKD = "#d9707f"
SKIN = "#d39a6a"; SKIND = "#8a5634"; KID = "#ffe2c4"; SHIRT = "#ffd34d"
HEART = "M0 130 C-120 50 -200 -20 -190 -95 C-180 -165 -90 -190 -30 -140 C-12 -125 -4 -112 0 -100 C4 -112 12 -125 30 -140 C90 -190 180 -165 190 -95 C200 -20 120 50 0 130Z"


def heart(pid):
    """A friendly heart (red, two tubes on top: the blood vessels), -sq is the part that squeezes (scale tween around its middle), -glow a soft
    light around it (opacity 0)."""
    return (f'<g id="{pid}"><g id="{pid}-glow" opacity="0"><path d="{HEART}" fill="{REDL}" opacity=".35" transform="scale(1.3)"/></g>'
            f'<g id="{pid}-sq"><path d="M-40 -130 C-50 -200 -10 -230 30 -232" stroke="{NAVY}" stroke-width="58" fill="none" stroke-linecap="round"/>'
            f'<path d="M-40 -130 C-50 -200 -10 -230 30 -232" stroke="{BLUE}" stroke-width="38" fill="none" stroke-linecap="round"/>'
            f'<path d="M40 -130 C40 -210 100 -240 150 -220" stroke="{NAVY}" stroke-width="64" fill="none" stroke-linecap="round"/>'
            f'<path d="M40 -130 C40 -210 100 -240 150 -220" stroke="{RED}" stroke-width="44" fill="none" stroke-linecap="round"/>'
            f'<path d="{HEART}" fill="{RED}" stroke="{NAVY}" stroke-width="12" stroke-linejoin="round"/>'
            f'<path d="M-140 -90 C-140 -130 -100 -150 -70 -130" stroke="#fff" stroke-width="18" fill="none" stroke-linecap="round" opacity=".7"/>'
            f'<circle cx="-62" cy="-20" r="13" fill="{INK}"/><circle cx="62" cy="-20" r="13" fill="{INK}"/>'
            f'<path d="M-40 28 Q0 62 40 28" stroke="{INK}" stroke-width="11" fill="none" stroke-linecap="round"/>'
            f'<ellipse cx="-104" cy="20" rx="20" ry="11" fill="{PINK}"/><ellipse cx="104" cy="20" rx="20" ry="11" fill="{PINK}"/></g></g>')


def small_heart(pid, col=RED):
    """A small plain heart (no face), -sq squeezes."""
    return f'<g id="{pid}"><g id="{pid}-sq"><path d="{HEART}" fill="{col}" stroke="{NAVY}" stroke-width="14" stroke-linejoin="round"/></g></g>'


# the way of the blood in the body outline (in the body's own units; the heart sits at HX, HY: a little to the left of the middle of the chest,
# that is to the RIGHT on screen, because the child faces us)
HX, HY = 34, -150
OUT = [(HX + 20, HY - 50, 60, -330), (60, -330, -40, -330), (HX - 10, HY + 40, 70, 160), (70, 160, 80, 380), (HX + 40, HY, 190, -60)]    # red: away from the heart
BACK = [(-80, 380, -70, 160), (-70, 160, HX - 30, HY + 50), (-190, -60, HX - 50, HY), (-40, -300, HX - 30, HY - 50)]                   # blue: back to the heart


def body(pid):
    """A child's body outline (front view, smiling, a yellow shirt), the heart in the chest a little to the left of the middle (-h, with -h-sq),
    the blood vessels as soft lines (red away from the heart -out, blue back to it -back, both opacity 0), arrows along them shown one after
    another (-o0.. red, -b0.. blue, opacity 0). Feet at y = 480, head top at y = -560."""
    vessel = lambda segs, col: "".join(f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{col}" stroke-width="16" stroke-linecap="round" opacity=".8"/>' for x1, y1, x2, y2 in segs)
    arrows = lambda segs, col, tag: "".join(f'<g id="{pid}-{tag}{k}" opacity="0"><g transform="translate({(x1 + x2) / 2:.0f} {(y1 + y2) / 2:.0f}) scale(.45) translate({-(x1 + x2) / 2:.0f} {-(y1 + y2) / 2:.0f})">'
                                            f'{art.arrow(pid + tag + str(k), x1, y1, x2, y2, col)}</g></g>' for k, (x1, y1, x2, y2) in enumerate(segs))
    return (f'<g id="{pid}">'
            # legs, arms, body, head
            f'<rect x="-120" y="140" width="100" height="330" rx="46" fill="#5b7fd6" stroke="{NAVY}" stroke-width="12"/><rect x="20" y="140" width="100" height="330" rx="46" fill="#5b7fd6" stroke="{NAVY}" stroke-width="12"/>'
            f'<ellipse cx="-74" cy="476" rx="70" ry="30" fill="{NAVY}"/><ellipse cx="74" cy="476" rx="70" ry="30" fill="{NAVY}"/>'
            f'<path d="M-190 -250 C-260 -180 -290 -40 -280 80" stroke="{NAVY}" stroke-width="76" fill="none" stroke-linecap="round"/><path d="M-190 -250 C-260 -180 -290 -40 -280 80" stroke="{KID}" stroke-width="54" fill="none" stroke-linecap="round"/>'
            f'<path d="M190 -250 C260 -180 290 -40 280 80" stroke="{NAVY}" stroke-width="76" fill="none" stroke-linecap="round"/><path d="M190 -250 C260 -180 290 -40 280 80" stroke="{KID}" stroke-width="54" fill="none" stroke-linecap="round"/>'
            f'<path d="M-200 -270 Q0 -310 200 -270 L180 180 Q0 210 -180 180Z" fill="{SHIRT}" stroke="{NAVY}" stroke-width="12" stroke-linejoin="round"/>'
            f'<rect x="-36" y="-340" width="72" height="70" fill="{KID}" stroke="{NAVY}" stroke-width="10"/>'
            f'<circle cx="0" cy="-440" r="130" fill="{KID}" stroke="{NAVY}" stroke-width="12"/>'
            f'<path d="M-128 -470 C-120 -580 120 -590 128 -470 C90 -520 -60 -530 -128 -470Z" fill="#6b4226" stroke="{NAVY}" stroke-width="10"/>'
            f'<circle cx="-46" cy="-440" r="15" fill="{INK}"/><circle cx="46" cy="-440" r="15" fill="{INK}"/><path d="M-44 -390 Q0 -356 44 -390" stroke="{INK}" stroke-width="11" fill="none" stroke-linecap="round"/>'
            f'<ellipse cx="-86" cy="-400" rx="20" ry="11" fill="{PINK}"/><ellipse cx="86" cy="-400" rx="20" ry="11" fill="{PINK}"/>'
            # the blood's way and the heart
            f'<g id="{pid}-out" opacity="0">{vessel(OUT, RED)}</g><g id="{pid}-back" opacity="0">{vessel(BACK, BLUE)}</g>'
            f'{arrows(OUT, RED, "o")}{arrows(BACK, BLUE, "b")}'
            f'<g id="{pid}-h" transform="translate({HX} {HY})"><circle r="92" fill="#fff" opacity=".55"/><g transform="scale(.36)">{small_heart(pid + "-h")}</g></g>'
            f'</g>')


def fist(pid):
    """A child's fist seen from the front: four bent fingers in a row, the thumb across them, the wrist and a yellow sleeve below."""
    fingers = "".join(f'<rect x="{x}" y="-120" width="78" height="150" rx="36" fill="{SKIN}" stroke="{SKIND}" stroke-width="10"/>' for x in (-160, -82, -4, 74))
    return (f'<g id="{pid}"><rect x="-110" y="20" width="200" height="190" rx="40" fill="{SKIN}" stroke="{SKIND}" stroke-width="10"/>'
            f'<rect x="-170" y="-60" width="330" height="170" rx="60" fill="{SKIN}" stroke="{SKIND}" stroke-width="12"/>{fingers}'
            f'<path d="M-170 40 C-110 0 -10 0 60 30 C86 42 80 80 50 78 C-20 70 -100 76 -160 96Z" fill="#e0ab7d" stroke="{SKIND}" stroke-width="10" stroke-linejoin="round"/>'
            f'<rect x="-135" y="190" width="250" height="90" rx="22" fill="{SHIRT}" stroke="{NAVY}" stroke-width="10"/></g>')


def lungs(pid):
    """The two lungs (pink) with the heart between them; the blood in the lungs as dots: -blue (opacity 1) turns into -red (opacity 0) when it
    picks up oxygen; -o2 are little bubbles of air coming in (opacity 0)."""
    lobe = lambda s: (f'<path d="M{40 * s} -230 C{150 * s} -260 {260 * s} -120 {260 * s} 60 C{260 * s} 200 {200 * s} 250 {120 * s} 240 C{60 * s} 232 {40 * s} 200 {40 * s} 140Z" '
                      f'fill="{PINK}" stroke="{NAVY}" stroke-width="12" stroke-linejoin="round"/>')
    dots = lambda col, tag: f'<g id="{pid}-{tag}" opacity="{1 if tag == "blue" else 0}">' + "".join(f'<circle cx="{x}" cy="{y}" r="17" fill="{col}" stroke="{NAVY}" stroke-width="4"/>' for x, y in ((-200, -40), (-150, 60), (-210, 150), (-120, -130), (200, -40), (150, 60), (210, 150), (120, -130))) + '</g>'
    o2 = f'<g id="{pid}-o2" opacity="0">' + "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff" stroke="{BLUED}" stroke-width="5" opacity=".9"/>' for x, y, r in ((-150, -10, 22), (-190, 100, 16), (150, -10, 22), (190, 100, 16), (-110, 160, 14), (110, 160, 14))) + '</g>'
    return (f'<g id="{pid}"><path d="M0 -340 V-240 M0 -250 C-20 -230 -40 -230 -60 -220 M0 -250 C20 -230 40 -230 60 -220" stroke="{NAVY}" stroke-width="40" fill="none" stroke-linecap="round"/>'
            f'<path d="M0 -340 V-240" stroke="#f3c4cc" stroke-width="22" stroke-linecap="round"/>'
            f'{lobe(-1)}{lobe(1)}{dots(BLUE, "blue")}{dots(RED, "red")}{o2}'
            f'<g transform="translate(0 110) scale(.42)">{small_heart(pid + "h")}</g></g>')


def rooms(pid):
    """The heart's four rooms (chambers): a big heart cut open, two rooms on top and two on the bottom (-c0 top left, -c1 top right, -c2 bottom left,
    -c3 bottom right: a light in each, opacity 0), and the little doors between top and bottom rooms (-d0, -e0 left, -d1, -e1 right: open flaps; DOORS in the episode closes them)."""
    shape = f'<path d="{HEART}" transform="scale(1.6)"/>'
    lit = lambda k, x, y, w, h: f'<g id="{pid}-c{k}" opacity="0"><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#fff36b" opacity=".55" clip-path="url(#{pid}-cp)"/></g>'
    def flap(fid, hx, ex):      # a little door: a white bar from its hinge (hx, -20) down to (ex, 30), open; closed it lies flat (see the episode's DOORS)
        return (f'<g id="{pid}-{fid}"><path d="M{hx} -20 L{ex} 30" stroke="{NAVY}" stroke-width="30" stroke-linecap="round"/>'
                f'<path d="M{hx} -20 L{ex} 30" stroke="#fff" stroke-width="16" stroke-linecap="round"/><circle cx="{hx}" cy="-20" r="13" fill="{NAVY}"/></g>')
    return (f'<g id="{pid}"><defs><clipPath id="{pid}-cp">{shape}</clipPath></defs>'
            f'<path d="{HEART}" transform="scale(1.6)" fill="{RED}" stroke="{NAVY}" stroke-width="10" stroke-linejoin="round"/>'
            f'<g clip-path="url(#{pid}-cp)"><rect x="-320" y="-300" width="320" height="280" fill="{REDL}"/><rect x="0" y="-300" width="320" height="280" fill="{REDL}"/>'
            f'<rect x="-320" y="-20" width="320" height="260" fill="{RED}"/><rect x="0" y="-20" width="320" height="260" fill="#f05a6c"/></g>'
            + lit(0, -320, -300, 320, 280) + lit(1, 0, -300, 320, 280) + lit(2, -320, -20, 320, 260) + lit(3, 0, -20, 320, 260)
            + f'<g clip-path="url(#{pid}-cp)"><path d="M0 -170 V230" stroke="{NAVY}" stroke-width="22"/><path d="M-320 -20 H-225 M-75 -20 H75 M225 -20 H320" stroke="{NAVY}" stroke-width="18"/></g>'
            + flap("d0", -225, -160) + flap("e0", -75, -140) + flap("d1", 75, 140) + flap("e1", 225, 160)
            + f'<path d="{HEART}" transform="scale(1.6)" fill="none" stroke="{NAVY}" stroke-width="14" stroke-linejoin="round"/></g>')


def beat_line(pid, fast=False):
    """A heartbeat line on a little screen: two spikes per beat (lub, dub); fast = the beats closer together. -dot runs along it (move x)."""
    step = 200 if fast else 400
    d = "M-400 0"
    x = -400
    while x + step <= 400:
        d += f" L{x + step * .35:.0f} 0 L{x + step * .42:.0f} -110 L{x + step * .5:.0f} 60 L{x + step * .56:.0f} 0 L{x + step * .64:.0f} -50 L{x + step * .7:.0f} 0 L{x + step:.0f} 0"
        x += step
    return (f'<g id="{pid}"><rect x="-460" y="-170" width="920" height="300" rx="36" fill="#13204a" stroke="{NAVY}" stroke-width="12"/>'
            f'<path d="{d}" stroke="{ACC}" stroke-width="14" fill="none" stroke-linejoin="round" stroke-linecap="round"/>'
            f'<g id="{pid}-dot"><circle cx="-400" cy="0" r="20" fill="#fff36b"/></g></g>')


def bed(pid):
    """A child asleep in bed under a blue blanket (eyes closed, a calm smile), a small heart over the chest that keeps beating (-h, with -h-sq)."""
    return (f'<g id="{pid}"><rect x="-430" y="40" width="860" height="70" rx="20" fill="#b07a48" stroke="{NAVY}" stroke-width="10"/>'
            f'<rect x="-440" y="-160" width="60" height="320" rx="20" fill="#c98a4a" stroke="{NAVY}" stroke-width="10"/><rect x="380" y="-60" width="60" height="220" rx="20" fill="#c98a4a" stroke="{NAVY}" stroke-width="10"/>'
            f'<rect x="-380" y="-80" width="200" height="110" rx="40" fill="#fff" stroke="{NAVY}" stroke-width="10"/>'
            f'<circle cx="-270" cy="-90" r="80" fill="{KID}" stroke="{NAVY}" stroke-width="10"/><path d="M-348 -110 C-340 -190 -200 -190 -192 -110 C-230 -150 -310 -150 -348 -110Z" fill="#6b4226" stroke="{NAVY}" stroke-width="8"/>'
            f'<path d="M-300 -86 q12 10 24 0 M-246 -86 q12 10 24 0" stroke="{INK}" stroke-width="7" fill="none" stroke-linecap="round"/><path d="M-286 -56 q16 10 32 0" stroke="{INK}" stroke-width="7" fill="none" stroke-linecap="round"/>'
            f'<path d="M-200 -70 C-60 -110 200 -110 380 -60 L380 60 L-200 60Z" fill="{BLUE}" stroke="{NAVY}" stroke-width="10" stroke-linejoin="round"/>'
            f'<path d="M-160 -40 C0 -70 200 -70 360 -30" stroke="#8fb4ff" stroke-width="10" fill="none" stroke-linecap="round"/>'
            f'<g id="{pid}-h" transform="translate(-60 -190)"><g transform="scale(.3)">{small_heart(pid + "-h")}</g></g></g>')


def moon(pid):
    """A calm crescent moon with two stars."""
    return (f'<g id="{pid}"><path d="M40 -150 A150 150 0 1 0 40 150 A120 120 0 1 1 40 -150Z" fill="#fff3a8" stroke="#e8c84a" stroke-width="10"/>'
            + "".join(f'<path d="M{x} {y - 30} L{x + 8} {y - 8} L{x + 30} {y} L{x + 8} {y + 8} L{x} {y + 30} L{x - 8} {y + 8} L{x - 30} {y} L{x - 8} {y - 8}Z" fill="#fff3a8"/>' for x, y in ((200, -120), (240, 60)))
            + '</g>')


def night(pid):
    """The lab window at night (covers the window of gwindow, centre (960, 350)): a dark blue sky, the moon and stars, dark hills."""
    stars = "".join(f'<circle cx="{x}" cy="{y}" r="7" fill="#fff" opacity=".9"/>' for x, y in ((-460, -300), (-300, -180), (-120, -320), (60, -260), (-400, 40), (-200, -60), (120, -120), (480, 60)))
    return (f'<g id="{pid}"><rect x="-580" y="-410" width="1160" height="780" fill="#1a2a66"/>{stars}'
            f'<g transform="translate(330 -200) scale(.7)">{moon(pid + "m")}</g>'
            f'<path d="M-580 210 C-300 150 0 190 300 160 S520 170 580 180 V370 H-580Z" fill="#20406a"/>'
            f'<rect x="-600" y="-430" width="1200" height="820" fill="none" stroke="{SILVER}" stroke-width="40"/><path d="M0 -430 V390 M-600 -20 H600" stroke="{SILVER}" stroke-width="24"/></g>')


def ball(pid):
    """A bouncy play ball."""
    return (f'<g id="{pid}"><circle r="90" fill="#ff7a59" stroke="{NAVY}" stroke-width="10"/><path d="M-90 0 Q0 -50 90 0" stroke="#fff" stroke-width="14" fill="none"/>'
            f'<path d="M-60 66 Q0 20 60 66" stroke="#fff" stroke-width="12" fill="none"/><ellipse cx="-34" cy="-40" rx="18" ry="10" fill="#fff" opacity=".7"/></g>')
