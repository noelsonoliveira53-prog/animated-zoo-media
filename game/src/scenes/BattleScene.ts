import Phaser from 'phaser';
import { LEVELS } from '../data/levels';
import { TOWERS, TOWER_ORDER, sellValue } from '../data/towers';
import type { LevelDef, TargetMode, Vec2 } from '../data/types';
import { BattleSim, type Enemy, type SimEvent, type Soldier } from '../systems/BattleSim';
import { sfx } from '../systems/audio';
import { loadSave, recordStars, starsForLives, writeSave } from '../systems/save';
import { Button } from '../ui/Button';
import { C, GAME_H, GAME_W, TEXT, textStyle } from '../ui/theme';

interface EnemyView {
  sprite: Phaser.GameObjects.Image;
  bar: Phaser.GameObjects.Graphics;
  bob: number;
  shadow: Phaser.GameObjects.Ellipse | null;
}

const TARGET_MODES: TargetMode[] = ['first', 'last', 'strongest', 'closest'];

export class BattleScene extends Phaser.Scene {
  private sim!: BattleSim;
  private level!: LevelDef;
  private levelIndex = 0;
  private speed = 1;
  private paused = false;

  private enemyViews = new Map<number, EnemyView>();
  private projViews = new Map<number, Phaser.GameObjects.Image>();
  private soldierViews = new Map<number, { sprite: Phaser.GameObjects.Image; bar: Phaser.GameObjects.Graphics }>();
  private rallyFlags = new Map<number, Phaser.GameObjects.Image>();
  private rallyMode: number | null = null; // slot whose rally point is being placed
  private towerViews: (Phaser.GameObjects.Image | null)[] = [];
  private slotViews: Phaser.GameObjects.Image[] = [];

  private coinText!: Phaser.GameObjects.Text;
  private livesText!: Phaser.GameObjects.Text;
  private waveText!: Phaser.GameObjects.Text;
  private nextWaveBtn!: Button;
  private speedBtn!: Button;
  private pauseBtn!: Button;

  private menu: Phaser.GameObjects.Container | null = null;
  private rangeRing!: Phaser.GameObjects.Graphics;
  private particles!: Phaser.GameObjects.Particles.ParticleEmitter;
  private ended = false;
  private bossBar!: Phaser.GameObjects.Graphics;
  private bossLabel!: Phaser.GameObjects.Text;

  constructor() {
    super('Battle');
  }

  init(data: { levelIndex?: number }): void {
    this.levelIndex = data.levelIndex ?? 0;
    this.level = LEVELS[this.levelIndex];
    this.sim = new BattleSim(this.level);
    this.speed = 1;
    this.paused = false;
    this.ended = false;
    this.enemyViews.clear();
    this.projViews.clear();
    this.soldierViews.clear();
    this.rallyFlags.clear();
    this.rallyMode = null;
    this.towerViews = this.level.slots.map(() => null);
    this.slotViews = [];
    this.menu = null;
  }

  create(): void {
    this.drawMap();
    this.rangeRing = this.add.graphics().setDepth(5);

    this.level.slots.forEach((s, i) => {
      const img = this.add.image(s.x, s.y, 'slot').setDepth(s.y).setInteractive({ useHandCursor: true });
      img.on('pointerdown', (_p: Phaser.Input.Pointer, _x: number, _y: number, ev: Phaser.Types.Input.EventData) => {
        ev.stopPropagation();
        sfx.unlock();
        this.openSlotMenu(i);
      });
      this.slotViews.push(img);
    });

    this.particles = this.add.particles(0, 0, 'dot', {
      speed: { min: 60, max: 200 },
      scale: { start: 0.6, end: 0 },
      lifespan: 500,
      gravityY: 300,
      emitting: false,
    });
    this.particles.setDepth(2000);

    this.buildHud();

    this.input.on('pointerdown', (p: Phaser.Input.Pointer) => {
      if (this.rallyMode !== null) {
        this.placeRally(this.rallyMode, { x: p.worldX, y: p.worldY });
        return;
      }
      this.closeMenu();
    });
    this.input.keyboard?.on('keydown-SPACE', () => this.togglePause());
    this.input.keyboard?.on('keydown-N', () => this.callWave());

    this.cameras.main.fadeIn(300, 16, 38, 27);
    this.showBanner(this.level.name, 'Build outposts on the stone pads, then call the first wave!');
  }

  // ---------- map ----------

  private drawMap(): void {
    const { theme } = this.level;
    const g = this.add.graphics().setDepth(-10);
    g.fillStyle(theme.grass, 1);
    g.fillRect(-60, -60, GAME_W + 120, GAME_H + 120); // oversized so screen shake never shows edges
    // deterministic grass patches + tufts
    const rnd = new Phaser.Math.RandomDataGenerator([this.level.id]);
    for (let i = 0; i < 40; i++) {
      g.fillStyle(theme.grassDark, 0.5);
      g.fillEllipse(rnd.between(0, GAME_W), rnd.between(0, GAME_H), rnd.between(60, 180), rnd.between(30, 90));
    }
    for (let i = 0; i < 160; i++) {
      const x = rnd.between(0, GAME_W);
      const y = rnd.between(0, GAME_H);
      g.lineStyle(2, theme.grassDark, 0.9);
      g.lineBetween(x, y, x - 3, y - 7);
      g.lineBetween(x, y, x + 3, y - 8);
    }
    // roads: edge then fill, with round joints
    for (const pts of this.level.paths) {
      this.strokePath(g, pts, 64, theme.roadEdge);
      this.strokePath(g, pts, 52, theme.road);
      // pebbles
      for (let i = 0; i < 50; i++) {
        const seg = rnd.between(1, pts.length - 1);
        const t = rnd.frac();
        const a = pts[seg - 1];
        const b = pts[seg];
        const px = a.x + (b.x - a.x) * t + rnd.between(-18, 18);
        const py = a.y + (b.y - a.y) * t + rnd.between(-18, 18);
        g.fillStyle(theme.roadEdge, 0.7);
        g.fillCircle(px, py, rnd.between(2, 4));
      }
    }
    // decorations: trees & flowers away from roads and slots
    const deco = this.add.graphics().setDepth(1);
    for (let i = 0; i < 60; i++) {
      const p = { x: rnd.between(20, GAME_W - 20), y: rnd.between(90, GAME_H - 10) };
      if (this.sim.paths.some((path) => path.distanceTo(p) < 60)) continue;
      if (this.level.slots.some((s) => Math.hypot(s.x - p.x, s.y - p.y) < 60)) continue;
      if (rnd.frac() < 0.45) {
        deco.fillStyle(0x000000, 0.2);
        deco.fillEllipse(p.x, p.y + 4, 40, 14);
        deco.fillStyle(0x6b4a2b, 1);
        deco.fillRect(p.x - 4, p.y - 14, 8, 18);
        const leaf = rnd.pick([0x3f7f34, 0x4b8f3a, 0x377030]);
        deco.fillStyle(leaf, 1);
        deco.fillCircle(p.x, p.y - 26, 18);
        deco.fillCircle(p.x - 12, p.y - 16, 12);
        deco.fillCircle(p.x + 12, p.y - 16, 12);
        deco.lineStyle(2, C.ink, 0.6);
        deco.strokeCircle(p.x, p.y - 26, 18);
      } else {
        const col = rnd.pick([0xffffff, 0xffe066, 0xff8fb1, 0xb5a8ff]);
        deco.fillStyle(col, 1);
        for (let k = 0; k < 4; k++) deco.fillCircle(p.x + rnd.between(-8, 8), p.y + rnd.between(-6, 6), 3);
      }
    }
    // gate marker at path ends
    for (const pts of this.level.paths) {
      const end = pts[pts.length - 2];
      const gate = this.add.graphics().setDepth(end.y);
      const gx = Math.min(GAME_W - 40, end.x + 260);
      gate.fillStyle(0x7a5232, 1);
      gate.fillRect(gx - 40, end.y - 60, 12, 70);
      gate.fillRect(gx + 28, end.y - 60, 12, 70);
      gate.fillStyle(0x9a6a40, 1);
      gate.fillRect(gx - 48, end.y - 70, 96, 16);
      gate.lineStyle(3, C.ink, 1);
      gate.strokeRect(gx - 48, end.y - 70, 96, 16);
      gate.fillStyle(0x4b8f3a, 1);
      gate.fillCircle(gx - 34, end.y - 70, 10);
      gate.fillCircle(gx + 34, end.y - 70, 10);
    }
  }

  private strokePath(g: Phaser.GameObjects.Graphics, pts: Vec2[], width: number, color: number): void {
    g.lineStyle(width, color, 1);
    g.beginPath();
    g.moveTo(pts[0].x, pts[0].y);
    for (let i = 1; i < pts.length; i++) g.lineTo(pts[i].x, pts[i].y);
    g.strokePath();
    g.fillStyle(color, 1);
    for (const p of pts) g.fillCircle(p.x, p.y, width / 2);
  }

  // ---------- HUD ----------

  private buildHud(): void {
    const bar = this.add.graphics().setDepth(3000);
    bar.fillStyle(C.ink, 0.75);
    bar.fillRoundedRect(12, 10, 440, 54, 16);

    this.add.image(40, 37, 'icon_heart').setDepth(3001);
    this.livesText = this.add.text(60, 37, '', textStyle(26, TEXT.heart)).setOrigin(0, 0.5).setDepth(3001);
    this.add.image(150, 37, 'icon_coin').setDepth(3001);
    this.coinText = this.add.text(170, 37, '', textStyle(26, TEXT.gold)).setOrigin(0, 0.5).setDepth(3001);
    this.add.image(290, 36, 'icon_wave').setDepth(3001);
    this.waveText = this.add.text(310, 37, '', textStyle(24)).setOrigin(0, 0.5).setDepth(3001);

    this.nextWaveBtn = new Button(this, GAME_W - 130, 40, 'Call Wave', {
      width: 220,
      height: 52,
      fontSize: 22,
      color: 0xff9f43,
      onClick: () => this.callWave(),
    }).setDepth(3001);
    this.speedBtn = new Button(this, GAME_W - 300, 40, 'x1', {
      width: 80,
      height: 52,
      fontSize: 22,
      color: C.sky,
      onClick: () => this.cycleSpeed(),
    }).setDepth(3001);
    this.pauseBtn = new Button(this, GAME_W - 400, 40, 'II', {
      width: 80,
      height: 52,
      fontSize: 22,
      color: C.sky,
      onClick: () => this.togglePause(),
    }).setDepth(3001);
    this.bossBar = this.add.graphics().setDepth(3001);
    this.bossLabel = this.add.text(GAME_W / 2, 92, '', textStyle(18, TEXT.heart)).setOrigin(0.5).setDepth(3002).setVisible(false);
    this.refreshHud();
  }

  private drawBossBar(): void {
    this.bossBar.clear();
    const boss = this.sim.enemies.find((e) => e.alive && e.def.boss);
    this.bossLabel.setVisible(!!boss);
    if (!boss) return;
    const w = 420;
    const x = GAME_W / 2 - w / 2;
    const y = 104;
    this.bossBar.fillStyle(C.ink, 0.85);
    this.bossBar.fillRoundedRect(x - 6, y - 6, w + 12, 26, 10);
    this.bossBar.fillStyle(0x5a1f24, 1);
    this.bossBar.fillRect(x, y, w, 14);
    this.bossBar.fillStyle(C.danger, 1);
    this.bossBar.fillRect(x, y, w * Math.max(0, boss.hp / boss.maxHp), 14);
    if (boss.shield > 0) {
      this.bossBar.fillStyle(0x9fd8ff, 0.9);
      this.bossBar.fillRect(x, y + 10, w * (boss.shield / Math.max(1, boss.maxShield)), 4);
    }
    // phase ticks
    this.bossBar.fillStyle(C.cream, 0.9);
    for (const ph of boss.def.phases ?? []) this.bossBar.fillRect(x + w * ph.at - 1, y - 2, 3, 18);
    this.bossLabel.setText(boss.def.name);
  }

  private refreshHud(): void {
    this.livesText.setText(String(this.sim.lives));
    this.coinText.setText(String(this.sim.coins));
    this.waveText.setText(`${Math.max(0, this.sim.waveIndex + 1)}/${this.sim.totalWaves}`);
    if (this.sim.wavesRemaining && this.sim.isActive()) {
      const secs = Math.ceil(this.sim.waveCountdown);
      this.nextWaveBtn.label.setText(this.sim.waveIndex < 0 ? `Start! (${secs})` : `Next Wave (${secs})`);
      this.nextWaveBtn.setEnabled(true);
    } else {
      this.nextWaveBtn.label.setText('Final Wave');
      this.nextWaveBtn.setEnabled(false);
    }
  }

  private callWave(): void {
    if (this.ended) return;
    sfx.unlock();
    this.sim.callNextWave();
  }

  private cycleSpeed(): void {
    this.speed = this.speed === 1 ? 2 : this.speed === 2 ? 3 : 1;
    this.speedBtn.label.setText(`x${this.speed}`);
  }

  private togglePause(): void {
    if (this.ended) return;
    this.paused = !this.paused;
    this.pauseBtn.label.setText(this.paused ? '>' : 'II');
    if (this.paused) this.showBanner('Paused', 'Press II again or Space to resume', true);
    else this.children.getByName('banner')?.destroy();
  }

  private showBanner(title: string, sub: string, sticky = false): void {
    this.children.getByName('banner')?.destroy();
    // Sits just under the HUD so it never hides the battlefield centre.
    const c = this.add.container(GAME_W / 2, sticky ? GAME_H / 2 - 40 : 172).setDepth(4000).setName('banner');
    const bg = this.add.graphics();
    bg.fillStyle(C.ink, 0.72);
    bg.fillRoundedRect(-300, -42, 600, 84, 18);
    c.add(bg);
    c.add(this.add.text(0, -12, title, textStyle(32, TEXT.gold)).setOrigin(0.5));
    c.add(this.add.text(0, 22, sub, textStyle(17, TEXT.cream, false)).setOrigin(0.5));
    c.setScale(0.6).setAlpha(0);
    this.tweens.add({ targets: c, scale: 1, alpha: 1, duration: 250, ease: 'Back.easeOut' });
    if (!sticky) {
      this.tweens.add({ targets: c, alpha: 0, delay: 2600, duration: 400, onComplete: () => c.destroy() });
    }
  }

  // ---------- build / upgrade menus ----------

  private closeMenu(): void {
    this.menu?.destroy();
    this.menu = null;
    this.rangeRing.clear();
  }

  private drawRange(pos: Vec2, range: number, color: number): void {
    this.rangeRing.clear();
    this.rangeRing.fillStyle(color, 0.12);
    this.rangeRing.fillCircle(pos.x, pos.y, range);
    this.rangeRing.lineStyle(3, color, 0.7);
    this.rangeRing.strokeCircle(pos.x, pos.y, range);
  }

  private openSlotMenu(slot: number): void {
    this.closeMenu();
    if (!this.sim.isActive()) return;
    const tower = this.sim.towers[slot];
    const pos = this.level.slots[slot];
    const c = this.add.container(pos.x, pos.y).setDepth(3500);
    this.menu = c;

    const ring = this.add.graphics();
    ring.lineStyle(4, C.cream, 0.6);
    ring.strokeCircle(0, 0, 70);
    c.add(ring);

    if (!tower) {
      const offsets = [
        { x: -58, y: -58 },
        { x: 58, y: -58 },
        { x: -58, y: 58 },
        { x: 58, y: 58 },
      ];
      TOWER_ORDER.forEach((id, i) => {
        const def = TOWERS[id];
        const cost = def.tiers[0].cost;
        const o = offsets[i];
        const opt = this.menuOption(o.x, o.y, `tower_${id}_0`, String(cost), this.sim.coins >= cost, () => {
          if (this.sim.build(slot, id)) this.closeMenu();
        });
        opt.on('pointerover', () => this.drawRange(pos, def.tiers[0].range, def.color));
        c.add(opt);
      });
      c.add(this.add.text(0, 0, 'Build', textStyle(18)).setOrigin(0.5));
    } else {
      const stats = tower.def.tiers[tower.tier];
      this.drawRange(pos, stats.range, tower.def.color);
      const upCost = this.sim.upgradeCost(tower);
      if (upCost !== null) {
        c.add(
          this.menuOption(0, -80, `tower_${tower.def.id}_${tower.tier + 1}`, String(upCost), this.sim.coins >= upCost, () => {
            if (this.sim.upgrade(slot)) this.openSlotMenu(slot);
          }),
        );
      } else {
        c.add(this.add.text(0, -80, 'MAX', textStyle(22, TEXT.gold)).setOrigin(0.5));
      }
      const refund = sellValue(tower.def, tower.tier);
      c.add(
        this.textOption(-74, 30, `Sell\n+${refund}`, C.danger, () => {
          this.sim.sell(slot);
          this.closeMenu();
        }),
      );
      if (tower.rally) {
        c.add(
          this.textOption(74, 30, 'Rally\nPoint', C.sky, () => {
            this.closeMenu();
            this.rallyMode = slot;
            this.drawRange(pos, stats.range, tower.def.color);
            this.showBanner('Rally Point', 'Tap the road inside the circle to send your Wardens there');
          }),
        );
      } else {
        c.add(
          this.textOption(74, 30, `Aim:\n${tower.target}`, C.sky, () => {
            const next = TARGET_MODES[(TARGET_MODES.indexOf(tower.target) + 1) % TARGET_MODES.length];
            this.sim.setTargetMode(slot, next);
            this.openSlotMenu(slot);
          }),
        );
      }
      c.add(this.add.text(0, 92, `${tower.def.name} • Lv ${tower.tier + 1}`, textStyle(16)).setOrigin(0.5));
    }
    c.setScale(0.5);
    this.tweens.add({ targets: c, scale: 1, duration: 160, ease: 'Back.easeOut' });
  }

  private placeRally(slot: number, p: Vec2): void {
    this.rallyMode = null;
    this.rangeRing.clear();
    this.children.getByName('banner')?.destroy();
    const onRoad = this.sim.paths.some((path) => path.distanceTo(p) < 34);
    if (onRoad && this.sim.setRally(slot, p)) {
      const t = this.sim.towers[slot];
      if (t) this.updateRallyFlag(t.uid, p);
      sfx.click();
    } else {
      this.floatText(p.x, p.y, 'Out of reach!', TEXT.heart, 18);
    }
  }

  private updateRallyFlag(towerUid: number, p: Vec2): void {
    this.rallyFlags.get(towerUid)?.destroy();
    const flag = this.add.image(p.x + 6, p.y - 10, 'rally').setDepth(p.y - 1).setAlpha(0.85);
    this.tweens.add({ targets: flag, y: flag.y - 4, yoyo: true, repeat: -1, duration: 700, ease: 'Sine.easeInOut' });
    this.rallyFlags.set(towerUid, flag);
  }

  private menuOption(x: number, y: number, tex: string, cost: string, affordable: boolean, onPick: () => void): Phaser.GameObjects.Container {
    const o = this.add.container(x, y);
    const bg = this.add.graphics();
    bg.fillStyle(C.ink, 0.9);
    bg.fillCircle(0, 0, 38);
    bg.lineStyle(3, affordable ? C.gold : 0x777777, 1);
    bg.strokeCircle(0, 0, 38);
    const icon = this.add.image(0, -4, tex).setScale(0.62);
    const label = this.add.text(0, 30, cost, textStyle(17, affordable ? TEXT.gold : '#999999')).setOrigin(0.5);
    o.add([bg, icon, label]);
    if (!affordable) icon.setTint(0x777777);
    o.setSize(76, 76).setInteractive({ useHandCursor: true });
    o.on('pointerdown', (_p: Phaser.Input.Pointer, _x: number, _y: number, ev: Phaser.Types.Input.EventData) => {
      ev.stopPropagation();
      if (!affordable) {
        this.tweens.add({ targets: o, x: x + 6, duration: 40, yoyo: true, repeat: 2 });
        return;
      }
      onPick();
    });
    return o;
  }

  private textOption(x: number, y: number, text: string, color: number, onPick: () => void): Phaser.GameObjects.Container {
    const o = this.add.container(x, y);
    const bg = this.add.graphics();
    bg.fillStyle(C.ink, 0.9);
    bg.fillCircle(0, 0, 34);
    bg.lineStyle(3, color, 1);
    bg.strokeCircle(0, 0, 34);
    o.add([bg, this.add.text(0, 0, text, { ...textStyle(14), align: 'center' }).setOrigin(0.5)]);
    o.setSize(68, 68).setInteractive({ useHandCursor: true });
    o.on('pointerdown', (_p: Phaser.Input.Pointer, _x: number, _y: number, ev: Phaser.Types.Input.EventData) => {
      ev.stopPropagation();
      sfx.click();
      onPick();
    });
    return o;
  }

  // ---------- frame loop ----------

  update(_time: number, deltaMs: number): void {
    const dt = Math.min(deltaMs / 1000, 0.1);
    if (!this.paused && !this.ended) this.sim.update(dt * this.speed);
    for (const ev of this.sim.drainEvents()) this.handleEvent(ev);
    this.syncViews(dt);
    this.drawBossBar();
    this.refreshHud();
  }

  private handleEvent(ev: SimEvent): void {
    switch (ev.type) {
      case 'spawn':
        this.addEnemyView(ev.enemy);
        if (ev.enemy.def.boss) {
          this.showBanner(`${ev.enemy.def.name} approaches!`, 'Focus everything on the boss');
          this.cameras.main.shake(500, 0.01);
          sfx.waveHorn();
        }
        break;
      case 'shoot': {
        const key = `proj_${ev.tower.def.id}`;
        const img = this.add.image(ev.projectile.pos.x, ev.projectile.pos.y, this.textures.exists(key) ? key : 'dot').setDepth(2500);
        this.projViews.set(ev.projectile.uid, img);
        const tv = this.towerViews[ev.tower.slot];
        if (tv) this.tweens.add({ targets: tv, scaleY: 0.92, duration: 50, yoyo: true });
        sfx.shoot(ev.tower.def.id);
        break;
      }
      case 'hit': {
        const v = this.enemyViews.get(ev.enemy.uid);
        if (v) {
          v.sprite.setTintFill(0xffffff);
          this.time.delayedCall(60, () => v.sprite.active && v.sprite.clearTint());
        }
        this.floatText(ev.pos.x, ev.pos.y - 20, String(Math.round(ev.damage)), '#ffffff', 16);
        sfx.hit();
        break;
      }
      case 'splash': {
        this.particles.setParticleTint(0xb59a72);
        this.particles.explode(14, ev.pos.x, ev.pos.y);
        const ring = this.add.circle(ev.pos.x, ev.pos.y, ev.radius, 0xffffff, 0).setStrokeStyle(4, 0xe8d9b5, 0.9).setDepth(2400).setScale(0.3);
        this.tweens.add({ targets: ring, scale: 1, alpha: 0, duration: 280, onComplete: () => ring.destroy() });
        this.cameras.main.shake(70, 0.002);
        sfx.boom();
        break;
      }
      case 'kill': {
        const v = this.enemyViews.get(ev.enemy.uid);
        if (v) this.killView(ev.enemy.uid, v);
        this.particles.setParticleTint(ev.enemy.def.color);
        this.particles.explode(14, ev.enemy.pos.x, ev.enemy.pos.y);
        this.floatText(ev.enemy.pos.x, ev.enemy.pos.y - 34, `+${ev.bounty}`, TEXT.gold, 18);
        sfx.kill();
        sfx.coin();
        break;
      }
      case 'leak': {
        const v = this.enemyViews.get(ev.enemy.uid);
        if (v) this.killView(ev.enemy.uid, v);
        this.cameras.main.shake(180, 0.006);
        this.cameras.main.flash(120, 120, 0, 0);
        this.tweens.add({ targets: this.livesText, scale: 1.5, duration: 100, yoyo: true });
        sfx.leak();
        break;
      }
      case 'waveStart':
        sfx.waveHorn();
        this.showBanner(`Wave ${ev.index + 1}`, ev.bonus > 0 ? `Early call bonus +${ev.bonus} coins` : 'Here they come!');
        break;
      case 'waveCleared':
        break;
      case 'melee':
        sfx.melee();
        break;
      case 'heal': {
        const ring = this.add.circle(ev.source.pos.x, ev.source.pos.y, ev.radius, 0x6fe08a, 0.12).setStrokeStyle(3, 0x6fe08a, 0.8).setDepth(2400).setScale(0.2);
        this.tweens.add({ targets: ring, scale: 1, alpha: 0, duration: 450, onComplete: () => ring.destroy() });
        for (const t of ev.targets) {
          this.floatText(t.pos.x, t.pos.y - 26, '+', '#7bff9a', 20);
        }
        sfx.heal();
        break;
      }
      case 'shieldBreak': {
        this.particles.setParticleTint(0xd8c27a);
        this.particles.explode(12, ev.enemy.pos.x, ev.enemy.pos.y);
        this.floatText(ev.enemy.pos.x, ev.enemy.pos.y - 40, 'Shield broken!', '#ffe9a8', 16);
        sfx.shieldBreak();
        break;
      }
      case 'phase':
        this.showBanner(ev.enemy.def.name, ev.message);
        this.cameras.main.shake(300, 0.008);
        sfx.waveHorn();
        break;
      case 'split':
        this.particles.setParticleTint(ev.parent.def.color);
        this.particles.explode(20, ev.parent.pos.x, ev.parent.pos.y);
        break;
      case 'soldierDown':
        this.particles.setParticleTint(0x9aa8b5);
        this.particles.explode(8, ev.soldier.pos.x, ev.soldier.pos.y);
        break;
      case 'build':
      case 'upgrade': {
        const t = ev.tower;
        if (t.rally && ev.type === 'build') this.updateRallyFlag(t.uid, t.rally);
        this.towerViews[t.slot]?.destroy();
        const img = this.add.image(t.pos.x, t.pos.y - 26, `tower_${t.def.id}_${t.tier}`).setDepth(t.pos.y + 1);
        img.setScale(0.3, 1.4);
        this.tweens.add({ targets: img, scaleX: 1, scaleY: 1, duration: 300, ease: 'Back.easeOut' });
        this.towerViews[t.slot] = img;
        this.slotViews[t.slot].setAlpha(0.6);
        this.particles.setParticleTint(0xd9c39a);
        this.particles.explode(12, t.pos.x, t.pos.y + 6);
        sfx.build();
        break;
      }
      case 'sell': {
        const v = this.towerViews[ev.tower.slot];
        if (v) this.tweens.add({ targets: v, scale: 0, alpha: 0, duration: 200, onComplete: () => v.destroy() });
        this.towerViews[ev.tower.slot] = null;
        this.slotViews[ev.tower.slot].setAlpha(1);
        this.rallyFlags.get(ev.tower.uid)?.destroy();
        this.rallyFlags.delete(ev.tower.uid);
        this.floatText(ev.tower.pos.x, ev.tower.pos.y - 40, `+${ev.refund}`, TEXT.gold, 20);
        sfx.sell();
        break;
      }
      case 'victory':
        this.endBattle(true);
        break;
      case 'defeat':
        this.endBattle(false);
        break;
    }
  }

  private addEnemyView(e: Enemy): void {
    const sprite = this.add.image(e.pos.x, e.pos.y, `enemy_${e.def.id}`);
    const bar = this.add.graphics();
    const shadow = e.def.flying ? this.add.ellipse(e.pos.x, e.pos.y, e.def.radius * 1.6, e.def.radius * 0.6, 0x000000, 0.22) : null;
    this.enemyViews.set(e.uid, { sprite, bar, bob: Math.random() * Math.PI * 2, shadow });
  }

  private killView(uid: number, v: EnemyView): void {
    this.enemyViews.delete(uid);
    v.bar.destroy();
    v.shadow?.destroy();
    this.tweens.add({ targets: v.sprite, scale: 1.4, alpha: 0, duration: 180, onComplete: () => v.sprite.destroy() });
  }

  private syncViews(dt: number): void {
    for (const e of this.sim.enemies) {
      const v = this.enemyViews.get(e.uid);
      if (!v) continue;
      v.bob += dt * (6 + (e.def.speed * e.speedMult) / 20) * (e.blockedBy ? 0.5 : 1);
      const prevX = v.sprite.x;
      const lift = e.def.flying ? 34 + Math.sin(v.bob * 0.7) * 5 : Math.abs(Math.sin(v.bob)) * 4;
      v.sprite.setPosition(e.pos.x, e.pos.y - lift);
      if (e.def.flying) v.sprite.setScale(1, 1 + Math.sin(v.bob * 3) * 0.08);
      else v.sprite.setScale(1 + Math.sin(v.bob * 2) * 0.04, 1 - Math.sin(v.bob * 2) * 0.04);
      if (e.speedMult > 1) v.sprite.setTint(0xff9a8a);
      v.shadow?.setPosition(e.pos.x, e.pos.y + 4).setDepth(e.pos.y - 1);
      if (Math.abs(e.pos.x - prevX) > 0.01) v.sprite.setFlipX(e.pos.x < prevX);
      v.sprite.setDepth(e.def.flying ? e.pos.y + 1000 : e.pos.y);
      v.bar.clear();
      if (e.def.boss) continue; // boss uses the big HUD bar
      if (e.hp < e.maxHp || e.shield > 0) {
        const w = Math.max(24, e.def.radius * 2.4);
        const x = e.pos.x - w / 2;
        const y = e.pos.y - e.def.radius - 14 - (e.def.flying ? 34 : 0);
        if (e.shield > 0) {
          v.bar.fillStyle(C.ink, 0.85);
          v.bar.fillRect(x - 1, y - 7, w + 2, 6);
          v.bar.fillStyle(0xe8d27a, 1);
          v.bar.fillRect(x, y - 6, w * (e.shield / Math.max(1, e.maxShield)), 4);
        }
        v.bar.fillStyle(C.ink, 0.85);
        v.bar.fillRect(x - 1, y - 1, w + 2, 7);
        v.bar.fillStyle(e.hp / e.maxHp > 0.4 ? 0x7be35a : 0xff5d4a, 1);
        v.bar.fillRect(x, y, w * Math.max(0, e.hp / e.maxHp), 5);
        v.bar.setDepth(e.def.flying ? e.pos.y + 1000.5 : e.pos.y + 0.5);
      }
    }
    this.syncSoldiers();
    const live = new Set(this.sim.projectiles.map((p) => p.uid));
    for (const p of this.sim.projectiles) {
      const img = this.projViews.get(p.uid);
      if (!img) continue;
      if (p.homing) {
        img.setRotation(Math.atan2(p.lastTargetPos.y - img.y, p.lastTargetPos.x - img.x));
        img.setPosition(p.pos.x, p.pos.y);
      } else {
        // Arc: lift by a parabola over the flight progress.
        const left = Math.hypot(p.lastTargetPos.x - p.pos.x, p.lastTargetPos.y - p.pos.y);
        const t = p.travel > 0 ? 1 - left / p.travel : 1;
        const lift = Math.sin(Math.PI * Math.max(0, Math.min(1, t))) * Math.min(120, 40 + p.travel * 0.35);
        img.setPosition(p.pos.x, p.pos.y - lift);
        img.rotation += 0.15;
      }
    }
    for (const [uid, img] of this.projViews) {
      if (!live.has(uid)) {
        img.destroy();
        this.projViews.delete(uid);
      }
    }
  }

  private syncSoldiers(): void {
    const seen = new Set<number>();
    for (const s of this.sim.soldiers) {
      seen.add(s.uid);
      let v = this.soldierViews.get(s.uid);
      if (!v) {
        v = { sprite: this.add.image(s.pos.x, s.pos.y, 'soldier'), bar: this.add.graphics() };
        this.soldierViews.set(s.uid, v);
      }
      this.drawSoldier(s, v.sprite, v.bar);
    }
    for (const [uid, v] of this.soldierViews) {
      if (!seen.has(uid)) {
        v.sprite.destroy();
        v.bar.destroy();
        this.soldierViews.delete(uid);
      }
    }
  }

  private drawSoldier(s: Soldier, sprite: Phaser.GameObjects.Image, bar: Phaser.GameObjects.Graphics): void {
    sprite.setVisible(s.alive);
    bar.clear();
    if (!s.alive) return;
    const fighting = s.targetUid !== 0;
    const jiggle = fighting ? Math.sin(this.time.now / 60 + s.uid) * 2 : 0;
    if (Math.abs(sprite.x - s.pos.x) > 0.3) sprite.setFlipX(s.pos.x < sprite.x);
    sprite.setPosition(s.pos.x + jiggle, s.pos.y - 10).setDepth(s.pos.y);
    if (s.hp < s.maxHp) {
      const w = 22;
      bar.fillStyle(C.ink, 0.85);
      bar.fillRect(s.pos.x - w / 2 - 1, s.pos.y - 34, w + 2, 6);
      bar.fillStyle(0x7fc8ff, 1);
      bar.fillRect(s.pos.x - w / 2, s.pos.y - 33, w * (s.hp / s.maxHp), 4);
      bar.setDepth(s.pos.y + 0.5);
    }
  }

  private floatText(x: number, y: number, text: string, color: string, size: number): void {
    const t = this.add.text(x, y, text, textStyle(size, color)).setOrigin(0.5).setDepth(2600);
    this.tweens.add({ targets: t, y: y - 30, alpha: 0, duration: 700, ease: 'Cubic.easeOut', onComplete: () => t.destroy() });
  }

  // ---------- end of battle ----------

  private endBattle(won: boolean): void {
    if (this.ended) return;
    this.ended = true;
    this.closeMenu();
    const stars = won ? starsForLives(this.sim.lives, this.level.lives) : 0;
    if (won) {
      writeSave(recordStars(loadSave(), this.level.id, stars));
      sfx.victory();
    } else {
      sfx.defeat();
    }

    const shade = this.add.rectangle(GAME_W / 2, GAME_H / 2, GAME_W, GAME_H, 0x000000, 0).setDepth(5000).setInteractive();
    this.tweens.add({ targets: shade, fillAlpha: 0.55, duration: 300 });
    const panel = this.add.container(GAME_W / 2, GAME_H / 2).setDepth(5001);
    const bg = this.add.graphics();
    bg.fillStyle(C.ink, 1);
    bg.fillRoundedRect(-280, -200, 560, 400, 28);
    bg.fillStyle(C.panel, 1);
    bg.fillRoundedRect(-270, -190, 540, 380, 22);
    panel.add(bg);
    panel.add(this.add.text(0, -140, won ? 'Victory!' : 'The Gate Fell', textStyle(54, won ? TEXT.gold : TEXT.heart)).setOrigin(0.5));
    for (let i = 0; i < 3; i++) {
      const star = this.add.image(-90 + i * 90, -40, i < stars ? 'star' : 'star_empty').setScale(0);
      panel.add(star);
      this.tweens.add({ targets: star, scale: 1.4, delay: 400 + i * 250, duration: 300, ease: 'Back.easeOut' });
    }
    panel.add(
      this.add
        .text(0, 40, won ? `Lives kept: ${this.sim.lives}/${this.level.lives}` : `You held until wave ${this.sim.waveIndex + 1}`, textStyle(22))
        .setOrigin(0.5),
    );
    const retry = new Button(this, -120, 120, 'Retry', {
      width: 200,
      color: 0xff9f43,
      onClick: () => this.scene.restart({ levelIndex: this.levelIndex }),
    });
    const menu = new Button(this, 120, 120, 'Menu', { width: 200, onClick: () => this.scene.start('Menu') });
    panel.add([retry, menu]);
    panel.setScale(0.5).setAlpha(0);
    this.tweens.add({ targets: panel, scale: 1, alpha: 1, duration: 350, ease: 'Back.easeOut' });
  }
}
