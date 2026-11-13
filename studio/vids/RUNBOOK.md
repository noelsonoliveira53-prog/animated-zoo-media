# Vids production runbook (one episode)

Browser: the Claude browser pane on Noelson's PC (signed in to Google with the AI Pro plan). Vids = docs.google.com/videos.

## 1. Write the spec (cloud)
`studio/vids/eps/<id>.json` (id: zoov_epNN, ttv_epNN, blv_epNN, frv_epNN, mbv_epNN, gzv_epNN). Copy zoov_ep01.json:
song.style, song.lyrics ([Chorus]/[Verse]/[Bridge]/[Final Chorus]/[Outro] tags, about 2:30), facts_checked, look, cast,
15 clips (one per 10 s, each prompt names the characters with the cast descriptions and the action for that lyric),
meta (title, description, tags). Topic and title follow docs/STRATEGY_3D.md. Commit and push (Vids fetches it from raw GitHub
by commit sha).

## 2. Song (Vids Music, Lyria 3.5)
New video: docs.google.com/videos/create, close the start dialog, rename to "<id> <title>". Music panel -> settings: Full, vocals ON.
Focus the textarea `textarea[aria-label^="Describe your song"]`, insert `style + "\n\n" + lyrics` with execCommand insertText,
click Generate (find "Generate"). About 1-3 min. Listen check: insert it, read its length in the timeline.
Usage: +1 song (count retries).

## 3. Clips (AI Video, model Omni, 720p, Landscape, 10 s)
For each clip in order: AI Video panel -> Create, paste the clip prompt prefixed with `look` and the cast lines it uses,
Generate (~90 s each, several can run while you prepare the next), Insert. If a clip has text glitches, extra limbs,
off-model characters or anything scary: Recreate once, otherwise use a calmer prompt. Usage: +1 clip per generation.
Character consistency: from clip 2 on, add the best Milo frame (and mama/baby frames once they exist) as Ingredients.

## 4. Assemble
Clips back to back in lyric order on the timeline; the song as the audio track starting at 0:00; trim the last clip to the
song end. Captions: add the lyric lines as on-screen text per section (big, bottom, high contrast).

## 5. Export + finish
File -> Download -> MP4 (1080p if offered). Then in the cloud: stage it, run
`python3 studio/zoo3d/finish.py <mp4> --vids studio/vids/eps/<id>.json` (4K upscale + <100 MB gate) or, until that flag
exists, `ffmpeg` lanczos to 3840x2160 + SVT-AV1 sized under 100 MB, copy into the channel folder, add the plan entry
(`"format": "vids_full"`, status to_upload) to studio/upload_plan_3d.json, commit, push.

## 6. Schedule
Upload with the PLAYBOOK.md Studio recipe on the channel's next free slot. Mark scheduled + video id.

## 7. Report usage
Write `usage` into the spec: songs, clips, images, retries, minutes spent. Add a row to docs/GOOGLE_VIDS.md "Credit log".
