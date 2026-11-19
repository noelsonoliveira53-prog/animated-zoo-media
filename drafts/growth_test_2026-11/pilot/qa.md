# Quality check: zool_g01 Whose Feet Are These? Guess With Milo (DRAFT, checked Nov 19 2026)

## Facts (each line read at its source today; a line whose source could not be read is not in the script)
| Script claim | Source (read Nov 19 2026) | Status |
|---|---|---|
| An elephant walks on its tiptoes | SDZWA Library, African Elephant, Physical Characteristics: "on tiptoes," digits angled toward ground | OK |
| A soft cushion under the toes soaks up the bump | same: fat pads "cushion bottoms of feet", "Absorb shock from impact with ground" | OK |
| Some elephants have four nails on a front foot, some five | same: savanna "4 to 5 nails on forefeet" | OK (the count of five on screen is one of the two true numbers) |
| Elephants may feel tiny rumbles with their feet | same: "May detect vibrations through their feet, bones, and inner ear structures" | OK, said as "scientists think ... may" |
| A giraffe has two hooves on each foot | Live Science, Giraffes: "two weight-bearing hooves on each foot" | OK |
| Its feet are about as wide as a ruler is long | Live Science: "their feet are 12 inches (30.5 cm) across"; a school ruler is 12 in | OK |
| It moves the two legs on one side together, then the other side | SDZWA Library, Giraffe, Behavior: "Alternate moving the two right limbs together and then the two left" | OK |
| That keeps its front and back legs from bumping | same: "keeps front legs from tangling with hind legs" | OK |
| Each leg is about as tall as a grown-up | Live Science: "legs are also 6 feet long" | OK (6 ft is a tall adult: "about") |
| A baby giraffe can stand and walk about an hour after birth | Live Science "At just an hour after birth, they can stand up and walk around"; PBS Nature "About an hour after birth ... stand up and walk" | OK (birth not shown) |
| A zebra walks on just one toe on each foot | SDZWA Library, Plains Zebra: "Single toe at terminus of each limb" | OK |
| The hoof covers the toe and keeps it safe | same: "Hooves enclose and protect the toe" | OK |
| A hoof keeps on growing | same: "Modified skin, grows continually" | OK ("a little like your fingernails" is a comparison, not a claim) |
| No two zebras are the same | same: "Unique pattern on each individual" | OK |
| Footprint drawings (round print with nail dents / two halves / one hoof) | drawn from the anatomy above | Picture only, never narrated as a measured track shape |

## Kid safety (CLAUDE.md, channel rules)
Nobody is hurt, lost, crying or trapped. No birth shown (the calf fact is a sign only). Actions to copy are safe sitting or standing moves
(tiptoe, step softly, stand tall, one finger up); the earlier idea "stand on one toe" was removed because toddlers can fall. Hand on the
floor is a calm listening action. No calls to action aimed at kids, no "subscribe" line.

## Milo continuity
Same rig (`chars/milo.py`), voice af_heart at 0.84 (the current lesson voice), same personality lines ("Super thinking!", "You remembered!",
"Bye-bye, friends!"). Milo still introduces himself, after the hook instead of before it. No new costume or colour.

## Readable on a phone
Footprint fills ~40% of the first frame. Answer signs are the current two-sign board. 3D words are short (WHOSE FEET?, TIPTOES!, TWO HOOVES!,
ONE TOE!). Thumbnail has one word (WHO?). Still to check: one still of every shot in 16:9 and 9:16 before rendering (feet framing on the
giraffe especially), as the stills rule requires.

## Narration clarity
Average line 9 words; every question is followed by a real pause (4 s answer signs, 3 s "Hmm." thinking time, 3 s for actions), the
same pauses the current lessons use. The music bed stays ducked under the voice; no sound effect lands on a word. `listen.py` must run on
the built job before rendering. It measures level, clicks and clashes; it does not hear, so how the voice and tune sound is the owner's call.

## Not checked (cannot be until the lesson is built)
Exact line times and part lengths (estimated 90, 89 and 87 s), mouth sync, stills of every shot, the new footprint prop, the 9:16 framing
of each Short, review.py, the watermark corner.
