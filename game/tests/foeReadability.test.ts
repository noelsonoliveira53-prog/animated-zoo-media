import { describe, expect, it } from 'vitest';
import { brightness, foeShadowAlpha, stackLabel } from '../src/systems/foeReadability';

describe('foe readability', () => {
  it('measures brightness', () => {
    expect(brightness(0x000000)).toBe(0);
    expect(brightness(0xffffff)).toBeCloseTo(1, 5);
    expect(brightness(0xc8b48a)).toBeGreaterThan(0.6);
  });
  it('deepens shadows on pale roads only', () => {
    expect(foeShadowAlpha(0x8a6a3a, false)).toBe(0.2);
    expect(foeShadowAlpha(0xd8d0c0, false)).toBeCloseTo(0.34, 5);
    expect(foeShadowAlpha(0xd8d0c0, true)).toBeCloseTo(0.36, 5);
  });
  it('stacks labels that pop close together', () => {
    let r: number[] = [];
    const a = stackLabel(r, 0); r = a.recent;
    const b = stackLabel(r, 300); r = b.recent;
    const c = stackLabel(r, 600); r = c.recent;
    expect([a.dy, b.dy, c.dy]).toEqual([0, -20, -40]);
    expect(stackLabel(r, 5000).dy).toBe(0);
  });
});
