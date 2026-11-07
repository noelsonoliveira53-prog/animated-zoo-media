import Phaser from 'phaser';
import { pf } from '../ui/touch';
import { music } from '../systems/music';
import { themeById } from '../data/musicThemes';
import { LEVELS, REGIONS, isLevelUnlocked, regionOf, totalStars } from '../data/levels';
import { ENEMIES } from '../data/enemies';
import { loadSave } from '../systems/save';
import { sfx } from '../systems/audio';
import { Button } from '../ui/Button';
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

    this.drawLand(reg.dusk ? 'dusk' : reg.snow ? 'snow' : reg.ember ? 'ember' : 'meadow');
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
    this.add.text(GAME_W / 2 - 50, 38, reg.name, textStyle(26, TEXT.gold)).setOrigin(0.5).setDepth(101);
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

  private drawLand(style: 'meadow' | 'snow' | 'ember' | 'dusk'): void {
    const snow = style === 'snow';
    const ember = style === 'ember';
    const dusk = style === 'dusk';
    const g = this.add.graphics();
    g.fillStyle(dusk ? 0x1e2340 : ember ? 0x2a1a18 : snow ? 0x2a4f6a : 0x2f6e8f, 1); // sea (or ash wastes, or night mist)
    g.fillRect(-20, -20, GAME_W + 40, GAME_H + 40);
    // main island
    g.fillStyle(dusk ? 0x5a4a6a : ember ? 0x3a2a24 : snow ? 0xb8c4cc : 0xd9c79a, 1);
    g.fillEllipse(GAME_W / 2, GAME_H / 2 + 20, GAME_W * 1.02, GAME_H * 0.98);
    g.fillStyle(dusk ? 0x4a5a78 : ember ? 0x5a4a44 : snow ? 0xe6eef2 : 0x6aae52, 1);
    g.fillEllipse(GAME_W / 2, GAME_H / 2 + 20, GAME_W * 0.98, GAME_H * 0.92);
    // regions
    const regions: [number, number, number, number, number][] = dusk
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
    g.fillStyle(dusk ? 0x7ad8c8 : ember ? 0xff6a2a : snow ? 0xbfe3f2 : 0x5fb8d8, 1);
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
    g.fillStyle(dusk ? 0x8a5ab8 : ember ? 0x8a3a2a : snow ? 0xffffff : 0x4b8f3a, 1);
    g.fillTriangle(50, 604, 130, 604, 90, 570);
    this.add.text(90, 692, dusk ? 'Ember Gate' : ember ? 'Ash Road' : snow ? 'Mountain Gate' : 'Sanctuary', textStyle(pf(14))).setOrigin(0.5);
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
    const enemyIds = [...new Set(lvl.waves.flatMap((w) => w.groups.map((g) => g.enemy)))];
    p.add(
      this.add
        .text(0, -14, `${lvl.waves.length} waves • ${lvl.paths.length} ${lvl.paths.length > 1 ? 'roads' : 'road'} • ${lvl.lives} lives`, textStyle(16, TEXT.dim, false))
        .setOrigin(0.5),
    );
    const spacing = Math.min(44, (W - 60) / Math.max(1, enemyIds.length));
    enemyIds.forEach((id, k) => {
      const img = this.add.image(-((enemyIds.length - 1) * spacing) / 2 + k * spacing, 36, `enemy_${id}`);
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
      if (top > 0) p.add(this.add.text(-30, H / 2 - 82, `Best: ${top} waves`, textStyle(14, TEXT.dim, false)).setOrigin(0.5));
    }
    p.setScale(0.6).setAlpha(0);
    this.tweens.add({ targets: p, scale: 1, alpha: 1, duration: 220, ease: 'Back.easeOut' });
    this.panel = p;
  }
}
