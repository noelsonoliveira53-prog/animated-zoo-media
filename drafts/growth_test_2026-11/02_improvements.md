# 2. Five highest-priority improvements (ranked by expected benefit ÷ production effort)

All of these apply to **new** episodes only. No live title, thumbnail or video is touched.

## 1. Open on the promise, greet after the hook (benefit: high · effort: low, script only)
**Evidence:** every Zoo lesson opens "Hi, friends! I'm Milo the bluebird, and welcome to The Animated Zoo!" (all 9 2D lessons, the 3D lessons).
The four 2D lessons with a retention curve lose 61-68% of viewers by 10 s and keep 18-27% at 30 s (Amazing Animal Bodies 20%, Savanna 18%, Ocean & Ice 26%).

**Before** (Amazing Animal Feet, zool_ep16, public Nov 19): first shot = Milo in the savanna. First line: *"Hello, friends! I am Milo the bluebird."*
Then: *"Today we are learning about amazing animal feet! Paws, claws and toes..."* The first animal question comes at 0:22.

**After** (pilot zool_g01): first shot = a low, close camera on one giant footprint pressed in the sand, Milo hopping in from the left to peer
at it. First line, at 0:00: ***"Look! A giant footprint in the sand! Who made it?"*** then a 1.6 s pause. Milo says his name at 0:09, after
the hook. The first answer signs are on screen by 0:20.

**How we'll know:** % still watching at 10 s and 30 s, compared with the median of the four 2D lessons read today (10 s: 36%, 30 s: 23%).
Helped = 30 s at least 30%.

## 2. Titles: promise first, a question, whole on a phone (benefit: high · effort: low)
**Evidence:** "<Topic> for Kids! Meet 5 Zoo Friends with Milo" titles get 1.4-3.5% CTR; familiar-tune and question titles get 5.5-12.3%
(Head, Shoulders 12.3%, Freeze Dance 8.5%, Milo Had a Zoo 6.1%, Count 10 5.5%), though on small impression counts.
Rule: the promise in the first 40 characters, as a question a child would ask; series name last; no "for Kids!" filler.

| Before (live, not to be edited) | After (for the next episode of that kind) |
|---|---|
| Animal Sounds Song for Kids! Roar, Toot, Neigh with Milo (cut after "Roar, Toot,") | What Does the Elephant Say? Sing With Milo (42) |
| Treetop Animals for Kids! 5 Zoo Friends with Milo | Who Lives at the Top of the Tree? Guess With Milo |
| Amazing Animal Feet! Paws, Claws and Toes for Kids | Whose Feet Are These? Guess With Milo (37) |

**How we'll know:** 7-day CTR against the same format's median (today's table: 2D lessons 2.8%, songs 4.2%; half of those songs have under 600 impressions).

## 3. One-idea thumbnails a pre-reader understands (benefit: medium-high · effort: low-medium)
**Evidence:** two of the top three use the same Milo-and-three-animals picture; Amazing Bodies shows five small animals; the new Feet thumbnail
puts a white bear on white snow. Rule: one big object (the mystery or the animal doing the action), Milo only where he adds meaning (looking,
pointing, guessing), a high-contrast background, at most 1-2 words, none from the title (`thumb.py` already enforces the words).
**Before:** "WHERE IS MY MAMA?" over Milo with lion, giraffe and zebra. **After (for a mama/baby episode):** one baby elephant peeking from behind
a huge grey leg, Milo with his wing at his beak, the word "WHO?".
**How we'll know:** CTR, plus the "stayed to watch" share where Studio shows it.

## 4. A recurring format with a payoff every 90 seconds (benefit: medium-high · effort: medium)
**Evidence:** Where Is My Mama? = 41% of all long-form hours, built as one question answered in every verse. The guessing lessons have the
best CTR (on tiny samples). Two named formats, said in the video and in the title: **Guess With Milo** (a mystery clue, answer signs, the
reveal, then the facts) and **Sing With Milo** (a question chorus, a reveal in every verse). Each episode has its own animals, places and
facts; no footage is reused to fill time.
**How we'll know:** watch hours per episode at 7 days compared with same-length episodes, and returning viewers (Audience tab) for the
series playlist.

## 5. Room to answer, and narration over the music (benefit: medium · effort: low)
**Evidence:** the v3 lessons already pause 4 s after answer-sign questions and 3 s after "Hmm." (measured in zool_ep16's timing). Keep that
in every new lesson and song: a sung question is followed by one silent bar before the reveal line; the music bed stays ducked under every
spoken line (the current setting); no sound effect on a word. Facts are read at their source the same day (the pilot's 14 claims: `pilot/qa.md`).
**How we'll know:** the retention curve should flatten (no drop) across each guess-and-reveal; check the 10-15 s around each reveal.

---
### Changes that would need a settings change (explained only, not done)
- **Fewer, stronger lesson slots** (for example two lessons a day instead of four, so more impressions land on each): changes the daily grid and
  the automation. Not done.
- **Holding the test slots from the automatic builds**: the four builds a day take the next free lesson slots by themselves. To keep a test
  slot free, the owner would mark it in the plan. Until then, the test uses slots the automation does not fill (see `03_test_plan.md`).
