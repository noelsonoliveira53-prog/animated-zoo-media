Update The Animated Zoo production and YouTube publishing workflow to support multiple languages on the existing channel. Do not create separate language channels or upload duplicate videos.

GOAL

Publish each episode once, with multiple selectable audio tracks and localized metadata attached to the same YouTube video.

SUPPORTED LANGUAGES

1. English — original/default language
2. Spanish — neutral Latin American Spanish
3. Portuguese — natural Brazilian Portuguese

PRODUCTION REQUIREMENTS

For every episode:

* Create the original English script.
* Translate and culturally adapt the script into Spanish and Brazilian Portuguese.
* Preserve the story’s meaning, educational lesson, character names, humor, emotional tone, and child-safe vocabulary.
* Make each translated narration approximately the same duration as the English narration.
* Generate natural, expressive, child-friendly narration for all three languages.
* Keep Milo’s voice personality consistent between languages.
* Use the same animation, original music, ambience, and sound effects for every language.
* Never translate character names unless specifically instructed.
* Do not translate songs literally when that produces unnatural lyrics. Adapt them while preserving their meaning, rhythm, and educational purpose.
* Avoid robotic translations and review every script for grammar, pronunciation, age appropriateness, and cultural accuracy.

REQUIRED OUTPUT FILES

Create the following organized structure for each episode:

episode-name/
├── video/
│   └── episode-master-1080p.mp4
├── audio/
│   ├── narration-en.wav
│   ├── narration-es-419.wav
│   └── narration-pt-BR.wav
├── captions/
│   ├── captions-en.srt
│   ├── captions-es-419.srt
│   └── captions-pt-BR.srt
├── metadata/
│   ├── metadata-en.json
│   ├── metadata-es-419.json
│   └── metadata-pt-BR.json
├── thumbnails/
│   ├── thumbnail-en.png
│   ├── thumbnail-es-419.png
│   └── thumbnail-pt-BR.png
└── validation-report.json

YOUTUBE CONFIGURATION

Configure the publishing workflow as follows:

* Use the existing Animated Zoo channel.
* Upload only one master video for each episode.
* Set English as the video’s original language.
* Attach Spanish and Brazilian Portuguese as additional audio tracks to the same video.
* Add localized titles and descriptions for all three languages.
* Upload accurate captions for all three languages.
* Add localized thumbnails when the thumbnail contains written language.
* Use one language-neutral thumbnail when there is no text.
* Set every episode as “Made for Kids.”
* Do not upload three separate copies of the same episode.
* Do not create separate Spanish or Portuguese channels.
* Do not enable automatic publication of unreviewed AI-generated dubs.
* Do not publish, delete, replace, or modify an existing public video without explicit approval.

METADATA REQUIREMENTS

Create natural, search-friendly metadata for each language. Do not simply translate keywords word-for-word.

Each metadata file must contain:

* language
* localized_title
* localized_description
* educational_topic
* parent_summary
* primary_keywords
* secondary_keywords
* hashtags
* playlist
* audience_setting
* original_language
* audio_track_filename
* caption_filename
* thumbnail_filename

Keep titles clear and appealing to parents without clickbait. Do not use misleading educational claims, excessive capitalization, keyword stuffing, or promises that cannot be supported by the episode.

QUALITY VALIDATION

Before marking an episode ready:

* Confirm all narration tracks match the master video timing.
* Confirm there are no clipped sentences or long unintended silences.
* Confirm the music does not overpower narration.
* Confirm Spanish uses neutral Latin American vocabulary.
* Confirm Portuguese uses Brazilian vocabulary and pronunciation.
* Confirm captions are synchronized and correctly encoded.
* Confirm the educational explanation is accurate in all languages.
* Confirm every video is safe and appropriate for toddlers and young children.
* Confirm no copyrighted music, characters, voices, or visual assets are used.
* Confirm the “Made for Kids” audience value is included in the upload configuration.
* Confirm only one YouTube video is created per episode.

ANALYTICS

Extend the admin dashboard to display performance by audio language, including:

* Views
* Watch time
* Average view duration
* Audience retention
* Top countries
* Most-used audio language
* Search traffic by localized title
* Episode performance comparison by language

Track these results so we can determine later whether Spanish or Portuguese has enough demand for a dedicated localized channel.

IMPLEMENTATION PROCESS

1. Inspect the current Animated Zoo codebase and production workflow.
2. Identify the existing rendering, narration, caption, metadata, and YouTube upload components.
3. Present a concise implementation plan before making major architectural changes.
4. Preserve the current English production workflow.
5. Add multilingual support as reusable modules rather than duplicating the entire pipeline.
6. Implement the changes incrementally.
7. Test everything with one complete Milo episode.
8. Produce a dry-run upload manifest showing exactly what would be sent to YouTube.
9. Stop before the public publishing step and request my approval.
10. Document how to add another language in the future without rebuilding the system.

The final system must allow us to produce one Milo episode, render it once, generate three carefully reviewed narration packages, and publish it as one multilingual YouTube video on the existing Animated Zoo channel.