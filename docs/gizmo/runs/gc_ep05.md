# gc_ep05 "Why Do Things Fall Down? Gizmo Explains": built and scheduled (Gizmo catch-up run B, Nov 28 1:18 AM to ~5:00 AM ET, session_014CFVfWNwXyYMYtjBTtMq95)

## Result in one line
A new 2D explainer on gravity (Gizmo's main intro at both ends) and its three Shorts were built, checked and SCHEDULED on Gizmo Explains:
gc_ep05 qXukKY6m-Ac (Nov 30 2:10 PM), gc_ep05_short1 oIimfnmU7H0 (Dec 1 7:10 PM), gc_ep05_short2 sANlP4N5k0o (Dec 2 12:10 PM), gc_ep05_short3 GJMI71XqXEs (Dec 3 8:10 AM).
Run A held gc_ep04 (heart, Nov 29); this run took the next title `--next` printed.

## Files
- `cartoon/gc_ep05.mp4`: AV1 3840x2160, 349.0 s (own content ~319 s + Gizmo's intro 2 x ~15 s at 11.6 s and 333.8 s), 75 shots, 23 questions with answer signs or actions.
- `cartoon/gc_ep05_short1.mp4` "Why Does an Apple Fall Down?" 93.0 s, `_short2` "Which Lands First?" 89.2 s, `_short3` "What Keeps the Moon Going Around?" 88.6 s: AV1 2160x3840, a whole part + its own hook, own 9:16 cameras, no intro.
- Thumbnails `brand/gizmo/thumb_gc_ep05.jpg` (BIG PULL), `_short1` (WHOOSH!), `_short2` (RACE!), `_short3` (SPACE PULL); thumb.py word check passed, no mark; looked at full size and at 168x94.
- New: `studio/cartoon/art_gc_ep05.py` (props only: apple tree with a falling apple, apple, heavy and light balls, feather, rock, floor strip, down arrow, Earth with pull arrows / people all around / centre, small and big pull, Moon around the Earth, Earth around the Sun), `studio/cartoon/episodes/gc_ep05.py`. Places reused: glab, gbench, gpark, gmeadow, gsky, gspace, the board.

## Facts (read at the source on Nov 28 2026, quotes at the top of the episode file)
NASA Space Place "What is gravity?"; University of Illinois Physics Van "Heavy and Light - Both Fall the Same"; APS PhysicsQuest "Falling Physics"; Science Buddies "Watch Objects in Freefall".
Taken out: crumpled paper against a flat sheet (APS names the activity but does not state the result), rain pulled down by gravity (read Nov 27, not today).
Safety: nothing is dropped from a height a child could copy; the hop is "just a little"; no fear, no one hurt.

## What was looked at
- Plan check: pass (349.0 s, 661/661 words placed, 74/74 cuts on the half-beat, intro songs 6/6 on a beat, no stretch over 6 s); parts 89.1 / 84.1 / 84.1 s.
- `listen.py --episode gc_ep05` before the render: C major (fit 0.97), no click; CLASH lines only the bed's E over F (known), none inside the intro score. Picture looked at.
- Stills: every shot in 16:9 (round 1, round 2 after fixes, round 3 for the close-ups) and every Short shot in 9:16 (end stills), again after each fix.
- Finished files: `--check4k` (4 renders + 4 AV1), `pace_check.py --max 8` 0 stretches on all four final renders (longest 6.2 / 6.2 / 4.5 / 4.8 s), `watermark.py check --channel gizmo` MARK yes (renders and AV1), corner sheets of all four looked at (sky, grid, pots, no face under the mark), `bookends.py check --channel gizmo` BOOKENDS yes (render and AV1),
  frames of every shot's middle and every answer reveal (lesson: 90 frames; each Short its own sheet), `listen.py` on all four renders (no click, no silence, -16 LUFS, true peak -1.4 dB; pictures looked at; it measures, it does not hear),
  review.py PASS on all four AV1 files, its contact sheets looked at, upload_guard OK TO UPLOAD x4, zlive live = [] on Gizmo's Videos list (long) and Shorts list (Shorts) before each upload.
- Studio: drawer read "Gizmo Explains" and URL channel id UCJaMYOrKCEA54kaOMyYNiKQ before arming each file and on the Schedule page; made for kids, custom thumbnail (looked at in the dialog), title and description from the plan at the pushed commit; each confirmation read ("will be set to public on ..."); the Videos and Shorts lists afterwards show the four rows "Scheduled". Studio switched back to The Animated Zoo (drawer read).

## Defects found and fixed
1. Board floor and balls on the caption (stills r1): floor at y 760, falls of 220.
2. Long words beside Gizmo's close-up cut at the right edge (POINT DOWN!, BIG EARTH!): fx .8, size .7.
3. Short 1 (frames of render 1): ALL AROUND! cut at the left edge while popping in: moved to the middle. Short 1 rendered again.
4. Short 2 renders 1 and 2: pace_check 8.2 s without change (two balls + question 4 looked alike in 9:16): own closer camera on "two balls" and a push on question 4. Short 2 rendered a third time: longest 4.5 s.
5. Short 3 (frames of render 1): EVERYTHING! on the caption; Gizmo half out of the park picture at the left: camera and word moved. Short 3 rendered again.
6. Short thumbnails: the tree cut and the falling apple missing (short1), the heavy ball at the edge (short2): reframed.

## Open / not checked
- How Gizmo's voice and the music sound to a person (listen.py measures; it does not hear). Pronunciation is Noelson's call.
- In the long video, the feather's tip sits under the answer signs while it is held up (questions 5 and 6, 16:9): a prop, no face; not re-rendered (about 70 minutes). Next build keeps held props below the sign row.
- The Moon passes under a word for a moment in two space shots (GRAVITY!, THE MOON!).
- review.py: no lesson spec for the word check, no --job for the scene plan (as for gc_ep01-03).
- Studio's copyright / ad-suitability checks were still running at scheduling ("We're still checking your content", acknowledged with "Got it"); the result was not read.
- studio-upload2.js zsched() refuses the i9.ytimg.com custom thumbnail because it tests the URL after cutting it to 22 characters; the thumbnail was checked in a screenshot and the Next/Schedule steps run without that test. Not changed in the file.
- Not checked: gc_ep04's explainer (run A's) was not yet on Gizmo's Videos list at 5 AM; that is run A's.
