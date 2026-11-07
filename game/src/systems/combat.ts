import type { DamageType, EnemyDef } from '../data/types';

/** Damage after armor / magic resistance. Always at least 1 for a non-zero hit. */
export function computeDamage(raw: number, type: DamageType, target: Pick<EnemyDef, 'armor' | 'magicResist'>): number {
  if (raw <= 0) return 0;
  let mult = 1;
  if (type === 'physical') mult = 1 - clamp01(target.armor);
  else if (type === 'magic') mult = 1 - clamp01(target.magicResist);
  return Math.max(1, Math.round(raw * mult * 10) / 10);
}

function clamp01(v: number): number {
  return Math.max(0, Math.min(0.9, v));
}
