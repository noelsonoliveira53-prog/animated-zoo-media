/** Small readability helpers for foes on the battlefield (pure, testable). */

/** Relative luminance-ish brightness of a 0xRRGGBB colour, 0..1. */
export function brightness(color: number): number {
  const r = (color >> 16) & 255;
  const g = (color >> 8) & 255;
  const b = color & 255;
  return (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255;
}

/** Ground-shadow alpha under a foe: deeper on pale roads (stone, sand, snow) so pale foes stay grounded and readable. */
export function foeShadowAlpha(road: number, flying: boolean): number {
  const base = flying ? 0.22 : 0.2;
  return brightness(road) > 0.6 ? base + 0.14 : base;
}

/**
 * Vertical offset for a floating label so labels that pop within `windowMs` of each other stack instead of
 * overlapping. `recent` holds the times of earlier labels; returns the offset and the pruned list with `now` added.
 */
export function stackLabel(recent: number[], now: number, windowMs = 1500, step = 20): { dy: number; recent: number[] } {
  const live = recent.filter((t) => now - t < windowMs);
  return { dy: live.length ? -live.length * step : 0, recent: [...live, now] };
}
