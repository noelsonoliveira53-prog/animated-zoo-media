import { describe, expect, it } from 'vitest';
import { regionProgress } from '../src/systems/mapProgress';
import { LEVELS, REGIONS } from '../src/data/levels';

describe('regionProgress', () => {
  it('a fresh save points at the first level', () => {
    const p = regionProgress(0, {});
    expect(p).toMatchObject({ stars: 0, max: REGIONS[0].count * 3, done: false });
    expect(p.next).toEqual({ index: 0, name: LEVELS[0].name });
  });
  it('counts stars and moves the next level along', () => {
    const p = regionProgress(0, { [LEVELS[0].id]: 3, [LEVELS[1].id]: 2 });
    expect(p.stars).toBe(5);
    expect(p.next?.index).toBe(2);
  });
  it('a fully starred region is done with nothing next', () => {
    const stars: Record<string, number> = {};
    for (let i = 0; i < REGIONS[0].count; i++) stars[LEVELS[i].id] = 3;
    expect(regionProgress(0, stars)).toMatchObject({ done: true, next: null, stars: REGIONS[0].count * 3 });
  });
});
