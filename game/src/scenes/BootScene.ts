import Phaser from 'phaser';
import { applyRim } from '../systems/rimLight';
import { brightness } from '../systems/foeReadability';
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
    for (const def of Object.values(ENEMIES)) this.makeEnemy(def.id, def.color, def.radius, !!def.flying, !!def.boss);
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

  /**
   * Outline weight by role: every ink stroke of 2.5 px or more on this sprite is a body outline and becomes
   * `body` (3 px heroes and bosses, 2.5 px regular foes); ink strokes of 2 to 2.5 px are small parts and become 2 px.
   * Finer ink detail lines, coloured strokes and thick ink strokes used as shapes (over 4 px, e.g. an eel's
   * inked body underlay) are left as drawn.
   */
  private roleOutlines(g: Phaser.GameObjects.Graphics, body: number): void {
    const lineStyle = g.lineStyle.bind(g);
    g.lineStyle = ((width: number, color: number, alpha?: number) =>
      lineStyle(color === C.ink && width <= 4 ? (width >= 2.5 ? body : width >= 2 ? 2 : width) : width, color, alpha)) as typeof g.lineStyle;
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
    // a glint in each pupil (design D2)
    g.fillStyle(0xffffff, 0.95);
    g.fillCircle(cx - gap + r * 0.12, cy - r * 0.08, Math.max(0.7, r * 0.2));
    g.fillCircle(cx + gap + r * 0.12, cy - r * 0.08, Math.max(0.7, r * 0.2));
  }

  /**
   * Like orb() but strokes with whatever line style is already set (each enemy picks its own outline weight) and
   * leaves the fill colour on `color` afterwards, so the drawing code that follows behaves as before (design D2).
   */
  private orbKeep(g: Phaser.GameObjects.Graphics, x: number, y: number, w: number, h: number, color: number): void {
    const dark = Phaser.Display.Color.IntegerToColor(color).darken(16).color;
    g.fillStyle(dark, 1);
    g.fillEllipse(x, y, w, h);
    g.fillStyle(color, 1);
    g.fillEllipse(x - w * 0.06, y - h * 0.07, w * 0.86, h * 0.84);
    g.fillStyle(0xffffff, 0.26);
    g.fillEllipse(x - w * 0.2, y - h * 0.24, w * 0.3, h * 0.18);
    g.strokeEllipse(x, y, w, h);
    g.fillStyle(color, 1);
  }

  private makeEnemy(id: string, color: number, radius: number, flying: boolean, boss = false): void {
    const g = this.g();
    this.roleOutlines(g, boss ? 3 : 2.5);
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
        // wing veins and a sheen (design F17)
        g.lineStyle(1, id === 'gnat' ? 0xa8b880 : 0x5a4a90, 0.9);
        for (const side of [-1, 1]) {
          g.lineBetween(cx + side * r * 0.5, cy - r * 0.3, cx + side * r * 1.6, cy - r * 0.55);
          g.lineBetween(cx + side * r * 0.5, cy - r * 0.3, cx + side * r * 1.5, cy + r * 0.05);
        }
        g.fillStyle(0xffffff, id === 'gnat' ? 0.5 : 0.25);
        g.fillEllipse(cx - r * 1.2, cy - r * 0.55, r * 0.6, r * 0.25);
        g.fillEllipse(cx + r * 0.9, cy - r * 0.55, r * 0.6, r * 0.25);
        g.lineStyle(id === 'gnat' ? 2 : 3, C.ink, 1);
        this.orbKeep(g, cx, cy, r * 1.2, r * 1.6, color);
        if (id === 'gnat') {
          g.fillStyle(0x4a4a2a, 0.8);
          g.fillRect(cx - r * 0.5, cy + r * 0.2, r, r * 0.14);
          g.fillRect(cx - r * 0.42, cy + r * 0.5, r * 0.84, r * 0.12);
        }
        if (id === 'gloomwing') {
          g.fillStyle(shade, 1);
          g.fillTriangle(cx - r * 0.5, cy - r * 0.6, cx - r * 0.2, cy - r * 0.6, cx - r * 0.45, cy - r * 1.1);
          g.fillTriangle(cx + r * 0.5, cy - r * 0.6, cx + r * 0.2, cy - r * 0.6, cx + r * 0.45, cy - r * 1.1);
        }
        g.fillStyle(0xffe066, 1);
        g.fillCircle(cx - r * 0.25, cy - r * 0.2, r * 0.18);
        g.fillCircle(cx + r * 0.25, cy - r * 0.2, r * 0.18);
        g.fillStyle(0xffffff, 1);
        g.fillCircle(cx - r * 0.3, cy - r * 0.26, r * 0.06);
        g.fillCircle(cx + r * 0.2, cy - r * 0.26, r * 0.06);
        if (id === 'gloomwing') {
          // two little white fangs
          g.fillStyle(0xfff4d6, 1);
          g.fillTriangle(cx - r * 0.18, cy + r * 0.15, cx - r * 0.06, cy + r * 0.15, cx - r * 0.12, cy + r * 0.38);
          g.fillTriangle(cx + r * 0.06, cy + r * 0.15, cx + r * 0.18, cy + r * 0.15, cx + r * 0.12, cy + r * 0.38);
        }
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
        this.orbKeep(g, cx, cy + r * 0.1, r * 2, r * 1.6, color);
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
        this.orbKeep(g, cx, cy, (r) * 2, (r) * 2, color);
        this.eyes(g, cx - r * 0.15, cy - r * 0.3, r * 0.2, r * 0.28);
        // woven shield
        g.fillStyle(0xd8c27a, 1);
        g.fillRoundedRect(cx + r * 0.1, cy - r * 0.4, r * 1.1, r * 1.4, 5);
        g.lineStyle(2.5, C.ink, 1);
        g.strokeRoundedRect(cx + r * 0.1, cy - r * 0.4, r * 1.1, r * 1.4, 5);
        g.lineStyle(1.5, 0x8a7440, 1);
        for (let i = 1; i < 4; i++) g.lineBetween(cx + r * 0.1, cy - r * 0.4 + i * r * 0.35, cx + r * 1.2, cy - r * 0.4 + i * r * 0.35);
        for (let i = 1; i < 3; i++) g.lineBetween(cx + r * 0.1 + i * r * 0.37, cy - r * 0.4, cx + r * 0.1 + i * r * 0.37, cy + r);
        // a polished river-stone boss on the shield and a green reed headband with a feather (design F17)
        g.fillStyle(0x6a8a9a, 1);
        g.lineStyle(2, C.ink, 1);
        g.fillCircle(cx + r * 0.65, cy + r * 0.3, r * 0.2);
        g.strokeCircle(cx + r * 0.65, cy + r * 0.3, r * 0.2);
        g.fillStyle(0xffffff, 0.7);
        g.fillCircle(cx + r * 0.6, cy + r * 0.24, r * 0.06);
        g.fillStyle(0xe8453a, 1);
        g.lineStyle(1.5, C.ink, 1);
        g.fillEllipse(cx - r * 0.62, cy - r * 0.95, r * 0.2, r * 0.48);
        g.strokeEllipse(cx - r * 0.62, cy - r * 0.95, r * 0.2, r * 0.48);
        g.fillStyle(0x5aa04a, 1);
        g.fillRoundedRect(cx - r * 0.88, cy - r * 0.72, r * 1.0, r * 0.2, r * 0.08);
        g.strokeRoundedRect(cx - r * 0.88, cy - r * 0.72, r * 1.0, r * 0.2, r * 0.08);
        g.fillStyle(0x9ae87a, 1);
        g.fillRect(cx - r * 0.8, cy - r * 0.69, r * 0.8, r * 0.05);
        break;
      }
      case 'splotch': {
        // mud drips trailing off the sides (design D2)
        g.fillStyle(shade, 1);
        g.fillEllipse(cx - r * 1.05, cy + r * 0.85, r * 0.3, r * 0.42);
        g.fillEllipse(cx + r * 0.95, cy + r * 0.9, r * 0.26, r * 0.36);
        this.orbKeep(g, cx, cy + r * 0.3, r * 2.3, r * 1.5, color);
        g.fillCircle(cx - r * 0.4, cy - r * 0.2, r * 0.7);
        g.fillCircle(cx + r * 0.45, cy - r * 0.1, r * 0.65);
        g.fillCircle(cx, cy - r * 0.5, r * 0.6);
        g.fillStyle(0xffffff, 0.22);
        g.fillEllipse(cx - r * 0.45, cy - r * 0.55, r * 0.5, r * 0.28);
        g.fillStyle(shade, 1);
        g.fillCircle(cx - r * 0.6, cy + r * 0.5, r * 0.2);
        g.fillCircle(cx + r * 0.7, cy + r * 0.3, r * 0.15);
        g.fillStyle(light, 1);
        g.fillCircle(cx - r * 0.3, cy - r * 0.6, r * 0.18);
        this.eyes(g, cx, cy - r * 0.05, r * 0.22, r * 0.35);
        break;
      }
      case 'thornhog': {
        // back quills: four pale spines with brown tips, outlines drawn first so the fills sit on top and read (design F17)
        const quills = [-1.5, -0.5, 0.5, 1.5].map((i) => cx + i * r * 0.4);
        g.lineStyle(2.4, C.ink, 1);
        for (const bx of quills) g.strokeTriangle(bx - r * 0.2, cy - r * 0.4, bx + r * 0.2, cy - r * 0.4, bx, cy - r * 1.12);
        for (const bx of quills) {
          g.fillStyle(0xf0e0b0, 1);
          g.fillTriangle(bx - r * 0.2, cy - r * 0.4, bx + r * 0.2, cy - r * 0.4, bx, cy - r * 1.12);
          g.fillStyle(0x9a6a3a, 1);
          g.fillTriangle(bx - r * 0.08, cy - r * 0.86, bx + r * 0.08, cy - r * 0.86, bx, cy - r * 1.12);
        }
        g.lineStyle(3, C.ink, 1);
        this.orbKeep(g, cx, cy, r * 2.1, r * 1.5, color);
        g.fillStyle(shade, 1);
        g.fillEllipse(cx + r * 0.85, cy + r * 0.15, r * 0.6, r * 0.5);
        g.fillStyle(0xfff4d6, 1);
        g.fillTriangle(cx + r * 0.75, cy + r * 0.35, cx + r * 0.9, cy + r * 0.35, cx + r * 0.7, cy - r * 0.05);
        // pink snout tip, a perky ear and a lit back (design F17)
        g.fillStyle(0xff9aa8, 1);
        g.fillCircle(cx + r * 1.08, cy + r * 0.12, r * 0.12);
        g.fillStyle(C.ink, 1);
        g.fillCircle(cx + r * 1.1, cy + r * 0.1, r * 0.04);
        g.fillStyle(color, 1);
        g.lineStyle(1.5, C.ink, 1);
        g.fillEllipse(cx + r * 0.62, cy - r * 0.55, r * 0.3, r * 0.22);
        g.strokeEllipse(cx + r * 0.62, cy - r * 0.55, r * 0.3, r * 0.22);
        g.fillStyle(0xff9aa8, 1);
        g.fillEllipse(cx + r * 0.62, cy - r * 0.55, r * 0.14, r * 0.1);
        g.fillStyle(0xffffff, 0.22);
        g.fillEllipse(cx - r * 0.35, cy - r * 0.3, r * 0.8, r * 0.25);
        this.eyes(g, cx + r * 0.35, cy - r * 0.2, r * 0.15, r * 0.2);
        break;
      }
      case 'wispling': {
        g.fillStyle(color, 0.18);
        g.fillCircle(cx, cy, r * 1.55);
        g.fillStyle(color, 0.3);
        g.fillCircle(cx, cy, r * 1.25);
        // a trail of sparkles drifting below (design D2)
        g.fillStyle(0xffffff, 0.7);
        for (const [dx, dy, rr] of [[-0.5, 1.45, 0.1], [0.35, 1.7, 0.08], [-0.1, 1.95, 0.06]]) g.fillCircle(cx + dx * r, cy + dy * r, r * rr);
        g.fillStyle(color, 1);
        g.fillCircle(cx, cy, r);
        g.fillTriangle(cx - r * 0.9, cy + r * 0.3, cx + r * 0.9, cy + r * 0.3, cx, cy + r * 1.5);
        // a bright core
        g.fillStyle(0xffffff, 0.45);
        g.fillCircle(cx + r * 0.05, cy + r * 0.1, r * 0.55);
        g.fillStyle(0xffffff, 0.85);
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
        // shaded hide: darker right side, lit top-left (design D3)
        g.fillStyle(shade, 1);
        g.fillRoundedRect(cx - r * 0.85, cy - r * 0.9, r * 1.7, r * 1.9, r * 0.6);
        g.fillStyle(color, 1);
        g.fillRoundedRect(cx - r * 0.85, cy - r * 0.9, r * 1.45, r * 1.75, r * 0.55);
        g.fillStyle(0xffffff, 0.2);
        g.fillEllipse(cx - r * 0.45, cy - r * 0.55, r * 0.5, r * 0.3);
        g.strokeRoundedRect(cx - r * 0.85, cy - r * 0.9, r * 1.7, r * 1.9, r * 0.6);
        // colour accent (fix C2): glowing bog-light warts instead of dull olive ones
        g.fillStyle(0xd8f05a, 0.35);
        g.fillCircle(cx - r * 0.4, cy + r * 0.5, r * 0.24);
        g.fillCircle(cx + r * 0.3, cy + r * 0.2, r * 0.2);
        g.fillStyle(0xe8ff7a, 1);
        g.fillCircle(cx - r * 0.4, cy + r * 0.5, r * 0.13);
        g.fillCircle(cx + r * 0.3, cy + r * 0.2, r * 0.1);
        // a mossy cap on the head
        g.fillStyle(0x5a9a3e, 1);
        g.fillEllipse(cx - r * 0.1, cy - r * 0.92, r * 1.0, r * 0.32);
        g.fillStyle(0x8ad86a, 1);
        g.fillEllipse(cx - r * 0.25, cy - r * 0.98, r * 0.4, r * 0.14);
        // a little red toadstool growing out of the moss
        g.fillStyle(0xfff4d6, 1);
        g.fillRect(cx + r * 0.26, cy - r * 1.02, r * 0.14, r * 0.2);
        g.lineStyle(1.5, C.ink, 1);
        g.fillStyle(0xe8453a, 1);
        g.fillEllipse(cx + r * 0.33, cy - r * 1.06, r * 0.56, r * 0.32);
        g.strokeEllipse(cx + r * 0.33, cy - r * 1.06, r * 0.56, r * 0.32);
        g.fillStyle(0xffffff, 1);
        g.fillCircle(cx + r * 0.22, cy - r * 1.1, r * 0.06);
        g.fillCircle(cx + r * 0.4, cy - r * 1.12, r * 0.05);
        g.fillCircle(cx + r * 0.46, cy - r * 1.02, r * 0.04);
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
        this.orbKeep(g, cx, cy - r * 0.3, r * 1.8, r * 1.8, color);
        // frost sparkles drifting off the hood (design D3)
        g.fillStyle(0xffffff, 0.85);
        for (const [dx, dy, rr] of [[-1.1, -0.6, 0.08], [1.05, -0.2, 0.07], [0.8, 0.7, 0.06], [-0.9, 0.5, 0.06]]) g.fillCircle(cx + dx * r, cy + dy * r, r * rr);
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
        this.orbKeep(g, cx, cy + r * 0.1, r * 2, r * 1.6, color);
        g.fillStyle(0xff8a3c, 1);
        for (const [ex, ey] of [[-0.5, -0.2], [0.3, -0.4], [-0.1, 0.3], [0.6, 0.2]]) g.fillCircle(cx + ex * r, cy + ey * r, r * 0.09);
        g.fillStyle(0xe8a090, 1);
        g.fillEllipse(cx + r * 0.85, cy + r * 0.2, r * 0.6, r * 0.45);
        g.fillStyle(0xff5d4a, 1);
        g.fillCircle(cx + r * 1.1, cy + r * 0.2, r * 0.13);
        // glowing claws: a warm halo under the bright claw lines (design D3)
        g.fillStyle(0xff8a3c, 0.3);
        g.fillEllipse(cx + r * 0.45, cy + r * 0.95, r * 0.8, r * 0.45);
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
        // bramble thorns: outlines first, then green fills with pale tips, so they read instead of a dark crest (design F19)
        const thorns = [0, 1, 2, 3, 4].map((k) => cx - r * 0.7 + k * r * 0.38);
        g.lineStyle(2.2, C.ink, 1);
        for (const tx of thorns) g.strokeTriangle(tx - r * 0.16, cy - r * 0.42, tx + r * 0.16, cy - r * 0.42, tx, cy - r * 0.9);
        for (const tx of thorns) {
          g.fillStyle(0x5aa04a, 1);
          g.fillTriangle(tx - r * 0.16, cy - r * 0.42, tx + r * 0.16, cy - r * 0.42, tx, cy - r * 0.9);
          g.fillStyle(0xe8f0b0, 1);
          g.fillTriangle(tx - r * 0.06, cy - r * 0.72, tx + r * 0.06, cy - r * 0.72, tx, cy - r * 0.9);
        }
        g.lineStyle(2.5, C.ink, 1);
        this.orbKeep(g, cx + r * 0.1, cy, r * 1.9, r * 1.1, color);
        g.lineStyle(3, 0x4a8a3a, 1);
        g.lineBetween(cx - r * 0.3, cy - r * 0.5, cx + r * 0.1, cy + r * 0.5);
        g.lineBetween(cx + r * 0.4, cy - r * 0.5, cx + r * 0.7, cy + r * 0.45);
        // ripe bramble berries caught in the vines
        for (const [bx, by] of [[-0.1, 0.1], [0.55, -0.05], [0.62, 0.3]]) {
          g.fillStyle(0x8a2a6a, 1);
          g.fillCircle(cx + bx * r, cy + by * r, r * 0.11);
          g.fillStyle(0xe8a0d8, 1);
          g.fillCircle(cx + bx * r - r * 0.03, cy + by * r - r * 0.04, r * 0.035);
        }
        g.lineStyle(2.5, C.ink, 1);
        this.orbKeep(g, cx - r * 0.85, cy + r * 0.05, (r * 0.45) * 2, (r * 0.45) * 2, color);
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
        this.orbKeep(g, cx, cy, r * 1.9, r * 1.1, color);
        g.fillStyle(0xe8604a, 1);
        g.fillEllipse(cx + r * 0.35, cy + r * 0.05, r * 0.9, r * 0.8);
        g.fillStyle(0x3a7a2a, 1);
        for (let k = 0; k < 4; k++) g.fillTriangle(cx - r * 0.6 + k * r * 0.4, cy - r * 0.45, cx - r * 0.4 + k * r * 0.4, cy - r * 0.45, cx - r * 0.5 + k * r * 0.4, cy - r * 0.8);
        this.orbKeep(g, cx - r * 0.85, cy - r * 0.1, (r * 0.42) * 2, (r * 0.42) * 2, color);
        g.fillStyle(0xffe066, 1);
        g.fillCircle(cx - r * 0.95, cy - r * 0.2, r * 0.2);
        g.fillStyle(0x111111, 1);
        g.fillCircle(cx - r * 1.0, cy - r * 0.2, r * 0.09);
        g.fillStyle(0xffffff, 1);
        g.fillCircle(cx - r * 1.03, cy - r * 0.25, r * 0.04);
        // scale freckles across both halves of the hide: green on the green, orange on the turning red (design F19)
        for (const [dx, dy] of [[-0.35, 0.15], [-0.1, -0.1], [-0.2, 0.3], [0.2, -0.15], [0.45, 0.2], [0.6, -0.05], [0.3, 0.35]]) {
          g.fillStyle(dx > 0.05 ? 0xffa86a : 0x8ad86a, 1);
          g.fillCircle(cx + dx * r, cy + dy * r, r * 0.06);
        }
        break;
      }
      case 'idolkeeper': {
        // temple monkey: round body, pale face, long curled tail, holding up a glowing golden idol
        g.lineStyle(2.5, C.ink, 1);
        g.beginPath();
        g.arc(cx + r * 0.8, cy + r * 0.2, r * 0.45, -2.6, 1.6, false);
        g.strokePath();
        this.orbKeep(g, cx, cy + r * 0.3, r * 1.3, r * 1.2, color);
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
      case 'barkwarden': {
        // walking stump: ringed top, root legs, two knot-hole eyes, a few red leaves still clinging on
        g.lineStyle(2.5, C.ink, 1);
        for (const lx of [-0.6, -0.2, 0.2, 0.6]) g.lineBetween(cx + lx * r, cy + r * 0.55, cx + lx * r * 1.3, cy + r * 1.0);
        g.fillStyle(color, 1);
        g.fillRoundedRect(cx - r * 0.8, cy - r * 0.6, r * 1.6, r * 1.25, 6);
        g.strokeRoundedRect(cx - r * 0.8, cy - r * 0.6, r * 1.6, r * 1.25, 6);
        g.fillStyle(0xc8a878, 1);
        g.fillEllipse(cx, cy - r * 0.6, r * 1.6, r * 0.5);
        g.strokeEllipse(cx, cy - r * 0.6, r * 1.6, r * 0.5);
        g.lineStyle(1.5, 0x8a6a3a, 1);
        g.strokeEllipse(cx, cy - r * 0.6, r * 0.9, r * 0.28);
        g.lineStyle(2.5, C.ink, 1);
        g.fillStyle(0x2a1a0a, 1);
        g.fillEllipse(cx - r * 0.3, cy - r * 0.05, r * 0.25, r * 0.32);
        g.fillEllipse(cx + r * 0.3, cy - r * 0.05, r * 0.25, r * 0.32);
        g.fillStyle(0xffd84a, 1);
        g.fillCircle(cx - r * 0.3, cy - r * 0.05, r * 0.06);
        g.fillCircle(cx + r * 0.3, cy - r * 0.05, r * 0.06);
        g.fillStyle(0xd04a2a, 1);
        g.fillEllipse(cx - r * 0.55, cy - r * 0.85, r * 0.3, r * 0.16);
        g.fillEllipse(cx + r * 0.45, cy - r * 0.9, r * 0.3, r * 0.16);
        // bark grain down the trunk, a shaded right side and a patch of moss (design F21)
        g.fillStyle(Phaser.Display.Color.IntegerToColor(color).darken(22).color, 1);
        g.fillRect(cx + r * 0.42, cy - r * 0.35, r * 0.34, r * 0.95);
        g.lineStyle(1.2, Phaser.Display.Color.IntegerToColor(color).darken(35).color, 1);
        for (const bx of [-0.55, -0.05, 0.55]) g.lineBetween(cx + bx * r, cy - r * 0.3, cx + bx * r + r * 0.05, cy + r * 0.55);
        g.fillStyle(0x6ab04c, 1);
        g.fillEllipse(cx - r * 0.5, cy + r * 0.48, r * 0.5, r * 0.2);
        g.fillStyle(0x9ae87a, 1);
        g.fillEllipse(cx - r * 0.55, cy + r * 0.44, r * 0.22, r * 0.08);
        g.fillStyle(0xffffff, 0.8);
        g.fillCircle(cx - r * 0.33, cy - r * 0.09, r * 0.025);
        g.fillCircle(cx + r * 0.27, cy - r * 0.09, r * 0.025);
        break;
      }
      case 'seedcaster': {
        // rot-sprite: a hooded little figure with a bulging seed pouch and glowing eyes
        g.lineStyle(2.5, C.ink, 1);
        g.fillStyle(color, 1);
        g.fillTriangle(cx - r * 0.75, cy + r * 0.8, cx + r * 0.75, cy + r * 0.8, cx, cy - r * 0.9);
        g.strokeTriangle(cx - r * 0.75, cy + r * 0.8, cx + r * 0.75, cy + r * 0.8, cx, cy - r * 0.9);
        // shaded right side of the hood, a frayed hem, and a seedling sprouting from the hood's tip (design F21)
        g.fillStyle(Phaser.Display.Color.IntegerToColor(color).darken(25).color, 1);
        g.fillTriangle(cx, cy - r * 0.9, cx + r * 0.75, cy + r * 0.8, cx + r * 0.15, cy + r * 0.8);
        g.fillStyle(0xffffff, 0.22);
        g.fillTriangle(cx - r * 0.05, cy - r * 0.7, cx - r * 0.45, cy + r * 0.5, cx - r * 0.25, cy + r * 0.5);
        g.strokeTriangle(cx - r * 0.75, cy + r * 0.8, cx + r * 0.75, cy + r * 0.8, cx, cy - r * 0.9);
        g.fillStyle(color, 1);
        for (let k = 0; k < 4; k++) g.fillTriangle(cx - r * 0.7 + k * r * 0.36, cy + r * 0.78, cx - r * 0.52 + k * r * 0.36, cy + r * 0.78, cx - r * 0.61 + k * r * 0.36, cy + r * 0.98);
        g.lineStyle(1.5, 0x3a7a2a, 1);
        g.lineBetween(cx, cy - r * 0.9, cx + r * 0.08, cy - r * 1.2);
        g.fillStyle(0x8ad86a, 1);
        g.fillEllipse(cx - r * 0.1, cy - r * 1.18, r * 0.26, r * 0.14);
        g.fillEllipse(cx + r * 0.22, cy - r * 1.24, r * 0.28, r * 0.15);
        g.lineStyle(2.5, C.ink, 1);
        // the dark face inside the hood, eyes glowing with a soft halo
        g.fillStyle(0x1a1028, 1);
        g.fillCircle(cx, cy - r * 0.15, r * 0.32);
        g.fillStyle(0xc8ff6a, 0.35);
        g.fillCircle(cx - r * 0.12, cy - r * 0.18, r * 0.13);
        g.fillCircle(cx + r * 0.12, cy - r * 0.18, r * 0.13);
        g.fillStyle(0xc8ff6a, 1);
        g.fillCircle(cx - r * 0.12, cy - r * 0.18, r * 0.07);
        g.fillCircle(cx + r * 0.12, cy - r * 0.18, r * 0.07);
        g.fillStyle(0x6a4a2a, 1);
        g.fillCircle(cx + r * 0.6, cy + r * 0.45, r * 0.35);
        g.strokeCircle(cx + r * 0.6, cy + r * 0.45, r * 0.35);
        g.fillStyle(0x2a1a2a, 1);
        for (const [dx, dy] of [[0.5, 0.35], [0.7, 0.5], [0.58, 0.6]]) g.fillCircle(cx + dx * r, cy + dy * r, r * 0.07);
        break;
      }
      case 'gorgegrub': {
        // fat segmented grub: three bulging rings, stubby legs, a wide hungry mouth
        g.lineStyle(2.5, C.ink, 1);
        for (const lx of [-0.5, 0, 0.5]) g.lineBetween(cx + lx * r, cy + r * 0.5, cx + lx * r, cy + r * 0.85);
        // each ring shaded as its own orb, lit from the upper left (design F22)
        for (const [dx, sz] of [[0.55, 0.62], [0, 0.8], [-0.55, 0.7]] as const) this.orbKeep(g, cx + dx * r, cy + r * 0.05, r * sz * 1.3, r * sz * 1.4, color);
        g.fillStyle(0xe8d8a0, 1);
        g.fillEllipse(cx - r * 0.55, cy - r * 0.3, r * 0.5, r * 0.2);
        g.fillStyle(0x3a1a1a, 1);
        g.fillEllipse(cx - r * 0.8, cy + r * 0.2, r * 0.35, r * 0.3);
        g.fillStyle(0xfff4d6, 1);
        g.fillTriangle(cx - r * 0.92, cy + r * 0.08, cx - r * 0.84, cy + r * 0.08, cx - r * 0.88, cy + r * 0.2);
        g.fillTriangle(cx - r * 0.76, cy + r * 0.07, cx - r * 0.68, cy + r * 0.07, cx - r * 0.72, cy + r * 0.19);
        g.fillStyle(0x9ae8ff, 0.85);
        g.fillEllipse(cx - r * 0.86, cy + r * 0.42, r * 0.08, r * 0.16); // a hungry drool drop
        g.fillStyle(0x1a1010, 1);
        g.fillCircle(cx - r * 0.7, cy - r * 0.15, r * 0.08);
        g.fillCircle(cx - r * 0.45, cy - r * 0.2, r * 0.08);
        g.fillStyle(0xffffff, 1);
        g.fillCircle(cx - r * 0.72, cy - r * 0.18, r * 0.03);
        g.fillCircle(cx - r * 0.47, cy - r * 0.23, r * 0.03);
        break;
      }
      case 'rotseed': {
        // black seed half-buried, a pale shoot just poking out
        g.lineStyle(2, C.ink, 1);
        this.orbKeep(g, cx, cy + r * 0.2, r * 1.5, r * 1.1, color);
        g.fillStyle(0x5a4a5a, 1);
        g.fillEllipse(cx - r * 0.25, cy, r * 0.4, r * 0.25);
        g.lineStyle(2.5, 0x9ac85a, 1);
        g.beginPath();
        g.moveTo(cx, cy - r * 0.3);
        g.lineTo(cx + r * 0.1, cy - r * 0.8);
        g.lineTo(cx + r * 0.35, cy - r * 1.0);
        g.strokePath();
        g.fillStyle(0x9ac85a, 1);
        g.fillEllipse(cx + r * 0.45, cy - r * 1.0, r * 0.4, r * 0.2);
        break;
      }
      case 'stormcaller': {
        // hunched shaman in a grey cloak, a copper lightning rod on its back, a little cloud over its head
        g.lineStyle(3, 0xc87a3a, 1);
        g.lineBetween(cx + r * 0.35, cy + r * 0.6, cx + r * 0.6, cy - r * 1.05);
        g.lineStyle(2.5, C.ink, 1);
        g.fillStyle(color, 1);
        g.fillTriangle(cx - r * 0.8, cy + r * 0.85, cx + r * 0.8, cy + r * 0.85, cx - r * 0.05, cy - r * 0.55);
        g.strokeTriangle(cx - r * 0.8, cy + r * 0.85, cx + r * 0.8, cy + r * 0.85, cx - r * 0.05, cy - r * 0.55);
        // cloak shading, a lit left fold and a zigzag bolt stitched down the front (design F22)
        g.fillStyle(Phaser.Display.Color.IntegerToColor(color).darken(25).color, 1);
        g.fillTriangle(cx - r * 0.05, cy - r * 0.55, cx + r * 0.8, cy + r * 0.85, cx + r * 0.15, cy + r * 0.85);
        g.fillStyle(0xffffff, 0.2);
        g.fillTriangle(cx - r * 0.1, cy - r * 0.35, cx - r * 0.55, cy + r * 0.6, cx - r * 0.35, cy + r * 0.6);
        g.strokeTriangle(cx - r * 0.8, cy + r * 0.85, cx + r * 0.8, cy + r * 0.85, cx - r * 0.05, cy - r * 0.55);
        g.lineStyle(2, 0xfff07a, 1);
        g.beginPath();
        g.moveTo(cx - r * 0.05, cy + r * 0.25);
        g.lineTo(cx - r * 0.2, cy + r * 0.45);
        g.lineTo(cx + r * 0.02, cy + r * 0.48);
        g.lineTo(cx - r * 0.12, cy + r * 0.75);
        g.strokePath();
        g.lineStyle(2.5, C.ink, 1);
        g.fillStyle(0x1a1e2a, 1);
        g.fillCircle(cx - r * 0.05, cy - r * 0.1, r * 0.3);
        g.fillStyle(0xfff07a, 0.35);
        g.fillCircle(cx - r * 0.15, cy - r * 0.12, r * 0.13);
        g.fillCircle(cx + r * 0.06, cy - r * 0.12, r * 0.13);
        g.fillStyle(0xfff07a, 1);
        g.fillCircle(cx - r * 0.15, cy - r * 0.12, r * 0.07);
        g.fillCircle(cx + r * 0.06, cy - r * 0.12, r * 0.07);
        // the rod's copper tip sparks
        g.fillStyle(0xfff07a, 1);
        g.fillCircle(cx + r * 0.6, cy - r * 1.07, r * 0.09);
        g.fillStyle(0xd8dce8, 1);
        g.fillCircle(cx - r * 0.3, cy - r * 0.95, r * 0.22);
        g.fillCircle(cx, cy - r * 1.05, r * 0.28);
        g.fillCircle(cx + r * 0.3, cy - r * 0.95, r * 0.2);
        g.fillStyle(0xfff07a, 1);
        g.fillTriangle(cx - r * 0.05, cy - r * 0.8, cx + r * 0.1, cy - r * 0.8, cx - r * 0.1, cy - r * 0.55);
        break;
      }
      case 'thunderhoof': {
        // shaggy buffalo: big humped body, curled horns, stamping hooves
        g.lineStyle(3, C.ink, 1);
        for (const lx of [-0.55, -0.2, 0.25, 0.6]) g.lineBetween(cx + lx * r, cy + r * 0.4, cx + lx * r, cy + r * 0.95);
        this.orbKeep(g, cx + r * 0.1, cy, r * 1.7, r * 1.15, color);
        g.fillStyle(0x4a3226, 1);
        g.fillEllipse(cx - r * 0.25, cy - r * 0.3, r * 0.9, r * 0.7);
        this.orbKeep(g, cx - r * 0.7, cy + r * 0.05, (r * 0.42) * 2, (r * 0.42) * 2, color);
        g.lineStyle(3, 0xe8e0c8, 1);
        g.beginPath();
        g.arc(cx - r * 0.95, cy - r * 0.3, r * 0.22, Math.PI * 0.2, Math.PI * 1.3);
        g.strokePath();
        g.beginPath();
        g.arc(cx - r * 0.45, cy - r * 0.35, r * 0.22, Math.PI * 1.7, Math.PI * 0.8, true);
        g.strokePath();
        g.fillStyle(0x1a1010, 1);
        g.fillCircle(cx - r * 0.82, cy, r * 0.07);
        g.fillCircle(cx - r * 0.58, cy, r * 0.07);
        break;
      }
      case 'copperhorn': {
        // big grey ox, head low, wide horns capped with shining copper, a copper ring through its nose
        g.lineStyle(3, C.ink, 1);
        for (const lx of [-0.6, -0.25, 0.25, 0.6]) g.lineBetween(cx + lx * r, cy + r * 0.4, cx + lx * r, cy + r * 0.95);
        this.orbKeep(g, cx + r * 0.15, cy, r * 1.7, r * 1.1, color);
        g.fillCircle(cx - r * 0.7, cy + r * 0.1, r * 0.45);
        g.strokeCircle(cx - r * 0.7, cy + r * 0.1, r * 0.45);
        g.lineStyle(4, 0xe8e0c8, 1);
        g.lineBetween(cx - r * 0.9, cy - r * 0.2, cx - r * 1.3, cy - r * 0.6);
        g.lineBetween(cx - r * 0.5, cy - r * 0.25, cx - r * 0.2, cy - r * 0.7);
        g.fillStyle(0xd88a3a, 1);
        g.fillCircle(cx - r * 1.3, cy - r * 0.62, r * 0.13);
        g.fillCircle(cx - r * 0.2, cy - r * 0.72, r * 0.13);
        g.fillStyle(0xffd8a0, 1);
        g.fillCircle(cx - r * 1.34, cy - r * 0.66, r * 0.05);
        g.fillCircle(cx - r * 0.24, cy - r * 0.76, r * 0.05);
        g.lineStyle(2, 0xd88a3a, 1);
        g.strokeCircle(cx - r * 0.85, cy + r * 0.42, r * 0.11);
        // a woven copper-studded harness over the shoulders and a pale muzzle (design F22)
        g.fillStyle(0x8a5a2a, 1);
        g.fillRect(cx - r * 0.05, cy - r * 0.5, r * 0.22, r * 1.0);
        g.fillStyle(0xd88a3a, 1);
        for (const yy of [-0.32, 0.0, 0.32]) g.fillCircle(cx + r * 0.06, cy + yy * r, r * 0.07);
        g.fillStyle(0xc8c0b8, 1);
        g.fillEllipse(cx - r * 0.82, cy + r * 0.28, r * 0.42, r * 0.3);
        g.fillStyle(0x1a1010, 1);
        g.fillCircle(cx - r * 0.9, cy + r * 0.28, r * 0.04);
        g.fillCircle(cx - r * 0.75, cy + r * 0.28, r * 0.04);
        g.fillCircle(cx - r * 0.85, cy + r * 0.02, r * 0.07);
        g.fillCircle(cx - r * 0.55, cy + r * 0.02, r * 0.07);
        g.fillStyle(0xffffff, 1);
        g.fillCircle(cx - r * 0.87, cy - r * 0.01, r * 0.03);
        g.fillCircle(cx - r * 0.57, cy - r * 0.01, r * 0.03);
        break;
      }
      case 'shimmerjack':
      case 'mirageling': {
        // long-eared desert hare mid-bound, with heat-haze wiggles behind it
        g.lineStyle(2, 0xffffff, 0.5);
        for (const dy of [-0.2, 0.15, 0.5]) {
          g.beginPath();
          g.moveTo(cx + r * 0.9, cy + dy * r);
          g.lineTo(cx + r * 1.05, cy + dy * r - r * 0.1);
          g.lineTo(cx + r * 1.2, cy + dy * r);
          g.strokePath();
        }
        g.lineStyle(2.5, C.ink, 1);
        this.orbKeep(g, cx + r * 0.1, cy + r * 0.15, r * 1.4, r * 0.95, color);
        g.fillCircle(cx - r * 0.55, cy - r * 0.15, r * 0.42);
        g.strokeCircle(cx - r * 0.55, cy - r * 0.15, r * 0.42);
        g.fillEllipse(cx - r * 0.6, cy - r * 0.95, r * 0.24, r * 0.85);
        g.strokeEllipse(cx - r * 0.6, cy - r * 0.95, r * 0.24, r * 0.85);
        g.fillEllipse(cx - r * 0.3, cy - r * 0.9, r * 0.24, r * 0.8);
        g.strokeEllipse(cx - r * 0.3, cy - r * 0.9, r * 0.24, r * 0.8);
        g.fillStyle(0x1a1010, 1);
        g.fillCircle(cx - r * 0.68, cy - r * 0.2, r * 0.08);
        g.fillStyle(0xffffff, 1);
        g.fillCircle(cx + r * 0.75, cy + r * 0.05, r * 0.15);
        break;
      }
      case 'sandpicker': {
        // grinning jackal thief: pointed ears, bandit mask, a sack slung over the shoulder
        g.lineStyle(2.5, C.ink, 1);
        for (const lx of [-0.4, 0.4]) g.lineBetween(cx + lx * r, cy + r * 0.5, cx + lx * r, cy + r * 0.95);
        g.fillStyle(0x8a7a5a, 1);
        g.fillCircle(cx + r * 0.6, cy - r * 0.15, r * 0.45);
        g.strokeCircle(cx + r * 0.6, cy - r * 0.15, r * 0.45);
        this.orbKeep(g, cx, cy + r * 0.15, r * 1.1, r * 1.0, color);
        g.fillCircle(cx - r * 0.45, cy - r * 0.4, r * 0.38);
        g.strokeCircle(cx - r * 0.45, cy - r * 0.4, r * 0.38);
        g.fillTriangle(cx - r * 0.75, cy - r * 0.6, cx - r * 0.55, cy - r * 0.6, cx - r * 0.7, cy - r * 1.05);
        g.fillTriangle(cx - r * 0.35, cy - r * 0.65, cx - r * 0.15, cy - r * 0.6, cx - r * 0.25, cy - r * 1.05);
        g.fillStyle(0x2a1a10, 1);
        g.fillRect(cx - r * 0.8, cy - r * 0.5, r * 0.65, r * 0.17);
        g.fillStyle(0xffd84a, 1);
        g.fillCircle(cx - r * 0.62, cy - r * 0.42, r * 0.05);
        g.fillCircle(cx - r * 0.35, cy - r * 0.42, r * 0.05);
        g.fillStyle(0xffd84a, 1);
        g.fillCircle(cx + r * 0.62, cy - r * 0.3, r * 0.08);
        break;
      }
      case 'kilnback': {
        // tortoise with a tall baked-clay shell in glazed hexagons, stubby legs, a small wise head
        g.lineStyle(2.5, C.ink, 1);
        for (const lx of [-0.55, -0.15, 0.25, 0.6]) g.lineBetween(cx + lx * r, cy + r * 0.35, cx + lx * r, cy + r * 0.85);
        g.fillStyle(0x8a7a5a, 1);
        g.fillCircle(cx - r * 0.85, cy + r * 0.15, r * 0.3);
        g.strokeCircle(cx - r * 0.85, cy + r * 0.15, r * 0.3);
        this.orbKeep(g, cx + r * 0.05, cy, r * 1.6, r * 1.3, color);
        g.lineStyle(1.8, 0x7a3a1a, 1);
        for (const [hx, hy] of [[-0.35, -0.15], [0.1, -0.3], [0.5, -0.1], [-0.1, 0.2], [0.35, 0.25]]) g.strokeCircle(cx + hx * r, cy + hy * r, r * 0.2);
        g.fillStyle(0xffe0a0, 0.6);
        g.fillEllipse(cx - r * 0.2, cy - r * 0.4, r * 0.4, r * 0.15);
        g.fillStyle(0x111111, 1);
        g.fillCircle(cx - r * 0.95, cy + r * 0.08, r * 0.06);
        break;
      }
      case 'shellsnap': {
        // reef crab: barnacled dome shell, two big claws, stalk eyes, little legs
        g.lineStyle(2.5, C.ink, 1);
        for (const lx of [-0.7, -0.4, 0.4, 0.7]) g.lineBetween(cx + lx * r, cy + r * 0.3, cx + lx * r * 1.3, cy + r * 0.85);
        this.orbKeep(g, cx - r * 0.95, cy - r * 0.05, (r * 0.32) * 2, (r * 0.32) * 2, color);
        g.fillCircle(cx + r * 0.95, cy - r * 0.05, r * 0.32);
        g.strokeCircle(cx + r * 0.95, cy - r * 0.05, r * 0.32);
        // the claw tips: a pale pincer notch in each (design F23)
        g.fillStyle(0xfff0e0, 1);
        g.fillTriangle(cx - r * 1.2, cy - r * 0.2, cx - r * 1.05, cy - r * 0.05, cx - r * 1.25, cy + r * 0.0);
        g.fillTriangle(cx + r * 1.2, cy - r * 0.2, cx + r * 1.05, cy - r * 0.05, cx + r * 1.25, cy + r * 0.0);
        g.lineStyle(2.5, C.ink, 1);
        this.orbKeep(g, cx, cy + r * 0.05, r * 1.5, r * 1.1, 0x9a8a7a);
        g.fillStyle(0xe8e0d0, 1);
        for (const [bx, by] of [[-0.3, -0.15], [0.25, -0.2], [0, 0.2], [0.4, 0.15], [-0.4, 0.2]]) g.fillCircle(cx + bx * r, cy + by * r, r * 0.09);
        g.fillStyle(0x6ab04c, 1);
        g.fillEllipse(cx + r * 0.1, cy - r * 0.32, r * 0.4, r * 0.14); // a frond of seaweed on the shell
        g.lineStyle(2, C.ink, 1);
        g.lineBetween(cx - r * 0.2, cy - r * 0.45, cx - r * 0.25, cy - r * 0.75);
        g.lineBetween(cx + r * 0.2, cy - r * 0.45, cx + r * 0.25, cy - r * 0.75);
        g.fillStyle(0x111111, 1);
        g.fillCircle(cx - r * 0.25, cy - r * 0.78, r * 0.08);
        g.fillCircle(cx + r * 0.25, cy - r * 0.78, r * 0.08);
        break;
      }
      case 'tidecaller': {
        // sea otter floating upright: round face with whiskers, a pale belly, a spiral conch held to its mouth
        g.lineStyle(2.5, C.ink, 1);
        this.orbKeep(g, cx, cy + r * 0.15, r * 1.2, r * 1.4, color);
        g.fillStyle(0xd8c8a8, 1);
        g.fillEllipse(cx, cy + r * 0.3, r * 0.7, r * 0.9);
        this.orbKeep(g, cx, cy - r * 0.55, (r * 0.45) * 2, (r * 0.45) * 2, color);
        g.fillStyle(0xd8c8a8, 1);
        g.fillEllipse(cx, cy - r * 0.42, r * 0.5, r * 0.3);
        g.fillStyle(0x111111, 1);
        g.fillCircle(cx - r * 0.17, cy - r * 0.65, r * 0.07);
        g.fillCircle(cx + r * 0.17, cy - r * 0.65, r * 0.07);
        g.lineStyle(1.2, 0xffffff, 0.8);
        g.lineBetween(cx - r * 0.2, cy - r * 0.42, cx - r * 0.55, cy - r * 0.48);
        g.lineBetween(cx + r * 0.2, cy - r * 0.42, cx + r * 0.55, cy - r * 0.48);
        g.fillStyle(0xf0c8b0, 1);
        g.lineStyle(2, C.ink, 1);
        g.fillTriangle(cx + r * 0.2, cy - r * 0.35, cx + r * 0.95, cy - r * 0.55, cx + r * 0.85, cy - r * 0.05);
        g.strokeTriangle(cx + r * 0.2, cy - r * 0.35, cx + r * 0.95, cy - r * 0.55, cx + r * 0.85, cy - r * 0.05);
        // conch spiral bands and a pink lip, a dark nose, eye glints, and little rings of water at its waist (design F23)
        g.lineStyle(1.2, 0xc88a6a, 1);
        g.lineBetween(cx + r * 0.45, cy - r * 0.42, cx + r * 0.58, cy - r * 0.15);
        g.lineBetween(cx + r * 0.68, cy - r * 0.47, cx + r * 0.75, cy - r * 0.1);
        g.fillStyle(0xff9ab8, 1);
        g.fillCircle(cx + r * 0.9, cy - r * 0.3, r * 0.08);
        g.fillStyle(0x3a2a2a, 1);
        g.fillEllipse(cx, cy - r * 0.47, r * 0.16, r * 0.1);
        g.fillStyle(0xffffff, 1);
        g.fillCircle(cx - r * 0.19, cy - r * 0.68, r * 0.03);
        g.fillCircle(cx + r * 0.15, cy - r * 0.68, r * 0.03);
        g.lineStyle(1.5, 0x9ae8ff, 0.9);
        g.strokeEllipse(cx, cy + r * 0.85, r * 1.5, r * 0.32);
        g.lineStyle(1, 0xd8f8ff, 0.7);
        g.strokeEllipse(cx, cy + r * 0.88, r * 1.9, r * 0.4);
        break;
      }
      case 'inkspitter': {
        // small octopus: round mantle, big eyes, curling tentacles
        g.lineStyle(3, color, 1);
        for (const [x1, x2] of [[-0.55, -0.95], [-0.25, -0.45], [0.05, 0.1], [0.35, 0.6], [0.6, 1.0]]) {
          g.beginPath();
          g.moveTo(cx + x1 * r, cy + r * 0.25);
          g.lineTo(cx + (x1 + x2) * 0.5 * r, cy + r * 0.7);
          g.lineTo(cx + x2 * r, cy + r * 0.6);
          g.strokePath();
        }
        g.lineStyle(2.5, C.ink, 1);
        this.orbKeep(g, cx, cy - r * 0.15, r * 1.3, r * 1.2, color);
        g.fillStyle(0xffffff, 1);
        g.fillCircle(cx - r * 0.25, cy - r * 0.1, r * 0.2);
        g.fillCircle(cx + r * 0.25, cy - r * 0.1, r * 0.2);
        g.fillStyle(0x111111, 1);
        g.fillCircle(cx - r * 0.22, cy - r * 0.08, r * 0.1);
        g.fillCircle(cx + r * 0.28, cy - r * 0.08, r * 0.1);
        g.fillStyle(0xc88ad8, 1);
        g.fillCircle(cx - r * 0.1, cy - r * 0.5, r * 0.08);
        g.fillCircle(cx + r * 0.2, cy - r * 0.55, r * 0.06);
        break;
      }
      case 'brinecrown': {
        // colossal hermit crab: a spiral shell crowned with coral, big claws, stalk eyes, legs splayed under it
        g.lineStyle(3, C.ink, 1);
        for (const lx of [-0.75, -0.45, 0.45, 0.75]) g.lineBetween(cx + lx * r, cy + r * 0.45, cx + lx * r * 1.35, cy + r * 0.95);
        this.orbKeep(g, cx - r * 1.0, cy + r * 0.15, (r * 0.38) * 2, (r * 0.38) * 2, color);
        g.fillCircle(cx + r * 0.95, cy + r * 0.2, r * 0.3);
        g.strokeCircle(cx + r * 0.95, cy + r * 0.2, r * 0.3);
        g.fillStyle(0xd8c8a8, 1);
        g.fillCircle(cx, cy - r * 0.1, r * 0.75);
        g.strokeCircle(cx, cy - r * 0.1, r * 0.75);
        g.lineStyle(2, 0x9a8a6a, 1);
        g.beginPath();
        g.arc(cx, cy - r * 0.1, r * 0.5, 0, Math.PI * 1.6);
        g.strokePath();
        g.beginPath();
        g.arc(cx, cy - r * 0.1, r * 0.25, 0, Math.PI * 1.5);
        g.strokePath();
        // coral crown
        for (const [dx, h, col] of [[-0.45, 0.55, 0xf07a6a], [-0.15, 0.75, 0xf0a05a], [0.2, 0.65, 0xd86aa8], [0.45, 0.5, 0xf07a6a]] as const) {
          g.lineStyle(5, col, 1);
          g.lineBetween(cx + dx * r, cy - r * 0.65, cx + dx * r * 1.2, cy - r * (0.65 + h));
          g.fillStyle(col, 1);
          g.fillCircle(cx + dx * r * 1.2, cy - r * (0.65 + h), r * 0.09);
        }
        g.lineStyle(2.5, C.ink, 1);
        g.lineBetween(cx - r * 0.6, cy + r * 0.35, cx - r * 0.65, cy - r * 0.05);
        g.lineBetween(cx - r * 0.35, cy + r * 0.4, cx - r * 0.35, cy);
        g.fillStyle(0x111111, 1);
        g.fillCircle(cx - r * 0.65, cy - r * 0.08, r * 0.08);
        g.fillCircle(cx - r * 0.35, cy - r * 0.03, r * 0.08);
        break;
      }
      case 'deckgunner': {
        // rat pirate: bandana, round ears, a long brass blunderbuss with a flared muzzle
        g.lineStyle(2.5, C.ink, 1);
        this.orbKeep(g, cx, cy + r * 0.2, r * 1.1, r * 1.2, color);
        g.fillStyle(0xd8a0a0, 1);
        g.fillCircle(cx - r * 0.42, cy - r * 0.78, r * 0.17);
        g.fillCircle(cx + r * 0.22, cy - r * 0.8, r * 0.17);
        g.strokeCircle(cx - r * 0.42, cy - r * 0.78, r * 0.17);
        g.strokeCircle(cx + r * 0.22, cy - r * 0.8, r * 0.17);
        this.orbKeep(g, cx - r * 0.1, cy - r * 0.45, r * 0.84, r * 0.84, color);
        // a striped sailor's shirt, pink snout and a bandana with trailing tails (design F23)
        g.fillStyle(0xf0ece0, 1);
        g.fillEllipse(cx, cy + r * 0.35, r * 0.8, r * 0.6);
        g.fillStyle(0x3a6ac8, 1);
        for (const yy of [0.18, 0.38, 0.56]) g.fillRect(cx - r * 0.36, cy + yy * r, r * 0.72, r * 0.07);
        g.fillStyle(0xff9aa8, 1);
        g.fillCircle(cx - r * 0.48, cy - r * 0.38, r * 0.08);
        g.fillStyle(0xc83a3a, 1);
        g.fillRect(cx - r * 0.5, cy - r * 0.72, r * 0.8, r * 0.14);
        g.fillTriangle(cx + r * 0.28, cy - r * 0.7, cx + r * 0.55, cy - r * 0.62, cx + r * 0.42, cy - r * 0.48);
        g.fillStyle(0xffffff, 1);
        g.fillCircle(cx - r * 0.3, cy - r * 0.68, r * 0.03);
        g.fillCircle(cx, cy - r * 0.68, r * 0.03);
        g.fillStyle(0x111111, 1);
        g.fillCircle(cx - r * 0.3, cy - r * 0.45, r * 0.07);
        g.fillCircle(cx + r * 0.05, cy - r * 0.45, r * 0.07);
        g.fillStyle(0xffffff, 1);
        g.fillCircle(cx - r * 0.32, cy - r * 0.48, r * 0.025);
        g.fillCircle(cx + r * 0.03, cy - r * 0.48, r * 0.025);
        g.fillStyle(0xd8a040, 1);
        g.fillRect(cx - r * 0.2, cy - r * 0.05, r * 1.15, r * 0.16);
        g.fillTriangle(cx + r * 0.95, cy - r * 0.15, cx + r * 0.95, cy + r * 0.21, cx + r * 1.2, cy + r * 0.03);
        g.strokeRect(cx - r * 0.2, cy - r * 0.05, r * 1.15, r * 0.16);
        g.fillStyle(0xfff0b0, 1);
        g.fillRect(cx - r * 0.1, cy - r * 0.03, r * 0.9, r * 0.04); // brass shine along the barrel
        break;
      }
      case 'ironkeel': {
        // walrus: big round body, white tusks, a dark anchor hanging from a chain over its shoulder
        g.lineStyle(3, C.ink, 1);
        this.orbKeep(g, cx + r * 0.1, cy + r * 0.15, r * 1.7, r * 1.25, color);
        g.fillCircle(cx - r * 0.6, cy - r * 0.15, r * 0.5);
        g.strokeCircle(cx - r * 0.6, cy - r * 0.15, r * 0.5);
        g.fillStyle(0xe8e0d0, 1);
        g.fillTriangle(cx - r * 0.85, cy + r * 0.05, cx - r * 0.72, cy + r * 0.05, cx - r * 0.8, cy + r * 0.55);
        g.fillTriangle(cx - r * 0.5, cy + r * 0.05, cx - r * 0.37, cy + r * 0.05, cx - r * 0.44, cy + r * 0.55);
        g.fillStyle(0x111111, 1);
        g.fillCircle(cx - r * 0.75, cy - r * 0.35, r * 0.07);
        g.fillCircle(cx - r * 0.45, cy - r * 0.35, r * 0.07);
        g.fillStyle(0xe8e0d0, 1);
        for (const [bx, by] of [[0.3, -0.3], [0.6, 0.1], [0.1, 0.4]]) g.fillCircle(cx + bx * r, cy + by * r, r * 0.08);
        g.lineStyle(2, 0x3a3a42, 1);
        g.lineBetween(cx + r * 0.2, cy - r * 0.45, cx + r * 0.75, cy - r * 0.05);
        g.lineStyle(3, 0x3a3a42, 1);
        g.lineBetween(cx + r * 0.8, cy - r * 0.05, cx + r * 0.8, cy + r * 0.6);
        g.lineBetween(cx + r * 0.6, cy + r * 0.45, cx + r * 1.0, cy + r * 0.45);
        g.beginPath();
        g.arc(cx + r * 0.8, cy + r * 0.45, r * 0.22, 0.2, Math.PI - 0.2);
        g.strokePath();
        break;
      }
      case 'barkdrum': {
        // stag beetle: glossy brown shell split down the middle, big curved mandibles, a log drum on its back
        g.lineStyle(2.5, C.ink, 1);
        this.orbKeep(g, cx + r * 0.1, cy + r * 0.2, r * 1.5, r * 1.3, color);
        g.lineBetween(cx + r * 0.1, cy - r * 0.45, cx + r * 0.1, cy + r * 0.85);
        g.fillStyle(0xffffff, 0.25);
        g.fillEllipse(cx - r * 0.25, cy, r * 0.35, r * 0.6);
        g.fillStyle(0x3a2414, 1);
        g.fillCircle(cx - r * 0.7, cy - r * 0.1, r * 0.35);
        g.strokeCircle(cx - r * 0.7, cy - r * 0.1, r * 0.35);
        g.lineStyle(3, 0x3a2414, 1);
        g.beginPath();
        g.arc(cx - r * 1.0, cy - r * 0.45, r * 0.35, Math.PI * 0.2, Math.PI * 1.1);
        g.strokePath();
        g.beginPath();
        g.arc(cx - r * 1.0, cy + r * 0.2, r * 0.35, Math.PI * 0.9, Math.PI * 1.8);
        g.strokePath();
        // the log drum, strapped across the shell
        g.lineStyle(2, C.ink, 1);
        g.fillStyle(0xa8784a, 1);
        g.fillRoundedRect(cx - r * 0.25, cy - r * 0.75, r * 0.95, r * 0.5, r * 0.18);
        g.strokeRoundedRect(cx - r * 0.25, cy - r * 0.75, r * 0.95, r * 0.5, r * 0.18);
        g.fillStyle(0xe8d0a0, 1);
        g.fillEllipse(cx + r * 0.7, cy - r * 0.5, r * 0.22, r * 0.5);
        g.strokeEllipse(cx + r * 0.7, cy - r * 0.5, r * 0.22, r * 0.5);
        // rope lacing zig-zagging round the drum, wood grain, and a stick tucked under the strap (design F24)
        g.lineStyle(1, 0x7a5030, 0.9);
        for (let k = 0; k < 3; k++) {
          const lx = cx - r * 0.12 + k * r * 0.26;
          g.lineBetween(lx, cy - r * 0.72, lx + r * 0.13, cy - r * 0.28);
          g.lineBetween(lx + r * 0.13, cy - r * 0.28, lx + r * 0.26, cy - r * 0.72);
        }
        g.lineStyle(1, 0x7a5030, 1);
        g.lineBetween(cx - r * 0.2, cy - r * 0.62, cx + r * 0.6, cy - r * 0.62);
        g.lineStyle(2.5, 0x5a3a1a, 1);
        g.lineBetween(cx + r * 0.25, cy - r * 0.95, cx + r * 0.85, cy - r * 0.8);
        g.fillStyle(0xe8d0a0, 1);
        g.fillCircle(cx + r * 0.25, cy - r * 0.95, r * 0.07);
        g.fillStyle(0xffe066, 1);
        g.fillCircle(cx - r * 0.8, cy - r * 0.18, r * 0.07);
        break;
      }
      case 'rustantler': {
        // great elk: heavy brown body, shaggy cream mane, long legs, huge branching antlers glowing ember-red
        g.lineStyle(3, C.ink, 1);
        g.fillStyle(0x5a3020, 1);
        for (const lx of [-0.45, -0.15, 0.3, 0.6]) {
          g.fillRect(cx + lx * r - r * 0.07, cy + r * 0.3, r * 0.14, r * 0.55);
          g.strokeRect(cx + lx * r - r * 0.07, cy + r * 0.3, r * 0.14, r * 0.55);
        }
        this.orbKeep(g, cx + r * 0.1, cy + r * 0.15, r * 1.6, r * 0.9, color);
        g.fillStyle(0xe8d0a0, 1);
        g.fillEllipse(cx - r * 0.45, cy + r * 0.05, r * 0.55, r * 0.7);
        this.orbKeep(g, cx - r * 0.75, cy - r * 0.3, r * 0.6, r * 0.42, color);
        g.fillStyle(0x3a2014, 1);
        g.fillCircle(cx - r * 1.02, cy - r * 0.25, r * 0.08);
        g.fillStyle(0xffd040, 1);
        g.fillCircle(cx - r * 0.78, cy - r * 0.38, r * 0.07);
        // antlers: two branching sweeps, glowing
        for (const side of [-1, 1]) {
          const bx = cx - r * 0.65 + side * r * 0.12;
          const by = cy - r * 0.48;
          g.lineStyle(r * 0.16, 0xffb050, 0.35);
          g.lineBetween(bx, by, bx + side * r * 0.35, by - r * 0.55);
          g.lineStyle(r * 0.08, 0xd8501a, 1);
          g.lineBetween(bx, by, bx + side * r * 0.35, by - r * 0.55);
          g.lineBetween(bx + side * r * 0.12, by - r * 0.2, bx - side * r * 0.08, by - r * 0.45);
          g.lineBetween(bx + side * r * 0.25, by - r * 0.4, bx + side * r * 0.55, by - r * 0.5);
          g.lineBetween(bx + side * r * 0.35, by - r * 0.55, bx + side * r * 0.3, by - r * 0.8);
          g.fillStyle(0xffe08a, 1);
          g.fillCircle(bx + side * r * 0.3, by - r * 0.8, r * 0.05);
          g.fillCircle(bx + side * r * 0.55, by - r * 0.5, r * 0.05);
        }
        // a few falling leaves around it
        g.fillStyle(0xe87a1a, 1);
        g.fillEllipse(cx + r * 0.7, cy - r * 0.55, r * 0.18, r * 0.1);
        g.fillStyle(0xc83a1a, 1);
        g.fillEllipse(cx + r * 0.45, cy - r * 0.8, r * 0.16, r * 0.09);
        break;
      }
      case 'glowbearer': {
        // tortoise: domed patterned shell, stubby legs, a bamboo pole with a glowing paper lantern
        g.lineStyle(2.5, C.ink, 1);
        g.fillStyle(0x8a9a6a, 1);
        for (const [lx, ly] of [[-0.55, 0.45], [0.45, 0.45], [-0.35, 0.6], [0.25, 0.6]]) g.fillCircle(cx + lx * r, cy + ly * r, r * 0.16);
        g.fillCircle(cx - r * 0.95, cy + r * 0.15, r * 0.25);
        g.strokeCircle(cx - r * 0.95, cy + r * 0.15, r * 0.25);
        this.orbKeep(g, cx, cy + r * 0.1, r * 1.6, r * 1.0, color);
        g.lineStyle(1.5, 0x3a5a3a, 1);
        for (const [hx, hy] of [[-0.35, 0], [0.05, -0.12], [0.4, 0.05], [-0.1, 0.3], [0.25, 0.32]]) g.strokeCircle(cx + hx * r, cy + hy * r, r * 0.17);
        g.fillStyle(0x111111, 1);
        g.fillCircle(cx - r * 1.05, cy + r * 0.08, r * 0.06);
        // pole and lantern
        g.lineStyle(2, 0x8a6a3a, 1);
        g.lineBetween(cx + r * 0.3, cy - r * 0.3, cx + r * 0.3, cy - r * 1.1);
        g.lineBetween(cx + r * 0.3, cy - r * 1.1, cx + r * 0.75, cy - r * 1.1);
        g.fillStyle(0xffd27a, 0.35);
        g.fillCircle(cx + r * 0.75, cy - r * 0.8, r * 0.42);
        g.fillStyle(0xf0e0b0, 1);
        g.fillRoundedRect(cx + r * 0.58, cy - r * 1.0, r * 0.34, r * 0.42, r * 0.1);
        g.lineStyle(1.5, C.ink, 1);
        g.strokeRoundedRect(cx + r * 0.58, cy - r * 1.0, r * 0.34, r * 0.42, r * 0.1);
        g.fillStyle(0xd84a2a, 1);
        g.fillRect(cx + r * 0.58, cy - r * 1.02, r * 0.34, r * 0.06);
        break;
      }
      case 'veilwhisker': {
        // great fox spirit: tall pale body, pointed ears with violet tips, a huge misty tail, a glowing paper lantern in its jaws
        g.lineStyle(3, C.ink, 1);
        g.fillStyle(0xf4f4ff, 0.75);
        g.fillEllipse(cx + r * 0.85, cy - r * 0.25, r * 1.0, r * 0.6);
        g.fillStyle(0xffffff, 0.5);
        g.fillEllipse(cx + r * 1.1, cy - r * 0.5, r * 0.55, r * 0.35);
        g.fillStyle(0xc8c8e0, 1);
        for (const lx of [-0.35, -0.05, 0.3, 0.55]) {
          g.fillRect(cx + lx * r - r * 0.07, cy + r * 0.3, r * 0.14, r * 0.5);
          g.strokeRect(cx + lx * r - r * 0.07, cy + r * 0.3, r * 0.14, r * 0.5);
        }
        this.orbKeep(g, cx + r * 0.1, cy + r * 0.1, r * 1.5, r * 0.8, color);
        g.fillEllipse(cx - r * 0.6, cy - r * 0.35, r * 0.75, r * 0.6);
        g.strokeEllipse(cx - r * 0.6, cy - r * 0.35, r * 0.75, r * 0.6);
        g.fillTriangle(cx - r * 0.85, cy - r * 0.55, cx - r * 0.62, cy - r * 0.62, cx - r * 0.8, cy - r * 1.15);
        g.fillTriangle(cx - r * 0.5, cy - r * 0.62, cx - r * 0.28, cy - r * 0.55, cx - r * 0.35, cy - r * 1.15);
        g.fillStyle(0x9a7ae8, 1);
        g.fillTriangle(cx - r * 0.82, cy - r * 0.95, cx - r * 0.76, cy - r * 0.97, cx - r * 0.8, cy - r * 1.15);
        g.fillTriangle(cx - r * 0.36, cy - r * 0.97, cx - r * 0.31, cy - r * 0.95, cx - r * 0.35, cy - r * 1.15);
        g.fillStyle(0xffb040, 1);
        g.fillCircle(cx - r * 0.75, cy - r * 0.42, r * 0.07);
        g.fillCircle(cx - r * 0.48, cy - r * 0.42, r * 0.07);
        // lantern hanging from the jaws
        g.lineStyle(1.5, 0x5a4a3a, 1);
        g.lineBetween(cx - r * 0.85, cy - r * 0.15, cx - r * 0.95, cy + r * 0.05);
        g.fillStyle(0xffd27a, 0.35);
        g.fillCircle(cx - r * 0.95, cy + r * 0.3, r * 0.4);
        g.fillStyle(0xf0e0b0, 1);
        g.fillRoundedRect(cx - r * 1.12, cy + r * 0.05, r * 0.34, r * 0.46, r * 0.1);
        g.lineStyle(1.5, C.ink, 1);
        g.strokeRoundedRect(cx - r * 1.12, cy + r * 0.05, r * 0.34, r * 0.46, r * 0.1);
        g.fillStyle(0xd84a2a, 1);
        g.fillRect(cx - r * 1.12, cy + r * 0.03, r * 0.34, r * 0.06);
        g.fillRect(cx - r * 1.12, cy + r * 0.48, r * 0.34, r * 0.05);
        break;
      }
      case 'crownmane': {
        // great red-maned ape: shaggy mane, long arms on the ground, pale face, crown of green vines with gold blossoms
        g.lineStyle(3, C.ink, 1);
        g.fillStyle(0x8a3a1a, 1);
        for (const sx of [-1, 1]) {
          g.fillEllipse(cx + sx * r * 0.85, cy + r * 0.35, r * 0.4, r * 0.95);
          g.strokeEllipse(cx + sx * r * 0.85, cy + r * 0.35, r * 0.4, r * 0.95);
        }
        this.orbKeep(g, cx, cy + r * 0.2, r * 1.5, r * 1.25, color);
        // mane: a ring of shaggy tufts around the head
        g.fillStyle(0xd86a2a, 1);
        for (let k = 0; k < 9; k++) {
          const a = Math.PI * (0.9 + (k / 8) * 1.2);
          g.fillCircle(cx + Math.cos(a) * r * 0.55, cy - r * 0.35 + Math.sin(a) * r * 0.5, r * 0.22);
        }
        g.fillCircle(cx, cy - r * 0.35, r * 0.5);
        g.strokeCircle(cx, cy - r * 0.35, r * 0.52);
        // face
        g.fillStyle(0xe8c8a0, 1);
        g.fillEllipse(cx, cy - r * 0.28, r * 0.6, r * 0.55);
        g.lineStyle(1.5, C.ink, 1);
        g.strokeEllipse(cx, cy - r * 0.28, r * 0.6, r * 0.55);
        g.fillStyle(C.ink, 1);
        g.fillCircle(cx - r * 0.13, cy - r * 0.36, r * 0.06);
        g.fillCircle(cx + r * 0.13, cy - r * 0.36, r * 0.06);
        g.fillEllipse(cx, cy - r * 0.15, r * 0.22, r * 0.1);
        // vine crown with gold blossoms
        g.lineStyle(4, 0x3a8a3a, 1);
        g.beginPath();
        g.arc(cx, cy - r * 0.45, r * 0.42, Math.PI * 1.15, Math.PI * 1.85);
        g.strokePath();
        g.fillStyle(0x4aa04a, 1);
        for (const lx of [-0.3, 0, 0.3]) g.fillTriangle(cx + lx * r - r * 0.08, cy - r * 0.78, cx + lx * r + r * 0.08, cy - r * 0.78, cx + lx * r, cy - r * 1.02);
        g.fillStyle(0xffd040, 1);
        for (const lx of [-0.36, -0.12, 0.12, 0.36]) g.fillCircle(cx + lx * r, cy - r * 0.8 + Math.abs(lx) * r * 0.25, r * 0.06);
        break;
      }
      case 'waxback': {
        // round beetle under a thick glossy wax coat with drips, little dark legs and antennae
        g.lineStyle(2.5, C.ink, 1);
        g.fillStyle(0x3a2a1a, 1);
        for (const [lx, ly] of [[-0.75, -0.3], [-0.85, 0.2], [-0.6, 0.6], [0.75, -0.3], [0.85, 0.2], [0.6, 0.6]]) g.fillRect(cx + lx * r - r * 0.14, cy + ly * r - r * 0.05, r * 0.28, r * 0.1);
        g.fillCircle(cx, cy - r * 0.75, r * 0.3);
        g.lineStyle(1.5, C.ink, 1);
        g.lineBetween(cx - r * 0.12, cy - r * 0.95, cx - r * 0.35, cy - r * 1.25);
        g.lineBetween(cx + r * 0.12, cy - r * 0.95, cx + r * 0.35, cy - r * 1.25);
        g.lineStyle(2.5, C.ink, 1);
        this.orbKeep(g, cx, cy + r * 0.05, r * 1.5, r * 1.6, color);
        g.lineStyle(1.5, 0xa87a30, 1);
        g.lineBetween(cx, cy - r * 0.7, cx, cy + r * 0.8);
        g.fillStyle(0xfff0b0, 0.7);
        g.fillEllipse(cx - r * 0.3, cy - r * 0.3, r * 0.35, r * 0.55);
        g.fillStyle(0xf0c860, 1);
        for (const dx of [-0.45, 0.2, 0.5]) g.fillEllipse(cx + dx * r, cy + r * 0.8, r * 0.16, r * 0.3);
        break;
      }
      case 'hexguard': {
        // striped wasp from above with clear wings, holding a six-sided comb shield in front
        g.lineStyle(2, C.ink, 1);
        g.fillStyle(0xe8f4ff, 0.6);
        g.fillEllipse(cx - r * 0.55, cy - r * 0.35, r * 0.8, r * 0.45);
        g.fillEllipse(cx + r * 0.55, cy - r * 0.35, r * 0.8, r * 0.45);
        g.strokeEllipse(cx - r * 0.55, cy - r * 0.35, r * 0.8, r * 0.45);
        g.strokeEllipse(cx + r * 0.55, cy - r * 0.35, r * 0.8, r * 0.45);
        this.orbKeep(g, cx, cy + r * 0.25, r * 0.7, r * 1.2, color);
        g.fillStyle(0x1a1208, 1);
        for (const dy of [0.05, 0.4]) g.fillRect(cx - r * 0.33, cy + dy * r, r * 0.66, r * 0.14);
        g.fillCircle(cx, cy - r * 0.45, r * 0.3);
        // comb shield
        const pts: { x: number; y: number }[] = [];
        for (let n = 0; n < 6; n++) pts.push({ x: cx + r * 0.55 + Math.cos((n * Math.PI) / 3) * r * 0.42, y: cy - r * 0.05 + Math.sin((n * Math.PI) / 3) * r * 0.42 });
        g.fillStyle(0xe8b030, 1);
        g.fillPoints(pts, true);
        g.lineStyle(2, 0x8a5a10, 1);
        g.strokePoints(pts, true);
        g.lineStyle(1, 0x8a5a10, 0.8);
        g.lineBetween(pts[0].x, pts[0].y, pts[3].x, pts[3].y);
        break;
      }
      case 'honeypaw': {
        // round bear cub seen from above: brown body, little round ears, pale muzzle, golden honey dripping off its paws
        g.lineStyle(2.5, C.ink, 1);
        g.fillStyle(color, 1);
        for (const sx of [-1, 1]) {
          g.fillCircle(cx + sx * r * 0.7, cy + r * 0.35, r * 0.3);
          g.strokeCircle(cx + sx * r * 0.7, cy + r * 0.35, r * 0.3);
        }
        g.fillEllipse(cx, cy + r * 0.15, r * 1.4, r * 1.3);
        g.strokeEllipse(cx, cy + r * 0.15, r * 1.4, r * 1.3);
        g.fillCircle(cx, cy - r * 0.5, r * 0.5);
        g.strokeCircle(cx, cy - r * 0.5, r * 0.5);
        for (const sx of [-1, 1]) {
          g.fillCircle(cx + sx * r * 0.38, cy - r * 0.9, r * 0.17);
          g.strokeCircle(cx + sx * r * 0.38, cy - r * 0.9, r * 0.17);
        }
        g.fillStyle(0xd8b088, 1);
        g.fillEllipse(cx, cy - r * 0.35, r * 0.42, r * 0.3);
        g.fillStyle(C.ink, 1);
        g.fillCircle(cx, cy - r * 0.42, r * 0.07);
        g.fillCircle(cx - r * 0.2, cy - r * 0.62, r * 0.06);
        g.fillCircle(cx + r * 0.2, cy - r * 0.62, r * 0.06);
        g.fillStyle(0xf0b030, 1);
        for (const sx of [-1, 1]) {
          g.fillCircle(cx + sx * r * 0.7, cy + r * 0.45, r * 0.18);
          g.fillEllipse(cx + sx * r * 0.72, cy + r * 0.72, r * 0.1, r * 0.22);
        }
        break;
      }
      case 'combqueen': {
        // giant queen bee from above: long striped abdomen glazed with wax, four big wings, a crown of hexagonal comb
        g.lineStyle(3, C.ink, 1);
        g.fillStyle(0xe8f4ff, 0.55);
        for (const [wx, wy, ww, wh] of [[-0.75, -0.45, 1.0, 0.5], [0.75, -0.45, 1.0, 0.5], [-0.65, -0.05, 0.8, 0.4], [0.65, -0.05, 0.8, 0.4]]) {
          g.fillEllipse(cx + wx * r, cy + wy * r, ww * r, wh * r);
          g.strokeEllipse(cx + wx * r, cy + wy * r, ww * r, wh * r);
        }
        this.orbKeep(g, cx, cy + r * 0.4, r * 0.95, r * 1.4, color);
        g.fillStyle(0x1a1208, 1);
        for (const dy of [0.1, 0.42, 0.74]) g.fillRect(cx - r * 0.44, cy + dy * r, r * 0.88, r * 0.13);
        g.fillStyle(0xfff0b0, 0.55);
        g.fillEllipse(cx - r * 0.2, cy + r * 0.2, r * 0.22, r * 0.6);
        g.fillStyle(0x3a2a10, 1);
        g.fillCircle(cx, cy - r * 0.4, r * 0.36);
        g.strokeCircle(cx, cy - r * 0.4, r * 0.36);
        g.fillStyle(0x6a3a10, 1);
        g.fillCircle(cx - r * 0.16, cy - r * 0.48, r * 0.1);
        g.fillCircle(cx + r * 0.16, cy - r * 0.48, r * 0.1);
        // comb crown
        for (const k of [-1, 0, 1]) {
          const hx = cx + k * r * 0.2;
          const hy = cy - r * 0.86 + Math.abs(k) * r * 0.06;
          const pts: { x: number; y: number }[] = [];
          for (let n = 0; n < 6; n++) pts.push({ x: hx + Math.cos((n * Math.PI) / 3 + Math.PI / 6) * r * 0.12, y: hy + Math.sin((n * Math.PI) / 3 + Math.PI / 6) * r * 0.12 });
          g.fillStyle(0xffd040, 1);
          g.fillPoints(pts, true);
          g.lineStyle(1.5, 0x8a5a10, 1);
          g.strokePoints(pts, true);
        }
        break;
      }
      case 'lanternfrog': {
        // squat bog-frog from above: bumpy green body, big eyes, and a glowing bulb on a stalk curling over its head
        g.lineStyle(2.5, C.ink, 1);
        g.fillStyle(0x2a6a4a, 1);
        for (const sx of [-1, 1]) {
          g.fillEllipse(cx + sx * r * 0.75, cy + r * 0.5, r * 0.5, r * 0.32);
          g.strokeEllipse(cx + sx * r * 0.75, cy + r * 0.5, r * 0.5, r * 0.32);
        }
        this.orbKeep(g, cx, cy + r * 0.1, r * 1.5, r * 1.3, color);
        g.fillStyle(0x5aaa7a, 1);
        for (const [bx, by] of [[-0.3, 0.2], [0.35, 0.35], [0.1, -0.1], [-0.1, 0.5]]) g.fillCircle(cx + bx * r, cy + by * r, r * 0.08);
        for (const sx of [-1, 1]) {
          g.fillStyle(0xe8e8a0, 1);
          g.fillCircle(cx + sx * r * 0.38, cy - r * 0.45, r * 0.2);
          g.strokeCircle(cx + sx * r * 0.38, cy - r * 0.45, r * 0.2);
          g.fillStyle(C.ink, 1);
          g.fillCircle(cx + sx * r * 0.38, cy - r * 0.45, r * 0.08);
        }
        g.lineStyle(2, 0x2a5a3a, 1);
        g.lineBetween(cx, cy - r * 0.55, cx + r * 0.2, cy - r * 1.05);
        g.lineBetween(cx + r * 0.2, cy - r * 1.05, cx + r * 0.55, cy - r * 1.1);
        g.fillStyle(0xe8ff8a, 0.35);
        g.fillCircle(cx + r * 0.62, cy - r * 1.0, r * 0.38);
        g.fillStyle(0xf4ffb0, 1);
        g.fillCircle(cx + r * 0.62, cy - r * 1.0, r * 0.18);
        break;
      }
      case 'hexcroak': {
        // round purple toad with a puffed throat sac, warts and heavy-lidded yellow eyes
        g.lineStyle(2.5, C.ink, 1);
        this.orbKeep(g, cx, cy + r * 0.1, r * 1.5, r * 1.3, color);
        g.fillStyle(0xc8a0e8, 1);
        g.fillCircle(cx, cy + r * 0.35, r * 0.42);
        g.strokeCircle(cx, cy + r * 0.35, r * 0.42);
        g.fillStyle(0x4a2a5a, 1);
        for (const [bx, by] of [[-0.45, -0.1], [0.5, 0.05], [-0.2, -0.3], [0.25, -0.35]]) g.fillCircle(cx + bx * r, cy + by * r, r * 0.08);
        for (const sx of [-1, 1]) {
          g.fillStyle(0xf0d040, 0.35);
          g.fillCircle(cx + sx * r * 0.4, cy - r * 0.45, r * 0.28);
          g.fillStyle(0xf0d040, 1);
          g.fillCircle(cx + sx * r * 0.4, cy - r * 0.45, r * 0.18);
          g.fillStyle(color, 1);
          g.fillRect(cx + sx * r * 0.4 - r * 0.2, cy - r * 0.66, r * 0.4, r * 0.15);
          g.fillStyle(C.ink, 1);
          g.fillRect(cx + sx * r * 0.4 - r * 0.1, cy - r * 0.45, r * 0.2, r * 0.05);
        }
        // a glossy sheen on the throat sac and a faint green hex rune glowing on its back (design F27)
        g.fillStyle(0xffffff, 0.55);
        g.fillEllipse(cx - r * 0.14, cy + r * 0.22, r * 0.2, r * 0.12);
        g.lineStyle(1.5, 0x9aff7a, 0.85);
        const hx = cx + r * 0.42;
        const hy = cy - r * 0.02;
        g.beginPath();
        for (let k = 0; k <= 6; k++) {
          const a = (k / 6) * Math.PI * 2 + Math.PI / 6;
          const px = hx + Math.cos(a) * r * 0.16;
          const py = hy + Math.sin(a) * r * 0.16;
          if (k === 0) g.moveTo(px, py);
          else g.lineTo(px, py);
        }
        g.strokePath();
        g.fillStyle(0x9aff7a, 1);
        g.fillCircle(hx, hy, r * 0.04);
        break;
      }
      case 'mudskipper': {
        // a mud-brown fish propped on its front fins, with big goggling eyes on top and a wide grin
        g.lineStyle(2.5, C.ink, 1);
        g.fillStyle(0x6a5a3a, 1);
        g.fillTriangle(cx + r * 0.7, cy, cx + r * 1.25, cy - r * 0.35, cx + r * 1.25, cy + r * 0.35);
        g.strokeTriangle(cx + r * 0.7, cy, cx + r * 1.25, cy - r * 0.35, cx + r * 1.25, cy + r * 0.35);
        this.orbKeep(g, cx, cy, r * 1.7, r * 1.0, color);
        g.fillStyle(0x5a4a2a, 1);
        for (const sx of [-1, 1]) g.fillEllipse(cx - r * 0.2, cy + sx * r * 0.55, r * 0.45, r * 0.22);
        g.fillStyle(0x6a5a3a, 1);
        for (const [bx, by] of [[0.1, -0.15], [0.35, 0.15], [-0.05, 0.25]]) g.fillCircle(cx + bx * r, cy + by * r, r * 0.07);
        // a spiny dorsal fin along its back and a wet sheen of mud (design F27)
        g.fillStyle(0xd88a4a, 1);
        for (let k = 0; k < 4; k++) g.fillTriangle(cx - r * 0.05 + k * r * 0.18, cy - r * 0.05, cx + r * 0.12 + k * r * 0.18, cy - r * 0.05, cx + r * 0.04 + k * r * 0.18, cy - r * 0.32);
        g.fillStyle(0xffffff, 0.35);
        g.fillEllipse(cx + r * 0.2, cy - r * 0.25, r * 0.6, r * 0.12);
        for (const sx of [-1, 1]) {
          g.fillStyle(0xf0f0e0, 1);
          g.fillCircle(cx - r * 0.5, cy + sx * r * 0.22, r * 0.2);
          g.strokeCircle(cx - r * 0.5, cy + sx * r * 0.22, r * 0.2);
          g.fillStyle(C.ink, 1);
          g.fillCircle(cx - r * 0.56, cy + sx * r * 0.22, r * 0.09);
          g.fillStyle(0xffffff, 1);
          g.fillCircle(cx - r * 0.59, cy + sx * r * 0.22 - r * 0.04, r * 0.035);
        }
        g.lineStyle(1.5, C.ink, 1);
        g.beginPath();
        g.arc(cx - r * 0.72, cy, r * 0.22, Math.PI * 0.6, Math.PI * 1.4);
        g.strokePath();
        break;
      }
      case 'glowmaw': {
        // colossal anglerfrog from above: a wide dark-green body, warts, a huge grin, little arms,
        // and a tall stalk curling over her head to a blazing lantern bulb
        g.lineStyle(3, C.ink, 1);
        g.fillStyle(0x245a44, 1);
        for (const sx of [-1, 1]) {
          g.fillEllipse(cx + sx * r * 0.9, cy + r * 0.55, r * 0.6, r * 0.35);
          g.strokeEllipse(cx + sx * r * 0.9, cy + r * 0.55, r * 0.6, r * 0.35);
        }
        this.orbKeep(g, cx, cy + r * 0.15, r * 1.8, r * 1.4, color);
        g.fillStyle(0x5aaa7a, 1);
        for (const [bx, by] of [[-0.5, 0.3], [0.45, 0.45], [0.15, 0.6], [-0.2, -0.05], [0.6, 0.0]]) g.fillCircle(cx + bx * r, cy + by * r, r * 0.07);
        g.lineStyle(2, C.ink, 1);
        g.beginPath();
        g.arc(cx, cy - r * 0.05, r * 0.55, Math.PI * 0.15, Math.PI * 0.85);
        g.strokePath();
        for (const sx of [-1, 1]) {
          g.fillStyle(0xe8e8a0, 1);
          g.fillCircle(cx + sx * r * 0.4, cy - r * 0.4, r * 0.18);
          g.lineStyle(2, C.ink, 1);
          g.strokeCircle(cx + sx * r * 0.4, cy - r * 0.4, r * 0.18);
          g.fillStyle(C.ink, 1);
          g.fillCircle(cx + sx * r * 0.4, cy - r * 0.4, r * 0.07);
        }
        g.lineStyle(3, 0x1e4a34, 1);
        g.lineBetween(cx, cy - r * 0.5, cx + r * 0.25, cy - r * 1.05);
        g.lineBetween(cx + r * 0.25, cy - r * 1.05, cx + r * 0.7, cy - r * 1.15);
        g.fillStyle(0xe8ff8a, 0.3);
        g.fillCircle(cx + r * 0.78, cy - r * 1.02, r * 0.42);
        g.fillStyle(0xf4ffb0, 1);
        g.fillCircle(cx + r * 0.78, cy - r * 1.02, r * 0.2);
        g.fillStyle(0xffffff, 0.9);
        g.fillCircle(cx + r * 0.72, cy - r * 1.08, r * 0.06);
        break;
      }
      case 'tumblehog': {
        // a hedgehog curled inside a ball of dry thistle stems, its little face peeking out
        g.lineStyle(2.5, C.ink, 1);
        this.orbKeep(g, cx, cy, (r * 0.95) * 2, (r * 0.95) * 2, color);
        g.lineStyle(1.5, 0x8a6a30, 1);
        for (let n = 0; n < 6; n++) {
          const a = (n * Math.PI) / 3;
          g.lineBetween(cx + Math.cos(a) * r * 0.95, cy + Math.sin(a) * r * 0.95, cx - Math.cos(a) * r * 0.95, cy - Math.sin(a) * r * 0.95);
        }
        g.fillStyle(0x6a4a2a, 1);
        for (let n = 0; n < 8; n++) {
          const a = (n * Math.PI) / 4 + 0.2;
          g.fillTriangle(cx + Math.cos(a) * r * 0.9, cy + Math.sin(a) * r * 0.9, cx + Math.cos(a + 0.2) * r * 0.9, cy + Math.sin(a + 0.2) * r * 0.9, cx + Math.cos(a + 0.1) * r * 1.2, cy + Math.sin(a + 0.1) * r * 1.2);
        }
        g.fillStyle(0xe8d0a8, 1);
        g.fillCircle(cx - r * 0.25, cy + r * 0.15, r * 0.35);
        g.lineStyle(1.5, C.ink, 1);
        g.strokeCircle(cx - r * 0.25, cy + r * 0.15, r * 0.35);
        g.fillStyle(C.ink, 1);
        g.fillCircle(cx - r * 0.38, cy + r * 0.08, r * 0.06);
        g.fillCircle(cx - r * 0.12, cy + r * 0.08, r * 0.06);
        g.fillCircle(cx - r * 0.25, cy + r * 0.3, r * 0.07);
        break;
      }
      case 'bloomdoe': {
        // a slender prairie deer seen from above: fawn body with pale spots, long neck, big ears, a crown of purple thistle blooms
        g.lineStyle(2.5, C.ink, 1);
        // slim legs: ink first, then the fawn colour down the middle with dark little hooves (design F27)
        const legs = [-0.45, -0.15, 0.25, 0.5];
        g.lineStyle(r * 0.2, C.ink, 1);
        for (const lx of legs) g.lineBetween(cx + lx * r, cy + r * 0.3, cx + lx * r, cy + r * 0.82);
        g.lineStyle(r * 0.09, Phaser.Display.Color.IntegerToColor(color).lighten(8).color, 1);
        for (const lx of legs) g.lineBetween(cx + lx * r, cy + r * 0.3, cx + lx * r, cy + r * 0.74);
        g.lineStyle(2.5, C.ink, 1);
        this.orbKeep(g, cx + r * 0.05, cy + r * 0.1, r * 1.3, r * 0.75, color);
        g.fillStyle(0xfff4e8, 1);
        g.fillEllipse(cx + r * 0.68, cy + r * 0.0, r * 0.18, r * 0.2); // a white tail flag
        g.fillStyle(0xf0e0c8, 1);
        for (const [sx, sy] of [[0.2, -0.05], [0.4, 0.15], [-0.05, 0.2]]) g.fillCircle(cx + sx * r, cy + sy * r, r * 0.07);
        this.orbKeep(g, cx - r * 0.6, cy - r * 0.35, r * 0.5, r * 0.45, color);
        g.fillEllipse(cx - r * 0.85, cy - r * 0.6, r * 0.18, r * 0.35);
        g.fillEllipse(cx - r * 0.38, cy - r * 0.62, r * 0.18, r * 0.35);
        g.fillStyle(0xd8b8c8, 1);
        g.fillEllipse(cx - r * 0.85, cy - r * 0.6, r * 0.08, r * 0.2);
        g.fillEllipse(cx - r * 0.38, cy - r * 0.62, r * 0.08, r * 0.2);
        g.fillStyle(C.ink, 1);
        g.fillCircle(cx - r * 0.7, cy - r * 0.32, r * 0.05);
        g.fillCircle(cx - r * 0.82, cy - r * 0.22, r * 0.035);
        for (const [fx, fy] of [[-0.75, -0.75], [-0.55, -0.82], [-0.35, -0.75]]) {
          g.fillStyle(0x9a6ab8, 1);
          g.fillCircle(cx + fx * r, cy + fy * r, r * 0.12);
          g.fillStyle(0xd8b8f0, 1);
          g.fillCircle(cx + fx * r - r * 0.03, cy + fy * r - r * 0.03, r * 0.05);
        }
        break;
      }
      case 'marmot': {
        // a plump marmot from above, sitting up: round brown body, pale belly, small round ears, a dark nose
        g.lineStyle(2.5, C.ink, 1);
        this.orbKeep(g, cx, cy + r * 0.2, r * 1.3, r * 1.2, color);
        g.fillStyle(0xe8d0a8, 1);
        g.fillEllipse(cx, cy + r * 0.3, r * 0.75, r * 0.8);
        this.orbKeep(g, cx, cy - r * 0.5, (r * 0.45) * 2, (r * 0.45) * 2, color);
        for (const sx of [-1, 1]) {
          g.fillCircle(cx + sx * r * 0.35, cy - r * 0.85, r * 0.13);
          g.strokeCircle(cx + sx * r * 0.35, cy - r * 0.85, r * 0.13);
        }
        g.fillStyle(0xe8d0a8, 1);
        g.fillEllipse(cx, cy - r * 0.38, r * 0.4, r * 0.25);
        g.fillStyle(C.ink, 1);
        g.fillCircle(cx, cy - r * 0.45, r * 0.07);
        g.fillCircle(cx - r * 0.18, cy - r * 0.6, r * 0.055);
        g.fillCircle(cx + r * 0.18, cy - r * 0.6, r * 0.055);
        g.fillStyle(0x8a5a3a, 1);
        for (const sx of [-1, 1]) g.fillEllipse(cx + sx * r * 0.25, cy - r * 0.05, r * 0.15, r * 0.25);
        break;
      }
      case 'galestag': {
        // a colossal elk from above: long tawny body, pale rump, a shaggy dark neck-mane,
        // and wide branching antlers grown through with purple thistle blooms
        g.lineStyle(3, C.ink, 1);
        g.fillStyle(0x6a4a2a, 1);
        for (const lx of [-0.55, -0.2, 0.35, 0.65]) {
          g.fillRect(cx + lx * r - r * 0.07, cy + r * 0.3, r * 0.14, r * 0.55);
          g.strokeRect(cx + lx * r - r * 0.07, cy + r * 0.3, r * 0.14, r * 0.55);
        }
        this.orbKeep(g, cx + r * 0.1, cy + r * 0.1, r * 1.6, r * 0.85, color);
        g.fillStyle(0xe8d8b8, 1);
        g.fillEllipse(cx + r * 0.75, cy + r * 0.1, r * 0.35, r * 0.5);
        g.fillStyle(0x5a3a22, 1);
        g.fillEllipse(cx - r * 0.5, cy - r * 0.05, r * 0.6, r * 0.7);
        this.orbKeep(g, cx - r * 0.75, cy - r * 0.35, r * 0.45, r * 0.4, color);
        g.fillStyle(C.ink, 1);
        g.fillCircle(cx - r * 0.85, cy - r * 0.38, r * 0.05);
        // antlers: two branching sprays with thistle heads at the tips
        g.lineStyle(3, 0xd8c8a0, 1);
        for (const sx of [-1, 1]) {
          const bx = cx - r * 0.7;
          const by = cy - r * 0.5;
          const tx = bx + sx * r * 0.55;
          const ty = by - r * 0.7;
          g.lineBetween(bx, by, tx, ty);
          g.lineBetween(bx + sx * r * 0.2, by - r * 0.25, bx + sx * r * 0.55, by - r * 0.15);
          g.lineBetween(bx + sx * r * 0.38, by - r * 0.5, bx + sx * r * 0.2, by - r * 0.85);
          for (const [px, py] of [[tx, ty], [bx + sx * r * 0.55, by - r * 0.15], [bx + sx * r * 0.2, by - r * 0.85]]) {
            g.fillStyle(0x9a6ab8, 1);
            g.fillCircle(px, py, r * 0.11);
            g.fillStyle(0xd8b8f0, 1);
            g.fillCircle(px - r * 0.03, py - r * 0.03, r * 0.045);
          }
        }
        break;
      }
      case 'titheweasel': {
        // a long sleek weasel in a green waistcoat, a tiny ledger under one arm
        g.lineStyle(2.5, C.ink, 1);
        this.orbKeep(g, cx + r * 0.5, cy + r * 0.2, r * 0.9, r * 0.35, color);
        g.fillEllipse(cx, cy, r * 1.4, r * 0.7);
        g.strokeEllipse(cx, cy, r * 1.4, r * 0.7);
        g.fillStyle(0x3a7a3a, 1);
        g.fillRect(cx - r * 0.35, cy - r * 0.3, r * 0.6, r * 0.6);
        this.orbKeep(g, cx - r * 0.7, cy - r * 0.15, (r * 0.35) * 2, (r * 0.35) * 2, color);
        g.fillStyle(0xf0e0c0, 1);
        g.fillEllipse(cx - r * 0.85, cy - r * 0.05, r * 0.25, r * 0.18);
        g.fillStyle(C.ink, 1);
        g.fillCircle(cx - r * 0.78, cy - r * 0.25, r * 0.06);
        g.fillStyle(0xf4ecd8, 1);
        g.fillRect(cx + r * 0.05, cy - r * 0.55, r * 0.35, r * 0.28);
        g.lineStyle(1, C.ink, 1);
        g.strokeRect(cx + r * 0.05, cy - r * 0.55, r * 0.35, r * 0.28);
        g.fillStyle(0xffd040, 1);
        g.fillCircle(cx + r * 0.5, cy - r * 0.45, r * 0.08);
        // ledger lines on its tally sheet, a bulging coin purse at its hip and a sly eye glint (design F28)
        g.lineStyle(0.8, 0x8a7a5a, 1);
        for (const ly of [-0.48, -0.41, -0.34]) g.lineBetween(cx + r * 0.1, cy + ly * r, cx + r * 0.35, cy + ly * r);
        g.fillStyle(0x8a5a2a, 1);
        g.lineStyle(1.5, C.ink, 1);
        g.fillCircle(cx + r * 0.45, cy + r * 0.25, r * 0.17);
        g.strokeCircle(cx + r * 0.45, cy + r * 0.25, r * 0.17);
        g.fillStyle(0xffd040, 1);
        g.fillCircle(cx + r * 0.45, cy + r * 0.08, r * 0.07);
        g.fillStyle(0xffffff, 1);
        g.fillCircle(cx - r * 0.8, cy - r * 0.27, r * 0.025);
        break;
      }
      case 'ploughox': {
        // a broad ox from above: big brown body, a pale muzzle, curved horns and a wooden yoke across the shoulders
        g.lineStyle(3, C.ink, 1);
        this.orbKeep(g, cx + r * 0.1, cy + r * 0.05, r * 1.6, r * 1.1, color);
        g.fillStyle(0x6a4a2a, 1);
        g.fillRect(cx - r * 0.45, cy - r * 0.6, r * 0.18, r * 1.2);
        g.lineStyle(2, C.ink, 1);
        g.strokeRect(cx - r * 0.45, cy - r * 0.6, r * 0.18, r * 1.2);
        this.orbKeep(g, cx - r * 0.75, cy, r * 0.55, r * 0.6, color);
        g.fillStyle(0xe8d0b0, 1);
        g.fillEllipse(cx - r * 0.95, cy, r * 0.25, r * 0.35);
        g.lineStyle(3, 0xf0e8d0, 1);
        g.beginPath();
        g.arc(cx - r * 0.7, cy - r * 0.32, r * 0.22, Math.PI * 1.1, Math.PI * 1.9);
        g.strokePath();
        g.beginPath();
        g.arc(cx - r * 0.7, cy + r * 0.32, r * 0.22, Math.PI * 0.1, Math.PI * 0.9);
        g.strokePath();
        g.fillStyle(C.ink, 1);
        g.fillCircle(cx - r * 0.75, cy - r * 0.15, r * 0.05);
        g.fillCircle(cx - r * 0.75, cy + r * 0.15, r * 0.05);
        // a brass nose ring, a lit flank and a little bell hanging from the yoke (design F28)
        g.lineStyle(1.5, 0xe8b04a, 1);
        g.strokeCircle(cx - r * 1.06, cy, r * 0.08);
        g.fillStyle(0xffffff, 0.22);
        g.fillEllipse(cx + r * 0.15, cy - r * 0.32, r * 0.9, r * 0.25);
        g.fillStyle(0xf0c040, 1);
        g.fillCircle(cx - r * 0.42, cy + r * 0.55, r * 0.1);
        g.fillStyle(0x8a6a1a, 1);
        g.fillCircle(cx - r * 0.42, cy + r * 0.6, r * 0.03);
        break;
      }
      case 'collie': {
        // a black-and-white sheepdog mid-dash: long body, white collar and blaze, flicking tail, one ear up
        g.lineStyle(2.5, C.ink, 1);
        this.orbKeep(g, cx + r * 0.85, cy - r * 0.1, r * 0.6, r * 0.25, color);
        for (const lx of [-0.45, -0.15, 0.3, 0.55]) {
          g.fillRect(cx + lx * r - r * 0.06, cy + r * 0.2, r * 0.12, r * 0.45);
          g.strokeRect(cx + lx * r - r * 0.06, cy + r * 0.2, r * 0.12, r * 0.45);
        }
        g.fillEllipse(cx + r * 0.05, cy, r * 1.3, r * 0.6);
        g.strokeEllipse(cx + r * 0.05, cy, r * 1.3, r * 0.6);
        g.fillStyle(0xf4f0e8, 1);
        g.fillEllipse(cx - r * 0.45, cy + r * 0.05, r * 0.35, r * 0.5);
        this.orbKeep(g, cx - r * 0.75, cy - r * 0.25, r * 0.5, r * 0.4, color);
        g.fillStyle(0xf4f0e8, 1);
        g.fillRect(cx - r * 0.8, cy - r * 0.42, r * 0.08, r * 0.3);
        g.fillEllipse(cx - r * 0.98, cy - r * 0.18, r * 0.2, r * 0.15);
        g.fillStyle(color, 1);
        g.fillTriangle(cx - r * 0.65, cy - r * 0.4, cx - r * 0.5, cy - r * 0.4, cx - r * 0.55, cy - r * 0.7);
        g.fillStyle(C.ink, 1);
        g.fillCircle(cx - r * 0.85, cy - r * 0.3, r * 0.05);
        g.fillCircle(cx - r * 1.05, cy - r * 0.2, r * 0.05);
        // a bright eye, a pink lolling tongue, a red neckerchief and a white tail tip (design F28)
        g.fillStyle(0xffffff, 1);
        g.fillCircle(cx - r * 0.86, cy - r * 0.32, r * 0.022);
        g.fillStyle(0xff8aa0, 1);
        g.fillEllipse(cx - r * 0.98, cy - r * 0.04, r * 0.08, r * 0.14);
        g.fillStyle(0xd83a3a, 1);
        g.fillTriangle(cx - r * 0.62, cy - r * 0.12, cx - r * 0.38, cy - r * 0.1, cx - r * 0.5, cy + r * 0.12);
        g.fillStyle(0xf4f0e8, 1);
        g.fillCircle(cx + r * 0.92, cy - r * 0.12, r * 0.1);
        break;
      }
      case 'ironhorn': {
        // a colossal bull from above: massive dark-brown shoulders, a wheat garland, iron-capped horns and a brass nose ring
        g.lineStyle(3, C.ink, 1);
        this.orbKeep(g, cx + r * 0.2, cy + r * 0.05, r * 1.6, r * 1.15, color);
        g.fillStyle(0x4a2414, 1);
        g.fillEllipse(cx - r * 0.25, cy, r * 0.8, r * 1.0);
        g.fillStyle(0xd8b050, 1);
        for (let n = 0; n < 7; n++) {
          const a = -Math.PI / 2 + (n / 6) * Math.PI;
          g.fillEllipse(cx - r * 0.35 + Math.cos(a) * r * 0.15, cy + Math.sin(a) * r * 0.45, r * 0.14, r * 0.22);
        }
        this.orbKeep(g, cx - r * 0.75, cy, r * 0.55, r * 0.6, color);
        g.fillStyle(0xd8a888, 1);
        g.fillEllipse(cx - r * 0.98, cy, r * 0.2, r * 0.32);
        g.lineStyle(2, 0xd8a840, 1);
        g.strokeCircle(cx - r * 1.05, cy, r * 0.09);
        for (const sy of [-1, 1]) {
          g.lineStyle(4, 0xe8e0c8, 1);
          g.lineBetween(cx - r * 0.7, cy + sy * r * 0.25, cx - r * 0.55, cy + sy * r * 0.6);
          g.lineBetween(cx - r * 0.55, cy + sy * r * 0.6, cx - r * 0.75, cy + sy * r * 0.82);
          g.fillStyle(0x8a8a9a, 1);
          g.fillCircle(cx - r * 0.75, cy + sy * r * 0.82, r * 0.07);
        }
        g.fillStyle(C.ink, 1);
        g.fillCircle(cx - r * 0.78, cy - r * 0.15, r * 0.05);
        g.fillCircle(cx - r * 0.78, cy + r * 0.15, r * 0.05);
        break;
      }
      case 'rustcoil': {
        // a giant coiled rattlesnake from above: rust-red loops with dark diamond bands, a wedge head and a rattle
        g.lineStyle(3, C.ink, 1);
        for (const [rr, a0] of [[0.95, 0], [0.62, 0.5], [0.32, 1]] as const) {
          this.orbKeep(g, cx + r * 0.15, cy, (r * rr) * 2, (r * rr) * 2, color);
          g.fillStyle(0x5a2214, 1);
          for (let n = 0; n < 8; n++) {
            const a = a0 + (n / 8) * Math.PI * 2;
            g.fillTriangle(
              cx + r * 0.15 + Math.cos(a) * r * (rr - 0.12), cy + Math.sin(a) * r * (rr - 0.12),
              cx + r * 0.15 + Math.cos(a + 0.18) * r * (rr - 0.04), cy + Math.sin(a + 0.18) * r * (rr - 0.04),
              cx + r * 0.15 + Math.cos(a - 0.18) * r * (rr - 0.04), cy + Math.sin(a - 0.18) * r * (rr - 0.04),
            );
          }
        }
        g.fillStyle(0xe8c890, 1);
        for (let n = 0; n < 3; n++) g.fillEllipse(cx + r * 1.0 + n * r * 0.12, cy + r * 0.55, r * 0.14, r * 0.2);
        g.fillStyle(color, 1);
        g.fillTriangle(cx - r * 1.15, cy, cx - r * 0.6, cy - r * 0.32, cx - r * 0.6, cy + r * 0.32);
        g.strokeTriangle(cx - r * 1.15, cy, cx - r * 0.6, cy - r * 0.32, cx - r * 0.6, cy + r * 0.32);
        g.fillStyle(0xf0d040, 1);
        g.fillCircle(cx - r * 0.78, cy - r * 0.15, r * 0.07);
        g.fillCircle(cx - r * 0.78, cy + r * 0.15, r * 0.07);
        g.lineStyle(2, 0xd83030, 1);
        g.lineBetween(cx - r * 1.15, cy, cx - r * 1.32, cy - r * 0.08);
        g.lineBetween(cx - r * 1.15, cy, cx - r * 1.32, cy + r * 0.08);
        break;
      }
      case 'thunderfleece': {
        // a colossal ram from above: a great storm-cloud of fleece with darker billows, a craggy face,
        // horns curling round three times, and little sparks crackling in the wool
        g.lineStyle(3, C.ink, 1);
        g.fillStyle(0x8a8478, 1);
        for (const [fx, fy, fr] of [[0.1, 0, 0.75], [0.5, -0.4, 0.45], [0.5, 0.4, 0.45], [-0.15, -0.5, 0.4], [-0.15, 0.5, 0.4], [0.85, 0, 0.42]]) g.fillCircle(cx + fx * r, cy + fy * r, r * fr);
        g.fillStyle(color, 1);
        for (const [fx, fy, fr] of [[0.1, 0, 0.62], [0.5, -0.35, 0.36], [0.5, 0.35, 0.36], [-0.12, -0.42, 0.3], [-0.12, 0.42, 0.3], [0.8, 0, 0.32]]) g.fillCircle(cx + fx * r, cy + fy * r, r * fr);
        g.strokeCircle(cx + r * 0.1, cy, r * 0.92);
        g.fillStyle(0xe0d8cc, 1);
        for (const [fx, fy] of [[0.2, -0.2], [0.45, 0.15], [0, 0.25], [0.65, -0.15]]) g.fillCircle(cx + fx * r, cy + fy * r, r * 0.12);
        g.fillStyle(0x2e2a28, 1);
        g.fillEllipse(cx - r * 0.85, cy, r * 0.5, r * 0.4);
        g.lineStyle(5, 0xa89068, 1);
        for (const sy of [-1, 1]) {
          for (const [rr, a1] of [[0.32, 0.9], [0.2, 0.85], [0.1, 0.8]] as const) {
            g.beginPath();
            g.arc(cx - r * 0.68, cy + sy * r * 0.36, r * rr, 0, Math.PI * 2 * a1);
            g.strokePath();
          }
        }
        g.fillStyle(0xf0d040, 1);
        g.fillCircle(cx - r * 0.98, cy - r * 0.1, r * 0.05);
        g.fillCircle(cx - r * 0.98, cy + r * 0.1, r * 0.05);
        g.lineStyle(2, 0xfff0a0, 1);
        for (const [sx, sy] of [[0.3, -0.6], [0.7, 0.45], [-0.1, 0.55]]) {
          g.lineBetween(cx + sx * r, cy + sy * r, cx + sx * r + 4, cy + sy * r + 5);
          g.lineBetween(cx + sx * r + 4, cy + sy * r + 5, cx + sx * r, cy + sy * r + 9);
        }
        break;
      }
      case 'mossback': {
        // a huge snapping turtle from above: a domed shell plated in moss with reeds and a flower growing on it,
        // a hooked beak, stubby clawed legs and a ridged tail
        g.lineStyle(3, C.ink, 1);
        g.fillStyle(0x6a6a4a, 1);
        for (const [lx, ly] of [[-0.55, -0.8], [-0.55, 0.8], [0.55, -0.8], [0.55, 0.8]]) {
          g.fillEllipse(cx + lx * r, cy + ly * r * 0.85, r * 0.42, r * 0.32);
          g.strokeEllipse(cx + lx * r, cy + ly * r * 0.85, r * 0.42, r * 0.32);
        }
        g.fillTriangle(cx + r * 0.9, cy - r * 0.15, cx + r * 0.9, cy + r * 0.15, cx + r * 1.35, cy);
        g.fillCircle(cx - r * 1.0, cy, r * 0.32);
        g.strokeCircle(cx - r * 1.0, cy, r * 0.32);
        g.fillStyle(0x4a4a30, 1);
        g.fillTriangle(cx - r * 1.28, cy - r * 0.1, cx - r * 1.28, cy + r * 0.1, cx - r * 1.42, cy + r * 0.12);
        g.fillStyle(0xf0d040, 1);
        g.fillCircle(cx - r * 1.08, cy - r * 0.14, r * 0.06);
        g.fillCircle(cx - r * 1.08, cy + r * 0.14, r * 0.06);
        g.fillStyle(color, 1);
        g.fillEllipse(cx, cy, r * 1.9, r * 1.55);
        g.lineStyle(3, C.ink, 1);
        g.strokeEllipse(cx, cy, r * 1.9, r * 1.55);
        g.lineStyle(2, 0x3a5a2a, 1);
        g.strokeEllipse(cx, cy, r * 0.8, r * 0.65);
        for (let k = 0; k < 6; k++) {
          const a = (k / 6) * Math.PI * 2;
          g.lineBetween(cx + Math.cos(a) * r * 0.4, cy + Math.sin(a) * r * 0.33, cx + Math.cos(a) * r * 0.95, cy + Math.sin(a) * r * 0.77);
        }
        g.fillStyle(0x7aaa4a, 1);
        for (const [mx, my, mr] of [[-0.4, -0.35, 0.22], [0.3, 0.35, 0.2], [0.45, -0.3, 0.16], [-0.25, 0.4, 0.14]]) g.fillCircle(cx + mx * r, cy + my * r, r * mr);
        g.lineStyle(2, 0x3a7a3a, 1);
        for (const k of [-1, 0, 1]) g.lineBetween(cx + r * 0.1 + k * 4, cy - r * 0.05, cx + r * 0.15 + k * 6, cy - r * 0.45);
        g.fillStyle(0xf08aa8, 1);
        g.fillCircle(cx - r * 0.1, cy + r * 0.1, r * 0.09);
        g.fillStyle(0xffe070, 1);
        g.fillCircle(cx - r * 0.1, cy + r * 0.1, r * 0.04);
        break;
      }
      case 'sandburrow': {
        // a sandy gopher popping up: round body, little ears, huge orange buck teeth and digging claws
        g.lineStyle(2.5, C.ink, 1);
        this.orbKeep(g, cx, cy + r * 0.15, r * 1.3, r * 1.2, color);
        g.fillCircle(cx, cy - r * 0.45, r * 0.45);
        g.strokeCircle(cx, cy - r * 0.45, r * 0.45);
        for (const sx of [-1, 1]) {
          g.fillCircle(cx + sx * r * 0.32, cy - r * 0.82, r * 0.12);
          g.strokeCircle(cx + sx * r * 0.32, cy - r * 0.82, r * 0.12);
        }
        g.fillStyle(0xf0dcb0, 1);
        g.fillEllipse(cx, cy + r * 0.25, r * 0.7, r * 0.75);
        g.fillStyle(0xf0a040, 1);
        g.fillRect(cx - r * 0.12, cy - r * 0.3, r * 0.1, r * 0.2);
        g.fillRect(cx + r * 0.02, cy - r * 0.3, r * 0.1, r * 0.2);
        g.fillStyle(C.ink, 1);
        g.fillCircle(cx - r * 0.18, cy - r * 0.55, r * 0.06);
        g.fillCircle(cx + r * 0.18, cy - r * 0.55, r * 0.06);
        g.fillCircle(cx, cy - r * 0.4, r * 0.06);
        g.fillStyle(0xe8d8c8, 1);
        for (const sx of [-1, 1]) g.fillEllipse(cx + sx * r * 0.6, cy + r * 0.1, r * 0.2, r * 0.14);
        break;
      }
      case 'curlshell': {
        // an armadillo from above: banded grey-brown shell, small pointed head with big ears, and a ringed tail
        g.lineStyle(2.5, C.ink, 1);
        g.fillStyle(0x8a6a4a, 1);
        g.fillEllipse(cx + r * 0.85, cy + r * 0.05, r * 0.6, r * 0.2);
        g.strokeEllipse(cx + r * 0.85, cy + r * 0.05, r * 0.6, r * 0.2);
        this.orbKeep(g, cx + r * 0.05, cy, r * 1.35, r * 1.0, color);
        g.lineStyle(1.5, 0x6a5a3a, 1);
        for (const dx of [-0.3, -0.05, 0.2, 0.45]) g.lineBetween(cx + dx * r, cy - r * 0.45, cx + dx * r, cy + r * 0.45);
        g.lineStyle(2.5, C.ink, 1);
        g.fillStyle(0xc8a888, 1);
        g.fillTriangle(cx - r * 0.55, cy - r * 0.22, cx - r * 0.55, cy + r * 0.22, cx - r * 1.1, cy);
        g.strokeTriangle(cx - r * 0.55, cy - r * 0.22, cx - r * 0.55, cy + r * 0.22, cx - r * 1.1, cy);
        g.fillEllipse(cx - r * 0.6, cy - r * 0.35, r * 0.18, r * 0.28);
        g.fillEllipse(cx - r * 0.6, cy + r * 0.35, r * 0.18, r * 0.28);
        g.fillStyle(C.ink, 1);
        g.fillCircle(cx - r * 0.8, cy - r * 0.08, r * 0.05);
        break;
      }
      case 'rattler': {
        // a coiled desert snake from above: banded sandy body in an S, a diamond head, a little segmented rattle
        g.lineStyle(r * 0.5, C.ink, 1);
        g.beginPath();
        g.moveTo(cx + r * 0.9, cy + r * 0.4);
        g.lineTo(cx + r * 0.3, cy + r * 0.5);
        g.lineTo(cx - r * 0.1, cy + r * 0.1);
        g.lineTo(cx + r * 0.3, cy - r * 0.3);
        g.lineTo(cx - r * 0.4, cy - r * 0.45);
        g.strokePath();
        g.lineStyle(r * 0.36, color, 1);
        g.beginPath();
        g.moveTo(cx + r * 0.9, cy + r * 0.4);
        g.lineTo(cx + r * 0.3, cy + r * 0.5);
        g.lineTo(cx - r * 0.1, cy + r * 0.1);
        g.lineTo(cx + r * 0.3, cy - r * 0.3);
        g.lineTo(cx - r * 0.4, cy - r * 0.45);
        g.strokePath();
        g.fillStyle(0x6a4a2a, 1);
        for (const [bx, by] of [[0.55, 0.45], [0.1, 0.3], [0.1, -0.1], [-0.05, -0.38]]) g.fillCircle(cx + bx * r, cy + by * r, r * 0.08);
        g.lineStyle(2, C.ink, 1);
        g.fillStyle(color, 1);
        g.fillTriangle(cx - r * 0.35, cy - r * 0.62, cx - r * 0.35, cy - r * 0.28, cx - r * 0.85, cy - r * 0.45);
        g.strokeTriangle(cx - r * 0.35, cy - r * 0.62, cx - r * 0.35, cy - r * 0.28, cx - r * 0.85, cy - r * 0.45);
        g.fillStyle(C.ink, 1);
        g.fillCircle(cx - r * 0.55, cy - r * 0.52, r * 0.05);
        g.fillStyle(0xe8d0a0, 1);
        for (let n = 0; n < 3; n++) g.fillEllipse(cx + r * (0.98 + n * 0.12), cy + r * 0.38, r * 0.12, r * 0.18);
        break;
      }
      case 'moonhare': {
        // a silver hare from above: long body, two long black-tipped ears laid back, and pale moon eyes
        g.lineStyle(2.5, C.ink, 1);
        this.orbKeep(g, cx + r * 0.15, cy, r * 1.5, r * 0.85, color);
        g.fillStyle(0xffffff, 1);
        g.fillCircle(cx + r * 0.95, cy, r * 0.22);
        this.orbKeep(g, cx - r * 0.65, cy, (r * 0.38) * 2, (r * 0.38) * 2, color);
        // long laid-back ears: thin outlines so the slim ears stay silver, pink insides, black tips (design F29)
        g.lineStyle(1.5, C.ink, 1);
        for (const sy of [-1, 1]) {
          g.fillStyle(color, 1);
          g.fillEllipse(cx - r * 0.2, cy + sy * r * 0.32, r * 0.95, r * 0.24);
          g.strokeEllipse(cx - r * 0.2, cy + sy * r * 0.32, r * 0.95, r * 0.24);
          g.fillStyle(0xf0c0cc, 1);
          g.fillEllipse(cx - r * 0.25, cy + sy * r * 0.32, r * 0.6, r * 0.08);
          g.fillStyle(0x3a3a48, 1);
          g.fillEllipse(cx + r * 0.2, cy + sy * r * 0.32, r * 0.16, r * 0.14);
        }
        g.lineStyle(2.5, C.ink, 1);
        g.fillStyle(0xffffff, 0.35);
        g.fillEllipse(cx + r * 0.1, cy - r * 0.22, r * 0.9, r * 0.15); // moonlight along its back
        g.fillStyle(0xf0f0b0, 1);
        g.fillCircle(cx - r * 0.78, cy - r * 0.16, r * 0.09);
        g.fillCircle(cx - r * 0.78, cy + r * 0.16, r * 0.09);
        g.fillStyle(0xe8a8b8, 1);
        g.fillCircle(cx - r * 1.02, cy, r * 0.06);
        break;
      }
      case 'heathwisp': {
        // a pale floating light: a soft glow, a bright core and a trailing wisp
        g.fillStyle(color, 0.25);
        g.fillCircle(cx, cy, r * 1.15);
        g.fillStyle(color, 0.5);
        g.fillCircle(cx, cy, r * 0.8);
        g.fillStyle(0xffffff, 1);
        g.fillCircle(cx, cy, r * 0.45);
        g.fillStyle(color, 0.6);
        g.fillTriangle(cx + r * 0.3, cy - r * 0.35, cx + r * 0.3, cy + r * 0.35, cx + r * 1.4, cy + r * 0.2);
        g.fillStyle(0x6a7aa8, 1);
        g.fillCircle(cx - r * 0.15, cy - r * 0.12, r * 0.08);
        g.fillCircle(cx - r * 0.15, cy + r * 0.12, r * 0.08);
        break;
      }
      case 'moorram': {
        // a shaggy ram from above: a big cloud of fleece, a dark face and two curled horns
        g.lineStyle(2.5, C.ink, 1);
        g.fillStyle(color, 1);
        for (const [fx, fy, fr] of [[0, 0, 0.62], [0.3, -0.3, 0.38], [0.3, 0.3, 0.38], [-0.15, -0.38, 0.32], [-0.15, 0.38, 0.32], [0.55, 0, 0.32]]) g.fillCircle(cx + fx * r, cy + fy * r, r * fr);
        g.strokeCircle(cx, cy, r * 0.75);
        g.fillStyle(0xe0d8cc, 1);
        for (const [fx, fy] of [[0.1, -0.15], [0.35, 0.1], [-0.05, 0.2]]) g.fillCircle(cx + fx * r, cy + fy * r, r * 0.16);
        g.fillStyle(0x3a3430, 1);
        g.fillEllipse(cx - r * 0.75, cy, r * 0.45, r * 0.36);
        g.lineStyle(4, 0xa89068, 1);
        for (const sy of [-1, 1]) {
          g.beginPath();
          g.arc(cx - r * 0.62, cy + sy * r * 0.3, r * 0.22, 0, Math.PI * 2 * 0.8);
          g.strokePath();
        }
        g.fillStyle(0xf0d040, 1);
        g.fillCircle(cx - r * 0.85, cy - r * 0.09, r * 0.05);
        g.fillCircle(cx - r * 0.85, cy + r * 0.09, r * 0.05);
        // horn ridges and a lit top-left of the fleece, shade on the lower right, a sprig of heather caught in it (design F29)
        g.lineStyle(1, 0x6a5838, 1);
        for (const sy of [-1, 1]) for (const a of [0.6, 1.5, 2.4]) g.lineBetween(cx - r * 0.62 + Math.cos(a) * r * 0.15, cy + sy * r * 0.3 + Math.sin(a) * r * 0.15, cx - r * 0.62 + Math.cos(a) * r * 0.28, cy + sy * r * 0.3 + Math.sin(a) * r * 0.28);
        g.fillStyle(0xffffff, 0.3);
        g.fillCircle(cx + r * 0.05, cy - r * 0.3, r * 0.22);
        g.fillStyle(0x000000, 0.12);
        g.fillCircle(cx + r * 0.4, cy + r * 0.35, r * 0.25);
        g.fillStyle(0xb06ab8, 1);
        for (const [hx, hy] of [[0.45, -0.45], [0.52, -0.38], [0.4, -0.36]]) g.fillCircle(cx + hx * r, cy + hy * r, r * 0.05);
        break;
      }
      case 'bubbler': {
        // a spotted newt from above: long tail, splayed little legs and a puffed pale throat, with a bubble at its mouth
        g.lineStyle(2.5, C.ink, 1);
        g.fillStyle(color, 1);
        g.fillTriangle(cx + r * 0.4, cy - r * 0.2, cx + r * 0.4, cy + r * 0.2, cx + r * 1.25, cy + r * 0.05);
        g.fillEllipse(cx, cy, r * 1.4, r * 0.8);
        g.strokeEllipse(cx, cy, r * 1.4, r * 0.8);
        for (const [lx, ly] of [[-0.35, -1], [-0.35, 1], [0.3, -1], [0.3, 1]]) {
          g.lineStyle(3, color, 1);
          g.lineBetween(cx + lx * r, cy + ly * r * 0.3, cx + lx * r - r * 0.12, cy + ly * r * 0.62);
        }
        g.fillStyle(color, 1);
        g.fillCircle(cx - r * 0.75, cy, r * 0.38);
        g.lineStyle(2.5, C.ink, 1);
        g.strokeCircle(cx - r * 0.75, cy, r * 0.38);
        g.fillStyle(0xe8f0b0, 1);
        g.fillCircle(cx - r * 0.95, cy, r * 0.2);
        g.fillStyle(0xf0a040, 1);
        for (const [sx, sy] of [[-0.1, -0.15], [0.25, 0.12], [0.05, 0.2], [0.45, -0.1]]) g.fillCircle(cx + sx * r, cy + sy * r, r * 0.08);
        g.fillStyle(C.ink, 1);
        g.fillCircle(cx - r * 0.8, cy - r * 0.2, r * 0.07);
        g.fillCircle(cx - r * 0.8, cy + r * 0.2, r * 0.07);
        g.fillStyle(0xc8f0ff, 0.6);
        g.fillCircle(cx - r * 1.35, cy - r * 0.15, r * 0.22);
        g.lineStyle(1.5, 0xffffff, 0.9);
        g.strokeCircle(cx - r * 1.35, cy - r * 0.15, r * 0.22);
        break;
      }
      case 'sprayotter': {
        // a sleek brown otter from above: long body, pale face, thick tapering tail and droplets flying off
        g.lineStyle(2.5, C.ink, 1);
        g.fillStyle(color, 1);
        g.fillTriangle(cx + r * 0.5, cy - r * 0.25, cx + r * 0.5, cy + r * 0.25, cx + r * 1.3, cy);
        g.strokeTriangle(cx + r * 0.5, cy - r * 0.25, cx + r * 0.5, cy + r * 0.25, cx + r * 1.3, cy);
        for (const [lx, ly] of [[-0.4, -1], [-0.4, 1], [0.35, -1], [0.35, 1]]) g.fillEllipse(cx + lx * r, cy + ly * r * 0.45, r * 0.22, r * 0.18);
        this.orbKeep(g, cx, cy, r * 1.5, r * 0.85, color);
        g.fillStyle(0xffffff, 0.35);
        g.fillEllipse(cx + r * 0.1, cy - r * 0.2, r * 0.9, r * 0.12); // wet sheen along its back (design F29)
        this.orbKeep(g, cx - r * 0.8, cy, r * 0.84, r * 0.84, color);
        g.fillStyle(0xe8d0a8, 1);
        g.fillEllipse(cx - r * 0.98, cy, r * 0.32, r * 0.42);
        g.fillStyle(C.ink, 1);
        g.fillCircle(cx - r * 0.82, cy - r * 0.18, r * 0.07);
        g.fillCircle(cx - r * 0.82, cy + r * 0.18, r * 0.07);
        g.fillCircle(cx - r * 1.12, cy, r * 0.08);
        g.fillStyle(0x6a4a2a, 1);
        g.fillCircle(cx - r * 0.75, cy - r * 0.38, r * 0.09);
        g.fillCircle(cx - r * 0.75, cy + r * 0.38, r * 0.09);
        g.fillStyle(0xc8ecff, 0.9);
        for (const [wx, wy] of [[0.2, -0.75], [-0.3, 0.8], [0.8, 0.6], [0.7, -0.6]]) g.fillCircle(cx + wx * r, cy + wy * r, r * 0.09);
        // whiskers and eye glints
        g.lineStyle(1, 0xfff4e0, 0.9);
        for (const sy of [-1, 1]) for (const k of [0, 1]) g.lineBetween(cx - r * 1.1, cy + sy * r * 0.05, cx - r * 1.35, cy + sy * r * (0.12 + k * 0.12));
        g.fillStyle(0xffffff, 1);
        g.fillCircle(cx - r * 0.84, cy - r * 0.2, r * 0.025);
        g.fillCircle(cx - r * 0.84, cy + r * 0.16, r * 0.025);
        break;
      }
      case 'pike': {
        // a long steel-blue fish from above: pointed snout, banded back, forked tail and a fringe of white water
        g.lineStyle(2.5, C.ink, 1);
        g.fillStyle(color, 1);
        g.fillTriangle(cx + r * 0.75, cy, cx + r * 1.25, cy - r * 0.42, cx + r * 1.25, cy + r * 0.42);
        g.strokeTriangle(cx + r * 0.75, cy, cx + r * 1.25, cy - r * 0.42, cx + r * 1.25, cy + r * 0.42);
        g.fillEllipse(cx, cy, r * 1.9, r * 0.62);
        g.strokeEllipse(cx, cy, r * 1.9, r * 0.62);
        g.fillTriangle(cx - r * 0.9, cy - r * 0.15, cx - r * 0.9, cy + r * 0.15, cx - r * 1.3, cy);
        g.fillStyle(0x3a5a78, 1);
        for (let k = 0; k < 4; k++) g.fillEllipse(cx - r * 0.35 + k * r * 0.3, cy, r * 0.12, r * 0.45);
        g.fillStyle(0xc8d8b0, 1);
        g.fillTriangle(cx + r * 0.1, cy - r * 0.3, cx + r * 0.35, cy - r * 0.3, cx + r * 0.25, cy - r * 0.55);
        g.fillTriangle(cx + r * 0.1, cy + r * 0.3, cx + r * 0.35, cy + r * 0.3, cx + r * 0.25, cy + r * 0.55);
        g.fillStyle(0xf0d040, 1);
        g.fillCircle(cx - r * 0.75, cy - r * 0.13, r * 0.08);
        g.fillCircle(cx - r * 0.75, cy + r * 0.13, r * 0.08);
        g.fillStyle(0xe8fbff, 0.8);
        for (const [wx, wy] of [[1.35, -0.55], [1.45, 0.5], [1.55, 0]]) g.fillCircle(cx + wx * r, cy + wy * r, r * 0.1);
        break;
      }
      case 'harrier': {
        // hawk from above: broad rust wings with dark tips, pale speckled breast, hooked yellow beak
        g.lineStyle(2.5, C.ink, 1);
        g.fillStyle(color, 1);
        g.fillTriangle(cx - r * 0.2, cy - r * 0.1, cx - r * 1.4, cy - r * 0.45, cx - r * 0.25, cy + r * 0.3);
        g.fillTriangle(cx + r * 0.2, cy - r * 0.1, cx + r * 1.4, cy - r * 0.45, cx + r * 0.25, cy + r * 0.3);
        g.strokeTriangle(cx - r * 0.2, cy - r * 0.1, cx - r * 1.4, cy - r * 0.45, cx - r * 0.25, cy + r * 0.3);
        g.strokeTriangle(cx + r * 0.2, cy - r * 0.1, cx + r * 1.4, cy - r * 0.45, cx + r * 0.25, cy + r * 0.3);
        g.fillStyle(0x3a2418, 1);
        g.fillTriangle(cx - r * 1.4, cy - r * 0.45, cx - r * 1.05, cy - r * 0.4, cx - r * 1.1, cy - r * 0.2);
        g.fillTriangle(cx + r * 1.4, cy - r * 0.45, cx + r * 1.05, cy - r * 0.4, cx + r * 1.1, cy - r * 0.2);
        // pale feather bars across each wing and a lit leading edge (design F26)
        g.lineStyle(1, 0xe8c8a0, 0.6);
        for (const sd of [-1, 1]) for (const t of [0.5, 0.78]) g.lineBetween(cx + sd * r * (0.2 + t * 1.2), cy - r * (0.1 + t * 0.35), cx + sd * r * (0.25 + t * 0.85), cy + r * (0.3 - t * 0.45));
        g.lineStyle(1.5, 0xffe8c8, 0.7);
        g.lineBetween(cx - r * 0.25, cy - r * 0.12, cx - r * 1.3, cy - r * 0.44);
        g.lineBetween(cx + r * 0.25, cy - r * 0.12, cx + r * 1.3, cy - r * 0.44);
        g.lineStyle(2.5, C.ink, 1);
        g.fillStyle(0xe8d8b8, 1);
        g.fillEllipse(cx, cy, r * 0.6, r * 1.1);
        g.strokeEllipse(cx, cy, r * 0.6, r * 1.1);
        g.fillStyle(0x8a5a3a, 1);
        for (const [sx, sy] of [[-0.1, 0], [0.1, 0.2], [-0.05, 0.3]]) g.fillCircle(cx + sx * r, cy + sy * r, r * 0.05);
        g.fillStyle(color, 1);
        g.fillTriangle(cx - r * 0.2, cy + r * 0.5, cx + r * 0.2, cy + r * 0.5, cx, cy + r * 0.85);
        g.fillCircle(cx, cy - r * 0.6, r * 0.28);
        g.strokeCircle(cx, cy - r * 0.6, r * 0.28);
        g.fillStyle(0xf0c040, 1);
        g.fillTriangle(cx - r * 0.08, cy - r * 0.82, cx + r * 0.08, cy - r * 0.82, cx, cy - r * 1.0);
        g.fillStyle(0x111111, 1);
        g.fillCircle(cx - r * 0.1, cy - r * 0.66, r * 0.05);
        g.fillCircle(cx + r * 0.1, cy - r * 0.66, r * 0.05);
        break;
      }
      case 'howler': {
        // howler monkey: shaggy brown body, dark face, long curling tail, wide-open shouting mouth
        g.lineStyle(2.5, color, 1);
        g.beginPath();
        g.arc(cx + r * 0.75, cy - r * 0.1, r * 0.5, Math.PI * 0.6, Math.PI * 2.1);
        g.strokePath();
        g.lineStyle(2.5, C.ink, 1);
        this.orbKeep(g, cx + r * 0.05, cy + r * 0.15, r * 1.2, r * 1.1, color);
        this.orbKeep(g, cx - r * 0.45, cy - r * 0.4, r * 0.96, r * 0.96, color);
        // shaggy tufts on its crown and back, a bearded throat, and sound rings bursting from its howl (design F26)
        g.fillStyle(Phaser.Display.Color.IntegerToColor(color).lighten(12).color, 1);
        for (const [tx, ty] of [[-0.6, -0.85], [-0.35, -0.9], [0.3, -0.35], [0.55, -0.2]]) g.fillTriangle(cx + tx * r - r * 0.08, cy + ty * r + r * 0.12, cx + tx * r + r * 0.08, cy + ty * r + r * 0.12, cx + tx * r, cy + ty * r - r * 0.06);
        g.fillStyle(0x2a1a14, 1);
        g.fillEllipse(cx - r * 0.55, cy - r * 0.35, r * 0.55, r * 0.6);
        g.fillStyle(Phaser.Display.Color.IntegerToColor(color).darken(15).color, 1);
        g.fillTriangle(cx - r * 0.75, cy - r * 0.1, cx - r * 0.35, cy - r * 0.1, cx - r * 0.55, cy + r * 0.2);
        g.fillStyle(0xd84a3a, 1);
        g.fillEllipse(cx - r * 0.58, cy - r * 0.15, r * 0.24, r * 0.2);
        g.fillStyle(0xffd040, 1);
        g.fillCircle(cx - r * 0.7, cy - r * 0.48, r * 0.07);
        g.fillCircle(cx - r * 0.42, cy - r * 0.48, r * 0.07);
        g.fillStyle(0xffffff, 1);
        g.fillCircle(cx - r * 0.72, cy - r * 0.51, r * 0.025);
        g.fillCircle(cx - r * 0.44, cy - r * 0.51, r * 0.025);
        g.lineStyle(1.5, 0xfff4d6, 0.8);
        for (const rr of [0.25, 0.42]) {
          g.beginPath();
          g.arc(cx - r * 0.95, cy - r * 0.15, r * rr, Math.PI * 0.75, Math.PI * 1.25);
          g.strokePath();
        }
        break;
      }
      case 'mourner': {
        // ringtail lemur: soft grey body, white face mask with dark eye patches, big black-and-white ringed tail
        const tx = cx + r * 0.6;
        for (let k = 0; k < 6; k++) {
          g.fillStyle(k % 2 ? 0x222222 : 0xf4f4f4, 1);
          g.fillCircle(tx + k * r * 0.12, cy - r * 0.15 - k * r * 0.16, r * 0.17);
        }
        g.lineStyle(2.5, C.ink, 1);
        this.orbKeep(g, cx, cy + r * 0.2, r * 1.2, r * 1.0, color);
        // fluffy cheeks either side of a shaded head (design F26)
        g.fillStyle(0xd8d8e0, 1);
        g.fillCircle(cx - r * 0.85, cy - r * 0.22, r * 0.16);
        g.fillCircle(cx - r * 0.18, cy - r * 0.22, r * 0.16);
        this.orbKeep(g, cx - r * 0.5, cy - r * 0.35, r * 0.84, r * 0.84, color);
        g.fillStyle(0xf4f4f4, 1);
        g.fillEllipse(cx - r * 0.6, cy - r * 0.3, r * 0.45, r * 0.38);
        g.fillStyle(0x222222, 1);
        g.fillCircle(cx - r * 0.72, cy - r * 0.38, r * 0.11);
        g.fillCircle(cx - r * 0.48, cy - r * 0.38, r * 0.11);
        g.fillStyle(0xffb040, 1);
        g.fillCircle(cx - r * 0.72, cy - r * 0.38, r * 0.05);
        g.fillCircle(cx - r * 0.48, cy - r * 0.38, r * 0.05);
        g.fillStyle(0xffffff, 1);
        g.fillCircle(cx - r * 0.74, cy - r * 0.4, r * 0.02);
        g.fillCircle(cx - r * 0.5, cy - r * 0.4, r * 0.02);
        g.fillStyle(0x222222, 1);
        g.fillCircle(cx - r * 0.85, cy - r * 0.2, r * 0.06);
        // a single pale tear on its cheek: the Mourner weeps as it walks
        g.fillStyle(0x9ad8ff, 1);
        g.fillCircle(cx - r * 0.74, cy - r * 0.2, r * 0.04);
        g.fillTriangle(cx - r * 0.77, cy - r * 0.21, cx - r * 0.71, cy - r * 0.21, cx - r * 0.74, cy - r * 0.29);
        break;
      }
      case 'mistfox': {
        // pale fox spirit: slim body, big pointed ears, a long wisp of a tail, glowing amber eyes
        g.lineStyle(2.5, C.ink, 1);
        g.fillStyle(0xeef0ff, 0.9);
        g.fillEllipse(cx + r * 0.95, cy - r * 0.05, r * 0.95, r * 0.42);
        g.fillStyle(0xffffff, 0.6);
        g.fillEllipse(cx + r * 1.25, cy - r * 0.2, r * 0.45, r * 0.25);
        this.orbKeep(g, cx, cy + r * 0.15, r * 1.3, r * 0.7, color);
        this.orbKeep(g, cx - r * 0.7, cy - r * 0.15, r * 0.84, r * 0.84, color);
        // pale ears with lavender insides (the ears are too slim to outline), drawn over the shaded head (design F24)
        g.lineStyle(1.5, C.ink, 1);
        g.fillStyle(color, 1);
        g.fillTriangle(cx - r * 0.95, cy - r * 0.35, cx - r * 0.75, cy - r * 0.45, cx - r * 0.9, cy - r * 0.9);
        g.fillTriangle(cx - r * 0.6, cy - r * 0.45, cx - r * 0.4, cy - r * 0.35, cx - r * 0.45, cy - r * 0.9);
        g.fillStyle(0xc8b8e8, 1);
        g.fillTriangle(cx - r * 0.88, cy - r * 0.42, cx - r * 0.8, cy - r * 0.45, cx - r * 0.88, cy - r * 0.72);
        g.fillTriangle(cx - r * 0.55, cy - r * 0.45, cx - r * 0.47, cy - r * 0.42, cx - r * 0.5, cy - r * 0.72);
        // amber eyes glowing through the mist, and wisps curling off its tail
        g.fillStyle(0xffb040, 0.35);
        g.fillCircle(cx - r * 0.85, cy - r * 0.2, r * 0.14);
        g.fillCircle(cx - r * 0.6, cy - r * 0.2, r * 0.14);
        g.fillStyle(0xffb040, 1);
        g.fillCircle(cx - r * 0.85, cy - r * 0.2, r * 0.08);
        g.fillCircle(cx - r * 0.6, cy - r * 0.2, r * 0.08);
        g.fillStyle(0xffffff, 1);
        g.fillCircle(cx - r * 0.87, cy - r * 0.23, r * 0.03);
        g.fillCircle(cx - r * 0.62, cy - r * 0.23, r * 0.03);
        g.fillStyle(0x6a6a8a, 1);
        g.fillCircle(cx - r * 1.1, cy - r * 0.05, r * 0.06);
        g.fillStyle(0xeef0ff, 0.5);
        g.fillCircle(cx + r * 1.55, cy - r * 0.38, r * 0.12);
        g.fillCircle(cx + r * 1.72, cy - r * 0.52, r * 0.08);
        break;
      }
      case 'silkcrane': {
        // white crane: long legs, long neck, a red crown, black wingtips
        g.lineStyle(2, 0x3a3a3a, 1);
        g.lineBetween(cx - r * 0.1, cy + r * 0.3, cx - r * 0.2, cy + r * 0.95);
        g.lineBetween(cx + r * 0.2, cy + r * 0.3, cx + r * 0.3, cy + r * 0.95);
        g.lineStyle(2.5, C.ink, 1);
        this.orbKeep(g, cx + r * 0.1, cy + r * 0.05, r * 1.2, r * 0.7, color);
        g.fillStyle(0x1a1a1a, 1);
        g.fillTriangle(cx + r * 0.5, cy - r * 0.1, cx + r * 0.9, cy + r * 0.05, cx + r * 0.5, cy + r * 0.25);
        g.lineStyle(r * 0.18, color, 1);
        g.lineBetween(cx - r * 0.3, cy - r * 0.1, cx - r * 0.55, cy - r * 0.8);
        g.lineStyle(2.5, C.ink, 1);
        this.orbKeep(g, cx - r * 0.6, cy - r * 0.85, (r * 0.2) * 2, (r * 0.2) * 2, color);
        g.fillStyle(0xd83a3a, 1);
        g.fillCircle(cx - r * 0.6, cy - r * 0.98, r * 0.09);
        g.fillStyle(0xd8b040, 1);
        g.fillTriangle(cx - r * 0.75, cy - r * 0.88, cx - r * 0.75, cy - r * 0.8, cx - r * 1.15, cy - r * 0.82);
        g.fillStyle(0x111111, 1);
        g.fillCircle(cx - r * 0.65, cy - r * 0.88, r * 0.05);
        break;
      }
      case 'sapstoat': {
        // stoat: long low russet body, cream belly, black tail tip, bared amber teeth
        g.lineStyle(2.5, C.ink, 1);
        this.orbKeep(g, cx + r * 0.85, cy + r * 0.05, r * 0.9, r * 0.32, color);
        g.fillStyle(0x1a1a1a, 1);
        g.fillCircle(cx + r * 1.25, cy + r * 0.02, r * 0.17);
        this.orbKeep(g, cx, cy + r * 0.15, r * 1.6, r * 0.75, color);
        g.fillStyle(0xf0e0c0, 1);
        g.fillEllipse(cx - r * 0.1, cy + r * 0.35, r * 0.9, r * 0.28);
        this.orbKeep(g, cx - r * 0.8, cy - r * 0.15, (r * 0.42) * 2, (r * 0.42) * 2, color);
        g.fillCircle(cx - r * 0.65, cy - r * 0.55, r * 0.14);
        g.strokeCircle(cx - r * 0.65, cy - r * 0.55, r * 0.14);
        g.fillStyle(0xf0e0c0, 1);
        g.fillEllipse(cx - r * 1.0, cy + r * 0.05, r * 0.4, r * 0.22);
        g.fillStyle(0xf0b040, 1);
        g.fillTriangle(cx - r * 1.12, cy + r * 0.1, cx - r * 1.02, cy + r * 0.1, cx - r * 1.07, cy + r * 0.28);
        g.fillTriangle(cx - r * 0.95, cy + r * 0.1, cx - r * 0.85, cy + r * 0.1, cx - r * 0.9, cy + r * 0.26);
        g.fillStyle(0x111111, 1);
        g.fillCircle(cx - r * 0.9, cy - r * 0.25, r * 0.08);
        g.fillCircle(cx - r * 1.18, cy - r * 0.06, r * 0.07);
        break;
      }
      case 'turnleaf': {
        // gecko: slim orange body, splayed toes, a big maple-leaf tail, round gold eye
        g.lineStyle(2.5, C.ink, 1);
        // leaf tail
        g.fillStyle(0xd84a1a, 1);
        const tx = cx + r * 0.95;
        const ty = cy + r * 0.1;
        g.fillTriangle(tx - r * 0.2, ty, tx + r * 0.5, ty - r * 0.55, tx + r * 0.35, ty);
        g.fillTriangle(tx - r * 0.2, ty, tx + r * 0.7, ty, tx + r * 0.35, ty + r * 0.2);
        g.fillTriangle(tx - r * 0.2, ty, tx + r * 0.5, ty + r * 0.55, tx + r * 0.35, ty);
        g.lineStyle(1.5, 0x8a2a0a, 1);
        g.lineBetween(tx - r * 0.2, ty, tx + r * 0.55, ty);
        g.lineStyle(2.5, C.ink, 1);
        this.orbKeep(g, cx, cy + r * 0.1, r * 1.4, r * 0.75, color);
        g.fillEllipse(cx - r * 0.75, cy - r * 0.1, r * 0.7, r * 0.55);
        g.strokeEllipse(cx - r * 0.75, cy - r * 0.1, r * 0.7, r * 0.55);
        // toes
        g.fillStyle(color, 1);
        for (const [fx, fy] of [[-0.35, 0.5], [0.35, 0.5], [-0.35, -0.3], [0.35, -0.3]]) {
          g.fillCircle(cx + fx * r, cy + fy * r, r * 0.13);
          g.strokeCircle(cx + fx * r, cy + fy * r, r * 0.13);
        }
        // spots
        g.fillStyle(0xf0c040, 1);
        g.fillCircle(cx - r * 0.1, cy, r * 0.1);
        g.fillCircle(cx + r * 0.3, cy + r * 0.2, r * 0.08);
        g.fillStyle(0xffd040, 1);
        g.fillCircle(cx - r * 0.85, cy - r * 0.2, r * 0.14);
        g.fillStyle(0x111111, 1);
        g.fillCircle(cx - r * 0.87, cy - r * 0.2, r * 0.06);
        break;
      }
      case 'powdermonkey': {
        // monkey with a curly tail, a striped sailor shirt, a black keg on its back with a lit fuse
        g.lineStyle(2.5, color, 1);
        g.beginPath();
        g.arc(cx + r * 0.6, cy + r * 0.5, r * 0.3, Math.PI, Math.PI * 2.4);
        g.strokePath();
        g.lineStyle(2.5, C.ink, 1);
        g.fillStyle(0x2a2a32, 1);
        g.fillRoundedRect(cx + r * 0.05, cy - r * 0.55, r * 0.75, r * 0.85, 4);
        g.strokeRoundedRect(cx + r * 0.05, cy - r * 0.55, r * 0.75, r * 0.85, 4);
        g.lineStyle(1.5, 0x8a8a92, 1);
        g.lineBetween(cx + r * 0.05, cy - r * 0.3, cx + r * 0.8, cy - r * 0.3);
        g.lineBetween(cx + r * 0.05, cy + r * 0.05, cx + r * 0.8, cy + r * 0.05);
        g.lineStyle(2, 0xc8a050, 1);
        g.lineBetween(cx + r * 0.45, cy - r * 0.55, cx + r * 0.6, cy - r * 0.85);
        g.fillStyle(0xffb040, 1);
        g.fillCircle(cx + r * 0.62, cy - r * 0.9, r * 0.1);
        g.lineStyle(2.5, C.ink, 1);
        g.fillStyle(0xe8e0d0, 1);
        g.fillEllipse(cx - r * 0.25, cy + r * 0.25, r * 0.8, r * 0.9);
        g.strokeEllipse(cx - r * 0.25, cy + r * 0.25, r * 0.8, r * 0.9);
        g.lineStyle(2, 0x3a5a9a, 1);
        g.lineBetween(cx - r * 0.6, cy + r * 0.1, cx + r * 0.1, cy + r * 0.1);
        g.lineBetween(cx - r * 0.6, cy + r * 0.4, cx + r * 0.1, cy + r * 0.4);
        g.lineStyle(2.5, C.ink, 1);
        this.orbKeep(g, cx - r * 0.3, cy - r * 0.35, (r * 0.38) * 2, (r * 0.38) * 2, color);
        g.fillStyle(0xe8c8a0, 1);
        g.fillEllipse(cx - r * 0.35, cy - r * 0.28, r * 0.45, r * 0.32);
        g.fillStyle(0x111111, 1);
        g.fillCircle(cx - r * 0.45, cy - r * 0.42, r * 0.06);
        g.fillCircle(cx - r * 0.22, cy - r * 0.42, r * 0.06);
        break;
      }
      case 'dreadmast': {
        // black ship hull with oars, a tall mast and a tattered black sail with a pale skull-less sigil, gun ports glowing
        g.lineStyle(3, C.ink, 1);
        for (const ox of [-0.7, -0.35, 0, 0.35, 0.7]) g.lineBetween(cx + ox * r, cy + r * 0.45, cx + ox * r - r * 0.12, cy + r * 0.95);
        g.fillStyle(color, 1);
        g.beginPath();
        g.moveTo(cx - r * 1.2, cy);
        g.lineTo(cx + r * 1.25, cy - r * 0.1);
        g.lineTo(cx + r * 0.95, cy + r * 0.55);
        g.lineTo(cx - r * 0.95, cy + r * 0.55);
        g.closePath();
        g.fillPath();
        g.strokePath();
        g.fillStyle(0xffb040, 1);
        for (const gx of [-0.6, -0.2, 0.2, 0.6]) g.fillRect(cx + gx * r - r * 0.07, cy + r * 0.18, r * 0.14, r * 0.12);
        g.lineStyle(4, 0x5a3a2a, 1);
        g.lineBetween(cx, cy, cx, cy - r * 1.3);
        g.fillStyle(0x1a1418, 1);
        g.lineStyle(2, C.ink, 1);
        g.fillTriangle(cx + r * 0.05, cy - r * 1.25, cx + r * 0.05, cy - r * 0.15, cx + r * 0.95, cy - r * 0.3);
        g.strokeTriangle(cx + r * 0.05, cy - r * 1.25, cx + r * 0.05, cy - r * 0.15, cx + r * 0.95, cy - r * 0.3);
        g.fillTriangle(cx - r * 0.05, cy - r * 1.1, cx - r * 0.05, cy - r * 0.2, cx - r * 0.75, cy - r * 0.3);
        g.strokeTriangle(cx - r * 0.05, cy - r * 1.1, cx - r * 0.05, cy - r * 0.2, cx - r * 0.75, cy - r * 0.3);
        g.fillStyle(0xe8e0c8, 1);
        g.fillCircle(cx + r * 0.35, cy - r * 0.62, r * 0.13);
        g.fillStyle(0x1a1418, 1);
        g.fillCircle(cx + r * 0.31, cy - r * 0.64, r * 0.035);
        g.fillCircle(cx + r * 0.39, cy - r * 0.64, r * 0.035);
        g.fillStyle(0xc83a3a, 1);
        g.fillTriangle(cx, cy - r * 1.3, cx, cy - r * 1.15, cx - r * 0.3, cy - r * 1.22);
        break;
      }
      case 'scourmaw': {
        // sand wyrm rearing out of a dune: segmented baked-clay body, a ring-toothed round maw, sand spray
        g.fillStyle(0xe0c088, 1);
        g.fillEllipse(cx + r * 0.3, cy + r * 0.85, r * 2.2, r * 0.6);
        g.lineStyle(3, C.ink, 1);
        g.fillStyle(color, 1);
        for (const [sx, sy, sr] of [[0.9, 0.55, 0.42], [0.55, 0.35, 0.5], [0.15, 0.05, 0.56], [-0.25, -0.3, 0.6]] as const) {
          g.fillCircle(cx + sx * r, cy + sy * r, sr * r);
          g.strokeCircle(cx + sx * r, cy + sy * r, sr * r);
        }
        g.lineStyle(2, 0x8a5a2a, 1);
        for (const [sx, sy, sr] of [[0.55, 0.35, 0.5], [0.15, 0.05, 0.56]] as const) {
          g.beginPath();
          g.arc(cx + sx * r, cy + sy * r, sr * r * 0.75, Math.PI * 0.9, Math.PI * 1.6);
          g.strokePath();
        }
        g.fillStyle(0x2a1010, 1);
        g.fillCircle(cx - r * 0.35, cy - r * 0.4, r * 0.36);
        g.fillStyle(0xf0e8d0, 1);
        for (let k = 0; k < 10; k++) {
          const a = (k / 10) * Math.PI * 2;
          const tx = cx - r * 0.35 + Math.cos(a) * r * 0.3;
          const ty = cy - r * 0.4 + Math.sin(a) * r * 0.3;
          g.fillTriangle(tx, ty, tx - Math.cos(a) * r * 0.12 + Math.sin(a) * r * 0.05, ty - Math.sin(a) * r * 0.12 - Math.cos(a) * r * 0.05, tx - Math.cos(a) * r * 0.12 - Math.sin(a) * r * 0.05, ty - Math.sin(a) * r * 0.12 + Math.cos(a) * r * 0.05);
        }
        g.fillStyle(0xffe066, 1);
        g.fillCircle(cx - r * 0.05, cy - r * 0.75, r * 0.07);
        g.fillCircle(cx - r * 0.65, cy - r * 0.8, r * 0.07);
        g.fillStyle(0xe0c088, 0.9);
        for (const [px, py] of [[1.3, 0.6], [1.45, 0.4], [-0.6, 0.85], [-0.8, 0.7]]) g.fillCircle(cx + px * r, cy + py * r, r * 0.08);
        break;
      }
      case 'thrumhorn': {
        // colossal storm bull: dark shaggy hump, huge forward horns crackling with sparks, a little thundercloud on its back
        g.lineStyle(3, C.ink, 1);
        for (const lx of [-0.65, -0.25, 0.3, 0.7]) g.lineBetween(cx + lx * r, cy + r * 0.35, cx + lx * r, cy + r * 1.0);
        this.orbKeep(g, cx + r * 0.15, cy, r * 1.75, r * 1.2, color);
        g.fillStyle(0x2a2a36, 1);
        g.fillEllipse(cx - r * 0.2, cy - r * 0.35, r * 1.0, r * 0.75);
        this.orbKeep(g, cx - r * 0.75, cy + r * 0.1, (r * 0.48) * 2, (r * 0.48) * 2, color);
        g.lineStyle(5, 0xe8e0c8, 1);
        g.beginPath();
        g.moveTo(cx - r * 1.0, cy - r * 0.15);
        g.lineTo(cx - r * 1.35, cy - r * 0.5);
        g.lineTo(cx - r * 1.2, cy - r * 0.85);
        g.strokePath();
        g.beginPath();
        g.moveTo(cx - r * 0.5, cy - r * 0.2);
        g.lineTo(cx - r * 0.3, cy - r * 0.6);
        g.lineTo(cx - r * 0.5, cy - r * 0.9);
        g.strokePath();
        g.fillStyle(0xfff07a, 1);
        for (const [sx, sy] of [[-1.25, -0.95], [-0.55, -1.0], [-1.45, -0.6]]) g.fillCircle(cx + sx * r, cy + sy * r, r * 0.07);
        g.fillStyle(0xffd84a, 1);
        g.fillCircle(cx - r * 0.9, cy + r * 0.02, r * 0.08);
        g.fillCircle(cx - r * 0.6, cy + r * 0.02, r * 0.08);
        g.fillStyle(0xd8dce8, 1);
        g.fillCircle(cx + r * 0.1, cy - r * 0.95, r * 0.22);
        g.fillCircle(cx + r * 0.38, cy - r * 1.02, r * 0.28);
        g.fillCircle(cx + r * 0.66, cy - r * 0.93, r * 0.2);
        g.fillStyle(0xfff07a, 1);
        g.fillTriangle(cx + r * 0.35, cy - r * 0.8, cx + r * 0.48, cy - r * 0.8, cx + r * 0.3, cy - r * 0.55);
        break;
      }
      case 'mawbloom': {
        // rotten heart-tree: a split trunk with a gaping maw, a crown of withered branches with bruised fruit, root feet
        g.lineStyle(3, C.ink, 1);
        for (const lx of [-0.75, -0.3, 0.3, 0.75]) g.lineBetween(cx + lx * r, cy + r * 0.55, cx + lx * r * 1.35, cy + r * 1.05);
        g.lineStyle(4, 0x4a2a2a, 1);
        for (const [x1, y1, x2, y2] of [[-0.3, -0.6, -0.95, -1.15], [0.3, -0.6, 0.95, -1.1], [0, -0.7, 0.1, -1.3], [-0.6, -0.9, -1.25, -0.8], [0.6, -0.85, 1.25, -0.75]]) g.lineBetween(cx + x1 * r, cy + y1 * r, cx + x2 * r, cy + y2 * r);
        g.lineStyle(3, C.ink, 1);
        g.fillStyle(color, 1);
        g.fillRoundedRect(cx - r * 0.85, cy - r * 0.75, r * 1.7, r * 1.4, 14);
        g.strokeRoundedRect(cx - r * 0.85, cy - r * 0.75, r * 1.7, r * 1.4, 14);
        g.lineStyle(2, 0x4a2430, 1);
        for (const lx of [-0.55, -0.2, 0.25, 0.6]) g.lineBetween(cx + lx * r, cy - r * 0.65, cx + lx * r * 0.9, cy + r * 0.5);
        g.fillStyle(0x1a0a10, 1);
        g.fillEllipse(cx, cy + r * 0.15, r * 0.9, r * 0.55);
        g.fillStyle(0xe8e0c8, 1);
        for (const tx of [-0.3, -0.1, 0.1, 0.3]) g.fillTriangle(cx + tx * r - r * 0.07, cy - r * 0.08, cx + tx * r + r * 0.07, cy - r * 0.08, cx + tx * r, cy + r * 0.1);
        g.fillStyle(0xc8ff6a, 1);
        g.fillCircle(cx - r * 0.32, cy - r * 0.35, r * 0.11);
        g.fillCircle(cx + r * 0.32, cy - r * 0.35, r * 0.11);
        g.fillStyle(0x8a3a6a, 1);
        for (const [fx, fy] of [[-0.95, -1.15], [0.95, -1.1], [0.1, -1.3], [-1.25, -0.8], [1.25, -0.75]]) g.fillCircle(cx + fx * r, cy + fy * r, r * 0.12);
        break;
      }
      case 'velumbra': {
        // shadow manta: vast dark wings, a long tail, a cluster of glowing eyes and a faint inner light
        g.lineStyle(3, C.ink, 1);
        g.lineBetween(cx, cy + r * 0.5, cx + r * 0.2, cy + r * 1.35);
        const wing = [
          new Phaser.Math.Vector2(cx, cy - r * 0.8),
          new Phaser.Math.Vector2(cx + r * 0.9, cy - r * 0.55),
          new Phaser.Math.Vector2(cx + r * 1.45, cy + r * 0.05),
          new Phaser.Math.Vector2(cx + r * 0.7, cy + r * 0.25),
          new Phaser.Math.Vector2(cx, cy + r * 0.65),
          new Phaser.Math.Vector2(cx - r * 0.7, cy + r * 0.25),
          new Phaser.Math.Vector2(cx - r * 1.45, cy + r * 0.05),
          new Phaser.Math.Vector2(cx - r * 0.9, cy - r * 0.55),
        ];
        g.fillStyle(color, 1);
        g.fillPoints(wing, true);
        g.strokePoints(wing, true);
        g.fillStyle(0x5a4a9a, 0.6);
        g.fillEllipse(cx, cy - r * 0.05, r * 0.9, r * 0.9);
        g.fillStyle(0x8a6ad8, 0.35);
        for (const sx of [-1, 1]) g.fillTriangle(cx + sx * r * 0.5, cy - r * 0.3, cx + sx * r * 1.3, cy + r * 0.02, cx + sx * r * 0.6, cy + r * 0.15);
        for (const [dx, dy, rr] of [[0, -0.2, 0.16], [-0.3, -0.05, 0.11], [0.3, -0.05, 0.11], [-0.15, 0.18, 0.08], [0.15, 0.18, 0.08], [0, -0.48, 0.07]]) {
          g.fillStyle(0x5ae8d0, 1);
          g.fillCircle(cx + dx * r, cy + dy * r, rr * r);
          g.fillStyle(0x0a0c1a, 1);
          g.fillCircle(cx + dx * r, cy + dy * r, rr * r * 0.45);
        }
        break;
      }
      case 'sparkeel': {
        // cave eel: a long S-curved glowing body, fin ridge, bright spots along its side, a little spark at the tail
        g.lineStyle(r * 0.75, C.ink, 1);
        g.beginPath();
        g.moveTo(cx - r * 1.1, cy - r * 0.1);
        g.lineTo(cx - r * 0.4, cy - r * 0.45);
        g.lineTo(cx + r * 0.3, cy + r * 0.2);
        g.lineTo(cx + r * 1.0, cy - r * 0.15);
        g.strokePath();
        g.lineStyle(r * 0.55, color, 1);
        g.beginPath();
        g.moveTo(cx - r * 1.1, cy - r * 0.1);
        g.lineTo(cx - r * 0.4, cy - r * 0.45);
        g.lineTo(cx + r * 0.3, cy + r * 0.2);
        g.lineTo(cx + r * 1.0, cy - r * 0.15);
        g.strokePath();
        // a lit stripe along the upper edge of the body, and glowing spots with soft halos (design F21)
        g.lineStyle(r * 0.14, 0xffffff, 0.35);
        g.beginPath();
        g.moveTo(cx - r * 1.05, cy - r * 0.22);
        g.lineTo(cx - r * 0.4, cy - r * 0.56);
        g.lineTo(cx + r * 0.3, cy + r * 0.08);
        g.lineTo(cx + r * 0.95, cy - r * 0.26);
        g.strokePath();
        for (const [dx, dy] of [[-0.75, -0.25], [-0.1, -0.12], [0.6, 0.05]]) {
          g.fillStyle(0xbff8ff, 0.35);
          g.fillCircle(cx + dx * r, cy + dy * r, r * 0.16);
          g.fillStyle(0xbff8ff, 1);
          g.fillCircle(cx + dx * r, cy + dy * r, r * 0.09);
        }
        g.fillStyle(0xffe066, 1);
        g.fillTriangle(cx + r * 1.0, cy - r * 0.15, cx + r * 1.35, cy - r * 0.5, cx + r * 1.2, cy - r * 0.05);
        g.fillStyle(0xffffff, 1);
        g.fillCircle(cx - r * 1.0, cy - r * 0.18, r * 0.12);
        g.fillStyle(0x111111, 1);
        g.fillCircle(cx - r * 1.0, cy - r * 0.18, r * 0.06);
        break;
      }
      case 'dimlantern': {
        // lantern jelly: a translucent violet bell, trailing tendrils, a dark lantern glowing faintly inside
        g.lineStyle(2, 0x8a6ad8, 0.9);
        for (const tx of [-0.5, -0.2, 0.15, 0.45]) {
          g.beginPath();
          g.moveTo(cx + tx * r, cy + r * 0.3);
          g.lineTo(cx + tx * r - r * 0.1, cy + r * 0.7);
          g.lineTo(cx + tx * r + r * 0.05, cy + r * 1.05);
          g.strokePath();
        }
        g.lineStyle(2.5, C.ink, 1);
        g.fillStyle(color, 0.9);
        g.beginPath();
        g.arc(cx, cy + r * 0.3, r * 0.9, Math.PI, 0, false);
        g.closePath();
        g.fillPath();
        g.strokePath();
        g.fillStyle(0xffe08a, 0.35);
        g.fillCircle(cx, cy - r * 0.05, r * 0.42);
        g.fillStyle(0x2a1a3a, 1);
        g.fillRoundedRect(cx - r * 0.2, cy - r * 0.3, r * 0.4, r * 0.5, 3);
        g.fillStyle(0xffd84a, 1);
        g.fillCircle(cx, cy - r * 0.05, r * 0.1);
        g.fillStyle(0xffffff, 0.4);
        g.fillEllipse(cx - r * 0.45, cy - r * 0.25, r * 0.25, r * 0.4);
        break;
      }
      case 'echowisp': {
        // echo wisp: a pale flame with a ghost of itself trailing behind
        g.fillStyle(color, 0.35);
        g.fillCircle(cx + r * 0.55, cy + r * 0.15, r * 0.55);
        g.fillTriangle(cx + r * 0.1, cy, cx + r * 1.0, cy, cx + r * 0.55, cy - r * 0.9);
        g.lineStyle(2, 0x6a7aa8, 1);
        g.fillStyle(color, 1);
        g.fillCircle(cx - r * 0.1, cy + r * 0.2, r * 0.6);
        g.fillTriangle(cx - r * 0.65, cy + r * 0.05, cx + r * 0.45, cy + r * 0.05, cx - r * 0.1, cy - r * 1.05);
        g.strokeCircle(cx - r * 0.1, cy + r * 0.2, r * 0.6);
        g.fillStyle(0x9ad8ff, 1);
        g.fillCircle(cx - r * 0.1, cy + r * 0.25, r * 0.28);
        g.fillStyle(0x111111, 1);
        g.fillCircle(cx - r * 0.28, cy + r * 0.1, r * 0.07);
        g.fillCircle(cx + r * 0.08, cy + r * 0.1, r * 0.07);
        break;
      }
      case 'grindmaw': {
        // engine titan: a riveted furnace body on piston legs, a glowing grate mouth, twin smokestacks and a big flywheel
        g.lineStyle(3, C.ink, 1);
        for (const lx of [-0.6, 0.6]) {
          g.fillStyle(0x7a7a84, 1);
          g.fillRect(cx + lx * r - r * 0.15, cy + r * 0.45, r * 0.3, r * 0.6);
          g.strokeRect(cx + lx * r - r * 0.15, cy + r * 0.45, r * 0.3, r * 0.6);
        }
        for (const sx of [-0.45, 0.45]) {
          g.fillStyle(0x5a5a64, 1);
          g.fillRect(cx + sx * r - r * 0.12, cy - r * 1.2, r * 0.24, r * 0.5);
          g.strokeRect(cx + sx * r - r * 0.12, cy - r * 1.2, r * 0.24, r * 0.5);
        }
        g.fillStyle(color, 1);
        g.fillRoundedRect(cx - r * 0.95, cy - r * 0.75, r * 1.9, r * 1.3, 10);
        g.strokeRoundedRect(cx - r * 0.95, cy - r * 0.75, r * 1.9, r * 1.3, 10);
        g.fillStyle(0x8a6a2a, 1);
        for (let k = 0; k < 10; k++) {
          const a0 = (k / 10) * Math.PI * 2;
          g.fillRect(cx + r * 0.95 + Math.cos(a0) * r * 0.42 - r * 0.07, cy - r * 0.1 + Math.sin(a0) * r * 0.42 - r * 0.07, r * 0.14, r * 0.14);
        }
        g.fillStyle(0xe8c070, 1);
        g.fillCircle(cx + r * 0.95, cy - r * 0.1, r * 0.36);
        g.strokeCircle(cx + r * 0.95, cy - r * 0.1, r * 0.36);
        g.fillStyle(0x2a2a30, 1);
        g.fillRoundedRect(cx - r * 0.55, cy - r * 0.15, r * 1.0, r * 0.45, 4);
        g.fillStyle(0xff8a3c, 1);
        for (let k = 0; k < 4; k++) g.fillRect(cx - r * 0.48 + k * r * 0.24, cy - r * 0.1, r * 0.14, r * 0.35);
        g.fillStyle(0xffe066, 1);
        g.fillCircle(cx - r * 0.35, cy - r * 0.48, r * 0.1);
        g.fillCircle(cx + r * 0.15, cy - r * 0.48, r * 0.1);
        g.fillStyle(0x3a3a3a, 1);
        for (const [dx, dy] of [[-0.8, -0.6], [0.6, -0.6], [-0.8, 0.4], [0.5, 0.4]]) g.fillCircle(cx + dx * r, cy + dy * r, r * 0.05);
        break;
      }
      case 'rivetshell': {
        // clockwork armadillo: banded steel shell studded with rivets, small snout, stubby legs
        g.lineStyle(2.5, C.ink, 1);
        for (const lx of [-0.5, -0.15, 0.25, 0.55]) g.lineBetween(cx + lx * r, cy + r * 0.35, cx + lx * r, cy + r * 0.85);
        this.orbKeep(g, cx + r * 0.1, cy, r * 1.9, r * 1.3, color);
        g.lineStyle(2, 0x5a5a64, 1);
        for (const bx of [-0.35, 0.1, 0.55]) g.lineBetween(cx + bx * r, cy - r * 0.6, cx + bx * r, cy + r * 0.6);
        g.fillStyle(0xe8c070, 1);
        for (const bx of [-0.35, 0.1, 0.55]) for (const by of [-0.35, 0, 0.35]) g.fillCircle(cx + bx * r, cy + by * r, r * 0.07);
        g.lineStyle(2.5, C.ink, 1);
        g.fillStyle(0x7a7a84, 1);
        g.fillEllipse(cx - r * 0.95, cy + r * 0.15, r * 0.6, r * 0.45);
        g.strokeEllipse(cx - r * 0.95, cy + r * 0.15, r * 0.6, r * 0.45);
        g.fillStyle(0xffe066, 1);
        g.fillCircle(cx - r * 0.95, cy + r * 0.05, r * 0.08);
        break;
      }
      case 'cogjammer': {
        // brass beetle: domed shell with a big gear on its back, rivets, little legs
        g.lineStyle(2.5, C.ink, 1);
        for (const s2 of [-1, 1]) for (let k = 0; k < 3; k++) g.lineBetween(cx + s2 * r * 0.6, cy - r * 0.2 + k * r * 0.35, cx + s2 * r * 1.1, cy - r * 0.05 + k * r * 0.4);
        this.orbKeep(g, cx, cy + r * 0.1, r * 1.6, r * 1.4, color);
        // gear: toothed ring
        g.fillStyle(0x8a6a2a, 1);
        for (let k = 0; k < 8; k++) {
          const a0 = (k / 8) * Math.PI * 2;
          g.fillRect(cx + Math.cos(a0) * r * 0.55 - r * 0.1, cy - r * 0.05 + Math.sin(a0) * r * 0.55 - r * 0.1, r * 0.2, r * 0.2);
        }
        g.fillStyle(0xe8c070, 1);
        g.fillCircle(cx, cy - r * 0.05, r * 0.5);
        g.strokeCircle(cx, cy - r * 0.05, r * 0.5);
        g.fillStyle(0x5a4a2a, 1);
        g.fillCircle(cx, cy - r * 0.05, r * 0.16);
        g.fillStyle(0x3a3a3a, 1);
        g.fillEllipse(cx, cy - r * 0.75, r * 0.7, r * 0.35);
        g.fillStyle(0xffe066, 1);
        g.fillCircle(cx - r * 0.15, cy - r * 0.8, r * 0.07);
        g.fillCircle(cx + r * 0.15, cy - r * 0.8, r * 0.07);
        break;
      }
      case 'steamrunner': {
        // boiler on legs: riveted round tank, chimney with a puff, pressure gauge face
        g.lineStyle(2.5, C.ink, 1);
        g.lineBetween(cx - r * 0.35, cy + r * 0.5, cx - r * 0.6, cy + r * 1.0);
        g.lineBetween(cx + r * 0.35, cy + r * 0.5, cx + r * 0.6, cy + r * 1.0);
        g.fillStyle(0x5a5a64, 1);
        g.fillRect(cx + r * 0.25, cy - r * 1.05, r * 0.3, r * 0.55);
        g.strokeRect(cx + r * 0.25, cy - r * 1.05, r * 0.3, r * 0.55);
        g.fillStyle(0xffffff, 0.85);
        g.fillCircle(cx + r * 0.45, cy - r * 1.2, r * 0.18);
        g.fillCircle(cx + r * 0.65, cy - r * 1.3, r * 0.13);
        this.orbKeep(g, cx, cy, (r * 0.8) * 2, (r * 0.8) * 2, color);
        g.fillStyle(0xc8963a, 1);
        g.fillRect(cx - r * 0.8, cy - r * 0.08, r * 1.6, r * 0.16);
        g.fillStyle(0xf0ead8, 1);
        g.fillCircle(cx - r * 0.1, cy - r * 0.25, r * 0.3);
        g.lineStyle(1.5, C.ink, 1);
        g.strokeCircle(cx - r * 0.1, cy - r * 0.25, r * 0.3);
        g.lineStyle(2, 0xd03a2a, 1);
        g.lineBetween(cx - r * 0.1, cy - r * 0.25, cx + r * 0.08, cy - r * 0.4);
        g.fillStyle(0x3a3a3a, 1);
        for (const [dx, dy] of [[-0.55, 0.35], [0.55, 0.35], [-0.55, -0.4], [0.5, -0.45]]) g.fillCircle(cx + dx * r, cy + dy * r, r * 0.06);
        break;
      }
      case 'ulmaroth': {
        // overgrown idol: a stone block body on stumpy legs, a carved face with glowing eyes, vines and moss draped over it
        g.lineStyle(3, C.ink, 1);
        for (const lx of [-0.55, 0.55]) {
          g.fillStyle(shade, 1);
          g.fillRect(cx + lx * r - r * 0.22, cy + r * 0.55, r * 0.44, r * 0.5);
          g.strokeRect(cx + lx * r - r * 0.22, cy + r * 0.55, r * 0.44, r * 0.5);
        }
        g.fillStyle(color, 1);
        g.fillRoundedRect(cx - r * 0.95, cy - r * 0.9, r * 1.9, r * 1.55, 8);
        g.strokeRoundedRect(cx - r * 0.95, cy - r * 0.9, r * 1.9, r * 1.55, 8);
        g.fillStyle(shade, 1);
        g.fillRect(cx - r * 1.1, cy - r * 1.05, r * 2.2, r * 0.25);
        g.strokeRect(cx - r * 1.1, cy - r * 1.05, r * 2.2, r * 0.25);
        g.fillStyle(0x5a5440, 1);
        g.fillRect(cx - r * 0.55, cy - r * 0.55, r * 0.35, r * 0.22);
        g.fillRect(cx + r * 0.2, cy - r * 0.55, r * 0.35, r * 0.22);
        g.fillStyle(0x9aff8a, 1);
        g.fillCircle(cx - r * 0.37, cy - r * 0.44, r * 0.09);
        g.fillCircle(cx + r * 0.37, cy - r * 0.44, r * 0.09);
        g.fillStyle(0x5a5440, 1);
        g.fillRect(cx - r * 0.45, cy - r * 0.05, r * 0.9, r * 0.18);
        for (let k = 0; k < 5; k++) g.fillRect(cx - r * 0.4 + k * r * 0.2, cy + r * 0.13, r * 0.08, r * 0.12);
        g.lineStyle(4, 0x3f8a34, 1);
        g.beginPath();
        g.moveTo(cx - r * 0.95, cy - r * 0.7);
        g.lineTo(cx - r * 0.4, cy + r * 0.3);
        g.lineTo(cx + r * 0.1, cy + r * 0.6);
        g.strokePath();
        g.beginPath();
        g.moveTo(cx + r * 0.95, cy - r * 0.8);
        g.lineTo(cx + r * 0.6, cy - r * 0.2);
        g.lineTo(cx + r * 0.9, cy + r * 0.5);
        g.strokePath();
        g.fillStyle(0x4a9a3a, 1);
        for (const [dx, dy] of [[-0.8, -1.0], [-0.2, -1.05], [0.5, -1.0], [0.9, -0.95]]) g.fillEllipse(cx + dx * r, cy + dy * r, r * 0.45, r * 0.22);
        g.fillStyle(0xe8604a, 1);
        g.fillCircle(cx + r * 0.62, cy + r * 0.05, r * 0.08);
        g.fillCircle(cx - r * 0.65, cy - r * 0.2, r * 0.07);
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
        this.orbKeep(g, cx, cy + r * 0.05, r * 0.85, r * 1.15, color);
        g.fillStyle(0xe8f0f8, 1);
        g.fillEllipse(cx, cy + r * 0.2, r * 0.5, r * 0.7);
        g.fillStyle(0x3a5a7a, 1);
        for (const dx of [-0.18, 0, 0.18]) g.fillTriangle(cx + dx * r - r * 0.07, cy - r * 0.6, cx + dx * r + r * 0.07, cy - r * 0.6, cx + dx * r, cy - r * 0.95);
        this.orbKeep(g, cx, cy - r * 0.5, (r * 0.3) * 2, (r * 0.3) * 2, color);
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
        // a warm glow behind the body, feathery feelers and two dark eyes (design F18)
        g.fillStyle(0xfff0b8, 0.35);
        g.fillCircle(cx, cy, r * 0.6);
        g.lineStyle(1.5, C.ink, 1);
        g.lineBetween(cx - r * 0.1, cy - r * 0.6, cx - r * 0.45, cy - r * 1.2);
        g.lineBetween(cx + r * 0.1, cy - r * 0.6, cx + r * 0.45, cy - r * 1.2);
        g.fillStyle(0xffe066, 1);
        g.fillCircle(cx - r * 0.46, cy - r * 1.22, r * 0.08);
        g.fillCircle(cx + r * 0.46, cy - r * 1.22, r * 0.08);
        g.lineStyle(2, C.ink, 1);
        this.orbKeep(g, cx, cy, r * 0.6, r * 1.3, color);
        g.fillStyle(0x2a2a3a, 1);
        g.fillCircle(cx - r * 0.11, cy - r * 0.42, r * 0.08);
        g.fillCircle(cx + r * 0.11, cy - r * 0.42, r * 0.08);
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
        // faceted: a shaded right face, a facet ridge and two small shards riding its back (design F18)
        g.fillStyle(Phaser.Display.Color.IntegerToColor(color).darken(22).color, 1);
        g.fillTriangle(cx, cy - r * 1.1, cx + r, cy + r * 0.3, cx + r * 0.15, cy + r * 0.3);
        g.lineStyle(1.5, C.ink, 0.6);
        g.lineBetween(cx, cy - r * 1.1, cx + r * 0.15, cy + r * 0.3);
        g.fillStyle(0xffffff, 0.6);
        g.fillTriangle(cx - r * 0.3, cy + r * 0.1, cx + r * 0.1, cy + r * 0.1, cx - r * 0.05, cy - r * 0.8);
        g.lineStyle(2, C.ink, 1);
        g.lineStyle(1.5, C.ink, 1);
        for (const [sx, h] of [[-0.78, 0.5], [0.74, 0.4]]) {
          g.fillStyle(0xd8f8ff, 1);
          g.fillTriangle(cx + sx * r - r * 0.24, cy + r * 0.25, cx + sx * r + r * 0.24, cy + r * 0.25, cx + sx * r, cy - h * r - r * 0.15);
          g.strokeTriangle(cx + sx * r - r * 0.24, cy + r * 0.25, cx + sx * r + r * 0.24, cy + r * 0.25, cx + sx * r, cy - h * r - r * 0.15);
        }
        // the glowing core, with a soft halo
        g.fillStyle(0xb89aff, 0.35);
        g.fillCircle(cx, cy - r * 0.05, r * 0.38);
        g.fillStyle(0x7a5ad8, 1);
        g.fillCircle(cx, cy - r * 0.05, r * 0.22);
        g.fillStyle(0xe8dcff, 1);
        g.fillCircle(cx - r * 0.07, cy - r * 0.12, r * 0.07);
        this.eyes(g, cx, cy - r * 0.42, r * 0.13, r * 0.26);
        break;
      }
      case 'galehound': {
        // lean cliff hound: long low body, swept-back ears, wind streaks trailing behind
        g.lineStyle(2, 0xffffff, 0.8);
        for (let k = 0; k < 3; k++) g.lineBetween(cx + r * 1.0, cy - r * 0.4 + k * r * 0.4, cx + r * 1.7, cy - r * 0.5 + k * r * 0.4);
        g.lineStyle(2.5, C.ink, 1);
        for (const lx of [-0.6, -0.2, 0.3, 0.7]) g.lineBetween(cx + lx * r, cy + r * 0.3, cx + lx * r - r * 0.25, cy + r * 1.0);
        // a feathery tail swept back in the wind (design F18)
        g.fillStyle(color, 1);
        g.lineStyle(2, C.ink, 1);
        g.fillEllipse(cx + r * 1.15, cy - r * 0.3, r * 0.9, r * 0.42);
        g.strokeEllipse(cx + r * 1.15, cy - r * 0.3, r * 0.9, r * 0.42);
        g.fillStyle(0xffffff, 0.5);
        g.fillEllipse(cx + r * 1.2, cy - r * 0.38, r * 0.5, r * 0.12);
        g.lineStyle(2.5, C.ink, 1);
        this.orbKeep(g, cx + r * 0.1, cy + r * 0.05, r * 1.9, r * 0.9, color);
        this.orbKeep(g, cx - r * 0.85, cy - r * 0.3, r * 0.96, r * 0.96, color);
        g.fillStyle(0x6a8aa8, 1);
        g.fillTriangle(cx - r * 0.75, cy - r * 0.65, cx - r * 0.2, cy - r * 0.95, cx - r * 0.5, cy - r * 0.45);
        g.strokeTriangle(cx - r * 0.75, cy - r * 0.65, cx - r * 0.2, cy - r * 0.95, cx - r * 0.5, cy - r * 0.45);
        g.fillStyle(0xffffff, 0.6);
        g.fillEllipse(cx + r * 0.1, cy - r * 0.15, r * 1.1, r * 0.25);
        g.fillStyle(0xffffff, 1);
        g.fillCircle(cx - r * 1.0, cy - r * 0.38, r * 0.14);
        g.fillStyle(0x111111, 1);
        g.fillCircle(cx - r * 1.02, cy - r * 0.37, r * 0.09);
        g.fillCircle(cx - r * 1.3, cy - r * 0.22, r * 0.09);
        g.fillStyle(0xffffff, 1);
        g.fillCircle(cx - r * 1.04, cy - r * 0.41, r * 0.035);
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
        // the lower-right half in shadow and a lit upper-left edge, light from the upper left (design F19)
        g.fillStyle(Phaser.Display.Color.IntegerToColor(color).darken(18).color, 1);
        g.fillTriangle(cx, cy + r * 0.6, cx + r * 1.5, cy + r * 0.05, cx, cy + r * 0.05);
        g.fillStyle(0xffffff, 0.35);
        g.fillTriangle(cx, cy - r * 0.9, cx - r * 1.5, cy + r * 0.05, cx - r * 1.2, cy + r * 0.0);
        g.lineStyle(1.5, C.ink, 0.5);
        g.lineBetween(cx - r * 1.5, cy + r * 0.05, cx + r * 1.5, cy + r * 0.05);
        g.lineStyle(2, C.ink, 1);
        g.strokePoints(wing, true);
        g.fillStyle(0xd8eef8, 1);
        g.fillEllipse(cx, cy - r * 0.05, r * 0.5, r * 1.0);
        g.fillStyle(0x4a7a98, 1);
        g.fillTriangle(cx - r * 1.5, cy + r * 0.05, cx - r * 0.9, cy - r * 0.2, cx - r * 1.0, cy + r * 0.2);
        g.fillTriangle(cx + r * 1.5, cy + r * 0.05, cx + r * 0.9, cy - r * 0.2, cx + r * 1.0, cy + r * 0.2);
        this.eyes(g, cx, cy - r * 0.45, r * 0.12, r * 0.2);
        // a red bow on the ribbon tail
        g.fillStyle(0xe8453a, 1);
        g.fillTriangle(cx + r * 0.12, cy + r * 0.78, cx + r * 0.36, cy + r * 0.7, cx + r * 0.24, cy + r * 0.86);
        g.fillTriangle(cx + r * 0.12, cy + r * 0.78, cx + r * 0.0, cy + r * 0.9, cx + r * 0.24, cy + r * 0.86);
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
        this.orbKeep(g, cx, cy, r * 1.8, r * 1.5, color);
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
          this.orbKeep(g, cx + s * r * 1.05, cy - r * 0.55, r * 0.75, r * 0.55, color);
          g.fillStyle(shade, 1);
          g.fillTriangle(cx + s * r * 1.2, cy - r * 0.6, cx + s * r * 1.5, cy - r * 1.05, cx + s * r * 1.45, cy - r * 0.45);
          g.strokeTriangle(cx + s * r * 1.2, cy - r * 0.6, cx + s * r * 1.5, cy - r * 1.05, cx + s * r * 1.45, cy - r * 0.45);
        }
        this.orbKeep(g, cx, cy, r * 1.9, r * 1.3, color);
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
        this.orbKeep(g, cx - r * 0.15, cy - r * 0.05, (r * 0.95) * 2, (r * 0.95) * 2, color);
        g.lineStyle(2, shade, 1);
        g.beginPath();
        g.arc(cx - r * 0.15, cy - r * 0.05, r * 0.6, 0, Math.PI * 1.5);
        g.strokePath();
        g.beginPath();
        g.arc(cx - r * 0.15, cy - r * 0.05, r * 0.3, 0, Math.PI * 1.5);
        g.strokePath();
        // coral tips with a soft glow (design D3)
        g.fillStyle(0xffb0c0, 0.35);
        for (const [dx, dy] of [[-0.75, -0.75], [-0.35, -1.0], [0.1, -0.95]]) g.fillCircle(cx + dx * r, cy + dy * r - 2, 6);
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
        this.orbKeep(g, cx, cy, r * 2, r * 1.4, color);
        g.lineStyle(1.5, C.ink, 0.8);
        for (const [dx, dy, rr] of [[-0.45, -0.25, 0.22], [0.05, -0.4, 0.26], [0.5, -0.15, 0.2], [-0.1, 0.1, 0.18], [0.35, 0.25, 0.15]]) {
          g.fillStyle(0xeee6d6, 1);
          g.fillCircle(cx + dx * r, cy + dy * r, r * rr);
          g.strokeCircle(cx + dx * r, cy + dy * r, r * rr);
          // each barnacle's dark mouth and a glint (design D3)
          g.fillStyle(0x6a6058, 1);
          g.fillCircle(cx + dx * r, cy + dy * r, r * rr * 0.35);
          g.fillStyle(0xffffff, 0.8);
          g.fillCircle(cx + dx * r - r * rr * 0.4, cy + dy * r - r * rr * 0.4, r * rr * 0.22);
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
        // feather lines along each swept wing (design F18)
        g.lineStyle(1, 0x7a8490, 1);
        for (const sd of [-1, 1]) for (const t of [0.45, 0.7]) g.lineBetween(cx + sd * r * 0.4, cy - r * 0.05, cx + sd * r * (0.4 + t * 1.3), cy - r * (0.05 + t * 0.6));
        g.lineStyle(2.5, C.ink, 1);
        this.orbKeep(g, cx, cy, r * 1.3, r * 1.1, color);
        this.orbKeep(g, cx + r * 0.45, cy - r * 0.45, r * 0.9, r * 0.9, color);
        g.fillStyle(0xffc93c, 1);
        g.fillTriangle(cx + r * 0.8, cy - r * 0.5, cx + r * 0.8, cy - r * 0.3, cx + r * 1.25, cy - r * 0.4);
        g.fillStyle(0xe8453a, 1);
        g.fillCircle(cx + r * 1.05, cy - r * 0.36, r * 0.05); // the gull's red beak spot
        g.fillStyle(0x111111, 1);
        g.fillCircle(cx + r * 0.55, cy - r * 0.55, r * 0.1);
        g.fillStyle(0xffffff, 1);
        g.fillCircle(cx + r * 0.52, cy - r * 0.59, r * 0.04);
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
        this.orbKeep(g, cx, cy - r * 0.25, r * 2.1, r * 1.35, color);
        g.fillStyle(0xfff0f8, 1);
        for (const [dx, dy, rr] of [[-0.55, -0.45, 0.18], [0.1, -0.7, 0.14], [0.6, -0.35, 0.16], [-0.1, -0.2, 0.1]]) g.fillCircle(cx + dx * r, cy + dy * r, r * rr);
        g.fillStyle(0x111111, 1);
        g.fillCircle(cx - r * 0.2, cy + r * 0.35, r * 0.1);
        g.fillCircle(cx + r * 0.2, cy + r * 0.35, r * 0.1);
        // rosy cheeks and a shadow under the cap's rim (design D2)
        g.fillStyle(0xf08aa8, 0.6);
        g.fillCircle(cx - r * 0.38, cy + r * 0.48, r * 0.1);
        g.fillCircle(cx + r * 0.38, cy + r * 0.48, r * 0.1);
        g.fillStyle(0x000000, 0.15);
        g.fillEllipse(cx, cy + r * 0.05, r * 1.0, r * 0.18);
        break;
      }
      case 'veilstalker': {
        // lanky mist-cat: hooded head, long tail, faint aura
        g.fillStyle(0xc8b8ff, 0.25);
        g.fillCircle(cx, cy, r * 1.5);
        g.lineStyle(3, C.ink, 1);
        g.lineBetween(cx - r * 0.8, cy + r * 0.4, cx - r * 1.5, cy - r * 0.4);
        g.lineStyle(2, C.ink, 1);
        this.orbKeep(g, cx, cy + r * 0.3, r * 1.8, r * 1.1, color);
        this.orbKeep(g, cx + r * 0.6, cy - r * 0.35, r * 1.4, r * 1.4, color);
        g.fillTriangle(cx + r * 0.15, cy - r * 0.7, cx + r * 0.5, cy - r * 0.8, cx + r * 0.2, cy - r * 1.3);
        g.fillTriangle(cx + r * 0.75, cy - r * 0.8, cx + r * 1.1, cy - r * 0.7, cx + r * 1.0, cy - r * 1.3);
        g.fillStyle(0xbff4ff, 0.35);
        g.fillCircle(cx + r * 0.45, cy - r * 0.4, r * 0.24);
        g.fillCircle(cx + r * 0.85, cy - r * 0.4, r * 0.24);
        g.fillStyle(0xbff4ff, 1);
        g.fillCircle(cx + r * 0.45, cy - r * 0.4, r * 0.13);
        g.fillCircle(cx + r * 0.85, cy - r * 0.4, r * 0.13);
        // mist curling off the tail tip (design D2)
        g.fillStyle(0xe8e0ff, 0.5);
        g.fillCircle(cx - r * 1.55, cy - r * 0.5, r * 0.18);
        g.fillCircle(cx - r * 1.35, cy - r * 0.75, r * 0.12);
        break;
      }
      case 'rootrager': {
        // angry stump: bark body, rings on top, root legs, glowing eyes
        g.fillStyle(shade, 1);
        for (const dx of [-0.8, -0.25, 0.3, 0.85]) g.fillTriangle(cx + dx * r - 4, cy + r * 0.6, cx + dx * r + 4, cy + r * 0.6, cx + dx * r * 1.2, cy + r * 1.15);
        // shaded bark: the right side in shadow, a lit edge on the left (design D3)
        g.fillStyle(shade, 1);
        g.fillRoundedRect(cx - r, cy - r * 0.7, r * 2, r * 1.5, 6);
        g.fillStyle(color, 1);
        g.fillRoundedRect(cx - r, cy - r * 0.7, r * 1.55, r * 1.5, 6);
        g.fillStyle(0xffffff, 0.16);
        g.fillRect(cx - r * 0.9, cy - r * 0.4, r * 0.18, r * 0.9);
        g.strokeRoundedRect(cx - r, cy - r * 0.7, r * 2, r * 1.5, 6);
        // leaf sprigs sprouting from the rim
        g.fillStyle(0x6ab04c, 1);
        g.fillEllipse(cx - r * 0.75, cy - r * 0.95, r * 0.4, r * 0.2);
        g.fillEllipse(cx + r * 0.7, cy - r * 1.0, r * 0.36, r * 0.18);
        g.fillStyle(0xd9b47a, 1);
        g.fillEllipse(cx, cy - r * 0.7, r * 2, r * 0.6);
        g.strokeEllipse(cx, cy - r * 0.7, r * 2, r * 0.6);
        g.lineStyle(1.5, shade, 1);
        g.strokeEllipse(cx, cy - r * 0.7, r * 1.2, r * 0.34);
        g.strokeEllipse(cx, cy - r * 0.7, r * 0.5, r * 0.14);
        g.lineStyle(2, shade, 1);
        g.lineBetween(cx - r * 0.5, cy - r * 0.2, cx - r * 0.5, cy + r * 0.6);
        g.lineBetween(cx + r * 0.6, cy - r * 0.1, cx + r * 0.6, cy + r * 0.5);
        g.fillStyle(0xffb84a, 0.35);
        g.fillCircle(cx - r * 0.3, cy, r * 0.26);
        g.fillCircle(cx + r * 0.3, cy, r * 0.26);
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
        this.orbKeep(g, cx, cy, r * 2, r * 2, color);
        // a layered flame crown on top of the head: orange tongue, yellow core (design D3)
        g.fillStyle(color, 1);
        g.fillTriangle(cx - r * 0.6, cy - r * 0.62, cx + r * 0.6, cy - r * 0.62, cx, cy - r * 1.6);
        g.fillStyle(0xffc93c, 1);
        g.fillTriangle(cx - r * 0.3, cy - r * 0.66, cx + r * 0.3, cy - r * 0.66, cx, cy - r * 1.25);
        g.fillStyle(0xfff0a8, 0.4);
        g.fillCircle(cx - r * 0.35, cy - r * 0.1, r * 0.34);
        g.fillCircle(cx + r * 0.35, cy - r * 0.1, r * 0.34);
        g.fillStyle(0xfff0a8, 1);
        g.fillCircle(cx - r * 0.35, cy - r * 0.1, r * 0.22);
        g.fillCircle(cx + r * 0.35, cy - r * 0.1, r * 0.22);
        break;
      }
      case 'ashhive': {
        // wisps of smoke rising from the top (design D3)
        g.fillStyle(0x9a8a88, 0.45);
        g.fillCircle(cx - r * 0.2, cy - r * 1.35, r * 0.22);
        g.fillCircle(cx + r * 0.15, cy - r * 1.6, r * 0.17);
        g.fillCircle(cx - r * 0.05, cy - r * 1.85, r * 0.12);
        this.orbKeep(g, cx, cy + r * 0.2, r * 2.2, r * 1.7, color);
        g.fillCircle(cx, cy - r * 0.4, r * 0.8);
        g.fillStyle(0xffffff, 0.18);
        g.fillEllipse(cx - r * 0.25, cy - r * 0.65, r * 0.5, r * 0.25);
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
        this.orbKeep(g, cx, cy - r * 0.4, r * 2.3, r * 1.3, color);
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
        this.orbKeep(g, cx, cy + r * 0.05, r * 1.9, r * 1.2, color);
        g.lineStyle(3, 0xffb84a, 1);
        g.lineBetween(cx - r * 0.7, cy + r * 0.1, cx - r * 0.2, cy + r * 0.3);
        g.lineBetween(cx - r * 0.2, cy + r * 0.3, cx + r * 0.2, cy);
        g.lineBetween(cx - r * 0.9, cy + r * 0.6, cx - r * 0.4, cy + r * 0.75);
        g.lineStyle(3, C.ink, 1);
        // head
        this.orbKeep(g, cx + r * 0.65, cy - r * 0.45, r * 1.1, r * 0.85, color);
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
        this.orbKeep(g, cx, cy, r * 2.2, r * 1.6, color);
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
        this.orbKeep(g, cx, cy, r * 2.1, r * 1.6, color);
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
        this.orbKeep(g, cx, cy, radius * 1.6, radius * 2, color);
        g.lineBetween(cx, cy - radius * 0.4, cx, cy + radius);
        // iridescent shell: a long sky-teal sheen on each wing case and a gold glint (design F17)
        g.fillStyle(0x9af0d8, 0.55);
        g.fillEllipse(cx - radius * 0.38, cy + radius * 0.15, radius * 0.22, radius * 0.9);
        g.fillStyle(0x7ad0ff, 0.4);
        g.fillEllipse(cx + radius * 0.4, cy + radius * 0.25, radius * 0.16, radius * 0.7);
        g.fillStyle(light, 1);
        g.fillCircle(cx - radius * 0.35, cy - radius * 0.1, radius * 0.25);
        g.fillStyle(0xfff0a0, 1);
        g.fillCircle(cx - radius * 0.42, cy - radius * 0.18, radius * 0.08);
        // feelers
        g.lineStyle(1.5, C.ink, 1);
        g.lineBetween(cx - radius * 0.2, cy - radius * 0.9, cx - radius * 0.55, cy - radius * 1.35);
        g.lineBetween(cx + radius * 0.2, cy - radius * 0.9, cx + radius * 0.55, cy - radius * 1.35);
        g.fillStyle(C.ink, 1);
        g.fillCircle(cx - radius * 0.57, cy - radius * 1.37, radius * 0.08);
        g.fillCircle(cx + radius * 0.57, cy - radius * 1.37, radius * 0.08);
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
        g.lineStyle(2, C.ink, 0.8);
        for (const [px, py] of plates) this.orbKeep(g, cx + px * radius, cy + py * radius, radius * 0.76, radius * 0.76, color);
        // a tuft of moss on the shell (design D2)
        g.fillStyle(0x6ab04c, 1);
        g.fillEllipse(cx - radius * 0.15, cy - radius * 0.82, radius * 0.5, radius * 0.22);
        g.fillStyle(0x8ad86a, 1);
        g.fillEllipse(cx - radius * 0.22, cy - radius * 0.86, radius * 0.24, radius * 0.12);
        // colour accent (fix C2): bright orange lichen freckling the plates, so the grey shell pops off grey roads
        g.fillStyle(0xffa63a, 1);
        for (const [lx, ly, lr] of [[0.42, -0.5, 0.15], [0.58, -0.32, 0.1], [-0.58, 0.42, 0.14], [0.6, 0.42, 0.11], [-0.45, -0.22, 0.09]]) g.fillCircle(cx + lx * radius, cy + ly * radius, lr * radius);
        g.fillStyle(0xffe08a, 1);
        g.fillCircle(cx + 0.4 * radius, cy - 0.53 * radius, 0.04 * radius);
        this.eyes(g, cx, cy - radius * 0.05, radius * 0.17, radius * 0.25);
        break;
      }
      default: {
        // mudling: droopy blob with a little sprout and a mud drip (design D2)
        g.fillStyle(shade, 1);
        g.fillEllipse(cx, cy + radius * 0.5, radius * 2.2, radius * 1.05);
        this.orbKeep(g, cx, cy, radius * 2, radius * 2, color);
        g.fillStyle(color, 1);
        g.fillEllipse(cx - radius * 0.1, cy + radius * 0.42, radius * 1.9, radius * 0.8);
        g.fillStyle(shade, 1);
        g.fillEllipse(cx + radius * 0.75, cy + radius * 0.95, radius * 0.28, radius * 0.4);
        g.fillStyle(light, 1);
        g.fillCircle(cx - radius * 0.42, cy - radius * 0.48, radius * 0.2);
        g.fillStyle(shade, 1);
        g.fillCircle(cx + radius * 0.5, cy + radius * 0.4, radius * 0.16);
        g.fillCircle(cx - radius * 0.6, cy + radius * 0.25, radius * 0.1);
        // sprout
        g.lineStyle(1.5, 0x3a6a2a, 1);
        g.lineBetween(cx, cy - radius * 0.95, cx + radius * 0.05, cy - radius * 1.3);
        g.fillStyle(0x7bc85a, 1);
        g.fillEllipse(cx - radius * 0.18, cy - radius * 1.32, radius * 0.4, radius * 0.22);
        g.fillEllipse(cx + radius * 0.26, cy - radius * 1.38, radius * 0.42, radius * 0.24);
        // colour accent (fix C2): a pink flower bud on the sprout and rosy cheeks, so the brown blob pops off dirt roads
        g.fillStyle(0xff7aa8, 1);
        g.fillCircle(cx + radius * 0.05, cy - radius * 1.36, radius * 0.16);
        g.fillStyle(0xffd0e0, 1);
        g.fillCircle(cx + radius * 0.01, cy - radius * 1.4, radius * 0.06);
        g.fillStyle(0xff8a95, 0.75);
        g.fillEllipse(cx - radius * 0.62, cy + radius * 0.18, radius * 0.34, radius * 0.18);
        g.fillEllipse(cx + radius * 0.62, cy + radius * 0.18, radius * 0.34, radius * 0.18);
        this.eyes(g, cx, cy - radius * 0.1, radius * 0.25, radius * 0.35);
      }
    }
    g.generateTexture(`enemy_${id}`, s, s);
    g.destroy();
    // near-black foes hide their own ink outline: give their upper-left edge a cool rim light (consistency pass F25)
    if (brightness(color) < 0.25) this.rimLight(`enemy_${id}`, 0xb8c4dc, 0.45);
    // bosses catch the light: a warm sheen along every upper-left edge, so horns, crowns and shells read as polished (design F32)
    else if (boss) this.rimLight(`enemy_${id}`, 0xfff0c8, 0.4);
  }

  /** Light the upper-left edge of a baked texture (see systems/rimLight). */
  private rimLight(key: string, color: number, amount: number): void {
    const tex = this.textures.get(key) as Phaser.Textures.CanvasTexture;
    if (!tex || typeof tex.getContext !== 'function') return;
    const ctx = tex.getContext();
    const img = ctx.getImageData(0, 0, tex.width, tex.height);
    applyRim(img.data, tex.width, tex.height, color, amount, 1);
    ctx.putImageData(img, 0, 0);
    tex.refresh();
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
      case 'shaman': {
        // reed hut with a bone-and-feather staff planted beside it and a glowing bowl of bog-brew
        g.fillStyle(def.color, 1);
        g.fillTriangle(cx - 28, cy + 22, cx + 22, cy + 22, cx - 3, cy - 30);
        g.strokeTriangle(cx - 28, cy + 22, cx + 22, cy + 22, cx - 3, cy - 30);
        g.lineStyle(1.5, 0x4a2a5a, 1);
        for (const dx of [-14, -3, 8]) g.lineBetween(cx + dx * 0.3 - 3, cy - 22, cx + dx, cy + 20);
        g.fillStyle(0x1a1020, 1);
        g.fillEllipse(cx - 3, cy + 12, 14, 18);
        g.lineStyle(3, C.ink, 1);
        g.lineBetween(cx + 26, cy + 24, cx + 26, cy - 26);
        g.fillStyle(0xe8e0c8, 1);
        g.fillCircle(cx + 26, cy - 28, 6);
        g.strokeCircle(cx + 26, cy - 28, 6);
        g.fillStyle(0x4fae7c, 1);
        g.fillTriangle(cx + 30, cy - 22, cx + 40, cy - 14, cx + 30, cy - 14);
        g.fillStyle(0x5a4632, 1);
        g.fillEllipse(cx + 14, cy + 24, 18, 9);
        g.fillStyle(0x9bff8a, 1);
        g.fillEllipse(cx + 14, cy + 22, 12, 5);
        break;
      }
      case 'hive': {
        // a papery striped hornet nest hanging from a dead branch, with a dark entrance hole and a few hornets
        g.lineStyle(4, 0x5a4632, 1);
        g.lineBetween(cx - 30, cy - 26, cx + 30, cy - 22);
        g.lineBetween(cx, cy - 24, cx, cy - 18);
        g.lineStyle(2.5, C.ink, 1);
        g.fillStyle(def.color, 1);
        g.fillEllipse(cx, cy + 4, 42, 48);
        g.strokeEllipse(cx, cy + 4, 42, 48);
        g.lineStyle(2, 0x8a6a30, 1);
        for (const dy of [-10, 0, 10, 20]) {
          const w = Math.sqrt(Math.max(0, 1 - ((dy - 4) / 24) ** 2)) * 21;
          g.lineBetween(cx - w + 2, cy + dy, cx + w - 2, cy + dy);
        }
        g.fillStyle(0x1a1208, 1);
        g.fillCircle(cx, cy + 18, 5);
        for (const [hx, hy] of [[24, -6], [-24, 6], [20, 22]]) {
          g.fillStyle(0xffc83a, 1);
          g.fillEllipse(cx + hx, cy + hy, 8, 5);
          g.fillStyle(0x1a1208, 1);
          g.fillRect(cx + hx - 1, cy + hy - 2.5, 2, 5);
          g.fillStyle(0xffffff, 0.7);
          g.fillCircle(cx + hx - 1, cy + hy - 4, 2);
        }
        break;
      }
      case 'menhir': {
        // a tall leaning grey standing stone on a heather mound, carved with pale spirals
        g.fillStyle(0x6a5a6a, 1);
        g.fillEllipse(cx, cy + 14, 58, 22);
        g.fillStyle(0x9a6aa8, 1);
        for (let h = 0; h < 8; h++) g.fillCircle(cx - 24 + h * 7, cy + 12 + (h % 2) * 4, 3);
        g.fillStyle(0x000000, 0.18);
        g.fillEllipse(cx + 8, cy + 14, 26, 8);
        g.fillStyle(0x8a8a88, 1);
        g.fillRoundedRect(cx - 11, cy - 30, 22, 44, 6);
        g.lineStyle(2, C.ink, 1);
        g.strokeRoundedRect(cx - 11, cy - 30, 22, 44, 6);
        g.fillStyle(0xa8a8a4, 1);
        g.fillRect(cx - 9, cy - 28, 6, 40);
        g.lineStyle(1.5, 0xe0e0f0, 0.9);
        for (const [sx, sy] of [[0, -16], [1, 2]]) {
          g.beginPath();
          g.arc(cx + sx, cy + sy, 5, 0, Math.PI * 1.6);
          g.strokePath();
        }
        g.fillStyle(0xc8c060, 0.85);
        g.fillCircle(cx + 6, cy + 8, 3);
        break;
      }
      case 'rattle': {
        // a ring of sun-bleached rocks around a sandy pit, with rattlesnake heads and tails poking out
        g.fillStyle(0xe0c088, 1);
        g.fillEllipse(cx, cy + 6, 62, 40);
        g.strokeEllipse(cx, cy + 6, 62, 40);
        g.fillStyle(0xc8a068, 1);
        g.fillEllipse(cx, cy + 8, 46, 26);
        g.fillStyle(0x9a8a7a, 1);
        for (const a of [0.2, 1.1, 2.0, 2.9, 3.8, 4.7, 5.6]) g.fillCircle(cx + Math.cos(a) * 31, cy + 6 + Math.sin(a) * 20, 5);
        g.lineStyle(4, 0xb86a3a, 1);
        for (const [sx, sy, dx, dy] of [[-14, 6, -6, -14], [6, 12, 12, -8], [16, 2, 24, -12]]) {
          g.lineBetween(cx + sx, cy + sy, cx + dx, cy + dy);
          g.fillStyle(0xb86a3a, 1);
          g.fillTriangle(cx + dx - 4, cy + dy + 2, cx + dx + 4, cy + dy + 2, cx + dx, cy + dy - 6);
          g.fillStyle(0xf0d040, 1);
          g.fillCircle(cx + dx, cy + dy - 1, 1.2);
        }
        g.fillStyle(0xe8d0a0, 1);
        for (let k = 0; k < 3; k++) g.fillEllipse(cx - 2 + k * 4, cy + 18, 4, 5);
        break;
      }
      case 'sludge': {
        // a bubbling pit of brown-green muck ringed with stakes, a ladle sticking out
        g.fillStyle(0x3a2e1e, 1);
        g.fillEllipse(cx, cy + 6, 64, 42);
        g.strokeEllipse(cx, cy + 6, 64, 42);
        g.fillStyle(0x6a6a2a, 1);
        g.fillEllipse(cx, cy + 6, 52, 32);
        g.fillStyle(0x8a8a3a, 1);
        for (const [bx, by, br] of [[-12, 2, 5], [8, 10, 4], [14, -2, 3], [-4, 14, 3]]) g.fillCircle(cx + bx, cy + by, br);
        g.lineStyle(1.5, 0xc8c87a, 0.8);
        g.strokeCircle(cx - 12, cy + 2, 5);
        g.lineStyle(3, 0x5a4632, 1);
        for (const a of [0.3, 1.4, 2.6, 3.7, 4.9, 5.8]) {
          const sx = cx + Math.cos(a) * 34;
          const sy = cy + 6 + Math.sin(a) * 23;
          g.lineBetween(sx, sy, sx, sy - 12);
        }
        g.lineStyle(3, 0x9a7a52, 1);
        g.lineBetween(cx + 4, cy + 4, cx + 22, cy - 22);
        g.fillStyle(0x9a7a52, 1);
        g.fillCircle(cx + 23, cy - 23, 4);
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
    } else if (id === 'otter') {
      // otter: cream muzzle, little round ears, a sack slung over the shoulder, a wet sheen
      g.fillStyle(0xe8d8b8, 1);
      g.fillEllipse(15, 15, 9, 6);
      g.fillStyle(0x111111, 1);
      g.fillCircle(15, 13, 1.4);
      g.fillStyle(0x6a4a2a, 1);
      g.fillCircle(9, 6, 2.5);
      g.fillCircle(21, 6, 2.5);
      g.fillStyle(0xc8a878, 1);
      g.fillEllipse(24, 22, 9, 10);
      g.lineStyle(1.5, C.ink, 1);
      g.strokeEllipse(24, 22, 9, 10);
      g.fillStyle(0xbfe8ff, 0.7);
      g.fillCircle(10, 18, 1.5);
    } else if (id === 'mole') {
      // mole: pink star-nose, tiny eyes, a miner's lamp on its head and big pale digging claws
      g.fillStyle(0xf0a0b0, 1);
      g.fillCircle(15, 14, 3);
      g.fillStyle(0xffe066, 1);
      g.fillCircle(15, 3, 3);
      g.lineStyle(1.5, C.ink, 1);
      g.strokeCircle(15, 3, 3);
      g.fillStyle(0xe8d8c8, 1);
      g.fillEllipse(5, 22, 7, 5);
      g.fillEllipse(25, 22, 7, 5);
      g.lineStyle(1.2, C.ink, 1);
      g.strokeEllipse(5, 22, 7, 5);
      g.strokeEllipse(25, 22, 7, 5);
    } else if (id === 'mender') {
      // toad: wide mouth line, a tonic gourd on its hip
      g.lineStyle(1.5, 0x2a4a1a, 1);
      g.lineBetween(11, 14, 19, 14);
      g.fillStyle(0xc8a050, 1);
      g.fillCircle(25, 22, 4);
      g.fillCircle(25, 17, 2.5);
      g.lineStyle(1.5, C.ink, 1);
      g.strokeCircle(25, 22, 4);
      g.fillStyle(0x9bff8a, 1);
      g.fillCircle(25, 22, 1.6);
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
      case 'shrine': {
        // a soft glow pool, a ring of standing stones, and a night-blooming flower in the middle
        g.fillStyle(def.color, 0.18 + lvl * 0.08);
        g.fillCircle(cx, cy + 2, 30 * k);
        const stones = 5 + lvl;
        for (let i = 0; i < stones; i++) {
          const a = (i / stones) * Math.PI * 2 - Math.PI / 2;
          const sx = cx + Math.cos(a) * 30 * k;
          const sy = cy + 4 + Math.sin(a) * 22 * k;
          g.fillStyle(0xcfc8bc, 1);
          g.fillRoundedRect(sx - 5, sy - 14, 10, 16, 4);
          g.lineStyle(2, C.ink, 1);
          g.strokeRoundedRect(sx - 5, sy - 14, 10, 16, 4);
        }
        // stem and moon-petals
        g.lineStyle(3, 0x4b8f3a, 1);
        g.lineBetween(cx, cy + 8, cx, cy - 10);
        for (let i = 0; i < 5; i++) {
          const a = (i / 5) * Math.PI * 2 - Math.PI / 2;
          g.fillStyle(0xf0eaff, 1);
          g.fillEllipse(cx + Math.cos(a) * 8, cy - 14 + Math.sin(a) * 8, 11, 11);
        }
        g.fillStyle(def.color, 1);
        g.fillCircle(cx, cy - 14, 5);
        g.fillStyle(0xffffff, 0.9);
        g.fillCircle(cx - 1.5, cy - 15.5, 1.8);
        // a little moth keeper
        g.fillStyle(0xe8d8b0, 1);
        g.fillEllipse(cx + 18, cy - 30, 9, 6);
        g.fillEllipse(cx + 26, cy - 30, 9, 6);
        g.fillStyle(0x6a5a3a, 1);
        g.fillEllipse(cx + 22, cy - 29, 3, 7);
        break;
      }
      case 'market': {
        // a little market stall: a striped awning on poles over a counter with sacks of acorns and jars of glowsap
        g.fillStyle(0x7a5232, 1);
        g.fillRect(cx - 26, cy - 14, 4, 34);
        g.fillRect(cx + 22, cy - 14, 4, 34);
        g.fillStyle(0x9a6a40, 1);
        g.fillRect(cx - 28, cy + 6, 56, 14);
        g.lineStyle(2, C.ink, 1);
        g.strokeRect(cx - 28, cy + 6, 56, 14);
        for (let n = 0; n < 5; n++) {
          g.fillStyle(n % 2 ? 0xf4ecd8 : def.color, 1);
          g.fillRect(cx - 32 + n * 13, cy - 26, 13, 14);
        }
        g.strokeRect(cx - 32, cy - 26, 65, 14);
        for (let n = 0; n < 5; n++) {
          g.fillStyle(n % 2 ? 0xf4ecd8 : def.color, 1);
          g.fillTriangle(cx - 32 + n * 13, cy - 12, cx - 19 + n * 13, cy - 12, cx - 25.5 + n * 13, cy - 6);
        }
        g.fillStyle(0xc8a050, 1);
        g.fillEllipse(cx - 14, cy + 2, 14, 12);
        g.fillStyle(0xffc93c, 1);
        g.fillCircle(cx - 16, cy - 2, 2.5);
        g.fillCircle(cx - 11, cy - 3, 2.5);
        g.fillStyle(0x9be86a, 1);
        g.fillRoundedRect(cx + 4, cy - 6, 8, 12, 2);
        g.fillRoundedRect(cx + 14, cy - 4, 7, 10, 2);
        break;
      }
      case 'apiary': {
        // a little meadow with painted hive-boxes stacked on stands, a few bees, and a honey pot
        g.fillStyle(0x8ab84a, 0.35);
        g.fillEllipse(cx, cy + 14, 66 * k, 26 * k);
        const boxes = 1 + lvl;
        for (let i = 0; i < boxes; i++) {
          const bx = cx - 20 + (i % 2) * 26;
          const by = cy + 8 - Math.floor(i / 2) * 18 - (i % 2) * 4;
          g.fillStyle(0x7a5a3a, 1);
          g.fillRect(bx - 1, by + 10, 3, 8);
          g.fillRect(bx + 17, by + 10, 3, 8);
          g.fillStyle([0xf0e0b0, 0x9ad0e8, 0xf0b8c8][i % 3], 1);
          g.fillRect(bx - 4, by - 6, 26, 16);
          g.lineStyle(2, C.ink, 1);
          g.strokeRect(bx - 4, by - 6, 26, 16);
          g.lineStyle(1.5, 0x8a6a40, 0.8);
          g.lineBetween(bx - 4, by + 1, bx + 22, by + 1);
          g.fillStyle(0x3a2a1a, 1);
          g.fillRect(bx + 5, by + 6, 8, 3);
          g.fillStyle(0xc8a050, 1);
          g.fillRect(bx - 6, by - 10, 30, 5);
          g.lineStyle(1.5, C.ink, 1);
          g.strokeRect(bx - 6, by - 10, 30, 5);
        }
        g.fillStyle(0xe8a030, 1);
        g.fillCircle(cx + 26, cy + 18, 7);
        g.lineStyle(1.5, C.ink, 1);
        g.strokeCircle(cx + 26, cy + 18, 7);
        g.fillStyle(0xffd060, 1);
        g.fillEllipse(cx + 26, cy + 12, 10, 4);
        for (const [hx, hy] of [[-26, -26], [12, -34], [30, -16]]) {
          g.fillStyle(0xffc83a, 1);
          g.fillEllipse(cx + hx, cy + hy, 7, 5);
          g.fillStyle(0x1a1208, 1);
          g.fillRect(cx + hx - 0.5, cy + hy - 2.5, 1.5, 5);
        }
        break;
      }
      case 'weir': {
        // a little stream crossing the plot, a woven willow fence across it, a fish basket and leaping fish
        g.fillStyle(0x6ab8d8, 1);
        g.fillRoundedRect(cx - 34 * k, cy - 4, 68 * k, 22, 8);
        g.lineStyle(1.5, 0xd8f4ff, 0.8);
        for (let i = 0; i < 4; i++) g.lineBetween(cx - 26 * k + i * 16 * k, cy + 4 + (i % 2) * 6, cx - 18 * k + i * 16 * k, cy + 4 + (i % 2) * 6);
        const posts = 3 + lvl;
        g.lineStyle(3, 0x7a5a32, 1);
        for (let i = 0; i < posts; i++) {
          const px = cx - 22 + (i * 44) / (posts - 1);
          g.lineBetween(px, cy + 20, px - 4, cy - 14);
        }
        g.lineStyle(2.5, 0xb89a5a, 1);
        for (const yy of [-6, 2, 10]) g.lineBetween(cx - 26, cy + yy + 4, cx + 22, cy + yy - 4);
        g.fillStyle(0xc89a5a, 1);
        g.fillEllipse(cx + 28, cy - 14, 16, 14);
        g.lineStyle(1.5, C.ink, 1);
        g.strokeEllipse(cx + 28, cy - 14, 16, 14);
        g.lineStyle(1, 0x8a6a3a, 1);
        g.lineBetween(cx + 21, cy - 14, cx + 35, cy - 14);
        g.fillStyle(0x7a9ac0, 1);
        for (const [fx, fy, fr] of [[-14, -22, 0.4], [10, -26, -0.5]] as const) {
          g.fillEllipse(cx + fx, cy + fy, 12, 5);
          g.fillTriangle(cx + fx + 5, cy + fy, cx + fx + 10, cy + fy - 4 + fr * 4, cx + fx + 10, cy + fy + 4 + fr * 4);
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

  /**
   * A shaded rounded body part: base colour, a darker crescent toward the lower right, a soft highlight toward the
   * upper left, then a crisp ink outline — gives the flat shapes some volume (design pass, iteration D1).
   */
  private orb(g: Phaser.GameObjects.Graphics, x: number, y: number, w: number, h: number, color: number, outline = 2.5): void {
    const dark = Phaser.Display.Color.IntegerToColor(color).darken(18).color;
    g.fillStyle(dark, 1);
    g.fillEllipse(x, y, w, h);
    g.fillStyle(color, 1);
    g.fillEllipse(x - w * 0.06, y - h * 0.07, w * 0.86, h * 0.84);
    g.fillStyle(0xffffff, 0.28);
    g.fillEllipse(x - w * 0.2, y - h * 0.24, w * 0.32, h * 0.2);
    if (outline > 0) {
      g.lineStyle(outline, C.ink, 1);
      g.strokeEllipse(x, y, w, h);
    }
  }

  private makeHero(id: string): void {
    const g = this.g();
    this.roleOutlines(g, 3);
    const w = 52;
    const h = 70; // 60 clipped Fen's cap, Hazel's nightcap and Sorrel's ears; the art is drawn up from the feet
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
      // a quiver of arrows on the back (behind the body)
      g.fillStyle(0x7a5232, 1);
      g.fillRoundedRect(cx + 5, base - 44, 7, 20, 3);
      g.lineStyle(2, C.ink, 1);
      g.strokeRoundedRect(cx + 5, base - 44, 7, 20, 3);
      g.fillStyle(0xe8e0c8, 1);
      for (let k = 0; k < 3; k++) g.fillTriangle(cx + 5 + k * 2.5, base - 44, cx + 7 + k * 2.5, base - 44, cx + 6 + k * 2.5, base - 50);
      this.orb(g, cx, base - 26, 22, 22, 0xdde8f0, 3);
      g.fillStyle(0x7fb0d8, 1);
      g.fillEllipse(cx + 3, base - 24, 14, 16);
      g.fillStyle(0x5a8ab8, 0.6);
      g.fillEllipse(cx + 5, base - 21, 9, 9);
      // a knitted scarf
      g.fillStyle(0xd8584a, 1);
      g.fillRoundedRect(cx - 6, base - 37, 12, 5, 2);
      g.fillRect(cx - 5, base - 34, 4, 9);
      g.fillStyle(0xf09080, 1);
      g.fillRect(cx - 5, base - 30, 4, 1.5);
      g.fillStyle(0xdde8f0, 1);
      g.fillRect(cx - 3, base - 46, 6, 10);
      this.orb(g, cx, base - 46, 14, 14, 0xdde8f0, 3);
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
    } else if (id === 'hazel') {
      // dormouse: round golden-brown body, big round ears, black bead eyes, patchwork nightcap, fluffy tail
      g.fillStyle(0xb88a5a, 1);
      g.fillEllipse(cx + 14, base - 14, 12, 20);
      g.strokeEllipse(cx + 14, base - 14, 12, 20);
      this.orb(g, cx, base - 18, 26, 28, 0xd8b088, 3);
      g.fillStyle(0xf4e4c8, 1);
      g.fillEllipse(cx, base - 14, 14, 16);
      // a tiny lantern on a stick, glowing warm
      g.lineStyle(2, 0x7a5232, 1);
      g.lineBetween(cx - 10, base - 14, cx - 15, base - 30);
      g.fillStyle(0xffd060, 0.35);
      g.fillCircle(cx - 16, base - 26, 7);
      g.fillStyle(0x5a4a3a, 1);
      g.fillRect(cx - 19, base - 31, 7, 2);
      g.fillStyle(0xffe680, 1);
      g.fillRoundedRect(cx - 18.5, base - 29, 6, 7, 2);
      g.lineStyle(1.5, C.ink, 1);
      g.strokeRoundedRect(cx - 18.5, base - 29, 6, 7, 2);
      g.fillStyle(0xd8b088, 1);
      g.fillCircle(cx - 9, base - 46, 7);
      g.fillCircle(cx + 9, base - 46, 7);
      g.strokeCircle(cx - 9, base - 46, 7);
      g.strokeCircle(cx + 9, base - 46, 7);
      g.fillStyle(0xf0b8b8, 1);
      g.fillCircle(cx - 9, base - 46, 3.5);
      g.fillCircle(cx + 9, base - 46, 3.5);
      this.orb(g, cx, base - 37, 22, 22, 0xd8b088, 3);
      g.fillStyle(0x111111, 1);
      g.fillCircle(cx - 4, base - 38, 2.6);
      g.fillCircle(cx + 4, base - 38, 2.6);
      g.fillStyle(0xffffff, 1);
      g.fillCircle(cx - 3.3, base - 38.8, 0.9);
      g.fillCircle(cx + 4.7, base - 38.8, 0.9);
      g.fillStyle(0xe88a9a, 1);
      g.fillCircle(cx, base - 34, 1.6);
      // patchwork nightcap flopping to one side, with a pompom
      g.fillStyle(0x8a6ad8, 1);
      g.fillTriangle(cx - 10, base - 45, cx + 10, base - 45, cx + 16, base - 58);
      g.lineStyle(2, C.ink, 1);
      g.strokeTriangle(cx - 10, base - 45, cx + 10, base - 45, cx + 16, base - 58);
      g.fillStyle(0xf0d070, 1);
      g.fillTriangle(cx - 2, base - 45, cx + 6, base - 45, cx + 6, base - 51);
      g.fillStyle(0xffffff, 1);
      g.fillCircle(cx + 16, base - 58, 3);
    } else if (id === 'sorrel') {
      // hare medic: long upright ears, cream belly, a red-cross moss satchel, sling in paw
      this.orb(g, cx, base - 18, 24, 28, 0xc8a888, 3);
      g.fillStyle(0xf4e8d8, 1);
      g.fillEllipse(cx, base - 15, 13, 18);
      // satchel strap across the chest
      g.lineStyle(2.5, 0x8a6a4a, 1);
      g.lineBetween(cx + 9, base - 30, cx - 11, base - 18);
      // ears
      g.fillStyle(0xc8a888, 1);
      g.fillEllipse(cx - 6, base - 56, 7, 22);
      g.fillEllipse(cx + 5, base - 57, 7, 22);
      g.strokeEllipse(cx - 6, base - 56, 7, 22);
      g.strokeEllipse(cx + 5, base - 57, 7, 22);
      g.fillStyle(0xf0b8b8, 1);
      g.fillEllipse(cx - 6, base - 55, 3, 15);
      g.fillEllipse(cx + 5, base - 56, 3, 15);
      // head
      this.orb(g, cx, base - 38, 22, 22, 0xc8a888, 3);
      // a white medic headband with a green leaf
      g.fillStyle(0xf4f0e0, 1);
      g.fillRect(cx - 10, base - 45, 20, 3.5);
      g.fillStyle(0x4fae4a, 1);
      g.fillEllipse(cx + 6, base - 43.5, 5, 3);
      g.fillStyle(0x111111, 1);
      g.fillCircle(cx - 4, base - 40, 2);
      g.fillCircle(cx + 4, base - 40, 2);
      g.fillStyle(0xe88a9a, 1);
      g.fillCircle(cx, base - 35, 2);
      // satchel with a green leaf cross
      g.fillStyle(0xf4f0e0, 1);
      g.fillRoundedRect(cx - 18, base - 24, 13, 12, 3);
      g.lineStyle(2, C.ink, 1);
      g.strokeRoundedRect(cx - 18, base - 24, 13, 12, 3);
      g.fillStyle(0x4fae4a, 1);
      g.fillRect(cx - 13, base - 22, 3, 8);
      g.fillRect(cx - 15.5, base - 19.5, 8, 3);
      // sling
      g.lineStyle(2, 0x7a5232, 1);
      g.lineBetween(cx + 10, base - 26, cx + 16, base - 36);
      g.fillStyle(0xb8b0a0, 1);
      g.fillCircle(cx + 16, base - 37, 3);
      // feet
      g.fillStyle(0xc8a888, 1);
      g.fillEllipse(cx - 6, base - 2, 10, 5);
      g.fillEllipse(cx + 6, base - 2, 10, 5);
    } else if (id === 'wren') {
      // barn owl: round heart-shaped face, wings folded, scroll satchel
      this.orb(g, cx, base - 18, 26, 30, 0xb8905a, 3);
      // speckled chest feathers
      g.fillStyle(0xf0dcb0, 1);
      g.fillEllipse(cx, base - 14, 12, 16);
      g.fillStyle(0x8a6a3a, 1);
      for (const [dx, dy] of [[-3, -18], [2, -15], [-1, -11], [3, -9]]) g.fillCircle(cx + dx, base + dy, 0.9);
      g.fillStyle(0x9a7444, 1);
      g.fillEllipse(cx - 11, base - 18, 8, 22);
      g.fillEllipse(cx + 11, base - 18, 8, 22);
      this.orb(g, cx, base - 38, 26, 26, 0xd8b880, 3);
      g.fillStyle(0xfff4e0, 1);
      g.fillEllipse(cx - 5, base - 38, 11, 14);
      g.fillEllipse(cx + 5, base - 38, 11, 14);
      g.fillStyle(0x111111, 1);
      g.fillCircle(cx - 5, base - 39, 2.4);
      g.fillCircle(cx + 5, base - 39, 2.4);
      g.fillStyle(0xe0a040, 1);
      g.fillTriangle(cx - 2, base - 35, cx + 2, base - 35, cx, base - 30);
      // round reading spectacles
      g.lineStyle(1.5, 0x5a4020, 1);
      g.strokeCircle(cx - 5, base - 39, 4.5);
      g.strokeCircle(cx + 5, base - 39, 4.5);
      g.lineBetween(cx - 0.5, base - 39, cx + 0.5, base - 39);
      g.fillStyle(0xffffff, 0.35);
      g.fillCircle(cx - 6.5, base - 41, 1.2);
      g.fillCircle(cx + 3.5, base - 41, 1.2);
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
      g.fillStyle(0x6a3478, 1);
      g.fillRoundedRect(cx - 9, base - 30, 18, 26, 7);
      g.fillStyle(0x8a4a9a, 1);
      g.fillRoundedRect(cx - 9, base - 30, 15, 24, 7);
      g.fillStyle(0xffffff, 0.2);
      g.fillRoundedRect(cx - 7, base - 28, 5, 12, 3);
      // gold trim down the robe and along its hem
      g.fillStyle(0xf0c040, 1);
      g.fillRect(cx - 1, base - 26, 2, 21);
      g.fillRect(cx - 8, base - 7, 16, 2.5);
      g.lineStyle(3, C.ink, 1);
      g.strokeRoundedRect(cx - 9, base - 30, 18, 26, 7);
      this.orb(g, cx, base - 36, 20, 20, 0xff8a3c, 3);
      g.fillStyle(0xff8a3c, 1);
      g.fillTriangle(cx - 9, base - 40, cx - 3, base - 44, cx - 8, base - 52);
      g.fillTriangle(cx + 9, base - 40, cx + 3, base - 44, cx + 8, base - 52);
      g.fillStyle(0xffffff, 1);
      g.fillEllipse(cx, base - 32, 10, 6);
      g.fillStyle(0x111111, 1);
      g.fillCircle(cx - 4, base - 38, 1.8);
      g.fillCircle(cx + 4, base - 38, 1.8);
      g.fillCircle(cx, base - 33, 1.5);
      // the flame in her paw: a soft halo, an orange tongue and a white-hot core
      g.fillStyle(0xffd23c, 0.28);
      g.fillCircle(cx + 15, base - 27, 10);
      g.fillStyle(0xff8a3c, 1);
      g.fillTriangle(cx + 10, base - 25, cx + 20, base - 25, cx + 15, base - 39);
      g.fillCircle(cx + 15, base - 25, 5);
      g.fillStyle(0xffe680, 1);
      g.fillCircle(cx + 15, base - 26, 3.5);
      g.fillStyle(0xffffff, 1);
      g.fillCircle(cx + 15, base - 26.5, 1.6);
    } else {
      // badger knight with bark armor, a red cape and a wooden sword
      g.fillStyle(0xa8302a, 1);
      g.fillTriangle(cx - 13, base - 30, cx + 13, base - 30, cx + 16, base - 4);
      g.fillTriangle(cx - 13, base - 30, cx - 16, base - 4, cx + 16, base - 4);
      g.fillStyle(0x7a1e1a, 1);
      g.fillTriangle(cx + 4, base - 28, cx + 13, base - 30, cx + 16, base - 4);
      g.lineStyle(2, C.ink, 1);
      g.strokeTriangle(cx - 13, base - 30, cx - 16, base - 4, cx + 16, base - 4);
      g.fillStyle(0x5a3a1e, 1);
      g.fillRoundedRect(cx - 12, base - 28, 24, 24, 8);
      g.fillStyle(0x7a5232, 1);
      g.fillRoundedRect(cx - 12, base - 28, 21, 22, 8);
      g.fillStyle(0xffffff, 0.18);
      g.fillRoundedRect(cx - 10, base - 26, 7, 10, 4);
      g.lineStyle(3, C.ink, 1);
      g.strokeRoundedRect(cx - 12, base - 28, 24, 24, 8);
      g.fillStyle(0x9a6a40, 1);
      g.fillRect(cx - 10, base - 22, 20, 4);
      g.fillStyle(0xf0c040, 1);
      g.fillCircle(cx, base - 20, 2);
      this.orb(g, cx, base - 36, 24, 24, 0x3b3b3b, 3);
      // a little crest of leaves on top of the head
      g.fillStyle(0x6ab04c, 1);
      g.fillEllipse(cx - 3, base - 49, 5, 9);
      g.fillEllipse(cx + 3, base - 50, 5, 10);
      g.lineStyle(1.5, C.ink, 1);
      g.strokeEllipse(cx + 3, base - 50, 5, 10);
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
    proj('proj_hero_sorrel', 0xb8b0a0, 4); // sling pebble
    proj('proj_hero_hazel', 0xc8a8ff, 4); // dream-dart

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
