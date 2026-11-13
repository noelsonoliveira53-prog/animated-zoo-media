# The Animated Zoo: production playbook

Channel: **The Animated Zoo** (@TheAnimatedZoo, UC1YuY8nqnViTtm85qxE_M1w). Host: **Milo the bluebird**.
Audience: kids 3–8. Channel and every video are set **made for kids**.

## Posting cadence (keep to this)
- **4 Shorts a day** at **7:30 AM, 11:00 AM, 3:00 PM and 7:00 PM ET**.
- **1 five-minute episode a day** at **5:00 PM ET**.
- This is Noelson's chosen volume. Keep every video different: a new animal or a NEW fact
  (never re-upload the same script). Near-identical mass uploads risk YouTube's
  "repetitious content" rule, which is the main risk to the channel.
- Every upload is scheduled ahead in Studio, so posting doesn't need the PC to be on.
- Keep at least 2 days of videos scheduled ahead.

## Kids-safety rules (non-negotiable)
- Facts only from zoo / science sources (San Diego Zoo, Smithsonian's National Zoo, NOAA, NASA,
  Natural History Museum). If unsure, cut the line. Hedge guesses ("scientists think").
- No scary words (kill, attack, deadly, blood-and-guts, monster), no predation detail,
  no brands or toys, no "subscribe" nagging, no requests for kids' names, ages or comments.
- Calm pacing (TTS speed 0.85 for long-form), music ducked under voice, loudness -16 LUFS.
- All art is original (`studio/art.py`, `studio/art2.py`). Never draw known characters.
- Every video ends with the kindness rule: "Be kind to every animal."

## Animation quality layer (`studio/fx.py`)
Every video gets: dark sticker outline + ground shadow, eye blinks, breathing/idle sway,
Milo's beak moving while he talks, slow camera push-in, bounce/slide-in entrances with squash,
confetti + camera punch on reveals, twinkling sparkles, birds flying across, circle-wipe
transitions between animals (episodes), and bouncy captions. GSAP gotcha: never combine
`rotation` with `svgOrigin` in the same tween as `x` on `#animal`; it leaves an offset.
Any new art must keep `<g id="animal">` and dark pupils `fill="#1a1a2e"` so blinks work.

## Formats
- **Short** (1080x1920, ~25 s): hook question → Milo flies in → 3 facts → move-along ask → sign-off.
  Defined in `studio/shorts2.json` / `studio/episodes.json`, built with `build.py <id>`.
- **Episode** (1920x1080, ~5 min): intro + count-along → 5 animals × (clue + guess pause, fact,
  move-along, question + think pause, reveal, say-it-together, fact, bye) → recap → outro.
  Defined in `studio/eps/*.json`, built with `long.py eps/<id>.json`.

## Build environment
```
npm i -g hyperframes@0.8.231 && pip install kokoro-onnx soundfile numpy --break-system-packages
cd studio && mkdir -p vendor && cd vendor && npm pack gsap@3.15.0 @fontsource/baloo-2@5.1.1 \
  && tar xzf gsap-3.15.0.tgz && mkdir f && tar xzf fontsource-baloo-2-5.1.1.tgz -C f && cd ..
export HYPERFRAMES_BROWSER_PATH=$(node -e "console.log(require('playwright').chromium.executablePath())")
./night.sh s_<animal> ep04_<theme>     # renders, then pushes MP4s to this repo
```
`night.sh` expects the repo at /home/claude/animated-zoo-media and the builder in /root/zoo;
adjust the two paths if running elsewhere.

## Posting (YouTube Studio in the browser on Noelson's PC)
YouTube's API isn't reachable from the cloud workspace, so uploads go through Studio:
1. Open `studio.youtube.com/channel/UC1YuY8nqnViTtm85qxE_M1w/videos/upload?d=ud`.
2. In the page, fetch `https://raw.githubusercontent.com/noelsonoliveira53-prog/animated-zoo-media/main/<file>.mp4`
   into a File and intercept `HTMLInputElement.prototype.click` for file inputs (see `studio/studio-upload.js`).
3. Click **Select files** (it's at about (400, 547) in an 800x892 view).
4. Fill title + description (execCommand insertText into `#textbox`), tick made-for-kids,
   click `#next-button` ×3, click `#second-container-expand-button` (Schedule), and set the TIME
   by script first (`ytcp-datetime-picker input`, insertText "7:30 AM", then dispatch input/change).
   The DATE needs real input: click the date trigger at about (150, 489) in an 800x892 view, take a
   screenshot to confirm the calendar is open, triple-click the date box at (150, 482), type e.g.
   "Nov 5, 2026", press Enter. Verify `#datepicker-trigger` text and the time value by script, then
   click `#done-button`. Confirm with a zoom on (140,220)-(660,380): "Video scheduled ... on <date> at <time>".
   (Clicking calendar day cells is unreliable, so don't.)
   If execCommand returns false (browser pane hidden / page not focused), click the title box once with a
   real click first, then rerun the fill script. If Studio opens on another channel, switch to
   @TheAnimatedZoo via the account menu > Switch account. Schedule panel shows GMT-0500 = ET.
   **If the browser pane is hidden on the PC** (document.hasFocus() is false), execCommand does nothing.
   Then set the title and description by writing `textContent` on each `#textbox` and dispatching an
   `input` InputEvent. Set the date and time with real input only: click the date trigger (150, 489),
   take a screenshot (the calendar must be open), triple-click the date text (120, 483), type, press Enter,
   click empty space (680, 420) to close the calendar. For the TIME, the reliable way is: by script run
   `ti=document.querySelector('ytcp-uploads-dialog ytcp-datetime-picker input'); ti.focus(); ti.select()`,
   then type "3:00 PM" with real keystrokes and press Enter.
   If #done-button click by script does nothing, wait until the header stops saying "Saving..." and click
   the Schedule button for real at about (731, 810).
   Read back `#datepicker-trigger` and the time value by script before clicking `#done-button`, because a
   wrong value silently schedules for 12:00 AM. To fix a scheduled time later: open /video/<id>/edit, open
   Visibility, retype the time the same way, click Done, then click `#save`.
   Other channels: Studio only opens the channel that is active in the channel switcher. Switch with
   youtube.com/channel_switcher (click the channel's ytd-account-item-renderer), and switch back to
   The Animated Zoo when done, or the nightly task's Zoo URLs show "Oops".
   Nov 4 run (hidden pane, 800x892 emulated): after the 3 Nexts, really click the Schedule header (540, 583); if the calendar
   doesn't open, click the date box (150, 496). Then by script focus+select the calendar's date input (value contains the year),
   type "Nov 7, 2026" + Enter; focus+select the time input by script, type + Enter; read back; real-click Schedule (731, 808).
   Do NOT use studio-upload.js `fill()` for scheduled posts: it clicks PUBLIC and publishes immediately.
5. Episodes: also set the thumbnail from `brand/thumb_<id>.png` via `ytcp-thumbnail-uploader input#file-loader`.
   **Verified channels (Nov 7, 2026, Noelson): The Animated Zoo, Bloop's Color Lab and Gizmo Explains are phone-verified.**
   On those three, EVERY upload gets the full package before scheduling: custom thumbnail `brand/<channel>/thumb_<id>.png`
   (1280x720, under 2 MB), title, searchable description, made for kids. Do it in the upload dialog's Details step:
   `armThumb(path)` (same File + `HTMLInputElement.prototype.click` interception as the MP4), scroll `ytcp-thumbnail-uploader`
   into view, then REAL-click its "Upload file" tile (the tile's left third). Setting files on input#file-loader by script does
   nothing. Confirm an `img` with a `data:` src appears in the uploader before clicking Next. If it was missed, fix it after
   scheduling on /video/<id>/edit (same click, then click `ytcp-button#save`; "Changes saved" toast).
   Tiny Truck Town, Fruity Friends and Moonbeam Bedtime are NOT verified: "Upload file" opens "verify your phone number";
   cancel it and schedule without a custom thumbnail.
   Channel switching (Nov 7): if youtube.com/channel_switcher clicks stop sticking, use Studio's own avatar menu >
   Switch account (avatar at about (758, 32) on a desktop-size pane), then pick the channel. That always worked.
   Nov 7 run (focused pane): execCommand worked; after "Select files" the date input in the open calendar has no offsetParent, so find it
   with `[...document.querySelectorAll('input')].filter(i=>/202\d/.test(i.value))` (no visibility filter), focus+select, type, Enter.

## Animal library
Drawn: giraffe, penguin, elephant, lion, zebra, hippo, monkey, flamingo, kangaroo, octopus,
sea turtle, polar bear, owl, panda, koala, sloth, red panda, meerkat, sea otter, gorilla, rhino, harbor seal, camel, ostrich.
Fact-highlight variants (Shorts): `gorillanose` (ring on nose), `rhinoears` (sound waves at ears).
Next to draw: tiger (gentle), peacock, armadillo, toucan, chameleon, bison.
Episodes made: ep01 savanna, ep02 ocean & ice, ep03 treetops, ep04 amazing animal bodies, ep05 baby animals, ep06 sunny desert (camel, meerkat, ostrich, kangaroo, lion).
Shorts made: panda, kangaroo, sloth, zebra, hippo, lion, flamingo, polar bear, turtle, octopus, monkey, koala, red panda, owl, meerkat, sea otter, camel, gorilla, ostrich, rhino.
Note: the seal pup (`#fx` in SEAL) sits partly past x 1080, so it suits episodes; reposition it before using it in a Short. SLOTH now also has a baby sloth in `#fx2`.

## Schedule so far
See `studio/upload_plan.json`.

## Sister channels (same engine, pick with `CHANNEL=space|dino|wild`)
Settings live in `studio/channel.py`. Each channel keeps the same safety rules and its own art, so no
video is reused across channels. New channels follow the network ramp in `docs/CHANNELS.md` (week 1:
1 Short/day + an episode every 2 days; week 2: 2 Shorts + 1 episode daily; week 3: 3 + 1; week 4 on: 4 + 1).
Never start a new channel at full speed. Keep 2 hours between uploads on one channel.
Slot offsets so channels don't post at the same minute: Space +50 min, Dino +60, Wild +70
(on the network's Shorts 07:30 / 11:30 / 15:30 / 18:30 and episode 13:30 ET slots).
Handles: @SpaceKidsAcademy and @DinoWorldKids belong to other people; use the HQ versions.
Writing voice for these three channels: `docs/voice.md`.

| Channel | Host | Voice | Art | Shorts / episodes | Repo folder |
|---|---|---|---|---|---|
| Space Kids Academy | Nova the robot | af_nova | `art_space.py` | `shorts_space.json`, `eps/sp_*.json` | `space/` |
| Dino World Kids | Dash the baby dino | af_sky | `art_dino.py` | `shorts_dino.json`, `eps/dn_*.json` | `dino/` |
| WildKids Discovery | Pip the mouse explorer | bf_emma | `art_wild.py` | `shorts_wild.json`, `eps/wk_*.json` | `wild/` |

Build: `CHANNEL=dino SUBDIR=dino bash night.sh dn_trex dn_ep01_dinos` (anything with `ep0` goes to long.py).
Brand assets: `python3 brand2.py` writes `brand/<channel>/banner, avatar, thumb_<episode>` HTML (screenshot to PNG).
Fact sources: NASA (space); Natural History Museum London and Smithsonian NMNH (dinosaurs);
Smithsonian, NHM and USDA (bugs). Dino scripts say "scientists think" for anything still debated,
and remind kids that birds are living dinosaurs. Bug scripts end with "Be gentle with every bug."

Drawn so far. Space: Mercury, Venus, Moon, Mars, Jupiter, Saturn, Sun. Dino: T. rex, Triceratops,
Stegosaurus, Brachiosaurus, Pteranodon. Wild: ladybug, honeybee, butterfly, ant, snail.
Next ideas. Space: Uranus, Neptune, comets, astronauts, rockets. Dino: Ankylosaurus, Velociraptor
(feathers!), Parasaurolophus, Diplodocus, Spinosaurus. Wild: firefly, grasshopper, caterpillar, dragonfly, worm.

## Upload limit (learned Nov 3, 2026)
- Phone-unverified channels hit "Daily upload limit reached" — and the cap is **account-wide** across all Brand Accounts (~20 uploads in 24h hit it).
- A blocked upload saves nothing (no draft). Window is rolling 24h from each upload.
- Fix: phone-verify each channel at youtube.com/verify (also unlocks custom thumbnails). Until then, spread uploads ≤ ~20/day and upload the soonest slots first.
- Render queue: `studio/queue.txt` + `studio/runq.sh` — each run pops one chunk (<2h) and logs to night_q.log.
- Container clock is America/New_York.

## Upload cap (Nov 3, 2026)
- Hard cap: **max 15 uploads per morning run** across the 5 new kids channels (YouTube allows ~20 per rolling 24h account-wide; the Animated Zoo nightly batch needs the rest).
- Soonest slots first; anything over the cap waits for the next day's run (plans are scheduled ahead, so nothing airs late).
- Descriptions: first 2 lines = searchable phrase + subjects (yt-seo query test); titles ≤ 60 chars (yt-package).

## Duplicate guard (Nov 4, 2026)
- Before uploading on a channel, check its Studio Shorts/Videos tabs (or the Command Center status) as well as the plan file: Nov 3 scheduled all 5 Tiny Truck Town Shorts without marking the plan, and the Nov 4 run re-uploaded tt_firetruck. The duplicate (1VDyCj71-hA) was set to Private; delete it in Studio when convenient.
- After switching channels, the first Studio load returns 403 "Oops"; just load it again (sometimes 2-3 times).

## Strategy change: episodes only (Nov 4, 2026, Noelson's call)
- **No more Shorts** on the 5 kids channels (Tiny Truck Town, Bloop's Color Lab, Fruity Friends, Moonbeam Bedtime, Gizmo Explains).
  The 15 Shorts already scheduled in Studio stay and air as planned; every other unposted Short is marked `"status": "dropped"` in the old plans — never upload those.
- **One episode per channel per day** at each channel's slot: Truck 1:40 PM, Bloop 1:50 PM, Gizmo 2:10 PM, Fruity 2:20 PM, Moonbeam 7:00 PM ET.
- The only plan to upload from is `studio/upload_plan_episodes.json` (sorted by date). Stock runs through Nov 15.
- Upload budget: **5 uploads per morning run** (one per channel, the soonest `to_upload` episode for each). Never more. That keeps the account far under YouTube's ~20/24h cap with room for The Animated Zoo.
- The render queue holds episodes only (`studio/queue.txt`); Shorts generators are retired for these channels.

## Strategy change 2: Blender 3D sing-alongs only (Nov 4, 2026, 10:30 AM)
- **All 2D production is stopped.** Every unposted 2D episode is `"status": "paused_2d"`; never upload those. Render queue is empty.
- From now on every video is a **Blender 3D**, informational **sing-along** episode built to go viral. One per channel per day once the pipeline is producing.
- Rendering happens on Noelson's PC (RTX 4060 Ti) through the ZooBlender render worker. Jobs go into Documents\ZooBlender\jobs and finished videos land in Documents\ZooBlender\out.
- Only upload from `studio/upload_plan_3d.json`. Until it has `to_upload` entries, the morning run uploads nothing and only checks analytics.

## 3D pipeline location (Nov 4, 2026)
- Code: `studio/zoo3d/` (engine.py, lib.py, chars/, sets/, songs/, jobs/, finish.py, worker.py, setup.sh) and `studio/sing/sing.py`.
- Daily runbook: `studio/zoo3d/DAILY_3D.md`. Contract: `studio/zoo3d/API.md`. Viral rules: `docs/STRATEGY_3D.md`.
- Episode 1 for all six channels: tt3d_ep01 (Fire Truck Song), bl3d_ep01 (Colors Song), fr3d_ep01 (Yummy Fruits Song),
  mb3d_ep01 (Time for Bed, Sleepyhead), gz3d_ep01 (The Planets Song), zoo3d_ep01 (Savanna Animals Song).
- PC worker: Documents\ZooBlender\START_RENDER_WORKER.bat runs zoo3d\worker.py inside Blender 5.4 (portable copy in Downloads),
  renders EEVEE frames, and assembles the MP4 with ffmpeg. Its log is worker.log and its status is status.txt.

## Views check recipe (Nov 5, 2026)
- Per channel: switch with youtube.com/channel_switcher, then open
  `studio.youtube.com/channel/<id>/analytics/tab-content/period-default/explore?entity_type=CHANNEL&entity_id=<id>&time_period=lifetime&explore_type=TABLE_AND_CHART&metric=VIEWS&granularity=DAY&t_metrics=VIEWS&t_metrics=VIDEO_THUMBNAIL_IMPRESSIONS&t_metrics=VIDEO_THUMBNAIL_IMPRESSIONS_VTR&t_metrics=AVERAGE_WATCH_TIME&t_metrics=AVERAGE_WATCH_PERCENTAGE&t_metrics=RATINGS_LIKES&dimension=VIDEO&o_column=VIEWS&o_direction=ANALYTICS_ORDER_DIRECTION_DESC`
  (reload once or twice on "Oops"), and read the `yta-explore-table-row` cells. The views cell has the share glued on ("35748.3%" = 357 views, 48.3%).
- In the hidden browser pane the channel switcher list doesn't render until a screenshot is taken; take one, then click the
  `ytd-account-item-renderer` by script. Reset the 800x892 viewport emulation to desktop before switching, or the switcher stays blank.

## Video quality standard (Nov 6, 2026, Noelson: "make the upscaling standard for every video")
EVERY episode published from now on is 4K. No exceptions, no 1080p uploads.
1. Render: Blender EEVEE at native 1920x1080, every frame (job "res": "1920x1080", "step": 1). align.py sets these by default.
2. Finish: `studio/zoo3d/finish.py` ALWAYS upscales to 3840x2160 (lanczos + light unsharp), burns the karaoke lyrics at 4K,
   and encodes AV1 10-bit (SVT-AV1, tune VQ) with the bitrate sized to land under 100 MB (GitHub raw limit), AAC 192k audio.
3. Quality gate (built into finish.py): the output must probe 3840x2160 and be under 100 MB, or finish.py exits with an error
   and the episode must NOT be uploaded. The old 1080p --hd path is disabled.
4. Upload: in YouTube Studio the uploader should see "4K" processing; YouTube serves 2160p/1440p/VP9-AV1 streams for 4K uploads.
5. Thumbnails stay 1280x720 PNG (YouTube's thumbnail spec).
Episodes uploaded before this rule (Nov 5–6 batch, 1080p H.264) stay as they are unless Noelson asks to replace them.

## Schedule buffer rule (Noelson, Nov 8, 2026) — the schedule is ALWAYS filled
- Every channel keeps at least 3 days of episodes uploaded and scheduled in YouTube Studio ahead of today. Every production check uploads the soonest `to_upload` entries (within the ~20/24h account cap) until that buffer is met.
- Format changes never empty a slot. New formats (2D/3D hybrid, new worlds, lessons) are tested on extra renders only; the classic 3D sing-along keeps rendering daily as the default. If a new-format episode is held or rejected, a classic episode takes that date (as zoo3d_ep06c did for Nov 11).
- If a render fails or its timing is broken, re-render it or fill the slot with the next finished episode for that channel. A missing slot is worse than a late fix.

## Packaging rules (yt-package check, Nov 9, 2026)
- Thumbnail text: 3 words max and it must NOT repeat the title's words (the title says the topic, the thumbnail adds the hook: "ALL RED!", "STICK OR NOT?", "1 TO 10!"). Set `meta.thumb_text` that way in every new song spec; lint with `python3 /root/.claude/skills/yt-package/title.py --title "..." --thumb "..."`.
- Custom thumbnails only show on Zoo, Bloop and Gizmo (phone-verified). To redo a thumbnail after finishing: `studio/zoo3d/rethumb.py` (crops out the burned-in lyrics).
- Before every finish: `studio/zoo3d/check_timing.py <timing.json> <words_tx.json>`; skipped verses or garbled/wrong-fact singing → rebuild timing or re-sing; never publish a wrong fact.

## Run notes (Nov 9, 2026)
- `fetch(raw).blob()` on a 90 MB MP4 sometimes throws "Failed to fetch" in the hidden pane; reading `r.body.getReader()` chunks into a File worked every time.
- Install the `HTMLInputElement.prototype.click` intercept BEFORE clicking "Select files", and make it swallow every file-input click, so a failed fetch never opens a native picker on the PC.
- Studio avatar menu > Switch account: the submenu opens slowly; wait ~2 s and screenshot before clicking a channel, or the click lands on the account under the cursor (it switched to Rainy Window Dog TV twice).
- The Schedule button usually needs two real clicks at (720, 535) in an 800x600 frame (first one blurs the time field). Confirm via the "Video processing ... set to public on <date> at <time>" dialog.

## Zoo Shorts test (Noelson approved Nov 9, 2026)
- The Nov 4 "no Shorts" rule is lifted for **The Animated Zoo only**, as a test after "Why Are Flamingos Pink?" went 85 -> 1,825 views in a day.
- One Short a day at **11:00 AM ET**, made from finished 3D songs: `studio/zoo3d/make_short.sh <song.mp4> <start> <end> "<LINE1>" "<LINE2>" shorts3d/<id>.mp4`
  (vertical 1080x1920, blurred background, 4:3 song crop with the burned lyrics, question title on top, loudness -16 LUFS). Find clean cut points by OCR'ing the
  burned lyrics (1 fps strips + tesseract) because job timing files don't match the published edit.
- Pick one animal + one true fact or sound per Short, 13-20 s, title "What/Why ... ? <Verb> Along with Milo!" (60 chars max). Made for kids, scheduled, never published now.
  Studio preselects PUBLIC for Shorts: always open Schedule and confirm the button reads "Schedule" before clicking it.
- Plan file: `studio/upload_plan_shorts_zoo.json`. These count toward the account's ~20 uploads/24h, so they come after the 6 daily episodes.
- Tiny Truck Town duplicate 1VDyCj71-hA was deleted Nov 9 (Noelson approved).

## Nov 13, 2026 run notes
- **Missed runs:** no morning runs happened Nov 10-12, so Truck/Fruity/Moonbeam slots on those days stayed empty. Backlogs were re-dated to one per day
  from Nov 14 (`planned_date` keeps the old date). If a run is missed again, upload the soonest `to_upload` per channel on the next free day.
- **Holds:** `"status": "hold_fact_check"` in upload_plan_3d.json means never upload until fixed (zoo3d_ep08: hippo "purple" line).
- **Upload recipe that worked (PC browser pane, hidden):** Studio tab (not fronted is fine for script steps) -> `?d=ud` -> one script that fetches the plan
  JSON from raw GitHub, arms the MP4, clicks `#select-files-button`, fills title/description (execCommand with textContent fallback), ticks made for kids.
  Thumbnail (verified channels): arm the PNG, then scroll `ytcp-thumbnail-uploader` into view; it has zero size until the video finishes uploading, so
  scroll the dialog once with the mouse and retry, then real-click "Upload file" at about (122, 328) in an 800x600 view and check for a `data:` img.
  Then Next x3 by script, expand Schedule, real-click the date box (144, 388), focus+select the date input by script, type "Nov 13, 2026" + Enter,
  focus+select the time input, type "1:40 PM" + Enter, read both back, real-click Schedule (720, 535).
- **Channel switch:** youtube.com/channel_switcher, take a screenshot (renders the list), click the `ytd-account-item-renderer` by script, then load
  Studio twice (first load is a 403 "Oops").
- **Google Vids:** see docs/GOOGLE_VIDS.md. Noelson's PC browser pane is signed in to vids.google.com. Free plan = about 10 AI clips a month.
- **Zoo-only mode (Nov 13, evening):** other 5 channels paused (plan status "paused_channel").
- **PC render state (Nov 13):** zoo3d_ep11-13 (v1 songs) are already RENDERED in Documents\ZooBlender\out (since Nov 10) and only need
  finish.py (4K) + upload: Zoo stock for Nov 15-17. Note: the cloud box has 2 cores, so a full 4K finish takes about an hour per episode;
  do one per run. zoo3d_ep14-16 (songs v2 + editing v2) were copied to ZooBlender\jobs for the worker to make songs; next runs build
  timing/job files and queue the renders. ZooBlender\zoo3d\engine.py now = repo engine.py (PC version merged with the v2 cut logic).
