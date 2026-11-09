/**
 * Rolling HUD counters: the shown number eases toward the real one so coin and
 * life changes tick up and down instead of jumping.
 */
export function stepCounter(shown: number, target: number, dt: number, rate = 10): number {
  const diff = target - shown;
  if (Math.abs(diff) < 0.5) return target;
  // ease toward the target, but always move at least a few units per second so small changes still finish quickly
  const step = diff * Math.min(1, dt * rate);
  const minStep = Math.sign(diff) * Math.min(Math.abs(diff), Math.max(1, 30 * dt));
  return shown + (Math.abs(step) > Math.abs(minStep) ? step : minStep);
}

/** Fraction of the level's waves that have started (0..1); endless levels have no bar. */
export function waveProgress(waveIndex: number, total: number): number {
  if (!isFinite(total) || total <= 0) return 0;
  return Math.max(0, Math.min(1, (waveIndex + 1) / total));
}
