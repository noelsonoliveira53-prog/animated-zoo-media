# Gizmo Explains: production run (owner, Nov 19 2026, 12:37 AM)

> "Gizmo Explains channel is the second better performing channel now; let's incorporate that channel on our posting starting tonight:
> create 2 new videos for that channel and post, also change channel description, create a nice banner for the channel and follow same
> principles we are following for The Animated Zoo, however with one 3D explainer a day, minimum 5 mins, and Shorts come from that,
> + create a cartoon version of that and let's test it."

**2D ONLY (Noelson, Nov 21 2026, 11:27 AM: "chaneg gizmo as well and start the workflow for the day"; the evening before, for The Animated Zoo:
"Let's keep just 2d cartons on the channel suspend all 3d uploads of songs and fill the spaces with the same carton model we have").** It overrides
every line below that builds, renders or uploads something in 3D:
- Gizmo Explains posts cartoon explainers only (`studio/cartoon/toon.py`, Gizmo's cast `studio/cartoon/art_gizmo.py`). No 3D explainer is written,
  rendered on the PC or uploaded, and no Short is cut from one. `upload_guard.py --channel gizmo` refuses the 3D formats (gizmo_explainer,
  gizmo_short_90), as a fix too, and its audit fails one that waits.
- gzx_ep01 (rockets), gzx_ep02 (rain) and their six Shorts were never rendered (the PC's render folder was refused three nights running) and never
  uploaded: they carry "hold_2d_only". Specs, jobs and audio stay in the repo; nothing on the PC is touched or deleted. Their topics are built again
  as cartoons (rockets first).
- The 3D songs that were public before Nov 19 stay (deleting a video is the owner's decision).
- The PC is no longer needed to BUILD: a cartoon is rendered in the cloud session. Only the upload uses the PC (Studio in its built-in browser).
- THE FORMAT IS APPROVED since Nov 21 2026 2:33 PM (owner, after watching gc_ep01.mp4: "gizmo is aproved please upload"; the marker file exists, `--next` prints "finish_as": "to_upload"). What follows in this bullet is the record of the gate as it stood until then.
- [until Nov 21 2:33 PM] THE FORMAT GATE STANDS (CLAUDE.md: "Nothing in a new format is uploaded until the owner has watched one full video of it and approved it"):
  he has not watched a Gizmo cartoon yet. `cartoon/gc_ep01.mp4` ("How Does a Seed Grow Into a Plant?", built Nov 19) and its Short 1 were sent to
  him on Nov 21 at noon. Until he says yes every Gizmo cartoon entry is "hold_review" and the guard refuses it. On his yes: write the file
  `studio/cartoon/GIZMO_CARTOON_APPROVED` (one line: his words, the date), set the waiting entries "to_upload" with slots from `--next`, and
  upload them. If he asks for changes instead: fix them in gc_ep01 first, send it again, and log each in docs/IMPROVE.md.

Channel: Gizmo Explains, @GizmoExplainsHQ, channel id UCJaMYOrKCEA54kaOMyYNiKQ, ages 4-8, made for kids. Host: Gizmo, a small round
silver robot with a screen face and an antenna that lights up when he has an idea (3D: `studio/zoo3d/chars/gizmo.py`; flat cartoon:
`studio/cartoon/gizmo/gizmo_flat.svg.part`). Brand: background #1d3a8a to #3561d9, text white, accent #5ff3ff.

Done Nov 19 (about 10 AM ET): new channel description and banner (`brand/gizmo/banner.png`, safe area checked in Studio's crop view), both read
back after a reload of the customization page.

## What the channel posts

- ONE cartoon explainer a day, 5:00 to 6:30 long, built like an Animated Zoo cartoon fact lesson (interactive: questions with answer signs and
  thinking time, on-screen examples of the exact thing explained, every word in sync, a quiz at the end) with Gizmo as the host and science
  examples instead of animals. Three parts of 83-90 s, each cut whole into one vertical Short (85-95 s, 2160x3840, every shot framed again for 9:16).
  [Until Nov 21 11:27 AM this was a 3D explainer; see 2D ONLY above.]
- Slots (ET): explainer 2:10 PM; its Shorts on the next days at 8:10 AM, 12:10 PM and 7:10 PM, each on its own day. Always scheduled, never published
  at once. `python3 studio/upload_guard.py --next explainer --channel gizmo` prints the topic, the id (gc_epNN), the slots, what waits and what is missing.
- Main intro: Gizmo has his own (owner, Nov 21 12:01 PM: "create an intro for the gizmo explain as well"): `studio/cartoon/intro_gizmo.py`
  (four shots, about 15 s: the idea, the things he explains, the logo, "Gizmo Explains!"), its music `studio/cartoon/score_gzintro.py` (his own tune
  on recorded instruments, C | F | G C), preview `python3 toon.py gzintro`. APPROVED by him on Nov 21 at 12:18 PM, picture and music ("amazing emplement on every new video and update the worflows"): every new long
  Gizmo cartoon carries `*gz_intro_shots()` right after the hook (the episode still opens on its promise) and again as the last four shots, with
  `**GZ_INTRO_STAGES` in STAGES and no `"intro"` key in the EP. The plan check fails an episode that has it once, not last, or that carries the
  Zoo's intro; `review.py` fails a long Gizmo cartoon whose file does not show it at both ends (`python3 studio/bookends.py check <file> --channel gizmo`,
  against `cartoon/gzintro.mp4`). Its own content stays 5:00 or more, the whole file 6:30 or less. Never in a Short. Never the Zoo's `intro_shots()`
  on Gizmo. Change the intro in intro_gizmo.py only (its music is approved: picture changes do not touch score_gzintro.py), then render
  `toon.py gzintro` again and replace `cartoon/gzintro.mp4`.
  Explainers built before the approval have no intro and are not uploaded as they are: gc_ep01 (it also opens with a greeting: give it an opening
  on its promise, the first line asks the title's question) and gc_ep02 if the noon build of Nov 21 finished it without one. Add the intro in both
  places, look at the stills of the changed shots, render again, run every check again. Their Shorts are not touched.
- No playlists yet, no song: a voice only speaks.
- Every rule of CLAUDE.md "Working preferences" applies to Gizmo too: 4K native, watermark (Gizmo's channel picture + "Gizmo Explains",
  not Milo), custom thumbnail with at most 3 words and none of the title's words, facts read at the source the same day (line taken out
  if the source cannot be read), stills before the render, frames after, listen.py, review.py, no voice sung or hummed onto notes,
  no '<' or '>' in titles or descriptions, every defect in docs/IMPROVE.md.
- Writing: warm, simple words, short sentences, one true idea per video, questions to the viewer; no danger, fear, anyone hurt, lost,
  crying or trapped, nothing unsafe a child could copy (no fire, electricity at home, chemicals, climbing), no calls to action aimed at kids.
  Description ends with the channel boilerplate: "Gizmo Explains makes gentle, colorful videos for little learners. New videos every day!
  Made with care for ages 4-8. Every fact is checked against trusted sources and every script is reviewed for kid safety before publishing."

## A cartoon explainer, step by step (the daily build)

Model: `studio/cartoon/episodes/gc_ep01.py` and its run note `docs/gizmo/runs/gc_ep01.md` (what was built, looked at and fixed). The steps are
docs/CARTOON_RUN.md's ("Steps", "A fact lesson and its three Shorts", the STOP section about voices, "Several cartoon builds at the same time"),
with these differences:
1. `python3 studio/upload_guard.py --next explainer --channel gizmo`. "unfinished_first" and "shorts_missing" come before a new title (gc_ep01 has
   Short 1 only: Shorts 2 and 3 are built first). If "note" says two or more explainers wait, build NO new explainer. Otherwise claim the title:
   entries in `studio/upload_plan_gizmo_v3.json` (`cartoon_lesson` + three `cartoon_short_90`, `"channel": "gizmo"`, `"topic"`: the title as
   topics.json has it, the slots printed) as "in_production", commit and push at once.
2. Facts: read each at its source today, quotes at the top of the episode file; a line whose source cannot be read is taken out. Nothing a child
   could copy unsafely (no fire, electricity at home, chemicals, climbing).
3. Episode: `EP["wm"] = "brand/gizmo"` (Gizmo's mark), `"beat": True`, Gizmo's rig and places from `art_gizmo.py` (new props go into that file or an
   `art_gc_epNN.py`), voice `am_michael`, Gizmo's main intro after the hook and as the last four shots (see "Main intro" above; never the Zoo's `intro_shots()`), no tune shot unless instruments play it. Gizmo's arms stay between -50 and -85 degrees
   (a hand raised higher disappears behind his head); a camera on Gizmo frames the whole robot ("all"), or his antenna is cut; 9:16 words at or
   below 0.35 of the view (higher they sit on the title band).
4. Packaging as docs/CARTOON_RUN.md "VIRAL PACKAGING" with Gizmo in Milo's place: opens on its promise, Gizmo's name after the hook, a question
   title under 60 characters with no '<' or '>' (the series name "Gizmo Explains" last when it fits), a one-object thumbnail with 1-2 words and none
   of the title's words (`brand/gizmo/thumb_<id>.jpg`). Description: where the facts come from, then the Gizmo boilerplate below; never "AI".
5. Checks, none skipped: plan check, `listen.py --episode <id>` before the render, a still of EVERY shot in 16:9 and again in 9:16 looked at (and
   again after each fix), 4K render as a tracked background command, then on every finished file `--check4k`, `pace_check.py --max 8`,
   `watermark.py check <file> --channel gizmo` and its corner sheet looked at, `bookends.py check <file> --channel gizmo` on the explainer, frames of the finished file (every answer reveal), listen.py on the
   file with its picture looked at (it measures, it does not hear), AV1 encode of the explainer, `review.py` PASS.
6. Finish: the entries get the status `--next` printed as "finish_as" ("hold_review" until the owner's yes, then "to_upload"), title, description,
   tags, thumb, thumb_text, seconds; run note `docs/gizmo/runs/<id>.md` (what was looked at, what was not checked, every defect); commit, push.
7. Upload (only "to_upload" entries, so only after his yes): section "Never upload twice, on the RIGHT channel" below.

## Topics

The list is `docs/gizmo/topics.json` (in order; `--next` takes the first one with no cartoon entry: rockets, then rain, then the heart). The
paragraph below is the list as it was written on Nov 19.

Already on the channel (songs, do not repeat as explainers): magnets, day and night, the 5 senses, rainbows, why the sky is blue, sink or
float, weather, the planets. Explainer topics in order (take the first one with no plan entry): How Do Rockets Fly?; Where Does Rain Come
From? (the water cycle, not weather); How Does a Seed Grow Into a Plant?; How Does Your Heart Work?; Why Do Things Fall Down? (gravity);
How Do Bees Make Honey?; Why Does Ice Melt? (solid, liquid); How Does Sound Travel?; Where Do Shadows Come From?; Why Does the Moon
Change Shape?; How Do Birds Fly?; How Do Our Teeth Help Us?; How Does a Bicycle Move?; Where Does Light Come From?

## Never upload twice, on the RIGHT channel

- Plan file: `studio/upload_plan_gizmo_v3.json`. Guard: `python3 studio/upload_guard.py <file> --channel gizmo` (and `--audit --channel gizmo`).
- Studio's active channel is shared with The Animated Zoo's runs. Switch: Studio avatar menu > Switch account > "Gizmo Explains" (the
  youtube.com/account list does NOT switch Studio reliably, seen Nov 19). Before arming any file read the drawer's channel name
  (`document.querySelector('.entity-name').innerText` must be "Gizmo Explains") and the URL's channel id UCJaMYOrKCEA54kaOMyYNiKQ;
  `zlive("<title>")` on Gizmo's content list must give live = []. Read the channel name again on the upload dialog's page before
  clicking Schedule. When done, switch back to The Animated Zoo the same way and read its name in the drawer.
- Never drive Studio while another run is using it (the Zoo daily run 6:31 AM until it finishes; check the commit log for a run note
  in the last 30 minutes).

## Engine [3D: SUSPENDED Nov 21 2026 11:27 AM, see 2D ONLY at the top. Nothing below is run; it stays for the record and for the code it describes.]

The 3D lesson tools (`studio/zoo3d/teach.py`, `lesson_shorts.py`, `teachprops.py`, `finish.py`, `watermark.py`) were written for the Zoo:
the host is Milo and the cast are animals. The first Gizmo build adds a channel switch (`"channel": "gizmo"` in the spec: host char gizmo,
Gizmo's lab and outdoor sets, science example props, Gizmo watermark, `gizmo/` output folder) without changing anything a Zoo spec
produces (prove it: a Zoo spec's job JSON is byte-identical before and after). The PC renders the 3D jobs (worker, Blender) as for the Zoo.

### Engine, built Nov 19 (first explainers gzx_ep01, gzx_ep02)

- Spec `"channel": "gizmo"` (see `studio/zoo3d/make_gizmo_x1.py`): host `gizmo`, cast `["pal"]` (pink mini helper bot; `pal2` green), set
  `gizmoworld` (`"biome": "lab"` = his science lab, any other biome = a Zoo World place), job `"channel": "gizmo"`, song format `gizmo_explainer`,
  Gizmo boilerplate. finish.py -> `gizmo/<id>.mp4`, `brand/gizmo/thumb_<id>.png`, plan `studio/upload_plan_gizmo_v3.json`, Gizmo's mark;
  lesson_shorts.py -> `gizmo/shorts/`, `brand/gizmo/shorts/`, same plan, format `gizmo_short_90`; review.py reads that plan and checks Gizmo's mark
  and boilerplate; `watermark.py <cmd> ... --channel gizmo` (`build gizmo` made `brand/gizmo/watermark*.png` from the channel picture
  `brand/gizmo/avatar.jpg`, read from the channel page Nov 19). A Zoo spec builds a byte-identical job (proved on zool_ep22, run note).
- Science props in teachprops.py: rocket (gas, stages, drop), tanks, jet, cloud (grey, rain), vapor, puddle (shrink), dust, drops, cycle, river.
- The quiz is a teach part with three answer-sign rounds (`checks`), not the Zoo's arc quiz.
- Stills: `python3 studio/zoo3d/stills_by_place.py <id> <tag> seg:line:frac ...` (one place at a time: the local software render stalls on the
  lab when all places are in one scene).
- Audio for the PC: `jobs/audio_gizmo/<id>_song.flac` (the .wav files are not in git); copy it to the PC as `<id>_song.wav` (decoded) with the job
  and timing, read back and compare, as for the Zoo.
