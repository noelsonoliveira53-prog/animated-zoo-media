import Phaser from 'phaser';
import { LEVELS, isLevelUnlocked, totalStars } from '../data/levels';
import { ENEMIES } from '../data/enemies';
import { loadSave } from '../systems/save';
import { sfx } from '../systems/audio';
import { Button } from '../ui/Button';
import { C, GAME_H, GAME_W, TEXT, textStyle } from '../ui/theme';

// Campaign overview: the Grove's lands from the Mossgate (bottom-left) to Murkmaw's Den (top-right).
export class WorldMapScene extends Phaser.Scene {
  private panel: Phaser.GameObjects.Container | null = null;

  constructor() {
    super('WorldMap');
  }

  create(data: { focus?: number }): void {
    this.panel = null;
    const save = loadSave();
    this.drawLand();
    this.drawTrail(save.stars);

    LEVELS.forEach((lvl, i) => this.makeNode(i, isLevelUnlocked(i, save.stars), save.stars[lvl.id] ?? 0));

    // Top bar
    const bar = this.add.graphics().setDepth(100);
    bar.fillStyle(C.ink, 0.75);
    bar.fillRoundedRect(GAME_W / 2 - 220, 10, 440, 56, 18);
    this.add.text(GAME_W / 2 - 40, 38, 'The Grovelands', textStyle(28, TEXT.gold)).setOrigin(0.5).setDepth(101);
    this.add.image(GAME_W / 2 + 110, 38, 'star').setScale(0.55).setDepth(101);
    this.add.text(GAME_W / 2 + 132, 38, `${totalStars(save.stars)}/${LEVELS.length * 3}`, textStyle(24)).setOrigin(0, 0.5).setDepth(101);
    new Button(this, 90, 40, 'Back', { width: 140, height: 50, fontSize: 22, color: C.sky, onClick: () => this.scene.start('Menu') }).setDepth(101);

    this.input.on('pointerdown', () => this.closePanel());
    this.cameras.main.fadeIn(250, 16, 38, 27);

    // Open the info card for the focused level (e.g. the next level after a win).
    const focus = data?.focus;
    if (focus !== undefined && focus >= 0 && focus < LEVELS.length && isLevelUnlocked(focus, save.stars)) {
      this.time.delayedCall(250, () => this.openPanel(focus));
    }
  }

  private drawLand(): void {
    const g = this.add.graphics();
    g.fillStyle(0x2f6e8f, 1); // sea
    g.fillRect(-20, -20, GAME_W + 40, GAME_H + 40);
    // main island
    g.fillStyle(0xd9c79a, 1);
    g.fillEllipse(GAME_W / 2, GAME_H / 2 + 20, GAME_W * 1.02, GAME_H * 0.98);
    g.fillStyle(0x6aae52, 1);
    g.fillEllipse(GAME_W / 2, GAME_H / 2 + 20, GAME_W * 0.98, GAME_H * 0.92);
    // regions
    const regions: [number, number, number, number, number][] = [
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
    // lake
    g.fillStyle(0x5fb8d8, 1);
    g.fillEllipse(900, 520, 200, 90);
    g.fillStyle(0xffffff, 0.4);
    g.fillEllipse(870, 505, 60, 14);
    // trees / reeds decoration (deterministic)
    const rnd = new Phaser.Math.RandomDataGenerator(['grovelands']);
    for (let i = 0; i < 90; i++) {
      const x = rnd.between(80, GAME_W - 80);
      const y = rnd.between(110, GAME_H - 60);
      if (LEVELS.some((l) => Math.hypot(l.mapPos.x - x, l.mapPos.y - y) < 70)) continue;
      if (Math.hypot((x - 900) / 110, (y - 520) / 55) < 1) continue;
      const dark = x > 960 && y < 380;
      g.fillStyle(dark ? 0x24412a : 0x2f6a30, 1);
      g.fillCircle(x, y, rnd.between(8, 14));
      g.fillStyle(dark ? 0x2f5236 : 0x3f8a3a, 1);
      g.fillCircle(x - 3, y - 3, rnd.between(4, 7));
    }
    // the sanctuary at the start
    g.fillStyle(0x9a6a40, 1);
    g.fillRect(60, 600, 60, 40);
    g.fillStyle(0x4b8f3a, 1);
    g.fillTriangle(50, 604, 130, 604, 90, 570);
    this.add.text(90, 660, 'Sanctuary', textStyle(14)).setOrigin(0.5);
  }

  private drawTrail(stars: Record<string, number>): void {
    const g = this.add.graphics();
    const pts = [{ x: 90, y: 600 }, ...LEVELS.map((l) => l.mapPos)];
    for (let i = 1; i < pts.length; i++) {
      const a = pts[i - 1];
      const b = pts[i];
      const open = i === 1 || isLevelUnlocked(i - 1, stars);
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
    p.setScale(0.6).setAlpha(0);
    this.tweens.add({ targets: p, scale: 1, alpha: 1, duration: 220, ease: 'Back.easeOut' });
    this.panel = p;
  }
}
