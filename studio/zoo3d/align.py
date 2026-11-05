"""Word-level timing for a generated song (runs on Noelson's PC inside the ACE-Step uv env, GPU if available).
uv run --with stable-ts python align.py <song.mp3> <lyrics.txt> <words.json>
Writes {"words": [{"w","start","end"}...], "duration": s}.
"""
import sys, json, re
import stable_whisper

song, lyr, out = sys.argv[1:4]
text = open(lyr, encoding="utf-8").read()
plain = "\n".join(l for l in text.splitlines() if l.strip() and not re.match(r"^\s*\[.*\]\s*$", l))
try:
    import torch; dev = "cuda" if torch.cuda.is_available() else "cpu"
except Exception:
    dev = "cpu"
model = stable_whisper.load_model("small", device=dev)
res = model.align(song, plain, language="en")
words = [{"w": w.word.strip(), "start": round(w.start, 3), "end": round(w.end, 3)} for s in res.segments for w in s.words if w.word.strip()]
dur = words[-1]["end"] if words else 0
try:
    import soundfile as sf; dur = sf.info(song).duration
except Exception:
    pass
json.dump({"words": words, "duration": dur}, open(out, "w", encoding="utf-8"))
print("ALIGNED", len(words), "words")
