# The Animated Zoo: production playbook

Channel: **The Animated Zoo** (@TheAnimatedZoo, UC1YuY8nqnViTtm85qxE_M1w). Host: **Milo the bluebird**.
Audience: kids 3–8. Channel and every video are set **made for kids**.

## Posting cadence (keep to this)
- **Shorts:** 1 per day at **11:00 AM ET**.
- **5-minute episodes:** Mon / Wed / Fri at **4:00 PM ET**.
- Never more than 2 uploads go public per day. Mass-posting near-identical AI videos can be
  flagged as "repetitious content", which is the main risk to a new kids channel.
- Every upload is scheduled in advance in Studio, so posting doesn't need the PC to be on.

## Kids-safety rules (non-negotiable)
- Facts only from zoo / science sources (San Diego Zoo, Smithsonian's National Zoo, NOAA, NASA,
  Natural History Museum). If unsure, cut the line. Hedge guesses ("scientists think").
- No scary words (kill, attack, deadly, blood-and-guts, monster), no predation detail,
  no brands or toys, no "subscribe" nagging, no requests for kids' names, ages or comments.
- Calm pacing (TTS speed 0.85 for long-form), music ducked under voice, loudness -16 LUFS.
- All art is original (`studio/art.py`, `studio/art2.py`). Never draw known characters.
- Every video ends with the kindness rule: "Be kind to every animal."

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
4. Fill title + description, tick made-for-kids, Next ×3, expand **Schedule**, open the date
   picker, wait for `.calendar-day` cells, click the target day, type the time, then **Schedule**.
5. Episodes: also set the thumbnail from `brand/thumb_<id>.png` via `ytcp-thumbnail-uploader input#file-loader`.

## Animal library
Drawn: giraffe, penguin, elephant, lion, zebra, hippo, monkey, flamingo, kangaroo, octopus,
sea turtle, polar bear, owl, panda, koala, sloth. Next to draw: rhino, tiger (gentle), red panda,
meerkat, gorilla, camel, peacock, seal, otter, armadillo, toucan, chameleon, bison, ostrich.

## Schedule so far
See `studio/upload_plan.json`.
