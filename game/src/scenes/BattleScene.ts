import Phaser from 'phaser';
import { music } from '../systems/music';
import { themeForRegion } from '../data/musicThemes';
import { STORY } from '../data/story';
import { ENDLESS } from '../data/endless';
import { endlessMutatorFor, makeEndlessLevel, mutatorReward, wavesHeld } from '../systems/endless';
import { LEVELS } from '../data/levels';
import { ENEMIES } from '../data/enemies';
import { combine, DAILY_MODIFIERS } from '../data/daily';
import { dailyFor, todayString, type DailyChallenge } from '../systems/daily';
import { isLevelUnlocked, regionOf } from '../data/levels';
import { TOWERS, TOWER_ORDER, sellValue } from '../data/towers';
import { HERO_MAX_LEVEL, HERO_XP } from '../data/heroes';
import { SPELLS, SPELL_ORDER } from '../data/spells';
import type { LevelDef, TargetMode, Vec2 } from '../data/types';
import { BattleSim, type Enemy, type SimEvent, type Soldier } from '../systems/BattleSim';
import { sfx } from '../systems/audio';
import { bumpStats, ensureVillage, loadSave, markSeen, recordStars, starsForLives, writeSave } from '../systems/save';
import { checkAchievements } from '../systems/achievements';
import { showAchievementToasts } from '../ui/toast';
import { addResources, battlePerks, battleReward, grantSwiftbloom, type BattlePerks } from '../systems/village';
import { Button } from '../ui/Button';
import { C, GAME_H, GAME_W, TEXT, textStyle } from '../ui/theme';
import { fitWidth, padHit, pf } from '../ui/touch';

interface EnemyView {
  sprite: Phaser.GameObjects.Image;
  bar: Phaser.GameObjects.Graphics;
  bob: number;
  shadow: Phaser.GameObjects.Ellipse | null;
  mound: Phaser.GameObjects.Image | null;
  air: number; // 0 = on the ground, 1 = flying height (eases for swooping flyers)
}

const TARGET_MODES: TargetMode[] = ['first', 'last', 'strongest', 'closest'];

export class BattleScene extends Phaser.Scene {
  private sim!: BattleSim;
  private level!: LevelDef;
  private levelIndex = 0;
  private speed = 1;
  private paused = false;

  private enemyViews = new Map<number, EnemyView>();
  private lastGulp = new Map<number, number>(); // throttle clock: uid -> last "Gulp!" text; -uid -> last Copperhorn arc
  private projViews = new Map<number, Phaser.GameObjects.Image>();
  private soldierViews = new Map<number, { sprite: Phaser.GameObjects.Image; bar: Phaser.GameObjects.Graphics }>();
  private rallyFlags = new Map<number, Phaser.GameObjects.Image>();
  private pendingSpec: string | null = null; // "slot:index" awaiting a confirming tap
  private rallyMode: number | null = null; // slot whose rally point is being placed
  private spellMode: string | null = null; // spell waiting for a target tap
  private spellHud!: Phaser.GameObjects.Graphics;
  private strikeViews = new Map<number, { star: Phaser.GameObjects.Image; mark: Phaser.GameObjects.Arc }>();
  private reticle!: Phaser.GameObjects.Arc;
  private towerViews: (Phaser.GameObjects.Image | null)[] = [];
  private slotViews: Phaser.GameObjects.Image[] = [];

  private coinText!: Phaser.GameObjects.Text;
  private livesText!: Phaser.GameObjects.Text;
  private waveText!: Phaser.GameObjects.Text;
  private nextWaveBtn!: Button;
  private speedBtn!: Button;
  private pauseBtn!: Button;

  private menu: Phaser.GameObjects.Container | null = null;
  private jamG: Phaser.GameObjects.Graphics | null = null;
  private rangeRing!: Phaser.GameObjects.Graphics;
  private particles!: Phaser.GameObjects.Particles.ParticleEmitter;
  private ended = false;
  private heroSprite: Phaser.GameObjects.Image | null = null;
  private heroBar!: Phaser.GameObjects.Graphics;
  private heroRing!: Phaser.GameObjects.Ellipse;
  private heroSelected = false;
  private heroHud!: Phaser.GameObjects.Graphics;
  private heroLevelText!: Phaser.GameObjects.Text;
  private skillText!: Phaser.GameObjects.Text;
  private bossBar!: Phaser.GameObjects.Graphics;
  private perks: BattlePerks = { towerDamageMult: 1, bonusCoins: 0, rangerMult: 1 };
  private seen = new Set<string>();
  private tally = { kills: 0, specs: 0, bosses: [] as string[] };
  private bossLabel!: Phaser.GameObjects.Text;

  constructor() {
    super('Battle');
  }

  private daily: DailyChallenge | null = null;
  private endless = false;
  private mutator: import('../data/daily').ModifierDef | null = null;
  private endlessResult: { held: number; best: number; isBest: boolean } | null = null;

  init(data: { levelIndex?: number; daily?: boolean; endless?: boolean }): void {
    this.levelIndex = data.levelIndex ?? 0;
    this.daily = null;
    this.endless = !!data.endless && !data.daily;
    this.endlessResult = null;
    if (data.daily) {
      const st = loadSave().stars;
      const unlocked = LEVELS.filter((_, i) => isLevelUnlocked(i, st)).length;
      this.daily = dailyFor(todayString(), unlocked);
      this.levelIndex = this.daily.levelIndex;
    }
    this.level = this.endless ? makeEndlessLevel(LEVELS[this.levelIndex]) : LEVELS[this.levelIndex];
    this.mutator = this.endless ? endlessMutatorFor(todayString()) : null;
    const save = loadSave();
    this.perks = battlePerks(save.village);
    this.sim = new BattleSim(this.level, save.hero, {
      ...this.perks,
      heroLevel: 1 + (save.heroRanks[save.hero] ?? 0),
      mods: this.daily ? combine(this.daily.modifiers) : this.mutator ? combine([this.mutator.id]) : undefined,
    });
    this.heroSprite = null;
    this.heroSelected = false;
    this.seen = new Set();
    this.tally = { kills: 0, specs: 0, bosses: [] };
    this.speed = 1;
    this.paused = false;
    this.ended = false;
    this.enemyViews.clear();
    this.lastGulp.clear();
    this.projViews.clear();
    this.soldierViews.clear();
    this.rallyFlags.clear();
    this.rallyMode = null;
    this.spellMode = null;
    this.strikeViews.clear();
    this.towerViews = this.level.slots.map(() => null);
    this.slotViews = [];
    this.menu = null;
    this.jamG = null;
  }

  create(): void {
    music.setMood('battle');
    music.setTheme(themeForRegion(regionOf(this.levelIndex)));
    this.drawMap();
    this.rangeRing = this.add.graphics().setDepth(5);

    this.level.slots.forEach((s, i) => {
      const img = padHit(this.add.image(s.x, s.y, 'slot').setDepth(s.y).setInteractive({ useHandCursor: true }));
      img.on('pointerdown', (_p: Phaser.Input.Pointer, _x: number, _y: number, ev: Phaser.Types.Input.EventData) => {
        ev.stopPropagation();
        sfx.unlock();
        if (this.spellMode) {
          this.castAt(this.spellMode, { x: _p.worldX, y: _p.worldY });
          return;
        }
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

    if (this.level.theme.lava) {
      // drifting embers
      this.add.particles(0, 0, 'dot', {
        x: { min: 0, max: GAME_W },
        y: GAME_H + 10,
        speedY: { min: -60, max: -25 },
        speedX: { min: -15, max: 15 },
        scale: { min: 0.12, max: 0.3 },
        alpha: { start: 0.9, end: 0 },
        tint: [0xff8a3c, 0xffc93c, 0xff5d4a],
        lifespan: 9000,
        frequency: 160,
      }).setDepth(2200);
    }
    if (this.level.theme.snow) {
      this.add.particles(0, 0, 'dot', {
        x: { min: -20, max: GAME_W + 20 },
        y: -10,
        speedY: { min: 30, max: 70 },
        speedX: { min: -20, max: 10 },
        scale: { min: 0.15, max: 0.4 },
        alpha: { start: 0.9, end: 0.4 },
        lifespan: 12000,
        frequency: 120,
      }).setDepth(2200);
    }
    this.buildHud();
    this.buildHero();
    this.buildSpells();
    this.refreshWavePreview();

    this.input.on('pointerdown', (p: Phaser.Input.Pointer) => {
      if (this.rallyMode !== null) {
        this.placeRally(this.rallyMode, { x: p.worldX, y: p.worldY });
        return;
      }
      if (this.spellMode !== null) {
        this.castAt(this.spellMode, { x: p.worldX, y: p.worldY });
        return;
      }
      if (this.heroSelected && !this.menu) {
        this.orderHeroMove({ x: p.worldX, y: p.worldY });
        return;
      }
      this.closeMenu();
    });
    this.input.keyboard?.on('keydown-SPACE', () => this.togglePause());
    this.input.keyboard?.on('keydown-N', () => this.callWave());
    this.input.keyboard?.on('keydown-H', () => this.selectHero(!this.heroSelected));
    this.input.keyboard?.on('keydown-Q', () => this.sim.useHeroSkill());
    this.input.keyboard?.on('keydown-ONE', () => this.armSpell(SPELL_ORDER[0]));
    this.input.keyboard?.on('keydown-TWO', () => this.armSpell(SPELL_ORDER[1]));
    this.input.keyboard?.on('keydown-THREE', () => this.armSpell(SPELL_ORDER[2]));
    this.input.keyboard?.on('keydown-ESC', () => (this.spellMode ? this.armSpell(null) : this.togglePause()));
    this.input.on('pointermove', (p: Phaser.Input.Pointer) => {
      if (this.spellMode) this.reticle.setPosition(p.worldX, p.worldY);
    });

    this.cameras.main.fadeIn(300, 16, 38, 27);
    const bonus: string[] = [];
    if (this.perks.bonusCoins) bonus.push(`+${this.perks.bonusCoins} coins`);
    if (this.perks.towerDamageMult > 1) bonus.push(`+${Math.round((this.perks.towerDamageMult - 1) * 100)}% tower damage`);
    if (this.perks.rangerMult > 1) bonus.push(`Rangers +${Math.round((this.perks.rangerMult - 1) * 100)}%`);
    if (this.sim.hero && this.sim.hero.level > 1) bonus.push(`${this.sim.hero.def.name} starts at Lv ${this.sim.hero.level}`);
    if (this.daily) {
      const names = this.daily.modifiers.map((id) => DAILY_MODIFIERS.find((m) => m.id === id)!.name);
      this.showBanner(`Daily: ${this.level.name}`, `Today's twists: ${names.join(' + ')}`);
    } else if (this.mutator) {
      const pay = mutatorReward(this.mutator);
      this.showBanner(`Endless: ${this.level.name}`, `Today's mutator: ${this.mutator.name} (${this.mutator.text})${pay > 1 ? ` • payout ×${pay}` : ''}`);
    } else {
      this.showBanner(this.level.name, bonus.length ? `Village bonuses: ${bonus.join(' • ')}` : 'Build outposts on the stone pads, then call the first wave!');
    }
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
    // ponds
    const lava = !!this.level.theme.lava;
    const abyss = !!this.level.theme.abyss;
    for (const pd of this.level.ponds ?? []) {
      g.fillStyle(lava ? 0x5a2a1a : abyss ? 0x0a0c1a : 0x3f8a9a, 1);
      g.fillEllipse(pd.x, pd.y + 3, pd.w + 10, pd.h + 8);
      g.fillStyle(lava ? 0xff6a2a : abyss ? 0x1a8a8a : 0x6fc4dc, 1);
      g.fillEllipse(pd.x, pd.y, pd.w, pd.h);
      if (lava || abyss) {
        const glow = this.add.ellipse(pd.x, pd.y, pd.w * 0.7, pd.h * 0.6, abyss ? 0x5ae8d0 : 0xffc93c, 0.5).setDepth(-9);
        this.tweens.add({ targets: glow, alpha: 0.15, scale: 0.85, yoyo: true, repeat: -1, duration: 900, ease: 'Sine.easeInOut' });
      }
      g.fillStyle(0xffffff, 0.35);
      g.fillEllipse(pd.x - pd.w * 0.2, pd.y - pd.h * 0.2, pd.w * 0.3, pd.h * 0.2);
      if (this.level.theme.dunes) this.drawOasis(pd);
    }
    if (this.level.theme.reef) {
      // sunlight caustics: a few soft pale blobs drifting slowly across the shallows
      for (let i = 0; i < 9; i++) {
        const blob = this.add.ellipse(rnd.between(0, GAME_W), rnd.between(100, GAME_H), rnd.between(60, 110), rnd.between(18, 30), 0xe8ffff, 0.1).setDepth(0.6);
        this.tweens.add({ targets: blob, x: blob.x + rnd.between(-60, 60), alpha: 0.2, duration: rnd.between(2400, 3600), yoyo: true, repeat: -1, ease: 'Sine.easeInOut' });
      }
    }
    if (this.level.theme.dunes) {
      // heat shimmer: a few pale horizontal bands slowly breathing in and out
      for (let i = 0; i < 4; i++) {
        const band = this.add.rectangle(GAME_W / 2, 140 + i * 150, GAME_W, 26, 0xfff4d8, 0.08).setDepth(0.6);
        this.tweens.add({ targets: band, alpha: 0.18, y: band.y - 8, duration: 1600 + i * 300, yoyo: true, repeat: -1, ease: 'Sine.easeInOut' });
      }
    }
    if (this.level.theme.storm) {
      // light slanting rain over the steppe: a 120px-periodic pattern scrolled down and wrapped
      const rain = this.add.graphics().setDepth(0.6).setAlpha(0.22);
      rain.lineStyle(1.5, 0xdce4f0, 1);
      for (let y = -120; y < GAME_H + 120; y += 30)
        for (let x = (y / 30) % 2 ? 0 : 22; x < GAME_W + 40; x += 44) rain.lineBetween(x, y, x - 7, y + 14);
      this.tweens.add({ targets: rain, y: 120, duration: 900, repeat: -1 });
    }
    if (this.level.theme.gale) {
      // low clouds drifting past the cliffs, west to east, then wrapping round
      for (let i = 0; i < 5; i++) {
        const cloud = this.add.graphics().setDepth(0.5).setAlpha(0.4);
        cloud.fillStyle(0xffffff, 1);
        for (const [dx, dy, r] of [[0, 0, 26], [-26, 6, 18], [26, 6, 20], [10, -12, 18]]) cloud.fillCircle(dx, dy, r);
        cloud.setPosition(rnd.between(0, GAME_W), rnd.between(110, GAME_H - 110));
        const speed = rnd.between(14, 26);
        this.tweens.add({ targets: cloud, x: GAME_W + 80, duration: ((GAME_W + 80 - cloud.x) / speed) * 1000, onComplete: () => {
          cloud.x = -80;
          this.tweens.add({ targets: cloud, x: GAME_W + 80, duration: ((GAME_W + 160) / speed) * 1000, repeat: -1 });
        } });
      }
    }
    // decorations: trees & flowers away from roads and slots
    const deco = this.add.graphics().setDepth(1);
    for (let i = 0; i < 60; i++) {
      const p = { x: rnd.between(20, GAME_W - 20), y: rnd.between(90, GAME_H - 10) };
      if (this.sim.paths.some((path) => path.distanceTo(p) < 60)) continue;
      if (this.level.slots.some((s) => Math.hypot(s.x - p.x, s.y - p.y) < 60)) continue;
      if ((this.level.ponds ?? []).some((pd) => Math.hypot((p.x - pd.x) / (pd.w / 2 + 20), (p.y - pd.y) / (pd.h / 2 + 20)) < 1)) continue;
      if (this.level.theme.crystals && rnd.frac() < 0.5) {
        // glass spires: a cluster of faceted crystals
        const col = rnd.pick(this.level.theme.trees ?? [0x9ad8f0]);
        deco.fillStyle(0x000000, 0.2);
        deco.fillEllipse(p.x, p.y + 4, 34, 10);
        for (const [dx, h, w] of [[-9, 22, 8], [0, 34, 10], [9, 18, 7]]) {
          deco.fillStyle(col, 0.95);
          deco.fillTriangle(p.x + dx - w, p.y + 2, p.x + dx + w, p.y + 2, p.x + dx, p.y - h);
          deco.fillStyle(0xffffff, 0.45);
          deco.fillTriangle(p.x + dx - w * 0.3, p.y, p.x + dx + w * 0.2, p.y, p.x + dx, p.y - h * 0.9);
          deco.lineStyle(1.5, C.ink, 0.5);
          deco.strokeTriangle(p.x + dx - w, p.y + 2, p.x + dx + w, p.y + 2, p.x + dx, p.y - h);
        }
      } else if (this.level.theme.reef) {
        const k = rnd.frac();
        if (k < 0.55) {
          // a branching coral head
          const col = rnd.pick(this.level.theme.trees ?? [0xf07a6a]);
          deco.fillStyle(0x000000, 0.12);
          deco.fillEllipse(p.x, p.y + 4, 30, 9);
          deco.lineStyle(5, col, 1);
          for (const [dx, h] of [[-8, 18], [0, 26], [8, 20], [-14, 10], [14, 12]]) {
            deco.lineBetween(p.x + dx * 0.3, p.y + 2, p.x + dx, p.y - h);
          }
          deco.fillStyle(col, 1);
          for (const [dx, h] of [[-8, 18], [0, 26], [8, 20], [-14, 10], [14, 12]]) deco.fillCircle(p.x + dx, p.y - h, 3.5);
        } else if (k < 0.8) {
          // a round brain coral
          deco.fillStyle(rnd.pick([0xe8b07a, 0xd8a0c8, 0xb8d07a]), 1);
          deco.fillCircle(p.x, p.y, rnd.between(9, 13));
          deco.lineStyle(1.5, 0x8a6a5a, 0.6);
          deco.strokeCircle(p.x, p.y, 6);
          deco.strokeCircle(p.x, p.y, 10);
        } else {
          // a starfish on the sand
          deco.fillStyle(0xf0905a, 1);
          for (let s2 = 0; s2 < 5; s2++) {
            const a = (s2 / 5) * Math.PI * 2 - Math.PI / 2;
            deco.fillTriangle(p.x, p.y, p.x + Math.cos(a - 0.35) * 4, p.y + Math.sin(a - 0.35) * 4, p.x + Math.cos(a) * 11, p.y + Math.sin(a) * 11);
            deco.fillTriangle(p.x, p.y, p.x + Math.cos(a + 0.35) * 4, p.y + Math.sin(a + 0.35) * 4, p.x + Math.cos(a) * 11, p.y + Math.sin(a) * 11);
          }
        }
      } else if (this.level.theme.dunes) {
        if (rnd.frac() < 0.5) {
          // a saguaro-style cactus with two arms and a pink flower
          deco.fillStyle(0x000000, 0.18);
          deco.fillEllipse(p.x, p.y + 4, 26, 8);
          const col = rnd.pick(this.level.theme.trees ?? [0x6a9a4a]);
          deco.fillStyle(col, 1);
          deco.lineStyle(2, C.ink, 0.55);
          deco.fillRoundedRect(p.x - 5, p.y - 34, 10, 38, 5);
          deco.strokeRoundedRect(p.x - 5, p.y - 34, 10, 38, 5);
          deco.fillRoundedRect(p.x - 15, p.y - 24, 7, 14, 3);
          deco.fillRoundedRect(p.x - 15, p.y - 14, 12, 6, 3);
          deco.fillRoundedRect(p.x + 8, p.y - 28, 7, 14, 3);
          deco.fillRoundedRect(p.x + 3, p.y - 18, 12, 6, 3);
          deco.fillStyle(0xf08aa8, 1);
          deco.fillCircle(p.x, p.y - 36, 3);
        } else if (rnd.frac() < 0.6) {
          // a sun-bleached rock with a skull of some long-gone beast... or just a rock
          deco.fillStyle(rnd.pick([0xc8a878, 0xb89868, 0xd8b888]), 1);
          deco.fillEllipse(p.x, p.y, rnd.between(18, 30), rnd.between(10, 16));
          deco.lineStyle(1.5, C.ink, 0.4);
          deco.strokeEllipse(p.x, p.y, 24, 13);
        } else {
          // ripples in the sand
          deco.lineStyle(2, 0xc8a068, 0.7);
          for (let k = 0; k < 3; k++) {
            deco.beginPath();
            deco.arc(p.x + k * 6, p.y + 8 + k * 5, 16, Math.PI * 1.15, Math.PI * 1.85);
            deco.strokePath();
          }
        }
      } else if (this.level.theme.storm && rnd.frac() < 0.8) {
        if (rnd.frac() < 0.45) {
          // a weathered standing stone with a lichen patch
          const h = rnd.between(22, 34);
          deco.fillStyle(0x000000, 0.2);
          deco.fillEllipse(p.x, p.y + 4, 30, 10);
          deco.fillStyle(rnd.pick([0x7a7a82, 0x6a6e78, 0x8a8a90]), 1);
          deco.fillRoundedRect(p.x - 8, p.y - h, 16, h + 4, 5);
          deco.lineStyle(2, C.ink, 0.55);
          deco.strokeRoundedRect(p.x - 8, p.y - h, 16, h + 4, 5);
          deco.fillStyle(0x9aaa6a, 0.8);
          deco.fillEllipse(p.x - 2, p.y - h * 0.4, 8, 5);
        } else {
          // tufts of steppe grass bent flat by the wind
          deco.lineStyle(2, rnd.pick(this.level.theme.trees ?? [0x5a6a5a]), 0.9);
          for (let k = 0; k < 5; k++) {
            const bx = p.x - 8 + k * 4;
            deco.lineBetween(bx, p.y + 4, bx + 9, p.y - 8 + rnd.between(-2, 2));
          }
        }
      } else if (this.level.theme.orchard && rnd.frac() < 0.75) {
        if (rnd.frac() < 0.7) {
          // autumn fruit tree with a few red apples (and some fallen ones)
          const leaf = rnd.pick(this.level.theme.trees ?? [0xd8642a]);
          deco.fillStyle(0x000000, 0.2);
          deco.fillEllipse(p.x, p.y + 4, 40, 14);
          deco.fillStyle(0x6b4a2b, 1);
          deco.fillRect(p.x - 4, p.y - 14, 8, 18);
          deco.fillStyle(leaf, 1);
          deco.fillCircle(p.x, p.y - 26, 18);
          deco.fillCircle(p.x - 12, p.y - 16, 12);
          deco.fillCircle(p.x + 12, p.y - 16, 12);
          deco.lineStyle(2, C.ink, 0.6);
          deco.strokeCircle(p.x, p.y - 26, 18);
          deco.fillStyle(0xd02a2a, 1);
          for (let k = 0; k < 3; k++) deco.fillCircle(p.x - 10 + k * 10 + rnd.between(-2, 2), p.y - 22 + rnd.between(-6, 8), 3);
          deco.fillCircle(p.x + rnd.between(-14, 14), p.y + 6, 2.5);
        } else {
          // a little heap of fallen leaves
          for (let k = 0; k < 5; k++) {
            deco.fillStyle(rnd.pick([0xd8642a, 0xe8a03a, 0xb8442a]), 0.9);
            deco.fillEllipse(p.x + rnd.between(-12, 12), p.y + rnd.between(-5, 5), 10, 6);
          }
        }
      } else if (this.level.theme.abyss && rnd.frac() < 0.9) {
        if (rnd.frac() < 0.5) {
          // a pale stalagmite cluster
          deco.fillStyle(0x000000, 0.25);
          deco.fillEllipse(p.x, p.y + 4, 30, 9);
          for (const [dx, h, w] of [[-8, 18, 7], [2, 30, 9], [10, 14, 6]]) {
            deco.fillStyle(0x5a5a80, 1);
            deco.fillTriangle(p.x + dx - w, p.y + 2, p.x + dx + w, p.y + 2, p.x + dx, p.y - h);
            deco.lineStyle(1.5, C.ink, 0.5);
            deco.strokeTriangle(p.x + dx - w, p.y + 2, p.x + dx + w, p.y + 2, p.x + dx, p.y - h);
          }
        } else {
          // a glowing pool that breathes
          const col = rnd.pick(this.level.theme.trees ?? [0x6ad8e8]);
          deco.fillStyle(0x0a0c1a, 1);
          deco.fillEllipse(p.x, p.y, 44, 20);
          const glow = this.add.ellipse(p.x, p.y, 36, 14, col, 0.55).setDepth(1);
          this.tweens.add({ targets: glow, alpha: 0.2, yoyo: true, repeat: -1, duration: rnd.between(1200, 2200), ease: 'Sine.easeInOut' });
        }
      } else if (this.level.theme.gears && rnd.frac() < 0.9) {
        if (rnd.frac() < 0.6) {
          // a big brass gear half-sunk in the ground
          const col = rnd.pick(this.level.theme.trees ?? [0xc8963a]);
          const r0 = rnd.between(12, 20);
          deco.fillStyle(0x000000, 0.2);
          deco.fillEllipse(p.x, p.y + 4, r0 * 2.2, r0 * 0.7);
          deco.fillStyle(col, 1);
          for (let k = 0; k < 8; k++) {
            const a0 = (k / 8) * Math.PI * 2;
            deco.fillRect(p.x + Math.cos(a0) * r0 - 4, p.y - r0 + Math.sin(a0) * r0 - 4, 8, 8);
          }
          deco.fillCircle(p.x, p.y - r0, r0);
          deco.lineStyle(1.5, C.ink, 0.5);
          deco.strokeCircle(p.x, p.y - r0, r0);
          deco.fillStyle(0x2a2a30, 1);
          deco.fillCircle(p.x, p.y - r0, r0 * 0.3);
        } else {
          // a steam pipe with a valve wheel
          deco.fillStyle(0x000000, 0.2);
          deco.fillEllipse(p.x, p.y + 4, 30, 9);
          deco.fillStyle(0x7a7a84, 1);
          deco.fillRect(p.x - 6, p.y - 30, 12, 34);
          deco.fillRect(p.x - 6, p.y - 30, 24, 10);
          deco.lineStyle(1.5, C.ink, 0.5);
          deco.strokeRect(p.x - 6, p.y - 30, 12, 34);
          deco.lineStyle(3, 0xd03a2a, 1);
          deco.strokeCircle(p.x, p.y - 12, 6);
        }
      } else if (this.level.theme.ruins && rnd.frac() < 0.6) {
        if (rnd.frac() < 0.65) {
          // jungle palm: curved trunk and drooping fronds
          deco.fillStyle(0x000000, 0.2);
          deco.fillEllipse(p.x, p.y + 4, 36, 10);
          deco.lineStyle(5, 0x7a5a3a, 1);
          deco.beginPath();
          deco.moveTo(p.x, p.y + 2);
          deco.lineTo(p.x + 3, p.y - 12);
          deco.lineTo(p.x + 2, p.y - 26);
          deco.strokePath();
          const col = rnd.pick(this.level.theme.trees ?? [0x3f7f34]);
          deco.fillStyle(col, 1);
          deco.lineStyle(1.5, C.ink, 0.5);
          for (const [dx, dy, rot] of [[-14, -22, 0.5], [18, -22, -0.5], [-12, -32, 0.25], [16, -32, -0.25], [2, -36, 0]] as [number, number, number][]) {
            const f = new Phaser.Geom.Ellipse(p.x + 2 + dx, p.y + dy, 32, 12);
            deco.save();
            deco.translateCanvas(f.x, f.y);
            deco.rotateCanvas(rot);
            deco.fillEllipse(0, 0, f.width, f.height);
            deco.strokeEllipse(0, 0, f.width, f.height);
            deco.restore();
          }
        } else {
          // broken temple pillar wrapped in vines
          const h = rnd.between(18, 34);
          deco.fillStyle(0x000000, 0.2);
          deco.fillEllipse(p.x, p.y + 4, 30, 9);
          deco.fillStyle(0xb8ae94, 1);
          deco.fillRect(p.x - 7, p.y - h, 14, h + 4);
          deco.fillStyle(0x8a8270, 1);
          deco.fillRect(p.x - 10, p.y - 2, 20, 6);
          deco.fillRect(p.x - 9, p.y - h - 3, 18, 5);
          deco.lineStyle(1.5, C.ink, 0.5);
          deco.strokeRect(p.x - 7, p.y - h, 14, h + 4);
          deco.lineStyle(2.5, 0x3f8a34, 1);
          deco.beginPath();
          deco.moveTo(p.x - 7, p.y);
          deco.lineTo(p.x + 7, p.y - h * 0.4);
          deco.lineTo(p.x - 7, p.y - h * 0.75);
          deco.strokePath();
        }
      } else if (this.level.theme.gale && rnd.frac() < 0.55) {
        if (rnd.frac() < 0.7) {
          // wind-bent pine: tiers swept toward the east
          const col = rnd.pick(this.level.theme.trees ?? [0x4a6a5a]);
          deco.fillStyle(0x000000, 0.2);
          deco.fillEllipse(p.x + 4, p.y + 4, 36, 10);
          deco.fillStyle(0x6b4a2b, 1);
          deco.fillRect(p.x - 3, p.y - 10, 6, 14);
          for (const [dy, w, lean] of [[-6, 34, 8], [-20, 26, 10], [-32, 18, 12]]) {
            deco.fillStyle(col, 1);
            deco.fillTriangle(p.x - w / 2, p.y + dy, p.x + w / 2 + lean, p.y + dy, p.x + lean, p.y + dy - 18);
            deco.lineStyle(1.5, C.ink, 0.5);
            deco.strokeTriangle(p.x - w / 2, p.y + dy, p.x + w / 2 + lean, p.y + dy, p.x + lean, p.y + dy - 18);
          }
        } else {
          // stone cairn
          deco.fillStyle(0x000000, 0.2);
          deco.fillEllipse(p.x, p.y + 4, 28, 9);
          for (const [dy, r] of [[0, 10], [-13, 7.5], [-23, 5]]) {
            deco.fillStyle(0x9a9aa2, 1);
            deco.fillEllipse(p.x, p.y + dy, r * 2.2, r * 1.5);
            deco.lineStyle(1.5, C.ink, 0.5);
            deco.strokeEllipse(p.x, p.y + dy, r * 2.2, r * 1.5);
          }
        }
      } else if (this.level.theme.shrooms && rnd.frac() < 0.5) {
        // giant duskcap mushrooms with glowing spots
        const cap = rnd.pick(this.level.theme.trees ?? [0x8a5ab8]);
        const h = rnd.between(14, 24);
        deco.fillStyle(0x000000, 0.2);
        deco.fillEllipse(p.x, p.y + 4, 36, 12);
        deco.fillStyle(0xe8dcc8, 1);
        deco.fillRoundedRect(p.x - 5, p.y - h, 10, h + 4, 4);
        deco.fillStyle(cap, 1);
        deco.fillEllipse(p.x, p.y - h, 40, 24);
        deco.lineStyle(2, C.ink, 0.6);
        deco.strokeEllipse(p.x, p.y - h, 40, 24);
        deco.fillStyle(0xbff4ff, 0.9);
        for (let k = 0; k < 3; k++) deco.fillCircle(p.x - 10 + k * 10 + rnd.between(-2, 2), p.y - h - 4 + rnd.between(-2, 3), 2.5);
      } else if (rnd.frac() < 0.45) {
        deco.fillStyle(0x000000, 0.2);
        deco.fillEllipse(p.x, p.y + 4, 40, 14);
        deco.fillStyle(0x6b4a2b, 1);
        deco.fillRect(p.x - 4, p.y - 14, 8, 18);
        const leaf = rnd.pick(this.level.theme.trees ?? [0x3f7f34, 0x4b8f3a, 0x377030]);
        deco.fillStyle(leaf, 1);
        deco.fillCircle(p.x, p.y - 26, 18);
        deco.fillCircle(p.x - 12, p.y - 16, 12);
        deco.fillCircle(p.x + 12, p.y - 16, 12);
        deco.lineStyle(2, C.ink, 0.6);
        deco.strokeCircle(p.x, p.y - 26, 18);
        if (this.level.theme.snow) {
          deco.fillStyle(0xffffff, 0.95);
          deco.fillEllipse(p.x - 3, p.y - 36, 22, 10);
        }
      } else {
        const col = rnd.pick([0xffffff, 0xffe066, 0xff8fb1, 0xb5a8ff]);
        deco.fillStyle(col, 1);
        for (let k = 0; k < 4; k++) deco.fillCircle(p.x + rnd.between(-8, 8), p.y + rnd.between(-6, 6), 3);
      }
    }
    // gate marker at each distinct road exit (clamped on screen)
    const gates = new Set<string>();
    for (const pts of this.level.paths) {
      const last = pts[pts.length - 1];
      const gx = Math.max(60, Math.min(GAME_W - 60, last.x));
      const gy = Math.max(80, Math.min(GAME_H - 20, last.y));
      const key = `${Math.round(gx)},${Math.round(gy)}`;
      if (gates.has(key)) continue;
      gates.add(key);
      const gate = this.add.graphics().setDepth(gy);
      gate.fillStyle(0x7a5232, 1);
      gate.fillRect(gx - 40, gy - 60, 12, 70);
      gate.fillRect(gx + 28, gy - 60, 12, 70);
      gate.fillStyle(0x9a6a40, 1);
      gate.fillRect(gx - 48, gy - 70, 96, 16);
      gate.lineStyle(3, C.ink, 1);
      gate.strokeRect(gx - 48, gy - 70, 96, 16);
      gate.fillStyle(0x4b8f3a, 1);
      gate.fillCircle(gx - 34, gy - 70, 10);
      gate.fillCircle(gx + 34, gy - 70, 10);
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

  // ---------- spells ----------

  private spellPos(i: number): Vec2 {
    return { x: GAME_W - 58 - (SPELL_ORDER.length - 1 - i) * 92, y: GAME_H - 58 };
  }

  private buildSpells(): void {
    this.spellHud = this.add.graphics().setDepth(3000);
    this.reticle = this.add.circle(0, 0, 60, 0xffffff, 0.12).setStrokeStyle(3, C.cream, 0.9).setDepth(2900).setVisible(false);
    SPELL_ORDER.forEach((id, i) => {
      const p = this.spellPos(i);
      this.add.image(p.x, p.y - 4, `icon_${id}`).setDepth(3001);
      fitWidth(this.add.text(p.x, p.y + 30, SPELLS[id].name, textStyle(pf(12))).setOrigin(0.5).setDepth(3002), 84);
      const zone = this.add.zone(p.x, p.y, 80, 80).setDepth(3002).setInteractive({ useHandCursor: true });
      zone.on('pointerdown', (_p: Phaser.Input.Pointer, _x: number, _y: number, ev: Phaser.Types.Input.EventData) => {
        ev.stopPropagation();
        sfx.unlock();
        sfx.click();
        this.closeMenu();
        this.selectHero(false);
        this.armSpell(this.spellMode === id ? null : id);
      });
    });
  }

  private armSpell(id: string | null): void {
    if (id && this.sim.mods.noSpells) {
      this.floatText(GAME_W - 120, GAME_H - 120, 'Spells are clouded today', TEXT.dim, 18);
      return;
    }
    if (id && !this.sim.spellReady(id)) {
      this.floatText(GAME_W - 120, GAME_H - 120, 'Recharging…', TEXT.dim, 18);
      return;
    }
    this.spellMode = id;
    this.reticle.setVisible(!!id);
    this.children.getByName('spellHint')?.destroy();
    if (id) {
      const def = SPELLS[id];
      this.reticle.setRadius(def.radius ?? 50).setStrokeStyle(3, def.color, 0.9).setFillStyle(def.color, 0.12);
      const how = def.kind === 'reinforce' ? 'Tap a spot on the road' : def.kind === 'snare' ? 'Tap a crowd of walkers' : 'Tap where the star should fall';
      this.showBanner(def.name, how);
      // What the spell does, just above the spell bar, while it's armed.
      const w = 330;
      const hint = this.add.container(GAME_W - 20 - w / 2, GAME_H - 132).setDepth(3500).setName('spellHint');
      const txt = this.add.text(0, 0, `${def.text}\nRecharge ${def.cooldown}s`, { ...textStyle(pf(14), TEXT.cream, false), align: 'center', wordWrap: { width: w - 24 } }).setOrigin(0.5);
      const bg = this.add.graphics();
      bg.fillStyle(C.ink, 0.85);
      bg.fillRoundedRect(-w / 2, -txt.height / 2 - 10, w, txt.height + 20, 12);
      bg.lineStyle(2, def.color, 0.9);
      bg.strokeRoundedRect(-w / 2, -txt.height / 2 - 10, w, txt.height + 20, 12);
      hint.add([bg, txt]);
      hint.y = GAME_H - 104 - txt.height / 2;
    } else {
      this.children.getByName('banner')?.destroy();
    }
  }

  private castAt(id: string, p: Vec2): void {
    if (this.sim.castSpell(id, p)) {
      this.armSpell(null);
    } else {
      this.floatText(p.x, p.y, SPELLS[id].kind === 'reinforce' ? 'Must be on the road!' : 'Not ready', TEXT.heart, 18);
    }
  }

  private drawSpellHud(): void {
    const g = this.spellHud;
    g.clear();
    SPELL_ORDER.forEach((id, i) => {
      const p = this.spellPos(i);
      const def = SPELLS[id];
      const cd = this.sim.mods.noSpells ? def.cooldown : (this.sim.spellCd[id] ?? 0);
      g.fillStyle(C.ink, 0.85);
      g.fillCircle(p.x, p.y, 40);
      g.fillStyle(cd > 0 ? 0x3a4a3e : C.panelLight, 1);
      g.fillCircle(p.x, p.y, 35);
      if (cd > 0) {
        g.fillStyle(0x000000, 0.5);
        g.slice(p.x, p.y, 35, -Math.PI / 2, -Math.PI / 2 + Math.PI * 2 * (cd / def.cooldown), false);
        g.fillPath();
      }
      const armed = this.spellMode === id;
      g.lineStyle(armed ? 5 : 3, armed ? C.cream : cd > 0 ? 0x777777 : def.color, 1);
      g.strokeCircle(p.x, p.y, armed ? 41 : 36);
    });
  }

  // ---------- hero ----------

  private buildHero(): void {
    const h = this.sim.hero;
    if (!h) return;
    this.heroRing = this.add.ellipse(h.pos.x, h.pos.y, 56, 22).setStrokeStyle(3, C.gold, 1).setFillStyle(C.gold, 0.15).setVisible(false);
    this.tweens.add({ targets: this.heroRing, scale: 1.15, yoyo: true, repeat: -1, duration: 500 });
    this.heroSprite = this.add.image(h.pos.x, h.pos.y, `hero_${h.def.id}`).setOrigin(0.5, 0.9).setInteractive({ useHandCursor: true });
    padHit(this.heroSprite, 84);
    this.heroSprite.on('pointerdown', (_p: Phaser.Input.Pointer, _x: number, _y: number, ev: Phaser.Types.Input.EventData) => {
      ev.stopPropagation();
      sfx.unlock();
      this.closeMenu();
      this.selectHero(!this.heroSelected);
    });
    this.heroBar = this.add.graphics();

    // HUD: portrait (select) + skill button, bottom-left.
    const px = 58;
    const py = GAME_H - 58;
    this.heroHud = this.add.graphics().setDepth(3000);
    const portrait = this.add.image(px, py + 6, `hero_${h.def.id}`).setDepth(3001).setScale(1.05);
    portrait.setInteractive(new Phaser.Geom.Circle(26, 30, 40), Phaser.Geom.Circle.Contains);
    portrait.on('pointerdown', (_p: Phaser.Input.Pointer, _x: number, _y: number, ev: Phaser.Types.Input.EventData) => {
      ev.stopPropagation();
      sfx.unlock();
      sfx.click();
      this.closeMenu();
      this.selectHero(!this.heroSelected);
    });
    this.heroLevelText = this.add.text(px + 30, py + 30, '1', textStyle(18, TEXT.gold)).setOrigin(0.5).setDepth(3002);
    const skillZone = this.add.zone(px + 104, py, 76, 76).setDepth(3002).setInteractive({ useHandCursor: true });
    skillZone.on('pointerdown', (_p: Phaser.Input.Pointer, _x: number, _y: number, ev: Phaser.Types.Input.EventData) => {
      ev.stopPropagation();
      sfx.unlock();
      if (!this.sim.useHeroSkill()) this.tweens.add({ targets: this.skillText, x: this.skillText.x + 4, duration: 40, yoyo: true, repeat: 2 });
    });
    this.skillText = this.add.text(px + 104, py, h.def.active.name.replace(' ', '\n'), { ...textStyle(pf(13)), align: 'center' }).setOrigin(0.5).setDepth(3002);
    fitWidth(this.skillText, 68);
  }

  private selectHero(on: boolean): void {
    if (!this.sim.hero?.alive) on = false;
    this.heroSelected = on;
    this.heroRing?.setVisible(on);
    if (on) this.floatText(this.sim.hero!.pos.x, this.sim.hero!.pos.y - 70, 'Tap to move', TEXT.cream, 16);
  }

  private orderHeroMove(p: Vec2): void {
    this.selectHero(false);
    if (!this.sim.moveHero(p)) return;
    sfx.click();
    const mark = this.add.circle(p.x, p.y, 16).setStrokeStyle(3, C.gold, 1).setDepth(p.y);
    this.tweens.add({ targets: mark, scale: 0.2, alpha: 0, duration: 450, onComplete: () => mark.destroy() });
  }

  private syncHero(): void {
    const h = this.sim.hero;
    if (!h || !this.heroSprite) return;
    const moving = !!h.dest;
    const bob = moving ? Math.abs(Math.sin(this.time.now / 90)) * 4 : 0;
    this.heroSprite.setVisible(h.alive).setPosition(h.pos.x, h.pos.y - bob).setDepth(h.pos.y).setFlipX(h.facing < 0);
    this.heroRing.setPosition(h.pos.x, h.pos.y).setDepth(h.pos.y - 1);
    if (!h.alive && this.heroSelected) this.selectHero(false);
    this.heroBar.clear();
    if (h.alive && h.hp < h.maxHp) {
      const w = 34;
      this.heroBar.fillStyle(C.ink, 0.85);
      this.heroBar.fillRect(h.pos.x - w / 2 - 1, h.pos.y - 62, w + 2, 7);
      this.heroBar.fillStyle(0x7be35a, 1);
      this.heroBar.fillRect(h.pos.x - w / 2, h.pos.y - 61, w * (h.hp / h.maxHp), 5);
      this.heroBar.setDepth(h.pos.y + 0.5);
    }

    // HUD
    const px = 58;
    const py = GAME_H - 58;
    const g = this.heroHud;
    g.clear();
    g.fillStyle(C.ink, 0.8);
    g.fillCircle(px, py, 42);
    g.fillStyle(h.alive ? C.panelLight : 0x553333, 1);
    g.fillCircle(px, py, 36);
    // xp arc
    const next = HERO_XP[h.level] ?? HERO_XP[HERO_MAX_LEVEL - 1];
    const prev = HERO_XP[h.level - 1];
    const frac = h.level >= HERO_MAX_LEVEL ? 1 : (h.xp - prev) / Math.max(1, next - prev);
    g.lineStyle(5, C.gold, 1);
    g.beginPath();
    g.arc(px, py, 39, -Math.PI / 2, -Math.PI / 2 + Math.PI * 2 * frac);
    g.strokePath();
    if (this.heroSelected) {
      g.lineStyle(3, C.cream, 1);
      g.strokeCircle(px, py, 44);
    }
    g.fillStyle(C.ink, 1);
    g.fillCircle(px + 30, py + 30, 14);
    this.heroLevelText.setText(String(h.level));
    // skill button with cooldown pie
    const sx = px + 104;
    const ready = h.alive && h.skillCd <= 0;
    g.fillStyle(C.ink, 0.85);
    g.fillCircle(sx, py, 38);
    g.fillStyle(ready ? h.def.color : 0x44524a, 1);
    g.fillCircle(sx, py, 33);
    if (!ready && h.alive) {
      const cdFrac = h.skillCd / h.def.active.cooldown;
      g.fillStyle(0x000000, 0.45);
      g.slice(sx, py, 33, -Math.PI / 2, -Math.PI / 2 + Math.PI * 2 * cdFrac, false);
      g.fillPath();
    }
    g.lineStyle(3, ready ? C.gold : 0x777777, 1);
    g.strokeCircle(sx, py, 34);
    this.skillText.setAlpha(ready ? 1 : 0.6);
    if (!h.alive) this.heroLevelText.setText(`${Math.ceil(h.respawnTimer)}s`);
  }

  /** Desert ponds become oases: a ring of reeds and a date palm leaning out over each end. */
  private drawOasis(pd: { x: number; y: number; w: number; h: number }): void {
    const g = this.add.graphics().setDepth(1);
    g.lineStyle(2, 0x5a9a3a, 0.9);
    for (let k = 0; k < 14; k++) {
      const a = (k / 14) * Math.PI * 2;
      const rx = pd.x + Math.cos(a) * (pd.w / 2 + 2);
      const ry = pd.y + Math.sin(a) * (pd.h / 2 + 2);
      g.lineBetween(rx, ry, rx + Math.cos(a) * 3, ry - 9);
    }
    for (const side of [-1, 1]) {
      const bx = pd.x + side * (pd.w / 2 - 6);
      const by = pd.y - 2;
      const tx = bx + side * 14;
      const ty = by - 44;
      g.fillStyle(0x000000, 0.18);
      g.fillEllipse(tx, by + 6, 34, 9);
      g.lineStyle(6, 0x8a6a3a, 1);
      g.beginPath();
      g.moveTo(bx, by);
      g.lineTo(bx + side * 8, by - 24);
      g.lineTo(tx, ty);
      g.strokePath();
      // drooping fronds: thick curved strokes arching out and down from the crown
      for (const [dx, lift, col] of [[-26, 10, 0x3f7a32], [26, 10, 0x3f7a32], [-18, -2, 0x4f9a3a], [18, -2, 0x4f9a3a], [-6, -8, 0x5aaa44], [8, -8, 0x5aaa44]] as const) {
        g.lineStyle(5, col, 1);
        g.beginPath();
        g.moveTo(tx, ty);
        g.lineTo(tx + dx * 0.5, ty - 6 + lift * 0.2);
        g.lineTo(tx + dx, ty + lift);
        g.strokePath();
      }
      g.fillStyle(0x9a5a2a, 1);
      g.fillCircle(tx - 3, ty + 4, 3);
      g.fillCircle(tx + 3, ty + 5, 3);
    }
  }

  private skillEffect(kind: string, pos: Vec2, radius: number, color: number, fx?: number): void {
    if (kind === 'quake') {
      for (let i = 0; i < 3; i++) {
        const ring = this.add.ellipse(pos.x, pos.y, radius * 2, radius * 1.1).setStrokeStyle(6, 0xc9a66b, 1).setDepth(2400).setScale(0.2);
        this.tweens.add({ targets: ring, scale: 1, alpha: 0, delay: i * 90, duration: 420, onComplete: () => ring.destroy() });
      }
      this.particles.setParticleTint(0xa8844e);
      this.particles.explode(30, pos.x, pos.y);
      this.cameras.main.shake(260, 0.01);
      sfx.boom();
    } else if (kind === 'rally') {
      // a soft green pulse of healing
      const ring = this.add.circle(pos.x, pos.y, radius, color, 0.18).setStrokeStyle(4, fx ?? 0x9bff8a, 1).setDepth(2400).setScale(0.1);
      this.tweens.add({ targets: ring, scale: 1, alpha: 0, duration: 600, onComplete: () => ring.destroy() });
      sfx.trait('mend');
    } else if (kind === 'ring') {
      const ring = this.add.circle(pos.x, pos.y, radius, color, 0.25).setStrokeStyle(6, fx ?? 0xffd23c, 1).setDepth(2400).setScale(0.1);
      this.tweens.add({ targets: ring, scale: 1, alpha: 0, duration: 500, onComplete: () => ring.destroy() });
      this.particles.setParticleTint(fx ?? 0xffa040);
      for (let i = 0; i < 12; i++) {
        const a = (i / 12) * Math.PI * 2;
        this.particles.explode(3, pos.x + Math.cos(a) * radius * 0.8, pos.y + Math.sin(a) * radius * 0.8);
      }
      sfx.shoot('glimmer');
    } else {
      sfx.shoot('thornbow');
    }
  }

  /** Small strip under the wave button showing which enemies the next wave brings. */
  private refreshWavePreview(): void {
    this.children.getByName('wavePreview')?.destroy();
    const next = this.sim.waveIndex + 1;
    if (next >= this.sim.totalWaves || this.ended) return;
    const counts = new Map<string, number>();
    for (const g of this.level.waves[next].groups) counts.set(g.enemy, (counts.get(g.enemy) ?? 0) + g.count);
    const entries = [...counts.entries()].slice(0, 4);
    const w = entries.length * 62 + 16;
    // Lives in the empty strip of the top bar between the stats panel and the buttons.
    const c = this.add.container(470 + 36 + w / 2, 37).setDepth(3000).setName('wavePreview');
    const bg = this.add.graphics();
    bg.fillStyle(C.ink, 0.7);
    bg.fillRoundedRect(-w / 2, -18, w, 36, 12);
    c.add(bg);
    entries.forEach(([id, n], i) => {
      const x = -w / 2 + 22 + i * 62;
      const img = this.add.image(x, 0, `enemy_${id}`);
      img.setScale(Math.min(0.8, 30 / Math.max(img.width, img.height)));
      c.add(img);
      const def = ENEMIES[id];
      c.add(this.add.text(x + 14, 2, `${n}`, textStyle(pf(14), def.boss ? TEXT.heart : TEXT.cream)).setOrigin(0, 0.5));
      if (def.flying) c.add(this.add.text(x - 14, -12, '✈', textStyle(pf(10), '#bfe8ff')).setOrigin(0.5));
    });
    c.add(this.add.text(-w / 2 - 4, 0, 'Next', textStyle(pf(13), TEXT.dim)).setOrigin(1, 0.5));
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
    this.waveText.setText(`${Math.max(0, this.sim.waveIndex + 1)}/${this.endless ? '∞' : this.sim.totalWaves}`);
    if (this.sim.wavesRemaining && this.sim.isActive()) {
      const secs = Math.ceil(this.sim.waveCountdown);
      this.nextWaveBtn.label.setText(
        this.sim.waveIndex < 0 ? `Start! (${secs})` : this.sim.spawning ? 'Call Early' : `Next Wave (${secs})`,
      );
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
    this.children.getByName('pauseMenu')?.destroy();
    if (!this.paused) return;
    this.closeMenu();
    this.children.getByName('banner')?.destroy();
    const c = this.add.container(GAME_W / 2, GAME_H / 2).setDepth(4800).setName('pauseMenu');
    const shade = this.add.rectangle(0, 0, GAME_W, GAME_H, 0x000000, 0.45).setInteractive();
    shade.on('pointerdown', (_p: Phaser.Input.Pointer, _x: number, _y: number, ev: Phaser.Types.Input.EventData) => ev.stopPropagation());
    const bg = this.add.graphics();
    bg.fillStyle(C.ink, 1);
    bg.fillRoundedRect(-200, -190, 400, 380, 26);
    bg.fillStyle(C.panel, 1);
    bg.fillRoundedRect(-192, -182, 384, 364, 22);
    c.add([shade, bg, this.add.text(0, -140, 'Paused', textStyle(44, TEXT.gold)).setOrigin(0.5)]);
    const soundLabel = () => (loadSave().settings.muted ? 'Sound: Off' : 'Sound: On');
    const items: [string, number, () => void][] = [
      ['Resume', C.leaf, () => this.togglePause()],
      ['Restart', C.sky, () => this.scene.restart({ levelIndex: this.levelIndex, daily: !!this.daily, endless: this.endless })],
      [soundLabel(), 0xb07cff, () => {}],
      ['Quit to Map', 0xff9f43, () => this.scene.start('WorldMap', { focus: this.levelIndex })],
    ];
    items.forEach(([label, color, fn], i) => {
      const b = new Button(this, 0, -60 + i * 70, label, { width: 260, height: 56, fontSize: 22, color, onClick: fn });
      if (i === 2) {
        b.removeAllListeners('pointerdown');
        b.on('pointerdown', (_p: Phaser.Input.Pointer, _x: number, _y: number, ev: Phaser.Types.Input.EventData) => {
          ev.stopPropagation();
          const s2 = loadSave();
          s2.settings.muted = !s2.settings.muted;
          writeSave(s2);
          sfx.setVolume(s2.settings.volume, s2.settings.muted);
          sfx.unlock();
          sfx.click();
          b.label.setText(soundLabel());
        });
      }
      c.add(b);
    });
    c.setScale(0.8).setAlpha(0);
    this.tweens.add({ targets: c, scale: 1, alpha: 1, duration: 160, ease: 'Back.easeOut' });
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
    this.pendingSpec = null;
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
        const cost = this.sim.price(def.tiers[0].cost);
        const o = offsets[i];
        const opt = this.menuOption(o.x, o.y, `tower_${id}_0`, String(cost), this.sim.coins >= cost, () => {
          if (this.sim.build(slot, id)) this.closeMenu();
        });
        opt.on('pointerover', () => this.drawRange(pos, def.tiers[0].range, def.color));
        c.add(opt);
      });
      c.add(this.add.text(0, 0, 'Build', textStyle(18)).setOrigin(0.5));
    } else {
      const stats = this.sim.stats(tower);
      this.drawRange(pos, stats.range, tower.def.color);
      const upCost = this.sim.upgradeCost(tower);
      if (this.sim.canSpecialize(tower)) {
        tower.def.specs.forEach((sp, k) => {
          const ox = k === 0 ? -56 : 56;
          const opt = this.menuOption(ox, -82, `tower_${tower.def.id}_${sp.id}`, String(this.sim.price(sp.stats.cost)), this.sim.coins >= this.sim.price(sp.stats.cost), () => {
            if (this.pendingSpec === `${slot}:${k}`) {
              if (this.sim.specialize(slot, k)) this.openSlotMenu(slot);
              return;
            }
            this.pendingSpec = `${slot}:${k}`;
            this.drawRange(pos, sp.stats.range, sp.color);
            this.showBanner(sp.name, `${sp.text}  (tap again to buy)`);
          });
          opt.add(this.add.text(0, -50, sp.name, { ...textStyle(pf(13)), align: 'center', wordWrap: { width: 110 } }).setOrigin(0.5, 1));
          c.add(opt);
        });
      } else if (upCost !== null) {
        c.add(
          this.menuOption(0, -80, `tower_${tower.def.id}_${tower.tier + 1}`, String(upCost), this.sim.coins >= upCost, () => {
            if (this.sim.upgrade(slot)) this.openSlotMenu(slot);
          }),
        );
      } else {
        c.add(this.add.text(0, -80, 'MAX', textStyle(22, TEXT.gold)).setOrigin(0.5));
      }
      const refund = sellValue(tower.def, tower.tier, tower.spec, this.sim.mods.costMult);
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
      const specName = tower.spec ? tower.def.specs.find((x) => x.id === tower.spec)!.name : `${tower.def.name} • Lv ${tower.tier + 1}`;
      c.add(this.add.text(0, 92, specName, textStyle(16)).setOrigin(0.5));
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
    o.add([bg, this.add.text(0, 0, text, { ...textStyle(pf(14)), align: 'center' }).setOrigin(0.5)]);
    o.setSize(68, 68).setInteractive({ useHandCursor: true });
    padHit(o);
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
    this.syncHero();
    this.drawSpellHud();
    if (!this.ended) music.setMood(this.sim.enemies.some((e) => e.alive && e.def.boss) ? 'boss' : 'battle');
    this.drawBossBar();
    this.refreshHud();
  }

  private handleEvent(ev: SimEvent): void {
    switch (ev.type) {
      case 'spawn':
        this.addEnemyView(ev.enemy);
        if (!this.seen.has(ev.enemy.def.id)) {
          this.seen.add(ev.enemy.def.id);
          // Persist new sightings right away so the Field Guide unlocks even if the battle is quit.
          const s0 = loadSave();
          if (!s0.seenEnemies.includes(ev.enemy.def.id)) {
            writeSave(markSeen(s0, [ev.enemy.def.id]));
            if (s0.seenEnemies.length > 0) this.floatText(ev.enemy.pos.x + 40, ev.enemy.pos.y - 40, 'New in Field Guide!', '#bfe8ff', 14);
          }
        }
        if (ev.enemy.def.boss) {
          this.showBanner(`${ev.enemy.def.name} approaches!`, 'Focus everything on the boss');
          this.cameras.main.shake(500, 0.01);
          sfx.waveHorn();
        }
        break;
      case 'heroShoot': {
        const key = `proj_${ev.projectile.kind}`;
        const img = this.add.image(ev.projectile.pos.x, ev.projectile.pos.y, this.textures.exists(key) ? key : 'dot').setDepth(2500);
        this.projViews.set(ev.projectile.uid, img);
        sfx.shoot(ev.hero.def.id === 'ember' ? 'glimmer' : 'thornbow');
        break;
      }
      case 'heroSkill': {
        const sk = ev.hero.def.active;
        this.skillEffect(sk.kind, ev.hero.pos, sk.radius, sk.fxColor ?? ev.hero.def.color, sk.fxColor);
        if (sk.kind === 'volley') {
          for (const e of ev.hits) {
            const f = this.add.image(ev.hero.pos.x, ev.hero.pos.y - 30, 'proj_hero_fen').setDepth(2500);
            f.setRotation(Math.atan2(e.pos.y - f.y, e.pos.x - f.x));
            this.tweens.add({ targets: f, x: e.pos.x, y: e.pos.y, duration: 200, onComplete: () => f.destroy() });
          }
        }
        for (const p of ev.healed ?? []) {
          this.particles.setParticleTint(0x9bff8a);
          this.particles.explode(6, p.x, p.y - 16);
          this.floatText(p.x, p.y - 40, '+' + Math.round(this.sim.heroStat(sk.heal ?? 0)), '#9bff8a', 14);
        }
        this.floatText(ev.hero.pos.x, ev.hero.pos.y - 80, sk.name + '!', TEXT.gold, 22);
        break;
      }
      case 'heroLevel':
        this.floatText(ev.hero.pos.x, ev.hero.pos.y - 80, `Level ${ev.hero.level}!`, TEXT.gold, 24);
        this.particles.setParticleTint(C.gold);
        this.particles.explode(24, ev.hero.pos.x, ev.hero.pos.y - 30);
        sfx.victory();
        break;
      case 'heroDown':
        this.floatText(ev.hero.pos.x, ev.hero.pos.y - 60, `${ev.hero.def.name} is down!`, TEXT.heart, 20);
        this.particles.setParticleTint(0xffffff);
        this.particles.explode(16, ev.hero.pos.x, ev.hero.pos.y - 20);
        sfx.leak();
        break;
      case 'heroBack':
        this.floatText(ev.hero.pos.x, ev.hero.pos.y - 60, `${ev.hero.def.name} returns!`, TEXT.gold, 20);
        break;
      case 'shoot': {
        const key = `proj_${ev.tower.def.id}`;
        const img = this.add.image(ev.projectile.pos.x, ev.projectile.pos.y, this.textures.exists(key) ? key : 'dot').setDepth(2500);
        if (ev.tower.spec) img.setTint(ev.projectile.color);
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
        this.tally.kills++;
        if (ev.enemy.def.boss) this.tally.bosses.push(ev.enemy.def.id);
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
        this.refreshWavePreview();
        {
          const parts: string[] = [];
          if (ev.income > 0) parts.push(`Supplies +${ev.income}`);
          if (ev.bonus > 0) parts.push(`Early call +${ev.bonus}`);
          this.showBanner(this.endless ? `Endless wave ${ev.index + 1}` : `Wave ${ev.index + 1} of ${this.sim.totalWaves}`, parts.length ? parts.join('   •   ') + ' coins' : 'Here they come!');
          if (ev.income + ev.bonus > 0) this.tweens.add({ targets: this.coinText, scale: 1.35, duration: 120, yoyo: true });
        }
        break;
      case 'waveCleared':
        break;
      case 'melee':
        sfx.melee();
        break;
      case 'spellCast': {
        const def = SPELLS[ev.spellId];
        if (def.kind === 'meteor') {
          // Visuals are created in syncStrikes() from sim.strikes so they track game time exactly.
          sfx.waveHorn();
        } else if (def.kind === 'snare') {
          const r = def.radius ?? 90;
          const ring = this.add.circle(ev.pos.x, ev.pos.y, r, 0x4a7a2a, 0.3).setStrokeStyle(5, 0x8fdc5a, 1).setDepth(2400).setScale(0.3);
          this.tweens.add({ targets: ring, scale: 1, alpha: 0, duration: 600, ease: 'Back.easeOut', onComplete: () => ring.destroy() });
          const vines = this.add.graphics().setDepth(2401);
          for (let k = 0; k < 9; k++) {
            const a = (k / 9) * Math.PI * 2;
            const d = r * (0.3 + (k % 3) * 0.25);
            const x = ev.pos.x + Math.cos(a) * d;
            const y = ev.pos.y + Math.sin(a) * d * 0.6;
            vines.fillStyle(0x3f7a2e, 1);
            vines.fillTriangle(x - 5, y + 4, x + 5, y + 4, x, y - 16);
            vines.fillStyle(0xd9e8a0, 1);
            vines.fillTriangle(x - 1, y - 6, x + 3, y - 8, x + 1, y - 12);
          }
          this.tweens.add({ targets: vines, alpha: 0, delay: 2500, duration: 900, onComplete: () => vines.destroy() });
          this.particles.setParticleTint(0x6a9a3a);
          this.particles.explode(20, ev.pos.x, ev.pos.y);
          sfx.build();
        } else {
          this.particles.setParticleTint(0x8fdc5a);
          this.particles.explode(24, ev.pos.x, ev.pos.y);
          this.floatText(ev.pos.x, ev.pos.y - 50, 'Rangers, to me!', TEXT.gold, 20);
          sfx.build();
        }
        break;
      }
      case 'strike': {
        const sv = this.strikeViews.get(ev.uid);
        sv?.star.destroy();
        sv?.mark.destroy();
        this.strikeViews.delete(ev.uid);
        const ring = this.add.circle(ev.pos.x, ev.pos.y, ev.radius, 0xfff0a8, 0.4).setStrokeStyle(8, 0xffc93c, 1).setDepth(2400).setScale(0.2);
        this.tweens.add({ targets: ring, scale: 1.1, alpha: 0, duration: 450, onComplete: () => ring.destroy() });
        this.particles.setParticleTint(0xffc93c);
        this.particles.explode(40, ev.pos.x, ev.pos.y);
        this.particles.setParticleTint(0x9a8a6a);
        this.particles.explode(20, ev.pos.x, ev.pos.y);
        this.cameras.main.shake(350, 0.014);
        this.cameras.main.flash(100, 255, 240, 180);
        sfx.boom();
        break;
      }
      case 'summonGone':
        this.particles.setParticleTint(0x8fdc5a);
        this.particles.explode(8, ev.soldier.pos.x, ev.soldier.pos.y);
        break;
      case 'spores': {
        sfx.trait('spores');
        const cloud = this.add.circle(ev.enemy.pos.x, ev.enemy.pos.y, ev.radius, 0xe8a0d0, 0.28).setStrokeStyle(3, 0xffd0f0, 0.8).setDepth(2400).setScale(0.3);
        this.tweens.add({ targets: cloud, scale: 1, alpha: 0, duration: 700, ease: 'Cubic.easeOut', onComplete: () => cloud.destroy() });
        this.particles.setParticleTint(0xffc0e8);
        this.particles.explode(18, ev.enemy.pos.x, ev.enemy.pos.y);
        if (ev.hasted.length) this.floatText(ev.enemy.pos.x, ev.enemy.pos.y - 28, `Spores! ×${ev.hasted.length}`, '#ffc0e8', 16);
        break;
      }
      case 'coral': {
        sfx.trait('coral');
        const ring = this.add.circle(ev.source.pos.x, ev.source.pos.y, ev.radius, 0xff9aa8, 0.12).setStrokeStyle(3, 0xffc0c8, 0.9).setDepth(2400).setScale(0.3);
        this.tweens.add({ targets: ring, scale: 1, alpha: 0, duration: 550, onComplete: () => ring.destroy() });
        for (const t of ev.targets) {
          this.particles.setParticleTint(0xffc0c8);
          this.particles.explode(4, t.pos.x, t.pos.y - 6);
        }
        break;
      }
      case 'shock': {
        sfx.trait('shock');
        const ring = this.add.circle(ev.source.pos.x, ev.source.pos.y, ev.radius, 0x9af0ff, 0.1).setStrokeStyle(3, 0xbff8ff, 0.9).setDepth(2400).setScale(0.3);
        this.tweens.add({ targets: ring, scale: 1, alpha: 0, duration: 350, onComplete: () => ring.destroy() });
        for (const h of ev.hits) {
          this.particles.setParticleTint(0xbff8ff);
          this.particles.explode(5, h.x, h.y - 14);
        }
        if (ev.hits.length) this.floatText(ev.source.pos.x, ev.source.pos.y - 34, 'Zap!', '#bff8ff', 15);
        break;
      }
      case 'molt': {
        sfx.trait('crack');
        this.particles.setParticleTint(0x9a8a7a);
        this.particles.explode(12, ev.enemy.pos.x, ev.enemy.pos.y - 8);
        this.floatText(ev.enemy.pos.x, ev.enemy.pos.y - 34, 'Molted!', '#ffb0a0', 15);
        this.enemyViews.get(ev.enemy.uid)?.sprite.setTint(0xffa8a0);
        break;
      }
      case 'cleanse': {
        sfx.trait('cleanse');
        const ring = this.add.circle(ev.source.pos.x, ev.source.pos.y - 6, ev.radius, 0x7ad8f0, 0.18).setStrokeStyle(3, 0xbff0ff, 0.9).setDepth(2400).setScale(0.15);
        this.tweens.add({ targets: ring, scale: 1, alpha: 0, duration: 500, onComplete: () => ring.destroy() });
        for (const o of ev.washed) {
          this.particles.setParticleTint(0xbff0ff);
          this.particles.explode(3, o.pos.x, o.pos.y - 10);
        }
        break;
      }
      case 'crack': {
        sfx.trait('crack');
        this.particles.setParticleTint(0xc87a4a);
        this.particles.explode(8, ev.enemy.pos.x, ev.enemy.pos.y - 8);
        this.floatText(ev.enemy.pos.x, ev.enemy.pos.y - 34, 'Crack!', '#f0b080', 14);
        break;
      }
      case 'mirage': {
        sfx.trait('mirage');
        const ring = this.add.circle(ev.enemy.pos.x, ev.enemy.pos.y - 8, 22, 0xfff4d8, 0.3).setDepth(2450);
        this.tweens.add({ targets: ring, scale: 2.2, alpha: 0, duration: 400, onComplete: () => ring.destroy() });
        this.floatText(ev.enemy.pos.x, ev.enemy.pos.y - 34, 'Mirage!', '#fff4d8', 15);
        break;
      }
      case 'pilfer': {
        if (ev.coins <= 0) break;
        sfx.trait('pilfer');
        this.floatText(ev.enemy.pos.x - 60, ev.enemy.pos.y - 40, `-${ev.coins} coins!`, '#ffd84a', 18);
        break;
      }
      case 'ground': {
        // a quick copper arc from the sheltered ally to the Copperhorn (throttled per Copperhorn)
        const now = this.time.now;
        if ((this.lastGulp.get(-ev.to.uid) ?? -1e9) + 250 > now) break;
        this.lastGulp.set(-ev.to.uid, now);
        const g = this.add.graphics().setDepth(2500);
        g.lineStyle(2, 0xffb86a, 0.9);
        g.lineBetween(ev.from.pos.x, ev.from.pos.y - 10, ev.to.pos.x, ev.to.pos.y - 14);
        this.tweens.add({ targets: g, alpha: 0, duration: 180, onComplete: () => g.destroy() });
        break;
      }
      case 'bolt': {
        sfx.trait('bolt');
        const g = this.add.graphics().setDepth(2600);
        const tx = ev.tower.pos.x;
        const ty = ev.tower.pos.y - 40;
        g.lineStyle(4, 0xfff07a, 1);
        g.beginPath();
        g.moveTo(tx + 10, -10);
        let y = -10;
        let x = tx + 10;
        while (y < ty) {
          y = Math.min(ty, y + 40);
          x = tx + Phaser.Math.Between(-18, 18);
          g.lineTo(x, y);
        }
        g.strokePath();
        g.lineStyle(2, 0xffffff, 1);
        g.strokePath();
        this.tweens.add({ targets: g, alpha: 0, duration: 260, onComplete: () => g.destroy() });
        this.particles.setParticleTint(0xfff07a);
        this.particles.explode(10, tx, ty + 20);
        this.floatText(tx, ty - 6, 'Struck!', '#fff07a', 15);
        break;
      }
      case 'feed': {
        sfx.trait('feed');
        this.particles.setParticleTint(0xc8b878);
        this.particles.explode(6, ev.from.x, ev.from.y - 6);
        // Several deaths at once can feed the same grub: one "Gulp!" per eater every 0.6s keeps the screen readable.
        const now = this.time.now;
        if ((this.lastGulp.get(ev.enemy.uid) ?? -1e9) + 600 <= now) {
          this.lastGulp.set(ev.enemy.uid, now);
          this.floatText(ev.enemy.pos.x, ev.enemy.pos.y - 36, 'Gulp!', '#e8d898', 15);
        }
        break;
      }
      case 'grow': {
        sfx.trait('grow');
        this.particles.setParticleTint(0x6a9a3a);
        this.particles.explode(10, ev.enemy.pos.x, ev.enemy.pos.y - 6);
        this.floatText(ev.enemy.pos.x, ev.enemy.pos.y - 34, 'Sprouted!', '#c8e88a', 15);
        break;
      }
      case 'echo': {
        sfx.trait('echo');
        const ring = this.add.circle(ev.enemy.pos.x, ev.enemy.pos.y - 8, 26, 0xd8e8ff, 0.35).setDepth(2450);
        this.tweens.add({ targets: ring, scale: 1.8, alpha: 0, duration: 450, onComplete: () => ring.destroy() });
        this.floatText(ev.enemy.pos.x, ev.enemy.pos.y - 34, 'Echo!', '#d8e8ff', 15);
        this.enemyViews.get(ev.enemy.uid)?.sprite.setAlpha(0.6);
        break;
      }
      case 'charge': {
        sfx.trait('charge');
        this.particles.setParticleTint(0xf0f4f8);
        this.particles.explode(6, ev.enemy.pos.x + 8, ev.enemy.pos.y - 12);
        break;
      }
      case 'thorns': {
        sfx.trait('thorns');
        // a few green thorn sparks on whoever just hit a thorny enemy
        if (Math.random() < 0.5) {
          this.particles.setParticleTint(0x7ac84a);
          this.particles.explode(3, ev.pos.x, ev.pos.y - 10);
        }
        break;
      }
      case 'shift': {
        sfx.trait('shift');
        // hide flips: a puff in the new colour (green scales vs red skin)
        this.particles.setParticleTint(ev.scales ? 0x7ad85a : 0xe8604a);
        this.particles.explode(6, ev.enemy.pos.x, ev.enemy.pos.y - 8);
        const v = this.enemyViews.get(ev.enemy.uid);
        if (v) {
          if (ev.scales) v.sprite.clearTint();
          else v.sprite.setTint(0xff9a8a);
        }
        break;
      }
      case 'revive': {
        sfx.trait('revive');
        // golden beam from the idol to the risen ally
        const beam = this.add.line(0, 0, ev.source.pos.x, ev.source.pos.y - 20, ev.enemy.pos.x, ev.enemy.pos.y - 10, 0xffd84a, 0.9).setOrigin(0, 0).setLineWidth(3).setDepth(2450);
        this.tweens.add({ targets: beam, alpha: 0, duration: 500, onComplete: () => beam.destroy() });
        const glow = this.add.circle(ev.enemy.pos.x, ev.enemy.pos.y - 8, 22, 0xffd84a, 0.45).setDepth(2450);
        this.tweens.add({ targets: glow, scale: 1.8, alpha: 0, duration: 500, onComplete: () => glow.destroy() });
        this.floatText(ev.enemy.pos.x, ev.enemy.pos.y - 34, 'Risen!', '#ffe08a', 15);
        this.enemyViews.get(ev.enemy.uid)?.sprite.setTint(0xffe8a0).setAlpha(0.85); // risen: pale gold, a little ghostly
        break;
      }
      case 'gust': {
        sfx.trait('gust');
        // a pale swirl around the Kitewing and wind streaks behind everything it shoved
        const ring = this.add.circle(ev.source.pos.x, ev.source.pos.y - 30, ev.radius, 0xffffff, 0.08).setStrokeStyle(2, 0xe8f4ff, 0.8).setDepth(2400).setScale(0.4);
        this.tweens.add({ targets: ring, scale: 1, alpha: 0, angle: 90, duration: 500, onComplete: () => ring.destroy() });
        for (const t of ev.targets) {
          const streak = this.add.line(0, 0, t.from.x, t.from.y - 8, t.enemy.pos.x, t.enemy.pos.y - 8, 0xffffff, 0.7).setOrigin(0, 0).setLineWidth(2).setDepth(2400);
          this.tweens.add({ targets: streak, alpha: 0, duration: 400, onComplete: () => streak.destroy() });
        }
        break;
      }
      case 'glare': {
        sfx.trait('glare');
        const flash = this.add.circle(ev.enemy.pos.x, ev.enemy.pos.y - 30, ev.radius, 0xffffff, 0.5).setDepth(2600).setScale(0.2);
        this.tweens.add({ targets: flash, scale: 1, alpha: 0, duration: 380, ease: 'Cubic.easeOut', onComplete: () => flash.destroy() });
        if (ev.towers.length) this.floatText(ev.enemy.pos.x, ev.enemy.pos.y - 50, 'Dazzled!', '#fff0b8', 16);
        break;
      }
      case 'blink': {
        sfx.trait('blink');
        this.particles.setParticleTint(0xbff4ff);
        this.particles.explode(8, ev.from.x, ev.from.y);
        this.particles.explode(8, ev.to.x, ev.to.y);
        const streak = this.add.line(0, 0, ev.from.x, ev.from.y, ev.to.x, ev.to.y, 0xbff4ff, 0.7).setOrigin(0).setLineWidth(3).setDepth(2400);
        this.tweens.add({ targets: streak, alpha: 0, duration: 300, onComplete: () => streak.destroy() });
        break;
      }
      case 'swoop':
        sfx.trait('swoop');
        if (ev.landed) {
          this.particles.setParticleTint(0xe8f4ff);
          this.particles.explode(8, ev.enemy.pos.x, ev.enemy.pos.y);
        }
        break;
      case 'enrage':
        sfx.trait('enrage');
        this.floatText(ev.enemy.pos.x, ev.enemy.pos.y - 30, 'Enraged!', TEXT.heart, 18);
        this.particles.setParticleTint(0xff5d4a);
        this.particles.explode(12, ev.enemy.pos.x, ev.enemy.pos.y);
        break;
      case 'burrow':
        sfx.trait('burrow');
        this.particles.setParticleTint(0x9a7a52);
        this.particles.explode(10, ev.enemy.pos.x, ev.enemy.pos.y);
        break;
      case 'chill': {
        const ring = this.add.circle(ev.source.pos.x, ev.source.pos.y, ev.radius, 0xbff4ff, 0.18).setStrokeStyle(4, 0xe8fbff, 0.95).setDepth(2400).setScale(0.2);
        this.tweens.add({ targets: ring, scale: 1, alpha: 0, duration: 500, onComplete: () => ring.destroy() });
        this.particles.setParticleTint(0xe8fbff);
        this.particles.explode(16, ev.source.pos.x, ev.source.pos.y);
        for (const t of ev.towers) this.floatText(t.pos.x, t.pos.y - 70, 'Frozen!', '#bff4ff', 16);
        if (ev.towers.length) sfx.shieldBreak();
        break;
      }
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
        sfx.trait('split');
        this.particles.setParticleTint(ev.parent.def.color);
        this.particles.explode(20, ev.parent.pos.x, ev.parent.pos.y);
        break;
      case 'soldierDown':
        this.particles.setParticleTint(0x9aa8b5);
        this.particles.explode(8, ev.soldier.pos.x, ev.soldier.pos.y);
        break;
      case 'chain': {
        const g = this.add.graphics().setDepth(2550);
        g.lineStyle(4, 0xffffff, 1);
        for (let k = 1; k < ev.points.length; k++) this.zigzag(g, ev.points[k - 1], ev.points[k]);
        g.lineStyle(8, ev.color, 0.45);
        for (let k = 1; k < ev.points.length; k++) this.zigzag(g, ev.points[k - 1], ev.points[k]);
        this.tweens.add({ targets: g, alpha: 0, duration: 220, onComplete: () => g.destroy() });
        sfx.zap();
        break;
      }
      case 'specialize':
        this.tally.specs++;
        this.floatText(ev.tower.pos.x, ev.tower.pos.y - 80, ev.tower.def.specs.find((x) => x.id === ev.tower.spec)!.name + '!', TEXT.gold, 22);
        this.particles.setParticleTint(C.gold);
        this.particles.explode(30, ev.tower.pos.x, ev.tower.pos.y - 30);
        this.handleEvent({ type: 'upgrade', tower: ev.tower });
        sfx.victory();
        break;
      case 'build':
      case 'upgrade': {
        const t = ev.tower;
        if (t.rally && ev.type === 'build') this.updateRallyFlag(t.uid, t.rally);
        this.towerViews[t.slot]?.destroy();
        const img = this.add.image(t.pos.x, t.pos.y - 34, t.spec ? `tower_${t.def.id}_${t.spec}` : `tower_${t.def.id}_${t.tier}`).setDepth(t.pos.y + 1);
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
    const mound = e.def.burrow ? this.add.image(e.pos.x, e.pos.y, 'mound').setVisible(false) : null;
    this.enemyViews.set(e.uid, { sprite, bar, bob: Math.random() * Math.PI * 2, shadow, mound, air: e.def.flying ? 1 : 0 });
  }

  private killView(uid: number, v: EnemyView): void {
    this.enemyViews.delete(uid);
    v.bar.destroy();
    v.shadow?.destroy();
    v.mound?.destroy();
    this.tweens.add({ targets: v.sprite, scale: 1.4, alpha: 0, duration: 180, onComplete: () => v.sprite.destroy() });
  }

  private syncViews(dt: number): void {
    // Cogjammer range: a faint dashed brass ring that turns as it rattles.
    if (!this.jamG) this.jamG = this.add.graphics().setDepth(5);
    this.jamG.clear();
    for (const e of this.sim.enemies) {
      if (!e.alive || !e.def.fortify) continue;
      // Barkwarden bark-song: a ring of falling leaf-brown dashes
      this.jamG.lineStyle(2, 0xc8864a, 0.5);
      const t0 = -this.sim.time * 0.6;
      for (let k = 0; k < 10; k++) {
        const a0 = t0 + (k / 10) * Math.PI * 2;
        this.jamG.beginPath();
        this.jamG.arc(e.pos.x, e.pos.y, e.def.fortify.radius, a0, a0 + 0.25);
        this.jamG.strokePath();
      }
    }
    for (const e of this.sim.enemies) {
      if (!e.alive || !e.def.dim) continue;
      // Dimlantern gloom: a soft dark disc with a violet rim
      this.jamG.fillStyle(0x10081e, 0.22);
      this.jamG.fillCircle(e.pos.x, e.pos.y, e.def.dim.radius);
      this.jamG.lineStyle(2, 0x8a6ad8, 0.4);
      this.jamG.strokeCircle(e.pos.x, e.pos.y, e.def.dim.radius);
    }
    for (const e of this.sim.enemies) {
      if (!e.alive || !e.def.jam) continue;
      const r = e.def.jam.radius;
      this.jamG.lineStyle(2, 0xd8a84a, 0.45);
      const turn = this.sim.time * 0.8;
      for (let k = 0; k < 12; k++) {
        const a0 = turn + (k / 12) * Math.PI * 2;
        this.jamG.beginPath();
        this.jamG.arc(e.pos.x, e.pos.y, r, a0, a0 + 0.3);
        this.jamG.strokePath();
      }
    }
    for (const e of this.sim.enemies) {
      const v = this.enemyViews.get(e.uid);
      if (!v) continue;
      v.bob += dt * (6 + (e.def.speed * e.speedMult) / 20) * (e.blockedBy ? 0.5 : 1);
      const prevX = v.sprite.x;
      const airborne = this.sim.airborne(e);
      v.air = Phaser.Math.Clamp(v.air + (airborne ? dt : -dt) * 3, 0, 1);
      const lift = v.air * (34 + Math.sin(v.bob * 0.7) * 5) + (1 - v.air) * Math.abs(Math.sin(v.bob)) * 4;
      v.sprite.setPosition(e.pos.x, e.pos.y - lift);
      const swell = 1 + e.fed * 0.08; // fed Gorgegrubs visibly bulk up
      if (airborne) v.sprite.setScale(swell, swell * (1 + Math.sin(v.bob * 3) * 0.08));
      else v.sprite.setScale(swell * (1 + Math.sin(v.bob * 2) * 0.04), swell * (1 - Math.sin(v.bob * 2) * 0.04));
      if (e.speedMult > 1) v.sprite.setTint(0xff9a8a);
      else if (e.hasteMult > 1) v.sprite.setTint(0xffc0e8);
      else if (e.hasteTime <= 0 && v.sprite.tintTopLeft === 0xffc0e8) v.sprite.clearTint();
      if (this.sim.regenerating(e) && Math.random() < dt * 5) {
        // Fleece knitting back: little green pluses drift up off it.
        const plus = this.add.text(e.pos.x + Phaser.Math.Between(-10, 10), e.pos.y - 18, '+', textStyle(16, '#8fe86a')).setOrigin(0.5).setDepth(2500);
        this.tweens.add({ targets: plus, y: plus.y - 22, alpha: 0, duration: 650, onComplete: () => plus.destroy() });
      }
      if (e.def.veil) {
        // Veiled: a faint shimmer until a tower is close enough to spot it.
        const veil = e.def.veil;
        const spotted = this.sim.towers.some((t) => t && !t.rally && Math.hypot(t.pos.x - e.pos.x, t.pos.y - e.pos.y) <= veil);
        v.sprite.setAlpha(spotted ? 1 : 0.32 + Math.sin(v.bob * 1.5) * 0.1);
      }
      v.shadow?.setPosition(e.pos.x, e.pos.y + 4).setDepth(e.pos.y - 1);
      if (v.mound) {
        v.mound.setVisible(e.underground).setPosition(e.pos.x, e.pos.y + 2).setDepth(e.pos.y);
        v.sprite.setVisible(!e.underground);
        if (e.underground) {
          v.bar.clear();
          continue;
        }
      }
      if (Math.abs(e.pos.x - prevX) > 0.01) v.sprite.setFlipX(e.pos.x < prevX);
      v.sprite.setDepth(v.air > 0.5 ? e.pos.y + 1000 : e.pos.y);
      v.bar.clear();
      if (e.def.boss) continue; // boss uses the big HUD bar
      if (e.hp < e.maxHp || e.shield > 0) {
        const w = Math.max(24, e.def.radius * 2.4);
        const x = e.pos.x - w / 2;
        const y = e.pos.y - e.def.radius - 14 - 34 * v.air;
        if (e.shield > 0) {
          v.bar.fillStyle(C.ink, 0.85);
          v.bar.fillRect(x - 1, y - 7, w + 2, 6);
          v.bar.fillStyle(0xe8d27a, 1);
          v.bar.fillRect(x, y - 6, w * (e.shield / Math.max(1, e.maxShield)), 4);
        }
        if (e.def.brittle && e.def.armor > 0) {
          // Brittle crust: a grey bar that wears down as hits land.
          v.bar.fillStyle(C.ink, 0.85);
          v.bar.fillRect(x - 1, y + 6, w + 2, 4);
          v.bar.fillStyle(0xc8c0b4, 1);
          v.bar.fillRect(x, y + 7, w * (e.armor / e.def.armor), 2);
        }
        v.bar.fillStyle(C.ink, 0.85);
        v.bar.fillRect(x - 1, y - 1, w + 2, 7);
        v.bar.fillStyle(e.hp / e.maxHp > 0.4 ? 0x7be35a : 0xff5d4a, 1);
        v.bar.fillRect(x, y, w * Math.max(0, e.hp / e.maxHp), 5);
        v.bar.setDepth(v.air > 0.5 ? e.pos.y + 1000.5 : e.pos.y + 0.5);
      }
    }
    this.syncSoldiers();
    this.syncStrikes();
    // Frozen towers turn icy.
    this.sim.towers.forEach((t, i) => {
      const v = this.towerViews[i];
      if (!t || !v) return;
      if (t.frozen > 0) v.setTint(0xbfe8ff);
      else if (v.isTinted) v.clearTint();
    });
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

  private syncStrikes(): void {
    for (const st of this.sim.strikes) {
      const def = SPELLS[st.spellId];
      let v = this.strikeViews.get(st.uid);
      if (!v) {
        const mark = this.add.circle(st.pos.x, st.pos.y, def.radius ?? 60, def.color, 0.15).setStrokeStyle(3, def.color, 0.9).setDepth(2300);
        this.tweens.add({ targets: mark, alpha: 0.4, yoyo: true, repeat: -1, duration: 150 });
        const star = this.add.image(st.pos.x + 260, -60, 'meteor').setDepth(4500).setScale(1.6);
        v = { star, mark };
        this.strikeViews.set(st.uid, v);
      }
      const t = 1 - Math.max(0, st.timer) / (def.delay ?? 1);
      const e = t * t; // ease-in fall
      v.star.setPosition(st.pos.x + 260 * (1 - e), -60 + (st.pos.y + 60) * e).setRotation(t * 6);
    }
  }

  private syncSoldiers(): void {
    const seen = new Set<number>();
    for (const s of this.sim.soldiers) {
      seen.add(s.uid);
      let v = this.soldierViews.get(s.uid);
      if (!v) {
        v = { sprite: this.add.image(s.pos.x, s.pos.y, s.summoned ? 'ranger' : 'soldier'), bar: this.add.graphics() };
        if (s.summoned) {
          v.sprite.setScale(0);
          this.tweens.add({ targets: v.sprite, scale: 1, duration: 250, ease: 'Back.easeOut' });
        }
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
    if (s.summoned && s.life < 3) sprite.setAlpha(0.5 + 0.5 * Math.abs(Math.sin(this.time.now / 120)));
    if (s.hp < s.maxHp) {
      const w = 22;
      bar.fillStyle(C.ink, 0.85);
      bar.fillRect(s.pos.x - w / 2 - 1, s.pos.y - 34, w + 2, 6);
      bar.fillStyle(0x7fc8ff, 1);
      bar.fillRect(s.pos.x - w / 2, s.pos.y - 33, w * (s.hp / s.maxHp), 4);
      bar.setDepth(s.pos.y + 0.5);
    }
  }

  private zigzag(g: Phaser.GameObjects.Graphics, a: Vec2, b: Vec2): void {
    const segs = 5;
    g.beginPath();
    g.moveTo(a.x, a.y - 10);
    for (let i = 1; i < segs; i++) {
      const t = i / segs;
      g.lineTo(a.x + (b.x - a.x) * t + Phaser.Math.Between(-8, 8), a.y + (b.y - a.y) * t - 10 + Phaser.Math.Between(-8, 8));
    }
    g.lineTo(b.x, b.y - 10);
    g.strokePath();
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
    music.setMood('calm');
    const stars = won ? starsForLives(this.sim.lives, this.sim.maxLives) : 0;
    let reward = { coins: 0, glowsap: 0 };
    let after = loadSave();
    let bloom = 0;
    if (this.endless) {
      // Endless: no stars; pay per wave held and remember the best run on this map.
      const held = wavesHeld(this.sim.waveIndex + (won ? 1 : 0));
      const key = LEVELS[this.levelIndex].id;
      const prev = after.endlessBest[key] ?? 0;
      after.endlessBest = { ...after.endlessBest, [key]: Math.max(prev, held) };
      const payMult = this.mutator ? mutatorReward(this.mutator) : 1;
      reward = addResources(ensureVillage(after), Math.round(ENDLESS.rewardPerWave.coins * held * payMult), Math.round(ENDLESS.rewardPerWave.glowsap * held * payMult));
      this.endlessResult = { held, best: Math.max(prev, held), isBest: held > prev };
      if (!music.stinger(held > prev ? 'victory' : 'defeat')) sfx.defeat();
    } else if (won) {
      const prevStars = after.stars[this.level.id] ?? 0;
      after = recordStars(after, this.level.id, stars);
      const want = battleReward(this.levelIndex, prevStars, stars);
      reward = addResources(ensureVillage(after), want.coins, want.glowsap);
      // First time taking this level to 3 stars: a free village speed-up.
      if (prevStars < 3 && stars === 3) bloom = grantSwiftbloom(ensureVillage(after));
      if (!music.stinger('victory')) sfx.victory();
    } else if (!music.stinger('defeat')) {
      sfx.defeat();
    }
    let dailyPaid: { coins: number; glowsap: number } | null = null;
    if (won && this.daily && after.dailyDone !== this.daily.date) {
      dailyPaid = addResources(ensureVillage(after), this.daily.reward.coins, this.daily.reward.glowsap);
      after.dailyDone = this.daily.date;
      after = bumpStats(after, { dailies: 1 });
    }
    // Lifetime stats + achievements (counted for losses too).
    const add: Record<string, number> = {
      kills: this.tally.kills,
      specs: this.tally.specs,
      wins: won ? 1 : 0,
      perfectWins: won && this.sim.lives === this.level.lives ? 1 : 0,
      soldierHealing: Math.round(this.sim.healTotal),
    };
    if (won && this.sim.hero) add[`wins_hero_${this.sim.hero.def.id}`] = 1;
    for (const b of this.tally.bosses) add[`boss_${b}`] = (add[`boss_${b}`] ?? 0) + 1;
    after = bumpStats(after, add, { heroMaxLevel: this.sim.hero?.level ?? 0 });
    const checked = checkAchievements(after);
    writeSave(checked.save);
    showAchievementToasts(this, checked.unlocked);

    const shade = this.add.rectangle(GAME_W / 2, GAME_H / 2, GAME_W, GAME_H, 0x000000, 0).setDepth(5000).setInteractive();
    this.tweens.add({ targets: shade, fillAlpha: 0.55, duration: 300 });
    const panel = this.add.container(GAME_W / 2, GAME_H / 2).setDepth(5001);
    const bg = this.add.graphics();
    bg.fillStyle(C.ink, 1);
    bg.fillRoundedRect(-280, -200, 560, 400, 28);
    bg.fillStyle(C.panel, 1);
    bg.fillRoundedRect(-270, -190, 540, 380, 22);
    panel.add(bg);
    const er = this.endlessResult;
    panel.add(this.add.text(0, -140, er ? 'Endless Run Over' : won ? 'Victory!' : 'The Gate Fell', textStyle(er ? 46 : 54, won || er?.isBest ? TEXT.gold : TEXT.heart)).setOrigin(0.5));
    if (er) {
      panel.add(this.add.text(0, -54, `${er.held}`, textStyle(64, TEXT.gold)).setOrigin(0.5).setName('endlessHeld'));
      panel.add(this.add.text(0, -6, er.held === 1 ? 'wave held' : 'waves held', textStyle(20)).setOrigin(0.5));
      panel.add(this.add.text(0, 24, er.isBest ? 'New best on this map!' : `Best on this map: ${er.best}`, textStyle(17, er.isBest ? '#9be86a' : TEXT.dim, false)).setOrigin(0.5));
      panel.add(this.add.text(0, 52, `Village reward: +${reward.coins} coins, +${reward.glowsap} glowsap`, textStyle(16, TEXT.gold, false)).setOrigin(0.5));
      if (this.mutator) panel.add(this.add.text(0, 76, `Mutator: ${this.mutator.name}`, textStyle(14, TEXT.dim, false)).setOrigin(0.5));
    }
    for (let i = 0; i < (er ? 0 : 3); i++) {
      const star = this.add.image(-90 + i * 90, -40, i < stars ? 'star' : 'star_empty').setScale(0);
      panel.add(star);
      this.tweens.add({ targets: star, scale: 1.4, delay: 400 + i * 250, duration: 300, ease: 'Back.easeOut' });
    }
    if (!er) panel.add(
      this.add
        .text(0, 14, won ? `Lives kept: ${this.sim.lives}/${this.sim.maxLives}` : `You held until wave ${this.sim.waveIndex + 1}`, textStyle(22))
        .setOrigin(0.5),
    );
    if (dailyPaid) {
      panel.add(this.add.text(0, 74, `Daily challenge bonus: +${dailyPaid.coins} coins, +${dailyPaid.glowsap} glowsap`, textStyle(16, '#9be86a', false)).setOrigin(0.5));
    }
    if (bloom) {
      const t = this.add.text(222, -40, '+1\nSwiftbloom', { ...textStyle(16, '#ffc0e8'), align: 'center' }).setOrigin(0.5).setName('bloomText').setScale(0);
      panel.add(t);
      this.tweens.add({ targets: t, scale: 1, delay: 1250, duration: 300, ease: 'Back.easeOut' });
    }
    if (won && !er) {
      const msg = reward.coins + reward.glowsap > 0 ? `Village reward: +${reward.coins} coins, +${reward.glowsap} glowsap` : 'Village storage is full!';
      panel.add(this.add.text(0, 46, msg, textStyle(17, TEXT.gold, false)).setOrigin(0.5));
    }
    const finale = won && !er && !!this.level.finale;
    const story = won && !er && !finale && !!STORY[this.level.id];
    const hasNext = won && !er && (this.levelIndex + 1 < LEVELS.length || finale || story);
    const retry = new Button(this, hasNext ? -170 : -120, 120, 'Retry', {
      width: hasNext ? 150 : 200,
      color: C.sky,
      onClick: () => this.scene.restart({ levelIndex: this.levelIndex, daily: !!this.daily, endless: this.endless }),
    });
    const map = new Button(this, hasNext ? 0 : 120, 120, 'Map', {
      width: hasNext ? 150 : 200,
      onClick: () => this.scene.start('WorldMap', { focus: this.levelIndex }),
    });
    panel.add([retry, map]);
    if (hasNext) {
      panel.add(
        new Button(this, 170, 120, finale ? 'Epilogue' : story ? 'Story' : 'Next', {
          width: 150,
          color: 0xff9f43,
          onClick: () =>
            finale ? this.scene.start('Ending') : story ? this.scene.start('Story', { levelId: this.level.id }) : this.scene.start('WorldMap', { focus: this.levelIndex + 1 }),
        }),
      );
    }
    panel.setScale(0.5).setAlpha(0);
    this.tweens.add({ targets: panel, scale: 1, alpha: 1, duration: 350, ease: 'Back.easeOut' });
  }
}
