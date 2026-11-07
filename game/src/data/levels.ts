import type { LevelDef } from './types';

const MEADOW = { grass: 0x5f9e45, grassDark: 0x4d8a38, road: 0xc9a66b, roadEdge: 0xa8844e };
const FOREST = { grass: 0x4a8a3f, grassDark: 0x3b7534, road: 0xb89a64, roadEdge: 0x96784a };
const LAKE = { grass: 0x5a9a6a, grassDark: 0x4a8a5c, road: 0xc4b28a, roadEdge: 0xa08e66 };
const DEN = { grass: 0x3f6b48, grassDark: 0x325a3c, road: 0x8a7a5a, roadEdge: 0x6a5a3e };
const FEN = { grass: 0x4f8a52, grassDark: 0x3f7446, road: 0x9c8a62, roadEdge: 0x7d6c48 };

// Shared tail for Murkmaw's Den: all three roads meet at (600, 360).
const DEN_TAIL = [
  { x: 600, y: 360 },
  { x: 900, y: 360 },
  { x: 900, y: 170 },
  { x: 1150, y: 170 },
  { x: 1150, y: 560 },
  { x: 1320, y: 560 },
];

// Shared tail for Gloomfen Edge: both roads merge at (700, 360).
const FEN_TAIL = [
  { x: 700, y: 360 },
  { x: 700, y: 200 },
  { x: 1000, y: 200 },
  { x: 1000, y: 470 },
  { x: 1320, y: 470 },
];

export const LEVELS: LevelDef[] = [
  {
    id: 'l1',
    name: 'Mossgate Meadow',
    blurb: 'The first Murkhorde scouts creep toward the sanctuary gate. Learn the ropes.',
    mapPos: { x: 170, y: 560 },
    startCoins: 250,
    lives: 20,
    theme: MEADOW,
    paths: [
      [
        { x: -40, y: 200 },
        { x: 300, y: 200 },
        { x: 300, y: 500 },
        { x: 640, y: 500 },
        { x: 640, y: 260 },
        { x: 960, y: 260 },
        { x: 960, y: 560 },
        { x: 1320, y: 560 },
      ],
    ],
    slots: [
      { x: 200, y: 300 },
      { x: 400, y: 380 },
      { x: 400, y: 600 },
      { x: 540, y: 380 },
      { x: 760, y: 360 },
      { x: 860, y: 160 },
      { x: 860, y: 440 },
      { x: 1080, y: 460 },
      { x: 1050, y: 640 },
      { x: 180, y: 110 },
    ],
    waves: [
      { groups: [{ enemy: 'mudling', count: 6, interval: 1.2 }] },
      { groups: [{ enemy: 'mudling', count: 10, interval: 0.9 }] },
      {
        groups: [
          { enemy: 'mudling', count: 6, interval: 1.0 },
          { enemy: 'skitter', count: 6, interval: 0.7, delay: 4 },
        ],
      },
      { groups: [{ enemy: 'skitter', count: 14, interval: 0.5 }] },
      {
        groups: [
          { enemy: 'mudling', count: 10, interval: 0.8 },
          { enemy: 'shellback', count: 2, interval: 3, delay: 5 },
        ],
      },
      {
        groups: [
          { enemy: 'shellback', count: 5, interval: 2.2 },
          { enemy: 'skitter', count: 10, interval: 0.5, delay: 2 },
        ],
      },
      {
        groups: [
          { enemy: 'mudling', count: 16, interval: 0.6 },
          { enemy: 'skitter', count: 12, interval: 0.45, delay: 3 },
          { enemy: 'shellback', count: 4, interval: 2, delay: 6 },
        ],
      },
      {
        groups: [
          { enemy: 'shellback', count: 5, interval: 2 },
          { enemy: 'skitter', count: 14, interval: 0.45, delay: 4 },
          { enemy: 'mudling', count: 14, interval: 0.6, delay: 8 },
        ],
      },
    ],
  },
  {
    id: 'l2',
    name: 'Gloomfen Edge',
    blurb: 'Two bog roads meet at the fen. Old Murkmaw himself comes to test you.',
    mapPos: { x: 380, y: 470 },
    startCoins: 380,
    lives: 20,
    theme: FEN,
    paths: [
      [{ x: -40, y: 140 }, { x: 260, y: 140 }, { x: 260, y: 360 }, ...FEN_TAIL],
      [{ x: -40, y: 600 }, { x: 440, y: 600 }, { x: 440, y: 360 }, ...FEN_TAIL],
    ],
    slots: [
      { x: 160, y: 240 },
      { x: 360, y: 250 },
      { x: 340, y: 470 },
      { x: 540, y: 470 },
      { x: 560, y: 260 },
      { x: 820, y: 290 },
      { x: 850, y: 110 },
      { x: 880, y: 560 },
      { x: 1110, y: 330 },
      { x: 1130, y: 580 },
      { x: 250, y: 680 },
    ],
    waves: [
      { groups: [{ enemy: 'mudling', count: 8, interval: 1 }, { enemy: 'mudling', count: 6, interval: 1.2, path: 1, delay: 3 }] },
      { groups: [{ enemy: 'gnat', count: 10, interval: 0.4 }, { enemy: 'skitter', count: 8, interval: 0.7, path: 1 }] },
      { groups: [{ enemy: 'reedguard', count: 5, interval: 1.8 }, { enemy: 'mudling', count: 10, interval: 0.8, path: 1 }] },
      { groups: [{ enemy: 'splotch', count: 5, interval: 2.2, path: 1 }, { enemy: 'gloomwing', count: 6, interval: 1.2, delay: 4 }] },
      { groups: [{ enemy: 'wispling', count: 8, interval: 1 }, { enemy: 'shellback', count: 5, interval: 1.8, path: 1 }] },
      {
        groups: [
          { enemy: 'bogmender', count: 2, interval: 4, delay: 2 },
          { enemy: 'reedguard', count: 6, interval: 1.4 },
          { enemy: 'thornhog', count: 4, interval: 2, path: 1, delay: 3 },
        ],
      },
      { groups: [{ enemy: 'gnat', count: 18, interval: 0.3, path: 1 }, { enemy: 'gloomwing', count: 8, interval: 0.9 }] },
      { groups: [{ enemy: 'bogbrute', count: 1, interval: 1 }, { enemy: 'mudling', count: 12, interval: 0.6, path: 1 }, { enemy: 'bogmender', count: 2, interval: 3, delay: 4 }] },
      {
        groups: [
          { enemy: 'thornhog', count: 8, interval: 1.2 },
          { enemy: 'wispling', count: 10, interval: 0.8, path: 1 },
          { enemy: 'splotch', count: 4, interval: 2, delay: 6 },
        ],
      },
      {
        groups: [
          { enemy: 'bogbrute', count: 3, interval: 4, path: 1 },
          { enemy: 'reedguard', count: 10, interval: 1 },
          { enemy: 'gloomwing', count: 12, interval: 0.7, delay: 5 },
        ],
      },
      {
        groups: [
          { enemy: 'bogmender', count: 4, interval: 2.5 },
          { enemy: 'shellback', count: 10, interval: 1, path: 1 },
          { enemy: 'thornhog', count: 8, interval: 1.1, delay: 4 },
          { enemy: 'gnat', count: 20, interval: 0.3, path: 1, delay: 8 },
        ],
      },
      {
        groups: [
          { enemy: 'murkmaw', count: 1, interval: 1, delay: 6 },
          { enemy: 'mudling', count: 12, interval: 0.6 },
          { enemy: 'skitter', count: 12, interval: 0.6, path: 1 },
        ],
      },
    ],
  },
  {
    id: 'l3',
    name: 'Thornwood Hollow',
    blurb: 'A long road snakes through the old wood. Thornhogs charge and wisplings shrug off magic.',
    mapPos: { x: 600, y: 330 },
    startCoins: 400,
    lives: 20,
    theme: FOREST,
    paths: [
      [
        { x: -40, y: 540 },
        { x: 220, y: 540 },
        { x: 220, y: 150 },
        { x: 520, y: 150 },
        { x: 520, y: 560 },
        { x: 820, y: 560 },
        { x: 820, y: 180 },
        { x: 1100, y: 180 },
        { x: 1100, y: 440 },
        { x: 1320, y: 440 },
      ],
    ],
    slots: [
      { x: 120, y: 380 },
      { x: 370, y: 260 },
      { x: 370, y: 450 },
      { x: 670, y: 300 },
      { x: 670, y: 470 },
      { x: 670, y: 660 },
      { x: 960, y: 300 },
      { x: 960, y: 470 },
      { x: 1200, y: 320 },
      { x: 1240, y: 560 },
    ],
    waves: [
      { groups: [{ enemy: 'mudling', count: 10, interval: 0.8 }, { enemy: 'skitter', count: 6, interval: 0.6, delay: 5 }] },
      { groups: [{ enemy: 'thornhog', count: 3, interval: 2.5 }, { enemy: 'mudling', count: 8, interval: 0.8, delay: 2 }] },
      { groups: [{ enemy: 'wispling', count: 8, interval: 1 }, { enemy: 'gnat', count: 10, interval: 0.4, delay: 4 }] },
      { groups: [{ enemy: 'reedguard', count: 6, interval: 1.4 }, { enemy: 'thornhog', count: 4, interval: 2, delay: 5 }] },
      { groups: [{ enemy: 'splotch', count: 6, interval: 1.8 }, { enemy: 'gloomwing', count: 6, interval: 1, delay: 3 }] },
      { groups: [{ enemy: 'bogmender', count: 2, interval: 3 }, { enemy: 'shellback', count: 8, interval: 1.2, delay: 1 }] },
      { groups: [{ enemy: 'wispling', count: 12, interval: 0.7 }, { enemy: 'thornhog', count: 6, interval: 1.4, delay: 4 }] },
      { groups: [{ enemy: 'gnat', count: 24, interval: 0.25 }, { enemy: 'gloomwing', count: 8, interval: 0.8, delay: 3 }] },
      { groups: [{ enemy: 'bogbrute', count: 2, interval: 5 }, { enemy: 'bogmender', count: 3, interval: 2.5, delay: 2 }, { enemy: 'mudling', count: 16, interval: 0.5, delay: 4 }] },
      { groups: [{ enemy: 'thornhog', count: 10, interval: 0.9 }, { enemy: 'reedguard', count: 8, interval: 1.1, delay: 3 }] },
      { groups: [{ enemy: 'splotch', count: 10, interval: 1.1 }, { enemy: 'wispling', count: 10, interval: 0.8, delay: 4 }, { enemy: 'gloomwing', count: 10, interval: 0.7, delay: 8 }] },
      { groups: [{ enemy: 'bogbrute', count: 3, interval: 4 }, { enemy: 'thornhog', count: 8, interval: 0.9, delay: 3 }, { enemy: 'bogmender', count: 4, interval: 2.5, delay: 6 }] },
    ],
  },
  {
    id: 'l4',
    name: 'Mirelake Crossing',
    blurb: 'Two separate roads skirt the lake, each with its own gate. Split your defenses wisely.',
    mapPos: { x: 840, y: 420 },
    startCoins: 700,
    lives: 25,
    theme: LAKE,
    ponds: [
      { x: 560, y: 655, w: 220, h: 64 },
      { x: 1185, y: 380, w: 150, h: 46 },
      { x: 600, y: 380, w: 260, h: 36 },
    ],
    paths: [
      [{ x: -40, y: 170 }, { x: 400, y: 170 }, { x: 400, y: 330 }, { x: 800, y: 330 }, { x: 800, y: 170 }, { x: 1320, y: 170 }],
      [{ x: -40, y: 560 }, { x: 350, y: 560 }, { x: 350, y: 430 }, { x: 760, y: 430 }, { x: 760, y: 580 }, { x: 1320, y: 580 }],
    ],
    slots: [
      { x: 200, y: 270 },
      { x: 200, y: 450 },
      { x: 500, y: 90 },
      { x: 560, y: 250 },
      { x: 560, y: 520 },
      { x: 950, y: 260 },
      { x: 950, y: 480 },
      { x: 1150, y: 300 },
      { x: 1150, y: 460 },
      { x: 900, y: 660 },
    ],
    waves: [
      { groups: [{ enemy: 'mudling', count: 6, interval: 1.1 }, { enemy: 'mudling', count: 6, interval: 1.1, path: 1, delay: 3 }] },
      { groups: [{ enemy: 'skitter', count: 8, interval: 0.7 }, { enemy: 'reedguard', count: 3, interval: 2, path: 1 }] },
      { groups: [{ enemy: 'gloomwing', count: 6, interval: 1.1 }, { enemy: 'shellback', count: 3, interval: 2, path: 1 }] },
      { groups: [{ enemy: 'wispling', count: 6, interval: 1, path: 1 }, { enemy: 'thornhog', count: 3, interval: 2.2 }] },
      { groups: [{ enemy: 'splotch', count: 4, interval: 2.2 }, { enemy: 'splotch', count: 4, interval: 2.2, path: 1 }, { enemy: 'bogmender', count: 2, interval: 4, delay: 3 }] },
      { groups: [{ enemy: 'gnat', count: 10, interval: 0.35, path: 1 }, { enemy: 'reedguard', count: 6, interval: 1.3 }] },
      { groups: [{ enemy: 'bogbrute', count: 1, interval: 1 }, { enemy: 'bogbrute', count: 1, interval: 1, path: 1, delay: 4 }, { enemy: 'skitter', count: 16, interval: 0.4, delay: 2 }] },
      { groups: [{ enemy: 'thornhog', count: 6, interval: 1.2, path: 1 }, { enemy: 'wispling', count: 8, interval: 0.9 }, { enemy: 'gloomwing', count: 8, interval: 0.9, delay: 5, path: 1 }] },
      { groups: [{ enemy: 'shellback', count: 8, interval: 1.1 }, { enemy: 'bogmender', count: 2, interval: 3, path: 1 }, { enemy: 'splotch', count: 6, interval: 1.2, path: 1, delay: 2 }] },
      { groups: [{ enemy: 'gnat', count: 12, interval: 0.3 }, { enemy: 'gnat', count: 12, interval: 0.3, path: 1 }, { enemy: 'gloomwing', count: 8, interval: 0.8, delay: 4 }] },
      { groups: [{ enemy: 'bogbrute', count: 2, interval: 4 }, { enemy: 'thornhog', count: 6, interval: 1.1, path: 1 }, { enemy: 'reedguard', count: 6, interval: 1, delay: 5 }] },
      { groups: [{ enemy: 'bogbrute', count: 2, interval: 4, path: 1 }, { enemy: 'wispling', count: 10, interval: 0.8 }, { enemy: 'bogmender', count: 3, interval: 2.5, delay: 3, path: 1 }, { enemy: 'thornhog', count: 6, interval: 1.1, delay: 6 }] },
    ],
  },
  {
    id: 'l5',
    name: "Murkmaw's Den",
    blurb: 'Three roads pour out of the deep bog. End this: defeat Old Murkmaw in his own den.',
    mapPos: { x: 1090, y: 260 },
    startCoins: 480,
    lives: 20,
    theme: DEN,
    paths: [
      [{ x: -40, y: 150 }, { x: 300, y: 150 }, { x: 300, y: 360 }, ...DEN_TAIL],
      [{ x: -40, y: 580 }, { x: 300, y: 580 }, { x: 300, y: 360 }, ...DEN_TAIL],
      [{ x: 600, y: -40 }, ...DEN_TAIL],
    ],
    slots: [
      { x: 150, y: 260 },
      { x: 150, y: 470 },
      { x: 450, y: 250 },
      { x: 450, y: 470 },
      { x: 750, y: 250 },
      { x: 750, y: 470 },
      { x: 1025, y: 280 },
      { x: 1025, y: 450 },
      { x: 1250, y: 400 },
      { x: 790, y: 95 },
    ],
    waves: [
      { groups: [{ enemy: 'mudling', count: 8, interval: 0.9 }, { enemy: 'mudling', count: 8, interval: 0.9, path: 1, delay: 2 }, { enemy: 'skitter', count: 6, interval: 0.7, path: 2, delay: 4 }] },
      { groups: [{ enemy: 'reedguard', count: 5, interval: 1.6, path: 2 }, { enemy: 'gnat', count: 12, interval: 0.4 }] },
      { groups: [{ enemy: 'thornhog', count: 5, interval: 1.8, path: 1 }, { enemy: 'wispling', count: 6, interval: 1, path: 2 }] },
      { groups: [{ enemy: 'splotch', count: 6, interval: 1.6 }, { enemy: 'gloomwing', count: 8, interval: 0.9, path: 2, delay: 3 }] },
      { groups: [{ enemy: 'bogmender', count: 3, interval: 3, path: 2 }, { enemy: 'shellback', count: 8, interval: 1.2, path: 1 }, { enemy: 'skitter', count: 12, interval: 0.4 }] },
      { groups: [{ enemy: 'bogbrute', count: 2, interval: 5, path: 2 }, { enemy: 'mudling', count: 20, interval: 0.4, path: 1 }] },
      { groups: [{ enemy: 'gnat', count: 24, interval: 0.25, path: 2 }, { enemy: 'gloomwing', count: 10, interval: 0.8 }, { enemy: 'thornhog', count: 6, interval: 1.4, path: 1, delay: 4 }] },
      { groups: [{ enemy: 'wispling', count: 12, interval: 0.7 }, { enemy: 'reedguard', count: 10, interval: 1, path: 1 }, { enemy: 'bogmender', count: 3, interval: 3, path: 2, delay: 5 }] },
      { groups: [{ enemy: 'splotch', count: 10, interval: 1.1, path: 2 }, { enemy: 'thornhog', count: 10, interval: 1, delay: 3 }, { enemy: 'bogbrute', count: 2, interval: 4, path: 1, delay: 6 }] },
      { groups: [{ enemy: 'shellback', count: 12, interval: 0.9 }, { enemy: 'wispling', count: 12, interval: 0.8, path: 1 }, { enemy: 'gloomwing', count: 12, interval: 0.7, path: 2, delay: 4 }] },
      { groups: [{ enemy: 'bogbrute', count: 4, interval: 3.5, path: 2 }, { enemy: 'bogmender', count: 4, interval: 2.5 }, { enemy: 'thornhog', count: 12, interval: 0.8, path: 1, delay: 3 }] },
      { groups: [{ enemy: 'gnat', count: 30, interval: 0.2 }, { enemy: 'gnat', count: 30, interval: 0.2, path: 1 }, { enemy: 'gloomwing', count: 14, interval: 0.6, path: 2, delay: 3 }] },
      { groups: [{ enemy: 'reedguard', count: 14, interval: 0.8, path: 2 }, { enemy: 'splotch', count: 12, interval: 1 }, { enemy: 'bogbrute', count: 3, interval: 4, path: 1, delay: 5 }] },
      { groups: [{ enemy: 'bogbrute', count: 5, interval: 3, path: 1 }, { enemy: 'wispling', count: 16, interval: 0.6, path: 2 }, { enemy: 'bogmender', count: 5, interval: 2.4, delay: 4 }] },
      { groups: [{ enemy: 'murkmaw', count: 1, interval: 1, path: 2, delay: 8 }, { enemy: 'thornhog', count: 12, interval: 0.8 }, { enemy: 'skitter', count: 16, interval: 0.4, path: 1 }, { enemy: 'bogbrute', count: 2, interval: 6, delay: 12, path: 1 }] },
    ],
  },
];

/** A level is open once the previous one has been beaten (at least 1 star). */
export function isLevelUnlocked(index: number, stars: Record<string, number>): boolean {
  if (index <= 0) return true;
  const prev = LEVELS[index - 1];
  return !!prev && (stars[prev.id] ?? 0) > 0;
}

export function totalStars(stars: Record<string, number>): number {
  return LEVELS.reduce((n, l) => n + (stars[l.id] ?? 0), 0);
}
