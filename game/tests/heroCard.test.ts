import { describe, expect, it } from 'vitest';
import { HEROES, HERO_MAX_LEVEL, HERO_XP } from '../src/data/heroes';
import type { HeroDef } from '../src/data/types';
import { heroCardRows, heroXpProgress } from '../src/systems/heroCard';

describe('hero card', () => {
  it('XP progress runs 0..1 within a level', () => {
    expect(heroXpProgress(0, 1)).toMatchObject({ have: 0, frac: 0, max: false });
    const mid = heroXpProgress((HERO_XP[1] + HERO_XP[2]) / 2, 2);
    expect(mid.frac).toBeCloseTo(0.5);
    expect(heroXpProgress(99999, HERO_MAX_LEVEL)).toMatchObject({ max: true, frac: 1 });
  });
  it('bars stay in range and preview the next level until max', () => {
    for (const d of Object.values(HEROES) as HeroDef[]) {
      for (let lv = 1; lv <= HERO_MAX_LEVEL; lv++) {
        const rows = heroCardRows(d, lv);
        for (const r of rows) { expect(r.value).toBeGreaterThan(0); expect(r.value).toBeLessThanOrEqual(1); }
        expect(rows[0].next !== null).toBe(lv < HERO_MAX_LEVEL);
        expect(rows[2].next).toBeNull(); // speed doesn't grow with level
      }
    }
  });
});
