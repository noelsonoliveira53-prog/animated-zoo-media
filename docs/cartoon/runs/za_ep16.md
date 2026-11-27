# za_ep16 "Can Little Clover Lead the Sheep Home?" (cartoon adventure, Farm week 1: the first Clover story)

Theme title "Clover Leads the Flock Home". Slot: Nov 29 2026, 5:30 AM ET. Claimed Nov 27 by the scheduled afternoon adventure build
(https://claude.ai/code/session_014CFVfWGhydZaCrxaKUuTsv; claim commit a068f5f, 3:16 PM ET by the session's clock). Status: **to_upload** (not uploaded;
the 6:31 AM daily run schedules it).
File: `cartoon/za_ep16.mp4`, AV1 4K 3840x2160, 352.2 s (321.8 s own content + the main intro at the beginning and at the end).
Thumbnail: `brand/zoo/thumb_za_ep16.jpg` ("FOLLOW ME!", none of the title's words; little Clover walking in front of big grey Woolly, the barn far ahead).

## Why za_ep16 and new themes
- `upload_guard.py --next adventure` printed no title (all 15 THEMES adventures had a plan entry) and listed za_ep15 as unfinished; za_ep15 had been
  claimed two minutes earlier by another session (commit 24c6b53), so it was left to that session.
- As the note of `--next` says, new titles were written into `docs/cartoon/build_plan.py` first: FIVE new adventure titles in TWO new themes, not
  five whole themes: "Farm week" (Clover the lamb: Clover Leads the Flock Home, Clover and the Woolly Haircut, Clover's Big Jump Over the Puddle) and
  "Night forest week" (Hazel the hedgehog: Hazel's Night-Time Snack Hunt, Hazel and the Crunchy Leaf Bed). Their facts are marked V (ideas only: to be
  read at the source on the build day). No lessons, songs or Shorts were written for the two themes. `plan.html` rebuilt (its count check now 20
  adventures). `upload_guard.py` NAMES: clover / lamb / flock = sheep, hazel = hedgehog (the day rule sees the new friends).

## What was checked (this session, Nov 27)
- Facts read at the source today (Britannica Kids "sheep"; Sheep 101 "Sheep behavior", Susan Schoenian; verbatim quotes in the episode's docstring).
  Said as facts: sheep live together in a flock; sheep eat grass and other plants and like to munch over a wide meadow; sheep like to follow each
  other: when one sheep moves, the rest will follow. NOT said as a fact: that a lamb leads a flock (the sources say an old ram or the dominant sheep
  usually leads: Clover leading is the story). Supper in the barn is called "sweet, dry grass", not hay (no page read today says hay).
- Episode `studio/cartoon/episodes/za_ep16.py` ("beat": True) and art `studio/cartoon/art_za_ep16.py` (new places meadow, meadow_gold, lane,
  farm_gold, barn; big sheep = art2.lamb in other colours with a bell or a daisy; props tuft, dizzy, hay, arrow, sock; kit points for the lamb).
- Plan check: exit 0, 352.2 s (the main intro at 8.4 s and 336.2 s, 30.4 s together), 64 shots, longest gap 4.5 s, 6 places + 3 boards, 18 questions
  (longest stretch without one 43.8 s), every story beat, words 637/637, sync 64/64 cuts on the half-beat, 8/8 songs on a beat, no suspect word.
- No voice on notes: Clover SAYS the rhyme ("Follow, follow, one by one. Home together, day is done!"), the tune is played on instruments in the next
  shot (`~` lines, notes on the chord tones or a whole step from them), and again at the end (SING_END).
- `listen.py --episode za_ep16` before the render: key C major (fit 0.95), no tone outside the key, no clicks, no silences, tempo 95.3 against 96.
  CLASH lines only the bed's E4 over F (47.4, 117.4, 167.4, 227.4, 257.4, 277.4, 317.4 s); none inside the tune shots (263.75-273.75 s,
  325.0-330.0 s). Picture looked at. listen.py measures, it does not hear.
- Stills: one still near the end of every shot in three rounds (`out/za_ep16/look/`; rounds 1 and 2 were not kept, round 3 `r3_*` is committed), the middle of every story shot (`r3mid_*`), and the
  twelve changed shots again after the last fixes (`r4_01.jpg`). A small geometry check (boxes of every actor against both cameras and against each
  other, start and end of walks) was run after each round; it is not committed and is not the look.

## Defects found in the stills (all fixed and seen fixed in a later round)
- Round 1: the three big sheep stood inside each other (scale .7, too close) in every meadow shot: scale .6 and wider apart; the same for the
  walking line and the solution shots.
- Words on legs in every close-up of Clover and Mama; words under the mark at the top left ("THE GREEN MEADOW", "DIZZY!", "DAISY FOLLOWS!");
  words on Milo ("A LITTLE SAD", "LOOK!", "STEP, STEP, STEP!", "FOLLOW, FOLLOW", "HOORAY!"): close-ups now put the face on one side and the words on
  the other, wide words sit at fx .6 or lower than the mark, Milo is moved or hidden.
- Captions on feet on the three picture boards and in the rhyme close-up: the sheep stand higher / the camera sits lower.
- Sheep, Clover or Milo cut by the frame edge (the fact boards, the flock following, the lane, the barn questions, the push-in of close-ups):
  positions and end cameras changed; the "flock follows" shot no longer pans (Bramble walked last and was cut for seconds).
- Clover inside Mama at the farm and at the barn; Clover's head on Daisy's nose in the solution shot; the hay heap over Clover: moved apart.
- Clover's run "round the flock" ran through the sheep: the flock stands further back, Clover runs along the front.
- The idea close-up was framed for an unflipped Clover (she faces left there): camera set by hand; the bulb sat on the far barn and at the frame top.
- "ICE CREAM" (a long answer sign) covered the thinking dots: the answer is "CAKE".
- Count shots: "COUNT!" on the number; the count ran 1.3 s for words said in 0.53 s (CNT3 set from the timing file).
- Thumbnail 1: Clover drawn bigger than the big sheep, Bramble inside Woolly and cut at the edge: redrawn with one big sheep behind a small Clover.

## Render and finished file
- Render 1 (4K, tmux, about 42 min): `--check4k` 3840x2160; `pace_check.py --max 8`: 0 stretches over 8 s (longest 8.0 s; "same shot" 7 stretches
  over 8 s, longest 12.0 s: question, board and tune shots); `watermark.py check`: MARK yes; corner sheet (`look/corner_tl.jpg`) looked at: under the
  mark only sky, tree leaves, board paper, barn planks, the lantern's foot and corners of words and signs. At 1:00 the corner is all blue (an answer
  sign's reveal covers the mark for a moment; the engine does this in every episode). `bookends.py`: intro at both ends.
- Frames of the finished render looked at (`look/fr_01..13.jpg`, 148 frames): middle and end of every shot (the intro shots too), every answer
  reveal 1.1 s and 0.3 s before the cut (12 questions with signs: the check mark is on the right answer before every cut; the two counts end on 3; four copy-me moments),
  the rhyme shot and both tune shots. The render matches the stills.
- `listen.py` on the render: -15.5 LUFS, true peak -1.4 dB, no clipped samples, no clicks, no silences; picture looked at (even level). With the
  speaking voice in the file it read the tempo as 63.9 (the music alone read 95.3): with speech it judges level and silences only. listen.py
  measures, it does not hear.
- AV1 file `cartoon/za_ep16.mp4` (encode about 25 min, 84 MB): 4K, MARK yes, BOOKENDS yes, 352.25 s, listen.py the same (-15.5 LUFS, no clicks, no
  silences). `review.py cartoon/za_ep16.mp4`: PASS, contact sheet looked at. Thumbnail looked at full size and at 168x94 (`look/thumb.jpg`,
  `look/thumb_small.jpg`): two sheep and the words read at the small size.
- `upload_guard.py cartoon/za_ep16.mp4`: OK TO UPLOAD; `--audit`: 0 failures.

## Not checked
- How the voices sound: Clover (af_bella, pitch +4, formant 1.2) and Mama (af_sarah, unshifted) are NEW voices, Milo is af_heart as always. Nobody
  has heard them, nor the two tunes, nor how "Baa!" and "Woolly" are said. listen.py measures, it does not hear. Noelson's ears decide.
- Frames of the AV1 file itself were not looked at one by one (the render's frames were; the AV1 checks are 4K, mark, bookends, review's sheet).
- A 9:16 version: none was built (an adventure has no Short).
- The look of the new characters and places is a first look for the owner: big sheep are the lamb's drawing made bigger in other colours; their
  heads go down only a little when they graze (the lamb rig's neck is short), so "munching" is the jaw moving next to a grass tuft.

## Defects seen in the finished render (small, kept, not re-rendered)
- The known iris-wipe dot (a small blue ring in the last 0.3 s before an iris cut) shows at 8.1 s (sky), 62.2 s (board), 117.8 s, 145.6 s (meadow),
  196.3 s (on Clover's ear), 240.9 s, 280.0 s (lane, beside Daisy), 289.7 s (logged with za_ep12).
- Milo's wing touches the right frame edge in the lane's wide shots when he hops (244 s, 273 s).
- Several end-of-shot frames catch Clover mid-blink (the idle blink).
- The count-alongs are quick: the voice says "One, two, three!" in half a second.

## Engine change (smallest fix, old episodes not touched)
- `studio/zoo3d/wordsync.py`: `ALIAS = {"baa": "bah"}`, used by the ALIGNER only. The bundled dictionary spells "baa" letter by letter
  (B IY EY EY) and refuses a replacement, so every line with "Baa!" had 0 words placed. The voice gets the script's own spelling (Kokoro phonemizes
  "Baa" and "Bah" the same, /bɑː/, checked with `tokenizer.phonemize`); captions keep "Baa!".

## For the next build
- Clover close-ups: `CH` (face left, words at fx .74) and for a flipped Clover a camera set by hand; sheep at .6 need 400 px between feet.
- A character who walks last in a panning shot is cut by the pan: no pan, or start it earlier.
- The next Farm week title is "Clover and the Woolly Haircut" (the goodbye names it). `art_za_ep16` has the farm places and the big sheep.
