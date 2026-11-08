import Phaser from 'phaser';

/** Signature bursts for each hero's active skill, layered on top of the shared ring/quake effect. */

const ADD = Phaser.BlendModes.ADD;
type Pos = { x: number; y: number };

function kill(scene: Phaser.Scene, o: Phaser.GameObjects.GameObject, props: object, duration: number, delay = 0, ease = 'Quad.easeOut'): void {
  scene.tweens.add({ targets: o, ...props, duration, delay, ease, onComplete: () => o.destroy() });
}

/** Bramble's Earthshake: jagged cracks race out and chunks of rock hop up. */
function earthshake(scene: Phaser.Scene, p: Pos, r: number): void {
  const g = scene.add.graphics().setDepth(7);
  g.lineStyle(4, 0x24170a, 0.9);
  for (let i = 0; i < 7; i++) {
    let a = (i / 7) * Math.PI * 2 + Math.random() * 0.4;
    let x = p.x, y = p.y;
    g.beginPath();
    g.moveTo(x, y);
    for (let s = 0; s < 4; s++) {
      a += (Math.random() - 0.5) * 0.8;
      x += Math.cos(a) * r * 0.22;
      y += Math.sin(a) * r * 0.13;
      g.lineTo(x, y);
    }
    g.strokePath();
  }
  g.setScale(0.2);
  g.setPosition(p.x * 0.8, p.y * 0.8); // scale about the hero: offset so (p) stays put
  scene.tweens.add({ targets: g, scale: 1, x: 0, y: 0, duration: 180, ease: 'Quad.easeOut' });
  kill(scene, g, { alpha: 0 }, 900, 900);
  for (let i = 0; i < 6; i++) {
    const a = Math.random() * Math.PI * 2, d = r * (0.3 + Math.random() * 0.6);
    const rx = p.x + Math.cos(a) * d, ry = p.y + Math.sin(a) * d * 0.55;
    const rock = scene.add.polygon(rx, ry, [0, 0, 8, -3, 12, 4, 6, 9, -1, 6], 0x8a7a64).setDepth(2402);
    scene.tweens.add({ targets: rock, y: ry - 22 - Math.random() * 12, duration: 200, yoyo: true, ease: 'Quad.easeOut' });
    kill(scene, rock, { alpha: 0, angle: 90 }, 300, 420);
  }
}

/** Feather whirl spiralling up around the hero (Fen's Feather Storm). */
function featherStorm(scene: Phaser.Scene, p: Pos, color: number): void {
  for (let i = 0; i < 14; i++) {
    const a = (i / 14) * Math.PI * 2;
    const f = scene.add.ellipse(p.x + Math.cos(a) * 18, p.y + Math.sin(a) * 9, 12, 5, i % 2 ? color : 0xf4efe4).setDepth(2402).setRotation(a);
    kill(scene, f, { x: p.x + Math.cos(a + 2) * 60, y: p.y + Math.sin(a + 2) * 30 - 60, rotation: a + 5, alpha: 0 }, 750 + i * 15);
  }
  for (let i = 0; i < 4; i++) {
    const gust = scene.add.arc(p.x, p.y - 20, 30 + i * 10, 200 + i * 30, 300 + i * 30, false, 0xffffff, 0).setStrokeStyle(2, 0xffffff, 0.6).setDepth(2401);
    kill(scene, gust, { scale: 1.6, alpha: 0, angle: 120 }, 500, i * 60);
  }
}

/** Foxfire tongues licking up all around the ring (Ember's Foxfire Ring). */
function foxfire(scene: Phaser.Scene, p: Pos, r: number, color: number): void {
  const glow = scene.add.ellipse(p.x, p.y, r * 2, r * 1.1, color, 0.25).setDepth(7).setBlendMode(ADD);
  kill(scene, glow, { alpha: 0 }, 700);
  for (let i = 0; i < 16; i++) {
    const a = (i / 16) * Math.PI * 2;
    const fx = p.x + Math.cos(a) * r * 0.85, fy = p.y + Math.sin(a) * r * 0.5;
    const flame = scene.add.triangle(fx, fy, -6, 0, 6, 0, 0, -22, i % 2 ? color : 0xffe08a, 0.9).setOrigin(0.5, 1).setDepth(2401 + fy / 10000).setBlendMode(ADD).setScale(1, 0.2);
    scene.tweens.add({ targets: flame, scaleY: 1.2, duration: 160, delay: i * 18, yoyo: true, hold: 120, ease: 'Sine.easeOut' });
    kill(scene, flame, { alpha: 0, y: fy - 10 }, 260, 420 + i * 18);
  }
}

/** Slow, soft ripples and drifting moon-crescents (Wren's Hush). */
function hush(scene: Phaser.Scene, p: Pos, r: number, color: number): void {
  for (let i = 0; i < 3; i++) {
    const w = scene.add.ellipse(p.x, p.y, r * 2, r * 1.1, color, 0).setStrokeStyle(2, 0xeaf2ff, 0.8).setDepth(2401).setScale(0.15);
    kill(scene, w, { scale: 1, alpha: 0 }, 900, i * 220, 'Sine.easeOut');
  }
  for (let i = 0; i < 5; i++) {
    const c = scene.add.container(p.x + (Math.random() - 0.5) * r, p.y - 10).setDepth(2402);
    c.add(scene.add.circle(0, 0, 5, 0xeaf2ff, 0.95));
    c.add(scene.add.circle(2.5, -1.5, 4.4, color, 1));
    kill(scene, c, { y: p.y - 60 - Math.random() * 30, alpha: 0 }, 1400, i * 90, 'Sine.easeOut');
  }
}

/** A column of green light with motes spiralling up (Sorrel's Second Wind). */
function secondWind(scene: Phaser.Scene, p: Pos, r: number): void {
  // grow, then fade (chained: two overlapping tweens on the same scale props fight each other)
  const col = scene.add.rectangle(p.x, p.y, 34, 140, 0xe0ffc8, 0.55).setOrigin(0.5, 1).setDepth(2400).setBlendMode(ADD).setScale(0.3, 0.05);
  scene.tweens.add({
    targets: col, scaleX: 1, scaleY: 1, duration: 220, ease: 'Quad.easeOut',
    onComplete: () => kill(scene, col, { alpha: 0, scaleX: 0.2 }, 500, 160),
  });
  for (let i = 0; i < 12; i++) {
    const a = (i / 12) * Math.PI * 2;
    const m = scene.add.circle(p.x + Math.cos(a) * r * 0.6, p.y + Math.sin(a) * r * 0.35, 3, 0xd8ffb0, 1).setDepth(2402).setBlendMode(ADD);
    kill(scene, m, { x: p.x + Math.cos(a + 2.5) * 10, y: p.y - 90 - i * 3, alpha: 0 }, 900, i * 25, 'Sine.easeIn');
  }
}

/** Dreamy purple stars and bubbles popping out (Hazel's Dream Darts). */
function dreamDarts(scene: Phaser.Scene, p: Pos, color: number): void {
  for (let i = 0; i < 8; i++) {
    const a = (i / 8) * Math.PI * 2;
    const st = scene.add.star(p.x, p.y - 26, 4, 2, 6, i % 2 ? color : 0xffe8ff).setDepth(2402).setBlendMode(ADD);
    kill(scene, st, { x: p.x + Math.cos(a) * 46, y: p.y - 26 + Math.sin(a) * 30, angle: 180, alpha: 0, scale: 0.5 }, 600);
  }
  for (let i = 0; i < 5; i++) {
    const b = scene.add.circle(p.x + (Math.random() - 0.5) * 40, p.y - 10, 4 + Math.random() * 4, color, 0.15).setStrokeStyle(1.5, 0xffe8ff, 0.8).setDepth(2402);
    kill(scene, b, { y: b.y - 50 - Math.random() * 30, scale: 1.5, alpha: 0 }, 1200, i * 80, 'Sine.easeOut');
  }
}

export function heroSignature(scene: Phaser.Scene, heroId: string, p: Pos, radius: number, color: number, low: boolean): void {
  if (low) return;
  switch (heroId) {
    case 'bramble': earthshake(scene, p, radius); break;
    case 'fen': featherStorm(scene, p, color); break;
    case 'ember': foxfire(scene, p, radius, color); break;
    case 'wren': hush(scene, p, radius, color); break;
    case 'sorrel': secondWind(scene, p, radius); break;
    case 'hazel': dreamDarts(scene, p, color); break;
  }
}

/** A one-off "ready!" ping on the skill button. */
export function readyPing(scene: Phaser.Scene, x: number, y: number, color: number): void {
  const r = scene.add.circle(x, y, 36, color, 0).setStrokeStyle(4, 0xffe27a, 1).setDepth(3003);
  kill(scene, r, { scale: 1.6, alpha: 0 }, 500);
}
