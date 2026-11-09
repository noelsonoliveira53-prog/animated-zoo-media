"""Flag lyric lines whose words weren't actually sung at that time (vs the transcription)."""
import json, sys, re
sys.path.insert(0, '/root/zoo/blender/zoo3d'); from timing_lib import norm
t = json.load(open(sys.argv[1])); tx = json.load(open(sys.argv[2]))['words']
bad = 0
for l in t['lines']:
    if l.get('extra'): continue
    ws = [norm(w) for w in l['text'].split() if norm(w)]
    near = {norm(x['w']) for x in tx if l['start'] - 1.5 <= x['start'] <= l['end'] + 1.5}
    sc = sum(w in near for w in ws) / max(1, len(ws))
    dur = l['end'] - l['start']
    if sc < 0.6 or dur < 0.25 * len(ws):
        bad += 1; print(f"  BAD {l['start']:6.1f}-{l['end']:6.1f} match={sc:.2f} {l['text'][:55]}")
ext = [l for l in t['lines'] if l.get('extra')]
print(f"{sys.argv[1].split('/')[-1]}: {bad} bad lines, {len(ext)} extra lines")
