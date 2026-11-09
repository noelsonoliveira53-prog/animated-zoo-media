/** How long a boss kill slows the battle down, and how slow it starts. */
export const SLOWMO_MS = 1100;
export const SLOWMO_MIN = 0.25;

/**
 * The battle's time scale `elapsed` ms into a slow-motion beat lasting `duration`: starts at `min` and eases back
 * to full speed (quadratic, so most of the beat feels slow and the return is smooth). 1 outside the beat.
 */
export function slowMoScale(elapsed: number, duration = SLOWMO_MS, min = SLOWMO_MIN): number {
  if (elapsed < 0 || elapsed >= duration) return 1;
  const t = elapsed / duration;
  return min + (1 - min) * t * t;
}
