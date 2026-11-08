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
