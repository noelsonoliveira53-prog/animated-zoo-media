"""Finish a rendered 3D sing-along: karaoke lyrics, thumbnail, repo copy, upload-plan entry.

python3 finish.py <raw.mp4> <job.json> [--date YYYY-MM-DD] [--time "1:40 PM"] [--repo /home/claude/animated-zoo-media] [--nopush]

Needs next to the job: <id>_timing.json and songs/<id>.json (whose "meta" holds title, description, tags).
Writes <repo>/<channel folder>/<id>.mp4, <repo>/brand/<channel folder>/thumb_<id>.png and adds/updates the entry in
<repo>/studio/upload_plan_3d.json (status to_upload).
"""
import json, os, sys, subprocess, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(HERE, "fonts")
SLOT = {"truck": "1:40 PM", "bloop": "1:50 PM", "gizmo": "2:10 PM", "fruity": "2:20 PM", "moon": "7:00 PM", "zoo": "4:00 PM"}
HILITE = {"truck": "&H0000D7FF&", "bloop": "&H00FF66CC&", "fruity": "&H0040C0FF&", "moon": "&H00FFE0A0&", "gizmo": "&H00FFD040&", "zoo": "&H0000D7FF&"}

LOUD = "loudnorm=I=-14:TP=-1.5:LRA=11"   # YouTube reference loudness; set per channel in main()

def arg(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d

def ts(t):
    h, r = divmod(max(0, t), 3600); m, s = divmod(r, 60)
    return f"{int(h)}:{int(m):02d}:{s:05.2f}"

def clean_extra(timing):
    """Captions for improvised repeats come from speech-to-text: fix spelling against the lyrics (colours -> colors,
    'Mama has found' -> 'Mama is found') and drop transcription hallucinations ('Thanks for watching!')."""
    import difflib, re
    nrm = lambda x: re.sub(r"[^a-z ]", "", x.lower()).strip()
    lyr = [l for l in timing["lines"] if not l.get("extra")]
    vocab = {}
    for l in lyr:
        for t in l["text"].split(): vocab.setdefault(nrm(t), t)
    keep_l, drop = [], set()
    for l in timing["lines"]:
        if not l.get("extra"): keep_l.append(l); continue
        if re.search(r"thanks? for watching|subscribe|like and", l["text"], re.I): drop.add((l["start"], l["end"])); continue
        best = max(lyr, key=lambda x: difflib.SequenceMatcher(None, nrm(x["text"]), nrm(l["text"])).ratio()) if lyr else None
        ws = [w for w in timing["words"] if l["start"] - 0.01 <= w["start"] < l["end"] - 0.01 or abs(w["start"] - l["start"]) < 0.01]
        lt = l["text"].split()
        wins = [ll["text"].split()[i:i + len(lt)] for ll in lyr for i in range(max(1, len(ll["text"].split()) - len(lt) + 1))]
        wins = [w for w in wins if len(w) == len(lt)]
        bw = max(wins, key=lambda w: difflib.SequenceMatcher(None, nrm(" ".join(w)), nrm(l["text"])).ratio()) if wins else None
        if bw and difflib.SequenceMatcher(None, nrm(" ".join(bw)), nrm(l["text"])).ratio() >= 0.7:
            bt = bw
            if True:
                l["text"] = " ".join(bt)
                for w, t in zip(sorted(ws, key=lambda w: w["start"])[:len(bt)], bt): w["w"] = t
        for w in ws:
            k = nrm(w["w"]); k2 = k.replace("our", "or")
            if k not in vocab and k2 in vocab: w["w"] = vocab[k2] + ("," if w["w"].endswith(",") else "")
        l["text"] = " ".join(w["w"] for w in sorted(ws, key=lambda w: w["start"])) or l["text"]
        keep_l.append(l)
    timing["lines"] = keep_l
    timing["words"] = [w for w in timing["words"] if not any(a - 0.01 <= w["start"] <= b + 0.01 for a, b in drop)]
    return timing

def ass(timing, channel, title, W=1920, H=1080):
    hl = HILITE.get(channel, "&H0000D7FF&")
    soft = channel == "moon"
    head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Lyric,Baloo 2 ExtraBold,{86 if not soft else 76},{hl},&H00FFFFFF&,&H00402010&,&H80000000&,-1,0,0,0,100,100,1,0,1,6,3,2,80,80,46,1
Style: Speak,Baloo 2 ExtraBold,66,&H00FFFFFF&,&H00FFFFFF&,&H00402010&,&H80000000&,-1,0,0,0,100,100,0,0,1,5,2,2,120,120,50,1
Style: Title,Baloo 2 ExtraBold,150,&H00FFFFFF&,&H00FFFFFF&,&H00402010&,&H64000000&,-1,0,0,0,100,100,2,0,1,9,5,8,60,60,70,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    ev = []
    # title card for the first 3.2 s: pops in, then floats away
    if os.environ.get("ZOO_TITLE_CARD"):   # views data (Nov 5): no title card - get to the song immediately
        ev.append(f"Dialogue: 1,{ts(0.25)},{ts(3.4)},Title,,0,0,0,,{{\\fad(150,350)}}{title}")
    words = timing["words"]
    starts = sorted(l["start"] for l in timing["lines"])
    def until(ln, pad):   # a line clears the moment the next one starts (no stacked lyrics)
        nxt = [x for x in starts if x > ln["start"] + 0.01]
        return min(ln["end"] + pad, nxt[0] - 0.35) if nxt else ln["end"] + pad
    for ln in timing["lines"]:
        if ln.get("kind") == "speak":
            ev.append(f"Dialogue: 0,{ts(ln['start'])},{ts(until(ln, 0.4))},Speak,,0,0,0,,{{\\fad(120,160)}}{ln['text']}")
            continue
        ws = [w for w in words if ln["start"] - 0.01 <= w["start"] < ln["end"]]
        if not ws: continue
        t0 = ws[0]["start"] - 0.35
        parts = []; cur = t0
        for w in ws:
            gap = max(0, w["start"] - cur)
            if gap > 0.01: parts.append(f"{{\\k{int(gap * 100)}}}")
            d = max(0.05, w["end"] - w["start"])
            parts.append(f"{{\\kf{int(d * 100)}}}{w['w']} ")
            cur = w["start"] + d
        ev.append(f"Dialogue: 0,{ts(t0)},{ts(until(ln, 0.25))},Lyric,,0,0,0,,{{\\fad(100,120)}}{''.join(parts).strip()}")
    return head + "\n".join(ev) + "\n"

def main():
    raw, jobp = sys.argv[1], sys.argv[2]
    job = json.load(open(jobp)); jd = os.path.dirname(os.path.abspath(jobp)); jid = job["id"]
    timing = clean_extra(json.load(open(os.path.join(jd, job["timing_file"]))))
    trim = float(arg("--trim", "0"))
    if trim > 0:   # cut a long instrumental intro: trim raw video+audio and shift every time by -trim
        tr = os.path.join(os.path.dirname(os.path.abspath(raw)), os.path.basename(raw)[:-4] + f"_trim{trim:g}.mp4")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{trim}", "-i", raw, "-c:v", "libx264", "-preset", "fast", "-crf", "16",
                        "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "256k", "-af", "afade=t=in:d=0.15", tr], check=True)
        raw = tr
        sh = lambda x: round(max(0.0, x - trim), 3)
        for l in timing["lines"]: l["start"], l["end"] = sh(l["start"]), sh(l["end"])
        for w in timing["words"]: w["start"], w["end"] = sh(w["start"]), sh(w["end"])
        timing["duration"] = max(0.0, timing["duration"] - trim)
        job["thumb_frame"] = max(0, job.get("thumb_frame", 120) - int(trim * 24))
    song = json.load(open(os.path.join(HERE, "songs", job.get("song", jid) + ".json")))
    meta = song["meta"]; ch = job["channel"]
    global LOUD
    LOUD = "loudnorm=I=-16:TP=-1.5:LRA=11" if ch == "moon" else "loudnorm=I=-14:TP=-1.5:LRA=11"   # lullabies a bit softer
    _has_a = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=codec_name", "-of", "csv=p=0", raw], capture_output=True, text=True).stdout.strip()
    if not _has_a:   # a silent raw (Nov 14: ep12w/ep13w were assembled without their song) must never be published
        _au = os.path.join(jd, job.get("audio", ""))
        if not (job.get("audio") and os.path.exists(_au)): sys.exit(f"QUALITY GATE: {raw} has no audio and {_au} is missing; stage the song file into jobs/ first")
        _fx = raw[:-4] + "_withaudio.mp4"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", raw, "-i", _au, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", _fx], check=True)
        raw = _fx; print("raw had no audio: added", _au)
    repo = arg("--repo", "/home/claude/animated-zoo-media")
    work = os.path.join(HERE, "finished"); os.makedirs(work, exist_ok=True)
    sub = os.path.join(work, jid + ".ass")
    open(sub, "w").write(ass(timing, ch, meta.get("card", meta["title"].split("|")[0].strip())))
    out = os.path.join(work, jid + ".mp4")
    if "--hd" in sys.argv and os.environ.get("ZOO_ALLOW_HD"):   # legacy 1080p path, disabled unless explicitly allowed
        vf = f"subtitles={sub}:fontsdir={FONT_DIR}"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", raw, "-vf", vf, "-c:v", "libx264", "-preset", "veryfast", "-crf", "22", "-maxrate", "4M", "-bufsize", "8M",
                        "-pix_fmt", "yuv420p", "-af", LOUD, "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out], check=True)
    else:   # 4K: lanczos upscale + light sharpen, lyrics burned at 4K (crisp), AV1 10-bit sized to stay under GitHub's 100 MB
        dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", raw], capture_output=True, text=True).stdout.strip() or timing["duration"])
        vb = int(((94 * 8 * 1e6) / dur - 192e3) * 0.96)
        src_h = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=height", "-of", "csv=p=0", raw], capture_output=True, text=True).stdout.strip()
        if src_h == "2160":   # native 4K render: no upscale, no sharpen, just burn the lyrics
            vf = f"subtitles={sub}:fontsdir={FONT_DIR}"
        else:
            vf = f"scale=3840:2160:flags=lanczos,unsharp=5:5:0.5:5:5:0.0,subtitles={sub}:fontsdir={FONT_DIR}"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", raw, "-vf", vf, "-c:v", "libsvtav1", "-preset", arg("--preset", "9"), "-b:v", str(vb),
                        "-svtav1-params", "tune=0", "-g", "240", "-pix_fmt", "yuv420p10le", "-af", LOUD, "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out], check=True)
        print("4K AV1", round(os.path.getsize(out) / 1e6, 1), "MB, video", vb // 1000, "kbps")
        # quality gate: every published episode must be 3840x2160 and under 100 MB (GitHub raw upload limit)
        wh = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0", out], capture_output=True, text=True).stdout.strip()
        if wh != "3840,2160": sys.exit(f"QUALITY GATE: output is {wh}, expected 3840,2160")
        if os.path.getsize(out) >= 99.5e6:   # re-encode tighter once
            vb = int(vb * 0.9)
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", raw, "-vf", vf, "-c:v", "libsvtav1", "-preset", arg("--preset", "9"), "-b:v", str(vb),
                            "-svtav1-params", "tune=0", "-g", "240", "-pix_fmt", "yuv420p10le", "-af", LOUD, "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out], check=True)
            if os.path.getsize(out) >= 99.5e6: sys.exit("QUALITY GATE: 4K file still over 100 MB")
    # thumbnail: the thumb frame + big words
    tf = job.get("thumb_frame", 120) / timing.get("fps", 24)
    thumb = os.path.join(work, f"thumb_{jid}.png")
    words = meta.get("thumb_text", meta["title"].split("|")[0].strip().upper())
    tsub = os.path.join(work, jid + "_thumb.ass")
    open(tsub, "w").write(f"""[Script Info]
PlayResX: 1280
PlayResY: 720
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: T,Baloo 2 ExtraBold,150,{HILITE.get(ch, '&H0000D7FF&')},&H00FFFFFF&,&H00301808&,&H96000000&,-1,0,0,0,100,100,2,-4,1,10,6,7,40,40,26,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.00,0:00:10.00,T,,0,0,0,,{words}
""")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{tf:.2f}", "-i", raw, "-frames:v", "1",
                    "-vf", f"scale=1280:720,eq=saturation=1.15:contrast=1.05,subtitles={tsub}:fontsdir={FONT_DIR}", thumb], check=True)
    jid_pub = job.get("song", jid)   # publish under the episode name (not _v2)
    folder = {"truck": "truck", "bloop": "bloop", "fruity": "fruity", "moon": "moon", "gizmo": "gizmo", "zoo": "."}[ch]
    os.makedirs(os.path.join(repo, folder), exist_ok=True); os.makedirs(os.path.join(repo, "brand", folder if folder != "." else "zoo"), exist_ok=True)
    dst = os.path.join(repo, folder, jid_pub + ".mp4")
    subprocess.run(["cp", out, dst], check=True)
    tdst = os.path.join(repo, "brand", folder if folder != "." else "zoo", f"thumb_{jid_pub}.png")
    subprocess.run(["cp", thumb, tdst], check=True)
    plan_p = os.path.join(repo, "studio", "upload_plan_3d.json")
    plan = json.load(open(plan_p)) if os.path.exists(plan_p) else []
    rel = f"{folder}/{jid_pub}.mp4" if folder != "." else f"{jid_pub}.mp4"
    date = arg("--date")
    if not date:   # next free day for this channel, starting tomorrow
        taken = {p["date"] for p in plan if p["file"].startswith(folder + "/") and p["file"] != rel and p.get("status") != "dropped"}
        d = datetime.date.today() + datetime.timedelta(days=1)
        while d.isoformat() in taken: d += datetime.timedelta(days=1)
        date = d.isoformat()
    # Description lyrics come from the WRITTEN song (songs/<id>.json "lyrics"), not the timing lines: the timing
    # includes speech-to-text captions for improvised repeats, which left junk like "Type Subscribe" / "Thank you."
    # in descriptions (Nov 8-9 runs). Fall back to timing only if the spec has no lyrics.
    if song.get("lyrics"):
        lyrics = "\n".join(x.strip() for x in song["lyrics"].split("\n") if x.strip() and not x.strip().startswith("["))
    else:
        lyrics = "\n".join(l["text"] for l in timing["lines"] if l.get("kind") == "sing")
    seen = []; [seen.append(x) for x in lyrics.split("\n") if x not in seen]
    desc = meta["description"].rstrip() + "\n\n" + song.get("desc_header", "LYRICS") + "\n" + "\n".join(seen[:40])
    entry = {"file": rel, "title": meta["title"], "description": desc, "tags": meta.get("tags", []), "date": date,
             "time": arg("--time", SLOT.get(ch, "2:00 PM")), "thumb": os.path.relpath(tdst, repo), "made_for_kids": True,
             "status": "to_upload", "format": song.get("format", "3d_singalong"), "duration": round(timing["duration"], 1)}
    plan = [p for p in plan if p["file"] != rel] + [entry]
    plan.sort(key=lambda p: (p["date"], p["time"]))
    json.dump(plan, open(plan_p, "w"), indent=1)
    print("FINISHED", dst, tdst, date, entry["time"])
    if "--nopush" not in sys.argv:
        g = lambda *a: subprocess.run(["git", "-C", repo, *a], check=False)
        g("add", "-A"); g("commit", "-qm", f"Add 3D sing-along {jid}\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_014CFVfVuQKcnZwKkabBsmrF")
        for _ in range(3):
            if g("pull", "-q", "--rebase").returncode == 0 and g("push", "-q", "origin", "main").returncode == 0: break

if __name__ == "__main__":
    main()
