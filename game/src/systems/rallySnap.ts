import type { Vec2 } from '../data/types';
import type { Path } from './path';

/** How far from the road a tap or drag still snaps onto it. */
export const RALLY_SNAP = 46;

/**
 * Where a rally flag dropped at `p` would land: the nearest point on any road (if within `snap` px of it), and
 * whether that spot is inside the tower's reach. `point` is null when `p` is too far from every road.
 */
export function snapRally(paths: readonly Path[], p: Vec2, towerPos: Vec2, range: number, snap = RALLY_SNAP): { point: Vec2 | null; ok: boolean } {
  let best: { point: Vec2; distance: number } | null = null;
  for (const path of paths) {
    const c = path.closest(p);
    if (!best || c.distance < best.distance) best = c;
  }
  if (!best || best.distance > snap) return { point: null, ok: false };
  const ok = Math.hypot(best.point.x - towerPos.x, best.point.y - towerPos.y) <= range;
  return { point: { x: best.point.x, y: best.point.y }, ok };
}
