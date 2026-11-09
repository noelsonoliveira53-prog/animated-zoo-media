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

import { minHitGamePx, TARGET_CSS_MIN } from '../src/ui/hitpad';

describe('minimum hit size on every device', () => {
  it('is 44 game px at full size on desktop', () => {
    expect(minHitGamePx(1, false)).toBe(TARGET_CSS_MIN);
  });
  it('grows when the canvas is shown smaller', () => {
    expect(minHitGamePx(2, false)).toBe(88);
  });
  it('never drops below the touch minimum on touch devices', () => {
    expect(minHitGamePx(1, true)).toBe(TOUCH_MIN);
    expect(minHitGamePx(2, true)).toBe(88);
  });
  it('shrinks on a big screen but stays sane', () => {
    expect(minHitGamePx(0.5, false)).toBe(22);
    expect(minHitGamePx(0, false)).toBe(11);
  });
});

import { paddedHitXY, roomToGrow, ROOMY_MAX_PAD } from '../src/ui/hitpad';

describe('room to grow between neighbours', () => {
  const a = { x: 0, y: 0, w: 100, h: 30 };
  it('a lone control may grow to the roomy cap', () => {
    expect(roomToGrow(a, [a])).toEqual({ x: ROOMY_MAX_PAD, y: ROOMY_MAX_PAD });
  });
  it('a neighbour beside it limits sideways growth to half the gap', () => {
    expect(roomToGrow(a, [a, { x: 120, y: 5, w: 50, h: 20 }]).x).toBe(10);
  });
  it('a neighbour below it limits vertical growth', () => {
    expect(roomToGrow(a, [{ x: 10, y: 50, w: 50, h: 20 }]).y).toBe(10);
  });
  it('diagonal controls do not limit growth', () => {
    expect(roomToGrow(a, [{ x: 200, y: 200, w: 20, h: 20 }])).toEqual({ x: ROOMY_MAX_PAD, y: ROOMY_MAX_PAD });
  });
  it('per-axis padding respects each cap', () => {
    expect(paddedHitXY(100, 30, 80, 5, 30)).toEqual({ x: -0, y: -25, w: 100, h: 80 });
  });
});
