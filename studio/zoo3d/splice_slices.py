"""Put re-rendered slices (jobs with "frame_range") back into a full raw, keeping the raw's own sound.
python3 splice_slices.py <full raw.mp4> <out raw.mp4> <slice raw.mp4>:<first frame> [<slice raw.mp4>:<first frame> ...]
The first frame is frame_range[0] of the slice job. A slice raw has frame_range[1]-frame_range[0] frames (its own sound is ignored:
the worker lays the song from 0:00 under it). The output has exactly the frame count of the full raw; that is checked.
Nov 16: the first version (one ffmpeg, concat filter over trims of the same input) was killed for memory on a 4K raw. Now every
piece is encoded by its own ffmpeg (same x264 settings), then joined by stream copy.
--cover F:N:x:y:w:h  (optional, repeatable; F must be the first frame after a slice): in frames F..F+N-1 the region x,y,w,h is covered
with the same region of frame F-1 (the slice's last frame). Nov 16: a quiz slice whose QUIZ TIME! word leaves early ends without the
word, but the old frames after it still show the word shrinking away for 7 frames (zool_ep09: --cover 7635:12:1480:220:900:260).
Only for a region where nothing moves (static camera). Better: let a quiz slice's frame_range end 12 frames into the next section."""
import subprocess, sys, json, os

def nframes(p):
    o = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_packets", "-show_entries", "stream=nb_read_packets", "-of", "json", p],
                       capture_output=True, text=True).stdout
    return int(json.loads(o)["streams"][0]["nb_read_packets"])

ENC = ["-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "15", "-pix_fmt", "yuv420p", "-r", "24", "-video_track_timescale", "12288"]
argv = sys.argv[1:]; covers = {}
while "--cover" in argv:
    k = argv.index("--cover"); F, N, x, y, w, h = (int(v) for v in argv[k + 1].split(":")); covers[F] = (N, x, y, w, h); del argv[k:k + 2]
full, out = argv[0], argv[1]
sl = sorted(((int(a.rsplit(":", 1)[1]), a.rsplit(":", 1)[0]) for a in argv[2:]))
NF = nframes(full); work = out + ".pieces"; os.makedirs(work, exist_ok=True); pieces = []; extra = []; pos = 0

def piece(src, a, n, name):
    p = os.path.join(work, name); cmd = ["ffmpeg", "-y", "-loglevel", "error"]
    if a: cmd += ["-ss", f"{a / 24 - 0.005:.4f}"]
    cmd += ["-i", src]
    if src == full and a in covers and pieces:
        N, x, y, w, h = covers[a]; prev = pieces[-1]; pn = nframes(prev); patch = os.path.join(work, f"patch{a}.png")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{(pn - 1) / 24 - 0.005:.4f}", "-i", prev, "-frames:v", "1",
                        "-vf", f"crop={w}:{h}:{x}:{y}", patch], check=True)
        cmd += ["-i", patch, "-filter_complex", f"[0:v][1:v]overlay={x}:{y}:enable='lt(n,{N})'"]; extra.append(patch)
        print(f"frames {a}..{a + N - 1}: region {x},{y} {w}x{h} covered from frame {a - 1}", flush=True)
    cmd += ["-frames:v", str(n)] + ENC + [p]
    subprocess.run(cmd, check=True); got = nframes(p); assert got == n, f"{name}: {got} frames, wanted {n}"
    pieces.append(p); print(f"{name}: {n} frames", flush=True)

for k, (f0, path) in enumerate(sl):
    n = nframes(path); assert pos <= f0 and f0 + n <= NF, f"slice {path} ({f0}+{n}) does not fit after frame {pos} of {NF}"
    if f0 > pos: piece(full, pos, f0 - pos, f"keep{k}.mp4")
    piece(path, 0, n, f"slice{k}.mp4")
    print(f"frames {f0}..{f0 + n - 1} ({f0 / 24:.2f}-{(f0 + n) / 24:.2f} s) come from {path}", flush=True)
    pos = f0 + n
if pos < NF: piece(full, pos, NF - pos, "keepz.mp4")
lst = os.path.join(work, "list.txt"); open(lst, "w").write("".join(f"file '{p}'\n" for p in pieces))
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-i", full, "-map", "0:v", "-map", "1:a", "-c", "copy",
                "-movflags", "+faststart", out], check=True)
got = nframes(out); assert got == NF, f"output has {got} frames, the full raw has {NF}"
for p in pieces + extra + [lst]: os.remove(p)
os.rmdir(work)
print("OK", out, got, "frames")
