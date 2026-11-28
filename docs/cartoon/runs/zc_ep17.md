# zc_ep17 "Can a Turtle Leave Its Shell?" - run note (scheduled 1:47 AM lesson build, Nov 28 2026; session in the commits' Claude-Session line)

Nothing was uploaded; no Studio, no browser, nothing on the PC. The 6:31 AM daily run schedules the four files.

## Why this title
`upload_guard.py --next lesson` (1:55 AM ET): unfinished_first empty; Ocean week "Can a Turtle Leave Its Shell?", id zc_ep17, lesson Nov 30 9:30 AM,
Shorts Dec 5 / Dec 6 / Dec 7 7:30 AM (each on its own day; the guard skips days that carry 'turtle'). Claimed in commit 0748988.
Same friend as zc_ep16 (Nov 29 5:30 PM) one day later; different topic (the shell, not breathing).

## What exists
- `studio/cartoon/episodes/zc_ep17.py` ("beat": True; `*intro_shots()` right after the hook and as the last four shots; the shot before the closing
  intro is Milo saying `intro.SUBSCRIBE_LINE`; the goodbye before it is "Have a happy swim, Tula!", no "Bye-bye"). First zc_ep17+ lesson with the
  like-and-subscribe goodbye.
- New art only in `studio/cartoon/art_zc_ep17.py`: a see-through sea turtle on a board with the backbone along the top of the shell and wide flat
  ribs from it to the rim (-spine, -ribs, -shell, hidden -nerves), a coat on a hanger with a red cross, a door doodled on Tula's shell with a "?"
  (cold open and thumbnail), a grow arrow, a fingernail = scute board, a land turtle whose head slides into its shell, gentle-tap lines. Tula is the
  existing rig; places reused (reef, ocean, kelp, zoo, zoo_eve, paper boards). No existing character, prop or place changed. No engine change.
- Files: `cartoon/zc_ep17.mp4` (AV1 4K, 364.6 s: about 334 s own content + the main intro at both ends), `cartoon/zc_ep17_short1.mp4` 87.8 s,
  `_short2.mp4` 88.9 s, `_short3.mp4` 87.4 s (2160x3840 H.264, copied byte for byte from the render, cmp). Thumbnails `brand/zoo/thumb_zc_ep17.jpg`
  (DOOR?!: Tula with the door doodle), `brand/zoo/shorts/thumb_zc_ep17_short1..3.jpg` (BONES! / LIKE NAILS! / STAYS OUT!).

## Facts (read Nov 28, about 2:05-2:15 AM ET, by the session's page reader; verbatim quotes in the episode file's header)
Used: San Diego Zoo Wildlife Alliance "Turtle and Tortoise"; Ask Dr. Universe (WSU) on turtle shells; PBS Nature "Photo Essay: Turtle Anatomy";
Smithsonian Ocean "Sea Turtles"; Live Science "Turtle Facts"; Olive Ridley Project "Facts about sea turtles"; Spokesman-Review / Ask Dr. Universe
"Why can't sea turtles pull back into their shell?". Smithsonian and Olive Ridley pages were read verbatim only for their first ~40k characters
(the reader summarised the rest); every quote used is from the verbatim part.
Not said: the number of bones (sources differ: 50, 59-61, about 60), "keratin", "pain", the leatherback exception (Tula is a green sea turtle).
Kid safety: copy-me moves are feeling your ribs, touching your back, stretching tall, tapping your fingernails, pulling your head in and out.
The shell is shown as Tula's own body, never as something she is stuck in.

## Checks before the render
- Plan check: no fails, 364.6 s; parts 84.7 / 85.9 / 84.1 s; 720/720 words placed; all 75 cuts on the half-beat; 6/6 intro tunes on a beat; no suspect
  word; longest stretch 5.2 s. First version was 295 s own content (parts 70-73 s): 10 shots added in two rounds.
- "scutes" checked with the phonemizer: skjˈuːts (right).
- listen.py --episode BEFORE rendering: key C (fit 0.98), no click, no silence, tempo 94.8; CLASH lines only E4 over F2 at the bed's bar changes
  (77.4, 197.4, 247.4 s; the known E-over-F of the lessons' bed) and the answer chime C6 over the bed's B4 at 294.5 s (as zc_ep13/15); none inside a
  tune (the only tunes are the two intros). Picture looked at.
- Stills 16:9 of every shot (round 1, 76 stills) and the changed shots (rounds 2-3); 9:16 stills of every shot of each Short (round 1) and the changed
  shots (rounds 2-4). Fixed: coat drawn over the turtle's tail (16:9) and on top of it (9:16), then the caption on the flippers (9:16); ribs invisible
  (redrawn as wide bones from the backbone to the rim); turtle cut by the frame on the backbone and ribs boards (16:9 and 9:16), the grow boards
  (9:16), the no-room board (9:16, also Tula inside the land turtle in 16:9), the nerves board and a close shell camera; Milo cut at the top when the
  camera pushed in (no door, tap); words on Milo's crest (NO DOOR!, SHE FEELS IT!), BONES!/RIBS! cut at the top, STAYS OUT! cut at the left.

## Renders and checks on the finished files (one render each, no re-render needed)
- Lesson: --check4k 3840x2160, pace 0 stretches over 8 s (longest 8.0 s), MARK yes, corner sheet looked at (sky, water, boards, gate post), BOOKENDS yes
  (both ends), frames at the middle and end of every shot (152) looked at, all 9 answer reveals included, listen.py -15.6 LUFS, true peak -1.4 dB, no
  clicks, no silences, picture looked at. AV1 `cartoon/zc_ep17.mp4` 364.6 s, 84.8 MB: --check4k, MARK yes, BOOKENDS yes, listen.py same numbers, six
  frames of the AV1 file looked at, review.py PASS (contact sheet looked at).
- Shorts: each --check4k 2160x3840, MARK yes, pace 0 stretches over 8 s (longest 6.0 / 6.8 / 6.2 s), corner sheet looked at, frames at the middle and end
  of every shot (38 / 38 / 36, every reveal) looked at, listen.py -15.2 / -15.3 / -15.2 LUFS, true peak -1.4 / -1.4 / -1.5 dB, no clicks, no silences,
  pictures looked at, review.py PASS (contact sheets written; not each looked at beyond the frame sheets).
- Thumbnails looked at full size and the lesson's at 168x94 (first version: Tula too small; short 1 head cut; short 3 shell cut: reframed).
- upload_guard: OK TO UPLOAD for all four; --audit 0 failures.

## Not checked / for the owner's ears and eyes
- listen.py measures, it does not hear: nobody listened. "scutes", "fingernails", "backbone" checked by word alignment and phonemes only.
- New art the owner has not seen: the see-through shell with backbone and ribs, the coat, the door doodle, the fingernail = scute board, the land turtle.
- The iris wipe into parts 2 and 3 starts as a small blue/yellow disc on Tula's neck in the last frame of the shot before it (engine behaviour, seen in
  zc_ep16 too); left as it is.
- The corner sheet of Short 2 shows a solid blue tile at "0:00" (the sampler's first pick lands on the iris at about 2.5 s); the first three frames of
  the file were looked at and show the hook picture.

## Defects for docs/IMPROVE.md (the daily run folds them in)
- 2026-11-28: A board prop drawn next to another (coat beside the x-ray turtle) in 16:9 lands ON it in 9:16 when both keep the default 9:16 place
  (960, y): give every prop on a two-prop board its own `p=` place, one above the other, and check the caption line in the 9:16 still.
- 2026-11-28: Inner bones drawn as short arcs under the shell outline read as nothing at board size: inner parts that the line names (ribs) need wide
  strokes that reach the edge of what they belong to.
- 2026-11-28: A close board camera (width 1150-1300) cut the side-view turtle (950 wide at scale 1) on two shots and a narrower pcam2 cut it again in
  9:16: a board camera is at least 1.5x the prop's width, and a pcam2 never narrower than what holds the prop whole.
- 2026-11-28: `review.py` needs the plan's file path (`cartoon/<file>.mp4`); a bare file name gives "not in an upload plan".
