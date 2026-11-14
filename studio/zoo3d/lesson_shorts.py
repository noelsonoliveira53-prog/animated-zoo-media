"""Cut the fact Shorts out of a finished teaching lesson, in 4K vertical (2160x3840).
Noelson, Nov 14 2026: "Shorts should come only from teaching videos ... create all of them in 4K".

  python3 lesson_shorts.py <lesson_raw.mp4> <lesson id> [--only <short id>] [--out <dir>]

Uses the RAW 4K render (no burned captions) so the Short gets its own big captions, the lesson's own voice track
(jobs/<id>_song.wav) and the cut points teach.py stored in songs/<id>.json "shorts" (question -> answer -> example, 20-60 s).
Layout: blurred full-frame background, the centre 4:3 of the 4K picture across the full width (2160x1620, real 4K detail),
the question as a big title on top, the spoken line as a caption underneath. No calls to action.
Writes <repo>/shorts3d/<short id>.mp4 and adds/updates studio/upload_plan_shorts_zoo.json entries with status "hold_review".
"""
import json, os, sys, subprocess, textwrap

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
FONT = os.path.join(HERE, "fonts", "Baloo2-ExtraBold.ttf")
BOILER = ("The Animated Zoo makes gentle, colorful videos for little learners. New videos every day! Made with care for ages 2-6. "
          "Characters and visuals are animated with the help of AI tools and reviewed for kid safety before publishing.")


def arg(k, d=None): return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d
def ts(t):
    h, r = divmod(max(0, t), 3600); m, s = divmod(r, 60); return f"{int(h)}:{int(m):02d}:{s:05.2f}"


def make(raw, sid, sh, outdir):
    timing = json.load(open(os.path.join(HERE, "jobs", f"{sid}_timing.json")))
    a, b = sh["start"], sh["end"]; d = round(b - a, 2)
    assert 15 <= d <= 60, f"{sh['id']}: {d} s is outside 15-60 s"
    lines = [l for l in timing["lines"] if a - 0.05 <= l["start"] < b - 0.3]
    ass = os.path.join(outdir, sh["id"] + ".ass")
    with open(ass, "w") as f:
        f.write("[Script Info]\nScriptType: v4.00+\nPlayResX: 2160\nPlayResY: 3840\nWrapStyle: 0\n\n[V4+ Styles]\n"
                "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
                "Style: Cap,Baloo 2 ExtraBold,132,&H00FFFFFF,&H00FFFFFF,&H00102040,&H00000000,1,0,0,0,100,100,0,0,1,12,4,8,110,110,2700,1\n\n"
                "[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")
        for i, l in enumerate(lines):
            st = max(0.0, l["start"] - a); en = min(d, (lines[i + 1]["start"] - a) if i + 1 < len(lines) else l["end"] - a + 0.8)
            txt = "\\N".join(textwrap.wrap(l["text"], 26))
            f.write(f"Dialogue: 0,{ts(st)},{ts(en)},Cap,,0,0,0,,{txt}\n")
    out = os.path.join(outdir, sh["id"] + ".mp4")
    l1 = sh.get("l1", "").replace("'", "’").replace(":", "\\:"); l2 = sh.get("l2", "").replace("'", "’").replace(":", "\\:")
    s1 = min(230, int(2000 / max(1, len(l1) * 0.62))); s2 = min(330, int(2000 / max(1, len(l2) * 0.62)))
    fc = (f"[0:v]split[a][b];[a]scale=-2:3840,crop=2160:3840,boxblur=40:4,eq=brightness=-0.10:saturation=1.15[bg];"
          f"[b]crop=2880:2160:480:0,scale=2160:1620:flags=lanczos[fg];[bg][fg]overlay=0:1070,"
          f"drawbox=x=0:y=1058:w=2160:h=12:color=white@0.9:t=fill,drawbox=x=0:y=2690:w=2160:h=12:color=white@0.9:t=fill,"
          f"drawtext=fontfile={FONT}:text='{l1}':fontsize={s1}:fontcolor=white:borderw=18:bordercolor=0x402010:x=(w-tw)/2:y=470,"
          f"drawtext=fontfile={FONT}:text='{l2}':fontsize={s2}:fontcolor=0xFFD23F:borderw=22:bordercolor=0x402010:x=(w-tw)/2:y=710,"
          f"subtitles={ass}:fontsdir={os.path.join(HERE, 'fonts')},"
          f"fade=t=in:st=0:d=0.25,fade=t=out:st={d - 0.35}:d=0.35,format=yuv420p[v];"
          f"[1:a]afade=t=in:st=0:d=0.25,afade=t=out:st={d - 0.5}:d=0.5,loudnorm=I=-16:TP=-1.5[au]")
    cmd = ["ffmpeg", "-v", "error", "-y", "-ss", str(a), "-t", str(d), "-i", raw, "-ss", str(a), "-t", str(d), "-i", os.path.join(HERE, "jobs", f"{sid}_song.wav"),
           "-filter_complex", fc, "-map", "[v]", "-map", "[au]", "-r", "24", "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-maxrate", "40M", "-bufsize", "80M",
           "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", out]
    subprocess.run(cmd, check=True)
    # custom thumbnail (Noelson, Nov 14: every video gets its own thumbnail when it is posted): the moment the example is on
    # screen, same layout as the Short, its own 3 words (never the title's words), no captions. 1080x1920 PNG.
    tdir = os.path.join(REPO, "brand", "zoo", "shorts"); os.makedirs(tdir, exist_ok=True)
    thumb = os.path.join(tdir, "thumb_" + sh["id"] + ".png")
    tt = sh.get("thumb_text", "").replace("'", "\u2019").replace(":", "\\:"); st = min(330, int(1900 / max(1, len(tt) * 0.62)))
    tfc = (f"[0:v]split[a][b];[a]scale=-2:3840,crop=2160:3840,boxblur=40:4,eq=brightness=-0.12:saturation=1.2[bg];"
           f"[b]crop=2880:2160:480:0,scale=2160:1620:flags=lanczos,eq=saturation=1.15:contrast=1.05[fg];[bg][fg]overlay=0:1110,"
           f"drawbox=x=0:y=1098:w=2160:h=12:color=white@0.9:t=fill,drawbox=x=0:y=2730:w=2160:h=12:color=white@0.9:t=fill,"
           f"drawtext=fontfile={FONT}:text='{tt}':fontsize={st}:fontcolor=0xFFD23F:borderw=24:bordercolor=0x402010:x=(w-tw)/2:y=1190,scale=1080:1920:flags=lanczos")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(a + d * sh.get("thumb_at", 0.78)), "-i", raw, "-filter_complex", tfc, "-frames:v", "1", thumb], check=True)
    mb = os.path.getsize(out) / 1e6
    print(f"SHORT {sh['id']}: {d} s, 2160x3840, {mb:.1f} MB -> {out}")
    return out, d, thumb


def main():
    raw, sid = sys.argv[1], sys.argv[2]
    song = json.load(open(os.path.join(HERE, "songs", f"{sid}.json")))
    outdir = arg("--out", os.path.join(REPO, "shorts3d")); os.makedirs(outdir, exist_ok=True)
    only = arg("--only")
    planp = os.path.join(REPO, "studio", "upload_plan_shorts_zoo.json")
    plan = json.load(open(planp)) if os.path.exists(planp) else []
    items = plan if isinstance(plan, list) else (plan.get("items") or plan.get("shorts") or [])
    for sh in song.get("shorts", []):
        if only and sh["id"] != only: continue
        out, d, thumb = make(raw, sid, sh, outdir)
        rel = os.path.relpath(out, REPO)
        fact = next((x for x in song.get("lyrics", "").split("\n") if sh["seg"].replace("_", " ").split()[-1] in x.lower()), "")
        desc = f"{sh['title']} A quick animal fact for kids with Milo the bluebird, from the lesson “{song['meta']['title']}”.\n{fact}\n\n{BOILER}"
        ent = {"file": rel, "title": sh["title"], "description": desc, "tags": song["meta"].get("tags", [])[:8], "made_for_kids": True,
               "status": "hold_review", "format": "lesson_fact_short_4k", "from": sid, "seconds": d, "res": "2160x3840",
               "thumb": os.path.relpath(thumb, REPO), "thumb_text": sh.get("thumb_text", ""),
               "note": "interactive-lesson prototype: do not upload until Noelson approves the new format"}
        old = next((e for e in items if e.get("file") == rel), None)
        if old: old.update(ent)
        else: items.append(ent)
    json.dump(plan, open(planp, "w"), indent=1)


if __name__ == "__main__":
    main()
