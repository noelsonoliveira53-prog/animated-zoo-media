import { describe, expect, it } from 'vitest';
import { hpColor, newTrail, resistPips, stepTrail, TRAIL_HOLD } from '../src/systems/hpBar';

describe('hp bar damage trail', () => {
  it('holds after a hit, then drains to the new health', () => {
    const s = newTrail(1);
    stepTrail(s, 0.6, 0.016);
    expect(s.trail).toBe(1);
    stepTrail(s, 0.6, TRAIL_HOLD / 2);
    expect(s.trail).toBe(1);
    for (let i = 0; i < 200; i++) stepTrail(s, 0.6, 0.016);
    expect(s.trail).toBeCloseTo(0.6);
  });
  it('never drops below the fill', () => {
    const s = newTrail(0.5);
    stepTrail(s, 0.2, 0.01);
    for (let i = 0; i < 100; i++) { stepTrail(s, 0.2, 0.5); expect(s.trail).toBeGreaterThanOrEqual(0.2); }
  });
  it('jumps up with healing', () => {
    const s = newTrail(0.3);
    stepTrail(s, 0.8, 0.016);
    expect(s.trail).toBe(0.8);
  });
  it('a new hit restarts the hold', () => {
    const s = newTrail(1);
    stepTrail(s, 0.9, 0.016);
    stepTrail(s, 0.9, TRAIL_HOLD + 0.1);
    stepTrail(s, 0.9, 0.05);
    const before = s.trail;
    stepTrail(s, 0.7, 0.016);
    stepTrail(s, 0.7, 0.1);
    expect(s.trail).toBe(before);
  });
});

describe('hp bar color and pips', () => {
  it('goes green → amber → red', () => {
    expect(hpColor(0.9)).toBe(0x7be35a);
    expect(hpColor(0.5)).toBe(0xf2c94c);
    expect(hpColor(0.1)).toBe(0xff5d4a);
  });
  it('lists only the resistances an enemy has', () => {
    expect(resistPips(0, 0)).toEqual([]);
    expect(resistPips(0.1, 0.2)).toEqual([]);
    expect(resistPips(0.6, 0)).toEqual(['armor']);
    expect(resistPips(0.3, 0.5)).toEqual(['armor', 'mr']);
  });
});
