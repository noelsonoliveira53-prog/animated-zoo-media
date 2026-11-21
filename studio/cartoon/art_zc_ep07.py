"""Art for zc_ep07 "Who Looks After a Baby Elephant?" (Nov 18-19 2026): Tumble's family. Three more elephants drawn with art2.elephant
in other skin colours (Auntie, big sister, Grandma; Mama and Tumble are unchanged), a drop of milk, a bundle of grass, a little bed of grass.
Same hand as art.py / art2.py: flat fills, one warm dark outline. Nothing here changes an existing character, prop or place."""
import art, art2, kit
from art import INK

# ------------------------------------------------------------------ the family: art2.elephant with other skin (Mama "elephant" and Tumble "tumble" unchanged)
SKIN = {"auntie": {"fill": "#b7aec6", "shade": "#998fab", "light": "#d8d1e4", "line": "#4a4060", "far": "#a197b3", "ear": "#f6c3d2", "nail": "#f3f0f8"},     # a soft lilac grey
        "sister": {"fill": "#9fc4c4", "shade": "#80a8a8", "light": "#c8e2e2", "line": "#355656", "far": "#8bb2b2", "ear": "#f4bfcd", "nail": "#eef8f8"},     # a soft sea grey
        "grandma": {"fill": "#c4c9cc", "shade": "#a3aaae", "light": "#e2e6e8", "line": "#4a5258", "far": "#b0b6ba", "ear": "#efc6cf", "nail": "#f7f8f8"}}    # a pale silver grey
_Q = dict(neck="200 -420", tail="-268 -390", ear="250 -590", legs={"fl": 150, "bl": -140, "fl2": 96, "bl2": -196}, hip=-250, jaw=("y", 16), eyes=["eye"], brows=["brow"], trunk="392 -430")
for _k, _c in SKIN.items():
    art2.RIGS[_k] = dict(build=(lambda c: lambda p: art2.elephant(p, c=c))(_c), **_Q)
    kit.PT[_k] = kit.PT["elephant"]; kit.BOX[_k] = kit.BOX["elephant"]


# ------------------------------------------------------------------ props
def milk(pid, s=1.0):
    """A drop of milk: white, with a soft blue edge and a shine."""
    return (f'<g id="{pid}" transform="scale({s})"><path d="M0 -120 C60 -40 80 0 80 40 A80 80 0 0 1 -80 40 C-80 0 -60 -40 0 -120Z" fill="#ffffff" stroke="#9cc8e6" stroke-width="10"/>'
            f'<ellipse cx="-30" cy="30" rx="16" ry="26" fill="#dff1ff"/></g>')


def grass(pid):
    """A bundle of green grass, the size of an elephant's trunk tip."""
    blades = "".join(f'<path d="M{k * 14} 40 q{-10 + k * 6} -70 {-26 + k * 14} -130" stroke="{c}" stroke-width="16" fill="none" stroke-linecap="round"/>'
                     for k, c in zip(range(-3, 4), ("#4f9e3c", "#62b84a", "#4f9e3c", "#74c95a", "#4f9e3c", "#62b84a", "#4f9e3c")))
    return f'<g id="{pid}"><ellipse cx="0" cy="44" rx="70" ry="16" fill="#000" opacity=".12"/>{blades}</g>'


def zzz(pid):
    """Three soft Z's: someone is resting."""
    return f'<g id="{pid}">' + "".join(f'<text x="{x}" y="{y}" font-family="Fredoka, sans-serif" font-weight="700" font-size="{fs}" fill="#fff" stroke="{INK}" stroke-width="7" paint-order="stroke">z</text>'
                                       for x, y, fs in ((0, 0, 70), (50, -60, 90), (110, -140, 110))) + '</g>'


def star(pid, col="#ffd23f"):
    """A gold star for the leader."""
    import math
    pts = " ".join(f"{(60 if k % 2 == 0 else 26) * math.sin(math.pi * k / 5):.0f},{-(60 if k % 2 == 0 else 26) * math.cos(math.pi * k / 5):.0f}" for k in range(10))
    return f'<g id="{pid}"><polygon points="{pts}" fill="{col}" stroke="{INK}" stroke-width="9" stroke-linejoin="round"/></g>'


# ------------------------------------------------------------------ places
def bg_jungle_path(p):
    """The green jungle with more sky above its trees (art2.bg_jungle stops at y = -900): for the tall 9:16 views of the whole herd walking."""
    far, mid, near = art2.bg_jungle(p)
    return '<rect x="-500" y="-1900" width="2920" height="1010" fill="#bff0d4"/>' + far, mid, near


art.BG.update({"jungle_path": bg_jungle_path})
art.PLACE.update({"jungle_path": "the jungle path"})
