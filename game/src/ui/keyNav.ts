import Phaser from 'phaser';
import { C, GAME_H, GAME_W } from './theme';
import { FocusDir, isBackLabel, nextFocus } from '../systems/focusNav';

type GO = Phaser.GameObjects.GameObject & {
  visible?: boolean;
  alpha?: number;
  enabled?: boolean;
  scrollFactorX?: number;
  scrollFactorY?: number;
  cameraFilter?: number;
  list?: Phaser.GameObjects.GameObject[];
  getBounds?: () => Phaser.Geom.Rectangle;
};

interface Target {
  obj: GO;
  /** Screen-space rectangle (game px). */
  r: Phaser.Geom.Rectangle;
}

const RING_DEPTH = 5000;

/**
 * Keyboard play for every scene: Tab / Shift+Tab and the arrow keys move a gold focus ring
 * between clickable controls (anything with a hand cursor that the pointer could reach),
 * Enter presses the focused control (Space too, in scenes that don't use Space themselves),
 * and Esc presses a Back / Close control in scenes without an Esc key of their own.
 * Registered once as a scene plugin, so every scene gets it.
 */
export class KeyNavPlugin extends Phaser.Plugins.ScenePlugin {
  private focused: GO | null = null;
  private ring: Phaser.GameObjects.Graphics | null = null;
  private shown = false;

  boot(): void {
    const ev = this.systems!.events;
    ev.on(Phaser.Scenes.Events.START, this.onStart, this);
    ev.on(Phaser.Scenes.Events.SHUTDOWN, this.onStop, this);
    ev.once(Phaser.Scenes.Events.DESTROY, () => {
      ev.off(Phaser.Scenes.Events.START, this.onStart, this);
      ev.off(Phaser.Scenes.Events.SHUTDOWN, this.onStop, this);
    });
  }

  private onStart(): void {
    const s = this.scene!;
    this.focused = null;
    this.shown = false;
    this.ring = null;
    s.input.keyboard?.on('keydown', this.onKey, this);
    s.input.keyboard?.addCapture('TAB');
    s.input.on('pointerdown', this.hide, this);
    this.systems!.events.on(Phaser.Scenes.Events.POST_UPDATE, this.drawRing, this);
  }

  private onStop(): void {
    const s = this.scene!;
    s.input.keyboard?.off('keydown', this.onKey, this);
    s.input.off('pointerdown', this.hide, this);
    this.systems!.events.off(Phaser.Scenes.Events.POST_UPDATE, this.drawRing, this);
    this.focused = null;
    this.ring = null;
  }

  private hide(): void {
    this.shown = false;
    this.ring?.clear();
  }

  /** Only the top-most running scene that has controls responds, so overlays take the keys. */
  private isTopScene(): boolean {
    for (const sc of this.game!.scene.getScenes(true, true)) {
      const nav = (sc as unknown as { keyNav?: KeyNavPlugin }).keyNav;
      if (!sc.input?.enabled || !nav) continue;
      if (nav.targets().length > 0) return sc === this.scene;
    }
    return false;
  }

  private onKey(e: KeyboardEvent): void {
    const dir: FocusDir | null =
      e.key === 'Tab' ? (e.shiftKey ? 'prev' : 'next')
      : e.key === 'ArrowUp' ? 'up' : e.key === 'ArrowDown' ? 'down'
      : e.key === 'ArrowLeft' ? 'left' : e.key === 'ArrowRight' ? 'right' : null;
    const kb = this.scene!.input.keyboard!;
    const press = e.key === 'Enter' || (e.key === ' ' && kb.listenerCount('keydown-SPACE') === 0);
    const back = e.key === 'Escape' && kb.listenerCount('keydown-ESC') === 0;
    if (!dir && !press && !back) return;
    if (!this.isTopScene()) return;
    const ts = this.targets();
    if (ts.length === 0) return;
    if (dir) {
      e.preventDefault();
      const cur = this.shown ? ts.findIndex((t) => t.obj === this.focused) : -1;
      const pts = ts.map((t) => ({ x: t.r.centerX, y: t.r.centerY }));
      const i = nextFocus(pts, cur, dir);
      this.focused = i >= 0 ? ts[i].obj : null;
      this.shown = true;
      this.drawRing();
      return;
    }
    if (press && this.shown && this.focused && ts.some((t) => t.obj === this.focused)) {
      e.preventDefault();
      this.activate(this.focused);
      return;
    }
    if (back) {
      const t = ts.find((t) => isBackLabel(labelOf(t.obj)));
      if (t) this.activate(t.obj);
    }
  }

  /** Press a control the way a tap would: its pointerup handler if it has one, else pointerdown. */
  private activate(obj: GO): void {
    const s = this.scene!;
    const t = this.screenRect(obj);
    const p = new Phaser.Input.Pointer(s.input.manager, 9);
    if (t) {
      p.x = t.centerX;
      p.y = t.centerY;
      const w = worldRect(obj);
      p.worldX = w?.centerX ?? t.centerX;
      p.worldY = w?.centerY ?? t.centerY;
    }
    const evData = { stopPropagation: () => undefined };
    const ev = obj.listenerCount('pointerup') > 0 ? 'pointerup' : 'pointerdown';
    const before = new Set(this.targets().map((t) => t.obj));
    obj.emit(ev, p, 0, 0, evData);
    // a panel that opened takes the focus: its biggest new control (usually the main action)
    s.time.delayedCall(60, () => {
      if (!s.sys.isActive()) return;
      const fresh = this.targets().filter((t) => !before.has(t.obj));
      if (fresh.length) this.focused = fresh.reduce((a, b) => (b.r.width * b.r.height > a.r.width * a.r.height ? b : a)).obj;
      this.drawRing();
    });
  }

  /** Every control the keyboard can reach right now, with its screen rectangle. */
  targets(): Target[] {
    const s = this.scene;
    if (!s?.sys.isActive()) return [];
    const out: Target[] = [];
    const visit = (list: Phaser.GameObjects.GameObject[], parentVisible: boolean): void => {
      for (const o of list as GO[]) {
        const vis = parentVisible && o.visible !== false && (o.alpha ?? 1) > 0.05 && o.active;
        if (!vis) continue;
        const io = o.input;
        if (io && io.enabled && io.cursor === 'pointer' && o.enabled !== false) {
          const r = this.screenRect(o);
          if (r && r.width > 2 && r.centerX > 0 && r.centerX < GAME_W && r.centerY > 0 && r.centerY < GAME_H && this.reachable(o, r)) out.push({ obj: o, r });
        }
        if (o.list) visit(o.list, vis);
      }
    };
    visit(s.children.list, true);
    return out;
  }

  /** The control's bounds on screen, through whichever camera draws it. */
  private screenRect(o: GO): Phaser.Geom.Rectangle | null {
    const b = worldRect(o);
    if (!b) return null;
    let root: GO = o;
    while (root.parentContainer) root = root.parentContainer as unknown as GO;
    const cams = this.scene!.cameras.cameras;
    let cam: Phaser.Cameras.Scene2D.Camera | undefined;
    for (let i = cams.length - 1; i >= 0; i--) if (((root.cameraFilter ?? 0) & cams[i].id) === 0) { cam = cams[i]; break; }
    if (!cam) return null;
    const sx = root.scrollFactorX ?? 1;
    const sy = root.scrollFactorY ?? 1;
    const z = cam.zoom;
    const x = (b.x - cam.worldView.x + cam.scrollX * (1 - sx)) * z + cam.x;
    const y = (b.y - cam.worldView.y + cam.scrollY * (1 - sy)) * z + cam.y;
    return new Phaser.Geom.Rectangle(x, y, b.width * z, b.height * z);
  }

  /** A control counts only if a tap at its centre would land on it rather than on a blocker above it. */
  private reachable(o: GO, r: Phaser.Geom.Rectangle): boolean {
    const s = this.scene!;
    const p = new Phaser.Input.Pointer(s.input.manager, 9);
    p.x = r.centerX;
    p.y = r.centerY;
    const hits = s.input.hitTestPointer(p);
    if (hits.length === 0) return false;
    const top = s.input.sortGameObjects(hits, p)[0] as GO;
    if (top === o) return true;
    return top.input?.cursor === 'pointer';
  }

  private drawRing(): void {
    const s = this.scene;
    if (!s || !this.shown || !this.focused) return;
    if (!this.ring || !this.ring.active) this.ring = s.add.graphics().setDepth(RING_DEPTH).setScrollFactor(0);
    const t = this.targets().find((t) => t.obj === this.focused);
    this.ring.clear();
    if (!t) return;
    const pulse = 0.82 + 0.18 * Math.sin(s.time.now / 180);
    const r = t.r;
    this.ring.lineStyle(7, C.ink, 0.9);
    this.ring.strokeRoundedRect(r.x - 6, r.y - 6, r.width + 12, r.height + 12, 14);
    this.ring.lineStyle(4, C.gold, pulse);
    this.ring.strokeRoundedRect(r.x - 6, r.y - 6, r.width + 12, r.height + 12, 14);
  }

  /** The focused control's on-screen label, if any (used by tests and announcements). */
  focusedLabel(): string {
    return this.shown && this.focused ? labelOf(this.focused) : '';
  }
}

/**
 * A control's world rectangle from its own size (what setSize / the art declares), through its
 * world transform. Container bounds would only cover children with bounds (text), not drawn graphics.
 */
function worldRect(o: GO): Phaser.Geom.Rectangle | null {
  const t = o as unknown as {
    width?: number; height?: number; displayOriginX?: number; displayOriginY?: number;
    getWorldTransformMatrix?: () => Phaser.GameObjects.Components.TransformMatrix;
  };
  const w = t.width ?? 0;
  const h = t.height ?? 0;
  if (w > 0 && h > 0 && t.getWorldTransformMatrix) {
    const m = t.getWorldTransformMatrix();
    const ox = t.displayOriginX ?? w / 2;
    const oy = t.displayOriginY ?? h / 2;
    const a = m.transformPoint(-ox, -oy);
    const b = m.transformPoint(w - ox, h - oy);
    return new Phaser.Geom.Rectangle(Math.min(a.x, b.x), Math.min(a.y, b.y), Math.abs(b.x - a.x), Math.abs(b.y - a.y));
  }
  return o.getBounds?.() ?? null;
}

/** The text on a control: its own text, or the first text inside it. */
export function labelOf(o: Phaser.GameObjects.GameObject): string {
  const t = o as unknown as { text?: string; list?: Phaser.GameObjects.GameObject[] };
  if (typeof t.text === 'string') return t.text;
  for (const c of t.list ?? []) {
    const s = labelOf(c);
    if (s) return s;
  }
  return '';
}
