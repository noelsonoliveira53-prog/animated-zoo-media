import { describe, expect, it } from 'vitest';
import { slowMoScale, SLOWMO_MIN, SLOWMO_MS } from '../src/systems/slowMo';

describe('slowMoScale', () => {
  it('starts slow and returns to full speed', () => {
    expect(slowMoScale(0)).toBeCloseTo(SLOWMO_MIN);
    expect(slowMoScale(SLOWMO_MS)).toBe(1);
    expect(slowMoScale(-5)).toBe(1);
  });
  it('rises steadily', () => {
    let prev = 0;
    for (let ms = 0; ms < SLOWMO_MS; ms += 50) {
      const v = slowMoScale(ms);
      expect(v).toBeGreaterThanOrEqual(prev);
      expect(v).toBeLessThan(1);
      prev = v;
    }
  });
  it('spends most of the beat below half speed', () => {
    expect(slowMoScale(SLOWMO_MS * 0.5)).toBeLessThan(0.5);
  });
});
