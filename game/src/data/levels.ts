import type { LevelDef } from './types';

const MEADOW = { grass: 0x5f9e45, grassDark: 0x4d8a38, road: 0xc9a66b, roadEdge: 0xa8844e };

export const LEVELS: LevelDef[] = [
  {
    id: 'l1',
    name: 'Mossgate Meadow',
    startCoins: 220,
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
      { x: 1100, y: 660 },
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
          { enemy: 'shellback', count: 8, interval: 1.6 },
          { enemy: 'skitter', count: 20, interval: 0.35, delay: 4 },
          { enemy: 'mudling', count: 14, interval: 0.6, delay: 8 },
        ],
      },
    ],
  },
];
