import { HEROES } from '../data/heroes';
import type { LevelDef, Vec2 } from '../data/types';
import { TOWERS } from '../data/towers';
import { ENEMIES } from '../data/enemies';
import { BattleSim } from './BattleSim';

// Simple scripted players used by the headless balance simulator and tests.

export interface Strategy {
  name: string;
  /** Tower ids to cycle through when building. */
  mix: string[];
  /** Fraction of slots this player will ever fill (weaker players use fewer). */
  slotFraction: number;
  /** Keeps this many coins in reserve (sloppy players hoard). */
  reserve: number;
  /** Whether the player upgrades towers at all. */
  upgrades: boolean;
  hero: string | null;
  /** Seconds between decisions (slower = weaker). */
  thinkEvery: number;
  /** Casts Starfall / Grove Call and the hero skill when useful. */
  useSpells?: boolean;
  /** Forces a specialization branch (0/1) for every tower; undefined alternates by slot. */
  specPick?: number;
  /** Moves the hero to the busiest choke point and picks branches from the level's enemy makeup. */
  smart?: boolean;
}

export const STRATEGIES: Strategy[] = [
  { name: 'expert-mixed', mix: ['adaptive'], slotFraction: 0.75, reserve: 0, upgrades: true, hero: 'fen', thinkEvery: 0.5, useSpells: true, smart: true },
  { name: 'casual-mixed', mix: ['adaptive'], slotFraction: 0.7, reserve: 40, upgrades: true, hero: 'fen', thinkEvery: 3, useSpells: true },
  { name: 'novice', mix: ['thornbow', 'thornbow', 'glimmer'], slotFraction: 0.5, reserve: 60, upgrades: true, hero: 'bramble', thinkEvery: 5, useSpells: true },
  { name: 'only-thornbow', mix: ['thornbow'], slotFraction: 1, reserve: 0, upgrades: true, hero: null, thinkEvery: 1 },
  { name: 'only-glimmer', mix: ['glimmer'], slotFraction: 1, reserve: 0, upgrades: true, hero: null, thinkEvery: 1 },
  { name: 'only-boulder', mix: ['boulder'], slotFraction: 1, reserve: 0, upgrades: true, hero: null, thinkEvery: 1 },
  { name: 'only-burrow', mix: ['burrow'], slotFraction: 1, reserve: 0, upgrades: true, hero: null, thinkEvery: 1 },
];

export interface RunResult {
  won: boolean;
  lives: number;
  maxLives: number;
  wavesReached: number;
  totalWaves: number;
  coinsLeft: number;
  seconds: number;
}

/**
 * A build order shaped by what the level sends: more air-capable towers vs flyers,
 * more magic vs armor, more physical vs magic resist. Mirrors how a thoughtful player adapts.
 */
/** Tower mix from the level's enemy makeup. A hero that can't hit flyers means more anti-air is needed. */
export function adaptiveMix(level: LevelDef, heroHitsAir = true): string[] {
  let total = 0;
  let fly = 0;
  let armored = 0;
  let warded = 0;
  let splashProof = 0;
  for (const w of level.waves)
    for (const g of w.groups) {
      const e = ENEMIES[g.enemy];
      const hp = e.hp * g.count;
      total += hp;
      if (e.flying) fly += hp;
      if (e.armor >= 0.4) armored += hp;
      if (e.magicResist >= 0.5) warded += hp;
      if ((e.splashResist ?? 0) >= 0.5) splashProof += hp * (e.boss ? 3 : 1); // a splash-proof boss decides the level
    }
  const f = Math.min(1, (fly / total) * (heroHitsAir ? 1 : 1.4));
  const a = armored / total;
  const m = warded / total;
  const sp = splashProof / total; // splash-resistant share: artillery is wasted on it
  const weights: Record<string, number> = {
    thornbow: 1 + f * 3 + m * 2,
    glimmer: 1 + a * 3 + f * 1.5 + sp * 1.5,
    boulder: Math.max(0.2, 1.2 - f * 3 - sp * 3),
    burrow: Math.max(0.2, 0.9 - f * 2),
  };
  // Expand to a repeating order of 8 picks, highest weight first, interleaved.
  const order: string[] = [];
  const acc: Record<string, number> = { thornbow: 0, glimmer: 0, boulder: 0, burrow: 0 };
  for (let i = 0; i < 8; i++) {
    for (const k of Object.keys(acc)) acc[k] += weights[k];
    const pick = Object.keys(acc).reduce((x, y) => (acc[y] > acc[x] ? y : x));
    acc[pick] -= Object.values(weights).reduce((p, q) => p + q, 0);
    order.push(pick);
  }
  return order;
}

/** Level makeup shares (by total enemy hp): flyers, armored, magic-resistant. */
function makeup(level: LevelDef): { fly: number; armored: number; warded: number } {
  let total = 0;
  let fly = 0;
  let armored = 0;
  let warded = 0;
  for (const w of level.waves)
    for (const g of w.groups) {
      const e = ENEMIES[g.enemy];
      const hp = e.hp * g.count;
      total += hp;
      if (e.flying) fly += hp;
      if (e.armor >= 0.4 || e.boss) armored += hp;
      if (e.magicResist >= 0.5) warded += hp;
    }
  return { fly: fly / total, armored: armored / total, warded: warded / total };
}

/** Branch choice a thoughtful player would make for this level. */
export function smartSpec(level: LevelDef, towerId: string): number {
  const m = makeup(level);
  switch (towerId) {
    case 'thornbow':
      return m.fly > 0.2 ? 1 : 0; // Volley vs flyers/swarms, else Hawkeye vs armor
    case 'glimmer':
      return 0; // Stormcall: best all-round crowd damage
    case 'boulder':
      return m.armored > 0.3 ? 0 : 1; // Quake vs tanks, Sap to hold crowds
    default:
      return m.armored > 0.3 ? 0 : 1; // Stonehide vs brutes, Raiders otherwise
  }
}

/** The road point with the most road (from all paths) within reach: merges and switchbacks. */
export function chokePoint(sim: BattleSim, reach = 150): Vec2 {
  let best = sim.heroSpawnPoint();
  let bestScore = -1;
  for (const path of sim.paths) {
    for (let d = path.length * 0.3; d < path.length - 60; d += 25) {
      const p = path.pointAt(d);
      let score = 0;
      for (const q of sim.paths) for (let k = 0; k < q.length; k += 20) {
        const r = q.pointAt(k);
        if (Math.hypot(r.x - p.x, r.y - p.y) <= reach) score++;
      }
      score += (d / path.length) * 5; // prefer later (closer to the gate)
      if (score > bestScore) {
        bestScore = score;
        best = p;
      }
    }
  }
  return best;
}

/** Ranks slots by how much road lies within a typical tower range (best coverage first). */
export function rankSlots(sim: BattleSim, range = 160): number[] {
  const scores = sim.level.slots.map((s, i) => {
    let cover = 0;
    for (const path of sim.paths) {
      for (let d = 0; d < path.length; d += 10) {
        const p = path.pointAt(d);
        if (Math.hypot(p.x - s.x, p.y - s.y) <= range) cover += 10;
      }
    }
    return { i, cover };
  });
  scores.sort((a, b) => b.cover - a.cover);
  return scores.map((s) => s.i);
}

function mulberry32(seed: number): () => number {
  let a = seed >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

/** Plays a whole level with a strategy. `seed` jitters slot order and tower rotation. */
export function playLevel(level: LevelDef, strat: Strategy, seed = 1, maxSeconds = 1800): RunResult {
  const rnd = mulberry32(seed);
  const sim = new BattleSim(level, strat.hero, { random: mulberry32(seed * 7919 + 17) });
  const ranked = rankSlots(sim);
  // Jitter: swap a few neighbours in the ranking so runs differ.
  for (let i = 0; i < ranked.length - 1; i++) if (rnd() < 0.35) [ranked[i], ranked[i + 1]] = [ranked[i + 1], ranked[i]];
  const mix = strat.mix[0] === 'adaptive' ? adaptiveMix(level, strat.hero ? HEROES[strat.hero].attack.hitsAir || !!HEROES[strat.hero].toss : true) : strat.mix;
  const usable = ranked.slice(0, Math.max(1, Math.round(ranked.length * strat.slotFraction)));
  let rotation = Math.floor(rnd() * mix.length);
  let think = 0;
  const dt = 1 / 30;
  // A level-designed hero spot (two-gate maps) beats the generic choke point.
  if (strat.smart && sim.hero && !level.heroSpawn) sim.moveHero(chokePoint(sim));

  while (sim.isActive() && sim.time < maxSeconds) {
    think -= dt;
    if (think <= 0) {
      think = strat.thinkEvery;
      act();
      if (strat.useSpells) castSpells();
    }
    // Start the first wave once the initial build is done; afterwards let the timer run.
    if (sim.waveIndex < 0 && sim.time > 2) sim.callNextWave();
    sim.update(dt);
    sim.drainEvents();
  }

  function castSpells(): void {
    const alive = sim.enemies.filter((e) => e.alive);
    if (!alive.length) return;
    // Starfall on the densest clump (or the boss).
    if (sim.spellReady('starfall')) {
      let best = alive[0];
      let bestN = 0;
      for (const e of alive) {
        const n = alive.filter((o) => Math.hypot(o.pos.x - e.pos.x, o.pos.y - e.pos.y) < 80).length + (e.def.boss ? 5 : 0);
        if (n > bestN) {
          bestN = n;
          best = e;
        }
      }
      if (bestN >= 5) {
        const ahead = sim.paths[best.path].pointAt(best.dist + best.def.speed * best.slowFactor * 0.9);
        sim.castSpell('starfall', ahead);
      }
    }
    // Grove Call just ahead of the enemy closest to the gate.
    if (sim.spellReady('grovecall') && alive.length >= 4) {
      const lead = alive.reduce((a, b) => (sim.paths[b.path].length - b.dist < sim.paths[a.path].length - a.dist ? b : a));
      sim.castSpell('grovecall', sim.paths[lead.path].pointAt(lead.dist + 70));
    }
    // Thornsnare on the densest clump of walkers (roots them inside the kill zone).
    if (sim.spellReady('thornsnare')) {
      const walkers = alive.filter((e) => !sim.airborne(e));
      let best: (typeof walkers)[number] | null = null;
      let bestN = 0;
      for (const e of walkers) {
        const n = walkers.filter((o) => Math.hypot(o.pos.x - e.pos.x, o.pos.y - e.pos.y) < 90).length + (e.def.boss ? 4 : 0);
        if (n > bestN) {
          bestN = n;
          best = e;
        }
      }
      if (best && bestN >= 5) sim.castSpell('thornsnare', best.pos);
    }
    // Hero skill when enough enemies are in reach.
    const h = sim.hero;
    if (h && h.alive && h.skillCd <= 0) {
      const n = alive.filter((e) => Math.hypot(e.pos.x - h.pos.x, e.pos.y - h.pos.y) <= h.def.active.radius).length;
      if (n >= 3) sim.useHeroSkill();
    }
  }

  function act(): void {
    for (let guard = 0; guard < 20; guard++) {
      const free = usable.find((i) => sim.towers[i] === null);
      if (free !== undefined) {
        const id = mix[rotation % mix.length];
        if (sim.coins - strat.reserve >= TOWERS[id].tiers[0].cost) {
          sim.build(free, id);
          rotation++;
          continue;
        }
        if (!strat.upgrades) return;
      }
      if (!strat.upgrades) return;
      // Upgrade the cheapest available upgrade.
      let best = -1;
      let bestCost = Infinity;
      sim.towers.forEach((t, i) => {
        if (!t) return;
        const c = sim.upgradeCost(t);
        if (c !== null && c < bestCost) {
          bestCost = c;
          best = i;
        }
      });
      if (best >= 0 && sim.coins - strat.reserve >= bestCost && (free === undefined || bestCost < 120)) {
        sim.upgrade(best);
        continue;
      }
      // Everything maxed: buy a specialization (alternate branches by slot).
      if (best < 0 && free === undefined) {
        const slot = sim.towers.findIndex((t) => t && sim.canSpecialize(t));
        if (slot >= 0) {
          const t = sim.towers[slot]!;
          const pick = strat.specPick ?? (strat.smart ? smartSpec(level, t.def.id) : slot % 2);
          if (sim.coins - strat.reserve >= t.def.specs[pick].stats.cost && sim.specialize(slot, pick)) continue;
        }
      }
      return;
    }
  }

  return {
    won: sim.status === 'victory',
    lives: sim.lives,
    maxLives: level.lives,
    wavesReached: sim.waveIndex + 1,
    totalWaves: sim.totalWaves,
    coinsLeft: sim.coins,
    seconds: Math.round(sim.time),
  };
}
