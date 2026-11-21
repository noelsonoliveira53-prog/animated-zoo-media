"""Word-level timing for a generated song (runs on Noelson's PC inside the ACE-Step uv env, GPU if available).
uv run --with stable-ts python align.py <song.mp3> <lyrics.txt> <words.json>
Writes words.json (forced alignment to the lyrics) and words_tx.json (free transcription with word times).
If jobs/<song id>.song.json has a "job" block, it then builds the engine timing (timing_lib, with repair of
collapsed spots) and writes jobs/<job id>_song.wav, jobs/<job id>_timing.json and, last, jobs/<job id>.json,
so the render worker picks the episode up by itself.
"""
import sys, os, json, re, shutil, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import stable_whisper

song, lyr, out = sys.argv[1:4]
text = open(lyr, encoding="utf-8").read()
plain = "\n".join(l for l in text.splitlines() if l.strip() and not re.match(r"^\s*\[.*\]\s*$", l))
try:
    import torch; dev = "cuda" if torch.cuda.is_available() else "cpu"
except Exception:
    dev = "cpu"
model = stable_whisper.load_model("small", device=dev)
dur = 0
try:
    import soundfile as sf; dur = sf.info(song).duration
except Exception:
    pass
res = model.align(song, plain, language="en")
words = [{"w": w.word.strip(), "start": round(w.start, 3), "end": round(w.end, 3)} for s in res.segments for w in s.words if w.word.strip()]
json.dump({"words": words, "duration": dur or (words[-1]["end"] if words else 0)}, open(out, "w", encoding="utf-8"))
print("ALIGNED", len(words), "words")
tw = []
try:
    tx = model.transcribe(song, language="en", word_timestamps=True, vad=False)
    tw = [{"w": w.word.strip(), "start": round(w.start, 3), "end": round(w.end, 3)} for s in tx.segments for w in s.words if w.word.strip()]
    json.dump({"words": tw, "duration": dur}, open(out[:-5] + "_tx.json", "w", encoding="utf-8"))
    print("TRANSCRIBED", len(tw), "words")
except Exception as e:
    print("transcribe failed", e)

# ---- episode hand-off
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sid = os.path.basename(os.path.dirname(os.path.abspath(out)))
specp = os.path.join(ROOT, "jobs", sid + ".song.json")
spec = json.load(open(specp, encoding="utf-8")) if os.path.exists(specp) else {}
if spec.get("job"):
    import timing_lib
    ff = "ffmpeg"
    try:
        c = open(os.path.join(ROOT, "ffmpeg_path.txt")).read().strip().strip('"')
        if c: ff = c
    except Exception:
        pass
    job = dict(spec["job"]); jid = job["id"]; J = os.path.join(ROOT, "jobs")
    t = timing_lib.build(song, words, tw, spec, ffmpeg=ff)
    json.dump(t, open(os.path.join(J, jid + "_timing.json"), "w"))
    shutil.copyfile(song, os.path.join(J, jid + "_song.wav"))     # mp3 content; ffmpeg probes it
    job.setdefault("timing_file", jid + "_timing.json"); job.setdefault("audio", jid + "_song.wav")
    job.setdefault("res", "1920x1080"); job.setdefault("step", 1)
    timing_lib.apply_colors(job, t, spec)
    json.dump(job, open(os.path.join(J, jid + ".json"), "w"))
    print("JOB", jid, "timing:", round(t["duration"], 1), "s,", len(t["sections"]), "sections, repaired", t["repaired_words"])
