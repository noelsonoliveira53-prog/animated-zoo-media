import { describe, expect, it } from 'vitest';
import { LEVELS, isLevelUnlocked, totalStars } from '../src/data/levels';
import { BattleSim } from '../src/systems/BattleSim';

describe('level data', () => {
  it('has at least 5 levels with valid layouts', () => {
    expect(LEVELS.length).toBeGreaterThanOrEqual(5);
    for (const l of LEVELS) {
      const sim = new BattleSim(l);
      expect(l.waves.length, l.id).toBeGreaterThanOrEqual(8);
      // Build pads must not sit on a road, and must be on screen.
      for (const s of l.slots) {
        expect(s.x, `${l.id} slot x`).toBeGreaterThan(30);
        expect(s.x).toBeLessThanOrEqual(1250);
        expect(s.y).toBeLessThan(700);
        for (const p of sim.paths) expect(p.distanceTo(s), `${l.id} slot ${s.x},${s.y}`).toBeGreaterThanOrEqual(55);
      }
    }
  });
  it('unlocks levels in order', () => {
    expect(isLevelUnlocked(0, {})).toBe(true);
    expect(isLevelUnlocked(1, {})).toBe(false);
    expect(isLevelUnlocked(1, { l1: 1 })).toBe(true);
    expect(isLevelUnlocked(2, { l1: 3 })).toBe(false);
    expect(totalStars({ l1: 3, l2: 2 })).toBe(5);
  });
});

import { REGIONS, regionOf } from '../src/data/levels';
describe('regions', () => {
  it('map every level to a region in order', () => {
    expect(regionOf(0)).toBe(0);
    expect(regionOf(4)).toBe(0);
    expect(regionOf(5)).toBe(1);
    for (let i = 0; i < LEVELS.length; i++) expect(REGIONS[regionOf(i)]).toBeDefined();
  });
  it('kill bounties scale with the level health multiplier', () => {
    const l = LEVELS.find((x) => (x.hpMult ?? 1) > 1.4)!;
    const sim = new BattleSim(l);
    const e = sim.spawn('mudling', 0, 100);
    const before = sim.coins;
    (sim as any).applyDamage(e, 1e6);
    expect(sim.coins - before).toBe(Math.round(5 * sim.waveHpMult()));
    expect(sim.waveHpMult()).toBeGreaterThan(1);
  });
});
