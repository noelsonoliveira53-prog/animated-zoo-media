import type { LevelDef } from '../data/types';
import { TOWERS } from '../data/towers';
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
}

export const STRATEGIES: Strategy[] = [
  { name: 'expert-mixed', mix: ['thornbow', 'burrow', 'glimmer', 'boulder'], slotFraction: 0.75, reserve: 0, upgrades: true, hero: 'bramble', thinkEvery: 0.5 },
  { name: 'casual-mixed', mix: ['thornbow', 'burrow', 'glimmer', 'boulder'], slotFraction: 0.7, reserve: 40, upgrades: true, hero: 'fen', thinkEvery: 3 },
  { name: 'novice', mix: ['thornbow', 'thornbow', 'glimmer'], slotFraction: 0.5, reserve: 60, upgrades: true, hero: null, thinkEvery: 5 },
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
  const sim = new BattleSim(level, strat.hero);
  const ranked = rankSlots(sim);
  // Jitter: swap a few neighbours in the ranking so runs differ.
  for (let i = 0; i < ranked.length - 1; i++) if (rnd() < 0.35) [ranked[i], ranked[i + 1]] = [ranked[i + 1], ranked[i]];
  const usable = ranked.slice(0, Math.max(1, Math.round(ranked.length * strat.slotFraction)));
  let rotation = Math.floor(rnd() * strat.mix.length);
  let think = 0;
  const dt = 1 / 30;

  while (sim.isActive() && sim.time < maxSeconds) {
    think -= dt;
    if (think <= 0) {
      think = strat.thinkEvery;
      act();
    }
    // Start the first wave once the initial build is done; afterwards let the timer run.
    if (sim.waveIndex < 0 && sim.time > 2) sim.callNextWave();
    sim.update(dt);
    sim.drainEvents();
  }

  function act(): void {
    for (let guard = 0; guard < 20; guard++) {
      const free = usable.find((i) => sim.towers[i] === null);
      if (free !== undefined) {
        const id = strat.mix[rotation % strat.mix.length];
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
