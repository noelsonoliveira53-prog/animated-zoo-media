# Grovewatch: Sanctuary Siege — Progress

An original tower-defense + village-building game. The **Keepers of the Grove** defend their
woodland sanctuary from the **Murkhorde**, bog critters creeping out of the Gloomfen.
Resources: **Coins** (battle currency / village gold) and **Glowsap** (the second village resource, planned).

Run: `npm run dev` · Build: `npm run build` · Tests: `npm test` · Smoke test + screenshots: `npm run build && node scripts/screenshot.mjs <name>` · Balance report: `npx vite-node scripts/balance.ts [runs]` · Branch damage benchmark: `npx vite-node scripts/spec-bench.ts` · Raid balance: `npx vite-node scripts/raid-balance.ts [--naive]` · Economy report: `npx vite-node scripts/economy.ts`

Iteration counter: **31** (next balance pass at iteration 35)

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

- [x] **Iter 15 — POLISH + BALANCE.** Smarter expert autoplayer (`smart: true`): moves its hero to the busiest
  **choke point** (`chokePoint()`: the road point with the most road in reach, biased toward the gate) and picks
  **branches from the level's makeup** (`smartSpec()`: Volley vs flyers else Hawkeye; Stormcall; Quake vs tanks
  else Sap; Stonehide vs brutes else Raiders). Expert now beats casual/novice on most levels. Retuned Glacier
  Hold and Cinder Tunnels (hp×1.7). Polish: **next-wave preview** in the top bar (enemy icons + counts, ✈ marks
  flyers, red count for bosses); moved a lava pool out from under the spell buttons. 78 tests.

- [x] **Iter 16** — **Campaign complete: levels 13–15, final boss, ending.** New mechanic **spawner** (enemies
  that release minions on a timer, capped by `limit`). New enemies: **Ember Imp** (fast flyer), **Ash Hive**
  (slow tank that hatches up to 6 imps) and final boss **Vulkhar the Ash Wyrm** (3200 hp, burrows, breeds imps,
  4 phases: moles → obsidian shield + brutes → frost wraiths + speed → fury). Levels: **13 Smoulder Fields**
  (long serpentine plain), **14 Obsidian Bridges** (two separate lava-bridge roads, two gates), **15 Heart of
  the Emberdeep** (three roads; Murkmaw, Grimtusk and Vulkhar return as a boss rush). New **EndingScene**
  (night-to-dawn over the great oak, stars total); the final victory shows "Epilogue". **Bug fixes found by
  the sim:** packs of Rime Wraiths could freeze towers forever → 3s thaw immunity; Ash Hives used to spawn
  ~26 imps each over their slow walk → capped. The smart AI now keeps the hero at a level's designed
  `heroSpawn`. 18 enemy types, 15 levels, 80 tests.

- [x] **Iter 17** — **Raid mode.** Train troops at the Ranger Lodge (instant, costs Glowsap; army space =
  10 × lodge level): **Badger Brawler** (tank), **Hedgehog Slinger** (ranged), **Beaver Sapper** (targets
  defenses, splash), **Owl Striker** (flyer, needs Lodge 2). Village **Raid** button opens a panel with
  training cards and 3 seeded Murkhorde camps (Outpost / Warren / Stronghold) showing their loot. Pure
  `RaidSim` (`systems/RaidSim.ts`) + seeded `generateCamp` (`systems/camp.ts`): Mud Totem (HQ), Spit Towers
  (hit air), Bog Mortars (splash, ground only), Loot Piles, Mud Huts; troops pick the nearest (or nearest
  defense) target, defenses shoot the nearest troop in range. Stars: ≥50%, HQ down, 100%. Loot is banked
  per destroyed building; survivors and undeployed troops return; new camps after every raid. `RaidScene`
  with a deploy bar (tap or drag outside the camp; a red no-deploy zone flashes when too close), HP bars,
  shots, destruction effects, HUD (%, timer, loot, stars) and a result panel. **Save fix:** the village now
  reloads the save before writing, so it can't overwrite the army or other progress. 89 tests.

- [x] **Iter 18** — **Raid walls + raid balance.** Warren and Stronghold camps get a ring of **Stake Walls** around
  their core (HQ + defenses). Ground melee troops whose next step would hit a wall stop and break it; Beaver
  Sappers do 3× damage to walls (and splash them); owls and slingers ignore them; walls don't count toward
  destruction %. Palisade wall art. New `scripts/raid-balance.ts` (full armies per Lodge level vs each tier,
  10 seeds). Tuning: Outpost +1 Spit Tower, Warren/Stronghold −1 mortar, Stronghold −1 spit, walls 320→220 hp,
  gentler tier scaling (hp +35%/tier, dmg +25%/tier). 92 tests.

- [x] **Iter 19** — **Field Guide + Settings (meta, part 1).** New `FieldGuideScene` (parchment book): tabs for
  **Enemies** (18 entries; unmet enemies show as "?" silhouettes until first seen in battle, "Discovered N/18"),
  **Towers** (4 towers + 8 branches) and **Heroes** (with training rank); each entry has art, stats (hp, speed,
  armor/MR %, lives, bounty, special tags) and a blurb. Battles record sightings (`seenEnemies`, saved
  immediately; "New in Field Guide!" popup). New `SettingsScene`: volume slider (drag or tap), sound on/off,
  two-tap **Reset progress** (keeps settings). Menu gets Field Guide + Settings buttons. **Bug fix:** top-tier
  tower textures were clipped at the top (84px canvas too short for roofs/orbs); now 100px. 95 tests.
  (Backlog reordered: meta features before the raid training queue, since the whole META pillar was missing.)

- [x] **Iter 20 — POLISH + BALANCE.** Structural: **per-wave health ramp** (`waveHpMult()`): a level's health bonus
  now ramps from 60% on wave 1 to 100% on the last wave (bounties follow), so late levels no longer open with
  brutal waves before the player has an economy. All level `hpMult`s rescaled (bonus × 1.3) to keep late-wave
  difficulty. Mobile polish: **"turn your phone sideways" overlay** in portrait on touch devices, **Fullscreen**
  button in Settings, no long-press context menu or text selection. 95 tests.

- [x] **Iter 21** — **Achievements (meta, part 2).** 17 achievements in `data/achievements.ts` (first win, perfect
  defense, stars 15/45, each boss, campaign complete, 500/5000 kills, 10 specializations, hero level 6,
  10 buildings, Grove Hall 3, first raid win, 3-star Stronghold, full Field Guide), each with a Coins/Glowsap reward
  paid into the village. Lifetime `stats` counters (`bumpStats`) are recorded at battle end (wins/losses), raid end
  and village building; `checkAchievements()` unlocks and pays out. Slide-in "Achievement" toasts in battle,
  raid and village; `AchievementsScene` lists all with progress bars; menu button. 98 tests.

- [x] **Iter 22** — **Daily challenge (meta, part 3).** `dailyFor(date, unlocked)` hashes the local date into one of
  the player's unlocked levels plus 2 modifiers (always at least one hard): Swift Horde (+30% speed), Thick Hides
  (+25% hp), Beaver Discount (−20% tower prices), Full Coffers (+50% coins), Clouded Sky (no spells), Hero on Leave,
  Thin Hedge (5 lives), Frenzy (waves twice as fast). New `Modifiers` in `BattleSim` (prices via `sim.price()`,
  sell refunds scaled, `maxLives` for stars). Menu card "Daily: <level>" with twists and reward; first win of the day
  pays +300…+1140 coins & glowsap (saved as `dailyDone`), replays allowed. Battle banner lists today's twists;
  spell buttons show as locked under Clouded Sky. Menu re-laid out (stars top-right, version bottom-right).
  4 new tests (102 total). **META pillar complete:** Field Guide, settings, achievements, daily challenge.

- [x] **Iter 23** — **Timed troop training.** Troops now train at the Ranger Lodge over time (Brawler 20s, Slinger 25s,
  Sapper 45s, Owl 60s), one after another; the queue (`trainQueue`, timestamps) keeps running while away.
  Glowsap is paid when queued and queued troops count toward army space (`totalArmySpace`). `tickTraining()` moves
  finished troops into the army. The raid panel shows "Training X: 12s (+N queued)", ready counts with "(+queued)",
  and train times on cards; Attack ticks the queue first and explains if troops are still training. Camp cards
  no longer count wall segments as buildings. Restored wall tests that an edit had dropped. 103 tests.

- [x] **Iter 24** — **Procedural background music** (`systems/music.ts`). A WebAudio lookahead scheduler plays a soft pad,
  bass and pentatonic arpeggio over a 4-chord loop, with three moods: **calm** (menu, map, village, guides; 78 bpm),
  **battle** (112 bpm, minor, kick + hats) and **boss** (132 bpm, tense progression), switching on a bar line. Battles
  flip to the boss mood while a boss is alive. Music has its own **Music: On/Off** toggle (`settings.music`) and follows
  the volume slider; the Settings screen was re-laid out (Effects / Music / Fullscreen). `scripts/music-check.mjs`
  verifies the music starts after a gesture and changes mood. 103 tests.

- [x] **Iter 25 — POLISH + BALANCE (economy).** Smarter raid deploy in `raid-balance.ts` (side nearest the defenses,
  sappers/owls first, brawlers 1s later, slingers 3s later; `--naive` keeps the old spread). New `scripts/economy.ts`:
  income (campaign, achievements, production per Grove Hall level, raid loot minus lost troops) vs spending (full
  build-out, hero training). Fix: Bramble Walls were an 84k-coin sink with no gameplay use → max 30 (was 80),
  40/120/300 coins (was 50/200/800); total build-out 179k → 109k coins. Music drops to the calm mood when a battle
  or raid ends. Campaign re-checked (no regressions). 103 tests.

- [x] **Iter 26 — Mobile touch targets.** New `ui/touch.ts` (+ pure `ui/hitpad.ts`): on coarse-pointer devices, hit
  areas grow toward 72 game px (≈42 CSS px on a phone), capped at 12 px per side so neighbours don't steal taps.
  Applied to every `Button`, build pads, the hero sprite, text options in the tower menu and the volume knob.
  Desktop hit areas are unchanged. New `scripts/mobile-check.mjs` (740×360, touch emulation) taps just outside a
  button edge and just outside a build pad, and both register. 106 tests.

- [x] **Iter 27 — Music polish.** New `data/musicThemes.ts`: moods plus 4 themes (Sanctuary for menus and the village,
  Grovelands, Frostfern, Emberdeep). Each theme transposes and re-tempos the mood loop, swaps arp/lead waveforms and
  adds a 2-bar lead motif every 4 bars (softer in calm). Battles pick the theme for their region; raids use Emberdeep.
  Victory and defeat stingers (fanfare / falling lament) rest the loop until they ring out; when music is off, the
  old short sfx jingle still plays. `music-check.mjs` now checks the region themes and that the stinger rests the
  loop. 111 tests.

- [x] **Iter 28 — Phone-readable labels.** On a phone the 1280×720 game renders at about 0.5×, so 12–14 px labels
  shrank to 6–7 CSS px. New `pf()` (pure `phoneFontSize`): on touch devices, labels under 18 px grow by up to 4 px
  (capped at 18). Applied to battle labels (spell names, hero skill, wave preview, spec names, tower menu) and the
  world map. `fitWidth()` shrinks a label back to fit its circle (the "Earthshake" skill name overflowed). Fix: the
  map's starting-point label sat under the first level's name on phones; moved it down. Village drag-to-pan dropped:
  FIT scaling already shows the whole grid. `mobile-check.mjs` now also captures the upgrade menu and map. 113 tests.

- [x] **Iter 29 — Region 4 opens: The Duskcap Weald.** A twilight forest of giant mushrooms beyond the Emberdeep.
  Two new enemy mechanics (20 enemies now): **Veilstalker** (`veil`: towers only target it within 105 px; splash,
  spells and soldiers still hit it, and it is drawn as a faint shimmer until a tower spots it) and **Rootrager**
  (`enrage`: double speed below 50% HP, red tint + "Enraged!"). Level 16 **Duskcap Verge** (2 roads, 11 pads, 15
  waves, `DUSK` theme with glowing-mushroom scenery), a Duskcap world-map style, and a hushed whole-tone music theme.
  The story ending is now tied to a `finale` flag on level 15 (it was "last level in the list"); the
  "Keeper of the Grove" achievement follows it. Fix: with 4 levels still to come, the 4th "?" placeholder on the
  world map was off-screen; placeholders now spread evenly. `balance.ts` takes an optional level filter. New
  `scripts/dusk-check.mjs`. 115 tests.

- [x] **Iter 30 — POLISH + BALANCE (16 levels).** Full campaign re-run (6–8 seeds × expert/casual/novice). Fixed three
  outliers: Glacier Hold hpMult 1.91 → 1.7 (expert was below casual), Obsidian Bridges 1.19 → 1.0 (expert only won
  17%), Heart of the Emberdeep 1.13 → 1.06 (finale: expert 88%). Polish: the Field Guide lists the new traits
  ("Veiled (towers see it within 105px)", "Enrages below 50% health"); checked that the 20-enemy grid still fits.
  `meta-check.mjs` now opens the Veilstalker entry. 115 tests.

- [x] **Iter 31 — Duskcap level 17 + Puffcap.** New enemy **Puffcap** (21 enemies): `sporeBurst` on death hastens
  nearby non-boss allies ×1.6 for 3 s (pink tint, spore cloud, "Spores! ×N"), so it pays to pop it away from the crowd.
  Level 17 **Glowspore Hollow**: long switchback plus a second road climbing up from the south and merging late,
  12 pads, 15 waves. Tuning found two spikes and fixed them: wave 6 mixed Puffcaps into fast Thornhogs (12-life leak
  for the novice), so the Puffcaps now trail behind; wave 5 Rootragers and the wave 6 Gnats moved to the long road.
  New test: no build pad may sit under the HUD (hero portrait/skill, spell buttons, top bar). It caught a Glowspore pad
  under the hero skill button and a Frostfern Pass pad under the wave preview (moved both). `dusk-check.mjs` now
  pops a Puffcap next to a Thornhog pack. 117 tests.

## In Progress
- (none)

## Backlog (ranked)
1. Region 4: levels 18–20 (a Duskcap boss with phases for level 20).
2. Village: a free speed-up after a 3-star win (parked idea).
3. Phone-readable text in Village and Achievements cards (needs a layout check for each card).

## Known Bugs
- (none known)

## Ideas parked
- Headless Chromium renders only a few FPS here, so live game time crawls in screenshots; scripts fast-forward sims.
- Village: "finish now" doesn't exist (no premium currency on purpose); maybe a free speed-up after a 3-star win.
- Village: drag-to-pan for small phone screens (the grid currently fits 1280×720).
- Pause menu with "Quit to map" / "Restart" (currently only via the end panel).
- Autoplayer should cast spells and move the hero (do this in the iteration-10 balance pass).

## Balance Notes
**Iteration 20** (`balance.ts 10`, after the per-wave ramp + rescale; expert/casual/novice):
L1 100/100/100 · L2 100/100/100 · L3 100/90/80 · L4 100/70/70 · L5 100/100/60 · L6 100/100/20 · L7 80/80/10 ·
L8 80/50/60 · L9 100/100/10 · L10 70/40/10 · L11 100/90/40 · L12 70/70/60 · L13 100/90/40 · L14 50/40/0 · L15 90/30/0.
- With the ramp alone (no rescale) almost every level got easier (Ashfall/Frostfern/Smoulder 100/100/100), as expected.
- Overall shape matches iteration 15, with gentler openings on late levels. Glacier Hold and Cinder Tunnels still
  let the novice keep up (merge maps favor Bramble at the choke); not worth more tuning until the AI can micro.

**Glowspore Hollow (iteration 31, 6–8 seeds):** at hpMult 2.4 → 83/50/0; the novice always died at wave 7 (trace showed
Puffcap-hastened Thornhogs plus Gnats on the short road). After the wave fixes: **2.2 → 88% / 100% / 0%** (8 seeds).
The novice still can't clear it even at 2.0: it fills only half the pads, so the late Veilstalkers on the merging road
slip past. That's acceptable for the region's second level.

**Campaign (iteration 30, 6 seeds unless noted; win % expert / casual / novice):**
| # | Level | hpMult | Expert | Casual | Novice |
|---|---|---|---|---|---|
| 1 | Mossgate Meadow | 1.00 | 100 | 100 | 100 |
| 2 | Gloomfen Edge | 1.32 | 100 | 100 | 100 |
| 3 | Thornwood Hollow | 1.65 | 100 | 100 | 67 |
| 4 | Mirelake Crossing | 1.19 | 100 | 50 | 67 |
| 5 | Murkmaw's Den | 1.84 | 100 | 100 | 50 |
| 6 | Frostfern Pass | 2.30 | 100 | 100 | 33 |
| 7 | Icicle Crossing | 1.58 | 83 | 83 | 17 |
| 8 | Glacier Hold | 1.91 → **1.7** | 50 → 83 | 67 → 83 | 50 → 50 |
| 9 | Rimewood Hollow | 2.50 | 100 | 100 | 17 |
| 10 | Frostpeak Summit | 1.98 | 67 | 50 | 17 |
| 11 | Ashfall Gate | 2.04 | 100 | 83 | 33 |
| 12 | Cinder Tunnels | 1.91 | 83 | 67 | 50 |
| 13 | Smoulder Fields | 2.69 | 100 | 83 | 50 |
| 14 | Obsidian Bridges | 1.19 → **1.0** | 17 → 88* | 17 → 75* | 0 → 0* |
| 15 | Heart of the Emberdeep | 1.13 → **1.06** | 67 → 88* | 33 → 38* | 0 → 13* |
| 16 | Duskcap Verge | 2.40 | 100 | 83 | 33 |
(* 8 seeds.) The novice can't clear Obsidian Bridges even at hpMult 0.8 (its bridges need focused anti-air/armor
picks), which is acceptable for the 14th level. Curve: each region opens easier than the previous region's end and
ramps up to its boss.

**Duskcap Verge (iteration 29, 6 seeds, expert / casual / novice):** hpMult 1.2 → 100/100/100 with ~20 lives (far too
easy); 2.0 → novice still 100%; **2.4 → 100% / 83% / 33%** (picked: matches the Emberdeep opener); 2.8 → novice 0%.

**Economy (iteration 25, `economy.ts`):**
- Income: campaign first clears 18.8k coins / 14.9k glowsap (+13.1k / +10.4k for all 3★); achievements 9.1k / 9.8k;
  production with maxed producers 1.4k/h (Grove Hall 1) → 3.3k (GH2) → 6.4k (GH3) → 11k (GH4) → 13.2k/h (GH5) of each.
- Raids (smart deploy) net after lost troops: Lodge 1 vs Outpost ≈ +600c +220s; Lodge 2 vs Warren ≈ +1.5k c +0.9k s;
  Lodge 3 vs Warren ≈ +1.6k c +1.0k s. With ~10–15 min of training per full army that's about 4k/h: on par with GH3
  production, so raids are worthwhile but not dominant.
- Spending: full build-out ≈ 109k coins + 66k glowsap, plus 32k glowsap of hero training. Campaign + achievements
  cover roughly the first third; production and raids carry the rest.
- Smart deploy vs naive (Lodge 3 vs Stronghold): 1.5★ vs 0.9★, so raid tactics are rewarded.

**Raids (iteration 18, `raid-balance.ts`, avg stars / destruction over 10 seeds, two-side deploy):**

| Army | Mudling Outpost | Bogscum Warren | Murkhorde Stronghold |
|---|---|---|---|
| Lodge 1 (10 space) | 1.8★ 69% | 0.4★ 41% | 0.0★ 36% |
| Lodge 2 (20 space) | 3.0★ 100% | 2.0★ 76% | 0.2★ 47% |
| Lodge 3 (30 space) | 3.0★ 100% | 2.9★ 98% | 0.9★ 59% |

Each lodge level has a "fair" camp (~2★), and the Stronghold is a stretch goal. Before tuning: Outpost 2.8★ with
Lodge 1 (trivial), Warren 0.9★ with Lodge 2.

**Iteration 16 — Emberdeep finale** (`balance.ts 8–10`):
13 Smoulder Fields 100/88/0 · 14 Obsidian Bridges 50/30/0 · 15 Heart of the Emberdeep 90/30/0 (expert/casual/novice).
- First drafts were walls (0% for everyone by wave 4–5). Root causes found with per-leak logs: chained freezes
  (fixed with thaw immunity), uncapped hive spawns (capped at 6), a too-short straight lane on Obsidian Bridges
  (now has a dip), no pads beside Heart's top road (added 2), and an overtuned final boss (5000 → 3200 hp).
- The level-wide `hpMult` also makes early waves harsh on late levels; a per-wave ramp might be cleaner later.

**Iteration 15** (`balance.ts 10`, smart expert):

| Level | expert | casual | novice |
|---|---|---|---|
| 1 Mossgate Meadow | 100% | 100% | 100% |
| 2 Gloomfen Edge | 100% | 100% | 100% |
| 3 Thornwood Hollow | 100% | 90% | 90% |
| 4 Mirelake Crossing | 100% | 80% | 80% |
| 5 Murkmaw's Den | 100% | 90% | 70% |
| 6 Frostfern Pass | 100% | 100% | 30% |
| 7 Icicle Crossing | 100% | 80% | 0% |
| 8 Glacier Hold | 90% | 40% | 50% |
| 9 Rimewood Hollow | 100% | 100% | 30% |
| 10 Frostpeak Summit | 80% | 70% | 10% |
| 11 Ashfall Gate | 100% | 90% | 10% |
| 12 Cinder Tunnels | 70% | 60% | 60% |

- With choke-point heroes and level-aware branches the expert is now clearly the strongest on 10/12 levels,
  which suggests the earlier "novice ≈ expert" finding was mostly an AI problem, not a game problem.
- hpMult is very sensitive on merge maps (Glacier/Cinder: 1.6 → 1.85 took the expert from 90% to 40–60%).
- Region 1 stays a gentle on-ramp on purpose; difficulty is driven by regions 2–3.

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
