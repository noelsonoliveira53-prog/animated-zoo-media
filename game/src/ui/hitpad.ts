// Pure tap-target math (no Phaser import, so it is unit-testable).

/** Smallest comfortable tap target, in game pixels. At 1280×720 squeezed onto a ~740px-wide phone
 * this is about 42 CSS px, close to the usual 44pt guideline. */
export const TOUCH_MIN = 72;
/** Never grow a hit area by more than this on each side, so neighbouring buttons don't steal taps. */
export const TOUCH_MAX_PAD = 12;

export interface HitRect { x: number; y: number; w: number; h: number }

/** Hit rectangle (local, top-left origin) that grows a w×h object toward `min`, capped at `maxPad` per side. */
export function paddedHit(w: number, h: number, min = TOUCH_MIN, maxPad = TOUCH_MAX_PAD): HitRect {
  const px = Math.min(maxPad, Math.max(0, (min - w) / 2));
  const py = Math.min(maxPad, Math.max(0, (min - h) / 2));
  return { x: -px, y: -py, w: w + px * 2, h: h + py * 2 };
}

