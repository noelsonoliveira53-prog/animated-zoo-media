# 3. Two-week content test (inside the existing schedule)

## Test window and slots
The current rules (docs/GROWTH_90D.md, Nov 18) allow **one 3D upload a day, in the 3:30 PM slot**, and stopped new 3D lessons. The grid
and those settings stay as they are. All four test episodes use the **3:30 PM slot**, the day's one 3D upload, which also keeps the time
of day constant across the test:

| Date (ET) | Slot | Now planned there | Test episode |
|---|---|---|---|
| Sun Nov 23 | 3:30 PM (3D) | nothing yet in the plan | **Sing With Milo #1**: Crunch, Crunch! Who's Munching? |
| Tue Nov 25 | 3:30 PM (3D) | nothing yet | **Guess With Milo #1 (pilot)**: Whose Feet Are These? |
| Thu Nov 27 | 3:30 PM (3D) | nothing yet | **Sing With Milo #2**: Whose Baby Is This? |
| Sat Nov 29 | 3:30 PM (3D) | nothing yet | **Guess With Milo #2**: Whose Ears Are These? |

Every other slot and setting stays as it is. The 3:30 PM slots on the other days keep their normal songs. Nov 20 and 21 already have songs
scheduled, which is why the test starts Nov 23. The day-7 readings fall on Nov 30, Dec 2, Dec 4 and Dec 6.

**Settings notes (explained, not changed):**
1. The two Guess With Milo episodes are 3D lessons. The Nov 18 rule "3D teaching lessons: 0, stopped" applies to them. Posting them in the 3:30 PM
   slot keeps the one-3D-a-day cap but is an exception to that rule, and that call is yours. If 3D lessons stay stopped, the same two scripts port to the
   2D fact-lesson engine (`studio/cartoon/toon.py`, slots 9:30 AM / 5:30 PM). The beats are the same: a mystery cold open, answer signs, a
   reveal, the facts, a quiz.
2. Guess With Milo is a new format, so by the channel rule nothing of it is uploaded until you have watched one full episode and approved it.
   The pilot has to be built and approved before Nov 25.
3. The daily builds fill the next free 2D lesson slots by themselves, so the test does not use those slots.

## The four episodes

### Sing With Milo #1: Crunch, Crunch! Who's Munching? (3D song, ~2:30, Nov 23)
- **Working title:** Crunch, Crunch! Who's Munching? Sing With Milo (44) · **Alternate:** Who's Eating Lunch? Sing With Milo (33)
- **Why this and not a second panda song:** "Panda Loves Bamboo!" went public Nov 19 and has no 7-day data yet. Your crunch opening is kept, but as
  a mystery chorus with four eaters, so it is not a near-copy of a live video.
- **Thumbnail brief:** one bamboo stalk snapped in half in close-up, a black-and-white furry paw holding it at the frame edge (the animal not
  shown), Milo peeking from behind the leaves; word: **CRUNCH!**
- **Opening shot:** extreme close-up of a bamboo stalk in a green grove; on beat 1 the stalk snaps (the crunch is a percussion hit in the
  music, on the beat, never over a sung word). **First lyric:** *"Crunch, crunch! Who's that munching? Crunch, crunch! What's for lunch?"*
- **Outline:** chorus (question) → verse 1 the panda appears with bamboo → chorus → verse 2 a long dark tongue wraps a leaf: the giraffe →
  verse 3 a koala with eucalyptus → bridge: "Munch with your hands! Crunch, crunch, crunch!" (pretend eating action, no real food) →
  verse 4 elephant with grass → final chorus answers "Crunch, crunch! Lunch is fun!"
- **Takeaway:** different animals eat different plants. Each food fact is read at its source on the day the lyrics are written; no numbers
  until then.
- **Hypothesis:** opening on the sound-and-picture mystery instead of a group shot raises 30 s retention. **Metric:** % still watching at
  30 s, at least 30% (songs read today: Where Is My Mama? 23%, Animal Sounds 19%, Milo Had a Zoo 32%).

### Guess With Milo #1 (pilot): Whose Feet Are These? (3D lesson, ~5:36, Nov 25)
- **Working title:** Whose Feet Are These? Guess With Milo (37) · **Alternate:** Who Made This Footprint? Guess With Milo (40)
- **Thumbnail brief:** one giant round footprint in warm sand, Milo leaning over it with his wing at his beak, a big "?"; word **WHO?**
- **Opening shot:** low close camera on the footprint, Milo hops in. **First line:** *"Look! A giant footprint in the sand! Who made it?"*
- **Outline:** 3-print trail → elephant (tiptoes, cushion), giraffe (two hooves, same-side walk), zebra (one toe in one hoof), each starting
  with its footprint and a 4 s guess → quiz → the footprint trail recap. The full package is in `pilot/`.
- **Takeaway:** animals' feet are built for how they walk.
- **Hypothesis:** a mystery cold open (no greeting first) keeps more children past 30 s. **Metric:** 30 s retention at least 30% and an
  average view of 1:00 or more (2D lessons read today: 18-27% at 30 s, 0:26-0:45 average).

### Sing With Milo #2: Whose Baby Is This? (3D song, ~2:45, Nov 27)
- **Working title:** Whose Baby Is This? Sing With Milo (34) · **Alternate:** Who's This Little Baby? Sing With Milo (38)
- **Why:** it copies the structure of the channel's best long-form video by far (Where Is My Mama?: 31.3 h, 41% of long-form hours): one question,
  answered in every verse. It uses new animals: panda cub, koala, polar bear cub, monkey, tiger cub (all existing rigs or variants).
- **Thumbnail brief:** one tiny cub peeking around a huge furry leg, Milo with his wing at his beak; word **WHOSE?**. Not the Mama picture
  (Milo centre with three animals).
- **Opening shot:** a small cub's ears poke up behind a log in close-up on beat 1. **First lyric:** *"Who's this baby, small and new? Peek-a-boo,
  I see you!"*
- **Outline:** question chorus → 4 verses, each a clue (fuzzy, stripy, clings tight, white and snowy) then mama walks in and the baby runs to her
  (warm hug, no one is lost: the baby is playing peekaboo) → bridge: "Peek and hide, peek and hide!" → final chorus.
- **Takeaway:** baby animals look like and stay near their mamas. Facts read at source on the script day.
- **Hypothesis:** the Mama structure with a new cast earns more watch hours per impression than the channel's other songs. **Metric:** watch
  hours at 7 days per 1,000 impressions (Where Is My Mama?: 0.26 h per 1,000 lifetime) and CTR at least 2.9%.

### Guess With Milo #2: Whose Ears Are These? (3D lesson, ~5:30, Nov 29)
- **Working title:** Whose Ears Are These? Guess With Milo (37) · **Alternate:** Who Has These Ears? Guess With Milo (35)
- **Why:** the most re-watched video on the channel is the Short "Rhinos Can Turn Each Ear a Different Way!" (360.6% viewed, 1:48 average on a
  0:30 Short). Children re-watch ear surprises.
- **Thumbnail brief:** two big grey ears swivelling in different directions above tall grass (the rhino hidden), Milo cupping a wing to his
  ear; word **WHO?**
- **Opening shot:** close on two ears poking out of tall grass, one turning left, one turning right. **First line:** *"Look! Two ears in
  the grass, and they're turning different ways! Who is it?"*
- **Outline:** cold open → rhino (turns each ear its own way), fox (big ears), koala (fluffy ears) → each with an ear silhouette guess, a
  listening action ("cup your hands behind your ears") → quiz → recap. Facts read at source on the script day.
- **Takeaway:** ears help animals hear what is around them.
- **Hypothesis:** a body-part guessing title tied to a fact children already re-watch lifts CTR. **Metric:** 7-day CTR at least 4% with at
  least 1,000 impressions.

## Reading the test
After seven days for each episode, fill in `05_scorecard.csv`. Compare each with the same-length videos in `data/` and with the other test
format. With under 1,000 impressions an episode's CTR and retention are noise: wait to day 14 before calling it.

## UPDATE Nov 20 2026, 10:40 AM: owner's decision, plan as implemented
Owner: "Aproved for your changes. Guess with Milo should be always 2d not 3d, 3d is only for viral songs. Implement the changes proposed to make
those videos viral starting today." What changed against the plan above:
- **Guess With Milo is 2D** (cartoon lessons, `studio/cartoon/toon.py`), queued first in `docs/cartoon/build_plan.py`: Whose Feet Are These? (claimed by
  the next lesson build for **Sun Nov 23, 5:30 PM**; Shorts Nov 27, 28, 29), then Whose Ears Are These?, then Whose Egg Is This?. The 3D pilot spec in
  `pilot/` stays a reference for the words and beats.
- **Sing With Milo songs** are written (`studio/zoo3d/make_specs_v3.py`, facts read Nov 20): Crunch, Crunch! Who's Munching? (zoo3d_ep25) on
  **Mon Nov 24, 3:30 PM**, Whose Baby Is This? (zoo3d_ep24) on **Wed Nov 26, 3:30 PM**. The Nov 23 3:30 PM slot already holds the tiger song.
  Whose Baby uses panda, koala, polar bear and tiger cubs (the variety check needed two cast changes against Crunch).
- The cold open, question titles and one-object thumbnails apply to every new 2D episode (`docs/CARTOON_RUN.md` "VIRAL PACKAGING").
