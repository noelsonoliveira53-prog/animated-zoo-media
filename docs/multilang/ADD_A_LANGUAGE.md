# Adding a language to an episode, or a new language to the channel

The picture is rendered once, in English timing. A language is a voice, a translation file and a run of the package builder. Nothing is rendered again.

## A new language (once)

1. Check that the local voice model has a voice for it: the names in `/root/.cache/hyperframes/tts/voices/voices-v1.0.bin` start with a language letter (`e` Spanish, `p` Brazilian Portuguese, `f` French, `i` Italian, `h` Hindi, `j` Japanese, `z` Mandarin).
2. Measure the voice's median pitch on three sentences and compare it with Milo's English voice (`af_heart`, 195 Hz): `pitch` = 12 x log2(195 / that voice's median), in semitones. Keep `formant` between 1.0 and 1.05.
3. Add one entry to `studio/multilang/languages.json`: the code (BCP-47, as in the file names: `fr`, `es-419`, `pt-BR`), `name`, `youtube` (the language's name in Studio's "Add language" list), `voice`, `tts_lang`, `pitch`, `formant`.
4. Send the owner one minute of that voice before any episode is built with it. Nobody in the build can listen.

## A language for one episode

1. Copy `studio/cartoon/episodes/lang/<episode>.es-419.json` to `<episode>.<code>.json`.
2. `lines`: one line per spoken shot, in the episode's order (the builder refuses a different count). Write for the SLOT, not for the English words: a line may take its English line's time plus the pause after it. Keep the fact, the question and the name; drop an adjective before dropping a fact. Character names stay. Sound words are the language's own (snif, tchibum), written so the voice can say them.
3. `metadata`: title (70 characters at most, asked the way a parent searches in that language, not a word-for-word copy), description, `educational_topic`, `parent_summary`, keywords, hashtags, `thumb_text` (3 words at most, none of that title's words).
4. `translator_notes`: every choice a native reader should look at (regional words avoided, names, sound words).
5. `python3 studio/multilang/build.py <episode> --fit` lists the lines that do not fit. Rewrite those lines shorter. The builder may speak a line up to speed 1.0 (the English is spoken at 0.8); it never cuts a line.
6. `python3 studio/multilang/build.py <episode>` writes `packages/<episode>/` and prints READY or NOT READY. Read `validation-report.json`: every check, and the list of what no machine checked.
7. Send the owner the track to hear, with the picture. A track goes on YouTube only after a human has listened to it.

## Stories with a cast, the main intro, tunes (added Nov 20 2026 with za_ep09, the first adventure in three languages)

- **A voice per character.** A story's characters keep, in every language, their English offsets from Milo (pitch, formant, speed, loudness): `build.voice_for`.
  A character whose English voice is a male voice (Tumble: `am_puck`) takes the language's `voice_m` (`pm_alex`, `em_alex`), brought to the English
  voice's height by `pitch_m` (measured, in `languages.json`) before the character's own offset is added. Each line is made as loud as the same
  character's English line.
- **"=" keeps the English recording.** A line that is only `=` in the adaptation is not spoken again: the English audio is used as it is. Used for the
  main intro's "The Animated Zoo!" (the channel's name; the logo on screen says it in English). The owner decides whether Milo says it in each language.
- **Tunes played by instruments** (a `sing=` shot whose lines are only `~`: the song moments, the main intro's timing shots) are music: they go into every
  language's track unchanged. A sung line with WORDS is still refused (lyrics have to be adapted to the same notes first).
- **The main intro's score** is part of toon.py's own bed, so every language has it without anything being done.
- **English fields the episode file does not carry** (`educational_topic`, `parent_summary`, hashtags): `studio/cartoon/episodes/lang/<episode>.en.json`.
- To hear a language over the picture: `ffmpeg -i cartoon/<id>.mp4 -i packages/<id>/audio/track-<code>.wav -map 0:v -map 1:a -vf scale=1280:-2 -c:v libx264 -preset veryfast -crf 23 -c:a aac <out>.mp4`.

## What the builder keeps the same in every language

The picture, the music and every sound effect: the bed is taken from `toon.py`'s own mix (the report checks that voice + bed reproduces the film's English sound sample for sample), with the music lowered under the ENGLISH lines' positions, so it is the same file in all languages.

## What is not built yet

- Sung lines (`sing=`) in other languages: the builder refuses an episode whose translation has no line for them. The elephant lesson has none. Songs need lyrics adapted to the same notes.
- The picture's own words (caption line, big words, answer signs, the Short's title band) are English. See PLAN.md, decision 1.
- 3D songs and 3D lessons (`studio/zoo3d/`): their voice path is different.
- Putting the files on YouTube: `upload-manifest.json` is a dry run. See PLAN.md, order of work, step 4.
