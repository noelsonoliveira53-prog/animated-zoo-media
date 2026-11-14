# Daily run: The Animated Zoo (the scheduled task follows this file step by step)

Channel: The Animated Zoo (UC1YuY8nqnViTtm85qxE_M1w, Milo the bluebird, ages 2-6). ONLY THE ANIMATED ZOO IS ACTIVE
(Noelson, Nov 13, 2026). Tiny Truck Town, Bloop's Color Lab, Fruity Friends, Moonbeam Bedtime and Gizmo Explains are PAUSED:
do not check, render for, or upload to them; their plan entries stay "paused_channel" until Noelson says otherwise.

Read first: PLAYBOOK.md (incl. all run notes at the end: current PC queue, what is cancelled), docs/STRATEGY_3D.md,
studio/zoo3d/DAILY_3D.md, docs/GOOGLE_VIDS.md, studio/vids/RUNBOOK.md, docs/IMPROVE.md, docs/quality_baseline/README.md.
Load the `youtube-network-channels` skill (the channel rulebook) at the start of every run and apply it to everything
written, rendered, titled and uploaded.

## Standing rules from Noelson
1. VARIETY (Nov 13): no two episodes may look the same, even when YouTube Studio suggests repeating a topic. Topics and
   title patterns may repeat; pictures, places and casts may not. New jobs use set "zooworld"; routes come from
   `python3 studio/zoo3d/variety.py suggest`; new songs/lessons get a fresh cast (17 animals in chars/animal.py);
   `variety.py check` must say OK, then `variety.py record`, and the ledger is committed. Applies to Vids episodes and Shorts too.
2. MORE SCENE CHANGES (Nov 13): once a song's timing file exists run `python3 studio/zoo3d/routes.py jobs/<id>.json`
   (about 12 scenes per song: own place, formation, only the animals that part is about, closer camera, camera move).
   Lessons get their scenes from lesson.py (one scene per segment). Never send a Zoo job to the PC without a scene plan.
3. QUALITY BAR (Nov 14): docs/quality_baseline/ holds the frames Noelson approved as the MINIMUM. Every episode must look at
   least that good and improve on the last one.
4. REVIEW AND IMPROVE EVERY TIME (Nov 14), using the youtube-network-channels skill:
   - Before writing any new song or lesson: `python3 studio/zoo3d/review.py --brief` and apply the latest notes; list them in
     the spec's "improves" field.
   - Before every upload: `python3 studio/zoo3d/review.py <file> --job studio/zoo3d/jobs/<job>.json --note "<one concrete
     thing the next episode will do better>"`. It checks the rulebook (KID-01..04, META-01..03, banned words, distress words,
     calls to action, 4K, size, length, scene plan, variety) and makes a contact sheet. LOOK at the sheet next to the baseline.
     Upload only on PASS and only if it meets the quality bar; otherwise fix (retitle, re-cut, re-render) or hold, and say so.
     "check:" lines are read and judged by you against the rulebook (a flagged word in a harmless sentence is fine).
   - After the views check: add one number-backed note with `review.py --improve "..." --why "..."`.
5. TEACHING FIRST (Noelson, Nov 14 noon; replaces the "song one day, lesson the next" rule):
   - Direction: "production needs to shift to videos teaching kids instead of music only": ONE music video a day and FOUR
     teaching lessons a day; Shorts come ONLY from teaching lessons (never cut a new Short from a song); everything native 4K.
     His proof (Studio, last 28 days): fact videos lead (Camel Humps 4.5K, Octopus 3.5K, Flamingos 3.0K, Meerkats 1.0K).
   - "Lessons should be interactive, not just the cartoon moving his body ... in-depth, with examples and images matching
     the items discussed. Music videos can keep the same dynamic." So lessons are built with `studio/zoo3d/teach.py` (v2):
     Milo left, the animal in the middle, a teaching board on the right: two answer signs + thinking timer, then the fact is
     SHOWN with an example from `teachprops.py` (house next to the giraffe, 4 cars counted, 7 neck bones counted, black skin under
     a magnifier, tiny pink newborn panda next to a stick of butter ...), calm cast (no dancing), a quiz with check marks.
     Formats: guessing game, champions, look-and-find, yes-or-no, this-or-that (specs: `make_lessons_p2.py`, ids zool_epNN).
     `lesson.py` (v1, narration over dancing characters) is retired for new lessons.
   - NOT LIVE YET. Prototypes zool_ep03..07 and their Shorts (shorts3d/zs4k_*.mp4, from `lesson_shorts.py`, 2160x3840) are
     "hold_review": NEVER upload a hold_review item. Noelson approves the format first; then this file gets the daily slots.
     Until then keep everything that is already scheduled and keep the schedule filled from the existing plan
     ("keep current videos ... keep the posting schedule; the new ones need to be approved by me first").
   - Every fact is checked against a reliable source before the lesson is built (spec "facts"). Lessons render with 16 samples
     at 3840x2160 (1.35 s/frame on the PC, same picture as 32); a 4:45 lesson takes about 2.6 hours, so 4 a day = ~10.5 h of GPU.
6. FULLY AUTOMATIC (Nov 13): Noelson never has to click anything for the daily run. A Google Vids download that opens a
   "save" prompt is picked up from ~/Downloads (newest .tmp/.crdownload/.mp4 after the click, size stable, verified with
   `bash studio/vids/pick_download.sh <staged> <out.mp4> 9`, 3 tries 20 s apart). Fallback: File > Export to Drive, then the
   Google Drive connector (<=10 MB). Leave the prompt alone.

## A. Views check (do this first)
1. YouTube Studio on The Animated Zoo: Content tab, then Analytics (lifetime table recipe in PLAYBOOK.md). For every public
   video record views, impressions, CTR, average view duration / % viewed, likes, title, publish date and type (Short cut,
   fact Short, song, lesson, hybrid-hook, full Vids, single-place vs multi-place vs scene-plan episode, old cast vs new cast).
2. Write it to the Command Center (https://claude.ai/artifact/VZdZppff7wA1BLKeFAWBeJ), collection "analytics", doc
   "animated-zoo-<YYYY-MM-DD>", per-video list plus totals. Pin writes with if_version.
3. What is winning vs the last check: songs vs lessons, scene-plan episodes vs older ones, new casts vs the old five,
   hybrid-hook vs plain, Short cuts vs fact Shorts.
4. Update docs/ANALYTICS.md and docs/STRATEGY_3D.md (number-backed adjustments), add the improvement note (rule 4), commit, push.
5. 2-3 line summary in the Command Center ops/status "note"; each strategy change as an "info" alert.

## B. Production
1. Collect finished renders from the PC (Documents\ZooBlender\out) and finish them to 4K with finish.py, one encode at a time.
   Jobs whose id ends in w or x are re-renders: finish them with their own job file (they publish under the song id and
   replace the old file). A folder with a DONE marker but no <id>_raw.mp4 is a cancelled job. Never use the old savanna raws
   in out\zoo3d_ep14, ep15, ep16. If status.txt has not changed for over 2 hours while it says RENDERING, the worker is
   stuck: tell Noelson (restart START_RENDER_WORKER.bat).
2. Collect finished songs (songs_out), build timing + job files (job block from the song spec, routes.py, variety check,
   2 test stills with bpy), send to the PC. Write new songs (make_specs_v3.py) and lessons (rule 5) to keep the queue full.
   Copy engine/chars/sets/worker changes to Documents\ZooBlender\zoo3d before the jobs that need them.
3. Vids hook for the soonest "to_upload" SONG that is not already a hybrid (docs/GOOGLE_VIDS.md "Hybrid"); log the credits.
   Lessons do not get a hook.
4. If nothing is available for tomorrow's 4:00 PM slot and the month's Vids allowance has 140 s or more, make one full Vids
   episode (RUNBOOK). Never more than one a day. If Vids shows a limit, terms or sign-in page: skip Vids and report it.

## C. Posting (HARD CAP 6 uploads per run; stop on "Daily upload limit reached")
1. Episode: the soonest "to_upload" Zoo entry in studio/upload_plan_3d.json at 4:00 PM ET (full Vids episodes 12:00 PM).
   Never upload "hold_fact_check", "paused_channel" or "rendering_variety" items. Review gate first (rule 4).
2. Shorts: THREE A DAY (Noelson, Nov 14) at 7:30 AM, 11:30 AM and 6:30 PM ET, at least 2 hours apart. Upload every
   "to_upload" item in studio/upload_plan_shorts_zoo.json dated today or tomorrow (soonest first), review gate first. Keep
   at least 6 Shorts (2 days) ready from what is already cut. Do NOT cut new Shorts from songs (rule 5); new Shorts come from
   lessons with lesson_shorts.py once Noelson approves the format (older note: 15-20 s cuts with make_short.sh,
   question title with the answer inside the clip), and never two Shorts from the same episode on the same day. Check each
   new Short has sound.
3. PLAYBOOK.md Studio recipe: MP4 from raw GitHub, Made for kids = yes, custom thumbnail, title 60 characters or less,
   first 2 description lines searchable, AI-disclosure boilerplate, SCHEDULE (never publish now). Passed slot: next free day.
4. Mark each upload "scheduled" with its video id, commit, push, and set it in the Command Center "videos" collection.

## D. Leave YouTube Studio on The Animated Zoo.

Notify Noelson with a short summary only when something needs him or something notable happened.
