import { TOWERS } from '../data/towers';
import type { TowerDef, TowerTier } from '../data/types';

/** One stat bar on the tower info card: `value` and `next` are 0..1 of the best any tower reaches. */
export interface CardRow { label: string; value: number; next: number | null; text: string; nextText: string | null }

type Key = 'damage' | 'rate' | 'range' | 'wardenHp' | 'wardenDmg';

function raw(t: TowerTier, k: Key): number {
  switch (k) {
    case 'damage': return t.damage * (t.multishot ?? 1);
    case 'rate': return t.fireRate;
    case 'range': return t.range;
    case 'wardenHp': return (t.soldiers?.hp ?? 0) * (t.soldiers?.count ?? 0);
    case 'wardenDmg': return (t.soldiers?.damage ?? 0) * (t.soldiers?.attackRate ?? 0);
  }
}

let maxCache: Record<Key, number> | null = null;
/** The best value of each stat across every tower tier and branch (the right end of each bar). */
export function statMaxima(): Record<Key, number> {
  if (maxCache) return maxCache;
  const m: Record<Key, number> = { damage: 1, rate: 1, range: 1, wardenHp: 1, wardenDmg: 1 };
  for (const def of Object.values(TOWERS) as TowerDef[]) {
    for (const t of [...def.tiers, ...def.specs.map((s) => s.stats)]) {
      for (const k of Object.keys(m) as Key[]) {
        if ((k === 'damage' || k === 'rate') && t.soldiers) continue; // barracks don't shoot
        m[k] = Math.max(m[k], raw(t, k));
      }
    }
  }
  return (maxCache = m);
}

const fmt = (k: Key, v: number) => (k === 'rate' ? v.toFixed(1) : String(Math.round(v)));

/** Bars for a tower at `cur`, with an optional preview of `next` (the next tier or a branch). */
export function cardRows(cur: TowerTier, next?: TowerTier | null): CardRow[] {
  const max = statMaxima();
  const keys: [Key, string][] = cur.soldiers
    ? [['wardenHp', 'Wardens'], ['wardenDmg', 'Melee'], ['range', 'Reach']]
    : [['damage', 'Damage'], ['rate', 'Shots/s'], ['range', 'Range']];
  return keys.map(([k, label]) => {
    const a = raw(cur, k);
    const b = next ? raw(next, k) : null;
    const changed = b !== null && Math.abs(b - a) > 1e-6;
    return {
      label,
      value: Math.max(0.05, Math.min(1, a / max[k])),
      next: changed ? Math.max(0.05, Math.min(1, b! / max[k])) : null,
      text: fmt(k, a),
      nextText: changed ? fmt(k, b!) : null,
    };
  });
}

/** Short trait tags: damage type, air, and up to two specials. */
export function cardTags(def: TowerDef, t: TowerTier): string[] {
  const tags = [def.damageType === 'magic' ? 'Magic' : def.damageType === 'true' ? 'True dmg' : 'Physical', def.hitsAir ? 'Hits flyers' : 'Ground only'];
  const extra: string[] = [];
  if (t.splash) extra.push('Splash');
  if (t.slow) extra.push('Slows');
  if (t.chain) extra.push('Chains');
  if (t.multishot && t.multishot > 1) extra.push(`${t.multishot} targets`);
  if (t.armorPierce) extra.push('Pierces armor');
  return [...tags, ...extra.slice(0, 2)];
}
