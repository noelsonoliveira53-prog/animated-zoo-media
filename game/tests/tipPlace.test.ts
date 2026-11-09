import { describe, expect, it } from 'vitest';
import { tipPosition } from '../src/ui/tipPlace';

describe('tooltip placement', () => {
  it('centres the tip under the control', () => {
    expect(tipPosition({ x: 100, y: 20, w: 80, h: 40 }, 120, 30, 1280, 720)).toEqual({ x: 80, y: 68 });
  });
  it('flips above when there is no room below', () => {
    expect(tipPosition({ x: 600, y: 660, w: 60, h: 50 }, 100, 30, 1280, 720).y).toBe(622);
  });
  it('stays inside the screen sideways', () => {
    expect(tipPosition({ x: 1250, y: 20, w: 30, h: 30 }, 200, 30, 1280, 720).x).toBe(1280 - 6 - 200);
    expect(tipPosition({ x: 0, y: 20, w: 30, h: 30 }, 200, 30, 1280, 720).x).toBe(6);
  });
});
