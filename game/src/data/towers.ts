import type { TowerDef } from './types';

// Keeper outposts. Tier 0 is the build; tiers 1-2 are upgrades.
export const TOWERS: Record<string, TowerDef> = {
  thornbow: {
    id: 'thornbow',
    name: 'Thornbow Nest',
    blurb: 'Rangers fire thorn darts quickly. Good vs swarms, poor vs armor.',
    damageType: 'physical',
    hitsAir: true,
    color: 0x8fbf4a,
    tiers: [
      { cost: 70, damage: 7, range: 150, fireRate: 1.6, projectileSpeed: 520 },
      { cost: 90, damage: 11, range: 165, fireRate: 1.8, projectileSpeed: 560 },
      { cost: 140, damage: 16, range: 180, fireRate: 2.1, projectileSpeed: 600 },
    ],
  },
  glimmer: {
    id: 'glimmer',
    name: 'Glimmer Spire',
    blurb: 'Firefly mages fling sparks that ignore armor. Slow but strong.',
    damageType: 'magic',
    hitsAir: true,
    color: 0xb07cff,
    tiers: [
      { cost: 100, damage: 22, range: 140, fireRate: 0.7, projectileSpeed: 380 },
      { cost: 120, damage: 36, range: 150, fireRate: 0.75, projectileSpeed: 400 },
      { cost: 180, damage: 58, range: 160, fireRate: 0.8, projectileSpeed: 420 },
    ],
  },
};

export const TOWER_ORDER = ['thornbow', 'glimmer'];

/** Coins returned when selling: 60% of everything invested. */
export function sellValue(def: TowerDef, tier: number): number {
  let spent = 0;
  for (let i = 0; i <= tier; i++) spent += def.tiers[i].cost;
  return Math.floor(spent * 0.6);
}
