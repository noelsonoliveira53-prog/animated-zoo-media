/**
 * Baked ground variation for battle maps: a soft noise height field lit from the upper left and
 * quantised into a few flat value steps, like cut paper (see docs/art/desire-lines.html).
 * Pure maths, no Phaser, so it is unit-testable.
 */

/** Seeded hash → 0..1 for an integer lattice point. */
function hash(ix: number, iy: number, seed: number): number {
  let h = (ix * 374761393 + iy * 668265263 + seed * 1442695041) | 0;
  h = Math.imul(h ^ (h >>> 13), 1274126177);
  h ^= h >>> 16;
  return (h >>> 0) / 4294967295;
}

/** Smooth value noise in 0..1. */
export function valueNoise(x: number, y: number, seed: number): number {
  const ix = Math.floor(x);
  const iy = Math.floor(y);
  const fx = x - ix;
  const fy = y - iy;
  const sx = fx * fx * (3 - 2 * fx);
  const sy = fy * fy * (3 - 2 * fy);
  const a = hash(ix, iy, seed);
  const b = hash(ix + 1, iy, seed);
  const c = hash(ix, iy + 1, seed);
  const d = hash(ix + 1, iy + 1, seed);
  return a + (b - a) * sx + (c - a) * sy + (a - b - c + d) * sx * sy;
}

/** Three octaves of value noise, 0..1. `scale` is the size of the largest features in px. */
export function fbm(x: number, y: number, seed: number, scale: number): number {
  const u = x / scale;
  const v = y / scale;
  return valueNoise(u, v, seed) * 0.6 + valueNoise(u * 2.1 + 17, v * 2.1, seed + 1) * 0.28 + valueNoise(u * 4.3, v * 4.3 + 31, seed + 2) * 0.12;
}

/** Light comes from the upper left: ground that rises toward the light (higher up-left than down-right) brightens. */
export function litValue(h: number, hUpLeft: number, hDownRight: number, relief = 1): number {
  return h * 0.75 + (hUpLeft - hDownRight) * 4 * relief + 0.125;
}

/** Index of the value step (0 = darkest) for a lit value. */
export function stepOf(v: number, steps: number): number {
  return Math.max(0, Math.min(steps - 1, Math.floor(v * steps)));
}

export interface GroundOpts {
  steps?: number;
  /** Largest feature size in px. */
  scale?: number;
  relief?: number;
  /** Sample spacing of the coarse grid, in px (each pixel interpolates between samples). */
  cell?: number;
}

/**
 * Step index for every pixel of a w×h ground, row-major. The height field is sampled on a coarse
 * grid and interpolated per pixel before quantising, so step edges are crisp but follow smooth contours.
 */
export function groundSteps(w: number, h: number, seed: number, opts: GroundOpts = {}): Uint8Array {
  const steps = opts.steps ?? 4;
  const scale = opts.scale ?? 260;
  const relief = opts.relief ?? 1;
  const cell = opts.cell ?? 8;
  const gw = Math.ceil(w / cell) + 2;
  const gh = Math.ceil(h / cell) + 2;
  const hf = new Float32Array(gw * gh);
  for (let j = 0; j < gh; j++) for (let i = 0; i < gw; i++) hf[j * gw + i] = fbm(i * cell, j * cell, seed, scale);
  const lit = new Float32Array(gw * gh);
  for (let j = 0; j < gh; j++)
    for (let i = 0; i < gw; i++) {
      const ul = hf[Math.max(0, j - 1) * gw + Math.max(0, i - 1)];
      const dr = hf[Math.min(gh - 1, j + 1) * gw + Math.min(gw - 1, i + 1)];
      lit[j * gw + i] = litValue(hf[j * gw + i], ul, dr, relief);
    }
  const out = new Uint8Array(w * h);
  for (let y = 0; y < h; y++) {
    const gy = y / cell;
    const j = Math.floor(gy);
    const fy = gy - j;
    for (let x = 0; x < w; x++) {
      const gx = x / cell;
      const i = Math.floor(gx);
      const fx = gx - i;
      const k = j * gw + i;
      const top = lit[k] + (lit[k + 1] - lit[k]) * fx;
      const bot = lit[k + gw] + (lit[k + gw + 1] - lit[k + gw]) * fx;
      out[y * w + x] = stepOf(top + (bot - top) * fy, steps);
    }
  }
  return out;
}

/** Blend two 0xRRGGBB colours. */
export function mixColor(a: number, b: number, t: number): number {
  const r = ((a >> 16) & 255) + ((((b >> 16) & 255) - ((a >> 16) & 255)) * t);
  const g = ((a >> 8) & 255) + ((((b >> 8) & 255) - ((a >> 8) & 255)) * t);
  const bl = (a & 255) + (((b & 255) - (a & 255)) * t);
  return (Math.round(r) << 16) | (Math.round(g) << 8) | Math.round(bl);
}

/**
 * Low-contrast step colours around a base ground colour: the darker steps lean toward `dark`,
 * the lighter toward `light`, never far from the base so gameplay stays readable.
 */
export function stepColors(base: number, dark: number, light: number, steps = 4, strength = 1): number[] {
  const out: number[] = [];
  for (let i = 0; i < steps; i++) {
    const t = steps === 1 ? 0 : (i / (steps - 1)) * 2 - 1; // -1..1
    out.push(t < 0 ? mixColor(base, dark, -t * 0.22 * strength) : mixColor(base, light, t * 0.3 * strength));
  }
  return out;
}
