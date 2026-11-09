import { describe, expect, it } from 'vitest';
import { applyRim, rimPixels } from '../src/systems/rimLight';

function square(w: number, h: number, x0: number, y0: number, size: number): Uint8ClampedArray {
  const a = new Uint8ClampedArray(w * h * 4);
  for (let y = y0; y < y0 + size; y++) for (let x = x0; x < x0 + size; x++) { const i = (y * w + x) * 4; a[i] = 20; a[i + 1] = 20; a[i + 2] = 20; a[i + 3] = 255; }
  return a;
}

describe('rim light', () => {
  it('lights only the upper-left edge of a shape', () => {
    const a = square(10, 10, 3, 3, 4);
    const px = rimPixels(a, 10, 10, 1);
    // top row and left column of the 4x4 square: 4 + 4 - 1 corner = 7
    expect(px.length).toBe(7);
    expect(px).toContain(3 * 10 + 3);
    expect(px).not.toContain(6 * 10 + 6);
  });
  it('treats the canvas edge as empty and skips see-through pixels', () => {
    const a = square(4, 4, 0, 0, 4);
    expect(rimPixels(a, 4, 4, 1).length).toBe(7);
    a[3] = 100; // first pixel half transparent: not solid, so not lit
    expect(rimPixels(a, 4, 4, 1)).not.toContain(0);
  });
  it('blends the rim toward the light colour', () => {
    const a = square(10, 10, 3, 3, 4);
    const n = applyRim(a, 10, 10, 0xffffff, 0.5, 1);
    expect(n).toBe(7);
    const i = (3 * 10 + 3) * 4;
    expect(a[i]).toBeGreaterThan(130);
    const j = (6 * 10 + 6) * 4;
    expect(a[j]).toBe(20);
  });
});
