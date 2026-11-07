import Phaser from 'phaser';
import { ENEMIES } from '../data/enemies';
import { TOWERS } from '../data/towers';
import { HEROES } from '../data/heroes';
import { BUILDINGS, type BuildingId } from '../data/buildings';
import { CAMP_BUILDINGS, TROOPS } from '../data/raid';

export const TILE = 46;
import { C } from '../ui/theme';

// Generates every texture in code. No image files are shipped.
export class BootScene extends Phaser.Scene {
  constructor() {
    super('Boot');
  }

  create(): void {
    for (const def of Object.values(ENEMIES)) this.makeEnemy(def.id, def.color, def.radius, !!def.flying);
    for (const def of Object.values(TOWERS)) {
      for (let tier = 0; tier < def.tiers.length; tier++) this.makeTower(def.id, def.color, tier);
      for (const sp of def.specs) this.makeTower(def.id, sp.color, def.tiers.length, `tower_${def.id}_${sp.id}`);
    }
    for (const id of Object.keys(HEROES)) this.makeHero(id);
    for (const def of Object.values(BUILDINGS)) {
      for (let lvl = 1; lvl <= def.levels.length; lvl++) this.makeBuilding(def.id, lvl);
    }
    for (const id of Object.keys(CAMP_BUILDINGS)) this.makeCampBuilding(id);
    for (const id of Object.keys(TROOPS)) this.makeTroop(id);
    this.makeMisc();
    this.scene.start('Menu');
  }

  private g(): Phaser.GameObjects.Graphics {
    return this.make.graphics({ x: 0, y: 0 }, false);
  }

  private eyes(g: Phaser.GameObjects.Graphics, cx: number, cy: number, r: number, gap: number): void {
    g.fillStyle(0xffffff, 1);
    g.fillCircle(cx - gap, cy, r);
    g.fillCircle(cx + gap, cy, r);
    g.fillStyle(0x111111, 1);
    g.fillCircle(cx - gap + r * 0.3, cy + r * 0.15, r * 0.55);
    g.fillCircle(cx + gap + r * 0.3, cy + r * 0.15, r * 0.55);
  }

  private makeEnemy(id: string, color: number, radius: number, flying: boolean): void {
    const g = this.g();
    const s = Math.ceil(radius * 3 + 12);
    const cx = s / 2;
    const cy = s / 2 + 2;
    const shade = Phaser.Display.Color.IntegerToColor(color).darken(25).color;
    const light = Phaser.Display.Color.IntegerToColor(color).lighten(20).color;
    // soft ground shadow (flyers get a separate shadow drawn on the ground by the scene)
    if (!flying) {
      g.fillStyle(0x000000, 0.25);
      g.fillEllipse(cx, cy + radius * 0.85, radius * 1.8, radius * 0.6);
    }
    g.lineStyle(3, C.ink, 1);
    const r = radius;
    switch (id) {
      case 'gloomwing':
      case 'gnat': {
        const wing = id === 'gnat' ? 0xe8f2c0 : 0x8a78c0;
        g.fillStyle(wing, id === 'gnat' ? 0.7 : 1);
        g.lineStyle(2, C.ink, 1);
        g.fillEllipse(cx - r * 1.05, cy - r * 0.3, r * 1.5, r * 1.1);
        g.fillEllipse(cx + r * 1.05, cy - r * 0.3, r * 1.5, r * 1.1);
        g.strokeEllipse(cx - r * 1.05, cy - r * 0.3, r * 1.5, r * 1.1);
        g.strokeEllipse(cx + r * 1.05, cy - r * 0.3, r * 1.5, r * 1.1);
        g.lineStyle(id === 'gnat' ? 2 : 3, C.ink, 1);
        g.fillStyle(color, 1);
        g.fillEllipse(cx, cy, r * 1.2, r * 1.6);
        g.strokeEllipse(cx, cy, r * 1.2, r * 1.6);
        if (id === 'gloomwing') {
          g.fillStyle(shade, 1);
          g.fillTriangle(cx - r * 0.5, cy - r * 0.6, cx - r * 0.2, cy - r * 0.6, cx - r * 0.45, cy - r * 1.1);
          g.fillTriangle(cx + r * 0.5, cy - r * 0.6, cx + r * 0.2, cy - r * 0.6, cx + r * 0.45, cy - r * 1.1);
        }
        g.fillStyle(0xffe066, 1);
        g.fillCircle(cx - r * 0.25, cy - r * 0.2, r * 0.18);
        g.fillCircle(cx + r * 0.25, cy - r * 0.2, r * 0.18);
        break;
      }
      case 'bogmender': {
        // staff with water orb
        g.lineStyle(3, 0x5a3b22, 1);
        g.lineBetween(cx + r * 0.9, cy + r * 0.8, cx + r * 0.9, cy - r * 1.2);
        g.fillStyle(0x6fd8ff, 1);
        g.fillCircle(cx + r * 0.9, cy - r * 1.3, r * 0.35);
        g.lineStyle(2, C.ink, 1);
        g.strokeCircle(cx + r * 0.9, cy - r * 1.3, r * 0.35);
        g.lineStyle(3, C.ink, 1);
        g.fillStyle(color, 1);
        g.fillEllipse(cx, cy + r * 0.1, r * 2, r * 1.6);
        g.strokeEllipse(cx, cy + r * 0.1, r * 2, r * 1.6);
        g.fillStyle(light, 1);
        g.fillEllipse(cx, cy + r * 0.4, r * 1.1, r * 0.7);
        // bulging eyes on top
        g.fillStyle(color, 1);
        g.fillCircle(cx - r * 0.45, cy - r * 0.6, r * 0.38);
        g.fillCircle(cx + r * 0.45, cy - r * 0.6, r * 0.38);
        g.lineStyle(2, C.ink, 1);
        g.strokeCircle(cx - r * 0.45, cy - r * 0.6, r * 0.38);
        g.strokeCircle(cx + r * 0.45, cy - r * 0.6, r * 0.38);
        this.eyes(g, cx, cy - r * 0.6, r * 0.24, r * 0.45);
        // leaf hat
        g.fillStyle(0x2f7a3e, 1);
        g.fillTriangle(cx - r * 0.3, cy - r * 0.85, cx + r * 0.3, cy - r * 0.85, cx, cy - r * 1.45);
        break;
      }
      case 'reedguard': {
        g.fillStyle(color, 1);
        g.fillCircle(cx, cy, r);
        g.strokeCircle(cx, cy, r);
        this.eyes(g, cx - r * 0.15, cy - r * 0.3, r * 0.2, r * 0.28);
        // woven shield
        g.fillStyle(0xd8c27a, 1);
        g.fillRoundedRect(cx + r * 0.1, cy - r * 0.4, r * 1.1, r * 1.4, 5);
        g.lineStyle(2.5, C.ink, 1);
        g.strokeRoundedRect(cx + r * 0.1, cy - r * 0.4, r * 1.1, r * 1.4, 5);
        g.lineStyle(1.5, 0x8a7440, 1);
        for (let i = 1; i < 4; i++) g.lineBetween(cx + r * 0.1, cy - r * 0.4 + i * r * 0.35, cx + r * 1.2, cy - r * 0.4 + i * r * 0.35);
        for (let i = 1; i < 3; i++) g.lineBetween(cx + r * 0.1 + i * r * 0.37, cy - r * 0.4, cx + r * 0.1 + i * r * 0.37, cy + r);
        break;
      }
      case 'splotch': {
        g.fillStyle(color, 1);
        g.fillEllipse(cx, cy + r * 0.3, r * 2.3, r * 1.5);
        g.fillCircle(cx - r * 0.4, cy - r * 0.2, r * 0.7);
        g.fillCircle(cx + r * 0.45, cy - r * 0.1, r * 0.65);
        g.fillCircle(cx, cy - r * 0.5, r * 0.6);
        g.strokeEllipse(cx, cy + r * 0.3, r * 2.3, r * 1.5);
        g.fillStyle(shade, 1);
        g.fillCircle(cx - r * 0.6, cy + r * 0.5, r * 0.2);
        g.fillCircle(cx + r * 0.7, cy + r * 0.3, r * 0.15);
        g.fillStyle(light, 1);
        g.fillCircle(cx - r * 0.3, cy - r * 0.6, r * 0.18);
        this.eyes(g, cx, cy - r * 0.05, r * 0.22, r * 0.35);
        break;
      }
      case 'thornhog': {
        // back spikes
        g.fillStyle(0xe0d0a0, 1);
        g.lineStyle(2, C.ink, 1);
        for (let i = -2; i <= 2; i++) {
          const bx = cx + i * r * 0.32;
          g.fillTriangle(bx - r * 0.18, cy - r * 0.4, bx + r * 0.18, cy - r * 0.4, bx, cy - r * 1.15);
          g.strokeTriangle(bx - r * 0.18, cy - r * 0.4, bx + r * 0.18, cy - r * 0.4, bx, cy - r * 1.15);
        }
        g.lineStyle(3, C.ink, 1);
        g.fillStyle(color, 1);
        g.fillEllipse(cx, cy, r * 2.1, r * 1.5);
        g.strokeEllipse(cx, cy, r * 2.1, r * 1.5);
        g.fillStyle(shade, 1);
        g.fillEllipse(cx + r * 0.85, cy + r * 0.15, r * 0.6, r * 0.5);
        g.fillStyle(0xfff4d6, 1);
        g.fillTriangle(cx + r * 0.75, cy + r * 0.35, cx + r * 0.9, cy + r * 0.35, cx + r * 0.7, cy - r * 0.05);
        this.eyes(g, cx + r * 0.35, cy - r * 0.2, r * 0.15, r * 0.2);
        break;
      }
      case 'wispling': {
        g.fillStyle(color, 0.25);
        g.fillCircle(cx, cy, r * 1.45);
        g.fillStyle(color, 1);
        g.fillCircle(cx, cy, r);
        g.fillTriangle(cx - r * 0.9, cy + r * 0.3, cx + r * 0.9, cy + r * 0.3, cx, cy + r * 1.5);
        g.fillStyle(0xffffff, 0.8);
        g.fillCircle(cx - r * 0.3, cy - r * 0.35, r * 0.25);
        g.fillStyle(0x1d4a5a, 1);
        g.fillCircle(cx - r * 0.3, cy, r * 0.16);
        g.fillCircle(cx + r * 0.3, cy, r * 0.16);
        break;
      }
      case 'bogbrute': {
        g.fillStyle(shade, 1);
        g.fillCircle(cx - r * 0.95, cy + r * 0.25, r * 0.42);
        g.fillCircle(cx + r * 0.95, cy + r * 0.25, r * 0.42);
        g.strokeCircle(cx - r * 0.95, cy + r * 0.25, r * 0.42);
        g.strokeCircle(cx + r * 0.95, cy + r * 0.25, r * 0.42);
        g.fillStyle(color, 1);
        g.fillRoundedRect(cx - r * 0.85, cy - r * 0.9, r * 1.7, r * 1.9, r * 0.6);
        g.strokeRoundedRect(cx - r * 0.85, cy - r * 0.9, r * 1.7, r * 1.9, r * 0.6);
        g.fillStyle(0x7a8a5a, 1);
        g.fillCircle(cx - r * 0.4, cy + r * 0.5, r * 0.15);
        g.fillCircle(cx + r * 0.3, cy + r * 0.2, r * 0.12);
        this.eyes(g, cx, cy - r * 0.4, r * 0.17, r * 0.3);
        g.lineStyle(3, C.ink, 1);
        g.lineBetween(cx - r * 0.35, cy - r * 0.05, cx + r * 0.35, cy - r * 0.05);
        g.fillStyle(0xfff4d6, 1);
        g.fillTriangle(cx - r * 0.3, cy - r * 0.05, cx - r * 0.15, cy - r * 0.05, cx - r * 0.22, cy - r * 0.3);
        g.fillTriangle(cx + r * 0.3, cy - r * 0.05, cx + r * 0.15, cy - r * 0.05, cx + r * 0.22, cy - r * 0.3);
        break;
      }
      case 'rimewraith': {
        // hooded frost spirit with a wispy tail
        g.fillStyle(color, 0.3);
        g.fillCircle(cx, cy, r * 1.4);
        g.fillStyle(color, 1);
        g.fillTriangle(cx - r, cy - r * 0.2, cx + r, cy - r * 0.2, cx, cy + r * 1.4);
        g.fillCircle(cx, cy - r * 0.3, r * 0.9);
        g.strokeCircle(cx, cy - r * 0.3, r * 0.9);
        g.fillStyle(0x2a4a6a, 1);
        g.fillEllipse(cx, cy - r * 0.2, r * 1.1, r * 0.9);
        g.fillStyle(0xbff4ff, 1);
        g.fillCircle(cx - r * 0.25, cy - r * 0.25, r * 0.14);
        g.fillCircle(cx + r * 0.25, cy - r * 0.25, r * 0.14);
        g.fillStyle(0xffffff, 0.9);
        for (let i = 0; i < 3; i++) g.fillTriangle(cx - r * 0.9 + i * r * 0.6, cy - r * 0.95, cx - r * 0.7 + i * r * 0.6, cy - r * 0.95, cx - r * 0.8 + i * r * 0.6, cy - r * 1.35);
        break;
      }
      case 'cindermole': {
        // stout mole with glowing claws and an ember-speckled coat
        g.fillStyle(color, 1);
        g.fillEllipse(cx, cy + r * 0.1, r * 2, r * 1.6);
        g.strokeEllipse(cx, cy + r * 0.1, r * 2, r * 1.6);
        g.fillStyle(0xff8a3c, 1);
        for (const [ex, ey] of [[-0.5, -0.2], [0.3, -0.4], [-0.1, 0.3], [0.6, 0.2]]) g.fillCircle(cx + ex * r, cy + ey * r, r * 0.09);
        g.fillStyle(0xe8a090, 1);
        g.fillEllipse(cx + r * 0.85, cy + r * 0.2, r * 0.6, r * 0.45);
        g.fillStyle(0xff5d4a, 1);
        g.fillCircle(cx + r * 1.1, cy + r * 0.2, r * 0.13);
        g.lineStyle(2.5, 0xffb84a, 1);
        for (let i = 0; i < 3; i++) g.lineBetween(cx + r * 0.3 + i * 4, cy + r * 0.8, cx + r * 0.4 + i * 4, cy + r * 1.1);
        g.fillStyle(0x111111, 1);
        g.fillCircle(cx + r * 0.45, cy - r * 0.15, r * 0.1);
        break;
      }
      case 'bramblehide': {
        // vine boar: heavy body, tusks, thorn spikes all along the back, green vines wrapped round
        g.lineStyle(2.5, C.ink, 1);
        for (const lx of [-0.55, -0.2, 0.25, 0.6]) g.lineBetween(cx + lx * r, cy + r * 0.35, cx + lx * r, cy + r * 0.95);
        g.fillStyle(0x4a8a3a, 1);
        for (let k = 0; k < 6; k++) {
          const tx = cx - r * 0.85 + k * r * 0.34;
          g.fillTriangle(tx - r * 0.12, cy - r * 0.42, tx + r * 0.12, cy - r * 0.42, tx, cy - r * 0.85);
          g.strokeTriangle(tx - r * 0.12, cy - r * 0.42, tx + r * 0.12, cy - r * 0.42, tx, cy - r * 0.85);
        }
        g.fillStyle(color, 1);
        g.fillEllipse(cx + r * 0.1, cy, r * 1.9, r * 1.1);
        g.strokeEllipse(cx + r * 0.1, cy, r * 1.9, r * 1.1);
        g.lineStyle(3, 0x4a8a3a, 1);
        g.lineBetween(cx - r * 0.3, cy - r * 0.5, cx + r * 0.1, cy + r * 0.5);
        g.lineBetween(cx + r * 0.4, cy - r * 0.5, cx + r * 0.7, cy + r * 0.45);
        g.lineStyle(2.5, C.ink, 1);
        g.fillStyle(color, 1);
        g.fillCircle(cx - r * 0.85, cy + r * 0.05, r * 0.45);
        g.strokeCircle(cx - r * 0.85, cy + r * 0.05, r * 0.45);
        g.fillStyle(0x9a8a6a, 1);
        g.fillEllipse(cx - r * 1.15, cy + r * 0.15, r * 0.3, r * 0.25);
        g.fillStyle(0xf8f0d8, 1);
        g.fillTriangle(cx - r * 1.05, cy + r * 0.3, cx - r * 0.95, cy + r * 0.3, cx - r * 1.1, cy - r * 0.05);
        g.fillStyle(0xff5d4a, 1);
        g.fillCircle(cx - r * 0.95, cy - r * 0.1, r * 0.08);
        break;
      }
      case 'shiftscale': {
        // chameleon: low body, curled tail, dorsal spines, half the hide already turning red, a big swivel eye
        g.lineStyle(2.5, C.ink, 1);
        g.beginPath();
        g.arc(cx + r * 0.95, cy + r * 0.3, r * 0.35, -1.6, 3.2, false);
        g.strokePath();
        for (const lx of [-0.5, 0.4]) g.lineBetween(cx + lx * r, cy + r * 0.3, cx + lx * r - r * 0.15, cy + r * 0.95);
        g.fillStyle(color, 1);
        g.fillEllipse(cx, cy, r * 1.9, r * 1.1);
        g.strokeEllipse(cx, cy, r * 1.9, r * 1.1);
        g.fillStyle(0xe8604a, 1);
        g.fillEllipse(cx + r * 0.35, cy + r * 0.05, r * 0.9, r * 0.8);
        g.fillStyle(0x3a7a2a, 1);
        for (let k = 0; k < 4; k++) g.fillTriangle(cx - r * 0.6 + k * r * 0.4, cy - r * 0.45, cx - r * 0.4 + k * r * 0.4, cy - r * 0.45, cx - r * 0.5 + k * r * 0.4, cy - r * 0.8);
        g.fillStyle(color, 1);
        g.fillCircle(cx - r * 0.85, cy - r * 0.1, r * 0.42);
        g.strokeCircle(cx - r * 0.85, cy - r * 0.1, r * 0.42);
        g.fillStyle(0xffe066, 1);
        g.fillCircle(cx - r * 0.95, cy - r * 0.2, r * 0.2);
        g.fillStyle(0x111111, 1);
        g.fillCircle(cx - r * 1.0, cy - r * 0.2, r * 0.09);
        break;
      }
      case 'idolkeeper': {
        // temple monkey: round body, pale face, long curled tail, holding up a glowing golden idol
        g.lineStyle(2.5, C.ink, 1);
        g.beginPath();
        g.arc(cx + r * 0.8, cy + r * 0.2, r * 0.45, -2.6, 1.6, false);
        g.strokePath();
        g.fillStyle(color, 1);
        g.fillEllipse(cx, cy + r * 0.3, r * 1.3, r * 1.2);
        g.strokeEllipse(cx, cy + r * 0.3, r * 1.3, r * 1.2);
        g.fillCircle(cx - r * 0.1, cy - r * 0.4, r * 0.55);
        g.strokeCircle(cx - r * 0.1, cy - r * 0.4, r * 0.55);
        g.fillStyle(0xe8d0b0, 1);
        g.fillEllipse(cx - r * 0.1, cy - r * 0.3, r * 0.65, r * 0.55);
        g.fillStyle(0x111111, 1);
        g.fillCircle(cx - r * 0.25, cy - r * 0.45, r * 0.07);
        g.fillCircle(cx + r * 0.05, cy - r * 0.45, r * 0.07);
        g.fillStyle(0xffe066, 0.35);
        g.fillCircle(cx - r * 0.75, cy - r * 0.95, r * 0.5);
        g.fillStyle(0xf0c040, 1);
        g.fillRoundedRect(cx - r * 0.95, cy - r * 1.2, r * 0.4, r * 0.55, 3);
        g.strokeRoundedRect(cx - r * 0.95, cy - r * 1.2, r * 0.4, r * 0.55, 3);
        g.fillStyle(0x6a4a1a, 1);
        g.fillCircle(cx - r * 0.82, cy - r * 1.0, r * 0.05);
        g.fillCircle(cx - r * 0.68, cy - r * 1.0, r * 0.05);
        g.lineStyle(2.5, C.ink, 1);
        g.lineBetween(cx - r * 0.55, cy - r * 0.05, cx - r * 0.75, cy - r * 0.65);
        break;
      }
      case 'zephyrax': {
        // storm roc: vast swept wings with feathered tips, pale chest, crested head, hooked beak, lightning in the wings
        g.lineStyle(3, C.ink, 1);
        for (const sx of [-1, 1]) {
          const wing = [
            new Phaser.Math.Vector2(cx + sx * r * 0.3, cy - r * 0.3),
            new Phaser.Math.Vector2(cx + sx * r * 1.0, cy - r * 0.95),
            new Phaser.Math.Vector2(cx + sx * r * 1.42, cy - r * 0.55),
            new Phaser.Math.Vector2(cx + sx * r * 1.32, cy - r * 0.15),
            new Phaser.Math.Vector2(cx + sx * r * 1.46, cy + r * 0.1),
            new Phaser.Math.Vector2(cx + sx * r * 1.3, cy + r * 0.25),
            new Phaser.Math.Vector2(cx + sx * r * 1.25, cy + r * 0.5),
            new Phaser.Math.Vector2(cx + sx * r * 0.35, cy + r * 0.35),
          ];
          g.fillStyle(color, 1);
          g.fillPoints(wing, true);
          g.strokePoints(wing, true);
          g.fillStyle(0x3a5a7a, 1);
          g.fillTriangle(cx + sx * r * 0.9, cy - r * 0.35, cx + sx * r * 1.32, cy - r * 0.4, cx + sx * r * 1.2, cy + r * 0.2);
          g.lineStyle(2.5, 0xffe066, 1);
          g.lineBetween(cx + sx * r * 0.65, cy - r * 0.45, cx + sx * r * 0.85, cy - r * 0.1);
          g.lineBetween(cx + sx * r * 0.85, cy - r * 0.1, cx + sx * r * 0.7, cy - r * 0.05);
          g.lineBetween(cx + sx * r * 0.7, cy - r * 0.05, cx + sx * r * 0.95, cy + r * 0.25);
          g.lineStyle(3, C.ink, 1);
        }
        g.fillStyle(0x5a7a98, 1);
        g.fillTriangle(cx - r * 0.3, cy + r * 0.5, cx + r * 0.3, cy + r * 0.5, cx, cy + r * 1.05);
        g.strokeTriangle(cx - r * 0.3, cy + r * 0.5, cx + r * 0.3, cy + r * 0.5, cx, cy + r * 1.05);
        g.fillStyle(color, 1);
        g.fillEllipse(cx, cy + r * 0.05, r * 0.85, r * 1.15);
        g.strokeEllipse(cx, cy + r * 0.05, r * 0.85, r * 1.15);
        g.fillStyle(0xe8f0f8, 1);
        g.fillEllipse(cx, cy + r * 0.2, r * 0.5, r * 0.7);
        g.fillStyle(0x3a5a7a, 1);
        for (const dx of [-0.18, 0, 0.18]) g.fillTriangle(cx + dx * r - r * 0.07, cy - r * 0.6, cx + dx * r + r * 0.07, cy - r * 0.6, cx + dx * r, cy - r * 0.95);
        g.fillStyle(color, 1);
        g.fillCircle(cx, cy - r * 0.5, r * 0.3);
        g.strokeCircle(cx, cy - r * 0.5, r * 0.3);
        g.fillStyle(0xf0c040, 1);
        g.fillTriangle(cx - r * 0.1, cy - r * 0.42, cx + r * 0.1, cy - r * 0.42, cx, cy - r * 0.15);
        g.strokeTriangle(cx - r * 0.1, cy - r * 0.42, cx + r * 0.1, cy - r * 0.42, cx, cy - r * 0.15);
        g.fillStyle(0xffffff, 1);
        g.fillCircle(cx - r * 0.13, cy - r * 0.55, r * 0.08);
        g.fillCircle(cx + r * 0.13, cy - r * 0.55, r * 0.08);
        g.fillStyle(0x111111, 1);
        g.fillCircle(cx - r * 0.13, cy - r * 0.54, r * 0.04);
        g.fillCircle(cx + r * 0.13, cy - r * 0.54, r * 0.04);
        break;
      }
      case 'kaleidrax': {
        // crystal colossus: blocky faceted body, shoulder spires, glowing violet core
        g.lineStyle(3, C.ink, 1);
        const body = [
          new Phaser.Math.Vector2(cx - r * 0.8, cy + r * 0.9),
          new Phaser.Math.Vector2(cx - r * 1.0, cy - r * 0.1),
          new Phaser.Math.Vector2(cx - r * 0.5, cy - r * 0.8),
          new Phaser.Math.Vector2(cx + r * 0.5, cy - r * 0.8),
          new Phaser.Math.Vector2(cx + r * 1.0, cy - r * 0.1),
          new Phaser.Math.Vector2(cx + r * 0.8, cy + r * 0.9),
        ];
        g.fillStyle(color, 1);
        g.fillPoints(body, true);
        g.strokePoints(body, true);
        for (const s of [-1, 1]) {
          g.fillStyle(0xc0a0f0, 1);
          g.fillTriangle(cx + s * r * 0.55, cy - r * 0.6, cx + s * r * 0.95, cy - r * 0.2, cx + s * r * 0.95, cy - r * 1.4);
          g.strokeTriangle(cx + s * r * 0.55, cy - r * 0.6, cx + s * r * 0.95, cy - r * 0.2, cx + s * r * 0.95, cy - r * 1.4);
        }
        g.fillStyle(0x80e8d0, 1);
        g.fillTriangle(cx - r * 0.2, cy - r * 0.8, cx + r * 0.2, cy - r * 0.8, cx, cy - r * 1.3);
        g.strokeTriangle(cx - r * 0.2, cy - r * 0.8, cx + r * 0.2, cy - r * 0.8, cx, cy - r * 1.3);
        g.fillStyle(0xffffff, 0.5);
        g.fillTriangle(cx - r * 0.7, cy + r * 0.6, cx - r * 0.85, cy - r * 0.05, cx - r * 0.35, cy - r * 0.6);
        g.fillStyle(0x6a4ab8, 1);
        g.fillCircle(cx, cy + r * 0.05, r * 0.28);
        g.fillStyle(0xe8d8ff, 1);
        g.fillCircle(cx - r * 0.07, cy - r * 0.02, r * 0.1);
        g.fillStyle(0x111111, 1);
        g.fillRect(cx - r * 0.42, cy - r * 0.45, r * 0.22, r * 0.08);
        g.fillRect(cx + r * 0.2, cy - r * 0.45, r * 0.22, r * 0.08);
        break;
      }
      case 'glarefly': {
        // glass moth: four broad faceted wings and a bright core
        g.lineStyle(1.5, 0x5a6a9a, 1);
        for (const [s, up] of [[-1, 1], [1, 1], [-1, -1], [1, -1]] as [number, number][]) {
          const wing = [
            new Phaser.Math.Vector2(cx, cy),
            new Phaser.Math.Vector2(cx + s * r * 0.9, cy - up * r * 1.3),
            new Phaser.Math.Vector2(cx + s * r * 1.7, cy - up * r * 0.7),
            new Phaser.Math.Vector2(cx + s * r * 1.0, cy + up * r * 0.05),
          ];
          g.fillStyle(up > 0 ? 0xd8f8ff : 0xf0e0ff, 1);
          g.fillPoints(wing, true);
          g.strokePoints(wing, true);
          g.fillStyle(0xffffff, 0.7);
          g.fillTriangle(cx + s * r * 0.3, cy - up * r * 0.25, cx + s * r * 0.85, cy - up * r * 1.0, cx + s * r * 1.1, cy - up * r * 0.6);
        }
        g.lineStyle(2, C.ink, 1);
        g.fillStyle(color, 1);
        g.fillEllipse(cx, cy, r * 0.6, r * 1.3);
        g.strokeEllipse(cx, cy, r * 0.6, r * 1.3);
        break;
      }
      case 'shardskipper': {
        // crystal hopper: faceted body, long legs, glowing core
        g.lineStyle(2.5, C.ink, 1);
        g.lineBetween(cx - r * 0.3, cy + r * 0.3, cx - r * 0.9, cy + r * 1.0);
        g.lineBetween(cx + r * 0.3, cy + r * 0.3, cx + r * 0.9, cy + r * 1.0);
        g.fillStyle(color, 1);
        g.fillTriangle(cx - r, cy + r * 0.3, cx + r, cy + r * 0.3, cx, cy - r * 1.1);
        g.strokeTriangle(cx - r, cy + r * 0.3, cx + r, cy + r * 0.3, cx, cy - r * 1.1);
        g.fillStyle(0xffffff, 0.6);
        g.fillTriangle(cx - r * 0.3, cy + r * 0.1, cx + r * 0.1, cy + r * 0.1, cx - r * 0.05, cy - r * 0.8);
        g.fillStyle(0x6a4ab8, 1);
        g.fillCircle(cx, cy - r * 0.05, r * 0.22);
        g.fillStyle(0x111111, 1);
        g.fillCircle(cx - r * 0.3, cy - r * 0.35, r * 0.09);
        g.fillCircle(cx + r * 0.3, cy - r * 0.35, r * 0.09);
        break;
      }
      case 'galehound': {
        // lean cliff hound: long low body, swept-back ears, wind streaks trailing behind
        g.lineStyle(2, 0xffffff, 0.8);
        for (let k = 0; k < 3; k++) g.lineBetween(cx + r * 1.0, cy - r * 0.4 + k * r * 0.4, cx + r * 1.7, cy - r * 0.5 + k * r * 0.4);
        g.lineStyle(2.5, C.ink, 1);
        for (const lx of [-0.6, -0.2, 0.3, 0.7]) g.lineBetween(cx + lx * r, cy + r * 0.3, cx + lx * r - r * 0.25, cy + r * 1.0);
        g.fillStyle(color, 1);
        g.fillEllipse(cx + r * 0.1, cy + r * 0.05, r * 1.9, r * 0.9);
        g.strokeEllipse(cx + r * 0.1, cy + r * 0.05, r * 1.9, r * 0.9);
        g.fillCircle(cx - r * 0.85, cy - r * 0.3, r * 0.48);
        g.strokeCircle(cx - r * 0.85, cy - r * 0.3, r * 0.48);
        g.fillStyle(0x6a8aa8, 1);
        g.fillTriangle(cx - r * 0.75, cy - r * 0.65, cx - r * 0.2, cy - r * 0.95, cx - r * 0.5, cy - r * 0.45);
        g.strokeTriangle(cx - r * 0.75, cy - r * 0.65, cx - r * 0.2, cy - r * 0.95, cx - r * 0.5, cy - r * 0.45);
        g.fillStyle(0xffffff, 0.6);
        g.fillEllipse(cx + r * 0.1, cy - r * 0.15, r * 1.1, r * 0.25);
        g.fillStyle(0x111111, 1);
        g.fillCircle(cx - r * 1.0, cy - r * 0.38, r * 0.1);
        g.fillCircle(cx - r * 1.3, cy - r * 0.22, r * 0.08);
        break;
      }
      case 'kitewing': {
        // sky-ray: broad diamond wings, pale belly stripe, a long ribbon tail with tufts
        g.lineStyle(2, C.ink, 1);
        g.lineBetween(cx, cy + r * 0.5, cx + r * 0.25, cy + r * 1.5);
        g.fillStyle(0xffffff, 1);
        g.fillTriangle(cx + r * 0.05, cy + r * 1.0, cx + r * 0.35, cy + r * 0.95, cx + r * 0.2, cy + r * 1.2);
        g.fillTriangle(cx + r * 0.15, cy + r * 1.35, cx + r * 0.45, cy + r * 1.3, cx + r * 0.3, cy + r * 1.55);
        const wing = [
          new Phaser.Math.Vector2(cx, cy - r * 0.9),
          new Phaser.Math.Vector2(cx + r * 1.5, cy + r * 0.05),
          new Phaser.Math.Vector2(cx, cy + r * 0.6),
          new Phaser.Math.Vector2(cx - r * 1.5, cy + r * 0.05),
        ];
        g.fillStyle(color, 1);
        g.fillPoints(wing, true);
        g.strokePoints(wing, true);
        g.fillStyle(0xd8eef8, 1);
        g.fillEllipse(cx, cy - r * 0.05, r * 0.5, r * 1.0);
        g.fillStyle(0x4a7a98, 1);
        g.fillTriangle(cx - r * 1.5, cy + r * 0.05, cx - r * 0.9, cy - r * 0.2, cx - r * 1.0, cy + r * 0.2);
        g.fillTriangle(cx + r * 1.5, cy + r * 0.05, cx + r * 0.9, cy - r * 0.2, cx + r * 1.0, cy + r * 0.2);
        g.fillStyle(0x111111, 1);
        g.fillCircle(cx - r * 0.18, cy - r * 0.45, r * 0.08);
        g.fillCircle(cx + r * 0.18, cy - r * 0.45, r * 0.08);
        break;
      }
      case 'cloudram': {
        // storm-fleece ram: a puffy cloud body, dark face, curled horns, a spark in the fleece
        g.lineStyle(2.5, C.ink, 1);
        for (const lx of [-0.5, 0.5]) g.lineBetween(cx + lx * r, cy + r * 0.5, cx + lx * r, cy + r * 1.05);
        g.fillStyle(color, 1);
        for (const [dx, dy, rr] of [[-0.5, 0.1, 0.55], [0.45, 0.1, 0.55], [0, -0.3, 0.6], [0, 0.35, 0.55], [-0.6, -0.35, 0.4], [0.6, -0.35, 0.4]]) {
          g.fillCircle(cx + dx * r, cy + dy * r, rr * r);
          g.strokeCircle(cx + dx * r, cy + dy * r, rr * r);
        }
        g.fillStyle(color, 1);
        for (const [dx, dy, rr] of [[-0.5, 0.1, 0.5], [0.45, 0.1, 0.5], [0, -0.3, 0.55], [0, 0.35, 0.5], [-0.6, -0.35, 0.35], [0.6, -0.35, 0.35]]) g.fillCircle(cx + dx * r, cy + dy * r, rr * r);
        g.fillStyle(0xb8c4d4, 1);
        g.fillCircle(cx + r * 0.35, cy + r * 0.35, r * 0.3);
        g.fillStyle(0x4a4a5a, 1);
        g.fillEllipse(cx, cy - r * 0.05, r * 0.7, r * 0.85);
        g.strokeEllipse(cx, cy - r * 0.05, r * 0.7, r * 0.85);
        g.lineStyle(4, 0xc8a878, 1);
        for (const sx of [-1, 1]) {
          g.beginPath();
          g.arc(cx + sx * r * 0.5, cy - r * 0.35, r * 0.3, sx > 0 ? -2.2 : -0.9, sx > 0 ? 1.4 : 2.6, sx < 0);
          g.strokePath();
        }
        g.fillStyle(0xffe066, 1);
        g.fillTriangle(cx + r * 0.55, cy - r * 0.95, cx + r * 0.75, cy - r * 0.95, cx + r * 0.6, cy - r * 0.65);
        g.fillStyle(0xffffff, 1);
        g.fillCircle(cx - r * 0.15, cy - r * 0.15, r * 0.1);
        g.fillCircle(cx + r * 0.15, cy - r * 0.15, r * 0.1);
        g.fillStyle(0x111111, 1);
        g.fillCircle(cx - r * 0.15, cy - r * 0.13, r * 0.05);
        g.fillCircle(cx + r * 0.15, cy - r * 0.13, r * 0.05);
        break;
      }
      case 'mirrorback': {
        // polished beetle: a bright reflective shell with a highlight band
        g.fillStyle(shade, 1);
        for (const s of [-1, 1]) for (let k = 0; k < 3; k++) g.fillRect(cx + s * r * 0.85, cy - r * 0.3 + k * r * 0.4, s * r * 0.35, 3);
        g.fillStyle(color, 1);
        g.fillEllipse(cx, cy, r * 1.8, r * 1.5);
        g.strokeEllipse(cx, cy, r * 1.8, r * 1.5);
        g.lineStyle(2, C.ink, 0.8);
        g.lineBetween(cx, cy - r * 0.75, cx, cy + r * 0.75);
        g.fillStyle(0xffffff, 0.8);
        g.fillEllipse(cx - r * 0.35, cy - r * 0.25, r * 0.35, r * 0.8);
        g.fillStyle(0x9ad8f0, 0.6);
        g.fillEllipse(cx + r * 0.35, cy + r * 0.2, r * 0.3, r * 0.6);
        g.fillStyle(0x3a3a4a, 1);
        g.fillEllipse(cx, cy - r * 0.8, r * 0.8, r * 0.4);
        g.fillStyle(0xff5d4a, 1);
        g.fillCircle(cx - r * 0.2, cy - r * 0.85, r * 0.08);
        g.fillCircle(cx + r * 0.2, cy - r * 0.85, r * 0.08);
        break;
      }
      case 'saltjaw': {
        // colossal crab: huge claws, eye stalks, a barnacle-and-coral crusted shell
        g.lineStyle(3, C.ink, 1);
        for (const s of [-1, 1]) for (let k = 0; k < 4; k++) g.lineBetween(cx + s * r * 0.5, cy + r * 0.15 + k * 5, cx + s * r * 1.25, cy + r * 0.45 + k * 7);
        for (const s of [-1, 1]) {
          g.fillStyle(color, 1);
          g.fillEllipse(cx + s * r * 1.05, cy - r * 0.55, r * 0.75, r * 0.55);
          g.strokeEllipse(cx + s * r * 1.05, cy - r * 0.55, r * 0.75, r * 0.55);
          g.fillStyle(shade, 1);
          g.fillTriangle(cx + s * r * 1.2, cy - r * 0.6, cx + s * r * 1.5, cy - r * 1.05, cx + s * r * 1.45, cy - r * 0.45);
          g.strokeTriangle(cx + s * r * 1.2, cy - r * 0.6, cx + s * r * 1.5, cy - r * 1.05, cx + s * r * 1.45, cy - r * 0.45);
        }
        g.fillStyle(color, 1);
        g.fillEllipse(cx, cy, r * 1.9, r * 1.3);
        g.strokeEllipse(cx, cy, r * 1.9, r * 1.3);
        // eye stalks
        g.lineStyle(3, C.ink, 1);
        g.lineBetween(cx - r * 0.25, cy - r * 0.5, cx - r * 0.3, cy - r * 0.85);
        g.lineBetween(cx + r * 0.25, cy - r * 0.5, cx + r * 0.3, cy - r * 0.85);
        g.fillStyle(0xfff0a8, 1);
        g.fillCircle(cx - r * 0.3, cy - r * 0.88, r * 0.1);
        g.fillCircle(cx + r * 0.3, cy - r * 0.88, r * 0.1);
        g.fillStyle(0x111111, 1);
        g.fillCircle(cx - r * 0.3, cy - r * 0.88, r * 0.05);
        g.fillCircle(cx + r * 0.3, cy - r * 0.88, r * 0.05);
        // barnacles + coral crust
        g.lineStyle(1.5, C.ink, 0.8);
        g.fillStyle(0xeee6d6, 1);
        for (const [dx, dy, rr] of [[-0.55, -0.15, 0.14], [-0.15, -0.3, 0.17], [0.3, -0.2, 0.13], [0.6, 0.05, 0.11], [-0.35, 0.2, 0.12], [0.1, 0.15, 0.1]]) {
          g.fillCircle(cx + dx * r, cy + dy * r, r * rr);
          g.strokeCircle(cx + dx * r, cy + dy * r, r * rr);
        }
        g.fillStyle(0xff8a9a, 1);
        for (const dx of [-0.7, 0.45]) g.fillTriangle(cx + dx * r - 4, cy - r * 0.35, cx + dx * r + 4, cy - r * 0.35, cx + dx * r, cy - r * 0.6);
        break;
      }
      case 'reefwarden': {
        // hermit crab: spiral coral shell, little claws, glowing staff-tip of coral
        g.lineStyle(2, C.ink, 1);
        g.fillStyle(0xd8a080, 1);
        g.fillEllipse(cx + r * 0.55, cy + r * 0.55, r * 0.9, r * 0.5);
        g.strokeEllipse(cx + r * 0.55, cy + r * 0.55, r * 0.9, r * 0.5);
        g.fillCircle(cx + r * 0.95, cy + r * 0.25, r * 0.22);
        g.strokeCircle(cx + r * 0.95, cy + r * 0.25, r * 0.22);
        g.lineStyle(3, C.ink, 1);
        g.fillStyle(color, 1);
        g.fillCircle(cx - r * 0.15, cy - r * 0.05, r * 0.95);
        g.strokeCircle(cx - r * 0.15, cy - r * 0.05, r * 0.95);
        g.lineStyle(2, shade, 1);
        g.beginPath();
        g.arc(cx - r * 0.15, cy - r * 0.05, r * 0.6, 0, Math.PI * 1.5);
        g.strokePath();
        g.beginPath();
        g.arc(cx - r * 0.15, cy - r * 0.05, r * 0.3, 0, Math.PI * 1.5);
        g.strokePath();
        g.fillStyle(0xffd0d8, 1);
        for (const [dx, dy] of [[-0.75, -0.75], [-0.35, -1.0], [0.1, -0.95]]) g.fillTriangle(cx + dx * r - 3, cy + dy * r + 4, cx + dx * r + 3, cy + dy * r + 4, cx + dx * r, cy + dy * r - 6);
        g.fillStyle(0x111111, 1);
        g.fillCircle(cx + r * 0.9, cy + r * 0.05, r * 0.08);
        break;
      }
      case 'barnaclad': {
        // crab: claws, legs, a shell heaped with pale barnacles
        g.lineStyle(2.5, C.ink, 1);
        for (const s of [-1, 1]) for (let k = 0; k < 3; k++) g.lineBetween(cx + s * r * 0.6, cy + r * 0.2 + k * 3, cx + s * r * 1.3, cy + r * 0.55 + k * 4);
        g.fillStyle(color, 1);
        for (const s of [-1, 1]) {
          g.fillCircle(cx + s * r * 1.15, cy - r * 0.45, r * 0.38);
          g.strokeCircle(cx + s * r * 1.15, cy - r * 0.45, r * 0.38);
          g.fillStyle(shade, 1);
          g.fillTriangle(cx + s * r * 1.15, cy - r * 0.45, cx + s * r * 1.55, cy - r * 0.75, cx + s * r * 1.45, cy - r * 0.25);
          g.fillStyle(color, 1);
        }
        g.lineStyle(3, C.ink, 1);
        g.fillEllipse(cx, cy, r * 2, r * 1.4);
        g.strokeEllipse(cx, cy, r * 2, r * 1.4);
        g.fillStyle(0xeee6d6, 1);
        g.lineStyle(1.5, C.ink, 0.8);
        for (const [dx, dy, rr] of [[-0.45, -0.25, 0.22], [0.05, -0.4, 0.26], [0.5, -0.15, 0.2], [-0.1, 0.1, 0.18], [0.35, 0.25, 0.15]]) {
          g.fillCircle(cx + dx * r, cy + dy * r, r * rr);
          g.strokeCircle(cx + dx * r, cy + dy * r, r * rr);
        }
        g.fillStyle(0x111111, 1);
        g.fillCircle(cx - r * 0.25, cy + r * 0.45, r * 0.09);
        g.fillCircle(cx + r * 0.25, cy + r * 0.45, r * 0.09);
        break;
      }
      case 'gullwing': {
        // gull: white body, grey swept wings, yellow beak
        g.fillStyle(0xb8c0c8, 1);
        g.lineStyle(2, C.ink, 1);
        g.fillTriangle(cx - r * 0.2, cy - r * 0.1, cx - r * 1.8, cy - r * 0.7, cx - r * 1.1, cy + r * 0.3);
        g.fillTriangle(cx + r * 0.2, cy - r * 0.1, cx + r * 1.8, cy - r * 0.7, cx + r * 1.1, cy + r * 0.3);
        g.strokeTriangle(cx - r * 0.2, cy - r * 0.1, cx - r * 1.8, cy - r * 0.7, cx - r * 1.1, cy + r * 0.3);
        g.strokeTriangle(cx + r * 0.2, cy - r * 0.1, cx + r * 1.8, cy - r * 0.7, cx + r * 1.1, cy + r * 0.3);
        g.fillStyle(0x3a3a3a, 1);
        g.fillTriangle(cx - r * 1.5, cy - r * 0.6, cx - r * 1.8, cy - r * 0.7, cx - r * 1.55, cy - r * 0.35);
        g.fillTriangle(cx + r * 1.5, cy - r * 0.6, cx + r * 1.8, cy - r * 0.7, cx + r * 1.55, cy - r * 0.35);
        g.fillStyle(color, 1);
        g.lineStyle(2.5, C.ink, 1);
        g.fillEllipse(cx, cy, r * 1.3, r * 1.1);
        g.strokeEllipse(cx, cy, r * 1.3, r * 1.1);
        g.fillCircle(cx + r * 0.45, cy - r * 0.45, r * 0.45);
        g.strokeCircle(cx + r * 0.45, cy - r * 0.45, r * 0.45);
        g.fillStyle(0xffc93c, 1);
        g.fillTriangle(cx + r * 0.8, cy - r * 0.5, cx + r * 0.8, cy - r * 0.3, cx + r * 1.25, cy - r * 0.4);
        g.fillStyle(0x111111, 1);
        g.fillCircle(cx + r * 0.55, cy - r * 0.55, r * 0.09);
        break;
      }
      case 'puffcap': {
        // round spotted cap on a stubby stem with little feet; spore puffs around it
        g.fillStyle(0xffd0f0, 0.35);
        for (const [dx, dy] of [[-1.3, -0.6], [1.35, -0.4], [-1.0, -1.3], [1.0, -1.25]]) g.fillCircle(cx + dx * r, cy + dy * r, r * 0.22);
        g.fillStyle(0xf0e2cc, 1);
        g.fillRoundedRect(cx - r * 0.55, cy - r * 0.1, r * 1.1, r * 1.05, 5);
        g.strokeRoundedRect(cx - r * 0.55, cy - r * 0.1, r * 1.1, r * 1.05, 5);
        g.fillStyle(0x5a4a3a, 1);
        g.fillEllipse(cx - r * 0.35, cy + r * 0.98, r * 0.5, r * 0.25);
        g.fillEllipse(cx + r * 0.35, cy + r * 0.98, r * 0.5, r * 0.25);
        g.fillStyle(color, 1);
        g.fillEllipse(cx, cy - r * 0.25, r * 2.1, r * 1.35);
        g.strokeEllipse(cx, cy - r * 0.25, r * 2.1, r * 1.35);
        g.fillStyle(0xfff0f8, 1);
        for (const [dx, dy, rr] of [[-0.55, -0.45, 0.18], [0.1, -0.7, 0.14], [0.6, -0.35, 0.16], [-0.1, -0.2, 0.1]]) g.fillCircle(cx + dx * r, cy + dy * r, r * rr);
        g.fillStyle(0x111111, 1);
        g.fillCircle(cx - r * 0.2, cy + r * 0.35, r * 0.1);
        g.fillCircle(cx + r * 0.2, cy + r * 0.35, r * 0.1);
        break;
      }
      case 'veilstalker': {
        // lanky mist-cat: hooded head, long tail, faint aura
        g.fillStyle(0xc8b8ff, 0.25);
        g.fillCircle(cx, cy, r * 1.5);
        g.lineStyle(3, C.ink, 1);
        g.lineBetween(cx - r * 0.8, cy + r * 0.4, cx - r * 1.5, cy - r * 0.4);
        g.lineStyle(2, C.ink, 1);
        g.fillStyle(color, 1);
        g.fillEllipse(cx, cy + r * 0.3, r * 1.8, r * 1.1);
        g.strokeEllipse(cx, cy + r * 0.3, r * 1.8, r * 1.1);
        g.fillCircle(cx + r * 0.6, cy - r * 0.35, r * 0.7);
        g.strokeCircle(cx + r * 0.6, cy - r * 0.35, r * 0.7);
        g.fillTriangle(cx + r * 0.15, cy - r * 0.7, cx + r * 0.5, cy - r * 0.8, cx + r * 0.2, cy - r * 1.3);
        g.fillTriangle(cx + r * 0.75, cy - r * 0.8, cx + r * 1.1, cy - r * 0.7, cx + r * 1.0, cy - r * 1.3);
        g.fillStyle(0xbff4ff, 1);
        g.fillCircle(cx + r * 0.45, cy - r * 0.4, r * 0.13);
        g.fillCircle(cx + r * 0.85, cy - r * 0.4, r * 0.13);
        break;
      }
      case 'rootrager': {
        // angry stump: bark body, rings on top, root legs, glowing eyes
        g.fillStyle(shade, 1);
        for (const dx of [-0.8, -0.25, 0.3, 0.85]) g.fillTriangle(cx + dx * r - 4, cy + r * 0.6, cx + dx * r + 4, cy + r * 0.6, cx + dx * r * 1.2, cy + r * 1.15);
        g.fillStyle(color, 1);
        g.fillRoundedRect(cx - r, cy - r * 0.7, r * 2, r * 1.5, 6);
        g.strokeRoundedRect(cx - r, cy - r * 0.7, r * 2, r * 1.5, 6);
        g.fillStyle(0xd9b47a, 1);
        g.fillEllipse(cx, cy - r * 0.7, r * 2, r * 0.6);
        g.strokeEllipse(cx, cy - r * 0.7, r * 2, r * 0.6);
        g.lineStyle(1.5, shade, 1);
        g.strokeEllipse(cx, cy - r * 0.7, r * 1.2, r * 0.34);
        g.strokeEllipse(cx, cy - r * 0.7, r * 0.5, r * 0.14);
        g.lineStyle(2, shade, 1);
        g.lineBetween(cx - r * 0.5, cy - r * 0.2, cx - r * 0.5, cy + r * 0.6);
        g.lineBetween(cx + r * 0.6, cy - r * 0.1, cx + r * 0.6, cy + r * 0.5);
        g.fillStyle(0xffb84a, 1);
        g.fillCircle(cx - r * 0.3, cy, r * 0.15);
        g.fillCircle(cx + r * 0.3, cy, r * 0.15);
        g.lineStyle(2.5, C.ink, 1);
        g.lineBetween(cx - r * 0.5, cy - r * 0.25, cx - r * 0.12, cy - r * 0.12);
        g.lineBetween(cx + r * 0.5, cy - r * 0.25, cx + r * 0.12, cy - r * 0.12);
        break;
      }
      case 'emberimp': {
        g.fillStyle(0xffc93c, 0.35);
        g.fillCircle(cx, cy, r * 1.5);
        g.fillStyle(0x8a3a2a, 1);
        g.lineStyle(2, C.ink, 1);
        g.fillTriangle(cx - r * 0.4, cy, cx - r * 1.6, cy - r * 0.8, cx - r * 1.2, cy + r * 0.4);
        g.fillTriangle(cx + r * 0.4, cy, cx + r * 1.6, cy - r * 0.8, cx + r * 1.2, cy + r * 0.4);
        g.strokeTriangle(cx - r * 0.4, cy, cx - r * 1.6, cy - r * 0.8, cx - r * 1.2, cy + r * 0.4);
        g.strokeTriangle(cx + r * 0.4, cy, cx + r * 1.6, cy - r * 0.8, cx + r * 1.2, cy + r * 0.4);
        g.fillStyle(color, 1);
        g.fillCircle(cx, cy, r);
        g.fillTriangle(cx - r * 0.7, cy - r * 0.5, cx + r * 0.7, cy - r * 0.5, cx, cy - r * 1.6);
        g.strokeCircle(cx, cy, r);
        g.fillStyle(0xfff0a8, 1);
        g.fillCircle(cx - r * 0.35, cy - r * 0.1, r * 0.22);
        g.fillCircle(cx + r * 0.35, cy - r * 0.1, r * 0.22);
        break;
      }
      case 'ashhive': {
        g.fillStyle(color, 1);
        g.fillEllipse(cx, cy + r * 0.2, r * 2.2, r * 1.7);
        g.fillCircle(cx, cy - r * 0.4, r * 0.8);
        g.strokeEllipse(cx, cy + r * 0.2, r * 2.2, r * 1.7);
        g.fillStyle(0x5a3f38, 1);
        g.fillEllipse(cx - r * 0.3, cy - r * 0.2, r * 0.9, r * 0.5);
        // glowing holes
        for (const [hx, hy] of [[-0.6, 0.2], [0.1, 0.5], [0.6, 0.0], [-0.1, -0.5], [0.45, 0.6]]) {
          g.fillStyle(0xff8a3c, 1);
          g.fillCircle(cx + hx * r, cy + hy * r, r * 0.16);
          g.fillStyle(0xffe066, 1);
          g.fillCircle(cx + hx * r, cy + hy * r, r * 0.07);
        }
        g.fillStyle(0x111111, 1);
        g.fillCircle(cx - r * 0.25, cy - r * 0.55, r * 0.09);
        g.fillCircle(cx + r * 0.25, cy - r * 0.55, r * 0.09);
        break;
      }
      case 'morrowcap': {
        // colossal mushroom matriarch: wide spotted cap, a ring of baby caps, a wise face on the stem
        g.fillStyle(0xf0e2cc, 1);
        g.fillRoundedRect(cx - r * 0.55, cy - r * 0.15, r * 1.1, r * 1.15, 10);
        g.strokeRoundedRect(cx - r * 0.55, cy - r * 0.15, r * 1.1, r * 1.15, 10);
        g.fillStyle(0xd8c8a8, 1);
        g.fillEllipse(cx, cy - r * 0.05, r * 1.3, r * 0.3);
        g.fillStyle(0x6a5a4a, 1);
        g.fillEllipse(cx - r * 0.4, cy + r * 1.0, r * 0.6, r * 0.25);
        g.fillEllipse(cx + r * 0.4, cy + r * 1.0, r * 0.6, r * 0.25);
        // face
        g.fillStyle(0x111111, 1);
        g.fillCircle(cx - r * 0.22, cy + r * 0.3, r * 0.08);
        g.fillCircle(cx + r * 0.22, cy + r * 0.3, r * 0.08);
        g.lineStyle(2, C.ink, 1);
        g.beginPath();
        g.arc(cx, cy + r * 0.5, r * 0.18, 0.2, Math.PI - 0.2);
        g.strokePath();
        g.lineStyle(3, C.ink, 1);
        // cap
        g.fillStyle(color, 1);
        g.fillEllipse(cx, cy - r * 0.4, r * 2.3, r * 1.3);
        g.strokeEllipse(cx, cy - r * 0.4, r * 2.3, r * 1.3);
        g.fillStyle(0xbff4ff, 0.95);
        for (const [dx, dy, rr] of [[-0.7, -0.5, 0.16], [-0.2, -0.85, 0.12], [0.35, -0.6, 0.18], [0.8, -0.35, 0.12], [-0.4, -0.2, 0.1], [0.1, -0.3, 0.09]]) g.fillCircle(cx + dx * r, cy + dy * r, r * rr);
        // crown of baby caps
        for (const [dx, col] of [[-0.6, 0xb85a8a], [0, 0x5a8ab8], [0.6, 0xb85a8a]] as [number, number][]) {
          g.fillStyle(0xf0e2cc, 1);
          g.fillRect(cx + dx * r - 2, cy - r * 1.15, 4, r * 0.2);
          g.fillStyle(col, 1);
          g.lineStyle(2, C.ink, 1);
          g.fillEllipse(cx + dx * r, cy - r * 1.15, r * 0.42, r * 0.24);
          g.strokeEllipse(cx + dx * r, cy - r * 1.15, r * 0.42, r * 0.24);
        }
        break;
      }
      case 'vulkhar': {
        // coiled ash wyrm: body coils, horned head, glowing magma cracks
        const shade2 = Phaser.Display.Color.IntegerToColor(color).darken(25).color;
        g.fillStyle(shade2, 1);
        g.fillEllipse(cx - r * 0.3, cy + r * 0.45, r * 2.1, r * 1.1);
        g.strokeEllipse(cx - r * 0.3, cy + r * 0.45, r * 2.1, r * 1.1);
        g.fillStyle(color, 1);
        g.fillEllipse(cx, cy + r * 0.05, r * 1.9, r * 1.2);
        g.strokeEllipse(cx, cy + r * 0.05, r * 1.9, r * 1.2);
        g.lineStyle(3, 0xffb84a, 1);
        g.lineBetween(cx - r * 0.7, cy + r * 0.1, cx - r * 0.2, cy + r * 0.3);
        g.lineBetween(cx - r * 0.2, cy + r * 0.3, cx + r * 0.2, cy);
        g.lineBetween(cx - r * 0.9, cy + r * 0.6, cx - r * 0.4, cy + r * 0.75);
        g.lineStyle(3, C.ink, 1);
        // head
        g.fillStyle(color, 1);
        g.fillEllipse(cx + r * 0.65, cy - r * 0.45, r * 1.1, r * 0.85);
        g.strokeEllipse(cx + r * 0.65, cy - r * 0.45, r * 1.1, r * 0.85);
        g.fillStyle(0x3a2a24, 1);
        g.lineStyle(2, C.ink, 1);
        g.fillTriangle(cx + r * 0.35, cy - r * 0.75, cx + r * 0.5, cy - r * 0.8, cx + r * 0.2, cy - r * 1.35);
        g.fillTriangle(cx + r * 0.75, cy - r * 0.8, cx + r * 0.9, cy - r * 0.78, cx + r * 0.85, cy - r * 1.4);
        g.strokeTriangle(cx + r * 0.35, cy - r * 0.75, cx + r * 0.5, cy - r * 0.8, cx + r * 0.2, cy - r * 1.35);
        g.strokeTriangle(cx + r * 0.75, cy - r * 0.8, cx + r * 0.9, cy - r * 0.78, cx + r * 0.85, cy - r * 1.4);
        g.fillStyle(0xffe066, 1);
        g.fillCircle(cx + r * 0.85, cy - r * 0.5, r * 0.12);
        g.fillStyle(0xff5d4a, 1);
        g.fillTriangle(cx + r * 1.15, cy - r * 0.3, cx + r * 1.15, cy - r * 0.2, cx + r * 1.4, cy - r * 0.25);
        break;
      }
      case 'grimtusk': {
        // great white boar with ice tusks and a frosty mane
        g.fillStyle(0xb8ccd8, 1);
        for (let i = -3; i <= 3; i++) {
          const bx = cx + i * r * 0.22;
          g.fillTriangle(bx - r * 0.14, cy - r * 0.5, bx + r * 0.14, cy - r * 0.5, bx, cy - r * (1.05 + (i % 2 ? 0 : 0.15)));
        }
        g.fillStyle(color, 1);
        g.fillEllipse(cx, cy, r * 2.2, r * 1.6);
        g.strokeEllipse(cx, cy, r * 2.2, r * 1.6);
        g.fillStyle(0xc4d6e0, 1);
        g.fillEllipse(cx + r * 0.8, cy + r * 0.15, r * 0.8, r * 0.7);
        g.strokeEllipse(cx + r * 0.8, cy + r * 0.15, r * 0.8, r * 0.7);
        g.fillStyle(0x8a6a6a, 1);
        g.fillEllipse(cx + r * 1.05, cy + r * 0.2, r * 0.3, r * 0.22);
        g.fillStyle(0xbff4ff, 1);
        g.lineStyle(2, C.ink, 1);
        g.fillTriangle(cx + r * 0.7, cy + r * 0.35, cx + r * 0.82, cy + r * 0.35, cx + r * 0.55, cy - r * 0.2);
        g.strokeTriangle(cx + r * 0.7, cy + r * 0.35, cx + r * 0.82, cy + r * 0.35, cx + r * 0.55, cy - r * 0.2);
        g.fillTriangle(cx + r * 1.0, cy + r * 0.35, cx + r * 1.12, cy + r * 0.35, cx + r * 1.3, cy - r * 0.15);
        g.strokeTriangle(cx + r * 1.0, cy + r * 0.35, cx + r * 1.12, cy + r * 0.35, cx + r * 1.3, cy - r * 0.15);
        g.fillStyle(0x6fd8ff, 1);
        g.fillCircle(cx + r * 0.6, cy - r * 0.15, r * 0.1);
        break;
      }
      case 'murkmaw': {
        g.fillStyle(shade, 1);
        g.fillEllipse(cx, cy + r * 0.2, r * 2.2, r * 1.7);
        g.fillStyle(color, 1);
        g.fillEllipse(cx, cy, r * 2.1, r * 1.6);
        g.strokeEllipse(cx, cy, r * 2.1, r * 1.6);
        g.fillStyle(0xc9d08a, 1);
        g.fillEllipse(cx, cy + r * 0.35, r * 1.4, r * 0.7);
        // warts
        g.fillStyle(0x5f8a5a, 1);
        for (const [wx, wy] of [[-0.6, -0.2], [0.7, -0.1], [-0.3, 0.1], [0.4, 0.2], [0.9, 0.3]]) g.fillCircle(cx + wx * r, cy + wy * r, r * 0.09);
        // mouth
        g.lineStyle(3, C.ink, 1);
        g.beginPath();
        g.arc(cx, cy + r * 0.05, r * 0.6, 0.15, Math.PI - 0.15);
        g.strokePath();
        // eyes + reed crown
        g.fillStyle(color, 1);
        g.fillCircle(cx - r * 0.5, cy - r * 0.6, r * 0.3);
        g.fillCircle(cx + r * 0.5, cy - r * 0.6, r * 0.3);
        g.strokeCircle(cx - r * 0.5, cy - r * 0.6, r * 0.3);
        g.strokeCircle(cx + r * 0.5, cy - r * 0.6, r * 0.3);
        g.fillStyle(0xffe066, 1);
        g.fillCircle(cx - r * 0.5, cy - r * 0.6, r * 0.18);
        g.fillCircle(cx + r * 0.5, cy - r * 0.6, r * 0.18);
        g.fillStyle(0x111111, 1);
        g.fillRect(cx - r * 0.53, cy - r * 0.72, r * 0.06, r * 0.24);
        g.fillRect(cx + r * 0.47, cy - r * 0.72, r * 0.06, r * 0.24);
        g.fillStyle(0xb59a4e, 1);
        g.lineStyle(2, C.ink, 1);
        for (let i = -2; i <= 2; i++) {
          const bx = cx + i * r * 0.18;
          g.fillTriangle(bx - r * 0.07, cy - r * 0.8, bx + r * 0.07, cy - r * 0.8, bx, cy - r * (1.2 + (i === 0 ? 0.15 : 0)));
          g.strokeTriangle(bx - r * 0.07, cy - r * 0.8, bx + r * 0.07, cy - r * 0.8, bx, cy - r * (1.2 + (i === 0 ? 0.15 : 0)));
        }
        break;
      }
      case 'skitter': {
        // beetle: oval shell with legs
        g.lineStyle(2, C.ink, 1);
        for (let i = -1; i <= 1; i++) {
          g.lineBetween(cx - radius * 0.6, cy + i * 4, cx - radius * 1.25, cy + i * 6 + 2);
          g.lineBetween(cx + radius * 0.6, cy + i * 4, cx + radius * 1.25, cy + i * 6 + 2);
        }
        g.lineStyle(3, C.ink, 1);
        g.fillStyle(color, 1);
        g.fillEllipse(cx, cy, radius * 1.6, radius * 2);
        g.strokeEllipse(cx, cy, radius * 1.6, radius * 2);
        g.lineBetween(cx, cy - radius * 0.4, cx, cy + radius);
        g.fillStyle(light, 1);
        g.fillCircle(cx - radius * 0.35, cy - radius * 0.1, radius * 0.25);
        this.eyes(g, cx, cy - radius * 0.65, radius * 0.22, radius * 0.3);
        break;
      }
      case 'shellback': {
        g.fillStyle(shade, 1);
        g.fillCircle(cx, cy, radius);
        g.strokeCircle(cx, cy, radius);
        // stone plates
        g.fillStyle(color, 1);
        const plates = [
          [-0.4, -0.35],
          [0.35, -0.4],
          [0, 0.15],
          [-0.5, 0.35],
          [0.5, 0.3],
        ];
        for (const [px, py] of plates) {
          g.fillCircle(cx + px * radius, cy + py * radius, radius * 0.38);
          g.lineStyle(2, C.ink, 0.8);
          g.strokeCircle(cx + px * radius, cy + py * radius, radius * 0.38);
        }
        this.eyes(g, cx, cy - radius * 0.05, radius * 0.17, radius * 0.25);
        break;
      }
      default: {
        // mudling: droopy blob
        g.fillStyle(color, 1);
        g.fillCircle(cx, cy, radius);
        g.fillEllipse(cx, cy + radius * 0.45, radius * 2.2, radius * 1.1);
        g.strokeCircle(cx, cy, radius);
        g.fillStyle(light, 1);
        g.fillCircle(cx - radius * 0.4, cy - radius * 0.45, radius * 0.22);
        g.fillStyle(shade, 1);
        g.fillCircle(cx + radius * 0.5, cy + radius * 0.5, radius * 0.18);
        this.eyes(g, cx, cy - radius * 0.1, radius * 0.25, radius * 0.35);
      }
    }
    g.generateTexture(`enemy_${id}`, s, s);
    g.destroy();
  }

  /** Murkhorde camp buildings for raids (40px tiles). */
  private makeCampBuilding(id: string): void {
    const def = CAMP_BUILDINGS[id];
    const S = def.size * 40;
    const cx = S / 2;
    const cy = S / 2;
    const g = this.g();
    g.fillStyle(0x000000, 0.25);
    g.fillEllipse(cx, cy + S * 0.32, S * 0.9, S * 0.3);
    g.lineStyle(3, C.ink, 1);
    switch (id) {
      case 'totem': {
        g.fillStyle(0x5a4a32, 1);
        g.fillRoundedRect(cx - 22, cy - 40, 44, 84, 10);
        g.strokeRoundedRect(cx - 22, cy - 40, 44, 84, 10);
        for (let i = 0; i < 3; i++) {
          g.fillStyle([0x7a5a3a, 0x4fae7c, 0x8a6440][i], 1);
          g.fillEllipse(cx, cy - 26 + i * 26, 50, 22);
          g.strokeEllipse(cx, cy - 26 + i * 26, 50, 22);
          g.fillStyle(0xffe066, 1);
          g.fillCircle(cx - 9, cy - 28 + i * 26, 4);
          g.fillCircle(cx + 9, cy - 28 + i * 26, 4);
        }
        g.fillStyle(0xb5651d, 1);
        g.fillTriangle(cx - 16, cy - 52, cx + 16, cy - 52, cx, cy - 72);
        break;
      }
      case 'spit': {
        g.fillStyle(0x6a5a3a, 1);
        g.fillRect(cx - 12, cy - 10, 24, 34);
        g.strokeRect(cx - 12, cy - 10, 24, 34);
        g.fillStyle(def.color, 1);
        g.fillEllipse(cx, cy - 16, 40, 30);
        g.strokeEllipse(cx, cy - 16, 40, 30);
        this.eyes(g, cx, cy - 20, 5, 9);
        g.fillStyle(0x2f6a40, 1);
        g.fillEllipse(cx, cy - 6, 14, 6);
        break;
      }
      case 'mortar': {
        g.fillStyle(0x6a6a5a, 1);
        g.fillEllipse(cx, cy + 6, 56, 36);
        g.strokeEllipse(cx, cy + 6, 56, 36);
        g.fillStyle(def.color, 1);
        g.fillRoundedRect(cx - 14, cy - 26, 28, 34, 8);
        g.strokeRoundedRect(cx - 14, cy - 26, 28, 34, 8);
        g.fillStyle(0x2a2420, 1);
        g.fillEllipse(cx, cy - 26, 24, 10);
        break;
      }
      case 'wall': {
        g.clear();
        g.fillStyle(0x000000, 0.25);
        g.fillRect(2, 30, 36, 8);
        g.lineStyle(2, C.ink, 1);
        for (let i = 0; i < 4; i++) {
          const x = 4 + i * 9;
          g.fillStyle(i % 2 ? 0x6a5236 : 0x5a4632, 1);
          g.fillRect(x, 8, 7, 26);
          g.strokeRect(x, 8, 7, 26);
          g.fillStyle(0xd9c8a0, 1);
          g.fillTriangle(x, 8, x + 7, 8, x + 3.5, 1);
        }
        g.lineStyle(3, 0x3a2a1a, 1);
        g.lineBetween(2, 20, 38, 20);
        break;
      }
      case 'pile': {
        g.fillStyle(0x7a5a3a, 1);
        g.fillEllipse(cx, cy + 8, 60, 34);
        g.strokeEllipse(cx, cy + 8, 60, 34);
        for (let i = 0; i < 7; i++) {
          g.fillStyle(i % 2 ? C.gold : 0x9be86a, 1);
          g.fillCircle(cx - 18 + (i % 4) * 12, cy + 2 - Math.floor(i / 4) * 10, 7);
          g.lineStyle(1.5, C.ink, 1);
          g.strokeCircle(cx - 18 + (i % 4) * 12, cy + 2 - Math.floor(i / 4) * 10, 7);
        }
        break;
      }
      default: {
        g.fillStyle(def.color, 1);
        g.fillEllipse(cx, cy + 4, 58, 44);
        g.strokeEllipse(cx, cy + 4, 58, 44);
        g.fillStyle(0x9a7a52, 1);
        g.fillEllipse(cx - 6, cy - 6, 30, 14);
        g.fillStyle(0x2a2420, 1);
        g.fillEllipse(cx, cy + 14, 16, 18);
      }
    }
    g.generateTexture(`camp_${id}`, S, S);
    g.destroy();
  }

  private makeTroop(id: string): void {
    const def = TROOPS[id];
    const g = this.g();
    const w = 30;
    const h = 34;
    g.fillStyle(0x000000, 0.25);
    g.fillEllipse(15, 30, 22, 7);
    g.lineStyle(2.5, C.ink, 1);
    if (def.flying) {
      g.clear();
      g.lineStyle(2.5, C.ink, 1);
      g.fillStyle(0x8a6a40, 1);
      g.fillEllipse(6, 15, 14, 9);
      g.fillEllipse(24, 15, 14, 9);
      g.strokeEllipse(6, 15, 14, 9);
      g.strokeEllipse(24, 15, 14, 9);
    }
    g.fillStyle(def.color, 1);
    g.fillRoundedRect(6, 12, 18, 17, 7);
    g.strokeRoundedRect(6, 12, 18, 17, 7);
    g.fillCircle(15, 10, 8);
    g.strokeCircle(15, 10, 8);
    g.fillStyle(0x111111, 1);
    g.fillCircle(12, 10, 1.6);
    g.fillCircle(18, 10, 1.6);
    if (id === 'brawler') {
      g.fillStyle(0xffffff, 1);
      g.fillRect(13, 2, 4, 10);
      g.fillStyle(0x7a5232, 1);
      g.fillRect(24, 8, 4, 16);
    } else if (id === 'slinger') {
      g.fillStyle(0x8a6440, 1);
      for (let i = 0; i < 4; i++) g.fillTriangle(8 + i * 4, 5, 11 + i * 4, 5, 9.5 + i * 4, 0);
    } else if (id === 'sapper') {
      g.fillStyle(0xfff4d6, 1);
      g.fillRect(13, 13, 4, 4);
      g.fillStyle(0x6a3a1a, 1);
      g.fillEllipse(15, 31, 18, 6);
    } else {
      g.fillStyle(0xffe066, 1);
      g.fillTriangle(13, 12, 17, 12, 15, 16);
    }
    g.generateTexture(`troop_${id}`, w, h);
    g.destroy();
  }

  /** Village buildings in a top-down 3/4 view. Bigger and fancier with each level. */
  private makeBuilding(id: BuildingId, lvl: number): void {
    const def = BUILDINGS[id];
    const S = def.size * TILE;
    const g = this.g();
    const cx = S / 2;
    const cy = S / 2;
    const k = 0.8 + lvl * 0.05; // grows a little per level
    const dark = Phaser.Display.Color.IntegerToColor(def.color).darken(25).color;
    // ground plate
    g.fillStyle(0x000000, 0.18);
    g.fillRoundedRect(4, 8, S - 8, S - 8, 10);
    g.fillStyle(0x8a9a5a, 1);
    g.fillRoundedRect(3, 3, S - 6, S - 8, 10);
    g.lineStyle(2, 0x6a7a44, 1);
    g.strokeRoundedRect(3, 3, S - 6, S - 8, 10);
    g.lineStyle(3, C.ink, 1);
    switch (id) {
      case 'townhall': {
        // giant hollow oak
        g.fillStyle(0x6b4a2b, 1);
        g.fillRoundedRect(cx - 24 * k, cy - 6, 48 * k, 50 * k, 12);
        g.strokeRoundedRect(cx - 24 * k, cy - 6, 48 * k, 50 * k, 12);
        g.fillStyle(0x3b2a1a, 1);
        g.fillEllipse(cx, cy + 30 * k, 20, 26);
        g.fillStyle(C.gold, 1);
        g.fillCircle(cx, cy + 14, 4);
        const leaf = [0x3f7f34, 0x4b8f3a, 0x5fa848];
        for (let i = 0; i < 5 + lvl; i++) {
          const a = (i / (5 + lvl)) * Math.PI * 2;
          g.fillStyle(leaf[i % 3], 1);
          g.fillCircle(cx + Math.cos(a) * 30 * k, cy - 24 + Math.sin(a) * 18 * k, 22 * k);
        }
        g.fillStyle(0x6fbf52, 1);
        g.fillCircle(cx, cy - 30, 26 * k);
        g.lineStyle(2.5, C.ink, 0.8);
        g.strokeCircle(cx, cy - 30, 26 * k);
        // banners per level
        for (let i = 0; i < lvl - 1; i++) {
          const bx = cx - 40 + i * 26;
          g.lineStyle(2, 0x5a3b22, 1);
          g.lineBetween(bx, S - 20, bx, S - 52);
          g.fillStyle(C.gold, 1);
          g.fillTriangle(bx + 1, S - 52, bx + 1, S - 40, bx + 14, S - 46);
        }
        break;
      }
      case 'coinmine': {
        g.fillStyle(0x8a8578, 1);
        g.fillEllipse(cx, cy, 70 * k, 56 * k);
        g.strokeEllipse(cx, cy, 70 * k, 56 * k);
        g.fillStyle(0x2a2420, 1);
        g.fillEllipse(cx, cy + 6, 26, 22);
        g.fillStyle(0x7a5232, 1);
        g.fillRect(cx - 18, cy + 18, 36, 12);
        g.strokeRect(cx - 18, cy + 18, 36, 12);
        g.fillStyle(C.gold, 1);
        for (let i = 0; i < 2 + lvl; i++) g.fillCircle(cx - 12 + (i % 4) * 8, cy + 16 - Math.floor(i / 4) * 5, 4.5);
        break;
      }
      case 'sapwell': {
        g.fillStyle(0x7a5232, 1);
        g.fillEllipse(cx, cy + 4, 56 * k, 40 * k);
        g.strokeEllipse(cx, cy + 4, 56 * k, 40 * k);
        g.fillStyle(0xa8784a, 1);
        g.fillEllipse(cx, cy - 2, 46 * k, 28 * k);
        g.lineStyle(1.5, 0x7a5232, 1);
        g.strokeEllipse(cx, cy - 2, 30 * k, 18 * k);
        g.strokeEllipse(cx, cy - 2, 14 * k, 8 * k);
        g.fillStyle(0x9be86a, 0.35 + lvl * 0.08);
        g.fillCircle(cx + 22, cy + 18, 14);
        g.fillStyle(0xc8ff8a, 1);
        g.fillCircle(cx + 22, cy + 18, 7);
        g.lineStyle(2, C.ink, 1);
        g.strokeCircle(cx + 22, cy + 18, 7);
        break;
      }
      case 'vault': {
        g.fillStyle(0x6a9a48, 1);
        g.fillEllipse(cx, cy, 68 * k, 56 * k);
        g.strokeEllipse(cx, cy, 68 * k, 56 * k);
        g.fillStyle(0x5a5a64, 1);
        g.fillCircle(cx, cy + 4, 16);
        g.strokeCircle(cx, cy + 4, 16);
        g.fillStyle(0x9a9aa4, 1);
        g.fillCircle(cx, cy + 4, 6);
        g.fillStyle(0x9a6a40, 1);
        for (let i = 0; i < lvl; i++) g.fillRect(cx + 18 + (i % 2) * 8, cy + 12 - Math.floor(i / 2) * 9, 9, 8);
        break;
      }
      case 'builderhut': {
        g.fillStyle(0x8a5a32, 1);
        for (let i = 0; i < 5; i++) g.fillRect(cx - 26 + i * 11, cy - 10, 9, 34);
        g.lineStyle(2, C.ink, 1);
        g.strokeRect(cx - 26, cy - 10, 53, 34);
        g.fillStyle(0xb5651d, 1);
        g.fillTriangle(cx - 32, cy - 8, cx + 32, cy - 8, cx, cy - 34);
        g.lineStyle(3, C.ink, 1);
        g.strokeTriangle(cx - 32, cy - 8, cx + 32, cy - 8, cx, cy - 34);
        g.fillStyle(0x3b2a1a, 1);
        g.fillRect(cx - 7, cy + 6, 14, 18);
        break;
      }
      case 'barracks': {
        g.fillStyle(0x9a6a40, 1);
        g.fillRect(cx - 44 * k, cy - 10, 88 * k, 44);
        g.strokeRect(cx - 44 * k, cy - 10, 88 * k, 44);
        g.fillStyle(def.color, 1);
        g.fillTriangle(cx - 52 * k, cy - 8, cx + 52 * k, cy - 8, cx, cy - 46);
        g.strokeTriangle(cx - 52 * k, cy - 8, cx + 52 * k, cy - 8, cx, cy - 46);
        g.fillStyle(0x3b2a1a, 1);
        g.fillRect(cx - 10, cy + 10, 20, 24);
        g.lineStyle(2, 0x5a3b22, 1);
        g.lineBetween(cx + 40, cy + 34, cx + 40, cy - 30);
        g.fillStyle(dark, 1);
        g.fillTriangle(cx + 41, cy - 30, cx + 41, cy - 14, cx + 58, cy - 22);
        break;
      }
      case 'workshop': {
        g.fillStyle(0x7a6a5a, 1);
        g.fillRect(cx - 46 * k, cy - 6, 92 * k, 40);
        g.strokeRect(cx - 46 * k, cy - 6, 92 * k, 40);
        g.fillStyle(def.color, 1);
        g.fillRect(cx - 52 * k, cy - 22, 104 * k, 18);
        g.strokeRect(cx - 52 * k, cy - 22, 104 * k, 18);
        // gear
        g.fillStyle(0xd0c8b8, 1);
        for (let i = 0; i < 8; i++) {
          const a = (i / 8) * Math.PI * 2;
          g.fillRect(cx + Math.cos(a) * 16 - 3, cy - 40 + Math.sin(a) * 16 - 3, 6, 6);
        }
        g.fillCircle(cx, cy - 40, 13);
        g.lineStyle(2, C.ink, 1);
        g.strokeCircle(cx, cy - 40, 13);
        g.fillStyle(0x7a6a5a, 1);
        g.fillCircle(cx, cy - 40, 5);
        for (let i = 0; i < lvl; i++) {
          g.fillStyle(0xb07cff, 1);
          g.fillCircle(cx - 30 + i * 14, cy + 20, 4);
        }
        break;
      }
      case 'wall': {
        g.clear();
        g.fillStyle(0x000000, 0.2);
        g.fillRoundedRect(2, 8, S - 4, S - 8, 8);
        const col = [0x4b8f3a, 0x3f7a6a, 0x5a5a64][lvl - 1] ?? 0x4b8f3a;
        g.fillStyle(col, 1);
        g.fillRoundedRect(2, 2, S - 4, S - 8, 8);
        g.lineStyle(2.5, C.ink, 1);
        g.strokeRoundedRect(2, 2, S - 4, S - 8, 8);
        g.fillStyle(0xffffff, 0.2);
        g.fillCircle(14, 12, 6);
        g.fillStyle(0xe0d0a0, 1);
        for (let i = 0; i < 3; i++) g.fillTriangle(8 + i * 12, 8, 12 + i * 12, 8, 10 + i * 12, 2);
        break;
      }
    }
    g.generateTexture(`bld_${id}_${lvl}`, S, S);
    g.destroy();
  }

  private makeHero(id: string): void {
    const g = this.g();
    const w = 52;
    const h = 60;
    const cx = w / 2;
    const base = h - 6;
    g.fillStyle(0x000000, 0.25);
    g.fillEllipse(cx, base, 34, 10);
    g.lineStyle(3, C.ink, 1);
    if (id === 'fen') {
      // heron: long legs, tall body, long beak, bow
      g.lineStyle(3, 0xe0a040, 1);
      g.lineBetween(cx - 4, base - 2, cx - 3, base - 18);
      g.lineBetween(cx + 4, base - 2, cx + 3, base - 18);
      g.lineStyle(3, C.ink, 1);
      g.fillStyle(0xdde8f0, 1);
      g.fillEllipse(cx, base - 26, 22, 22);
      g.strokeEllipse(cx, base - 26, 22, 22);
      g.fillStyle(0x7fb0d8, 1);
      g.fillEllipse(cx + 3, base - 24, 14, 16);
      g.fillStyle(0xdde8f0, 1);
      g.fillRect(cx - 3, base - 46, 6, 14);
      g.fillCircle(cx, base - 46, 7);
      g.strokeCircle(cx, base - 46, 7);
      g.fillStyle(0xf0b040, 1);
      g.fillTriangle(cx + 5, base - 48, cx + 5, base - 44, cx + 20, base - 46);
      g.fillStyle(0x334455, 1);
      g.fillRect(cx - 7, base - 54, 10, 3);
      g.fillStyle(0x111111, 1);
      g.fillCircle(cx + 2, base - 47, 1.6);
      // bow
      g.lineStyle(2.5, 0x7a5232, 1);
      g.beginPath();
      g.arc(cx - 12, base - 28, 12, -1.2, 1.2);
      g.strokePath();
      g.lineStyle(1, 0xffffff, 0.9);
      g.lineBetween(cx - 7, base - 39, cx - 7, base - 17);
    } else if (id === 'wren') {
      // barn owl: round heart-shaped face, wings folded, scroll satchel
      g.fillStyle(0xb8905a, 1);
      g.fillEllipse(cx, base - 18, 26, 30);
      g.strokeEllipse(cx, base - 18, 26, 30);
      g.fillStyle(0x9a7444, 1);
      g.fillEllipse(cx - 11, base - 18, 8, 22);
      g.fillEllipse(cx + 11, base - 18, 8, 22);
      g.fillStyle(0xd8b880, 1);
      g.fillCircle(cx, base - 38, 13);
      g.strokeCircle(cx, base - 38, 13);
      g.fillStyle(0xfff4e0, 1);
      g.fillEllipse(cx - 5, base - 38, 11, 14);
      g.fillEllipse(cx + 5, base - 38, 11, 14);
      g.fillStyle(0x111111, 1);
      g.fillCircle(cx - 5, base - 39, 2.4);
      g.fillCircle(cx + 5, base - 39, 2.4);
      g.fillStyle(0xe0a040, 1);
      g.fillTriangle(cx - 2, base - 35, cx + 2, base - 35, cx, base - 30);
      // satchel with a scroll
      g.fillStyle(0x7a5232, 1);
      g.fillRoundedRect(cx + 6, base - 20, 12, 10, 3);
      g.lineStyle(2, C.ink, 1);
      g.strokeRoundedRect(cx + 6, base - 20, 12, 10, 3);
      g.fillStyle(0xf0e2cc, 1);
      g.fillRect(cx + 9, base - 26, 6, 8);
      // feet
      g.lineStyle(2.5, 0xe0a040, 1);
      g.lineBetween(cx - 5, base - 4, cx - 5, base);
      g.lineBetween(cx + 5, base - 4, cx + 5, base);
    } else if (id === 'ember') {
      // fox: orange body, big tail, ears, flame in paw
      g.fillStyle(0xff8a3c, 1);
      g.fillEllipse(cx - 13, base - 14, 18, 12);
      g.strokeEllipse(cx - 13, base - 14, 18, 12);
      g.fillStyle(0xffffff, 1);
      g.fillCircle(cx - 20, base - 15, 4);
      g.fillStyle(0x8a4a9a, 1);
      g.fillRoundedRect(cx - 9, base - 30, 18, 26, 7);
      g.strokeRoundedRect(cx - 9, base - 30, 18, 26, 7);
      g.fillStyle(0xff8a3c, 1);
      g.fillCircle(cx, base - 36, 10);
      g.strokeCircle(cx, base - 36, 10);
      g.fillTriangle(cx - 9, base - 40, cx - 3, base - 44, cx - 8, base - 52);
      g.fillTriangle(cx + 9, base - 40, cx + 3, base - 44, cx + 8, base - 52);
      g.fillStyle(0xffffff, 1);
      g.fillEllipse(cx, base - 32, 10, 6);
      g.fillStyle(0x111111, 1);
      g.fillCircle(cx - 4, base - 38, 1.8);
      g.fillCircle(cx + 4, base - 38, 1.8);
      g.fillCircle(cx, base - 33, 1.5);
      g.fillStyle(0xffd23c, 0.5);
      g.fillCircle(cx + 15, base - 26, 8);
      g.fillStyle(0xffe680, 1);
      g.fillCircle(cx + 15, base - 26, 4.5);
    } else {
      // badger knight with bark armor and a wooden sword
      g.fillStyle(0x7a5232, 1);
      g.fillRoundedRect(cx - 12, base - 28, 24, 24, 8);
      g.strokeRoundedRect(cx - 12, base - 28, 24, 24, 8);
      g.fillStyle(0x9a6a40, 1);
      g.fillRect(cx - 10, base - 22, 20, 4);
      g.fillStyle(0x3b3b3b, 1);
      g.fillCircle(cx, base - 36, 12);
      g.strokeCircle(cx, base - 36, 12);
      g.fillStyle(0xffffff, 1);
      g.fillRect(cx - 2.5, base - 48, 5, 18);
      g.fillStyle(0x111111, 1);
      g.fillCircle(cx - 5, base - 36, 2);
      g.fillCircle(cx + 5, base - 36, 2);
      g.fillStyle(0xd9d2c0, 1);
      g.fillRect(cx + 14, base - 46, 4, 26);
      g.fillStyle(0x7a5232, 1);
      g.fillRect(cx + 10, base - 22, 12, 4);
      g.lineStyle(2, C.ink, 1);
      g.strokeRect(cx + 14, base - 46, 4, 26);
      g.fillStyle(C.gold, 1);
      g.fillCircle(cx - 14, base - 18, 8);
      g.lineStyle(2.5, C.ink, 1);
      g.strokeCircle(cx - 14, base - 18, 8);
    }
    g.generateTexture(`hero_${id}`, w, h);
    g.destroy();
  }

  private makeTower(id: string, color: number, tier: number, key?: string): void {
    const g = this.g();
    const w = 72;
    const h = 100; // tall enough for top-tier roofs/orbs (84 used to clip them)
    const cx = w / 2;
    const base = h - 10;
    const dark = Phaser.Display.Color.IntegerToColor(color).darken(30).color;
    const light = Phaser.Display.Color.IntegerToColor(color).lighten(15).color;
    g.fillStyle(0x000000, 0.25);
    g.fillEllipse(cx, base + 2, 60, 16);
    g.lineStyle(3, C.ink, 1);
    if (id === 'boulder') {
      // log-frame catapult on a stone base
      g.fillStyle(0x8a8578, 1);
      g.fillRoundedRect(cx - 26, base - 18, 52, 18, 6);
      g.strokeRoundedRect(cx - 26, base - 18, 52, 18, 6);
      g.fillStyle(0x7a5232, 1);
      g.fillRect(cx - 20, base - 40 - tier * 3, 8, 24 + tier * 3);
      g.fillRect(cx + 12, base - 40 - tier * 3, 8, 24 + tier * 3);
      g.strokeRect(cx - 20, base - 40 - tier * 3, 8, 24 + tier * 3);
      g.strokeRect(cx + 12, base - 40 - tier * 3, 8, 24 + tier * 3);
      // throwing arm
      g.lineStyle(7, 0x5c3b22, 1);
      g.lineBetween(cx - 4, base - 22, cx + 18, base - 58 - tier * 4);
      g.lineStyle(3, C.ink, 1);
      g.fillStyle(color, 1);
      g.fillCircle(cx + 18, base - 60 - tier * 4, 9);
      g.strokeCircle(cx + 18, base - 60 - tier * 4, 9);
      g.fillStyle(0x9a958a, 1);
      g.fillCircle(cx + 18, base - 64 - tier * 4, 6);
      g.fillStyle(dark, 1);
      g.fillRect(cx - 24, base - 44 - tier * 3, 48, 7);
    } else if (id === 'burrow') {
      // grassy mound with a round wooden door and a banner
      g.fillStyle(0x6a9a48, 1);
      g.fillEllipse(cx, base - 16, 64, 40 + tier * 4);
      g.strokeEllipse(cx, base - 16, 64, 40 + tier * 4);
      g.fillStyle(0x7fb35a, 1);
      g.fillEllipse(cx - 8, base - 26, 30, 14);
      g.fillStyle(0x5a3b22, 1);
      g.fillCircle(cx, base - 10, 13);
      g.strokeCircle(cx, base - 10, 13);
      g.fillStyle(0x7a5232, 1);
      g.fillCircle(cx, base - 10, 9);
      g.fillStyle(C.gold, 1);
      g.fillCircle(cx + 5, base - 10, 2);
      g.lineStyle(3, 0x5a3b22, 1);
      g.lineBetween(cx + 20, base - 26, cx + 20, base - 60 - tier * 4);
      g.fillStyle(color, 1);
      g.fillTriangle(cx + 21, base - 60 - tier * 4, cx + 21, base - 44 - tier * 4, cx + 38, base - 52 - tier * 4);
      g.lineStyle(2, C.ink, 1);
      g.strokeTriangle(cx + 21, base - 60 - tier * 4, cx + 21, base - 44 - tier * 4, cx + 38, base - 52 - tier * 4);
    } else if (id === 'glimmer') {
      // stone spire with glowing orb
      const height = 46 + tier * 6;
      g.fillStyle(0x8c8aa8, 1);
      g.fillTriangle(cx - 18, base, cx + 18, base, cx, base - height);
      g.strokeTriangle(cx - 18, base, cx + 18, base, cx, base - height);
      g.fillStyle(0x6d6a8c, 1);
      g.fillTriangle(cx, base, cx + 18, base, cx, base - height);
      g.fillStyle(dark, 1);
      g.fillRect(cx - 4, base - height * 0.55, 8, 10);
      g.fillStyle(color, 0.35);
      g.fillCircle(cx, base - height - 6, 14 + tier * 2);
      g.fillStyle(light, 1);
      g.fillCircle(cx, base - height - 6, 7 + tier);
      g.lineStyle(2, C.ink, 1);
      g.strokeCircle(cx, base - height - 6, 7 + tier);
      g.fillStyle(0xffffff, 0.9);
      g.fillCircle(cx - 2, base - height - 8, 2.5);
    } else {
      // wooden treehouse nest
      const height = 34 + tier * 5;
      g.fillStyle(0x7a5232, 1);
      g.fillRect(cx - 16, base - height, 8, height);
      g.fillRect(cx + 8, base - height, 8, height);
      g.strokeRect(cx - 16, base - height, 8, height);
      g.strokeRect(cx + 8, base - height, 8, height);
      g.fillStyle(0x9a6a40, 1);
      g.fillRect(cx - 24, base - height - 12, 48, 16);
      g.strokeRect(cx - 24, base - height - 12, 48, 16);
      // leafy roof
      g.fillStyle(color, 1);
      g.fillCircle(cx - 14, base - height - 18, 12);
      g.fillCircle(cx + 14, base - height - 18, 12);
      g.fillCircle(cx, base - height - 26, 14);
      g.lineStyle(2, C.ink, 1);
      g.strokeCircle(cx, base - height - 26, 14);
      g.fillStyle(light, 1);
      g.fillCircle(cx - 4, base - height - 30, 5);
      g.fillStyle(dark, 1);
      g.fillCircle(cx + 10, base - height - 16, 4);
    }
    // tier pips
    for (let i = 0; i < tier; i++) {
      g.fillStyle(C.gold, 1);
      g.fillCircle(cx - (tier - 1) * 6 + i * 12, base - 6, 4);
      g.lineStyle(1.5, C.ink, 1);
      g.strokeCircle(cx - (tier - 1) * 6 + i * 12, base - 6, 4);
    }
    if (key) {
      // specialization crest
      g.fillStyle(color, 1);
      g.fillCircle(w - 12, 14, 9);
      g.lineStyle(2.5, C.ink, 1);
      g.strokeCircle(w - 12, 14, 9);
      g.fillStyle(0xffffff, 0.8);
      g.fillCircle(w - 14, 11, 3);
    }
    g.generateTexture(key ?? `tower_${id}_${tier}`, w, h);
    g.destroy();
  }

  private makeMisc(): void {
    let g = this.g();
    // build slot: mossy stone pad
    g.fillStyle(0x000000, 0.2);
    g.fillEllipse(32, 36, 60, 26);
    g.fillStyle(0x9c9480, 1);
    g.fillEllipse(32, 30, 56, 26);
    g.lineStyle(3, C.ink, 1);
    g.strokeEllipse(32, 30, 56, 26);
    g.fillStyle(0xb8b09a, 1);
    g.fillEllipse(32, 27, 40, 14);
    g.fillStyle(0x6fae4a, 1);
    g.fillCircle(14, 34, 5);
    g.fillCircle(48, 24, 4);
    g.generateTexture('slot', 64, 48);
    g.destroy();

    const proj = (key: string, color: number, r: number) => {
      g = this.g();
      g.fillStyle(color, 0.35);
      g.fillCircle(r * 2, r * 2, r * 2);
      g.fillStyle(color, 1);
      g.fillCircle(r * 2, r * 2, r);
      g.fillStyle(0xffffff, 0.9);
      g.fillCircle(r * 2 - r * 0.3, r * 2 - r * 0.3, r * 0.4);
      g.generateTexture(key, r * 4, r * 4);
      g.destroy();
    };
    proj('proj_glimmer', 0xd6a8ff, 5);
    g = this.g();
    g.fillStyle(0x4b3320, 1);
    g.fillRect(0, 2, 14, 3);
    g.fillStyle(0x8fbf4a, 1);
    g.fillTriangle(14, 0, 14, 7, 20, 3.5);
    g.generateTexture('proj_thornbow', 20, 7);
    g.destroy();

    // river rock
    g = this.g();
    g.fillStyle(0x8a8578, 1);
    g.fillCircle(9, 9, 8);
    g.lineStyle(2, C.ink, 1);
    g.strokeCircle(9, 9, 8);
    g.fillStyle(0xb5b0a4, 1);
    g.fillCircle(6, 6, 3);
    g.generateTexture('proj_boulder', 18, 18);
    g.destroy();

    // Badger Warden soldier
    g = this.g();
    g.fillStyle(0x000000, 0.25);
    g.fillEllipse(14, 30, 22, 7);
    g.lineStyle(2.5, C.ink, 1);
    g.fillStyle(0x5d6d7a, 1);
    g.fillRoundedRect(5, 13, 18, 16, 6);
    g.strokeRoundedRect(5, 13, 18, 16, 6);
    g.fillStyle(0x3b3b3b, 1);
    g.fillCircle(14, 11, 9);
    g.strokeCircle(14, 11, 9);
    g.fillStyle(0xffffff, 1);
    g.fillRect(12, 3, 4, 14);
    g.fillStyle(0x111111, 1);
    g.fillCircle(10.5, 11, 1.8);
    g.fillCircle(17.5, 11, 1.8);
    g.fillStyle(0xd9d2c0, 1);
    g.fillRect(23, 8, 3, 18);
    g.fillStyle(0x6f8fa8, 1);
    g.fillCircle(6, 21, 6);
    g.strokeCircle(6, 21, 6);
    g.generateTexture('soldier', 30, 34);
    g.destroy();

    // Ranger (summoned by Grove Call): hedgehog in a green hood
    g = this.g();
    g.fillStyle(0x000000, 0.25);
    g.fillEllipse(14, 30, 22, 7);
    g.lineStyle(2.5, C.ink, 1);
    g.fillStyle(0x4f8a3a, 1);
    g.fillRoundedRect(5, 13, 18, 16, 6);
    g.strokeRoundedRect(5, 13, 18, 16, 6);
    g.fillStyle(0x8a6440, 1);
    for (let i = 0; i < 5; i++) g.fillTriangle(5 + i * 4, 8, 9 + i * 4, 8, 7 + i * 4, 1);
    g.fillStyle(0x6fae4a, 1);
    g.fillCircle(14, 11, 9);
    g.strokeCircle(14, 11, 9);
    g.fillStyle(0xe8c9a0, 1);
    g.fillEllipse(15, 13, 10, 8);
    g.fillStyle(0x111111, 1);
    g.fillCircle(12, 12, 1.6);
    g.fillCircle(18, 12, 1.6);
    g.fillCircle(15, 15, 1.4);
    g.fillStyle(0x7a5232, 1);
    g.fillRect(23, 6, 3, 20);
    g.generateTexture('ranger', 30, 34);
    g.destroy();

    // spell icons
    g = this.g();
    {
      const pts: Phaser.Math.Vector2[] = [];
      for (let i = 0; i < 10; i++) {
        const r = i % 2 === 0 ? 20 : 9;
        const a = -Math.PI / 2 + (i * Math.PI) / 5;
        pts.push(new Phaser.Math.Vector2(26 + Math.cos(a) * r, 26 + Math.sin(a) * r));
      }
      g.fillStyle(0xfff0a8, 1);
      g.fillPoints(pts, true);
      g.lineStyle(3, C.ink, 1);
      g.strokePoints(pts, true);
      g.lineStyle(4, 0xff9f43, 0.9);
      g.lineBetween(8, 44, 16, 36);
      g.lineBetween(14, 48, 20, 42);
    }
    g.generateTexture('icon_starfall', 52, 52);
    g.destroy();
    g = this.g();
    g.fillStyle(0x6fae4a, 1);
    g.lineStyle(3, C.ink, 1);
    g.fillEllipse(18, 28, 18, 30);
    g.strokeEllipse(18, 28, 18, 30);
    g.fillEllipse(34, 28, 18, 30);
    g.strokeEllipse(34, 28, 18, 30);
    g.fillStyle(0x8fdc5a, 1);
    g.fillEllipse(26, 22, 18, 30);
    g.strokeEllipse(26, 22, 18, 30);
    g.lineStyle(2, 0x3f7a2e, 1);
    g.lineBetween(26, 10, 26, 34);
    g.generateTexture('icon_grovecall', 52, 52);
    g.destroy();
    g = this.g();
    // Thornsnare: a coil of thorny vine
    g.lineStyle(5, 0x3f7a2e, 1);
    g.beginPath();
    g.arc(26, 28, 14, Math.PI * 0.1, Math.PI * 1.9);
    g.strokePath();
    g.lineStyle(3, 0x6a9a3a, 1);
    g.beginPath();
    g.arc(26, 28, 7, Math.PI * 0.6, Math.PI * 2.3);
    g.strokePath();
    g.fillStyle(0xd9e8a0, 1);
    g.lineStyle(1.5, C.ink, 1);
    for (const [x, y] of [[12, 22], [38, 20], [40, 36], [16, 40], [26, 12]]) {
      g.fillTriangle(x - 3, y + 2, x + 3, y + 2, x, y - 5);
      g.strokeTriangle(x - 3, y + 2, x + 3, y + 2, x, y - 5);
    }
    g.generateTexture('icon_thornsnare', 52, 52);
    g.destroy();

    // falling star
    g = this.g();
    g.fillStyle(0xffc93c, 0.35);
    g.fillCircle(20, 20, 20);
    g.fillStyle(0xfff0a8, 1);
    g.fillCircle(20, 20, 11);
    g.lineStyle(2, 0xff9f43, 1);
    g.strokeCircle(20, 20, 11);
    g.generateTexture('meteor', 40, 40);
    g.destroy();

    // rally flag
    g = this.g();
    g.lineStyle(3, 0x5a3b22, 1);
    g.lineBetween(4, 4, 4, 30);
    g.fillStyle(0x6f8fa8, 1);
    g.fillTriangle(5, 4, 22, 10, 5, 16);
    g.lineStyle(2, C.ink, 1);
    g.strokeTriangle(5, 4, 22, 10, 5, 16);
    g.generateTexture('rally', 24, 32);
    g.destroy();

    // hero projectiles
    g = this.g();
    g.fillStyle(0xffffff, 1);
    g.fillRect(0, 2, 14, 2);
    g.fillStyle(0x7fb0d8, 1);
    g.fillTriangle(0, 0, 0, 6, 5, 3);
    g.fillStyle(0xffe680, 1);
    g.fillTriangle(14, 0, 14, 6, 19, 3);
    g.generateTexture('proj_hero_fen', 19, 6);
    g.destroy();
    proj('proj_hero_ember', 0xff9a3c, 5);
    proj('proj_hero_bramble', 0xffffff, 3);

    // glowsap icon (glowing drop)
    g = this.g();
    g.fillStyle(0x9be86a, 0.35);
    g.fillCircle(14, 17, 13);
    g.fillStyle(0x9be86a, 1);
    g.fillCircle(14, 18, 9);
    g.fillTriangle(6, 15, 22, 15, 14, 2);
    g.lineStyle(2.5, C.ink, 1);
    g.strokeCircle(14, 18, 9);
    g.fillStyle(0xffffff, 0.8);
    g.fillCircle(11, 15, 3);
    g.generateTexture('icon_sap', 28, 30);
    g.destroy();

    // hammer icon (builders)
    g = this.g();
    g.fillStyle(0x7a5232, 1);
    g.fillRect(12, 8, 5, 20);
    g.fillStyle(0x9a9aa4, 1);
    g.fillRoundedRect(4, 4, 22, 9, 3);
    g.lineStyle(2, C.ink, 1);
    g.strokeRoundedRect(4, 4, 22, 9, 3);
    g.generateTexture('icon_hammer', 30, 30);
    g.destroy();

    // dirt mound (burrowed enemy)
    g = this.g();
    g.fillStyle(0x000000, 0.25);
    g.fillEllipse(16, 14, 32, 12);
    g.fillStyle(0x7a5a3a, 1);
    g.fillEllipse(16, 11, 28, 14);
    g.fillStyle(0x9a7a52, 1);
    g.fillEllipse(12, 8, 12, 6);
    g.fillStyle(0xff8a3c, 0.8);
    g.fillCircle(20, 10, 2);
    g.generateTexture('mound', 32, 20);
    g.destroy();

    // particle
    g = this.g();
    g.fillStyle(0xffffff, 1);
    g.fillCircle(6, 6, 6);
    g.generateTexture('dot', 12, 12);
    g.destroy();

    // coin icon
    g = this.g();
    g.fillStyle(0xc98a14, 1);
    g.fillCircle(14, 15, 12);
    g.fillStyle(C.gold, 1);
    g.fillCircle(14, 13, 12);
    g.lineStyle(2.5, C.ink, 1);
    g.strokeCircle(14, 13, 12);
    g.fillStyle(0xfff0a8, 1);
    g.fillCircle(10, 9, 3.5);
    g.generateTexture('icon_coin', 28, 30);
    g.destroy();

    // heart icon
    g = this.g();
    g.fillStyle(C.heart, 1);
    g.fillCircle(9, 10, 8);
    g.fillCircle(21, 10, 8);
    g.fillTriangle(1.5, 13, 28.5, 13, 15, 27);
    g.fillStyle(0xffffff, 0.8);
    g.fillCircle(7, 7, 2.5);
    g.generateTexture('icon_heart', 30, 30);
    g.destroy();

    // star icons
    for (const [key, color] of [
      ['star', C.gold],
      ['star_empty', 0x3a4a3e],
    ] as const) {
      g = this.g();
      const pts: Phaser.Math.Vector2[] = [];
      for (let i = 0; i < 10; i++) {
        const r = i % 2 === 0 ? 22 : 10;
        const a = -Math.PI / 2 + (i * Math.PI) / 5;
        pts.push(new Phaser.Math.Vector2(24 + Math.cos(a) * r, 25 + Math.sin(a) * r));
      }
      g.fillStyle(color, 1);
      g.fillPoints(pts, true);
      g.lineStyle(3, C.ink, 1);
      g.strokePoints(pts, true);
      g.generateTexture(key, 48, 50);
      g.destroy();
    }

    // skull-ish wave flag
    g = this.g();
    g.fillStyle(0x5a3b1e, 1);
    g.fillRect(4, 2, 4, 30);
    g.fillStyle(C.danger, 1);
    g.fillTriangle(8, 4, 28, 10, 8, 18);
    g.lineStyle(2, C.ink, 1);
    g.strokeTriangle(8, 4, 28, 10, 8, 18);
    g.generateTexture('icon_wave', 30, 34);
    g.destroy();
  }
}
