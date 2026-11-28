# gc_ep03 "Where Does Rain Come From? Gizmo Explains" — built and scheduled (Gizmo daily run, Nov 27 9:45 PM to Nov 28 ~1:20 AM ET, session_014CFVfVoMCFiR6Tndgu9wxQ)

## Result in one line
A new 2D explainer on the water cycle (Gizmo's main intro at both ends) and its three Shorts were built, checked and SCHEDULED on Gizmo Explains:
gc_ep03 5JZ53DqsC-4 (Nov 28 2:10 PM), gc_ep03_short1 ViD1xDjJuuA (Nov 29 8:10 AM), gc_ep03_short2 rs9iB3ElF0E (Nov 30 8:10 AM), gc_ep03_short3 yk3LYHptdk0 (Dec 1 8:10 AM).

## Files
- `cartoon/gc_ep03.mp4` — AV1 3840x2160, 349.6 s (own content ~319 s + Gizmo's intro 2 x ~15 s at 11.9 s and 334.1 s), 74 shots, 26 questions (14 with answer signs).
- `cartoon/gc_ep03_short1.mp4` "Where Does a Puddle Go?" 90.9 s, `_short2` "How Is a Cloud Made?" 92.3 s, `_short3` "Why Does Rain Fall Down?" 87.7 s: AV1 2160x3840, a whole part + its own hook, own 9:16 cameras, no intro.
- Thumbnails `brand/gizmo/thumb_gc_ep03.jpg` (DRIP DROP!), `_short1` (POOF!), `_short2` (TINY DROPS), `_short3` (PLOP!); thumb.py word check passed, no mark.
- New: `studio/cartoon/art_gc_ep03.py` (places gpark, ghills; props puddle, vapor dots, cloud with grey/rain/snow, speck of dust, dots-to-cloud, joining drops, winter window, snowflake, flow arrows, water-cycle circle, sea, heat lines), `studio/cartoon/episodes/gc_ep03.py`.

## Facts (read at the source on Nov 27 2026, quotes at the top of the episode file)
USGS Water Science School: "Interactive Water Cycle Diagram for Kids (Beginner)", "The Water Cycle for Kids: Condensation", "Follow a Drip Through the Water Cycle".
The first page reader call was refused (permission not answered, unattended); the URLs from a web search were read in a second call. Taken out (not read today): raindrop shapes, "most water ends up in the oceans".

## What was looked at
- Plan check: pass (349.6 s, 649/649 words placed, 73/73 cuts on the half-beat, intro songs 6/6 on a beat, no stretch over 6 s); parts 86.9 / 88.1 / 83.8 s; Short plans 90.9 / 92.3 / 87.7 s, no fails.
- `listen.py --episode gc_ep03` before the render: key C (fit 0.97), no click; CLASH lines only the bed's E over F and the answer ding's C6 over the bed's B (both known), none inside the intro score. Picture looked at.
- Stills: every shot in 16:9 twice (round 1 and after the fixes), every Short shot in 9:16 at its end and again at its middle after the fixes.
- Finished files: `--check4k` (4 renders, 4 AV1), `pace_check.py --max 8` 0 stretches on all four (longest 7.5 / 5.2 / 8.0 / 8.0 s), `watermark.py check --channel gizmo` MARK yes (renders and AV1), corner sheets of all four looked at (sky, grid, pots under the mark), `bookends.py check --channel gizmo` BOOKENDS yes (render and AV1),
  frames of every shot's middle and every answer reveal (lesson 14 reveals, Shorts theirs: right sign with its check), `listen.py` on all four renders (no click, no silence, -16 LUFS, true peak -1.4 dB; pictures looked at; it measures, it does not hear),
  review.py PASS on all four AV1 files, contact sheets looked at, upload_guard OK TO UPLOAD x4, zlive live = [] on Gizmo's Videos and Shorts lists before each upload.
- Studio: drawer read "Gizmo Explains" and URL channel id UCJaMYOrKCEA54kaOMyYNiKQ before arming each file and before each Schedule; made for kids, custom thumbnail, title and description from the plan; each Studio confirmation read ("will be set to public on ..."); the lists afterwards show the four rows "Scheduled". Studio switched back to The Animated Zoo (drawer read).

## Defects found and fixed (stills round 1)
1. Board answer signs on the sun (questions 1 and 3): sun moved down and smaller.
2. The puddle under the caption in the park close-ups (16:9 and 9:16): puddle higher, camera wider.
3. The tiny drops drew a spiral, not a cloud: dots now fill the cloud's shape.
4. The winter window prop covered Gizmo: the window shots are without Gizmo.
5. Up and down arrows drawn on top of each other: two arrows side by side.
6. Joining drops too small; Q8 board was empty (its arrows hidden): Q8 now on the hills.
7. CONDENSATION, TINY DROPS, COLD AIR! on the caption (fy .84): moved to the top.
8. PITTER, PATTER! cut at the right edge (16:9 and 9:16): moved left.
9. 9:16: board props (speck, dots, drops, snowflake, water-cycle circle, arrows, magnifier) under the caption or out of frame: placed between the signs and the caption (0.45-0.70 of the view).
10. Quiz 3: the HEAVY sign touched the grey cloud: cloud lower in that shot.
11. One spoken line could not be placed by the aligner ("No! Water vapor is invisible. We drew it with little dots, ..."): reworded to "Water vapor is invisible! We drew it as little dots, so you can see it." (15/15).

## Open / not checked
- How Gizmo's voice and the music sound to a person (listen.py measures; it does not hear). Pronunciation is Noelson's call.
- review.py: no lesson spec for the word check, no --job for the scene plan (as for gc_ep01/02).
- Studio's copyright / ad-suitability checks were still running at scheduling ("We're still checking your content", acknowledged with "Got it"); the result was not read.
- Frames show an engine "iris" transition as a small dot at the frame's centre in the last 0.3 s before an iris cut, and as a big circle in the Shorts' frames at an iris cut: the engine's transition, not changed.
- The spin action draws Gizmo as a thin sliver in mid-turn (scaleX through 0): left as a turn.
- My slip: `git pull --rebase` ran once while the AV1 encode of Short 2 was writing `cartoon/gc_ep03_short2.mp4` (against the rule). The pull did not touch that untracked file; the finished file decodes without an error, is 2160x3840 and 92.3 s, MARK yes, review PASS.
