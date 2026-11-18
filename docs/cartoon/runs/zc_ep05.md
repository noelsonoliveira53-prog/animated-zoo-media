# zc_ep05 "What Is Inside a Camel's Hump?" - run note (session 014CFVfW1MkPtZxDNFc2sgYy, scheduled night run, Nov 18 2026, 1:43-4:30 AM UTC)

Cartoon fact lesson with Milo, Sandy the baby camel and her Mama, and its three Shorts. Nothing was uploaded: the daily run schedules the entries that are "to_upload".

## What exists
- `studio/cartoon/episodes/zc_ep05.py` ("beat": True) and `studio/cartoon/art_zc_ep05.py` (new props only: the hump from outside, a lump of fat, a bunch of grass, a backpack, the tuft close up, a milk drop, a question card, a dashed hump, calendar pages). No character, place or older prop is drawn differently. kit.py is not changed: the grown camel's points are added from the episode file (`kit.PT.setdefault("camel", ...)`).
- `cartoon/zc_ep05.mp4` (3840x2160, AV1, 321.7 s) and `cartoon/zc_ep05_short1..3.mp4` (2160x3840, AV1, 86.9 / 88.7 / 87.2 s, about 21 MB each; the task asked for AV1 encodes of every file, the zc_ep02 Shorts are in the repo as rendered in H.264).
- Thumbnails `brand/zoo/thumb_zc_ep05.jpg` (WATER OR FAT?) and `brand/zoo/shorts/thumb_zc_ep05_short1..3.jpg` (ALL FAT! / TALL OR FLOPPY? / CURLY TUFT!).
- Plan entries: `cartoon/zc_ep05.mp4` in upload_plan_3d.json (Nov 21, 9:30 AM), `cartoon/zc_ep05_short1..3.mp4` in upload_plan_shorts_zoo.json (Nov 22, 23, 24 at 7:30 PM).

## Facts (read at the source on Nov 18, quoted in the episode file's header)
San Diego Zoo Wildlife Alliance (camel), Encyclopaedia Britannica ("Do Camels Store Water in Their Humps?"), PBS Nature (camel fact sheet).
- Said: the hump stores fat, not water; the fat is an energy source / nourishment when food is scarce; the hump's size changes with the food; it leans over and droops when food is scarce and sits upright again when the camel eats; one hump and two humps; a calf has no hump, small peaks with a tassel of curly hair that show where the hump will form; a newborn walks beside its mother within half an hour; calves nurse; mothers and newborns hum; a week or more without water, several months without food; up to 32 gallons in one drinking session; tough lips eat thorns.
- Not read today, so not said: pounds of fat in a hump, how fast a camel drinks, where in the body the water goes, the age at which a calf's hump forms.
- Milo's comparisons, not facts: "like a backpack full of snacks", "like a little hat", "like a little hill of sand".
- The San Diego Zoo page now says "up to 32 gallons (145 liters) of water in one drinking session"; zc_ep01 says thirty gallons in thirteen minutes (National Geographic, read Nov 16). Both are quoted figures from different sources.

## Checks
- Plan check: lesson 321.7 s, parts 83.8 / 85.0 / 83.1 s, 6 places, 715/715 words placed, 85/85 cuts on the half-beat, 3/3 tunes entering on a beat, no suspect word, longest stretch without a change 3.7 s. Shorts: plan check passes for each.
- Stills of EVERY shot looked at in 16:9 and in 9:16 (three Shorts), three rounds, then the changed shots again. Found and fixed (the plan check saw none of them): an answer sign on Mama's face and on the board camel's face; Mama's nose, Sandy's tail, a board camel's feet cut by the frame; a sliver of Mama or of Milo at the frame edge in close shots on Sandy; words cut by the frame, on the watermark corner, on a camel's face (MILK, FOOD INSIDE, ENERGY), on the 9:16 title band, two labels on one spot (SANDY / MAMA); a backpack larger than the picture; a fat lump cut at the edge; captions on feet in 9:16; a half cut-away in 9:16; the calendar under the caption.
- Finished files: `toon.py --check4k` (all four), `pace_check.py --max 8` (0 stretches over 8 s in all four), `watermark.py check` (mark present) and the corner sheet looked at (nothing that matters under the mark), frames of the finished file looked at near the end of every shot and before and after every answer reveal (lesson: 6 reveals; one in each Short), `review.py cartoon/zc_ep05.mp4` PASS.
- Sound, measured by listen.py (it measures, it does not hear): music without the voice: key C major (fit 0.96), no tone outside the key, no click, no silence; the three tunes enter on beats 376, 381 and 391; the bells play the written notes one octave higher (Mama G C E, Sandy C G E), with the soft band on a C chord; the tunes are about 4 dB quieter than a spoken line before the final levelling. Finished lesson: -15.3 LUFS, true peak -1.2 dB, no clipped sample, no click, no silence. listen.py reports "CLASH E4 + F2/F4" for 0.3-0.6 s every 10 s: the same known F-major-7 colour of the 3D music bed at each A minor to F change, not a wrong note. It hears the bed's tempo as 64 (two thirds of 96; 75% of attacks on the half-beat grid, 29% by chance).

## Not checked / open
- Nobody has LISTENED: Milo's voice and pronunciation ("thirty-two gallons", "tuft", "Sandy"), and the three little tunes (bells and soft band) are for the owner's ears. Between Mama's tune and Sandy's tune the music bed comes back for about half a second on an F chord; listen.py shows it, whether it sounds odd is for an ear.
- The Short 3 picture was rendered twice: in the first file a sliver of Mama's tail showed at the right edge at the end of "the tuft" shot (seen in the finished frames, not in the stills, because the stills were taken at one moment of a slow camera move). Mama is now hidden in "the tuft" and "no!"; the lesson file was rendered before that change, and its 16:9 picture does not show her in those two shots (frames at the start, middle and end of both looked at).
- Small, left as it is: in Short 2 the IT CHANGES! label ends close to the top of the camel's head (it does not cover the face); in the question shots the board camel is small.
- review.py was run on the lesson; it has no spec or job file for a cartoon, so it did not check the words (toon.py's plan check does).
- The lesson's title is the first half of zc_ep01's title ("What Is Inside a Camel's Hump? Baby Camel Story with Milo", scheduled); the plan line gave this title. The three Short titles are new.
- No Studio, no browser, no upload in this run.
- All four plan entries are "to_upload": stills, finished frames and every check passed for each file. `review.py` PASS on all four (it appended four rows to docs/REVIEW_LOG.md, as it always does).
- One frame of two of the AV1 files was looked at after encoding; the frame look of every shot was done on the 4K H.264 renders they were encoded from (kept in studio/cartoon/out/zc_ep05/ on the session machine only, not in git).

## Defects for docs/IMPROVE.md (the daily run folds these in)
- stills.sh takes one still at t1-0.3 of each shot: with the slow push-in or pull-out a thing at the frame edge can show at the other end of the shot. Look at the first frame of close shots too, or give close shots `cam2`/`pcam2` equal to the camera.
- A 16:9 answer sign sits at x = 600 and 1320, y = 178: a character whose head is at the right third of a wide view is under the second sign. Question views now keep heads under y = 300 on screen.
- A board camel at (880, 930, 1.05) with camera (960, 520, 1560) has its feet under the 16:9 caption; `BCAM = (960, 585, 1640)` keeps them above it.
- A long render was lost once when the session's background processes were stopped (tmux server gone, 03:47-03:55); the render was started again and finished.
