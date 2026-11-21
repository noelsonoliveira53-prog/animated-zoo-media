# gc_ep01 — Gizmo Explains cartoon TEST: "How Does a Seed Grow Into a Plant?" (Nov 19 2026)

Session: session_014CFVfWXNYNsprEv7qN3bvz (scheduled one-off test build). Noelson, Nov 19 12:37 AM: "create a cartoon version of that and let's test it".
Status: **hold_review** in `studio/upload_plan_gizmo_v3.json` (lesson + Short 1). NOT uploaded; a new format is uploaded only after Noelson has watched one full video and said yes.
Nothing was done in a browser, in Studio or on Noelson's PC.

## What was made
- `cartoon/gc_ep01.mp4` — 4K 3840x2160 AV1, 309.8 s (5:10), 69 shots, 6 places + a blueprint picture board; parts 83.8 / 84.4 / 84.1 s; 11 questions with answer signs and thinking time (8 in the lesson, 3 in the quiz).
- `cartoon/gc_ep01_short1.mp4` — 4K 2160x3840 AV1, 87.3 s: part 1 (what is inside a seed) + its own hook, every shot framed again for 9:16, title band "WHAT IS / INSIDE?". Shorts 2 and 3 are not built (test).
- Thumbnails `brand/gizmo/thumb_gc_ep01.jpg` ("ROOT FIRST!") and `thumb_gc_ep01_short1.jpg` ("BABY PLANT!"): 2 words each, none of the titles' words (thumb.py check), no watermark.
- Topic: the third of docs/GIZMO_RUN.md "Topics". Rockets and rain (the first two) were left to tonight's two 3D explainers; neither had a plan entry when this build claimed seed (commit 0877f24).

## New files / engine changes
- `studio/cartoon/art_gizmo.py`: Gizmo as a toon.py rig from `gizmo/gizmo_flat.svg.part` (screen-face smile with a talking mouth on the voice, blinking screen eyes, arms -al/-ar, hover bob, antenna bulb -glow), places glab (lab), gbench (work bench), gwindow (sunny lab window), gsoil (cutaway under the ground), ggarden (garden), gmeadow (flower meadow), paper_gz (blueprint board), all in #1d3a8a–#3561d9 with #5ff3ff accents; props (seed, seed cut open, growth stages, drop, air, warm sun, pot, watering can, sunflower, magnifier, leaf kitchen, life-cycle circle).
- `studio/cartoon/episodes/gc_ep01.py` (facts and their sources at the top).
- `toon.py`, two additions that a Zoo episode never triggers: `EP["wm"]` (another channel's watermark folder, laid at its own width) and a rig key `"hover"` (a slow bob). No Zoo episode sets either key, so Zoo renders are unchanged (not re-rendered to prove it; the change is keyed).
- Watermark: `brand/gizmo/watermark.png` / `watermark_short.png` from the real channel picture (built by the 3D Gizmo session, commit fb3b175; checked with `watermark.py check --channel gizmo`). My first drawn avatar was removed.
- Voice: Gizmo speaks with `am_michael` (Kokoro), the voice the 3D Gizmo videos use for spoken lines; Milo's is `af_heart`. No sung or hummed voice; this lesson has no tune at all (only the 3D lessons' music bed, lowered under the voice).

## Facts (read at the source on Nov 19, quotes in the episode file)
Science News Explores (how a seed grows), Australian Academy of Science Curious (germination), Britannica (germination), US Botanic Garden (flower to seed K-2).
Taken out: "a seed needs sunlight to sprout" (Science News Explores says it, the Academy says most seeds do not need light: the video says most seeds start in the dark), "the seed swells".
Our pictures, said as pictures: seed coat "like a little jacket", food "like a packed lunch", a leaf "like a little kitchen".

## What was looked at
- Plan check: passes (309.8 s, 0 stretches over 6 s, 6 places, 661/661 words placed, 68/68 cuts on the half-beat, no suspect word). Short 1 plan: 87.3 s, 192/192 words.
- `listen.py --episode gc_ep01` before the render: no click; the only CLASH lines are the 3D bed's own E over F every 10 s (logged before) and one answer ding over the G bar at 254.3 s (logged OPEN before); no tune shot exists. Picture looked at.
- Stills: three rounds of 16:9 stills of every shot, start AND end (plus mid-move times for Gizmo's arm poses), one round of 9:16 stills of every Short shot (start and end), looked at after each round of fixes.
- Finished files: `--check4k` (3840x2160, 2160x3840), `pace_check.py --max 8` (0 stretches over 8 s in both; longest 7.0 s / 6.8 s), `watermark.py check --channel gizmo` MARK yes on the render and on both AV1 files, corner sheets of both looked at (nothing under the mark: pots, sky, sun), frames of every shot's middle and of all 11 answer reveals in the lesson and all 3 in the Short (the right sign with its check mark; reveals stay 1.1–1.4 s before the cut), `listen.py` on both files (no click, no silence, -16 LUFS, true peak -1.4 dB; picture looked at), review.py PASS on both AV1 files (with the "NOT APPROVED YET" note), contact sheets looked at.

## Defects found and fixed before the render (for docs/IMPROVE.md, fold in at the next daily run)
- Gizmo's arms are drawn behind his head and body: a hand raised past about -90 degrees disappears (first "wave" and "reach up" stills showed nothing). Arm poses now stay at -50..-85 degrees.
- A camera on Gizmo's "body" point cut his antenna; cameras on him use the whole robot ("all").
- Under the ground, Gizmo hovered in the watermark corner and under the answer signs: he is now right of the corner, hidden in the question shots.
- A close bench camera showed a sliver of his hand at the frame edge; a prop rotated with svgOrigin on its translate wrapper flew across the picture (the can): rotate the prop's own group.
- 9:16 words at y 0.26 of the view sat on the title band's second line: the episode now keeps every 9:16 word at or below 0.35.
- Pale cream root on the cream food was hard to see: outlined.

## Not checked / open
- How Gizmo's voice and the music sound to a person: listen.py measures, it does not hear. Pronunciation and warmth are Noelson's call.
- The "same shot" figure of pace_check is high in the Short (the open-seed board holds one framing for 26 s while signs, pulses and words change): it passes the 8 s gate, but the board could use more framings if the format is approved.
- Zoo episodes were not re-rendered after the toon.py additions (keyed, see above).
- Shorts 2 and 3 are not built.
