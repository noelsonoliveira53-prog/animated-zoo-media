# zc_ep14 "Whose Egg Is This? Guess With Milo" - run note (scheduled 1:17 PM ET lesson build, Nov 27 2026; session in the commits' Claude-Session line)

Scheduled, unattended build: the third Guess With Milo episode (2D cartoon lesson, docs/CARTOON_RUN.md "Guess With Milo", "VIRAL PACKAGING",
"MAIN INTRO") and its three Shorts. Nothing was uploaded; no Studio, no browser, nothing on the PC.

## Why this title
`upload_guard.py --next lesson` (about 3:12 PM ET): unfinished_first empty; first free THEMES title "Whose Egg Is This? Guess With Milo" (theme
"guess"), id zc_ep14, lesson Nov 28 5:30 PM, Shorts Dec 2 / Dec 3 / Dec 4 7:30 AM. Claimed in commit 2baf761 (four entries added, the za_ep15 claim
of the afternoon adventure build pushed a minute earlier kept on rebase).

## Animals: ostrich, green sea turtle, emperor penguin (all three the build plan named; every egg fact confirmed at its source)

## What exists
- `studio/cartoon/episodes/zc_ep14.py` ("beat": True, `*intro_shots()` right after the hook and as the last four shots) and new art only in
  `studio/cartoon/art_zc_ep14.py`: rigs `ostrich` (dad) / `ostrich_mom`, `ostrich_chick`, `penguin`, `penguin_egg` (an egg on the feet under the
  brood pouch), `penguin_chick_pouch` (a chick at mama's feet under her pouch), `penguin_chick` (not used in the end), `turtle_baby` (art2.turtle in
  hatchling colours); props: a big egg that cracks and opens (`-whole`, `-top`, `-bot`, `-crack`), the ostrich scrape (back and front lip), the
  sea turtle nest (17 eggs, a sand cover), the three clues for the game board, 24 chicken eggs that pop in one by one, a ping-pong ball, a finger
  that presses a soft egg (art_zc_ep09.fingertip turned down), a day / night board with mom and dad on the nest; a new place `shore_night` (the
  za_ep13 shore darkened, stars and moon). No existing character, prop or place changed. No engine change.
- Mama sea turtle = the existing Tula rig ("turtle"). The penguins stand on the "arctic" place; the script never says Arctic for them.
- Files: `cartoon/zc_ep14.mp4` (AV1 4K, 360.8 s: 330.3 s own content + the main intro at the beginning and at the end, 83.7 MB),
  `cartoon/zc_ep14_short1.mp4` 92.5 s, `_short2.mp4` 89.0 s, `_short3.mp4` 89.0 s (2160x3840 H.264, copied byte for byte from the render, cmp).
  Thumbnails `brand/zoo/thumb_zc_ep14.jpg` (CRACK!: one big cracked egg in its dirt nest, Milo beside it), `brand/zoo/shorts/thumb_zc_ep14_short1..3.jpg`
  (SO BIG! / SO MANY! / BRRR!). thumb.py accepted the words.

## Facts (read Nov 27, about 3:30-3:40 PM ET, by the session's page reader; verbatim quotes in the episode file's header)
Read and used: SDZWA Animals and Plants "Ostrich"; Los Angeles Zoo "Ostrich"; Smithsonian's National Zoo "Ostrich"; Nova Southeastern University,
Broward County Sea Turtle Conservation Program "Sea Turtles"; National Geographic Kids "Emperor penguin"; National Geographic "Emperor penguin";
SeaWorld "Emperor penguin". NOAA Fisheries "Green turtle" was read, but the reader returned only a summary for the nesting part: nothing from it is used
(the line "the eggs stay warm in the sand" was therefore NOT written).
Not said: egg colours, inches, pounds, days to hatch, speeds, how deep the turtle digs, the dads not eating, storms, what happens to hatchlings at sea.

## Checks before the render
- Plan check (`toon.py zc_ep14 --plan`, last run): no fails, 360.8 s with the two main intros (30.5 s), own content 330.3 s; parts 88.1 / 84.7 / 84.7 s;
  8 places (savanna, shore, shore_night, arctic, zoo, zoo_eve, intro_gate, intro_logo) + 3 boards; 700/700 words placed; 71 cuts, all on the half-beat;
  6/6 intro tunes on a beat; no suspect word; longest stretch without a change 5.39 s; 29 question moments. First words at 0.42 s ("Look! An egg
  is wobbling! Who is inside?"), Milo's name at about 9 s. First plan check: part 1 92.8 s and part 2 82.8 s: one shot cut ("Wow! That is one big
  egg!"), a pause shortened, "Great job" line shortened; part 2 got "So many!", "Super digging!" and a 0.8 s pause.
- listen.py --episode (music without the voice, BEFORE rendering): key C (fit 0.97), no click, no silence, tempo 95; CLASH lines only at the bed's
  bar changes (E4 over F2 at 117.4, 167.4, 217.4, 277.4 s: the known E-over-F of the lessons' bed), none inside a tune. Picture looked at.
- Stills of EVERY shot (end of shot) in 16:9 and in 9:16 for every shot of each Short, three rounds, and the changed shots again. Found and fixed:
  the game board's clue props drawn as boxes (hard-edged dirt, sand and ice blocks) -> low ovals; the ostrich's head cut by the frame top and
  words (BIGGEST BIRD!, CHICKEN SIZE!, SCRATCH!, SAY IT!, BIG!, OSTRICH!) on or touching its head -> wider cameras, words moved right; the turtle's
  sand cover lower than the eggs (eggs stuck out) -> taller; a "finger" that read as a small circle -> a real fingertip; the penguin's egg hidden
  under the pouch and the chick invisible -> pouch raised, egg and chick bigger and lower; the hatchlings "at night" on a daytime beach -> new
  shore_night; the huddle penguins standing inside each other, a beak in a head -> spaced; in 9:16 the nest lips showed hard side edges -> lips that
  taper into the ground (the hidden chick now waits with opacity 0 instead of behind a block); the 24-egg board, the day/night board and the
  ping-pong board cut or under the caption in 9:16 -> re-placed; PENGUIN / FEET signs over the penguin's face in 9:16 -> taller 9:16 view; the
  Short 1 and 3 hook "?" on the egg -> beside it; the mama penguin still walking in at the end of her shot -> walk starts earlier.
- NOTE: stills.sh hides a failed render: the second round showed the FIRST round's pictures again (the snapshot failed on a missing place name
  and sheet.py took the older snapshot folder). Caught because the sheet was identical; the old snapshot folder was removed and the round redone.

## Renders and checks on the finished files
- Lesson render (4K, 38 min on 2 cores): `out/zc_ep14/zc_ep14.mp4` 360.8 s. --check4k 3840x2160; watermark MARK yes; bookends.py BOOKENDS yes (both
  ends); pace_check --max 8: 0 stretches over 8 s (longest 7.5 s); corner sheet looked at (sky, boards, the gate, the penguin's back; at about 100 s
  the running ostrich's head passes just right of the mark, not under it); frames at the middle and end of every shot, the end of each intro shot
  and 0.4 s after all 9 answer reveals looked at (147 frames): nothing needed a re-render. The small blue ring seen at the centre in the last frame
  before some cuts is the iris wipe starting (the next shot has trans="iris"), as in every cartoon.
- AV1: `cartoon/zc_ep14.mp4` 360.8 s, 83.7 MB, --check4k 3840x2160, MARK yes, BOOKENDS yes; listen.py: key C, -15.7 LUFS, true peak -1.4 dB, no clicks,
  no silences; picture looked at; six frames of the AV1 file looked at (hook, reveal, hatch, two answer signs, recap).
- Shorts (one render each): each --check4k 2160x3840, MARK yes, pace_check 0 stretches over 8 s (longest 7.0 / 7.5 / 6.8 s), corner sheet looked at
  (sky, clouds, boards, the penguin's back), frames at the middle and end of every shot and 0.4 s after every reveal looked at, listen.py -15.4 LUFS,
  true peak -1.4 dB, no clicks, no silences, pictures looked at.
- review.py: PASS for all four (no lesson spec or job for a cartoon, so its word and variety checks do not run, as for every cartoon); contact sheet
  of the lesson looked at.
- upload_guard.py: OK TO UPLOAD for all four; `--audit` 0 failures, 0 topic pairs.
- Plan entries: status to_upload with title, description (no '<' or '>', no AI, the channel boilerplate, where the facts come from), tags, thumb,
  thumb_text, seconds. Titles: "Whose Egg Is This? Guess With Milo" (lesson, Nov 28 5:30 PM); Shorts "Whose Giant Egg Is This? Guess With Milo"
  (Dec 2 7:30 AM), "Whose Eggs Are in the Sand? Guess With Milo" (Dec 3 7:30 AM), "Whose Egg Is on His Feet? Guess With Milo" (Dec 4 7:30 AM).

## Not checked / for the owner's ears and eyes
- listen.py measures, it does not hear: nobody listened. "ostrich", "emperor", "brood pouch", "leathery", "ping-pong" were checked by word alignment
  only (all placed, none suspect); how Milo's voice says them is for the owner.
- New art the owner has not seen: ostrich (dad and mom), ostrich chick, emperor penguin with the egg and with the chick, the hatching egg, the nests,
  the beach at night.
- In the penguin question shots (16:9) the penguin's head is above the frame on purpose (the egg on the feet is the clue); in the quiz it stays so.
- Stills were taken at the end of every shot; mid-shot stills only through the finished frames (middle of every shot).
- Thumbnails looked at full size and the main one at 168x94; not compared with click data.
- A tiny blue dot is in two lesson frames at the very centre 0.3 s before an iris cut: the iris wipe, not a stray drawing.

## Defects for docs/IMPROVE.md (the daily run folds them in)
- 2026-11-27: stills.sh shows OLD pictures when the snapshot fails: sheet.py takes the newest snapshot folder that has files, so a failed toon.py
  --stills (here: KeyError for a place missing from art.PLACE) gave a sheet of the previous round with exit 0. Look for a changed picture, or remove
  `out/<id>/proj_l/.hyperframes/artifacts/snapshots/<old>` before each round. (why: zc_ep14 stills round 2 identical to round 1)
- 2026-11-27: a solid "front" prop that ends inside the picture (a nest lip with a 500 px block under it) shows its side edges in 9:16 views: hide a
  waiting actor with opacity 0 (fromto at 0) and taper ground props into the ground. (why: zc_ep14 9:16 stills)
- 2026-11-27: this machine had no `hyperframes` (npm i -g hyperframes@0.8.231) although setup.sh ran: the setup line's `which hyperframes` check matters.
