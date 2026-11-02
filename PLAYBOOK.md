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
5. Episodes: also set the thumbnail from `brand/thumb_<id>.png` via `ytcp-thumbnail-uploader input#file-loader`.

## Animal library
Drawn: giraffe, penguin, elephant, lion, zebra, hippo, monkey, flamingo, kangaroo, octopus,
sea turtle, polar bear, owl, panda, koala, sloth. Next to draw: rhino, tiger (gentle), red panda,
meerkat, gorilla, camel, peacock, seal, otter, armadillo, toucan, chameleon, bison, ostrich.

## Schedule so far
See `studio/upload_plan.json`.
