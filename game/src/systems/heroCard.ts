import { HEROES, HERO_MAX_LEVEL, HERO_XP, heroLevelMult } from '../data/heroes';
import type { HeroDef } from '../data/types';
import type { CardRow } from './towerCard';

/** XP progress inside the current level (`frac` 0..1); `max` once the hero can't level further. */
export function heroXpProgress(xp: number, level: number): { have: number; need: number; frac: number; max: boolean } {
  if (level >= HERO_MAX_LEVEL) return { have: 0, need: 0, frac: 1, max: true };
  const base = HERO_XP[level - 1];
  const need = HERO_XP[level] - base;
  const have = Math.max(0, Math.min(need, xp - base));
  return { have, need, frac: have / need, max: false };
}

const hpAt = (d: HeroDef, lv: number) => d.hp * heroLevelMult(lv);
const dpsAt = (d: HeroDef, lv: number) => d.attack.damage * d.attack.rate * heroLevelMult(lv);

let maxCache: { hp: number; dps: number; speed: number } | null = null;
function maxima() {
  if (maxCache) return maxCache;
  const defs = Object.values(HEROES) as HeroDef[];
  return (maxCache = {
    hp: Math.max(...defs.map((d) => hpAt(d, HERO_MAX_LEVEL))),
    dps: Math.max(...defs.map((d) => dpsAt(d, HERO_MAX_LEVEL))),
    speed: Math.max(...defs.map((d) => d.speed)),
  });
}

/** Health / damage-per-second / speed bars, with the next level's gain as a preview (none at max level). */
export function heroCardRows(def: HeroDef, level: number): CardRow[] {
  const m = maxima();
  const nextLv = level < HERO_MAX_LEVEL ? level + 1 : null;
  const row = (label: string, a: number, b: number | null, max: number, fmt: (v: number) => string): CardRow => ({
    label,
    value: Math.max(0.05, Math.min(1, a / max)),
    next: b !== null && b !== a ? Math.max(0.05, Math.min(1, b / max)) : null,
    text: fmt(a),
    nextText: b !== null && b !== a ? fmt(b) : null,
  });
  const r = (v: number) => String(Math.round(v));
  return [
    row('Health', hpAt(def, level), nextLv ? hpAt(def, nextLv) : null, m.hp, r),
    row('Dmg/s', dpsAt(def, level), nextLv ? dpsAt(def, nextLv) : null, m.dps, (v) => v.toFixed(1)),
    row('Speed', def.speed, null, m.speed, r),
  ];
}
