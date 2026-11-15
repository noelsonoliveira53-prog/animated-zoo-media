# The Animated Zoo: production repo

Full process: `docs/DAILY_RUN.md` (daily run, quality loop, posting grid). Run notes: `PLAYBOOK.md`. Open defects: `docs/IMPROVE.md`.

## Working preferences

Learned from the owner's corrections (Nov 14-15, 2026). One rule per topic; replace a rule instead of adding a contradicting one.

- Report only what exists and was checked; say what was not checked; never present an estimate as a fact.
- Deliver finished files to look at, not explanations of what will be done.
- Teaching lessons are at least 5:00 long (6:30 at most), built from three parts of 85-95 s; each part is cut whole into one Short of about a minute and a half.
- Shorts come only from teaching lessons, never from songs. Songs have no minimum length: each is as long as it needs.
- Lessons are interactive: questions with answer signs and thinking time, on-screen examples of the exact thing being discussed, every word in sync with the voice. Never just a character moving to narration.
- Render everything in native 4K.
- Every video and every Short gets its own custom thumbnail that shows the example, with 3 words at most and none of the title's words.
- Daily grid (ET): lessons 5:30 AM, 9:30 AM, 1:30 PM, 5:30 PM; Shorts 7:30 AM, 11:30 AM, 7:30 PM; song 3:30 PM. Always schedule, never publish immediately.
- Nothing in a new format is uploaded until the owner has watched one full video of it and approved it.
- Before rendering, look at test stills of every example, every answer sign and every group scene: no character stands inside another, nothing is cut by the frame or by the Short's crop, each example is the right size next to the animal.
- After rendering, look at frames of the finished video, of every Short and of every thumbnail before sending or uploading anything.
- Read every fact at its source on the day the script is written; if the source cannot be read, take the line out.
- Log every defect in `docs/IMPROVE.md` the same day and name it as fixed in the next video's spec; a defect counts as fixed only after a frame shows it fixed.
- When the owner says a scheduled or published video is wrong: set it to Private (do not delete), fix the cause in the engine, check every other video for the same cause, re-render, upload the fixed one on the same slot.
- Never run `git pull`, `git stash` or a rebase while an encode is writing a file inside the repo.
