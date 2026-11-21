# Shot list: Whose Feet Are These? Guess With Milo (zool_g01), DRAFT

Workflow: the existing 3D lesson pipeline (`studio/zoo3d/teach.py` → `jobs/zool_g01.json` → PC worker in Blender, zooworld set, native 4K
3840x2160, 16 samples; `lesson_shorts.py` re-frames each animal part for 9:16). Cast are the current rigs: Milo (`chars/milo.py`), elephant,
giraffe and zebra (base kinds in `chars/animal.py`). The layout is the current lesson layout: Milo on the left, the animal in the middle,
the teaching board (answer signs, timer dots, examples) on the right third. Times are the script's estimates.

## Shots

| # | Time (est.) | Place / light | Camera | On screen | Notes |
|---|---|---|---|---|---|
| 1 | 0:00-0:05 | savanna, morning | LOW, close on the sand, slow push-in | One big round FOOTPRINT pressed in the sand (new prop), toenail dents at the front edge. Milo hops in from frame left on "Look!" and leans over it. | **The first frame is the mystery.** No title card, no greeting before it. The print is centred, filling ~40% of the frame, so it reads on a phone. |
| 2 | 0:05-0:09 | same | rise to a medium-wide | A trail of 3 prints pops in on "one, two, three" (elephant round, giraffe two-part, zebra single hoof) | count rhythm, prints left to right |
| 3 | 0:09-0:17 | same | medium on Milo | WHOSE FEET? 3D word; Milo wing-points down the trail | "Guess With Milo" said once, the series name parents can find again |
| 4 | 0:17-0:25 | savanna, morning | lesson wide, animal spot EMPTY | Elephant print on the board; answer signs ELEPHANT / LION | thinking time 4 s. No elephant visible yet |
| 5 | 0:25-0:29 | same | wide | Elephant walks in on "It is the elephant!" (visit at line 2); ELEPHANT sign lights | reveal = the payoff of the hook |
| 6 | 0:29-0:52 | same | medium | TIPTOES! sign; CUSHION magnifier (or the new `footcut` card, see below); timer dots on "Hmm." | |
| 7 | ~0:52 | same | **close:elephant, framed on the front feet** | big round feet stepping | needs feet framing: check the still, the default close crops at the chest on tall animals |
| 8 | 0:56-1:20 | same | medium | count 1-5 nails; rumble RINGS on the ground by the foot | rings prop exists |
| 9 | ~1:24 | same | close:host | Milo: "Say it with me" | |
| 10 | 1:27-1:46 | same | wide | Milo tiptoes in place (action), check signs CUSHION / WHEEL | Short 1 ends here |
| 11 | 1:46-1:54 | savanna, golden | wide, animal spot empty | Giraffe two-part print on board; GIRAFFE / LION | |
| 12 | 1:54-2:20 | same | wide → medium | Giraffe walks in; count 2 (two hooves); RULER "12 INCHES" beside the print | ruler prop exists |
| 13 | ~2:20 | same | **close:giraffe, framed on the legs** | giraffe walks a few steps moving both legs of one side together | **new walk cycle**: the current walk is not a same-side (pacing) gait; without it, drop the "Look!" shot and keep the sign |
| 14 | 2:24-2:50 | same | medium | SIDE, SIDE! sign; 1 HOUR! sign | no birth shown, only the sign |
| 15 | 2:50-3:16 | same | close:host → wide | Milo "this side, that side" action; TWO / TEN check | Short 2 ends here |
| 16 | 3:16-3:24 | spring meadow, noon | wide, animal spot empty | Zebra single hoof print in mud; ZEBRA / ELEPHANT | |
| 17 | 3:24-3:44 | same | wide → medium | Zebra trots in; count 1; HOOF! sign | |
| 18 | ~3:44 | same | **close:zebra, framed on the hooves** | hooves stepping | |
| 19 | 3:48-4:12 | same | medium | count 1-4 legs; FINGERPRINT card next to the stripes | fingerprint prop exists |
| 20 | 4:12-4:42 | same | close:host → wide | trot action, one finger up, ONE / FIVE check | Short 3 ends here |
| 21 | 4:42-5:16 | beach, noon | quiz layout as zool_ep16 | QUIZ TIME! → three questions with answer signs; each animal appears on its answer | unchanged quiz code |
| 22 | 5:16-5:36 | savanna, sunset | medium-wide | the 3-print trail again, Milo waves; closing picture 3 s: next Guess With Milo card | made-for-kids: no end screens, so the pointer is this picture + the series playlist |

## New work needed (all inside the current tools and budget)

1. **`footprint` prop in `teachprops.py`** (required): a flat decal pressed into a ground patch, options `kind` = `elephant` (large
   round print, 4-5 shallow nail dents on the front edge), `giraffe` (two halves side by side), `zebra` (one rounded hoof print),
   `ground` = `sand` | `mud`, `s` = scale, and `trail` = a list of kinds laid left to right with `dx` spacing. Shapes follow the facts
   read (two hooves; one toe in one hoof; toenails), not a guess at real track size.
2. **Feet framing for `close:<animal>`** (required): a variant that frames the lower legs and feet (tall animals: giraffe). Check one
   still of each before rendering, per the stills rule.
3. **Giraffe same-side walk** (optional): a pacing gait (both right legs, then both left). If it is not added, shot 13 shows the
   giraffe standing and the SIDE, SIDE! sign carries the fact.
4. **`footcut` card** (optional): a side-view cutaway of an elephant foot (toe bones angled down, cushion under the heel). Without it the
   CUSHION magnifier stays.

No new character, voice, set or render setting. Same watermark (`watermark.py`), same 4K size, same music bed.

## 9:16 Shorts (three, one per animal part)

Each part (shots 4-10, 11-15, 16-20) is re-framed by `lesson_shorts.py` with its own 9:16 camera. Title band two lines "WHOSE" / "FOOT?"
(5 and 5 letters, under the 15/10 limit). The part starts on its own footprint, so each Short opens on a mystery too.
