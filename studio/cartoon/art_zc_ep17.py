"""Art for zc_ep17 "Can a Turtle Leave Its Shell?" (Nov 28 2026): a see-through sea turtle on a picture board showing the bones of its shell,
its backbone and its ribs joined to the shell (and the thin nerves along the shell, hidden until their line); a coat on a hanger with a red
cross (a coat comes off, a shell does not); a little door doodled on Tula's shell with a question mark (the cold open and the thumbnail); a
"grows" arrow; a fingernail next to a shell plate (scute); a land turtle whose head goes into its shell; gentle-tap lines. Tula is the
existing rig ("turtle", art2.py). Same hand as art.py / art2.py. Nothing here changes an existing character, prop or place."""
import art, art2
from art import INK

BONE, BONE_LN = "#fff6dc", "#9a8458"
SH, SH_LN = "#4fae7a", "#1f5a3c"


def _body(skin="#a8dc8c", ln=SH_LN):
    """The side-view sea turtle of lungs_cut (art_zc_ep16): plastron, head, flippers (no shell). Centred at 0 0, about 950 wide."""
    return (f'<path d="M-380 40 Q0 150 400 40 Q0 90 -380 40Z" fill="#f2e6a8" stroke="{ln}" stroke-width="12"/>'
            f'<path d="M330 10 C380 -70 560 -80 590 0 C600 50 520 80 430 70 C380 66 340 50 330 10Z" fill="{skin}" stroke="{ln}" stroke-width="12"/>'
            f'<circle cx="500" cy="-14" r="20" fill="#fff" stroke="{ln}" stroke-width="5"/><circle cx="506" cy="-12" r="11" fill="#1a1a2e"/>'
            f'<circle cx="578" cy="-6" r="6" fill="{ln}"/><path d="M520 40 q24 12 46 0" stroke="{ln}" stroke-width="7" fill="none" stroke-linecap="round"/>'
            f'<path d="M150 60 C230 100 200 220 110 250 C100 180 110 120 130 70Z" fill="{skin}" stroke="{ln}" stroke-width="10"/>'
            f'<path d="M-280 60 C-360 80 -380 150 -350 180 C-310 160 -290 110 -260 70Z" fill="{skin}" stroke="{ln}" stroke-width="10"/>')


def xray_turtle(pid):
    """A sea turtle with a see-through shell: inside, the backbone (a row of round bones, -spine) runs along the top of the shell and the ribs
    (-ribs, wide flat bones) run from it to the shell's edge, joined to it (San Diego Zoo: "the shell is permanently attached to the spine and
    the rib cage"; PBS: "The spine is fused to the carapace"). -shell (the outline, it pulses), -nerves (thin yellow lines along the shell,
    hidden: opacity 0). Centred at 0 0, about 950 wide."""
    shell_d = "M-360 40 C-300 -300 260 -330 380 40Z"
    shell = (f'<g id="{pid}-shell"><path d="{shell_d}" fill="#bfe6cf" fill-opacity=".55" stroke="{SH_LN}" stroke-width="16"/>'
             f'<path d="M-300 20 C-250 -250 220 -270 320 20" stroke="{SH}" stroke-width="10" fill="none" stroke-dasharray="30 18" opacity=".7"/></g>')
    # the backbone follows the inside of the dome (a quadratic close to the shell's top), from the tail to the neck
    pts = [(-330 + k * 62, 0) for k in range(12)]
    def top(x): return -235 + 235 * ((x - 10) / 340) ** 2      # the inner dome line
    vert = "".join(f'<ellipse cx="{x}" cy="{top(x) + 8:.0f}" rx="27" ry="21" fill="{BONE}" stroke="{BONE_LN}" stroke-width="7"/>' for x, _ in pts if -320 < x < 360)
    spine = f'<g id="{pid}-spine"><path d="M-330 {top(-330) + 8:.0f} Q10 -460 360 {top(360) + 8:.0f}" stroke="{BONE_LN}" stroke-width="10" fill="none"/>{vert}</g>'
    ribs = ""
    for x in (-230, -125, -15, 95, 205, 300):      # wide flat ribs from the backbone down to the shell's rim (a rib cage inside the shell)
        y0 = top(x) + 30; x1 = x * 1.12 + 10; y1 = 12
        d = f'M{x} {y0:.0f} Q{x * 1.1 + 5:.0f} {(y0 + y1) / 2:.0f} {x1:.0f} {y1}'
        ribs += f'<path d="{d}" stroke="{BONE_LN}" stroke-width="40" fill="none" stroke-linecap="round"/><path d="{d}" stroke="{BONE}" stroke-width="26" fill="none" stroke-linecap="round"/>'
    ribs = f'<g id="{pid}-ribs">{ribs}</g>'
    nerves = (f'<g id="{pid}-nerves" opacity="0"><path d="M-320 10 C-270 -230 210 -250 330 10" stroke="#ffcf3f" stroke-width="9" fill="none" stroke-dasharray="4 16" stroke-linecap="round"/>'
              f'<path d="M-250 0 C-200 -170 160 -190 260 0" stroke="#ffcf3f" stroke-width="7" fill="none" stroke-dasharray="4 16" stroke-linecap="round"/></g>')
    return f'<g id="{pid}">{_body()}{shell}{ribs}{spine}{nerves}</g>'


def coat(pid):
    """A little red coat on a hanger (it comes off); -x: a big red cross that is hidden (opacity 0) until 'a shell does not'. Centred at 0 0, about 420 tall."""
    body = (f'<path d="M0 -230 q0 -40 30 -40 q30 0 30 30" stroke="#6b6b7a" stroke-width="12" fill="none" stroke-linecap="round"/>'
            f'<path d="M-170 -150 L0 -220 L170 -150" stroke="#6b6b7a" stroke-width="14" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="M-150 -160 L-60 -200 L0 -150 L60 -200 L150 -160 L190 40 L120 50 L120 200 L-120 200 L-120 50 L-190 40Z" fill="#ef5b5b" stroke="{INK}" stroke-width="10" stroke-linejoin="round"/>'
            f'<path d="M0 -150 L0 200" stroke="{INK}" stroke-width="7"/>' + "".join(f'<circle cx="-22" cy="{y}" r="11" fill="#ffd23f" stroke="{INK}" stroke-width="5"/>' for y in (-80, 0, 80)))
    x = (f'<g id="{pid}-x" opacity="0"><path d="M-170 -170 L170 170 M170 -170 L-170 170" stroke="#fff" stroke-width="52" stroke-linecap="round"/>'
         f'<path d="M-170 -170 L170 170 M170 -170 L-170 170" stroke="#e63946" stroke-width="34" stroke-linecap="round"/></g>')
    return f'<g id="{pid}"><g id="{pid}-c">{body}</g>{x}</g>'


def door(pid):
    """A little door doodled on Tula's shell, with a knob and a big question mark beside it. Drawn at the middle of the shell's side (Tula's shell
    in the rig spans x -196..204, top near y -330; this sits at the shell's side, anchor at the door's bottom middle)."""
    return (f'<g id="{pid}"><path d="M-46 0 L-46 -96 Q0 -140 46 -96 L46 0Z" fill="#c98a4a" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
            f'<circle cx="26" cy="-46" r="7" fill="#ffd23f" stroke="{INK}" stroke-width="4"/>'
            f'<g id="{pid}-q"><text x="104" y="-40" font-family="Fredoka, Nunito, sans-serif" font-weight="700" font-size="120" fill="#ffd23f" stroke="{INK}" stroke-width="8" paint-order="stroke" text-anchor="middle">?</text></g></g>')


def grow_arrow(pid):
    """A fat curved arrow from left to right ("grows"), centred at 0 0, about 300 wide."""
    return (f'<g id="{pid}"><path d="M-150 30 Q0 -70 120 10" stroke="{INK}" stroke-width="44" fill="none" stroke-linecap="round"/>'
            f'<path d="M-150 30 Q0 -70 120 10" stroke="#ffd23f" stroke-width="26" fill="none" stroke-linecap="round"/>'
            f'<path d="M96 -40 L170 40 L70 56Z" fill="#ffd23f" stroke="{INK}" stroke-width="9" stroke-linejoin="round"/></g>')


def nail_scute(pid):
    """Left: a big finger with a shiny fingernail (-nail). Middle: an equals sign. Right: one shell plate (a scute, -scute) with its growth
    rings. San Diego Zoo: scutes "are made of keratin like our fingernails". Centred at 0 0, about 1100 wide."""
    finger = (f'<g transform="translate(-340 0)"><path d="M-110 260 L-110 -120 Q-110 -230 0 -230 Q110 -230 110 -120 L110 260Z" fill="#f6c39b" stroke="{INK}" stroke-width="12"/>'
              f'<path d="M-80 120 q80 30 160 0" stroke="#d99a72" stroke-width="9" fill="none" stroke-linecap="round"/>'
              f'<g id="{pid}-nail"><path d="M-72 -40 L-72 -140 Q-72 -200 0 -200 Q72 -200 72 -140 L72 -40 Q0 -20 -72 -40Z" fill="#ffe3ea" stroke="#c9667d" stroke-width="9"/>'
              f'<path d="M-40 -150 q20 -26 50 -24" stroke="#fff" stroke-width="12" fill="none" stroke-linecap="round"/></g></g>')
    eq = f'<path d="M-60 -30 L60 -30 M-60 30 L60 30" stroke="{INK}" stroke-width="26" stroke-linecap="round"/>'
    hexd = lambda r: " ".join(f"{r * __import__('math').cos(__import__('math').radians(a)):.0f},{r * __import__('math').sin(__import__('math').radians(a)):.0f}" for a in range(0, 360, 60))
    scute = (f'<g transform="translate(360 0)"><g id="{pid}-scute"><polygon points="{hexd(210)}" fill="{SH}" stroke="{SH_LN}" stroke-width="14" stroke-linejoin="round"/>'
             f'<polygon points="{hexd(150)}" fill="none" stroke="#3a8f60" stroke-width="9"/><polygon points="{hexd(90)}" fill="none" stroke="#3a8f60" stroke-width="9"/>'
             f'<path d="M-120 -120 q50 -40 110 -36" stroke="#fff" stroke-width="14" fill="none" stroke-linecap="round" opacity=".45"/></g></g>')
    return f'<g id="{pid}">{finger}{eq}{scute}</g>'


def land_turtle(pid):
    """A land turtle (a high brown dome, short legs) seen from the side. Its head (-head) is drawn BEHIND the shell, so a tween of x -150 on
    -head pulls it into the shell (Live Science: "Many turtles are able to retract their heads and feet into their shells"). Feet at y 0,
    centred at 0, about 640 wide."""
    legs = "".join(f'<path d="M{x - 34} -40 L{x - 30} 0 L{x + 30} 0 L{x + 34} -40Z" fill="#b9a36a" stroke="{INK}" stroke-width="9" stroke-linejoin="round"/>' for x in (-170, 150))
    head = (f'<g id="{pid}-head"><path d="M150 -110 C200 -170 300 -170 320 -110 C330 -70 290 -50 230 -56 C190 -60 160 -76 150 -110Z" fill="#b9a36a" stroke="{INK}" stroke-width="10"/>'
            f'<circle cx="262" cy="-116" r="16" fill="#fff" stroke="{INK}" stroke-width="5"/><circle cx="267" cy="-114" r="9" fill="#1a1a2e"/>'
            f'<path d="M282 -80 q14 8 26 0" stroke="{INK}" stroke-width="6" fill="none" stroke-linecap="round"/></g>')
    dome = "M-260 -30 C-250 -330 250 -330 260 -30Z"
    shell = (f'<path d="{dome}" fill="#a0703c" stroke="{INK}" stroke-width="14"/>'
             f'<path d="M-150 -60 L-120 -200 L0 -230 L120 -200 L150 -60 M-120 -200 L-200 -150 M120 -200 L200 -150 M0 -230 L0 -60" stroke="#6e4a22" stroke-width="10" fill="none" stroke-linejoin="round"/>'
             f'<path d="M-270 -30 L270 -30" stroke="{INK}" stroke-width="16" stroke-linecap="round"/>'
             f'<path d="M-170 -230 Q-80 -290 20 -290" stroke="#fff" stroke-width="14" fill="none" stroke-linecap="round" opacity=".3"/>')
    return f'<g id="{pid}">{legs}{head}{shell}</g>'


def tap_lines(pid):
    """Three short curved lines and a little star around a gentle tap (a touch Tula can feel), centred at 0 0."""
    arcs = "".join(f'<path d="M{-40 - k * 30} {-60 - k * 26} Q0 {-100 - k * 36} {40 + k * 30} {-60 - k * 26}" stroke="#ffd23f" stroke-width="12" fill="none" stroke-linecap="round"/>' for k in range(3))
    return f'<g id="{pid}">{arcs}</g>'
