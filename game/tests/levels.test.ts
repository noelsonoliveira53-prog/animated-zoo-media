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
