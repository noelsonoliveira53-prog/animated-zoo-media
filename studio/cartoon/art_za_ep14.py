"""Pictures for za_ep14 "Can Poppy Stay Awake to See the Dancing Sky?" (Nov 23 2026). New places and props only: no character, place or older prop is
drawn differently (the night places reuse the ground of art2 / art_za_ep10 places under a night sky and a soft blue tint; the characters are drawn
after the ground, so they stay bright: never dark enough to hide a face).

Places (each has the northern lights in its far layer as #<p>_aur, with three ribbons #<p>_aur1..3; "..._lights" places show them from frame 1,
the others keep them hidden until an fx fades them in):
  "arctic_night"   the Arctic shore at night (art2 "arctic" ground): stars, a moon, ice and dark water.
  "snow_night"     the flat snow at the bottom of the hill at night (art_za_ep10 "snowbottom" ground, y 935).
  "hilltop_night"  on top of the snowy hill at night (art_za_ep10 "hilltop" ground, y 880); "hilltop_lights" the same with the lights.
  "nest_night"     the little ledge in the middle of the hill at night (art_za_ep10 "hillmid" ground, y 920) with a round snow nest;
                   "nest_lights" the same with the lights.
Props:
  zzz(p)           three Z's floating up (sleep). Anchored at the lowest Z.
  globe(p)         the Earth seen from the side, the North Pole on top, a green ring of light round it, an arrow at the top. Anchored at its middle.
  night_card(p)    a picture: the night sky over snow with green lights. #<p>-rib: the ribbons. Anchored at its middle.
  cloud_card(p)    a picture: the night sky over snow, a big grey cloud in front of the lights. Anchored at its middle.
  sun_card(p)      a picture: a bright day sky over snow with the sun, no lights. Anchored at its middle.
  colors(p)        three dots: a big green one, a pink one, a purple one. Anchored at its middle.
"""
import math, random
import art, art2, kit
import art_za_ep10 as A10

INK = art.INK
TINT = '<rect x="-700" y="-1100" width="3400" height="3400" fill="#1a2766" opacity=".34"/>'


def _stars(p, n=110, seed=14, y1=520):
    r = random.Random(seed)
    return "".join(f'<circle cx="{r.uniform(-400, 2300):.0f}" cy="{r.uniform(-800, y1):.0f}" r="{r.choice((3, 4, 5, 6))}" fill="#fff8d6" opacity="{r.uniform(.5, 1):.2f}"/>' for _ in range(n))


def _moon(x, y):
    return f'<circle cx="{x}" cy="{y}" r="140" fill="#fff6c9" opacity=".18"/><circle cx="{x}" cy="{y}" r="92" fill="#fff6c9"/><circle cx="{x - 26}" cy="{y - 20}" r="16" fill="#efe2a8"/><circle cx="{x + 30}" cy="{y + 28}" r="11" fill="#efe2a8"/>'


def _ribbon(pid, x0, x1, ytop, h, amp, seed, cols):
    """One curtain of light: a wavy band, bright at the bottom edge, fading up into the sky, with soft upright rays inside it."""
    r = random.Random(seed); n = 9; xs = [x0 + (x1 - x0) * k / n for k in range(n + 1)]
    ys = [ytop + amp * math.sin(k * 1.3 + seed) + r.uniform(-14, 14) for k in range(n + 1)]
    top = "M%.0f %.0f " % (xs[0], ys[0]) + " ".join("Q%.0f %.0f %.0f %.0f" % ((xs[k - 1] + xs[k]) / 2, ys[k - 1] - 30, xs[k], ys[k]) for k in range(1, n + 1))
    bot = " ".join("L%.0f %.0f" % (xs[k], ys[k] + h + 20 * math.sin(k * 2.1 + seed)) for k in range(n, -1, -1))
    g = f"{pid}g"; d = f"{top} {bot}Z"
    rays = "".join(f'<rect x="{x:.0f}" y="{ytop - amp - 80:.0f}" width="{r.choice((10, 14, 18))}" height="{h + 2 * amp + 160:.0f}" fill="#eafff4" opacity="{r.uniform(.18, .4):.2f}"/>'
                   for x in [x0 + k * 34 + r.uniform(-8, 8) for k in range(int((x1 - x0) / 34))])
    return (f'<defs><linearGradient id="{g}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{cols[0]}" stop-opacity="0"/>'
            f'<stop offset=".35" stop-color="{cols[0]}" stop-opacity=".75"/><stop offset=".82" stop-color="{cols[1]}" stop-opacity=".95"/><stop offset="1" stop-color="{cols[2]}" stop-opacity=".95"/></linearGradient>'
            f'<clipPath id="{pid}c"><path d="{d}"/></clipPath></defs>'
            f'<g id="{pid}"><path d="{d}" fill="url(#{g})"/><g clip-path="url(#{pid}c)">{rays}</g></g>')


def lights(p, on, y=0, x=0):
    """The northern lights: three green curtains (one with a pink edge), high in the sky, away from the top-left corner (the channel mark)."""
    return (f'<g id="{p}_aur" opacity="{1 if on else 0}" transform="translate({x} {y})">'
            + _ribbon(f"{p}_aur1", 380, 1500, -40, 300, 50, 1, ("#19ff7a", "#8dffc0", "#ff7fc8"))
            + _ribbon(f"{p}_aur2", 900, 2150, 40, 260, 60, 2, ("#22f58e", "#8affc4", "#d2ffe6"))
            + _ribbon(f"{p}_aur3", 1200, 2300, -120, 220, 40, 3, ("#3dff9c", "#a6ffd2", "#d29cff"))
            + '</g>')


def _night_far(p, on, horizon, moon=(1660, 150), band="#3a4f8f", ly=0):
    return (art._sky(p, "#111c50", "#3c4f9e") + _stars(p) + _moon(*moon)
            + A10._peaks(horizon, "#4b5f9e", "#8fa3d6", 9) + f'<rect x="-500" y="{horizon - 10}" width="2920" height="300" fill="{band}"/>' + lights(p, on, ly))


def bg_arctic_night(p, on=False):
    far, mid, near = art2.bg_arctic(p)
    far = _night_far(p, on, 700, (1660, 140))
    mid = mid.replace('fill="#6fbfe8"', 'fill="#2f5d9a"') + TINT
    return far, mid, near + TINT


def bg_snow_night(p, on=False):
    far, mid, near = A10.bg_snowbottom(p)
    return _night_far(p, on, 720, (1500, 160)), mid + TINT, near + TINT


def bg_hilltop_night(p, on=False):
    far, mid, near = A10.bg_hilltop(p)
    far = _night_far(p, on, 600, (1780, 130), "#4a5f9c", 200) + '<rect x="-500" y="600" width="2920" height="40" fill="#5a7cc0" opacity=".7"/>'
    return far, mid + TINT, near + TINT


def _nest(x, y, s=1.0):
    """A round snow nest: a low ring of snow (the cub lies inside it, so it is drawn in the ground layer behind her)."""
    return (f'<g transform="translate({x} {y}) scale({s})"><ellipse cx="0" cy="-10" rx="360" ry="70" fill="#b9d6ef"/><ellipse cx="0" cy="-26" rx="340" ry="60" fill="#ffffff"/>'
            f'<ellipse cx="0" cy="-20" rx="250" ry="34" fill="#dcecfb"/><path d="M-300 -50 q60 -40 140 -30 M120 -70 q90 -10 160 24" stroke="#ffffff" stroke-width="16" fill="none" stroke-linecap="round"/></g>')


def bg_nest_night(p, on=False):
    far, mid, near = A10.bg_hillmid(p)
    return _night_far(p, on, 700, (1760, 140), ly=200), mid + TINT, near + TINT + _nest(880, 930, 1.0)


art.BG.update({"arctic_night": bg_arctic_night, "snow_night": bg_snow_night, "hilltop_night": bg_hilltop_night, "nest_night": bg_nest_night,
               "hilltop_lights": lambda p: bg_hilltop_night(p, True), "nest_lights": lambda p: bg_nest_night(p, True)})
art.PLACE.update({"arctic_night": "the Arctic shore at night", "snow_night": "the snow at the bottom of the hill at night", "hilltop_night": "the top of the snowy hill at night",
                  "nest_night": "the snow nest on the hill at night", "hilltop_lights": "the hilltop under the northern lights", "nest_lights": "the snow nest under the northern lights"})


# ------------------------------------------------------------------ props
def zzz(p):
    z = lambda x, y, s, o: (f'<g transform="translate({x} {y}) scale({s})" opacity="{o}"><path d="M-30 -30 L30 -30 L-30 30 L30 30" stroke="{INK}" stroke-width="22" fill="none" stroke-linejoin="round" stroke-linecap="round"/>'
                            f'<path d="M-30 -30 L30 -30 L-30 30 L30 30" stroke="#ffffff" stroke-width="11" fill="none" stroke-linejoin="round" stroke-linecap="round"/></g>')
    return f'<g id="{p}">{z(0, 0, 1.0, 1)}{z(70, -90, .8, .9)}{z(120, -170, .6, .8)}</g>'


def globe(p):
    land = ('<path d="M-150 -40 q40 -50 90 -30 q30 30 70 10 q40 -10 50 40 q-30 40 -90 30 q-60 20 -100 -10Z" fill="#7cc96a"/>'
            '<path d="M40 60 q50 -20 90 10 q10 50 -40 70 q-50 -10 -50 -80Z" fill="#7cc96a"/>')
    return (f'<g id="{p}"><circle r="250" fill="#ffffff" opacity=".5"/><circle r="220" fill="#4aa8e8" stroke="{INK}" stroke-width="12"/>{land}'
            f'<path d="M-150 -160 A220 220 0 0 1 150 -160 Q0 -128 -150 -160Z" fill="#ffffff"/>'
            f'<g id="{p}-ring"><ellipse cx="0" cy="-168" rx="170" ry="40" fill="none" stroke="#3ef0a0" stroke-width="22" opacity=".9"/>'
            f'<ellipse cx="0" cy="-168" rx="170" ry="40" fill="none" stroke="#c7ffe0" stroke-width="8"/></g>'
            f'<g id="{p}-arr"><path d="M0 -420 L0 -300" stroke="{INK}" stroke-width="34" stroke-linecap="round"/><path d="M0 -420 L0 -300" stroke="#ff8a3d" stroke-width="18" stroke-linecap="round"/>'
            f'<path d="M-40 -320 L0 -262 L40 -320Z" fill="#ff8a3d" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/></g></g>')


def _card(p, sky, inner, w=520, h=360):
    return (f'<g id="{p}"><rect x="{-w / 2 - 18}" y="{-h / 2 - 18}" width="{w + 36}" height="{h + 36}" rx="40" fill="#ffffff" stroke="{INK}" stroke-width="12"/>'
            f'<clipPath id="{p}cl"><rect x="{-w / 2}" y="{-h / 2}" width="{w}" height="{h}" rx="26"/></clipPath>'
            f'<g clip-path="url(#{p}cl)"><rect x="{-w / 2}" y="{-h / 2}" width="{w}" height="{h}" fill="{sky}"/>{inner}'
            f'<path d="M{-w / 2} {h / 2 - 70} q{w / 4} -40 {w / 2} -10 t{w / 2} 0 L{w / 2} {h / 2} L{-w / 2} {h / 2}Z" fill="#eef7ff"/></g></g>')


def _mini_rib(pid, scale=1.0):
    return (f'<g id="{pid}" transform="scale({scale})">' + _ribbon(f"{pid}a", -260, 120, -150, 160, 22, 1, ("#19ff7a", "#8dffc0", "#ff7fc8"))
            + _ribbon(f"{pid}b", -60, 280, -120, 140, 26, 2, ("#22f58e", "#8affc4", "#d2ffe6")) + '</g>')


def night_card(p):
    stars = "".join(f'<circle cx="{x}" cy="{y}" r="5" fill="#fff8d6"/>' for x, y in ((-210, -140), (-90, -60), (60, -150), (200, -90), (230, 10), (-230, 0)))
    return _card(p, "#1a2a6c", stars + _mini_rib(f"{p}-rib"))


def cloud_card(p):
    cloud = ('<g><ellipse cx="0" cy="-40" rx="200" ry="80" fill="#9aa6c0"/><ellipse cx="-90" cy="-80" rx="100" ry="80" fill="#9aa6c0"/>'
             '<ellipse cx="80" cy="-100" rx="110" ry="90" fill="#aab4cc"/></g>')
    return _card(p, "#1a2a6c", _mini_rib(f"{p}-rib", .9) + f'<g id="{p}-cl">{cloud}</g>')


def sun_card(p):
    return _card(p, "#8fd8ff", art._sun(p + "sun", 120, -80, 60, "#ffe066"))


def colors(p):
    dot = lambda x, r, c: f'<circle cx="{x}" cy="0" r="{r}" fill="{c}" stroke="{INK}" stroke-width="10"/>'
    return f'<g id="{p}">{dot(-150, 90, "#3ef0a0")}{dot(30, 60, "#ff8fd0")}{dot(170, 60, "#b07cff")}</g>'
