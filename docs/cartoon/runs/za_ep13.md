# za_ep13 "Can Little Crab Find a Shell That Fits?" (cartoon adventure, Ocean week)

Slot: Nov 22 2026, 3:30 PM ET. Status: **to_upload** (not uploaded; the 6:31 AM daily run schedules it).
File: `cartoon/za_ep13.mp4`, AV1 4K 3840x2160, 339.7 s (309.7 s own content + the main intro at the beginning and at the end), 77 MB.
Thumbnail: `brand/zoo/thumb_za_ep13.jpg` ("TOO SMALL!", none of the title's words).

## Who did what
- Afternoon adventure build (session_014CFVfXscEKDwdXMj83y6My, Nov 21 3:16 PM claim): theme renamed to a question title, episode
  `studio/cartoon/episodes/za_ep13.py` and art `studio/cartoon/art_za_ep13.py` (Little Crab the hermit crab, his shells, the snail, six places),
  facts read at the source about 3:30 PM (Seattle Aquarium, Britannica, Discover Wildlife; verbatim quotes in the episode's docstring), plan check
  passing, `listen.py --episode` with no click, stills in four rounds (`look/r1_*` to `look/r4_*`). It pushed at 3:37 PM and nothing after; it wrote
  no run note.
- Evening adventure build (session_014CFVfYkcaUYhCEdWzrCGV7, Nov 21 7:35 PM): took it over as "unfinished_first" (silent for 4 hours), checked
  again and finished it. Everything below is this session's own check.

## What was checked (this session)
- Plan check `toon.py za_ep13 --plan`: exit 0, 339.7 s, 66 shots, longest gap 4.4 s, places shore, shellbed, rocks, kelp, deep, shore_eve (+ intro),
  13 questions, all story beats, main intro at 5.9 s and 324.1 s, words placed 696/696, sync: 65/65 cuts on the half-beat, 8/8 songs on a beat,
  no suspect word.
- `listen.py --episode za_ep13` before the render (music without the speaking voice): key C major (fit 0.94), no tone outside the key, no clicks,
  no silences, tempo 95.3 against 96. CLASH lines: only the bed's known E4-over-F2 (47.4, 117.4, 127.4, 147.4, 237.4, 257.4, 297.4, 307.4 s) and the
  answer ding's C6 against the bed's B4 (54.3, 93.6, 164.4 s, 0.26 s each; known since za_ep09). None inside the tune shots (242.5-252.5 s and
  313.1-318.1 s). Picture looked at (`look/listen_ep.png`): the two tunes are where they should be.
- Stills, 16:9: one still near the end of EVERY shot (66, `look/r5_1..8.jpg`) and start + middle stills of the 12 moving shots (walk-ins, swims,
  the dive, the count, the climb into the big shell, the slip into the golden shell, the tiny crab, the hook, both tune shots: `look/r5_mid_*`),
  all looked at. Nothing needed fixing. (No 9:16 stills: an adventure has no Shorts.)
- Render 1 (4K, tmux, 38 min): `--check4k` 3840x2160; `pace_check.py --max 8`: 0 stretches over 8 s (longest 6.8 s; "same shot" 7 stretches over
  8 s, longest 14.0 s: question, board and tune shots); `watermark.py check`: MARK yes; corner sheet (`look/corner_tl.jpg`) looked at: only sky, water,
  kelp, paper or the tops of signs and words under the mark at every 5 s step, nothing that matters under it; `bookends.py`: intro at both ends.
- Frames of the finished render, looked at (`look/fr_render1_01..10.jpg`, 139 frames): middle and end of every story shot, middle of every intro
  shot, and every answer reveal 1.1 s and 0.3 s before the cut (13 questions): every check mark is on the right answer before the cut; the rhyme
  shot and both tune shots.
- AV1 file: 4K, MARK yes, BOOKENDS yes. `listen.py` on the file: -15.5 LUFS, true peak -1.4 dB, no clipped samples, no clicks, no silences;
  picture looked at (`look/listen_file.png`, even level). listen.py measures, it does not hear.
- Thumbnail: first version had "TOO SMALL!" over the tip of the blue shell; words moved up 50 px (THUMBS in the episode file), rendered again and
  looked at full size and at 168x94 (`look/thumb.jpg`): one crab, big words, readable small.
- `review.py cartoon/za_ep13.mp4`: PASS (contact sheet looked at). `upload_guard.py cartoon/za_ep13.mp4`: OK TO UPLOAD.

## Not checked
- How the voices sound (Milo, Tula and Little Crab's new voice: af_nova, pitch +5, formant 1.22), pronunciation, and how pleasant the tunes are:
  nobody has heard them. listen.py measures, it does not hear.
- The facts were read by the afternoon session today (Nov 21, about 3:30 PM, quotes in the docstring); this session did not read the pages again.
- Frames of the AV1 file itself were not looked at one by one (the render's frames were; the AV1 checks are 4K, mark, bookends, listen, review's
  contact sheet).
- The upload guard's 24-hour count read the commit log of a shallow clone (10 of 20).

## Defects seen (small, kept, not re-rendered)
- Background starfish on the sand sit under the caption in some shore shots (e.g. 224 s "It fits just right!", 1-3 s in the hook) and are cut by
  the bottom edge: decoration, the caption stays readable. Next ocean episode: keep the shore's sand props out of the caption band.
- The known iris-wipe dot (yellow and blue, last 0.3 s before an iris cut) shows on Little Crab's eye at 5.6 s and on Milo at 323.8 s (logged
  with za_ep12).
- The snail comes out on the far side of its shell, not from the opening (138 s): reads as a snail beside its shell; the line "Two little eyes peek
  out" still matches.
- Nov 22 carries za_ep12 (Tula's race, 1:30 PM) and this episode (3:30 PM), where Tula is Little Crab's helper: the guard passes it (this story's
  animal is the hermit crab), but it is two ocean stories with Tula on one day.

## Disk (for the next build on a fresh machine)
The session started with 100 MB free: `git sparse-checkout set --no-cone '/*' '!/truck/' '!/moon/' '!/bloop/' '!/gizmo/' '!/fruity/' '!/space/'
'!/wild/' '!/shorts3d/' '!/*.mp4'` and removing ~/.cache/uv and ~/.cache/pip freed about 9 GB (the render and encode need about 0.4 GB).
