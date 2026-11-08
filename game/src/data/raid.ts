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
  prefers: 'any' | 'defense' | 'loot' | 'hq';
  splash?: number;
  wallMult?: number; // damage multiplier against walls
  flying?: boolean;
  burrows?: boolean; // tunnels: passes under walls, and defenses can't hit it while it's digging toward a target
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
    blurb: 'A plump old toad with a gourd of tonic. Heals the troops around it.',
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
  mole: {
    id: 'mole',
    name: 'Mole Tunneler',
    blurb: 'Digs under walls straight for the Mud Totem. Nothing can hit it until it pops up.',
    hp: 320,
    damage: 44,
    rate: 0.8,
    range: 22,
    speed: 30,
    cost: 90,
    space: 2,
    trainTime: 45,
    prefers: 'hq',
    burrows: true,
    lodge: 3,
    color: 0x5a4a5a,
  },
};

export const TROOP_ORDER = ['brawler', 'slinger', 'sapper', 'otter', 'mole', 'owl', 'mender'];

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
  burst?: { radius: number; damage: number }; // when destroyed, stings every troop (flyers too) within radius
  ward?: { radius: number; cut: number }; // other camp buildings within radius take `cut` less damage while it stands
  venom?: { radius: number; dps: number; duration: number }; // ground troops passing within radius are poisoned: dps health a second for duration s
  blurb?: string;
  color: number;
}

export const CAMP_BUILDINGS: Record<string, CampBuildingDef> = {
  totem: { id: 'totem', name: 'Mud Totem', blurb: "A heap of mud and bones the Murkhorde rally around. Topple it and the camp loses heart.", hp: 1200, size: 3, hq: true, loot: { coins: 300, glowsap: 300 }, color: 0x6a5a3a },
  spit: { id: 'spit', name: 'Spit Tower', blurb: "A bog-frog perched on a stump, spitting gobs of muck at anything that moves, flyers included.", hp: 480, size: 2, defense: { damage: 14, rate: 1.3, range: 150, hitsAir: true }, color: 0x4fae7c },
  mortar: { id: 'mortar', name: 'Bog Mortar', blurb: "A hollow log packed with swamp-gas that lobs mudballs in a wide splash. It cannot aim up at flyers.", hp: 620, size: 2, defense: { damage: 34, rate: 0.45, range: 175, splash: 45, hitsAir: false }, color: 0x5a6b45 },
  pile: { id: 'pile', name: 'Loot Pile', blurb: "Stolen acorns and jars of sap, piled high. Smash it to take them home.", hp: 380, size: 2, loot: { coins: 220, glowsap: 220 }, color: 0xb59a4e },
  shaman: { id: 'shaman', name: 'Mire Shaman', blurb: "A reed hut where an old mire-witch brews bog tonic, patching up the buildings around her.", hp: 420, size: 2, mend: { amount: 30, interval: 3, range: 130 }, color: 0x7a4a8a },
  sludge: { id: 'sludge', name: 'Sludge Pit', blurb: "A bubbling pit of muck. Anything walking near it wades slowly, right under the Spit Towers.", hp: 360, size: 2, mire: { radius: 120, factor: 0.55 }, color: 0x5a4a2a },
  hive: { id: 'hive', name: 'Hornet Hive', blurb: "A papery nest hung from a dead branch, buzzing angrily. Knock it down and the swarm boils out to sting everyone close by, wings or no wings.", hp: 300, size: 2, burst: { radius: 100, damage: 45 }, color: 0xc8a050 },
  rattle: { id: 'rattle', name: 'Rattle Trap', blurb: "A sandy pit full of buried rattlesnakes. Walk past it and they strike at your ankles, and the venom keeps burning long after you leave.", hp: 340, size: 2, venom: { radius: 80, dps: 9, duration: 4 }, color: 0xc08a50 },
  menhir: { id: 'menhir', name: 'Standing Stone', blurb: "A tall grey stone dragged down from the Starheath moors and carved with old marks. While it stands, a heavy hush hangs over the buildings around it and blows land soft.", hp: 520, size: 2, ward: { radius: 110, cut: 0.3 }, color: 0x8a8a88 },
  hut: { id: 'hut', name: 'Mud Hut', blurb: "Where the critters sleep. Not much to it, but it counts toward the camp's destruction.", hp: 280, size: 2, color: 0x7a5a3a },
  wall: { id: 'wall', name: 'Stake Wall', blurb: "Sharpened stakes lashed together. Ground troops must chew through them.", hp: 220, size: 1, wall: true, color: 0x5a4632 },
};

export const RAID_TIME = 90; // seconds

export const CAMP_TIERS = [
  { name: 'Mudling Outpost', counts: { spit: 3, mortar: 1, pile: 2, hut: 3 }, walls: false },
  { name: 'Bogscum Warren', counts: { spit: 3, mortar: 1, shaman: 1, sludge: 1, hive: 1, pile: 3, hut: 3 }, walls: true },
  { name: 'Murkhorde Stronghold', counts: { spit: 3, mortar: 2, shaman: 2, sludge: 2, hive: 1, rattle: 1, menhir: 1, pile: 4, hut: 3 }, walls: true },
];
