"""Nov 15 frame check of zool_ep09b (and the same frames of zool_ep08): four layout defects that a job patch can fix
without re-voicing the lesson.  python3 fix_layout.py jobs/<job>.json [out.json]   (teach.py does the same for new lessons)
 1. quiz: the green check stood 0.9 in front of the animal, so in the answer close-up it covered the animal's face
    (lion 5:16 of ep09b, koala 5:12 of ep08). It now stands beside the head, on the outer side, at the animal's depth,
    a little smaller, and leaves before the next question's wide shot.
 2. quiz: the "?" badge covered the middle of the QUIZ TIME! word. The word now leaves just before the first badge.
 3. teaching parts: the 3D word (TALLEST!, BIGGEST!) stood at x=0 and a wide top sign covered its end. It now stands at x=-0.7.
 4. teaching parts: a close-up while a high example (sun, count badges; z >= 3.0) is up cut the example at the top of the
    picture (sun at 2:32 of ep09b, 2:23 of ep08). Every close-up line that overlaps such an example is shown on the teaching shot
    (the 'exhibit' shot stays: it is framed on the example)."""
import json, sys, os
jp = sys.argv[1]; out = sys.argv[2] if len(sys.argv) > 2 else jp
job = json.load(open(jp))
if job.get("layout_fix"): print("already patched:", job["layout_fix"]); sys.exit(0)
tm = json.load(open(os.path.join(os.path.dirname(jp), job["timing_file"])))
secs = tm["sections"]; lines = tm["lines"]; n = [0, 0, 0, 0]
OUT = 1.75   # stills Nov 15: at 1.25 the check was half behind the elephant's ear and the lion's mane
for i, d in enumerate(job["direct"]):
    sc = next(s for s in secs if s["name"] == d["section"]); s0 = sc["start"] if i else 0.0
    sl = [l for l in lines if sc["start"] - 0.01 <= l["start"] < sc["end"]]
    T = [p for p in d["props"] if p.get("type") == "teach"]
    signs = [p for p in T if p["name"] == "sign"]; badges = [p for p in T if p["name"] == "badge"]
    for p in T:
        if p["name"] == "check":
            x = p["at"][0] - 1.0; y = p["at"][1] + 0.9
            # back-left place (-2.3, 1.2): its outer side is hidden behind the front-left animal (tiger, zool_ep10a still), so inner side
            # (1.5 from the head and 0.3 higher there: at 1.75 Milo's head hid the lower quarter of the polar bear's check, zool_ep11c still)
            inner = abs(x + 2.3) < 0.05 and abs(y - 1.2) < 0.05; z = p["at"][2] - 0.15
            sx = (1.5 if inner else OUT) if (x >= 0 or inner) else -OUT
            if inner and z < 3.0: z += 0.3
            p["at"] = [round(x + sx, 3), round(y, 3), round(z, 3)]; p.setdefault("opts", {})["s"] = 0.6
            nxt = [l["start"] - s0 for l in sl if l["start"] - s0 > p["delay"] + 0.3]      # gone before the next question's wide shot
            if nxt: p["dur"] = round(max(0.6, min(p["dur"], nxt[0] - 0.05 - p["delay"])), 3)
            n[0] += 1
    for p in d["props"]:
        if p.get("type") != "text": continue
        if badges and not signs:
            p["dur"] = round(max(1.0, min(b["delay"] for b in badges) - p.get("delay", 0) - 0.15), 3); n[1] += 1
        elif signs and isinstance(p.get("at"), list) and abs(p["at"][0]) < 0.01:
            p["at"][0] = -0.7; n[2] += 1
    if signs:
        hi = [(p["delay"], p["delay"] + p["dur"], p["name"]) for p in T if p["name"] not in ("sign", "dots") and p["at"][2] >= 3.0]
        for k, l in enumerate(sl):
            if k >= len(d["shots"]): break
            a_, b_ = l["start"] - s0, l["end"] - s0
            hit = [h for h in hi if h[0] < b_ and a_ < h[1]]
            if hit and str(d["shots"][k]).startswith("close"):
                print(f"{d['section']} line {k} '{l['text'][:40]}': {d['shots'][k]} -> teach ({hit[0][2]} is up)"); d["shots"][k] = "teach"; n[3] += 1
job["layout_fix"] = "2026-11-15"
json.dump(job, open(out, "w"), indent=1)
print(f"checks moved {n[0]}, quiz words timed {n[1]}, words moved {n[2]}, shots changed {n[3]} ->", out)
