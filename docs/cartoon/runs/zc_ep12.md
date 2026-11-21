# zc_ep12 "Whose Ears Are These? Guess With Milo" - run note (session_014CFVfZ8ooeZ2N6bW87hm8L, scheduled 1:47 AM ET lesson build, Nov 21)

Scheduled, unattended build: the second Guess With Milo episode (2D cartoon lesson, docs/CARTOON_RUN.md "Guess With Milo", "VIRAL PACKAGING",
"MAIN INTRO") and its three Shorts. Nothing was uploaded; no Studio, no browser, nothing on the PC.

## Why this title
`upload_guard.py --next lesson` (1:55 AM ET): unfinished_first empty; first THEMES title "Whose Ears Are These? Guess With Milo" (theme "guess"),
id zc_ep12, lesson Nov 24 9:30 AM, Shorts Nov 29 7:30 PM / Nov 30 11:30 AM / Dec 1 11:30 AM. Claimed in commit db98c9b (only the four new
entries added; the plan files were re-written with the same \u escapes as before, the diff shows additions only).

## Animals: rhino, fennec fox, polar bear (the plan said "rhino, fox, koala (or the three whose ear facts the build day's sources confirm)")
- The koala was replaced by the polar bear: small round ears that keep the warmth in are the opposite of the fennec fox's big ears that let heat
  out (one board compares them), and the Poppy rig exists. The elephant was considered and left out: zc_ep03 "Why Do Elephants Have Such Big
  Ears?" and its Shorts are on the channel.
- The polar bear's fur and fat were NOT used (the queued Arctic lesson "How Do Polar Bears Stay Warm?" is about them).

## What exists
- `studio/cartoon/episodes/zc_ep12.py` ("beat": True, `*intro_shots()` right after the hook and as the last four shots) and new art only in
  `studio/cartoon/art_zc_ep12.py`: new rigs `rhino` (each ear its own part, `-ear` and `-ear2`, so they turn different ways; hair fringes on the
  ears) and `fennec` (two big ears `-ear`, `-ear2`, furry feet); hiding places drawn in front of the actors (tall grass, a sand dune, a snow bank)
  so only the ears show for the guess and the hiding place sinks away on the reveal; sound rings, heat waves, forward / back arrows, a fennec
  face for the boards, a cut through the sand with a beetle under it, the two ears side by side (big fox ear with heat going out, small round
  bear ear with a warm glow), ear-only pieces for the thumbnails. kit.PT/BOX for the new kinds set from the art file; "ears" and "tail" points
  added to the existing bear's PT there (its drawing is unchanged). No existing character, prop or place changed. No engine change.
- Thumbnails: `brand/zoo/thumb_zc_ep12.jpg` (LISTEN!: two big grey ears turned two ways above tall grass, Milo peeking; checked at 168x94),
  `brand/zoo/shorts/thumb_zc_ep12_short1..3.jpg` (LISTEN! / DIG DIG! / COZY!: the ears alone above the grass, the dune, the snow). thumb.py
  accepted the words. First version looked at and redrawn: Milo was hidden behind the grass, the ears small and crossing, the word on an ear,
  and the 9:16 ones showed mostly sand and snow.

## Facts (read Nov 21, about 2:05-2:35 AM ET, by the session's page reader, which quotes the sentences it finds; quotes in the episode file's header)
Read (all loaded): SDZWA Animals and Plants "Rhinoceros" (node/109 and /animals/rhinoceros); SDZWA Library white rhino and black rhino
(characteristics, behavior); SDZWA Library fennec fox (characteristics, behavior); SDZWA Animals and Plants "Fennec fox"; Smithsonian's
National Zoo "Fennec fox"; SDZWA Animals and Plants "Elephant" (read, not used); SDZWA Library polar bear (characteristics); SDZWA "Polar
bear" (nothing on ears); Polar Bears International "Adaptation"; SeaWorld polar bear characteristics.
Said: a rhino can move each ear on its own; one ear can point forward while the other points back; both ears perk straight up when it hears
something interesting; its ears have a little fringe of hair (white rhino sheet); a rhino can't see very well but hears very well; a fennec fox
is a little fox with giant ears (largest ears for its size of any fox, dog or wolf); its ears can be half as long as its body; they listen for
food hiding under the sand ("like a little beetle": both zoo pages list insects); then it digs with all four feet; big ears let extra heat out
and help it stay cool in the hot desert; a polar bear has small, round ears; small ears help keep the warmth in, in the cold Arctic; a short
little tail keeps the warmth in too.
Not said: ear lengths in inches, the oxpecker bird in the rhino's ears, burrow sizes, panting, polar bear fur and fat.

## Checks before the render
- Plan check (`toon.py zc_ep12 --plan`, last run): no fails, 363.9 s with the two main intros (30.2 s), own content 333.7 s; parts 87.5 / 85.3 / 83.8 s
  (Shorts 91.6 s and about 89-88 s with their hooks); 7 places (savanna, dunes, arctic, zoo, zoo_eve, intro_gate, intro_logo) + 3 boards;
  667/667 words placed; 62 cuts, all on the half-beat; 6/6 intro tunes on a beat; no suspect word; longest stretch without a change 5.35 s;
  30 question moments (9 with answer signs, thinking dots and the reveal at wait:2.0). First words at 0.42 s ("Look! Two ears in the grass,
  and they're turning different ways! Who is it?"), Milo's name at about 10 s, the first answer signs at about 40 s in the lesson (after the
  15 s intro) and at about 6 s in Short 1.
- First plan check: parts of 75.9 / 78.4 / 72.5 s (too short for 85-95 s Shorts): five shots added (the ears perk "to listen very closely",
  "point both hands straight up", "a lot of ear for a little fox", counting the fox's ears, counting the bear's ears, shivering) and two pauses
  made longer. One 6.2 s stretch (Milo "dig like a fox" pause): two more hops.
- Repeated-word cues: a script check found 13 cues on words said twice in their line (back. / back!, do?, dig x4, Listen, all!, ears?:3);
  all given their number before the stills; a second pass checked every numbered cue points at the right word.
- listen.py --episode (music without the voice, BEFORE rendering): key C (fit 0.96), no click, no silence, tempo 95.0, nothing outside the key.
  The intro's tune shots (the shared intro.py score) show no clash. CLASH lines: E4 over F2/F4 at the bed's bar changes (47.4, 67.4, 157.4,
  217.4, 257.4, 277.4 s: the known E-over-F of the 3D lessons' bed) and one at 28.63 s for 0.39 s, 0.2 s after the first intro ends (the
  intro score's last E dying out over the bed's F bar as the bed comes back): none inside a tune. Picture looked at. This machine first lacked
  `tinysoundfont` (installed with --no-deps: its pyaudio dependency does not build and is not used) and `pedalboard` (installed).
- Stills of EVERY shot at the START and the END in 16:9 (the 59 shots outside the intro), and in 9:16 for every shot of each Short, then the
  changed shots again after each fix (16:9: 5 rounds counting the partial ones; 9:16: 4). Found and fixed:
  - the rhino's back (its body is higher than its ear bases) showed above the grass and only the top half of each ear: rhino ears drawn 35%
    bigger, the grass made solid up to 80% of its height, cameras closer on the ears;
  - the grass, dune and snow bank ended in the 9:16 views (a strip of ground under them, the dune's edge at the frame side): all three drawn
    600 px deeper, the snow bank and grass wider;
  - the fox's eye and nose peeked over the dune (gave the answer away): the dune moved under the fox's head and made taller;
  - the hiding places sank only 700 px on the reveal and stayed in the bottom of the 9:16 view: 1500 px;
  - the three hiding places on the game board: grass looked like a box with a hard bottom edge, the rhino and bear ears barely showed, the
    fox's tail stuck out of its dune: all moved down out of the frame's bottom and re-sized;
  - "half as long as its body": the bars were under the caption and off the frame: the shot moved to a board with the fox and the bars beside
    the ear and under the feet;
  - heat waves cut by the frame top (stay-cool board, the two-ears board) and over the word OUT!: lower, smaller;
  - words: BACK! on the rhino's body, EACH EAR! touching an ear tip, GIANT EARS! and COOL! on the fennec's face, ROUND! on the bear's ear,
    POLAR BEAR! on the bear's head, Milo's FRONT!/BACK!, PERK!, LISTEN!, DIG, DIG! on his crest: moved (16:9 and 9:16);
  - the captions crossed the rhino's, fox's and bear's faces in the 9:16 close-ups (subject pushed too low) and in two 16:9 counting shots:
    9:16 views wider and the subject higher, the counting cameras wider;
  - three pairs of back-to-back shots with the same framing (two Milo shots, two fox head shots, two bear head shots): different cameras or a
    shot moved between them; 9:16 PERK UP! / SMALL EARS! / WARM! / LISTEN! against the title band: lower;
  - the short-tail shot showed only the bear's body: wider, the tail in the picture's left third.
