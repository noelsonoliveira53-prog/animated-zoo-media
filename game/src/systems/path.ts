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

  /** Closest point on the path to p, and how far along the path it lies. */
  closest(p: Vec2): { point: Vec2; along: number; distance: number } {
    let best = { point: this.points[0], along: 0, distance: Infinity };
    for (let i = 1; i < this.points.length; i++) {
      const a = this.points[i - 1];
      const b = this.points[i];
      const dx = b.x - a.x;
      const dy = b.y - a.y;
      const len2 = dx * dx + dy * dy;
      let t = len2 === 0 ? 0 : ((p.x - a.x) * dx + (p.y - a.y) * dy) / len2;
      t = Math.max(0, Math.min(1, t));
      const q = { x: a.x + dx * t, y: a.y + dy * t };
      const d = Math.hypot(p.x - q.x, p.y - q.y);
      if (d < best.distance) best = { point: q, along: this.cumulative[i - 1] + Math.sqrt(len2) * t, distance: d };
    }
    return best;
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

/** A spot beside a road: where it sits, which side, and the outward unit normal (pointing away from the road). */
export interface EdgeSpot {
  x: number;
  y: number;
  nx: number;
  ny: number;
  side: -1 | 1;
}

/**
 * Spots along both edges of a road polyline, `offset` px from its centre line, about every `spacing` px
 * (`jitter(k)` returns a per-spot extra in px, so callers can keep it seeded). Ends of segments are skipped
 * by `margin` px so corners stay clean.
 */
export function roadEdgeSpots(pts: Vec2[], spacing: number, offset: number, jitter: () => number = () => 0, margin = 14): EdgeSpot[] {
  const out: EdgeSpot[] = [];
  for (let k = 1; k < pts.length; k++) {
    const a = pts[k - 1];
    const b = pts[k];
    const len = Math.hypot(b.x - a.x, b.y - a.y);
    if (len < margin * 2) continue;
    const nx = -(b.y - a.y) / len;
    const ny = (b.x - a.x) / len;
    for (let d = margin; d < len - margin; d += Math.max(4, spacing + jitter())) {
      for (const side of [-1, 1] as const) {
        out.push({ x: a.x + ((b.x - a.x) * d) / len + nx * side * offset, y: a.y + ((b.y - a.y) * d) / len + ny * side * offset, nx: nx * side, ny: ny * side, side });
      }
    }
  }
  return out;
}
