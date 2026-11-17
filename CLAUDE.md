# The Animated Zoo: production repo

Full process: `docs/DAILY_RUN.md` (daily run, quality loop, posting grid). Run notes: `PLAYBOOK.md`. Open defects: `docs/IMPROVE.md`.

## Working preferences

Learned from the owner's corrections (Nov 14-15, 2026). One rule per topic; replace a rule instead of adding a contradicting one.

- Report only what exists and was checked; say what was not checked; never present an estimate as a fact.
- Deliver finished files to look at, not explanations of what will be done.
- Decide production, quality and scheduling questions yourself and act (upload, hold, replace, re-render); tell the owner the decision afterwards in one line. Do not ask him. The only things left to him: passwords, purchases, new accounts or terms, deleting a video.
- Three pillars (owner, Nov 16): songs stay in 3D and are not changed; adventure stories and animal-fact lessons are cartoon (`studio/cartoon/toon.py`); Shorts are cartoon and vertical. The formats, the cast and the look are in `docs/cartoon/` (plan, bible, findings).
- Fact lessons and adventure stories are at least 5:00 long (6:30 at most). A fact lesson is built from three parts of 85-95 s, each cut whole into one Short of about a minute and a half. A story has a hook in the first 5 s, a goal, three obstacles, a low moment, a solution the characters find, a warm ending, 2-3 true facts shown on screen and a song moment; nobody is hurt, lost, crying or trapped.
- Shorts come from fact lessons and adventure stories, never from songs; each shot is framed again for 9:16, not cropped. Songs have no minimum length: each is as long as it needs.
- Lessons are interactive: questions with answer signs and thinking time, on-screen examples of the exact thing being discussed, every word in sync with the voice. Never just a character moving to narration.
- 4K is the minimum for every video on the channel, cartoon included (owner, Nov 16): 3840x2160, or 2160x3840 for a Short, rendered at that size and not enlarged afterwards. `toon.py` refuses a finished file of any other size (`toon.py --check4k <files>`).
- Every video and every Short gets its own custom thumbnail that shows the example, with 3 words at most and none of the title's words.
- Every video and every Short is uploaded with the channel watermark in the picture (Milo's channel picture + "The Animated Zoo", `studio/zoo3d/watermark.py`); look at the mark's corner sheet: nothing that matters sits under it. Thumbnails carry no mark.
- Daily grid (ET): lessons 5:30 AM, 9:30 AM, 1:30 PM, 5:30 PM; Shorts 7:30 AM, 11:30 AM, 7:30 PM; song 3:30 PM. Always schedule, never publish immediately. The cartoon formats were approved by the owner on Nov 16, 3:36 PM ("cartoon formats are approved, build and post"): as cartoon videos become ready the four lesson slots are filled as adventures 5:30 AM and 1:30 PM, fact lessons 9:30 AM and 5:30 PM; a slot with no cartoon video ready keeps its 3D lesson, never stays empty.
- Nothing in a new format is uploaded until the owner has watched one full video of it and approved it.
- Before rendering, look at test stills of every example, every answer sign, every quiz answer close-up and every group scene: no character stands inside another, no sign or check mark covers a face or hides behind a character, nothing is cut by the frame or by the Short's crop, each example is the right size next to the animal.
- After rendering, look at frames of the finished video (every answer reveal included: close-ups cut the answer signs in zool_ep09/10), of every Short and of every thumbnail before sending or uploading anything; a "PASS" from review.py is not that look.
- Read every fact at its source on the day the script is written; if the source cannot be read, take the line out.
- Log every defect in `docs/IMPROVE.md` the same day and name it as fixed in the next video's spec; a defect counts as fixed only after a frame shows it fixed.
- When the owner says a scheduled or published video is wrong: set it to Private (do not delete), fix the cause in the engine, check every other video for the same cause, re-render, upload the fixed one on the same slot.
- Cartoon videos: the plan check (`toon.py <id> --plan`) must pass before any still is made (no stretch over 6 s without a change, 6 places, 300-390 s, every word placed, the story beats); `pace_check.py --max 8` and `watermark.py check` must pass on the finished file.
- Cartoon stills: look at one still of EVERY shot, in 16:9 and again in 9:16, before rendering (`studio/cartoon/stills.sh`), and again after each fix. Each look so far found defects the plan check cannot see: a word on a face or on the watermark, half a character at the frame edge, a caption on feet, a nose that stayed open on "Closed!", words stacked on one spot in 9:16, a strip of another colour at the top or bottom of a tall 9:16 view.
- Cartoon Shorts: every shot of a Short has its own 9:16 camera (`pcam`, and `pcam2` for wide views so the slow zoom never cuts a character); the title band is two lines of at most 15 and 10 letters; a lesson's parts are written 83-90 s long so part + hook is a Short of 85-95 s.
- A walk-in is `move` (where the actor starts) + `("walk", at, who, dx, seconds)`; a `fromto` on x together with a walk of 0 leaves the actor at the start (seen in zc_ep02's stills, Nov 16).
- In toon.py a group the engine moves carries only a translate; its size and its mirror go on a group inside it (GSAP measures x and y of a scaled SVG group from its bounding box: a tween to x = 300 stopped at 257).
- An animal that sings, hums or calls gets its own sung shot after the line that names it: written notes in C (the show loop's key) with its own soft band, `sing={"hum": True, ...}` for a hum; never a sound effect on top of the narration (owner, Nov 16: the camels' two-note beep).
- Cartoon music and sync follow the 3D process (owner, Nov 16 9:40 PM): every new episode has `"beat": True` in its EP: the 3D lessons' music bed lowered under the voice the same way, every cut on the music's half-beat, sung shots entering on a beat, idle motion in tempo, the mouth read at every frame, and teach.py's word-sync checks in the plan (`sync`: all cuts on the half-beat, all songs on a beat, no suspect word). Episodes rendered before that keep their file without it, so their timing can be rebuilt.
- A cue on a word that is said twice needs its number ("w:Closed!:2"); punctuation does not tell the two apart.
- A thumbnail's words are checked against the title by `thumb.py`; it refuses a word the title already has.
- I cannot listen: voices, songs and music are checked by word alignment and loudness only. Say so every time and leave the judgement of how they sound to the owner.
- YouTube Help (read Nov 16): end screens, cards and the watermark button are not available on made-for-kids videos. The pointer to the next episode is a closing picture in the video and the series playlist.
- When only the picture of a built lesson changes (a prop, a visit, a word's timing), patch jobs/<id>.json and the spec together and re-check with stills; re-running teach.py re-voices and moves part lengths (a Short fell from 84.7 to 83.8 s on Nov 16).
- Never run `git pull`, `git stash` or a rebase while an encode is writing a file inside the repo.
- After copying any file to the PC, read it back and compare it with the local file before a render depends on it; give every copy a new staged file name (a re-used staged path delivered the old content on Nov 15).
