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
  boulder: {
    id: 'boulder',
    name: 'Boulder Bellows',
    blurb: 'A beaver-built catapult that lobs river rocks. Crushes crowds, cannot hit flyers.',
    damageType: 'physical',
    hitsAir: false,
    color: 0xd98c3f,
    tiers: [
      { cost: 120, damage: 18, range: 165, fireRate: 0.4, projectileSpeed: 300, splash: 48, lob: true },
      { cost: 140, damage: 30, range: 175, fireRate: 0.42, projectileSpeed: 310, splash: 54, lob: true },
      { cost: 210, damage: 48, range: 190, fireRate: 0.45, projectileSpeed: 320, splash: 62, lob: true },
    ],
  },
  burrow: {
    id: 'burrow',
    name: 'Burrow Den',
    blurb: 'Badger Wardens rush out to block the road and brawl. Flyers pass overhead.',
    damageType: 'physical',
    hitsAir: false,
    color: 0x6f8fa8,
    tiers: [
      { cost: 90, damage: 0, range: 150, fireRate: 0, projectileSpeed: 0, soldiers: { count: 2, hp: 60, damage: 4, attackRate: 1, respawn: 9, armor: 0.1, regen: 4 } },
      { cost: 110, damage: 0, range: 160, fireRate: 0, projectileSpeed: 0, soldiers: { count: 3, hp: 90, damage: 6, attackRate: 1.1, respawn: 8, armor: 0.2, regen: 6 } },
      { cost: 160, damage: 0, range: 170, fireRate: 0, projectileSpeed: 0, soldiers: { count: 3, hp: 150, damage: 10, attackRate: 1.2, respawn: 7, armor: 0.35, regen: 9 } },
    ],
  },
};

export const TOWER_ORDER = ['thornbow', 'glimmer', 'boulder', 'burrow'];

/** Coins returned when selling: 60% of everything invested. */
export function sellValue(def: TowerDef, tier: number): number {
  let spent = 0;
  for (let i = 0; i <= tier; i++) spent += def.tiers[i].cost;
  return Math.floor(spent * 0.6);
}
