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
  prefers: 'any' | 'defense' | 'loot';
  splash?: number;
  wallMult?: number; // damage multiplier against walls
  flying?: boolean;
  wader?: boolean; // swims through Sludge Pit muck at full speed
  lootBonus?: number; // buildings it finishes off drop this much more loot (0.3 = +30%)
  heals?: { amount: number; interval: number; radius: number }; // pulses healing into nearby troops (itself included)
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
    blurb: 'Gnaws down defenses first, hitting everything nearby.',
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
  mender: {
    id: 'mender',
    name: 'Toad Mender',
    blurb: 'A plump old toad with a gourd of swamp-tonic. Stays behind the front line and patches everyone up.',
    hp: 120,
    damage: 6,
    rate: 0.8,
    range: 90,
    speed: 46,
    cost: 110,
    space: 3,
    trainTime: 55,
    prefers: 'any',
    heals: { amount: 28, interval: 1.5, radius: 115 },
    lodge: 3,
    color: 0x6aa84a,
  },
  otter: {
    id: 'otter',
    name: 'Otter Scavenger',
    blurb: 'Swims through sludge, runs for the loot and digs out 30% more.',
    hp: 150,
    damage: 20,
    rate: 1.2,
    range: 22,
    speed: 72,
    cost: 60,
    space: 1,
    trainTime: 25,
    prefers: 'loot',
    wader: true,
    lootBonus: 0.3,
    lodge: 2,
    color: 0x8a5a3a,
  },
};

export const TROOP_ORDER = ['brawler', 'slinger', 'sapper', 'otter', 'owl', 'mender'];

export interface CampBuildingDef {
  id: string;
  name: string;
  hp: number;
  size: number; // tiles
  defense?: { damage: number; rate: number; range: number; splash?: number; hitsAir: boolean };
  loot?: { coins: number; glowsap: number };
  hq?: boolean;
  wall?: boolean; // blocks ground troops; doesn't count toward destruction
  mend?: { amount: number; interval: number; range: number }; // heals damaged camp buildings in range every `interval` s
  mire?: { radius: number; factor: number }; // ground troops within radius move at this fraction of their speed
  color: number;
}

export const CAMP_BUILDINGS: Record<string, CampBuildingDef> = {
  totem: { id: 'totem', name: 'Mud Totem', hp: 1200, size: 3, hq: true, loot: { coins: 300, glowsap: 300 }, color: 0x6a5a3a },
  spit: { id: 'spit', name: 'Spit Tower', hp: 480, size: 2, defense: { damage: 14, rate: 1.3, range: 150, hitsAir: true }, color: 0x4fae7c },
  mortar: { id: 'mortar', name: 'Bog Mortar', hp: 620, size: 2, defense: { damage: 34, rate: 0.45, range: 175, splash: 45, hitsAir: false }, color: 0x5a6b45 },
  pile: { id: 'pile', name: 'Loot Pile', hp: 380, size: 2, loot: { coins: 220, glowsap: 220 }, color: 0xb59a4e },
  shaman: { id: 'shaman', name: 'Mire Shaman', hp: 420, size: 2, mend: { amount: 30, interval: 3, range: 130 }, color: 0x7a4a8a },
  sludge: { id: 'sludge', name: 'Sludge Pit', hp: 360, size: 2, mire: { radius: 120, factor: 0.55 }, color: 0x5a4a2a },
  hut: { id: 'hut', name: 'Mud Hut', hp: 280, size: 2, color: 0x7a5a3a },
  wall: { id: 'wall', name: 'Stake Wall', hp: 220, size: 1, wall: true, color: 0x5a4632 },
};

export const RAID_TIME = 90; // seconds

export const CAMP_TIERS = [
  { name: 'Mudling Outpost', counts: { spit: 3, mortar: 1, pile: 2, hut: 3 }, walls: false },
  { name: 'Bogscum Warren', counts: { spit: 3, mortar: 1, shaman: 1, sludge: 1, pile: 3, hut: 3 }, walls: true },
  { name: 'Murkhorde Stronghold', counts: { spit: 3, mortar: 2, shaman: 2, sludge: 2, pile: 4, hut: 4 }, walls: true },
];
