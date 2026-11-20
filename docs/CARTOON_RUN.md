# Cartoon run: one episode from draft to scheduled (for a scheduled, unattended session)

Rules: `CLAUDE.md` (every line applies). Engine notes: `PLAYBOOK.md`, section "Cartoon" (search "kit.py", "stills.sh", "Studio upload"). Decide and act; nobody answers questions at night.
Never: passwords, purchases, new accounts or terms, deleting a video, CAPTCHAs, "Publish" (always Schedule). Stop all Studio work by 6:15 AM ET: the daily run uses the same browser at 6:31 AM.

## STOP: no sung or hummed voice (owner, Nov 17 8:25 PM)
Milo's sung line in za_ep02 "sounds robotic". From now on no cartoon shot has a voice synthesized onto notes: no lyrics in a `sing` line, no `"hum": True`. A song moment = one ordinary spoken shot where the character SAYS the rhyme, then one `sing` shot where only instruments play the tune: `{"text": "~ ~ ~ ~", "notes": "C4:1 E4:1 G4:1 D4:2"}` (one `~` per note group; bpm 96, chords in C), words on screen with numeric times (`("words", 0.4, ...)` style cues, not `w:`), nobody's mouth moving. The models za_ep01.py, za_ep02.py and zc_ep01.py are fixed (Nov 17 11 PM): their `SING_*` and `HUM_*` lines are the pattern. A tune's notes over a chord are that chord's notes or a whole step from them (E over the F bar clashed). Run `python3 ../listen/listen.py --episode <id>` BEFORE rendering: no click, no CLASH line inside a tune shot (the bed's own E over F every 10 s is the 3D lessons' bed, logged in docs/IMPROVE.md). A build that already wrote a sung or hummed line changes it before its plan check and never renders it.

## VIRAL PACKAGING: every new 2D lesson, adventure and Short (owner approved Nov 20 2026, 10:37 AM: "implement the changes proposed to make those videos viral starting today")
Evidence: `drafts/growth_test_2026-11/01_audit.md` (lessons lose 61-68% of viewers in the first 10 s; every lesson so far opened with a greeting).
1. **Cold open.** Shot 1 shows the episode's promise (the mystery, the problem, the example) from the first frame, and the first spoken line asks
   or shows the title's question within 0-3 s. Never open on "Hi, friends! I'm Milo..." or a channel greeting. Milo says his name AFTER the hook
   (around 0:08-0:12), once. The first answer signs or the first obstacle are on screen by 0:20.
2. **Title.** The promise in the first 40 characters, as the question a child would ask ("Whose Feet Are These?", "Why Do Camels Have Humps?");
   a series name last if there is one ("Guess With Milo"); no "for Kids!" filler, no "5 Fun Facts", under 60 characters, no '<' '>' and no "AI".
3. **Thumbnail.** ONE big object (the mystery or the animal doing the action) filling about half the frame, high-contrast background,
   Milo only where he adds meaning (looking, pointing, guessing), 1-2 words (3 at most), none of the title's words (`thumb.py`). It shows the
   same picture as the first shot, so the click leads straight to what was promised. Check it at 168x94 px.
4. **Answering room.** Every question is followed by 4 s of thinking time with the answer signs on screen; every action line ("Can you...")
   gets about 3 s to do it. No sound effect on a spoken word; the music bed ducked under every line.
5. **Each Short** opens on its own mystery (the part's first shot), never on a greeting.

## MAIN INTRO in every new long 2D episode (owner, Nov 20 2026 12:44 PM: "create a main intro for the animated zoo that will be repeated on every episode ... just for future ones")
`studio/cartoon/intro.py` (made richer on the owner's ask, Nov 20 12:56 PM: "more sophisticated with more details and effects"): the same four shots
every time (about 15 s), a cut on each bar line. MUSIC (owner, Nov 20 3:52 PM: "now it sounds like artificial music"): one continuous score
on RECORDED instruments (`studio/cartoon/score_intro.py` -> `studio/sing/sf2render.py`, GeneralUser GS SoundFont, licence free for commercial
music): flute + bells carry the tune (C E G C | D B G B D | A C F C E D C D C), nylon guitar, pizzicato, acoustic bass, strings, light kit with
tambourine and shaker; every picture hit has its own instrument (pops = marimba, swoops = harp, letters = xylophone run, ZOO = brass + low piano +
kick, ding = tubular bell, confetti = celesta, ears = wood blocks), no synthetic sound effects; each group has its own room, EQ, compression,
then a master. The tune shots keep `sing` for their timing with `"mute": True`; the first shot carries `score` / `score_shots` (toon.mix_parts
mixes it, dips it under Milo's line and holds the lesson bed back). Real mallets, timpani, toms, crash and brass have overtones listen.py reads as
clashes: check `listen.py --episode` after every change (rounds 1-11 on Nov 20 removed each one; the reasons are in the comments).
PICTURE:
1. the morning sky (turning sun rays, twinkling stars), camera glides down to the gate; 2. the dressed-up gate: the friends pop up on the beat in
puffs of stars, bunting and balloons bounce in tempo, Milo swoops in with a sparkle trail and lands on the arch; 3. the logo card: turning
sunburst, badge with a spinning star, THE, rainbow ANIMATED dropping letter by letter, ZOO slamming in with a ding, bear ears on the O's,
confetti burst, a shine along the letters, Milo flies onto the badge, the friends pop up; 4. Milo says "The Animated Zoo!", the friends hop after
the line (silently: no sound effect on a spoken word), confetti rains. Never in a 9:16 Short, so it has no 9:16 framing.
Details added Nov 20 (owner: "include more details"): drifting clouds, a flock of birds and a far-off hot-air balloon in the sky; bubbles and two
butterflies at the gate and a star burst where Milo lands; light rings pulsing from the badge, a rainbow drawn on behind the logo (in the backdrop,
behind the friends, its feet behind the hill), letters that squash as they land, a sparkle burst on the bear ears, balloons rising at the sides, a
star burst on the last chord. Every hit lands on its note (TB = half a beat after the cut).
- In the episode file: `from intro import INTRO_STAGES, intro_shots`, `STAGES = {..., **INTRO_STAGES}` before `Kit(STAGES)`, and `*intro_shots()` in SHOTS
  RIGHT AFTER the hook shots (the episode still opens on its promise). It replaces the old "Welcome to The Animated Zoo, friends!" gate shot.
- Not in the Shorts (the intro shots carry no `part`, so `--short` leaves them out). Episodes already built are not changed.
- Preview alone: `python3 toon.py zintro`. Never edit the intro inside one episode: change `intro.py`, so every episode keeps the same intro.

## Guess With Milo (2D series, owner Nov 20 2026: "Guess With Milo should be always 2d not 3d; 3d is only for viral songs")
A Guess With Milo episode is a `cartoon_lesson` (5:00-6:30, three parts of 83-90 s, three Shorts) with this shape:
- Cold open on ONE mystery clue (a footprint, two ears in the grass, a wobbling egg). The first line asks "Who ...?". The words "Guess With Milo" are said once after the hook.
- Each part: its own clue on the board → two answer signs → 4 s thinking time → the animal walks in on "It is the ...!" (the reveal) → the
  fact with an on-screen example → a "Hmm." question with thinking time → one copy-me action → "Say it with me" → a quick check with answer signs.
- Quiz with all three animals, then a recap of the three clues; the closing picture names the next Guess With Milo.
- Title "Whose/Who ... ? Guess With Milo"; Shorts' title band "WHOSE" / "FOOT?" style (two lines, at most 15 and 10 letters).
- The titles are queued in `docs/cartoon/build_plan.py` (theme "guess"), so `upload_guard.py --next lesson` hands them out first.
- It is the approved 2D fact-lesson format with a new opening and series name, so it posts like any cartoon lesson. Send the owner the first
  finished episode's file and link in the run report.

## Setup (fresh session)
`bash studio/zoo3d/setup.sh` (voice model), `which hyperframes` (else `npm i -g hyperframes@0.8.231`), `python3 -c "import pyworld, pocketsphinx, kokoro_onnx, soundfile"` (else pip install with `--break-system-packages`).
HyperFrames refuses to start under 1 GB of free disk (`df -h .`). If needed: `git sparse-checkout set --no-cone '/*' '!/truck/' '!/moon/' '!/bloop/' '!/gizmo/' '!/fruity/' '!/space/' '!/wild/'` (they stay in git).
Renders and encodes: ONE at a time, started as a tracked background command, never `nohup ... &` (the render is cancelled when the launching call returns). No `git pull`, stash or rebase while one writes.

## Steps (all in `studio/cartoon/`)
1. `python3 toon.py <id> --plan` must exit 0 (300-390 s, no stretch over 6 s, 6 places, the story beats, every word placed, `sync`: all cuts on the half-beat, songs on a beat, no suspect word).
2. `./stills.sh <id> L <sheet.jpg> 8 300`: LOOK at one still of EVERY shot. Fix what the plan check cannot see (a character inside another, a word on a face or on the watermark, half a character at the edge, a prop that is not where the line says, a sign over a face). Stills again after each fix (`TAGS="tag a|tag b"` limits them).
3. Render: `python3 toon.py <id>` (4K, about 35 min for 5 minutes), then `toon.py --check4k`, `pace_check.py --max 8`, `../zoo3d/watermark.py check` and the mark's corner sheet, frames of the finished file (every answer reveal), `../listen/listen.py --episode <id>` and on the file (LOOK at its picture; it measures, it does not hear).
4. AV1: `ffmpeg -i out/<id>/<id>.mp4 -c:v libsvtav1 -preset 9 -b:v 2150k -svtav1-params tune=0 -g 240 -pix_fmt yuv420p10le -c:a copy -movflags +faststart ../../cartoon/<id>.mp4` (about 20 min). Thumbnail: `python3 thumb.py <id>` and look at it. `python3 ../zoo3d/review.py` gate on the final file (a PASS is not the look).
5. Upload (an adventure build that uploads itself; daily builds do NOT upload, see "The two daily builds"): `python3 ../upload_guard.py <plan file>` must say OK TO UPLOAD and `zlive("<title>")` on Studio's content list must give live = [] (never a second upload of a file, a title or a slot; a fix is `--replace <old id>`, then old one Private and renamed "OLD (replaced): <title>"). Count the last 24 hours first (`git log --since="24 hours ago" --format="%ad %s" --date=format:%H:%M | grep -i scheduled`; 20 is the allowance). Studio recipe: PLAYBOOK "Studio upload" + `studio/studio-upload2.js` (made for kids, custom thumbnail, the button must read "Schedule", list row reads "Scheduled").
6. Record: `studio/upload_plan_3d.json` (status, video_id), `docs/cartoon/status.json`, defects in `docs/IMPROVE.md`, a run note in `PLAYBOOK.md`; commit and push.
If a step cannot be finished: leave the entry un-uploaded, write exactly what was and was not done, commit, stop. Never upload a file whose stills or frames were not looked at.

## za_ep02 "Baby Elephant Tumble and the Big Muddy Puddle" (state: Nov 17, 3:05 PM ET)
- DONE: stills of every shot looked at and fixed, rendered in 4K, every check of steps 3 and 4 passed, scheduled for Nov 19 5:30 AM ET (GxNV3lIIkyA). Run note in PLAYBOOK.md, defects in docs/IMPROVE.md.
- Long renders on this machine: `tmux new-session -d -s render "python3 toon.py <id> > out/<id>/render.log 2>&1; echo EXIT \$? >> out/<id>/render.log"`, then read the log until EXIT 0 (a watched background command ends after 30 min; `--from/--to` fails with assertSwiftShader).
- Answer signs: reveal at least 1 s before the shot ends (pause 3.2 with "wait:2.0"), and look at the reveal frames of the finished file.
- Not built: a Short from it (its 9:16 cameras are not written), the closing "next adventure" picture.

## Several cartoon builds at the same time (Nov 17 evening: za_ep03 and the lessons zc_ep03, zc_ep04, zc_ep05, zc_ep06)
Each build is its own session with its own copy of the repo. So that their pushes do not collide:
- A build writes ONLY: `studio/cartoon/episodes/<id>.py`, a new art file `studio/cartoon/art_<id>.py` (register new places and kinds from there, the way `art3.py` does; never change how an existing character, prop or place is drawn), `studio/cartoon/out/<id>/` (timing files and logs), `cartoon/<id>*.mp4`, its thumbnails under `brand/zoo/`, its OWN entries in the two upload plans (already there as "in_production": change only those blocks), and its run note `docs/cartoon/runs/<id>.md` (what was done, what was not checked, defects found). Not PLAYBOOK.md, not docs/IMPROVE.md, not docs/cartoon/status.json: the daily run folds the run notes in.
- An engine bug that blocks the build (`toon.py`, `kit.py`, `thumb.py`): the smallest fix, described in the run note. Old episodes must still pass their plan check.
- Before pushing, with no render or encode running: `git pull --rebase origin main`, then push; on a conflict keep both sides.
- A lesson build does NOT upload. It leaves every finished and checked file with status "to_upload" (title, description, tags, thumb, thumb_text, seconds filled in); the 6:31 AM daily run schedules them soonest first as the 20-per-24-hours allowance frees.

## A fact lesson and its three Shorts
Model: `episodes/zc_ep02.py` (three parts with `part=1|2|3`, `SHORTS`, `THUMBS`, a 9:16 camera `pcam` on every shot, `pcam2` for wide views, the two-line title band) plus `"beat": True` in EP as in `episodes/za_ep02.py`.
- Lesson: at least 5:00, three parts written 83-90 s each so part + hook is a Short of 85-95 s; questions with answer signs and thinking time (reveal at least 1 s before the shot ends), on-screen examples of the exact thing, every word in sync.
- Stills of EVERY shot twice: `./stills.sh <id> L sheet.jpg 8 300` (16:9) and `./stills.sh <id> 0|1|2 sheet.jpg 8 300` (9:16), again after each fix.
- Render the lesson (`python3 toon.py <id>`), then each Short (`python3 toon.py <id> --short 0`, then 1, then 2), one at a time. Every finished file: `--check4k` (3840x2160, Shorts 2160x3840), pace check, watermark check and corner sheet, frames looked at, listen.py, AV1 encode into `cartoon/`, its own thumbnail (`thumb.py`; 3 words at most, none of its title's words), review.py.

## The daily builds (owner, Nov 17 10:42 PM: continuous 2D production; Nov 18 11:00 PM: fill the empty slots. Scheduled tasks: cartoon lesson + 3 Shorts at 1:47 AM and 1:17 PM ET, cartoon adventure at 8:43 AM and 7:23 PM ET, all on Opus 5.5. Builds may run at the same time: the claim commit in step 2 is what keeps two of them off one title or slot)
1. `git pull --rebase origin main`, then `python3 studio/upload_guard.py --next lesson` (or `adventure`): it prints the title, premise, facts to read today and thumbnail idea of the first THEMES entry (`docs/cartoon/build_plan.py`) that has no plan entry, the next free id (`zc_epNN` / `za_epNN`) and the first free slots two days ahead (lesson 9:30 AM or 5:30 PM, adventure 5:30 AM or 1:30 PM, three Short slots 7:30 AM / 11:30 AM / 7:30 PM).
2. Claim it at once: add the entries to the plans as "in_production" with that title, date, time, format (`cartoon_lesson` + three `cartoon_short_90`, or `cartoon_adventure`), `"res"`, `"watermark": "tl"` and a note with the session id; commit and push. If the push is refused because another session claimed the same id or title, pull and take the next one.
3. Build by this file ("Steps", "A fact lesson and its three Shorts", the STOP section, "Several cartoon builds at the same time": write only your own files). Facts are read at their source today; a line whose source cannot be read is taken out.
4. Finish: every checked file "to_upload" (title, description, tags, thumb, thumb_text, seconds), `python3 studio/upload_guard.py <file>` says OK TO UPLOAD for each, run note `docs/cartoon/runs/<id>.md` (what was looked at, what was not checked, defects), commit and push. No browser, no upload: the 6:31 AM daily run schedules them on their slots.
5. If the build cannot be finished in the session: leave the entries "in_production", write in the run note exactly where it stopped (the next day's build of the same kind finishes it first, before starting a new title).
