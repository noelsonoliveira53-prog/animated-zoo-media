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
