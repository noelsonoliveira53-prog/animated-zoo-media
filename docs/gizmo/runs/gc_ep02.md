# gc_ep02 "How Do Rockets Fly? Gizmo Explains" — finished (Gizmo daily run, Nov 21 9:45 PM to Nov 22 ~1:30 AM ET, session_014CFVfUmeUNgUPieXvi1pVN)

## Result in one line
The rockets explainer (episode, art, facts, first stills by session_014CFVfX9xTrYXRL7oziQw2A at noon Nov 21; silent since 1:02 PM) got Gizmo's main
intro at both ends, two rounds of fixes, a 4K render and every check. The explainer and its three Shorts are "to_upload" on the slots claimed at noon
(explainer Nov 22 2:10 PM; Shorts Nov 23/24/25 8:10 AM). NOT uploaded: Studio's browser on the PC is signed out of Google (account chooser shows
"Signed out" at 10:05 PM); signing in needs Noelson's password. Noelson was notified.

## Files
- `cartoon/gc_ep02.mp4` — AV1 3840x2160, 345.9 s (own content 315.9 s + Gizmo's intro 2 x ~15 s at 12.2 s and 330.3 s), 76 shots, 24 questions.
- `cartoon/gc_ep02_short1.mp4` (What Pushes a Rocket Up?, 89.2 s), `_short2` (Can a Rocket Fly in Space?, 91.0 s), `_short3` (Why Do Big Rockets Drop Parts?, 87.4 s):
  AV1 2160x3840, a whole part + its own hook, own 9:16 cameras, no intro.
- Thumbnails `brand/gizmo/thumb_gc_ep02.jpg` (BLAST OFF!), `_short1` (WHOOSH!), `_short2` (NO AIR!), `_short3` (BYE-BYE!): thumb.py word check passed, no mark.

## What changed in this session
- Gizmo's main intro: `from intro_gizmo import GZ_INTRO_STAGES, gz_intro_shots`, `**GZ_INTRO_STAGES` in STAGES, `*gz_intro_shots()` after "hook: Gizmo" and as the
  last four shots, `"intro": False` taken out of the EP. intro_gizmo.py and score_gzintro.py not touched. The episode opens on its promise ("How does a big
  rocket fly up, up into the sky?"), Gizmo's name after the hook.
- Fixes (defects for docs/IMPROVE.md, found by this session):
  1. pace_check on the first render: 63.0-74.0 s, 11 s with no visual change (question 2 board; the signs wobble, so they do not count). Fixed: slow push-in
     `cam2=(960, 555, 1390)`. Second render: 0 stretches over 8 s, longest 7.1 s.
  2. The board's down arrow (gas goes down) had its head below the frame in question 2, "rocket goes up" and "every push" (prop at y 880 under a 1500-wide
     board camera): only a cream bar showed. Moved to y 690; frames show the whole arrow.
  3. "...A PUSH BACK!" lay across the rocket body in 16:9 and 9:16: now "...PUSH BACK!" left of the rocket (16:9) and small at the left (9:16).
  4. Short 1 board shots in 9:16: arrow heads under the caption, UP!/DOWN on the arrows: arrows moved up and right, words to the left column.
  5. Ten 9:16 words under Gizmo (HMM..., PRESS!, NO AIR?, A BACKPACK!, STACK!, WAVE!, ...) at 0.72 of the view sat on two-line captions (seen in the
     Short 1 render's frames, mid-shot): now 0.67.
  6. Short 1 question 3: the WATER sign touched the rocket's nose in 9:16: camera lowered (pcam y 360).
  7. Short 1 thumbnail: WHOOSH! touched the nose: moved up.
  8. My own slip: the thumbnail edit put the closing brace inside a comment, so the first Short renders failed on import (caught in the log, fixed, re-rendered).
     The lesson render was not affected (it had loaded the episode before).

## What was looked at
- Plan check passes (345.8 s, own content 315.9 s, 0 stretches over 6 s, 668/668 words, 75/75 cuts on the half-beat, songs 6/6 on a beat, intro at 12.2 and 330.3 s);
  Short plans 89.2 / 91.0 / 87.4 s, no fails.
- `listen.py --episode gc_ep02` before the render: key C (fit 0.98), no click; CLASH lines are only the 3D bed's E over F every ~10 s (known); none inside the
  intro score at either end. Picture looked at.
- Stills: every shot in 16:9 (76) at 640 px, the three Shorts in 9:16 (18/21/20 shots), then the changed shots again after each fix.
- Finished files: `--check4k` (all four render files and the AV1 explainer), `pace_check.py --max 8` 0 stretches on all four renders, `watermark.py check --channel gizmo`
  MARK yes on all four renders and the AV1 explainer, corner sheets of all four looked at (sky, board, pots, stars under the mark), `bookends.py check --channel gizmo`
  BOOKENDS yes on the render and on the AV1 file, frames of every shot's middle and of every answer reveal (lesson: all 10 question/quiz reveals show the right
  sign with its check; Shorts: their reveals), both intros in the frames, `listen.py` on all four renders (no click, no silence, -16 LUFS, true peak -1.4 dB;
  pictures looked at; it measures, it does not hear), review.py PASS on the AV1 explainer and its contact sheet looked at.

## Not checked
- How Gizmo's voice and the music sound to a person (listen.py measures; it does not hear). Pronunciation is Noelson's call.
- review.py says: no lesson spec for the word check, no --job for the scene plan (as for gc_ep01).
- Studio, Gizmo's content list, zlive: not reached (signed out).

## Waits for Noelson
- Sign Studio's browser on the PC back into Google. Until then nothing uploads: gc_ep01 (its Nov 21 6:10 PM slot has passed: it takes the next free 2:10 PM slot
  at upload), gc_ep01_short1 (Nov 22 8:10 AM), gc_ep02 (Nov 22 2:10 PM) and its Shorts. If Nov 22 2:10 PM passes too, the next run moves them to the next free slots.
- gc_ep01 Shorts 2 and 3 are still "in_production" with no file in cartoon/ (the noon session wrote and checked their 9:16 stills; the renders it mentions are not
  in the repo). Not built tonight; the next Gizmo run builds them (they are the "shorts_missing" step).
