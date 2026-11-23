# za_ep14 "Can Poppy Stay Awake to See the Dancing Sky?" (cartoon adventure, Arctic week)

Theme title "Poppy and the Dancing Sky". Slot: Nov 25 2026, 1:30 PM ET. Claimed Nov 23 about 9:00 AM ET by the scheduled morning adventure build
(https://claude.ai/code/session_014CFVfZKcbUYhCEdWzrCGV7). Status: **to_upload** (not uploaded; the 6:31 AM daily run schedules it).
File: `cartoon/za_ep14.mp4`, AV1 4K 3840x2160, 376.6 s (346 s own content + the main intro at the beginning and at the end), 88 MB.
Thumbnail: `brand/zoo/thumb_za_ep14.jpg` ("WAKE UP!", none of the title's words; Poppy asleep under the green lights, the Z's).

## What was checked (this session, Nov 23)
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

## Render and finished file
- Render 1 (4K, tmux, 53 min): `--check4k` 3840x2160; `pace_check.py --max 8`: 0 stretches over 8 s (longest 6.5 s; "same shot" 7 stretches over
  8 s, longest 15.5 s: question, board and tune shots); `watermark.py check`: MARK yes; corner sheet (`look/corner_tl.jpg`) looked at: only sky,
  the lights, board paper, the moon's edge and the tops of signs and words under the mark at every 5 s step, nothing that matters; `bookends.py`:
  intro at both ends.
- Frames of the finished render looked at (`look/fr_render1_01..12.jpg`, 142 frames): middle and end of every story shot, middle of every intro
  shot, every answer reveal 1.1 s and 0.3 s before the cut (16 questions and the count): the check mark is on the right answer before every cut;
  the rhyme shot and both tune shots. The render matches the stills (compared at 257-259 s).
- `listen.py` on the render: -15.5 LUFS, true peak -1.4 dB, no clipped samples, no clicks, no silences, tempo 95.7; picture looked at (even level).
  listen.py measures, it does not hear.
- AV1 file: 4K, MARK yes, BOOKENDS yes, 376.6 s, listen.py the same (-15.5 LUFS, no clicks, no silences). `review.py cartoon/za_ep14.mp4`: PASS,
  contact sheet looked at. Thumbnail looked at full size and at 168x94 (`look/thumb.jpg`, `look/thumb_small.jpg`): one sleeping cub, big words.
- `upload_guard.py cartoon/za_ep14.mp4`: OK TO UPLOAD (24-hour count by the commit log: 0 of 20).

## Not checked
- How the voices sound (Milo af_heart, Poppy af_jessica pitch +4, Tumble am_puck pitch +5, as in za_ep10), pronunciation, and how pleasant the two
  tunes are: nobody has heard them. listen.py measures, it does not hear.
- Frames of the AV1 file itself were not looked at one by one (the render's frames were; the AV1 checks are 4K, mark, bookends, listen, review's
  contact sheet).
- The northern-lights art is new: how real it looks to a child is the owner's call (green curtains with rays and a pink edge, swaying).

## Defects seen in the finished render (small, kept, not re-rendered)
- The known iris-wipe dot (yellow and blue, last 0.3 s before an iris cut) shows on Poppy's head at 7.5 s, by her mouth at 108.8 s and on the snow
  at 305.3 s (logged with za_ep12).
- "So beautiful!" (256.6-259.4 s): the caption sits on Poppy's front paws and the nest's rim for the last second (the end camera, cam2, frames her low).
- The northern lights look teal more than bright green where the gradient fades into the dark sky (both in the film and the thumbnail).
- Several end-of-shot frames catch Tumble or Milo mid-blink (the idle blink); not a defect of the drawing.
- Story note: the premise's "a song" became "a bouncy dance" (owner's rule: no voice on notes).

## For the next build
- toon's `"sleep"` fx shuts the lid at its own time and again 0.9 s before: a wake cue earlier in the line than the sleep cue is undone. For a
  character asleep from frame 1 put the sleep cue at 0.3 s plus a lid "to" at 0.0 (za_ep14 `ASLEEP`).
- `count`'s x/y are SCREEN pixels, not stage coordinates.
- Stills show the END camera (cam2): a character whole in the start camera can be cut by cam2; check cam2's left edge against the character's box.
