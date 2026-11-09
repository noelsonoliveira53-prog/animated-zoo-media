import type { Enemy } from './BattleSim';

/** How far above its ground position a flyer is drawn (matches the battle view's 34 px air lift). */
export const AIR_LIFT = 34;

/**
 * The enemy a tap at (x, y) lands on: the closest living one whose drawn body (lifted for flyers) is within its
 * radius plus `slack` pixels, so small foes are still easy to tap on a phone. Null when the tap hits no one.
 */
export function pickEnemy(enemies: readonly Enemy[], x: number, y: number, slack = 14): Enemy | null {
  let best: Enemy | null = null;
  let bestD = Infinity;
  for (const e of enemies) {
    if (e.hp <= 0) continue;
    const ey = e.pos.y - (e.def.flying ? AIR_LIFT : 0);
    const d = Math.hypot(e.pos.x - x, ey - y);
    if (d <= e.def.radius + slack && d < bestD) {
      best = e;
      bestD = d;
    }
  }
  return best;
}
