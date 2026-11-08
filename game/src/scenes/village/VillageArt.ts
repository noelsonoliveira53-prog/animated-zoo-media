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
    const t = addTree(scene, x, y, s, rnd.pick([0x2f6a30, 0x3a7a34, 0x2a5f2c]));
    trees.push(t);
  }
  if (!motion.reduced && !motion.lowFx) {
    for (const t of trees) {
      scene.tweens.add({ targets: t, angle: { from: -1.6, to: 1.6 }, duration: rnd.between(1800, 2800), yoyo: true, repeat: -1, ease: 'Sine.easeInOut', delay: rnd.between(0, 1500) });
    }
  }
}

/** One tree with a shadow, a trunk and a two-tone canopy; returns the canopy graphics (sway it by tweening `angle`). */
export function addTree(scene: Phaser.Scene, x: number, y: number, s: number, leaf: number, light = 0x6fae4c): Phaser.GameObjects.Graphics {
  scene.add.ellipse(x + 6 * s, y + 4, 34 * s, 12 * s, 0x000000, 0.22).setDepth(-9);
  const t = scene.add.graphics({ x, y }).setDepth(-8 + y / 10000);
  t.fillStyle(0x6b4a2a, 1);
  t.fillRect(-3 * s, -14 * s, 6 * s, 14 * s);
  t.fillStyle(leaf, 1);
  t.fillCircle(0, -26 * s, 17 * s);
  t.fillCircle(-10 * s, -18 * s, 11 * s);
  t.fillCircle(10 * s, -19 * s, 11 * s);
  t.fillStyle(light, 0.55);
  t.fillCircle(-5 * s, -31 * s, 8 * s);
  return t;
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

export interface LifeSpot { x: number; y: number; type: string; depth: number }

/**
 * Village life: a few villagers stroll between buildings and little carts trundle resources from mines and sap
 * wells to the vault or Grove Hall. `spots` is called each time so moved or new buildings are used. Each walker is
 * a small container destroyed when its trip ends; at most 5 villagers and 2 carts are out at once.
 */
export function startVillageLife(scene: Phaser.Scene, spots: () => LifeSpot[], depthAt: (y: number) => number): Phaser.Time.TimerEvent | null {
  if (motion.reduced || motion.lowFx) return null;
  let walkers = 0;
  let carts = 0;
  const coats = [0xc8604a, 0x4a7ac8, 0xd8a83a, 0x6aae42, 0x9a6ac8];
  const trip = (o: Phaser.GameObjects.Container, from: LifeSpot, to: LifeSpot, speed: number, k: number, done: () => void) => {
    // an L-shaped route along the grid: across first, then up or down
    const mid = { x: to.x, y: from.y };
    const leg = (a: { x: number; y: number }, b: { x: number; y: number }, next: () => void) => {
      const d = Math.hypot(b.x - a.x, b.y - a.y);
      if (b.x !== a.x) o.setScale(b.x < a.x ? -k : k, k); // face the way it walks, at its display size
      scene.tweens.add({
        targets: o, x: b.x, y: b.y, duration: Math.max(200, (d / speed) * 1000),
        onUpdate: () => o.active && o.setDepth(depthAt(o.y)),
        onComplete: next,
      });
    };
    leg(from, mid, () => leg(mid, to, () => {
      scene.tweens.add({ targets: o, alpha: 0, duration: 250, onComplete: () => { o.destroy(); done(); } });
    }));
  };
  const villager = () => {
    const all = spots();
    if (all.length < 2 || walkers >= 5) return;
    const a = all[Math.floor(Math.random() * all.length)];
    let b = all[Math.floor(Math.random() * all.length)];
    if (b === a) b = all[(all.indexOf(a) + 1) % all.length];
    const v = scene.add.container(a.x, a.y).setAlpha(0);
    const body = scene.add.container(0, 0);
    body.add(scene.add.ellipse(0, 1, 10, 4, 0x000000, 0.25));
    body.add(scene.add.ellipse(0, -5, 8, 10, coats[Math.floor(Math.random() * coats.length)]));
    body.add(scene.add.circle(0, -12, 4, 0xa07850));
    body.add(scene.add.circle(-2.5, -15, 1.6, 0xa07850));
    body.add(scene.add.circle(2.5, -15, 1.6, 0xa07850));
    body.add(scene.add.circle(1.6, -12.5, 0.8, 0x111111));
    v.add(body);
    scene.tweens.add({ targets: v, alpha: 1, duration: 250 });
    scene.tweens.add({ targets: body, y: -2, duration: 160, yoyo: true, repeat: -1 }); // a stepping bob
    walkers++;
    v.setScale(1.8);
    trip(v, a, b, 34, 1.8, () => walkers--);
  };
  const cart = () => {
    const all = spots();
    const sources = all.filter((s) => s.type === 'coinmine' || s.type === 'sapwell');
    const sinks = all.filter((s) => s.type === 'vault' || s.type === 'townhall');
    if (!sources.length || !sinks.length || carts >= 2) return;
    const a = sources[Math.floor(Math.random() * sources.length)];
    const b = sinks[Math.floor(Math.random() * sinks.length)];
    const c = scene.add.container(a.x, a.y).setAlpha(0);
    c.add(scene.add.ellipse(0, 2, 22, 6, 0x000000, 0.25));
    c.add(scene.add.rectangle(0, -5, 18, 9, 0x8a5a32).setStrokeStyle(1, 0x3a2a18));
    const load = a.type === 'coinmine' ? 0xffd23c : 0x9be86a;
    c.add(scene.add.circle(-4, -11, 3, load));
    c.add(scene.add.circle(3, -11, 3, load));
    const w1 = scene.add.circle(-6, 0, 3.2, 0x3a2a18);
    const w2 = scene.add.circle(6, 0, 3.2, 0x3a2a18);
    c.add([w1, w2]);
    // the pusher: a villager walking behind the cart
    c.add(scene.add.ellipse(-15, -5, 7, 9, 0x6aae42));
    c.add(scene.add.circle(-15, -11.5, 3.5, 0xa07850));
    scene.tweens.add({ targets: c, alpha: 1, duration: 250 });
    scene.tweens.add({ targets: [w1, w2], scaleY: 0.8, duration: 120, yoyo: true, repeat: -1 }); // a wobbly wheel
    carts++;
    c.setScale(1.6);
    trip(c, a, b, 26, 1.6, () => carts--);
  };
  for (let i = 0; i < 2; i++) villager();
  return scene.time.addEvent({ delay: 2600, loop: true, callback: () => (Math.random() < 0.35 ? cart() : villager()) });
}

/** Where a building's windows (or door lamp) sit, as fractions of its footprint, for the evening glow. */
export const WINDOW_SPOTS: Record<string, { fx: number; fy: number }[]> = {
  townhall: [{ fx: 0.5, fy: 0.72 }],
  builderhut: [{ fx: 0.5, fy: 0.68 }],
  barracks: [{ fx: 0.5, fy: 0.66 }],
  workshop: [{ fx: 0.36, fy: 0.62 }, { fx: 0.64, fy: 0.62 }],
  market: [{ fx: 0.5, fy: 0.5 }],
  shrine: [{ fx: 0.5, fy: 0.4 }],
  apiary: [{ fx: 0.5, fy: 0.55 }],
};

/** A warm window glow with a soft flicker; returns the objects so the caller can clear them. */
export function windowGlow(scene: Phaser.Scene, x: number, y: number, depth: number): Phaser.GameObjects.GameObject[] {
  // a warm orange pool of light (normal blend, so it stays orange on pale ground) with a bright lamp at its heart
  const halo = scene.add.circle(x, y, 16, 0xffa040, 0.3).setDepth(depth);
  const inner = scene.add.circle(x, y, 8, 0xffc860, 0.45).setDepth(depth);
  const core = scene.add.circle(x, y, 3.5, 0xffe890, 1).setDepth(depth);
  if (!motion.reduced) scene.tweens.add({ targets: halo, alpha: 0.2, scale: 0.9, duration: 700 + Math.random() * 500, yoyo: true, repeat: -1, ease: 'Sine.easeInOut' });
  return [halo, inner, core];
}
