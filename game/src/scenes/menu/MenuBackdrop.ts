import Phaser from 'phaser';
import { motion } from '../../ui/motion';

/** Animated title backdrop: a warm evening sky, drifting clouds, layered hills, a lit watchtower and fireflies. */
export function drawMenuBackdrop(scene: Phaser.Scene, w: number, h: number): void {
  const still = motion.reduced || motion.lowFx;
  const sky = scene.add.graphics().setDepth(-20);
  sky.fillGradientStyle(0x5aa8e0, 0x5aa8e0, 0xffd9a0, 0xffd9a0, 1);
  sky.fillRect(0, 0, w, h * 0.75);
  sky.fillStyle(0xffd9a0, 1);
  sky.fillRect(0, h * 0.75, w, h * 0.25);

  // low sun with a soft halo
  const sx = w * 0.8, sy = h * 0.33; // up and to the right, clear of the title text
  const halo = scene.add.circle(sx, sy, 150, 0xfff0c0, 0.25).setDepth(-19).setBlendMode(Phaser.BlendModes.ADD);
  scene.add.circle(sx, sy, 90, 0xfff4d0, 0.35).setDepth(-19).setBlendMode(Phaser.BlendModes.ADD);
  scene.add.circle(sx, sy, 48, 0xfff8e4, 1).setDepth(-19);
  if (!still) scene.tweens.add({ targets: halo, scale: 1.08, alpha: 0.32, duration: 2600, yoyo: true, repeat: -1, ease: 'Sine.easeInOut' });

  // clouds drift right and wrap around
  const rnd = new Phaser.Math.RandomDataGenerator(['menu-sky']);
  for (let i = 0; i < 7; i++) {
    const cy = rnd.between(40, 300);
    const s = rnd.realInRange(0.6, 1.3);
    const c = scene.add.container(rnd.between(-100, w + 100), cy).setDepth(-18).setAlpha(0.85);
    const parts: [number, number, number][] = [[-40, 6, 26], [-12, -8, 34], [22, -2, 30], [48, 8, 22], [6, 10, 28]];
    for (const [px, py, r] of parts) c.add(scene.add.circle(px * s, py * s, r * s, 0xfff8ee));
    for (const [px, py, r] of parts) c.add(scene.add.circle(px * s, py * s + r * s * 0.45, r * s * 0.7, 0xf2d2c0, 0.6));
    if (!still) {
      const speed = rnd.between(10, 22) * (1.4 - s * 0.4); // px per second; nearer clouds a touch faster
      const drift = () => {
        const dist = w + 220 - c.x;
        scene.tweens.add({
          targets: c, x: w + 220, duration: (dist / speed) * 1000,
          onComplete: () => { c.x = -220; drift(); },
        });
      };
      drift();
    }
  }

  // far mountains, then layered hills
  const g = scene.add.graphics().setDepth(-17);
  g.fillStyle(0x9fb6c8, 1);
  g.beginPath();
  g.moveTo(0, h);
  for (let x = 0; x <= w; x += 40) g.lineTo(x, 400 - Math.abs(Math.sin(x / 210)) * 120 - Math.sin(x / 67) * 14);
  g.lineTo(w, h);
  g.closePath();
  g.fillPath();
  const hills: [number, number, number][] = [
    [0x86c56a, 470, 90],
    [0x6aae52, 540, 70],
    [0x52953f, 620, 60],
  ];
  const hillY = (x: number, base: number, amp: number) => base - Math.sin(x / 170 + base) * amp * 0.5 - Math.cos(x / 90) * amp * 0.2;
  hills.forEach(([color, base, amp], li) => {
    g.fillStyle(color, 1);
    g.beginPath();
    g.moveTo(0, h);
    for (let x = 0; x <= w; x += 20) g.lineTo(x, hillY(x, base, amp));
    g.lineTo(w, h);
    g.closePath();
    g.fillPath();
    // sunlit rim along each ridge
    g.lineStyle(3, 0xffe8a8, 0.35 - li * 0.08);
    g.beginPath();
    for (let x = 0; x <= w; x += 20) (x === 0 ? g.moveTo(x, hillY(x, base, amp) + 2) : g.lineTo(x, hillY(x, base, amp) + 2));
    g.strokePath();
  });
  // pine silhouettes on the middle ridge
  for (let i = 0; i < 16; i++) {
    const x = rnd.between(0, w);
    const y = hillY(x, 540, 70) + 6;
    const s = rnd.realInRange(0.7, 1.2);
    g.fillStyle(0x3f7a33, 1);
    g.fillTriangle(x - 12 * s, y, x + 12 * s, y, x, y - 40 * s);
    g.fillTriangle(x - 9 * s, y - 16 * s, x + 9 * s, y - 16 * s, x, y - 50 * s);
  }

  // the watchtower on its hill, with a lit window and a waving pennant
  const tx = 745, ty = hillY(745, 470, 90) + 8;
  const t = scene.add.graphics().setDepth(-16);
  t.fillStyle(0x3a2a20, 1);
  t.fillRect(tx - 18, ty - 150, 36, 150);
  t.fillStyle(0x4a362a, 1);
  t.fillRect(tx - 26, ty - 168, 52, 22);
  for (let k = 0; k < 4; k++) t.fillRect(tx - 26 + k * 15, ty - 182, 9, 14);
  t.fillStyle(0x2c2018, 1);
  t.fillTriangle(tx - 30, ty - 182, tx + 30, ty - 182, tx, ty - 222);
  t.lineStyle(2, 0x2c2018, 1);
  t.lineBetween(tx, ty - 222, tx, ty - 252);
  const win = scene.add.rectangle(tx, ty - 110, 12, 18, 0xffd36a).setDepth(-15);
  const glow = scene.add.circle(tx, ty - 110, 14, 0xffc040, 0.3).setDepth(-15).setBlendMode(Phaser.BlendModes.ADD);
  const flag = scene.add.triangle(tx + 1, ty - 252, 0, 0, 26, 6, 0, 12, 0xff9f43).setOrigin(0, 0).setDepth(-15);
  if (!still) {
    scene.tweens.add({ targets: [win, glow], alpha: 0.7, duration: 900, yoyo: true, repeat: -1, ease: 'Sine.easeInOut' });
    scene.tweens.add({ targets: flag, scaleX: 0.75, duration: 500, yoyo: true, repeat: -1, ease: 'Sine.easeInOut' });
  }

  // drifting fireflies over the meadow
  for (let i = 0; i < 26; i++) {
    const dot = scene.add.image(Phaser.Math.Between(0, w), Phaser.Math.Between(330, h - 20), 'dot').setTint(0xfff3a0).setScale(0.35).setAlpha(0.8).setBlendMode(Phaser.BlendModes.ADD);
    if (still) continue;
    scene.tweens.add({
      targets: dot,
      y: dot.y - Phaser.Math.Between(30, 80),
      x: dot.x + Phaser.Math.Between(-40, 40),
      alpha: 0.15,
      duration: Phaser.Math.Between(1800, 3600),
      yoyo: true,
      repeat: -1,
      ease: 'Sine.easeInOut',
    });
  }
}
