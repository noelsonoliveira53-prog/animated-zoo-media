// Village buildings. Costs are in Coins (gold) and Glowsap (the glowing tree-sap second resource).

export type BuildingId = 'townhall' | 'coinmine' | 'sapwell' | 'vault' | 'builderhut' | 'barracks' | 'workshop' | 'shrine' | 'apiary' | 'wall';

export interface Cost {
  coins?: number;
  glowsap?: number;
}

export interface BuildingLevel {
  cost: Cost; // cost to build (level 1) or upgrade to this level
  time: number; // seconds of construction
  th: number; // Town Hall level required
  produces?: { resource: 'coins' | 'glowsap'; perHour: number; capacity: number };
  storage?: number; // extra capacity for both resources
  hp?: number; // for walls / future raids
}

export interface BuildingDef {
  id: BuildingId;
  name: string;
  blurb: string;
  size: number; // footprint in tiles (square)
  color: number;
  levels: BuildingLevel[];
  /** Max number of this building allowed at each Town Hall level (index = TH level - 1). */
  maxCount: number[];
}

export const BUILDINGS: Record<BuildingId, BuildingDef> = {
  townhall: {
    id: 'townhall',
    name: 'Grove Hall',
    blurb: 'The great hollow oak at the heart of the sanctuary. Upgrade it to unlock more of everything.',
    size: 3,
    color: 0x9a6a40,
    maxCount: [1, 1, 1, 1, 1],
    levels: [
      { cost: {}, time: 0, th: 0, storage: 1000 },
      { cost: { coins: 800, glowsap: 400 }, time: 60, th: 1, storage: 2000 },
      { cost: { coins: 2500, glowsap: 1500 }, time: 300, th: 2, storage: 4000 },
      { cost: { coins: 6000, glowsap: 4000 }, time: 900, th: 3, storage: 7000 },
      { cost: { coins: 12000, glowsap: 9000 }, time: 2400, th: 4, storage: 12000 },
    ],
  },
  coinmine: {
    id: 'coinmine',
    name: 'Acorn Mine',
    blurb: 'Squirrel miners dig up golden acorns: the Grove’s coin.',
    size: 2,
    color: 0xffc93c,
    maxCount: [2, 3, 4, 5, 6],
    levels: [
      { cost: { glowsap: 150 }, time: 10, th: 1, produces: { resource: 'coins', perHour: 400, capacity: 500 } },
      { cost: { glowsap: 300 }, time: 45, th: 1, produces: { resource: 'coins', perHour: 700, capacity: 1000 } },
      { cost: { glowsap: 700 }, time: 180, th: 2, produces: { resource: 'coins', perHour: 1100, capacity: 2000 } },
      { cost: { glowsap: 1500 }, time: 600, th: 3, produces: { resource: 'coins', perHour: 1600, capacity: 3500 } },
      { cost: { glowsap: 3000 }, time: 1500, th: 4, produces: { resource: 'coins', perHour: 2200, capacity: 5000 } },
    ],
  },
  sapwell: {
    id: 'sapwell',
    name: 'Glowsap Tap',
    blurb: 'A tapped ancient tree that drips glowing sap, used for magic and upgrades.',
    size: 2,
    color: 0x9be86a,
    maxCount: [2, 3, 4, 5, 6],
    levels: [
      { cost: { coins: 150 }, time: 10, th: 1, produces: { resource: 'glowsap', perHour: 400, capacity: 500 } },
      { cost: { coins: 300 }, time: 45, th: 1, produces: { resource: 'glowsap', perHour: 700, capacity: 1000 } },
      { cost: { coins: 700 }, time: 180, th: 2, produces: { resource: 'glowsap', perHour: 1100, capacity: 2000 } },
      { cost: { coins: 1500 }, time: 600, th: 3, produces: { resource: 'glowsap', perHour: 1600, capacity: 3500 } },
      { cost: { coins: 3000 }, time: 1500, th: 4, produces: { resource: 'glowsap', perHour: 2200, capacity: 5000 } },
    ],
  },
  vault: {
    id: 'vault',
    name: 'Burrow Vault',
    blurb: 'Underground larders that hold more Coins and Glowsap.',
    size: 2,
    color: 0x8a7a5a,
    maxCount: [1, 2, 2, 3, 4],
    levels: [
      { cost: { coins: 300 }, time: 15, th: 1, storage: 1500 },
      { cost: { coins: 700 }, time: 60, th: 2, storage: 3000 },
      { cost: { coins: 1600 }, time: 240, th: 3, storage: 6000 },
      { cost: { coins: 3500 }, time: 720, th: 4, storage: 10000 },
    ],
  },
  builderhut: {
    id: 'builderhut',
    name: 'Builder Burrow',
    blurb: 'Home of a beaver builder. Each burrow lets you build or upgrade one thing at a time.',
    size: 2,
    color: 0xb5651d,
    maxCount: [2, 2, 3, 3, 4],
    levels: [{ cost: { coins: 1000 }, time: 0, th: 1 }],
  },
  barracks: {
    id: 'barracks',
    name: 'Ranger Lodge',
    blurb: 'Trains raiding parties to strike back at Murkhorde camps. Higher levels unlock tougher troops.',
    size: 3,
    color: 0x6f8fa8,
    maxCount: [0, 1, 1, 2, 2],
    levels: [
      { cost: { glowsap: 400 }, time: 30, th: 2 },
      { cost: { glowsap: 1200 }, time: 300, th: 3 },
      { cost: { glowsap: 3000 }, time: 900, th: 4 },
    ],
  },
  workshop: {
    id: 'workshop',
    name: 'Defense Workshop',
    blurb: 'Keeper engineers here refine outposts. Each level gives your battle towers an edge.',
    size: 3,
    color: 0xb07cff,
    maxCount: [1, 1, 1, 1, 1],
    levels: [
      { cost: { coins: 500, glowsap: 300 }, time: 20, th: 1 },
      { cost: { coins: 1200, glowsap: 900 }, time: 120, th: 2 },
      { cost: { coins: 3000, glowsap: 2200 }, time: 600, th: 3 },
      { cost: { coins: 6500, glowsap: 5000 }, time: 1800, th: 4 },
    ],
  },
  shrine: {
    id: 'shrine',
    name: 'Moonpetal Shrine',
    blurb: 'A ring of pale stones where moth-keepers tend night-blooming petals. Each level makes your battle spells recharge faster.',
    size: 2,
    color: 0xc8b8ff,
    maxCount: [0, 1, 1, 1, 1],
    levels: [
      { cost: { coins: 900, glowsap: 600 }, time: 90, th: 2 },
      { cost: { coins: 2200, glowsap: 1800 }, time: 480, th: 3 },
      { cost: { coins: 5000, glowsap: 4200 }, time: 1500, th: 4 },
    ],
  },
  apiary: {
    id: 'apiary',
    name: 'Honeycomb Apiary',
    blurb: 'Painted hive-boxes where friendly bees from the Honeycomb Hills make royal jelly. Each level sends your hero into battle tougher.',
    size: 2,
    color: 0xf0b030,
    maxCount: [0, 0, 1, 1, 1],
    levels: [
      { cost: { coins: 1400, glowsap: 1000 }, time: 240, th: 3 },
      { cost: { coins: 3200, glowsap: 2600 }, time: 900, th: 3 },
      { cost: { coins: 6500, glowsap: 5200 }, time: 2100, th: 4 },
    ],
  },
  wall: {
    id: 'wall',
    name: 'Bramble Wall',
    blurb: 'A thorny hedge segment to decorate and fence your sanctuary.',
    size: 1,
    color: 0x4b8f3a,
    maxCount: [10, 15, 20, 25, 30],
    levels: [
      { cost: { coins: 40 }, time: 0, th: 1, hp: 300 },
      { cost: { coins: 120 }, time: 0, th: 2, hp: 700 },
      { cost: { coins: 300 }, time: 0, th: 3, hp: 1500 },
    ],
  },
};

export const SHOP_ORDER: BuildingId[] = ['coinmine', 'sapwell', 'vault', 'builderhut', 'workshop', 'barracks', 'shrine', 'apiary', 'wall'];

/** Moonpetal Shrine: battle spell cooldowns shrink by this fraction per level. */
export const SHRINE_CD_PER_LEVEL = 0.06;

/** Honeycomb Apiary: the hero's max health grows by this fraction per level. */
export const APIARY_HP_PER_LEVEL = 0.1;

export const VILLAGE_COLS = 22;
export const VILLAGE_ROWS = 13;

/** Swiftbloom: a free build speed-up earned by taking a level to 3 stars for the first time. */
export const SWIFTBLOOM = {
  maxHeld: 3,
  seconds: 3600, // build time removed per use
};
