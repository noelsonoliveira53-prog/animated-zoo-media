import type { HeroDef } from './types';

// Champions of the Grove. Each hero grows stronger as it levels up during a battle.
export const HEROES: Record<string, HeroDef> = {
  bramble: {
    id: 'bramble',
    name: 'Bramble',
    title: 'Badger Knight',
    blurb: 'A stubborn old badger in bark armor. Holds the road against anything, and flings his shield at whatever flies over.',
    color: 0x6f8fa8,
    hp: 260,
    speed: 95,
    armor: 0.3,
    regen: 8,
    melee: true,
    toss: { name: 'Shield Toss', damage: 34, range: 160, interval: 2.5 },
    attack: { damage: 18, type: 'physical', range: 22, rate: 1.1, hitsAir: false, projectileSpeed: 0 },
    respawn: 14,
    passive: { kind: 'toughness', armor: 0.15, regen: 6, text: 'Thick Hide: extra armor and fast healing.' },
    active: {
      name: 'Earthshake',
      text: 'Slams the ground: damages and slows all ground enemies nearby.',
      cooldown: 16,
      kind: 'quake',
      damage: 70,
      damageType: 'physical',
      radius: 115,
      slow: { factor: 0.4, duration: 3 },
    },
  },
  fen: {
    id: 'fen',
    name: 'Fen',
    title: 'Heron Ranger',
    blurb: 'A sharp-eyed heron who never misses. Strikes flyers and ground alike.',
    color: 0x7fb0d8,
    hp: 160,
    speed: 115,
    armor: 0,
    regen: 6,
    melee: false,
    attack: { damage: 13, type: 'physical', range: 190, rate: 1.4, hitsAir: true, projectileSpeed: 600 },
    respawn: 12,
    passive: { kind: 'crit', chance: 0.25, mult: 2.5, text: 'Keen Eye: 25% chance for a critical hit.' },
    active: {
      name: 'Feather Storm',
      text: 'Fires a volley at up to 8 enemies in range.',
      cooldown: 14,
      kind: 'volley',
      damage: 45,
      damageType: 'physical',
      radius: 230,
      maxTargets: 8,
    },
  },
  ember: {
    id: 'ember',
    name: 'Ember',
    title: 'Fox Sage',
    blurb: 'A young fox who juggles foxfire. Nearby outposts work faster around her.',
    color: 0xff8a3c,
    hp: 180,
    speed: 105,
    armor: 0,
    regen: 6,
    melee: false,
    attack: { damage: 22, type: 'magic', range: 160, rate: 0.9, hitsAir: true, projectileSpeed: 420 },
    respawn: 12,
    passive: { kind: 'towerHaste', radius: 160, bonus: 0.25, text: 'Warm Glow: outposts within reach fire 25% faster.' },
    active: {
      name: 'Foxfire Ring',
      text: 'A ring of foxfire burns and slows everything around her, flyers included.',
      cooldown: 18,
      kind: 'ring',
      damage: 80,
      damageType: 'magic',
      radius: 140,
      slow: { factor: 0.6, duration: 2.5 },
    },
  },
  wren: {
    id: 'wren',
    name: 'Wren',
    title: 'Owl Lorekeeper',
    blurb: 'A bookish barn owl with a satchel of scrolls. Nothing escapes her notice, least of all loose coins.',
    color: 0xd8b880,
    hp: 170,
    speed: 110,
    armor: 0,
    regen: 6,
    melee: false,
    attack: { damage: 16, type: 'magic', range: 175, rate: 1.0, hitsAir: true, projectileSpeed: 480 },
    respawn: 12,
    passive: { kind: 'bounty', radius: 200, bonus: 0.3, text: "Scholar's Eye: enemies that fall near her drop 30% more coins." },
    active: {
      name: 'Hush',
      text: 'A deep hoot stills everything nearby: enemies all but stop for a few seconds.',
      cooldown: 18,
      kind: 'ring',
      damage: 30,
      damageType: 'magic',
      radius: 160,
      slow: { factor: 0.2, duration: 3 },
      fxColor: 0xbfe0ff,
    },
  },
};

export const HERO_ORDER = ['bramble', 'fen', 'ember', 'wren'];

/** XP needed to reach each level (index = level - 1). */
export const HERO_XP = [0, 40, 110, 220, 380, 600];
export const HERO_MAX_LEVEL = HERO_XP.length;

/** Stat multiplier for a hero level (1-based): +12% per level. */
export function heroLevelMult(level: number): number {
  return 1 + (level - 1) * 0.12;
}

export function levelForXp(xp: number): number {
  let lvl = 1;
  for (let i = 1; i < HERO_XP.length; i++) if (xp >= HERO_XP[i]) lvl = i + 1;
  return lvl;
}
