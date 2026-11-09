// Pure tooltip placement (no Phaser import, so it is unit-testable).

export interface Rect {
  x: number;
  y: number;
  w: number;
  h: number;
}

/**
 * Top-left of a tw×th tooltip for a control at `r`: centred under it with a small gap, or above it when
 * there is no room below, and always kept `margin` px inside the screen.
 */
export function tipPosition(r: Rect, tw: number, th: number, screenW: number, screenH: number, gap = 8, margin = 6): { x: number; y: number } {
  let x = r.x + r.w / 2 - tw / 2;
  x = Math.max(margin, Math.min(screenW - margin - tw, x));
  let y = r.y + r.h + gap;
  if (y + th > screenH - margin) y = r.y - gap - th;
  y = Math.max(margin, y);
  return { x, y };
}
