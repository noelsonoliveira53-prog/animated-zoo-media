import { describe, expect, it } from 'vitest';
import { Path } from '../src/systems/path';
import { snapRally } from '../src/systems/rallySnap';

const road = new Path([{ x: 0, y: 100 }, { x: 400, y: 100 }]);

describe('snapRally', () => {
  it('snaps a nearby drop onto the road', () => {
    const r = snapRally([road], { x: 150, y: 130 }, { x: 150, y: 40 }, 120);
    expect(r.point).toEqual({ x: 150, y: 100 });
    expect(r.ok).toBe(true);
  });
  it('rejects drops far from any road', () => {
    expect(snapRally([road], { x: 150, y: 220 }, { x: 150, y: 200 }, 300).point).toBeNull();
  });
  it('flags a road spot outside the tower reach', () => {
    const r = snapRally([road], { x: 390, y: 105 }, { x: 50, y: 40 }, 120);
    expect(r.point).not.toBeNull();
    expect(r.ok).toBe(false);
  });
  it('picks the closer of two roads', () => {
    const other = new Path([{ x: 0, y: 160 }, { x: 400, y: 160 }]);
    expect(snapRally([road, other], { x: 200, y: 150 }, { x: 200, y: 130 }, 200).point).toEqual({ x: 200, y: 160 });
  });
});
