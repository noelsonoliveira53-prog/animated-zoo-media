import type { WaveDef } from '../data/types';

export interface SpawnEvent {
  time: number; // seconds after wave start
  enemy: string;
  path: number;
}

/** Flatten a wave definition into a time-sorted spawn schedule. */
export function buildSchedule(wave: WaveDef): SpawnEvent[] {
  const out: SpawnEvent[] = [];
  for (const g of wave.groups) {
    const start = g.delay ?? 0;
    for (let i = 0; i < g.count; i++) {
      out.push({ time: start + i * g.interval, enemy: g.enemy, path: g.path ?? 0 });
    }
  }
  out.sort((a, b) => a.time - b.time);
  return out;
}

export function waveEnemyCount(wave: WaveDef): number {
  return wave.groups.reduce((n, g) => n + g.count, 0);
}

/** Bonus coins for calling a wave early: proportional to time left on the countdown. */
export function earlyCallBonus(secondsLeft: number, waveIndex: number): number {
  if (secondsLeft <= 0) return 0;
  return Math.round(secondsLeft * (1 + waveIndex * 0.25));
}
