import Phaser from 'phaser';
import type { WeatherSpec } from '../../data/weather';

const ADD = Phaser.BlendModes.ADD;
const DEPTH = 2200; // above the field and units, under the HUD

/** Spawns one piece of weather per tick; every piece is a plain shape that its own tween destroys. */
export function startWeather(scene: Phaser.Scene, spec: WeatherSpec, w: number, h: number): Phaser.Time.TimerEvent | null {
  if (spec.kind === 'none') return null;
  const rnd = Phaser.Math;
  const pick = () => spec.colors[rnd.Between(0, spec.colors.length - 1)];
  const gone = (o: Phaser.GameObjects.GameObject, props: object, duration: number, ease = 'Linear') =>
    scene.tweens.add({ targets: o, ...props, duration, ease, onComplete: () => o.destroy() });
  const spawn = () => {
    switch (spec.kind) {
      case 'leaves': {
        const x = rnd.Between(-40, w), s = rnd.FloatBetween(0.8, 1.3);
        const leaf = scene.add.ellipse(x, -12, 10 * s, 5 * s, pick(), 0.9).setDepth(DEPTH).setRotation(rnd.FloatBetween(0, 3));
        gone(leaf, { x: x + rnd.Between(80, 240), y: h + 20, rotation: leaf.rotation + rnd.FloatBetween(4, 9) }, rnd.Between(7000, 11000));
        break;
      }
      case 'rain': {
        const x = rnd.Between(-100, w);
        const drop = scene.add.rectangle(x, -20, 1.5, 16, pick(), 0.45).setDepth(DEPTH).setRotation(0.25);
        gone(drop, { x: x + 160, y: h + 20 }, rnd.Between(500, 700));
        break;
      }
      case 'wind': {
        const y = rnd.Between(80, h - 80), len = rnd.Between(60, 140);
        const streak = scene.add.rectangle(-len, y, len, 1.5, pick(), 0).setDepth(DEPTH).setOrigin(0, 0.5);
        scene.tweens.add({ targets: streak, alpha: 0.35, duration: 500, yoyo: true, hold: 600 });
        gone(streak, { x: w + 20, y: y - rnd.Between(0, 30) }, rnd.Between(1600, 2400));
        break;
      }
      case 'sand': {
        const y = rnd.Between(60, h), x = rnd.Between(-30, w * 0.3);
        const g = scene.add.circle(x, y, rnd.FloatBetween(1, 2.2), pick(), 0.7).setDepth(DEPTH);
        gone(g, { x: x + rnd.Between(500, 900), y: y + rnd.Between(-40, 20), alpha: 0 }, rnd.Between(2400, 3600));
        break;
      }
      case 'bubbles': {
        const x = rnd.Between(0, w), r = rnd.FloatBetween(2, 5);
        const b = scene.add.circle(x, h + 10, r, pick(), 0.08).setStrokeStyle(1, pick(), 0.6).setDepth(DEPTH);
        gone(b, { y: rnd.Between(80, h * 0.6), x: x + rnd.Between(-30, 30), alpha: 0 }, rnd.Between(5000, 8000), 'Sine.easeOut');
        break;
      }
      case 'spray': {
        const x = rnd.Between(0, w), y = rnd.Between(100, h);
        const s = scene.add.circle(x, y, rnd.FloatBetween(1, 2), pick(), 0).setDepth(DEPTH);
        scene.tweens.add({ targets: s, alpha: 0.7, duration: 600, yoyo: true });
        gone(s, { x: x + rnd.Between(40, 120), y: y - rnd.Between(10, 40) }, 1200);
        break;
      }
      case 'sparkles': {
        const st = scene.add.star(rnd.Between(0, w), rnd.Between(80, h), 4, 1, 4, pick(), 1).setDepth(DEPTH).setBlendMode(ADD).setScale(0);
        scene.tweens.add({ targets: st, scale: 1, angle: 90, duration: 500, yoyo: true, onComplete: () => st.destroy() });
        break;
      }
      case 'spores':
      case 'pollen': {
        const x = rnd.Between(0, w), y = rnd.Between(h * 0.3, h + 10);
        const p = scene.add.circle(x, y, rnd.FloatBetween(1.2, 2.6), pick(), 0).setDepth(DEPTH).setBlendMode(ADD);
        scene.tweens.add({ targets: p, alpha: spec.kind === 'pollen' ? 0.75 : 0.6, duration: 1600, yoyo: true, hold: 1600 });
        gone(p, { y: y - rnd.Between(80, 200), x: x + rnd.Between(-50, 50) }, 4800, 'Sine.easeInOut');
        break;
      }
      case 'down': {
        const x = rnd.Between(-60, w), y = rnd.Between(60, h);
        const c = scene.add.container(x, y).setDepth(DEPTH).setAlpha(0);
        c.add(scene.add.circle(0, 0, 3, pick(), 0.8));
        c.add(scene.add.rectangle(0, 4, 1, 6, 0xd8d0c0, 0.7));
        scene.tweens.add({ targets: c, alpha: 1, duration: 900, yoyo: true, hold: 3000 });
        gone(c, { x: x + rnd.Between(160, 320), y: y - rnd.Between(20, 70), angle: rnd.Between(-60, 60) }, 4800, 'Sine.easeInOut');
        break;
      }
      case 'soot': {
        const x = rnd.Between(0, w), y = rnd.Between(60, h);
        const s = scene.add.circle(x, y, rnd.FloatBetween(1, 2.2), pick(), 0).setDepth(DEPTH);
        scene.tweens.add({ targets: s, alpha: 0.55, duration: 1200, yoyo: true, hold: 1200 });
        gone(s, { x: x + rnd.Between(-40, 40), y: y + rnd.Between(40, 120) }, 3600);
        break;
      }
    }
  };
  // a quick head start so the screen isn't empty in the first seconds
  for (let i = 0; i < 6; i++) spawn();
  return scene.time.addEvent({ delay: spec.every, loop: true, callback: spawn });
}
