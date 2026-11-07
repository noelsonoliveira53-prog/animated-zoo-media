import Phaser from 'phaser';
import { ENEMIES } from '../data/enemies';
import { TOWERS } from '../data/towers';
import { C } from '../ui/theme';

// Generates every texture in code. No image files are shipped.
export class BootScene extends Phaser.Scene {
  constructor() {
    super('Boot');
  }

  create(): void {
    for (const def of Object.values(ENEMIES)) this.makeEnemy(def.id, def.color, def.radius);
    for (const def of Object.values(TOWERS)) {
      for (let tier = 0; tier < def.tiers.length; tier++) this.makeTower(def.id, def.color, tier);
    }
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

  private makeEnemy(id: string, color: number, radius: number): void {
    const g = this.g();
    const s = radius * 2 + 12;
    const cx = s / 2;
    const cy = s / 2 + 2;
    const shade = Phaser.Display.Color.IntegerToColor(color).darken(25).color;
    const light = Phaser.Display.Color.IntegerToColor(color).lighten(20).color;
    // soft ground shadow
    g.fillStyle(0x000000, 0.25);
    g.fillEllipse(cx, cy + radius * 0.85, radius * 1.8, radius * 0.6);
    g.lineStyle(3, C.ink, 1);
    switch (id) {
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

  private makeTower(id: string, color: number, tier: number): void {
    const g = this.g();
    const w = 72;
    const h = 84;
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
    g.generateTexture(`tower_${id}_${tier}`, w, h);
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
