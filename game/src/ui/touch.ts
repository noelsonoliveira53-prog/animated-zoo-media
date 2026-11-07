import Phaser from 'phaser';
import { paddedHit, phoneFontSize, TOUCH_MIN } from './hitpad';

export { TOUCH_MIN, TOUCH_MAX_PAD, paddedHit } from './hitpad';

let cached: boolean | null = null;
/** True on phones/tablets (coarse pointer). Safe when matchMedia is missing. */
export function isTouch(): boolean {
  if (cached !== null) return cached;
  try {
    cached = typeof window !== 'undefined' && !!window.matchMedia?.('(pointer: coarse)').matches;
  } catch {
    cached = false;
  }
  return cached;
}

type Sized = Phaser.GameObjects.GameObject & { width: number; height: number };

/** On touch devices, enlarge an interactive object's rectangular hit area. Call after setInteractive(). */
export function padHit<T extends Sized>(obj: T, min = TOUCH_MIN, force = false): T {
  if ((!force && !isTouch()) || !obj.input) return obj;
  const r = paddedHit(obj.width, obj.height, min);
  obj.input.hitArea = new Phaser.Geom.Rectangle(r.x, r.y, r.w, r.h);
  obj.input.hitAreaCallback = Phaser.Geom.Rectangle.Contains;
  return obj;
}

/** Font size for small in-play labels: bumped on phones so they stay readable (see phoneFontSize). */
export function pf(size: number): number {
  return phoneFontSize(size, isTouch());
}

/** Shrink a text object (never grow it) so it fits within maxW game px. */
export function fitWidth<T extends Phaser.GameObjects.Text>(t: T, maxW: number): T {
  t.setScale(Math.min(1, maxW / Math.max(1, t.width)));
  return t;
}
