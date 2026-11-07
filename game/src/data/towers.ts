import type { TowerDef, TowerTier } from './types';

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
    specs: [
      {
        id: 'hawkeye',
        name: 'Hawkeye Perch',
        text: 'A sniper nest: huge range, heavy shots that ignore most armor. Best against tanks and bosses.',
        color: 0xc9e07a,
        stats: { cost: 220, damage: 110, range: 270, fireRate: 0.65, projectileSpeed: 900, armorPierce: 0.7 },
      },
      {
        id: 'volley',
        name: 'Bramble Volley',
        text: 'Rangers fire at three targets at once. Shreds swarms and flyers.',
        color: 0x5fae4a,
        stats: { cost: 200, damage: 15, range: 185, fireRate: 2.2, projectileSpeed: 620, multishot: 3 },
      },
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
    specs: [
      {
        id: 'storm',
        name: 'Stormcall Spire',
        text: 'Sparks become lightning that leaps between up to 4 more enemies.',
        color: 0x7fd3ff,
        stats: { cost: 260, damage: 62, range: 165, fireRate: 0.8, projectileSpeed: 700, chain: { count: 4, falloff: 0.75, range: 110 } },
      },
      {
        id: 'frost',
        name: 'Frostbloom Spire',
        text: 'Icy blooms burst on impact, chilling everything nearby to a crawl.',
        color: 0xbfe8ff,
        stats: { cost: 230, damage: 34, range: 165, fireRate: 0.9, projectileSpeed: 450, splash: 45, slow: { factor: 0.45, duration: 2.5 } },
      },
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
      { cost: 120, damage: 30, range: 165, fireRate: 0.5, projectileSpeed: 300, splash: 55, lob: true },
      { cost: 140, damage: 48, range: 175, fireRate: 0.52, projectileSpeed: 310, splash: 60, lob: true },
      { cost: 210, damage: 72, range: 190, fireRate: 0.55, projectileSpeed: 320, splash: 68, lob: true },
    ],
    specs: [
      {
        id: 'quake',
        name: 'Quake Mortar',
        text: 'Hurls whole boulders. Enormous blast radius and damage, slower reload.',
        color: 0xb5651d,
        stats: { cost: 280, damage: 130, range: 200, fireRate: 0.4, projectileSpeed: 300, splash: 95, lob: true },
      },
      {
        id: 'sap',
        name: 'Sap Catapult',
        text: 'Flings sticky tree sap that slows whole crowds and keeps them in the blast zone.',
        color: 0xe0a83c,
        stats: { cost: 220, damage: 55, range: 190, fireRate: 0.6, projectileSpeed: 320, splash: 75, lob: true, slow: { factor: 0.45, duration: 3 } },
      },
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
      { cost: 90, damage: 0, range: 150, fireRate: 0, projectileSpeed: 0, soldiers: { count: 2, hp: 70, damage: 6, attackRate: 1, respawn: 9, armor: 0.1, regen: 4 } },
      { cost: 110, damage: 0, range: 160, fireRate: 0, projectileSpeed: 0, soldiers: { count: 3, hp: 110, damage: 9, attackRate: 1.1, respawn: 8, armor: 0.2, regen: 6 } },
      { cost: 160, damage: 0, range: 170, fireRate: 0, projectileSpeed: 0, soldiers: { count: 3, hp: 170, damage: 14, attackRate: 1.2, respawn: 7, armor: 0.35, regen: 9 } },
    ],
    specs: [
      {
        id: 'stonehide',
        name: 'Stonehide Wardens',
        text: 'Heavily armored badgers that can hold even a Bog Brute for ages.',
        color: 0x8a96a3,
        stats: { cost: 220, damage: 0, range: 180, fireRate: 0, projectileSpeed: 0, soldiers: { count: 3, hp: 340, damage: 15, attackRate: 1.1, respawn: 7, armor: 0.6, regen: 14 } },
      },
      {
        id: 'raiders',
        name: 'Thornback Raiders',
        text: 'Four quick, spiky fighters that hit hard and come back fast.',
        color: 0xa86a4a,
        stats: { cost: 210, damage: 0, range: 180, fireRate: 0, projectileSpeed: 0, soldiers: { count: 4, hp: 170, damage: 24, attackRate: 1.5, respawn: 5, armor: 0.25, regen: 10 } },
      },
    ],
  },
};

export const TOWER_ORDER = ['thornbow', 'glimmer', 'boulder', 'burrow'];

/** Coins returned when selling: 60% of everything invested. */
export function sellValue(def: TowerDef, tier: number, spec: string | null = null): number {
  let spent = 0;
  for (let i = 0; i <= tier; i++) spent += def.tiers[i].cost;
  const sp = spec ? def.specs.find((x) => x.id === spec) : undefined;
  if (sp) spent += sp.stats.cost;
  return Math.floor(spent * 0.6);
}

/** Current stat block for a tower (its specialization if chosen, else its tier). */
export function towerStats(def: TowerDef, tier: number, spec: string | null): TowerTier {
  const sp = spec ? def.specs.find((x) => x.id === spec) : undefined;
  return sp ? sp.stats : def.tiers[tier];
}
