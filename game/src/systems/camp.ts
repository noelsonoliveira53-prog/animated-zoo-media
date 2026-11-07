import { CAMP_BUILDINGS, CAMP_TIERS } from '../data/raid';

// Seeded Murkhorde camp generation. Same seed + tier always gives the same camp.

export const CAMP_TILE = 40;
export const CAMP_COLS = 24;
export const CAMP_ROWS = 14;
export const CAMP_OX = 160;
export const CAMP_OY = 92;

export interface CampBuilding {
  uid: number;
  type: string;
  col: number;
  row: number;
  hp: number;
  maxHp: number;
}

export interface Camp {
  tier: number; // 0-based
  seed: number;
  buildings: CampBuilding[];
}

function rng(seed: number): () => number {
  let a = seed >>> 0 || 1;
  return () => {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

/** Tier scaling for camp buildings: tougher defenses and richer loot. */
export function tierMult(tier: number): { hp: number; dmg: number; loot: number } {
  return { hp: 1 + 0.4 * tier, dmg: 1 + 0.35 * tier, loot: 1 + 0.7 * tier };
}

export function generateCamp(seed: number, tier: number): Camp {
  const r = rng(seed * 7919 + tier * 104729);
  const t = Math.max(0, Math.min(CAMP_TIERS.length - 1, tier));
  const mult = tierMult(t);
  const buildings: CampBuilding[] = [];
  let uid = 1;
  const occupied = (col: number, row: number, size: number) =>
    buildings.some((b) => {
      const s = CAMP_BUILDINGS[b.type].size;
      // keep a one-tile gap between buildings so troops can walk around
      return col < b.col + s + 1 && col + size + 1 > b.col && row < b.row + s + 1 && row + size + 1 > b.row;
    });
  const add = (type: string, col: number, row: number) => {
    const def = CAMP_BUILDINGS[type];
    const hp = Math.round(def.hp * mult.hp);
    buildings.push({ uid: uid++, type, col, row, hp, maxHp: hp });
  };
  // HQ in the middle, everything else scattered in a core area around it.
  const cx = Math.floor(CAMP_COLS / 2) - 1;
  const cy = Math.floor(CAMP_ROWS / 2) - 1;
  add('totem', cx, cy);
  const counts = CAMP_TIERS[t].counts as Record<string, number>;
  const order = ['mortar', 'spit', 'pile', 'hut'];
  for (const type of order) {
    const size = CAMP_BUILDINGS[type].size;
    for (let n = 0; n < counts[type]; n++) {
      // Defenses stay closer to the HQ; huts and piles may sit further out.
      const spread = type === 'mortar' || type === 'spit' ? 5 : 8;
      for (let tries = 0; tries < 200; tries++) {
        const col = cx + Math.round((r() * 2 - 1) * spread);
        const row = cy + Math.round((r() * 2 - 1) * (spread * 0.6));
        if (col < 3 || row < 1 || col + size > CAMP_COLS - 3 || row + size > CAMP_ROWS - 1) continue;
        if (occupied(col, row, size)) continue;
        add(type, col, row);
        break;
      }
    }
  }
  return { tier: t, seed, buildings };
}

export function buildingCenter(b: CampBuilding): { x: number; y: number } {
  const s = CAMP_BUILDINGS[b.type].size;
  return { x: CAMP_OX + (b.col + s / 2) * CAMP_TILE, y: CAMP_OY + (b.row + s / 2) * CAMP_TILE };
}

export function buildingRadius(b: CampBuilding): number {
  return (CAMP_BUILDINGS[b.type].size * CAMP_TILE) / 2;
}

/** Total loot in a camp (what a full clear would pay). */
export function campLoot(camp: Camp): { coins: number; glowsap: number } {
  const m = tierMult(camp.tier).loot;
  let coins = 0;
  let glowsap = 0;
  for (const b of camp.buildings) {
    const l = CAMP_BUILDINGS[b.type].loot;
    if (l) {
      coins += l.coins * m;
      glowsap += l.glowsap * m;
    }
  }
  return { coins: Math.round(coins), glowsap: Math.round(glowsap) };
}
