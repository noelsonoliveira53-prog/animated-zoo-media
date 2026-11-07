import { describe, expect, it } from 'vitest';
import { paddedHit, TOUCH_MAX_PAD, TOUCH_MIN } from '../src/ui/hitpad';

describe('touch hit padding', () => {
  it('grows small targets toward the minimum, capped per side', () => {
    const r = paddedHit(180, 44);
    expect(r.w).toBe(180);
    expect(r.h).toBe(44 + TOUCH_MAX_PAD * 2);
    expect(r.y).toBe(-TOUCH_MAX_PAD);
  });
  it('reaches the minimum when the gap is small', () => {
    const r = paddedHit(64, 60);
    expect(r.w).toBe(TOUCH_MIN);
    expect(r.h).toBe(TOUCH_MIN);
    expect(r.x).toBe(-4);
  });
  it('leaves big targets alone', () => {
    expect(paddedHit(200, 100)).toEqual({ x: -0, y: -0, w: 200, h: 100 });
  });
});

import { phoneFontSize, PHONE_MIN_FONT } from '../src/ui/hitpad';

describe('phone font sizes', () => {
  it('leaves desktop sizes alone', () => {
    expect(phoneFontSize(12, false)).toBe(12);
  });
  it('bumps small labels on phones, capped at the minimum', () => {
    expect(phoneFontSize(12, true)).toBe(16);
    expect(phoneFontSize(14, true)).toBe(PHONE_MIN_FONT);
    expect(phoneFontSize(16, true)).toBe(PHONE_MIN_FONT);
    expect(phoneFontSize(24, true)).toBe(24);
  });
});
