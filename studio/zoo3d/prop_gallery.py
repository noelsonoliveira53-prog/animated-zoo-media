"""Render every teaching prop on a plain stage (local check before a lesson uses it): python3 bpyrun.py prop_gallery.py -- out.png [tr]"""
import sys, os, math
import bpy
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import lib as L, teachprops as TP
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
out = argv[0] if argv else "/tmp/gallery.png"; tr = float(argv[1]) if len(argv) > 1 else 2.6
bpy.ops.wm.read_factory_settings(use_empty=True)
S = bpy.context.scene
L.sky("#9fd4ff", 0.9, True, 40); L.light("sun", "SUN", 3.0, rot=(math.radians(50), 0, math.radians(30)))
L.cube("ground", 1, (0, 0, -0.05), (60, 30, 0.1), L.mat("gr", "#cfe8a9", 0.9))
ITEMS = [("sign", {"text": "YES", "color": "#22a84a", "win": 1.6}), ("sign", {"text": "NOT A BEAR", "color": "#e85d00"}), ("badge", {"text": "2", "s": 1.1}), ("qbox", {}), ("dots", {}),
         ("check", {"s": 0.7}), ("cross", {"s": 0.9}), ("arrow", {}), ("count", {"n": 3, "gap": 0.3}), ("flies", {"n": 5}), ("mud", {}), ("sun", {"s": 1.25}),
         ("snowflake", {"s": 1.2}), ("leaves", {}), ("plate", {}), ("pool", {}), ("house2", {}), ("ruler", {"mark": 3.75}), ("cars", {"n": 4, "gap": 0.3}),
         ("rings", {"reach": 2.0}), ("town", {}), ("swatch", {"kind": "stripes"}), ("swatch", {"kind": "spots", "base": "#ffd23f", "mark": "#f0443a"}), ("fingerprint", {"s": 1.2}),
         ("magnifier", {"fill": "#17171c", "hairs": 6, "label": "SKIN", "s": 1.05}), ("table", {"w": 2.5}), ("butter", {}), ("sock", {}), ("ball", {}), ("zzz", {"s": 1.2, "color": "#2459b8"}),
         ("bones", {"n": 7, "gap": 0.2}), ("thermo", {"hot": True}), ("thermo", {"hot": False}), ("bamboo", {}), ("den", {}), ("notree", {"nocross": 1}), ("heart", {"s": 1.3})]
FLOAT = {"sign", "badge", "dots", "check", "cross", "sun", "snowflake", "swatch", "fingerprint", "magnifier", "zzz", "heart", "count", "rings", "flies", "arrow"}
cols = 10
for i, (n, o) in enumerate(ITEMS):
    x = (i % cols - (cols - 1) / 2) * 4.2; row = i // cols
    r = TP.build(L, n, (x, row * 9.0, 1.8 if n in FLOAT else 0.0), **o)
    TP.animate(r, tr, 6.0, {"beat": 0})
cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam")); S.collection.objects.link(cam); S.camera = cam
cam.data.type = "ORTHO"; cam.data.ortho_scale = 44; cam.location = (0, -40, 26); cam.rotation_euler = (math.radians(62), 0, 0)
S.render.engine = "BLENDER_EEVEE_NEXT" if "BLENDER_EEVEE_NEXT" in [e.identifier for e in type(S.render).bl_rna.properties["engine"].enum_items] else "BLENDER_EEVEE"
S.render.resolution_x, S.render.resolution_y = 2400, 1350; S.render.filepath = out
try: S.eevee.taa_render_samples = 8
except Exception: pass
bpy.ops.render.render(write_still=True); print("gallery", out)
