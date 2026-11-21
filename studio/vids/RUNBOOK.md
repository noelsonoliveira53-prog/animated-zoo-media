# Vids production runbook (one episode)

Browser: the Claude browser pane on Noelson's PC (signed in to Google with the AI Pro plan). Vids = docs.google.com/videos.

## Variety rule (Nov 13): no two episodes look alike
Every Vids episode (and every hook) needs its own places and cast: run `python3 studio/zoo3d/variety.py suggest`, use 3-5
different settings across the clips (never the same background twice in a row), and never copy the look of a recent episode,
even if YouTube Studio suggests that topic. Record the episode in studio/zoo3d/variety_ledger.json.

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

## 5. Export + finish (no clicks from Noelson, ever)
File -> Download -> MP4 (1080p if offered). **Never wait for, or ask Noelson to answer, the browser's save prompt.**
The pane writes the whole video to `~/Downloads/<uuid>.tmp` (or `.crdownload`) before the prompt is answered. So:
1. Note the time, click Download, wait about 30-60 s (Vids shows "Preparing download" then finishes).
2. `device_list_dir` on the Downloads folder; take the newest `*.mp4`, `*.tmp` or `*.crdownload` modified after step 1
   (size stops growing between two listings 10 s apart).
3. `device_stage_files` it, then `bash studio/vids/pick_download.sh <staged> <scratch>/hook.mp4 9` (checks duration and a
   full decode). NOT_READY: wait 20 s, re-stage, retry (3 tries).
4. Fallback if nothing shows in Downloads: File -> Export to Drive, then Google Drive `search_files` for the title and
   `download_file_content` (works up to 10 MB; a 10 s 720p hook is about 3-6 MB).
The leftover prompt on the PC can be ignored or closed; it does not block anything.
Then in the cloud: run
`python3 studio/zoo3d/finish.py <mp4> --vids studio/vids/eps/<id>.json` (4K upscale + <100 MB gate) or, until that flag
exists, `ffmpeg` lanczos to 3840x2160 + SVT-AV1 sized under 100 MB, copy into the channel folder, add the plan entry
(`"format": "vids_full"`, status to_upload) to studio/upload_plan_3d.json, commit, push.

## 6. Schedule
Upload with the PLAYBOOK.md Studio recipe on the channel's next free slot. Mark scheduled + video id.

## 7. Report usage
Write `usage` into the spec: songs, clips, images, retries, minutes spent. Add a row to docs/GOOGLE_VIDS.md "Credit log".

## Hybrid hook (daily Zoo method)
See docs/GOOGLE_VIDS.md "Hybrid". 1 Animate clip (10 s) per Blender episode, spliced with studio/vids/hybrid_splice.sh. No Lyria.
