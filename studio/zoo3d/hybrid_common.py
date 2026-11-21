"""Shared pure-Python helpers for the hybrid 2.5D pipeline (sprites.py in Blender, compose.py in plain Python).

No bpy imports here: both sides must agree on asset keys and on the camera math.
"""
import hashlib, json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")

MOUTHS = [0.0, 0.3, 0.6, 1.0]          # closed, small, mid, wide
LOOPS = {                               # loop name -> pose state (phase comes from the bar)
    "idle":  {"energy": 0.45, "jump": 0.0, "wave": 0},
    "dance": {"energy": 0.95, "jump": 0.3, "wave": 0},
    "wave":  {"energy": 0.9,  "jump": 0.3, "wave": 1},
}
ANGLES = {"front": 0.0, "q": 0.6}      # q = 3/4 view, character turned toward screen right (mirror for left)
SENSOR = 36.0                           # Blender default sensor width (sensor_fit AUTO, landscape)

STRIP = ("scale", "color_schedule")     # per-episode opts that do not change the sprite


def _h(obj, n=6):
    return hashlib.sha1(json.dumps(obj, sort_keys=True).encode()).hexdigest()[:n]


def char_key(char, opts):
    """Asset folder name for a cast member: char + variant + hash of the look-defining opts."""
    o = {k: v for k, v in (opts or {}).items() if k not in STRIP}
    tag = o.get("shape") or o.get("variant") or o.get("kind") or ""
    return f"{char}{'-' + str(tag) if tag else ''}-{_h(o)}"


def prop_spec(p):
    """The look-defining part of a job prop (position, delay and timing excluded)."""
    keep = ("type", "name", "text", "color", "size", "shape", "opts", "emit")
    return {k: p[k] for k in keep if k in p}


def prop_key(p):
    s = prop_spec(p)
    base = s.get("name") or s.get("text") or s.get("shape") or s["type"]
    base = "".join(c for c in str(base).lower() if c.isalnum())[:12] or "prop"
    return f"{s['type']}-{base}-{_h(s)}"


# ------------------------------------------------------------------ camera math (matches Blender TRACK_TO -Z / up Y)
def _sub(a, b): return (a[0] - b[0], a[1] - b[1], a[2] - b[2])
def _dot(a, b): return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]
def _cross(a, b): return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])
def _norm(a):
    l = math.sqrt(_dot(a, a)) or 1.0
    return (a[0] / l, a[1] / l, a[2] / l)


def cam_basis(loc, aim):
    f = _norm(_sub(aim, loc))
    r = _cross(f, (0, 0, 1))
    if _dot(r, r) < 1e-9: r = (1, 0, 0)
    r = _norm(r); u = _cross(r, f)
    return f, r, u


def project(p, cam):
    """World point -> (px, py, depth) in the image of cam = {loc, aim, lens, res:[W,H]}. Pixel origin top-left."""
    f, r, u = cam_basis(cam["loc"], cam["aim"])
    d = _sub(p, cam["loc"])
    z = _dot(d, f)
    if z <= 1e-4: z = 1e-4
    W, H = cam["res"]
    k = cam["lens"] / SENSOR * (W if W >= H else H)
    return W / 2 + _dot(d, r) / z * k, H / 2 - _dot(d, u) / z * k, z


def view_yaw(cam, p):
    """Horizontal angle (radians) of the camera ray toward world point p, measured from -Y (the characters' front).
    Positive = camera sits to the right (+X) of the character."""
    dx = cam["loc"][0] - p[0]; dy = cam["loc"][1] - p[1]
    return math.atan2(dx, -dy)


def load_json(p, d=None):
    try:
        return json.load(open(p))
    except Exception:
        return d
