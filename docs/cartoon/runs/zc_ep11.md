# zc_ep11 "Whose Feet Are These? Guess With Milo" - run note (session_014CFVfY3R62hFRMYeAWfnuR, scheduled 1:17 PM ET lesson build, Nov 20)

Scheduled, unattended build: the first Guess With Milo episode (2D cartoon lesson, docs/CARTOON_RUN.md "Guess With Milo", "VIRAL PACKAGING", "MAIN INTRO") and its three Shorts. Nothing was uploaded; no Studio, no browser, nothing on the PC.

## Why this title
`upload_guard.py --next lesson` (1:23 PM ET): unfinished_first empty; first THEMES title "Whose Feet Are These? Guess With Milo" (theme "guess"), id zc_ep11, lesson Nov 23 5:30 PM, Shorts Nov 27 7:30 PM / Nov 28 7:30 PM / Nov 29 11:30 AM. No other session's commit named the id or title. Claimed in commit 9b4383f (that commit re-wrote the shorts plan with \u escapes for the non-ASCII characters of older entries; the JSON content of every older entry is unchanged).

## What exists
- `studio/cartoon/episodes/zc_ep11.py` ("beat": True, `*intro_shots()` right after the hook) and new art only in `studio/cartoon/art_zc_ep11.py`: new rigs `giraffe`, `zebra`, `zebra2` (other stripes), three footprints (elephant: big and round with nail marks; giraffe: two halves; zebra: one smooth hoof), foot close-ups for the boards (elephant foot from the front with five nails; elephant foot cut open: toe bones on tiptoe over a soft cushion that squishes; giraffe foot with two hooves; zebra foot cut open: one toe inside one hoof), a dinner plate seen from above, a bump, rumble lines, a side arrow, a question-mark disc, and the place `sandtrail` (the savanna with a wide sandy path). kit.PT/BOX entries for the new kinds are set from the art file. No existing character, prop or place changed. No engine change.
- (finished files: see the end of this note)

## Facts (read Nov 20, about 1:35-1:45 PM ET, by the session's page reader, which quotes the sentences it finds; quotes in the episode file's header)
Read: SDZWA Library African elephant (Physical Characteristics, Behavior); Live Science "Giraffe Facts & Photos"; SDZWA Animals and Plants "Giraffe"; SDZWA Library giraffe (Behavior, Physical Characteristics); SDZWA Library plains zebra (Physical Characteristics); PBS Nature zebra and giraffe fact sheets (read; the zebra one has nothing on hooves or stripes, nothing taken from it; the giraffe one confirms the calf standing about an hour after birth).
The first read of Live Science gave the two-hooves sentence only as a summary; it was read again and the sentence quoted verbatim ("two weight-bearing hooves on each foot") before it was used.
Said: elephant walks on tiptoes; big, soft cushion under its toes that soaks up the bump of a heavy step; some elephants have four nails on a front foot, some five; elephants may feel tiny rumbles in the ground with their feet; giraffe: two hooves on each foot, feet as big as a dinner plate, the two legs of one side move together then the other side, so front and back legs do not bump, a baby giraffe stands and walks about an hour after it is born; zebra: one toe on each foot, the hoof wraps around the toe and keeps it safe, a hoof keeps growing (said "a little like your fingernails", a comparison), every zebra has its own stripes.
Not said: nails on hind feet, speeds, leg length in feet, heights and weights. The pilot draft's "Each leg is about as tall as a grown-up" was left out.

## Checks that passed
- Plan check: lesson 348.1 s, parts 86.6 / 86.2 / 86.2 s (Shorts 90.6 / 90.5 / 91.0 s with their hooks), 7 places (sandtrail, intro_gate, intro_logo, river, zoo, savanna, zoo_eve) + 3 boards, 669/669 words placed, 66/66 cuts on the half-beat, 3/3 intro tunes on a beat, no suspect word, longest stretch without a change 4.3 s, 32 question moments (12 with answer signs, thinking dots and the reveal at wait:2.0), longest without a question 20.6 s; first words at 0.42 s ("Look! A giant footprint in the sand! Who made it?"), Milo's name at about 8 s, first answer signs at about 37 s in the lesson (after the 15 s main intro) and at about 9 s in Short 1.
- Three "Hmm." words were not placed by the word aligner: taken out of the three thinking lines (the "?" word now comes on the question's last word).
- Repeated-word cues: a script check found 11 cues on words said twice in their line; all given their number before the stills.
- listen.py --episode (music without the voice, BEFORE rendering): key C (fit 0.96), no click, no silence, tempo 95.0. The intro's three tune shots (the shared intro.py tune) show no clash. The 12 CLASH lines are E4 over F2/F4 at the bed's bar changes (7.4, 67.4, 87.4, 197.4, 217.4, 277.4 s), the known E-over-F moments of the 3D lessons' bed, none inside a tune. Picture looked at.
- Stills of EVERY shot at the START and the END in 16:9 (67 shots) and in 9:16 for every shot of each Short, then the changed shots again after each fix (16:9: 9 rounds counting the partial ones; 9:16: 3). Found and fixed:
  - prints too high in the frame (sky filled the picture, BIG!/ROUND! words over the sky line): cameras lowered onto the sand;
  - the three hook numbers at the bottom on the caption: moved above the prints;
  - GUESS WITH MILO! pill across Milo's face: one word GUESS! beside him; Milo's close-ups cut his crest: wider;
  - the elephant walk-in stopped ON its own print: walks past it; ELEPHANT! word moved off its back;
  - foot close-ups so big they touched the caption (16:9 and 9:16): smaller and higher;
  - "?" words sitting on the elephant's, giraffe's and zebra's backs or faces: moved to free sky;
  - THIS SIDE! / THAT SIDE! and NO BUMP! on the giraffe's body: moved left; the side arrow first lay on the ground under the legs, then moved beside the body;
  - rumble lines drawn in the river water: the rumbles shot moved to the sandy path, lines at the feet; RUMBLE! first on the elephant's back, then under the mark, then placed left of the elephant;
  - the soaks-up-the-bump lines were white on a pale board (invisible) and on the caption: blue, beside the foot;
  - the elephant-foot cutaway read as an empty box: a light fill inside, darker bone outlines;
  - the giraffe's two hooves read as one block: taller hooves with a clear gap;
  - dinner plate drawn as a tilted ellipse beside the foot: a round plate from above with the giraffe print lying on it (same size as the plate);
  - the footprint trail recap: prints on the caption, YOU DID IT! on the giraffe: prints smaller and higher, word above;
  - 9:16: elephant, giraffe and zebra close-ups cut at the frame edges (whole-animal 9:16 views), the 9:16 "4 / 5" over the nail board, the wobbling calf hidden behind the big giraffe (calf alone in that shot).
- Lesson render 1 (4K): pace_check found one 8.2 s stretch without a visual change (the third quick check's thinking time: still board, signs bobbing only). Fixed in all three quick checks: a slow push in, the picture pulses in the pause, and a "?" pops in on the question's last word. Also from the frames of render 1: RUMBLE! sat on the elephant's back at the shot's end in 16:9 (the camera drifted in) - the shot now pulls out; GIRAFFE! on the giraffe's neck at the walk-in's end - moved right of it. The lesson was rendered again with these fixes.
- Short 1 render 1: its 9:16 rumbles shot drifted in and cut the elephant's back - pull-out camera; rendered again (render 2 frames looked at, every shot middle and end and the reveal: clean).

## Not checked / for the owner's ears
- listen.py measures, it does not hear: nobody listened. "Giraffe", "zebra", "hooves", "tiptoes", "rumbles" were checked by word alignment only (all placed, none suspect); how Milo's voice says them is for the owner.
- New art the owner has not seen: the giraffe and the zebra (first cartoon versions of both), the foot cutaways, the sandy path. Guess With Milo itself is a new opening on the approved lesson format; CARTOON_RUN says to send the owner the first finished episode.
- The iris wipe covers the picture and the mark for 2-3 frames, as in every cartoon.
- pace_check's "SAME SHOT" line (no cut, no camera move) reads up to 11.5 s; its gate (8 s without any visual change) is what the rule asks.
- review.py: no lesson spec or job for a cartoon, so its word and variety checks do not run (as for every cartoon).

## Defects for docs/IMPROVE.md (the daily run folds them in)
- 2026-11-20: A quick-check board with one still picture and bobbing signs gave 8.2 s without a visual change in the thinking time (pace_check, first 4K render of zc_ep11, one 30-min re-render): every answer-sign question on a board gets a slow push or a picture that pulses in the pause, and a "?" on the question's last word. (why: zc_ep11 pace_check)
- 2026-11-20: Words and props placed from the START still of a shot with a push-in camera end up on the animal at the END (RUMBLE!, GIRAFFE!): look at the end still of every shot after moving a word, and give shots with a word beside a big animal a pull-out (cam2 wider). (why: zc_ep11 frames of render 1)
- 2026-11-20: The word aligner does not place a spoken "Hmm." (3 of 3): use "?" on screen for the thinking moment instead of a "Hmm." in the line. (why: zc_ep11 plan check)
- 2026-11-20: Live Science's two-hooves sentence first came back from the page reader as a summary, not a quote; it was read again verbatim before use. A fact is used only from a verbatim quote. (why: zc_ep11 fact reading)
- 2026-11-20: A foot cutaway drawn with a half-transparent fill read as an empty box on the board, and white bump lines vanished on the pale blue board: board props need a solid fill and a dark line. (why: zc_ep11 stills, round 2)
- Short 3 render 1: pace_check found 8.5 s without a visual change in its quick check (the 9:16 view had no push). Fixed with a 9:16 push (pcam2) on that shot, still looked at, rendered again: 0 stretches over 8 s.

## Finished files
- `cartoon/zc_ep11.mp4`: AV1 + AAC, 348.1 s, 82.3 MB; --check4k 3840x2160; watermark check MARK yes. Checks on the H.264 render it was encoded from (final render 3): pace_check 0 stretches over 8 s (longest 7.0 s), corner sheet looked at (nothing under the mark: sand, sky, board grid, the edge of a sign), frames at the middle and end of every shot and 0.4 s after all 12 answer reveals looked at (167 frames). listen.py on the AV1 file: -15.6 LUFS, true peak -1.3 dB, no clipped samples, no clicks, no silences, picture looked at. Eight frames of the AV1 file itself and review.py's contact sheet of it were looked at; the AV1 file was not looked at frame by frame.
- Shorts copied byte for byte (cmp) from the renders: `cartoon/zc_ep11_short1.mp4` 90.6 s, `_short2.mp4` 90.5 s, `_short3.mp4` 91.0 s, 2160x3840 H.264 (as zc_ep09/zc_ep10 Shorts). Each: --check4k, pace_check 0 stretches over 8 s (longest 6.0 / 8.0 / 6.8 s), MARK yes, corner sheet looked at (nothing under the mark), frames at the middle and end of every shot and after every answer reveal looked at, listen.py -15.6 / -15.3 / -15.5 LUFS, true peak -1.4 dB, no clicks, no silences.
- Thumbnails: `brand/zoo/thumb_zc_ep11.jpg` (WHO?: the giant elephant print with Milo looking at it; also checked at 168x94), `brand/zoo/shorts/thumb_zc_ep11_short1..3.jpg` (SQUISH! / HALVES? / CLIP CLOP!, each print alone). thumb.py accepted the words (none of the titles' words, 2 at most). The first main thumbnail had the word and the print small: redrawn bigger and looked at again.
- review.py: PASS for all four; contact sheets (studio/zoo3d/finished/review_zc_ep11*.png) looked at (blue discs are the iris wipe frame).
- upload_guard.py: OK TO UPLOAD for all four.
- Plan entries: status to_upload with title, description (no '<' or '>', the channel boilerplate, where the facts come from), tags, thumb, thumb_text, seconds. Not uploaded: the 6:31 AM daily run schedules them (lesson Nov 23 5:30 PM; Shorts Nov 27 7:30 PM, Nov 28 7:30 PM, Nov 29 11:30 AM).
