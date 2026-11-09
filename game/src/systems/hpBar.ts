/**
 * Enemy health bar helpers (visual only). The bar shows a pale "damage trail" behind the fill: when a hit
 * lands the trail holds for a moment where the health was, then drains down to it, so you can see how big
 * each hit was. Healing moves the trail up with the fill at once.
 */
export interface TrailState { trail: number; hold: number; last: number }

export const TRAIL_HOLD = 0.35; // seconds the trail waits after a hit
export const TRAIL_DRAIN = 0.9; // fraction of the bar per second

export function newTrail(frac: number): TrailState {
  return { trail: frac, hold: 0, last: frac };
}

/** Advance the trail by `dt` seconds toward the current health fraction `frac`. Mutates and returns `s`. */
export function stepTrail(s: TrailState, frac: number, dt: number): TrailState {
  if (frac < s.last - 1e-6) s.hold = TRAIL_HOLD; // a fresh hit restarts the wait
  s.last = frac;
  if (frac >= s.trail) {
    s.trail = frac;
    s.hold = 0;
    return s;
  }
  if (s.hold > 0) {
    s.hold = Math.max(0, s.hold - dt);
    return s;
  }
  // drain a little faster when the gap is large so big hits don't linger
  const gap = s.trail - frac;
  s.trail = Math.max(frac, s.trail - dt * (TRAIL_DRAIN + gap * 2));
  return s;
}

/** Fill color: green when healthy, amber in the middle, red when low. */
export function hpColor(frac: number): number {
  if (frac > 0.6) return 0x7be35a;
  if (frac > 0.3) return 0xf2c94c;
  return 0xff5d4a;
}

/** Resistance from which a marker shows: most foes have a little of both, so only the ones that matter get one. */
export const RESIST_PIP_MIN = 0.3;

/** Little markers next to the bar: armor (grey shield) and magic resist (violet gem) for notable resistances. */
export function resistPips(armor: number, magicResist: number): ('armor' | 'mr')[] {
  const out: ('armor' | 'mr')[] = [];
  if (armor >= RESIST_PIP_MIN) out.push('armor');
  if (magicResist >= RESIST_PIP_MIN) out.push('mr');
  return out;
}
