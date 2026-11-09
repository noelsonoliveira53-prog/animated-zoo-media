import Phaser from 'phaser';
import { C, GAME_H, GAME_W, textStyle } from './theme';
import { pf } from './touch';
import { tipPosition } from './tipPlace';

type Tip = string | (() => string);
const TIP_DEPTH = 5100;

/** World-space rect of a control from its size and world transform (falls back to getBounds). */
function rectOf(o: Phaser.GameObjects.GameObject): { x: number; y: number; w: number; h: number } | null {
  const t = o as unknown as {
    width?: number; height?: number; displayOriginX?: number; displayOriginY?: number;
    getWorldTransformMatrix?: () => Phaser.GameObjects.Components.TransformMatrix;
    getBounds?: () => Phaser.Geom.Rectangle;
  };
  if ((t.width ?? 0) > 0 && (t.height ?? 0) > 0 && t.getWorldTransformMatrix) {
    const m = t.getWorldTransformMatrix();
    const a = m.transformPoint(-(t.displayOriginX ?? 0), -(t.displayOriginY ?? 0));
    const b = m.transformPoint(t.width! - (t.displayOriginX ?? 0), t.height! - (t.displayOriginY ?? 0));
    return { x: Math.min(a.x, b.x), y: Math.min(a.y, b.y), w: Math.abs(b.x - a.x), h: Math.abs(b.y - a.y) };
  }
  const b = t.getBounds?.();
  return b ? { x: b.x, y: b.y, w: b.width, h: b.height } : null;
}

/** Show the tooltip for `obj` (if it has one), replacing any other in its scene. */
export function showTip(obj: Phaser.GameObjects.GameObject): void {
  const tip = obj.getData?.('tip') as Tip | undefined;
  const scene = obj.scene;
  if (!tip || !scene) return;
  hideTip(scene);
  const r = rectOf(obj);
  if (!r) return;
  const text = scene.add.text(0, 0, typeof tip === 'function' ? tip() : tip, { ...textStyle(pf(15), '#fff4d6', false), wordWrap: { width: 260 } });
  const pad = 8;
  const tw = text.width + pad * 2;
  const th = text.height + pad * 2;
  const pos = tipPosition(r, tw, th, GAME_W, GAME_H);
  const bg = scene.add.graphics();
  bg.fillStyle(C.ink, 0.94);
  bg.fillRoundedRect(0, 0, tw, th, 8);
  bg.lineStyle(2, C.gold, 0.8);
  bg.strokeRoundedRect(0, 0, tw, th, 8);
  text.setPosition(pad, pad);
  const c = scene.add.container(pos.x, pos.y, [bg, text]).setDepth(TIP_DEPTH).setScrollFactor(0).setName('tooltip');
  c.setAlpha(0);
  scene.tweens.add({ targets: c, alpha: 1, duration: 120 });
}

export function hideTip(scene: Phaser.Scene): void {
  scene.children.getByName('tooltip')?.destroy();
}

/**
 * Give an icon-only control a tooltip: shown on mouse hover (after a short pause), on a long press on
 * touch screens (unless `touch: false`), and when the keyboard focus ring lands on it (see keyNav).
 */
export function attachTip<T extends Phaser.GameObjects.GameObject>(obj: T, tip: Tip, opts: { touch?: boolean } = {}): T {
  const touch = opts.touch ?? true; // false where the control already shows its own info on a touch press
  obj.setData('tip', tip);
  // real-time timers, so a tooltip still appears while the battle is paused
  let timer: ReturnType<typeof setTimeout> | null = null;
  const later = (ms: number, fn: () => void) => setTimeout(() => obj.active && obj.scene && fn(), ms);
  const cancel = () => {
    if (timer) clearTimeout(timer);
    timer = null;
  };
  obj.on('pointerover', (p: Phaser.Input.Pointer) => {
    if (p.wasTouch) return;
    cancel();
    timer = later(350, () => showTip(obj));
  });
  obj.on('pointerout', () => {
    cancel();
    hideTip(obj.scene);
  });
  obj.on('pointerdown', (p: Phaser.Input.Pointer) => {
    cancel();
    hideTip(obj.scene);
    if (p.wasTouch && touch) timer = later(450, () => showTip(obj));
  });
  obj.on('pointerup', () => {
    cancel();
    timer = later(1200, () => hideTip(obj.scene));
  });
  obj.once('destroy', cancel);
  return obj;
}
