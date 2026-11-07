# Grovewatch: Sanctuary Siege — Progress

An original tower-defense + village-building game. The **Keepers of the Grove** defend their
woodland sanctuary from the **Murkhorde**, bog critters creeping out of the Gloomfen.
Resources: **Coins** (battle currency / village gold) and **Glowsap** (the second village resource, planned).

Run: `npm run dev` · Build: `npm run build` · Tests: `npm test` · Smoke test + screenshots: `npm run build && node scripts/screenshot.mjs <name>` · Balance report: `npx vite-node scripts/balance.ts [runs]` · Branch damage benchmark: `npx vite-node scripts/spec-bench.ts`

Iteration counter: **14** (next iteration = 15 → POLISH + BALANCE pass)

## Done
- [x] **Iter 1** — Project scaffold (Vite + TS + Phaser 3 + Vitest), procedural textures, WebAudio SFX.
  Renderer-free `BattleSim` (paths, waves, towers, projectiles, splash/slow support, armor/magic resist,
  4 targeting modes, early-call bonus, win/lose). Level 1 *Mossgate Meadow* (8 waves), 2 towers
  (Thornbow Nest, Glimmer Spire, 3 tiers each), 3 enemies (Mudling, Skitter, Shellback).
  Battle HUD (lives/coins/wave, call wave, pause, speed x1/x2/x3), radial build/upgrade/sell/aim menu,
  hit flash, damage numbers, particles, screen shake on leak, victory/defeat panel with stars saved to localStorage.
  Headless Playwright smoke test script.
- [x] **Iter 2** — All 4 base tower types. **Boulder Bellows** (artillery: lobbed rocks that aim ahead of
  the target, splash damage, can't hit flyers, arc rendering, dust ring + small shake) and **Burrow Den**
  (barracks: squads of Badger Wardens that walk to a rally point on the road, block and brawl with ground
  enemies, take damage, die, respawn, heal when idle; tap "Rally Point" then the road to move them).
  Enemies now have melee stats. 4-option radial build menu. 7 new unit tests (30 total).
- [x] **Iter 3** — Enemy roster expanded to **12 types**: Gloomwing + Bog Gnat (flying: soldiers and
  artillery can't touch them; drawn high with a ground shadow), Bogmender (healer aura), Reedguard
  (reed shield absorbs damage first), Splotch (splits into 2 Mudlings), Thornhog (fast + armored),
  Wispling (70% magic resist), Bog Brute (tank that hits soldiers hard), and the boss **Old Murkmaw**
  with 3 phases (summons Mudlings → mud shell + healers → enrage speed). Boss HUD bar with phase ticks
  and shield, boss arrival/phase banners + shake, heal/shield-break/split effects. New level 2
  **Gloomfen Edge** (2 merging roads, 12 waves, boss finale). Banners moved under the HUD so they
  don't cover the battlefield; oversized map background so shake doesn't show edges.
  `scripts/showcase-enemies.mjs` visual check. 6 new tests (36 total).
- [x] **Iter 4** — **Heroes.** 3 heroes in `data/heroes.ts`: **Bramble** the Badger Knight (melee
  blocker; passive Thick Hide; active Earthshake = ground AoE + slow), **Fen** the Heron Ranger (ranged,
  hits air; passive 25% crits; active Feather Storm = volley at 8 targets), **Ember** the Fox Sage
  (magic; passive Warm Glow = nearby towers +20% fire rate; active Foxfire Ring = AoE burn + slow).
  Tap the hero (or portrait / H) then tap the map to move; skill button (or Q) with cooldown pie.
  XP from kills (full nearby, 35% far), levels 1–6 (+12% stats/level), death + respawn timer.
  Hero picker on the menu (saved). Smoke scripts now start battles via the Menu scene (old way left
  the menu running underneath and its buttons swallowed clicks). 8 new tests (44 total).

- [x] **Iter 5 — POLISH + BALANCE.** Headless autoplayer (`src/systems/autoplay.ts`) with 7 scripted
  strategies + `scripts/balance.ts` report. Structural fixes: the next-wave countdown now waits until the
  current wave finishes spawning (waves used to stack every 14s); supply coins at each wave start
  (`waveIncome`: 10 + 3×wave). Tuning: Boulder Bellows damage/rate up (was useless), Burrow soldiers
  hit harder and are tougher, Mudling/Skitter/Shellback bounties up, L1 start 250 coins and softer
  final wave, L2 start 380 coins, softer waves 7–8, Murkmaw hp 2400 → 1900. Polish: wave banner shows
  "Wave N of M" plus supply and early-call coins; the wave button says "Call Early" while a wave is spawning.
  Balance guard-rail tests (47 total).

- [x] **Iter 6** — **Global spells** (`data/spells.ts`): **Starfall** (tap a spot; a falling star lands
  0.9s later for 140 damage in an 85px radius, hits flyers; 40s cooldown) and **Grove Call** (tap the
  road; 3 hedgehog Rangers hold that spot for 16s; 28s cooldown). Bottom-right spell buttons with
  cooldown pies and a targeting reticle; keys 1/2, Esc cancels. Soldiers now carry their own stats/anchor
  (needed for summons). The falling-star animation follows game time (stays in sync on slow devices and at
  x3 speed). Moved the L1 bottom-right build pad out from under the spell buttons. 2 new tests (49 total).

- [x] **Iter 7** — **World map + campaign levels 3–5.** New `WorldMapScene` ("The Grovelands"): island
  map with regions, dotted trail, level nodes with stars, locks, a pulsing next level, total stars, and a
  level card (blurb, waves/roads/lives, enemy preview, Play). Levels unlock in order (≥1 star on the
  previous one). Menu → Campaign; the victory screen has Retry / Map / Next. New levels: **3 Thornwood Hollow**
  (long serpentine road), **4 Mirelake Crossing** (two separate roads and gates, 25 lives, ponds),
  **5 Murkmaw's Den** (three roads merge, 15 waves, boss finale). Gates are now drawn at the real road
  exit and deduplicated; levels can have decorative ponds. Level-data tests (pads off roads, on screen)
  and guard rails for levels 3–5 (53 tests).

- [x] **Iter 8** — **Tower specializations.** Every tower offers 2 branches at max tier (`specs` in
  `data/towers.ts`): Thornbow → **Hawkeye Perch** (270 range, 70 dmg, pierces 50% armor) / **Bramble
  Volley** (3 targets per volley); Glimmer → **Stormcall Spire** (chain lightning to 4 more) / **Frostbloom
  Spire** (splash + heavy slow); Boulder → **Quake Mortar** (huge blast) / **Sap Catapult** (slowing splash);
  Burrow → **Stonehide Wardens** (armored tanks) / **Thornback Raiders** (4 fast hitters). New sim mechanics:
  multishot, chain, armor pierce. Menu shows both branches; the first tap previews (description + range),
  the second tap buys. Crested tower art per branch, tinted shots, lightning effect + zap sound. The
  autoplayer buys specializations once everything is maxed. Sell refunds include the spec. 8 new tests (61 total).

- [x] **Iter 9** — **Home village** (`VillageScene`, rules in `systems/village.ts`, data in `data/buildings.ts`).
  22×13 grid with 8 building types: **Grove Hall** (town hall, 5 levels, gates counts/levels), **Acorn Mine**
  (coins/hour), **Glowsap Tap** (glowsap/hour, the second resource), **Burrow Vault** (storage), **Builder
  Burrow** (each = 1 builder), **Defense Workshop**, **Ranger Lodge** (for raids later), **Bramble Wall**.
  Real-time construction timers (keep running while away), production accumulates offline up to each
  producer's capacity, storage cap, builders limit, Grove Hall requirements and max counts. Tap a producer
  to harvest (bubble shows when ready); info panel with upgrade cost/time and a progress bar; Build shop;
  placement and move modes with a green/red snapped ghost. Procedural art for every building level, coin/
  glowsap/hammer icons. **Battle links:** campaign wins pay village resources (more for first clears and
  new stars, shown on the victory panel); the Defense Workshop gives +5% tower damage per level in battle.
  Menu now has Campaign + Village. 10 new tests (71 total).

- [x] **Iter 10 — POLISH + BALANCE.** The autoplayer now casts Starfall on the densest clump, Grove Call ahead of
  the lead enemy, and the hero skill when ≥3 enemies are in reach; expert/casual pick an **adaptive tower mix**
  from the level's enemy makeup. The novice profile now has a hero + spells (every real player does).
  New `scripts/spec-bench.ts` (DPS and DPS-per-coin per branch vs armored / crowd / flyers).
  Tuning: spells nerfed (Starfall 140→100 dmg, 40→50s; Grove Call 16→12s, 28→35s, weaker Rangers);
  new per-level **enemy health ramp** (`hpMult`: L2 1.25, L3 1.3, L4 1.15, L5 1.4); Hawkeye Perch buffed
  (110 dmg, 70% pierce: now the best anti-armor branch); Frostbloom nerfed (34 dmg, 45 splash).
  Polish: real **pause menu** (Resume / Restart / Sound on-off / Quit to Map; Esc toggles it).
  Guard rails updated (late levels winnable but not guaranteed). 71 tests.

- [x] **Iter 11** — **More village → battle perks.** `battlePerks()` now returns tower damage (Defense
  Workshop +5%/lvl), **starting coins** (Grove Hall +40 per level above 1) and **Ranger strength** (Ranger
  Lodge: Grove Call Rangers +25% hp/damage per level). **Hero training**: spend Glowsap on the menu's hero
  card (300/800/1600/3000/5000) to raise a hero's rank; rank N heroes start every battle at level N+1
  (persisted in `heroRanks`). Battles open with a "Village bonuses" banner listing what's active; building
  panels describe their battle bonus. 2 new tests (73 total).

- [x] **Iter 12** — **Region 2 + levels 6–8.** World map is now paged by region (`REGIONS`, `regionOf`) with
  `<`/`>` arrows; the next region stays locked (toast) until its gate level is beaten. New snowy region
  **Frostfern Highlands** (snowy island map with pines, frozen lake, "Mountain Gate", placeholders for
  levels still to come). Levels: **6 Frostfern Pass** (long switchback), **7 Icicle Crossing** (two roads
  cross in an X and split to two gates, hero starts at the crossing), **8 Glacier Hold** (three trails
  merge; Murkmaw returns). Snow theme: pale ground, pine-colored trees with snow caps, falling snow.
  New level fields: `heroSpawn`, theme `trees`/`snow`. **Economy fix:** kill bounties now scale with the
  level's `hpMult` (later levels used to starve the player). All hpMults retuned (L3 1.5, L4 1.15, L5 1.65,
  L6 2.0, L7 1.45, L8 1.6). 75 tests (regions, bounty scaling, levels 3–8 winnable).

- [x] **Iter 13** — **Highlands complete (levels 9–10) + frost enemies.** New mechanic **chill**: enemies with
  `chill` periodically freeze shooting towers in a radius (soldier dens are immune); frozen towers turn icy
  and can't fire. New enemies: **Rime Wraith** (hooded frost spirit, 40% magic resist, freezes towers in 95px
  every 5s) and boss **Grimtusk the Frost Boar** (3200 hp, big freeze aura; phases: summons wraiths → ice
  hide shield + thornhogs → charge). Levels: **9 Rimewood Hollow** (wraith debut, hp×2.15) and **10 Frostpeak
  Summit** (two roads merge, Grimtusk finale, hp×1.75). Ice-ring + "Frozen!" effects; enemy showcase script
  takes a level index. 14 enemy types now. 76 tests.

- [x] **Iter 14** — **Region 3: The Emberdeep (levels 11–12) + burrowers.** New mechanic **burrow**: enemies dive
  underground on a cycle. While underground they can't be targeted by towers, hero, splash, chain, Starfall or
  hero skills, they can't be blocked (diving frees them from soldiers), and they move 1.5× faster. In-flight
  shots miss. New enemy **Cinder Mole** (rendered as a moving dirt mound while under). Volcanic theme:
  dark ash ground, rust/dead trees, **lava pools** with pulsing glow, drifting embers; ember-style world-map
  page ("Ash Road", smoking rocks, lava lake). Levels: **11 Ashfall Gate** (switchbacks, hp×1.8) and
  **12 Cinder Tunnels** (two roads merge, hp×1.6). 15 enemy types now. 78 tests.

## In Progress
- (none)

## Backlog (ranked)
1. Levels 13–15 to finish the Emberdeep + the final boss (and a campaign ending screen).
2. Raid mode: AI villages, train troops in Barracks, deploy to attack.
3. Meta: achievements, daily challenge, encyclopedia, settings scene (volume / mute).
4. Mobile polish: larger touch targets, pinch-free layout, orientation hint.
5. Ambient music loop (procedural).

## Known Bugs
- (none known)

## Ideas parked
- Village: "finish now" doesn't exist (no premium currency on purpose); maybe a free speed-up after a 3-star win.
- Village: drag-to-pan for small phone screens (the grid currently fits 1280×720).
- Pause menu with "Quit to map" / "Restart" (currently only via the end panel).
- Autoplayer should cast spells and move the hero (do this in the iteration-10 balance pass).

## Balance Notes
**Iteration 14 (first pass, to revisit in the iteration-15 balance pass):** 11 Ashfall Gate 100/100/13 ·
12 Cinder Tunnels 75/75/75. At first hp×2.2/2.3 was a wall (Cinder Tunnels: 0% for everyone by wave 6).

**Iteration 13:** 9 Rimewood Hollow 100/100/30 · 10 Frostpeak Summit 88/75/13 (expert/casual/novice, 8–10 seeds).

**Iteration 12** (`balance.ts 10`, after bounty scaling + retune):

| Level | expert | casual | novice |
|---|---|---|---|
| 1–2 | 100% | 100% | 100% |
| 3 Thornwood Hollow | 100% | 100% | 90% |
| 4 Mirelake Crossing | 90% | 90% | 80% |
| 5 Murkmaw's Den | 90% | 80% | 70% |
| 6 Frostfern Pass | 100% | 100% | 30% |
| 7 Icicle Crossing | 100%* | 100%* | 0% |
| 8 Glacier Hold | 100% | 80% | 90% |

\* 90% in the 10-seed tuning run.
- Icicle Crossing was a wall (0% for everyone at wave ~8) until (a) the hero started at the crossing instead of
  one gate and (b) bounties scaled with hpMult. On two-gate maps, where the hero starts matters a lot.
- Novice ≈ expert on Glacier Hold again (chokepoint-focused upgrades). Smarter-AI follow-up still pending.

**Iteration 10** (`balance.ts 10`, autoplayer uses spells + hero skill; novice has a hero now):

| Level | expert | casual | novice |
|---|---|---|---|
| 1 Mossgate Meadow | 100% | 100% | 100% |
| 2 Gloomfen Edge | 100% | 90% | 100% |
| 3 Thornwood Hollow | 90% | 100% | 70% |
| 4 Mirelake Crossing | 50% | 70% | 40% |
| 5 Murkmaw's Den | 70% | 70% | 70% |

- Before tuning, spells + hero skill made **every** profile win every level with ~full lives; each single power
  (Starfall, Grove Call or the hero skill) was enough to flip the novice from losing to winning L3–L5.
- Difficulty now ramps: trivial → easy → medium → hard. The village Defense Workshop (+5–20% tower damage)
  gives returning players a way to push through L4–L5.
- **Autoplayer limitation:** on late levels expert ≈ casual ≈ novice. The novice concentrates upgrades on
  a few top slots near chokepoints, which turns out to be very efficient. A smarter AI (moving the hero,
  choosing branches per level) is needed before fine-tuning L4/L5 further.
- Branch benchmark after tuning (DPS per 100 coins, armored / crowd / flyers): Hawkeye 11.6/14.1/14.1,
  Volley 2.6/19.5/19.5, Stormcall 7.5/22.9/22.9, Frostbloom 4.9/38.9/29.1, Quake 2.8/55.5/0,
  Sap 1.9/38.3/0, Stonehide 3.4/8.5/0 (tank), Raiders 10.1/25.3/0. Stationary clumps flatter splash.

**Iteration 7: new levels** (`balance.ts 8–10`; the expert AI now uses Fen since Bramble can't hit flyers):

| Level | expert | casual | novice |
|---|---|---|---|
| 3 Thornwood Hollow | 100% | 88% | 0% |
| 4 Mirelake Crossing | 80% | 60% | 0% |
| 5 Murkmaw's Den | 100% | 88% | 0% |

- Mirelake was unwinnable at first (two full roads on one budget, and the hero can only guard one). Fixes: 700 start
  coins, lighter waves, 25 lives (one pool per gate).
- Hero choice is level-dependent: Bramble is weak on flyer-heavy maps (Den: expert with Bramble 0%, with Fen 100%).
  Good for strategy, but players need a hint (show flyers in the level card ✔ — enemy preview icons).
- The autoplayer still doesn't cast spells or move the hero, so humans should do better than these numbers.

**Iteration 5 results** (`npx vite-node scripts/balance.ts 12`, after tuning):

| Level | Strategy | Win % | Avg lives left |
|---|---|---|---|
| Mossgate Meadow | expert-mixed | 100% | 20.0/20 |
| Mossgate Meadow | casual-mixed | 100% | 20.0/20 |
| Mossgate Meadow | novice | 100% | 12.6/20 |
| Mossgate Meadow | only-thornbow | 100% | 15.5/20 |
| Mossgate Meadow | only-burrow | 0% | 0/20 (support tower, expected) |
| Gloomfen Edge | expert-mixed | 100% | 11.8/20 |
| Gloomfen Edge | casual-mixed | 100% | 18.8/20 |
| Gloomfen Edge | novice | 0% | dies ~wave 9 |
| Gloomfen Edge | any single tower type | 0% | — (mixing required) |

Before tuning, **every strategy lost both levels** (waves stacked + starved economy).

Findings / follow-ups:
- Heroes matter a lot on L2: no hero → 0–10% win for the expert AI; with a hero → 40–50% (before the final tuning).
  Bramble and Fen are close; Ember is a bit weaker for this AI (it doesn't move her next to towers).
- Filling every slot before upgrading is worse than upgrading the best 70–75% of slots.
- L1 is now a gentle tutorial; difficulty should ramp from L3 onward (target: expert ~90%, casual ~60%,
  novice ~10–20% by level 5).
- Burrow Den alone can't win (it only blocks); that's intended, but its value in mixes deserves a look later.
