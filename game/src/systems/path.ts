import type { Vec2 } from '../data/types';

/** A polyline path with precomputed segment lengths for distance -> position lookup. */
export class Path {
  readonly points: Vec2[];
  readonly cumulative: number[];
  readonly length: number;

  constructor(points: Vec2[]) {
    if (points.length < 2) throw new Error('Path needs at least 2 points');
    this.points = points;
    this.cumulative = [0];
    let total = 0;
    for (let i = 1; i < points.length; i++) {
      total += Math.hypot(points[i].x - points[i - 1].x, points[i].y - points[i - 1].y);
      this.cumulative.push(total);
    }
    this.length = total;
  }

  /** Position at a distance along the path (clamped). */
  pointAt(distance: number): Vec2 {
    const d = Math.max(0, Math.min(this.length, distance));
    let i = 1;
    while (i < this.cumulative.length - 1 && this.cumulative[i] < d) i++;
    const a = this.points[i - 1];
    const b = this.points[i];
    const segLen = this.cumulative[i] - this.cumulative[i - 1];
    const t = segLen === 0 ? 0 : (d - this.cumulative[i - 1]) / segLen;
    return { x: a.x + (b.x - a.x) * t, y: a.y + (b.y - a.y) * t };
  }

  /** Minimum distance from a point to the path polyline. */
  distanceTo(p: Vec2): number {
    let best = Infinity;
    for (let i = 1; i < this.points.length; i++) {
      best = Math.min(best, distToSegment(p, this.points[i - 1], this.points[i]));
    }
    return best;
  }
}

export function distToSegment(p: Vec2, a: Vec2, b: Vec2): number {
  const dx = b.x - a.x;
  const dy = b.y - a.y;
  const len2 = dx * dx + dy * dy;
  let t = len2 === 0 ? 0 : ((p.x - a.x) * dx + (p.y - a.y) * dy) / len2;
  t = Math.max(0, Math.min(1, t));
  return Math.hypot(p.x - (a.x + dx * t), p.y - (a.y + dy * t));
}
