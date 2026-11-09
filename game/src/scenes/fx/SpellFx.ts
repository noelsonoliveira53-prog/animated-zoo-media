import Phaser from 'phaser';

/** Richer spell visuals. Every piece is a plain shape destroyed by its own tween; `low` keeps only the essentials. */

const ADD = Phaser.BlendModes.ADD;

/** A glowing ember left behind the falling star each frame. */
export function starTrail(scene: Phaser.Scene, x: number, y: number, low: boolean): void {
  if (low) return;
  const c = scene.add.circle(x, y, 14, 0xffd86a, 0.55).setDepth(4490).setBlendMode(ADD);
  scene.tweens.add({ targets: c, scale: 0.2, alpha: 0, duration: 320, onComplete: () => c.destroy() });
}

/** Starfall landing: scorched ground, light rays, a dust ring and rising embers. */
export function starImpact(scene: Phaser.Scene, x: number, y: number, r: number, low: boolean): void {
  const scorch = scene.add.ellipse(x, y + 4, r * 1.3, r * 0.62, 0x2a1a0e, 0.45).setDepth(6);
  scene.tweens.add({ targets: scorch, alpha: 0, delay: 2600, duration: 1600, onComplete: () => scorch.destroy() });
  if (low) return;
  const glow = scene.add.ellipse(x, y + 4, r * 0.9, r * 0.42, 0xff8a2a, 0.5).setDepth(7).setBlendMode(ADD);
  scene.tweens.add({ targets: glow, alpha: 0, duration: 1400, onComplete: () => glow.destroy() });
  for (let i = 0; i < 8; i++) {
    const a = (i / 8) * Math.PI * 2 + 0.2;
    const ray = scene.add.triangle(x, y, 0, -4, 0, 4, r * 1.1, 0, 0xfff0b0, 0.7).setOrigin(0, 0.5).setRotation(a).setDepth(2405).setBlendMode(ADD).setScale(0.2, 1);
    scene.tweens.add({ targets: ray, scaleX: 1, alpha: 0, duration: 380, ease: 'Quad.easeOut', onComplete: () => ray.destroy() });
  }
  const dust = scene.add.ellipse(x, y + 6, r * 1.6, r * 0.7, 0xb8a888, 0).setStrokeStyle(10, 0xb8a888, 0.5).setDepth(2399).setScale(0.3);
  scene.tweens.add({ targets: dust, scale: 1.2, alpha: 0, duration: 700, ease: 'Quad.easeOut', onComplete: () => dust.destroy() });
  for (let i = 0; i < 7; i++) {
    const e = scene.add.circle(x + (Math.random() - 0.5) * r, y + (Math.random() - 0.5) * r * 0.4, 2.5, 0xffa040, 1).setDepth(2406).setBlendMode(ADD);
    scene.tweens.add({ targets: e, y: e.y - 40 - Math.random() * 40, x: e.x + (Math.random() - 0.5) * 20, alpha: 0, duration: 900 + Math.random() * 600, ease: 'Sine.easeOut', onComplete: () => e.destroy() });
  }
}

/** Grove Call: bushes pop up, a whirl of leaves flies out and a soft golden ring marks the spot. */
export function groveBurst(scene: Phaser.Scene, x: number, y: number, low: boolean): void {
  const ring = scene.add.circle(x, y, 46, 0xffe27a, 0).setStrokeStyle(3, 0xffe27a, 0.9).setDepth(2400).setScale(0.3);
  scene.tweens.add({ targets: ring, scale: 1.3, alpha: 0, duration: 520, ease: 'Quad.easeOut', onComplete: () => ring.destroy() });
  if (low) return;
  for (let i = 0; i < 3; i++) {
    const a = (i / 3) * Math.PI * 2 - Math.PI / 2;
    const bx = x + Math.cos(a) * 26, by = y + Math.sin(a) * 14;
    const bush = scene.add.container(bx, by).setDepth(2398).setScale(0);
    bush.add(scene.add.circle(-8, 0, 10, 0x3f7a2e));
    bush.add(scene.add.circle(8, 0, 10, 0x3f7a2e));
    bush.add(scene.add.circle(0, -6, 12, 0x4f9a38));
    bush.add(scene.add.circle(-3, -10, 5, 0x8fdc5a, 0.7));
    scene.tweens.add({ targets: bush, scale: 1, duration: 200, delay: i * 60, ease: 'Back.easeOut' });
    scene.tweens.add({ targets: bush, scale: 0, alpha: 0, delay: 1300 + i * 60, duration: 300, onComplete: () => bush.destroy() });
  }
  for (let i = 0; i < 12; i++) {
    const a = (i / 12) * Math.PI * 2;
    const leaf = scene.add.ellipse(x, y, 10, 5, i % 3 ? 0x8fdc5a : 0xd9e8a0, 1).setDepth(2402).setRotation(a);
    const d = 50 + Math.random() * 30;
    scene.tweens.add({
      targets: leaf,
      x: x + Math.cos(a + 0.9) * d,
      y: y + Math.sin(a + 0.9) * d * 0.6 - 10,
      rotation: a + 4,
      alpha: 0,
      duration: 700 + Math.random() * 300,
      ease: 'Quad.easeOut',
      onComplete: () => leaf.destroy(),
    });
  }
}

/** Thornsnare: the road cracks, thorny vines grow up one after another and a tangled patch lingers while walkers are slowed. */
export function thornGrowth(scene: Phaser.Scene, x: number, y: number, r: number, linger: number, low: boolean): void {
  const patch = scene.add.ellipse(x, y, r * 2, r * 1.2, 0x2f4a1e, 0.35).setDepth(6).setScale(0.4);
  scene.tweens.add({ targets: patch, scale: 1, duration: 260, ease: 'Back.easeOut' });
  scene.tweens.add({ targets: patch, alpha: 0, delay: linger * 1000, duration: 700, onComplete: () => patch.destroy() });
  const ring = scene.add.circle(x, y, r, 0x4a7a2a, 0.25).setStrokeStyle(5, 0x8fdc5a, 1).setDepth(2400).setScale(0.3);
  scene.tweens.add({ targets: ring, scale: 1, alpha: 0, duration: 600, ease: 'Back.easeOut', onComplete: () => ring.destroy() });
  const n = low ? 7 : 13;
  for (let k = 0; k < n; k++) {
    const a = (k / n) * Math.PI * 2 + (k % 2) * 0.3;
    const d = r * (0.2 + ((k * 7) % 5) * 0.17);
    const vx = x + Math.cos(a) * d, vy = y + Math.sin(a) * d * 0.6;
    const h = 14 + ((k * 5) % 4) * 4;
    const v = scene.add.graphics({ x: vx, y: vy }).setDepth(2401 + vy / 10000).setScale(1, 0);
    v.fillStyle(0x2f6024, 1);
    v.fillTriangle(-5, 2, 5, 2, 0, -h);
    v.fillStyle(0x4f8a34, 1);
    v.fillTriangle(-2, 0, 3, 0, 1, -h + 3);
    v.fillStyle(0xd9e8a0, 1); // pale thorns
    v.fillTriangle(1, -h * 0.5, 6, -h * 0.55, 1, -h * 0.4);
    v.fillTriangle(-1, -h * 0.75, -6, -h * 0.8, -1, -h * 0.65);
    scene.tweens.add({ targets: v, scaleY: 1, duration: 220, delay: low ? 0 : k * 35, ease: 'Back.easeOut' });
    scene.tweens.add({ targets: v, scaleY: 0, alpha: 0, delay: linger * 1000 + k * 20, duration: 450, onComplete: () => v.destroy() });
  }
}
