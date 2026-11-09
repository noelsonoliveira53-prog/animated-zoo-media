import type { LevelDef } from './types';

/** Light weather drawn over a battle map, picked from the map's theme. Purely visual. */
export type WeatherKind = 'leaves' | 'spores' | 'rain' | 'wind' | 'sand' | 'bubbles' | 'sparkles' | 'down' | 'soot' | 'pollen' | 'spray' | 'none';

export interface WeatherSpec {
  kind: WeatherKind;
  colors: number[];
  /** spawn interval in ms (lower = denser) */
  every: number;
}

type ThemeFlags = LevelDef['theme'];

/** First matching flag wins; snow and lava maps keep their own embers and snowfall. */
const TABLE: [keyof ThemeFlags, WeatherSpec][] = [
  ['snow', { kind: 'none', colors: [], every: 0 }],
  ['lava', { kind: 'none', colors: [], every: 0 }],
  ['storm', { kind: 'rain', colors: [0xbfd8ff], every: 40 }],
  ['gale', { kind: 'wind', colors: [0xffffff], every: 260 }],
  ['dunes', { kind: 'sand', colors: [0xe8c890, 0xd8b070], every: 90 }],
  ['canyon', { kind: 'sand', colors: [0xd89a6a, 0xc88a5a], every: 140 }],
  ['reef', { kind: 'bubbles', colors: [0xd8f4ff], every: 260 }],
  ['shoal', { kind: 'spray', colors: [0xf0faff], every: 300 }],
  ['flotilla', { kind: 'spray', colors: [0xf0faff], every: 300 }],
  ['crystals', { kind: 'sparkles', colors: [0xd8c8ff, 0xffffff, 0xa8e8ff], every: 220 }],
  ['shrooms', { kind: 'spores', colors: [0xc8ffb0, 0xe0b0ff], every: 260 }],
  ['bog', { kind: 'spores', colors: [0xc8e890, 0xa8d870], every: 280 }],
  ['mist', { kind: 'spores', colors: [0xe8f0ff], every: 320 }],
  ['abyss', { kind: 'spores', colors: [0xa070ff, 0x70a0ff], every: 260 }],
  ['gears', { kind: 'soot', colors: [0x3a3430, 0x5a524a], every: 200 }],
  ['amber', { kind: 'pollen', colors: [0xffd060, 0xffe8a0], every: 240 }],
  ['comb', { kind: 'pollen', colors: [0xffd23c, 0xffe8a0], every: 220 }],
  ['ruins', { kind: 'down', colors: [0xf4f0e4], every: 360 }],
  ['thistle', { kind: 'down', colors: [0xf4f0ff, 0xe8d8ff], every: 300 }],
  ['heath', { kind: 'down', colors: [0xf4e8f0], every: 340 }],
  ['wold', { kind: 'down', colors: [0xf8f4e8], every: 360 }],
  ['orchard', { kind: 'leaves', colors: [0xff9a8a, 0xffd0e0, 0x8fdc5a], every: 300 }],
  ['canopy', { kind: 'leaves', colors: [0x5a9a3a, 0x8fdc5a, 0x3f7a2e], every: 280 }],
];

/** Default for plain meadows: a few drifting leaves. */
const MEADOW: WeatherSpec = { kind: 'leaves', colors: [0x8fdc5a, 0x6aae42, 0xe8c050], every: 520 };

export function weatherFor(theme: ThemeFlags): WeatherSpec {
  for (const [flag, spec] of TABLE) if (theme[flag]) return spec;
  return MEADOW;
}

/** Which ambience bed a battle map plays (see sfx.startAmbience). */
export function ambienceFor(theme: ThemeFlags): 'wind' | 'rain' | 'water' | 'crackle' | 'meadow' {
  if (theme.lava) return 'crackle';
  const k = weatherFor(theme).kind;
  if (k === 'rain') return 'rain';
  if (k === 'bubbles' || k === 'spray' || theme.brook) return 'water';
  if (theme.snow || k === 'wind' || k === 'sand' || k === 'down') return 'wind';
  return 'meadow';
}
