# Grovewatch: Sanctuary Siege — Progress

An original tower-defense + village-building game. The **Keepers of the Grove** defend their
woodland sanctuary from the **Murkhorde**, bog critters creeping out of the Gloomfen.
Resources: **Coins** (battle currency / village gold) and **Glowsap** (the second village resource, planned).

Run: `npm run dev` · Build: `npm run build` · Tests: `npm test` · Smoke test + screenshots: `npm run build && node scripts/screenshot.mjs <name>` · Balance report: `npx vite-node scripts/balance.ts [runs]`

Iteration counter: **5** (next balance pass at iteration 10)

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

## In Progress
- (none)

## Backlog (ranked)
1. Global spells: Starfall (meteor AoE) + Call the Rangers (temporary soldiers), cooldowns.
2. World map scene with level nodes, star totals, unlock progression; levels 2–5.
3. Tower top-tier specializations (2 branches per tower).
4. Home base (village) scene: grid, Town Hall, Coin Mine, Glowsap Well, Storage, builders, timed upgrades; campaign rewards feed the village.
5. Village buildings grant battle perks (e.g. Defense Workshop unlocks/boosts towers).
6. Levels 6–15+, multi-path levels.
7. Raid mode: AI villages, train troops in Barracks, deploy to attack.
8. Meta: achievements, daily challenge, encyclopedia, settings scene (volume / mute).
9. Mobile polish: larger touch targets, pinch-free layout, orientation hint.
10. Ambient music loop (procedural).

## Known Bugs
- (none known)

## Ideas parked
- Persistent hero levels across battles (meta progression) — currently levels reset each battle.

## Balance Notes
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
