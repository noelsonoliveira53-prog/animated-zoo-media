# zc_ep16 "How Do Sea Turtles Breathe?" - run note (hand-fired 1:17 PM lesson build, catch-up, Nov 27 2026; session in the commits' Claude-Session line)

The owner fired this build by hand at about 3:15 PM to catch up ("work right now on publish videos for tomorrow and all days for the next 4 days").
The same session had just finished zc_ep14 (scheduled 1:17 PM build). Nothing was uploaded; no Studio, no browser, nothing on the PC.

## Why this title
`upload_guard.py --next lesson` (about 5:46 PM ET): unfinished_first listed zc_ep15 ("Is a Polar Bear Really White?"), which another session was
building at that moment (commits from its render at 5:2x PM): left to it. Next free title "How Do Sea Turtles Breathe?" (Ocean week), id zc_ep16,
lesson Nov 29 5:30 PM, Shorts Dec 2 / Dec 3 / Dec 4 7:30 PM. Claimed in commit 2fed329.
Same-day check: za_ep15 (Nov 28) also shows Tula coming up for air; this lesson is on Nov 29.

## What exists
- `studio/cartoon/episodes/zc_ep16.py` ("beat": True, `*intro_shots()` right after the hook and as the last four shots) and new art only in
  `studio/cartoon/art_zc_ep16.py`: a new place `surface` (sky above, water line across the middle) with a see-through water layer drawn in front
  of Tula, so her body is under the water and her head above it; a cut-away turtle with two lungs right under the shell (they fill and empty), air
  bubbles, a slow-heartbeat board (heart + line with long flat gaps + a travelling dot), a nose puff, a rock ledge for the sleeping turtle. Tula is
  the existing rig. Places reused: reef, ocean, kelp (za_ep12/13). No existing character, prop or place changed. No engine change.
- Files: `cartoon/zc_ep16.mp4` (AV1 4K, 358.3 s: 327.8 s own content + the main intro at both ends), `cartoon/zc_ep16_short1.mp4` 89.8 s,
  `_short2.mp4` 87.4 s, `_short3.mp4` 88.3 s (2160x3840 H.264, copied byte for byte from the render, cmp). Thumbnails `brand/zoo/thumb_zc_ep16.jpg`
  (NO GILLS?!: Tula's head out of the water, bubbles under it), `brand/zoo/shorts/thumb_zc_ep16_short1..3.jpg` (LUNGS! / POP UP! / HOURS!).

## Facts (read Nov 27, about 5:50-6:00 PM ET, by the session's page reader; verbatim quotes in the episode file's header)
Used: Smithsonian Ocean "Sea Turtles"; Olive Ridley Project "Can sea turtles breathe underwater?" and "How do sea turtles breathe?"; State of the World's
Sea Turtles "How long can sea turtles hold their breath?"; Florida Museum "Tell me about: sea turtle adaptations"; NOAA Fisheries "10 tremendous turtle
facts" (seagrass only); Scuba Diving "How Do Sea Turtles Breathe?" (David Shiffman) for "no gills" (the only page read that says it).
Not used: NOAA's breathing item (returned as a summary only). No source read said "a quick breath" or "nostrils": not said.
Kid safety: no child is asked to hold their breath; the moves are breathing slowly with a hand on the chest, popping the head up, paddling, tapping
slowly, resting the head.

## Checks before the render
- Plan check (last run): no fails, 358.3 s, own content 327.8 s; parts 86.2 / 84.4 / 84.7 s; 677/677 words placed; all cuts on the half-beat; 6/6 intro
  tunes on a beat; no suspect word; longest stretch 5.08 s. First version was 274 s of own content and one line ("Bye-bye, sky!") the aligner could
  not place: 12 shots added, the line rewritten; then one 6.2 s stretch (Milo paddle pause) fixed with a hop.
- listen.py --episode BEFORE rendering: key C (fit 0.97), no click, no silence, tempo 94.9; CLASH lines only E4 over F2/F4 at the bed's bar changes
  (27.4 ... 337.4 s, the known E-over-F of the lessons' bed; 27.4 is 0.2 s after the first intro, as noted for zc_ep12), none inside a tune. Picture looked at.
- Stills of every shot (end) in 16:9 and in 9:16 for every shot of each Short, two full rounds plus the changed shots: fixed Tula's head cut by the
  frame and the "?" on her shell in 9:16 close-ups (wider 9:16 view), "?" words on her shell, the counting numbers on Milo's crest and on the band in
  9:16, the clock under the caption / beside the turtle's face in 9:16, the seagrass in front of Tula's face, Tula's head at the water line too low.

## Renders and checks on the finished files
- Lesson render 1: pace_check found 4 stretches over 8 s (14.0 s on the three lungs boards, 8.5 s at the part 2 question, the part 2 quick check
  and quiz 2): the boards got different cameras and pushes, the questions pull-outs. Render 2: one left (part 2 opening + question, 8.5 s): Tula now
  swims across with bubbles and the question moved to the seagrass place. Render 3: frames showed the heart on the slow-heart board flying in from
  the top-left corner (a scale tween on a group that carries its own translate): heart wrapped in a plain group (art_zc_ep16.slow_heart). Render 4
  is the file: --check4k 3840x2160, pace 0 stretches over 8 s (longest 7.0 s), MARK yes, BOOKENDS yes (both ends), corner sheet looked at (sky,
  water, boards, the gate post; three solid-blue frames are the iris wipe), frames at the middle and end of every shot and after all 9 answer
  reveals looked at on render 3 (153 frames) and the render-4 frames compared with them (only the heart board differs; that sheet looked at),
  listen.py -15.6 LUFS, true peak -1.4 dB, no clicks, no silences, picture looked at.
- AV1: `cartoon/zc_ep16.mp4` 358.3 s, 85.4 MB, --check4k 3840x2160, MARK yes, BOOKENDS yes; listen.py -15.6 LUFS, true peak -1.4 dB, no clicks, no silences; six frames of the AV1 file looked at (hook, answer, surface, pop, heart board, recap).
- Shorts (one render each; Short 1 was rendered before the heart fix, but the heart board is in part 3 only): each --check4k 2160x3840, MARK yes,
  pace 0 stretches over 8 s (longest 5.2 / 5.8 / 7.0 s), corner sheet looked at, frames at the middle and end of every shot and after every reveal
  looked at, listen.py -15.5 / -15.3 / -15.3 LUFS, true peak -1.4 / -1.4 / -1.5 dB, no clicks, no silences, pictures looked at.
- Thumbnails looked at full size and the main one at 168x94 (first version: Tula too big, the words on her shell; redone).

## Not checked / for the owner's ears and eyes
- listen.py measures, it does not hear: nobody listened. "reptile", "algae", "gills", "seagrass" checked by word alignment only.
- New art the owner has not seen: the top of the sea with the see-through water, the lungs cut-away, the slow heart board, the rock ledge.
- In the 9:16 surface shots Tula sits under the title band's line in a few frames (her shell's top touches the band's second line once); not re-rendered.

## Defects for docs/IMPROVE.md (the daily run folds them in)
- 2026-11-27: A board with one still picture held for three shots in a row (lungs, lungs under the shell, lungs fill) read as 14 s without a visual
  change (pace_check, one extra 38-min render): consecutive boards on the same picture need different cameras (one close, one wide) or a new place.
- 2026-11-27: A scale tween ("PULSE") on a prop group that carries its own transform (translate + scale on the same `<g id>`) throws the group to
  the frame's corner (zc_ep16 render 3, slow-heart board): a part that pulses must be a plain group around the transformed one.
- 2026-11-27: "Bye-bye, sky!" could not be placed by the word aligner (7/7 words): avoid it.
