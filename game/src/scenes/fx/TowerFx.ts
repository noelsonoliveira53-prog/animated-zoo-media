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
/** Glimmer (mage): arcane violet. */
const GLIM_VIOLET = 0xc89aff;

/** The effect style of each tower kind that has one: its signature colour and where its weapon sits. */
const STYLE: Record<string, { color: number; muzzle: number }> = {
  thornbow: { color: THORN_GOLD, muzzle: 58 },
  glimmer: { color: GLIM_VIOLET, muzzle: 66 },
  boulder: { color: 0xffa860, muzzle: 50 },
};

export class TowerFx {
  private sparks: Phaser.GameObjects.Particles.ParticleEmitter;
  private trailG: Phaser.GameObjects.Graphics;
  private dustG: Phaser.GameObjects.Graphics; // non-glowing trails (boulder dust)
  private shadows = new Map<number, Phaser.GameObjects.Ellipse>(); // ground shadows under lobbed shots
  private trails = new Map<number, Trail>();
  private auras = new Map<number, Phaser.GameObjects.GameObject[]>();
  private loops = new Map<number, Phaser.Tweens.Tween[]>(); // tweens driving plain objects (not game objects)

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
    this.dustG = scene.add.graphics().setDepth(2489);
  }

  /** A tower fired: a launch flash at the bow and a trail that follows the arrow. */
  onShoot(tower: Tower, p: Projectile, view: Phaser.GameObjects.Image | null | undefined): void {
    const st = STYLE[tower.def.id];
    if (!st) return;
    const color = tower.spec ? p.color : st.color;
    this.trails.set(p.uid, { kind: tower.def.id, color, pts: [] });
    const top = { x: tower.pos.x, y: tower.pos.y - st.muzzle };
    if (tower.def.id === 'boulder') {
      // the catapult arm thumps: the tower squats, a dust puff bursts at its feet and a few pebbles skitter out
      if (view) this.scene.tweens.add({ targets: view, scaleY: 0.86, scaleX: 1.06, duration: 70, yoyo: true, ease: 'Quad.easeOut' });
      for (let k = 0; k < 5; k++) {
        const puff = this.scene.add.circle(tower.pos.x + (Math.random() - 0.5) * 40, tower.pos.y + 8 + Math.random() * 6, 6 + Math.random() * 5, 0xc8b490, 0.55).setDepth(tower.pos.y + 2);
        this.scene.tweens.add({ targets: puff, x: puff.x + (puff.x - tower.pos.x) * 0.8, y: puff.y - 6, scale: 2, alpha: 0, duration: 420, onComplete: () => puff.destroy() });
      }
      this.shadows.set(p.uid, this.scene.add.ellipse(tower.pos.x, tower.pos.y, 22, 8, 0x000000, 0.28).setDepth(2480));
      return;
    }
    if (tower.def.id === 'glimmer') {
      // the orb gathers light, then looses the bolt: an inward-rushing ring and a bright core
      const ring = this.scene.add.circle(top.x, top.y, 18, color, 0).setStrokeStyle(2, color, 0.9).setDepth(2600).setBlendMode(Phaser.BlendModes.ADD);
      this.scene.tweens.add({ targets: ring, scale: 0.2, alpha: 0, duration: 160, onComplete: () => ring.destroy() });
      const core = this.scene.add.circle(top.x, top.y, 6, 0xffffff, 1).setDepth(2600).setBlendMode(Phaser.BlendModes.ADD);
      this.scene.tweens.add({ targets: core, scale: 2.4, alpha: 0, duration: 220, onComplete: () => core.destroy() });
      this.sparks.setParticleTint(color);
      this.sparks.explode(5, top.x, top.y);
      return;
    }
    // the bowstring snaps: a bright flick and a little puff of sparks pointing at the target
    const flash = this.scene.add.circle(top.x, top.y, 7, 0xfff6c8, 0.9).setDepth(2600).setBlendMode(Phaser.BlendModes.ADD);
    this.scene.tweens.add({ targets: flash, scale: 2.2, alpha: 0, duration: 140, onComplete: () => flash.destroy() });
    const a = Math.atan2(p.lastTargetPos.y - top.y, p.lastTargetPos.x - top.x);
    this.sparks.setParticleTint(color);
    this.sparks.explode(4, top.x + Math.cos(a) * 10, top.y + Math.sin(a) * 10);
    if (view && !motion.reduced) this.scene.tweens.add({ targets: view, angle: Math.cos(a) > 0 ? -3 : 3, duration: 60, yoyo: true });
  }

  /** Record where a projectile is drawn this frame (for its trail). */
  track(uid: number, x: number, y: number, groundX = x, groundY = y): void {
    const sh = this.shadows.get(uid);
    if (sh) {
      // the shadow stays on the ground and shrinks while the boulder is high
      const lift = Math.max(0, groundY - y);
      sh.setPosition(groundX, groundY + 6).setScale(Math.max(0.4, 1 - lift / 160)).setAlpha(0.32 - Math.min(0.18, lift / 600));
    }
    const t = this.trails.get(uid);
    if (!t) return;
    t.pts.push({ x, y });
    if (t.pts.length > 7) t.pts.shift();
  }

  /** A projectile landed (or fizzled): sparks and splinters where it ended. */
  gone(uid: number, x: number, y: number): void {
    const sh = this.shadows.get(uid);
    if (sh) {
      sh.destroy();
      this.shadows.delete(uid);
    }
    const t = this.trails.get(uid);
    if (!t) return;
    this.trails.delete(uid);
    if (t.kind === 'boulder') {
      // a heavy landing: a dust cloud, chunks of rock arcing out, a hot flash and a scorch mark that fades
      const flash = this.scene.add.circle(x, y, 16, 0xffd8a0, 0.7).setDepth(2600).setBlendMode(Phaser.BlendModes.ADD);
      this.scene.tweens.add({ targets: flash, scale: 2, alpha: 0, duration: 180, onComplete: () => flash.destroy() });
      for (let k = 0; k < 6; k++) {
        const a = (k / 6) * Math.PI * 2 + Math.random() * 0.5;
        const cloud = this.scene.add.circle(x, y, 9, 0xbca888, 0.6).setDepth(2595);
        this.scene.tweens.add({ targets: cloud, x: x + Math.cos(a) * 34, y: y + Math.sin(a) * 18 - 4, scale: 2.2, alpha: 0, duration: 520, ease: 'Cubic.easeOut', onComplete: () => cloud.destroy() });
      }
      for (let k = 0; k < 6; k++) {
        const chunk = this.scene.add.rectangle(x, y, 4 + Math.random() * 4, 4 + Math.random() * 3, 0x7a7068).setDepth(2600);
        const dx = (Math.random() - 0.5) * 90;
        const peak = 20 + Math.random() * 26;
        const prog = { t: 0 };
        this.scene.tweens.add({
          targets: prog,
          t: 1,
          duration: 420 + Math.random() * 160,
          onUpdate: () => chunk.setPosition(x + dx * prog.t, y - Math.sin(Math.PI * prog.t) * peak + prog.t * 10).setRotation(prog.t * 8),
          onComplete: () => chunk.destroy(),
        });
      }
      const scorch = this.scene.add.ellipse(x, y + 4, 40, 16, 0x2a2018, 0.35).setDepth(1.5);
      this.scene.tweens.add({ targets: scorch, alpha: 0, duration: 2600, delay: 600, onComplete: () => scorch.destroy() });
      return;
    }
    if (t.kind === 'glimmer') {
      // an arcane burst: an expanding rune ring, a flash and a spray of violet sparks
      const ring = this.scene.add.circle(x, y, 8, t.color, 0.25).setStrokeStyle(2.5, t.color, 1).setDepth(2600).setBlendMode(Phaser.BlendModes.ADD);
      this.scene.tweens.add({ targets: ring, scale: 2.8, alpha: 0, duration: 300, ease: 'Cubic.easeOut', onComplete: () => ring.destroy() });
      const flash = this.scene.add.circle(x, y, 10, 0xffffff, 0.9).setDepth(2600).setBlendMode(Phaser.BlendModes.ADD);
      this.scene.tweens.add({ targets: flash, scale: 0.2, alpha: 0, duration: 160, onComplete: () => flash.destroy() });
      this.sparks.setParticleTint(t.color);
      this.sparks.explode(10, x, y);
      return;
    }
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
    this.dustG.clear();
    for (const t of this.trails.values()) {
      const n = t.pts.length;
      if (t.kind === 'boulder') {
        // a faint grey dust trail behind the tumbling rock
        for (let i = 1; i < n; i++) {
          const f = i / n;
          this.dustG.fillStyle(0xb8a888, 0.08 + f * 0.18);
          this.dustG.fillCircle(t.pts[i].x, t.pts[i].y, 2 + (1 - f) * 5);
        }
        continue;
      }
      if (t.kind === 'glimmer') {
        // a crackling arcane streak: a soft wide glow with a jittering bright filament inside
        for (let i = 1; i < n; i++) {
          const f = i / n;
          g.lineStyle(3 + f * 6, t.color, 0.08 + f * 0.22);
          g.lineBetween(t.pts[i - 1].x, t.pts[i - 1].y, t.pts[i].x, t.pts[i].y);
        }
        g.lineStyle(1.5, 0xffffff, 0.85);
        g.beginPath();
        for (let i = 0; i < n; i++) {
          const j = i === n - 1 ? 0 : (Math.random() - 0.5) * 7;
          if (i === 0) g.moveTo(t.pts[i].x + j, t.pts[i].y + j);
          else g.lineTo(t.pts[i].x + j, t.pts[i].y - j);
        }
        g.strokePath();
        continue;
      }
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
    const st = STYLE[tower.def.id];
    if (!st) return;
    const objs: Phaser.GameObjects.GameObject[] = [];
    const tier = tower.spec ? 3 : tower.tier;
    if (tower.def.id === 'glimmer' && !motion.reduced) {
      // a ring of floating runes slowly circling the orb, more of them at higher tiers
      const runes = this.scene.add.graphics().setDepth(tower.pos.y + 2).setBlendMode(Phaser.BlendModes.ADD);
      const cx = tower.pos.x;
      const cy = tower.pos.y - st.muzzle;
      const count = 3 + tier;
      const spin = { a: Math.random() * Math.PI * 2 };
      const drawRunes = () => {
        runes.clear();
        for (let k = 0; k < count; k++) {
          const a = spin.a + (k / count) * Math.PI * 2;
          const rx = cx + Math.cos(a) * 22;
          const ry = cy + Math.sin(a) * 8;
          runes.fillStyle(st.color, 0.75);
          runes.fillRect(rx - 2, ry - 3, 4, 6);
          runes.fillStyle(0xffffff, 0.8);
          runes.fillRect(rx - 0.5, ry - 2, 1, 4);
        }
      };
      drawRunes();
      const tw = this.scene.tweens.add({ targets: spin, a: spin.a + Math.PI * 2, duration: 4200 - tier * 500, repeat: -1, onUpdate: () => runes.active && drawRunes() });
      this.loops.set(tower.slot, [tw]);
      objs.push(runes);
    }
    if (tier >= 1) {
      const glow = this.scene.add
        .ellipse(tower.pos.x, tower.pos.y + 4, 70 + tier * 6, 24 + tier * 2, st.color, 0.1 + tier * 0.05)
        .setDepth(tower.pos.y - 1)
        .setBlendMode(Phaser.BlendModes.ADD);
      objs.push(glow);
      if (!motion.reduced) this.scene.tweens.add({ targets: glow, alpha: glow.alpha * 0.45, duration: 1100, yoyo: true, repeat: -1, ease: 'Sine.easeInOut' });
    }
    if (tower.def.id === 'boulder' && tier >= 2 && !motion.reduced) {
      // the top-tier catapult's furnace: wisps of smoke curling up from its base
      const smoke = this.scene.add.particles(0, 0, 'dot', {
        x: { min: tower.pos.x - 14, max: tower.pos.x + 14 },
        y: tower.pos.y - 12,
        speedY: { min: -26, max: -12 },
        speedX: { min: -6, max: 10 },
        scale: { start: 0.5, end: 1.4 },
        alpha: { start: 0.35, end: 0 },
        lifespan: 1600,
        frequency: tier >= 3 ? 260 : 480,
        tint: 0x8a8278,
      });
      smoke.setDepth(tower.pos.y + 2);
      objs.push(smoke);
    } else if (tier >= 2 && !motion.reduced) {
      // drifting golden motes rising round the top-tier tower
      const motes = this.scene.add.particles(0, 0, 'dot', {
        x: { min: tower.pos.x - 26, max: tower.pos.x + 26 },
        y: { min: tower.pos.y - 10, max: tower.pos.y + 6 },
        speedY: { min: -30, max: -14 },
        scale: { start: 0.3, end: 0 },
        alpha: { start: 0.8, end: 0 },
        lifespan: 1400,
        frequency: tier >= 3 ? 220 : 420,
        tint: tower.spec ? 0xfff0c0 : st.color,
        blendMode: Phaser.BlendModes.ADD,
      });
      motes.setDepth(tower.pos.y + 2);
      objs.push(motes);
    }
    if (!motion.reduced) this.scene.tweens.add({ targets: view, scaleX: 1.03, duration: 1300 + (tower.slot % 5) * 90, yoyo: true, repeat: -1, ease: 'Sine.easeInOut', delay: 320 });
    this.auras.set(tower.slot, objs);
  }

  removed(slot: number): void {
    for (const o of this.auras.get(slot) ?? []) {
      this.scene.tweens.killTweensOf(o);
      o.destroy();
    }
    this.auras.delete(slot);
    for (const tw of this.loops.get(slot) ?? []) tw.remove();
    this.loops.delete(slot);
  }
}
