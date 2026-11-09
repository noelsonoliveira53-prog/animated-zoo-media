/** Keyboard focus movement between on-screen controls (pure logic, no Phaser). */
export interface FocusPoint {
  x: number;
  y: number;
}
export type FocusDir = 'next' | 'prev' | 'up' | 'down' | 'left' | 'right';

/** Rows are grouped in bands this tall, so controls on roughly one line read left to right. */
const ROW_BAND = 28;

/** Indices of the points in reading order: top row first, left to right within a row. */
export function readingOrder(points: FocusPoint[]): number[] {
  return points
    .map((_, i) => i)
    .sort((a, b) => {
      const ra = Math.round(points[a].y / ROW_BAND);
      const rb = Math.round(points[b].y / ROW_BAND);
      return ra !== rb ? ra - rb : points[a].x - points[b].x;
    });
}

/**
 * The index focus moves to from `current` (-1 = nothing focused yet) in direction `dir`.
 * Tab order wraps. Arrows pick the nearest control in that direction, weighting sideways
 * distance double so focus moves along rows and columns, and stay put when nothing is there.
 */
export function nextFocus(points: FocusPoint[], current: number, dir: FocusDir): number {
  if (points.length === 0) return -1;
  const order = readingOrder(points);
  if (current < 0 || current >= points.length) return dir === 'prev' || dir === 'up' || dir === 'left' ? order[order.length - 1] : order[0];
  if (dir === 'next' || dir === 'prev') {
    const at = order.indexOf(current);
    const step = dir === 'next' ? 1 : -1;
    return order[(at + step + order.length) % order.length];
  }
  const [vx, vy] = dir === 'up' ? [0, -1] : dir === 'down' ? [0, 1] : dir === 'left' ? [-1, 0] : [1, 0];
  const c = points[current];
  let best = current;
  let bestScore = Infinity;
  points.forEach((p, i) => {
    if (i === current) return;
    const dx = p.x - c.x;
    const dy = p.y - c.y;
    const along = dx * vx + dy * vy;
    if (along <= 4) return;
    const side = Math.abs(dx * vy - dy * vx);
    const score = along + side * 2;
    if (score < bestScore) {
      bestScore = score;
      best = i;
    }
  });
  return best;
}

/** True for a control label that means "go back": Esc presses it when a scene has no Esc key of its own. */
export function isBackLabel(text: string): boolean {
  return /^\s*(←|✕|×|back\b|close\b|cancel\b|done\b|menu\b)/i.test(text);
}
