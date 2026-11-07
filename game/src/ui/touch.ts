import Phaser from 'phaser';
import { paddedHit, TOUCH_MIN } from './hitpad';

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
