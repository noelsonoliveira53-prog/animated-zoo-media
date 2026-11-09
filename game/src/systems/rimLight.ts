/**
 * Rim light for dark sprites: a near-black body hides its own ink outline, so the silhouette turns into a blob
 * on dark maps. This lights the opaque pixels whose neighbour toward the upper-left light is empty, the same
 * light direction as every hand-drawn highlight. Pure: works on an RGBA byte array.
 */

/** Indices (pixel numbers) of opaque pixels whose neighbour at (-d, -d) is transparent or off the edge. */
export function rimPixels(rgba: Uint8ClampedArray | Uint8Array, w: number, h: number, d = 2, solid = 200): number[] {
  const out: number[] = [];
  for (let y = 0; y < h; y++)
    for (let x = 0; x < w; x++) {
      const i = y * w + x;
      if (rgba[i * 4 + 3] < solid) continue;
      const nx = x - d;
      const ny = y - d;
      const empty = nx < 0 || ny < 0 || rgba[(ny * w + nx) * 4 + 3] < 40;
      if (empty) out.push(i);
    }
  return out;
}

/** Blend the rim pixels toward `color` (0xRRGGBB) by `amount`, in place. Returns how many pixels were lit. */
export function applyRim(rgba: Uint8ClampedArray | Uint8Array, w: number, h: number, color: number, amount = 0.55, d = 2): number {
  const r = (color >> 16) & 255;
  const g = (color >> 8) & 255;
  const b = color & 255;
  const px = rimPixels(rgba, w, h, d);
  for (const i of px) {
    rgba[i * 4] += (r - rgba[i * 4]) * amount;
    rgba[i * 4 + 1] += (g - rgba[i * 4 + 1]) * amount;
    rgba[i * 4 + 2] += (b - rgba[i * 4 + 2]) * amount;
  }
  return px.length;
}
