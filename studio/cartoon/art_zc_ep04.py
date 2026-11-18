"""Art for zc_ep04 "Why Do Monkeys Have Long Tails?" (Nov 18 2026): the pictures of the tail lesson.
Mango hanging by her tail with a fruit in each hand (a new kind, "monkey_hangfruit": the same hanging drawing as art2.monkey(hang=True), a fruit drawn
inside each hand group so it moves with the hand), a branch for the picture boards, the tail stretched out next to her body, number badges,
a toy ball, a scarf, Mango's hand with four long fingers, the tip of the tail with its little lines (three monkeys, three patterns), a child's
fingertip, a friendly round spider, and a baby's tiny tail wrapped round its mama's tail.
Same hand as art.py / art2.py: flat fills, one warm dark outline. Nothing here changes an existing character, prop or place."""
import art, art2, kit
from art import INK, SUN

MON = art2.MON
FONT = 'font-family="Baloo, sans-serif" font-weight="800"'


def _limb(d, w=30, c=MON):
    return f'<path d="{d}" stroke="{c["line"]}" stroke-width="{w + 16}" fill="none" stroke-linecap="round"/><path d="{d}" stroke="{c["fur"]}" stroke-width="{w}" fill="none" stroke-linecap="round"/>'


# ------------------------------------------------------------------ Mango hanging, a fruit in each hand
def monkey_hangfruit(pid):
    s = art2.monkey(pid, hang=True)
    hl = f'<circle cx="-118" cy="-62" r="22" fill="{MON["dark"]}" stroke="{MON["line"]}" stroke-width="7"/>'
    hr = f'<circle cx="118" cy="-62" r="22" fill="{MON["dark"]}" stroke="{MON["line"]}" stroke-width="7"/>'
    # the body group is turned upside down, so a fruit drawn inside it is turned back with rotate(180): it hangs the right way up
    fl = f'<g transform="translate(-118 -40) rotate(180) scale(.62)">{art2.fruit(pid + "-fl")}</g>'
    fr = f'<g transform="translate(118 -40) rotate(180) scale(.62)">{art2.fruit(pid + "-fr")}</g>'
    assert hl in s and hr in s
    return s.replace(hl, fl + hl, 1).replace(hr, fr + hr, 1)


art2.RIGS["monkey_hangfruit"] = dict(build=monkey_hangfruit, neck=None, tail=None, ear=None, legs=None, hip=0, jaw=("y", 12), eyes=["eyeL", "eyeR"], brows=["browL", "browR"])
kit.PT["monkey_hangfruit"] = kit.PT["monkey_hang"]
kit.BOX["monkey_hang"] = (-170, 170, -40)       # hanging: (0, 0) is the branch, she hangs below it (WV needs "up" only; the feet point is 560 below)
kit.BOX["monkey_hangfruit"] = kit.BOX["monkey_hang"]


# ------------------------------------------------------------------ boards
def branch(pid, w=1400):
    return (f'<g id="{pid}"><rect x="{-w / 2}" y="-40" width="{w}" height="62" rx="28" fill="#8a6238" stroke="{INK}" stroke-width="8"/>'
            f'<path d="M{-w / 2 + 80} -12 h160 M{-w / 4} 0 h120 M{w / 6} -14 h180" stroke="#6a4a26" stroke-width="7" stroke-linecap="round"/></g>')


def tail_straight(pid, h=560):
    """Mango's tail held out straight up, to measure it against her body: (0, 0) is its root, the curled tip at the top."""
    d = f"M0 0 C-24 {-h * .25:.0f} 24 {-h * .5:.0f} 0 {-h * .75:.0f} C-16 {-h * .9:.0f} 10 {-h - 30:.0f} 44 {-h - 10:.0f}"
    return f'<g id="{pid}">{_limb(d, 30)}</g>'


def level(pid, w=520, col="#e63946"):
    """A dashed line across the board: how tall something is."""
    return f'<g id="{pid}"><path d="M{-w / 2} 0 H{w / 2}" stroke="{col}" stroke-width="12" stroke-dasharray="30 20" stroke-linecap="round"/></g>'


def badge(n, col=SUN):
    def f(pid):
        return (f'<g id="{pid}"><circle r="56" fill="{col}" stroke="{INK}" stroke-width="10"/>'
                f'<text x="0" y="26" text-anchor="middle" {FONT} font-size="80" fill="{INK}">{n}</text></g>')
    return f


def ball(pid):
    """A toy ball."""
    return (f'<g id="{pid}"><circle r="110" fill="#ff7aa2" stroke="{INK}" stroke-width="10"/><path d="M-110 0 A110 40 0 0 0 110 0" fill="none" stroke="#fff" stroke-width="22"/>'
            f'<path d="M0 -110 A40 110 0 0 1 0 110" fill="none" stroke="{SUN}" stroke-width="22"/><circle r="110" fill="none" stroke="{INK}" stroke-width="10"/>'
            f'<ellipse cx="-44" cy="-56" rx="26" ry="16" fill="#fff" opacity=".6" transform="rotate(-30 -44 -56)"/></g>')


def scarf(pid):
    """A warm striped scarf."""
    band = "M-150 -40 C-60 -90 60 10 150 -40 L150 30 C60 80 -60 -20 -150 30Z"
    return (f'<g id="{pid}"><path d="{band}" fill="#2f80ed" stroke="{INK}" stroke-width="10" stroke-linejoin="round"/>'
            f'<path d="M-90 -58 L-90 28 M-20 -40 L-20 46 M50 -24 L50 62" stroke="#fff" stroke-width="16"/>'
            f'<path d="M100 -20 L120 120 L170 110 L150 -30Z" fill="#2f80ed" stroke="{INK}" stroke-width="10" stroke-linejoin="round"/>'
            f'<path d="M126 120 v26 M146 116 v26 M166 112 v26" stroke="#2f80ed" stroke-width="10" stroke-linecap="round"/></g>')


def hand_big(pid, c=MON):
    """Mango's hand, big: a palm and four long fingers that hook (Nat Geo: "Four long fingers on each hand help them grasp branches").
    -f is the fingers' group: scaleY on it from the knuckles (svgOrigin 0 -60) bends them into a hook."""
    fing = "".join(f'<path d="M{x} -60 C{x} -170 {x + 6} -230 {x + 40} -250" stroke="{c["line"]}" stroke-width="58" fill="none" stroke-linecap="round"/>'
                   f'<path d="M{x} -60 C{x} -170 {x + 6} -230 {x + 40} -250" stroke="{c["dark"]}" stroke-width="40" fill="none" stroke-linecap="round"/>' for x in (-66, -22, 22, 66))
    return (f'<g id="{pid}"><path d="M-30 260 L-40 60 L40 60 L30 260Z" fill="{c["fur"]}" stroke="{c["line"]}" stroke-width="10" stroke-linejoin="round"/>'
            f'<g id="{pid}-f">{fing}</g><rect x="-96" y="-80" width="192" height="170" rx="70" fill="{c["dark"]}" stroke="{c["line"]}" stroke-width="10"/>'
            f'<ellipse cx="0" cy="10" rx="54" ry="40" fill="{c["face"]}" opacity=".55"/></g>')


_PAT = [  # three different sets of little lines (each monkey's own, like fingerprints)
    lambda: "".join(f'<path d="M-70 {y} q70 -26 140 0" stroke="#c49a74" stroke-width="7" fill="none" stroke-linecap="round"/>' for y in (-50, -26, -2, 22, 46)),
    lambda: "".join(f'<path d="M-70 {y} q70 26 140 0" stroke="#c49a74" stroke-width="7" fill="none" stroke-linecap="round"/>' for y in (-56, -30, -4, 22)) +
    '<path d="M-60 48 q60 -20 120 0" stroke="#c49a74" stroke-width="7" fill="none" stroke-linecap="round"/>',
    lambda: "".join(f'<path d="M{-70 + k * 8} {y} l140 -30" stroke="#c49a74" stroke-width="7" fill="none" stroke-linecap="round"/>' for k, y in enumerate((-30, -4, 22, 48))) +
    '<ellipse cx="0" cy="-40" rx="40" ry="18" fill="none" stroke="#c49a74" stroke-width="7"/>']


def tail_tip(k=0, c=MON):
    """The end of the tail, big, the underside towards us: a bare pad with little lines (Wisconsin primate centre: "a patch of skin with distinct
    pattern of lines like a fingerprint"). k chooses the pattern (0 = Mango's). -pad is the pad (it can glow)."""
    def f(pid):
        d = "M-260 300 C-200 120 -140 -40 -40 -120 C40 -180 150 -160 170 -60 C190 30 120 100 40 70"
        return (f'<g id="{pid}">{_limb(d, 150, c)}'
                f'<g id="{pid}-pad" transform="translate(70 -40) rotate(-30)"><ellipse rx="100" ry="82" fill="{c["face"]}" stroke="{c["line"]}" stroke-width="9"/>{_PAT[k]()}</g></g>')
    return f


def fingertip(pid):
    """A child's finger seen from the front, with the little lines of a fingertip."""
    skin, ln = "#f3c9a2", "#8a5a3a"
    lines = "".join(f'<ellipse cx="0" cy="-150" rx="{rx}" ry="{rx * 1.25:.0f}" fill="none" stroke="#d29a74" stroke-width="7"/>' for rx in (16, 34, 52, 70))
    return (f'<g id="{pid}"><rect x="-110" y="-290" width="220" height="560" rx="110" fill="{skin}" stroke="{ln}" stroke-width="10"/>{lines}'
            f'<path d="M-60 120 q60 20 120 0 M-56 190 q56 16 112 0" stroke="#d29a74" stroke-width="8" fill="none" stroke-linecap="round"/></g>')


def spider(pid):
    """A friendly round spider (cartoon, smiling): only to show why the monkey has its name."""
    legs = "".join(f'<path d="M{s * 40} {y} C{s * 120} {y - 60} {s * 170} {y - 20} {s * 200} {y + 70}" stroke="{INK}" stroke-width="16" fill="none" stroke-linecap="round"/>'
                   for s in (-1, 1) for y in (-30, -6, 18, 42))
    return (f'<g id="{pid}">{legs}<ellipse cx="0" cy="10" rx="80" ry="72" fill="#8e6bd8" stroke="{INK}" stroke-width="10"/>'
            f'<circle cx="-28" cy="-4" r="20" fill="#fff" stroke="{INK}" stroke-width="6"/><circle cx="28" cy="-4" r="20" fill="#fff" stroke="{INK}" stroke-width="6"/>'
            f'<circle cx="-24" cy="0" r="9" fill="{INK}"/><circle cx="32" cy="0" r="9" fill="{INK}"/><path d="M-22 34 q22 18 44 0" stroke="{INK}" stroke-width="7" fill="none" stroke-linecap="round"/>'
            f'<ellipse cx="-50" cy="30" rx="12" ry="8" fill="#ff8fb1" opacity=".8"/><ellipse cx="50" cy="30" rx="12" ry="8" fill="#ff8fb1" opacity=".8"/></g>')


def tails_hug(pid):
    """Mama's tail and her baby's tiny tail wrapped round it (Nat Geo: "Baby spider monkeys also wrap their tiny tail around their mother's tail")."""
    big = "M-520 -60 C-260 -160 -60 60 200 -20 C340 -64 460 -40 540 40"
    small = "M-300 200 C-240 120 -180 40 -120 -10 C-90 -40 -40 -60 -30 -20 C-20 20 -80 40 -60 -10 C-40 -70 10 -60 20 -20 C30 20 -20 30 -10 -10"
    return (f'<g id="{pid}">{_limb(big, 60)}<g id="{pid}-baby">{_limb(small, 22, dict(MON, fur="#b07a52"))}</g>'
            '</g>')


def tail_up(pid, h=440):
    """Mango's tail held up beside her, to measure it against her body: (0, 0) is where it leaves her hip; it goes out to the side, then up, the tip curled."""
    d = f"M0 0 C70 0 130 -30 130 -110 C130 {-110 - h * .3:.0f} 110 {-110 - h * .6:.0f} 130 {-110 - h * .85:.0f} C140 {-110 - h - 20:.0f} 190 {-110 - h - 30:.0f} 200 {-110 - h + 10:.0f}"
    return f'<g id="{pid}">{_limb(d, 22)}</g>'
