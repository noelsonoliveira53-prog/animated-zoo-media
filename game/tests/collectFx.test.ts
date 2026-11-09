import { describe, expect, it } from 'vitest';
import { flightCount } from '../src/systems/collectFx';

describe('flightCount', () => {
  it('grows with the haul and caps at 6', () => {
    expect(flightCount(0)).toBe(0);
    expect(flightCount(5)).toBe(2);
    expect(flightCount(250)).toBe(4);
    expect(flightCount(99999)).toBe(6);
  });
  it('keeps a big Collect all light (about 24 icons in total at most)', () => {
    expect(flightCount(5000, 12) * 12).toBeLessThanOrEqual(24);
    expect(flightCount(5000, 40)).toBe(1);
  });
});
