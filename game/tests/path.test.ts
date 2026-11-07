import { describe, expect, it } from 'vitest';
import { Path } from '../src/systems/path';

describe('Path', () => {
  const p = new Path([
    { x: 0, y: 0 },
    { x: 100, y: 0 },
    { x: 100, y: 50 },
  ]);
  it('computes total length', () => expect(p.length).toBe(150));
  it('interpolates positions', () => {
    expect(p.pointAt(50)).toEqual({ x: 50, y: 0 });
    expect(p.pointAt(125)).toEqual({ x: 100, y: 25 });
  });
  it('clamps out-of-range distances', () => {
    expect(p.pointAt(-10)).toEqual({ x: 0, y: 0 });
    expect(p.pointAt(999)).toEqual({ x: 100, y: 50 });
  });
  it('measures distance to the polyline', () => {
    expect(p.distanceTo({ x: 50, y: 20 })).toBe(20);
  });
});
