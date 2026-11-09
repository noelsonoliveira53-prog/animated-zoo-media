/**
 * Status effects shown as small icons beside a unit's health bar, so they don't rely on tint alone
 * (accessibility: colour is never the only cue). Pure logic: which icons a unit shows, in a fixed order.
 */
export type StatusIcon = 'slow' | 'haste' | 'rage' | 'anchor' | 'poison' | 'glaze' | 'stun';

export interface EnemyStatusInput {
  slowTime: number;
  slowFactor: number;
  hasteTime: number;
  hasteMult: number;
  speedMult: number;
  anchored: boolean;
}

/** Icons for an enemy: slowed, hasted by spores, enraged / sped up, anchored. */
export function enemyStatuses(e: EnemyStatusInput): StatusIcon[] {
  const out: StatusIcon[] = [];
  if (e.slowTime > 0 && e.slowFactor < 1) out.push('slow');
  if (e.hasteTime > 0 && e.hasteMult > 1) out.push('haste');
  if (e.speedMult > 1) out.push('rage');
  if (e.anchored) out.push('anchor');
  return out;
}

export interface SoldierStatusInput {
  poisonT?: number;
  glazed?: number;
  stun?: number;
}

/** Icons for a soldier or the hero: poisoned, glazed in honey, stunned. */
export function soldierStatuses(s: SoldierStatusInput): StatusIcon[] {
  const out: StatusIcon[] = [];
  if ((s.poisonT ?? 0) > 0) out.push('poison');
  if ((s.glazed ?? 0) > 0) out.push('glaze');
  if ((s.stun ?? 0) > 0) out.push('stun');
  return out;
}

/** Centre x of the k-th of n icons laid out from `x0` with `gap` spacing (a row grows to the right). */
export function iconX(x0: number, k: number, gap = 12): number {
  return x0 + k * gap;
}
