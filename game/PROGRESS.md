# Grovewatch: Sanctuary Siege — Progress

An original tower-defense + village-building game. The **Keepers of the Grove** defend their
woodland sanctuary from the **Murkhorde**, bog critters creeping out of the Gloomfen.
Resources: **Coins** (battle currency / village gold) and **Glowsap** (the second village resource, planned).

Run: `npm run dev` · Build: `npm run build` · Tests: `npm test` · Smoke test + screenshots: `npm run build && node scripts/screenshot.mjs <name>` · Balance report: `npx vite-node scripts/balance.ts [runs]` · Branch damage benchmark: `npx vite-node scripts/spec-bench.ts` · Raid balance: `npx vite-node scripts/raid-balance.ts [--naive]` · Economy report: `npx vite-node scripts/economy.ts`

Iteration counter: **103** (next balance pass at iteration 105)

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

- [x] **Iter 32 — Duskcap level 18: Mirrorpool Glade.** Three roads: two from the west skirt a glowing pool and merge
  in the glade, and a third winds up from the south and joins the tail. 13 pads, 16 waves. Tracing leaks found a layout trap:
  nearly every pad sat 120 px from a road, just outside the Veilstalker's 105 px veil, so towers barely saw them.
  Fix: five pads moved to about 90 px, and the southern road lengthened (about 1280 → 1760 px) with a pad added. New
  reusable `scripts/level-shot.mjs <name> <levelIndex>` (builds every pad, plays 3 waves, screenshots). 117 tests.

- [x] **Iter 33 — Duskcap level 19: Hollowroot Switchback.** One long road (about 3,440 px) that doubles back three
  times. Pads between the rows sit about 100 px from both neighbouring roads (inside Veilstalker reveal range), plus an
  outer row. 12 pads, 16 heavy waves mixing every Duskcap enemy. First tuning try worked; no layout fixes needed.
  117 tests.

- [x] **Iter 34 — Duskcap finale: Morrowcap's Throne (level 20).** New boss **Matriarch Morrowcap** (22 enemies): heals
  nearby allies (and herself) every 4 s, releases Puffcaps (14 at most), and has four phases (Veilstalker mist → spore-bark
  shield + Rootragers → scattered Puffcaps + haste → final lurch). Level 20: two roads that merge, 12 pads, 18 waves,
  boss on the last wave. The Duskcap Weald now has all 5 levels (20-level campaign). New achievement **Weald Warden**
  (18 total). Fix: a pad near the top edge put a tower behind the speed/next-wave buttons; replaced it.
  `level-shot.mjs` takes a boss id and drives it through its phases; new `scripts/enemy-sprites.mjs` renders sprites
  close up. 117 tests.

- [x] **Iter 35 — POLISH + BALANCE (20 levels).** Full campaign re-run. Fixed two outliers: Frostpeak Summit hpMult
  1.98 → 1.75 (the Frostfern boss had expert at 50%, below every later boss) and Mirrorpool Glade 1.8 → 1.65 (casual was
  50%, below the next level; the novice now wins some runs). Economy re-check: with 20 levels, campaign + achievements
  pay about 65k coins / 55k glowsap against a 109k / 99k full build-out. Polish: Achievements screen pages (new pure
  `ui/paging.ts`, `<`/`>` buttons, "1/2" label), plus a 19th achievement **Mistwalker** (3★ on every Duskcap level).
  `ach-check.mjs` clicks through the pages. 119 tests.

- [x] **Iter 36 — Swiftbloom speed-ups.** Taking a level to 3★ for the first time grants a **Swiftbloom** (hold at most
  3; data in `SWIFTBLOOM`). Each one cuts 1 hour off a building under construction; the village tick then finishes it
  if due. Pure rules `grantSwiftbloom` / `rushBuilding` in `systems/village.ts` (stored on `VillageState.swiftblooms`, so
  old saves just start at 0). The victory panel shows a pink "+1 Swiftbloom"; the building panel shows a
  "Swiftbloom (N)" button while it is under construction. One per level means at most 20 in a playthrough, so they
  can't be farmed. Fix: the construction progress bar now clamps to 0–1 (a long timer drew an orange bar across half
  the village). New `scripts/swift-check.mjs`: a 3★ win grants the token, then real clicks rush a Grove Hall upgrade.
  122 tests.

- [x] **Iter 37 — Phone-readable Village, Achievements and Menu text.** `pf()` applied to the small labels in the Village
  (badges, building panel, shop cards, troop and raid panels), Achievements cards, Menu (daily line, version) and
  achievement toasts. New `scripts/phone-screens.mjs` (740×360, touch) screenshots each screen; it found and fixed three
  overflows: the shop's "Defense Workshop" name and its two-part cost ran into the count (the name now shrinks to fit,
  and costs read "500c + 300s"); the Mistwalker description ran under its progress bar (descriptions shrink to the free
  width); the Menu hero description overflowed its panel (kept at desktop size). Desktop layouts re-checked.
  122 tests.

- [x] **Iter 38 — Endless mode.** Any beaten level's map card has an **Endless** button. `systems/endless.ts` turns the
  map into 200 seeded, generated waves (`data/endless.ts`): the enemy pool grows in tiers (waves 1/4/8/12/16), a boss
  every 10th wave (Murkmaw → Grimtusk → Vulkhar → Morrowcap), a per-wave HP budget, and a new `LevelDef.endless.hpRamp`
  (+7% enemy health per wave, bounties too). HUD shows "n/∞" and "Endless wave n". The result panel shows waves held,
  new best or best on this map, and a village payout (12c + 12s per wave). Best runs go to `save.endlessBest`, and endless
  never records stars. Retry and pause → Restart stay in endless. New achievement **Unending Vigil** (25 waves; 20 total).
  New `scripts/endless-balance.ts` and `scripts/endless-check.mjs` (real click on the card's Endless button). 127 tests.

- [x] **Iter 39 — Region 5 opens: The Saltmarrow Shoals.** A sandy coast of sandbars and tide pools. Two new enemy
  mechanics (24 enemies): **Barnaclad** (`brittle`: 75% armor that drops 5 points with every hit taken, so fast towers strip
  it; a grey crust bar shows what's left) and **Gullwing** (`swoop`: a flyer that lands for 1.6 s every 3 s, when
  ground-only towers and soldiers can reach it; soldiers let go when it takes off). Enemies now carry runtime `armor`,
  and all flyer checks go through `sim.airborne(e)`. Level 21 **Wrackline Beach** (2 roads, 12 pads all about 100 px
  from a road, 15 waves), `SHOAL` theme, a shoal world-map style (shells, pebbles, dune grass, lagoon) and a lilting
  Saltmarrow music theme. 129 tests.

- [x] **Iter 40 — POLISH + BALANCE (21 levels + heroes).** The campaign curve was healthy (every level ≥ 83% for the
  expert), so this pass looked at heroes. Investigating why the novice outlasted the expert in endless showed the hero is
  the deciding factor: on hard levels, expert wins were Fen 95% / Ember 60% / Bramble 35%, and **Obsidian Bridges was
  effectively Fen-only** (two lanes that never merge, and only Fen's 190 px range covers both from the hero spot).
  Fixes: two pads between Obsidian's lanes (hpMult 1.0 → 1.15); Icicle Crossing's big Thornhog waves split across both
  roads (hpMult 1.58 → 1.7); autoplayer `adaptiveMix` is now hero-aware (more anti-air when the hero can't hit flyers);
  Ember: bolt 18 → 22 damage, Warm Glow 20% → 25%; Bramble: hit 14 → 18, Earthshake 60 → 70 damage / 110 → 115 px;
  Murkmaw's Den 1.84 → 1.95 so the buffed Bramble doesn't trivialise it for novices. Hero win rates on hard levels now
  Fen ~80–95% / Ember 75% / Bramble 35–55%. 129 tests.

- [x] **Iter 41 — Shoals level 22 + Reefwarden.** New enemy **Reefwarden** (25 enemies): `shieldAura` coats nearby
  non-boss allies in a coral shield (40 × the wave HP multiplier) every 5 s (pink ring), so it's a priority target. Level 22
  **Tidepool Terraces**: a long zigzag road plus a short northern road that merge, 13 pads, 16 waves. Tuning found the
  first layout was undefendable: the merged tail was only 420 px, so it now bends down to the lower right (+260 px),
  with 2 pads moved. Thornhog and Gullwing spikes trimmed. 130 tests.

- [x] **Iter 42 — Shoals level 23: Saltspray Fork.** One road off the beach splits into two mirrored lanes running to
  two different gates. Middle-band pads sit about 110 px from both lanes, and the hero starts on the shared stretch
  before the split. 12 pads, 16 waves using all three Shoals enemies plus a few Duskcap guests. Tuned on the first try
  (leaks spread out, no spikes). Fix: the north exit at y=120 put its gate marker under the Next Wave button; that lane
  now runs at y=150. New test: no road exit may put its gate under the top-right buttons. 131 tests.

- [x] **Iter 43 — Shoals level 24: Wreckspiral.** One road (about 4,700 px) spirals inward around an old shipwreck to a
  gate at the centre of the map. 12 pads in the bands between rings (70–90 px from each road), 16 heavy waves mixing all
  Shoals enemies with Duskcap and Murkhorde guests. Fix: the outer ring started at y=100, under the top HUD, so enemies
  and flying gulls hid behind the stats bar; rings moved to y=130/270. New test: no horizontal road above y=120.
  132 tests.

- [x] **Iter 44 — Shoals finale: Saltjaw's Grotto (level 25).** New boss **Saltjaw the Tidecrab** (26 enemies): 80%
  armor that is itself `brittle` (0.4 points per hit, so sustained fire cracks it), sheds Gullwings (16 at most), and has
  four phases (Barnaclad shell-kin → coral crust shield + Reefwardens → a gull swarm + haste → a final scuttle for
  the gate). Level 25: two roads merging into a 1,360 px shared tail, 12 pads, 18 waves, boss on the last wave.
  **The Saltmarrow Shoals is complete: 25 levels in 5 regions.** New achievement **Tide Turner** (21 total). Boss phases
  checked in-browser (phase 2 reached, coral shield 1,178). 132 tests.

- [x] **Iter 45 — POLISH + BALANCE (25 levels).** Full campaign re-run: every level ≥ 83% for the expert. Each region
  opens easier than the last one ended and ramps to its boss. One tweak: Morrowcap's Throne hpMult 2.4 → 2.47 (it had
  slipped to 100/83/0; now 75/50/0, level with Saltjaw). Polish: endless mode adds the Shoals enemies (Barnaclad,
  Gullwing and Reefwarden from wave 20) and Saltjaw to the boss rotation; endless runs still end at waves 10–30. The
  Field Guide holds 26 of 30 grid cells, and a new test fails past 30 so paging gets built first. 133 tests.

- [x] **Iter 46 — Region 6 opens: The Shardglass Barrens.** A twilight desert of glass dunes and crystal spires. Two
  new enemy mechanics (28 enemies): **Shardskipper** (`blink`: jumps 90 px ahead every 3.5 s and breaks free of any
  blocker, with a streak effect) and **Mirrorback** (`splashResist` 0.8: area shots barely scratch it, so it wants
  focused single-target fire). Level 26 **Glassfall Flats** (2 roads merging into a 1,280 px tail, 12 pads about 100 px
  from roads, 15 waves), a `GLASS` theme with crystal-spire scenery, a Shardglass world-map style and a bell-like
  music theme built on fourths. 135 tests.

- [x] **Iter 47 — Shardglass level 27 + Glarefly.** New enemy **Glarefly** (29 enemies): a glass moth (flyer) that
  flashes on death and dazzles shooting towers within 120 px for 2 s. It reuses the frozen state and the 3 s immunity
  window, so flashes can't chain; soldier dens are unaffected. Kill it before it reaches your towers. Level 27 **Prism
  Canyon**: a doubling-back west road plus a north road joining late, 12 pads, 15 waves. Fix found by the region rules:
  the merged tail was only 420 px, so it now bends down to the lower right (680 px). Sprite polish: the first
  Glarefly's wings were thin, dark triangles; they're now broad, pale four-point wings. 136 tests.

- [x] **Iter 48 — Shardglass level 28: Shattered Crossroads.** Three roads (west, southwest, north) merge into a 1,160 px
  shared tail that dips south and exits east, kept clear of the spell buttons. 11 pads about 100 px from the roads,
  16 waves mixing all three Shardglass enemies with guests from earlier regions. It followed the region recipe, so no
  layout fixes were needed. 136 tests.

- [x] **Iter 49 — Shardglass level 29: Glassteeth Ladder.** One road (about 3,300 px) zigzags up and down five glass
  columns, with pads between the columns, 16 heavy waves and a final wave trimmed so it isn't a wall. Fixes from the
  screenshot: the road first entered from the top at x=140, behind the stats panel. New test: top entries must come
  down in the gap between the stats panel and the buttons (x 470–830). It caught two existing maps, now fixed: Tidepool
  Terraces' north road came down at x=1100, under Next Wave (now x=720, hpMult 1.9 → 1.4), and Shattered Crossroads'
  at x=900, under Pause (now x=800). Autoplayer: `adaptiveMix` now builds fewer splash towers when splash-resistant
  enemies are a big share of a level's health. 137 tests.

- [x] **Iter 50 — POLISH + BALANCE (29 levels).** Full campaign re-run: every level except one stays ≥ 83% for the
  expert, and every region ramps to its boss. Saltjaw's Grotto had slipped (expert 50–63% at 2.25; the curve is very
  steep there), so hpMult is now 2.2 (2.15 → 100/75/0). Polish: the Field Guide pages (30 per page, `<`/`>` beside the
  count, reusing `ui/paging.ts`), so the 30-slot grid is no longer a ceiling; the capacity test now checks every enemy
  lands on exactly one page. New `scripts/guide-paging-check.mjs` inflates the list in-browser and flips pages with real
  clicks. 137 tests.

- [x] **Iter 51 — Shardglass finale: Kaleidrax's Spire (level 30).** New boss **Kaleidrax, the Shattered Colossus**
  (30 enemies): 50% splash resistance, blinks 60 px every 12 s, sheds Shardskippers (16 at most), and has four phases
  (Mirrorback shards → a light-wall shield + Glareflies → a skipper storm + haste → a final lunge). Level 30: two roads
  (a west road, and a north road that enters through the HUD gap at x=520) merging into a 1,360 px tail, 13 pads,
  18 waves. **The Shardglass Barrens is complete: 30 levels in 6 regions.** New achievement **Shatterer** (22 total).
  Endless adds the Shardglass enemies from wave 24 and Kaleidrax to the boss rotation. Fixes: the first-draft boss was
  unbeatable (3,600 HP, blinking every 9 s; now 2,800 HP every 12 s), and two north pads put towers under the boss bar
  (moved down). The autoplayer weighs a splash-proof boss's HP ×3 when choosing its tower mix. 137 tests.

- [x] **Iter 52 — Hero #4: Wren, the Owl Lorekeeper.** A ranged magic hero who hits flyers. New passive kind
  `bounty` (**Scholar's Eye**: enemies that fall within 200 px of her pay 30% more coins; `sim.bountyMult`). Active
  **Hush** (a `ring` with an 80% slow for 3 s and light damage; enemies all but stop). New `HeroActive.fxColor`, so
  Hush draws a pale moonlight ring instead of Ember's foxfire gold. A hand-drawn barn-owl sprite with a scroll satchel.
  She appears automatically in the hero picker, Field Guide and village training. Hero win rates on hard levels:
  Fen 85% / Ember 75% / **Wren 75%** / Bramble 35%. 138 tests.

- [x] **Iter 53 — Third global spell: Thornsnare.** New spell kind `snare` (instant): brambles burst from the road,
  dealing 30 damage and rooting ground enemies within 95 px (a 75% slow for 3 s); flyers are unaffected. Cooldown 55 s
  (first tuned at 40 s / 90% slow, which made bosses too easy). It has a THREE hotkey, a vine-coil icon and a bramble-burst
  effect. The spell bar grows to three buttons, so the HUD clearance test's spell zone widened to x ≥ 1000; it caught
  two pads now under the third button (Mossgate Meadow, Saltjaw's Grotto; both moved). The autoplayer casts Thornsnare
  on the densest clump of walkers. New `scripts/snare-check.mjs` (real clicks: arm the button, tap a crowd, 5 walkers
  rooted, the flyer not). 138 tests.

- [x] **Iter 54 — Bramble rework (part 1): Shield Toss.** New optional hero attack `toss`: every 2.5 s Bramble flings
  his bark shield at the nearest flyer within 160 px (34 dmg × hero level multiplier, hits air), even while he brawls on
  the ground. That gives the melee tank his first answer to flyers. Shown in his blurb and on the Field Guide hero page.
  The autoplayer now counts a toss as hitting air when choosing anti-air. Expert wins with Bramble on hard levels go from
  35% to about 40–45%; Heart of the Emberdeep 1/6 → 3/6. Icicle Crossing stays his worst map (two crossing roads that
  only a ranged hero can cover from the crossing). New `scripts/toss-check.mjs`. 139 tests.

- [x] **Iter 55 — POLISH + BALANCE (30 levels, with Thornsnare + Wren + Shield Toss in play).** The new tools made the
  campaign a little easier across the board (novice win rates rose on most levels). Two levels had become trivial
  (100/100/100): Wrackline Beach hpMult 2.4 → 2.8 (100/100/50) and Tidepool Terraces 1.4 → 1.55 (100/75/100; Bramble
  suits that converging map). Every other level still meets its region target. Polish: when a spell is armed, a hint
  panel above the spell bar shows what it does and its recharge. Fix: arming Thornsnare said "Tap where the star should
  fall"; each spell kind now gets its own instruction. `snare-check.mjs` also screenshots the armed state and asserts
  the hint. 139 tests.

- [x] **Iter 56 — Bramble rework (part 2): Bulwark.** New melee-hero trait `bulwark`: Bramble holds 2 enemies at once
  from hero level 3 and 3 from level 5 (`sim.heroHolds`; extra free ground enemies within reach get pinned while he
  brawls). It's listed on the Field Guide hero page. Endless levels now carry `heroRegen` (0.5); halving regen, or
  even cutting it to 20%, didn't dent Bramble's endless lead, which comes from blocking. Results: expert wins with Bramble
  on hard levels **40% → 60%**, Icicle Crossing 1/6 → 4/6. Side effect: the novice (Bramble) got much stronger early, so
  Murkmaw's Den hpMult goes 1.95 → 2.3 (83/67/67); a full retune at iteration 60. 140 tests.

- [x] **Iter 57 — Endless hero balance.** In endless, enemy melee hits now ramp with the wave (`endless.attackRamp`,
  +15% per wave; `sim.attackMult()`, 1 in the campaign), so a blocker can't stall forever. Endless waves held by the
  expert: Bramble 31.7 → **16.5**, Fen 16.7 → 13.2, Ember 18.2 → 14.7, Wren 15.0 → 13.3 (8% per wave only narrowed it
  to 21 vs 14). Typical runs now end at waves 12–22, and the novice-over-expert oddity mostly went away. 141 tests.

- [x] **Iter 58 — Endless daily mutator.** Every endless run that day gets one modifier picked by date from
  `ENDLESS.mutators` (Swift Horde, Thick Hides, Beaver Discount, Full Coffers, Clouded Sky, Frenzy; no hero-less or
  5-life days). Hard mutators pay ×1.5 village coins and glowsap per wave. It's shown on the map card ("Best N • Today:
  …"), in the endless start banner and on the result panel. `endlessMutatorFor` / `mutatorReward` in `systems/endless.ts`
  (reusing the daily hash). Fix: Clouded Sky said "No Starfall or Grove Call", outdated since Thornsnare; now "No global
  spells." 143 tests.
- [x] **Iter 59 — Field Guide Spells tab.** A fourth tab lists Starfall, Grove Call and Thornsnare with their icon,
  description and facts built from data by `spellFacts` in `systems/spellInfo.ts` (damage/radius/delay, summoned
  soldiers' stats, snare slow, recharge, hotkey), plus a short how-to-cast note. Tab buttons narrowed to fit four.
  Browser check `scripts/guide-spells-check.mjs` taps the real tab. 145 tests.
- [x] **Iter 60 — POLISH + BALANCE pass.** Full sweep (`balance.ts 6`, then 12–16 seeds on outliers). Saltjaw's
  Grotto had a wall at waves 6–8 (10 Shellbacks under coral + 20 Gnats, then Splotches) that killed half of expert runs
  before the boss; trimmed those two waves and raised hpMult 2.2 → 2.55 so the boss is the real test. Heart of the
  Emberdeep hpMult 1.06 → 1.03 (casual was 17–25%). Screenshot `60.png` (Saltjaw fight).
- [x] **Iter 61 — Region 7 opens: The Galecrest Aeries.** Windswept cliffs above the clouds. Two new enemy mechanics
  (32 enemies): **Galehound** (`windborne`: immune to every slow; all slows now go through one `sim.slow()` helper) and
  **Cloudram** (`regen`: once unhit for 2 s it regrows 6% max health per second, shown by drifting green pluses).
  Level 31 **Windgap Ledge** (west + north roads merging into an 800 px tail, 12 pads, 15 waves, hpMult 1.7), a `GALE`
  theme (wind-bent pines, stone cairns, drifting clouds), a sky-blue world-map style and a soaring music theme. Endless
  adds both enemies from wave 28. Field Guide tags for both traits.
  **Bug fixes:** (1) battle music was off by one region for regions 4–6 (Duskcap played the Shoals tune, the Shoals
  played Shardglass, Shardglass played Duskcap): `themeForRegion` indexed the THEMES list, which isn't in region order;
  it now uses an explicit `REGION_THEMES` list, and a test checks each region's theme matches its flag. (2) Fen's crit
  used `Math.random()`, so autoplay "seeds" didn't replay and balance numbers were noisy (casual on Windgap Ledge read
  38% one run and 100% the next). The sim now takes an optional `random` source; `playLevel` passes a seeded one; a
  test checks the same seed replays exactly. Browser check `scripts/gale-check.mjs`. 149 tests.
- [x] **Iter 62 — Galecrest level 32 + Kitewing.** New enemy **Kitewing** (33 enemies): a sky-ray flyer with `gust`:
  every 5 s it blows free walkers within 110 px 45 px further along their road (held enemies, flyers and bosses don't
  budge, so blockers are the counter), shown as a wind ring plus streaks. Level 32 **Updraft Stair**: a switchback west
  road and a second road rising from the south, 13 pads, 15 waves, hpMult 1.4. First draft was unwinnable for casual:
  the south road reaches the shared tail after only 620 px, so its fast packs moved to the long road, wave 5's
  Gullwings and wave 7's Thornhogs were trimmed, and a pad was added by the south entry. Endless adds Kitewing from
  wave 28. Browser check `scripts/kite-check.mjs`. 150 tests.
- [x] **Iter 63 — Galecrest level 33: Spiral Gale.** One 3,200 px road loops round a mesa and crosses its own earlier
  stretch at (600, 240), so pads by the crossing cover the road twice. 13 pads, 16 waves mixing all three Galecrest
  enemies with guests. Long single roads are generous (1.8 was 100/100/92), so it sits at hpMult 2.6. Screenshot
  `63.png`. 150 tests.
- [x] **Iter 64 — Galecrest level 34: Three Winds.** West, north and south roads merge into one tail (two merge points;
  the west and north roads run 180 px apart with pads between them). 13 pads, 16 waves, hpMult 1.55. First draft was
  unwinnable (25/0/0 at 1.8): the north road is only 1,100 px, and Cloudrams there never took steady enough fire to stop
  regrowing, so Cloudrams and Bogbrutes now stay off it and the late south Galehound packs were trimmed. Screenshot
  `64.png`. 150 tests.
- [x] **Iter 65 — POLISH + BALANCE (34 levels, first sweep with the deterministic sim).** 12 seeds per level and
  player. Retuned three outliers: Murkmaw's Den 2.3 → 2.45 (boss was 100/75/83), Frostpeak Summit 1.75 → 1.85 (boss
  was 100/67/67), Cinder Tunnels 1.91 → 1.75 (expert was 75%). Endless still holds 12–22 waves. Screenshot `65.png`.
- [x] **Iter 66 — Galecrest finale: Roc's Aerie (level 35) + Zephyrax, the Gale Roc.** New boss (34 enemies), built
  from existing traits: a flyer that swoops down to land for 3.5 s every 4 s (blockers and ground towers get their
  window), `windborne` (no slows), `gust` (wingbeats shove the herd 50 px), and four phases (kitewings → thundercloud
  shield + cloudrams → a pack of galehounds → a dive). Level 35: west + north roads merge into a 1,160 px tail, 12 pads,
  18 waves, hpMult 1.95. Achievements **Stormbreaker** (beat Zephyrax) and **Cloudwalker** (15 stars in the Aeries):
  24 total. Zephyrax joins the endless boss rotation. Autoplayer: a flying boss counts triple when picking the tower mix
  and makes the smart player branch archers into Hawkeye (big single shots); before that the expert lost to the roc
  more often than the novice. Screenshot `66.png`. 150 tests.
- [x] **Iter 67 — Field Guide boss phases.** Boss pages list each phase under the stats ("At 50%: shield 1200, summons
  3 Cloudram"), built from data by `bossPhaseLines` in `systems/guideInfo.ts`. **Fix:** the detail text wrapped at
  540 px starting from x=750, so long trait lines ran off the parchment (edge at 1240); every enemy with several traits
  was clipped. Now 470 px. Browser check `scripts/guide-boss-check.mjs <name> [bossId]` checks every text fits; all
  seven bosses do. 151 tests.
- [x] **Iter 68 — Region 8 opens: The Verdant Ruins.** A jungle swallowing an old temple road. Two new enemy mechanics
  (36 enemies): **Shiftscale** (`shift`: every 4 s swaps between hard scales, 70% armor / 0 MR, and slick skin,
  0 armor / 70% MR; enemies now carry a runtime `mr` next to `armor`) and **Idol Keeper** (`revive`: every 6 s raises
  the latest ally that died within 140 px in the last 8 s at 50% health; risen enemies glow pale gold, pay no bounty and
  can't rise twice). Level 36 **Overgrown Causeway** (west + north roads, 1,160 px tail, 11 pads, 15 waves, hpMult
  1.4), a `RUINS` theme (palms, vine-wrapped pillars), a jungle world-map style and a hand-drum music theme. Endless adds
  both from wave 32. First draft lost to the short north road again (armored packs moved to the long road).
  `sim.res()` is now public. Browser check `scripts/ruins-check.mjs`. 153 tests.
- [x] **Iter 69 — Ruins level 37 + Bramblehide.** New enemy **Bramblehide** (37 enemies): a vine-grown temple boar with
  `thorns` 0.5: soldiers and heroes that hit it in melee take half the damage they deal back (green thorn sparks);
  ranged attacks are safe. Level 37 **Sunken Stairs**: west + south roads of similar length (760 / 640 px to the merge)
  meeting on a causeway, 13 pads, 15 waves, hpMult 1.5; early Shiftscale packs trimmed (casual died at wave 7).
  **Fix from the screenshot:** towers on two pads hid behind the stats panel / poked into the speed buttons. New test:
  a tower (about 75 px tall) must clear the stats panel and the top-right buttons. It caught 8 pads in 7 levels
  (Mossgate Meadow, Gloomfen Edge, Glacier Hold, Windgap Ledge, Updraft Stair, Three Winds ×2, Sunken Stairs), all
  moved down or sideways and re-checked for road clearance. 155 tests.
- [x] **Iter 70 — POLISH + BALANCE (37 levels).** Full deterministic sweep (12 seeds): every level is in its band and
  no hpMult changed. Three Winds' novice at 50% is the blocker-at-a-merge quirk (raising hpMult to 1.62 only cut casual
  67 → 42%, so it stays at 1.55). Polish: new phone check `scripts/phone-late.mjs` (740×360 touch: region 8 map, a Ruins
  battle, Field Guide spells + boss page), all clean; boss phase lines use the phone font size. Playable demo published
  as an artifact.
- [x] **Iter 71 — Ruins level 38: Serpent Terraces.** One 3,560 px road snakes across three terraces (y 160 → 340 →
  520) with pad rows between the coils, so each pad covers two stretches. 12 pads, 16 waves, hpMult 1.65. The first
  draft lost to Shiftscale + Idol Keeper packs in waves 5–9 (trimmed). Autoplayer: a shifter now counts half armored,
  half magic-resistant when picking the tower mix (it was read as purely armored, so the expert over-built magic
  towers that bounce off the slick form). Screenshot `71.png`. 155 tests.
- [x] **Iter 72 — Ruins level 39: Idol Courtyard.** A west road and a north road that detours round the shrines
  (1,220 / 960 px to the merge) meet before an 800 px tail. 12 pads, 16 waves, hpMult 1.22. First draft was 25/0/0 at
  1.4: wave 1's eight Shiftscales overran the opening gold, and waves 4–7 stacked fast packs on the north road; both
  thinned. Screenshot `72.png`. 155 tests.
- [x] **Iter 73 — Ruins finale: Heart of the Ruins (level 40) + Ulmaroth, the Overgrown Idol.** New boss (38 enemies)
  built from the region's traits: `shift` (stone 60% armor ↔ moss 60% MR every 6 s), `thorns` 0.3, `revive` (raises
  fallen allies within 180 px at 60%), and four phases (bramblehides → stone shell + idol keepers → a flood of
  shiftscales → a lurch for the gate). Level 40: a long west road and a short north road (light groups only) merge into a
  1,240 px tail, 12 pads, 18 waves, hpMult 1.56. Achievements **Idolbreaker** and **Pathfinder** (26 total); Ulmaroth
  joins the endless boss rotation. Region 8 complete: 40 levels. Screenshot `73.png`. 155 tests.
- [x] **Iter 74 — Village zoom + drag-to-pan.** A "Zoom in / Zoom out" button (above Build) zooms the village 1.7×;
  while zoomed, dragging anywhere pans (clamped to the village), and a tap only counts on release if the finger didn't
  move, so panning never opens a building by accident. A second, fixed camera draws everything at depth ≥ 900 (HUD,
  panels, toasts) so the UI never zooms; floating "+coins" text moved to the world layer. Placing/moving buildings uses
  the camera's world point, so it stays exact when zoomed. Browser check `scripts/village-zoom-check.mjs` (real button,
  real drag, tap on the moved Town Hall, zoom out); existing village/phone checks still pass. Screenshot `74.png`.
- [x] **Iter 75 — POLISH + BALANCE.** Sweep of levels 31–40 (12 seeds; 1–30 unchanged since iteration 70 and untouched
  by the autoplayer changes): all in band, no retunes. Endless holds 11–21 waves with Zephyrax and Ulmaroth in the boss
  rotation. Polish: twelve enemy traits were silent (gust, swoop, revive, shift, blink, thorns, glare, coral, spores,
  enrage, burrow, split); each now has a short, throttled WebAudio cue via `sfx.trait(kind)`. `window.__sfx` test
  handle; `scripts/sfx-check.mjs` unlocks audio with a click and plays every cue (context running, no errors).
- [x] **Iter 76 — Region 9 opens: The Brasswork Hollows.** An underground machine city of brass and steam. Two new enemy
  mechanics (40 enemies): **Cogjammer** (`jam`: towers within 130 px fire 40% slower while it lives; the strongest
  jammer applies, they don't stack; shown as a turning dashed brass ring) and **Steamrunner** (`charge`: bolts at ×2.2
  for 1.6 s when hit, then 4 s cooldown; steam puff + hiss). Level 41 **Boilerworks Gate** (west + winding north road,
  1,000 / 920 px to the merge, 860 px tail, 11 pads, 15 waves, hpMult 1.95), a `GEARS` theme (half-sunk gears, steam
  pipes), a dark brass world-map style and a clockwork music theme. Endless adds both from wave 36. Fix from the
  screenshot: generic round trees picked up the brass/grey palette and looked like metal puffballs, so gears/pipes now
  fill 90% of the scenery. Browser check `scripts/brass-check.mjs`. 157 tests.
- [x] **Iter 77 — Brasswork level 42 + Rivetshell.** New enemy **Rivetshell** (41 enemies): a clockwork armadillo
  with `harden` (+2% armor per hit, up to 80%), the reverse of Saltjaw's brittle shell: rapid physical fire makes it
  tougher, magic and big shots don't care. The autoplayer counts hardeners as armored. Level 42 **Piston Yard**: west +
  south roads (780 / 660 px to the merge, pad row between the parallel stretches), 1,260 px tail, 12 pads, 15 waves,
  hpMult 1.28. First draft lost to bolting Steamrunner packs on the south road (moved/thinned). Endless adds Rivetshell
  from wave 36. Screenshot `77.png`. 158 tests.
- [x] **Iter 78 — Brasswork level 43: Gearwell Shafts.** One ~3,000 px road zigzags up and down five shafts 200 px
  apart, with pad columns between them (each pad covers two shafts). 12 pads, 16 waves, hpMult 1.42; waves 9–10 thinned.
  **Fix from the screenshot:** two pads at y=690 cut their towers off at the bottom edge. New test: pads stay at
  y ≤ 680. It caught six more in Cinder Tunnels, Mirrorpool Glade, Morrowcap's Throne (×2), Tidepool Terraces and
  Updraft Stair, all moved up to 680 (balance re-checked, small shifts only). Screenshot `78.png`. 159 tests.
- [x] **Iter 79 — Brasswork level 44: Foundry Crossroads.** Three roads (west 840 px, north 920 px looping round the
  furnace, south 640 px to the shared stretch) feed a 760 px tail. 12 pads, 16 waves, hpMult 1.39; one north-road
  Steamrunner pack thinned. Fix from the screenshot: a pad at the top right hid its tower behind the exit gate posts
  (moved below the exit road). Screenshot `79.png`. 159 tests.
- [x] **Iter 80 — POLISH + BALANCE.** Region 9 curve checked (41 100/100/33 · 42 100/83/8 · 43 83/83/17 · 44 83/83/0):
  no retunes. The expert-trails-casual gap on Foundry Crossroads is noise, not a bug: switching off smart branching,
  forcing either branch or thinking slower moves it by at most one seed in 12 (`expert.ts` probe). New guard-rail test:
  the expert must win every region finale in at least 2 of 3 seeds, so a change that makes a boss unbeatable fails CI
  (adds ~7 s). Screenshot `80.png`. 160 tests.
- [x] **Iter 81 — Brasswork finale: Heart of the Engine (level 45) + Grindmaw, the Engine Titan.** New boss (42
  enemies) from the region's traits: a wide `jam` aura (180 px, 30% slower fire), slow `harden` (+0.3% armor per hit,
  up to 70%), a Steamrunner `spawner`, and four phases (cogjammers → steam shield + rivetshells → every boiler at once →
  a grind for the gate). Level 45: west + south roads (920 / 680 px) merge into a 1,240 px tail, 12 pads, 18 waves,
  hpMult 1.58. Achievements **Engine Breaker** and **Master Tinker** (28 total); Grindmaw joins the endless boss
  rotation. Region 9 complete: 45 levels. Screenshot `81.png`. 160 tests.
- [x] **Iter 82 — Story cards after every region boss.** New data file `data/story.ts` and `StoryScene`: after a region
  finale the victory panel's Next button becomes **Story**, which shows a short chapter card in the region's sky colours
  (title, three lines, drifting motes, victory chime) and then **Onward** to the next land or **Village**. Cards for
  Morrowcap, Saltjaw, Kaleidrax, Zephyrax, Ulmaroth and Grindmaw; each one hints at the next region. The Emberdeep keeps
  its full epilogue. Tests: every card belongs to a region finale, and every finished region after the Emberdeep has one.
  Browser check `scripts/story-check.mjs` (forced win, checks the panel offers "Story", opens the card). 162 tests.
  Playable demo artifact refreshed with this build (45 levels).
- [x] **Iter 83 — Region 10 opens: The Starwell Abyss.** A dark cavern lit by glowing pools, below the engines. Two new
  enemy mechanics (44 enemies): **Dimlantern** (`dim`: shooting towers within 150 px lose 30% range while it lives; the
  strongest applies; drawn as a dark gloom disc with a violet rim) and **Echo Wisp** (`echo`: on its first death it
  re-forms on the spot at 50% health, paying no second bounty; "Echo!" ring + double ping). Level 46 **Glimmerpool
  Descent** (west + winding south road, 1,120 / 1,000 px to the merge, 920 px tail, 11 pads, 15 waves, hpMult 1.75), an
  `ABYSS` theme (pale stalagmites, breathing glow pools), a starry world-map style and a slow cavernous music theme.
  Endless adds both from wave 40. Browser check `scripts/abyss-check.mjs`. 164 tests.
- [x] **Iter 84 — Starwell level 47 + Sparkeel.** New enemy **Sparkeel** (45 enemies): a glowing cave eel with `shock`
  (every 5 s, soldiers and the hero within 110 px are stunned for 1.5 s: no attacking, and they let go of everything they
  held, including Bramble's Bulwark holds). Soldiers and heroes gained an optional `stun` timer. Level 47 **Lantern
  Hollow**: bottom-left + north roads (780 / 700 px to the merge, pad row between the parallel stretches), 1,280 px tail,
  12 pads, 15 waves, hpMult 1.8. Fixes found by the tests/screenshot: the north road first entered at x=840, under the
  top-right buttons (now 800), and a top pad hid its tower behind the wide "Next wave" preview (moved). Endless adds
  Sparkeel from wave 40. Screenshot `84.png`. 165 tests.
- [x] **Iter 85 — POLISH + BALANCE (47 levels, full sweep).** All 47 levels re-run with 12 seeds after the many
  mechanic and autoplayer changes since iteration 70: every level is in its band and every region ramps to its boss, so
  no hpMult changed. Polish: `scripts/phone-late.mjs` now takes a region and level (`node scripts/phone-late.mjs <name>
  <region> <level>`); the Starwell map, battle and Field Guide pages are clean at 740×360. Screenshot `85.png`.
- [x] **Iter 86 — Starwell level 48: Moonring Lake.** One road circles three sides of a glowing lake and exits at the
  bottom; pads ring the inner shore. 13 pads, 16 waves, hpMult 2.38. Fixes from the screenshot: the first exit came
  out at the bottom-left beside the hero HUD (now at x=500), and ponds were drawn in the daylight sky-blue; ponds in the
  Abyss theme now have a dark rim, a teal fill and a pulsing glow. Screenshot `86.png`. 165 tests.
- [x] **Iter 87 — Starwell level 49: Starfall Gorge.** A west road and a north road that winds round the gorge edge
  (1,180 / 880 px) meet at a T before a 760 px tail. 11 pads, 16 waves, hpMult 2.0. **Fix from the screenshot:** a top-
  right pad stood its tower on the exit gate's crossbar (moved below the exit road). New test: no tower may overlap a
  road-exit gate's posts or crossbar. It also caught the same spot in Three Winds (moved to (1100,148); balance
  re-checked 92/58/67). Screenshot `87.png`. 166 tests.
- [x] **Iter 88 — Starwell finale: Heart of the Abyss (level 50) + Velumbra, the Dark Below.** New boss (46 enemies):
  a shadow manta with a huge `dim` aura (200 px, −25% range), a crackling `shock` (stuns blockers within 150 px every
  7 s), an Echo Wisp `spawner`, and four phases (dimlanterns → shadow shield + sparkeels → a flood of wisps → a surge).
  No `echo` on the boss: re-forming at low health would re-trigger every phase at once. Level 50: a long west road (the
  boss) and a short north road (light groups only) merge into a 1,240 px tail around a glowing pool, 11 pads, 18 waves,
  hpMult 2.45. Achievements **Lightbringer** and **Starwalker** (30 total); Velumbra joins the endless boss rotation;
  story card "The Stars Come Home". Region 10 complete: 50 levels. Screenshot `88.png`. 166 tests. Playable demo
  artifact refreshed with this build.
- [x] **Iter 89 — Region 11 opens: The Rotbloom Orchard.** The Keepers' own orchards, rotting from the roots. New
  mechanics (49 enemies): **Barkwarden** (`fortify`: allies within 130 px gain +25% armor while it lives; the strongest
  aura applies, capped at 85%; shown as a turning ring of leaf-brown dashes; `sim.res()` and projectile damage both use
  it) and **Seedcaster**, which sows up to three **Rotseeds** (a still, 0-lives "enemy" with `grow`: after 6 s it
  sprouts into a Skitter, paying nothing). The first draft grew Thornhogs and four seeds per caster, which overran even
  the expert; now Skitters and three. Field Guide tags for fortify, grow and every spawner. Level 51 **Windfall Rows**
  (west + winding north road, 1,000 / 920 px, 860 px tail, 11 pads, 15 waves, hpMult 2.1), an `ORCHARD` theme (autumn
  fruit trees with apples, leaf heaps), an autumn world-map style and a slightly sour harvest-jig music theme. Endless
  adds Barkwarden and Seedcaster from wave 44. Browser check `scripts/orchard-check.mjs`. 168 tests.
- **Iteration 91**: third Rotbloom enemy, the **Gorgegrub** (new `feed` trait). When a non-boss ally dies within 120px,
  it gains +15% max health and heals 20% (up to 4 meals), and it visibly swells with each one. It comes with "Gulp!" text,
  crumbs and a wet-gulp sound cue, a segmented-grub sprite and a Field Guide tag. Level 52 **Grubfield Lane**: a long
  snaking west road plus a short north road that joins for the last stretch, 11 pads, 15 waves, hpMult 1.9. Grubs ride
  with fodder packs so they have something to eat. Endless adds Gorgegrub from wave 46. Browser check
  `scripts/grub-check.mjs`. 169 tests.
- **Iteration 92**: level 53 **Cider Press Crossing**. A north road and a south-west road meet at a central crossing,
  with a shared 540px tail to an east exit. It has 11 pads, 16 waves and hpMult 1.85, and is the first level to combine
  all three Rotbloom traits: Seedcasters' seeds die beside Gorgegrubs (food), and Barkwardens armor the swollen grubs.
  169 tests.
- **Iteration 93**: level 54 **Rotroot Hollow**. A 2,280px serpentine west road through the hollow, plus a 1,100px
  ridge track from the north for fliers and light enemies. The two roads only join for the last 260px. It has 11 pads,
  16 waves and hpMult 1.77. 169 tests.
- **Iteration 94**: Rotbloom finale, level 55 **Heart of the Orchard** (18 waves, 12 pads, hpMult 2.43). The boss
  **Mawbloom, the Rot Heart**:
  - Bark-song aura (+20% armor to allies within 160px).
  - Sows Rotseeds every 6s.
  - Feeds on fallen allies (+3% max health, up to 8 times).
  - Phases: 75% summons Barkwardens; 50% a 1,300 shield plus Gorgegrubs; 25% Seedcasters and a speed-up; 10% a final
    surge.
  - Code-drawn rotten heart-tree sprite with a toothy maw and bruised fruit.

  Also: achievements `boss_mawbloom` (Heartwood) and `orchard_stars` (Harvest Keeper), story card "The Orchard Wakes",
  and Mawbloom joins the endless boss rotation. New layout test: no road may run under the hero HUD. It caught the
  first draft of this level, where the boss walked behind the portrait. 170 tests.
- **Iteration 95** (polish + balance): the "Gulp!" feed text is throttled to once per 0.6s per eater, because Mawbloom
  surrounded by dying minions spammed it. Sweep results are in Balance Notes. 170 tests.
- **Iteration 96** (raid variety): a new camp building, the **Mire Shaman**:
  - A reed tent with a bone staff and a glowing brew bowl. Every 3s it heals every damaged camp building within 130px
    (itself and walls included) by 30, scaled by camp tier.
  - It shows a green pulse ring and sparkles on healed buildings, with a bubbling chime.
  - Warrens field 1 (replacing a hut) and Strongholds 2, so raiders want to take the shaman out early.

  Camp generation fix: a crowded core used to drop buildings silently. Placement now widens its search after 150
  tries, and Strongholds get every building they list. 172 tests (shaman heal and placement).
- **Iteration 97**: region 12 opens, **The Thunderhead Steppes**.
  - **Theme:** a `STORM` theme (grey-green steppe, standing stones with lichen, wind-flattened grass, light scrolling
    rain), a slate world-map style (grass tufts and standing stones, "Orchard Gate" exit label), and a galloping minor
    "Thunderhead" music theme.
  - **New traits:**
    - `bolt`: the **Stormcaller** calls lightning every 6s on the nearest shooting tower within 170px and stuns it for
      1.8s. It shares the chill-immunity window, with a jagged bolt, "Struck!" text and a thunderclap sound.
    - `herd`: the **Thunderhoof** gains +15% speed per herd-mate within 90px on its road, capped at +60%.
  - Both have code-drawn sprites and Field Guide tags. Endless adds them from wave 48.
  - **Level 56 Rainmarch Downs:** two long roads (the north road joins the west road early), 11 pads, 15 waves, hpMult
    2.1.
  - **World-map title fix:** long region names collided with the star counter. The title is now right-aligned to the
    star and shrinks to fit.
  - 174 tests (bolt and herd). The first bolt test passed vacuously because the test level had no pads, so it was
    rewritten with real pads.
- **Iteration 98**: third Thunderhead enemy, the **Copperhorn** (new `ground` trait).
  - A big grey ox with copper-capped horns. The nearest Copperhorn within 110px takes 40% of the damage aimed at
    an ally onto itself, so splash fire piles damage onto it. It takes its own hits in full, and players will want to
    focus it first.
  - A throttled copper arc shows each redirect.
  - Level 57 **Copperhorn Ford**: a long serpentine west road plus a short north road that joins at the ford, 11 pads,
    15 waves, hpMult 1.95. Endless adds Copperhorn from wave 50. 175 tests.
- **Iteration 99**: level 58 **Forked Lightning**. One west entrance forks around two hills (north and south loops)
  that rejoin at x=700, then a shared bend to the south-east exit. It has 11 pads (two between the loops cover both
  forks), 16 waves mixing all three Thunderhead enemies, and hpMult 2.2. 175 tests.
- **Iteration 100** (polish + balance): full 58-level sweep, run in 4 parallel batches (results in Balance Notes). No
  regressions from the new traits, so no retunes. The Field Guide entries for Stormcaller, Thunderhoof and
  Copperhorn were checked in-browser: all fit (right edge ≤ 1214px) with no console errors. 175 tests.
- **Iteration 101**: level 59 **Stormwatch Barrows**. A 2,540px serpentine herd road from the north-west winds around
  the barrow mounds. A 720px ridge track from the north joins it at the last bend (1,420px total). It has 10 pads,
  16 waves (Thunderhoof herds with Copperhorn escorts on the long road, fliers on the ridge) and hpMult 2.1.
  175 tests.
- **Iteration 102**: Thunderhead finale, level 60 **Thunderhead Crown**: a 2,960px storm-crown road plus a 1,360px
  north track, 12 pads, 18 waves, hpMult 2.0. The boss **Thrumhorn, the Storm Bull** (2,800 health):
  - Lightning bolt on the nearest tower in range 220, every 7s, stunning it 1.8s.
  - Calls in Thunderhoof herds (2 every 10s, up to 8).
  - Phases: 75% Stormcallers; 50% a 1,400 shield plus 2 Copperhorns; 25% a 10-strong stampede and a speed-up; 10%
    a charge.
  - Code-drawn sprite: storm bull with sparking horns and a little thundercloud on its back.

  Also: achievements `boss_thrumhorn` (Lightning Rod) and `storm_stars` (Rainmaker), story card "The Sky Clears", and
  Thrumhorn joins the endless boss rotation. 175 tests.
- **Iteration 103** (breather: hero variety): fifth hero **Sorrel, Hare Medic**, a support hero.
  - Ranged sling (14 physical, hits flyers, fast mover).
  - New passive `mend` ("Field Dressing"): soldiers within 170px heal 10/s, even while brawling.
  - New active `rally` ("Second Wind", cooldown 16s): heals every soldier in reach and Sorrel by 90 (scales with
    hero level), and stings enemies around her. It shows a green pulse, "+N" floaters and a chime.
  - Code-drawn hare sprite with long ears, a leaf-cross satchel and a sling, plus a pebble projectile.
  - The menu hero card was checked; long ability text overflowed it, so the lines were shortened.

  Browser check `scripts/sorrel-check.mjs`. 177 tests (mend and rally).

## In Progress
- (none)

## Backlog (ranked)
1. Iter 105 balance pass.
2. Region 13, or a breather feature (hero / tower variety, a village quality-of-life pass).
3. Field Guide holds 30 enemies per page and has 54 now. The next region pushes it past 60, so check paging then.

## Known Bugs
- (none known)

## Ideas parked
- Headless Chromium renders only a few FPS here, so live game time crawls in screenshots; scripts fast-forward sims.
- Village: "finish now" doesn't exist (no premium currency on purpose); maybe a free speed-up after a 3-star win.

## Balance Notes
**Iteration 102**: 60 Thunderhead Crown started at hpMult 2.5 with the boss at 3,000 health, bolting every 5s and
spawning herds of up to 12. The expert went 0/3, leaking Glareflies on the north track and wave 6–7 Echo Wisps and
Thunderhooves. Fixes: Glareflies moved to the long road, wave 6 trimmed to 9 wisps and wave 7 to 10 hooves, the boss
bolts every 7s with a herd limit of 8, and boss health went to 2,800. Tuning: 2.3 gave 33/8, 2.1 gave 67/17, 1.9 gave
83/25, and **2.0 → 83/33/0** (kept; the casual player mainly loses to the boss itself).

**Iteration 101**: 59 Stormwatch Barrows was **83/75/0** at hpMult 2.1 on the first try (kept, a fourth-level ramp).

**Iteration 100** (full sweep, 12 seeds, expert/casual/novice):
- Levels 1–50: identical to the last per-region passes (iterations 70–90), e.g. 5 Murkmaw 92/58/83 · 15 Emberdeep
  83/33/67 · 30 Kaleidrax 83/42/58 · 35 Roc's Aerie 100/50/17 · 45 Engine 83/67/8 · 50 Abyss 92/67/0.
- Rotbloom: 51 100/92/42 · 52 83/100/17 · 53 100/83/8 · 54 83/67/0 · 55 75/50/0.
- Thunderhead: 56 Rainmarch 100/100/42 · 57 Copperhorn Ford 83/83/25 · 58 Forked Lightning 92/83/0.

Every boss is in band (expert 75–92, casual 33–67), and every opener is at 100/≥92. No retunes.

**Iteration 99**: 58 Forked Lightning was 100/100/0 at hpMult 1.85 and 100/100/0 at 2.05. **2.2 → 92/83/0** (kept). Converging forks reward central pads, so it needed a higher multiplier than usual.

**Iteration 98**: 57 Copperhorn Ford is 83/83/25 at hpMult 1.95 on the first try (kept).

**Iteration 97**: 56 Rainmarch Downs began with a 900px north road and went 25/42/0, leaking everything on that road (galehounds, gullwings, skitters). I rerouted it to join the west road early (both ≈2,300px), which gave **100/100/42** at hpMult 2.1 (the opener target).

**Iteration 96** (raids, smart deploy, 10 seeds, avg stars / destruction):

| Army | Outpost | Warren | Stronghold |
|---|---|---|---|
| Lodge 1 | 1.8 / 67% | 0.4 / 27% | 0.0 / 17% |
| Lodge 2 | 3.0 / 100% | 1.9 / 75% (was 2.5 / 88%) | 0.6 / 37% |
| Lodge 3 | 3.0 / 100% | 3.0 / 100% | 1.2 / 47% (was 1.5 / 51%) |

The first shaman (45 heal every 2.5s, 150px, plus an extra building) dropped Lodge 2 vs Warren to 1.5 stars. It was
toned down, and one Warren hut was traded for the shaman. Note: `scripts/raid-balance.ts` prints nothing under
vite-node (argv check), so import `raidOnce` from a wrapper instead.

**Iteration 95** (12 seeds, expert/casual/novice): 51 Windfall Rows 100/92/42 · 52 Grubfield Lane 83/100/17 ·
53 Cider Press Crossing 100/83/8 · 54 Rotroot Hollow 83/67/0 · 55 Heart of the Orchard (boss) 75/50/0. The expert won
every region finale in at least 3 of 4 seeds (all 11). No retunes.

**Iteration 94**: 55 Heart of the Orchard went 50/75/0 at hpMult 2.2, with gnat swarms on the short north road. I moved them to the long road, which gave 100/92/0. 2.4 gave 83/67, then I reshaped the road away from the HUD and re-tuned: 2.45 gave 67/58, 2.35 gave 83/83, 2.4 gave 83/75, and **2.43 → 75/50/0** (kept, in the boss band).

**Iteration 93**: 54 Rotroot Hollow started at 50/67/0 (hpMult 1.9). 56 of the expert's leaked lives were Galehounds on the short ridge track (the short-road lesson again), so I moved them to the long road, which gave 75/75/0. 1.8 gave 75/67/0, 1.75 gave 92/92/0, and **1.77 → 83/67/0** (kept, a fourth-level ramp).

**Iteration 92**: 53 Cider Press Crossing was 83/50/0 at hpMult 1.95, 100/83/8 at 1.85 (kept) and 100/83/17 at 1.8.

**Iteration 91**: 52 Grubfield Lane at hpMult 2.15 was 67/58/8 (too hard for the region's second level). 1.95 gave 75/83/42 (noisy), 1.85 gave 100/100/17, and **1.9 → 83/100/17**, which I kept. The expert's main leak is Gorgegrubs on the long road, as intended.

**Iteration 90** (12 seeds, expert/casual/novice, Starwell + Orchard): 46 Glimmerpool 100/100/33 · 47 Lantern Hollow
100/100/25 · 48 Moonring Lake 100/83/0 · 49 Starfall 83/83/0 · 50 Heart of the Abyss (boss) 92/67/0 · 51 Windfall Rows
100/92/42. All in band, so no retunes. A per-step cache of Barkwarden auras was benchmarked: no measurable gain, and it gave
stale armor between steps. I reverted it, so `res()` stays exact.

**Iteration 85** (full sweep, 12 seeds, expert/casual/novice): levels 1–30 unchanged from iteration 70 except the
bottom-pad levels (Cinder 83/67/83, Morrowcap 83/67/0); 31–40 as in iteration 75; 41 Boilerworks 100/100/17 ·
42 Piston 100/83/8 · 43 Gearwell 83/83/17 · 44 Foundry 83/83/0 · 45 Heart of the Engine 83/67/8 · 46 Glimmerpool
100/100/33 · 47 Lantern Hollow 100/100/25. No retunes.

**Iteration 75** (camp sweep 31–40, 12 seeds): 31 Windgap 100/92/25 · 32 Updraft 100/75/42 · 33 Spiral 100/75/0 ·
34 Three Winds 92/67/50 · 35 Roc's Aerie 100/50/17 · 36 Overgrown 100/92/33 · 37 Sunken 100/83/17 · 38 Serpent
92/92/33 · 39 Idol Courtyard 92/58/33 · 40 Heart of the Ruins 92/50/0. Endless (3 seeds, waves held, expert/casual/
novice): Mossgate 12/12/12 · Duskcap 15/15/18 · Windgap 17/11/21 · Overgrown 12/12/18.

**Iteration 70** (camp sweep, 12 seeds, expert/casual/novice): unchanged from iteration 65 for levels 1–30; 31 Windgap
100/92/25 · 32 Updraft 100/75/42 · 33 Spiral 100/75/0 · 34 Three Winds 92/67/50 · 35 Roc's Aerie 100/50/17 ·
36 Overgrown Causeway 100/100/33 · 37 Sunken Stairs 100/92/17. No retunes needed.
**Iteration 71:** 38 Serpent Terraces 92/92/33 at hpMult 1.65 (1.5 → 100/100/50, 1.72 → 67/67/17, 1.8 → 58/58/0):
the steepest curve yet, so it errs easy. After the shifter mix change: Overgrown Causeway 100/92/33, Sunken Stairs
100/83/17.
**Iteration 89:** 51 Windfall Rows 100/92/42 at hpMult 2.1 (1.8 → 100/100/100, 2.15 → 100/83/75, 2.4 → 100/42/17).
**Iteration 88:** 50 Heart of the Abyss 92/67/0 at hpMult 2.45 (1.8 → 92/92/0, 2.1 → 92/92/0, 2.4 → 75/75/0,
2.55 → 67/67/0, 2.7 → 58/33/0). Expert and casual fall together here, so casual sits a little above the boss band.
**Iteration 87:** 49 Starfall Gorge 83/83/0 at hpMult 2.0 (1.6 → 100/100/0, 1.9 → 92/83/0, 2.1 → 58/33/0).
Three Winds after its pad move: 92/58/67 at 1.55.
**Iteration 86:** 48 Moonring Lake 100/83/0 at hpMult 2.38 (2.1 → 100/100/0, 2.45 → 75/75/0, 2.6 → 58/33/0).
**Iteration 84:** 47 Lantern Hollow 100/100/25 at hpMult 1.8 (1.5 → 100/100/100, 1.9 → 100/100/0, 2.05 → 100/92/0):
the novice falls off a cliff (Sparkeels break Bramble's holds).
**Iteration 83:** 46 Glimmerpool Descent 100/100/33 at hpMult 1.75 (1.6 → 100/100/100, 1.85 → 100/100/25,
2.0 → 100/100/0).
**Iteration 81:** 45 Heart of the Engine 83/67/8 at hpMult 1.58 (1.5 → 83/83/17, 1.61 → 75/67/0, 1.65 → 50/58/0,
1.8 → 0/33/0).
**Iteration 79:** 44 Foundry Crossroads 83/83/0 at hpMult 1.39 (1.2 → 100/100/33, 1.36 → 83/100/0, 1.45 → 75/83/0,
1.55 → 42/67/0). The expert trails casual here: likely its branch picks vs. Rivetshells/Cogjammers; check in iter 80.
**Iteration 78:** 43 Gearwell Shafts 83/83/17 at hpMult 1.42 (1.3 → 100/100/42, 1.5 → 75/58/0, 1.7 → 25/0/0). After
the bottom-pad moves: Cinder Tunnels 83/67/83, Mirrorpool 100/75/58, Morrowcap 83/67/0, Tidepool 92/83/100,
Updraft 100/75/42.
**Iteration 77:** 42 Piston Yard 100/83/8 at hpMult 1.28 (1.2 → 100/100/8, 1.35 → 100/75/0, 1.5 → 75/42/0). The
novice is weak here at any hpMult: jammers slow its towers and bolting Steamrunners slip past Bramble.
**Iteration 76:** 41 Boilerworks Gate 100/100/~33 at hpMult 1.95 (1.85 → 100/100/83, 1.93 → 100/100/58, 1.96 →
100/100/17, 2.2 → 92/75/0). The novice falls off a cliff here; expert/casual stay at 100% until ~2.1.
**Iteration 73:** 40 Heart of the Ruins 92/50/0 at hpMult 1.56 (1.4 → 100/92/0, 1.6 → 83/33/0, 1.7 → 67/25/0).
**Iteration 72:** 39 Idol Courtyard 92/58/33 at hpMult 1.22 (1.15 → 100/83/17, 1.3 → 92/33/0).

**Iteration 65** (camp sweep, 12 seeds, expert/casual/novice, deterministic): 1 Mossgate 100/100/100 · 2 Gloomfen
100/100/100 · 3 Thornwood 100/100/100 · 4 Mirelake 100/92/75 · 5 Murkmaw 100/75/83 → **92/58/83 (2.45)** · 6 Frostfern
100/100/100 · 7 Icicle 100/83/0 · 8 Glacier 92/92/92 · 9 Rimewood 100/100/92 · 10 Frostpeak 100/67/67 → **83/67/42
(1.85)** · 11 Ashfall 100/83/75 · 12 Cinder 75/75/58 → **83/75/75 (1.75)** · 13 Smoulder 100/83/100 · 14 Obsidian
92/83/0 · 15 Heart 83/33/67 · 16 Duskcap 100/92/100 · 17 Glowspore 92/92/0 · 18 Mirrorpool 100/75/58 · 19 Hollowroot
92/75/0 · 20 Morrowcap 75/75/0 · 21 Wrackline 100/100/100 · 22 Tidepool 92/83/100 · 23 Saltspray 92/75/0 · 24 Wreckspiral
92/92/0 · 25 Saltjaw 100/58/0 · 26 Glassfall 100/100/92 · 27 Prism 100/75/8 · 28 Shattered 100/75/0 · 29 Glassteeth
100/83/0 · 30 Kaleidrax 83/42/58 · 31 Windgap 100/92/25 · 32 Updraft 100/83/42 · 33 Spiral 100/75/0 · 34 Three Winds
92/58/33. Bosses are steep: ±0.15 hpMult can move expert 25 points (Frostpeak 1.75 → 2.0: 100 → 58%). The novice
(Bramble) stays strong on bosses and converging maps (Murkmaw, Heart, Kaleidrax, Tidepool, Smoulder).

**Iteration 61** (deterministic sim, 12 seeds): 31 Windgap Ledge 100/92/25 at hpMult 1.7 (2.2 was 75/58/0).
Galehounds were the main leak; Cloudrams on the north road second.
**Iteration 62:** 32 Updraft Stair 100/83/42 at hpMult 1.4 (first draft 75/0/0 at 1.6). Lesson: on a map where one
road is far shorter than the other, keep fast packs off the short road.
**Iteration 63:** 33 Spiral Gale 100/75/0 at hpMult 2.6 (sweep: 1.4 → 100/100/100, 2.1 → 100/100/8, 2.4 → 100/92/0,
2.8 → 100/50/0, 3.2 → 42/17/0).
**Iteration 64:** 34 Three Winds 92/58/33 at hpMult 1.55 (1.4 → 100/92/100, 1.5 → 92/67/42, 1.9 → 17/0/0). The novice
(Bramble) holds the merge well, so it outscores its usual curve here; regen enemies want the longest road.
**Iteration 66:** 35 Roc's Aerie 100/50/17 at hpMult 1.95 (1.72 → 100/83/92, 2.03 → 100/8/8, 2.1 → 83/17/0). The
first Zephyrax (hp 2900, short landings) was unbeatable (0/8/25 at 1.6); now hp 2200, speed 18, MR 0.35, lands 3.5 s
of every 7.5 s. Hawkeye archers are the counter: with Volley the expert won only 50% at 1.72.
**Iteration 68:** 36 Overgrown Causeway 100/100/33 at hpMult 1.4 (first draft 67/83/0 at 1.5 from armored packs on
the short north road; after the fix 1.5 → 100/100/8, 1.7 → 100/50/0).
**Iteration 69:** 37 Sunken Stairs 100/92/17 at hpMult 1.5 (first draft 92/58/0 at 1.4). After the HUD pad moves:
Updraft Stair 100/75/42 (was 100/83/42), Three Winds 92/67/50 (was 92/58/33); others unchanged.

**Iteration 60** (`balance.ts 6` full sweep, expert/casual/novice): 1–3, 6 at 100/100/100 (left easy on purpose:
first levels of a region) · 4 Mirelake 100/83/67 · 5 Murkmaw 83/50/67 · 7 Icicle 100/83/0 · 8 Glacier 100/83/83 ·
9 Rimewood 100/100/83 · 10 Frostpeak 83/83/67 · 11 Ashfall 83/100/83 · 12 Cinder 100/83/50 · 13 Smoulder 100/83/100 ·
14 Obsidian 100/83/0 · 16 Duskcap 100/83/100 · 17 Glowspore 83/83/0 · 18 Mirrorpool 100/50/83 · 19 Hollowroot 100/83/0 ·
20 Morrowcap 83/83/0 · 21 Wrackline 100/100/100 · 22 Tidepool 100/83/100 · 23 Saltspray 100/83/0 · 24 Wreckspiral
83/100/0 · 26 Glassfall 100/100/83 · 27 Prism 100/83/0 · 28 Shattered 100/67/0 · 29 Glassteeth 100/100/0 ·
30 Kaleidrax 83/33/50. Retuned (12–16 seeds): **15 Heart of the Emberdeep** 83/25/33 → 88/38/50 (hp 1.03);
**25 Saltjaw's Grotto** 50/50/8 → 81/69/0 (wave 6–7 trim, hp 2.55). Saltjaw is very sensitive to hpMult (±0.07
swung expert 75 → 44%) because losses came from one mid-level wave; smoothing the spike fixed that.
Watch: the novice (Bramble) beats casual on Heart of the Emberdeep and Kaleidrax; casual lags on Mirrorpool.

**Iteration 20** (`balance.ts 10`, after the per-wave ramp + rescale; expert/casual/novice):
L1 100/100/100 · L2 100/100/100 · L3 100/90/80 · L4 100/70/70 · L5 100/100/60 · L6 100/100/20 · L7 80/80/10 ·
L8 80/50/60 · L9 100/100/10 · L10 70/40/10 · L11 100/90/40 · L12 70/70/60 · L13 100/90/40 · L14 50/40/0 · L15 90/30/0.
- With the ramp alone (no rescale) almost every level got easier (Ashfall/Frostfern/Smoulder 100/100/100), as expected.
- Overall shape matches iteration 15, with gentler openings on late levels. Glacier Hold and Cinder Tunnels still
  let the novice keep up (merge maps favor Bramble at the choke); not worth more tuning until the AI can micro.

**Campaign (iteration 50, 6 seeds):** expert ≥ 83% on 28 of 29 levels (the outlier was Saltjaw's Grotto, now fixed).
Region openers: 100/100/100, 100/100/50, 100/100/67, 100/83/33, 100/100/50, 100/100/33. Bosses: Murkmaw 83/83/67,
Frostpeak 83/83/33, Heart 83/33/33, Morrowcap 83/33/0, Saltjaw (fixed) ~83/70/0.

**Campaign (iteration 55, 6 seeds, with the new spell/hero):** expert ≥ 83% on 27 of 30 levels; the three at 67%
are boss or late levels (Obsidian Bridges, Morrowcap's Throne, Saltjaw's Grotto), within noise of earlier passes.
Novice win rates rose by about 15–30 points on early and mid levels thanks to Thornsnare.

**Kaleidrax's Spire (iteration 51, 8 seeds):** first draft 0/0/0 (the boss leaked every run). After the boss nerf and the
autoplayer tweak, the curve was jagged: 2.15 → 88/63/100, then after moving the pads 2.15 → 100/63/63, **2.3 → 88% / 38% / 75%**
(kept), 2.45 → 63/0/25. The novice (Bramble blocking + all single-target towers) suits this boss's splash resistance.

**Glassteeth Ladder (iteration 49, 8 seeds):** first draft 0/0/0 at 3.4 (the final wave of 6 Bog Brutes + 12
Mirrorbacks was a wall). After trimming it and the other Mirrorback waves, and the shorter entry: **2.5 → 100% / 83% / 0%**
(kept). The casual autoplayer lags the expert most on Mirrorback-heavy maps (it specializes into splash variants
blindly). Re-tuned after the entry moves: Tidepool Terraces **1.4 → 88% / 88% / 25%**; Shattered Crossroads
2.8 → 100/67/0 (unchanged).

**Shattered Crossroads (iteration 48):** 2.6 → 100/100/0, **2.8 → 100% / 75% / 0%** (8 seeds, kept), 3.0 → 83/33/0.

**Prism Canyon (iteration 47, 6–8 seeds):** easy at first: 2.0 → 100/100/100, 2.6 → 100/100/17, 3.0 → 100/100/0;
**3.1 → 100% / 88% / 0%** (kept); 3.3 → 67/33/0, 3.6 → 17/0/0.

**Glassfall Flats (iteration 46, 6 seeds):** 2.4 → 100/100/0 (the novice lost 96 lives to big Shardskipper waves
on the short south road). Trimmed those two waves → **2.4: 100% / 100% / 33%** (kept, matches the other openers).

**Campaign (iteration 45, 6 seeds; expert / casual / novice):** Grovelands 100/50–100/67–100; Frostfern 83–100 /
67–100 / 0–67; Emberdeep 83–100 / 33–83 / 0–67; Duskcap 83–100 / 83–100 / 0–33; Shoals 83–100 / 67–100 / 0–83.
Bosses: Murkmaw 100/83/67, Frostpeak 83/83/33, Heart 83/33/33, Morrowcap 75/50/0 (after the tweak), Saltjaw 83/67/0.

**Saltjaw's Grotto (iteration 44, 8 seeds):** 2.2 → 83/83/0, **2.25 → 75% / 88% / 0%** (kept), 2.3 → 50/50/0,
2.4 → 50/25/0. Very steep around 2.25, like the other late boss levels.

**Wreckspiral (iteration 43):** steep curve: 2.9 → 100/100/0, 3.2 → 83/100/0, **3.25 → 88% / 75% / 0%** (8 seeds,
kept), 3.35 → 88/38/0, 4.2 → 0/0/0. Leaks at the top end were Reefwarden-shielded Thornhogs.

**Saltspray Fork (iteration 42, 6–8 seeds):** 2.2 → 67/50/0, 1.9 → 83/100/17, **2.05 → 88% / 63% / 0%** (kept).

**Tidepool Terraces (iteration 41):** first draft 0/33/0 at 2.4. Leak traces: Thornhogs (path 0) and Gullwings (short
north road), plus only 420 px of shared tail before the exit. After the wave trims and the longer tail: 2.2 → 50/33/0,
2.0 → 67/67/50, **1.9 → 75% / 50% / 75%** (8 seeds, picked). Bramble/novice does well on this converging map.
Lesson: give merged tails at least ~600 px.

**Heroes (iteration 40; expert wins on Icicle, Frostpeak, Obsidian, Heart and Morrowcap, 4 seeds each):**
| Hero | Before | After |
|---|---|---|
| Bramble | 35% | 35–55% (Fen's crit is the only random element, so ±10% run-to-run) |
| Fen | 95% | 80–95% |
| Ember | 60% | 75% |
Obsidian Bridges per hero (6 seeds): Bramble 0 → 5/6, Ember 0 → 4/6, Fen 5 → 6/6. Endless waves held (expert): Bramble
about 30, Fen 16–18, Ember 16. Most of Bramble's endless lead comes from regen + blocking in long fights; follow-up in
the backlog. Changed levels: Icicle 1.7 → 100/67/0, Murkmaw's Den 1.95 → 100/83/67, Obsidian 1.15 → 100/83/0.

**Wrackline Beach (iteration 39, 6 seeds):** at 2.4 → 100/100/0 with the novice losing 72 lives to wave 5's
Thornhogs (the same novice spike as on earlier maps). Thinned that wave → **2.4: 100% / 100% / 33%** (kept, matches
the Duskcap opener).

**Endless (iteration 38, 3 seeds, waves held expert / casual / novice):** Mossgate 18.7 / 15.7 / 16.3; Murkmaw's Den
11.7 / 11.7 / 25.0; Frostpeak 25.3 / 12.0 / 19.7; Duskcap Verge 21.3 / 18.3 / 30.7. Runs mostly end at waves 10–30
(the wave-10 and wave-20 bosses are the usual walls), which is the intended range.

**Campaign (iteration 35, 6 seeds; changed rows use 8):**
| # | Level | hpMult | Expert | Casual | Novice |
|---|---|---|---|---|---|
| 1–9 | Grovelands + Frostfern (unchanged) | — | 83–100 | 67–100 | 17–100 |
| 10 | Frostpeak Summit (boss) | 1.98 → **1.75** | 50 → 88 | 50 → 75 | 17 → 13 |
| 11 | Ashfall Gate | 2.04 | 100 | 83 | 33 |
| 12 | Cinder Tunnels | 1.91 | 83 | 83 | 50 |
| 13 | Smoulder Fields | 2.69 | 100 | 100 | 50 |
| 14 | Obsidian Bridges | 1.00 | 67 | 83 | 0 |
| 15 | Heart of the Emberdeep (finale) | 1.06 | 83 | 33 | 0 |
| 16 | Duskcap Verge | 2.40 | 100 | 83 | 33 |
| 17 | Glowspore Hollow | 2.20 | 83 | 100 | 0 |
| 18 | Mirrorpool Glade | 1.80 → **1.65** | 100 → 100 | 50 → 88 | 0 → 25 |
| 19 | Hollowroot Switchback | 3.70 | 100 | 83 | 0 |
| 20 | Morrowcap's Throne (boss) | 2.40 | 100 | 33 | 0 |
The Duskcap Weald is post-story endgame, so novice 0% on most of it is acceptable. Bosses now rank Murkmaw <
Grimtusk ≈ Vulkhar ≈ Morrowcap for the expert.

**Morrowcap's Throne (iteration 34, 8 seeds):** first draft at 2.4 → 63/63/0; leaks were mostly Thornhogs on the south
road (wave 5 and wave 11). Thinned and split those waves → 2.4: 75/75/0. After replacing the top-edge pad: **2.4 →
88% / 50% / 0%** (kept). The boss phases trigger correctly in-browser (phase 2 reached, 978 shield).

**Hollowroot Switchback (iteration 33):** the long road makes it easy per HP point: 2.6 → 100/100/33, 3.2 → 100/100/0,
3.8 → 83/67/0, 4.4 → 33/33/0. **3.7 → 88% / 75% / 0%** (8 seeds, picked). Its hpMult is the campaign's highest, but
bounties scale with it, so coin income keeps pace.

**Mirrorpool Glade (iteration 32):** first draft 0/0/0 at hpMult 2.2 and still only 83/100/0 at 1.2, so the problem
was the layout. Pads beyond veil range made Veilstalkers unhittable on the vertical roads. After moving the pads, lengthening
the south road and a lighter wave 6: 2.2 → 100/17/0, 2.0 → 88/25/0, **1.8 → 100% / 63% / 0%** (8 seeds, picked).
Lesson for Duskcap maps: keep some pads within ~95 px of each road.

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
