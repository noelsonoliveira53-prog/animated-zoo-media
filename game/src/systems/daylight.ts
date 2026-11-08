/** Cosmetic village light by local hour: golden late afternoon, a blue night with lit windows, a pink dawn. */
export interface DayLight {
  color: number;
  alpha: number;
  /** windows glow (dusk and night) */
  windows: boolean;
  name: 'day' | 'golden' | 'night' | 'dawn';
}

export function dayLight(hour: number): DayLight {
  const h = ((hour % 24) + 24) % 24;
  if (h >= 8 && h < 17) return { color: 0x000000, alpha: 0, windows: false, name: 'day' };
  if (h >= 17 && h < 19) return { color: 0xff8a30, alpha: 0.16, windows: h >= 18, name: 'golden' };
  if (h >= 6 && h < 8) return { color: 0xff9ac0, alpha: 0.1, windows: false, name: 'dawn' };
  return { color: 0x101c48, alpha: 0.42, windows: true, name: 'night' };
}
