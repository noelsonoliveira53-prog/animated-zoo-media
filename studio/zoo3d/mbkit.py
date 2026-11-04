"""Moonbeam Bedtime shape + material kit (shared by chars/luna.py, chars/sleepy.py, sets/nightroom.py).
Puffy 2D curve shapes (stars, crescents, hearts) and patterned soft materials, built on lib.py conventions."""
import bpy, math


def curve_shape(L, name, pts, depth=0.06, bevel=0.04, m=None, parent=None, loc=(0, 0, 0), rot=(math.pi / 2, 0, 0), scale=(1, 1, 1)):
    """Closed 2D poly outline (XY) -> filled, extruded, rounded solid. Default rot faces -Y like text3d."""
    cu = bpy.data.curves.new(name, "CURVE"); cu.dimensions = "2D"; cu.fill_mode = "BOTH"
    cu.extrude = depth; cu.bevel_depth = bevel; cu.bevel_resolution = 3
    sp = cu.splines.new("POLY"); sp.points.add(len(pts) - 1)
    for p, (x, y) in zip(sp.points, pts):
        p.co = (x, y, 0, 1)
    sp.use_cyclic_u = True
    o = bpy.data.objects.new(name, cu); L.scene().collection.objects.link(o)
    if m is not None: cu.materials.append(m)
    if parent is not None: o.parent = parent
    o.location = loc; o.rotation_euler = rot; o.scale = scale
    return o


def star_pts(r=0.5, inner=0.5, n=5, round_=2):
    pts = []
    for i in range(n * 2):
        a = math.pi / 2 + i * math.pi / n
        rr = r if i % 2 == 0 else r * inner
        pts.append((math.cos(a) * rr, math.sin(a) * rr))
    return pts


def crescent_pts(r=0.5, cut=0.8, off=0.42, n=28):
    assert cut + off > 1.0, "cutter must poke out of the disc to make a crescent"
    """Crescent opening to the right: outer circle r minus a circle (r*cut) shifted right by r*off."""
    rc, ox = r * cut, r * off
    # intersection angles of the two circles
    # x^2+y^2=r^2 ; (x-ox)^2+y^2=rc^2 -> x = (r^2 - rc^2 + ox^2) / (2 ox)
    xi = (r * r - rc * rc + ox * ox) / (2 * ox); yi = math.sqrt(max(1e-6, r * r - xi * xi))
    a0 = math.atan2(yi, xi); b0 = math.atan2(yi, xi - ox)
    pts = []
    for k in range(n + 1):   # outer arc: a0 -> 2pi - a0 (through the left)
        a = a0 + (2 * math.pi - 2 * a0) * k / n
        pts.append((math.cos(a) * r, math.sin(a) * r))
    for k in range(1, n):    # inner arc back: -b0 -> b0 (through the left side of the cutter)
        b = (2 * math.pi - b0) - (2 * math.pi - 2 * b0) * k / n
        pts.append((ox + math.cos(b) * rc, math.sin(b) * rc))
    return pts


def heart_pts(r=0.5, n=40):
    pts = []
    for k in range(n):
        t = 2 * math.pi * k / n
        x = 16 * math.sin(t) ** 3
        y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
        pts.append((x / 17 * r, y / 17 * r))
    return pts


_pm = {}
def pattern_mat(name, c1, c2, kind="stripes", scale=6.0, rough=0.7, sheen=0.6, emit_color=None, emit=0.0, axis="Z"):
    """Soft fabric with stripes / dots / checker (two colors). Object-space coordinates so it sticks to the mesh."""
    if name in _pm: return _pm[name]
    m = L_mat_base(name, rough, sheen)
    nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    tc = nt.nodes.new("ShaderNodeTexCoord"); mix = nt.nodes.new("ShaderNodeMix"); mix.data_type = "RGBA"
    mix.inputs[6].default_value = (*_rgb(c1), 1); mix.inputs[7].default_value = (*_rgb(c2), 1)
    if kind == "stripes":
        wv = nt.nodes.new("ShaderNodeTexWave"); wv.wave_type = "BANDS"
        try: wv.bands_direction = axis
        except Exception: pass
        wv.inputs["Scale"].default_value = scale; wv.inputs["Distortion"].default_value = 0.0
        ramp = nt.nodes.new("ShaderNodeValToRGB"); ramp.color_ramp.elements[0].position = 0.45; ramp.color_ramp.elements[1].position = 0.55
        nt.links.new(tc.outputs["Object"], wv.inputs["Vector"]); nt.links.new(wv.outputs["Fac"], ramp.inputs["Fac"])
        nt.links.new(ramp.outputs["Color"], mix.inputs[0])
    elif kind == "dots":
        vo = nt.nodes.new("ShaderNodeTexVoronoi"); vo.inputs["Scale"].default_value = scale
        try: vo.inputs["Randomness"].default_value = 0.25
        except Exception: pass
        ramp = nt.nodes.new("ShaderNodeValToRGB"); ramp.color_ramp.elements[0].position = 0.22; ramp.color_ramp.elements[1].position = 0.26
        nt.links.new(tc.outputs["Object"], vo.inputs["Vector"]); nt.links.new(vo.outputs["Distance"], ramp.inputs["Fac"])
        # dots = c2 inside (small distance) -> invert by swapping
        mix.inputs[6].default_value = (*_rgb(c2), 1); mix.inputs[7].default_value = (*_rgb(c1), 1)
        nt.links.new(ramp.outputs["Color"], mix.inputs[0])
    else:
        ck = nt.nodes.new("ShaderNodeTexChecker"); ck.inputs["Scale"].default_value = scale
        ck.inputs["Color1"].default_value = (*_rgb(c1), 1); ck.inputs["Color2"].default_value = (*_rgb(c2), 1)
        nt.links.new(tc.outputs["Object"], ck.inputs["Vector"]); nt.links.new(ck.outputs["Color"], b.inputs["Base Color"])
        _pm[name] = m
        return m
    nt.links.new(mix.outputs[2], b.inputs["Base Color"])
    if emit_color is not None and "Emission Color" in b.inputs:
        b.inputs["Emission Color"].default_value = (*_rgb(emit_color), 1); b.inputs["Emission Strength"].default_value = emit
    _pm[name] = m
    return m


def L_mat_base(name, rough, sheen):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Roughness"].default_value = rough
    if "Sheen Weight" in b.inputs: b.inputs["Sheen Weight"].default_value = sheen
    return m


def _rgb(h):
    if not isinstance(h, str): return h
    h = h.lstrip("#"); c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return tuple(((x + 0.055) / 1.055) ** 2.4 if x > 0.04045 else x / 12.92 for x in c)


def lerp(a, b, x):
    return a + (b - a) * x


def pulse(t, period, length, offset=0.0):
    """0..1..0 smooth bump of `length` seconds once every `period` seconds."""
    ph = (t + offset) % period
    if ph > length: return 0.0
    return math.sin(math.pi * ph / length) ** 2
