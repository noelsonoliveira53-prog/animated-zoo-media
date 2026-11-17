# Cartoon run: one episode from draft to scheduled (for a scheduled, unattended session)

Rules: `CLAUDE.md` (every line applies). Engine notes: `PLAYBOOK.md`, section "Cartoon" (search "kit.py", "stills.sh", "Studio upload"). Decide and act; nobody answers questions at night.
Never: passwords, purchases, new accounts or terms, deleting a video, CAPTCHAs, "Publish" (always Schedule). Stop all Studio work by 6:15 AM ET: the daily run uses the same browser at 6:31 AM.

## Setup (fresh session)
`bash studio/zoo3d/setup.sh` (voice model), `which hyperframes` (else `npm i -g hyperframes@0.8.231`), `python3 -c "import pyworld, pocketsphinx, kokoro_onnx, soundfile"` (else pip install with `--break-system-packages`).
HyperFrames refuses to start under 1 GB of free disk (`df -h .`). If needed: `git sparse-checkout set --no-cone '/*' '!/truck/' '!/moon/' '!/bloop/' '!/gizmo/' '!/fruity/' '!/space/' '!/wild/'` (they stay in git).
Renders and encodes: ONE at a time, started as a tracked background command, never `nohup ... &` (the render is cancelled when the launching call returns). No `git pull`, stash or rebase while one writes.

## Steps (all in `studio/cartoon/`)
1. `python3 toon.py <id> --plan` must exit 0 (300-390 s, no stretch over 6 s, 6 places, the story beats, every word placed, `sync`: all cuts on the half-beat, songs on a beat, no suspect word).
2. `./stills.sh <id> L <sheet.jpg> 8 300`: LOOK at one still of EVERY shot. Fix what the plan check cannot see (a character inside another, a word on a face or on the watermark, half a character at the edge, a prop that is not where the line says, a sign over a face). Stills again after each fix (`TAGS="tag a|tag b"` limits them).
3. Render: `python3 toon.py <id>` (4K, about 35 min for 5 minutes), then `toon.py --check4k`, `pace_check.py --max 8`, `../zoo3d/watermark.py check` and the mark's corner sheet, frames of the finished file (every answer reveal), `../listen/listen.py --episode <id>` and on the file (LOOK at its picture; it measures, it does not hear).
4. AV1: `ffmpeg -i out/<id>/<id>.mp4 -c:v libsvtav1 -preset 9 -b:v 2150k -svtav1-params tune=0 -g 240 -pix_fmt yuv420p10le -c:a copy -movflags +faststart ../../cartoon/<id>.mp4` (about 20 min). Thumbnail: `python3 thumb.py <id>` and look at it. `python3 ../zoo3d/review.py` gate on the final file (a PASS is not the look).
5. Upload: count the last 24 hours first (`git log --since="24 hours ago" --format="%ad %s" --date=format:%H:%M | grep -i scheduled`; 20 is the allowance). Studio recipe: PLAYBOOK "Studio upload" + `studio/studio-upload2.js` (made for kids, custom thumbnail, the button must read "Schedule", list row reads "Scheduled").
6. Record: `studio/upload_plan_3d.json` (status, video_id), `docs/cartoon/status.json`, defects in `docs/IMPROVE.md`, a run note in `PLAYBOOK.md`; commit and push.
If a step cannot be finished: leave the entry un-uploaded, write exactly what was and was not done, commit, stop. Never upload a file whose stills or frames were not looked at.

## za_ep02 "Baby Elephant Tumble and the Big Muddy Puddle" (state: Nov 17, 3:05 PM ET)
- DONE: stills of every shot looked at and fixed, rendered in 4K, every check of steps 3 and 4 passed, scheduled for Nov 19 5:30 AM ET (GxNV3lIIkyA). Run note in PLAYBOOK.md, defects in docs/IMPROVE.md.
- Long renders on this machine: `tmux new-session -d -s render "python3 toon.py <id> > out/<id>/render.log 2>&1; echo EXIT \$? >> out/<id>/render.log"`, then read the log until EXIT 0 (a watched background command ends after 30 min; `--from/--to` fails with assertSwiftShader).
- Answer signs: reveal at least 1 s before the shot ends (pause 3.2 with "wait:2.0"), and look at the reveal frames of the finished file.
- Not built: a Short from it (its 9:16 cameras are not written), the closing "next adventure" picture.
