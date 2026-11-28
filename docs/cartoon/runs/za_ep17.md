# za_ep17 "How Does Hazel Find Snacks at Night?" (cartoon adventure, Night forest week 1: the first Hazel story)

Theme title "Hazel's Night-Time Snack Hunt". Slot: Nov 29 2026, 1:30 PM ET. Claimed Nov 27 by the scheduled 7:23 PM adventure build
(https://claude.ai/code/session_014CFVfXX1ET44dwkntqUY3i; claim commit 9032d80, about 7:27 PM ET by the session's clock). Status: **to_upload** (not uploaded; the 6:31 AM daily run schedules it).
File: `cartoon/za_ep17.mp4`, AV1 4K 3840x2160, 339.1 s (309.1 s own content + the main intro at the beginning and at the end), 81 MB.
Thumbnail: `brand/zoo/thumb_za_ep17.jpg` ("SNIFF, SNIFF!", none of the title's words; Hazel's nose down to the ground, smell lines rising, the moon behind).

## Setup and claim
- The session's repo was already there (a shallow copy of the lean main, 1.5 GB in .git, 26 GB free), so the light clone of the prompt was not needed;
  `git fetch --deepen=60` for the guard's 24-hour count. `upload_guard.py --audit`: 147 live videos, 0 failures, 0 topic pairs.
  setup.sh (voice model, Python modules) and `hyperframes@0.8.231` installed. The machine has 2 CPUs.
- `upload_guard.py --next adventure`: za_ep17, Nov 29 1:30 PM, "Hazel's Night-Time Snack Hunt", unfinished_first empty. The title was made a question
  for the viral packaging ("How Does Hazel Find Snacks at Night?", 36 characters); the THEMES title is kept as theme_title.

## Facts (read at the source today, about 7:30 PM ET; verbatim quotes in the episode's docstring)
- National Geographic "Hedgehog", Live Science "Hedgehog Facts", Warwickshire Wildlife Trust "About hedgehogs", Encyclopaedia Britannica "Hedgehog".
  The RSPB page that was also tried redirected to a news index and was not used.
- Said as facts: hedgehogs sleep in the day and look for food at night [NG, LS, EB]; hedgehogs can not see very well and use their nose (and ears) to
  find food [NG, LS, EB]; hedgehogs eat beetles, caterpillars and worms [WWT]. Hazel snuffles and grunts while she hunts [EB, NG]; the berries are fruit [LS].
- NOT said as facts: that hedgehogs look under logs (no page read says so: the log is this story); spines, rolling up, hibernation, milk, pets.
  Nobody eats a beetle on screen: the beetle scuttles off into the leaves; the snack shown and shared is blackberries.

## What was built and checked
- Episode `studio/cartoon/episodes/za_ep17.py` ("beat": True, the main intro after the hook and as the last four shots) and art
  `studio/cartoon/art_za_ep17.py` (new places dusk_wood, dawn_wood, leafwood, darkwood, logglade; kit points and box for "hedgehog", which art2 had
  not registered; props sniff, crunch, leafpile, biglog, berries, worm, caterpillar, skycard, hog_lids, zzz, bigmoon). Reused: art2 "nightforest",
  Hazel (art2.hedgehog as it is), art_zc_ep12.beetle, art_za_ep13.think_bulb, art_za_ep07.shut_eyes. Hazel's voice: af_sky, pitch +4, formant 1.2 (NEW).
- Story: hook (the moonlit wood, Hazel's nose sniffing: "How does Hazel find snacks at night?"), goal (Hazel wakes up hungry at dusk, sleepy Milo
  comes along), obstacle 1 (too dark under the tall trees for Milo's eyes), obstacle 2 (the dry leaves go crunch, the beetle scuttles away),
  obstacle 3 (the best smell is under a big log: too heavy to lift, too dark to peek), low moment (they sit; "Maybe we can not get the snack"),
  solution (Hazel's own idea: follow her nose and snuffle under; out come blackberries, enough for two), the rhyme said by Hazel, the tune on
  instruments, warm ending (sunrise: Hazel's bedtime in her leaf nest, Milo wide awake), recap questions, closing rhyme and tune, goodbye naming
  "Hazel and the Crunchy Leaf Bed". Nobody is hurt, lost, crying or trapped.
- Plan check: exit 0, 339.1 s (main intro at 7.8 s and 323.4 s, 30.0 s together: own content 309.1 s), 58 shots, longest gap 4.73 s, nothing over 6 s,
  6 places + 3 boards, 16 questions (longest stretch without one 43.4 s), every story beat, words 624/624, sync 57/57 cuts on the half-beat,
  8/8 songs on a beat, no suspect word.
- `listen.py --episode za_ep17` before the render: key C major (fit 0.94), no tone outside the key, no clicks, no silences, tempo 95.2 against 96.
  CLASH lines only the bed's E4 over F2 (87.4, 107.4, 137.4, 257.4, 297.4 s) and the answer ding's C6 against the bed's B4 (214.3, 304.4 s, 0.26 s,
  the known za_ep09 case); none inside the tune shots (258.1-268.1 s, 311.9-316.9 s). Picture looked at (`out/za_ep17/look/listen_episode.png`).
  listen.py measures, it does not hear.
- Stills: one still near the end of every shot in rounds 1 and 2 (`look/r1_*`, `look/r2_*`), round 3 of every shot after the second fixes
  (`look/r3_*`), the middle of every shot (`look/mid_*`), and the three shots changed last again (`look/r4_0`, `look/r5_0`).

## Defects found in the stills (each fixed and seen fixed in a later round)
- Round 1: Hazel's leaf nest was a solid brown dome and read as a turtle shell (redrawn as a loose heap of separate leaves with a doorway).
- The smell lines sat on Hazel's snout in the hook, her dark-wood close-up and the "nose or tail" board (moved in front of the nose).
- Hazel cut by the left frame edge in the dusk "Yes!" and day/night question, the beetle shot and every log-glade obstacle shot (cameras and places changed).
- Words and answer signs on Milo in the dark-wood copy-me and question shots (Milo moved low).
- Board captions on the hedgehogs' feet (day/night board, nose board): pictures raised.
- Crunch marks under Milo's feet in the "quiet or crunchy" question (moved right).
- "AWAKE AT NIGHT" under the channel mark at the top left, then cut by the top edge (moved to the top middle, lower).
- Round 2: after Hazel moved, her snout stood inside Milo in the four log-pushing shots (Hazel 500, Milo 800, cameras wider).
- Milo cut at the left edge and near the mark in the snuffle shot: he now watches from the top of the log; "GRUNT, GRUNT!" then touched him and
  later overlapped "SNUFFLE!" (both moved; seen in r5_0).
- Berries over Hazel's snout (moved right); "FOR TWO!" touching Milo (moved).
- Thumbnail 1: two moons (the backdrop's and a prop): the prop was taken out.

## Render and finished file
- Render 1 (4K, tmux, about 54 min on this 2-CPU machine): `--check4k` 3840x2160, `watermark.py check` MARK yes, `bookends.py` yes at both ends,
  frames looked at (`look/render1_fr_*`), but `pace_check.py --max 8` FAILED: 0:40.2-0:49.0 (8.8 s) and 4:49.0-4:58.8 (9.8 s). Cause: the dusk
  "day or night" question kept almost the framing of the shot before it (no cut seen), and the dawn "night or day" question had only a tiny push
  while the floating z's and the signs do not count as change. Fix: the dusk question opens wider and pushes in (700,640,1560 -> 780,700,1320);
  the dawn "night or day" question pushes in on Hazel (860,680,1700 -> 700,780,1200); "eyes or nose" opens on the wide view and pushes in.
  These three framings were NOT looked at in stills before render 2 (the stills tool shares the render's project folder); they were looked at in
  the frames of render 2 (middle, 1.1 s and 0.3 s before the cut): Hazel whole, Milo clear of the signs, the check mark on NIGHT / NIGHT / NOSE.
- Render 2 (about 54 min): `--check4k` 3840x2160; `pace_check.py --max 8 --shots`: PASS, 0 stretches over 8 s (longest 6.8 s; "same shot" 10
  stretches over 8 s, longest 24.5 s: board, question and tune shots); `watermark.py check`: MARK yes; corner sheet (`look/corner_tl.jpg`) looked
  at: under the mark only sky, tree tops, board paper and the corners of words and signs passing by (THIS WAY at 1:15, LEAVES at 1:50, answer
  signs); `bookends.py check`: intro at both ends.
- Frames of render 2 looked at (`look/fr_00..06.jpg`, 132 frames): middle and end of every shot (the intro shots too), every answer reveal 1.1 s and
  0.3 s before the cut (14 questions with signs: the check mark is on the right answer before every cut), the count (ends on 3), the copy-me moments,
  the rhyme shot and both tune shots. The render matches the stills.
- `listen.py` on the AV1 file: -15.4 LUFS, true peak -1.3 dB, no clipped samples, no clicks, no silences; picture looked at (`look/listen_file.png`,
  even level). With the speaking voice in the file it judges level and silences only. listen.py measures, it does not hear.
- AV1 file `cartoon/za_ep17.mp4` (encode about 24 min, 81 MB): 4K, AV1 + AAC, 339.1 s, MARK yes, BOOKENDS yes. `review.py cartoon/za_ep17.mp4`:
  PASS, contact sheet looked at (its first picture, at about 14 s, is the main intro's own star wipe filling the frame, cream; frames at 0 s and
  14.1 s pulled to make sure). Thumbnail looked at full size and at 168x94: the hedgehog, the smell lines and the words read at the small size.
- `upload_guard.py cartoon/za_ep17.mp4`: OK TO UPLOAD (14 of 20 uploads in the last 24 hours by the commit log); `--audit`: 0 failures.
- Small, kept: the known iris-wipe dot (a small blue ring in the last 0.3 s before an iris cut) shows on the board at 107.8 s and 160.9 s.
- Frames of the AV1 file itself were not looked at one by one (render 2's frames were; the AV1 checks are 4K, mark, bookends, listen, review's sheet).

## Not checked
- How the voices sound: Hazel (af_sky, pitch +4, formant 1.2) is a NEW voice; Milo is af_heart as always. Nobody has heard Hazel, the two tunes, or
  how "snuffle", "hedgehog" and "Grunt, grunt!" are said. listen.py measures, it does not hear. Noelson's ears decide.
- The look of the new places and of Hazel's first story is a first look for the owner. The night places are tinted blue; they were judged readable
  from the stills, not on a TV.
- A 9:16 version: none was built (an adventure has no Short).
- Small, kept: `("nod", ..., "milo")` in the "some friends sleep in the day" shot does nothing (Milo's rig has no neck; GSAP warned "#s48_milo-neck
  not found"); Milo stands a little above the moss when he is on the log; the dark wood's mushroom glows read as pale circles.

## Nov 28, 6:31 AM daily run: held, back to in_production
- Not uploaded: the episode has no like-and-subscribe goodbye. CLAUDE.md (owner Nov 27 7:29 PM) requires Milo's `intro.SUBSCRIBE_LINE` shot right before the closing `*intro_shots()` for za_ep17+; `grep SUBSCRIBE_LINE studio/cartoon/episodes/za_ep17.py` finds nothing and toon.py's plan check (lines 570-576) fails it. The build was claimed at 7:27 PM, two minutes before the rule.
- WHERE IT STOPS: the next adventure build finishes this first: add `S(<place>, say=SUBSCRIBE_LINE, ...)` (Milo's camera, "THANK YOU!" at about (.8, .18)) as the last shot before the closing intro, take "Bye-bye" out of the story's goodbye, plan check, listen.py --episode, stills of the new shot in 16:9, re-render, AV1, review.py, then "to_upload" on Nov 29 1:30 PM.

## Nov 28, 8:43 AM adventure build: like-and-subscribe goodbye added, re-rendered, to_upload again
Session https://claude.ai/code/session_014CFVfXab3DiYHdYpCYSXWN; claim commit 35ffd37 (about 8:50 AM ET). `upload_guard.py --next adventure` listed za_ep17 in unfinished_first; nobody had touched it since the 6:37 AM hold.
The session's repo was already there (a full, non-sparse checkout of the lean main, 5.2 GB, 24 GB free), so the light clone was not run. setup.sh and hyperframes@0.8.231 installed.
- Change: `from intro import ..., SUBSCRIBE_LINE`; a new shot "goodbye: like and subscribe" in dawn_wood (Milo alone, Hazel hidden, `say` = SUBSCRIBE_LINE, hops on "Thank" and "subscribe,", THANK YOU! at (.74, .2)) as the last shot before the closing `*intro_shots()`. The story's goodbye ("Next time: Hazel and the Crunchy Leaf Bed! See you on the next adventure, friends!") already had no "Bye-bye" and was not changed. Nothing else in the script changed, so the facts were not re-read today (read at the source Nov 27, the day the script was written).
- Plan check: exit 0, 349.7 s (main intro at 7.8 s and 333.8 s, 30.4 s together: own content 319.3 s), longest gap 5.16 s, nothing over 6 s, every story beat, words 649/649, sync 58/58 cuts on the half-beat, 8/8 songs on a beat, no suspect word, fails [].
- `listen.py --episode za_ep17` before the render: C major (fit 0.94), no clicks, no silences, tempo 95.2 vs 96; CLASH lines are the same known ones as before (bed E4 over F2 at 87.4/107.4/137.4/257.4/297.4 s; answer ding C6 vs bed B4 at 214.3/304.4 s), none inside the tune shots (258.1-268.1, 311.9-316.9 s). Picture looked at. listen.py measures, it does not hear.
- Stills of the new shot (and the goodbye before it), three rounds: `look/r6_goodbye.jpg` (same framing as the shot before: a cut that changes nothing and a 17 s stretch with the same camera, risk for the pace check), `look/r7_goodbye.jpg` (a push-in: THANK YOU! is fixed in the world and was carried off the top-right edge: DEFECT), `look/r8_goodbye.jpg` (a pull-out from Milo's close framing: Milo whole, the words clear of his head, the mark and the frame edges in every still: seen fixed).
- Render 3 (4K, tmux, about 55 min): `--check4k` 3840x2160; `pace_check.py --max 8 --shots`: 0 stretches over 8 s; `watermark.py check` MARK yes, corner sheet `look/corner3_tl.jpg` looked at (only sky, trees, board paper and the edges of words and signs passing by); `bookends.py` yes at both ends.
- Frames of render 3 looked at (`look/fr3_00..05.jpg`, 135 frames): middle and end of every shot, every question 1.1 s and 0.3 s before its cut (the check mark is on the right answer each time), the count, the rhyme and both tune shots, the new goodbye and the closing intro. Matches render 2 and the stills.
- AV1 `cartoon/za_ep17.mp4` (about 34 min): AV1 + AAC, 3840x2160, 349.75 s, 83 MB; `--check4k`, MARK yes, BOOKENDS yes. `listen.py` on the file: -15.4 LUFS, true peak -1.3 dB, no clipped samples, no clicks, no silences, picture looked at (`look/listen_file3.png`, even level). `review.py`: PASS, contact sheet looked at. Thumbnail unchanged (`brand/zoo/thumb_za_ep17.jpg`, looked at again).
- `upload_guard.py cartoon/za_ep17.mp4`: OK TO UPLOAD (the clone is shallow: its 24-hour count is the commit-message count only; `git fetch --deepen=60` did not finish in 5 minutes and was stopped. The daily run counts before uploading).
- Not checked: how the new line sounds (Milo's af_heart voice; nobody has heard it in this episode); the AV1 file's frames one by one (render 3's frames were looked at). Still unheard from before: Hazel's new voice and the two tunes. listen.py measures, it does not hear.
- Small, kept: the double farewell ("See you on the next adventure, friends!" then "... See you next time!").
