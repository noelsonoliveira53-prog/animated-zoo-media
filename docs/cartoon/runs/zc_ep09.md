# zc_ep09 "What Do Camels Eat in the Desert?" - run note (session_014CFVfYJyTj4rc8TGoYFmDc, scheduled 1:17 PM ET lesson build, Nov 19)

Scheduled, unattended build: one cartoon fact lesson (Milo, Sandy the baby camel and Mama look for lunch in the desert) and its three Shorts. Nothing was uploaded; no Studio, no browser, nothing on the PC.

## Why this title
`upload_guard.py --next lesson` (1:25 PM ET): unfinished_first empty; first THEMES title "What Do Camels Eat in the Desert?" (Desert week), id zc_ep09, lesson Nov 22 5:30 PM, Shorts Nov 26 7:30 PM / Nov 27 11:30 AM / Nov 28 11:30 AM. Claimed in commit 204277d.
Kept off the live zc_ep01 topics (eyelashes, nose, feet, hump, drinking): this lesson is about food, lips and chewing only.

## What exists
- `studio/cartoon/episodes/zc_ep09.py` ("beat": True) and new art only in `studio/cartoon/art_zc_ep09.py`: a camel's face from the front with the split top lip (two halves that wiggle), the inside of the mouth with hard cone bumps that point to the throat and an arrow down, a fingertip with its nail, food pictures (grass, leaf, twig, thorny branch, saltbush with salt sparkles, hay from art_zc_ep05), a leafy bush whose leaves can be eaten one by one, a loop arrow. No existing character, prop or place was changed. No engine change.
- Lesson `cartoon/zc_ep09.mp4`, 315.4 s, 3840x2160, AV1, 74.7 MB. Status to_upload (Nov 22 5:30 PM).
- Shorts `cartoon/zc_ep09_short1.mp4` ("What Does a Baby Camel Eat?"), `_short2.mp4` ("How Can Camels Eat Thorny Plants?"), `_short3.mp4` ("Why Do Camels Chew Their Food Again?"): 88.3 s each, 2160x3840, as rendered (H.264). Status to_upload.
- Thumbnails: `brand/zoo/thumb_zc_ep09.jpg` (THORNS? YUM!: Mama eating at the thorny bush), `brand/zoo/shorts/thumb_zc_ep09_short1..3.jpg` (MUNCH, MUNCH! / TOUGH LIPS! / SALTY SNACK!). thumb.py accepted the words; all four looked at (the first lesson thumbnail had the words over Mama's head and the camel cut: redrawn, looked at again).

## Facts (read Nov 19 about 1:40 PM ET, quoted in the episode file's header)
San Diego Zoo Wildlife Alliance camel page (animals.sandiegozoo.org/node/173), San Diego Zoo library fact sheet "Camels: Diet", National Geographic "how camels eat cactus" article, National Geographic Arabian camel facts, SeaWorld dromedary camel.
Said: camels eat desert plants (grass, leaves, twigs); a few leaves from each plant, then on to the next; they spend their days eating; many animals cannot eat thorny plants, camels can; big, tough lips; the top lip is split in two and each half moves on its own; tough but bendy lips pick at little leaves; lots of little bumps inside the mouth, hard like fingernails, that push the food down toward the tummy; camels can eat salty plants like saltbush; salt is very important for camels; camels bring their food back up and chew it again; at the zoo camels eat hay.
Not said: cactus and its needles (National Geographic says eating them can hurt), fish, cows and sheep, amounts of salt, hours, poisonous plants, drinking, water in plants, breath.
How the pages were read: the session's page reader, which quotes the sentences it finds; not compared by a second method.

## Checks that passed
- Plan check: lesson 315.4 s, parts 84.7 / 83.8 / 83.8 s, 6 places (trail, dunes, zoo, dune_eve, oasis, night) + 3 boards, 631/631 words placed, 77/77 cuts on the half-beat, no suspect word, no song (no tune, so no instrument shot). Shorts 88.3 / 88.3 / 88.3 s, each plan check passes.
- listen.py --episode (music without the voice, BEFORE rendering): key C, no click, no silence; only the known E-over-F moments of the bed at the 10 s bar changes (no tune in this episode).
- Stills of EVERY shot, at the START and the END, in 16:9 (78 shots) and in 9:16 for each Short (23 / 21 / 22 shots), then again for every changed shot, eight rounds in all. Found and fixed: Milo's words on his crest in every Milo shot (moved to the top right in 16:9, Milo lower in 9:16); Mama cut at the right edge at the trail and the oasis (moved right, bush moved); the leafy bush covering Sandy's face; the bush shot cutting Mama's head in half; board pictures too low under the caption in 9:16 and words on them; the mouth bumps pointing sideways (rotation fixed, cones made longer) and the mouth looking like a cup (lip rim added); the split-lip arrow pointing at the nose; the bumps-and-arrow word on top of the mouth; the loop arrow covering the camel's head; the 9:16 Sandy-and-bush views cutting Sandy's tail and the bush; Milo cut at the right of the 9:16 oasis question view; the 9:16 bendy-lips board cut at the top; two oasis Milo words in the palm leaves; the quiz-3 muzzle under the answer signs.
- First lesson render: pace_check found 13.8 s with no visual change (2:09.8-2:23.5, four lip boards with one camera). Fixed with three different cameras (close on the lip, wide for the count, middle for the wiggle), stills of those shots looked at again, lesson rendered again. Frames of the first render (106: every shot end and every answer reveal) were looked at.
- Final lesson (second render): --check4k 3840x2160, pace_check --max 8 (0 stretches over 8 s, longest 7.2 s), watermark check MARK yes, corner sheet looked at (nothing under the mark; the two all-blue pictures are the iris wipe), frames at the end of every shot and every answer reveal: shots 13-47 and 61-70 looked at on this file, the others are the same picture as the first render whose frames were looked at. AV1 file: --check4k, MARK yes, listen.py (-15.3 LUFS, true peak -1.4 dB, no clipped samples, no clicks, no silences, picture looked at), review.py PASS, contact sheet looked at.
- Shorts: --check4k 2160x3840, pace_check --max 8 (0 stretches over 8 s; longest 5.0 / 5.0 / 5.5 s), MARK yes and corner sheets looked at (nothing under the mark), frames at the end of every shot and every answer reveal looked at, listen.py (-15.4 / -15.2 / -15.3 LUFS, true peak -1.5 / -1.4 / -1.5 dB, no clicks, no silences, pictures looked at), review.py PASS, contact sheets looked at.
- upload_guard: OK TO UPLOAD for all four.

## Not checked / for the owner's ears
- listen.py measures, it does not hear: nobody listened. Milo's voice on "saltbush", "Sandy", "twigs", "fingernails" was checked by word alignment only.
- The iris wipe between places covers the picture and the mark for 2-3 frames (a small ring at the frame middle in the last frame before it, and a full blue frame in review contact sheets), as in every cartoon so far.
- pace_check's second line (same shot without a cut or a camera move) reads up to 11.0 s in the lesson (boards where pictures change); its gate passes.
- The new boards (the camel's face from the front, the inside of the mouth) are new drawings: the owner has not seen them.
- review.py: no lesson spec or job for a cartoon, so its word and variety checks did not run (as for every cartoon).

## Defects for docs/IMPROVE.md (the daily run folds them in)
- 2026-11-19: Several picture boards in a row with the SAME camera (four lip boards) read as 13.8 s without a visual change in pace_check, although each board had a new prop or word: consecutive boards of one picture need different cameras. (why: zc_ep09 first render, pace_check)
- 2026-11-19: A MILO(place) shot puts the top-right word (fx .74, fy .22) on Milo's crest in 16:9 and in 9:16; the word must sit at fy .1 and Milo lower in 9:16 (V(..., 1100, 0, -90)). (why: zc_ep09 stills, first round)
- 2026-11-19: Cone shapes in art drawn pointing up, then turned by atan2(dy, dx) - 90, pointed sideways: for a path that points DOWN, the turn toward a point is atan2(x, dy). (why: zc_ep09 mouth board stills)
