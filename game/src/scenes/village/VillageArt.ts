import Phaser from 'phaser';
import { motion } from '../../ui/motion';

/** Buildings that puff chimney smoke, with the chimney's spot as a fraction of the footprint. */
export const SMOKE_SPOTS: Record<string, { fx: number; fy: number }> = {
  townhall: { fx: 0.66, fy: 0.12 },
  barracks: { fx: 0.62, fy: 0.2 },
  workshop: { fx: 0.5, fy: 0.12 },
  builderhut: { fx: 0.66, fy: 0.22 },
  coinmine: { fx: 0.5, fy: 0.22 },
};

export interface GridBox { ox: number; oy: number; w: number; h: number; tile: number; cols: number; rows: number }

/** The village lawn: soft grass with sunlit patches and tufts, a brook at the foot of the grid and swaying trees around it. */
export function drawVillageGround(scene: Phaser.Scene, box: GridBox, gameW: number, gameH: number): void {
  const { ox, oy, w, h, tile, cols, rows } = box;
  const rnd = new Phaser.Math.RandomDataGenerator(['village-art']);
  const g = scene.add.graphics().setDepth(-10);
  g.fillStyle(0x497f36, 1);
  g.fillRect(-20, -20, gameW + 40, gameH + 40);
  // darker meadow blotches outside the lawn
  for (let i = 0; i < 26; i++) {
    g.fillStyle(0x426f30, 0.6);
    g.fillEllipse(rnd.between(0, gameW), rnd.between(0, gameH), rnd.between(80, 180), rnd.between(40, 90));
  }
  // lawn: drop shadow, raised edge, then soft two-tone tiles
  g.fillStyle(0x000000, 0.18);
  g.fillRoundedRect(ox - 12, oy - 8, w + 28, h + 28, 24);
  g.fillStyle(0x3f7a33, 1);
  g.fillRoundedRect(ox - 14, oy - 14, w + 28, h + 28, 24);
  g.fillStyle(0x5f9e45, 1);
  g.fillRoundedRect(ox - 14, oy - 14, w + 28, h + 22, 24);
  for (let c = 0; c < cols; c++) {
    for (let r = 0; r < rows; r++) {
      g.fillStyle((c + r) % 2 ? 0x68a94d : 0x6daf51, 1);
      g.fillRect(ox + c * tile, oy + r * tile, tile, tile);
    }
  }
  // sunlit patches (warm, from the top-left) and shady ones
  for (let i = 0; i < 14; i++) {
    const x = ox + rnd.between(0, w), y = oy + rnd.between(0, h);
    const k = 1 - (x - ox) / w * 0.5 - (y - oy) / h * 0.5;
    g.fillStyle(0xd8f08a, 0.08 + 0.06 * k);
    g.fillEllipse(x, y, rnd.between(90, 200), rnd.between(50, 110));
  }
  // faint tile seams so the grid still reads for placement
  g.lineStyle(1, 0x2f5e26, 0.12);
  for (let c = 1; c < cols; c++) g.lineBetween(ox + c * tile, oy, ox + c * tile, oy + h);
  for (let r = 1; r < rows; r++) g.lineBetween(ox, oy + r * tile, ox + w, oy + r * tile);
  // two-tone grass tufts and a few flowers on the lawn
  for (let i = 0; i < 90; i++) {
    const x = ox + rnd.between(4, w - 4), y = oy + rnd.between(4, h - 4);
    g.fillStyle(0x4f8f3a, 0.9);
    g.fillTriangle(x - 3, y, x - 1, y - 6, x + 1, y);
    g.fillStyle(0x8cc865, 0.9);
    g.fillTriangle(x, y, x + 2, y - 7, x + 4, y);
  }
  for (let i = 0; i < 24; i++) {
    const x = ox + rnd.between(6, w - 6), y = oy + rnd.between(6, h - 6);
    g.fillStyle(rnd.pick([0xffffff, 0xffe27a, 0xf7a8c8]), 0.9);
    g.fillCircle(x, y, 2);
  }
  // a brook below the lawn
  const by = oy + h + 26;
  if (by < gameH + 10) {
    g.fillStyle(0x2f6f8a, 1);
    g.beginPath();
    g.moveTo(-10, by);
    for (let x = -10; x <= gameW + 10; x += 20) g.lineTo(x, by + Math.sin(x / 70) * 5);
    g.lineTo(gameW + 10, gameH + 20);
    g.lineTo(-10, gameH + 20);
    g.closePath();
    g.fillPath();
    g.lineStyle(2, 0xbfe8f2, 0.5);
    for (let x = 30; x < gameW; x += 110) g.lineBetween(x, by + 9 + Math.sin(x / 70) * 5, x + 34, by + 9 + Math.sin((x + 34) / 70) * 5);
  }

  // trees around the lawn: shadow, trunk and a two-tone canopy that sways
  const trees: Phaser.GameObjects.Graphics[] = [];
  for (let i = 0; i < 34; i++) {
    const left = i % 2 === 0;
    const x = left ? rnd.between(14, ox - 30) : rnd.between(ox + w + 30, gameW - 14);
    const y = rnd.between(130, gameH - 60);
    if (x < 10 || x > gameW - 10) continue;
    const s = rnd.realInRange(0.8, 1.25);
    const sh = scene.add.ellipse(x + 6 * s, y + 4, 34 * s, 12 * s, 0x000000, 0.22).setDepth(-9);
    void sh;
    const t = scene.add.graphics({ x, y }).setDepth(-8 + y / 10000);
    t.fillStyle(0x6b4a2a, 1);
    t.fillRect(-3 * s, -14 * s, 6 * s, 14 * s);
    t.fillStyle(rnd.pick([0x2f6a30, 0x3a7a34, 0x2a5f2c]), 1);
    t.fillCircle(0, -26 * s, 17 * s);
    t.fillCircle(-10 * s, -18 * s, 11 * s);
    t.fillCircle(10 * s, -19 * s, 11 * s);
    t.fillStyle(0x6fae4c, 0.55);
    t.fillCircle(-5 * s, -31 * s, 8 * s);
    trees.push(t);
  }
  if (!motion.reduced && !motion.lowFx) {
    for (const t of trees) {
      scene.tweens.add({ targets: t, angle: { from: -1.6, to: 1.6 }, duration: rnd.between(1800, 2800), yoyo: true, repeat: -1, ease: 'Sine.easeInOut', delay: rnd.between(0, 1500) });
    }
  }
}

/** A soft contact shadow under a building footprint (drawn just beneath it). */
export function addBuildingShadow(scene: Phaser.Scene, x: number, y: number, size: number, depth: number): Phaser.GameObjects.Ellipse {
  return scene.add.ellipse(x + size / 2 + 6, y + size - 6, size * 0.95, size * 0.34, 0x000000, 0.2).setDepth(depth - 0.01);
}

/** One puff of chimney smoke rising from (x, y). */
export function puffSmoke(scene: Phaser.Scene, x: number, y: number, depth: number): void {
  const c = scene.add.circle(x, y, 4, 0xeeeae2, 0.7).setDepth(depth + 0.02);
  scene.tweens.add({
    targets: c,
    x: x + 10 + Math.random() * 8,
    y: y - 34 - Math.random() * 10,
    scale: 2.6,
    alpha: 0,
    duration: 1800 + Math.random() * 500,
    ease: 'Sine.easeOut',
    onComplete: () => c.destroy(),
  });
}
