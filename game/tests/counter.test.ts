import { describe, it, expect } from 'vitest';
import { stepCounter, waveProgress } from '../src/ui/counter';

describe('HUD counters', () => {
  it('eases toward the target and lands exactly', () => {
    let v = 0;
    for (let i = 0; i < 120; i++) v = stepCounter(v, 500, 1 / 60);
    expect(v).toBe(500);
  });
  it('moves partway in one frame, both directions', () => {
    const up = stepCounter(100, 200, 1 / 60);
    expect(up).toBeGreaterThan(100);
    expect(up).toBeLessThan(200);
    const down = stepCounter(200, 100, 1 / 60);
    expect(down).toBeLessThan(200);
    expect(down).toBeGreaterThan(100);
  });
  it('wave progress clamps and handles endless', () => {
    expect(waveProgress(-1, 10)).toBe(0);
    expect(waveProgress(4, 10)).toBe(0.5);
    expect(waveProgress(20, 10)).toBe(1);
    expect(waveProgress(3, Infinity)).toBe(0);
  });
});
