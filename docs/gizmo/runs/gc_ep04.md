# gc_ep04 "How Does Your Heart Work? Gizmo Explains" — built and scheduled (Gizmo catch-up run A, Nov 28 1:08 AM to ~5:20 AM ET, session_014CFVfXs8xfsEZKF885Z161)

## Result in one line
A new 2D explainer on the heart (Gizmo's main intro at both ends) and its three Shorts were built, checked and SCHEDULED on Gizmo Explains:
gc_ep04 bCNRbeUIlXg (Nov 29 2:10 PM), gc_ep04_short1 CDFtRYVkI3Y (Nov 30 12:10 PM), gc_ep04_short2 fcRWHxhjUms (Dec 1 12:10 PM), gc_ep04_short3 Q8bjVFBd50w (Dec 2 8:10 AM).

## Files
- `cartoon/gc_ep04.mp4` — AV1 3840x2160, 354.6 s (Gizmo's intro 2 x ~15 s at 12.2 s and 339.1 s; own content ~325 s), 75 shots, 25+ questions with answer signs, three parts 88.4 / 85.6 / 85.9 s.
- `cartoon/gc_ep04_short1.mp4` "How Big Is Your Heart?" 91.8 s, `_short2` "Where Does Your Oxygen Go?" 89.2 s, `_short3` "What Makes the Heartbeat Sound?" 90.5 s: AV1 2160x3840, a whole part + its own hook, own 9:16 cameras, no intro.
- Thumbnails `brand/gizmo/thumb_gc_ep04.jpg` (THUMP THUMP!), `_short1` (FIST SIZE), `_short2` (OUT, BACK!), `_short3` (LUB DUB!); thumb.py word check passed, no mark, looked at (Short 1 re-made: heart and fist were cut at the edges).
- New: `studio/cartoon/art_gc_ep04.py` (props only: friendly heart that squeezes, child's body outline with the heart and the blood's way out and back, fist, lungs with blood picking up oxygen, the heart's four rooms with door flaps, heartbeat line, bed, moon, night window, ball), `studio/cartoon/episodes/gc_ep04.py`. No new place (glab, gbench, gwindow, gpark, gmeadow, ghills + the board).

## Facts (read at the source on Nov 28 2026, quotes at the top of the episode file)
KidsHealth (Nemours): "Your Heart & Circulatory System" for kids (akronchildrens.org/kidshealth/en/kids/heart.html) and "Heart & Circulatory System" for parents (kidshealth.org/en/parents/circulatory-system.html). Two kidshealth.org kids URLs served the parents article; the kids article was read at the Akron Children's copy, verbatim for its first ~40,000 characters.
Taken out (not read verbatim today): where to feel the pulse (neck, wrist), beats per minute. Safety: the only actions are a hand on the chest, a fist, breathing, touching head and toes, marching and hopping in place.

## What was looked at
- Plan check: pass (354.6 s, 659/659 words placed, 71/71 cuts on the half-beat, intro songs 6/6 on a beat, no stretch over 6 s); Short plans 91.9 / 89.2 / 90.5 s, no fails.
- `listen.py --episode gc_ep04` before the render: key C (fit 0.98), no click; CLASH lines only the bed's E over F (known), none inside the intro score. Picture looked at.
- Stills: every shot in 16:9 (round 1) and every Short shot in 9:16 (round 1), then the fixed shots again (rounds 2-4, 16:9 and 9:16).
- Finished files: `--check4k` (4 renders, 4 AV1), `pace_check.py --max 8` 0 stretches on all four (longest 7.1 / 4.8 / 7.8 / 5.8 s; render 1 of the explainer had two, fixed), `watermark.py check --channel gizmo` MARK yes, corner sheets of all four looked at (grid, sky, pots and plants of the lab shelf under the mark, nothing that matters), `bookends.py check --channel gizmo` BOOKENDS yes on the AV1 explainer, frames of every shot's middle and every answer reveal (explainer render 2 and the changed shots of render 3; all three Shorts), `listen.py` on all four renders (no click, no silence, about -16 LUFS, true peak -1.4 dB; pictures looked at; it measures, it does not hear), review.py PASS on all four AV1 files with contact sheets looked at, upload_guard OK TO UPLOAD x4, zlive live = [] on Gizmo's Shorts and Videos lists before each upload.
- Studio: drawer read "Gizmo Explains" and URL channel id UCJaMYOrKCEA54kaOMyYNiKQ before arming each file and before each Schedule; made for kids, custom thumbnail, title and description from the plan; each Studio confirmation read ("will be set to public on ..."; the explainer's said "after the standard definition (SD) finishes processing"). Studio switched back to The Animated Zoo (drawer read). Uploads 4:05-4:12 AM (Shorts) and 5:05 AM (explainer) ET; run B's last upload commit was 4:40 AM.

## Defects found and fixed
1. Stills r1: THUMP, THUMP! cut at the left edge; IN YOUR CHEST!, AGAIN AND AGAIN!, ROUND AND BACK! on the child's head or arm: moved to the left side.
2. Stills r1: the child's head at the top edge (16:9) and words on the head (9:16): body smaller and lower.
3. Stills r1: copy-me words in the lab (SQUEEZE!, FIST UP!, HAND ON CHEST, BREATHE IN!, HEAD, TOES!, CLAP, CLAP!, FASTER?) on Gizmo's head; small pictures cut at the right edge: wider lab camera (1400) and pictures beside the magnifier; in 9:16 those pictures sat on the word: 16:9 only.
4. Stills r1: the heart's doors read as check marks and the room numbers 3 and 4 sat on them: doors redrawn as white flaps that swing shut; numbers inside the rooms.
5. Stills r1: SLEEP TIGHT! on the moon; the ball cut at the frame edge (always working, goodbye): word moved, ball taken out of those shots; run-and-play 9:16 camera moved so Gizmo is whole.
6. Quiz pause 9 (two or four rooms) had nothing big moving: doors swing during the pause.
7. Render 1 pace check: 9.0 s (valves, doors, question 8 on one framing) and 11.2 s (quiz 1 and its answer): own framings and pushes; render 2: 7.1 s.
8. Render 2 frames: YOUR FIST! (quiz 1 answer) cut at the top by the new push-in: word lower; render 3 frames show it whole.
9. Short 2's title was first "Where Does Your Blood Go?": "blood" is on the rulebook's banned list for titles and descriptions; renamed "Where Does Your Oxygen Go?", descriptions written without it.

## Open / not checked
- How Gizmo's voice and the music sound to a person (listen.py measures; it does not hear). Pronunciation of "lub, dub" is Noelson's call.
- review.py: no lesson spec for the word check, no --job for the scene plan (as for gc_ep01-03).
- Studio's copyright / ad-suitability checks were still running at scheduling ("We're still checking your content", acknowledged with "Got it"); the result was not read. The explainer was still processing (row "Pending") when the run ended.
- The engine's iris transition shows as a big circle in frames at an iris cut (as in gc_ep03): not changed.
- The container restarted once mid-render (06:48 UTC); the render was started again from scratch.
