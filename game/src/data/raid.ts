// Raid mode data: Keeper troops you train, and the Murkhorde camp buildings you attack.

export interface TroopDef {
  id: string;
  name: string;
  blurb: string;
  hp: number;
  damage: number;
  rate: number; // attacks / second
  range: number; // pixels (melee ~22)
  speed: number; // pixels / second
  cost: number; // glowsap per troop
  space: number; // army capacity used
  trainTime: number; // seconds at the Ranger Lodge
  prefers: 'any' | 'defense';
  splash?: number;
  wallMult?: number; // damage multiplier against walls
  flying?: boolean;
  lodge: number; // Ranger Lodge level required
  color: number;
}

export const TROOPS: Record<string, TroopDef> = {
  brawler: {
    id: 'brawler',
    name: 'Badger Brawler',
    blurb: 'Tough and stubborn. Walks to the nearest building and smashes it.',
    hp: 190,
    damage: 18,
    rate: 1,
    range: 22,
    speed: 45,
    cost: 40,
    space: 1,
    trainTime: 20,
    prefers: 'any',
    lodge: 1,
    color: 0x6f8fa8,
  },
  slinger: {
    id: 'slinger',
    name: 'Hedgehog Slinger',
    blurb: 'Fragile, but pelts buildings from a safe distance.',
    hp: 70,
    damage: 13,
    rate: 1.2,
    range: 110,
    speed: 55,
    cost: 50,
    space: 1,
    trainTime: 25,
    prefers: 'any',
    lodge: 1,
    color: 0x6fae4a,
  },
  sapper: {
    id: 'sapper',
    name: 'Beaver Sapper',
    blurb: 'Goes straight for defenses and gnaws them down. Hits everything nearby.',
    hp: 130,
    damage: 45,
    rate: 0.6,
    range: 24,
    speed: 48,
    cost: 90,
    space: 2,
    trainTime: 45,
    prefers: 'defense',
    splash: 45,
    wallMult: 3,
    lodge: 1,
    color: 0xb5651d,
  },
  owl: {
    id: 'owl',
    name: 'Owl Striker',
    blurb: 'Flies over everything and dives on defenses. Mortars cannot hit it.',
    hp: 95,
    damage: 22,
    rate: 1,
    range: 26,
    speed: 75,
    cost: 120,
    space: 3,
    trainTime: 60,
    prefers: 'defense',
    flying: true,
    lodge: 2,
    color: 0xc9a66b,
  },
};

export const TROOP_ORDER = ['brawler', 'slinger', 'sapper', 'owl'];

export interface CampBuildingDef {
  id: string;
  name: string;
  hp: number;
  size: number; // tiles
  defense?: { damage: number; rate: number; range: number; splash?: number; hitsAir: boolean };
  loot?: { coins: number; glowsap: number };
  hq?: boolean;
  wall?: boolean; // blocks ground troops; doesn't count toward destruction
  color: number;
}

export const CAMP_BUILDINGS: Record<string, CampBuildingDef> = {
  totem: { id: 'totem', name: 'Mud Totem', hp: 1200, size: 3, hq: true, loot: { coins: 300, glowsap: 300 }, color: 0x6a5a3a },
  spit: { id: 'spit', name: 'Spit Tower', hp: 480, size: 2, defense: { damage: 14, rate: 1.3, range: 150, hitsAir: true }, color: 0x4fae7c },
  mortar: { id: 'mortar', name: 'Bog Mortar', hp: 620, size: 2, defense: { damage: 34, rate: 0.45, range: 175, splash: 45, hitsAir: false }, color: 0x5a6b45 },
  pile: { id: 'pile', name: 'Loot Pile', hp: 380, size: 2, loot: { coins: 220, glowsap: 220 }, color: 0xb59a4e },
  hut: { id: 'hut', name: 'Mud Hut', hp: 280, size: 2, color: 0x7a5a3a },
  wall: { id: 'wall', name: 'Stake Wall', hp: 220, size: 1, wall: true, color: 0x5a4632 },
};

export const RAID_TIME = 90; // seconds

export const CAMP_TIERS = [
  { name: 'Mudling Outpost', counts: { spit: 3, mortar: 1, pile: 2, hut: 3 }, walls: false },
  { name: 'Bogscum Warren', counts: { spit: 3, mortar: 1, pile: 3, hut: 4 }, walls: true },
  { name: 'Murkhorde Stronghold', counts: { spit: 3, mortar: 2, pile: 4, hut: 5 }, walls: true },
];
