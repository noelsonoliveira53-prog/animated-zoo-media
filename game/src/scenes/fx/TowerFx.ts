import Phaser from 'phaser';
import type { Projectile, Tower } from '../../systems/BattleSim';
import { motion } from '../../ui/motion';

// Per-tower visual effects: launch flashes, projectile trails, impacts, idle animation and a per-tier aura.
// Each tower kind gets its own look; kinds without a style yet fall back to the plain sprites.

interface Trail {
  kind: string;
  color: number;
  pts: { x: number; y: number }[];
}

/** Thornbow (archer): warm gold for plain arrows; specialised arrows keep their own colour. */
const THORN_GOLD = 0xffe08a;

export class TowerFx {
  private sparks: Phaser.GameObjects.Particles.ParticleEmitter;
  private trailG: Phaser.GameObjects.Graphics;
  private trails = new Map<number, Trail>();
  private auras = new Map<number, Phaser.GameObjects.GameObject[]>();

  constructor(private scene: Phaser.Scene) {
    this.sparks = scene.add.particles(0, 0, 'dot', {
      speed: { min: 40, max: 160 },
      scale: { start: 0.45, end: 0 },
      lifespan: { min: 180, max: 360 },
      blendMode: Phaser.BlendModes.ADD,
      emitting: false,
    });
    this.sparks.setDepth(2600);
    this.trailG = scene.add.graphics().setDepth(2490).setBlendMode(Phaser.BlendModes.ADD);
  }

  /** A tower fired: a launch flash at the bow and a trail that follows the arrow. */
  onShoot(tower: Tower, p: Projectile, view: Phaser.GameObjects.Image | null | undefined): void {
    if (tower.def.id !== 'thornbow') return;
    const color = tower.spec ? p.color : THORN_GOLD;
    this.trails.set(p.uid, { kind: 'thornbow', color, pts: [] });
    const top = { x: tower.pos.x, y: tower.pos.y - 58 };
    // the bowstring snaps: a bright flick and a little puff of sparks pointing at the target
    const flash = this.scene.add.circle(top.x, top.y, 7, 0xfff6c8, 0.9).setDepth(2600).setBlendMode(Phaser.BlendModes.ADD);
    this.scene.tweens.add({ targets: flash, scale: 2.2, alpha: 0, duration: 140, onComplete: () => flash.destroy() });
    const a = Math.atan2(p.lastTargetPos.y - top.y, p.lastTargetPos.x - top.x);
    this.sparks.setParticleTint(color);
    this.sparks.explode(4, top.x + Math.cos(a) * 10, top.y + Math.sin(a) * 10);
    if (view && !motion.reduced) this.scene.tweens.add({ targets: view, angle: Math.cos(a) > 0 ? -3 : 3, duration: 60, yoyo: true });
  }

  /** Record where a projectile is drawn this frame (for its trail). */
  track(uid: number, x: number, y: number): void {
    const t = this.trails.get(uid);
    if (!t) return;
    t.pts.push({ x, y });
    if (t.pts.length > 7) t.pts.shift();
  }

  /** A projectile landed (or fizzled): sparks and splinters where it ended. */
  gone(uid: number, x: number, y: number): void {
    const t = this.trails.get(uid);
    if (!t) return;
    this.trails.delete(uid);
    if (t.kind === 'thornbow') {
      this.sparks.setParticleTint(t.color);
      this.sparks.explode(7, x, y);
      const g = this.scene.add.graphics().setDepth(2600);
      g.lineStyle(2, 0xc89a5a, 1);
      for (let k = 0; k < 4; k++) {
        const a = Math.random() * Math.PI * 2;
        g.lineBetween(x + Math.cos(a) * 3, y + Math.sin(a) * 3, x + Math.cos(a) * 9, y + Math.sin(a) * 9);
      }
      this.scene.tweens.add({ targets: g, alpha: 0, scale: 1.4, duration: 220, onComplete: () => g.destroy() });
    }
  }

  /** Draw every live trail as a glowing streak that thins toward its tail. */
  draw(): void {
    const g = this.trailG;
    g.clear();
    for (const t of this.trails.values()) {
      const n = t.pts.length;
      for (let i = 1; i < n; i++) {
        const f = i / n;
        g.lineStyle(1 + f * 3, t.color, 0.15 + f * 0.55);
        g.lineBetween(t.pts[i - 1].x, t.pts[i - 1].y, t.pts[i].x, t.pts[i].y);
      }
    }
  }

  /** A tower was built or upgraded: idle sway and a glowing aura that grows with its tier. */
  placed(tower: Tower, view: Phaser.GameObjects.Image): void {
    this.removed(tower.slot);
    if (tower.def.id !== 'thornbow') return;
    const objs: Phaser.GameObjects.GameObject[] = [];
    const tier = tower.spec ? 3 : tower.tier;
    if (tier >= 1) {
      const glow = this.scene.add
        .ellipse(tower.pos.x, tower.pos.y + 4, 70 + tier * 6, 24 + tier * 2, THORN_GOLD, 0.1 + tier * 0.05)
        .setDepth(tower.pos.y - 1)
        .setBlendMode(Phaser.BlendModes.ADD);
      objs.push(glow);
      if (!motion.reduced) this.scene.tweens.add({ targets: glow, alpha: glow.alpha * 0.45, duration: 1100, yoyo: true, repeat: -1, ease: 'Sine.easeInOut' });
    }
    if (tier >= 2 && !motion.reduced) {
      // drifting golden motes rising round the top-tier tower
      const motes = this.scene.add.particles(0, 0, 'dot', {
        x: { min: tower.pos.x - 26, max: tower.pos.x + 26 },
        y: { min: tower.pos.y - 10, max: tower.pos.y + 6 },
        speedY: { min: -30, max: -14 },
        scale: { start: 0.3, end: 0 },
        alpha: { start: 0.8, end: 0 },
        lifespan: 1400,
        frequency: tier >= 3 ? 220 : 420,
        tint: tower.spec ? 0xfff0c0 : THORN_GOLD,
        blendMode: Phaser.BlendModes.ADD,
      });
      motes.setDepth(tower.pos.y + 2);
      objs.push(motes);
    }
    if (!motion.reduced) this.scene.tweens.add({ targets: view, scaleX: 1.03, duration: 1300 + (tower.slot % 5) * 90, yoyo: true, repeat: -1, ease: 'Sine.easeInOut', delay: 320 });
    this.auras.set(tower.slot, objs);
  }

  removed(slot: number): void {
    for (const o of this.auras.get(slot) ?? []) o.destroy();
    this.auras.delete(slot);
  }
}
