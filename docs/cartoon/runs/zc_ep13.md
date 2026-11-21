# zc_ep13 "How Do Polar Bears Stay Warm?" (scheduled 1:17 PM lesson build, Nov 21 2026, session_014CFVfXgMKBYjCDMoPebUaE)

State: FINISHED, all four files "to_upload" (the 6:31 AM daily run schedules them; nothing uploaded here).

Arctic week, fact lesson 1 (2D cartoon fact lesson + three 9:16 Shorts). Claimed 1:25 PM ET (commit ce982d0): lesson Nov 24 5:30 PM, Shorts Nov 27, 28, 30 7:30 PM.
`upload_guard.py --next lesson` listed no unfinished lesson. Files: `studio/cartoon/episodes/zc_ep13.py`, `studio/cartoon/art_zc_ep13.py` (new props only:
thermometer, fat_ruler, glow_ring, water_front, drops, paw_sole, den_cut, coat, splash, pointer; no character, place or older prop drawn differently),
`cartoon/zc_ep13.mp4` (AV1) and `cartoon/zc_ep13_short1..3.mp4`, thumbnails `brand/zoo/thumb_zc_ep13.jpg`, `brand/zoo/shorts/thumb_zc_ep13_short1..3.jpg`.

## Facts (read at the source today, 1:35-1:45 PM ET, by the session's page reader; quotes in the episode docstring)
- Loaded and used: San Diego Zoo Wildlife Alliance polar bear page and its Library fact sheet, National Geographic Education "Animals 101: Polar Bears",
  SeaWorld polar bear page, Lincoln Park Zoo "Polar Bear Adaptations" (PDF).
- NOT read: Polar Bears International's adaptation page (the reader's permission request timed out) and the SDZWA "21 cool polar bear facts" story
  (it redirected to another host, not followed). Nothing in the lesson comes from them.
- Left out on purpose: the clear, hollow hairs and the black skin (they are the next Arctic lesson, "Is a Polar Bear Really White?", which the closing
  names), and the small ears / short tail (already taught in zc_ep12, live).
- Said: thick fat under the skin, up to four inches, keeps it warm and helps it float in the cold water; two layers of fur (soft thick undercoat, long
  guard hairs on top) that work like a raincoat, water rolls right off on land; fur covers almost all of its body; fur on the bottoms of the feet keeps
  them warm and stops slipping; mama and cubs in a cozy snow den that can be much warmer inside; so warm they sometimes cool off in the chilly water.

## Checks
- Plan check (`toon.py zc_ep13 --plan`): exit 0. 358.9 s with the main intro at both ends (13.8 s and 320.9 s; content about 329 s), parts 85.3 / 85.6 / 83.8 s,
  662/662 words placed, 63/63 cuts on the half-beat, longest stretch without a change 5.67 s. Shorts' plans: 91.5 / 90.1 / 89.4 s, all words placed.
- Repeated-word cues: a script check found 15 cues on words said twice or more (fat, Bob, Thick, pat, warm?, Fur, Wiggle, Snuggle, Whoosh...): all numbered,
  then every numbered cue printed against its word and read.
- `listen.py --episode zc_ep13` (music without the voice, BEFORE rendering): key C major (fit 0.97), nothing outside the key, no click, no silence, tempo heard
  94.9 against 96. CLASH lines only the known ones: the bed's E4 over F2/F4 at its bar changes (107.4, 187.4, 237.4, 257.4, 297.4, 307.4, 337.4 s), E4+F4 at
  28.6 s (the intro score's last E over the bed's F bar as the bed comes back, same as zc_ep12) and at 357.9 s (the closing intro's last chord), and the
  answer ding's C6 over the bed's B4 at 114.5 s (0.26 s). This lesson has no tune shot. Picture looked at.
- Stills: one still at the START (+0.9 s) and at the END (-0.3 s) of every shot outside the intro in 16:9 (59 shots), three rounds plus partial rounds after
  each fix; 9:16 stills of every shot of each Short at start and end, two rounds plus partial rounds.
- Lesson rendered twice in 4K (37 min each). First file: pace_check FAILED (46.2-57.2 s, 11.0 s: the two coat-board shots kept one camera and only pulsed);
  frames showed RAINCOAT! under the watermark, TOO HOT! on Poppy's back, the secret-3 "?" cut by the frame top. All fixed, rendered again.
- Final lesson file: `--check4k` 3840x2160; pace_check 0 stretches over 8 s (longest 8.0 s); watermark check MARK yes; corner sheet looked at (nothing under the
  mark: sky, board grid, the zoo gate's post); frames of the finished file at the end of every shot, the first frames of the intro shots and 0.6 s after every
  answer reveal (76 frames) looked at; listen.py on the file: -15.7 LUFS, true peak -1.4 dB, 0 clipped samples, no clicks, no silences, picture looked at.
- Shorts (2160x3840): short1 91.5 s and short3 89.4 s: --check4k, pace_check 0 over 8 s (longest 5.8 / 4.8 s), MARK yes, corner sheets looked at (clouds and
  sky only under the mark), frames at every shot end and every reveal looked at, listen.py on the file (-15.5 / -15.4 LUFS, no clicks, no silences, pictures
  looked at). short2 (90.1 s): first render FAILED pace_check (53.8-62.0 s, 8.2 s: the "coldest days" close-up had no 9:16 push); given a 9:16 push
  (pcam2, 9:16 only, so the rendered lesson is unchanged) and re-rendered: --check4k, pace_check 0 over 8 s (longest 5.5 s), MARK yes, corner sheet
  looked at (sky, clouds, board grid), frames at every shot end and every reveal looked at, listen.py on the file (-15.4 LUFS, no clicks, no silences,
  picture looked at).
- AV1 lesson `cartoon/zc_ep13.mp4` (85 MB, 359.0 s, 3840x2160): --check4k, `bookends.py check` BOOKENDS yes (beginning and end), review.py PASS and its
  contact sheet looked at. review.py PASS for the three Shorts, contact sheets looked at. `upload_guard.py` OK TO UPLOAD for all four files.
- Thumbnails (thumb.py: 3 words at most, none of the title's words): NOT COLD?! (Poppy and a thermometer, also looked at at 168x94 px), BOB, BOB! (Poppy
  swimming), DRIP DROP! (the coat cut-away with rain drops), COZY TOES! (the furry paw sole). Looked at; the Short thumbnails were re-framed once
  (the bear was small, the words sat on the boards).

## Defects found and fixed (for docs/IMPROVE.md)
- Captions on a still sheet looked cut at the left edge: it was the sheet's own time label covering them (label moved to the top right). Not a film defect.
- Two board shots back to back with one camera and only pulses/blinks read as 11 s without change in pace_check (the plan check counted the pulses): the
  second board shot got its own framing and a pointing arrow. Rule: every board shot gets its own camera AND a picture that moves or appears.
- A word at fx .3, fy .07 sat under the watermark (RAINCOAT!), a big "?" at fy .15 was cut by the frame top, words beside a moving prop (TOO HOT! and the heat
  waves) collided: each moved and looked at again in the finished frames.
- `art_za_ep11.warm_layers` reads poorly as a lesson board (light-blue guard hairs on light blue, thin undercoat): a clearer `coat` cut-away was drawn in
  art_zc_ep13 (white guard hairs with a blue-grey line, a band of cream curls for the undercoat).
- The first paw sole had white fur strokes on the big pad that read as a face: moved between the toes.
- A splash drawn at Poppy's head covered her face: moved to her back.
- 9:16: the secret-3 close camera cut Poppy's body at the frame edge (now the whole-bear 9:16 view); the number and the "?" of each secret sat on one spot
  (now left and right); a board at full 9:16 width touched the frame edges (wider 9:16 camera).

## Not checked
- How the voice, the music and the pronunciation sound to a person: listen.py measures, it does not hear.
- The facts on the two pages that did not load (see above): not used.
- Nothing was uploaded and nothing was done in a browser or on the PC (this build does not upload; the 6:31 AM daily run schedules the four files).
