import { describe, expect, it } from 'vitest';
import { fbm, groundSteps, litValue, mixColor, stepColors, stepOf, valueNoise } from '../src/systems/groundNoise';

describe('ground noise', () => {
  it('value noise is smooth, seeded and in 0..1', () => {
    for (let i = 0; i < 200; i++) {
      const v = valueNoise(i * 0.37, i * 0.21, 5);
      expect(v).toBeGreaterThanOrEqual(0);
      expect(v).toBeLessThanOrEqual(1);
    }
    expect(valueNoise(3.3, 4.4, 1)).toBe(valueNoise(3.3, 4.4, 1));
    expect(valueNoise(3.3, 4.4, 1)).not.toBe(valueNoise(3.3, 4.4, 2));
    expect(Math.abs(valueNoise(2.5, 2.5, 9) - valueNoise(2.501, 2.5, 9))).toBeLessThan(0.01);
  });
  it('fbm stays in 0..1', () => {
    for (let i = 0; i < 100; i++) {
      const v = fbm(i * 13, i * 7, 3, 200);
      expect(v).toBeGreaterThanOrEqual(0);
      expect(v).toBeLessThanOrEqual(1);
    }
  });
  it('ground rising toward the upper-left light is brighter', () => {
    expect(litValue(0.5, 0.6, 0.4)).toBeGreaterThan(litValue(0.5, 0.4, 0.6));
    expect(litValue(0.5, 0.6, 0.4, 0)).toBe(litValue(0.5, 0.4, 0.6, 0));
  });
  it('steps clamp to the range', () => {
    expect(stepOf(-1, 4)).toBe(0);
    expect(stepOf(0.3, 4)).toBe(1);
    expect(stepOf(5, 4)).toBe(3);
  });
  it('bakes a deterministic field that uses several steps', () => {
    const a = groundSteps(160, 90, 42);
    const b = groundSteps(160, 90, 42);
    expect(a).toEqual(b);
    expect(a.length).toBe(160 * 90);
    const used = new Set(groundSteps(640, 360, 42, { scale: 120 }));
    expect(used.size).toBeGreaterThanOrEqual(3);
    for (const v of used) expect(v).toBeLessThan(4);
  });
  it('step colours stay close to the base and run dark to light', () => {
    const cols = stepColors(0x6fbf4a, 0x3f8a34, 0xa8e070, 4);
    expect(cols).toHaveLength(4);
    const lum = (c: number) => ((c >> 16) & 255) + ((c >> 8) & 255) + (c & 255);
    for (let i = 1; i < 4; i++) expect(lum(cols[i])).toBeGreaterThan(lum(cols[i - 1]));
    for (const c of cols) expect(Math.abs(lum(c) - lum(0x6fbf4a))).toBeLessThan(110);
    expect(mixColor(0x000000, 0xffffff, 0.5)).toBe(0x808080);
  });
});
