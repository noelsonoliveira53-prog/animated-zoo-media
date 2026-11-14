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

## Variety rule (Noelson, Nov 13, 2026): no two Zoo episodes may look the same
"Each episode should have different images and theme ... no videos are the same, even if that is what YouTube Studio is suggesting."
A winning topic or title pattern may be reused; the PICTURES may not. Every Zoo job uses `"set": "zooworld"` with a
`"locations"` route (3-5 places, a new place every ~20-35 s, like Google Vids where each part of the song is its own scene):
`[{"from": "chorus1", "biome": "jungle", "tod": "morning"}, {"from": "verse1", "biome": "river", "tod": "noon"}, ...]`.
Biomes: savanna, jungle, arctic, beach, farm, desert, autumn_forest, spring_meadow, river, mountain, bamboo, night_meadow.
Times of day: morning, noon, golden, sunset, night. Animals (chars/animal.py): lion, elephant, giraffe, zebra, hippo, tiger,
bear, polar_bear, panda, monkey, fox, arctic_fox, koala, horse, pig, cow, rhino (+ scale 0.55 for babies).
1. `python3 studio/zoo3d/variety.py suggest` -> least-used places and animals. Build the NEW song around them
   (lyrics name that cast; set `"new_song": true` in the job so the cast check applies: change 2+ animals vs the last episode).
2. `python3 studio/zoo3d/variety.py check jobs/<id>.json` must say OK (first place differs from the last 4 episodes,
   at most half the places repeat the previous one, 3+ places). Then `variety.py record jobs/<id>.json` and commit the ledger.
3. Thumbnails follow: thumb_frame must show the episode's first place and its own cast. Vids hooks animate that frame.
4. Scene plan (Nov 13 night, "more change on the scenes"): after the song's timing file exists, run
   `python3 studio/zoo3d/routes.py jobs/<id>.json`. It turns the coarse route into a fine plan: every chorus, each half of
   every verse and the bridge is its own scene (about 12 scenes per song, a change every 8-15 s), each with a formation
   (line, arc, v, duo, host_left, host_right), only the animals that part is about ("show"), an automatic closer camera,
   and a camera move (dolly, reveal, vista, side, high, low). New songs carry `"verses": [[animals of verse 1], ...]`.
   Places come with landmarks (windmill, igloo, cabin, bridge, umbrella, kite ...) and moving details.
5. Never re-use the savanna-only look for a new episode. Old savanna renders that were not posted get re-rendered (`<id>w` jobs).

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

## Lessons from the Nov 5 views check (apply to every new song)
- Open on the CHORUS: the first sung line within 2 s, and the most visual moment within 10 s. Use intro_bars 0-1 and no spoken hook first.
- No title card (finish.py has it off by default).
- Length 2:30-3:30 until average view duration passes 1:00.
- Title pattern: "<Topic> Song for Kids! <number/hook> with <Host>" (60 characters or less), plus an optional theme emoji at the end.
- Keep props out of the singer's close-up (Fruity carrot verse was blocked by cherries and the arrow).

## Lessons (Nov 14, 2026)
Narrated teaching episodes alternate with songs. Spec in `lessons/<id>.json`, built by `lesson.py` (Kokoro voice, slow,
with quiet time after every question and "Can you ...?"). 4:30-6:30 long. See docs/DAILY_RUN.md rule 5.

## Review gate and improvement loop (Nov 14, 2026)
`review.py` before every upload, `review.py --brief` before every new spec. Logs: docs/REVIEW_LOG.md, docs/IMPROVE.md.
Minimum look: docs/quality_baseline/. See docs/DAILY_RUN.md rules 3 and 4.
