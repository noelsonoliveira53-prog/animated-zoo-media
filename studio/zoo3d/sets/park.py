"""Sunny park clearing: The Animated Zoo's home set. Reference set for the API (see API.md)."""
import math

def build(L, rng, **_):
    L.sky(nishita=True, sun_elev=40)
    L.light("Sun", "SUN", 3.0, rot=(math.radians(50), 0, math.radians(200)), color=(1, 0.95, 0.86), angle=math.radians(6))
    L.light("Fill", "AREA", 300, (-5, -8, 5), (math.radians(60), 0, math.radians(-35)), (1, 0.92, 0.85), 8)
    L.light("Rim", "AREA", 250, (5, 6, 4), (math.radians(-60), 0, math.radians(150)), (0.75, 0.88, 1), 5)
    g = L.mat("Lawn", "#62b043", 0.85, sheen=0.4, bump=0.3, bump_scale=40)
    L.cube("Ground", 1, (0, 10, -0.5), (80, 60, 1), g)
    L.cylinder("Clearing", 3.2, 0.02, (0, 0, 0.005), (1.5, 1, 1), L.mat("Path", "#e7cc96", 1.0, bump=0.2, bump_scale=12))
    bark = L.mat("Bark", "#7a4b2e", 0.9, bump=0.3, bump_scale=6)
    for i, (x, y, s) in enumerate(((-7, 7, 1.4), (7.5, 8, 1.6), (-11, 3, 1.2), (11, 3.5, 1.3), (-3.5, 12, 1.8), (4, 13, 1.5))):
        L.cylinder("Trunk", 0.22 * s, 1.8 * s, (x, y, 0.9 * s), m=bark, verts=16)
        leaf = L.mat(f"Leaves{i % 3}", ("#4caf50", "#5cb85c", "#43a047")[i % 3], 0.7, sss=0.08, bump=0.2, bump_scale=3)
        for dx, z, dy, r in ((0, 2.3, 0, 1.15), (0.6, 2.0, 0.2, 0.75), (-0.55, 2.1, -0.1, 0.8), (0.1, 2.95, 0.05, 0.8)):
            L.sphere("Leaf", r * s, (x + dx * s, y + dy * s, z * s), m=leaf, segs=24)
    petals = [L.mat(f"Petal{i}", c, 0.5, sss=0.2) for i, c in enumerate(("#ff6f9c", "#ffd23f", "#ffffff", "#b57cff", "#ff9f43"))]
    for i in range(70):
        a, rr = rng.random() * math.tau, 3.5 + rng.random() * 8
        L.sphere("Flower", 0.07, (math.cos(a) * rr, math.sin(a) * rr * 0.7 + 1.5, 0.08), (1, 1, 0.55), petals[i % 5], segs=10)
    return {
        "spots": {"center": (0, 0, 0), "left": (-2.6, 0.6, 0), "right": (2.6, 0.6, 0), "back": (0, 2.5, 0)},
        "cams": {"wide": ((0.8, -11, 2.6), (0, 0, 1.3)), "center": (0, 0, 1.3), "orbit_r": 9},
        "prop_spots": {"top": (0, 1.2, 3.3), "left": (-3.4, 0.6, 2.4), "right": (3.4, 0.6, 2.4), "front": (0, -2.0, 0.9)},
        "exposure": -0.1, "look": "AgX - High Contrast",
    }
