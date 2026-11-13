# Google Vids pipeline (started Nov 13, 2026, Noelson: "Blender is taking too long")

Goal: make the daily sing-along episodes faster by letting Claude build them in **Google Vids** (vids.google.com)
instead of rendering every frame in Blender on the PC. Blender stays as the fallback until a Vids episode passes review.

## What the reference video teaches
"Claude (Free Plan) + Google Vids = Full Stickman Animations on Autopilot" (Jacksons AI, 18 min).
- **Agentic method:** Claude desktop app, open its built-in browser (globe icon), go to vids.google.com, the human signs in
  (Claude never types passwords), then paste a "master prompt" with three inputs: topic, duration, aspect ratio.
  Claude writes the story, generates every scene in Vids, adds the voiceover and edits the whole video hands-free.
- **Manual method:** a chatbot writes scene-by-scene prompts and narration, a video tool animates each scene,
  clips are added one by one, and the voiceover is generated in chunks per clip (whole-script voiceovers glitch).
- Topics are curiosity questions ("Why were ancient humans scared of the dark?"). Same idea as our best titles
  ("Why Are Flamingos Pink?", "Where Is My Mama?").

## What we verified on Noelson's PC today (Nov 13)
- The PC browser pane is already signed in to Google Vids (no password step needed).
- Vids editor side panel: **AI Video** (Create / Edit / Animate / Extend, up to 3 "ingredient" images for consistent
  characters, model "Omni", 720p, landscape or portrait, up to 10 s per clip, Upscale button), Avatar, Voiceover, Music,
  Image, Uploads (Drive/Photos), Stock, Captions, Text, Templates. Exports can go straight to YouTube (private by default).
- **Test clip made:** "Vids pilot - Zoo test clip (Nov 13)" in Noelson's Drive. Prompt: a round blue bluebird hopping onto
  a log on a sunny savanna with a smiling giraffe, soft 3D cartoon. Generated in about 90 s, 720p, 10 s, good kid-friendly
  look. The bird only appears at the edge, so prompts must say where the hero stands ("center frame") and we should pass
  a Milo render as an ingredient image to keep him on-model.

## The hard limit: AI video clips per month
- Google's April 2026 announcement: **free personal accounts get 10 Veo/AI video generations a month** (8-10 s each).
  Google AI Ultra gets up to 1,000 a month. Pro's cap isn't published.
- A 2:30 song fully covered by AI clips needs about 15-19 clips. Six channels a day = about 100 clips a day, ~3,000 a month.
  So **full AI-clip episodes can't run on the free plan**, and even Ultra covers only about one channel.

## The plan: "Vids hybrid" episodes (fast, fits the quota)
Each episode keeps our existing song (lyrics + audio from `studio/sing/`) and builds the picture in Vids:
1. **Hook clip (AI Video, 1 per episode):** the first 0-10 s, the title payoff (a baby animal finds mama, Bloop turns yellow,
   Gizmo makes a rainbow). This is where retention is lost, so the one premium clip goes here.
2. **Scenes from stills:** one still per sung line, from our Blender character renders (a single frame renders in seconds,
   not the whole video) or Vids "Image", placed full-frame with Vids motion (pan/zoom, pop-in text for the counted word/color).
3. **Lyrics as captions** (Vids Captions/Text), the song as the audio track (Uploads).
4. **Final chorus clip (optional 2nd AI clip)** when quota allows.
5. Export 1080p MP4 to Drive, run `finish.py` for the 4K standard (it already upscales 1080p to 2160p and checks <100 MB),
   commit to the repo, add to `studio/upload_plan_3d.json` with `"format": "vids_hybrid"`, and schedule in Studio as usual.

Quota math (free plan, 10 clips): about 10 hybrid episodes a month. Enough for a **pilot on The Animated Zoo** (most reach),
not for the whole network. Network-wide Vids needs a paid Google AI plan (Noelson's call, see the decision below).

## Pilot schedule
- Day 1 (Nov 14 morning run): build one Zoo hybrid episode in Vids, "Where Is Baby Penguin? Ocean Babies Song" (the
  "Where Is My Mama?" pattern, our best long-form ever: 3,788 views on 119k impressions). Target slot: Nov 15 4:00 PM
  (Zoo stock runs out after zoo3d_ep10 on Nov 14; zoo3d_ep08 is on fact-check hold).
- Review gate before upload: on-model characters, no text glitches, facts true, calm and safe (kids-safety rules in
  PLAYBOOK.md), first payoff by 0:05, 4K after finish.py.
- Compare its retention and CTR with the Blender songs for 3 days, then decide whether to roll out.

## Rules that do not change
- Claude never types Noelson's password or creates accounts. If Vids ever asks to sign in, stop and ask Noelson.
- Original characters only (Milo, Bolt, Bloop, Pipkiko, Luna, Gizmo). Never prompt for known characters, brands or "in the
  style of" a studio.
- Made for kids, scheduled (never published immediately), titles 60 characters or less, first 2 description lines searchable.
- Vids "Share to YouTube" posts as Private to whichever channel is picked; we don't use it. We download the MP4 and use the
  Studio scheduling recipe, so the schedule, thumbnails and duplicate checks stay in one place.
- YouTube "altered or synthetic content" label: not needed for clearly cartoon, non-realistic animation; tick it if a clip ever
  looks like a real place, person or event.

## Decision for Noelson
1. Free plan = about 10 AI clips a month: enough for the Zoo pilot only.
2. To run Vids on all six channels, a paid Google AI plan with a high Vids clip allowance is needed (Ultra lists 1,000/month).
   Check the current price on Google's plans page before buying. Nothing has been bought.
3. Until then, Blender keeps rendering the other five channels, and the hybrid method cuts Blender time by rendering stills
   instead of full animations if you want that switched on.

## Update Nov 13 (afternoon): Noelson already has Google AI Pro ($19.99/mo)
With Pro, Vids shows **Music = "Generate a song" (Lyria 3.5)** with own lyrics, full-length songs and vocals. So the whole episode
can be made inside Vids: song + AI clips + captions. Pilot `zoov_ep01` "Where Is Baby Penguin?" was built fully in Vids
(spec: studio/vids/eps/zoov_ep01.json, agent: .claude/agents/vids-producer.md, steps: studio/vids/RUNBOOK.md).

### Credit log
| Date | Episode | Songs (blocked) | AI clips | Length | Notes |
|---|---|---|---|---|---|
| Nov 13 | Vids pilot test | 0 | 1 | 0:10 | first test clip |
| Nov 13 | zoov_ep01 Where Is Baby Penguin? | 1 (1) | 13 | 2:10 | 5 clips generated in parallel; no clip refused |

Lessons from the first episode
- Lyria refuses style text that says "preschool kids" or "kids chorus". Say "sing-along pop song for families" and "group chorus".
- Clip prompts: put the look + full character descriptions in every prompt; "all characters fully visible and centered" fixes Milo
  being cut off. Penguins came out consistent across clips without reference images.
- Insert clips with: Ctrl+M (new blank scene) then the card's "Insert" button. Clicking Insert while a clip is selected says
  "Replace"; clicking an already inserted card opens "Insert in new scene" (makes duplicates).
- AI clips carry their own sound: mute every Video track (Sound > All tracks > expand each Video > Mute), keep the song.
- Captions panel > "All scenes" + yellow word-emphasis style gives karaoke lyrics automatically.
- Export to YouTube uploads as Private to the channel active in YouTube; then schedule it in Studio (title, description, made for kids).
- Output is 1080p from 720p clips, so this episode is an exception to the 4K rule (decision for Noelson).
- Pro plan's monthly clip allowance is still unknown; no limit message appeared after 14 clips. Watch for a limit warning on the next episodes.
| Nov 13 | zoo3d_ep10h hybrid hook (Animate from Blender frame) | 0 | 1 | 0:10 | spliced onto the 4K Blender episode |

## Hybrid "Vids hook + Blender" (tested Nov 13; the daily Zoo method from Nov 14)
Why: the first 10 s is where viewers leave (avg view 0:20-0:34). One Vids clip makes that opening more alive, while Blender
keeps the rest on-model, in 4K, with our ACE-Step song and karaoke lyrics. It costs 10 s of Vids allowance per episode:
30 episodes a month = 300 s, which fits AI Pro (500 s) with 200 s spare for tests. No Lyria songs needed.
Recipe (studio/vids/RUNBOOK.md, section "Hybrid hook"):
1. Clean start frame from the finished Blender MP4: crop off the lyric band, keep 16:9, scale to 1920x1080
   (`ffmpeg -ss 0.4 -i ep.mp4 -frames:v 1 -vf "crop=ih*0.84*16/9:ih*0.84:(iw-ih*0.84*16/9)/2:0,scale=1920:1080" start.png`), push it.
2. Vids > AI Video > Animate > Add image (arm the PNG from raw GitHub with the file-input trick), prompt: "Keep this exact 3D cartoon
   style, characters, colors and background..." + the action of the first sung lines. 10 s, 720p. Insert, File > Download > MP4.
3. Stage it from Downloads with no click (Noelson asked Nov 13: "this needs to be automated without me clicking"): the pane
   holds the finished video as `~/Downloads/<uuid>.tmp` while its save prompt waits, so stage the newest .tmp/.mp4 and verify it
   with `studio/vids/pick_download.sh` (RUNBOOK step 5; Drive export is the fallback). Then write the hook lyrics (start end text, from the song's first 10 s), then
   `studio/vids/hybrid_splice.sh ep.mp4 hook.mp4 10 lyrics.txt epNNh.mp4` (the Blender MP4 has a keyframe at 10.0 s; the hook is
   upscaled to 4K AV1 and the rest is stream-copied, about 1 minute, result stays under 100 MB).
4. Upload epNNh.mp4 instead of epNN.mp4 (plan `format: 3d_singalong_vids_hook`).
First result: zoo3d_ep10h "Who's Hiding at the Zoo?" -c9dHJ5UOlc, Nov 14 4:00 PM. The Animate clip kept the Blender look
(same Milo, lion, elephant, zebra, hippo, giraffe, set) and the cut at 10 s is seamless.
