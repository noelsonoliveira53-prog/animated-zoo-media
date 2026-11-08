import Phaser from 'phaser';
import type { DeathStyle } from '../../systems/deathStyle';

const SHARD_GREY = 0xc8ccd4;

/** Short-lived, enemy-specific death bursts. Every piece is a plain shape with one tween that destroys it. */
export function playDeath(scene: Phaser.Scene, x: number, y: number, st: DeathStyle, low: boolean): void {
  const s = st.size;
  // movement eases out (a fast burst that settles); the fade eases in so pieces stay readable most of their life
  const fly = (o: Phaser.GameObjects.Shape, props: Record<string, number>, duration: number) => {
    const { alpha, ...move } = props;
    scene.tweens.add({ targets: o, ...move, duration, ease: 'Quad.easeOut' });
    scene.tweens.add({ targets: o, alpha: alpha ?? 0, duration, ease: 'Cubic.easeIn', onComplete: () => o.destroy() });
  };

  // a soft colored flash ring for every death
  const ring = scene.add.circle(x, y, 18 * s, st.color, 0).setStrokeStyle(st.heavy ? 5 : 3, st.color, 0.85).setDepth(2400).setScale(0.4);
  fly(ring, { scale: st.heavy ? 2.2 : 1.4, alpha: 0 }, st.heavy ? 420 : 260);
  if (low) return;

  const n = st.heavy ? 8 : 5;
  switch (st.kind) {
    case 'puff':
      for (let i = 0; i < n; i++) {
        const a = (i / n) * Math.PI * 2 + Math.random() * 0.5;
        const c = scene.add.circle(x + Math.cos(a) * 6, y + Math.sin(a) * 4, (5 + Math.random() * 4) * s, 0xe8e2d4, 0.55).setDepth(2390);
        fly(c, { x: x + Math.cos(a) * 20 * s, y: y + Math.sin(a) * 10 * s - 16 * s, scale: 1.8, alpha: 0 }, 420 + Math.random() * 160);
      }
      break;
    case 'feathers':
      for (let i = 0; i < n; i++) {
        const f = scene.add.ellipse(x, y - 20, 12 * s, 5 * s, i % 2 ? st.color : 0xf4efe4, 1).setDepth(2390).setRotation(Math.random() * 3);
        const dx = (Math.random() - 0.5) * 60 * s;
        fly(f, { x: x + dx, y: y + 10 + Math.random() * 20, rotation: f.rotation + (dx > 0 ? 3 : -3), alpha: 0 }, 700 + Math.random() * 300);
      }
      break;
    case 'shards':
      for (let i = 0; i < n + 1; i++) {
        const a = (i / (n + 1)) * Math.PI * 2;
        const t = scene.add.triangle(x, y, 0, 0, 10 * s, 3 * s, 3 * s, 10 * s, i % 2 ? SHARD_GREY : st.color, 1).setDepth(2390);
        const r = (24 + Math.random() * 16) * s;
        fly(t, { x: x + Math.cos(a) * r, y: y + Math.sin(a) * r * 0.6 + 8, angle: 360 * (Math.random() > 0.5 ? 1 : -1), alpha: 0 }, 380 + Math.random() * 120);
      }
      break;
    case 'ooze': {
      const splat = scene.add.ellipse(x, y + 6, 34 * s, 14 * s, st.color, 0.55).setDepth(6).setScale(0.3);
      scene.tweens.add({ targets: splat, scale: 1, duration: 140, ease: 'Back.easeOut' });
      scene.tweens.add({ targets: splat, alpha: 0, delay: 900, duration: 700, onComplete: () => splat.destroy() });
      for (let i = 0; i < 4; i++) {
        const d = scene.add.circle(x, y, 3 * s, st.color, 1).setDepth(2390);
        const dx = (Math.random() - 0.5) * 50 * s;
        fly(d, { x: x + dx, y: y + 4 + Math.random() * 8, alpha: 0 }, 320);
      }
      break;
    }
  }
}
