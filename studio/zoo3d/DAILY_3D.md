# Daily 3D sing-along production (6 channels, 1 episode each per day)

Repo: `studio/zoo3d/` (engine, chars, sets, songs, jobs, finish.py) and `studio/sing/` (sing.py).
PC: `C:\Users\Noels\Documents\ZooBlender\` runs START_RENDER_WORKER.bat (Blender EEVEE on RTX 4060 Ti).
  - `ZooBlender\zoo3d\` = copy of studio/zoo3d code (engine.py, lib.py, chars/, sets/)
  - `ZooBlender\jobs\` = <id>.json + <id>_timing.json + <id>_song.wav  (worker renders any job without out\<id>\DONE)
  - `ZooBlender\out\<id>\<id>_raw.mp4` + `DONE` when finished; `status.txt` = what it's doing now

## Container setup (fresh session)
```
bash studio/zoo3d/setup.sh        # pip pyworld soundfile kokoro-onnx, Kokoro model download, ffmpeg fonts
```

## A. Collect finished renders (morning run, before uploading)
1. List `ZooBlender\out` on the PC (device_list_dir). For every `<id>` folder that has `DONE` and isn't in
   studio/upload_plan_3d.json yet: stage `out\<id>\<id>_raw.mp4` (device_stage_files) and run
   `python3 studio/zoo3d/finish.py <staged raw.mp4> studio/zoo3d/jobs/<id>.json --repo <repo>`.
   That burns karaoke lyrics, makes the thumbnail, copies the MP4 to the channel folder, adds the
   upload_plan_3d.json entry for the channel's next free day, then commits and pushes.
2. Spot-check one finished MP4: grab 3 frames with ffmpeg and look at them (faces visible, lyrics readable, nothing broken).

## B. Write tomorrow's episodes (one per channel)
For each channel: truck (set town, char truck), bloop (colorlab, bloop + shape), fruity (kitchen, fruit),
moon (nightroom, luna + sleepy), gizmo (sciencelab, gizmo), zoo (savanna or park or a new habitat set, milo + animal).
1. Read docs/STRATEGY_3D.md and docs/ANALYTICS.md: do more of what's winning.
2. Pick a NEW topic (check studio/zoo3d/songs/ for what's done; never repeat a song). Write `songs/<id>.json`
   (id pattern: tt3d_epNN, bl3d_epNN, fr3d_epNN, mb3d_epNN, gz3d_epNN, zoo3d_epNN) in the format of the existing
   episode-1 songs, including `meta` (title 60 characters or less, card, thumb_text, description, tags). Facts must be true and safe.
3. `python3 studio/sing/sing.py songs/<id>.json songs/out_<id>`, then copy song.wav to `jobs/<id>_song.wav` and
   timing.json to `jobs/<id>_timing.json`.
4. Write `jobs/<id>.json` (copy the channel's episode-1 job and change the cast, directions, props and thumb_frame).
5. Test with 2 stills: `python3 bpyrun.py engine.py -- --job jobs/<id>.json --test --engine CYCLES --res 640x360 --samples 8 --frames A,B`
   (needs Blender as a Python module: `uv venv /root/bpyenv -p 3.11 && uv pip install --python /root/bpyenv bpy==5.0.1`).
6. Commit and push. Copy the job's 3 files into `ZooBlender\jobs\` on the PC (device_commit_files via /mnt/user-data/outputs),
   plus any changed chars/sets/engine files into `ZooBlender\zoo3d\`.
New characters or sets: add them as new modules under chars/ and sets/ following API.md, and copy them to the PC too.

## C. Budget
YouTube cap: at most 6 uploads/day (one per channel). PC render time grows with song length and cast size; check
`status.txt` and the `frame N/NF ... s/frame` lines in `ZooBlender\out\<id>.log`. If the PC falls behind (more than 6 jobs
waiting), write fewer new jobs that day.
