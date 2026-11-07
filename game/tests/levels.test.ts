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

describe('HUD clearance', () => {
  it('no build pad sits under the hero HUD, the spell buttons or the top bar', () => {
    const zones = [
      // Drawn extents of the HUD (portrait + skill circle, the two spell circles, the top bar).
      { name: 'hero HUD', x0: 16, y0: 620, x1: 200, y1: 712 },
      { name: 'spells', x0: 1000, y0: 620, x1: 1262, y1: 712 }, // three spell circles
      { name: 'top bar', x0: 0, y0: 0, x1: 1280, y1: 66 },
    ];
    for (const l of LEVELS) {
      for (const s of l.slots) {
        for (const z of zones) {
          // Build pads are 64×48.
          const inside = s.x + 32 > z.x0 && s.x - 32 < z.x1 && s.y + 24 > z.y0 && s.y - 24 < z.y1;
          expect(inside, `${l.name} pad (${s.x},${s.y}) under ${z.name}`).toBe(false);
        }
      }
    }
  });

  it('towers built near the top stay clear of the stats panel and the top-right buttons', () => {
    // A built tower rises about 75 px above its pad centre.
    const panels = [
      { name: 'stats panel', x0: 12, x1: 452, y1: 64 },
      { name: 'top-right buttons', x0: 836, x1: 1262, y1: 72 },
    ];
    for (const l of LEVELS)
      for (const s of l.slots)
        for (const p of panels) {
          const hidden = s.y - 75 < p.y1 && s.x + 32 > p.x0 && s.x - 32 < p.x1;
          expect(hidden, `${l.name} pad (${s.x},${s.y}) tower under the ${p.name}`).toBe(false);
        }
  });
});

describe('gate clearance', () => {
  it('no road exit puts its gate marker under the top-right buttons', () => {
    // BattleScene draws each gate at the road end clamped to x 60–1220, y 80–700, spanning ±40 px wide and 60 px up.
    for (const l of LEVELS) {
      for (const pts of l.paths) {
        const end = pts[pts.length - 1];
        const gx = Math.max(60, Math.min(1220, end.x));
        const gy = Math.max(80, Math.min(700, end.y));
        const underButtons = gx + 40 > 830 && gy - 60 < 72;
        expect(underButtons, `${l.name} gate at (${gx},${gy})`).toBe(false);
      }
    }
  });
});

describe('top HUD clearance for roads', () => {
  it('no horizontal road runs under the top HUD bar (enemies and flyers would hide behind it)', () => {
    for (const l of LEVELS)
      for (const pts of l.paths)
        for (let i = 1; i < pts.length; i++) {
          const a = pts[i - 1];
          const b = pts[i];
          const horizontal = a.y === b.y && Math.abs(a.x - b.x) > 60;
          expect(horizontal && a.y < 120, `${l.name}: road at y=${a.y}`).toBe(false);
        }
  });
});

describe('top entries', () => {
  it('roads entering from the top come down in the gap between the stats panel and the buttons', () => {
    for (const l of LEVELS)
      for (const pts of l.paths) {
        const a = pts[0];
        if (a.y >= 0) continue;
        const inGap = a.x >= 470 && a.x <= 830;
        expect(inGap || a.x > 1270, `${l.name}: top entry at x=${a.x}`).toBe(true);
      }
  });
});
