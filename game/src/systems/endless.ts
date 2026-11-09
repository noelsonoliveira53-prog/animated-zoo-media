import { ENDLESS } from '../data/endless';
import { ENEMIES } from '../data/enemies';
import { DAILY_MODIFIERS, type ModifierDef } from '../data/daily';
import { hash } from './daily';
import type { LevelDef, SpawnGroup, WaveDef } from '../data/types';
import { LEVELS, REGIONS, regionOf } from '../data/levels';

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
export function endlessWave(wave: number, paths: number, rand: () => number, native: string[] = [], bosses: string[] = ENDLESS.bosses): WaveDef {
  const base = endlessPool(wave);
  const pool = wave >= ENDLESS.nativeFrom ? [...base, ...native.filter((id) => !base.includes(id))] : base;
  const pick = <T>(xs: T[]) => xs[Math.floor(rand() * xs.length)];
  const groups: SpawnGroup[] = [];
  const budget = ENDLESS.budgetBase + ENDLESS.budgetPerWave * wave;
  if (wave % ENDLESS.bossEvery === 0) {
    const boss = bosses[(wave / ENDLESS.bossEvery - 1) % bosses.length];
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

/** A map's "home turf": the regular (non-boss) enemies its campaign waves use. */
export function nativeEnemies(level: LevelDef): string[] {
  const ids = new Set<string>();
  for (const w of level.waves) for (const g of w.groups) if (ENEMIES[g.enemy] && !ENEMIES[g.enemy].boss) ids.add(g.enemy);
  return [...ids];
}

/**
 * Boss order for an endless run on this map: the gentlest boss always opens (wave 10), then the map's own region
 * boss (wave 20), then the usual rotation. Opening with a late region's boss walled every strategy at wave 12
 * (Grimtusk on Frostpeak, iteration 315), since the towers are still young at wave 10.
 */
export function endlessBosses(level: LevelDef): string[] {
  const home = endlessHomeBoss(level);
  if (!home || home === ENDLESS.bosses[0]) return ENDLESS.bosses;
  const [first, ...rest] = ENDLESS.bosses;
  return [first, home, ...rest.filter((b) => b !== home)];
}

/** A copy of a campaign level set up for endless play. */
export function makeEndlessLevel(level: LevelDef, seed = 1): LevelDef {
  const rand = rng(seed);
  const waves: WaveDef[] = [];
  const native = nativeEnemies(level);
  const bosses = endlessBosses(level);
  for (let w = 1; w <= ENDLESS.waves; w++) waves.push(endlessWave(w, level.paths.length, rand, native, bosses));
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

/** The boss of this map's region (from its finale) if it is in the endless rotation, else null. */
export function endlessHomeBoss(level: LevelDef): string | null {
  const idx = LEVELS.findIndex((l) => l.id === level.id);
  if (idx < 0) return null;
  const reg = REGIONS[regionOf(idx)];
  const finale = LEVELS[reg.first + reg.count - 1];
  return finale?.waves.flatMap((w) => w.groups.map((g) => g.enemy)).find((id) => ENEMIES[id]?.boss && ENDLESS.bosses.includes(id)) ?? null;
}
