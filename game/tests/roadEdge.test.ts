import { describe, expect, it } from 'vitest';
import { distToSegment, roadEdgeSpots } from '../src/systems/path';

describe('road edge spots', () => {
  const road = [{ x: 0, y: 100 }, { x: 300, y: 100 }, { x: 300, y: 400 }];
  const spots = roadEdgeSpots(road, 40, 30);
  it('sit the requested distance from the road on both sides', () => {
    expect(spots.length).toBeGreaterThan(20);
    // every spot is 30 px from the road, except inner-corner spots that also come near the next segment
    const ds = spots.map((s) => Math.min(distToSegment(s, road[0], road[1]), distToSegment(s, road[1], road[2])));
    for (const d of ds) expect(d).toBeLessThanOrEqual(30 + 1e-6);
    expect(ds.filter((d) => Math.abs(d - 30) < 1e-6).length).toBeGreaterThan(spots.length * 0.9);
    expect(spots.some((s) => s.side === 1)).toBe(true);
    expect(spots.some((s) => s.side === -1)).toBe(true);
  });
  it('carry an outward unit normal', () => {
    for (const s of spots) {
      expect(Math.hypot(s.nx, s.ny)).toBeCloseTo(1, 6);
      const foot = { x: s.x - s.nx * 30, y: s.y - s.ny * 30 };
      const d = Math.min(distToSegment(foot, road[0], road[1]), distToSegment(foot, road[1], road[2]));
      expect(d).toBeLessThan(1e-6);
    }
  });
  it('are spaced along each segment and skip short ones', () => {
    const top = spots.filter((s) => s.y < 100 && s.x < 290).map((s) => s.x).sort((a, b) => a - b);
    for (let i = 1; i < top.length; i++) expect(top[i] - top[i - 1]).toBeCloseTo(40, 5);
    expect(roadEdgeSpots([{ x: 0, y: 0 }, { x: 20, y: 0 }], 10, 30)).toEqual([]);
  });
});
