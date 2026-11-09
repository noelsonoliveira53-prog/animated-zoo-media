import Phaser from 'phaser';
import { textStyle } from '../../ui/theme';

/** Construction and upgrade juice for towers. Plain shapes, each destroyed by its own tween. */

const ADD = Phaser.BlendModes.ADD;

function gone(scene: Phaser.Scene, o: Phaser.GameObjects.GameObject, props: object, duration: number, delay = 0, ease = 'Quad.easeOut'): void {
  scene.tweens.add({ targets: o, ...props, duration, delay, ease, onComplete: () => o.destroy() });
}

/** A new tower: a scaffold frame flashes up, a ring thumps the ground and dust rolls out low. */
export function buildPuff(scene: Phaser.Scene, x: number, y: number, low: boolean): void {
  const ring = scene.add.ellipse(x, y + 8, 80, 26, 0xd9c39a, 0).setStrokeStyle(4, 0xe8d9b5, 0.85).setDepth(y - 1).setScale(0.3);
  gone(scene, ring, { scale: 1.25, alpha: 0 }, 380);
  if (low) return;
  // scaffold: two poles, a cross-brace and a plank, flashing pale and fading as the tower pops in
  const sc = scene.add.graphics({ x, y }).setDepth(y + 3);
  sc.lineStyle(4, 0x8a6a42, 1);
  sc.lineBetween(-22, 6, -18, -70);
  sc.lineBetween(22, 6, 18, -70);
  sc.lineBetween(-20, -10, 20, -50);
  sc.lineBetween(-20, -50, 20, -10);
  sc.fillStyle(0xb08a5a, 1);
  sc.fillRect(-26, -72, 52, 6);
  sc.setScale(1, 0.2);
  scene.tweens.add({ targets: sc, scaleY: 1, duration: 120, ease: 'Back.easeOut' });
  gone(scene, sc, { alpha: 0, scaleY: 1.15 }, 260, 200);
  for (let i = 0; i < 8; i++) {
    const a = (i / 8) * Math.PI * 2;
    const p = scene.add.circle(x + Math.cos(a) * 14, y + 6 + Math.sin(a) * 5, 7 + (i % 3) * 2, 0xe2d6bc, 0.75).setDepth(y + 2);
    gone(scene, p, { x: x + Math.cos(a) * 52, y: y + 6 + Math.sin(a) * 16 - 6, scale: 1.8, alpha: 0 }, 520 + i * 20);
  }
}

/** An upgrade: a pillar of light, sparkles rising and a tier badge that floats up. `tier` is 1-based; 4 = specialization. */
export function upgradeBurst(scene: Phaser.Scene, x: number, y: number, tier: number, color: number, low: boolean): void {
  const badgeText = tier >= 4 ? '★★★' : 'Lv ' + tier;
  const badge = scene.add.text(x, y - 74, badgeText, textStyle(tier >= 4 ? 20 : 16, tier >= 4 ? '#ffd23c' : '#fff6d8')).setOrigin(0.5).setDepth(3050).setScale(0.4);
  scene.tweens.add({ targets: badge, scale: 1, duration: 180, ease: 'Back.easeOut' });
  gone(scene, badge, { y: y - 112, alpha: 0 }, 600, 520, 'Sine.easeIn');
  if (low) return;
  // soft-edged pillar: three nested bands, brightest in the middle
  const pillar = scene.add.container(x, y + 6).setDepth(y + 4).setScale(0.4, 0.05);
  for (const [w, a] of [[48, 0.14], [30, 0.22], [12, 0.45]] as const) {
    pillar.add(scene.add.rectangle(0, 0, w, 130, color, a).setOrigin(0.5, 1).setBlendMode(ADD));
    pillar.add(scene.add.ellipse(0, -130, w, w * 0.6, color, a).setBlendMode(ADD)); // rounded top
  }
  scene.tweens.add({
    targets: pillar, scaleX: 1, scaleY: 1, duration: 200, ease: 'Quad.easeOut',
    onComplete: () => gone(scene, pillar, { alpha: 0, scaleX: 0.15 }, 420, 80),
  });
  const n = 6 + tier * 2;
  for (let i = 0; i < n; i++) {
    const s = scene.add.star(x + (Math.random() - 0.5) * 50, y - Math.random() * 30, 4, 1.5, 4.5, i % 2 ? 0xffffff : color).setDepth(y + 5).setBlendMode(ADD);
    gone(scene, s, { y: s.y - 60 - Math.random() * 50, angle: 180, alpha: 0 }, 700 + Math.random() * 300, i * 25, 'Sine.easeOut');
  }
}
