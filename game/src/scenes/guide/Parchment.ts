import Phaser from 'phaser';

/**
 * An aged parchment page: a torn (deckled) outline, warm stains, darker burnt edges, faint fibres and speckles,
 * and a little curl shadow in each corner. Deterministic, drawn once into one Graphics.
 */
export function drawParchment(scene: Phaser.Scene, x: number, y: number, w: number, h: number): Phaser.GameObjects.Graphics {
  const rnd = new Phaser.Math.RandomDataGenerator(['parchment']);
  const g = scene.add.graphics();
  // torn outline: points walk the rectangle with small jitter
  const pts: Phaser.Types.Math.Vector2Like[] = [];
  const step = 18;
  const j = () => rnd.realInRange(-4, 4);
  for (let px = x; px < x + w; px += step) pts.push({ x: px, y: y + j() });
  for (let py = y; py < y + h; py += step) pts.push({ x: x + w + j(), y: py });
  for (let px = x + w; px > x; px -= step) pts.push({ x: px, y: y + h + j() });
  for (let py = y + h; py > y; py -= step) pts.push({ x: x + j(), y: py });
  // drop shadow
  g.fillStyle(0x000000, 0.3);
  g.fillPoints(pts.map((p) => ({ x: p.x + 6, y: p.y + 8 })), true);
  // burnt rim, then the page
  g.fillStyle(0x8a6a40, 1);
  g.fillPoints(pts, true);
  const inset = (k: number) => pts.map((p) => ({ x: p.x + (p.x < x + w / 2 ? k : -k), y: p.y + (p.y < y + h / 2 ? k : -k) }));
  g.fillStyle(0xcdb98c, 1);
  g.fillPoints(inset(4), true);
  g.fillStyle(0xdccb9f, 1);
  g.fillPoints(inset(10), true);
  g.fillStyle(0xe8dcb8, 1);
  g.fillPoints(inset(18), true);
  // stains
  for (let i = 0; i < 14; i++) {
    g.fillStyle(rnd.pick([0xd8c494, 0xdfcfa4, 0xe2d3a8]), 0.55);
    g.fillEllipse(x + rnd.between(60, w - 60), y + rnd.between(50, h - 50), rnd.between(60, 200), rnd.between(30, 110));
  }
  for (let i = 0; i < 3; i++) {
    // a faint ring left by a mug
    g.lineStyle(3, 0xc4ac7a, 0.25);
    g.strokeEllipse(x + rnd.between(120, w - 120), y + rnd.between(90, h - 90), 70, 64);
  }
  // fibres and speckles
  for (let i = 0; i < 70; i++) {
    const fx = x + rnd.between(24, w - 24), fy = y + rnd.between(24, h - 24);
    g.lineStyle(1, 0xb8a272, 0.35);
    g.lineBetween(fx, fy, fx + rnd.between(-14, 14), fy + rnd.between(-3, 3));
  }
  for (let i = 0; i < 120; i++) {
    g.fillStyle(0x9a8458, rnd.realInRange(0.15, 0.4));
    g.fillCircle(x + rnd.between(20, w - 20), y + rnd.between(20, h - 20), rnd.realInRange(0.6, 1.6));
  }
  // corner curls
  for (const [cx, cy, sx, sy] of [[x, y, 1, 1], [x + w, y, -1, 1], [x, y + h, 1, -1], [x + w, y + h, -1, -1]]) {
    g.fillStyle(0x8a6a40, 0.28);
    g.fillTriangle(cx + sx * 6, cy + sy * 6, cx + sx * 46, cy + sy * 8, cx + sx * 8, cy + sy * 46);
  }
  return g;
}

/** A soft ink-wash disc behind a portrait, with a ground shadow under the creature. */
export function portraitBacking(scene: Phaser.Scene, x: number, y: number, r: number): Phaser.GameObjects.Graphics {
  const g = scene.add.graphics();
  g.fillStyle(0xc8b488, 0.45);
  g.fillCircle(x, y, r);
  g.fillStyle(0xd6c498, 0.5);
  g.fillCircle(x - r * 0.12, y - r * 0.12, r * 0.78);
  g.lineStyle(2, 0xa88c5a, 0.5);
  g.strokeCircle(x, y, r);
  g.fillStyle(0x6a5232, 0.25);
  g.fillEllipse(x, y + r * 0.62, r * 1.1, r * 0.22);
  return g;
}
