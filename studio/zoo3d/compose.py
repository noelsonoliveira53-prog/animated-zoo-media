"""Hybrid 2.5D episode compositor: builds a sing-along episode from pre-rendered 3D assets on the CPU in minutes.

    python3 compose.py --job jobs/<id>.json                      # full episode -> out/<id>_hybrid/<id>_raw.mp4 (with the song)
    python3 compose.py --job jobs/<id>.json --test [--frames 600,900]   # a few stills -> out/<id>_hybrid/test_*.png
    python3 compose.py --job jobs/<id>.json --seconds 24-44     # a clip (with the matching audio slice)
    options: --res 1920x1080  --outfile path.mp4  --out DIR  --assets DIR  --workers 2  --crf 18  --sheet (contact sheet)
             --full3d out/<id>/frames --full3d-until 10   use engine.py's full-3D frames for the first N seconds (the hook)

Assets come from sprites.py (assets/<char key>/, assets/<set>/plates, assets/<set>/props). Same direction logic as
engine.py: each section's shots cycle once per sung line, props pop in with a scale bounce, the loop frame follows the
bar phase so the bounce stays on the beat, the mouth shape follows timing["mouth"] (4 shapes, with hysteresis), and
Bloop-style color schedules are applied as a masked hue shift. The raw MP4 goes to finish.py unchanged.
"""
import sys, os, json, math, time, zlib, random, subprocess, shutil, colorsys
from collections import OrderedDict
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import hybrid_common as HC

argv = sys.argv[1:]
def opt(name, default=None):
    if "--" + name in argv:
        i = argv.index("--" + name)
        return argv[i + 1] if i + 1 < len(argv) and not argv[i + 1].startswith("--") else True
    return default


FULL3D = os.path.abspath(opt("full3d")) if opt("full3d") else None     # engine.py frames dir (out/<id>/frames)
FULL3D_UNTIL = float(opt("full3d-until", 10))


def smoothstep(x):
    x = max(0.0, min(1.0, x)); return x * x * (3 - 2 * x)


def hex_rgb(h):
    h = h.lstrip("#"); return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def srgb_to_lin(c):
    return tuple(((x + 0.055) / 1.055) ** 2.4 if x > 0.04045 else x / 12.92 for x in c)


def lin_to_srgb(c):
    return tuple(1.055 * x ** (1 / 2.4) - 0.055 if x > 0.0031308 else 12.92 * x for x in c)


class LRU:
    def __init__(self, budget_bytes):
        self.d = OrderedDict(); self.sizes = {}; self.budget = budget_bytes; self.used = 0
    def get(self, k):
        v = self.d.get(k)
        if v is not None: self.d.move_to_end(k)
        return v
    def put(self, k, v, size):
        if k in self.d: self.used -= self.sizes.get(k, 0)
        self.d[k] = v; self.sizes[k] = size; self.used += size; self.d.move_to_end(k)
        while self.used > self.budget and len(self.d) > 1:
            kk, _ = self.d.popitem(last=False); self.used -= self.sizes.pop(kk, 0)


# ================================================================== episode model
class Episode:
    def __init__(self, job_path, res, assets):
        self.job_path = os.path.abspath(job_path); self.job_dir = os.path.dirname(self.job_path)
        self.job = job = json.load(open(self.job_path))
        self.timing = tm = job.get("timing") or json.load(open(os.path.join(self.job_dir, job["timing_file"])))
        self.fps = tm.get("fps", 24); self.dur = tm["duration"]; self.nf = int(math.ceil(self.dur * self.fps))
        self.W, self.H = res
        self.assets = assets
        self.beat_len = 60 / tm["bpm"]; self.bar_len = self.beat_len * 4
        self.mouth = tm["mouth"]
        setdir = os.path.join(assets, job["set"])
        self.setman = HC.load_json(os.path.join(setdir, "manifest.json"))
        if not self.setman:
            sys.exit(f"missing set plates: run  blender -b -P sprites.py -- --set {job['set']}")
        self.setdir = setdir
        self.spots = self.setman["spots"]
        self.propman = HC.load_json(os.path.join(setdir, "props", "manifest.json"), {}) or {}
        self.font = os.path.join(HERE, "fonts", "Baloo2-ExtraBold.ttf")
        self.img_cache = LRU(int(float(opt("cache-mb", 900)) * 1e6))
        self.plate_cache = {}
        self._build_cast(); self._build_cuts(); self._build_props(); self._mouth_track()
        self.shadow_stamp = self._make_shadow_stamp()

    # ---------------------------------------------------------- cast
    def _build_cast(self):
        self.cast = []
        missing = []
        for c in self.job["cast"]:
            key = HC.char_key(c["char"], c.get("opts", {}))
            man = HC.load_json(os.path.join(self.assets, key, "manifest.json"))
            if not man:
                missing.append((c["id"], key, c)); continue
            sp = c.get("spot", "center")
            base = tuple(self.spots.get(sp, (0, 0, 0))) if isinstance(sp, str) else tuple(sp)
            sched = [(float(t0), hex_rgb(h)) for t0, h in sorted(c.get("opts", {}).get("color_schedule") or [], key=lambda x: x[0])]
            self.cast.append({"id": c["id"], "char": c["char"], "key": key, "man": man, "dir": os.path.join(self.assets, key),
                              "base": base, "spot": sp, "scale": c.get("opts", {}).get("scale", 1.0), "yaw": c.get("yaw", 0.0),
                              "sched": sched, "home": hex_rgb(man.get("home_color") or c.get("opts", {}).get("color") or "#9d6bff"),
                              "foot_r": None})
        if missing:
            for cid, key, c in missing:
                print(f"missing sprites for cast '{cid}' ({key}): blender -b -P sprites.py -- --char {c['char']} --opts '{json.dumps(c.get('opts', {}))}'")
            sys.exit(2)
        self.host = self.job["cast"][0]["id"]
        self.by_id = {c["id"]: c for c in self.cast}

    # ---------------------------------------------------------- cuts (same logic as engine.py)
    def _build_cuts(self):
        tm = self.timing; cuts = []
        dmap = {d["section"]: d for d in self.job["direct"]}
        for sec in tm["sections"]:
            d = dmap.get(sec["name"], {})
            shots = d.get("shots", ["wide"])
            ls = [l["start"] for l in tm["lines"] if sec["start"] - 0.01 <= l["start"] < sec["end"]]
            starts = [sec["start"]] + [x for x in ls if x - sec["start"] > 0.8]
            for k, st in enumerate(starts):
                cuts.append((st, shots[k % len(shots)], d))
        if not cuts or cuts[0][0] > 0:
            cuts.insert(0, (0.0, self.job.get("intro_shot", "orbit"), self.job.get("intro", {"energy": 0.6})))
        cuts.sort(key=lambda c: c[0])
        self.cuts = cuts

    def cut_at(self, t):
        i = max(k for k, c in enumerate(self.cuts) if c[0] <= t)
        t0 = self.cuts[i][0]; t1 = self.cuts[i + 1][0] if i + 1 < len(self.cuts) else self.dur
        return self.cuts[i][1], (t - t0) / max(0.01, t1 - t0), self.cuts[i][2], i

    def who_sings(self, t):
        for l in self.timing["lines"]:
            if l["start"] - 0.05 <= t <= l["end"] + 0.05:
                return l.get("who", self.host), l.get("kind", "sing")
        return None, None

    # ---------------------------------------------------------- props
    def _build_props(self):
        self.props = []
        PA = self.setman.get("prop_spots") or {"top": (0, 0.5, 3.6), "left": (-3, 0.5, 2.2), "right": (3, 0.5, 2.2), "front": (0, -1.5, 1.0)}
        for d in self.job["direct"]:
            sec = next((s for s in self.timing["sections"] if s["name"] == d["section"]), None)
            if not sec: continue
            for k, p in enumerate(d.get("props", [])):
                at = tuple(PA.get(p.get("at", "top"), (0, 0.5, 3.6))) if isinstance(p.get("at", "top"), str) else tuple(p["at"])
                t0 = sec["start"] + p.get("delay", 0) + k * p.get("stagger", 0)
                t1 = self.dur if p.get("hold") else (min(sec["end"], t0 + p["dur"]) if p.get("dur") else sec["end"])
                key = HC.prop_key(p); pm = self.propman.get(key)
                if pm:
                    src = {"kind": "sprite", "path": os.path.join(self.setdir, "props", pm["file"]), "anchor": pm["anchor"], "ppu": pm["ppu"]}
                elif p.get("type") == "text":
                    src = self._text_sprite(p)
                else:
                    print("no sprite for prop", key, "(skipped; run sprites.py --props)"); continue
                self.props.append({"at": at, "t0": t0, "t1": t1, "spin": p.get("spin", 0.4), "src": src, "key": key})

    def _text_sprite(self, p):
        """Fallback when no 3D text sprite exists: the word in the channel font, candy fill + dark outline."""
        size = p.get("size", 1.2); px = 220
        f = ImageFont.truetype(self.font, px)
        txt = p["text"]; col = tuple(int(x * 255) for x in hex_rgb(p.get("color", "#ffcc00")))
        l, t, r, b = f.getbbox(txt, stroke_width=18)
        im = Image.new("RGBA", (r - l + 40, b - t + 60), (0, 0, 0, 0)); dr = ImageDraw.Draw(im)
        dr.text((20 - l + 8, 20 - t + 14), txt, font=f, fill=(40, 20, 60, 110), stroke_width=18, stroke_fill=(40, 20, 60, 110))
        dr.text((20 - l, 20 - t), txt, font=f, fill=col + (255,), stroke_width=18, stroke_fill=(61, 42, 122, 255))
        dr.text((20 - l, 20 - t - 6), txt, font=f, fill=tuple(min(255, int(c * 0.6 + 255 * 0.4)) for c in col) + (90,))
        # world: letters ~ size*0.75 units tall, centered on `at`
        ppu = (b - t) / (size * 0.75)
        return {"kind": "image", "img": im, "anchor": [im.width / 2, im.height / 2], "ppu": ppu}

    def prop_scale(self, pr, t):
        t0, t1 = pr["t0"], pr["t1"]
        if t < t0 or t > t1 + 0.4: return 0.0
        if t < t0 + 0.45:
            x = (t - t0) / 0.45
            return 1 + math.sin(x * math.pi) * 0.25 if x > 0.6 else smoothstep(x / 0.6) * 1.1
        if t > t1: return 1 - smoothstep((t - t1) / 0.4)
        return 1 + math.sin((t / self.beat_len) * math.pi * 2) * 0.04

    # ---------------------------------------------------------- mouth (4 shapes with hysteresis)
    def _mouth_track(self, hyst=0.07):
        M = HC.MOUTHS; th = [(M[i] + M[i + 1]) / 2 for i in range(len(M) - 1)]
        cur = 0; out = []
        for v in self.mouth:
            while cur < len(M) - 1 and v > th[cur] + hyst: cur += 1
            while cur > 0 and v < th[cur - 1] - hyst: cur -= 1
            out.append(cur)
        self.mq = out

    # ---------------------------------------------------------- per-character state (mirrors engine.state_for)
    def state(self, ch, f, t, d):
        who, kind = self.who_sings(t)
        singing = who in (ch["id"], "all") or (who == "host" and ch["id"] == self.host) or (d.get("group") and kind == "sing")
        e = d.get("energy", 0.5) * (1.0 if ch["id"] == self.host or singing else 0.7)
        rr = random.Random(zlib.crc32(f"{ch['id']}{int(t / 3.3)}".encode()))
        blink = (t + rr.random() * 3) % 3.3 > 3.15
        look = 0.0
        if not singing and who and who in self.by_id:
            sx = self.by_id[who]["base"][0] - ch["base"][0]
            look = max(-0.6, min(0.6, sx * 0.15))
        wave = d.get("wave", 0) * (1 if (t % (self.beat_len * 8)) < self.beat_len * 2 else 0)
        mi = self.mq[f] if (singing and f < len(self.mq)) else 0
        return {"singing": singing, "energy": e, "blink": blink, "look": look, "wave": wave, "mouth": mi, "jump": d.get("jump", 0)}

    def sprite_for(self, ch, st, rel_yaw, t):
        """Pick (path, mask_path, mirror) from the character's library."""
        av = ch["man"]["available"]
        ang, mirror = "front", False
        if abs(rel_yaw) > 0.3 and "q" in av:
            ang, mirror = "q", rel_yaw < 0
        lib = av.get(ang) or av["front"]
        if st["wave"] and "wave" in lib: lp = "wave"
        elif st["energy"] >= 0.75 and "dance" in lib: lp = "dance"
        elif "idle" in lib: lp = "idle"
        else: lp = next(iter(lib))
        if lp not in lib and ang != "front": ang, mirror, lib = "front", False, av["front"]
        info = lib[lp]; n = info["n"]
        fi = int(((t / self.bar_len) % 1.0) * n) % n
        mouths = info["mouths"]; want = HC.MOUTHS[st["mouth"]]
        mi = min(range(len(mouths)), key=lambda k: abs(mouths[k] - want))
        name = f"{lp}_m{mi}_{fi:02d}"
        if st["blink"] and info.get("blink"):
            bmi = min(info["blink"], key=lambda k: abs(mouths[k] - want))
            name = f"{lp}_b_m{bmi}_{fi:02d}"
        p = os.path.join(ch["dir"], ang, name + ".png")
        if not os.path.exists(p): p = os.path.join(ch["dir"], ang, f"{lp}_m{mi}_{fi:02d}.png")
        k = p[:-4] + "_k.png"
        return p, (k if ch["man"].get("mask") and os.path.exists(k) else None), mirror

    def color_at(self, ch, t):
        sched = ch["sched"]
        ch["_pair"] = None
        if not sched: return None, 99.0
        idx = -1
        for k, (t0, _) in enumerate(sched):
            if t0 <= t: idx = k
            else: break
        if idx < 0: return ch["home"], 99.0
        t0, cur = sched[idx]
        prev = sched[idx - 1][1] if idx > 0 else ch["home"]
        k = smoothstep((t - t0) / 0.25)
        a, b = srgb_to_lin(prev), srgb_to_lin(cur)       # blend in linear like the Blender material
        ch["_pair"] = (prev, cur, k)
        return lin_to_srgb(tuple(x + (y - x) * k for x, y in zip(a, b))), t - t0

    # ---------------------------------------------------------- images
    def load(self, path, mode="RGBA"):
        k = ("img", path)
        im = self.img_cache.get(k)
        if im is None:
            im = Image.open(path).convert(mode); im.load()
            self.img_cache.put(k, im, im.width * im.height * len(mode))
        return im

    def recolored(self, path, mpath, home, target, pair=None):
        tk = tuple(round(x * 64) for x in target)
        k = ("rc", path, tk)
        im = self.img_cache.get(k)
        if im is not None: return im
        src = self.load(path); msk = np.asarray(self.load(mpath, "RGBA"), dtype=np.float32)
        m = (msk[..., 0] / 255.0) * (msk[..., 3] / 255.0)
        a = np.asarray(src, dtype=np.float32) / 255.0
        rgb = a[..., :3]
        h, s, v = rgb_to_hsv_np(rgb)
        ch_dir = os.path.dirname(os.path.dirname(path))
        cal_h, cal_t = self.calib(ch_dir, mpath, home), self.calib(ch_dir, mpath, target)
        if pair and 0 < pair[2] < 1:   # mid-transition: blend the two measured colors (hue the short way round)
            ca, cb = self.calib(ch_dir, mpath, pair[0]), self.calib(ch_dir, mpath, pair[1])
            if ca and cb:
                k = pair[2]; dh = ((cb[0] - ca[0] + 0.5) % 1.0) - 0.5
                cal_t = ((ca[0] + dh * k) % 1.0, ca[1] + (cb[1] - ca[1]) * k, ca[2] + (cb[2] - ca[2]) * k)
        if cal_h and cal_t:      # measured from real renders of the jelly in both colors (sprites.py calib/)
            (hh, hs, hv), (th, ts, tv) = cal_h, cal_t
            gain = 1.0
        else:                    # fallback: shift by the hex colors, keep perceived brightness roughly right
            hh, hs, hv = colorsys.rgb_to_hsv(*home); th, ts, tv = colorsys.rgb_to_hsv(*target)
            lum = lambda c: 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]
            gain = (lum(srgb_to_lin(target)) / max(1e-3, lum(srgb_to_lin(home)))) ** 0.22
        dh = ((th - hh + 0.5) % 1.0) - 0.5
        h2 = (h + dh) % 1.0
        s2 = np.clip(s * (ts / max(hs, 1e-3)), 0, 1)
        v2 = np.clip(v * (tv / max(hv, 1e-3)) * gain, 0, 1)
        if ts < 0.15:   # white/grey targets: fade saturation instead of rotating
            s2 = s * ts / max(hs, 1e-3)
        rc = hsv_to_rgb_np(h2, s2, v2)
        out = rgb * (1 - m[..., None]) + rc * m[..., None]
        arr = np.concatenate([out, a[..., 3:4]], axis=-1)
        im = Image.fromarray((arr * 255 + 0.5).astype(np.uint8), "RGBA")
        self.img_cache.put(k, im, im.width * im.height * 4)
        return im

    def calib(self, ch_dir, mpath, rgb):
        """Measured (h, s, v) of the masked jelly in the calibration render nearest to `rgb` (None if none is close)."""
        cdir = os.path.join(ch_dir, "calib")
        if not os.path.isdir(cdir): return None
        cands = getattr(self, "_calib_list", {}).get(cdir)
        if cands is None:
            cands = [(fn[:-4], hex_rgb(fn[:-4])) for fn in os.listdir(cdir) if fn.endswith(".png")]
            self._calib_list = getattr(self, "_calib_list", {}); self._calib_list[cdir] = cands
        if not cands: return None
        hx, c = min(cands, key=lambda kc: sum((a - b) ** 2 for a, b in zip(kc[1], rgb)))
        if sum((a - b) ** 2 for a, b in zip(c, rgb)) > 0.06 ** 2: return None
        k = ("cal", cdir, hx)
        v = self.img_cache.get(k)
        if v is None:
            ref_mask = os.path.join(ch_dir, "front", "dance_m0_00_k.png")
            im = np.asarray(Image.open(os.path.join(cdir, hx + ".png")).convert("RGBA"), dtype=np.float32) / 255.0
            mk = np.asarray(Image.open(ref_mask).convert("RGBA"), dtype=np.float32) / 255.0
            sel = (mk[..., 0] * mk[..., 3] > 0.9) & (im[..., 3] > 0.9)
            hh, ss, vv = rgb_to_hsv_np(im[..., :3][sel])
            ang = hh * 2 * np.pi
            hm = (math.atan2(np.sin(ang).mean(), np.cos(ang).mean()) / (2 * np.pi)) % 1.0
            v = (hm, float(np.median(ss)), float(np.median(vv)))
            self.img_cache.put(k, v, 64)
        return v

    def plate(self, name):
        pl = self.setman["plates"].get(name)
        if pl is None: return None, None
        if name not in self.plate_cache:
            self.plate_cache[name] = Image.open(os.path.join(self.setdir, pl["file"])).convert("RGB")
        return self.plate_cache[name], pl

    def _make_shadow_stamp(self):
        s = Image.new("L", (256, 256), 0); ImageDraw.Draw(s).ellipse((40, 40, 216, 216), fill=255)
        return s.filter(ImageFilter.GaussianBlur(26))

    def foot_radius(self, ch):
        """World radius of the contact shadow, measured once from the sprite's alpha near the ground."""
        if ch["foot_r"] is None:
            man = ch["man"]; av = man["available"]["front"]; lp = "dance" if "dance" in av else next(iter(av))
            a = np.asarray(self.load(os.path.join(ch["dir"], "front", f"{lp}_m0_00.png")))[..., 3]
            ay = int(man["anchor"][1]); band = a[max(0, ay - int(man["ppu"] * 0.9)):ay + 2]
            cols = np.where(band.max(axis=0) > 40)[0]
            w = (cols[-1] - cols[0]) if len(cols) else man["ppu"]
            ch["foot_r"] = 0.5 * w / man["ppu"] * 0.95
        return ch["foot_r"]

    def ground_gap(self, path, man):
        k = ("gap", path)
        g = self.img_cache.get(k)
        if g is None:
            a = np.asarray(self.load(path))[..., 3]
            rows = np.where(a.max(axis=1) > 60)[0]
            g = max(0.0, (man["anchor"][1] - (rows[-1] if len(rows) else man["anchor"][1])) / man["ppu"])
            self.img_cache.put(k, g, 64)
        return g

    # ---------------------------------------------------------- view (shot -> plate + 2D camera move)
    def view(self, t):
        shot, u, d, ci = self.cut_at(t)
        us = smoothstep(u)
        par = 0.0
        if shot.startswith("close"):
            cid = shot.split(":")[1] if ":" in shot else self.host
            ch = self.by_id.get(cid, self.by_id[self.host])
            side = "R" if zlib.crc32(cid.encode()) % 2 else "L"
            name = f"close_{ch['spot']}_{side}" if isinstance(ch["spot"], str) else None
            img, pl = self.plate(name) if name else (None, None)
            bx, by, bz = ch["base"]; fz = bz + ch["man"]["face_z"] * ch["scale"]
            if img is None:      # no close plate for this spot: crop the wide plate around the face, background softened
                img, pl = self.plate("wide")
                cx, cy, _ = HC.project((bx, by, fz - 0.1), pl)
                _, ty, _ = HC.project((bx, by, fz + 1.0), pl)
                ppu = cy - ty
                vw = ppu * 3.4 / self.H * self.W * ch["scale"] / (1 + 0.1 * us)
                return dict(img=img, pl=pl, cx=cx, cy=cy - ppu * 0.15, vw=vw, par=0.0, shot=shot, u=u, d=d, blur=True, ci=ci)
            # frame the singer like engine.py's close-up (distance close_dist*scale, slow push-in of 0.6 units)
            cx, cy, _ = HC.project((bx, by, fz - 0.1 * ch["scale"]), pl)
            dist_eng = (ch["man"].get("close_dist", 6.4) - 0.6 * us) * ch["scale"]
            zoom = pl.get("dist", 6.4) / max(1.0, dist_eng)
            pw, ph = pl["res"]; vw = pw / self.setman["pad"] / zoom
            vw = min(vw, pw); vh = vw * self.H / self.W
            ccx = min(max(cx, vw / 2), pw - vw / 2); ccy = min(max(cy, vh / 2), ph - vh / 2)
            return dict(img=img, pl=pl, cx=ccx, cy=ccy, vw=vw, par=0.0, shot=shot, u=u, d=d, ci=ci)
        img, pl = self.plate(shot)
        if img is None: img, pl = self.plate("wide")
        pw, ph = pl["res"]; base_w = pw / self.setman["pad"]
        cx, cy = pw / 2, ph / 2
        if shot == "orbit":                # camera swings left -> right: pan the plate, sprites slide a bit more (parallax)
            span = (pw - base_w) * 0.5 * 0.9
            off = (-1 + 2 * us) * span; cx += off; par = -off * 0.18
            vw = base_w / 1.02
        elif shot == "low":                # camera trucks right -> left
            span = (pw - base_w) * 0.5 * 0.8
            off = (1 - 2 * us) * span; cx += off; par = -off * 0.15
            vw = base_w
        else:                               # named cams + top: slow push-in toward the aim point
            tx, ty, _ = HC.project(tuple(pl["aim"]), pl)
            zoom = 1 + 0.12 * us
            cx = cx + (tx - cx) * (1 - 1 / zoom); cy = cy + (ty - cy) * (1 - 1 / zoom)
            vw = base_w / zoom
        return dict(img=img, pl=pl, cx=cx, cy=cy, vw=vw, par=par, shot=shot, u=u, d=d, ci=ci)

    # ---------------------------------------------------------- one frame
    def frame(self, f):
        t = f / self.fps; W, H = self.W, self.H
        if FULL3D and t < FULL3D_UNTIL:      # splice: full-3D frames from engine.py for the hook
            fp = os.path.join(FULL3D, f"{f:05d}.png")
            if os.path.exists(fp):
                im = Image.open(fp).convert("RGB")
                return im if im.size == (W, H) else im.resize((W, H), Image.LANCZOS)
        v = self.view(t); pl = v["pl"]; img = v["img"]
        vw = v["vw"]; vh = vw * H / W
        x0, y0 = v["cx"] - vw / 2, v["cy"] - vh / 2
        canvas = img.resize((W, H), Image.BICUBIC, box=(x0, y0, x0 + vw, y0 + vh))
        if v.get("blur"): canvas = canvas.filter(ImageFilter.GaussianBlur(H / 140))
        canvas = canvas.convert("RGBA")
        k = W / vw                                     # plate px -> output px
        to_out = lambda px, py: ((px - x0) * k, (py - y0) * k)
        d = v["d"]
        layers = []
        for ch in self.cast:
            st = self.state(ch, f, t, d)
            bx, by, bz = ch["base"]
            ax, ay, depth = HC.project((bx, by, bz), pl)
            _, hy, _ = HC.project((bx, by, bz + 1.0), pl)
            ppu_out = (ay - hy) * k * ch["scale"]
            if ppu_out <= 0.5: continue
            rel = (ch["yaw"] - st["look"]) - HC.view_yaw(pl, (bx, by, bz))
            path, mpath, mirror = self.sprite_for(ch, st, rel, t)
            col, dt = self.color_at(ch, t)
            pop = math.exp(-dt * 5.0) * math.sin(dt * 26) * 0.14 if dt < 1.2 else 0.0
            ox, oy = to_out(ax, ay); ox += v["par"] * k
            layers.append(("char", depth, ch, st, path, mpath, mirror, col, pop, ox, oy, ppu_out))
        for pr in self.props:
            s = self.prop_scale(pr, t)
            if s <= 0.01: continue
            ax, ay, depth = HC.project(pr["at"], pl)
            _, hy, _ = HC.project((pr["at"][0], pr["at"][1], pr["at"][2] + 1.0), pl)
            ox, oy = to_out(ax, ay); ox += v["par"] * k * 0.8
            layers.append(("prop", depth, pr, s, ox, oy, (ay - hy) * k, t))
        # contact shadows first (they sit on the floor under everyone)
        for L in layers:
            if L[0] != "char": continue
            _, depth, ch, st, path, mpath, mirror, col, pop, ox, oy, ppu_out = L
            bx, by, bz = ch["base"]; r = self.foot_radius(ch) * ch["scale"]
            gap = self.ground_gap(path, ch["man"]) * ch["scale"]
            pts = [to_out(*HC.project(p, pl)[:2]) for p in ((bx - r, by, bz), (bx + r, by, bz), (bx, by - r * 0.8, bz), (bx, by + r * 0.8, bz))]
            sw = abs(pts[1][0] - pts[0][0]) * (1 - 0.25 * min(1, gap / 0.5)) * 1.25
            sh = max(4.0, abs(pts[3][1] - pts[2][1]) * 1.25 + sw * 0.06)
            alpha = 0.42 * (1 - 0.5 * min(1, gap / 0.5))
            sx0 = int(ox - sw / 2); sy0 = int(oy - sh / 2)
            if sw < 2 or sh < 2: continue
            stamp = self.shadow_stamp.resize((max(1, int(sw)), max(1, int(sh))), Image.BILINEAR)
            stamp = stamp.point(lambda x, a=alpha: int(x * a))
            canvas.paste((38, 18, 60, 255), (sx0, sy0), stamp)
        layers.sort(key=lambda L: -L[1])
        for L in layers:
            if L[0] == "char":
                _, depth, ch, st, path, mpath, mirror, col, pop, ox, oy, ppu_out = L
                man = ch["man"]
                im = self.recolored(path, mpath, ch["home"], col, ch.get("_pair")) if (mpath and col is not None) else self.load(path)
                s = ppu_out / man["ppu"]; sq = 1 + pop
                kx = s / math.sqrt(sq) * (-1 if mirror else 1); ky = s * sq
                self.blit(canvas, im, man["anchor"], ox, oy, kx, ky)
            else:
                _, depth, pr, s, ox, oy, ppu_out, tt = L
                src = pr["src"]
                im = src["img"] if src["kind"] == "image" else self.load(src["path"])
                sc = ppu_out / src["ppu"] * s
                spin = abs(math.cos(math.sin(tt * 1.3) * pr["spin"]))
                self.blit(canvas, im, src["anchor"], ox, oy, sc * max(0.35, spin), sc)
        return canvas.convert("RGB")

    @staticmethod
    def blit(canvas, im, anchor, ox, oy, kx, ky):
        """Affine-place sprite `im` so its anchor pixel lands at (ox, oy), scaled by kx (negative = mirrored), ky."""
        if abs(kx) < 1e-3 or ky < 1e-3: return
        axs, ays = anchor
        fac = int(0.75 / max(abs(kx), ky)) if max(abs(kx), ky) < 0.6 else 1
        if fac > 1:           # strong downscale: pre-shrink so bicubic does not alias
            im = im.reduce(fac); axs /= fac; ays /= fac; kx *= fac; ky *= fac
        sw, sh = im.size
        xs = sorted((ox + (0 - axs) * kx, ox + (sw - axs) * kx)); ys = (oy + (0 - ays) * ky, oy + (sh - ays) * ky)
        bx0, by0 = max(0, int(math.floor(xs[0]))), max(0, int(math.floor(ys[0])))
        bx1, by1 = min(canvas.width, int(math.ceil(xs[1]))), min(canvas.height, int(math.ceil(ys[1])))
        if bx1 <= bx0 or by1 <= by0: return
        a = 1 / kx; e = 1 / ky
        c = axs + (bx0 + 0.5 - ox) * a - 0.5; f_ = ays + (by0 + 0.5 - oy) * e - 0.5
        part = im.transform((bx1 - bx0, by1 - by0), Image.AFFINE, (a, 0, c, 0, e, f_), resample=Image.BICUBIC)
        canvas.alpha_composite(part, (bx0, by0))


# ------------------------------------------------------------------ numpy HSV
def rgb_to_hsv_np(rgb):
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    mx = rgb.max(-1); mn = rgb.min(-1); df = mx - mn
    h = np.zeros_like(mx)
    m = df > 1e-6
    rc = np.where(m, (mx - r) / np.where(m, df, 1), 0); gc = np.where(m, (mx - g) / np.where(m, df, 1), 0); bc = np.where(m, (mx - b) / np.where(m, df, 1), 0)
    h = np.where(r == mx, bc - gc, np.where(g == mx, 2.0 + rc - bc, 4.0 + gc - rc))
    h = np.where(m, (h / 6.0) % 1.0, 0)
    s = np.where(mx > 1e-6, df / np.where(mx > 1e-6, mx, 1), 0)
    return h, s, mx


def hsv_to_rgb_np(h, s, v):
    i = np.floor(h * 6.0); f = h * 6.0 - i; i = i.astype(np.int32) % 6
    p = v * (1 - s); q = v * (1 - s * f); t = v * (1 - s * (1 - f))
    r = np.choose(i, [v, q, p, p, t, v]); g = np.choose(i, [t, v, v, q, p, p]); b = np.choose(i, [p, p, t, v, v, q])
    return np.stack([r, g, b], -1)


# ================================================================== drivers
def encode_range(job_path, res, assets, f0, f1, out_mp4, crf, report=None):
    ep = Episode(job_path, res, assets)
    W, H = res
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(ep.fps),
                          "-i", "-", "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", str(crf), "-pix_fmt", "yuv420p", out_mp4],
                         stdin=subprocess.PIPE)
    t0 = time.time()
    for f in range(f0, f1):
        p.stdin.write(ep.frame(f).tobytes())
        if report and (f - f0) % 96 == 95:
            el = time.time() - t0; print(f"[{report}] frame {f}/{f1}  {(f - f0 + 1) / el:.1f} fps", flush=True)
    p.stdin.close(); p.wait()
    return time.time() - t0


def _worker(a):
    return encode_range(*a)


def main():
    if not opt("job"): sys.exit(__doc__)
    job_path = os.path.abspath(opt("job")); job = json.load(open(job_path))
    W, H = map(int, str(opt("res", job.get("res", "1920x1080"))).split("x"))
    assets = os.path.abspath(opt("assets", HC.ASSETS))
    out = os.path.abspath(opt("out", os.path.join(HERE, "out", job["id"] + "_hybrid"))); os.makedirs(out, exist_ok=True)
    t_start = time.time()
    ep = Episode(job_path, (W, H), assets)
    print(f"loaded in {time.time() - t_start:.2f}s: {len(ep.cast)} cast, {len(ep.props)} props, {len(ep.cuts)} cuts", flush=True)
    if opt("test"):
        fl = [int(x) for x in str(opt("frames", f"{ep.fps * 2},{ep.nf // 3},{ep.nf // 2},{ep.nf * 3 // 4}")).split(",")]
        for f in fl:
            t0 = time.time(); im = ep.frame(min(f, ep.nf - 1))
            fp = os.path.join(out, f"test_{f:05d}.png"); im.save(fp); print("TEST", fp, f"{time.time() - t0:.3f}s", flush=True)
        if opt("sheet"): contact_sheet([os.path.join(out, f"test_{f:05d}.png") for f in fl], os.path.join(out, "test_sheet.png"), fl, ep.fps)
        return
    if opt("seconds"):
        a, b = map(float, str(opt("seconds")).split("-"))
        f0, f1 = int(round(a * ep.fps)), min(ep.nf, int(round(b * ep.fps)))
        final = os.path.abspath(opt("outfile", os.path.join(out, f"{job['id']}_{a:g}-{b:g}.mp4")))
    else:
        f0, f1 = 0, ep.nf; a = 0.0
        final = os.path.abspath(opt("outfile", os.path.join(out, job["id"] + "_raw.mp4")))
    os.makedirs(os.path.dirname(final), exist_ok=True)
    workers = max(1, int(opt("workers", min(2, os.cpu_count() or 1))))
    crf = int(opt("crf", 18))
    tmp = os.path.join(out, "_seg"); shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
    edges = [f0 + (f1 - f0) * i // workers for i in range(workers + 1)]
    segs = [os.path.join(tmp, f"seg{i}.mp4") for i in range(workers)]
    args = [(job_path, (W, H), assets, edges[i], edges[i + 1], segs[i], crf, f"w{i}") for i in range(workers)]
    t_comp = time.time()
    if workers == 1: _worker(args[0])
    else:
        import multiprocessing as mp
        with mp.get_context("fork").Pool(workers) as pool: pool.map(_worker, args)
    comp_s = time.time() - t_comp
    lst = os.path.join(tmp, "list.txt"); open(lst, "w").write("".join(f"file '{s}'\n" for s in segs))
    audio = os.path.join(ep.job_dir, job["audio"]) if job.get("audio") else None
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst]
    if audio and os.path.exists(audio):
        cmd += ["-ss", f"{f0 / ep.fps:.3f}", "-t", f"{(f1 - f0) / ep.fps:.3f}", "-i", audio, "-map", "0:v", "-map", "1:a", "-c:a", "aac", "-b:a", "192k"]
    cmd += ["-c:v", "copy", "-movflags", "+faststart", final]
    subprocess.run(cmd, check=True)
    shutil.rmtree(tmp, ignore_errors=True)
    n = f1 - f0
    print(f"DONE {final}  {n} frames in {comp_s:.1f}s compose+encode ({n / comp_s:.1f} fps, {workers} workers); total {time.time() - t_start:.1f}s", flush=True)
    if opt("sheet"):
        step = max(1, n // 12); fl = list(range(f0 + step // 2, f1, step))[:12]
        paths = []
        for f in fl:
            fp = os.path.join(out, f"_sheet_{f:05d}.png"); ep.frame(f).save(fp); paths.append(fp)
        sp = os.path.splitext(final)[0] + "_sheet.png"
        contact_sheet(paths, sp, fl, ep.fps)
        for p_ in paths: os.remove(p_)
        print("SHEET", sp)


def contact_sheet(paths, out_path, frames, fps, cols=4):
    ims = [Image.open(p).convert("RGB") for p in paths]
    w, h = ims[0].size; tw = 480; th = int(h * tw / w)
    rows = (len(ims) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tw + (cols + 1) * 8, rows * (th + 30) + 8), (24, 20, 36))
    dr = ImageDraw.Draw(sheet)
    try: fnt = ImageFont.truetype(os.path.join(HERE, "fonts", "Poppins-Bold.ttf"), 16)
    except Exception: fnt = None
    for i, (im, f) in enumerate(zip(ims, frames)):
        x = 8 + (i % cols) * (tw + 8); y = 8 + (i // cols) * (th + 30)
        sheet.paste(im.resize((tw, th), Image.LANCZOS), (x, y))
        dr.text((x + 4, y + th + 4), f"f{f}  {f / fps:.2f}s", fill=(230, 220, 255), font=fnt)
    sheet.save(out_path)


if __name__ == "__main__":
    main()
