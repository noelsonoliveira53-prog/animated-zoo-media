# Grovewatch: Sanctuary Siege — Progress

An original tower-defense + village-building game. The **Keepers of the Grove** defend their
woodland sanctuary from the **Murkhorde**, bog critters creeping out of the Gloomfen.
Resources: **Coins** (battle currency / village gold) and **Glowsap** (the second village resource, planned).

Run: `npm run dev` · Build: `npm run build` · Tests: `npm test` · Smoke test + screenshots: `npm run build && node scripts/screenshot.mjs <name>`

Iteration counter: **3** (next balance pass at iteration 5)

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

## In Progress
- (none)

## Backlog (ranked)
1. Hero system: 1 movable hero (tap to move), melee, passive + active skill; then 3 heroes with level ups.
2. Global spells: Starfall (meteor AoE) + Call the Rangers (temporary soldiers), cooldowns.
3. World map scene with level nodes, star totals, unlock progression; levels 2–5.
4. Tower top-tier specializations (2 branches per tower).
5. Home base (village) scene: grid, Town Hall, Coin Mine, Glowsap Well, Storage, builders, timed upgrades; campaign rewards feed the village.
6. Village buildings grant battle perks (e.g. Defense Workshop unlocks/boosts towers).
7. Levels 6–15+, multi-path levels.
8. Raid mode: AI villages, train troops in Barracks, deploy to attack.
9. Meta: achievements, daily challenge, encyclopedia, settings scene (volume / mute).
10. Mobile polish: larger touch targets, pinch-free layout, orientation hint.
11. Ambient music loop (procedural).

## Known Bugs
- (none known)

## Balance Notes
- Level 2 (Gloomfen Edge) untuned and probably hard — boss has 2400 hp. Check in iteration 5.
- Level 1 untuned. First real pass scheduled for iteration 5 (headless sim harness to be written then).
