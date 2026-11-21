"""What every cartoon episode file needs (episodes after zc_ep01 and za_ep01, which carry their own copies):
where a part of a character is on a stage, cameras for 16:9 and for 9:16, words placed in the picture, props.

    K = kit.Kit(STAGES)      K.P(place, who, part)   K.C(place, who, part, w)   K.V(place, who, part, h)   K.WV(place, [who, ...])
    kit.S(place, cam, say, words=[(at, text, fx, fy, k, cls, (pfx, pfy), pk)], pcam=..., ...)      kit.prop(name, fn, x, y, s, hidden, p=(x, y, s))
"""
from toon import shot

PT = {"milo": {"head": (0, -185), "body": (0, -150), "top": (0, -360), "feet": (0, 0)},
      "tumble": {"head": (320, -430), "eye": (382, -449), "body": (-14, -290), "top": (320, -620), "trunk": (500, -250), "tip": (550, -137), "mouth": (387, -327), "feet": (0, 0), "all": (90, -330)},
      "elephant": {"head": (300, -470), "eye": (352, -486), "body": (-14, -340), "top": (300, -640), "trunk": (470, -250), "tip": (492, -146), "mouth": (356, -384), "feet": (0, 0), "all": (80, -360)},
      "monkey": {"head": (0, -296), "body": (0, -150), "top": (0, -410), "feet": (0, 0), "all": (0, -200)},
      "calf": {"head": (379, -690), "body": (0, -353), "top": (379, -760), "feet": (0, 0), "all": (90, -400), "back": (0, -470)}}
PT["elephant_hat"] = PT["elephant"]
PT["elephant_mud"] = PT["elephant"]; PT["tumble_mud"] = PT["tumble"]
PT["monkey_hang"] = {"head": (0, 446), "body": (0, 300), "top": (0, 0), "feet": (0, 560), "all": (0, 290)}
# how far a character reaches around its feet (left, right, up), in its own units: for 9:16 views that must hold it whole
BOX = {"milo": (-150, 150, -380), "tumble": (-320, 590, -650), "elephant": (-320, 540, -660), "elephant_hat": (-320, 540, -800), "monkey": (-170, 170, -420), "calf": (-240, 470, -780), "camel": (-340, 490, -660)}
BOX["elephant_mud"] = BOX["elephant"]; BOX["tumble_mud"] = BOX["tumble"]


def W(c, k=1.05): return (c[0], c[1], round(c[2] * k))      # the end of a slow pull-out: a wide view only gets wider, so nobody slides out of the frame


class Kit:
    def __init__(self, stages): self.stages = stages

    def actor(self, place, who, stage=None): return next(a for a in (stage or self.stages[place]) if a[0] == who)

    def P(self, place, who, part="head", dx=0, dy=0, stage=None):
        a = self.actor(place, who, stage); kind, x, y, s = a[1], a[2], a[3], a[4]; flip = len(a) > 5 and a[5]; lx, ly = PT[kind][part]
        return round(x + (-lx if flip else lx) * s + dx), round(y + ly * s + dy)

    def C(self, place, who, part, w, dx=0, dy=0, stage=None): return (*self.P(place, who, part, dx, dy, stage), w)      # a 16:9 camera on a part

    def V(self, place, who, part, h, dx=0, dy=0, stage=None):      # a 9:16 camera: the subject sits a little below the middle, under the title
        x, y = self.P(place, who, part, dx, dy, stage); return (x, round(y - h * .05), h)

    def WV(self, place, whos, stage=None, floor=.77, top=.43, pad=.05, hmin=0):
        """A 9:16 camera that holds these characters whole: feet at `floor` of the height (above the caption), heads under `top` (under the title and the answer signs)."""
        x0 = y0 = 1e9; x1 = yf = -1e9
        for w in whos:
            a = self.actor(place, w, stage); kind, x, y, s = a[1], a[2], a[3], a[4]; flip = len(a) > 5 and a[5]; l, r, u = BOX[kind]
            if flip: l, r = -r, -l
            x0 = min(x0, x + l * s); x1 = max(x1, x + r * s); y0 = min(y0, y + u * s); yf = max(yf, y)
        h = max((x1 - x0) * (1 + 2 * pad) * 16 / 9, (yf - y0) / (floor - top), hmin)
        return (round((x0 + x1) / 2), round(yf - floor * h + h / 2), round(h))


def S(place, cam, say="", words=(), fx=(), pcam=None, **kw):
    """shot() plus words=[(at, text, fx, fy, k, cls, (pfx, pfy), pk)]: a word at a place in the PICTURE (fx, fy = 0..1 across the camera's view), sized to the camera.
    In the 9:16 version it sits at (pfx, pfy) of that view (default: the middle, just under the title)."""
    out = list(fx)
    for w in words:
        at, text, fx_, fy_ = w[:4]; k = w[4] if len(w) > 4 else 1.0; cls = w[5] if len(w) > 5 else ""; pf = w[6] if len(w) > 6 else (.5, .34); pk = w[7] if len(w) > 7 else min(k, 1.2)
        cx, cy, cw = cam; o = {"x": round(cx + (fx_ - .5) * cw), "y": round(cy + (fy_ - .5) * cw * 9 / 16), "size": round(cw * .068 * k), "cls": cls}
        pc = pcam or (cam[0], cam[1], cam[2] * 9 / 16 * 1.5); pw = pc[2] * 9 / 16
        o["p"] = {"x": round(pc[0] + (pf[0] - .5) * pw), "y": round(pc[1] + (pf[1] - .5) * pc[2]), "size": round(pw * .125 * pk)}
        out.append(("word", at, text, o))
    return shot(place, cam, say, fx=out, pcam=pcam, **kw)


def prop(name, fn, x, y, s=1.0, hidden=False, p=None): return (name, fn, x, y, s, "hidden" if hidden else "", p)   # p=(x, y, s): where it sits in the 9:16 picture
