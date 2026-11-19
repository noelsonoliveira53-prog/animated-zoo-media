# Daily run: The Animated Zoo (the scheduled task follows this file step by step)

Channel: The Animated Zoo (UC1YuY8nqnViTtm85qxE_M1w, Milo the bluebird, ages 2-6). ONLY THE ANIMATED ZOO IS ACTIVE
(Noelson, Nov 13, 2026). Tiny Truck Town, Bloop's Color Lab, Fruity Friends, Moonbeam Bedtime and Gizmo Explains are PAUSED:
do not check, render for, or upload to them; their plan entries stay "paused_channel" until Noelson says otherwise.

Read first: CLAUDE.md "Working preferences" (the lasting rules learned from Noelson's corrections; Noelson, Nov 15: "learn all
improvement that works and perfect them next time for every run to be better"). At the END of every run: if something new
worked, or he corrected something, add or replace ONE short imperative line there (never a duplicate, never a secret), and
say in the run note which line changed. Then: PLAYBOOK.md (incl. all run notes at the end: current PC queue, what is cancelled), docs/STRATEGY_3D.md,
studio/zoo3d/DAILY_3D.md, docs/GOOGLE_VIDS.md, studio/vids/RUNBOOK.md, docs/IMPROVE.md, docs/quality_baseline/README.md.
Load the `youtube-network-channels` skill (the channel rulebook) at the start of every run and apply it to everything
written, rendered, titled and uploaded.

## Standing rules from Noelson

**90-DAY PLAN (Noelson, Nov 18, 2026): `docs/GROWTH_90D.md`.** It overrides the older rules below wherever they differ: at most ONE 3D upload a
day (the 3:30 PM song); no new 3D lessons, unuploaded ones `hold_3d_cap`; a long slot with no cartoon video ready STAYS EMPTY (no 3D lesson fills it);
compilations every 2 days once Noelson approves the first; Earn-tab progress in `docs/YPP_PROGRESS.md` every run; Monday weekly review
(`docs/REVIEW_WEEKLY.md`), monthly review on the 1st.

**CARTOON FORMATS APPROVED (Noelson, Nov 16, 3:36 PM: "cartoon formats are approved, build and post").** Three pillars: songs stay 3D;
adventure stories and fact lessons are cartoon (`studio/cartoon/`, PLAYBOOK "Cartoon pipeline"); Shorts are cartoon and vertical.
- Posting: cartoon videos are plan entries like any other (`upload_plan_3d.json` formats `cartoon_adventure`, `cartoon_lesson`;
  `upload_plan_shorts_zoo.json` format `cartoon_short_90`), files under `cartoon/`, thumbnails `brand/zoo/thumb_<id>.jpg`. Same review gate,
  same Studio recipe. Slots: adventures 5:30 AM and 1:30 PM, fact lessons 9:30 AM and 5:30 PM, Shorts 7:30 AM / 11:30 AM / 7:30 PM, song 3:30 PM.
  A slot with no cartoon video ready keeps a 3D lesson; a slot never stays empty.
- Upload file: the engine's 4K H.264 is over GitHub's 100 MB, so a long video is uploaded as 4K AV1 made from it
  (`ffmpeg -i out/<id>/<id>.mp4 -c:v libsvtav1 -preset 9 -b:v 2150k -svtav1-params tune=0 -g 240 -pix_fmt yuv420p10le -c:a copy -movflags +faststart cartoon/<id>.mp4`,
  about 25 minutes; write it outside the repo and move it in). A Short's H.264 is under 100 MB and goes up as it is.
- Building (Noelson, Nov 17 10:42 PM: "ensure there is a continuous production of 2D videos ... looks like the 3D videos are the only ones
  self-uploading, update this workflow"): cartoon videos are built by FOUR OWN scheduled tasks every day, not by this run: "Animated Zoo
  cartoon lesson + 3 Shorts" (1:47 AM and 1:17 PM ET) and "Animated Zoo cartoon adventure" (8:43 AM and 7:23 PM ET). Each asks `python3 studio/upload_guard.py --next
  lesson|adventure` for its title (first THEMES title of `docs/cartoon/build_plan.py` with no plan entry), id and slots, reserves them as
  "in_production", builds by `docs/CARTOON_RUN.md` and leaves the checked files "to_upload" with a run note in `docs/cartoon/runs/<id>.md`.
  THIS run's part: (1) section C uploads every cartoon "to_upload" entry; (2) fold new run notes from `docs/cartoon/runs/` into PLAYBOOK.md and
  their defects into docs/IMPROVE.md; (3) an "in_production" cartoon entry whose slot is less than 36 hours away and whose run note shows no
  finished file: the slot keeps a 3D lesson (write one for it today) and the cartoon entry is moved to the next free slot of
  `upload_guard.py --next`; (4) if `list_triggers` shows one of the two build tasks disabled or failing twice in a row, tell Noelson.
  3D lessons are written ONLY for lesson slots of the next two days that hold no plan entry (cartoon entries count, "in_production" included):
  with one cartoon lesson and one adventure a day that is normally the 1:30 PM and 5:30 PM slots, two 3D lessons a day instead of four.
- NEVER UPLOAD A VIDEO TWICE (Noelson, Nov 17 10:42 PM: "create a process to check if the video is already uploaded and not upload twice").
  One live video per file, per title, per slot. At the START of the run: `python3 studio/upload_guard.py --audit` (fix every FAIL line before
  anything is uploaded; a "SAME TOPIC" pair of lessons or stories: hold the newer one, never upload both). Before EVERY upload:
  `python3 studio/upload_guard.py <plan file>` must print OK TO UPLOAD, and on Studio's content list `zlive("<title>")` (studio/studio-upload2.js)
  must give live = [] with rows_read above 0. Right after Studio's "Video scheduled / Video processing" dialog: write video_id and status
  "scheduled" into the plan and commit and push BEFORE the next upload (an upload that is not recorded is the one that gets uploaded again).
  A fix of a live video is the only second upload: `upload_guard.py <file> --replace <old id>`, upload on the same slot, then the old video:
  Private and renamed "OLD (replaced): <title>" in one save, its id moved to "replaced_video_ids". Old copies are deleted only with Noelson there to say yes to the list (Nov 17 11:37 PM he had all twelve Private copies removed); this unattended run never deletes: it names the Private copies in its report.
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
   - THE QUALITY LOOP FOR EVERY NEW LESSON (Noelson, Nov 14 5:12 PM: "perfect the process ... and the quality improvement
     process going"). Do the steps in this order and do not skip one; a step that fails is fixed before the next one starts:
     1. BRIEF: `review.py --brief`; write into the spec's "improves" what this lesson does better than the last one
        (at least one picture improvement and one teaching improvement), plus every open defect from docs/IMPROVE.md.
     2. FACTS: every sentence that states a fact has a source that was opened and read that day (spec "facts"). A line
        whose source cannot be read is taken out. No fact is kept "because it is well known".
     3. BUILD: `python3 teach.py lessons/<id>.json`. It must print no "FAIL:" line: lesson 300-390 s, every part 85-95 s,
        100% of the words placed from the audio, no suspect pronunciation, every answer sign inside the Shorts-safe area.
        (The same list is saved in jobs/<id>_problems.json and review.py fails the video on it.)
     4. LOOK: `python3 teach_stills.py <id> "<part>:<line>:<frac>" ...` for at least one frame per part where an example or
        the answer signs are on screen. Check by eye: the example is the right size next to the animal, nothing covers a
        face, the signs and Milo are inside the centre 90% of the picture's width (that is what the Short shows).
        Also one frame of EVERY quiz answer close-up (the green check must stand beside the head, not on a face and not
        hidden behind a neighbour), one of the quiz question (the "?" badge and the QUIZ TIME! word are not on top of
        each other) and one of every close-up line while an example is up (Nov 15: all four were wrong in the approved
        format; engine `--frames a,b,c --test` renders any frame numbers; at most 10 stills per run, one run at a time:
        two at once ran out of memory). A rendered lesson with one of these defects is repaired with a slice job
        ("frame_range" in the job, see fix_layout.py) and `splice_slices.py`, not with a full re-render.
     5. RENDER on the PC (native 4K), then finish.py. v3 lessons are written to the plan as "hold_review".
     6. GATE: `review.py <file> --job jobs/<job>.json --note "<one concrete thing the next lesson does better>"`, and look at
        the contact sheet next to docs/quality_baseline/.
     7. SHORTS: `lesson_shorts.py <raw> <id>` (one 85-95 s Short per part), then look at one frame of EVERY Short at a
        moment with the answer signs: nothing may touch the edge of the middle band. Look at every Short's THUMBNAIL too:
        it must show the example (set "thumb_line" in the spec), not Milo's close-up.
     8. LOG: every defect seen in steps 4, 6 and 7 goes into docs/IMPROVE.md with `review.py --improve` the same day, and
        the next lesson's "improves" must name it as fixed. A defect is "fixed" only after a frame shows it fixed.
     9. REPORT to Noelson only what exists and was checked; list what was NOT checked.
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
   - CONFIRMED as the plan (Noelson, Nov 14 3:28 PM: "Keep that as the new plan"). He also asked: use the
     youtube-network-channels skill (channel bible + rulebook) on every new video; "ensure graphics are improved and enriched
     with details and all words in sync"; and "don't make assumptions, say only what is delivered".
     * REPORTING RULE: in every message to Noelson state only what exists and was checked (file made, render finished and
       probed, upload confirmed in Studio). No estimates presented as facts, no "should be", no promises about results.
     * WORD SYNC: teach.py places every word by forced alignment of each spoken line (`wordsync.py`, PocketSphinx, in setup.sh).
       Captions, counting props, answer signs and Shorts captions all use those times. songs/<id>.json "sync" records
       aligned/words; review.py FAILS a v2 lesson under 100% aligned or with "suspect_words" (a word the voice mispronounced:
       Kokoro read "Shh." as S-H-H and "Brrr" as B-R-R-R; wordsync.SAY maps such spellings to sayable ones, captions keep the text).
     * GRAPHICS: every new lesson must add or enrich on-screen detail (teachprops.py `_detail` pass: shutters, flower boxes,
       confetti on a right answer, sparkles, bubbles, smoke ...) and say what changed in the spec's "improves".
       Check new props with `python3 bpyrun.py prop_gallery.py -- out.png` before a lesson uses them.
     * 4K lesson raws are ~500 MB and the session can fetch 400 MB per file: the worker (split_big, needs the worker restarted
       once) also writes <id>_raw.partNN.mp4 pieces; join them with ffmpeg concat (-c copy) before finish.py.
   - LENGTHS (Noelson, Nov 14 5:12 PM: "adjust the shorts to be a minute and half long and long videos to be minimum
     5 minutes long"). This is lesson format v3 and replaces the 4:30 lesson with 30-second Shorts:
     * LESSON: 5:00 minimum (300 s), 6:30 maximum (390 s). Structure: hello, THREE parts, quiz (3 questions), goodbye.
     * PART = SHORT: each part is one complete mini-lesson of 85-95 s and is cut, whole, into one Short of 85-95 s
       (2160x3840). A part runs: hook question or 3 clues, thinking time, answer, the fact SHOWN with an example, a "why?" or
       second question round, one more sourced fact with its own example, say it with me, an action to copy, QUICK CHECK
       (two answer signs + thinking dots + confetti on the right one). Spec fields: "version": 3, "checks": [...] (see
       `studio/zoo3d/make_lessons_p3.py`, ids zool_ep08..12; teach.py clears the board before each check).
     * Three animals per lesson, not four: the time goes into depth. Shorts-safe layout: answer signs at x=1.95 and at most
       2.8 wide, Milo at x=-2.8, clue badges at x 1.2-3.2; the Short shows the centre 90% of the picture's width.
     * YouTube allows Shorts up to 3 minutes (square or vertical, uploaded after Oct 15 2024):
       https://support.google.com/youtube/answer/15424877 (read Nov 14). A Short over 1 minute with any copyright claim is
       blocked, so lesson Shorts use only our own voice and music.
     * Cut Shorts ON DEMAND: only for the slots of the next 2 days (3 a day), never the whole backlog. A 90 s 4K Short is a
       large file and the repo is already 9.1 GB (measured Nov 14).
     * The rulebook's old numbers (Shorts 20-60 s, long 4:30-6:30) no longer apply to The Animated Zoo's lessons; songs
       are as long as each one needs (his answer Nov 14 11:00 PM; no minimum).
   - FORMAT V3 APPROVED (Noelson, Nov 14 11:00 PM, after watching zool_ep08 and its three Shorts: "1: approved"). The file
     studio/zoo3d/LESSON_V3_APPROVED exists, so finish.py writes v3 lessons as "to_upload". Approved means the FORMAT: every
     single video still goes through the quality loop and the review gate, and an item marked "hold_review" is never uploaded.
     * THE DAILY GRID (Noelson, Nov 15 1:08 AM: "Fit four" = four lessons a day, existing times moved to fit). Eight
       videos a day, every slot 2 hours apart, all times ET:
         5:30 AM lesson 1 | 7:30 AM Short | 9:30 AM lesson 2 | 11:30 AM Short | 1:30 PM lesson 3 | 3:30 PM SONG |
         5:30 PM lesson 4 | 7:30 PM Short
       (song moved from 4:00 PM to 3:30 PM, evening Short from 6:30 PM to 7:30 PM, for everything NOT yet on YouTube).
       Fill order for lessons when fewer than four are ready: 1:30 PM, 9:30 AM, 5:30 PM, 5:30 AM.
       A slot is filled ONLY with a lesson that passed the whole quality loop; an empty lesson slot is better than a weak
       video. Videos already scheduled on YouTube keep their times; on a day that still has one at 4:00 PM or 6:30 PM the
       5:30 PM lesson slot stays empty (it would be closer than 2 hours).
       To reach four a day the PC must render four lessons a day (measured: 3 h each = 12 h) plus the song: write the next
       day's four lessons FIRST in every run and queue them before anything else.
       First lessons: zool_ep08 Nov 15 1:30 PM; zool_ep09 Nov 16 9:30 AM; zool_ep10 Nov 16 1:30 PM; zool_ep11 Nov 17 9:30 AM;
       zool_ep12 Nov 17 1:30 PM.
     * LESSON SHORTS get the Shorts slots first (his rule: Shorts only from teaching videos): from Nov 17 each day's three
       slots go to lesson Shorts (three different lessons on one day), and an already-cut song Short only fills a slot when
       no lesson Short is ready. Re-cut zool_ep08 Shorts (larger captions): Nov 17, 18 and 19 at 11:30 AM.
     * SONGS (Noelson, Nov 14 11:00 PM: "leave songs duration according to each necessity you judge"): no minimum length;
       each song is as long as its lyrics and teaching need. The 5-minute minimum is for teaching lessons only.
     * Superseded and never uploaded: zool_ep03..07, the "b" renders zool_ep03b..07b, shorts3d/zs4k_*.mp4.
     Keep everything that is already scheduled and keep the schedule filled from the existing plan
     ("keep current videos ... keep the posting schedule; the new ones need to be approved by me first").
   - Every fact is checked against a reliable source before the lesson is built (spec "facts"). Lessons render with 16 samples
     at 3840x2160 (measured on the PC Nov 14: 1.29-1.35 s/frame, same picture as 32). A v3 lesson is 8,000-8,430 frames.
     MEASURED Nov 14 on the first v3 lesson (job zool_ep08a, 8,000 frames): started 6:38:55 PM, frames done 9:35:06 PM, raw
     assembled 9:38:46 PM = 2 h 59 m 51 s for the whole job (1.30 s/frame after a 3 m 17 s scene load). Four lessons a day
     at that rate is about 12 hours of GPU; the song comes on top.
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

## C. Posting (up to 20 uploads in any 24 hours, all for The Animated Zoo; no lower cap per run since Nov 16 11:09 PM; stop on "Daily upload limit reached")
Owner, Nov 16: "daily cap should not be a thing since now we upload only the animated zoo ... should be 20 a day". Before uploading, COUNT the uploads of the last 24 hours
(`git log --since="24 hours ago" --format="%ad %s" --date=format:%H:%M | grep -i scheduled`, every session's uploads are committed there) and use what is left of 20. Never write
"at the cap" without that count. The 20 is our own observation of Nov 3 (the limit was hit at about 20 in 24 hours, when the channels were not phone-verified); YouTube Help gives no
number ("Limits may vary by country/region or channel history"), and the channel has Advanced features since then, so the real limit may be higher: it is only known when the message appears.
0. Guard first (standing rule "NEVER UPLOAD A VIDEO TWICE"): `upload_guard.py --audit`, then `upload_guard.py <file>` and `zlive` before each upload.
   CARTOON ENTRIES ARE UPLOADED BY THIS RUN: every "to_upload" entry with format cartoon_adventure or cartoon_lesson in studio/upload_plan_3d.json and
   every "to_upload" cartoon_short_90 in studio/upload_plan_shorts_zoo.json, WHATEVER ITS DATE (they are scheduled days ahead), soonest slot first, each on
   the date and time in its entry, after review.py PASS and a look at its contact sheet. They come before 3D lessons when the allowance is short.
1. Episodes, TWO a day since Nov 15: the SONG = the soonest "to_upload" 3d_singalong Zoo entry in studio/upload_plan_3d.json
   at 3:30 PM ET (full Vids episodes 12:00 PM); the LESSONS = every "to_upload" 3d_lesson entry with lesson_version 3, each at
   the date and time in its plan entry (rule 5 THE DAILY GRID: 5:30 AM, 9:30 AM, 1:30 PM, 5:30 PM). Schedule each for its own
   date and time, never "publish now".
   Never upload "hold_fact_check", "paused_channel" or "rendering_variety" items. Review gate first (rule 4).
2. Shorts: THREE A DAY (Noelson, Nov 14) at 7:30 AM, 11:30 AM and 7:30 PM ET (6:30 PM until Nov 16), at least 2 hours apart. Upload every
   "to_upload" item in studio/upload_plan_shorts_zoo.json dated today or tomorrow (soonest first), review gate first. Keep
   at least 6 Shorts (2 days) ready from what is already cut. Do NOT cut new Shorts from songs (rule 5); new Shorts come from
   lessons with lesson_shorts.py (format approved Nov 14 11:00 PM; lesson Shorts take the slots first): 85-95 s each, one whole lesson part per Short (rule 5
   LENGTHS; the older 15-60 s cuts are no longer made), and never two Shorts from the same episode on the same day. Check each
   new Short has sound.
   WATERMARK IS MANDATORY (Noelson, Nov 16: "include watermark on all videos on upload with the channel characteristics"). Every
   upload, episode AND Short, carries the channel mark in the picture: Milo's channel picture in a white ring + "The Animated Zoo"
   (brand/zoo/watermark.png, watermark_short.png; built by `python3 studio/zoo3d/watermark.py build`). YouTube's own channel
   watermark is not shown on made-for-kids videos, so it is burned in:
   - finish.py lays it on every episode (top left; job "watermark_pos": "tr" = top right) and lesson_shorts.py on every Short
     (centred above the title). Both stop if the mark is not in the finished picture. Thumbnails stay without the mark.
   - A finished file from before Nov 16 that is still waiting: `python3 studio/zoo3d/watermark.py apply <in.mp4> <out.mp4>`,
     then replace the file (same name) and set the plan entry's "watermark".
   - review.py FAILS a video without the mark (`watermark.py check <file>`). Never upload around it.
   - LOOK at every new episode: `python3 studio/zoo3d/watermark.py corner <file> <sheet.jpg>` shows the mark's corner every 5 s
     with the time. No face, answer sign, 3D word or example may sit under the mark (zool_ep11's sheet, Nov 16: the giraffe's face
     in its close-ups at 5:05, 5:25, 5:45 and the top of the YES sign at 0:10-0:25; zool_ep14, zoo3d_ep17, zoo3d_ep18: nothing).
     If something does: put "watermark_hide": [[from s, to s], ...] into the job (the mark fades away for those moments; take each
     window from the shot's start to its end in the job's timing, not from the 5 s sheet alone) or "watermark_pos": "tr" when the
     top right is free for the whole video (it is where the answer sign's check mark sits), then finish again and look again.
     To see it before the 25-minute encode: `watermark.py corner <file> <sheet.jpg> --hide 300-312,340-350` on an unmarked file.
   - Videos that were already uploaded or scheduled before Nov 16 10 AM have no mark and are not replaced for it.
3. THUMBNAILS ARE MANDATORY (Noelson, Nov 14: "ensure the new posts are activating with YouTube skills to ensure personalized
   thumbnails are being applied to all videos upon posting"). Every upload, episode AND Short, gets its own custom thumbnail:
   - The file comes from the plan entry's "thumb" (episodes: brand/zoo/thumb_<id>.png from finish.py; Shorts:
     brand/zoo/shorts/thumb_<id>.png from lesson_shorts.py or `python3 studio/zoo3d/short_thumb.py <short.mp4> --text "3 WORDS" --plan`).
     Packaging follows the yt-package skill: title and thumbnail are one unit, thumbnail text 3 words max and never the title's
     words, lint with `python3 /root/.claude/skills/yt-package/title.py --title "..." --thumb "..."`. review.py FAILS a video
     with no thumbnail file, a thumbnail shared with another video, or more than 3 thumbnail words.
   - In the upload dialog set the thumbnail (PLAYBOOK recipe: arm the PNG, `ytcp-thumbnail-uploader`, "Upload file"), then
     VERIFY it before scheduling: the uploader shows the image as selected (a `data:`/`blob:` img with the "custom" tile active).
     Never use the old fallback "schedule without a custom thumbnail". If it will not take after 3 tries, schedule the video,
     then open its Details page (studio.youtube.com/video/<id>/edit) and set the thumbnail there in the same run.
   - Shorts: Studio on desktop accepts custom Shorts thumbnails since July 2026 (rolled out to Partner Program channels
     first). If the Short's upload dialog / Details page offers "Upload file", use the plan's thumb; if it only offers frame
     picking, pick the frame closest to the thumb and record it.
   - Record the result in the plan entry: "thumb_set": true | "frame_only" | false, and report every false to Noelson.
   Then the rest of the PLAYBOOK.md Studio recipe: MP4 from raw GitHub, Made for kids = yes, title 60 characters or less,
   first 2 description lines searchable, AI-disclosure boilerplate, SCHEDULE (never publish now). Passed slot: next free day.
4. Mark each upload "scheduled" with its video id, commit, push, and set it in the Command Center "videos" collection.

## D. Leave YouTube Studio on The Animated Zoo.

Notify Noelson with a short summary only when something needs him or something notable happened.
