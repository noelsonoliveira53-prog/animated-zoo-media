"""Channel watermark for The Animated Zoo (Noelson, Nov 16 2026: "include watermark on all videos on upload with the channel
characteristics"). YouTube's own channel watermark (Studio > Customization > Branding) is not shown on made-for-kids videos
(support.google.com/youtube/answer/10456525, read Nov 16), so the mark is part of the picture.
The mark: the channel's own picture (brand/avatar.png: Milo on yellow) in a white ring + the channel name in the channel font
(Baloo 2 ExtraBold, white with the captions' dark-brown outline), at 88% opacity.

  python3 watermark.py build                               -> brand/zoo/watermark.png (16:9, drawn for 3840x2160) and watermark_short.png (9:16, for 2160x3840)
  python3 watermark.py still <video> <seconds> <out.png>   -> one frame with the mark, to look at before an encode
  python3 watermark.py apply <in.mp4> <out.mp4> [tl|tr]    -> re-encode a finished file that has no mark yet (sound copied)
  python3 watermark.py check <video> [tl|tr]               -> "MARK yes/no": is the mark in the picture? (review.py fails a video without it)
  python3 watermark.py corner <video> <out.jpg> [tl|tr]    -> the mark's corner every 5 s on one sheet: LOOK at it (no face, sign or word under the mark)

finish.py and lesson_shorts.py call chain() so every new video and Short gets the mark when it is finished.
16:9: top left ("tl", default), 40 px from the edges at 4K, 136 px high (6% of the picture): above the answer signs (they start 8% from
the top), away from the captions (bottom). If the corner sheet shows a face or a sign under it, set the job's "watermark_pos": "tr".
9:16: centred in the free band above the Short's title. Thumbnails stay without the mark."""
import os, sys, subprocess, json

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
FONT = os.path.join(HERE, "fonts", "Baloo2-ExtraBold.ttf")
WM = os.path.join(REPO, "brand", "zoo", "watermark.png"); WM_SHORT = os.path.join(REPO, "brand", "zoo", "watermark_short.png")
NAME = "The Animated Zoo"
OPACITY = 0.88
MX, MY, SHORT_Y = 40, 36, 232          # margins of the 16:9 mark at 3840x2160; top of the 9:16 mark at 2160x3840


def build_one(path, badge, font_px, gap, ring, outline):
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
    S = 3                                                       # draw 3x and scale down: clean edges
    av = Image.open(os.path.join(REPO, "brand", "avatar.png")).convert("RGB").crop((70, 110, 710, 750))   # Milo fills the disc
    D = badge * S; r = ring * S
    disc = av.resize((D - 2 * r, D - 2 * r), Image.LANCZOS)
    mask = Image.new("L", disc.size, 0); ImageDraw.Draw(mask).ellipse([0, 0, disc.size[0] - 1, disc.size[1] - 1], fill=255)
    font = ImageFont.truetype(FONT, font_px * S)
    tw = int(font.getlength(NAME)); ol = outline * S
    pad = 10 * S
    W = pad + D + gap * S + tw + 2 * ol + pad; H = D + 2 * pad
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ds = ImageDraw.Draw(sh)      # soft shadow under the whole mark
    ds.ellipse([pad, pad + 3 * S, pad + D, pad + D + 3 * S], fill=(40, 20, 10, 110))
    tx = pad + D + gap * S + ol; asc, desc = font.getmetrics(); ty = pad + (D - (asc + desc)) // 2 - 2 * S
    ds.text((tx, ty + 4 * S), NAME, font=font, fill=(40, 20, 10, 120), stroke_width=ol, stroke_fill=(40, 20, 10, 120))
    im = Image.alpha_composite(im, sh.filter(ImageFilter.GaussianBlur(3 * S))); dr = ImageDraw.Draw(im)
    dr.ellipse([pad, pad, pad + D, pad + D], fill=(255, 255, 255, 255))
    im.paste(disc, (pad + r, pad + r), mask)
    dr.text((tx, ty), NAME, font=font, fill=(255, 255, 255, 255), stroke_width=ol, stroke_fill=(0x40, 0x20, 0x10, 255))
    im = im.resize((W // S, H // S), Image.LANCZOS)
    im.save(path); print(path, im.size)


def build():
    build_one(WM, badge=116, font_px=74, gap=16, ring=7, outline=7)
    build_one(WM_SHORT, badge=150, font_px=104, gap=22, ring=9, outline=10)


def kind_of(w, h): return "short" if h > w else "wide"


def wm_file(kind):
    p = WM_SHORT if kind == "short" else WM
    if not os.path.exists(p): build()
    return p


def place(kind, W, pos="tl"):
    """(scale, x, y, w, h) of the mark on a picture W wide (numbers, in that picture's pixels)."""
    from PIL import Image
    full = 2160 if kind == "short" else 3840; k = W / full
    mw, mh = Image.open(wm_file(kind)).size; mw, mh = int(round(mw * k)), int(round(mh * k))
    if kind == "short": return k, (W - mw) // 2, int(round(SHORT_Y * k)), mw, mh
    x = int(round(MX * k)) if pos != "tr" else W - mw - int(round(MX * k))
    return k, x, int(round(MY * k)), mw, mh


def chain(src_label, out_label, kind, wm_input=1, W=None, pos="tl"):
    """filter_complex piece: lays the mark (ffmpeg input number wm_input) on [src_label] -> [out_label]."""
    k, x, y, mw, mh = place(kind, W or (2160 if kind == "short" else 3840), pos)
    return (f"[{wm_input}:v]scale={mw}:{mh}:flags=lanczos,format=rgba,colorchannelmixer=aa={OPACITY}[zwm];"
            f"[{src_label}][zwm]overlay={x}:{y}:format=auto[{out_label}]")


def probe(p):
    o = json.loads(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height,codec_name:format=duration,bit_rate",
                                   "-of", "json", p], capture_output=True, text=True).stdout)
    s = o["streams"][0]; return s["width"], s["height"], s["codec_name"], float(o["format"]["duration"]), int(o["format"]["bit_rate"])


def still(video, t, out, pos="tl"):
    w, h, *_ = probe(video); k = kind_of(w, h)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(t), "-i", video, "-i", wm_file(k), "-filter_complex", chain("0:v", "v", k, 1, w, pos),
                    "-map", "[v]", "-frames:v", "1", out], check=True)


def apply(src, out, pos="tl"):
    """A finished file without the mark -> the same picture with it. One more encode, at the source's bitrate (4K AV1 for the long
    videos) or crf 18 (x264 Shorts); the sound is copied untouched."""
    w, h, codec, dur, br = probe(src); k = kind_of(w, h)
    assert not has_mark(src, pos), f"{src} already has the mark"
    base = ["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-i", wm_file(k), "-filter_complex", chain("0:v", "v", k, 1, w, pos), "-map", "[v]", "-map", "0:a?", "-c:a", "copy"]
    if codec == "av1":
        vb = min(int(br - 192e3), int(((94 * 8 * 1e6) / dur - 192e3) * 0.96))
        enc = ["-c:v", "libsvtav1", "-preset", "9", "-b:v", str(vb), "-svtav1-params", "tune=0", "-g", "240", "-pix_fmt", "yuv420p10le"]
    else:
        enc = ["-c:v", "libx264", "-preset", "medium", "-crf", "18", "-maxrate", "40M", "-bufsize", "80M", "-pix_fmt", "yuv420p"]
    subprocess.run(base + enc + ["-movflags", "+faststart", out], check=True)
    if os.path.getsize(out) >= 95e6 and codec != "av1":
        enc[enc.index("-crf") + 1] = "23"; enc[enc.index("-maxrate") + 1] = "8M"; enc[enc.index("-bufsize") + 1] = "16M"
        subprocess.run(base + enc + ["-movflags", "+faststart", out], check=True)
    assert os.path.getsize(out) < 100e6, f"{out} is over 100 MB"
    w2, h2, _, d2, _ = probe(out); assert (w2, h2) == (w, h) and abs(d2 - dur) < 0.2, f"{out}: {w2}x{h2} {d2} s, source {w}x{h} {dur} s"
    assert has_mark(out, pos), f"{out}: the mark is not in the picture"
    print(f"WATERMARKED {out}: {w2}x{h2}, {d2:.1f} s, {os.path.getsize(out) / 1e6:.1f} MB")


def has_mark(video, pos="tl", verbose=False):
    """Is the mark in the picture? Looks at 5 frames: where the mark's letters are white the picture must be bright, where their
    outline is dark brown it must be dark, and the disc's yellow must be yellow. True when 4 of 5 frames agree."""
    from PIL import Image
    import io
    w, h, _, dur, _ = probe(video); k = kind_of(w, h); sc, x, y, mw, mh = place(k, w, pos)
    m = Image.open(wm_file(k)).convert("RGBA").resize((mw, mh), Image.LANCZOS); px = m.load()
    white = [(i, j) for j in range(0, mh, 2) for i in range(0, mw, 2) if px[i, j][3] > 250 and min(px[i, j][:3]) > 245 and i > mh]
    brown = [(i, j) for j in range(0, mh, 2) for i in range(0, mw, 2) if px[i, j][3] > 250 and max(px[i, j][:3]) < 80 and i > mh]
    yel = [(i, j) for j in range(0, mh, 2) for i in range(0, mh, 2) if px[i, j][3] > 250 and px[i, j][0] > 230 and px[i, j][2] < 110]
    hits = 0
    for f in (0.12, 0.3, 0.5, 0.7, 0.88):
        raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-ss", f"{dur * f:.2f}", "-i", video, "-frames:v", "1", "-vf", f"crop={mw}:{mh}:{x}:{y}",
                              "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True).stdout
        if not raw: continue
        fp = Image.open(io.BytesIO(raw)).convert("RGB").load()
        lum = lambda c: 0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]
        a = sum(lum(fp[i, j]) for i, j in white) / max(1, len(white)); b = sum(lum(fp[i, j]) for i, j in brown) / max(1, len(brown))
        yy = [fp[i, j] for i, j in yel]; c = sum(1 for q in yy if q[0] > 190 and q[1] > 150 and q[2] < 150) / max(1, len(yy))
        ok = a > 205 and b < 125 and c > 0.8; hits += ok
        if verbose: print(f"  {dur * f:6.1f} s: letters {a:.0f}, outline {b:.0f}, yellow {c:.2f} -> {'mark' if ok else 'no mark'}")
    return hits >= 4


def corner(video, out, pos="tl", step=5.0):
    """One sheet with the mark's corner every 5 s (the mark laid on if the video has none yet), to LOOK at: nothing that matters
    (a face, an answer sign, a 3D word, an example) may sit under the mark."""
    w, h, _, dur, _ = probe(video); k = kind_of(w, h); sc, x, y, mw, mh = place(k, w, pos)
    cw, chh = min(w, int(mw * 1.45)), int(mh * 2.6); cx = max(0, min(w - cw, x - int(mw * 0.2))); n = int(dur // step) + 1; cols = 5; rows = -(-n // cols)
    marked = has_mark(video, pos)
    pre = "[0:v]null[m]" if marked else chain("0:v", "m", k, 1, w, pos)
    fc = f"{pre};[m]fps=1/{step},crop={cw}:{chh}:{cx}:0,scale=560:-1,tile={cols}x{rows}:padding=4:color=white[v]"
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", video] + ([] if marked else ["-i", wm_file(k)]) + ["-filter_complex", fc, "-map", "[v]", "-frames:v", "1", "-q:v", "3", out]
    subprocess.run(cmd, check=True); print(f"corner sheet: {out} ({n} frames, one every {step:g} s, row by row; the video {'has' if marked else 'has NOT'} the mark)")


if __name__ == "__main__":
    c = sys.argv[1]; a = sys.argv[2:]
    if c == "build": build()
    elif c == "still": still(a[0], a[1], a[2], *(a[3:4]))
    elif c == "apply": apply(a[0], a[1], *(a[2:3]))
    elif c == "check": r = has_mark(a[0], *(a[1:2]), verbose=True); print("MARK", "yes" if r else "no", a[0]); sys.exit(0 if r else 1)
    elif c == "corner": corner(a[0], a[1], *(a[2:3]))
