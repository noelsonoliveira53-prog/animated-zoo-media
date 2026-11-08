import type { EnemyDef } from '../data/types';

export type DeathKind = 'feathers' | 'shards' | 'ooze' | 'puff';

export interface DeathStyle {
  kind: DeathKind;
  color: number;
  /** 0.7..2.2, from the enemy's size */
  size: number;
  /** a heavy kill: earns a tiny hit-stop and a heavier ring */
  heavy: boolean;
}

/** How an enemy should burst when it dies: flyers shed feathers, armored foes crack into shards, slimy splitters splat. */
export function deathStyle(def: EnemyDef): DeathStyle {
  const size = Math.max(0.7, Math.min(2.2, def.radius / 14));
  const heavy = !!def.boss || def.hp >= 1500;
  let kind: DeathKind = 'puff';
  if (def.flying) kind = 'feathers';
  else if (def.armor >= 0.4 || def.harden || def.fortify) kind = 'shards';
  else if (def.splitInto || def.sporeBurst || def.feed || def.heal) kind = 'ooze';
  return { kind, color: def.color, size, heavy };
}

/** Does this hit deserve a squash on the enemy sprite? (a big chunk of a sturdy foe's health) */
export function bigHit(damage: number, maxHp: number): boolean {
  return maxHp >= 200 && damage >= maxHp * 0.15;
}
