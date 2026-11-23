# za_ep14 "Can Poppy Stay Awake to See the Dancing Sky?" (cartoon adventure, Arctic week)

Theme title "Poppy and the Dancing Sky". Slot: Nov 25 2026, 1:30 PM ET. Claimed Nov 23 about 9:00 AM ET by the scheduled morning adventure build
(https://claude.ai/code/session_014CFVfZKcbUYhCEdWzrCGV7). Status: **in_production** (render not started yet at this note).

## Done so far (Nov 23, morning)
- Facts read at the source today about 9:20 AM ET (NASA Space Place, NOAA NESDIS, NOAA NCEI, NOAA SWPC Aurora Tutorial, NASA Science; verbatim
  quotes in the episode's docstring). Said as facts: northern lights are often seen near the North Pole; best seen at night when the sky is dark,
  clouds can hide them; most are green, some pink or purple, they ripple and move like a waving curtain.
- Episode `studio/cartoon/episodes/za_ep14.py` ("beat": True) and art `studio/cartoon/art_za_ep14.py` (four night places from the za_ep10 / art2
  grounds under a night sky with the northern lights in the far layer, two "_lights" variants, the Z's, a globe, three picture cards, colour dots).
- Plan check: exit 0, 376.6 s (346 s own content + the main intro at 7.8 s and 360.6 s), 67 shots, longest gap 4.28 s, 7 places, 16 questions,
  every story beat, words 725/725, sync 66/66 cuts on the half-beat, 8/8 songs on a beat, no suspect word.
- No voice on notes: Poppy SAYS the rhyme ("Green lights dancing, way up high. Take turns, friends, and watch the sky!"), the tune is played on
  instruments in the next shot (`~` lines, notes on the chord tones), and again at the end (SING_END).
- `listen.py --episode za_ep14` before the render: key C major (fit 0.95), no tone outside the key, no clicks, no silences, tempo 95.3 against 96.
  CLASH lines only the bed's E4 over F (7.4, 47.4, 117.4, 187.4 s) and the answer ding's C6 against the bed's B4 (274.4 s); none inside the tune
  shots (288.8-298.8 s, 349.4-354.4 s). Picture looked at. listen.py measures, it does not hear.
- Stills: one still near the end of every shot in six rounds (`out/za_ep14/look/r1..r6`, the last round committed), start and middle stills of
  every story shot (`look/r5mid_*`), and the nest shots again after the last camera fix (`look/r7_nest.jpg`). Defects found and fixed are listed below.

## Defects found in the stills (all fixed and seen fixed in a later round)
- Words above fy .24 left of fx .34 (under the mark) in Poppy's close-ups and on boards: moved right or lower.
- Two questions showed only Milo while asking about Poppy ("Who falls asleep first?", "Sad or happy?"): now Poppy is in the picture.
- Wake-up shots: Poppy's eyes stayed shut after "Wake up" (toon's "sleep" fx at 0.95 s shut the lid again after an early wake cue): the asleep-from-
  frame-1 pattern now puts the sleep blink before the shot.
- The Z's appeared only after the still (cued on the END of "asleep!") and sat behind words and signs: cued on the word, moved over the head.
- The northern lights were faint, behind the mountains and mostly at the top edge: brighter gradient with rays, drawn in front of the far peaks, lower.
- Nest scenes: the cameras showed sky and cut Poppy at the bottom under the words; words moved up, cameras set so everybody is whole.
- Tumble's back cut at the left edge by the END camera (cam2) in several shots; his trunk over Poppy's back when he stood too close: moved and widened.
- Milo under the answer signs in three questions, and flying into the Z's: lowered / moved.
- Globe: the white polar cap stuck out above the globe: drawn inside it.
- The count's number (screen coordinates, not stage) sat on Poppy's face: moved left.
