import Phaser from 'phaser';
import { fitWidth, pf } from '../ui/touch';
import { endlessBosses, endlessMutatorFor } from '../systems/endless';
import { todayString } from '../systems/daily';
import { music } from '../systems/music';
import { themeById } from '../data/musicThemes';
import { LEVELS, REGIONS, isLevelUnlocked, regionOf, totalStars } from '../data/levels';
import { ENEMIES } from '../data/enemies';
import { loadSave } from '../systems/save';
import { sfx } from '../systems/audio';
import { Button } from '../ui/Button';
import { clampPage, pageCount, pageItems } from '../ui/paging';
import { C, GAME_H, GAME_W, TEXT, textStyle } from '../ui/theme';

// Campaign overview: the Grove's lands from the Mossgate (bottom-left) to Murkmaw's Den (top-right).
export class WorldMapScene extends Phaser.Scene {
  private panel: Phaser.GameObjects.Container | null = null;
  private region = 0;

  constructor() {
    super('WorldMap');
  }

  create(data: { focus?: number; region?: number }): void {
    music.setMood('calm');
    music.setTheme(themeById('home'));
    this.panel = null;
    const save = loadSave();
    // Pick the region: explicit, else the focused level's, else the furthest unlocked level's.
    let furthest = 0;
    LEVELS.forEach((_, i) => {
      if (isLevelUnlocked(i, save.stars)) furthest = i;
    });
    this.region = data?.region ?? regionOf(data?.focus ?? furthest);
    const reg = REGIONS[this.region];
    const inRegion = LEVELS.map((_, i) => i).filter((i) => regionOf(i) === this.region);

    this.drawLand(reg.bog ? 'bog' : reg.comb ? 'comb' : reg.canopy ? 'canopy' : reg.mist ? 'mist' : reg.amber ? 'amber' : reg.flotilla ? 'flotilla' : reg.reef ? 'reef' : reg.dunes ? 'dunes' : reg.storm ? 'storm' : reg.orchard ? 'orchard' : reg.abyss ? 'abyss' : reg.gears ? 'brass' : reg.ruins ? 'ruins' : reg.gale ? 'gale' : reg.glass ? 'glass' : reg.shoal ? 'shoal' : reg.dusk ? 'dusk' : reg.snow ? 'snow' : reg.ember ? 'ember' : 'meadow');
    this.drawTrail(save.stars, inRegion);
    inRegion.forEach((i) => this.makeNode(i, isLevelUnlocked(i, save.stars), save.stars[LEVELS[i].id] ?? 0));
    // Placeholders for levels still to come in this region.
    const missing = reg.count - inRegion.length;
    for (let k = 0; k < missing; k++) {
      const x = missing === 1 ? 1060 : 940 + (k * 240) / (missing - 1); // spread between x=940 and x=1180
      this.add.text(x, 640, '?', textStyle(28, TEXT.dim)).setOrigin(0.5).setAlpha(0.6);
    }
    if (inRegion.length < reg.count) this.add.text(1060, 680, 'More lands coming soon…', textStyle(pf(14), TEXT.dim, false)).setOrigin(0.5);

    // Top bar
    const bar = this.add.graphics().setDepth(100);
    bar.fillStyle(C.ink, 0.75);
    bar.fillRoundedRect(GAME_W / 2 - 260, 10, 520, 56, 18);
    // Right-aligned against the star counter; long region names shrink to fit between the '<' button and the star.
    const title = this.add.text(GAME_W / 2 + 108, 38, reg.name, textStyle(26, TEXT.gold)).setOrigin(1, 0.5).setDepth(101);
    if (title.width > 350) title.setScale(350 / title.width);
    this.add.image(GAME_W / 2 + 130, 38, 'star').setScale(0.55).setDepth(101);
    this.add.text(GAME_W / 2 + 152, 38, `${totalStars(save.stars)}/${LEVELS.length * 3}`, textStyle(22)).setOrigin(0, 0.5).setDepth(101);
    new Button(this, 90, 40, 'Back', { width: 140, height: 50, fontSize: 22, color: C.sky, onClick: () => this.scene.start('Menu') }).setDepth(101);

    // Region arrows
    if (this.region > 0) {
      new Button(this, GAME_W / 2 - 300, 38, '<', { width: 56, height: 50, fontSize: 24, color: C.sky, onClick: () => this.scene.restart({ region: this.region - 1 }) }).setDepth(101);
    }
    if (this.region < REGIONS.length - 1) {
      const next = REGIONS[this.region + 1];
      const open = isLevelUnlocked(next.first, save.stars) && next.first < LEVELS.length;
      new Button(this, GAME_W / 2 + 300, 38, '>', {
        width: 56,
        height: 50,
        fontSize: 24,
        color: open ? 0xff9f43 : 0x777777,
        onClick: () => {
          if (open) this.scene.restart({ region: this.region + 1 });
          else this.toast(`Beat ${LEVELS[next.first - 1].name} to reach ${next.name}`);
        },
      }).setDepth(101);
    }

    // Jump straight to any region you've reached (15+ regions make the arrows slow going).
    new Button(this, GAME_W - 100, 40, 'Regions', { width: 160, height: 50, fontSize: 22, color: 0xff9f43, onClick: () => this.openRegionPicker() }).setDepth(101);

    this.input.on('pointerdown', () => this.closePanel());
    this.cameras.main.fadeIn(250, 16, 38, 27);

    // Open the info card for the focused level (e.g. the next level after a win).
    const focus = data?.focus;
    if (focus !== undefined && focus >= 0 && focus < LEVELS.length && regionOf(focus) === this.region && isLevelUnlocked(focus, save.stars)) {
      this.time.delayedCall(250, () => this.openPanel(focus));
    }
  }

  private toast(msg: string): void {
    this.children.getByName('toast')?.destroy();
    const t = this.add.text(GAME_W / 2, 100, msg, textStyle(18, TEXT.heart)).setOrigin(0.5).setDepth(300).setName('toast');
    this.tweens.add({ targets: t, alpha: 0, delay: 1600, duration: 400, onComplete: () => t.destroy() });
  }

  private drawLand(style: 'meadow' | 'snow' | 'ember' | 'dusk' | 'shoal' | 'glass' | 'gale' | 'ruins' | 'brass' | 'abyss' | 'orchard' | 'storm' | 'dunes' | 'reef' | 'flotilla' | 'amber' | 'mist' | 'canopy' | 'comb' | 'bog'): void {
    const bog = style === 'bog';
    const comb = style === 'comb';
    const canopy = style === 'canopy';
    const mist = style === 'mist';
    const amber = style === 'amber';
    const flotilla = style === 'flotilla';
    const reef = style === 'reef';
    const dunes = style === 'dunes';
    const storm = style === 'storm';
    const orchard = style === 'orchard';
    const abyss = style === 'abyss';
    const brass = style === 'brass';
    const ruins = style === 'ruins';
    const gale = style === 'gale';
    const glass = style === 'glass';
    const shoal = style === 'shoal';
    const snow = style === 'snow';
    const ember = style === 'ember';
    const dusk = style === 'dusk';
    const g = this.add.graphics();
    g.fillStyle(bog ? 0x0e2230 : comb ? 0x6a8ab8 : canopy ? 0x1e3a22 : mist ? 0x8aa8b8 : amber ? 0x2f5a6a : flotilla ? 0x0a1a2a : reef ? 0x1a5a9a : dunes ? 0x3a8aa8 : storm ? 0x2a3040 : orchard ? 0x5a8aa8 : abyss ? 0x080a18 : brass ? 0x1a1a22 : ruins ? 0x1f5a5a : gale ? 0x9ac8e8 : glass ? 0x241a3a : shoal ? 0x1f6a80 : dusk ? 0x1e2340 : ember ? 0x2a1a18 : snow ? 0x2a4f6a : 0x2f6e8f, 1); // sea (or ash wastes, or night mist)
    g.fillRect(-20, -20, GAME_W + 40, GAME_H + 40);
    // main island
    g.fillStyle(bog ? 0x2a4a3a : comb ? 0xe8d088 : canopy ? 0x2a5a2a : mist ? 0xc8d4c8 : amber ? 0xd8b070 : flotilla ? 0x1a3a52 : reef ? 0xf0e0b0 : dunes ? 0xf0dca8 : storm ? 0x9a9a88 : orchard ? 0xd8c890 : abyss ? 0x3a3a6a : brass ? 0x8a6a2a : ruins ? 0xc8b890 : gale ? 0xf4f8fc : glass ? 0x6a5a88 : shoal ? 0xf0e2b8 : dusk ? 0x5a4a6a : ember ? 0x3a2a24 : snow ? 0xb8c4cc : 0xd9c79a, 1);
    g.fillEllipse(GAME_W / 2, GAME_H / 2 + 20, GAME_W * 1.02, GAME_H * 0.98);
    g.fillStyle(bog ? 0x3a5a4a : comb ? 0xb8a848 : canopy ? 0x3f6e38 : mist ? 0x7aa878 : amber ? 0x9a7a3a : flotilla ? 0x2a5a7a : reef ? 0x5ac0c8 : dunes ? 0xe0c088 : storm ? 0x7a8a6a : orchard ? 0xa8a050 : abyss ? 0x1e2440 : brass ? 0x5a5a62 : ruins ? 0x4a8a3a : gale ? 0x9cbca0 : glass ? 0x8a7aa8 : shoal ? 0xdcc898 : dusk ? 0x4a5a78 : ember ? 0x5a4a44 : snow ? 0xe6eef2 : 0x6aae52, 1);
    g.fillEllipse(GAME_W / 2, GAME_H / 2 + 20, GAME_W * 0.98, GAME_H * 0.92);
    // regions
    const regions: [number, number, number, number, number][] = bog
      ? [
          [0x2f5040, 230, 560, 420, 260],
          [0x1e3a3a, 480, 420, 320, 230],
          [0x3a6048, 760, 300, 340, 240],
          [0x203a34, 1020, 420, 320, 220],
          [0x34584a, 1100, 200, 340, 240],
        ]
      : comb
      ? [
          [0xc8b858, 230, 560, 420, 260],
          [0xa89a40, 480, 420, 320, 230],
          [0xd8c060, 760, 300, 340, 240],
          [0x9a9a3a, 1020, 420, 320, 220],
          [0xe0b850, 1100, 200, 340, 240],
        ]
      : canopy
      ? [
          [0x4a7a40, 230, 560, 420, 260],
          [0x3a6a34, 480, 420, 320, 230],
          [0x5a8a46, 760, 300, 340, 240],
          [0x2f5e2c, 1020, 420, 320, 220],
          [0x4a8a50, 1100, 200, 340, 240],
        ]
      : mist
      ? [
          [0x8ab888, 230, 560, 420, 260],
          [0x6a9868, 480, 420, 320, 230],
          [0x9ac8a0, 760, 300, 340, 240],
          [0x7aa888, 1020, 420, 320, 220],
          [0xb8c8c0, 1100, 200, 340, 240],
        ]
      : amber
      ? [
          [0xa8843e, 230, 560, 420, 260],
          [0xb8682e, 480, 420, 320, 230],
          [0x9a4a2a, 760, 300, 340, 240],
          [0xc89a3a, 1020, 420, 320, 220],
          [0x7a3a3a, 1100, 200, 340, 240],
        ]
      : flotilla
      ? [
          [0x32647e, 230, 560, 420, 260],
          [0x26506a, 480, 420, 320, 230],
          [0x1e4660, 760, 300, 340, 240],
          [0x2e5a74, 1020, 420, 320, 220],
          [0x163a52, 1100, 200, 340, 240],
        ]
      : reef
      ? [
          [0x6ad0d0, 230, 560, 420, 260],
          [0x4ab0c0, 480, 420, 320, 230],
          [0x3a98b8, 760, 300, 340, 240],
          [0x5ac8c0, 1020, 420, 320, 220],
          [0x2a80a8, 1100, 200, 340, 240],
        ]
      : dunes
      ? [
          [0xe8cc94, 230, 560, 420, 260],
          [0xd8b878, 480, 420, 320, 230],
          [0xc89a62, 760, 300, 340, 240],
          [0xe0b880, 1020, 420, 320, 220],
          [0xb8865a, 1100, 200, 340, 240],
        ]
      : storm
      ? [
          [0x8a9a72, 230, 560, 420, 260],
          [0x6e7e62, 480, 420, 320, 230],
          [0x7a7a6a, 760, 300, 340, 240],
          [0x6a7a5a, 1020, 420, 320, 220],
          [0x5a5e62, 1100, 200, 340, 240],
        ]
      : orchard
      ? [
          [0xb8b060, 230, 560, 420, 260],
          [0x9a9248, 480, 420, 320, 230],
          [0x8a6a3a, 760, 300, 340, 240],
          [0x7a8a44, 1020, 420, 320, 220],
          [0x6a5a4a, 1100, 200, 340, 240],
        ]
      : abyss
      ? [
          [0x262c50, 230, 560, 420, 260],
          [0x1a1e3a, 480, 420, 320, 230],
          [0x2a2050, 760, 300, 340, 240],
          [0x1e2a44, 1020, 420, 320, 220],
          [0x161830, 1100, 200, 340, 240],
        ]
      : brass
      ? [
          [0x6a6a72, 230, 560, 420, 260],
          [0x4e4e58, 480, 420, 320, 230],
          [0x6a5a44, 760, 300, 340, 240],
          [0x52525c, 1020, 420, 320, 220],
          [0x44444c, 1100, 200, 340, 240],
        ]
      : ruins
      ? [
          [0x5a9a44, 230, 560, 420, 260],
          [0x3f7f34, 480, 420, 320, 230],
          [0x2f6a2a, 760, 300, 340, 240],
          [0x4a8a5a, 1020, 420, 320, 220],
          [0x2a5a2a, 1100, 200, 340, 240],
        ]
      : gale
      ? [
          [0xb0ccb0, 230, 560, 420, 260],
          [0xa0b8a8, 480, 420, 320, 230],
          [0x94aca4, 760, 300, 340, 240],
          [0xa8b8c0, 1020, 420, 320, 220],
          [0x8a9aa8, 1100, 200, 340, 240],
        ]
      : glass
      ? [
          [0x9a8ab8, 230, 560, 420, 260],
          [0x8070a8, 480, 420, 320, 230],
          [0x7a6aa0, 760, 300, 340, 240],
          [0x6a7ab0, 1020, 420, 320, 220],
          [0x6a5a98, 1100, 200, 340, 240],
        ]
      : shoal
      ? [
          [0xe6d4a4, 230, 560, 420, 260],
          [0xd2bf8c, 480, 420, 320, 230],
          [0xc8b482, 760, 300, 340, 240],
          [0x8fc8b8, 1020, 420, 320, 220],
          [0xb8a678, 1100, 200, 340, 240],
        ]
      : dusk
      ? [
          [0x56688a, 230, 560, 420, 260],
          [0x4e5c80, 480, 420, 320, 230],
          [0x5a4e80, 760, 300, 340, 240],
          [0x4a4a74, 1020, 420, 320, 220],
          [0x40406a, 1100, 200, 340, 240],
        ]
      : ember
      ? [
          [0x6a5a50, 230, 560, 420, 260],
          [0x5f4a42, 480, 420, 320, 230],
          [0x553f38, 760, 300, 340, 240],
          [0x4a3530, 1020, 420, 320, 220],
          [0x40302c, 1100, 200, 340, 240],
        ]
      : snow
      ? [
          [0xd4e2ea, 230, 560, 420, 260],
          [0xc6d8e4, 480, 420, 320, 230],
          [0xb4c8d6, 760, 300, 340, 240],
          [0xa8bccc, 1020, 420, 320, 220],
          [0x9fb2c2, 1100, 200, 340, 240],
        ]
      : [
          [0x86c56a, 230, 560, 420, 260], // meadow
          [0x5f8f5a, 420, 430, 300, 220], // fen
          [0x3f7a3a, 620, 300, 340, 240], // forest
          [0x4f9a8a, 860, 440, 320, 220], // lake shore
          [0x3a5a40, 1080, 230, 360, 260], // den
        ];
    for (const [col, x, y, w, h] of regions) {
      g.fillStyle(col, 0.85);
      g.fillEllipse(x, y, w, h);
    }
    // lake (frozen in the highlands)
    g.fillStyle(bog ? 0x123040 : comb ? 0xd89a20 : canopy ? 0x2a4a2a : mist ? 0x9ac8d8 : amber ? 0x5a8aa8 : flotilla ? 0x123048 : reef ? 0xf0e0b0 : dunes ? 0x5ac8c8 : storm ? 0x6a8aaa : orchard ? 0x6aaac8 : abyss ? 0x5ae8d0 : brass ? 0xff8a3c : ruins ? 0x3aa8a0 : gale ? 0xe8f4ff : glass ? 0xb8e8f8 : shoal ? 0x4ac0d8 : dusk ? 0x7ad8c8 : ember ? 0xff6a2a : snow ? 0xbfe3f2 : 0x5fb8d8, 1);
    g.fillEllipse(900, 520, 200, 90);
    g.fillStyle(0xffffff, 0.4);
    g.fillEllipse(870, 505, 60, 14);
    // trees / reeds decoration (deterministic)
    const rnd = new Phaser.Math.RandomDataGenerator(['grovelands']);
    for (let i = 0; i < 90; i++) {
      const x = rnd.between(80, GAME_W - 80);
      const y = rnd.between(110, GAME_H - 60);
      if (LEVELS.some((l, i) => regionOf(i) === this.region && Math.hypot(l.mapPos.x - x, l.mapPos.y - y) < 70)) continue;
      if (Math.hypot((x - 900) / 110, (y - 520) / 55) < 1) continue;
      const dark = x > 960 && y < 380;
      if (bog) {
        // lily pads and reeds, with the odd firefly
        const f = rnd.frac();
        if (f < 0.55) {
          g.fillStyle(rnd.pick([0x3a8a4a, 0x4a9a5a]), 1);
          g.fillCircle(x, y, 5);
        } else if (f < 0.9) {
          g.fillStyle(0x6a4a2a, 1);
          g.fillRect(x - 1, y - 7, 2, 8);
          g.fillRect(x + 3, y - 5, 2, 6);
        } else {
          g.fillStyle(0xe8ff8a, 0.9);
          g.fillCircle(x, y, 2);
        }
        continue;
      }
      if (comb) {
        // clover and flowers, with the odd wild hive
        if (rnd.frac() < 0.8) {
          g.fillStyle(rnd.pick([0x8a9a3a, 0x6a8a2a, 0xa8a848]), 1);
          g.fillCircle(x - 3, y, 4);
          g.fillCircle(x + 3, y, 4);
          g.fillStyle(rnd.pick([0xf4d8e8, 0xffffff, 0xf0c040]), 1);
          g.fillCircle(x, y - 4, 3);
        } else {
          g.fillStyle(0xe8b030, 1);
          g.fillEllipse(x, y, 10, 13);
          g.fillStyle(0x9a6a20, 1);
          g.fillRect(x - 4, y - 1, 8, 1.5);
        }
        continue;
      }
      if (canopy) {
        // the tops of giant trees: clumps of leaves, with the odd plank platform
        if (rnd.frac() < 0.8) {
          g.fillStyle(rnd.pick([0x3f8a3a, 0x5aa04a, 0x2f6a3a]), 1);
          g.fillCircle(x - 4, y, 6);
          g.fillCircle(x + 4, y - 1, 6);
          g.fillCircle(x, y - 5, 6);
        } else {
          g.fillStyle(0xb08a5e, 1);
          g.fillRect(x - 8, y - 2, 16, 4);
        }
        continue;
      }
      if (mist) {
        // rows of tea bushes, with the odd cherry tree in pink blossom
        if (rnd.frac() < 0.7) {
          g.fillStyle(0x4a7a4a, 1);
          g.fillRoundedRect(x - 10, y - 3, 20, 7, 3);
          g.fillStyle(0x6a9a5a, 1);
          g.fillRoundedRect(x - 8, y - 5, 16, 4, 2);
        } else {
          g.fillStyle(0x5a3a2a, 1);
          g.fillRect(x - 1.5, y, 3, 7);
          g.fillStyle(0xe89ab8, 1);
          g.fillCircle(x, y - 3, 7);
        }
        continue;
      }
      if (amber) {
        // round autumn trees in reds, oranges and golds, with the odd fallen leaf
        if (rnd.frac() < 0.75) {
          g.fillStyle(0x5a3a22, 1);
          g.fillRect(x - 1.5, y, 3, 8);
          g.fillStyle(rnd.pick([0xc83a1a, 0xe87a1a, 0xf0c040, 0x8a3a5a]), 1);
          g.fillCircle(x, y - 4, 8);
          g.fillStyle(0xffffff, 0.18);
          g.fillCircle(x - 3, y - 7, 3);
        } else {
          g.fillStyle(0xe87a1a, 0.9);
          g.fillEllipse(x, y, 7, 4);
        }
        continue;
      }
      if (flotilla) {
        // little ships with pale sails, and whitecaps between them
        if (rnd.frac() < 0.35) {
          g.fillStyle(0x6a4a2a, 1);
          g.fillRoundedRect(x - 9, y, 18, 6, 3);
          g.fillStyle(0xe8e0c8, 1);
          g.fillTriangle(x - 1, y - 2, x - 1, y - 16, x + 8, y - 2);
          g.fillStyle(0x2a2a32, 1);
          g.fillTriangle(x - 3, y - 2, x - 3, y - 13, x - 9, y - 2);
        } else {
          g.lineStyle(2, 0xbfe0f0, 0.7);
          g.beginPath();
          g.arc(x, y, 6, Math.PI * 1.1, Math.PI * 1.9);
          g.strokePath();
        }
        continue;
      }
      if (reef) {
        // coral heads and the odd starfish
        if (rnd.frac() < 0.7) {
          g.fillStyle(rnd.pick([0xf07a6a, 0xf0a05a, 0xd86aa8]), 1);
          g.fillCircle(x, y, rnd.between(4, 7));
          g.fillCircle(x + 5, y - 3, rnd.between(3, 5));
          g.fillCircle(x - 4, y - 4, rnd.between(3, 5));
        } else {
          g.fillStyle(0xf0905a, 1);
          for (let k = 0; k < 5; k++) {
            const a = (k / 5) * Math.PI * 2 - Math.PI / 2;
            g.fillTriangle(x, y, x + Math.cos(a - 0.3) * 3, y + Math.sin(a - 0.3) * 3, x + Math.cos(a) * 8, y + Math.sin(a) * 8);
            g.fillTriangle(x, y, x + Math.cos(a + 0.3) * 3, y + Math.sin(a + 0.3) * 3, x + Math.cos(a) * 8, y + Math.sin(a) * 8);
          }
        }
        continue;
      }
      if (dunes) {
        // little cacti and wind-rippled sand
        if (rnd.frac() < 0.5) {
          g.fillStyle(rnd.pick([0x6a9a4a, 0x5a8a3a]), 1);
          g.fillRoundedRect(x - 3, y - 14, 6, 18, 3);
          g.fillRoundedRect(x - 9, y - 9, 5, 8, 2);
          g.fillRoundedRect(x + 4, y - 11, 5, 8, 2);
        } else {
          g.lineStyle(2, 0xc8a068, 0.8);
          g.beginPath();
          g.arc(x, y + 6, 12, Math.PI * 1.15, Math.PI * 1.85);
          g.strokePath();
        }
        continue;
      }
      if (storm) {
        // wind-bent grass tufts and grey standing stones
        if (rnd.frac() < 0.65) {
          g.lineStyle(2, rnd.pick([0x5a6a4a, 0x8a9a6a, 0x6a7a52]), 1);
          for (let k = -1; k <= 1; k++) g.lineBetween(x + k * 3, y + 4, x + k * 3 + 6, y - 7);
        } else {
          g.fillStyle(0x6a6a72, 1);
          g.fillRoundedRect(x - 4, y - 12, 9, 16, 3);
        }
        continue;
      }
      if (orchard) {
        // rows of autumn fruit trees
        g.fillStyle(rnd.pick([0xd8642a, 0xe8a03a, 0xb8442a]), 1);
        g.fillCircle(x, y, rnd.between(7, 11));
        g.fillStyle(0xd02a2a, 1);
        g.fillCircle(x - 3, y + 1, 2);
        g.fillCircle(x + 3, y - 2, 2);
        continue;
      }
      if (abyss) {
        // twinkling motes and pale stalagmites
        if (rnd.frac() < 0.6) {
          g.fillStyle(rnd.pick([0x6ad8e8, 0x9a7ae8, 0x5ae8b0]), 0.9);
          g.fillCircle(x, y, rnd.between(2, 4));
        } else {
          g.fillStyle(0x4a4a6a, 1);
          g.fillTriangle(x - 6, y + 6, x + 6, y + 6, x, y - 14);
        }
        continue;
      }
      if (brass) {
        // little gears and pipe stubs
        if (rnd.frac() < 0.6) {
          g.fillStyle(rnd.pick([0xc8963a, 0x8a6a2a, 0xa0a0aa]), 1);
          const r0 = rnd.between(5, 9);
          for (let k = 0; k < 6; k++) { const a0 = (k / 6) * Math.PI * 2; g.fillRect(x + Math.cos(a0) * r0 - 2, y + Math.sin(a0) * r0 - 2, 4, 4); }
          g.fillCircle(x, y, r0);
          g.fillStyle(0x2a2a30, 1);
          g.fillCircle(x, y, r0 * 0.35);
        } else {
          g.fillStyle(0x7a7a84, 1);
          g.fillRect(x - 3, y - 12, 6, 16);
          g.fillStyle(0xffffff, 0.6);
          g.fillCircle(x + 2, y - 16, 4);
        }
        continue;
      }
      if (ruins) {
        // jungle canopy and the odd broken pillar
        if (rnd.frac() < 0.8) {
          g.fillStyle(rnd.pick([0x245a22, 0x2f6a2a, 0x3a7a30]), 1);
          g.fillCircle(x, y, rnd.between(8, 13));
          g.fillStyle(0x4a9a3a, 1);
          g.fillCircle(x - 3, y - 3, rnd.between(3, 6));
        } else {
          g.fillStyle(0xb8ae94, 1);
          g.fillRect(x - 4, y - 14, 8, 18);
          g.fillStyle(0x8a8270, 1);
          g.fillRect(x - 6, y - 16, 12, 4);
        }
        continue;
      }
      if (gale) {
        // wind-bent pines and grey cairns
        if (rnd.frac() < 0.7) {
          g.fillStyle(0x4a6a5a, 1);
          g.fillTriangle(x - 8, y + 8, x + 10, y + 8, x + 5, y - 14);
          g.fillStyle(0x5f8270, 1);
          g.fillTriangle(x - 4, y, x + 8, y, x + 6, y - 14);
        } else {
          g.fillStyle(0x8a8a90, 1);
          g.fillCircle(x, y + 2, 6);
          g.fillCircle(x + 1, y - 6, 4);
          g.fillCircle(x, y - 11, 2.5);
        }
        continue;
      }
      if (glass) {
        // small crystal spires
        const col = rnd.pick([0x9ad8f0, 0xc0a0f0, 0x80e8d0]);
        const h = rnd.between(10, 18);
        g.fillStyle(col, 0.95);
        g.fillTriangle(x - 5, y + 4, x + 5, y + 4, x, y - h);
        g.fillStyle(0xffffff, 0.5);
        g.fillTriangle(x - 1, y + 2, x + 2, y + 2, x, y - h + 3);
        continue;
      }
      if (shoal) {
        // shells, pebbles and the odd tuft of dune grass
        const k = rnd.between(0, 2);
        if (k === 0) {
          g.fillStyle(0xf6e6d0, 1);
          g.fillTriangle(x - 6, y + 4, x + 6, y + 4, x, y - 6);
          g.fillStyle(0xe0a890, 1);
          g.fillCircle(x, y + 2, 2);
        } else if (k === 1) {
          g.fillStyle(0x9a8a74, 1);
          g.fillCircle(x, y, rnd.between(3, 6));
        } else {
          g.lineStyle(2, 0x6a9a5a, 1);
          for (let q = -1; q <= 1; q++) g.lineBetween(x + q * 3, y + 6, x + q * 5, y - 8);
        }
        continue;
      }
      if (dusk) {
        // glowing mushrooms
        g.fillStyle(0xe8dcc8, 1);
        g.fillRect(x - 2, y - 6, 4, 10);
        g.fillStyle(rnd.pick([0x8a5ab8, 0xb85a8a, 0x5a8ab8]), 1);
        g.fillEllipse(x, y - 7, rnd.between(16, 24), 10);
        g.fillStyle(0xbff4ff, 0.9);
        g.fillCircle(x - 3, y - 9, 1.5);
        g.fillCircle(x + 3, y - 8, 1.5);
        continue;
      }
      if (ember) {
        // smoking rocks and dead trees
        g.fillStyle(0x2a201c, 1);
        g.fillCircle(x, y, rnd.between(6, 11));
        g.fillStyle(0xff8a3c, 0.6);
        g.fillCircle(x + 2, y - 2, 2);
        continue;
      }
      if (snow) {
        // pines with snow caps
        g.fillStyle(0x2f5a4a, 1);
        g.fillTriangle(x - 10, y + 8, x + 10, y + 8, x, y - 16);
        g.fillStyle(0xffffff, 1);
        g.fillTriangle(x - 5, y - 6, x + 5, y - 6, x, y - 16);
        continue;
      }
      g.fillStyle(dark ? 0x24412a : 0x2f6a30, 1);
      g.fillCircle(x, y, rnd.between(8, 14));
      g.fillStyle(dark ? 0x2f5236 : 0x3f8a3a, 1);
      g.fillCircle(x - 3, y - 3, rnd.between(4, 7));
    }
    // the trail's starting point
    g.fillStyle(0x9a6a40, 1);
    g.fillRect(60, 600, 60, 40);
    g.fillStyle(bog ? 0x8a7a5a : comb ? 0xe0b860 : canopy ? 0xb08a5e : mist ? 0x8a7e66 : amber ? 0xc83a1a : flotilla ? 0x2a2a32 : reef ? 0xf07a6a : dunes ? 0xd8a060 : storm ? 0x8a9aaa : orchard ? 0xd8642a : abyss ? 0x9a7ae8 : brass ? 0xc8963a : ruins ? 0x3f7f34 : gale ? 0xe8f4ff : glass ? 0x9ad8f0 : shoal ? 0x4a8ab8 : dusk ? 0x8a5ab8 : ember ? 0x8a3a2a : snow ? 0xffffff : 0x4b8f3a, 1);
    g.fillTriangle(50, 604, 130, 604, 90, 570);
    this.add.text(90, 692, bog ? 'Hive Steps' : comb ? 'Oldtree Roots' : canopy ? 'Shrine Steps' : mist ? 'Amber Edge' : amber ? 'Wreck Shore' : flotilla ? 'Coral Gate' : reef ? 'Dune Shore' : dunes ? 'Steppe Edge' : storm ? 'Orchard Gate' : orchard ? 'Homeward Road' : abyss ? 'Engine Deep' : brass ? 'Temple Stair' : ruins ? 'Cloud Stair' : gale ? 'Glass Pass' : glass ? 'Tideline' : shoal ? 'Weald Edge' : dusk ? 'Ember Gate' : ember ? 'Ash Road' : snow ? 'Mountain Gate' : 'Sanctuary', textStyle(pf(14))).setOrigin(0.5);
  }

  private drawTrail(stars: Record<string, number>, indices: number[]): void {
    const g = this.add.graphics();
    const pts = [{ x: 90, y: 600 }, ...indices.map((i) => LEVELS[i].mapPos)];
    for (let i = 1; i < pts.length; i++) {
      const a = pts[i - 1];
      const b = pts[i];
      const open = isLevelUnlocked(indices[i - 1], stars);
      const steps = Math.floor(Math.hypot(b.x - a.x, b.y - a.y) / 16);
      for (let k = 1; k < steps; k++) {
        const t = k / steps;
        // gentle curve
        const bend = Math.sin(t * Math.PI) * 30 * (i % 2 ? 1 : -1);
        const nx = -(b.y - a.y);
        const ny = b.x - a.x;
        const len = Math.hypot(nx, ny) || 1;
        g.fillStyle(open ? 0xfff4d6 : 0x55605a, open ? 0.95 : 0.6);
        g.fillCircle(a.x + (b.x - a.x) * t + (nx / len) * bend, a.y + (b.y - a.y) * t + (ny / len) * bend, 3.5);
      }
    }
  }

  private makeNode(i: number, unlocked: boolean, stars: number): void {
    const lvl = LEVELS[i];
    const { x, y } = lvl.mapPos;
    const c = this.add.container(x, y).setDepth(10);
    const g = this.add.graphics();
    g.fillStyle(0x000000, 0.3);
    g.fillEllipse(0, 30, 70, 20);
    g.fillStyle(C.ink, 1);
    g.fillCircle(0, 0, 36);
    g.fillStyle(unlocked ? (stars > 0 ? 0x6fae4a : 0xff9f43) : 0x5a625c, 1);
    g.fillCircle(0, 0, 31);
    g.fillStyle(0xffffff, 0.25);
    g.fillEllipse(-6, -12, 34, 16);
    c.add(g);
    if (unlocked) c.add(this.add.text(0, -1, String(i + 1), textStyle(30)).setOrigin(0.5));
    else {
      const lock = this.add.graphics();
      lock.lineStyle(4, 0xd0d4cc, 1);
      lock.beginPath();
      lock.arc(0, -4, 9, Math.PI, 0);
      lock.strokePath();
      lock.fillStyle(0xd0d4cc, 1);
      lock.fillRoundedRect(-13, -4, 26, 20, 4);
      lock.fillStyle(C.ink, 1);
      lock.fillCircle(0, 5, 3);
      c.add(lock);
    }
    for (let s = 0; s < 3; s++) c.add(this.add.image(-28 + s * 28, 44, s < stars ? 'star' : 'star_empty').setScale(0.48));
    c.add(this.add.text(0, 72, lvl.name, textStyle(16, unlocked ? TEXT.cream : TEXT.dim)).setOrigin(0.5));
    c.setSize(80, 80).setInteractive({ useHandCursor: unlocked });
    c.on('pointerdown', (_p: Phaser.Input.Pointer, _x: number, _y: number, ev: Phaser.Types.Input.EventData) => {
      ev.stopPropagation();
      sfx.unlock();
      if (!unlocked) {
        sfx.click();
        this.tweens.add({ targets: c, x: x + 6, duration: 40, yoyo: true, repeat: 2 });
        return;
      }
      sfx.click();
      this.openPanel(i);
    });
    // Pulse the next level to play.
    if (unlocked && stars === 0) this.tweens.add({ targets: c, scale: 1.1, yoyo: true, repeat: -1, duration: 600, ease: 'Sine.easeInOut' });
  }

  /** A grid of every region: unlocked ones show their stars and jump there; locked ones say what to beat. */
  /** Regions per picker page: 3 columns × 6 rows fill the screen. */
  static PICKER_PER_PAGE = 18;

  private openRegionPicker(page?: number): void {
    this.closePanel();
    const save = loadSave();
    const cols = 3;
    const perPage = WorldMapScene.PICKER_PER_PAGE;
    const pages = pageCount(REGIONS.length, perPage);
    const pg = clampPage(page ?? Math.floor(this.region / perPage), REGIONS.length, perPage);
    const first = pg * perPage;
    const shown = pageItems(REGIONS, pg, perPage);
    const rows = Math.ceil(Math.min(REGIONS.length, perPage) / cols);
    const cw = 330;
    const ch = 70;
    const W = cols * (cw + 14) + 26;
    const H = rows * (ch + 10) + 80;
    const p = this.add.container(GAME_W / 2, GAME_H / 2 + 20).setDepth(250);
    const bg = this.add.graphics();
    bg.fillStyle(C.ink, 0.96);
    bg.fillRoundedRect(-W / 2, -H / 2, W, H, 22);
    p.add(bg);
    const block = this.add.zone(0, 0, W, H).setInteractive();
    block.on('pointerdown', (_p: Phaser.Input.Pointer, _x: number, _y: number, ev: Phaser.Types.Input.EventData) => ev.stopPropagation());
    p.add(block);
    p.add(this.add.text(0, -H / 2 + 28, 'Choose a region', textStyle(24, TEXT.gold)).setOrigin(0.5));
    p.add(new Button(this, W / 2 - 34, -H / 2 + 28, 'X', { width: 46, height: 40, fontSize: 20, color: C.danger, onClick: () => this.closePanel() }));
    if (pages > 1) {
      p.add(new Button(this, -W / 2 + 40, -H / 2 + 28, '<', { width: 46, height: 40, fontSize: 20, color: C.sky, onClick: () => this.openRegionPicker((pg + pages - 1) % pages) }));
      p.add(new Button(this, -W / 2 + 96, -H / 2 + 28, '>', { width: 46, height: 40, fontSize: 20, color: C.sky, onClick: () => this.openRegionPicker((pg + 1) % pages) }));
      p.add(this.add.text(-W / 2 + 140, -H / 2 + 28, `${pg + 1}/${pages}`, textStyle(18, TEXT.dim)).setOrigin(0, 0.5).setName('pickerPage'));
    }
    shown.forEach((r, k) => {
      const i = first + k;
      const x = -W / 2 + 13 + cw / 2 + (k % cols) * (cw + 14);
      const y = -H / 2 + 62 + ch / 2 + Math.floor(k / cols) * (ch + 10);
      const open = r.first < LEVELS.length && isLevelUnlocked(r.first, save.stars);
      const ids = LEVELS.slice(r.first, r.first + r.count).map((l) => l.id);
      const stars = ids.reduce((n, id) => n + (save.stars[id] ?? 0), 0);
      const card = this.add.container(x, y);
      const g = this.add.graphics();
      g.fillStyle(i === this.region ? 0x3f6a3a : open ? C.panelLight : 0x333b35, 1);
      g.fillRoundedRect(-cw / 2, -ch / 2, cw, ch, 12);
      if (i === this.region) {
        g.lineStyle(3, C.gold, 1);
        g.strokeRoundedRect(-cw / 2, -ch / 2, cw, ch, 12);
      }
      card.add(g);
      const name = this.add.text(-cw / 2 + 14, -14, r.name.replace(/^The /, ''), textStyle(18, open ? TEXT.cream : TEXT.dim)).setOrigin(0, 0.5);
      if (name.width > cw - 28) name.setScale((cw - 28) / name.width);
      card.add(name);
      card.add(this.add.text(-cw / 2 + 14, 14, open ? `${stars} / ${ids.length * 3} stars` : 'Locked', textStyle(pf(14), open ? TEXT.gold : TEXT.dim, false)).setOrigin(0, 0.5));
      card.setSize(cw, ch).setInteractive({ useHandCursor: open });
      card.on('pointerdown', (_p: Phaser.Input.Pointer, _x: number, _y: number, ev: Phaser.Types.Input.EventData) => {
        ev.stopPropagation();
        if (!open) {
          this.toast(r.first < LEVELS.length ? `Beat ${LEVELS[r.first - 1].name} to reach ${r.name}` : `${r.name} is coming soon`);
          return;
        }
        sfx.click();
        this.scene.restart({ region: i });
      });
      p.add(card);
    });
    this.panel = p;
  }

  private closePanel(): void {
    this.panel?.destroy();
    this.panel = null;
  }

  private openPanel(i: number): void {
    this.closePanel();
    const lvl = LEVELS[i];
    const save = loadSave();
    const best = save.stars[lvl.id] ?? 0;
    const W = 520;
    const H = 330;
    const p = this.add.container(GAME_W / 2, GAME_H / 2 + 20).setDepth(200);
    const bg = this.add.graphics();
    bg.fillStyle(C.ink, 0.95);
    bg.fillRoundedRect(-W / 2 - 4, -H / 2 - 4, W + 8, H + 8, 26);
    bg.fillStyle(C.panel, 1);
    bg.fillRoundedRect(-W / 2, -H / 2, W, H, 22);
    p.add(bg);
    // swallow clicks on the panel itself
    const blocker = this.add.zone(0, 0, W, H).setInteractive();
    blocker.on('pointerdown', (_p: Phaser.Input.Pointer, _x: number, _y: number, ev: Phaser.Types.Input.EventData) => ev.stopPropagation());
    p.add(blocker);
    p.add(this.add.text(0, -H / 2 + 34, `${i + 1}. ${lvl.name}`, textStyle(30, TEXT.gold)).setOrigin(0.5));
    p.add(
      this.add
        .text(0, -H / 2 + 86, lvl.blurb, { ...textStyle(16, TEXT.cream, false), align: 'center', wordWrap: { width: W - 60 } })
        .setOrigin(0.5),
    );
    // Bosses first, then everyone else in order of appearance; long rosters show 13 faces and a "+N" count.
    const roster = [...new Set(lvl.waves.flatMap((w) => w.groups.map((g) => g.enemy)))].sort((x, y) => Number(!!ENEMIES[y].boss) - Number(!!ENEMIES[x].boss));
    const MAX_FACES = 13;
    const enemyIds = roster.length > MAX_FACES + 1 ? roster.slice(0, MAX_FACES) : roster;
    const extra = roster.length - enemyIds.length;
    p.add(
      this.add
        .text(0, -14, `${lvl.waves.length} waves • ${lvl.paths.length} ${lvl.paths.length > 1 ? 'roads' : 'road'} • ${lvl.lives} lives`, textStyle(16, TEXT.dim, false))
        .setOrigin(0.5),
    );
    const slots = enemyIds.length + (extra > 0 ? 1 : 0);
    const spacing = Math.min(44, (W - 60) / Math.max(1, slots));
    const left = -((slots - 1) * spacing) / 2;
    if (extra > 0) p.add(this.add.text(left + enemyIds.length * spacing, 36, `+${extra}`, textStyle(pf(16), TEXT.dim)).setOrigin(0.5).setName('moreFaces'));
    enemyIds.forEach((id, k) => {
      const img = this.add.image(left + k * spacing, 36, `enemy_${id}`);
      img.setScale(Math.min(1, 34 / Math.max(img.width, img.height)) * (ENEMIES[id].boss ? 1.25 : 1));
      p.add(img);
    });
    for (let s = 0; s < 3; s++) p.add(this.add.image(-W / 2 + 50 + s * 34, H / 2 - 44, s < best ? 'star' : 'star_empty').setScale(0.6));
    const play = new Button(this, W / 2 - 110, H / 2 - 44, best > 0 ? 'Replay' : 'Play!', {
      width: 170,
      height: 58,
      fontSize: 26,
      color: 0xff9f43,
      onClick: () => this.scene.start('Battle', { levelIndex: i }),
    });
    p.add(play);
    if (best > 0) {
      // Endless mode unlocks once the level is beaten.
      const top = save.endlessBest[lvl.id] ?? 0;
      p.add(
        new Button(this, -30, H / 2 - 44, 'Endless', {
          width: 140,
          height: 50,
          fontSize: 20,
          color: 0xb07ae8,
          onClick: () => this.scene.start('Battle', { levelIndex: i, endless: true }),
        }).setName('endlessBtn'),
      );
      const mut = endlessMutatorFor(todayString());
      const boss = ENEMIES[endlessBosses(lvl)[0]]?.name.split(',')[0] ?? '';
      const info = `${top > 0 ? `Best ${top} • ` : ''}Today: ${mut.name}${boss ? ` • Wave 10: ${boss}` : ''}`;
      p.add(fitWidth(this.add.text(-30, H / 2 - 82, info, textStyle(13, TEXT.dim, false)).setOrigin(0.5).setName('endlessInfo'), 340));
    }
    p.setScale(0.6).setAlpha(0);
    this.tweens.add({ targets: p, scale: 1, alpha: 1, duration: 220, ease: 'Back.easeOut' });
    this.panel = p;
  }
}
