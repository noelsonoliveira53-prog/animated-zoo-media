#!/usr/bin/env python3
"""One picture, several languages (docs/multilang/PLAN.md).

    python3 studio/multilang/build.py <episode id> [--fit]        --fit: only fit the lines and print the ones that do not fit

Reads   studio/multilang/languages.json                       the languages and their voices
        studio/cartoon/episodes/<id>.py                       the episode (English, the picture is cut to it)
        studio/cartoon/episodes/lang/<id>.<code>.json         one adaptation per extra language: lines, metadata, notes
        cartoon/<id>.mp4                                      the finished master (rendered once, never rendered again here)
Writes  packages/<id>/  video/ audio/ captions/ metadata/ thumbnails/ validation-report.json upload-manifest.json

Nothing here uploads, and nothing in the English path is changed: the English narration, music and effects are taken from toon.py as they are.
The other languages reuse the SAME music and effects bed and put their own voice lines into the English lines' time slots."""
import os, sys, json, re, subprocess, hashlib, importlib, shutil
import numpy as np, soundfile as sf

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE)); CART = os.path.join(REPO, "studio", "cartoon")
sys.path.insert(0, CART)
import toon, sing                       # toon puts studio/sing and studio/zoo3d on the path
SR = toon.SR
CONF = json.load(open(os.environ.get("ML_LANGS") or os.path.join(HERE, "languages.json")))      # ML_LANGS / ML_PKG: a trial with other voices writes its own package and leaves the real one alone
FIELDS = ["language", "localized_title", "localized_description", "educational_topic", "parent_summary", "primary_keywords", "secondary_keywords", "hashtags", "playlist",
          "audience_setting", "original_language", "audio_track_filename", "caption_filename", "thumbnail_filename"]


def english(eid):
    """The episode exactly as toon.py builds it: shots with their English audio and times, the film (for its sound effects), the length."""
    mod = importlib.import_module("episodes." + eid); ep = mod.EP; shots = [dict(s) for s in mod.SHOTS]
    total, miss, tot = toon.voice_lines(ep, shots); total += ep.get("tail", 0.6); shots[0]["t0"] = 0.0
    film = toon.Film(ep, mod.STAGES, shots, False); film.build_html(total, None)
    return mod, ep, shots, film, total


def bed_and_voice(film, shots, total, ep):
    """toon.mix_audio taken apart: the voice alone, and the bed (music ducked under the ENGLISH lines + every sound effect). The bed is the same for every language."""
    voice, bed = toon.mix_parts(film, total, ep)      # the engine itself gives the two parts (voice; music + effects)
    same = bool(np.allclose(np.clip(voice + bed, -1, 1), toon.mix_audio(film, total, ep), atol=1e-5))
    return voice, bed, same


def voice_for(L, c, ep):
    """The language's voice for one character. c: the character's English cast entry ({} = Milo / the narrator).
    A character keeps its own offsets from Milo (higher pitch, smaller head); a male English voice (am_, bm_) takes the language's "voice_m"."""
    if not c or c.get("voice", ep.get("voice")) == ep.get("voice") and not c.get("pitch") and c.get("formant", 1.0) == 1.0: return L
    male = c.get("voice", "af")[1] == "m" and "voice_m" in L
    return dict(L, voice=L["voice_m"] if male else L["voice"], pitch=(L.get("pitch_m", 0) if male else L.get("pitch", 0)) + c.get("pitch", 0),
                formant=c.get("formant", 1.0) if c.get("formant", 1.0) != 1.0 else L.get("formant", 1.0))


def say(text, L, speed):
    """One line in a language's voice, at the character's pitch. Cached like sing.say."""
    h = hashlib.md5(f"{text}|{L['voice']}|{speed:.3f}|{L['tts_lang']}|{L.get('pitch', 0)}|{L.get('formant', 1.0)}".encode()).hexdigest()[:16]; p = os.path.join(sing.CACHE, f"ml_{h}.npy")
    if os.path.exists(p): return np.load(p)
    a, sr = sing.kokoro().create(text, voice=L["voice"], speed=speed, lang=L["tts_lang"]); assert sr == SR
    a = sing.trim(a.astype(np.float64)).astype(np.float32)
    if L.get("pitch") or L.get("formant", 1.0) != 1.0: a = toon.shift(a, L.get("pitch", 0), L.get("formant", 1.0))
    pk = float(np.abs(a).max())
    if pk > .9: a = a * (.9 / pk)
    np.save(p, a); return a


def active_rms(a): x = a[np.abs(a) > 0.01]; return float(np.sqrt(np.mean(x ** 2))) if len(x) else 0.0


def fit(lines, shots, L, ep):
    """Every line into its English line's slot (the line's time + the pause after it). A line that is too long is spoken a little faster, never faster than max_speed, never cut."""
    base = ep.get("speed", 0.9); mx = CONF["fit"]["max_speed"]; endgap = CONF["fit"]["min_end_gap_s"]; spoken = [s for s in shots if s["audio"] is not None and not s.get("sung")]
    assert len(lines) == len(spoken), f"{len(lines)} lines for {len(spoken)} spoken shots"
    cast = ep.get("cast", {}); out = []
    for s, text in zip(spoken, lines):
        slot = s["t1"] - s["v0"] - endgap; c = cast.get(s.get("who") or "", {})
        if text.strip() == "=":       # the line stays in English (the channel's name in the main intro): the English recording itself
            out.append({"tag": s["tag"], "v0": round(s["v0"], 3), "text": s["say"], "english": s["say"], "speed": c.get("speed", base), "seconds": round(s["dur"], 2), "slot": round(slot, 2),
                        "english_seconds": round(s["dur"], 2), "fits": True, "over": 0.0, "audio": s["audio"], "kept_english": True}); continue
        V = voice_for(L, c, ep); sp0 = c.get("speed", base); sp = sp0; a = say(text, V, sp)
        for _ in range(3):
            d = len(a) / SR
            if d <= slot or sp >= mx: break
            sp = min(mx, round(sp * d / slot * 1.02 + 0.005, 2)); a = say(text, V, sp)
        d = len(a) / SR; g = min(2.0, max(0.5, active_rms(s["audio"]) / (active_rms(a) + 1e-9))); a = a * g; pk = float(np.abs(a).max())      # as loud as the same character's English line
        if pk > .9: a = a * (.9 / pk)
        out.append({"tag": s["tag"], "v0": round(s["v0"], 3), "text": text, "english": s["say"], "speed": sp, "base_speed": sp0, "seconds": round(d, 2), "slot": round(slot, 2), "english_seconds": round(s["dur"], 2),
                    "fits": d <= slot, "over": round(max(0.0, d - slot), 2), "audio": a, "who": s.get("who") or "milo", "voice": V["voice"]})
    return out


def voice_track(fitted, n):
    v = np.zeros(n, np.float32)
    for f in fitted:
        a0 = int(f["v0"] * SR); a = f["audio"]; v[a0:a0 + len(a)] += a[:n - a0] * 0.95
    return v


def wav48(x, path, dur, norm):
    """24 kHz mono -> 48 kHz 16-bit WAV exactly as long as the video; norm: the same loudness step toon.py uses for the film's sound."""
    tmp = path + ".24k.wav"; sf.write(tmp, x, SR)
    af = ("loudnorm=I=-14:TP=-1.5:LRA=11," if norm else "") + f"apad=whole_dur={dur:.4f}"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", tmp, "-af", af, "-t", f"{dur:.4f}", "-ar", "48000", "-ac", "1", "-c:a", "pcm_s16le", path], check=True); os.remove(tmp); exact(path, dur)


def exact(path, dur):
    """The file ends exactly with the video: ffmpeg left the tracks 78 ms short at the end (Nov 16; the start was in place), so the last samples are padded or cut here."""
    a, sr = sf.read(path, dtype="int16"); n = int(round(dur * sr))
    if len(a) != n: sf.write(path, np.concatenate([a, np.zeros(max(0, n - len(a)), np.int16)])[:n], sr, subtype="PCM_16")


def ts(t): t = max(0.0, t); h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60; return f"{h:02d}:{m:02d}:{int(s):02d},{int(round((s - int(s)) * 1000)) % 1000:03d}"


def wrap(text, width=42):
    if len(text) <= width: return text
    w = text.split(); best = None
    for k in range(1, len(w)):
        a, b = " ".join(w[:k]), " ".join(w[k:])
        if best is None or abs(len(a) - len(b)) < abs(len(best[0]) - len(best[1])): best = (a, b)
    return best[0] + "\n" + best[1]


def cues_english(shots):
    """The words as they are spoken, in the same groups as the picture's caption line."""
    out = []
    for s in shots:
        if not s["words"]: continue
        chunks = []; cur = []
        for w in s["words"]:
            cur.append(w)
            if len(cur) >= 9 or (re.search(r"[.!?]$", w[0]) and len(cur) >= 2) or (re.search(r",$", w[0]) and len(cur) >= 7): chunks.append(cur); cur = []
        if cur:
            if chunks and len(cur) == 1: chunks[-1] += cur
            else: chunks.append(cur)
        for ci, ch in enumerate(chunks):
            a = s["v0"] + ch[0][1]; b = (s["v0"] + chunks[ci + 1][0][1] - .04) if ci + 1 < len(chunks) else min(s["t1"] - .04, s["v0"] + s["dur"] + .4)
            out.append((a, b, " ".join(w[0] for w in ch)))
    return out


def cues_fitted(fitted):
    """One cue per line; a line of two sentences that is too long for two rows becomes two cues, timed by their share of the letters."""
    out = []
    for k, f in enumerate(fitted):
        a = f["v0"]; nxt = fitted[k + 1]["v0"] if k + 1 < len(fitted) else 1e9; b = min(a + f["seconds"] + .4, nxt - .04); parts = [f["text"]]
        if len(f["text"]) > 84 or ("\n" in wrap(f["text"]) and max(len(x) for x in wrap(f["text"]).split("\n")) > 42):
            m = re.split(r"(?<=[.!?])\s+", f["text"])
            if len(m) > 1: h = max(1, len(m) // 2); parts = [" ".join(m[:h]), " ".join(m[h:])]
        tot = sum(len(p) for p in parts); t0 = a
        for p in parts:
            t1 = t0 + (b - a) * len(p) / tot; out.append((t0, t1 - (.04 if p is not parts[-1] else 0), p)); t0 = t1
    return out


def write_srt(cues, path):
    open(path, "w", encoding="utf-8", newline="\n").write("".join(f"{k + 1}\n{ts(a)} --> {ts(b)}\n{wrap(t)}\n\n" for k, (a, b, t) in enumerate(cues)))


def read_srt(path):
    raw = open(path, "rb").read(); txt = raw.decode("utf-8"); cues = []
    for blk in txt.strip().split("\n\n"):
        ln = blk.split("\n"); m = re.match(r"(\d+):(\d+):(\d+),(\d+) --> (\d+):(\d+):(\d+),(\d+)", ln[1]); g = [int(x) for x in m.groups()]
        cues.append((g[0] * 3600 + g[1] * 60 + g[2] + g[3] / 1000, g[4] * 3600 + g[5] * 60 + g[6] + g[7] / 1000, "\n".join(ln[2:])))
    return cues, raw[:3] != b"\xef\xbb\xbf"


def probe(path, entries, stream="v:0"):
    return subprocess.run(["ffprobe", "-v", "error", "-select_streams", stream, "-show_entries", entries, "-of", "csv=p=0", path], capture_output=True, text=True).stdout.strip()


def longest_silence(voice, thr=0.01):
    q = np.abs(voice) > thr; idx = np.where(q)[0]
    if not len(idx): return len(voice) / SR
    gaps = np.diff(idx); return float(max(gaps.max(), idx[0], len(voice) - idx[-1]) / SR)


def title_issues(title):
    out = []
    if len(title) > 70: out.append(f"{len(title)} characters (70 at most)")
    if sum(1 for w in re.findall(r"\w+", title) if len(w) > 3 and w.isupper()) > 1: out.append("more than one word in capitals")
    return out


def main():
    eid = sys.argv[1]; mod, ep, shots, film, total = english(eid); default = CONF["default"]
    master = os.path.join(REPO, "cartoon", eid + ".mp4"); vdur = float(probe(master, "stream=duration")); wh = probe(master, "stream=width,height")
    voice_en, bed, same = bed_and_voice(film, shots, total, ep); n = len(bed); rep = {"episode": eid, "master": {"file": "cartoon/" + eid + ".mp4", "size": wh.replace(",", "x"), "seconds": round(vdur, 3)}, "checks": [], "languages": {}}

    def check(name, ok, detail): rep["checks"].append({"check": name, "pass": bool(ok), "detail": detail}); print("PASS" if ok else "FAIL", name, "|", detail)
    check("timing of this build equals the rendered master", abs(total - vdur) < 0.08, f"build {total:.3f} s, master video {vdur:.3f} s")
    check("music and effects bed is toon.py's own (voice + bed reproduces the film's English mix sample for sample)", same, "np.allclose with toon.mix_audio")
    codes = [c for c in CONF["languages"] if c != default and os.path.exists(os.path.join(CART, "episodes", "lang", f"{eid}.{c}.json"))]
    worded = [s["tag"] for s in shots if s.get("sung") and any(any(ch.isalpha() for ch in ln["text"]) for ln in s["sing"]["lines"])]
    if codes and worded: sys.exit(f"this episode has sung lines with words ({worded}): songs in other languages are not built yet (lyrics adapted to the same notes), see docs/multilang/ADD_A_LANGUAGE.md")
    tunes = np.zeros(n, np.float32)      # tunes played by instruments (sing lines of "~" only: the song moments, the main intro's timing shots): music, the same in every language
    for s in shots:
        if s.get("sung") and s["audio"] is not None: a0 = int(s["v0"] * SR); tunes[a0:a0 + len(s["audio"])] += s["audio"][:n - a0] * 0.95
    voice_en_spoken = voice_en - tunes; bed_ml = bed + tunes
    tr = {c: json.load(open(os.path.join(CART, "episodes", "lang", f"{eid}.{c}.json"), encoding="utf-8")) for c in codes}
    fitted = {c: fit(tr[c]["lines"], shots, CONF["languages"][c], ep) for c in codes}
    for c in codes:
        bad = [f for f in fitted[c] if not f["fits"]]; fast = [f for f in fitted[c] if f["speed"] > ep.get("speed", 0.9) + 1e-6]
        fast = [f for f in fitted[c] if f["speed"] > f.get("base_speed", f["speed"]) + 1e-6]
        print(f"{c}: {len(fitted[c])} lines, {len(fast)} spoken faster than the English pace, {sum(1 for f in fitted[c] if f.get('kept_english'))} kept in English, {len(bad)} do not fit")
        for f in bad: print(f"   TOO LONG by {f['over']} s ({f['seconds']} s in a slot of {f['slot']} s, English {f['english_seconds']} s): {f['text']}   <- {f['english']}")
    if "--fit" in sys.argv: return
    pk = os.environ.get("ML_PKG") or os.path.join(REPO, "packages", eid)
    for d in ("video", "audio", "captions", "metadata", "thumbnails"): os.makedirs(os.path.join(pk, d), exist_ok=True)
    mname = f"episode-master-{wh.split(',')[1]}p.mp4"; mp = os.path.join(pk, "video", mname)
    if not os.path.exists(mp):
        try: os.link(master, mp)                      # the same file, no second copy on the disk
        except OSError: shutil.copy(master, mp)
    # ---- sound
    spoken = [s for s in shots if s["audio"] is not None]; voices = {default: voice_en}
    for c in codes: voices[c] = voice_track(fitted[c], n)
    for c, v in voices.items():
        wav48(v, os.path.join(pk, "audio", f"narration-{c}.wav"), vdur, False)
        if c == default:        # the English track is the master's own sound, not a new mix
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", master, "-vn", "-af", f"apad=whole_dur={vdur:.4f}", "-t", f"{vdur:.4f}", "-ar", "48000", "-ac", "1", "-c:a", "pcm_s16le", os.path.join(pk, "audio", f"track-{c}.wav")], check=True); exact(os.path.join(pk, "audio", f"track-{c}.wav"), vdur)
        else: wav48(np.clip(v + bed_ml, -1, 1), os.path.join(pk, "audio", f"track-{c}.wav"), vdur, True)
    # ---- captions
    cues = {default: cues_english(shots)}
    for c in codes: cues[c] = cues_fitted(fitted[c])
    for c, q in cues.items(): write_srt(q, os.path.join(pk, "captions", f"captions-{c}.srt"))
    # ---- metadata + thumbnails
    import thumb
    from PIL import Image
    T0 = mod.THUMBS[eid]; metas = {}
    for c in [default] + codes:
        if c == default:
            enp = os.path.join(CART, "episodes", "lang", f"{eid}.en.json"); enm = json.load(open(enp, encoding="utf-8"))["metadata"] if os.path.exists(enp) else {}      # the English fields the episode file does not carry
            m = {"localized_title": ep["title"], "localized_description": ep["description"], "educational_topic": enm.get("educational_topic", ""), "parent_summary": enm.get("parent_summary", ""),
                 "primary_keywords": ep["tags"][:3], "secondary_keywords": ep["tags"][3:], "hashtags": enm.get("hashtags", []), "thumb_text": ep["thumb_text"]}
        else: m = dict(tr[c]["metadata"])
        tj = os.path.join(pk, "thumbnails", f"thumbnail-{c}.jpg"); w0 = T0["words"][0]; k = min(1.0, len(w0[0]) / max(1, len(m["thumb_text"])))        # longer words are set a little smaller, so they stay where the English words are
        t = dict(T0); t["words"] = [(m["thumb_text"], w0[1], w0[2], round(w0[3] * k)) + tuple(w0[4:])]
        thumb.build(eid, t, m["localized_title"], tj, False); Image.open(tj).save(tj.replace(".jpg", ".png")); os.remove(tj)
        tw = re.findall(r"\w+", m["thumb_text"].lower()); tt = set(re.findall(r"\w+", m["localized_title"].lower()))
        meta = {"language": c, "localized_title": m["localized_title"], "localized_description": m["localized_description"], "educational_topic": m["educational_topic"], "parent_summary": m["parent_summary"],
                "primary_keywords": m["primary_keywords"], "secondary_keywords": m["secondary_keywords"], "hashtags": m["hashtags"], "playlist": ep.get("series", ""), "audience_setting": "made_for_kids",
                "original_language": default, "audio_track_filename": f"audio/track-{c}.wav", "caption_filename": f"captions/captions-{c}.srt", "thumbnail_filename": f"thumbnails/thumbnail-{c}.png",
                "narration_only_filename": f"audio/narration-{c}.wav", "thumbnail_text": m["thumb_text"]}
        json.dump(meta, open(os.path.join(pk, "metadata", f"metadata-{c}.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False); metas[c] = meta
        check(f"{c}: metadata has every field", all(k in meta and meta[k] not in ("", None, []) for k in FIELDS), ", ".join(k for k in FIELDS if meta.get(k) in ("", None, [])) or "14 of 14")
        check(f"{c}: title is clean", not title_issues(meta["localized_title"]), "; ".join(title_issues(meta["localized_title"])) or f"{len(meta['localized_title'])} characters: {meta['localized_title']}")
        check(f"{c}: thumbnail has 3 words at most and none of its title's words", len(tw) <= 3 and not [w for w in tw if w in tt], m["thumb_text"])
        check(f"{c}: audience value is made for kids", meta["audience_setting"] == "made_for_kids", meta["audience_setting"])
    # ---- validation of the sound and the captions
    en_len = {s["tag"]: s for s in spoken}
    for c in [default] + codes:
        tp = os.path.join(pk, "audio", f"track-{c}.wav"); a, sr = sf.read(tp); d = len(a) / sr; v = voices[c]
        lufs = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", tp, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr; I = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", lufs)[-1])
        v = voice_en_spoken if c == default else v      # the spoken voice alone (instrument tunes are music)
        sp = np.abs(v) > 0.01; vr = 20 * np.log10(np.sqrt(np.mean(v[sp] ** 2))); br = 20 * np.log10(np.sqrt(np.mean(bed[sp] ** 2)) + 1e-9)
        info = {"track": f"audio/track-{c}.wav", "seconds": round(d, 3), "loudness_lufs": I, "peak": round(float(np.abs(a).max()), 3), "voice_over_bed_db": round(float(vr - br), 1), "longest_stretch_without_voice_s": round(longest_silence(v), 2)}
        check(f"{c}: track is as long as the video", abs(d - vdur) < 0.05, f"{d:.3f} s against {vdur:.3f} s")
        check(f"{c}: track is not clipped", float(np.abs(a).max()) < 0.999, f"peak {info['peak']}")
        check(f"{c}: the voice is well above the music", vr - br >= 10, f"voice {vr - br:.1f} dB above the music and effects while it speaks")
        if c != default:
            F = fitted[c]; bad = [f for f in F if not f["fits"]]; info.update(lines=len(F), lines_spoken_faster=sum(1 for f in F if f["speed"] > f.get("base_speed", f["speed"]) + 1e-6), fastest_speed=max(f["speed"] for f in F), lines_kept_in_english=sum(1 for f in F if f.get("kept_english")),
                                                                       mean_seconds_against_english=round(float(np.mean([f["seconds"] / f["english_seconds"] for f in F])), 2))
            check(f"{c}: every line ends inside its slot (no clipped sentence, no line running into the next)", not bad, f"{len(F) - len(bad)} of {len(F)} fit" + ("; too long: " + " | ".join(f["text"] for f in bad) if bad else ""))
            check(f"{c}: no long silence the English does not have", info["longest_stretch_without_voice_s"] <= longest_silence(voice_en_spoken) + 0.8, f"{info['longest_stretch_without_voice_s']} s (English {longest_silence(voice_en_spoken):.2f} s)")
            info["translator_notes"] = tr[c].get("translator_notes", []); info["line_table"] = [{k: f.get(k) for k in ("v0", "who", "voice", "seconds", "slot", "speed", "text", "english")} for f in F]
        q, nobom = read_srt(os.path.join(pk, "captions", f"captions-{c}.srt")); order = all(q[k][0] < q[k][1] and (k == 0 or q[k - 1][1] <= q[k][0] + 1e-6) for k in range(len(q)))
        worded = [s for s in spoken if s["words"]]      # a tune played by instruments ("~" only: a song moment, the main intro's timing shots) has no words and no caption
        starts = [s["v0"] + (s["words"][0][1] if c == default else 0) for s in worded]; off = max(min(abs(cu[0] - st) for cu in q) for st in starts)
        rows = max(len(r) for cu in q for r in cu[2].split("\n")); info.update(captions=f"captions/captions-{c}.srt", cues=len(q), longest_caption_row=rows)
        check(f"{c}: captions are UTF-8, in order, and every line's first caption starts with its voice", nobom and order and off < 0.06, f"{len(q)} cues, largest start difference {off * 1000:.0f} ms, longest row {rows} letters")
        rep["languages"][c] = info
    check("one master video, one YouTube video", len(os.listdir(os.path.join(pk, "video"))) == 1, mname)
    rep["not_checked_by_machine"] = ["how the voices sound and whether each word is pronounced right (nobody here can listen): one human listen per language",
                                     "regional vocabulary and age fit were checked by reading every line, not by a native speaker",
                                     "the picture's own words (caption line, big words, answer signs) are English in every language in this test"]
    rep["facts"] = "The English script's facts were read at their sources on the day the script was written (see the episode file's header); the adaptations state the same facts, line for line."
    rep["ready"] = all(c["pass"] for c in rep["checks"])
    json.dump(rep, open(os.path.join(pk, "validation-report.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    # ---- dry-run manifest: what would be sent to YouTube, in order. Nothing is sent by this script.
    plan = next((e for e in json.load(open(os.path.join(REPO, "studio", "upload_plan_3d.json"))) if e.get("file") == f"cartoon/{eid}.mp4"), {})
    man = {"dry_run": True, "sends_anything": False, "channel": "The Animated Zoo (UC1YuY8nqnViTtm85qxE_M1w)", "videos_created": 0 if plan.get("video_id") else 1,
           "video": {"existing_video_id": plan.get("video_id"), "file": f"video/{mname}", "made_for_kids": True, "video_language": "English", "schedule": f"{plan.get('date', '')} {plan.get('time', '')} ET".strip(), "visibility_now": plan.get("status")},
           "steps": [{"step": 1, "where": "Studio > Content > the video", "action": "already uploaded once; no second upload" if plan.get("video_id") else "upload the master once, schedule, never publish now"}]}
    k = 2
    for c in [default] + codes:
        m = metas[c]; yt = CONF["languages"][c]["youtube"]
        if c == default: man["steps"].append({"step": k, "where": "Studio > Languages", "language": yt, "action": "upload captions for the original language", "captions": m["caption_filename"]})
        else: man["steps"].append({"step": k, "where": "Studio > Languages > Add language", "language": yt, "title": m["localized_title"], "description": m["localized_description"], "audio_track": m["audio_track_filename"],
                                   "captions": m["caption_filename"], "thumbnail": m["thumbnail_filename"], "action": "add as DRAFT; the 'Publish' of the track waits for the owner's yes"})
        k += 1
    man["not_done_without_owner"] = ["publishing any audio track", "any change to a public video", "deleting anything"]
    json.dump(man, open(os.path.join(pk, "upload-manifest.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print("READY" if rep["ready"] else "NOT READY", pk)


if __name__ == "__main__":
    main()
