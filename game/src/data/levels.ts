import type { LevelDef } from './types';

const MEADOW = { grass: 0x5f9e45, grassDark: 0x4d8a38, road: 0xc9a66b, roadEdge: 0xa8844e };
const FEN = { grass: 0x4f8a52, grassDark: 0x3f7446, road: 0x9c8a62, roadEdge: 0x7d6c48 };

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
];
