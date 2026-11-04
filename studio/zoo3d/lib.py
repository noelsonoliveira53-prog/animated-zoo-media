"""Shared Blender helpers for the ZooBlender 3D sing-along engine (Blender 4.2+ / 5.x)."""
import bpy, math, random

def scene():
    return bpy.context.scene

def rgb(h):
    h = h.lstrip("#"); c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return tuple(((x + 0.055) / 1.055) ** 2.4 if x > 0.04045 else x / 12.92 for x in c)  # sRGB -> linear

_mats = {}
def mat(name, color, rough=0.5, coat=0.0, sheen=0.0, sss=0.0, metal=0.0, bump=0.0, bump_scale=8.0, emission=None, emit=1.0, alpha=1.0):
    """Principled material, cached by name. color = hex string or linear tuple."""
    if name in _mats: return _mats[name]
    if isinstance(color, str): color = rgb(color)
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*color, 1)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    for key, val in (("Coat Weight", coat), ("Sheen Weight", sheen), ("Subsurface Weight", sss)):
        if key in b.inputs: b.inputs[key].default_value = val
    if "Subsurface Radius" in b.inputs and sss: b.inputs["Subsurface Radius"].default_value = (0.4, 0.3, 0.25)
    if emission is not None and "Emission Color" in b.inputs:
        if isinstance(emission, str): emission = rgb(emission)
        b.inputs["Emission Color"].default_value = (*emission, 1); b.inputs["Emission Strength"].default_value = emit
    if alpha < 1:
        b.inputs["Alpha"].default_value = alpha
        try: m.surface_render_method = "BLENDED"
        except Exception: pass
    if bump:
        tc = nt.nodes.new("ShaderNodeTexCoord"); vor = nt.nodes.new("ShaderNodeTexVoronoi"); vor.inputs["Scale"].default_value = bump_scale
        bp = nt.nodes.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = bump; bp.inputs["Distance"].default_value = 0.02
        nt.links.new(tc.outputs["Object"], vor.inputs["Vector"]); nt.links.new(vor.outputs["Distance"], bp.inputs["Height"]); nt.links.new(bp.outputs["Normal"], b.inputs["Normal"])
    _mats[name] = m
    return m

def smooth(o):
    if o.type == "MESH":
        for p in o.data.polygons: p.use_smooth = True
    return o

def _finish(o, name, mat_, parent, loc, rot, scale):
    o.name = name
    if mat_ is not None: o.data.materials.append(mat_)
    if parent is not None: o.parent = parent
    o.location = loc; o.rotation_euler = rot; o.scale = scale
    return o

def sphere(name, r, loc=(0, 0, 0), scale=(1, 1, 1), m=None, parent=None, segs=48, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=segs, ring_count=max(8, segs // 2), radius=r)
    return smooth(_finish(bpy.context.object, name, m, parent, loc, rot, scale))

def cube(name, size=1, loc=(0, 0, 0), scale=(1, 1, 1), m=None, parent=None, rot=(0, 0, 0), bevel=0.0, segs=3):
    bpy.ops.mesh.primitive_cube_add(size=size)
    o = _finish(bpy.context.object, name, m, parent, loc, rot, scale)
    if bevel:
        b = o.modifiers.new("Bevel", "BEVEL"); b.width = bevel; b.segments = segs; b.use_clamp_overlap = True
        try: b.affect = "EDGES"
        except Exception: pass
        smooth(o)
        try:
            o.data.use_auto_smooth = True
        except Exception:
            pass
    return o

def cylinder(name, r, depth, loc=(0, 0, 0), scale=(1, 1, 1), m=None, parent=None, rot=(0, 0, 0), verts=40):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=depth, vertices=verts)
    return smooth(_finish(bpy.context.object, name, m, parent, loc, rot, scale))

def cone(name, r1, r2, depth, loc=(0, 0, 0), scale=(1, 1, 1), m=None, parent=None, rot=(0, 0, 0), verts=40):
    bpy.ops.mesh.primitive_cone_add(radius1=r1, radius2=r2, depth=depth, vertices=verts)
    return smooth(_finish(bpy.context.object, name, m, parent, loc, rot, scale))

def torus(name, R, r, loc=(0, 0, 0), scale=(1, 1, 1), m=None, parent=None, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_torus_add(major_radius=R, minor_radius=r, major_segments=48, minor_segments=16)
    return smooth(_finish(bpy.context.object, name, m, parent, loc, rot, scale))

def empty(name, loc=(0, 0, 0), parent=None):
    o = bpy.data.objects.new(name, None); scene().collection.objects.link(o); o.location = loc
    if parent is not None: o.parent = parent
    return o

def subsurf(o, lv=2):
    m = o.modifiers.new("Subsurf", "SUBSURF"); m.levels = lv; m.render_levels = lv
    return o

def text3d(name, body, size=1.0, loc=(0, 0, 0), m=None, parent=None, extrude=0.12, bevel=0.03, rot=(math.pi / 2, 0, 0)):
    """Chunky 3D letters (faces -Y like the characters). Centered."""
    cu = bpy.data.curves.new(name, "FONT"); cu.body = body; cu.size = size
    cu.extrude = extrude; cu.bevel_depth = bevel; cu.bevel_resolution = 3
    cu.align_x = "CENTER"; cu.align_y = "CENTER"
    o = bpy.data.objects.new(name, cu); scene().collection.objects.link(o)
    if m is not None: cu.materials.append(m)
    o.location = loc; o.rotation_euler = rot
    if parent is not None: o.parent = parent
    return o

def eye_pair(prefix, parent, spacing=0.3, z=0.25, y=-0.7, r=0.26, iris_hex="#3b2410", lid_mat=None, toward=0.3):
    """Big glossy cartoon eyes with lids. Returns list of (socket, lid) for blinking/looking.
    Blink: set lid.rotation_euler.x to radians(78) (closed) / radians(-110) (open)."""
    white = mat("EyeWhite", "#fbfdff", 0.12, coat=1.0)
    iris = mat(f"Iris{iris_hex}", iris_hex, 0.4, coat=0.3)
    pupil = mat("Pupil", "#050303", 0.45, coat=0.15)
    glint = mat("Glint", (1, 1, 1), 0.0, emission=(1, 1, 1), emit=2.0)
    out = []
    for sx in (-1, 1):
        sock = empty(f"{prefix}Eye{sx}", (spacing * sx, y, z), parent); sock.rotation_euler = (0, 0, -toward * sx)
        sphere(f"{prefix}White{sx}", r, (0, 0, 0), (1, 0.72, 1), white, sock, 48)
        sphere(f"{prefix}Iris{sx}", r * 0.66, (0, -r * 0.58, 0), (1, 0.35, 1), iris, sock, 32)
        sphere(f"{prefix}Pupil{sx}", r * 0.38, (0, -r * 0.8, 0), (1, 0.3, 1), pupil, sock, 24)
        sphere(f"{prefix}Glint{sx}", r * 0.14, (r * 0.22 * sx + r * 0.1, -r * 0.9, r * 0.25), (1, 0.5, 1), glint, sock, 12)
        bpy.ops.mesh.primitive_uv_sphere_add(segments=40, ring_count=20, radius=r * 1.05)
        lid = bpy.context.object; lid.name = f"{prefix}Lid{sx}"; smooth(lid)
        if lid_mat is not None: lid.data.materials.append(lid_mat)
        lid.parent = sock
        bpy.ops.object.mode_set(mode="EDIT"); bpy.ops.mesh.select_all(action="DESELECT"); bpy.ops.object.mode_set(mode="OBJECT")
        for v in lid.data.vertices: v.select = v.co.z < -0.01
        bpy.ops.object.mode_set(mode="EDIT"); bpy.ops.mesh.delete(type="VERT"); bpy.ops.object.mode_set(mode="OBJECT")
        lid.scale = (1, 0.76, 1); lid.rotation_euler = (math.radians(-110), 0, 0)
        out.append((sock, lid))
    return out

def key(o, path, frame, value):
    setattr(o, path, value); o.keyframe_insert(path, frame=frame)

def smoothstep(x):
    x = max(0.0, min(1.0, x)); return x * x * (3 - 2 * x)

def light(name, kind, energy, loc=(0, 0, 0), rot=(0, 0, 0), color=(1, 1, 1), size=1.0, angle=None):
    l = bpy.data.lights.new(name, kind); l.energy = energy; l.color = color
    if kind == "AREA": l.size = size
    if kind == "SUN" and angle is not None: l.angle = angle
    o = bpy.data.objects.new(name, l); scene().collection.objects.link(o); o.location = loc; o.rotation_euler = rot
    return o

def sky(color_hex="#9fd4ff", strength=0.9, nishita=True, sun_elev=38):
    world = bpy.data.worlds.new("Sky"); scene().world = world; world.use_nodes = True
    wn = world.node_tree; bg = wn.nodes["Background"]
    if nishita:
        try:
            s = wn.nodes.new("ShaderNodeTexSky")
            for t in ("MULTIPLE_SCATTERING", "NISHITA", "HOSEK_WILKIE"):
                try: s.sky_type = t; break
                except Exception: pass
            for a, v in (("sun_elevation", math.radians(sun_elev)), ("sun_rotation", math.radians(200)), ("altitude", 300)):
                if hasattr(s, a): setattr(s, a, v)
            wn.links.new(s.outputs["Color"], bg.inputs["Color"]); bg.inputs["Strength"].default_value = 0.2
            return world
        except Exception:
            pass
    bg.inputs["Color"].default_value = (*rgb(color_hex), 1); bg.inputs["Strength"].default_value = strength
    return world

def rand(seed):
    random.seed(seed); return random
