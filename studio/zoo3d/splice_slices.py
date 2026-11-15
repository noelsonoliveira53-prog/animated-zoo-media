"""Put re-rendered slices (jobs with "frame_range") back into a full raw, keeping the raw's own sound.
python3 splice_slices.py <full raw.mp4> <out raw.mp4> <slice raw.mp4>:<first frame> [<slice raw.mp4>:<first frame> ...]
The first frame is frame_range[0] of the slice job. A slice raw has frame_range[1]-frame_range[0] frames (its own sound is ignored:
the worker lays the song from 0:00 under it). The output has exactly the frame count of the full raw; that is checked."""
import subprocess, sys, json

def nframes(p):
    o = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_packets", "-show_entries", "stream=nb_read_packets", "-of", "json", p],
                       capture_output=True, text=True).stdout
    return int(json.loads(o)["streams"][0]["nb_read_packets"])

full, out = sys.argv[1], sys.argv[2]
sl = sorted(((int(a.rsplit(":", 1)[1]), a.rsplit(":", 1)[0]) for a in sys.argv[3:]))
NF = nframes(full); parts = []; fc = []; pos = 0; ins = ["-i", full]
for k, (f0, path) in enumerate(sl):
    n = nframes(path); assert pos <= f0 and f0 + n <= NF, f"slice {path} ({f0}+{n}) does not fit after frame {pos} of {NF}"
    ins += ["-i", path]
    if f0 > pos:
        fc.append(f"[0:v]trim=start_frame={pos}:end_frame={f0},setpts=PTS-STARTPTS[a{k}]"); parts.append(f"[a{k}]")
    fc.append(f"[{k + 1}:v]setpts=PTS-STARTPTS[s{k}]"); parts.append(f"[s{k}]")
    print(f"frames {f0}..{f0 + n - 1} ({f0 / 24:.2f}-{(f0 + n) / 24:.2f} s) come from {path}")
    pos = f0 + n
if pos < NF:
    fc.append(f"[0:v]trim=start_frame={pos},setpts=PTS-STARTPTS[z]"); parts.append("[z]")
fc.append("".join(parts) + f"concat=n={len(parts)}:v=1:a=0,fps=24[v]")
cmd = ["ffmpeg", "-y", "-loglevel", "error"] + ins + ["-filter_complex", ";".join(fc), "-map", "[v]", "-map", "0:a", "-c:v", "libx264", "-preset", "veryfast",
       "-crf", "14", "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", out]
subprocess.run(cmd, check=True)
got = nframes(out); assert got == NF, f"output has {got} frames, the full raw has {NF}"
print("OK", out, got, "frames")
