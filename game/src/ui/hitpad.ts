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


/** Smallest font (game px) we want for in-play labels on a phone, where the game renders at ~0.5×. */
export const PHONE_MIN_FONT = 18;

/** Smallest label size anywhere (game px): small captions and chart numbers never go below this. */
export const MIN_READABLE_FONT = 13;

/** Font size for a small label: never below MIN_READABLE_FONT; on phones, +4 px but no bigger than PHONE_MIN_FONT (or the original). */
export function phoneFontSize(size: number, touch: boolean): number {
  const s = Math.max(size, MIN_READABLE_FONT);
  if (!touch) return s;
  return Math.min(s + 4, Math.max(s, PHONE_MIN_FONT));
}

/** WCAG 2.5.5: a target should be at least this many CSS px across, on any device. */
export const TARGET_CSS_MIN = 44;

/**
 * Smallest hit size in game px for a control, given how many game px one CSS px covers
 * (Phaser's scale.displayScale.x: 1 at 1280 wide, about 1.7 on a 740-wide phone).
 * Touch devices never go below TOUCH_MIN.
 */
export function minHitGamePx(gamePxPerCss: number, touch: boolean): number {
  const css = Math.ceil(TARGET_CSS_MIN * Math.max(0.25, gamePxPerCss));
  return touch ? Math.max(TOUCH_MIN, css) : css;
}

/** Hard cap on hit growth per side when there is room around a control. */
export const ROOMY_MAX_PAD = 30;

/**
 * How far a control's hit area may grow on each axis without reaching into a neighbour:
 * half the gap to the nearest other control that sits alongside it on that axis, capped at ROOMY_MAX_PAD.
 * Rects are { x, y, w, h } with a top-left origin, all in the same space.
 */
export function roomToGrow(r: HitRect, others: HitRect[]): { x: number; y: number } {
  let x = ROOMY_MAX_PAD;
  let y = ROOMY_MAX_PAD;
  for (const o of others) {
    if (o === r) continue;
    const overlapY = o.y < r.y + r.h && o.y + o.h > r.y;
    const overlapX = o.x < r.x + r.w && o.x + o.w > r.x;
    if (overlapY && overlapX) continue; // nested or stacked: not a neighbour to keep clear of
    if (overlapY) {
      const gap = o.x >= r.x + r.w ? o.x - (r.x + r.w) : r.x - (o.x + o.w);
      x = Math.min(x, Math.max(0, gap / 2));
    }
    if (overlapX) {
      const gap = o.y >= r.y + r.h ? o.y - (r.y + r.h) : r.y - (o.y + o.h);
      y = Math.min(y, Math.max(0, gap / 2));
    }
  }
  return { x, y };
}

/** paddedHit with separate per-axis caps. */
export function paddedHitXY(w: number, h: number, min: number, maxX: number, maxY: number): HitRect {
  const px = Math.min(maxX, Math.max(0, (min - w) / 2));
  const py = Math.min(maxY, Math.max(0, (min - h) / 2));
  return { x: -px, y: -py, w: w + px * 2, h: h + py * 2 };
}
