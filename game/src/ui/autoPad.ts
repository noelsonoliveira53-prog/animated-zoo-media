import Phaser from 'phaser';
import { HitRect, minHitGamePx, paddedHitXY, roomToGrow } from './hitpad';
import { isTouch } from './touch';

type Padded = Phaser.GameObjects.GameObject & {
  width?: number;
  height?: number;
  list?: Phaser.GameObjects.GameObject[];
  __baseHit?: { w: number; h: number };
};

const SCAN_MS = 400;

/**
 * Every clickable control (hand cursor, plain rectangular hit area) gets its hit area grown toward
 * 44 CSS px on any device, so small pills and icons are easy to hit with a mouse in a small window
 * as well as with a finger. Growth is capped per side (TOUCH_MAX_PAD) so neighbours keep their taps.
 * Registered once as a scene plugin; it rescans a few times a second for new controls and resizes.
 */
export class AutoPadPlugin extends Phaser.Plugins.ScenePlugin {
  private last = 0;

  boot(): void {
    const ev = this.systems!.events;
    ev.on(Phaser.Scenes.Events.POST_UPDATE, this.tick, this);
    ev.once(Phaser.Scenes.Events.DESTROY, () => ev.off(Phaser.Scenes.Events.POST_UPDATE, this.tick, this));
  }

  private tick(time: number): void {
    if (time - this.last < SCAN_MS) return;
    this.last = time;
    const min = minHitGamePx(this.game!.scale.displayScale.x, isTouch());
    const found: { o: Padded; r: HitRect }[] = [];
    const visit = (list: Phaser.GameObjects.GameObject[], vis: boolean): void => {
      for (const o of list as Padded[]) {
        const v = vis && (o as unknown as { visible?: boolean }).visible !== false;
        if (v && o.input?.enabled && o.input.cursor === 'pointer') {
          const r = drawnRect(o);
          if (r) found.push({ o, r });
        }
        if (o.list) visit(o.list, v);
      }
    };
    visit(this.scene!.children.list, true);
    const rects = found.map((f) => f.r);
    for (const f of found) {
      const room = roomToGrow(f.r, rects);
      const sc = f.r.w / Math.max(1, f.o.width ?? 1); // world px per local px
      pad(f.o, min / sc, room.x / sc, room.y / sc);
    }
  }
}

/** A control's drawn rectangle in world space, from its own size and world transform. */
function drawnRect(o: Padded): HitRect | null {
  const t = o as unknown as { displayOriginX?: number; displayOriginY?: number; getWorldTransformMatrix?: () => Phaser.GameObjects.Components.TransformMatrix };
  const w = o.width ?? 0;
  const h = o.height ?? 0;
  if (w <= 0 || h <= 0 || !t.getWorldTransformMatrix) return null;
  const m = t.getWorldTransformMatrix();
  const a = m.transformPoint(-(t.displayOriginX ?? 0), -(t.displayOriginY ?? 0));
  const b = m.transformPoint(w - (t.displayOriginX ?? 0), h - (t.displayOriginY ?? 0));
  return { x: Math.min(a.x, b.x), y: Math.min(a.y, b.y), w: Math.abs(b.x - a.x), h: Math.abs(b.y - a.y) };
}

/** Grow one control's rectangular hit area toward `min` local px, within the room it has (idempotent). */
function pad(o: Padded, min: number, maxX: number, maxY: number): void {
  const io = o.input!;
  const hit = io.hitArea as Phaser.Geom.Rectangle | undefined;
  if (!(hit instanceof Phaser.Geom.Rectangle)) return;
  const w = o.width ?? 0;
  const h = o.height ?? 0;
  if (w <= 0 || h <= 0) return;
  const base = o.__baseHit;
  const untouched = hit.x === 0 && hit.y === 0 && hit.width === w && hit.height === h;
  if (!untouched && !(base && base.w === w && base.h === h)) return; // a custom shape someone set on purpose
  const r = paddedHitXY(w, h, min, maxX, maxY);
  if (hit.x === r.x && hit.y === r.y && hit.width === r.w && hit.height === r.h) return;
  hit.setTo(r.x, r.y, r.w, r.h);
  io.hitAreaCallback = Phaser.Geom.Rectangle.Contains;
  o.__baseHit = { w, h };
}
