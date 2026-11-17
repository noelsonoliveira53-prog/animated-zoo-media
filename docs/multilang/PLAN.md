# One video, three languages: plan (Nov 16, 2026)

Owner's brief: Nov 16, 8:46 PM (`docs/multilang/BRIEF.md`). English (original), Spanish es-419, Portuguese pt-BR on ONE video of the existing channel. No language channels, no duplicate uploads, nothing public without the owner's approval.

Status: PLAN. Nothing in the production or upload path has been changed for this yet.

## What exists today (inspected Nov 16)

| Part | Where | Today |
|---|---|---|
| Script and shots | `studio/cartoon/episodes/<id>.py` | English lines inside each shot |
| Narration | `toon.voice_lines` -> `sing.say` (Kokoro, local) | one voice track, English |
| Word timing | `studio/zoo3d/wordsync.py` | English alignment |
| Captions | `Film.captions` in `toon.py` | burned into the picture, English; no .srt files |
| Words in the picture | `words=`, answer `signs`, the Short's title band, closing pill | English |
| Songs and hums | `studio/sing/sing.py` | English voices; hums have no words |
| Metadata | `EP` in the episode + `studio/upload_plan_*.json` | English |
| Thumbnails | `thumb.py` (3 words at most) | English words |
| Upload | Studio in the PC browser, `studio/studio-upload2.js` | one file, title, description, thumbnail, schedule |
| Dashboard | Command Center artifact (collections `videos`, `analytics`, `ops`) | per video, no language split |

Checked today:
- The local voice model has Spanish voices (`ef_dora`, `em_alex`, `em_santa`) and Brazilian Portuguese voices (`pf_dora`, `pm_alex`, `pm_santa`). A test line came out in `es-419` and in `pt-br`. The same sentence took 2.65 s in Spanish and 2.9 s in Portuguese against 1.96 s in English at the same speed, so lines must be written to fit, not only translated. Nobody here can listen: how the two voices pronounce is for a human listener.
- YouTube Help "Add Multi-language features to your videos" (read Nov 16): multi-language audio is for channels with access to Advanced features; Studio > Languages > the video > add a language > Dub > upload an audio-only file about as long as the video > Publish; it works on videos and Shorts; a localized thumbnail is added on the same Languages page; an automatic dub in that language has to be deleted before our own track goes in; Analytics shows views and watch time by audio language. The page says nothing about made-for-kids videos.
- Read in Studio, Nov 16 8:55 PM, nothing changed: Settings > Channel > Feature eligibility shows Advanced features "Enabled". The Languages page of the elephant lesson (made for kids, scheduled) shows "Video language: English", an "Add language" button and a table with the columns Audio, Subtitles, Title & description, Thumbnail; it has no rows, so there is no automatic dub on it. Settings > Upload defaults > Advanced settings shows no automatic-dubbing switch at all (Video language: English).
- NOT checked yet: that an audio file is accepted on a made-for-kids video. That is only known after the first track is put in as a draft, which waits for the owner's yes.

## Design

1. **One picture, three sound tracks.** The picture keeps the English timing (every shot is cut to its English line). Spanish and Portuguese lines are written to fit each shot's time. A new module builds each line with that language's voice, fits it inside its slot (speed 0.85-1.15; a line that still does not fit is rewritten shorter, never cut), and mixes it with the SAME music and sound effects.
2. **Translations are files, not code.** `studio/cartoon/episodes/<id>.es-419.json` and `<id>.pt-BR.json`: every line, every song line, the metadata and the thumbnail words. Character names stay. Songs are adapted to the same notes (same number of syllables), not translated word for word.
3. **Captions become real caption files** (`captions-<lang>.srt`, UTF-8) made from each language's own word timing.
4. **Package builder** `studio/multilang/package.py <id>` writes the folder the brief asks for and `validation-report.json`.
5. **Upload**: one video as today, then the Languages page for each language: title, description, audio track, captions, thumbnail. A dry-run manifest (`upload-manifest.json`) lists every field and file first. The step that makes a track or a video public is never clicked without the owner's yes.
6. **Dashboard**: the Command Center gets a Languages view per video: views, watch time, average view duration by audio language, top countries, search terms that match a localized title. A number Studio does not show is written as "not available", never estimated.
7. **Adding a language later** = one voice entry in `studio/multilang/languages.json` + one translation file per episode. `docs/multilang/ADD_A_LANGUAGE.md` will say this step by step.

## Three decisions that are the owner's

1. **Words in the picture.** Today the picture carries English words: the burned-in caption line, the big words ("FAT!", "YOUR TURN!"), the answer signs, the Short's title band. With one picture they stay English under a Spanish or Portuguese voice. Proposal: from the multilingual test episode on, the master has no burned-in caption line (captions come from the three caption files), big words are numbers and symbols only, and answer signs are pictures. This changes the approved cartoon format, so one full video is shown to the owner first.
2. **Master size.** The brief names `episode-master-1080p.mp4`; the standing rule (Nov 16) is 4K minimum and `toon.py` refuses anything else. Kept: 4K (`episode-master-2160p.mp4`) unless the owner says 1080p.
3. **A listener.** Every Spanish and Portuguese track needs one human listen for pronunciation before it goes on a video. The checks here are written text, timing and loudness only.

## Order of work

1. Done Nov 16: read in Studio the Languages page of one scheduled video, feature eligibility and the upload defaults (read only).
2. `studio/multilang/`: languages.json, line fitting, stems (voice / music + effects), track mixer, .srt writer, package builder, validation.
3. Test episode: the elephant lesson `zc_ep02` (scheduled Nov 19, not public): translations, three tracks, captions, metadata, thumbnails, validation report, dry-run manifest.
4. Stop. Send the owner the three tracks to hear and the manifest. Nothing is attached to the video before his yes.
5. After approval: attach, read back, then the dashboard view and the 3D songs and lessons.

## File names

The brief's `audio/narration-<lang>.wav` is kept as the voice alone. YouTube replaces the whole sound of the video with an audio track, so the file that is uploaded is `audio/track-<lang>.wav` (voice + the same music and effects). Both are in the package.
