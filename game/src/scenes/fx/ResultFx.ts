import Phaser from 'phaser';
import { sfx } from '../../systems/audio';

/** Juice for the end-of-battle panel: rays, confetti or ash, ribbon, slamming stars and rolling reward numbers. */

const ADD = Phaser.BlendModes.ADD;

/** Slowly turning sun rays behind the victory panel. */
export function victoryRays(scene: Phaser.Scene, x: number, y: number, depth: number, still: boolean): void {
  const g = scene.add.graphics({ x, y }).setDepth(depth).setBlendMode(ADD).setAlpha(0);
  for (let i = 0; i < 14; i++) {
    const a = (i / 14) * Math.PI * 2;
    g.fillStyle(0xffe08a, 0.11);
    g.fillTriangle(0, 0, Math.cos(a - 0.09) * 520, Math.sin(a - 0.09) * 520, Math.cos(a + 0.09) * 520, Math.sin(a + 0.09) * 520);
  }
  scene.tweens.add({ targets: g, alpha: 1, duration: 500 });
  if (!still) scene.tweens.add({ targets: g, angle: 360, duration: 40000, repeat: -1 });
}

/** Confetti that tumbles down over the screen for a couple of seconds. */
export function confetti(scene: Phaser.Scene, w: number, depth: number): void {
  const colors = [0xffd23c, 0xff8a6a, 0x8fdc5a, 0x6ad8ff, 0xd8a8ff, 0xffffff];
  for (let i = 0; i < 46; i++) {
    const x = Math.random() * w;
    const p = scene.add.rectangle(x, -20 - Math.random() * 200, 7, 12, colors[i % colors.length]).setDepth(depth).setRotation(Math.random() * 3);
    scene.tweens.add({
      targets: p,
      y: 760,
      x: x + (Math.random() - 0.5) * 160,
      rotation: p.rotation + (Math.random() > 0.5 ? 8 : -8),
      scaleX: { from: 1, to: 0.3 },
      duration: 2200 + Math.random() * 1400,
      delay: 200 + Math.random() * 700,
      ease: 'Sine.easeIn',
      onComplete: () => p.destroy(),
    });
  }
}

/** Grey ash drifting up after a defeat. */
export function ash(scene: Phaser.Scene, w: number, h: number, depth: number): void {
  for (let i = 0; i < 24; i++) {
    const p = scene.add.circle(Math.random() * w, h + 10, 2 + Math.random() * 3, 0x9a948c, 0.6).setDepth(depth);
    scene.tweens.add({ targets: p, y: h * 0.2 + Math.random() * 200, x: p.x + (Math.random() - 0.5) * 120, alpha: 0, duration: 3000 + Math.random() * 1500, delay: Math.random() * 1200, onComplete: () => p.destroy() });
  }
}

/** A ribbon banner with forked tails, drawn into the panel behind the title. */
export function ribbon(scene: Phaser.Scene, y: number, w: number, color: number, dark: number): Phaser.GameObjects.Graphics {
  const g = scene.add.graphics();
  const h = 64;
  // tails
  g.fillStyle(dark, 1);
  for (const s of [-1, 1]) {
    const x0 = s * (w / 2 - 10);
    const x1 = s * (w / 2 + 44);
    g.fillPoints([{ x: x0, y: y - h / 2 + 12 }, { x: x1, y: y - h / 2 + 12 }, { x: x1 - s * 16, y: y + 6 }, { x: x1, y: y + h / 2 + 2 }, { x: x0, y: y + h / 2 + 2 }], true);
  }
  g.fillStyle(0x000000, 0.25);
  g.fillRoundedRect(-w / 2 + 4, y - h / 2 + 6, w, h, 10);
  g.fillStyle(color, 1);
  g.fillRoundedRect(-w / 2, y - h / 2, w, h, 10);
  g.fillStyle(0xffffff, 0.18);
  g.fillRoundedRect(-w / 2 + 4, y - h / 2 + 4, w - 8, h * 0.38, 8);
  g.lineStyle(3, dark, 1);
  g.strokeRoundedRect(-w / 2, y - h / 2, w, h, 10);
  return g;
}

/**
 * Earned stars drop in big and slam down with a flash ring, a burst of sparks and a chime;
 * empty stars just fade up. `world` is the star's position on screen (for the effects outside the panel).
 */
export function starSlam(scene: Phaser.Scene, star: Phaser.GameObjects.Image, earned: boolean, delay: number, world: { x: number; y: number }, depth: number, still: boolean): void {
  if (!earned || still) {
    star.setScale(0).setAlpha(earned ? 1 : 0.8);
    scene.tweens.add({ targets: star, scale: 1.4, delay, duration: 300, ease: 'Back.easeOut' });
    return;
  }
  star.setScale(3.2).setAlpha(0).setAngle(-30);
  scene.tweens.add({
    targets: star, scale: 1.4, alpha: 1, angle: 0, delay, duration: 260, ease: 'Quad.easeIn',
    onComplete: () => {
      sfx.coin();
      scene.cameras.main.shake(90, 0.004);
      const ring = scene.add.circle(world.x, world.y, 30, 0xffe08a, 0).setStrokeStyle(5, 0xffe08a, 1).setDepth(depth).setBlendMode(ADD);
      scene.tweens.add({ targets: ring, scale: 2.4, alpha: 0, duration: 420, onComplete: () => ring.destroy() });
      for (let k = 0; k < 10; k++) {
        const a = (k / 10) * Math.PI * 2;
        const sp = scene.add.star(world.x, world.y, 4, 2, 6, 0xffe08a).setDepth(depth).setBlendMode(ADD);
        scene.tweens.add({ targets: sp, x: world.x + Math.cos(a) * 70, y: world.y + Math.sin(a) * 70, alpha: 0, angle: 180, duration: 500, ease: 'Quad.easeOut', onComplete: () => sp.destroy() });
      }
      scene.tweens.add({ targets: star, scale: 1.6, duration: 90, yoyo: true });
    },
  });
}

/** Roll a text's numbers up from zero: `fmt` turns the current values into the label. */
export function countUp(scene: Phaser.Scene, text: Phaser.GameObjects.Text, values: number[], fmt: (v: number[]) => string, delay: number, still: boolean): void {
  if (still) {
    text.setText(fmt(values));
    return;
  }
  const o = { t: 0 };
  text.setText(fmt(values.map(() => 0)));
  scene.tweens.add({
    targets: o, t: 1, delay, duration: 900, ease: 'Cubic.easeOut',
    onUpdate: () => text.active && text.setText(fmt(values.map((v) => Math.round(v * o.t)))),
    onComplete: () => text.active && text.setText(fmt(values)),
  });
}
