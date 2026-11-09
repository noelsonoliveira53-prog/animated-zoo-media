import { describe, expect, it } from 'vitest';
import { ENEMIES } from '../src/data/enemies';
import { gaitFor, poseFor, type Gait } from '../src/systems/gait';

describe('enemy gaits', () => {
  it('flyers flap and every enemy gets a gait', () => {
    for (const d of Object.values(ENEMIES)) {
      const g = gaitFor(d);
      if (d.flying) expect(g).toBe('flap');
      expect(['march', 'waddle', 'hop', 'scuttle', 'flap']).toContain(g);
    }
  });
  it('poses stay small and sane over a full cycle', () => {
    for (const g of ['march', 'waddle', 'hop', 'scuttle', 'flap'] as Gait[]) {
      for (let b = 0; b < 12; b += 0.37) {
        const p = poseFor(g, b);
        expect(p.lift).toBeGreaterThanOrEqual(0);
        expect(p.lift).toBeLessThanOrEqual(10);
        expect(Math.abs(p.sx - 1)).toBeLessThan(0.2);
        expect(Math.abs(p.sy - 1)).toBeLessThan(0.2);
        expect(Math.abs(p.rot)).toBeLessThan(0.12);
      }
    }
  });
  it('hoppers squash on landing and stretch in the air', () => {
    expect(poseFor('hop', 0).sy).toBeLessThan(1);
    expect(poseFor('hop', Math.PI / 2).sy).toBeGreaterThan(1);
    expect(poseFor('hop', Math.PI / 2).lift).toBeGreaterThan(8);
  });
});

import { unitPose } from '../src/systems/gait';
describe('soldier and hero poses', () => {
  it('walkers lean and fighters swing toward their facing; idle only breathes', () => {
    expect(unitPose('walk', 0, 0, 1).rot).toBeGreaterThan(0);
    expect(unitPose('walk', 0, 0, -1).rot).toBeLessThan(0);
    let maxSwing = 0;
    for (let t = 0; t < 500; t += 10) maxSwing = Math.max(maxSwing, unitPose('fight', t, 0, 1).rot);
    expect(maxSwing).toBeGreaterThan(0.15);
    for (let t = 0; t < 2000; t += 50) {
      const p = unitPose('idle', t, 1, 1);
      expect(p.rot).toBe(0);
      expect(Math.abs(p.sy - 1)).toBeLessThanOrEqual(0.03);
    }
  });
});
