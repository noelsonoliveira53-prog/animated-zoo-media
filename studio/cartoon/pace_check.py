"""Pace check: where does the picture stay the same for too long?
Noelson, Nov 16 2026: "the 3D animation sacrifices scene changes ... same scene, same camera, few visual changes";
quality gate: "reject and redo if any stretch over 8 seconds without a visual change".

  python3 pace_check.py <video> [--max 8] [--json out.json] [--sheet out.jpg]

How it looks: 4 pictures a second, shrunk to 192x108 grey, the caption band (bottom 20%) and the watermark corner left out.
The picture is cut into 8x8-pixel blocks. A VISUAL CHANGE is one of
  cut      - more than 45% of the blocks differ from the picture a quarter second before (new shot, new location)
  move     - more than 22% of the blocks differ from the picture at the last change (camera move, zoom, new background)
  element  - 2.5-22% of the blocks differ from the picture at the last change and stay different for a second
             (a sign, a word, a diagram, a new character comes in)
             and the SAME blocks stay different, picture after picture (a waving wing or a bobbing body changes other blocks each time)
A character bobbing, blinking or waving in place is NOT a visual change.
Two results: ANY visual change (the gate), and SAME SHOT (only cuts and camera moves count: "same scene, same camera").
Prints every stretch longer than --max seconds; exit code 1 when there is one (so it works as a gate)."""
import subprocess, sys, json, numpy as np

W, H, FPS, B = 192, 108, 4, 8


def arg(k, d=None): return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


def frames(path):
    p = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-i", path, "-vf", f"fps={FPS},scale={W}:{H}:flags=area,format=gray", "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
    while True:
        b = p.stdout.read(W * H)
        if len(b) < W * H: break
        yield np.frombuffer(b, np.uint8).reshape(H, W).astype(np.float32)


def blocks(f, vertical):
    f = f.copy()
    if vertical: f = f[int(H * 0.05):int(H * 0.80)]        # a Short: leave out the top edge and the caption band
    else: f = f[:int(H * 0.80)]; f[:12, :44] = f[12:24, :44]   # 16:9: leave out the captions and the watermark corner
    h, w = (f.shape[0] // B) * B, (f.shape[1] // B) * B
    return f[:h, :w].reshape(h // B, B, w // B, B).mean((1, 3))


def analyse(path, vertical=None):
    pr = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height:format=duration", "-of", "csv=p=0", path], capture_output=True, text=True).stdout.split()
    w, h = (int(x) for x in pr[0].split(",")[:2]); dur = float(pr[1])
    if vertical is None: vertical = h > w
    ev = []; ref = None; prev = None; pend = 0; pmask = None
    for i, f in enumerate(frames(path)):
        t = i / FPS; b = blocks(f, vertical)
        if ref is None: ref = prev = b; ev.append((0.0, "start")); continue
        d_prev = (np.abs(b - prev) > 12).mean(); mask = np.abs(b - ref) > 12; d_ref = mask.mean()
        kind = None
        if d_prev > 0.45: kind = "cut"
        elif d_ref > 0.22: kind = "move"
        elif d_ref > 0.025:
            # a new element stays where it is: the same blocks differ, picture after picture (a waving wing or a bobbing body does not)
            same = pmask is not None and (mask & pmask).sum() >= 0.8 * max(1, (mask | pmask).sum())
            pend = pend + 1 if same else 0
            if pend >= FPS: kind = "element"
        else: pend = 0
        pmask = mask
        if kind and t - ev[-1][0] >= 0.75: ev.append((round(t, 2), kind)); ref = b; pend = 0; pmask = None
        elif kind: ref = b; pend = 0; pmask = None
        prev = b
    ev.append((round(dur, 2), "end"))
    gaps = [(ev[k][0], ev[k + 1][0], round(ev[k + 1][0] - ev[k][0], 2)) for k in range(len(ev) - 1)]
    return {"file": path, "duration": round(dur, 2), "vertical": vertical, "events": ev, "gaps": gaps}


def gaps_of(ev, kinds):
    e = [x for x in ev if x[1] in kinds or x[1] in ("start", "end")]
    return [(e[k][0], e[k + 1][0], round(e[k + 1][0] - e[k][0], 2)) for k in range(len(e) - 1)]


def summary(r, mx):
    g = [x[2] for x in r["gaps"]]; long_ = [x for x in r["gaps"] if x[2] > mx]
    kinds = {k: sum(1 for e in r["events"] if e[1] == k) for k in ("cut", "move", "element")}
    sg = gaps_of(r["events"], ("cut", "move")); slong = [x for x in sg if x[2] > mx]      # SHOTS: only a new shot or a camera move counts
    return {"changes": len(r["events"]) - 2, **kinds, "median_gap": round(float(np.median(g)), 2), "mean_gap": round(float(np.mean(g)), 2),
            "longest_gap": max(g), "over_max": len(long_), "seconds_in_long": round(sum(x[2] for x in long_), 1),
            "share_in_long": round(sum(x[2] for x in long_) / r["duration"], 3), "long": long_,
            "shots": kinds["cut"] + kinds["move"], "shot_mean_gap": round(r["duration"] / max(1, kinds["cut"] + kinds["move"] + 1), 2),
            "shot_longest": max(x[2] for x in sg), "shot_over_max": len(slong), "shot_seconds_in_long": round(sum(x[2] for x in slong), 1),
            "shot_share_in_long": round(sum(x[2] for x in slong) / r["duration"], 3), "shot_long": slong}


def mmss(t): return f"{int(t // 60)}:{t % 60:04.1f}"


if __name__ == "__main__":
    path = sys.argv[1]; mx = float(arg("--max", "8"))
    r = analyse(path); s = summary(r, mx); r["summary"] = s
    print(f"{path}: {r['duration']:.0f} s, {s['changes']} visual changes ({s['cut']} cuts, {s['move']} moves, {s['element']} new elements), "
          f"one every {s['mean_gap']:.1f} s on average (median {s['median_gap']:.1f} s), longest stretch {s['longest_gap']:.1f} s")
    for a, b, d in s["long"]: print(f"  OVER {mx:g} s: {mmss(a)} - {mmss(b)}  ({d:.1f} s with no visual change)")
    if "--shots" in sys.argv:
        for a, b, d in s["shot_long"]: print(f"  SAME SHOT over {mx:g} s: {mmss(a)} - {mmss(b)}  ({d:.1f} s)")
    print(f"  {s['over_max']} stretches over {mx:g} s = {s['seconds_in_long']} s = {s['share_in_long'] * 100:.0f}% of the video")
    print(f"  SAME SHOT (no cut, no camera move): a new shot every {s['shot_mean_gap']:.1f} s on average, longest {s['shot_longest']:.1f} s, "
          f"{s['shot_over_max']} stretches over {mx:g} s = {s['shot_seconds_in_long']} s = {s['shot_share_in_long'] * 100:.0f}% of the video")
    if arg("--json"): json.dump(r, open(arg("--json"), "w"), indent=1)
    which = sorted(s["shot_long"], key=lambda x: -x[2]) if "--shots" in sys.argv else s["long"]
    if arg("--sheet") and which:       # the first, middle and last picture of each long stretch (up to 8), to LOOK at (--shots: same-shot stretches, longest first)
        ins = []; n = 0
        for a, b, d in which[:8]:
            for t in (a + 0.3, (a + b) / 2, b - 0.3):
                ins += ["-ss", f"{t:.2f}", "-i", path]; n += 1
        lay = "|".join(f"{(k % 3) * 480}_{(k // 3) * (270 if not r['vertical'] else 853)}" for k in range(n))
        fc = "".join(f"[{k}:v]scale=480:-2[s{k}];" for k in range(n)) + "".join(f"[s{k}]" for k in range(n)) + f"xstack=inputs={n}:layout={lay}[v]"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error"] + ins + ["-filter_complex", fc, "-map", "[v]", "-frames:v", "1", "-q:v", "3", arg("--sheet")])
    sys.exit(1 if s["long"] else 0)
