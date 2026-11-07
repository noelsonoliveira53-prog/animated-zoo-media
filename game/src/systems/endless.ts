import { ENDLESS } from '../data/endless';
import { ENEMIES } from '../data/enemies';
import { DAILY_MODIFIERS, type ModifierDef } from '../data/daily';
import { hash } from './daily';
import type { LevelDef, SpawnGroup, WaveDef } from '../data/types';

// Endless mode: turn a campaign map into a long run of generated waves (pure + seeded, so it is testable).

function rng(seed: number): () => number {
  let a = seed >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

/** Enemies available on a 1-based wave number. */
export function endlessPool(wave: number): string[] {
  return ENDLESS.tiers.filter((t) => wave >= t.fromWave).flatMap((t) => t.enemies);
}

/** One generated wave (1-based number). Every `bossEvery`-th wave brings a boss with an escort. */
export function endlessWave(wave: number, paths: number, rand: () => number): WaveDef {
  const pool = endlessPool(wave);
  const pick = <T>(xs: T[]) => xs[Math.floor(rand() * xs.length)];
  const groups: SpawnGroup[] = [];
  const budget = ENDLESS.budgetBase + ENDLESS.budgetPerWave * wave;
  if (wave % ENDLESS.bossEvery === 0) {
    const boss = ENDLESS.bosses[(wave / ENDLESS.bossEvery - 1) % ENDLESS.bosses.length];
    groups.push({ enemy: boss, count: 1, interval: 1, delay: 6, path: Math.floor(rand() * paths) });
  }
  const nGroups = wave < 5 ? 2 : 3;
  for (let g = 0; g < nGroups; g++) {
    const id = pick(pool);
    const hp = ENEMIES[id].hp;
    const count = Math.max(1, Math.min(ENDLESS.maxGroupCount, Math.round(budget / nGroups / hp)));
    const interval = Math.max(0.25, Math.min(3, 18 / count));
    groups.push({ enemy: id, count, interval: +interval.toFixed(2), delay: g * 3, path: Math.floor(rand() * paths) });
  }
  return { groups };
}

/** A copy of a campaign level set up for endless play. */
export function makeEndlessLevel(level: LevelDef, seed = 1): LevelDef {
  const rand = rng(seed);
  const waves: WaveDef[] = [];
  for (let w = 1; w <= ENDLESS.waves; w++) waves.push(endlessWave(w, level.paths.length, rand));
  return { ...level, id: `${level.id}-endless`, waves, hpMult: 1, endless: { hpRamp: ENDLESS.hpRampPerWave, heroRegen: ENDLESS.heroRegen, attackRamp: ENDLESS.attackRamp }, finale: false };
}

/** Waves fully survived when a run ends during the given 0-based wave index. */
export function wavesHeld(waveIndex: number): number {
  return Math.max(0, waveIndex);
}

/** Today's endless mutator (the same for everyone on a given date). */
export function endlessMutatorFor(date: string): ModifierDef {
  const ids = ENDLESS.mutators;
  const id = ids[hash(`endless:${date}`) % ids.length];
  return DAILY_MODIFIERS.find((m) => m.id === id)!;
}

/** Village payout multiplier for a mutator (harder days pay more). */
export function mutatorReward(m: ModifierDef): number {
  return m.good ? 1 : ENDLESS.hardMutatorReward;
}
