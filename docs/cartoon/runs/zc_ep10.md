# zc_ep10 "One Hump or Two? Meet the Camels" - run note (session_014CFVfWzLWjjXdMstD7F8d5, scheduled 1:47 AM ET lesson build, Nov 20)

Scheduled, unattended build: one cartoon fact lesson (Milo meets Sandy's Mama, a dromedary, then flies to the snowy Gobi to meet Sandy's two-humped camel cousin) and its three Shorts. Nothing was uploaded; no Studio, no browser, nothing on the PC.

## Why this title
`upload_guard.py --next lesson` (about 1:55 AM ET): unfinished_first empty; first THEMES title "One Hump or Two? Meet the Camels" (Desert week), id zc_ep10, lesson Nov 23 9:30 AM, Shorts Nov 29 / Nov 30 / Dec 1 7:30 AM (each on its own day, no camel day). Claimed in commit 12ba6ea (the claim commit re-encoded the emoji escapes of other entries; commit after it restored the files byte for byte and appended only the four entries).
Kept off the live and built camel topics: no fat in the hump (zc_ep01), eyelashes, nose, feet, drinking (zc_ep01, za_ep07), food, lips, chewing (zc_ep09). zc_ep01 part 3 counted the cousin's two humps in one shot; this lesson is about the two kinds, where they live and the winter coat.

## What exists
- `studio/cartoon/episodes/zc_ep10.py` ("beat": True) and new art only in `studio/cartoon/art_zc_ep10.py`: two new kinds registered there (`bac_winter`: the existing Bactrian drawing plus eight shaggy patches #<pid>-sh0..7 that can fall to the ground one by one; `bac_summer`: the same camel without bib and patches), `bactrian_short` (the cousin drawn 1.1 wide x 0.88 tall on the comparison boards only), a letter B that turns -90 degrees so its bumps point up, snowflake, sun and flower discs, grey rocks with snow, a loose patch of shed hair, a dashed height line, and the place `gobi_spring` (the Gobi with green grass, snow only on the mountain tops). kit.PT/BOX entries for camel, bactrian and the two kinds are set from the art file. No existing character, prop or place was changed. No engine change.
- Lesson `cartoon/zc_ep10.mp4`: 315.7 s, 3840x2160, AV1. Status to_upload (Nov 23 9:30 AM).
- Shorts `cartoon/zc_ep10_short1.mp4` "Which Camel Has Two Humps?" (90.2 s), `_short2.mp4` "Where Do Camels Live in the Snow?" (88.2 s), `_short3.mp4` "Why Does a Camel's Coat Fall Off?" (89.0 s): 2160x3840, as rendered (H.264). Status to_upload.
- Thumbnails: `brand/zoo/thumb_zc_ep10.jpg` (COUSINS?!: the dromedary and the shaggy Bactrian face to face), `brand/zoo/shorts/thumb_zc_ep10_short1..3.jpg` (LIKE A B! / BRRR, COLD! / PLOP, PLOP!). thumb.py accepted the words. All four looked at; the first versions of the three Short thumbnails had the words across the camel and the camel cut at the frame: redrawn (wider cameras, words in the sky, the turned B above the camel) and looked at again.

## Facts (read Nov 20 about 2:10-2:30 AM ET; quoted in the episode file's header)
Read: National Geographic Kids "Bactrian camel"; National Geographic "Bactrian camel"; Lincoln Park Zoo, Denver Zoo and Brookfield Zoo "Bactrian camel"; San Diego Zoo Wildlife Alliance Library fact sheet "Camels: Summary"; Oakland Zoo and Sydney Zoo "Dromedary camel"; PBS Nature "Camel Fact Sheet".
Could NOT be read this session (permission/provenance refusal of the page reader), nothing taken from them: animals.sandiegozoo.org camel page, SeaWorld dromedary camel, the National Geographic Arabian camel URL.
Said: one hump = dromedary; two humps = Bactrian camel; two humps like the letter B (Denver Zoo); the two-humped camel is the dromedary's camel cousin (Sydney Zoo's word); dromedaries are taller with longer legs (SDZWA library); Bactrians shorter and heavier (Denver Zoo); dromedaries live in hot, dry deserts; the sand is hot; Bactrians live in the Gobi Desert, far away in Asia, a rocky desert; very, very cold in winter, snow in winter, hot in summer; a dromedary's coat is short and light; Bactrians grow a thick, shaggy coat for winter that keeps them warm; in spring it falls off in big patches; that is shedding; then the coat is thinner for summer; a new thick coat grows for the next winter.
Not said: fat in the humps, numbers (heights, weights, -20 F), wild camels and how few are left, Mongolia and China by name, Australia, water, eyelashes, feet.
How the pages were read: the session's page reader (a subagent), which quotes the sentences it finds (kept to short quotes); not compared by a second method.

## Checks that passed
- Plan check: lesson 315.7 s, parts 86.3 / 83.8 / 83.8 s, 7 places (gobi, zoo, dunes, trail, oasis, gobi_spring, night) + 3 boards, 629/629 words placed, 77/77 cuts on the half-beat, no suspect word, longest stretch without a change 5.0 s, 29 question moments (plan count; 12 of them with answer signs, thinking dots and the reveal at wait:2.0), longest stretch without a question 21.2 s. Shorts 90.2 / 88.2 / 89.0 s, each plan check passes. Two lines were changed to pass: "Brrr!" (suspect word, 1.0 s) and "Zip!" (not placed) are no longer spoken (BRRR! and ZIP! stay as on-screen words).
- Repeated-word cues: a script check found 23 cues on words said twice in their line; all given their number (w:word:N) before the stills.
- listen.py --episode (music without the voice, BEFORE rendering): key C (fit 0.96), no click, no silence, no tune in this episode (no song moment, as in zc_ep09). It lists 55 "clashes": E4 over F2/F3/F4 at the bed's 10 s bar changes (the known E-over-F moments of the bed, same as zc_ep09) and one B4 + C6 at 284.5 s (the answer ding over the bed's G bar, OPEN in IMPROVE since za_ep05). None is inside a tune. Picture looked at.
- Stills of EVERY shot at the START and the END in 16:9 (78 shots), then the changed shots again; 9:16 of every shot of each Short at start and end (24 / 22 / 21 shots), then the changed shots again. Rounds: 16:9 three, 9:16 three. Found and fixed:
  - the shaggy patches too big and dark (they hid the camel's shape): smaller, lighter, thinner outline;
  - falling patches landed in a heap under the body: each lands at its own spot beside the legs, so three can be counted;
  - on the comparison boards the cousin looked as tall as the dromedary although the line says "taller": she is drawn shorter and wider there (bactrian_short), and the dashed height line sits on the dromedary's head;
  - in 9:16 the two camels of the pair boards stood one above the other, so taller/shorter could not be seen, and the lower one sat under the caption: one side-by-side 9:16 camera (PAIRP) for every pair board;
  - words in the top-left corner on the watermark in 16:9 (16 words): moved to fx .33, fy .26;
  - 9:16 words under or on the title band (LONG LEGS, TALLER!, HEAVY!, COLD!, HOT!, PLOP!, YOU KNOW!, "?"): moved below the band;
  - the 9:16 "1" and "2" of "one and two" on the title band, the 9:16 SUMMER word on WINTER, THERE! on the snowflake, PATCHES! on the camel's head: moved;
  - boards whose picture popped in a second after the shot started (B, snowflake, sun, three snowflakes, the hook pair, one-and-two): the picture is there from the first frame and pulses on its word;
  - Milo flying out of the 9:16 frame on "fly far away": a short hop up instead;
  - the hook's 9:16 close-up cut the cousin's head: whole-camel 9:16 views for the hook, the coat close-up and the spring shots;
  - quiz 2 and quiz 3 answer signs on Mama's head (16:9): wider, lower cameras;
  - HEAVY! on the cousin's face in 16:9: moved to the left.
- Lesson render: --check4k 3840x2160; pace_check --max 8: 0 stretches over 8 s, longest 5.5 s (second line: same shot up to 15.8 s, its gate passes); watermark check MARK yes; corner sheet looked at (nothing that matters under the mark: sky, board grid, the edge of a sign or a cloud); frames of the finished file at the middle and the end of every shot and 0.4 s after all 12 answer reveals (168 frames) looked at; listen.py on the file: -15.3 LUFS, true peak -1.4 dB, no clipped samples, no clicks, no silences, picture looked at.
- Shorts: --check4k 2160x3840 each; pace_check --max 8: 0 stretches over 8 s (longest 5.5 / 6.2 / 7.2 s); MARK yes and corner sheets looked at (nothing under the mark); frames at the middle and end of every shot and after every answer reveal looked at; listen.py -15.3 / -15.3 / -15.3 LUFS, true peak -1.4 / -1.5 / -1.3 dB, no clicks, no silences.
- See the end of this note for the AV1 file, review.py and upload_guard.

## Not checked / for the owner's ears
- listen.py measures, it does not hear: nobody listened. "Bactrian", "dromedary", "Dromedaries", "Gobi", "B" were checked by word alignment only (all placed, none suspect); how Milo's voice says them is for the owner.
- The new drawings (the shaggy winter coat and its patches falling, the cousin's summer coat, the Gobi in spring, the turned letter B) are new art the owner has not seen.
- The iris wipe between places covers the picture and the mark for 2-3 frames (a blue disc with a yellow dot shows in a few frames), as in every cartoon so far.
- pace_check's second line (same shot, no cut and no camera move) reads up to 15.8 s in the lesson and 21.2 s in Short 1 (boards where pictures and words change); its gate (8 s without any visual change) passes. Short 1's pace_check counts only 9 cuts: same-colour boards in a row are not told apart by its frame difference.
- review.py: no lesson spec or job for a cartoon, so its word and variety checks do not run (as for every cartoon).
- Shorts are uploaded as rendered (H.264), as zc_ep09's were.

## Defects for docs/IMPROVE.md (the daily run folds them in)
- 2026-11-20: Comparison boards: two camel drawings at one scale showed the same height while the line said "the dromedary is taller"; a size claim needs the drawing to show it (bactrian_short) and a 9:16 view that keeps the two side by side, not stacked. (why: zc_ep10 stills, first round)
- 2026-11-20: A board picture that pops in on a word leaves an empty board for the first second of the shot (B, snowflake, sun, three snowflakes): show it from the first frame and pulse it on the word (same lesson as zc_ep06's seeds). (why: zc_ep10 start-of-shot stills)
- 2026-11-20: Words at fx <= .3 and fy <= .2 of a 16:9 camera land on the top-left watermark: 16 words in this script's first draft. Rule for the next script: no word above fy .24 left of fx .34. (why: zc_ep10 stills, first round)
- 2026-11-20: 23 cues on words said twice in their line were found by a script check before the stills (toon.py's warning for this is still OPEN since za_ep05). (why: zc_ep10)
- 2026-11-20: The page reader refused three fact pages (SDZWA camel page, SeaWorld, Nat Geo Arabian camel) with a provenance error; other zoo pages carried the same facts. (why: zc_ep10 fact reading)
- 2026-11-20: Short thumbnails: a camera close on the camel put the words across its body and cut its head; a 9:16 thumbnail needs the whole animal low and the words in the sky. (why: zc_ep10 thumbnails, first version)

## Finished files (after the AV1 encode)
- `cartoon/zc_ep10.mp4`: AV1 + AAC, 315.75 s, 74.8 MB; --check4k 3840x2160, watermark check MARK yes, listen.py on the AV1 file (-15.3 LUFS, true peak -1.4 dB, no clipped samples, no clicks, no silences; picture in studio/cartoon/out/zc_ep10/zc_ep10_av1_listen.png). The AV1 frames were NOT looked at frame by frame: the frames looked at are those of the H.264 render it was encoded from, plus review.py's contact sheet of the AV1 file.
- Shorts copied byte for byte (cmp) from the renders to `cartoon/`; --check4k 2160x3840 each.
- review.py: PASS for all four; contact sheets (studio/zoo3d/finished/review_zc_ep10*.png) looked at (the full blue disc in Short 3's sheet is the iris wipe frame).
- upload_guard.py: OK TO UPLOAD for all four (it counted 11 uploads in the last 24 hours by the commit log).
- Plan entries: status to_upload with title, description (no '<' or '>', the channel boilerplate, where the facts come from), tags, thumb, thumb_text, seconds.
