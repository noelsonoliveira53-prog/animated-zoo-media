import Phaser from 'phaser';
import { motion } from '../../ui/motion';
import { addTree } from '../village/VillageArt';

export interface CampBox { x: number; y: number; w: number; h: number }

/** The raid field: murky marsh grass with reeds and puddles, a rutted mud yard, edge trees and torches at the yard's corners. */
export function drawRaidGround(scene: Phaser.Scene, camp: CampBox, gameW: number, gameH: number): void {
  const rnd = new Phaser.Math.RandomDataGenerator(['raid-art']);
  const g = scene.add.graphics().setDepth(-10);
  g.fillStyle(0x3f5a3a, 1);
  g.fillRect(-20, -20, gameW + 40, gameH + 40);
  for (let i = 0; i < 60; i++) {
    g.fillStyle(rnd.pick([0x354f31, 0x4a6642, 0x5a5a3a]), 0.6);
    g.fillEllipse(rnd.between(0, gameW), rnd.between(0, gameH), rnd.between(40, 160), rnd.between(20, 70));
  }
  const inYard = (x: number, y: number) => x > camp.x - 10 && x < camp.x + camp.w + 10 && y > camp.y - 10 && y < camp.y + camp.h + 10;
  // dark marsh puddles with a pale glint
  for (let i = 0; i < 10; i++) {
    const x = rnd.between(10, gameW - 10), y = rnd.between(80, gameH - 90);
    if (inYard(x, y)) continue;
    const pw = rnd.between(40, 90), ph = pw * 0.4;
    g.fillStyle(0x24352a, 0.85);
    g.fillEllipse(x, y, pw, ph);
    g.fillStyle(0x6a8a7a, 0.35);
    g.fillEllipse(x - pw * 0.15, y - ph * 0.15, pw * 0.4, ph * 0.25);
  }
  // reeds and two-tone tufts across the marsh
  for (let i = 0; i < 160; i++) {
    const x = rnd.between(0, gameW), y = rnd.between(70, gameH);
    if (inYard(x, y)) continue;
    g.fillStyle(0x2c4428, 0.9);
    g.fillTriangle(x - 3, y, x - 1, y - 7, x + 1, y);
    g.fillStyle(0x7a9a5a, 0.85);
    g.fillTriangle(x, y, x + 2, y - 8, x + 4, y);
    if (i % 9 === 0) {
      g.lineStyle(2, 0x6a7a3a, 1);
      g.lineBetween(x + 8, y, x + 10, y - 18);
      g.fillStyle(0x6a4a2a, 1);
      g.fillEllipse(x + 10, y - 20, 4, 9); // a cattail head
    }
  }
  // the mud yard: a darker trampled rim, the yard itself, ruts, puddles and pebbles
  g.fillStyle(0x3a3020, 0.45);
  g.fillRoundedRect(camp.x - 12, camp.y - 10, camp.w + 24, camp.h + 22, 48);
  g.fillStyle(0x5a4a32, 0.62);
  g.fillRoundedRect(camp.x, camp.y, camp.w, camp.h, 40);
  g.fillStyle(0x6e5a3e, 0.35);
  for (let i = 0; i < 18; i++) g.fillEllipse(camp.x + rnd.between(30, camp.w - 30), camp.y + rnd.between(30, camp.h - 30), rnd.between(60, 140), rnd.between(24, 50));
  g.lineStyle(3, 0x3e3222, 0.45);
  for (let i = 0; i < 6; i++) {
    const y0 = camp.y + rnd.between(40, camp.h - 40), x0 = camp.x + rnd.between(20, camp.w / 2);
    g.beginPath();
    g.moveTo(x0, y0);
    for (let k = 1; k <= 6; k++) g.lineTo(x0 + k * 40, y0 + Math.sin(k + i) * 6);
    g.strokePath();
  }
  for (let i = 0; i < 6; i++) {
    const x = camp.x + rnd.between(40, camp.w - 40), y = camp.y + rnd.between(40, camp.h - 40);
    g.fillStyle(0x3a2e1e, 0.7);
    g.fillEllipse(x, y, rnd.between(24, 46), rnd.between(10, 16));
    g.fillStyle(0x9a8a6a, 0.3);
    g.fillEllipse(x - 4, y - 2, 10, 3);
  }
  for (let i = 0; i < 40; i++) {
    g.fillStyle(rnd.pick([0x8a7a64, 0x6a5e4c, 0xa89a80]), 0.8);
    g.fillCircle(camp.x + rnd.between(10, camp.w - 10), camp.y + rnd.between(10, camp.h - 10), rnd.between(1, 3));
  }

  // trees along the far left and right edges, outside the deploy action
  const still = motion.reduced || motion.lowFx;
  for (let i = 0; i < 14; i++) {
    const left = i % 2 === 0;
    const x = left ? rnd.between(16, Math.max(20, camp.x - 150)) : rnd.between(Math.min(gameW - 20, camp.x + camp.w + 150), gameW - 16);
    const y = rnd.between(140, gameH - 120);
    const t = addTree(scene, x, y, rnd.realInRange(0.8, 1.15), rnd.pick([0x2a4a2a, 0x34552e, 0x2c4630]), 0x5a7a44);
    if (!still) scene.tweens.add({ targets: t, angle: { from: -1.4, to: 1.4 }, duration: rnd.between(1900, 2900), yoyo: true, repeat: -1, ease: 'Sine.easeInOut', delay: rnd.between(0, 1400) });
  }

  // torches at the yard's four corners with a flickering glow
  const corners = [[camp.x + 6, camp.y + 6], [camp.x + camp.w - 6, camp.y + 6], [camp.x + 6, camp.y + camp.h - 6], [camp.x + camp.w - 6, camp.y + camp.h - 6]];
  for (const [x, y] of corners) {
    const post = scene.add.graphics().setDepth(y);
    post.fillStyle(0x000000, 0.25);
    post.fillEllipse(x + 4, y + 2, 16, 6);
    post.fillStyle(0x5a3e24, 1);
    post.fillRect(x - 3, y - 34, 6, 34);
    post.fillStyle(0x3a2a18, 1);
    post.fillRect(x - 6, y - 38, 12, 6);
    const glow = scene.add.circle(x, y - 44, 26, 0xffa040, 0.22).setDepth(y + 1).setBlendMode(Phaser.BlendModes.ADD);
    const flame = scene.add.triangle(x, y - 38, -6, 0, 6, 0, 0, -16, 0xffc040).setOrigin(0.5, 1).setDepth(y + 1);
    scene.add.triangle(x, y - 38, -3, 0, 3, 0, 0, -9, 0xfff0b0).setOrigin(0.5, 1).setDepth(y + 1);
    if (!still) {
      scene.tweens.add({ targets: flame, scaleY: 0.75, scaleX: 1.1, duration: 140 + rnd.between(0, 60), yoyo: true, repeat: -1 });
      scene.tweens.add({ targets: glow, alpha: 0.12, scale: 0.9, duration: 260 + rnd.between(0, 120), yoyo: true, repeat: -1 });
    }
  }
}

/** Where a squad lands: a dust ring, a puff and (throttled by the caller) a little banner that fades. */
export function deployMark(scene: Phaser.Scene, x: number, y: number, banner: boolean): void {
  const ring = scene.add.ellipse(x, y + 4, 40, 14, 0xd9c39a, 0).setStrokeStyle(3, 0xe8d9b5, 0.85).setDepth(y - 1).setScale(0.3);
  scene.tweens.add({ targets: ring, scale: 1.3, alpha: 0, duration: 380, onComplete: () => ring.destroy() });
  if (!banner || motion.reduced || motion.lowFx) return;
  const flag = scene.add.container(x + 10, y + 2).setDepth(y + 0.5).setScale(1, 0);
  const pole = scene.add.rectangle(0, -14, 2, 28, 0x5a3e24).setOrigin(0.5, 0.5);
  const cloth = scene.add.triangle(1, -26, 0, 0, 14, 4, 0, 9, 0x4a9ad8).setOrigin(0, 0);
  flag.add([pole, cloth]);
  scene.tweens.add({ targets: flag, scaleY: 1, duration: 180, ease: 'Back.easeOut' });
  scene.tweens.add({ targets: cloth, scaleX: 0.7, duration: 260, yoyo: true, repeat: 4 });
  scene.tweens.add({ targets: flag, alpha: 0, delay: 2200, duration: 500, onComplete: () => flag.destroy() });
}

/** A fallen camp building: a heap of stones and broken planks over its footprint, with smoke curling up for a while. */
export function rubble(scene: Phaser.Scene, cx: number, cy: number, size: number, depth: number): void {
  const rnd = new Phaser.Math.RandomDataGenerator([`${cx},${cy}`]);
  const g = scene.add.graphics().setDepth(depth + 0.1).setAlpha(0);
  g.fillStyle(0x000000, 0.25);
  g.fillEllipse(cx + 3, cy + size * 0.18, size * 0.95, size * 0.4);
  for (let i = 0; i < 9; i++) {
    const x = cx + rnd.realInRange(-0.36, 0.36) * size, y = cy + rnd.realInRange(-0.05, 0.22) * size;
    g.fillStyle(rnd.pick([0x8a7a64, 0x6a5e4c, 0x9a8a72]), 1);
    g.fillCircle(x, y, rnd.realInRange(3, 7));
  }
  g.lineStyle(4, 0x6a4a2a, 1);
  for (let i = 0; i < 4; i++) {
    const x = cx + rnd.realInRange(-0.3, 0.3) * size, y = cy + rnd.realInRange(0, 0.18) * size;
    const a = rnd.realInRange(-0.8, 0.8);
    g.lineBetween(x - Math.cos(a) * 10, y - Math.sin(a) * 10, x + Math.cos(a) * 10, y + Math.sin(a) * 10);
  }
  scene.tweens.add({ targets: g, alpha: 1, duration: 260, delay: 120 });
  if (motion.reduced || motion.lowFx) return;
  let n = 0;
  const ev = scene.time.addEvent({
    delay: 260,
    repeat: 18,
    callback: () => {
      n++;
      const p = scene.add.circle(cx + rnd.realInRange(-10, 10), cy, 5, 0x8a8278, 0.5).setDepth(depth + 0.2);
      scene.tweens.add({ targets: p, y: cy - 50 - rnd.between(0, 30), x: p.x + rnd.between(-12, 18), scale: 2.4, alpha: 0, duration: 1600, onComplete: () => p.destroy() });
      if (n > 18) ev.remove();
    },
  });
}

const ADD = Phaser.BlendModes.ADD;

/**
 * A camp defense firing (visual only: the sim has already dealt the damage). Darts streak straight in with a
 * muzzle flash; splash shooters lob a boulder in an arc that lands with a dust ring. `onHit` runs at impact.
 */
export function campShot(scene: Phaser.Scene, from: { x: number; y: number }, to: { x: number; y: number }, splash: number, low: boolean, onHit: () => void): void {
  const top = { x: from.x, y: from.y - 24 };
  if (!low) {
    const flash = scene.add.circle(top.x, top.y, 7, splash ? 0xffb860 : 0xd8ffb0, 0.9).setDepth(5600).setBlendMode(ADD);
    scene.tweens.add({ targets: flash, scale: 1.8, alpha: 0, duration: 140, onComplete: () => flash.destroy() });
  }
  if (!splash) {
    const dart = scene.add.rectangle(top.x, top.y, 12, 2.5, 0xc8f08a).setDepth(5550).setRotation(Math.atan2(to.y - top.y, to.x - top.x));
    scene.tweens.add({
      targets: dart, x: to.x, y: to.y - 8, duration: 140, ease: 'Linear',
      onComplete: () => { dart.destroy(); onHit(); },
    });
    return;
  }
  // splash: an arcing stone
  const stone = scene.add.circle(top.x, top.y, 5, 0x7a6a54).setStrokeStyle(1, 0x3a2a1a).setDepth(5550);
  const dist = Math.hypot(to.x - top.x, to.y - top.y);
  const o = { t: 0 };
  scene.tweens.add({
    targets: o, t: 1, duration: 260 + dist * 0.6, ease: 'Linear',
    onUpdate: () => {
      if (!stone.active) return;
      stone.setPosition(top.x + (to.x - top.x) * o.t, top.y + (to.y - top.y) * o.t - Math.sin(Math.PI * o.t) * Math.min(90, 30 + dist * 0.3));
    },
    onComplete: () => {
      stone.destroy();
      const ring = scene.add.ellipse(to.x, to.y + 2, splash * 2, splash * 0.8, 0xb8a888, 0).setStrokeStyle(4, 0xd8c8a0, 0.8).setDepth(to.y + 1).setScale(0.3);
      scene.tweens.add({ targets: ring, scale: 1, alpha: 0, duration: 320, onComplete: () => ring.destroy() });
      onHit();
    },
  });
}
