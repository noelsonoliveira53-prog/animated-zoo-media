import { leafReveal } from '../ui/transition';
import Phaser from 'phaser';
import { groundSteps, stepColors } from '../systems/groundNoise';
import { motion, shake } from '../ui/motion';
import { cardRows, cardTags, type CardRow } from '../systems/towerCard';
import { heroCardRows, heroXpProgress } from '../systems/heroCard';
import { pickEnemy } from '../systems/enemyPick';
import { snapRally } from '../systems/rallySnap';
import { shouldShowTouchTip, TOUCH_TIPS } from '../systems/touchTip';
import { slowMoScale, SLOWMO_MS } from '../systems/slowMo';
import { waveClearInfo } from '../systems/waveClear';
import { waveChart } from '../systems/waveChart';
import { runSummary, shortNum } from '../systems/runSummary';
import { justVeteran, towerRecord } from '../systems/veteran';
import { hpColor, newTrail, resistPips, stepTrail, type TrailState } from '../systems/hpBar';
import { TowerFx } from './fx/TowerFx';
import { addLighting } from '../ui/lighting';
import { stepCounter, waveProgress } from '../ui/counter';
import { deathStyle, bigHit } from '../systems/deathStyle';
import { enemyKeyTrait } from '../systems/guideInfo';
import { gaitFor, poseFor, unitPose } from '../systems/gait';
import { damageTextStyle } from '../systems/damageText';
import { playDeath } from './fx/DeathFx';
import { groveBurst, starImpact, starTrail, thornGrowth } from './fx/SpellFx';
import { heroSignature, readyPing } from './fx/HeroFx';
import { buildPuff, upgradeBurst } from './fx/BuildFx';
import { bossIntro } from './fx/BossIntro';
import { ash, confetti, countUp, ribbon, starSlam, victoryRays } from './fx/ResultFx';
import { startWeather } from './fx/Weather';
import { ambienceFor, weatherFor } from '../data/weather';
import { distToSegment, roadEdgeSpots } from '../systems/path';
import { music } from '../systems/music';
import { themeForRegion } from '../data/musicThemes';
import { STORY } from '../data/story';
import { ENDLESS } from '../data/endless';
import { endlessMutatorFor, makeEndlessLevel, mutatorReward, wavesHeld } from '../systems/endless';
import { LEVELS } from '../data/levels';
import { ENEMIES } from '../data/enemies';
import { combine, DAILY_MODIFIERS } from '../data/daily';
import { dailyFor, dailyLevel, todayString, type DailyChallenge } from '../systems/daily';
import { isLevelUnlocked, regionOf } from '../data/levels';
import { TOWERS, TOWER_ORDER, sellValue } from '../data/towers';
import { HERO_MAX_LEVEL, HERO_XP } from '../data/heroes';
import { SPELLS, SPELL_ORDER } from '../data/spells';
import type { LevelDef, TargetMode, TowerTier, Vec2 } from '../data/types';
import { BattleSim, type Enemy, type SimEvent, type Soldier, type Tower } from '../systems/BattleSim';
import { glossPanel } from '../ui/panels';
import { drawBar } from '../ui/bars';
import { sfx } from '../systems/audio';
import { bumpStats, ensureVillage, loadSave, markSeen, recordStars, starsForLives, writeSave } from '../systems/save';
import { checkAchievements } from '../systems/achievements';
import { withStorePerks } from '../systems/store';
import { DEV_COINS, DEV_LIVES, devOn } from '../systems/dev';
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
  pulse: number; // brief scale bump (a Barkdrum thumping its drum), decays to 0
  squash: number; // brief squash after a big hit, decays to 0
  trail: TrailState; // pale "damage trail" behind the health fill
}

/** Light color for each tower's upgrade pillar. */
const TOWER_GLOW: Record<string, number> = { thornbow: 0xb8f07a, glimmer: 0xc8a0ff, boulder: 0xffc870, burrow: 0xe8d9b5 };

/** Touch aiming draws the aim circle this far above the finger so it stays visible. */
const TOUCH_AIM_LIFT = 60;
/** A touch on the hero that moves less than this is a tap (select), more is a drag (move there). */
const HERO_DRAG_MIN = 24;
/** How long the boss bar flashes white on a phase change. */
const BOSS_FLASH_MS = 450;

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
  private fx!: TowerFx;
  private towerShadows = new Map<number, Phaser.GameObjects.Ellipse>(); // soft ground shadow under each built tower // per-tower launch flashes, trails, impacts and tier auras
  private soldierViews = new Map<number, { sprite: Phaser.GameObjects.Image; bar: Phaser.GameObjects.Graphics; trail: TrailState }>();
  private heroTrail: TrailState = newTrail(1);
  private heroCard: Phaser.GameObjects.Container | null = null;
  private enemyCard: Phaser.GameObjects.Container | null = null;
  private enemyCardUid = 0;
  private heroCardUntil = 0; // scene time when a fallen hero's status card closes itself (0 = stays)
  private rallyFlags = new Map<number, Phaser.GameObjects.Image>();
  private pendingSpec: string | null = null; // "slot:index" awaiting a confirming tap
  private rallyMode: number | null = null; // slot whose rally point is being placed
  private spellMode: string | null = null; // spell waiting for a target tap
  private spellHud!: Phaser.GameObjects.Graphics;
  private strikeViews = new Map<number, { star: Phaser.GameObjects.Image; mark: Phaser.GameObjects.Arc; ring: Phaser.GameObjects.Arc }>();
  private reticle!: Phaser.GameObjects.Arc;
  private callG: Phaser.GameObjects.Graphics | null = null;
  private callStrip: Phaser.GameObjects.Graphics | null = null;
  private callChip: Phaser.GameObjects.Text | null = null;
  private callFull = 1; // the countdown's starting length, so the strip drains from full
  private callLast = 0;
  private skillPreview = false; // the pointer is over the hero's skill button
  private skillHold = false; // touch: the finger is holding the skill button
  private veteranBadges = new Map<number, Phaser.GameObjects.Container>(); // tower uid → gold star
  private heroDrag: Vec2 | null = null; // touch: where a drag from the hero started
  private heroDragTo: Vec2 | null = null;
  private heroDragG: Phaser.GameObjects.Graphics | null = null;
  private bossTrail: TrailState = newTrail(1);
  private bossTrailUid = 0;
  private bossFlashUntil = 0; // scene time until which the boss bar flashes after a phase change
  private slowMoStart = 0; // scene time a boss-kill slow-motion beat began (0 = none)
  private rallyDrag = false; // touch: dragging a rally flag
  private rallyFinger: Vec2 | null = null;
  private rallyG: Phaser.GameObjects.Graphics | null = null;
  private rallyGhost: Phaser.GameObjects.Image | null = null;
  private aimHold = false; // touch: the finger is aiming an armed spell
  private touchAimTap = false; // Settings → Touch aim: Tap to cast (no drag-and-lift)
  private aimG: Phaser.GameObjects.Graphics | null = null; // spell aim: glow, turning rim, marks on the foes it would hit
  private aimText: Phaser.GameObjects.Text | null = null;
  private towerViews: (Phaser.GameObjects.Image | null)[] = [];
  private slotViews: Phaser.GameObjects.Image[] = [];

  private coinText!: Phaser.GameObjects.Text;
  private titheText!: Phaser.GameObjects.Text; // shown while a Tithe Weasel skims the bounty
  private livesText!: Phaser.GameObjects.Text;
  private waveText!: Phaser.GameObjects.Text;
  private waveBar!: Phaser.GameObjects.Graphics;
  private shownCoins = -1;
  private shownLives = -1;
  private shownWave = -1;
  private hitStopUntil = 0;
  private heroPortrait: Phaser.GameObjects.Image | null = null;
  private skillWasReady = true;
  private lastHitStop = -9999;
  private nextWaveBtn!: Button;
  private speedBtn!: Button;
  private pauseBtn!: Button;

  private menu: Phaser.GameObjects.Container | null = null;
  private jamG: Phaser.GameObjects.Graphics | null = null;
  private rangeRing!: Phaser.GameObjects.Graphics;
  private rangeDash: Phaser.GameObjects.Graphics | null = null;
  private padGlows: Phaser.GameObjects.Ellipse[] = [];
  private cheapestTower = 0;
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
  private perks: BattlePerks = { towerDamageMult: 1, bonusCoins: 0, rangerMult: 1, spellCdMult: 1, heroHpMult: 1, weirBountyMult: 1 };
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
    this.level = this.endless ? makeEndlessLevel(LEVELS[this.levelIndex]) : this.daily ? dailyLevel(LEVELS[this.levelIndex]) : LEVELS[this.levelIndex];
    this.mutator = this.endless ? endlessMutatorFor(todayString()) : null;
    const save = loadSave();
    motion.reduced = !!save.settings.reduceMotion;
    motion.lowFx = !!save.settings.fxLow;
    this.perks = withStorePerks(battlePerks(save.village), save);
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
    this.veteranBadges.clear();
    this.bossTrailUid = 0;
    this.bossFlashUntil = 0;
    this.slowMoStart = 0;
    this.heroTrail = newTrail(1);
    this.rallyFlags.clear();
    this.rallyMode = null;
    this.spellMode = null;
    this.strikeViews.clear();
    this.towerViews = this.level.slots.map(() => null);
    this.towerShadows.clear();
    this.slotViews = [];
    this.menu = null;
    this.jamG = null;
  }

  create(): void {
    leafReveal(this, GAME_W, GAME_H); // a gust of leaves uncovers the scene
    music.setMood('battle');
    music.setTheme(themeForRegion(regionOf(this.levelIndex)));
    this.drawMap();
    this.drawLighting();
    this.rangeRing = this.add.graphics().setDepth(5);
    this.rangeDash = null;
    // empty pads glow softly while you can afford at least the cheapest tower
    this.padGlows = this.level.slots.map((p) => {
      const glow = this.add.ellipse(p.x, p.y + 4, 82, 32, 0xffe27a, 0.22).setDepth(p.y - 0.5).setBlendMode(Phaser.BlendModes.ADD).setVisible(false);
      if (!motion.reduced) this.tweens.add({ targets: glow, alpha: 0.06, scale: 1.08, duration: 900, yoyo: true, repeat: -1, ease: 'Sine.easeInOut', delay: Math.random() * 600 });
      return glow;
    });

    this.level.slots.forEach((s, i) => {
      const img = padHit(this.add.image(s.x, s.y, 'slot').setDepth(s.y).setInteractive({ useHandCursor: true }));
      img.on('pointerdown', (_p: Phaser.Input.Pointer, _x: number, _y: number, ev: Phaser.Types.Input.EventData) => {
        ev.stopPropagation();
        sfx.unlock();
        if (this.spellMode) {
          if (_p.wasTouch && !this.touchAimTap) this.beginTouchAim(_p);
          else this.castAt(this.spellMode, { x: _p.worldX, y: _p.worldY });
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
    this.fx = new TowerFx(this);

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
    // light weather per theme (leaves, spores, rain, sand...), purely visual
    if (!motion.lowFx && !motion.reduced) startWeather(this, weatherFor(this.level.theme), GAME_W, GAME_H);
    // a quiet ambience bed for the map (wind, rain, water, crackle or birdsong), stopped when the battle scene ends
    sfx.startAmbience(ambienceFor(this.level.theme));
    this.events.once('shutdown', () => sfx.stopAmbience());
    this.buildHud();
    this.buildHero();
    this.buildSpells();
    this.refreshWavePreview();

    this.input.on('pointerdown', (p: Phaser.Input.Pointer) => {
      if (this.rallyMode !== null) {
        if (p.wasTouch) {
          // touch: drag a ghost flag along the road, let go to plant it
          this.rallyDrag = true;
          this.rallyFinger = { x: p.worldX, y: p.worldY };
        } else this.placeRally(this.rallyMode, { x: p.worldX, y: p.worldY });
        return;
      }
      if (this.spellMode !== null) {
        if (p.wasTouch && !this.touchAimTap) this.beginTouchAim(p);
        else this.castAt(this.spellMode, { x: p.worldX, y: p.worldY });
        return;
      }
      if (this.heroSelected && !this.menu) {
        this.orderHeroMove({ x: p.worldX, y: p.worldY });
        return;
      }
      const hadMenu = !!this.menu;
      this.closeMenu();
      // a plain tap on the map: tapping a foe shows its card, tapping anywhere else closes it
      if (!hadMenu) this.openEnemyCard(pickEnemy(this.sim.enemies, p.worldX, p.worldY));
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
      if (this.heroDrag) this.heroDragTo = { x: p.worldX, y: p.worldY };
      if (this.rallyDrag) this.rallyFinger = { x: p.worldX, y: p.worldY };
      if (this.spellMode) this.reticle.setPosition(p.worldX, p.worldY - (this.aimHold ? TOUCH_AIM_LIFT : 0));
    });
    this.input.on('pointerup', (p: Phaser.Input.Pointer) => {
      if (this.heroDrag) {
        const from = this.heroDrag;
        this.heroDrag = null;
        this.heroDragTo = null;
        if (Math.hypot(p.worldX - from.x, p.worldY - from.y) > HERO_DRAG_MIN) this.orderHeroMove({ x: p.worldX, y: p.worldY });
        else this.selectHero(!this.heroSelected);
        return;
      }
      if (this.rallyDrag && this.rallyMode !== null) {
        this.rallyDrag = false;
    this.heroDrag = null;
    this.heroDragTo = null;
        this.rallyGhost?.setVisible(false);
        this.placeRally(this.rallyMode, { x: p.worldX, y: p.worldY - TOUCH_AIM_LIFT }, true);
        return;
      }
      // a touch skill-hold that slid off the button: cancel quietly
      if (this.skillHold) {
        this.skillHold = false;
        this.skillPreview = false;
    this.skillHold = false;
    this.aimHold = false;
    this.rallyDrag = false;
      }
      if (!this.aimHold || !this.spellMode) return;
      this.aimHold = false;
      if (p.worldY > GAME_H - 110) {
        // let go over the spell bar: keep the spell armed, cast nothing
        this.floatText(p.worldX, GAME_H - 140, 'Cancelled', TEXT.dim, 16);
        return;
      }
      this.castAt(this.spellMode, { x: this.reticle.x, y: this.reticle.y });
    });

    this.touchAimTap = loadSave().settings.touchAim === 'tap';
    this.cameras.main.fadeIn(300, 16, 38, 27);
    // first battle on a touch screen: a one-time card about the touch gestures
    if (shouldShowTouchTip(loadSave(), this.sys.game.device.input.touch) && !(window as unknown as { __noTouchTip?: boolean }).__noTouchTip) this.showTouchTip(); // __noTouchTip: test hook for the phone checks
    const bonus: string[] = [];
    if (this.perks.bonusCoins) bonus.push(`+${this.perks.bonusCoins} coins`);
    if (this.perks.towerDamageMult > 1) bonus.push(`+${Math.round((this.perks.towerDamageMult - 1) * 100)}% tower damage`);
    if (this.perks.rangerMult > 1) bonus.push(`Rangers +${Math.round((this.perks.rangerMult - 1) * 100)}%`);
    if (this.perks.heroHpMult > 1 && this.sim.hero) bonus.push(`hero +${Math.round((this.perks.heroHpMult - 1) * 100)}% health`);
    if (this.perks.weirBountyMult > 1) bonus.push(`kills pay +${Math.round((this.perks.weirBountyMult - 1) * 100)}%`);
    if (this.perks.spellCdMult < 1) bonus.push(`spells recharge ${Math.round((1 - this.perks.spellCdMult) * 100)}% faster`);
    if (this.sim.hero && this.sim.hero.level > 1) bonus.push(`${this.sim.hero.def.name} starts at Lv ${this.sim.hero.level}`);
    if (this.daily) {
      const names = this.daily.modifiers.map((id) => DAILY_MODIFIERS.find((m) => m.id === id)!.name);
      this.showBanner(`Daily: ${this.level.name}`, `Today's twists: ${names.join(' + ')}`);
    } else if (this.mutator) {
      const pay = mutatorReward(this.mutator);
      this.showBanner(`Endless: ${this.level.name}`, `Today's mutator: ${this.mutator.name} (${this.mutator.text})${pay > 1 ? ` • payout ×${pay}` : ''}`);
    } else {
      this.showBanner(this.level.name, bonus.length ? `Bonuses: ${bonus.join(' • ')}` : 'Build outposts on the stone pads, then call the first wave!');
    }
  }

  // ---------- map ----------

  /** Bake this level's ground once into a canvas texture under everything else (see systems/groundNoise). */
  private bakeGround(base: number, dark: number): void {
    const w = GAME_W + 120;
    const h = GAME_H + 120;
    const key = `ground_${this.level.id}`;
    if (!this.textures.exists(key)) {
      const tex = this.textures.createCanvas(key, w, h);
      if (!tex) return;
      const light = Phaser.Display.Color.ValueToColor(base).lighten(14).color;
      const cols = stepColors(base, dark, light, 4, 1.6).map((c) => [(c >> 16) & 255, (c >> 8) & 255, c & 255]);
      let seed = 7;
      for (const ch of this.level.id) seed = (seed * 31 + ch.charCodeAt(0)) | 0;
      const idx = groundSteps(w, h, seed, { scale: 220, cell: 8, relief: 1.4 });
      const ctx = tex.getContext();
      const img = ctx.createImageData(w, h);
      const px = img.data;
      for (let i = 0; i < idx.length; i++) {
        const c = cols[idx[i]];
        px[i * 4] = c[0];
        px[i * 4 + 1] = c[1];
        px[i * 4 + 2] = c[2];
        px[i * 4 + 3] = 255;
      }
      ctx.putImageData(img, 0, 0);
      tex.refresh();
    }
    this.add.image(-60, -60, key).setOrigin(0).setDepth(-11);
  }

  private drawMap(): void {
    const { theme } = this.level;
    const g = this.add.graphics().setDepth(-10);
    // the ground: a baked, low-contrast value-step field lit from the upper left (oversized so screen shake never shows edges)
    this.bakeGround(theme.grass, theme.grassDark);
    const rnd = new Phaser.Math.RandomDataGenerator([this.level.id]);
    const sunlit = Phaser.Display.Color.ValueToColor(theme.grass).lighten(9).color;
    for (let i = 0; i < 160; i++) {
      const x = rnd.between(0, GAME_W);
      const y = rnd.between(0, GAME_H);
      g.lineStyle(2, theme.grassDark, 0.9);
      g.lineBetween(x, y, x - 3, y - 7);
      g.lineBetween(x, y, x + 3, y - 8);
      // a lighter middle blade catching the sun
      g.lineStyle(1.5, sunlit, 0.9);
      g.lineBetween(x, y, x + 0.5, y - 9);
    }
    // the meadows (no special theme) get clover patches and the odd mossy stone
    const meadow = !Object.values(theme).some((v) => v === true);
    if (meadow) {
      for (let i = 0; i < 26; i++) {
        const cx = rnd.between(20, GAME_W - 20);
        const cy = rnd.between(90, GAME_H - 20);
        for (let k = 0; k < 5; k++) {
          const fx = cx + rnd.between(-12, 12);
          const fy = cy + rnd.between(-7, 7);
          g.fillStyle(0x3f8a34, 0.8);
          for (const [dx, dy] of [[-2, 0], [2, 0], [0, -2]]) g.fillCircle(fx + dx, fy + dy, 2.2);
          if (rnd.frac() < 0.35) {
            g.fillStyle(rnd.pick([0xffffff, 0xf8c8d8]), 1);
            g.fillCircle(fx, fy - 4, 2);
          }
        }
      }
      for (let i = 0; i < 6; i++) {
        const sx = rnd.between(40, GAME_W - 40);
        const sy = rnd.between(120, GAME_H - 40);
        g.fillStyle(0x000000, 0.15);
        g.fillEllipse(sx + 3, sy + 5, 26, 9);
        g.fillStyle(0x8a8e84, 1);
        g.fillEllipse(sx, sy, 22, 14);
        g.fillStyle(0x6a9a4a, 0.9);
        g.fillEllipse(sx - 3, sy - 4, 13, 6);
      }
    }
    // roads: edge then fill, with round joints
    // a soft drop shadow under every road first, so the roads sit slightly sunk into the ground
    for (const pts of this.level.paths) this.strokePath(g, pts.map((p) => ({ x: p.x + 3, y: p.y + 5 })), 72, 0x000000, 0.12);
    // Roads are drawn in passes over every path, so crossings merge cleanly. Light comes from the upper left:
    const shade = (c: number, n: number) => (n > 0 ? Phaser.Display.Color.ValueToColor(c).lighten(n).color : Phaser.Display.Color.ValueToColor(c).darken(-n).color);
    const shift = (pts: Vec2[], d: number) => pts.map((p) => ({ x: p.x + d, y: p.y + d }));
    // the lower-right bank catches the light: a pale rim just past the kerb on that side
    for (const pts of this.level.paths) this.strokePath(g, shift(pts, 2), 64, shade(theme.roadEdge, 18), 0.9);
    for (const pts of this.level.paths) this.strokePath(g, pts, 64, theme.roadEdge);
    // the road bed sits low: the upper-left bank throws a strip of shadow across its near edge
    for (const pts of this.level.paths) this.strokePath(g, pts, 52, shade(theme.road, -10));
    for (const pts of this.level.paths) this.strokePath(g, shift(pts, 3), 46, theme.road);
    for (const pts of this.level.paths) {
      // a paler stripe down the middle of the road, worn smooth by feet
      this.strokePath(g, shift(pts, 2), 24, shade(theme.road, 9), 0.4);
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
        g.fillStyle(0xffffff, 0.18);
        g.fillCircle(px - 1, py - 1, 1.5);
      }
    }
    if (theme.snow) this.drawFrostGround(rnd);
    if (theme.lava) this.drawEmberGround(rnd);
    if (theme.shrooms) this.drawDuskGround(rnd);
    if (theme.shoal) this.drawShoreGround(rnd);
    if (theme.crystals) this.drawCrystalGround(rnd);
    if (theme.gale) this.drawGaleGround(rnd);
    if (theme.ruins) this.drawRuinsGround(rnd);
    if (theme.gears) this.drawGearsGround(rnd);
    if (theme.abyss) this.drawAbyssGround(rnd);
    if (theme.orchard) this.drawOrchardGround(rnd);
    if (theme.storm) this.drawStormGround(rnd);
    if (theme.dunes) this.drawDuneGround(rnd);
    if (theme.reef) this.drawReefGround(rnd);
    if (theme.flotilla || theme.amber || theme.mist || theme.canopy || theme.comb || theme.bog) this.drawMoreGround(rnd);
    if (theme.thistle || theme.wold || theme.canyon || theme.brook || theme.heath) this.drawLastGround(rnd);
    // kerb stones along the road edges (skipped where another road runs through)
    const nearRoad = (x: number, y: number) =>
      this.level.paths.some((pts) => pts.some((p, k) => k > 0 && distToSegment({ x, y }, pts[k - 1], p) < 28));
    const stone = Phaser.Display.Color.ValueToColor(theme.roadEdge);
    const stoneTop = stone.clone().lighten(14).color;
    for (const pts of this.level.paths) {
      for (let k = 1; k < pts.length; k++) {
        const a = pts[k - 1];
        const b = pts[k];
        const len = Math.hypot(b.x - a.x, b.y - a.y);
        const nx = -(b.y - a.y) / len;
        const ny = (b.x - a.x) / len;
        for (let d = 14; d < len - 14; d += 30 + rnd.between(-6, 6)) {
          for (const side of [-1, 1]) {
            const x = a.x + ((b.x - a.x) * d) / len + nx * side * 31;
            const y = a.y + ((b.y - a.y) * d) / len + ny * side * 31;
            if (x < -10 || x > GAME_W + 10 || y < -10 || y > GAME_H + 10 || nearRoad(x, y)) continue;
            g.fillStyle(stone.color, 1);
            g.fillEllipse(x, y + 1, 9, 6);
            g.fillStyle(stoneTop, 1);
            g.fillEllipse(x - 1, y - 1, 6, 3.5);
          }
        }
      }
    }
    // grass tufts along the verges, leaning in over the kerb so the road sits in the ground, not on it
    // (grassy ground only: no tufts on snow, lava, crystal, clockwork or abyss floors)
    const tuftSun = shade(theme.grass, 12);
    const grassy = !(theme.snow || theme.lava || theme.crystals || theme.gears || theme.abyss);
    for (const pts of grassy ? this.level.paths : []) {
      for (const sp of roadEdgeSpots(pts, 46, 35, () => rnd.between(-14, 14))) {
        if (sp.x < -10 || sp.x > GAME_W + 10 || sp.y < -10 || sp.y > GAME_H + 10 || nearRoad(sp.x, sp.y) || rnd.frac() < 0.45) continue;
        // a little fan of curved blades; on a side verge the fan leans toward the road
        const n = rnd.between(3, 5);
        const lean = Math.abs(sp.nx) > 0.5 ? -Math.sign(sp.nx) * 0.4 : 0;
        for (let k = 0; k < n; k++) {
          const ang = -Math.PI / 2 + (k / (n - 1) - 0.5) * 1.3 + lean;
          const len = rnd.between(6, 10);
          const bx = sp.x + rnd.between(-2, 2);
          const by = sp.y + rnd.between(-1, 1) + (sp.ny > 0.5 ? 3 : 0);
          const curl = Math.cos(ang) >= 0 ? 0.3 : -0.3;
          g.lineStyle(k === 1 ? 1.5 : 2, k === 1 ? tuftSun : theme.grassDark, 0.9);
          g.beginPath();
          g.moveTo(bx, by);
          g.lineTo(bx + Math.cos(ang) * len * 0.5, by + Math.sin(ang) * len * 0.55);
          g.lineTo(bx + Math.cos(ang + curl) * len, by + Math.sin(ang + curl) * len);
          g.strokePath();
        }
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
      if (!lava && !abyss && !motion.reduced && !motion.lowFx) {
        // living water: a glint drifting across the surface and ripple rings spreading now and then
        const glint = this.add.ellipse(pd.x - pd.w * 0.15, pd.y - pd.h * 0.1, pd.w * 0.22, pd.h * 0.1, 0xffffff, 0.3).setDepth(-9);
        this.tweens.add({ targets: glint, x: pd.x + pd.w * 0.15, alpha: 0.12, duration: 2600, yoyo: true, repeat: -1, ease: 'Sine.easeInOut' });
        this.time.addEvent({
          delay: 1700 + rnd.between(0, 600),
          loop: true,
          callback: () => {
            const rx = pd.x + (Math.random() - 0.5) * pd.w * 0.6;
            const ry = pd.y + (Math.random() - 0.5) * pd.h * 0.5;
            const ring = this.add.ellipse(rx, ry, 10, 4, 0xffffff, 0).setStrokeStyle(1.5, 0xe8fbff, 0.7).setDepth(-9);
            this.tweens.add({ targets: ring, scaleX: 3.2, scaleY: 3.2, alpha: 0, duration: 1400, onComplete: () => ring.destroy() });
          },
        });
      }
      if (this.level.theme.dunes) this.drawOasis(pd);
    }
    if (this.level.theme.reef && !motion.reduced) {
      // sunlight caustics: a few soft pale blobs drifting slowly across the shallows
      for (let i = 0; i < 9; i++) {
        const blob = this.add.ellipse(rnd.between(0, GAME_W), rnd.between(100, GAME_H), rnd.between(60, 110), rnd.between(18, 30), 0xe8ffff, 0.1).setDepth(0.6);
        this.tweens.add({ targets: blob, x: blob.x + rnd.between(-60, 60), alpha: 0.2, duration: rnd.between(2400, 3600), yoyo: true, repeat: -1, ease: 'Sine.easeInOut' });
      }
    }
    if (this.level.theme.dunes && !motion.reduced) {
      // heat shimmer: a few pale horizontal bands slowly breathing in and out
      for (let i = 0; i < 4; i++) {
        const band = this.add.rectangle(GAME_W / 2, 140 + i * 150, GAME_W, 26, 0xfff4d8, 0.08).setDepth(0.6);
        this.tweens.add({ targets: band, alpha: 0.18, y: band.y - 8, duration: 1600 + i * 300, yoyo: true, repeat: -1, ease: 'Sine.easeInOut' });
      }
    }
    if (this.level.theme.heath && !motion.reduced) {
      // gusts of wind rolling across the heather: long soft bands sweeping by
      for (let i = 0; i < 5; i++) {
        const band = this.add.ellipse(rnd.between(-300, GAME_W), rnd.between(140, GAME_H - 120), rnd.between(300, 460), 26, 0xd8c8e8, 0.07).setDepth(0.6);
        this.tweens.add({ targets: band, x: GAME_W + 300, duration: rnd.between(9000, 14000) * (1 - band.x / (GAME_W + 600)), onComplete: () => {
          band.x = -300;
          this.tweens.add({ targets: band, x: GAME_W + 300, duration: rnd.between(9000, 14000), repeat: -1 });
        } });
      }
    }
    if (this.level.theme.brook && !motion.reduced) {
      // fallen leaves riding the current, and a couple of darting dragonflies
      for (let i = 0; i < 10; i++) {
        const leaf = this.add.ellipse(rnd.between(-40, GAME_W), rnd.between(120, GAME_H - 120), 9, 5, rnd.pick([0xd8a040, 0xc86a30, 0x9ab848]), 0.85).setDepth(0.7).setRotation(rnd.frac() * 3);
        const dur = rnd.between(16000, 26000);
        this.tweens.add({ targets: leaf, x: GAME_W + 40, rotation: leaf.rotation + 4, duration: dur * (1 - leaf.x / (GAME_W + 80)), onComplete: () => {
          leaf.x = -40;
          this.tweens.add({ targets: leaf, x: GAME_W + 40, rotation: leaf.rotation + 4, duration: dur, repeat: -1 });
        } });
        this.tweens.add({ targets: leaf, y: leaf.y + 10, duration: rnd.between(1800, 2600), yoyo: true, repeat: -1, ease: 'Sine.easeInOut' });
      }
      for (let i = 0; i < 2; i++) {
        const fly = this.add.ellipse(rnd.between(200, GAME_W - 200), rnd.between(180, GAME_H - 180), 10, 3, 0x4ac0e8, 0.9).setDepth(0.8);
        const hop = () => this.tweens.add({ targets: fly, x: Phaser.Math.Clamp(fly.x + rnd.between(-160, 160), 80, GAME_W - 80), y: Phaser.Math.Clamp(fly.y + rnd.between(-90, 90), 140, GAME_H - 120), duration: 500, delay: rnd.between(600, 1800), ease: 'Quad.easeOut', onComplete: hop });
        hop();
      }
    }
    if (this.level.theme.canyon && !motion.reduced) {
      // vulture shadows wheeling slowly over the canyon floor
      for (let i = 0; i < 3; i++) {
        const cx0 = rnd.between(250, GAME_W - 250);
        const cy0 = rnd.between(220, GAME_H - 220);
        const r0 = rnd.between(90, 160);
        const sh = this.add.ellipse(cx0 + r0, cy0, 34, 12, 0x2a1408, 0.16).setDepth(0.6);
        const o = { a: rnd.frac() * Math.PI * 2 };
        this.tweens.add({ targets: o, a: o.a + Math.PI * 2, duration: rnd.between(14000, 20000), repeat: -1, onUpdate: () => sh.setPosition(cx0 + Math.cos(o.a) * r0, cy0 + Math.sin(o.a) * r0 * 0.6).setRotation(o.a + Math.PI / 2) });
      }
    }
    if (this.level.theme.wold && !motion.reduced) {
      // big soft cloud shadows sliding slowly across the fields
      for (let i = 0; i < 4; i++) {
        const sh = this.add.ellipse(rnd.between(-200, GAME_W), rnd.between(150, GAME_H - 150), rnd.between(260, 380), rnd.between(120, 180), 0x1a3a10, 0.1).setDepth(0.6);
        this.tweens.add({ targets: sh, x: sh.x + GAME_W + 400, duration: rnd.between(40000, 60000), repeat: -1, onRepeat: () => (sh.x = -300) });
      }
    }
    if (this.level.theme.thistle && !motion.reduced) {
      // thistledown fluff drifting across the prairie on the wind
      for (let i = 0; i < 16; i++) {
        const y = rnd.between(120, GAME_H - 140);
        const fluff = this.add.circle(rnd.between(-40, GAME_W), y, rnd.between(2, 3), 0xffffff, 0.75).setDepth(0.7);
        const dur = rnd.between(7000, 12000);
        this.tweens.add({ targets: fluff, x: GAME_W + 40, duration: dur * (1 - fluff.x / (GAME_W + 80)), onComplete: () => {
          fluff.x = -40;
          this.tweens.add({ targets: fluff, x: GAME_W + 40, duration: dur, repeat: -1 });
        } });
        this.tweens.add({ targets: fluff, y: y - rnd.between(10, 30), duration: rnd.between(1400, 2600), yoyo: true, repeat: -1, ease: 'Sine.easeInOut' });
      }
    }
    if (this.level.theme.bog) {
      // night over the bog: a soft dark wash, with fireflies blinking in and out
      this.add.rectangle(GAME_W / 2, GAME_H / 2, GAME_W, GAME_H, 0x0a1a2a, 0.22).setDepth(0.55);
      if (!motion.reduced) {
        for (let i = 0; i < 18; i++) {
          const fly = this.add.circle(rnd.between(60, GAME_W - 60), rnd.between(120, GAME_H - 130), 2.4, 0xe8ff8a, 0).setDepth(0.7);
          this.tweens.add({ targets: fly, alpha: 0.95, duration: rnd.between(500, 1100), yoyo: true, repeat: -1, delay: rnd.between(0, 3000), hold: rnd.between(100, 600), repeatDelay: rnd.between(800, 2600) });
          this.tweens.add({ targets: fly, x: fly.x + rnd.between(-40, 40), y: fly.y + rnd.between(-30, 30), duration: rnd.between(2600, 4800), yoyo: true, repeat: -1, ease: 'Sine.easeInOut' });
        }
      }
    }
    if (this.level.theme.comb && !motion.reduced) {
      // honeybees drifting lazily over the hills in slow figure-eights
      for (let i = 0; i < 10; i++) {
        const bee = this.add.ellipse(rnd.between(80, GAME_W - 80), rnd.between(130, GAME_H - 140), 6, 4, 0xffd040, 0.85).setDepth(0.7);
        this.tweens.add({ targets: bee, x: bee.x + rnd.between(-60, 60), duration: rnd.between(1800, 3200), yoyo: true, repeat: -1, ease: 'Sine.easeInOut' });
        this.tweens.add({ targets: bee, y: bee.y + rnd.between(-24, 24), duration: rnd.between(900, 1500), yoyo: true, repeat: -1, ease: 'Sine.easeInOut' });
      }
    }
    if (this.level.theme.canopy && !motion.reduced) {
      // slanting sunbeams through the canopy, breathing slowly
      for (let i = 0; i < 4; i++) {
        const beam = this.add.rectangle(rnd.between(150, GAME_W - 150), GAME_H / 2, 70, GAME_H * 1.4, 0xfff4c8, 0.06).setAngle(18).setDepth(0.6);
        this.tweens.add({ targets: beam, alpha: 0.13, duration: rnd.between(2600, 4200), yoyo: true, repeat: -1, ease: 'Sine.easeInOut' });
      }
    }
    if (this.level.theme.mist && !motion.reduced) {
      // low banks of hill fog drifting slowly across the terraces
      for (let i = 0; i < 6; i++) {
        const bank = this.add.ellipse(rnd.between(0, GAME_W), rnd.between(120, GAME_H - 60), rnd.between(220, 360), rnd.between(40, 70), 0xffffff, 0.13).setDepth(0.6);
        this.tweens.add({ targets: bank, x: bank.x + rnd.between(80, 160), alpha: 0.22, duration: rnd.between(5000, 8000), yoyo: true, repeat: -1, ease: 'Sine.easeInOut' });
      }
    }
    if (this.level.theme.amber && !motion.reduced) {
      // leaves forever drifting down through the Amberwood, swaying as they fall, then starting again at the top
      for (let i = 0; i < 18; i++) {
        const leaf = this.add.ellipse(rnd.between(0, GAME_W), rnd.between(-40, GAME_H), 9, 5, rnd.pick(theme.trees ?? [0xe87a1a]), 0.85).setDepth(0.6);
        leaf.setAngle(rnd.between(0, 180));
        const fall = rnd.between(9000, 15000);
        this.tweens.add({ targets: leaf, y: GAME_H + 30, duration: fall * ((GAME_H + 30 - leaf.y) / (GAME_H + 70)), onComplete: () => {
          leaf.y = -40;
          this.tweens.add({ targets: leaf, y: GAME_H + 30, duration: fall, repeat: -1 });
        } });
        this.tweens.add({ targets: leaf, x: leaf.x + rnd.between(30, 60), angle: leaf.angle + 160, duration: rnd.between(1400, 2200), yoyo: true, repeat: -1, ease: 'Sine.easeInOut' });
      }
    }
    if (this.level.theme.storm && !motion.reduced) {
      // light slanting rain over the steppe: a 120px-periodic pattern scrolled down and wrapped
      const rain = this.add.graphics().setDepth(0.6).setAlpha(0.22);
      rain.lineStyle(1.5, 0xdce4f0, 1);
      for (let y = -120; y < GAME_H + 120; y += 30)
        for (let x = (y / 30) % 2 ? 0 : 22; x < GAME_W + 40; x += 44) rain.lineBetween(x, y, x - 7, y + 14);
      this.tweens.add({ targets: rain, y: 120, duration: 900, repeat: -1 });
    }
    if (this.level.theme.gale && !motion.reduced) {
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
      const p = { x: rnd.between(20, GAME_W - 20), y: rnd.between(115, GAME_H - 10) }; // tall trees start low enough to stay clear of the top bar
      if (this.sim.paths.some((path) => path.distanceTo(p) < 60)) continue;
      // keep clutter out from under the hero portrait and the spell buttons
      if (p.y > 600 && (p.x < 230 || p.x > 980)) continue;
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
      } else if (this.level.theme.flotilla) {
        const k = rnd.frac();
        if (k < 0.35) {
          // a floating barrel with iron hoops
          deco.fillStyle(0x000000, 0.18);
          deco.fillEllipse(p.x, p.y + 6, 26, 8);
          deco.fillStyle(rnd.pick(this.level.theme.trees ?? [0x8a6a4a]), 1);
          deco.fillRoundedRect(p.x - 10, p.y - 14, 20, 22, 6);
          deco.lineStyle(2, 0x3a3a42, 1);
          deco.lineBetween(p.x - 10, p.y - 8, p.x + 10, p.y - 8);
          deco.lineBetween(p.x - 10, p.y + 2, p.x + 10, p.y + 2);
          deco.lineStyle(1.5, C.ink, 0.5);
          deco.strokeRoundedRect(p.x - 10, p.y - 14, 20, 22, 6);
        } else if (k < 0.6) {
          // a drifting crate
          deco.fillStyle(0xa8885a, 1);
          deco.fillRect(p.x - 11, p.y - 11, 22, 22);
          deco.lineStyle(2, 0x6a4a2a, 1);
          deco.strokeRect(p.x - 11, p.y - 11, 22, 22);
          deco.lineBetween(p.x - 11, p.y - 11, p.x + 11, p.y + 11);
        } else if (k < 0.75) {
          // a red-and-white buoy
          deco.fillStyle(0xe8e0d0, 1);
          deco.fillCircle(p.x, p.y, 9);
          deco.fillStyle(0xc83a3a, 1);
          deco.fillRect(p.x - 9, p.y - 3, 18, 6);
          deco.lineStyle(1.5, C.ink, 0.6);
          deco.strokeCircle(p.x, p.y, 9);
        } else {
          // whitecaps
          deco.lineStyle(2, 0xbfe0f0, 0.6);
          for (let w = 0; w < 2; w++) {
            deco.beginPath();
            deco.arc(p.x + w * 14, p.y + w * 4, 9, Math.PI * 1.1, Math.PI * 1.9);
            deco.strokePath();
          }
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
      } else if (this.level.theme.heath) {
        const k = rnd.frac();
        if (k < 0.5) {
          // a clump of purple heather
          deco.fillStyle(0x5a5a3a, 1);
          deco.fillEllipse(p.x, p.y + 4, 24, 10);
          deco.fillStyle(0x9a6aa8, 1);
          for (let h = 0; h < 9; h++) deco.fillCircle(p.x - 10 + (h % 5) * 5, p.y - 2 - Math.floor(h / 5) * 5 + rnd.between(-1, 1), 2.6);
        } else if (k < 0.75) {
          // a leaning standing stone with a lichen patch
          deco.fillStyle(0x000000, 0.15);
          deco.fillEllipse(p.x + 5, p.y + 12, 24, 7);
          deco.fillStyle(0x8a8a88, 1);
          deco.fillTriangle(p.x - 7, p.y + 10, p.x + 7, p.y + 10, p.x + 3, p.y - 22);
          deco.fillRect(p.x - 7, p.y - 6, 12, 16);
          deco.fillStyle(0xc8c060, 0.8);
          deco.fillCircle(p.x - 1, p.y - 2, 3);
        } else {
          // a yellow-flowered gorse bush
          deco.fillStyle(0x4a5a2a, 1);
          for (const [dx, dy] of [[-6, 0], [6, 1], [0, -5]]) deco.fillCircle(p.x + dx, p.y + dy, 7);
          deco.fillStyle(0xf0c830, 1);
          for (let h = 0; h < 7; h++) deco.fillCircle(p.x - 9 + h * 3, p.y - 3 + (h % 3) * 3, 1.6);
        }
      } else if (this.level.theme.brook) {
        const k = rnd.frac();
        if (k < 0.4) {
          // a clump of reeds with brown cattail heads
          deco.lineStyle(2, 0x3a7a3a, 1);
          for (let r = -2; r <= 2; r++) deco.lineBetween(p.x + r * 3, p.y + 8, p.x + r * 5, p.y - 14 - Math.abs(r) * -2);
          deco.fillStyle(0x7a4a22, 1);
          deco.fillEllipse(p.x - 5, p.y - 14, 4, 9);
          deco.fillEllipse(p.x + 5, p.y - 12, 4, 9);
        } else if (k < 0.75) {
          // mossy river stones
          deco.fillStyle(0x000000, 0.15);
          deco.fillEllipse(p.x + 3, p.y + 8, 30, 8);
          deco.fillStyle(0x8a9090, 1);
          deco.fillEllipse(p.x - 5, p.y + 2, 18, 12);
          deco.fillEllipse(p.x + 8, p.y + 4, 13, 9);
          deco.fillStyle(0x6a9a4a, 1);
          deco.fillEllipse(p.x - 7, p.y - 2, 10, 4);
        } else {
          // a curled fern
          deco.lineStyle(2, 0x4a8a3a, 1);
          for (const a of [-0.9, -0.3, 0.3, 0.9]) deco.lineBetween(p.x, p.y + 6, p.x + Math.sin(a) * 14, p.y - Math.cos(a) * 12);
          deco.fillStyle(0x5a9a4a, 1);
          for (const a of [-0.9, -0.3, 0.3, 0.9]) deco.fillCircle(p.x + Math.sin(a) * 14, p.y - Math.cos(a) * 12, 3);
        }
      } else if (this.level.theme.canyon) {
        const k = rnd.frac();
        if (k < 0.4) {
          // a tall saguaro-ish cactus with two arms
          deco.fillStyle(0x000000, 0.15);
          deco.fillEllipse(p.x + 4, p.y + 12, 26, 8);
          deco.fillStyle(0x5a8a3a, 1);
          deco.fillRoundedRect(p.x - 4, p.y - 20, 9, 32, 4);
          deco.fillRoundedRect(p.x - 13, p.y - 8, 6, 12, 3);
          deco.fillRoundedRect(p.x - 13, p.y - 2, 10, 5, 2);
          deco.fillRoundedRect(p.x + 8, p.y - 14, 6, 12, 3);
          deco.fillRoundedRect(p.x + 4, p.y - 6, 10, 5, 2);
          deco.fillStyle(0xf0d070, 1);
          deco.fillCircle(p.x + 1, p.y - 21, 2.5);
        } else if (k < 0.75) {
          // a stack of balanced red rocks
          deco.fillStyle(0x000000, 0.15);
          deco.fillEllipse(p.x + 3, p.y + 10, 30, 9);
          deco.fillStyle(0xa85a3a, 1);
          deco.fillEllipse(p.x, p.y + 4, 26, 14);
          deco.fillStyle(0xb86a42, 1);
          deco.fillEllipse(p.x + 2, p.y - 6, 18, 11);
          deco.fillStyle(0xc87a4a, 1);
          deco.fillEllipse(p.x - 1, p.y - 14, 11, 8);
        } else {
          // a scrubby desert bush with tiny flowers
          deco.fillStyle(0x8a8a4a, 1);
          for (const [dx, dy] of [[-6, 0], [6, 1], [0, -5]]) deco.fillCircle(p.x + dx, p.y + dy, 6);
          deco.fillStyle(0xf08aa8, 1);
          deco.fillCircle(p.x - 4, p.y - 6, 1.8);
          deco.fillCircle(p.x + 5, p.y - 3, 1.8);
        }
      } else if (this.level.theme.wold) {
        const k = rnd.frac();
        if (k < 0.35) {
          // a round hay bale with a tied band
          deco.fillStyle(0x000000, 0.15);
          deco.fillEllipse(p.x + 3, p.y + 10, 34, 12);
          deco.fillStyle(0xd8b050, 1);
          deco.fillCircle(p.x, p.y, 13);
          deco.lineStyle(2, 0xa88030, 1);
          deco.strokeCircle(p.x, p.y, 13);
          deco.strokeCircle(p.x, p.y, 7);
          deco.lineStyle(2, 0x8a4a2a, 1);
          deco.lineBetween(p.x - 13, p.y, p.x + 13, p.y);
        } else if (k < 0.7) {
          // a little strip of ripe wheat rows
          deco.fillStyle(0xc8a040, 1);
          for (let n = 0; n < 4; n++) deco.fillRect(p.x - 20 + n * 10, p.y - 8, 5, 18);
          deco.fillStyle(0xe8c860, 1);
          for (let n = 0; n < 4; n++) deco.fillEllipse(p.x - 17.5 + n * 10, p.y - 10, 6, 7);
        } else {
          // a scarecrow: a pole, a straw hat and outstretched sleeves
          deco.lineStyle(3, 0x6a4a2a, 1);
          deco.lineBetween(p.x, p.y + 14, p.x, p.y - 12);
          deco.lineBetween(p.x - 14, p.y - 4, p.x + 14, p.y - 4);
          deco.fillStyle(0x6a8ac8, 1);
          deco.fillRect(p.x - 6, p.y - 8, 12, 12);
          deco.fillStyle(0xe8d0a0, 1);
          deco.fillCircle(p.x, p.y - 13, 5);
          deco.fillStyle(0xd8b050, 1);
          deco.fillEllipse(p.x, p.y - 17, 18, 5);
        }
      } else if (this.level.theme.thistle) {
        const k = rnd.frac();
        if (k < 0.45) {
          // a clump of thistles: spiky green leaves under round purple flower heads
          deco.fillStyle(0x5a7a3a, 1);
          for (const dx of [-8, 0, 8]) deco.fillTriangle(p.x + dx - 5, p.y + 8, p.x + dx + 5, p.y + 8, p.x + dx, p.y - 8);
          deco.fillStyle(rnd.pick([0x9a6ab8, 0xb88ad0]), 1);
          for (const [dx, dy] of [[-6, -10], [5, -13], [0, -4]]) deco.fillCircle(p.x + dx, p.y + dy, 4.5);
          deco.fillStyle(0xffffff, 0.5);
          deco.fillCircle(p.x - 7, p.y - 12, 1.5);
        } else if (k < 0.75) {
          // a dry tumbleweed resting in the grass
          deco.lineStyle(1.5, 0xa88a50, 1);
          deco.strokeCircle(p.x, p.y, 9);
          deco.lineBetween(p.x - 9, p.y, p.x + 9, p.y);
          deco.lineBetween(p.x, p.y - 9, p.x, p.y + 9);
          deco.lineBetween(p.x - 6, p.y - 6, p.x + 6, p.y + 6);
          deco.lineBetween(p.x - 6, p.y + 6, p.x + 6, p.y - 6);
        } else {
          // a tuft of tall, pale prairie grass
          deco.lineStyle(2, 0xc8c878, 1);
          for (const dx of [-6, -2, 2, 6]) deco.lineBetween(p.x + dx, p.y + 8, p.x + dx * 1.8, p.y - 14);
        }
      } else if (this.level.theme.bog) {
        const k = rnd.frac();
        if (k < 0.45) {
          // a lily pad on a dark pool, maybe with a pale flower
          deco.fillStyle(0x1a3a3a, 0.8);
          deco.fillEllipse(p.x, p.y + 4, 54, 26);
          deco.fillStyle(0x4a9a5a, 1);
          deco.slice(p.x - 6, p.y + 2, 13, Phaser.Math.DegToRad(20), Phaser.Math.DegToRad(340), false);
          deco.fillPath();
          deco.fillStyle(0x3a8a4a, 1);
          deco.fillCircle(p.x + 12, p.y + 8, 7);
          if (rnd.frac() < 0.5) {
            deco.fillStyle(0xf4e8f0, 1);
            for (let n = 0; n < 5; n++) deco.fillEllipse(p.x - 6 + Math.cos(n * 1.26) * 4, p.y + Math.sin(n * 1.26) * 3, 6, 4);
            deco.fillStyle(0xffe06a, 1);
            deco.fillCircle(p.x - 6, p.y, 2);
          }
        } else if (k < 0.8) {
          // a clump of cattails
          deco.lineStyle(2, 0x4a6a3a, 1);
          for (const dx of [-6, 0, 6]) deco.lineBetween(p.x + dx, p.y + 10, p.x + dx * 1.4, p.y - 18);
          deco.fillStyle(0x6a4a2a, 1);
          for (const dx of [-6, 0, 6]) deco.fillEllipse(p.x + dx * 1.35, p.y - 14, 5, 12);
        } else {
          // a mossy, half-sunk stump with a glowing mushroom
          deco.fillStyle(0x4a3a2a, 1);
          deco.fillEllipse(p.x, p.y, 26, 14);
          deco.fillStyle(0x5a8a4a, 1);
          deco.fillEllipse(p.x - 3, p.y - 3, 18, 8);
          deco.fillStyle(0x9affd8, 0.9);
          deco.fillCircle(p.x + 10, p.y - 6, 3.5);
        }
      } else if (this.level.theme.comb) {
        const k = rnd.frac();
        if (k < 0.45) {
          // a patch of honeycomb cells half-sunk in the grass
          deco.fillStyle(0x000000, 0.12);
          deco.fillEllipse(p.x + 3, p.y + 10, 46, 16);
          for (const [dx, dy] of [[0, 0], [14, 0], [-14, 0], [7, -12], [-7, -12], [7, 12]]) {
            const cx = p.x + dx;
            const cy = p.y + dy;
            const pts = [0, 1, 2, 3, 4, 5].map((n) => new Phaser.Math.Vector2(cx + Math.cos((n * Math.PI) / 3 + Math.PI / 6) * 8, cy + Math.sin((n * Math.PI) / 3 + Math.PI / 6) * 8));
            deco.fillStyle(rnd.frac() < 0.5 ? 0xe8b030 : 0xd89a20, 1);
            deco.fillPoints(pts, true);
            deco.lineStyle(1.5, 0x9a6a20, 0.9);
            deco.strokePoints(pts, true);
          }
        } else if (k < 0.8) {
          // a clump of clover with white-pink flower heads
          deco.fillStyle(0x6a8a2a, 1);
          for (const [dx, dy] of [[-8, 2], [6, 4], [0, -6]]) deco.fillCircle(p.x + dx, p.y + dy, 7);
          deco.fillStyle(0xf4d8e8, 1);
          deco.fillCircle(p.x - 6, p.y - 8, 5);
          deco.fillCircle(p.x + 7, p.y - 4, 4);
        } else {
          // a dripping wild hive hung from a little bent sapling
          deco.lineStyle(2.5, 0x6a4a2a, 1);
          deco.lineBetween(p.x - 10, p.y + 12, p.x - 4, p.y - 24);
          deco.lineBetween(p.x - 4, p.y - 24, p.x + 10, p.y - 22);
          deco.fillStyle(0xe8c060, 1);
          deco.fillEllipse(p.x + 8, p.y - 10, 16, 20);
          deco.lineStyle(1.5, 0x9a7030, 1);
          deco.strokeEllipse(p.x + 8, p.y - 10, 16, 20);
          deco.fillStyle(0xd89a20, 1);
          deco.fillCircle(p.x + 9, p.y + 2, 2.5);
        }
      } else if (this.level.theme.canopy) {
        const k = rnd.frac();
        if (k < 0.55) {
          // a great clump of treetop leaves seen from above
          const col = rnd.pick(this.level.theme.trees ?? [0x3f8a3a]);
          deco.fillStyle(0x000000, 0.18);
          deco.fillEllipse(p.x + 4, p.y + 8, 56, 22);
          deco.fillStyle(col, 1);
          for (const [dx, dy, r] of [[-14, 0, 14], [12, -2, 15], [0, -12, 14], [2, 8, 12]]) deco.fillCircle(p.x + dx, p.y + dy, r);
          deco.fillStyle(0xffffff, 0.12);
          deco.fillCircle(p.x - 4, p.y - 14, 7);
        } else if (k < 0.8) {
          // a twiggy nest with speckled eggs
          deco.fillStyle(0x7a5a3a, 1);
          deco.fillEllipse(p.x, p.y, 30, 14);
          deco.lineStyle(1.5, 0x4a3420, 0.8);
          deco.strokeEllipse(p.x, p.y, 30, 14);
          deco.fillStyle(0xd8e8f0, 1);
          deco.fillEllipse(p.x - 5, p.y - 2, 7, 9);
          deco.fillEllipse(p.x + 4, p.y - 2, 7, 9);
        } else {
          // a hanging vine with leaves
          deco.lineStyle(2, 0x3a6a2a, 1);
          deco.lineBetween(p.x, p.y - 26, p.x + 3, p.y + 10);
          deco.fillStyle(0x5aa04a, 1);
          for (let n = 0; n < 4; n++) deco.fillEllipse(p.x + (n % 2 ? 6 : -4), p.y - 20 + n * 9, 8, 5);
        }
      } else if (this.level.theme.mist) {
        const k = rnd.frac();
        if (k < 0.5) {
          // a row of clipped tea bushes on its terrace
          deco.fillStyle(0x000000, 0.15);
          deco.fillEllipse(p.x, p.y + 6, 52, 10);
          for (let n = 0; n < 3; n++) {
            deco.fillStyle(0x3f6e45, 1);
            deco.fillEllipse(p.x - 16 + n * 16, p.y, 18, 14);
            deco.fillStyle(0x5f9a5a, 1);
            deco.fillEllipse(p.x - 17 + n * 16, p.y - 3, 12, 7);
          }
        } else if (k < 0.75) {
          // a stone lantern with a warm glow
          deco.fillStyle(0x000000, 0.18);
          deco.fillEllipse(p.x, p.y + 6, 24, 8);
          deco.fillStyle(0x9a9488, 1);
          deco.fillRect(p.x - 4, p.y - 10, 8, 14);
          deco.fillRect(p.x - 9, p.y - 22, 18, 12);
          deco.fillTriangle(p.x - 13, p.y - 22, p.x + 13, p.y - 22, p.x, p.y - 32);
          deco.fillStyle(0xffd27a, 1);
          deco.fillRect(p.x - 5, p.y - 19, 10, 6);
          deco.lineStyle(1.5, C.ink, 0.5);
          deco.strokeRect(p.x - 9, p.y - 22, 18, 12);
        } else {
          // a cherry tree in blossom
          const bloom = rnd.pick([0xe89ab8, 0xf4c0d4]);
          deco.fillStyle(0x000000, 0.2);
          deco.fillEllipse(p.x, p.y + 4, 38, 12);
          deco.fillStyle(0x5a3a2a, 1);
          deco.fillRect(p.x - 3, p.y - 14, 6, 18);
          deco.fillStyle(bloom, 1);
          deco.fillCircle(p.x, p.y - 24, 15);
          deco.fillCircle(p.x - 11, p.y - 16, 10);
          deco.fillCircle(p.x + 11, p.y - 16, 10);
          deco.fillStyle(0xffffff, 0.3);
          deco.fillCircle(p.x - 4, p.y - 28, 5);
        }
      } else if (this.level.theme.amber) {
        const k = rnd.frac();
        if (k < 0.6) {
          // a tall autumn tree: layered canopy in ember colours over a dark trunk
          const leaf = rnd.pick(this.level.theme.trees ?? [0xc83a1a]);
          const leaf2 = rnd.pick(this.level.theme.trees ?? [0xe87a1a]);
          deco.fillStyle(0x000000, 0.2);
          deco.fillEllipse(p.x, p.y + 4, 42, 14);
          deco.fillStyle(0x4a3020, 1);
          deco.fillRect(p.x - 4, p.y - 16, 8, 20);
          deco.fillStyle(leaf2, 1);
          deco.fillCircle(p.x - 11, p.y - 20, 13);
          deco.fillCircle(p.x + 11, p.y - 20, 13);
          deco.fillStyle(leaf, 1);
          deco.fillCircle(p.x, p.y - 30, 17);
          deco.lineStyle(2, C.ink, 0.5);
          deco.strokeCircle(p.x, p.y - 30, 17);
          deco.fillStyle(0xffffff, 0.16);
          deco.fillCircle(p.x - 6, p.y - 36, 6);
        } else if (k < 0.85) {
          // a heap of fallen leaves
          for (let n = 0; n < 7; n++) {
            deco.fillStyle(rnd.pick(this.level.theme.trees ?? [0xe87a1a]), 0.95);
            deco.fillEllipse(p.x + rnd.between(-14, 14), p.y + rnd.between(-6, 6), 11, 6);
          }
        } else {
          // a mossy fallen log with a little shelf fungus
          deco.fillStyle(0x000000, 0.18);
          deco.fillEllipse(p.x, p.y + 6, 50, 10);
          deco.fillStyle(0x6a4a2a, 1);
          deco.fillRoundedRect(p.x - 24, p.y - 7, 48, 14, 7);
          deco.fillStyle(0x9a7a4a, 1);
          deco.fillEllipse(p.x + 22, p.y, 10, 14);
          deco.fillStyle(0xe8b04a, 1);
          deco.fillEllipse(p.x - 6, p.y - 8, 12, 5);
          deco.lineStyle(1.5, C.ink, 0.5);
          deco.strokeRoundedRect(p.x - 24, p.y - 7, 48, 14, 7);
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

  private strokePath(g: Phaser.GameObjects.Graphics, pts: Vec2[], width: number, color: number, alpha = 1): void {
    g.lineStyle(width, color, alpha);
    g.beginPath();
    g.moveTo(pts[0].x, pts[0].y);
    for (let i = 1; i < pts.length; i++) g.lineTo(pts[i].x, pts[i].y);
    g.strokePath();
    g.fillStyle(color, alpha);
    for (const p of pts) g.fillCircle(p.x, p.y, width / 2);
  }

  /** Frost regions: wind-sculpted snow drifts, frozen puddles, and ice glinting on the roads. */
  private drawFrostGround(rnd: Phaser.Math.RandomDataGenerator): void {
    const g = this.add.graphics().setDepth(-9.5);
    const offRoad = (x: number, y: number, r: number) => !this.level.paths.some((pts) => pts.some((p, k) => k > 0 && distToSegment({ x, y }, pts[k - 1], p) < 34 + r));
    for (let i = 0; i < 18; i++) {
      const x = rnd.between(30, GAME_W - 30);
      const y = rnd.between(90, GAME_H - 20);
      const w = rnd.between(50, 120);
      if (!offRoad(x, y, w / 2)) continue;
      // a drift: blue shadow on the lee side, bright crest on top
      g.fillStyle(0x9ab0c8, 0.35);
      g.fillEllipse(x + 6, y + 5, w, w * 0.32);
      g.fillStyle(0xf4f8fc, 0.95);
      g.fillEllipse(x, y, w, w * 0.3);
      g.fillStyle(0xffffff, 1);
      g.fillEllipse(x - w * 0.12, y - w * 0.06, w * 0.55, w * 0.1);
    }
    for (let i = 0; i < 6; i++) {
      const x = rnd.between(60, GAME_W - 60);
      const y = rnd.between(120, GAME_H - 40);
      if (!offRoad(x, y, 30)) continue;
      // a frozen puddle with a crack and a shine
      g.fillStyle(0x8ac0e0, 0.6);
      g.fillEllipse(x, y, 54, 22);
      g.lineStyle(1.5, 0xd8f0ff, 0.9);
      g.strokeEllipse(x, y, 54, 22);
      g.lineBetween(x - 14, y - 4, x + 2, y + 2);
      g.lineBetween(x + 2, y + 2, x + 12, y - 3);
      g.fillStyle(0xffffff, 0.6);
      g.fillEllipse(x - 10, y - 5, 16, 4);
    }
    if (motion.reduced || motion.lowFx) return;
    // ice glints twinkling along the roads
    for (const pts of this.level.paths) {
      for (let i = 0; i < 10; i++) {
        const k = rnd.between(1, pts.length - 1);
        const t = rnd.frac();
        const x = pts[k - 1].x + (pts[k].x - pts[k - 1].x) * t + rnd.between(-18, 18);
        const y = pts[k - 1].y + (pts[k].y - pts[k - 1].y) * t + rnd.between(-18, 18);
        if (x < 0 || x > GAME_W || y < 70 || y > GAME_H) continue;
        const glint = this.add.star(x, y, 4, 1, 5, 0xffffff, 0.9).setDepth(-8).setBlendMode(Phaser.BlendModes.ADD).setAlpha(0);
        this.tweens.add({ targets: glint, alpha: 0.9, scale: 1.3, duration: 260, yoyo: true, repeat: -1, repeatDelay: rnd.between(1800, 4200), delay: rnd.between(0, 3000) });
      }
    }
  }

  /** Ember regions: scorched cracks with glowing lava seams that slowly breathe, and drifts of grey ash. */
  private drawEmberGround(rnd: Phaser.Math.RandomDataGenerator): void {
    const dark = this.add.graphics().setDepth(-9.5);
    const glow = this.add.graphics().setDepth(-9.4).setBlendMode(Phaser.BlendModes.ADD);
    const offRoad = (x: number, y: number) => !this.level.paths.some((pts) => pts.some((p, k) => k > 0 && distToSegment({ x, y }, pts[k - 1], p) < 40));
    const seams: { x: number; y: number }[] = [];
    for (let i = 0; i < 14; i++) {
      let x = rnd.between(40, GAME_W - 40);
      let y = rnd.between(100, GAME_H - 30);
      if (!offRoad(x, y)) continue;
      let a = rnd.frac() * Math.PI * 2;
      const segs = rnd.between(3, 6);
      for (let k = 0; k < segs; k++) {
        a += (rnd.frac() - 0.5) * 1.2;
        const len = rnd.between(12, 26);
        const nx = x + Math.cos(a) * len;
        const ny = y + Math.sin(a) * len * 0.6;
        if (!offRoad(nx, ny)) break;
        dark.lineStyle(8, 0x1a0e0a, 0.85);
        dark.lineBetween(x, y, nx, ny);
        dark.fillStyle(0x1a0e0a, 0.85);
        dark.fillCircle(nx, ny, 4);
        glow.lineStyle(3.5, 0xffa040, 0.95);
        glow.lineBetween(x, y, nx, ny);
        glow.lineStyle(11, 0xff5a1a, 0.22);
        glow.lineBetween(x, y, nx, ny);
        seams.push({ x: nx, y: ny });
        x = nx;
        y = ny;
      }
    }
    for (let i = 0; i < 40; i++) {
      dark.fillStyle(0x8a8078, 0.35);
      dark.fillCircle(rnd.between(0, GAME_W), rnd.between(80, GAME_H), rnd.between(1, 3));
    }
    if (!motion.reduced && !motion.lowFx) {
      this.tweens.add({ targets: glow, alpha: 0.45, duration: 1600, yoyo: true, repeat: -1, ease: 'Sine.easeInOut' });
      // now and then a spark spits out of a seam and floats up
      if (seams.length) {
        const sparks = this.add.particles(0, 0, 'dot', {
          speedY: { min: -40, max: -18 },
          speedX: { min: -8, max: 8 },
          scale: { start: 0.3, end: 0 },
          lifespan: 1200,
          tint: 0xffa040,
          blendMode: Phaser.BlendModes.ADD,
          emitting: false,
        });
        sparks.setDepth(-8);
        this.time.addEvent({ delay: 420, loop: true, callback: () => { const p = seams[Math.floor(Math.random() * seams.length)]; sparks.explode(1, p.x, p.y); } });
      }
    }
  }

  /** True when a point is clear of every road by `pad` px beyond the road's half-width. */
  private clearOfRoads(x: number, y: number, pad: number): boolean {
    return !this.level.paths.some((pts) => pts.some((p, k) => k > 0 && distToSegment({ x, y }, pts[k - 1], p) < 34 + pad));
  }

  /** Dusk regions: clusters of glowing toadstools and luminous moss that pulse softly. */
  private drawDuskGround(rnd: Phaser.Math.RandomDataGenerator): void {
    const g = this.add.graphics().setDepth(-9.5);
    const glow = this.add.graphics().setDepth(-9.4).setBlendMode(Phaser.BlendModes.ADD);
    const caps = [0x8ae8ff, 0xd88aff, 0x8affc8];
    for (let i = 0; i < 16; i++) {
      const cx = rnd.between(30, GAME_W - 30);
      const cy = rnd.between(100, GAME_H - 20);
      if (!this.clearOfRoads(cx, cy, 14)) continue;
      const col = rnd.pick(caps);
      glow.fillStyle(col, 0.16);
      glow.fillCircle(cx, cy, 26);
      for (let k = 0; k < rnd.between(2, 4); k++) {
        const x = cx + rnd.between(-12, 12);
        const y = cy + rnd.between(-6, 6);
        const r = rnd.between(4, 7);
        g.fillStyle(0xd8d0e0, 1);
        g.fillRect(x - 1.5, y - r * 0.2, 3, r + 2);
        g.fillStyle(col, 1);
        g.fillEllipse(x, y - r * 0.3, r * 2.2, r * 1.3);
        g.fillStyle(0xffffff, 0.8);
        g.fillCircle(x - r * 0.4, y - r * 0.5, 1.2);
        glow.fillStyle(col, 0.5);
        glow.fillEllipse(x, y - r * 0.3, r * 2.6, r * 1.6);
      }
    }
    for (let i = 0; i < 22; i++) {
      const x = rnd.between(0, GAME_W);
      const y = rnd.between(80, GAME_H);
      if (!this.clearOfRoads(x, y, 6)) continue;
      glow.fillStyle(0x6ae8c0, 0.22);
      glow.fillEllipse(x, y, rnd.between(14, 30), rnd.between(6, 12));
    }
    if (!motion.reduced && !motion.lowFx) this.tweens.add({ targets: glow, alpha: 0.55, duration: 2200, yoyo: true, repeat: -1, ease: 'Sine.easeInOut' });
  }

  /** Shore regions: darker wet-sand bands with ripple lines, scattered shells and the odd starfish. */
  private drawShoreGround(rnd: Phaser.Math.RandomDataGenerator): void {
    const g = this.add.graphics().setDepth(-9.5);
    for (let i = 0; i < 7; i++) {
      const y = rnd.between(120, GAME_H - 40);
      const x = rnd.between(0, GAME_W);
      g.fillStyle(0xb8a070, 0.25);
      g.fillEllipse(x, y, rnd.between(220, 420), rnd.between(40, 70));
      g.lineStyle(1.5, 0xf0e2b8, 0.5);
      for (let k = -2; k <= 2; k++) {
        g.beginPath();
        g.arc(x, y + k * 9 + 40, 120, Math.PI * 1.25, Math.PI * 1.75);
        g.strokePath();
      }
    }
    for (let i = 0; i < 26; i++) {
      const x = rnd.between(20, GAME_W - 20);
      const y = rnd.between(90, GAME_H - 15);
      if (!this.clearOfRoads(x, y, 6)) continue;
      const kind = rnd.frac();
      if (kind < 0.55) {
        // a fan shell with ribs
        g.fillStyle(rnd.pick([0xf8e8e0, 0xf0c8b8, 0xe8d8a8]), 1);
        g.slice(x, y + 3, 7, Math.PI * 1.1, Math.PI * 1.9, false);
        g.fillPath();
        g.lineStyle(1, 0xb89880, 0.8);
        for (let k = 0; k < 4; k++) {
          const a = Math.PI * (1.2 + k * 0.17);
          g.lineBetween(x, y + 3, x + Math.cos(a) * 6, y + 3 + Math.sin(a) * 6);
        }
      } else if (kind < 0.85) {
        // a little spiral snail shell
        g.fillStyle(0xe8d0b0, 1);
        g.fillCircle(x, y, 4);
        g.lineStyle(1, 0xa88a68, 0.9);
        g.beginPath();
        g.arc(x, y, 2.5, 0, Math.PI * 1.5);
        g.strokePath();
      } else {
        // a starfish
        g.fillStyle(0xf08a5a, 1);
        for (let k = 0; k < 5; k++) {
          const a = (k / 5) * Math.PI * 2 - Math.PI / 2;
          g.fillTriangle(x + Math.cos(a) * 8, y + Math.sin(a) * 8, x + Math.cos(a + 1.2) * 2.5, y + Math.sin(a + 1.2) * 2.5, x + Math.cos(a - 1.2) * 2.5, y + Math.sin(a - 1.2) * 2.5);
        }
        g.fillCircle(x, y, 2.8);
      }
    }
  }

  /** Crystal regions: clusters of faceted crystal shards that catch the light, with a twinkle now and then. */
  private drawCrystalGround(rnd: Phaser.Math.RandomDataGenerator): void {
    const g = this.add.graphics().setDepth(-9.5);
    const cols = [0x9ad8f0, 0xc0a0f0, 0x80e8d0];
    for (let i = 0; i < 14; i++) {
      const cx = rnd.between(30, GAME_W - 30);
      const cy = rnd.between(110, GAME_H - 20);
      if (!this.clearOfRoads(cx, cy, 16)) continue;
      const col = rnd.pick(cols);
      const light = Phaser.Display.Color.ValueToColor(col).lighten(18).color;
      g.fillStyle(0x000000, 0.18);
      g.fillEllipse(cx + 4, cy + 4, 34, 10);
      for (let k = 0; k < rnd.between(2, 4); k++) {
        const x = cx + rnd.between(-10, 10);
        const h = rnd.between(12, 24);
        const w = rnd.between(5, 8);
        const lean = rnd.between(-5, 5);
        g.fillStyle(col, 0.95);
        g.fillTriangle(x - w, cy, x + w, cy, x + lean, cy - h);
        g.fillStyle(light, 0.9);
        g.fillTriangle(x - w * 0.2, cy, x + w, cy, x + lean, cy - h);
      }
      if (!motion.reduced && !motion.lowFx) {
        const tw = this.add.star(cx + rnd.between(-6, 6), cy - rnd.between(10, 18), 4, 1, 5, 0xffffff, 0.9).setDepth(-8).setBlendMode(Phaser.BlendModes.ADD).setAlpha(0);
        this.tweens.add({ targets: tw, alpha: 1, scale: 1.4, duration: 240, yoyo: true, repeat: -1, repeatDelay: rnd.between(2000, 4500), delay: rnd.between(0, 3000) });
      }
    }
  }

  /** Windswept regions: long pale streaks where the wind combs the grass flat, and stray feathers. */
  private drawGaleGround(rnd: Phaser.Math.RandomDataGenerator): void {
    const g = this.add.graphics().setDepth(-9.5);
    for (let i = 0; i < 70; i++) {
      const x = rnd.between(0, GAME_W);
      const y = rnd.between(80, GAME_H);
      if (!this.clearOfRoads(x, y, 4)) continue;
      const len = rnd.between(18, 46);
      g.lineStyle(2, 0xe8f4ec, 0.35);
      g.lineBetween(x, y, x + len, y - len * 0.18);
    }
    for (let i = 0; i < 14; i++) {
      const x = rnd.between(30, GAME_W - 30);
      const y = rnd.between(100, GAME_H - 20);
      if (!this.clearOfRoads(x, y, 6)) continue;
      const a = rnd.frac() * Math.PI;
      const dx = Math.cos(a) * 8;
      const dy = Math.sin(a) * 4;
      g.lineStyle(1.2, 0x8a8a8a, 1);
      g.lineBetween(x - dx, y - dy, x + dx, y + dy);
      g.fillStyle(0xf4f4f0, 0.95);
      g.fillEllipse(x + dx * 0.2, y + dy * 0.2, 14, 5);
    }
  }

  /** Ruined regions: cracked flagstones half-sunk in the grass and toppled column drums. */
  private drawRuinsGround(rnd: Phaser.Math.RandomDataGenerator): void {
    const g = this.add.graphics().setDepth(-9.5);
    for (let i = 0; i < 12; i++) {
      const cx = rnd.between(40, GAME_W - 40);
      const cy = rnd.between(110, GAME_H - 30);
      if (!this.clearOfRoads(cx, cy, 30)) continue;
      for (let k = 0; k < rnd.between(3, 6); k++) {
        const x = cx + rnd.between(-30, 30);
        const y = cy + rnd.between(-14, 14);
        const w = rnd.between(14, 24);
        const h = rnd.between(9, 14);
        g.fillStyle(0x000000, 0.15);
        g.fillRect(x - w / 2 + 2, y - h / 2 + 3, w, h);
        g.fillStyle(rnd.pick([0xb8ae94, 0xa8a088, 0xc4baa0]), 1);
        g.fillRect(x - w / 2, y - h / 2, w, h);
        g.lineStyle(1, 0x6a6450, 0.8);
        g.lineBetween(x - w * 0.3, y - h / 2, x + w * 0.1, y + h / 2);
      }
    }
    for (let i = 0; i < 4; i++) {
      const x = rnd.between(80, GAME_W - 80);
      const y = rnd.between(140, GAME_H - 50);
      if (!this.clearOfRoads(x, y, 34)) continue;
      // a toppled column: two fluted drums lying in the grass
      for (const dx of [-16, 18]) {
        g.fillStyle(0x000000, 0.18);
        g.fillEllipse(x + dx + 3, y + 9, 34, 10);
        g.fillStyle(0xd0c8b0, 1);
        g.fillRect(x + dx - 15, y - 9, 30, 18);
        g.fillStyle(0xe4dcc4, 1);
        g.fillEllipse(x + dx + 15, y, 8, 18);
        g.lineStyle(1, 0x9a927a, 0.8);
        for (let k = -1; k <= 1; k++) g.lineBetween(x + dx - 15, y + k * 5, x + dx + 13, y + k * 5);
      }
      g.fillStyle(0x4a8a3a, 0.9);
      g.fillEllipse(x, y + 8, 30, 6);
    }
  }

  /** Clockwork regions: riveted plates bolted into the ground, glossy oil stains and stray cogs. */
  private drawGearsGround(rnd: Phaser.Math.RandomDataGenerator): void {
    const g = this.add.graphics().setDepth(-9.5);
    for (let i = 0; i < 9; i++) {
      const x = rnd.between(50, GAME_W - 50);
      const y = rnd.between(110, GAME_H - 30);
      if (!this.clearOfRoads(x, y, 30)) continue;
      const w = rnd.between(40, 70);
      const h = rnd.between(26, 40);
      g.fillStyle(0x6a6a72, 1);
      g.fillRect(x - w / 2, y - h / 2, w, h);
      g.lineStyle(2, 0x3a3a42, 1);
      g.strokeRect(x - w / 2, y - h / 2, w, h);
      g.fillStyle(0xb0b0b8, 1);
      for (const [rx, ry] of [[-1, -1], [1, -1], [-1, 1], [1, 1]]) g.fillCircle(x + rx * (w / 2 - 5), y + ry * (h / 2 - 5), 2.2);
    }
    for (let i = 0; i < 8; i++) {
      const x = rnd.between(30, GAME_W - 30);
      const y = rnd.between(100, GAME_H - 20);
      if (!this.clearOfRoads(x, y, 10)) continue;
      g.fillStyle(0x1a1a22, 0.55);
      g.fillEllipse(x, y, rnd.between(24, 44), rnd.between(10, 16));
      g.fillStyle(0x8a6ac8, 0.25);
      g.fillEllipse(x - 4, y - 2, 12, 3);
    }
    for (let i = 0; i < 10; i++) {
      const x = rnd.between(30, GAME_W - 30);
      const y = rnd.between(100, GAME_H - 20);
      if (!this.clearOfRoads(x, y, 8)) continue;
      const r = rnd.between(5, 9);
      g.fillStyle(0xc8963a, 1);
      for (let k = 0; k < 8; k++) {
        const a = (k / 8) * Math.PI * 2;
        g.fillRect(x + Math.cos(a) * r - 1.5, y + Math.sin(a) * r - 1.5, 3, 3);
      }
      g.fillCircle(x, y, r);
      g.fillStyle(0x5a4a2a, 1);
      g.fillCircle(x, y, r * 0.35);
    }
  }

  /** Abyss regions: branching veins of cold light under the dark ground, pulsing slowly. */
  private drawAbyssGround(rnd: Phaser.Math.RandomDataGenerator): void {
    const glow = this.add.graphics().setDepth(-9.4).setBlendMode(Phaser.BlendModes.ADD);
    for (let i = 0; i < 12; i++) {
      let x = rnd.between(30, GAME_W - 30);
      let y = rnd.between(100, GAME_H - 20);
      if (!this.clearOfRoads(x, y, 8)) continue;
      let a = rnd.frac() * Math.PI * 2;
      const col = rnd.pick([0x5ae8d0, 0x9a7ae8]);
      for (let k = 0; k < rnd.between(4, 8); k++) {
        a += (rnd.frac() - 0.5) * 1.1;
        const nx = x + Math.cos(a) * rnd.between(14, 26);
        const ny = y + Math.sin(a) * rnd.between(8, 16);
        if (!this.clearOfRoads(nx, ny, 4)) break;
        glow.lineStyle(2, col, 0.75);
        glow.lineBetween(x, y, nx, ny);
        glow.lineStyle(7, col, 0.12);
        glow.lineBetween(x, y, nx, ny);
        if (rnd.frac() < 0.3) {
          glow.fillStyle(col, 0.8);
          glow.fillCircle(nx, ny, 2.5);
        }
        x = nx;
        y = ny;
      }
    }
    if (!motion.reduced && !motion.lowFx) this.tweens.add({ targets: glow, alpha: 0.4, duration: 2600, yoyo: true, repeat: -1, ease: 'Sine.easeInOut' });
  }

  /** Orchard regions: windfall apples and pears in the grass and drifts of autumn leaf litter. */
  private drawOrchardGround(rnd: Phaser.Math.RandomDataGenerator): void {
    const g = this.add.graphics().setDepth(-9.5);
    for (let i = 0; i < 90; i++) {
      const x = rnd.between(0, GAME_W);
      const y = rnd.between(80, GAME_H);
      if (!this.clearOfRoads(x, y, 2)) continue;
      g.fillStyle(rnd.pick([0xd8642a, 0xe8a03a, 0xb8442a, 0xc8b040]), 0.85);
      const a = rnd.frac() * Math.PI;
      g.fillEllipse(x, y, 7, 3.5);
      g.lineStyle(1, 0x6a3a1a, 0.6);
      g.lineBetween(x - Math.cos(a) * 3, y - Math.sin(a) * 1.5, x + Math.cos(a) * 3, y + Math.sin(a) * 1.5);
    }
    for (let i = 0; i < 20; i++) {
      const x = rnd.between(20, GAME_W - 20);
      const y = rnd.between(100, GAME_H - 20);
      if (!this.clearOfRoads(x, y, 6)) continue;
      const pear = rnd.frac() < 0.35;
      g.fillStyle(0x000000, 0.15);
      g.fillEllipse(x + 2, y + 4, 12, 4);
      g.fillStyle(pear ? 0xc8c040 : rnd.pick([0xd83a2a, 0xe85a2a]), 1);
      if (pear) {
        g.fillCircle(x, y + 1, 4.5);
        g.fillCircle(x, y - 3, 3);
      } else g.fillCircle(x, y, 5);
      g.fillStyle(0xffffff, 0.5);
      g.fillCircle(x - 1.5, y - 1.5, 1.4);
      g.lineStyle(1.5, 0x5a3a1a, 1);
      g.lineBetween(x, y - (pear ? 5 : 4), x + 1, y - (pear ? 8 : 7));
    }
  }

  /** Storm regions: rain puddles that ripple, and starburst scorch marks where lightning struck. */
  private drawStormGround(rnd: Phaser.Math.RandomDataGenerator): void {
    const g = this.add.graphics().setDepth(-9.5);
    for (let i = 0; i < 7; i++) {
      const x = rnd.between(40, GAME_W - 40);
      const y = rnd.between(110, GAME_H - 30);
      if (!this.clearOfRoads(x, y, 16)) continue;
      g.fillStyle(0x2a2418, 0.45);
      g.fillCircle(x, y, 10);
      g.lineStyle(2, 0x2a2418, 0.4);
      for (let k = 0; k < 7; k++) {
        const a = (k / 7) * Math.PI * 2 + rnd.frac() * 0.4;
        g.lineBetween(x, y, x + Math.cos(a) * rnd.between(14, 24), y + Math.sin(a) * rnd.between(8, 14));
      }
    }
    for (let i = 0; i < 9; i++) {
      const x = rnd.between(40, GAME_W - 40);
      const y = rnd.between(110, GAME_H - 30);
      if (!this.clearOfRoads(x, y, 20)) continue;
      const w = rnd.between(30, 56);
      g.fillStyle(0x5a6a7a, 0.6);
      g.fillEllipse(x, y, w, w * 0.36);
      g.fillStyle(0xc8d8e8, 0.35);
      g.fillEllipse(x - w * 0.15, y - w * 0.06, w * 0.4, w * 0.08);
      if (!motion.reduced && !motion.lowFx) {
        this.time.addEvent({
          delay: 900 + rnd.between(0, 700),
          loop: true,
          callback: () => {
            const ring = this.add.ellipse(x + (Math.random() - 0.5) * w * 0.6, y + (Math.random() - 0.5) * w * 0.2, 6, 2.5, 0xffffff, 0).setStrokeStyle(1, 0xe8f4ff, 0.7).setDepth(-9);
            this.tweens.add({ targets: ring, scale: 3, alpha: 0, duration: 700, onComplete: () => ring.destroy() });
          },
        });
      }
    }
  }

  /** Desert regions: wind ripples combed across the sand and the odd bleached stone. */
  private drawDuneGround(rnd: Phaser.Math.RandomDataGenerator): void {
    const g = this.add.graphics().setDepth(-9.5);
    for (let i = 0; i < 26; i++) {
      const x = rnd.between(0, GAME_W);
      const y = rnd.between(90, GAME_H);
      if (!this.clearOfRoads(x, y, 20)) continue;
      const w = rnd.between(60, 130);
      for (let k = 0; k < 4; k++) {
        g.lineStyle(2, 0xb88a50, 0.28);
        g.beginPath();
        g.arc(x, y + k * 7 + w, w, Math.PI * 1.32, Math.PI * 1.68);
        g.strokePath();
        g.lineStyle(1.5, 0xfff0c8, 0.3);
        g.beginPath();
        g.arc(x, y + k * 7 + w - 2, w, Math.PI * 1.34, Math.PI * 1.66);
        g.strokePath();
      }
    }
    for (let i = 0; i < 8; i++) {
      const x = rnd.between(30, GAME_W - 30);
      const y = rnd.between(110, GAME_H - 20);
      if (!this.clearOfRoads(x, y, 8)) continue;
      g.fillStyle(0x000000, 0.15);
      g.fillEllipse(x + 3, y + 4, 18, 6);
      g.fillStyle(0xf0e4c8, 1);
      g.fillEllipse(x, y, 15, 9);
    }
  }

  /** Reef regions: branching coral, sea-glass pebbles and swaying anemones on the bright floor. */
  private drawReefGround(rnd: Phaser.Math.RandomDataGenerator): void {
    const g = this.add.graphics().setDepth(-9.5);
    for (let i = 0; i < 12; i++) {
      const x = rnd.between(30, GAME_W - 30);
      const y = rnd.between(110, GAME_H - 20);
      if (!this.clearOfRoads(x, y, 16)) continue;
      const col = rnd.pick([0xf07a6a, 0xf0a05a, 0xd86aa8, 0xf8c8d8]);
      g.lineStyle(4, col, 1);
      const branch = (bx: number, by: number, a: number, len: number, depth: number) => {
        const ex = bx + Math.cos(a) * len;
        const ey = by + Math.sin(a) * len;
        g.lineBetween(bx, by, ex, ey);
        if (depth > 0) {
          branch(ex, ey, a - 0.5, len * 0.7, depth - 1);
          branch(ex, ey, a + 0.5, len * 0.7, depth - 1);
        } else {
          g.fillStyle(col, 1);
          g.fillCircle(ex, ey, 2.5);
        }
      };
      branch(x, y, -Math.PI / 2, rnd.between(8, 12), 2);
    }
    for (let i = 0; i < 30; i++) {
      const x = rnd.between(10, GAME_W - 10);
      const y = rnd.between(90, GAME_H - 10);
      if (!this.clearOfRoads(x, y, 4)) continue;
      g.fillStyle(rnd.pick([0x9ae8d8, 0xb8d8f8, 0xd8f0a8]), 0.85);
      g.fillEllipse(x, y, 6, 4);
      g.fillStyle(0xffffff, 0.6);
      g.fillCircle(x - 1, y - 1, 1);
    }
  }

  /** Scatter `count` spots that keep `pad` px clear of the roads, calling draw(x, y) for each. */
  private scatter(rnd: Phaser.Math.RandomDataGenerator, count: number, pad: number, draw: (x: number, y: number) => void): void {
    for (let i = 0; i < count; i++) {
      const x = rnd.between(20, GAME_W - 20);
      const y = rnd.between(95, GAME_H - 15);
      if (this.clearOfRoads(x, y, pad)) draw(x, y);
    }
  }

  /** Ground detail for the flotilla, amber, mist, canopy, comb and bog regions. */
  private drawMoreGround(rnd: Phaser.Math.RandomDataGenerator): void {
    const { theme } = this.level;
    const g = this.add.graphics().setDepth(-9.5);
    const glow = this.add.graphics().setDepth(-9.4).setBlendMode(Phaser.BlendModes.ADD);
    if (theme.flotilla) {
      // floating flotsam on the dark water: plank rafts, rope coils and bobbing barrels
      this.scatter(rnd, 10, 24, (x, y) => {
        for (let k = 0; k < 3; k++) {
          g.fillStyle(rnd.pick([0x8a6a4a, 0x7a5a3a, 0x9a7a52]), 1);
          g.fillRect(x - 18, y - 8 + k * 6, 36, 5);
        }
        g.lineStyle(1, 0x4a3a2a, 0.8);
        g.lineBetween(x - 12, y - 9, x - 12, y + 9);
        g.lineBetween(x + 12, y - 9, x + 12, y + 9);
        g.lineStyle(1.5, 0xc8e0f0, 0.35);
        g.strokeEllipse(x, y + 2, 46, 18);
      });
      this.scatter(rnd, 8, 10, (x, y) => {
        g.lineStyle(2.5, 0xc8a86a, 1);
        g.strokeCircle(x, y, 6);
        g.strokeCircle(x, y, 3);
      });
    }
    if (theme.amber) {
      // glistening resin drops and beads of amber with something tiny caught inside
      this.scatter(rnd, 22, 6, (x, y) => {
        g.fillStyle(0xd88a20, 0.9);
        g.fillEllipse(x, y, 10, 7);
        g.fillStyle(0x6a3a10, 0.8);
        g.fillCircle(x + 1, y + 1, 1.2);
        glow.fillStyle(0xffc860, 0.45);
        glow.fillEllipse(x - 2, y - 2, 4, 2);
      });
      this.scatter(rnd, 30, 2, (x, y) => {
        g.fillStyle(rnd.pick([0xc83a1a, 0xe87a1a, 0xf0c040]), 0.8);
        g.fillEllipse(x, y, 6, 3);
      });
    }
    if (theme.mist) {
      // dewy grass glittering in pale patches, and soft low mist pooling in hollows
      this.scatter(rnd, 10, 10, (x, y) => {
        g.fillStyle(0xf0f8f4, 0.22);
        g.fillEllipse(x, y, rnd.between(80, 150), rnd.between(24, 40));
      });
      this.scatter(rnd, 60, 0, (x, y) => {
        glow.fillStyle(0xffffff, 0.55);
        glow.fillCircle(x, y, 1.2);
      });
    }
    if (theme.canopy) {
      // tangled surface roots and drifts of big fallen leaves on the forest floor
      this.scatter(rnd, 10, 16, (x, y) => {
        g.lineStyle(4, 0x5a3a22, 0.9);
        let a = rnd.frac() * Math.PI * 2;
        let px = x;
        let py = y;
        for (let k = 0; k < 4; k++) {
          a += (rnd.frac() - 0.5) * 0.9;
          const nx = px + Math.cos(a) * 14;
          const ny = py + Math.sin(a) * 8;
          g.lineBetween(px, py, nx, ny);
          px = nx;
          py = ny;
        }
      });
      this.scatter(rnd, 40, 2, (x, y) => {
        g.fillStyle(rnd.pick([0x6a8a3a, 0x8a7a3a, 0x5a7a2e]), 0.85);
        g.fillEllipse(x, y, 11, 5);
        g.lineStyle(1, 0x3a4a1a, 0.7);
        g.lineBetween(x - 5, y, x + 5, y);
      });
    }
    if (theme.comb) {
      // honey drips and broken bits of comb in the grass, with bees' wax glinting
      this.scatter(rnd, 10, 12, (x, y) => {
        for (let k = 0; k < 3; k++) {
          const hx = x + (k % 2) * 9 - 4;
          const hy = y + Math.floor(k / 2) * 8 - 4;
          g.fillStyle(0xe8b040, 1);
          g.fillCircle(hx, hy, 5);
          g.lineStyle(1.5, 0xa87020, 1);
          g.strokeCircle(hx, hy, 5);
        }
        glow.fillStyle(0xffe08a, 0.4);
        glow.fillCircle(x, y, 10);
      });
      this.scatter(rnd, 16, 4, (x, y) => {
        g.fillStyle(0xd89a20, 0.85);
        g.fillEllipse(x, y, 8, 5);
        g.fillStyle(0xfff0b0, 0.7);
        g.fillCircle(x - 1.5, y - 1, 1.3);
      });
    }
    if (theme.bog) {
      // lily pads with the odd pale flower floating on dark peat water, and marsh bubbles
      this.scatter(rnd, 16, 12, (x, y) => {
        g.fillStyle(0x1e3a30, 0.6);
        g.fillEllipse(x + 2, y + 3, 30, 12);
        g.fillStyle(0x4a8a4a, 1);
        g.slice(x, y, 11, 0.4, Math.PI * 2 - 0.2, false);
        g.fillPath();
        if (rnd.frac() < 0.3) {
          g.fillStyle(0xf8e8f0, 1);
          g.fillCircle(x + 2, y - 2, 3);
          g.fillStyle(0xf0d040, 1);
          g.fillCircle(x + 2, y - 2, 1.2);
        }
      });
      if (!motion.reduced && !motion.lowFx) {
        const spots: { x: number; y: number }[] = [];
        this.scatter(rnd, 8, 10, (x, y) => spots.push({ x, y }));
        if (spots.length) {
          this.time.addEvent({
            delay: 600,
            loop: true,
            callback: () => {
              const p = spots[Math.floor(Math.random() * spots.length)];
              const b = this.add.circle(p.x + (Math.random() - 0.5) * 10, p.y, 2.5, 0xffffff, 0).setStrokeStyle(1, 0xc8e8d8, 0.8).setDepth(-9);
              this.tweens.add({ targets: b, y: p.y - 6, scale: 1.6, alpha: 0, duration: 900, onComplete: () => b.destroy() });
            },
          });
        }
      }
    }
    if (!motion.reduced && !motion.lowFx && (theme.amber || theme.mist || theme.comb)) this.tweens.add({ targets: glow, alpha: 0.5, duration: 2000, yoyo: true, repeat: -1, ease: 'Sine.easeInOut' });
  }

  /** Ground detail for the thistle, wold, canyon, brook and heath regions. */
  private drawLastGround(rnd: Phaser.Math.RandomDataGenerator): void {
    const { theme } = this.level;
    const g = this.add.graphics().setDepth(-9.5);
    if (theme.thistle) {
      // tufts of thistledown caught in the grass and the odd low purple thistle head
      this.scatter(rnd, 40, 2, (x, y) => {
        g.fillStyle(0xffffff, 0.75);
        g.fillCircle(x, y, 2);
        g.lineStyle(0.8, 0xffffff, 0.6);
        for (let k = 0; k < 5; k++) {
          const a = (k / 5) * Math.PI * 2;
          g.lineBetween(x, y, x + Math.cos(a) * 4, y + Math.sin(a) * 4);
        }
      });
      this.scatter(rnd, 12, 6, (x, y) => {
        g.fillStyle(0x6a8a3a, 1);
        g.fillTriangle(x - 4, y + 2, x + 4, y + 2, x, y - 4);
        g.fillStyle(0xa86ac8, 1);
        g.fillCircle(x, y - 6, 3.5);
      });
    }
    if (theme.wold) {
      // furrowed field strips and scattered stooks of cut wheat
      this.scatter(rnd, 6, 40, (x, y) => {
        g.lineStyle(2, 0x5a8a3a, 0.35);
        for (let k = -3; k <= 3; k++) g.lineBetween(x - 60, y + k * 7, x + 60, y + k * 7 - 10);
      });
      this.scatter(rnd, 10, 8, (x, y) => {
        g.fillStyle(0x000000, 0.15);
        g.fillEllipse(x + 3, y + 5, 16, 5);
        g.fillStyle(0xd8b050, 1);
        g.fillTriangle(x - 7, y + 4, x + 7, y + 4, x, y - 10);
        g.lineStyle(1, 0xa88030, 1);
        g.lineBetween(x - 6, y, x + 6, y);
      });
    }
    if (theme.canyon) {
      // sun-baked cracked mud plates and rust-red pebbles
      this.scatter(rnd, 8, 20, (x, y) => {
        g.lineStyle(1.5, 0x8a4a2a, 0.55);
        for (let k = 0; k < 6; k++) {
          const a = (k / 6) * Math.PI * 2;
          g.lineBetween(x, y, x + Math.cos(a) * 22, y + Math.sin(a) * 12);
          g.lineBetween(x + Math.cos(a) * 12, y + Math.sin(a) * 7, x + Math.cos(a + 1) * 12, y + Math.sin(a + 1) * 7);
        }
      });
      this.scatter(rnd, 40, 2, (x, y) => {
        g.fillStyle(rnd.pick([0x9a4a2a, 0xb8683e, 0x7a3a22]), 0.9);
        g.fillCircle(x, y, rnd.between(1, 3));
      });
    }
    if (theme.brook) {
      // smooth river pebbles along the banks and patches of yellow marsh flowers
      this.scatter(rnd, 30, 4, (x, y) => {
        g.fillStyle(rnd.pick([0x9aa0a0, 0xb8b0a0, 0x8a9090]), 1);
        g.fillEllipse(x, y, rnd.between(6, 11), rnd.between(4, 7));
        g.fillStyle(0xffffff, 0.3);
        g.fillEllipse(x - 1, y - 1, 3, 1.5);
      });
      this.scatter(rnd, 10, 6, (x, y) => {
        for (let k = 0; k < 4; k++) {
          g.fillStyle(0xf0d040, 1);
          g.fillCircle(x + rnd.between(-8, 8), y + rnd.between(-4, 4), 2.2);
        }
      });
    }
    if (theme.heath) {
      // peat hags (dark exposed patches) and white bog-cotton tufts
      this.scatter(rnd, 7, 20, (x, y) => {
        g.fillStyle(0x3a2e24, 0.55);
        g.fillEllipse(x, y, rnd.between(40, 70), rnd.between(14, 22));
        g.fillStyle(0x5a4a3a, 0.5);
        g.fillEllipse(x - 4, y - 3, 20, 5);
      });
      this.scatter(rnd, 30, 3, (x, y) => {
        g.lineStyle(1, 0x6a6a4a, 1);
        g.lineBetween(x, y + 4, x, y - 2);
        g.fillStyle(0xffffff, 0.95);
        g.fillCircle(x, y - 4, 2.4);
      });
    }
  }

  /** A boss falls: a slow-motion beat, a white flash, a shockwave and a volley of fireworks over the battlefield. */
  /** "Wave N cleared" pill under the HUD (gold "Flawless" tag when no lives were lost), a chime and a sparkle. */
  private waveClearedPill(index: number): void {
    const info = waveClearInfo(index, this.sim.leaksByWave, this.sim.totalWaves, this.endless);
    sfx.waveClear(info.flawless);
    this.children.getByName('waveClear')?.destroy();
    // sit under the HUD, or below the centre banner if one is up (e.g. the next wave was called straight away)
    const py = this.children.getByName('banner') ? 262 : 140;
    const c = this.add.container(GAME_W / 2, py).setDepth(3990).setName('waveClear');
    const title = this.add.text(0, 0, `✓ ${info.title}`, textStyle(pf(18), '#d8ffc0')).setOrigin(0.5);
    const tag = info.flawless ? this.add.text(0, 0, 'Flawless', textStyle(pf(13), '#16241c')).setOrigin(0.5) : null;
    const sub = info.left ? this.add.text(0, 0, info.left, textStyle(pf(12), TEXT.cream, false)).setOrigin(0.5) : null;
    const tagW = tag ? tag.width + 18 : 0;
    const W = Math.max(title.width + tagW + 40, (sub?.width ?? 0) + 40);
    const H = sub ? 58 : 40;
    const g = this.add.graphics();
    glossPanel(g, -W / 2, -H / 2, W, H, { fill: 0x1e3a24, alpha: 0.95, rim: info.flawless ? 0xffd23c : 0x6ab04c, rimAlpha: 0.9, radius: 14 });
    c.add(g);
    title.setPosition(-tagW / 2, sub ? -10 : 0);
    c.add(title);
    if (tag) {
      const tx = title.x + title.width / 2 + 10 + tag.width / 2;
      const tg = this.add.graphics();
      tg.fillStyle(0xffd23c, 1);
      tg.fillRoundedRect(tx - tag.width / 2 - 7, title.y - 11, tag.width + 14, 22, 10);
      c.add(tg);
      tag.setPosition(tx, title.y);
      c.add(tag);
    }
    if (sub) {
      sub.setPosition(0, 14);
      c.add(sub);
    }
    if (!motion.lowFx) {
      this.particles.setParticleTint(info.flawless ? 0xffd23c : 0x9be86a);
      this.particles.explode(motion.reduced ? 4 : 12, GAME_W / 2, py);
    }
    if (motion.reduced) {
      this.time.delayedCall(1800, () => c.destroy());
      return;
    }
    c.setScale(0.6).setAlpha(0);
    this.tweens.add({
      targets: c,
      scale: 1,
      alpha: 1,
      duration: 220,
      ease: 'Back.easeOut',
      onComplete: () => this.tweens.add({ targets: c, alpha: 0, y: c.y - 14, delay: 1400, duration: 350, onComplete: () => c.destroy() }),
    });
  }

  /** "<Boss> defeated!" on a gold ribbon near the top, with the bounty, that pops in, holds and fades away. */
  private bossDefeatedBanner(name: string, bounty: number): void {
    this.children.getByName('bossDefeated')?.destroy();
    const c = this.add.container(GAME_W / 2, 196).setDepth(3995).setName('bossDefeated');
    c.add(ribbon(this, 0, 520, 0xd89a2a, 0x8a5a14));
    c.add(fitWidth(this.add.text(0, -4, `${name} defeated!`, textStyle(pf(30), '#fff2c0')).setOrigin(0.5).setStroke('#5a3a0a', 7), 420));
    c.add(this.add.text(0, 50, `+${bounty} coins`, textStyle(pf(18), TEXT.gold)).setOrigin(0.5).setStroke('#16241c', 5));
    if (motion.reduced) {
      this.time.delayedCall(2200, () => c.destroy());
      return;
    }
    c.setScale(0.4).setAlpha(0);
    this.tweens.add({
      targets: c,
      scale: 1,
      alpha: 1,
      duration: 260,
      ease: 'Back.easeOut',
      onComplete: () => this.tweens.add({ targets: c, alpha: 0, y: c.y - 20, delay: 1700, duration: 400, onComplete: () => c.destroy() }),
    });
  }

  private bossFireworks(x: number, y: number, color: number): void {
    this.cameras.main.flash(220, 255, 250, 230);
    shake(this, 400, 0.012);
    const ring = this.add.circle(x, y, 30, 0xffffff, 0).setStrokeStyle(6, 0xfff0c0, 1).setDepth(2700);
    this.tweens.add({ targets: ring, scale: 6, alpha: 0, duration: 700, ease: 'Cubic.easeOut', onComplete: () => ring.destroy() });
    this.particles.setParticleTint(color);
    this.particles.explode(40, x, y);
    if (motion.lowFx) return;
    const colors = [0xffd060, 0xff6a8a, 0x8ae8ff, 0xb08aff, 0x9be86a];
    for (let k = 0; k < 7; k++) {
      this.time.delayedCall(200 + k * 260, () => {
        const fx = Phaser.Math.Between(180, GAME_W - 180);
        const fy = Phaser.Math.Between(140, GAME_H / 2);
        const rocket = this.add.circle(fx, GAME_H - 60, 3, 0xfff0c0).setDepth(2700).setBlendMode(Phaser.BlendModes.ADD);
        this.tweens.add({
          targets: rocket,
          y: fy,
          duration: 420,
          ease: 'Quad.easeOut',
          onComplete: () => {
            rocket.destroy();
            const col = colors[k % colors.length];
            const burst = this.add.particles(fx, fy, 'dot', { speed: { min: 80, max: 220 }, scale: { start: 0.6, end: 0 }, lifespan: 900, gravityY: 120, tint: col, blendMode: Phaser.BlendModes.ADD, emitting: false });
            burst.setDepth(2700);
            burst.explode(36);
            this.time.delayedCall(1200, () => burst.destroy());
            sfx.boom();
          },
        });
      });
    }
  }

  /** Scene lighting: warm light from the top-left, a cooler bottom-right, and a soft vignette over the field. */
  private drawLighting(): void {
    addLighting(this, 2900);
  }

  // ---------- HUD ----------

  private buildHud(): void {
    // scene instances are reused between battles, so reset per-battle HUD state here
    this.shownCoins = this.shownLives = this.shownWave = -1;
    this.cheapestTower = 0;
    this.tipped = new Set();
    this.hitStopUntil = 0;
    this.lastHitStop = -9999;
    this.skillWasReady = true; // no ping for the skill being ready at the start
    this.heroPortrait = null;
    this.heroCard = null;
    this.enemyCard = null;
    this.enemyCardUid = 0;
    this.skillPreview = false;
    const bar = this.add.graphics().setDepth(3000);
    // glossy top bar: drop shadow, dark body, lighter upper half, rim light and slim gold dividers
    bar.fillStyle(0x000000, 0.25);
    bar.fillRoundedRect(14, 14, 440, 54, 16);
    bar.fillStyle(C.ink, 0.82);
    bar.fillRoundedRect(12, 10, 440, 54, 16);
    bar.fillStyle(0xffffff, 0.07);
    bar.fillRoundedRect(14, 12, 436, 24, { tl: 14, tr: 14, bl: 4, br: 4 });
    bar.lineStyle(2, 0xffffff, 0.18);
    bar.strokeRoundedRect(13, 11, 438, 52, 15);
    bar.lineStyle(2, 0x000000, 0.35);
    bar.strokeRoundedRect(11, 9, 442, 56, 17);
    bar.fillStyle(C.gold, 0.35);
    bar.fillRect(132, 22, 2, 30);
    bar.fillRect(268, 22, 2, 30);

    this.add.image(40, 37, 'icon_heart').setDepth(3001);
    this.livesText = this.add.text(60, 37, '', textStyle(26, TEXT.heart)).setOrigin(0, 0.5).setDepth(3001);
    this.add.image(150, 37, 'icon_coin').setDepth(3001);
    this.coinText = this.add.text(170, 37, '', textStyle(26, TEXT.gold)).setOrigin(0, 0.5).setDepth(3001);
    this.titheText = this.add.text(20, 76, '', textStyle(13, '#ff9a7a')).setOrigin(0, 0.5).setDepth(3001).setVisible(false);
    if (devOn()) this.add.text(GAME_W / 2, GAME_H - 14, 'DEV MODE: endless coins, lives and spells (results not saved)', textStyle(13, '#ffb0c8')).setOrigin(0.5).setDepth(3001);
    this.add.image(290, 34, 'icon_wave').setDepth(3001);
    this.waveText = this.add.text(310, 34, '', textStyle(24)).setOrigin(0, 0.5).setDepth(3001);
    this.waveBar = this.add.graphics().setDepth(3001);

    this.nextWaveBtn = new Button(this, GAME_W - 130, 40, 'Call Wave', {
      width: 220,
      height: 52,
      fontSize: 22,
      color: 0xff9f43,
      onClick: () => this.callWave(),
    }).setDepth(3001);
    // wave-call dressing: a pulsing glow behind the button, a countdown strip along its bottom, and a chip with
    // the coins an early call would pay right now
    this.callG = this.add.graphics().setDepth(3000);
    this.callStrip = this.add.graphics().setDepth(3002);
    this.callChip = this.add.text(GAME_W - 130, 80, '', textStyle(pf(13), TEXT.gold)).setOrigin(0.5, 0).setDepth(3002).setBackgroundColor('#16241ce0').setPadding(8, 2, 8, 3).setVisible(false);
    this.callFull = 1;
    this.callLast = 0;
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

  private spellIcons: Record<string, Phaser.GameObjects.Image> = {};
  private spellWasReady: Record<string, boolean> = {};

  private buildSpells(): void {
    this.spellIcons = {};
    this.spellWasReady = {};
    this.spellHud = this.add.graphics().setDepth(3000);
    this.reticle = this.add.circle(0, 0, 60, 0xffffff, 0.12).setStrokeStyle(3, C.cream, 0.9).setDepth(2900).setVisible(false);
    this.aimG = this.add.graphics().setDepth(2905);
    this.rallyG = this.add.graphics().setDepth(3290);
    this.heroDragG = this.add.graphics().setDepth(3290);
    this.rallyGhost = null;
    this.aimText = this.add.text(0, 0, '', textStyle(pf(14), TEXT.cream)).setOrigin(0.5).setDepth(2906).setVisible(false);
    SPELL_ORDER.forEach((id, i) => {
      const p = this.spellPos(i);
      this.spellIcons[id] = this.add.image(p.x, p.y - 4, `icon_${id}`).setDepth(3001);
      this.spellWasReady[id] = true; // no ping for spells that start ready
      fitWidth(this.add.text(p.x, p.y + 30, SPELLS[id].name, textStyle(pf(12))).setOrigin(0.5).setDepth(3002), 84);
      const zone = this.add.zone(p.x, p.y, 80, 80).setDepth(3002).setInteractive({ useHandCursor: true });
      zone.on('pointerdown', (_p: Phaser.Input.Pointer, _x: number, _y: number, ev: Phaser.Types.Input.EventData) => {
        ev.stopPropagation();
        sfx.unlock();
        sfx.click();
        // press-in: the icon squashes and springs back
        const icon = this.spellIcons[id];
        if (icon && !motion.reduced) {
          this.tweens.killTweensOf(icon);
          icon.setScale(1);
          this.tweens.add({ targets: icon, scaleX: 0.82, scaleY: 0.78, duration: 70, yoyo: true, ease: 'Quad.easeOut' });
        }
        this.closeMenu();
        this.selectHero(false);
        this.armSpell(this.spellMode === id ? null : id);
      });
    });
  }

  /**
   * While a spell is armed: soft glow rings and a slowly turning dashed rim around the aim circle, a small
   * crosshair, a ring on every foe it would hit (same rules as the cast, via `spellHits`) and a count above it.
   */
  private drawAim(): void {
    const g = this.aimG;
    const label = this.aimText;
    if (!g || !label) return;
    g.clear();
    const id = this.spellMode;
    if (!id) {
      if (this.skillPreview) this.drawSkillPreview(g, label);
      else label.setVisible(false);
      return;
    }
    // on touch the aim only shows while a finger is down (there's no hovering pointer to follow)
    const touchIdle = this.input.activePointer.wasTouch && !this.aimHold;
    this.reticle.setVisible(!touchIdle);
    if (touchIdle) {
      label.setVisible(false);
      return;
    }
    const def = SPELLS[id];
    const x = this.reticle.x;
    const y = this.reticle.y;
    const r = def.radius ?? 50;
    for (let k = 0; k < 3; k++) {
      g.lineStyle(4, def.color, 0.22 - k * 0.06);
      g.strokeCircle(x, y, r + 3 + k * 4);
    }
    const turn = motion.reduced ? 0 : this.time.now / 900;
    g.lineStyle(2, 0xffffff, 0.75);
    for (let k = 0; k < 16; k++) {
      const a0 = turn + (k / 16) * Math.PI * 2;
      g.beginPath();
      g.arc(x, y, r - 5, a0, a0 + 0.2);
      g.strokePath();
    }
    g.lineStyle(2, 0xffffff, 0.8);
    g.lineBetween(x - 8, y, x - 3, y);
    g.lineBetween(x + 3, y, x + 8, y);
    g.lineBetween(x, y - 8, x, y - 3);
    g.lineBetween(x, y + 3, x, y + 8);
    if (def.kind === 'reinforce') {
      label.setText('Rangers land here');
    } else {
      const hits = this.sim.spellHits(id, { x, y });
      const pulse = motion.reduced ? 1 : 1 + 0.12 * Math.sin(this.time.now / 140);
      for (const e of hits) {
        const ey = e.pos.y - 34 * (this.enemyViews.get(e.uid)?.air ?? 0);
        g.lineStyle(2.5, def.color, 0.95);
        g.strokeCircle(e.pos.x, ey, (e.def.radius + 5) * pulse);
      }
      label.setText(hits.length ? `${hits.length} ${hits.length === 1 ? 'foe' : 'foes'}` : 'No foes here');
      label.setColor(hits.length ? TEXT.cream : '#c8c0b0');
    }
    label.setPosition(x, Math.max(80, y - r - 18)).setVisible(true);
    label.setBackgroundColor('#16241cd0').setPadding(8, 3, 8, 3);
  }

  /** Hovering the hero's skill button: its reach around the hero, the foes it would hit and a count. */
  private drawSkillPreview(g: Phaser.GameObjects.Graphics, label: Phaser.GameObjects.Text): void {
    const h = this.sim.hero;
    if (!h || !h.alive) {
      label.setVisible(false);
      return;
    }
    const sk = h.def.active;
    const color = h.def.color;
    const r = sk.radius;
    g.fillStyle(color, 0.08);
    g.fillCircle(h.pos.x, h.pos.y, r);
    for (let k = 0; k < 3; k++) {
      g.lineStyle(4, color, 0.24 - k * 0.07);
      g.strokeCircle(h.pos.x, h.pos.y, r + 3 + k * 4);
    }
    const turn = motion.reduced ? 0 : -this.time.now / 1100;
    g.lineStyle(2, 0xffffff, 0.7);
    for (let k = 0; k < 18; k++) {
      const a0 = turn + (k / 18) * Math.PI * 2;
      g.beginPath();
      g.arc(h.pos.x, h.pos.y, r - 5, a0, a0 + 0.18);
      g.strokePath();
    }
    let text: string;
    if (sk.kind === 'rally') {
      const allies = this.sim.soldiers.filter((s) => s.alive && Math.hypot(s.pos.x - h.pos.x, s.pos.y - h.pos.y) <= r);
      g.lineStyle(2.5, 0x9be86a, 0.95);
      for (const s of allies) g.strokeCircle(s.pos.x, s.pos.y - 10, 14);
      text = `Heals ${allies.length} ${allies.length === 1 ? 'ally' : 'allies'} + ${h.def.name}`;
    } else {
      const hits = this.sim.heroSkillHits();
      const pulse = motion.reduced ? 1 : 1 + 0.12 * Math.sin(this.time.now / 140);
      g.lineStyle(2.5, color, 0.95);
      for (const e of hits) g.strokeCircle(e.pos.x, e.pos.y - 34 * (this.enemyViews.get(e.uid)?.air ?? 0), (e.def.radius + 5) * pulse);
      text = hits.length ? `${sk.name}: ${hits.length} ${hits.length === 1 ? 'foe' : 'foes'}` : `${sk.name}: no foes in reach`;
    }
    if (h.skillCd > 0) text += `  (ready in ${Math.ceil(h.skillCd)}s)`;
    label.setText(text).setColor(TEXT.cream).setBackgroundColor('#16241cd0').setPadding(8, 3, 8, 3);
    label.setPosition(Phaser.Math.Clamp(h.pos.x, label.width / 2 + 8, GAME_W - label.width / 2 - 8), Math.max(80, h.pos.y - r - 18)).setVisible(true);
  }

  /**
   * Touch aiming: the aim circle appears a little above the finger (so the finger doesn't hide it) and follows it;
   * the spell lands where the circle is when the finger lifts (see the scene's pointerup handler).
   */
  private beginTouchAim(p: Phaser.Input.Pointer): void {
    this.aimHold = true;
    this.reticle.setPosition(p.worldX, p.worldY - TOUCH_AIM_LIFT);
    this.showBanner(SPELLS[this.spellMode!].name, 'Drag to aim, lift to cast (lift on the spell bar to cancel)');
  }

  /** One-time card on a touch screen: hold to preview, drag to aim, drag the hero. Pauses until dismissed. */
  private showTouchTip(): void {
    const wasPaused = this.paused;
    this.paused = true;
    const W = 580;
    const c = this.add.container(GAME_W / 2, GAME_H / 2).setDepth(4900).setName('touchTip');
    const shade = this.add.rectangle(0, 0, GAME_W, GAME_H, 0x0a1410, 0.55).setInteractive();
    shade.on('pointerdown', (_p: Phaser.Input.Pointer, _x: number, _y: number, ev: Phaser.Types.Input.EventData) => ev.stopPropagation());
    const bg = this.add.graphics();
    c.add([shade, bg]);
    // lay the rows out top-down from their measured text heights (phone fonts are larger), then size the panel
    const items: { obj: Phaser.GameObjects.GameObject & { y: number }; y: number }[] = [];
    const title = this.add.text(0, 0, 'Playing on a touch screen', textStyle(pf(24), TEXT.gold)).setOrigin(0.5, 0);
    items.push({ obj: title, y: 0 });
    let y = title.height + 22;
    const ix = -W / 2 + 56;
    for (const tip of TOUCH_TIPS) {
      const head = this.add.text(ix + 46, 0, tip.title, textStyle(pf(17), TEXT.gold)).setOrigin(0, 0);
      const body = this.add.text(ix + 46, 0, tip.text, { ...textStyle(pf(14), TEXT.cream, false), wordWrap: { width: W - 140 } }).setOrigin(0, 0);
      const rowH = Math.max(56, head.height + 4 + body.height);
      const g = this.add.graphics();
      const cy = rowH / 2;
      g.fillStyle(0x24402c, 1);
      g.fillCircle(ix, cy, 26);
      g.lineStyle(2, 0x6ab04c, 0.8);
      g.strokeCircle(ix, cy, 26);
      // a fingertip, plus what the gesture does: rings for a hold, an arrow for a drag
      g.fillStyle(0xf2dcc0, 1);
      g.fillCircle(ix - 2, cy + 4, 8);
      g.fillRoundedRect(ix - 6, cy + 4, 8, 14, 3);
      if (tip.icon === 'hold') {
        g.lineStyle(2.5, 0xffd23c, 1);
        g.strokeCircle(ix - 2, cy + 4, 14);
        g.lineStyle(1.5, 0xffd23c, 0.5);
        g.strokeCircle(ix - 2, cy + 4, 19);
      } else {
        const col = tip.icon === 'drag' ? 0x9be86a : 0xffd23c;
        g.lineStyle(3, col, 1);
        g.lineBetween(ix + 6, cy - 4, ix + 18, cy - 16);
        g.fillStyle(col, 1);
        g.fillTriangle(ix + 20, cy - 18, ix + 12, cy - 17, ix + 19, cy - 10);
      }
      items.push({ obj: g as unknown as Phaser.GameObjects.GameObject & { y: number }, y });
      items.push({ obj: head, y: y + Math.max(0, (rowH - head.height - 4 - body.height) / 2) });
      items.push({ obj: body, y: y + Math.max(0, (rowH - head.height - 4 - body.height) / 2) + head.height + 4 });
      y += rowH + 12;
    }
    const H = 28 + y + 70;
    for (const it of items) {
      it.obj.y = -H / 2 + 26 + it.y;
      c.add(it.obj);
    }
    glossPanel(bg, -W / 2, -H / 2, W, H, { fill: C.ink, alpha: 0.97, rim: 0xc8a050, rimAlpha: 0.7, radius: 22 });
    const close = () => {
      const save = loadSave();
      save.settings.touchTipSeen = true;
      writeSave(save);
      c.destroy();
      this.paused = wasPaused;
    };
    c.add(new Button(this, 0, H / 2 - 44, 'Got it!', { width: 200, height: 52, fontSize: 22, color: C.leaf, onClick: close }));
    if (!motion.reduced) {
      c.setScale(0.85).setAlpha(0);
      this.tweens.add({ targets: c, scale: 1, alpha: 1, duration: 200, ease: 'Back.easeOut' });
    }
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
      // coming off cooldown: a radial ping in the spell's colour and a little icon pop
      const nowReady = cd <= 0;
      if (nowReady && !this.spellWasReady[id] && !this.ended) {
        readyPing(this, p.x, p.y, def.color);
        const icon = this.spellIcons[id];
        if (icon && !motion.reduced) this.tweens.add({ targets: icon, scale: 1.25, duration: 120, yoyo: true, ease: 'Back.easeOut' });
        if (!motion.reduced) {
          for (let k = 0; k < 8; k++) {
            const a = (k / 8) * Math.PI * 2;
            const sp = this.add.circle(p.x + Math.cos(a) * 30, p.y + Math.sin(a) * 30, 2.5, def.color).setDepth(3003).setBlendMode(Phaser.BlendModes.ADD);
            this.tweens.add({ targets: sp, x: p.x + Math.cos(a) * 52, y: p.y + Math.sin(a) * 52, alpha: 0, duration: 380, onComplete: () => sp.destroy() });
          }
        }
      }
      this.spellWasReady[id] = nowReady;
      g.fillStyle(C.ink, 0.85);
      g.fillCircle(p.x, p.y, 40);
      g.fillStyle(cd > 0 ? 0x3a4a3e : C.panelLight, 1);
      g.fillCircle(p.x, p.y, 35);
      const stalled = cd > 0 && this.sim.stallMult() < 1;
      if (cd > 0) {
        // Moon Hare hush: the recharge wedge turns a cold moonlit blue while it crawls
        g.fillStyle(stalled ? 0x2a3a6a : 0x000000, stalled ? 0.6 : 0.5);
        g.slice(p.x, p.y, 35, -Math.PI / 2, -Math.PI / 2 + Math.PI * 2 * (cd / this.sim.spellCooldown(id)), false);
        g.fillPath();
      }
      if (stalled) {
        // a little crescent moon badge on the button's shoulder
        g.fillStyle(0xe8ecff, 1);
        g.fillCircle(p.x + 26, p.y - 26, 8);
        g.fillStyle(C.ink, 1);
        g.fillCircle(p.x + 29, p.y - 28, 7);
      }
      // glassy highlight on the upper half and a soft shade at the bottom
      g.fillStyle(0xffffff, cd > 0 ? 0.06 : 0.16);
      g.fillEllipse(p.x, p.y - 17, 50, 24);
      g.lineStyle(3, 0x000000, 0.18);
      g.beginPath();
      g.arc(p.x, p.y, 32, 0.25, Math.PI - 0.25, false);
      g.strokePath();
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
    this.heroSprite.on('pointerdown', (p: Phaser.Input.Pointer, _x: number, _y: number, ev: Phaser.Types.Input.EventData) => {
      ev.stopPropagation();
      sfx.unlock();
      this.closeMenu();
      if (p.wasTouch) {
        // touch: drag from the hero to where they should go (a short tap still selects, as before)
        this.heroDrag = { x: p.worldX, y: p.worldY };
        this.heroDragTo = { x: p.worldX, y: p.worldY };
        return;
      }
      this.selectHero(!this.heroSelected);
    });
    this.heroBar = this.add.graphics();

    // HUD: portrait (select) + skill button, bottom-left.
    const px = 58;
    const py = GAME_H - 58;
    this.heroHud = this.add.graphics().setDepth(3000);
    const portrait = this.add.image(px, py + 6, `hero_${h.def.id}`).setDepth(3001).setScale(1.05);
    this.heroPortrait = portrait;
    portrait.setInteractive(new Phaser.Geom.Circle(26, 30, 40), Phaser.Geom.Circle.Contains);
    portrait.on('pointerdown', (_p: Phaser.Input.Pointer, _x: number, _y: number, ev: Phaser.Types.Input.EventData) => {
      ev.stopPropagation();
      sfx.unlock();
      sfx.click();
      this.closeMenu();
      const open = !this.heroCard;
      this.selectHero(open);
      if (this.enemyCard) this.openEnemyCard(null);
      this.toggleHeroCard(open);
    });
    this.heroLevelText = this.add.text(px + 30, py + 30, '1', textStyle(18, TEXT.gold)).setOrigin(0.5).setDepth(3002);
    const skillZone = this.add.zone(px + 104, py, 76, 76).setDepth(3002).setInteractive({ useHandCursor: true });
    skillZone.on('pointerover', () => (this.skillPreview = true));
    skillZone.on('pointerout', () => (this.skillPreview = false));
    const fireSkill = () => {
      if (!this.sim.useHeroSkill()) this.tweens.add({ targets: this.skillText, x: this.skillText.x + 4, duration: 40, yoyo: true, repeat: 2 });
    };
    skillZone.on('pointerdown', (p: Phaser.Input.Pointer, _x: number, _y: number, ev: Phaser.Types.Input.EventData) => {
      ev.stopPropagation();
      sfx.unlock();
      if (p.wasTouch) {
        // touch has no hover: hold to see the skill's reach, let go on the button to use it, slide off to cancel
        this.skillHold = true;
        this.skillPreview = true;
        return;
      }
      fireSkill();
    });
    skillZone.on('pointerup', (p: Phaser.Input.Pointer) => {
      if (!p.wasTouch || !this.skillHold) return;
      this.skillHold = false;
      this.skillPreview = false;
      fireSkill();
    });
    this.skillText = this.add.text(px + 104, py, h.def.active.name.replace(' ', '\n'), { ...textStyle(pf(13)), align: 'center' }).setOrigin(0.5).setDepth(3002);
    fitWidth(this.skillText, 68);
  }

  /** Level up: a gold flare bursts from the hero badge and its portrait pops. */
  private heroBadgeFlare(): void {
    const px = 58, py = GAME_H - 58;
    const ring = this.add.circle(px, py, 40, 0xffe27a, 0).setStrokeStyle(5, 0xffe27a, 1).setDepth(3003);
    this.tweens.add({ targets: ring, scale: 1.8, alpha: 0, duration: 520, onComplete: () => ring.destroy() });
    if (motion.reduced) return;
    for (let k = 0; k < 10; k++) {
      const a = (k / 10) * Math.PI * 2;
      const ray = this.add.rectangle(px, py, 18, 3, 0xfff0b0).setOrigin(0, 0.5).setRotation(a).setDepth(3003).setBlendMode(Phaser.BlendModes.ADD);
      this.tweens.add({ targets: ray, x: px + Math.cos(a) * 50, y: py + Math.sin(a) * 50, alpha: 0, duration: 480, ease: 'Quad.easeOut', onComplete: () => ray.destroy() });
    }
    if (this.heroPortrait) this.tweens.add({ targets: this.heroPortrait, scale: 1.3, duration: 140, yoyo: true });
    if (this.heroCard) this.toggleHeroCard(true); // fresh numbers for the new level
  }

  private selectHero(on: boolean): void {
    if (!this.sim.hero?.alive) on = false;
    this.heroSelected = on;
    this.heroRing?.setVisible(on);
    if (!on && this.heroCard && this.sim.hero?.alive) this.toggleHeroCard(false);
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
    const facing = h.facing < 0 ? -1 : 1;
    // run with a forward lean, swing while fighting, breathe while standing
    const pose = motion.reduced ? { lift: 0, sx: 1, sy: 1, rot: 0 } : unitPose(moving ? 'walk' : h.targetUid ? 'fight' : 'idle', this.time.now, 0.4, facing);
    const bob = moving ? pose.lift * 1.3 : 0;
    this.heroSprite.setVisible(h.alive).setPosition(h.pos.x, h.pos.y - bob).setDepth(h.pos.y).setFlipX(facing < 0).setScale(pose.sx, pose.sy).setRotation(pose.rot * (moving ? 1.4 : 1));
    this.heroRing.setPosition(h.pos.x, h.pos.y).setDepth(h.pos.y - 1);
    if (!h.alive && this.heroSelected) this.selectHero(false);
    this.heroBar.clear();
    if (this.heroCard && this.heroCardUntil && this.time.now > this.heroCardUntil) this.toggleHeroCard(false);
    if (h.alive) stepTrail(this.heroTrail, h.hp / h.maxHp, Math.min(this.game.loop.delta / 1000, 0.1));
    else this.heroTrail = newTrail(1);
    if (h.alive && h.hp < h.maxHp) {
      // the hero's bar is a touch longer and gold-rimmed so it stands out from the soldiers'
      const w = 38;
      const frac = Math.max(0, h.hp / h.maxHp);
      this.heroBar.fillStyle(0xc8a050, 0.8);
      this.heroBar.fillRoundedRect(h.pos.x - w / 2 - 3, h.pos.y - 64, w + 6, 10, 5);
      drawBar(this.heroBar, h.pos.x - w / 2, h.pos.y - 61.5, w, 5, frac, this.heroTrail.trail, hpColor(frac));
      this.heroBar.setDepth(h.pos.y + 0.5);
    }

    // HUD
    const px = 58;
    const py = GAME_H - 58;
    const g = this.heroHud;
    g.clear();
    // framed portrait: shadow, dark rim, a gold bevel, then the hero-tinted backdrop with a gloss
    g.fillStyle(0x000000, 0.3);
    g.fillCircle(px + 2, py + 3, 44);
    g.fillStyle(C.ink, 0.9);
    g.fillCircle(px, py, 44);
    g.lineStyle(2, 0xffe08a, 0.55);
    g.strokeCircle(px, py, 43);
    g.fillStyle(h.alive ? h.def.color : 0x553333, 1);
    g.fillCircle(px, py, 35);
    g.fillStyle(h.alive ? C.panelLight : 0x553333, 0.55);
    g.fillCircle(px, py + 4, 33);
    g.fillStyle(0xffffff, 0.14);
    g.fillEllipse(px - 6, py - 16, 40, 18);
    // xp track and arc, with a bright dot at its leading edge
    const next = HERO_XP[h.level] ?? HERO_XP[HERO_MAX_LEVEL - 1];
    const prev = HERO_XP[h.level - 1];
    const frac = h.level >= HERO_MAX_LEVEL ? 1 : (h.xp - prev) / Math.max(1, next - prev);
    g.lineStyle(5, 0x000000, 0.45);
    g.strokeCircle(px, py, 39);
    g.lineStyle(5, C.gold, 1);
    g.beginPath();
    g.arc(px, py, 39, -Math.PI / 2, -Math.PI / 2 + Math.PI * 2 * frac);
    g.strokePath();
    if (frac > 0.01 && frac < 1) {
      const a = -Math.PI / 2 + Math.PI * 2 * frac;
      g.fillStyle(0xfff6c8, 1);
      g.fillCircle(px + Math.cos(a) * 39, py + Math.sin(a) * 39, 3.5);
    }
    // down: a dark sweep that drains away as the respawn timer runs out, and a greyed portrait
    if (!h.alive) {
      const left = Math.max(0, Math.min(1, h.respawnTimer / Math.max(0.1, h.def.respawn)));
      g.fillStyle(0x000000, 0.55);
      g.slice(px, py, 35, -Math.PI / 2, -Math.PI / 2 + Math.PI * 2 * left, false);
      g.fillPath();
    }
    this.heroPortrait?.setTint(h.alive ? 0xffffff : 0x888888);
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
      const stalled = this.sim.stallMult() < 1;
      g.fillStyle(stalled ? 0x2a3a6a : 0x000000, stalled ? 0.6 : 0.45);
      g.slice(sx, py, 33, -Math.PI / 2, -Math.PI / 2 + Math.PI * 2 * cdFrac, false);
      g.fillPath();
      if (stalled) {
        g.fillStyle(0xe8ecff, 1);
        g.fillCircle(sx + 24, py - 24, 8);
        g.fillStyle(C.ink, 1);
        g.fillCircle(sx + 27, py - 26, 7);
      }
    }
    // glassy highlight, plus a breathing gold glow and a one-off ping when the skill comes off cooldown
    g.fillStyle(0xffffff, ready ? 0.16 : 0.06);
    g.fillEllipse(sx, py - 15, 46, 22);
    if (ready) {
      const t = motion.reduced ? 0.5 : (Math.sin(this.time.now / 260) + 1) / 2;
      g.lineStyle(6, 0xffe27a, 0.18 + 0.3 * t);
      g.strokeCircle(sx, py, 40 + t * 2);
      if (!this.skillWasReady && !motion.reduced) readyPing(this, sx, py, h.def.color);
    }
    this.skillWasReady = ready;
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
      shake(this, 260, 0.01);
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
    // enemies the player has never met get a NEW tag and go first in the strip
    const seen = new Set(loadSave().seenEnemies);
    const entries = [...counts.entries()].sort((a, b) => Number(seen.has(a[0])) - Number(seen.has(b[0]))).slice(0, 4);
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
      if (!seen.has(id)) {
        const glow = this.add.circle(x, 0, 16, 0xffe27a, 0.25).setBlendMode(Phaser.BlendModes.ADD);
        c.addAt(glow, 1);
        if (!motion.reduced) this.tweens.add({ targets: glow, scale: 1.3, alpha: 0.05, duration: 700, yoyo: true, repeat: -1 });
        const tag = this.add.container(x, -19);
        const pill = this.add.graphics();
        pill.fillStyle(0xffc83a, 1);
        const newT = this.add.text(0, 0, 'NEW', textStyle(pf(10), '#3a2408', false)).setOrigin(0.5);
        const pw = Math.max(34, newT.width + 10);
        const ph = Math.max(14, newT.height);
        pill.fillRoundedRect(-pw / 2, -ph / 2, pw, ph, ph / 2);
        pill.lineStyle(1.5, 0x5a3a0a, 1);
        pill.strokeRoundedRect(-pw / 2, -ph / 2, pw, ph, ph / 2);
        tag.add([pill, newT]);
        c.add(tag);
      }
    });
    // a short tip about the first brand-new enemy, shown once per battle under the strip
    const fresh = entries.find(([id]) => !seen.has(id) && !this.tipped.has(id));
    if (fresh) {
      this.tipped.add(fresh[0]);
      this.newEnemyTip(fresh[0], c.x, 66);
    }
    c.add(this.add.text(-w / 2 - 4, 0, 'Next', textStyle(pf(13), TEXT.dim)).setOrigin(1, 0.5));
  }

  private tipped = new Set<string>();

  /** "New: Name, key trait" under the next-wave strip for a few seconds. */
  private newEnemyTip(id: string, x: number, y: number): void {
    this.children.getByName('newEnemyTip')?.destroy();
    const def = ENEMIES[id];
    const text = this.add.text(0, 0, `New: ${def.name}  •  ${enemyKeyTrait(def)}`, textStyle(pf(13), TEXT.cream, false)).setOrigin(0.5);
    const w = text.width + 24;
    const tip = this.add.container(Math.min(GAME_W - w / 2 - 10, Math.max(w / 2 + 10, x)), y).setDepth(3001).setName('newEnemyTip').setAlpha(0);
    const bg = this.add.graphics();
    bg.fillStyle(C.ink, 0.88);
    bg.fillRoundedRect(-w / 2, -13, w, 26, 10);
    bg.lineStyle(2, 0xffc83a, 0.9);
    bg.strokeRoundedRect(-w / 2, -13, w, 26, 10);
    tip.add([bg, text]);
    this.tweens.add({ targets: tip, alpha: 1, y: y + 4, duration: 220 });
    this.tweens.add({ targets: tip, alpha: 0, delay: 6000, duration: 400, onComplete: () => tip.destroy() });
  }

  private drawBossBar(): void {
    this.bossBar.clear();
    const boss = this.sim.enemies.find((e) => e.alive && e.def.boss);
    this.bossLabel.setVisible(!!boss);
    if (!boss) return;
    const w = 420;
    const x = GAME_W / 2 - w / 2;
    const y = 104;
    const frac = Math.max(0, boss.hp / boss.maxHp);
    // a fresh boss starts a fresh trail
    if (this.bossTrailUid !== boss.uid) {
      this.bossTrailUid = boss.uid;
      this.bossTrail = newTrail(frac);
    }
    stepTrail(this.bossTrail, frac, Math.min(this.game.loop.delta / 1000, 0.1));
    this.bossBar.fillStyle(0x000000, 0.3);
    this.bossBar.fillRoundedRect(x - 4, y - 3, w + 12, 26, 12);
    this.bossBar.fillStyle(C.ink, 0.9);
    this.bossBar.fillRoundedRect(x - 6, y - 6, w + 12, 26, 12);
    this.bossBar.lineStyle(1.5, 0xff8a7a, 0.35);
    this.bossBar.strokeRoundedRect(x - 6, y - 6, w + 12, 26, 12);
    drawBar(this.bossBar, x, y, w, 14, frac, this.bossTrail.trail, frac > 0.3 ? C.danger : 0xff3a2a);
    if (boss.shield > 0) {
      this.bossBar.fillStyle(0x9fd8ff, 0.9);
      this.bossBar.fillRoundedRect(x, y + 10, Math.max(4, w * (boss.shield / Math.max(1, boss.maxShield))), 4, 2);
    }
    // phase notches: a little diamond at each threshold, gold once passed, cream while still ahead
    for (const ph of boss.def.phases ?? []) {
      const nx = x + w * ph.at;
      const passed = frac <= ph.at;
      this.bossBar.fillStyle(C.ink, 0.95);
      this.bossBar.fillTriangle(nx - 7, y - 4, nx + 7, y - 4, nx, y + 4);
      this.bossBar.fillStyle(passed ? 0xffd23c : C.cream, 1);
      this.bossBar.fillTriangle(nx - 5, y - 5, nx + 5, y - 5, nx, y + 2);
      this.bossBar.fillStyle(passed ? 0xffd23c : C.cream, passed ? 0.9 : 0.55);
      this.bossBar.fillRect(nx - 1, y, 2, 14);
    }
    // phase change: the bar flashes white and fades back
    const flash = this.bossFlashUntil - this.time.now;
    if (flash > 0) {
      this.bossBar.fillStyle(0xffffff, 0.75 * (flash / BOSS_FLASH_MS));
      this.bossBar.fillRoundedRect(x - 6, y - 6, w + 12, 26, 12);
    }
    if (boss.def.wax && boss.waxLeft > 0) {
      // a wax-coated boss: a glossy amber strip under the bar that drains as spells melt the coat
      const full = Math.max(1, Math.round(boss.maxHp * boss.def.wax.melt));
      this.bossBar.fillStyle(C.ink, 0.85);
      this.bossBar.fillRoundedRect(x - 2, y + 19, w + 4, 7, 3);
      this.bossBar.fillStyle(0xf0b840, 1);
      this.bossBar.fillRect(x, y + 21, w * Math.min(1, boss.waxLeft / full), 3);
    }
    if (boss.def.parry) {
      // comb-shield charges: amber cells to the right of the bar (dim when spent)
      for (let k = 0; k < boss.def.parry.charges; k++) {
        const px = x + w + 22 + k * 15;
        this.bossBar.fillStyle(C.ink, 0.85);
        this.bossBar.fillCircle(px, y + 7, 7);
        this.bossBar.fillStyle(k < boss.parryCharges ? 0xffc83a : 0x5a4a2a, 1);
        this.bossBar.fillCircle(px, y + 7, 5);
      }
    }
    if (boss.def.curl) {
      // a curling boss: a coil badge right of the bar. Steel and outlined while curled up (hits glance off),
      // a dim ring refilling while the curl recharges, and rust-red once it is ready to curl again.
      const cxb = x + w + 24;
      const cyb = y + 7;
      this.bossBar.fillStyle(C.ink, 0.85);
      this.bossBar.fillCircle(cxb, cyb, 9);
      if (boss.curlT > 0) {
        this.bossBar.fillStyle(0xc8d0d8, 1);
        this.bossBar.fillCircle(cxb, cyb, 7);
        this.bossBar.lineStyle(2, 0xc8d0d8, 0.9);
        this.bossBar.strokeRect(x - 2, y - 2, w + 4, 18);
      } else if (boss.curlCd > 0) {
        this.bossBar.fillStyle(0x4a3a30, 1);
        this.bossBar.fillCircle(cxb, cyb, 7);
        this.bossBar.lineStyle(3, 0xa84a2a, 1);
        const frac = 1 - Math.min(1, boss.curlCd / boss.def.curl.cooldown);
        this.bossBar.beginPath();
        this.bossBar.arc(cxb, cyb, 5, -Math.PI / 2, -Math.PI / 2 + frac * Math.PI * 2);
        this.bossBar.strokePath();
      } else {
        this.bossBar.fillStyle(0xa84a2a, 1);
        this.bossBar.fillCircle(cxb, cyb, 7);
      }
      this.bossBar.lineStyle(1.5, C.ink, 1);
      this.bossBar.strokeCircle(cxb, cyb, 3.5);
    }
    this.bossLabel.setText(boss.def.name);
  }

  private refreshHud(dt = 0): void {
    if (!this.cheapestTower) this.cheapestTower = Math.min(...Object.values(TOWERS).map((t) => this.sim.price(t.tiers[0].cost)));
    const canBuild = this.sim.isActive() && this.sim.coins >= this.cheapestTower;
    this.padGlows.forEach((g, i) => g.setVisible(canBuild && !this.sim.towers[i]));
    // rolling counters: snap on the first frame (or with Reduce Motion), then tick toward the real value
    const snap = this.shownCoins < 0 || motion.reduced || dt === 0;
    const coins = snap ? this.sim.coins : stepCounter(this.shownCoins, this.sim.coins, dt);
    const lives = snap ? this.sim.lives : stepCounter(this.shownLives, this.sim.lives, dt);
    // long numbers (dev mode, late-game hoards) shrink so they never run past the bar's dividers
    if (Math.round(coins) !== Math.round(this.shownCoins)) {
      const t = String(Math.round(coins));
      this.coinText.setText(t).setFontSize(t.length >= 6 ? 19 : t.length === 5 ? 23 : 26);
    }
    if (Math.round(lives) !== Math.round(this.shownLives)) {
      const t = String(Math.round(lives));
      this.livesText.setText(t).setFontSize(t.length >= 4 ? 18 : t.length === 3 ? 22 : 26);
    }
    this.shownCoins = coins;
    this.shownLives = lives;
    this.drawWaveBar(dt);
    const cut = this.sim.titheCut();
    const stall = this.sim.stallMult();
    const warn: string[] = [];
    if (cut > 0) warn.push(`Weasel tithe: kills pay -${Math.round(cut * 100)}%`);
    if (stall < 1) warn.push(`Moonhush: spells recharge -${Math.round((1 - stall) * 100)}%`);
    this.titheText.setVisible(warn.length > 0);
    if (warn.length) this.titheText.setText(warn.join('  •  '));
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
    this.drawCallFx();
  }

  /** The wave button's glow, countdown strip and early-call bonus chip. */
  private drawCallFx(): void {
    const g = this.callG;
    const strip = this.callStrip;
    const chip = this.callChip;
    if (!g || !strip || !chip) return;
    g.clear();
    strip.clear();
    const active = !this.ended && this.sim.wavesRemaining && this.sim.isActive();
    const c = Math.max(0, this.sim.waveCountdown);
    if (c > this.callLast + 0.5) this.callFull = Math.max(1, c); // a fresh countdown started
    this.callLast = c;
    if (!active) {
      chip.setVisible(false);
      return;
    }
    const x = GAME_W - 130;
    const y = 40;
    const pulse = motion.reduced ? 0.5 : 0.5 + 0.5 * Math.sin(this.time.now / 260);
    // the first wave glows more: it's the "press me" moment
    const base = this.sim.waveIndex < 0 ? 0.28 : 0.16;
    for (let k = 0; k < 3; k++) {
      g.fillStyle(0xffb84a, (base + 0.12 * pulse) * (1 - k * 0.3));
      g.fillRoundedRect(x - 114 - k * 4, y - 30 - k * 4, 228 + k * 8, 60 + k * 8, 18 + k * 4);
    }
    const frac = Phaser.Math.Clamp(c / this.callFull, 0, 1);
    if (frac > 0) {
      strip.fillStyle(0x000000, 0.35);
      strip.fillRoundedRect(x - 96, y + 15, 192, 5, 2.5);
      strip.fillStyle(0xfff2c0, 0.95);
      strip.fillRoundedRect(x - 96, y + 15, Math.max(5, 192 * frac), 5, 2.5);
    }
    const bonus = this.sim.callBonus();
    chip.setVisible(bonus > 0);
    if (bonus > 0) chip.setText(`Call now: +${bonus} coins`);
  }

  /** Slim progress bar under the wave counter: how far through the level's waves we are. */
  private drawWaveBar(dt: number): void {
    const target = this.endless ? 0 : waveProgress(this.sim.waveIndex, this.sim.totalWaves);
    const v = this.shownWave < 0 || dt === 0 ? target : this.shownWave + (target - this.shownWave) * Math.min(1, dt * 4);
    if (Math.abs(v - this.shownWave) < 0.0005) return;
    this.shownWave = v;
    const g = this.waveBar;
    g.clear();
    if (this.endless) return;
    const x = 282, y = 52, w = 156, h = 7;
    g.fillStyle(0x000000, 0.45);
    g.fillRoundedRect(x, y, w, h, 3.5);
    if (v > 0.01) {
      const fw = Math.max(h, w * v);
      g.fillStyle(0xff9f43, 1);
      g.fillRoundedRect(x, y, fw, h, 3.5);
      g.fillStyle(0xffe0a0, 0.6);
      g.fillRoundedRect(x + 2, y + 1, fw - 4, 2, 1);
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
    const shade = this.add.rectangle(0, 0, GAME_W, GAME_H, 0x0a1410, 0.55).setInteractive();
    shade.on('pointerdown', (_p: Phaser.Input.Pointer, _x: number, _y: number, ev: Phaser.Types.Input.EventData) => ev.stopPropagation());
    // a darker rim around the screen so the panel sits in a pool of light
    const rim = this.add.image(-GAME_W / 2, -GAME_H / 2, 'fx_vignette').setOrigin(0, 0).setAlpha(0.9);
    const bg = this.add.graphics();
    bg.fillStyle(0x000000, 0.35);
    bg.fillRoundedRect(-194, -182, 400, 392, 26);
    bg.fillStyle(C.ink, 1);
    bg.fillRoundedRect(-200, -190, 400, 392, 26);
    bg.fillStyle(C.panel, 0.97);
    bg.fillRoundedRect(-192, -182, 384, 376, 22);
    bg.fillStyle(0xffffff, 0.05);
    bg.fillRoundedRect(-188, -178, 376, 70, { tl: 20, tr: 20, bl: 6, br: 6 });
    bg.lineStyle(2, 0xc8a050, 0.6);
    bg.strokeRoundedRect(-196, -186, 392, 384, 24);
    c.add([shade, rim, bg, ribbon(this, -150, 260, 0x3a6a8a, 0x1a3a5a), this.add.text(0, -150, 'Paused', textStyle(40, '#e8f4ff')).setOrigin(0.5).setStroke('#0a1a2a', 8)]);
    // where you are: level, wave and lives at a glance
    const wave = `${Math.max(0, this.sim.waveIndex + 1)}/${this.endless ? '∞' : this.sim.totalWaves}`;
    c.add(fitWidth(this.add.text(0, -98, `${this.level.name}  •  Wave ${wave}  •  ${this.sim.lives} lives`, textStyle(pf(14), TEXT.cream, false)).setOrigin(0.5), 340));
    const soundLabel = () => (loadSave().settings.muted ? 'Sound: Off' : 'Sound: On');
    const items: [string, number, () => void][] = [
      ['Resume', C.leaf, () => this.togglePause()],
      ['Restart', C.sky, () => this.scene.restart({ levelIndex: this.levelIndex, daily: !!this.daily, endless: this.endless })],
      [soundLabel(), 0xb07cff, () => {}],
      ['Quit to Map', 0xff9f43, () => this.scene.start('WorldMap', { focus: this.levelIndex })],
    ];
    items.forEach(([label, color, fn], i) => {
      const b = new Button(this, 0, -46 + i * 64, label, { width: 260, height: 54, fontSize: 22, color, onClick: fn });
      if (!motion.reduced) {
        b.setScale(0.6).setAlpha(0);
        this.tweens.add({ targets: b, scale: 1, alpha: 1, delay: 60 + i * 50, duration: 180, ease: 'Back.easeOut' });
      }
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
    this.rangeDash?.setVisible(false);
  }

  private drawRange(pos: Vec2, range: number, color: number): void {
    const g = this.rangeRing;
    g.clear();
    // a soft field that brightens toward the edge (nested rings), so the reach reads at a glance
    for (let k = 0; k < 5; k++) {
      g.fillStyle(color, 0.035 + k * 0.012);
      g.fillCircle(pos.x, pos.y, range * (1 - k * 0.06));
    }
    g.fillStyle(0xffffff, 0.04);
    g.fillCircle(pos.x, pos.y, range * 0.25);
    g.lineStyle(6, color, 0.18);
    g.strokeCircle(pos.x, pos.y, range - 2);
    // a dashed rim that slowly turns
    if (!this.rangeDash) this.rangeDash = this.add.graphics().setDepth(5.1);
    const d = this.rangeDash;
    d.clear().setPosition(pos.x, pos.y).setVisible(true).setAngle(0);
    d.lineStyle(3, color, 0.85);
    const n = Math.max(16, Math.round(range / 9));
    for (let k = 0; k < n; k++) {
      const a0 = (k / n) * Math.PI * 2;
      d.beginPath();
      d.arc(0, 0, range, a0, a0 + (Math.PI * 2) / n * 0.55);
      d.strokePath();
    }
    this.tweens.killTweensOf(d);
    if (!motion.reduced) this.tweens.add({ targets: d, angle: 360, duration: 16000, repeat: -1 });
  }

  private openSlotMenu(slot: number): void {
    this.closeMenu();
    // one card at a time: a tower menu ends the hero's move selection and closes the hero card
    if (this.heroSelected) this.selectHero(false);
    if (this.heroCard) this.toggleHeroCard(false);
    if (this.enemyCard) this.openEnemyCard(null);
    if (!this.sim.isActive()) return;
    const tower = this.sim.towers[slot];
    const pos = this.level.slots[slot];
    const c = this.add.container(pos.x, pos.y).setDepth(3500);
    this.menu = c;

    const ring = this.add.graphics();
    ring.lineStyle(3, C.cream, 0.55);
    for (let k = 0; k < 24; k++) {
      const a0 = (k / 24) * Math.PI * 2;
      ring.beginPath();
      ring.arc(0, 0, 70, a0, a0 + 0.16);
      ring.strokePath();
    }
    c.add(ring);
    this.popIndex = 0;

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
            c.getByName('towerCard')?.destroy();
            c.add(this.towerCard(tower, pos, sp.stats, sp.name));
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
            this.showBanner('Rally Point', this.input.activePointer.wasTouch ? 'Drag the flag onto the road inside the circle' : 'Tap the road inside the circle to send your Wardens there');
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
      c.add(this.towerCard(tower, pos, upCost !== null && !this.sim.canSpecialize(tower) ? tower.def.tiers[tower.tier + 1] : null));
    }
    c.setScale(0.5);
    this.tweens.add({ targets: c, scale: 1, duration: 160, ease: 'Back.easeOut' });
  }

  /** Stat bars on an info card: label, a bar with the next step as a green extension, and `cur → next` text. */
  private drawCardRows(card: Phaser.GameObjects.Container, g: Phaser.GameObjects.Graphics, rows: CardRow[], y0: number, W: number, color: number): void {
    // the label column is as wide as its longest label (66..96 px); labels share one size if they still need shrinking
    const labels = rows.map((r) => this.add.text(10, 0, r.label, textStyle(pf(11), TEXT.cream, false)).setOrigin(0, 0.5));
    const maxW = Math.max(...labels.map((l) => l.width));
    const bx = Phaser.Math.Clamp(Math.ceil(10 + maxW + 8), 66, 96);
    const bw = W - bx - 88;
    const sc = Math.min(1, (bx - 14) / maxW);
    rows.forEach((r, i) => {
      const y = y0 + i * 22;
      card.add(labels[i].setY(y).setScale(sc));
      g.fillStyle(0x0c1a12, 1);
      g.fillRoundedRect(bx, y - 4, bw, 8, 4);
      if (r.next !== null && r.next > r.value) {
        g.fillStyle(0x7be35a, 0.95);
        g.fillRoundedRect(bx, y - 4, Math.max(8, bw * r.next), 8, 4);
      }
      g.fillStyle(r.next !== null && r.next < r.value ? 0xff9f6a : color, 1);
      g.fillRoundedRect(bx, y - 4, Math.max(8, bw * r.value), 8, 4);
      g.fillStyle(0xffffff, 0.3);
      g.fillRect(bx + 3, y - 3, Math.max(2, bw * r.value - 6), 1.5);
      const txt = r.nextText ? `${r.text} → ${r.nextText}` : r.text;
      card.add(fitWidth(this.add.text(W - 8, y, txt, textStyle(pf(11), r.nextText ? '#b8ff8a' : TEXT.cream, false)).setOrigin(1, 0.5), 76));
    });
  }

  /**
   * Hero card above the portrait: name and title, level with an XP track (or the respawn countdown), health /
   * damage / speed bars with the next level's gain in green, and the passive and active skill texts.
   */
  private toggleHeroCard(open: boolean): void {
    this.heroCard?.destroy();
    this.heroCard = null;
    const h = this.sim.hero;
    if (!open || !h) return;
    const W = 320;
    const card = this.add.container(12, 0).setDepth(3500).setName('heroCard');
    const bg = this.add.graphics();
    const g = this.add.graphics();
    card.add([bg, g]);
    card.add(fitWidth(this.add.text(12, 8, `${h.def.name}, ${h.def.title}`, textStyle(pf(16), TEXT.gold)), W - 24));
    if (h.alive) {
      const xp = heroXpProgress(h.xp, h.level);
      card.add(fitWidth(this.add.text(12, 38, `Level ${h.level}`, textStyle(pf(12), TEXT.cream, false)).setOrigin(0, 0.5), 64));
      g.fillStyle(0x0c1a12, 1);
      g.fillRoundedRect(84, 34, 130, 8, 4);
      g.fillStyle(0xffd23c, 1);
      g.fillRoundedRect(84, 34, Math.max(8, 130 * xp.frac), 8, 4);
      card.add(fitWidth(this.add.text(W - 10, 38, xp.max ? 'Max level' : `${Math.floor(xp.have)}/${xp.need} XP`, textStyle(pf(11), '#ffe9a0', false)).setOrigin(1, 0.5), W - 226));
    } else {
      card.add(this.add.text(12, 38, `Recovering: back in ${Math.ceil(h.respawnTimer)}s`, textStyle(pf(12), TEXT.heart, false)).setOrigin(0, 0.5));
    }
    this.drawCardRows(card, g, heroCardRows(h.def, h.level), 62, W, h.def.color);
    let y = 62 + 3 * 22 - 4;
    const para = (head: string, body: string, color: string) => {
      const hd = fitWidth(this.add.text(12, y, head, textStyle(pf(11), color, false)), W - 24);
      const t = this.add.text(12, y + hd.displayHeight - 2, body, { ...textStyle(pf(11), TEXT.cream, false), wordWrap: { width: W - 24 } });
      card.add([hd, t]);
      y = t.y + t.height + 6;
    };
    para('Passive', h.def.passive.text, '#9be86a');
    para(`Skill: ${h.def.active.name} (${Math.round(h.def.active.cooldown)}s)`, h.def.active.text, '#ffc870');
    const H = y + 6;
    glossPanel(bg, 0, 0, W, H, { fill: C.ink, alpha: 0.95, rim: h.def.color, rimAlpha: 0.75, radius: 14 });
    card.setY(GAME_H - 112 - H);
    if (!motion.reduced) {
      card.setAlpha(0).setY(card.y + 12);
      this.tweens.add({ targets: card, alpha: 1, y: card.y - 12, duration: 160, ease: 'Cubic.easeOut' });
    }
    this.heroCard = card;
    // a fallen hero's card is just a status glance: it closes by itself
    this.heroCardUntil = h.alive ? 0 : this.time.now + 4000;
  }

  /** A small card that follows a tapped enemy: name, live health bar, armor / magic resist / speed, key trait. */
  private openEnemyCard(e: Enemy | null): void {
    this.enemyCard?.destroy();
    this.enemyCard = null;
    this.enemyCardUid = 0;
    if (!e) return;
    sfx.click();
    const W = 236;
    const card = this.add.container(0, 0).setDepth(3400).setName('enemyCard');
    const bg = this.add.graphics();
    const bar = this.add.graphics();
    card.add([bg, bar]);
    card.add(fitWidth(this.add.text(10, 8, e.def.boss ? `${e.def.name}  (boss)` : e.def.name, textStyle(pf(14), '#ffb89a')), W - 20));
    const hp = this.add.text(W - 10, 36, '', textStyle(pf(11), TEXT.cream, false)).setOrigin(1, 0.5);
    card.add(hp);
    const stats = `Armor ${Math.round(e.def.armor * 100)}%  •  Magic res ${Math.round(e.def.magicResist * 100)}%  •  Speed ${Math.round(e.def.speed)}`;
    // stats wrap rather than shrink, so they stay readable on a phone
    const st = this.add.text(10, 44, stats.replace(/ {2}• {2}/g, ' • '), { ...textStyle(pf(11), '#c8d8c8', false), wordWrap: { width: W - 20 } });
    const trait = this.add.text(10, st.y + st.height + 3, enemyKeyTrait(e.def), { ...textStyle(pf(11), TEXT.cream, false), wordWrap: { width: W - 20 } });
    card.add([st, trait]);
    const H = trait.y + trait.height + 10;
    glossPanel(bg, 0, 0, W, H, { fill: C.ink, alpha: 0.94, rim: 0xff7a5a, rimAlpha: 0.7, radius: 12 });
    card.setData({ W, H, bar, hp, trail: newTrail(Math.max(0, e.hp / e.maxHp)) });
    this.enemyCard = card;
    this.enemyCardUid = e.uid;
    this.updateEnemyCard(0);
    if (!motion.reduced) {
      card.setAlpha(0);
      this.tweens.add({ targets: card, alpha: 1, duration: 140 });
    }
  }

  /** Keep the enemy card above its foe and its health bar live; close it when the foe is gone. */
  private updateEnemyCard(dt: number): void {
    const card = this.enemyCard;
    if (!card) return;
    const e = this.sim.enemies.find((x) => x.uid === this.enemyCardUid);
    if (!e || e.hp <= 0) {
      this.openEnemyCard(null);
      return;
    }
    const W = card.getData('W') as number;
    const H = card.getData('H') as number;
    const frac = Math.max(0, e.hp / e.maxHp);
    const trail = stepTrail(card.getData('trail') as TrailState, frac, dt);
    const bar = card.getData('bar') as Phaser.GameObjects.Graphics;
    bar.clear();
    drawBar(bar, 10, 32, W - 92, 7, frac, trail.trail, hpColor(frac));
    (card.getData('hp') as Phaser.GameObjects.Text).setText(`${Math.ceil(e.hp)}/${Math.round(e.maxHp)}`);
    const v = this.enemyViews.get(e.uid);
    const top = e.pos.y - 34 * (v?.air ?? (e.def.flying ? 1 : 0)) - e.def.radius;
    let y = top - 26 - H;
    if (y < 70) y = e.pos.y + e.def.radius + 16; // no room above: hang the card below the foe
    card.setPosition(Phaser.Math.Clamp(e.pos.x - W / 2, 8, GAME_W - W - 8), Math.min(y, GAME_H - H - 100));
  }

  /** A tower's 50th kill: a small gold star pops onto its shoulder with a ring of sparkles, and stays. */
  private addVeteranBadge(uid: number): void {
    const t = this.sim.towers.find((x) => x?.uid === uid);
    if (!t || this.veteranBadges.has(uid)) return;
    const x = t.pos.x + 22;
    const y = t.pos.y - 40;
    const badge = this.add.container(x, y).setDepth(t.pos.y + 2);
    const g = this.add.graphics();
    g.fillStyle(0x16241c, 0.9);
    g.fillCircle(0, 0, 10);
    g.lineStyle(2, 0xffd23c, 1);
    g.strokeCircle(0, 0, 10);
    const star: Phaser.Math.Vector2[] = [];
    for (let k = 0; k < 10; k++) {
      const a = -Math.PI / 2 + (k * Math.PI) / 5;
      const r = k % 2 ? 3 : 7;
      star.push(new Phaser.Math.Vector2(Math.cos(a) * r, Math.sin(a) * r));
    }
    g.fillStyle(0xffd23c, 1);
    g.fillPoints(star, true);
    badge.add(g);
    this.veteranBadges.set(uid, badge);
    this.floatText(t.pos.x, t.pos.y - 60, 'Veteran!', TEXT.gold, 18);
    if (!motion.reduced) {
      badge.setScale(0);
      this.tweens.add({ targets: badge, scale: 1, duration: 260, ease: 'Back.easeOut' });
      this.particles.setParticleTint(0xffd23c);
      this.particles.explode(motion.lowFx ? 6 : 14, x, y);
    }
  }

  /**
   * Info card beside the tower menu: name and level, trait tags, and three stat bars. `next` (the next tier,
   * or the branch you just tapped) shows as a green extension of each bar that grows.
   */
  private towerCard(tower: Tower, pos: Vec2, next: TowerTier | null, nextName?: string): Phaser.GameObjects.Container {
    const W = 226;
    const right = pos.x < GAME_W - 370;
    const x0 = right ? 118 : -118 - W;
    const card = this.add.container(x0, 0).setName('towerCard');
    const g = this.add.graphics();
    card.add(g);
    const cur = this.sim.stats(tower);
    const title = tower.spec ? tower.def.specs.find((x) => x.id === tower.spec)!.name : `${tower.def.name}  Lv ${tower.tier + 1}`;
    const titleT = fitWidth(this.add.text(10, 8, title, textStyle(pf(15), TEXT.gold)), W - 20);
    const tags = cardTags(tower.def, cur).join(' • ');
    const tagsT = fitWidth(this.add.text(10, titleT.y + titleT.displayHeight - 1, tags, textStyle(pf(11), '#b8d0c0', false)), W - 20);
    card.add([titleT, tagsT]);
    // rows start below the tags and the card grows to fit, so bigger phone text never overlaps
    const rows = cardRows(cur, next);
    const y0 = Math.max(52, tagsT.y + tagsT.displayHeight + 11);
    const H = Math.max(132, y0 + (rows.length - 1) * 22 + 38);
    card.y = Phaser.Math.Clamp(pos.y - H / 2, 70, GAME_H - H - 106) - pos.y; // clear of the HUD and the spell buttons
    glossPanel(g, 0, 0, W, H, { fill: C.ink, alpha: 0.94, rim: tower.def.color, rimAlpha: 0.7, radius: 12 });
    this.drawCardRows(card, g, rows, y0, W, tower.def.color);
    if (next) card.add(fitWidth(this.add.text(10, H - 14, nextName ? `Branch: ${nextName}` : 'Green: next level', textStyle(pf(10), '#9be86a', false)).setOrigin(0, 0.5), W / 2 - 14));
    // this run's record: kills and damage, gold once it's a veteran
    const rec = towerRecord(tower.uid, this.sim.dmgBy, this.sim.killsBy);
    card.add(
      fitWidth(
        this.add.text(W - 10, H - 14, `${rec.veteran ? '★ ' : ''}${rec.kills} kills • ${shortNum(rec.damage)} dmg`, textStyle(pf(10), rec.veteran ? TEXT.gold : '#c8d8c8', false)).setOrigin(1, 0.5).setName('towerRecord'),
        next ? W / 2 - 14 : W - 20,
      ),
    );
    return card;
  }

  private placeRally(slot: number, p: Vec2, touch = false): void {
    const t = this.sim.towers[slot];
    const snap = t ? snapRally(this.sim.paths, p, t.pos, this.sim.stats(t).range) : { point: null, ok: false };
    const placed = !!snap.point && snap.ok && this.sim.setRally(slot, snap.point);
    if (!placed && touch) {
      // keep the circle up so the player can drag again
      this.floatText(p.x, p.y, snap.point ? 'Out of reach!' : 'Drop it on the road', TEXT.heart, 18);
      return;
    }
    this.rallyMode = null;
    this.rangeRing.clear();
    this.rangeDash?.setVisible(false);
    this.children.getByName('banner')?.destroy();
    if (placed && t && snap.point) {
      this.updateRallyFlag(t.uid, snap.point);
      sfx.click();
    } else {
      this.floatText(p.x, p.y, 'Out of reach!', TEXT.heart, 18);
    }
  }

  /** Touch hero drag: a dashed trail from the hero to the finger and a gold ring where they'll stand. */
  private drawHeroDrag(): void {
    const g = this.heroDragG;
    if (!g) return;
    g.clear();
    const h = this.sim.hero;
    const to = this.heroDragTo;
    if (!this.heroDrag || !to || !h?.alive) return;
    if (Math.hypot(to.x - this.heroDrag.x, to.y - this.heroDrag.y) <= HERO_DRAG_MIN) return; // still a tap
    const dx = to.x - h.pos.x;
    const dy = to.y - h.pos.y;
    const len = Math.hypot(dx, dy);
    const shift = motion.reduced ? 0 : (this.time.now / 30) % 18;
    g.lineStyle(3, C.gold, 0.85);
    for (let d = shift; d + 9 < len; d += 18) {
      g.lineBetween(h.pos.x + (dx * d) / len, h.pos.y + (dy * d) / len, h.pos.x + (dx * (d + 9)) / len, h.pos.y + (dy * (d + 9)) / len);
    }
    g.fillStyle(C.gold, 0.18);
    g.fillEllipse(to.x, to.y, 56, 22);
    g.lineStyle(3, C.gold, 1);
    g.strokeEllipse(to.x, to.y, 56, 22);
  }

  /** Touch rally drag: a ghost flag above the finger, snapped onto the road, green when it can be planted. */
  private drawRallyGhost(): void {
    const g = this.rallyG;
    if (!g) return;
    g.clear();
    const slot = this.rallyMode;
    if (!this.rallyDrag || slot === null || !this.rallyFinger) {
      this.rallyGhost?.setVisible(false);
      return;
    }
    const t = this.sim.towers[slot];
    if (!t) return;
    const at = { x: this.rallyFinger.x, y: this.rallyFinger.y - TOUCH_AIM_LIFT };
    const snap = snapRally(this.sim.paths, at, t.pos, this.sim.stats(t).range);
    const spot = snap.point ?? at;
    const color = snap.ok ? 0x7be35a : 0xff5d4a;
    if (snap.point) {
      g.lineStyle(2, 0xffffff, 0.5);
      g.lineBetween(at.x, at.y, spot.x, spot.y);
    }
    g.fillStyle(color, 0.22);
    g.fillEllipse(spot.x, spot.y, 46, 20);
    g.lineStyle(2.5, color, 0.95);
    g.strokeEllipse(spot.x, spot.y, 46, 20);
    if (!this.rallyGhost) this.rallyGhost = this.add.image(0, 0, 'rally').setDepth(3300);
    this.rallyGhost.setPosition(spot.x + 6, spot.y - 10).setVisible(true).setAlpha(snap.ok ? 0.95 : 0.5).setTint(snap.ok ? 0xffffff : 0xff9a8a);
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
    // glossy disc: shadow, dark body, gold (or grey) rim, a soft top gloss
    bg.fillStyle(0x000000, 0.3);
    bg.fillCircle(2, 3, 38);
    bg.fillStyle(C.ink, 0.92);
    bg.fillCircle(0, 0, 38);
    bg.fillStyle(affordable ? 0x3a5a3a : 0x3a3a3a, 0.9);
    bg.fillCircle(0, 2, 33);
    bg.fillStyle(0xffffff, affordable ? 0.14 : 0.06);
    bg.fillEllipse(-4, -16, 46, 20);
    bg.lineStyle(3, affordable ? C.gold : 0x777777, 1);
    bg.strokeCircle(0, 0, 38);
    const icon = this.add.image(0, -6, tex).setScale(0.6);
    // the price sits on a little tag with a coin; red with a lock when you can't afford it
    const tag = this.add.graphics();
    tag.fillStyle(affordable ? 0x2a2010 : 0x3a1414, 0.95);
    tag.fillRoundedRect(-28, 22, 56, 20, 10);
    tag.lineStyle(2, affordable ? 0xffc83a : 0xd05a5a, 1);
    tag.strokeRoundedRect(-28, 22, 56, 20, 10);
    tag.fillStyle(affordable ? 0xffd23c : 0xd05a5a, 1);
    if (affordable) tag.fillCircle(-17, 32, 5);
    else {
      tag.fillRect(-21, 31, 8, 6); // a tiny padlock
      tag.lineStyle(2, 0xd05a5a, 1);
      tag.beginPath();
      tag.arc(-17, 31, 3, Math.PI, 0);
      tag.strokePath();
    }
    const label = this.add.text(4, 32, cost, textStyle(15, affordable ? TEXT.gold : '#ff9a8a')).setOrigin(0.5);
    o.add([bg, icon, tag, label]);
    if (!affordable) icon.setTint(0x777777);
    o.setSize(76, 76).setInteractive({ useHandCursor: true });
    o.on('pointerover', () => !motion.reduced && this.tweens.add({ targets: o, scale: 1.08, duration: 90 }));
    o.on('pointerout', () => !motion.reduced && this.tweens.add({ targets: o, scale: 1, duration: 90 }));
    this.popIn(o);
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

  /** Menu buttons pop in one after another. */
  private popIndex = 0;
  private popIn(o: Phaser.GameObjects.Container): void {
    if (motion.reduced) return;
    o.setScale(0.2);
    this.tweens.add({ targets: o, scale: 1, duration: 200, delay: (this.popIndex++ % 8) * 35, ease: 'Back.easeOut' });
  }

  private textOption(x: number, y: number, text: string, color: number, onPick: () => void): Phaser.GameObjects.Container {
    const o = this.add.container(x, y);
    const bg = this.add.graphics();
    bg.fillStyle(0x000000, 0.3);
    bg.fillCircle(2, 3, 34);
    bg.fillStyle(C.ink, 0.92);
    bg.fillCircle(0, 0, 34);
    bg.fillStyle(0xffffff, 0.1);
    bg.fillEllipse(-3, -14, 42, 18);
    bg.lineStyle(3, color, 1);
    bg.strokeCircle(0, 0, 34);
    o.add([bg, this.add.text(0, 0, text, { ...textStyle(pf(14)), align: 'center' }).setOrigin(0.5)]);
    o.setSize(68, 68).setInteractive({ useHandCursor: true });
    this.popIn(o);
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
    if (devOn() && !this.ended) this.devTopUp();
    // a boss kill slows everything down for a moment, then eases back to full speed
    const slow = this.slowMoStart ? slowMoScale(this.time.now - this.slowMoStart, motion.reduced ? SLOWMO_MS / 2 : SLOWMO_MS) : 1;
    if (slow >= 1) this.slowMoStart = 0;
    if (!this.paused && !this.ended && this.time.now >= this.hitStopUntil) this.sim.update(dt * this.speed * slow);
    for (const ev of this.sim.drainEvents()) this.handleEvent(ev);
    this.syncViews(dt);
    this.drawAim();
    this.drawRallyGhost();
    this.drawHeroDrag();
    this.syncHero();
    this.drawSpellHud();
    this.fx.draw();
    if (!this.ended) music.setMood(this.sim.enemies.some((e) => e.alive && e.def.boss) ? 'boss' : 'battle');
    this.drawBossBar();
    this.refreshHud(dt);
  }

  /** Dev mode: endless coins and lives, spells and the hero skill always ready. */
  private devTopUp(): void {
    const s = this.sim;
    if (s.coins < DEV_COINS) s.coins = DEV_COINS;
    if (s.lives < DEV_LIVES) s.lives = DEV_LIVES;
    for (const id of Object.keys(s.spellCd)) s.spellCd[id] = 0;
    if (s.hero) s.hero.skillCd = 0;
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
          // a nameplate slides across with a red edge pulse (replaces the plain banner)
          const bd = ev.enemy.def;
          const facts = [`Health ${Math.round(ev.enemy.maxHp)}`, `${bd.phases?.length ?? 0} phases`];
          if (bd.flying) facts.push('flies');
          if (bd.armor >= 0.3) facts.push(`armor ${Math.round(bd.armor * 100)}%`);
          if (bd.magicResist >= 0.3) facts.push(`magic resist ${Math.round(bd.magicResist * 100)}%`);
          bossIntro(this, bd, facts.join('  •  '), GAME_W, GAME_H, motion.reduced);
          shake(this, 500, 0.01);
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
        heroSignature(this, ev.hero.def.id, ev.hero.pos, sk.radius, sk.fxColor ?? ev.hero.def.color, motion.lowFx);
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
        this.heroBadgeFlare();
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
        this.fx.onShoot(ev.tower, ev.projectile, tv);
        sfx.shoot(ev.tower.def.id);
        break;
      }
      case 'hit': {
        const v = this.enemyViews.get(ev.enemy.uid);
        if (v) {
          v.sprite.setTintFill(0xffffff);
          const big = bigHit(ev.damage, ev.enemy.maxHp);
          if (big && !motion.reduced) v.squash = 1;
          this.time.delayedCall(big ? 90 : 60, () => v.sprite.active && v.sprite.clearTint());
        }
        this.floatDamage(ev.pos.x, ev.pos.y - 20, ev.damage, damageTextStyle(ev.damage, ev.enemy.maxHp, ev.dtype, !!ev.enemy.def.boss));
        sfx.hit();
        break;
      }
      case 'splash': {
        this.particles.setParticleTint(0xb59a72);
        this.particles.explode(14, ev.pos.x, ev.pos.y);
        const ring = this.add.circle(ev.pos.x, ev.pos.y, ev.radius, 0xffffff, 0).setStrokeStyle(4, 0xe8d9b5, 0.9).setDepth(2400).setScale(0.3);
        this.tweens.add({ targets: ring, scale: 1, alpha: 0, duration: 280, onComplete: () => ring.destroy() });
        shake(this, 70, 0.002);
        sfx.boom();
        break;
      }
      case 'kill': {
        this.tally.kills++;
        if (ev.enemy.lastSrc?.startsWith('tower:') && justVeteran(this.sim.killsBy[ev.enemy.lastSrc] ?? 0)) this.addVeteranBadge(Number(ev.enemy.lastSrc.slice(6)));
        if (ev.enemy.def.boss) this.tally.bosses.push(ev.enemy.def.id);
        const v = this.enemyViews.get(ev.enemy.uid);
        if (v) this.killView(ev.enemy.uid, v);
        this.particles.setParticleTint(ev.enemy.def.color);
        this.particles.explode(motion.lowFx ? 8 : 10, ev.enemy.pos.x, ev.enemy.pos.y);
        {
          const st = deathStyle(ev.enemy.def);
          playDeath(this, ev.enemy.pos.x, ev.enemy.pos.y, st, motion.lowFx);
          // a heavy kill freezes the action for a heartbeat (throttled, never with Reduce Motion)
          if (st.heavy) sfx.thump();
          if (st.heavy && !motion.reduced && this.time.now - this.lastHitStop > 700) {
            this.lastHitStop = this.time.now;
            this.hitStopUntil = this.time.now + 70;
          }
        }
        this.floatText(ev.enemy.pos.x, ev.enemy.pos.y - 34, `+${ev.bounty}`, TEXT.gold, 18);
        sfx.kill();
        sfx.coin();
        if (ev.enemy.def.boss) {
          this.bossFireworks(ev.enemy.pos.x, ev.enemy.pos.y, ev.enemy.def.color);
          this.bossDefeatedBanner(ev.enemy.def.name, ev.bounty);
          this.slowMoStart = this.time.now;
        }
        break;
      }
      case 'leak': {
        const v = this.enemyViews.get(ev.enemy.uid);
        if (v) this.killView(ev.enemy.uid, v);
        shake(this, 180, 0.006);
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
        this.waveClearedPill(ev.index);
        break;
      case 'melee':
        sfx.melee();
        if (ev.from) this.fx.swing(ev.from, ev.pos);
        break;
      case 'soldierUp':
        this.fx.popOut(ev.soldier.pos.x, ev.soldier.pos.y);
        break;
      case 'spellCast': {
        const def = SPELLS[ev.spellId];
        if (def.kind === 'meteor') {
          // Visuals are created in syncStrikes() from sim.strikes so they track game time exactly.
          sfx.waveHorn();
        } else if (def.kind === 'snare') {
          const r = def.radius ?? 90;
          thornGrowth(this, ev.pos.x, ev.pos.y, r, def.slow?.duration ?? 3, motion.lowFx);
          this.particles.setParticleTint(0x6a9a3a);
          this.particles.explode(20, ev.pos.x, ev.pos.y);
          sfx.build();
        } else {
          this.particles.setParticleTint(0x8fdc5a);
          this.particles.explode(motion.lowFx ? 14 : 18, ev.pos.x, ev.pos.y);
          groveBurst(this, ev.pos.x, ev.pos.y, motion.lowFx);
          this.floatText(ev.pos.x, ev.pos.y - 50, 'Rangers, to me!', TEXT.gold, 20);
          sfx.build();
        }
        break;
      }
      case 'strike': {
        const sv = this.strikeViews.get(ev.uid);
        sv?.star.destroy();
        sv?.mark.destroy();
        sv?.ring.destroy();
        this.strikeViews.delete(ev.uid);
        starImpact(this, ev.pos.x, ev.pos.y, ev.radius, motion.lowFx);
        const ring = this.add.circle(ev.pos.x, ev.pos.y, ev.radius, 0xfff0a8, 0.4).setStrokeStyle(8, 0xffc93c, 1).setDepth(2400).setScale(0.2);
        this.tweens.add({ targets: ring, scale: 1.1, alpha: 0, duration: 450, onComplete: () => ring.destroy() });
        this.particles.setParticleTint(0xffc93c);
        this.particles.explode(40, ev.pos.x, ev.pos.y);
        this.particles.setParticleTint(0x9a8a6a);
        this.particles.explode(20, ev.pos.x, ev.pos.y);
        shake(this, 350, 0.014);
        this.cameras.main.flash(100, 255, 240, 180);
        sfx.boom();
        const soaked = ev.hits.find((h) => h.alive && this.sim.drenchCut(h) > 0);
        if (soaked) {
          // Spray Otter mist: the blast hisses into steam on the soaked critters
          this.particles.setParticleTint(0xe8f6ff);
          this.particles.explode(14, soaked.pos.x, soaked.pos.y - 6);
          this.floatText(soaked.pos.x, soaked.pos.y - 30, 'Soaked!', '#bfe8ff', 13);
        }
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
      case 'keg': {
        sfx.boom();
        const ring = this.add.circle(ev.pos.x, ev.pos.y - 6, ev.radius, 0xffa040, 0.35).setStrokeStyle(4, 0xffe080, 0.9).setDepth(2450).setScale(0.2);
        this.tweens.add({ targets: ring, scale: 1, alpha: 0, duration: 380, onComplete: () => ring.destroy() });
        this.particles.setParticleTint(0x6a6a72);
        this.particles.explode(18, ev.pos.x, ev.pos.y - 8);
        this.particles.setParticleTint(0xffb040);
        this.particles.explode(12, ev.pos.x, ev.pos.y - 8);
        shake(this, 140, 0.004);
        if (ev.hits.length) this.floatText(ev.pos.x, ev.pos.y - 40, 'Kaboom!', '#ffd080', 17);
        break;
      }
      case 'enemyShot': {
        sfx.trait('blast');
        const g = this.add.graphics().setDepth(2500);
        g.lineStyle(3, 0xffd890, 0.9);
        g.lineBetween(ev.enemy.pos.x + 12, ev.enemy.pos.y - 10, ev.to.x, ev.to.y - 12);
        this.tweens.add({ targets: g, alpha: 0, duration: 160, onComplete: () => g.destroy() });
        this.particles.setParticleTint(0xc8c8c8);
        this.particles.explode(5, ev.enemy.pos.x + 14, ev.enemy.pos.y - 10);
        break;
      }
      case 'snatch': {
        sfx.trait('snatch');
        // a streak from the hawk to where the soldier stood, and a puff of feathers
        const g = this.add.graphics().setDepth(2500);
        g.lineStyle(3, 0xc8783a, 0.9);
        g.lineBetween(ev.enemy.pos.x, ev.enemy.pos.y - 30, ev.pos.x, ev.pos.y - 8);
        this.tweens.add({ targets: g, alpha: 0, duration: 260, onComplete: () => g.destroy() });
        this.particles.setParticleTint(0xd8b890);
        this.particles.explode(10, ev.pos.x, ev.pos.y - 6);
        this.floatText(ev.pos.x, ev.pos.y - 30, 'Snatched!', '#ffb070', 14);
        break;
      }
      case 'venom': {
        // a sickly green splash on the bitten soldier (throttled per soldier)
        const key = -6000000 - ev.soldier.uid;
        const last = this.lastGulp.get(key) ?? -99;
        if (this.time.now - last < 900) break;
        this.lastGulp.set(key, this.time.now);
        sfx.trait('venom');
        this.particles.setParticleTint(0x8ad84a);
        this.particles.explode(6, ev.soldier.pos.x, ev.soldier.pos.y - 6);
        this.floatText(ev.soldier.pos.x, ev.soldier.pos.y - 26, 'Poisoned', '#a8f06a', 12);
        break;
      }
      case 'link': {
        // the string of wisps flickers together as the blow is shared out (throttled)
        const key = -7000000 - (ev.mates[0]?.uid ?? 0);
        const last = this.lastGulp.get(key) ?? -99;
        if (this.time.now - last < 400) break;
        this.lastGulp.set(key, this.time.now);
        sfx.trait('link');
        for (const m of ev.mates) {
          const mv = this.enemyViews.get(m.uid);
          if (mv) mv.pulse = 0.1;
        }
        break;
      }
      case 'bubble': {
        // the newt puffs a cloud of shining bubbles over its friends
        sfx.trait('bubble');
        for (const t of ev.targets) {
          this.particles.setParticleTint(0xc8f0ff);
          this.particles.explode(3, t.pos.x, t.pos.y - 8);
        }
        break;
      }
      case 'pop': {
        const key = -6000000 - ev.enemy.uid;
        const last = this.lastGulp.get(key) ?? -99;
        if (this.time.now - last < 250) break;
        this.lastGulp.set(key, this.time.now);
        sfx.trait('pop');
        const r = ev.enemy.def.radius + 6;
        const ring = this.add.circle(ev.enemy.pos.x, ev.enemy.pos.y - 4, r, 0xc8f0ff, 0).setStrokeStyle(2, 0xe8fbff, 0.9).setDepth(2400);
        this.tweens.add({ targets: ring, scale: 1.6, alpha: 0, duration: 220, onComplete: () => ring.destroy() });
        break;
      }
      case 'surge': {
        // a rush of white water sweeps the school down the stream
        sfx.trait('surge');
        const ring = this.add.circle(ev.source.pos.x, ev.source.pos.y, ev.radius, 0x9ad8f0, 0.14).setStrokeStyle(3, 0xd8f4ff, 0.9).setDepth(2400).setScale(0.3);
        this.tweens.add({ targets: ring, scale: 1, alpha: 0, duration: 450, onComplete: () => ring.destroy() });
        for (const t of ev.moved) {
          this.particles.setParticleTint(0xe8fbff);
          this.particles.explode(5, t.pos.x, t.pos.y);
        }
        this.floatText(ev.source.pos.x, ev.source.pos.y - 28, 'Surge!', '#bfe8ff', 13);
        break;
      }
      case 'ambush': {
        // a spray of red dirt where the gopher bursts out of the ground
        sfx.trait('ambush');
        this.particles.setParticleTint(0xb86a3a);
        this.particles.explode(14, ev.enemy.pos.x, ev.enemy.pos.y);
        this.floatText(ev.enemy.pos.x, ev.enemy.pos.y - 26, 'Ambush!', '#ffb08a', 13);
        break;
      }
      case 'curl': {
        sfx.trait('curl');
        const cv = this.enemyViews.get(ev.enemy.uid);
        if (cv) cv.pulse = 0.12;
        break;
      }
      case 'trample': {
        // the ox shoulders a soldier aside: a dust puff and a thud (throttled per ox)
        const key = -5000000 - ev.enemy.uid;
        const last = this.lastGulp.get(key) ?? -99;
        if (this.time.now - last < 300) break;
        this.lastGulp.set(key, this.time.now);
        sfx.trait('trample');
        this.particles.setParticleTint(0xc8a878);
        this.particles.explode(8, ev.pos.x, ev.pos.y);
        this.floatText(ev.pos.x, ev.pos.y - 24, 'Trampled!', '#e8c8a0', 12);
        break;
      }
      case 'alarm': {
        // the marmot stands up and whistles: a sharp ring, and the startled critters flash
        sfx.trait('alarm');
        const ring = this.add.circle(ev.enemy.pos.x, ev.enemy.pos.y, 10).setStrokeStyle(3, 0xffe08a, 0.9).setDepth(2400);
        this.tweens.add({ targets: ring, radius: ev.radius, alpha: 0, duration: 450, onComplete: () => ring.destroy() });
        this.floatText(ev.enemy.pos.x, ev.enemy.pos.y - 30, 'Wheeet!', '#ffe08a', 13);
        for (const o of ev.startled) {
          const v = this.enemyViews.get(o.uid);
          if (v) v.pulse = 0.15;
        }
        break;
      }
      case 'blossom': {
        // a soft burst of white seed-fluff from the fallen doe, drifting onto the healed
        sfx.trait('blossom');
        const ring = this.add.circle(ev.enemy.pos.x, ev.enemy.pos.y, 14, 0xffffff, 0.15).setStrokeStyle(2, 0xe8d8f8, 0.8).setDepth(2400);
        this.tweens.add({ targets: ring, radius: ev.radius, alpha: 0, duration: 600, onComplete: () => ring.destroy() });
        this.particles.setParticleTint(0xffffff);
        this.particles.explode(16, ev.enemy.pos.x, ev.enemy.pos.y - 6);
        for (const o of ev.healed) {
          this.particles.setParticleTint(0x9bff8a);
          this.particles.explode(3, o.pos.x, o.pos.y - 8);
        }
        if (ev.healed.length) this.floatText(ev.enemy.pos.x, ev.enemy.pos.y - 30, 'Bloom', '#e8d8f8', 13);
        break;
      }
      case 'dive': {
        // a muddy splash as the Mudskipper ducks under (or pops back up)
        sfx.trait('dive');
        this.particles.setParticleTint(0x5a4a2a);
        this.particles.explode(ev.down ? 12 : 8, ev.enemy.pos.x, ev.enemy.pos.y);
        if (ev.down) this.floatText(ev.enemy.pos.x, ev.enemy.pos.y - 26, 'Splosh!', '#c8b08a', 13);
        break;
      }
      case 'hex': {
        // a sour green-violet croak ring rolls from the toad to the tower it curses
        sfx.trait('hex');
        const ring = this.add.circle(ev.source.pos.x, ev.source.pos.y, 12).setStrokeStyle(3, 0xa070e0, 0.8).setDepth(2400);
        this.tweens.add({ targets: ring, radius: 40, alpha: 0, duration: 450, onComplete: () => ring.destroy() });
        const line = this.add.graphics().setDepth(2400);
        line.lineStyle(3, 0xa070e0, 0.7);
        line.lineBetween(ev.source.pos.x, ev.source.pos.y - 8, ev.tower.pos.x, ev.tower.pos.y - 16);
        this.tweens.add({ targets: line, alpha: 0, duration: 400, onComplete: () => line.destroy() });
        this.floatText(ev.tower.pos.x, ev.tower.pos.y - 44, 'Hexed', '#c8a0f0', 13);
        break;
      }
      case 'glaze': {
        // a splat of honey on the soldier, throttled per soldier
        const key = -4000000 - ev.soldier.uid;
        const last = this.lastGulp.get(key) ?? -99;
        if (this.time.now - last < 900) break;
        this.lastGulp.set(key, this.time.now);
        sfx.trait('glaze');
        this.particles.setParticleTint(0xf0b030);
        this.particles.explode(6, ev.soldier.pos.x, ev.soldier.pos.y - 6);
        this.floatText(ev.soldier.pos.x, ev.soldier.pos.y - 26, 'Sticky!', '#ffc84a', 12);
        break;
      }
      case 'parry': {
        // a little hexagon flash in front of the wasp, throttled per wasp
        const key = -3000000 - ev.enemy.uid;
        const last = this.lastGulp.get(key) ?? -99;
        if (this.time.now - last < 250) break;
        this.lastGulp.set(key, this.time.now);
        sfx.trait('parry');
        const hex = this.add.polygon(ev.enemy.pos.x, ev.enemy.pos.y - 6, [0, -14, 12, -7, 12, 7, 0, 14, -12, 7, -12, -7], 0xffd040, 0.5).setStrokeStyle(2, 0xfff0a0, 0.9).setDepth(2400);
        this.tweens.add({ targets: hex, scale: 1.5, alpha: 0, duration: 260, onComplete: () => hex.destroy() });
        if (ev.left === 0) this.floatText(ev.enemy.pos.x, ev.enemy.pos.y - 28, 'Shield cracked', '#ffe08a', 12);
        break;
      }
      case 'melt': {
        sfx.trait('melt');
        this.floatText(ev.enemy.pos.x, ev.enemy.pos.y - 28, 'Melted!', '#ffb84a', 13);
        this.particles.setParticleTint(0xffc860);
        this.particles.explode(10, ev.enemy.pos.x, ev.enemy.pos.y);
        const mv = this.enemyViews.get(ev.enemy.uid);
        if (mv) mv.pulse = 0.2;
        break;
      }
      case 'rile': {
        // throttled per howler: an angry red "!" and a little hop
        const key = -2000000 - ev.enemy.uid;
        const last = this.lastGulp.get(key) ?? -99;
        if (this.time.now - last < 700) break;
        this.lastGulp.set(key, this.time.now);
        sfx.trait('rile');
        this.floatText(ev.enemy.pos.x, ev.enemy.pos.y - 28, 'Grr!', '#ff7a5a', 13);
        const rv = this.enemyViews.get(ev.enemy.uid);
        if (rv) rv.pulse = 0.15;
        break;
      }
      case 'grief': {
        sfx.trait('grief');
        const ring = this.add.circle(ev.enemy.pos.x, ev.enemy.pos.y, 14).setStrokeStyle(3, 0x8a8aa8, 0.8).setDepth(2400);
        this.tweens.add({ targets: ring, radius: ev.radius, alpha: 0, duration: 600, onComplete: () => ring.destroy() });
        if (ev.mourners.length) this.floatText(ev.enemy.pos.x, ev.enemy.pos.y - 30, 'Mourned', '#c8c8e0', 13);
        break;
      }
      case 'mist': {
        if (ev.on) {
          sfx.trait('mist');
          this.particles.setParticleTint(0xeef0ff);
          this.particles.explode(6, ev.enemy.pos.x, ev.enemy.pos.y);
        }
        break;
      }
      case 'dodge': {
        // throttled per crane: a little "Miss!" and a whoosh
        const key = -1000000 - ev.enemy.uid;
        const last = this.lastGulp.get(key) ?? -99;
        if (this.time.now - last < 500) break;
        this.lastGulp.set(key, this.time.now);
        sfx.trait('dodge');
        this.floatText(ev.enemy.pos.x, ev.enemy.pos.y - 28, 'Miss!', '#e8f0ff', 13);
        const cv = this.enemyViews.get(ev.enemy.uid);
        if (cv) cv.pulse = 0.18; // a quick flinch as the crane steps aside
        break;
      }
      case 'leech': {
        // throttled: a small red-gold "+" and a gulp, at most every 0.6s per stoat
        const last = this.lastGulp.get(ev.enemy.uid) ?? -99;
        if (this.time.now - last < 600) break;
        this.lastGulp.set(ev.enemy.uid, this.time.now);
        sfx.trait('leech');
        this.floatText(ev.enemy.pos.x, ev.enemy.pos.y - 28, `+${Math.round(ev.amount)}`, '#ff9a6a', 13);
        break;
      }
      case 'drum': {
        sfx.trait('drum');
        const dv = this.enemyViews.get(ev.enemy.uid);
        if (dv) dv.pulse = 0.3;
        // the beat spreads as a warm ring; hastened critters flash
        const ring = this.add.circle(ev.enemy.pos.x, ev.enemy.pos.y, 16).setStrokeStyle(4, 0xe8a03a, 0.85).setDepth(2400);
        this.tweens.add({ targets: ring, radius: ev.radius, alpha: 0, duration: 450, onComplete: () => ring.destroy() });
        this.floatText(ev.enemy.pos.x, ev.enemy.pos.y - 34, 'Boom!', '#ffcf7a', 14);
        break;
      }
      case 'anchor': {
        if (ev.down) {
          sfx.trait('anchor');
          this.particles.setParticleTint(0xbfe8ff);
          this.particles.explode(10, ev.enemy.pos.x, ev.enemy.pos.y);
          this.floatText(ev.enemy.pos.x, ev.enemy.pos.y - 36, 'Anchored!', '#c8d0d8', 15);
          // the anchor itself, planted in the deck beside it until it hauls up again
          const ax = ev.enemy.pos.x + 18;
          const ay = ev.enemy.pos.y + 4;
          // drawn around its own origin so the pop-in scale grows in place
          const g = this.add.graphics().setPosition(ax, ay).setDepth(ay - 1);
          g.lineStyle(3, 0x3a3a42, 1);
          g.lineBetween(0, -16, 0, 6);
          g.lineBetween(-6, -10, 6, -10);
          g.strokeCircle(0, -19, 3);
          g.beginPath();
          g.arc(0, 0, 8, 0.15, Math.PI - 0.15);
          g.strokePath();
          g.setScale(0.3);
          this.tweens.add({ targets: g, scale: 1, duration: 160, ease: 'Back.easeOut' });
          const hold = (ev.enemy.def.anchor?.duration ?? 2) * 1000;
          this.tweens.add({ targets: g, alpha: 0, delay: hold - 250, duration: 250, onComplete: () => g.destroy() });
        }
        break;
      }
      case 'ink': {
        sfx.trait('ink');
        // a murky cloud that hides whatever walks inside it, fading as it disperses
        const cloud = this.add.container(ev.pos.x, ev.pos.y - 6).setDepth(2300);
        for (const [dx, dy, rr] of [[0, 0, 1], [-0.45, 0.2, 0.7], [0.5, 0.15, 0.75], [0.1, -0.35, 0.7]]) {
          cloud.add(this.add.circle(dx * ev.radius, dy * ev.radius, ev.radius * rr * 0.7, 0x2a1a3a, 0.62));
        }
        cloud.setScale(0.3);
        this.tweens.add({ targets: cloud, scale: 1, duration: 220, ease: 'Back.easeOut' });
        this.tweens.add({ targets: cloud, alpha: 0, delay: ev.duration * 1000 - 500, duration: 500, onComplete: () => cloud.destroy() });
        this.floatText(ev.pos.x, ev.pos.y - 40, 'Ink!', '#c88ad8', 15);
        break;
      }
      case 'molt': {
        sfx.trait('crack');
        this.particles.setParticleTint(0x9a8a7a);
        this.particles.explode(12, ev.enemy.pos.x, ev.enemy.pos.y - 8);
        this.floatText(ev.enemy.pos.x, ev.enemy.pos.y - 34, 'Molted!', '#ffb0a0', 15);
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
        shake(this, 300, 0.008);
        if (ev.enemy.def.boss) this.bossFlashUntil = this.time.now + (motion.reduced ? BOSS_FLASH_MS / 2 : BOSS_FLASH_MS);
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
        const old = this.towerViews[t.slot];
        if (old) {
          this.tweens.killTweensOf(old);
          old.destroy();
        }
        const img = this.add.image(t.pos.x, t.pos.y - 34, t.spec ? `tower_${t.def.id}_${t.spec}` : `tower_${t.def.id}_${t.tier}`).setDepth(t.pos.y + 1);
        img.setScale(0.3, 1.4);
        this.tweens.add({ targets: img, scaleX: 1, scaleY: 1, duration: 300, ease: 'Back.easeOut' });
        this.towerViews[t.slot] = img;
        this.fx.placed(t, img);
        if (!this.towerShadows.has(t.slot)) this.towerShadows.set(t.slot, this.add.ellipse(t.pos.x + 4, t.pos.y + 8, 74, 22, 0x000000, 0.22).setDepth(t.pos.y - 2));
        this.slotViews[t.slot].setAlpha(0.6);
        this.particles.setParticleTint(0xd9c39a);
        this.particles.explode(motion.lowFx ? 8 : 6, t.pos.x, t.pos.y + 6);
        if (ev.type === 'build') buildPuff(this, t.pos.x, t.pos.y, motion.lowFx);
        else upgradeBurst(this, t.pos.x, t.pos.y, t.spec ? 4 : t.tier + 1, TOWER_GLOW[t.def.id] ?? 0xffe27a, motion.lowFx);
        sfx.build();
        break;
      }
      case 'sell': {
        this.veteranBadges.get(ev.tower.uid)?.destroy();
        this.veteranBadges.delete(ev.tower.uid);
        const v = this.towerViews[ev.tower.slot];
        this.fx.removed(ev.tower.slot);
        this.towerShadows.get(ev.tower.slot)?.destroy();
        this.towerShadows.delete(ev.tower.slot);
        if (v) {
          this.tweens.killTweensOf(v);
          this.tweens.add({ targets: v, scale: 0, alpha: 0, duration: 200, onComplete: () => v.destroy() });
        }
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
    // every critter casts a soft ground shadow (flyers a smaller, fainter one far below them)
    const shadow = e.def.flying
      ? this.add.ellipse(e.pos.x, e.pos.y, e.def.radius * 1.6, e.def.radius * 0.6, 0x000000, 0.22)
      : this.add.ellipse(e.pos.x, e.pos.y, e.def.radius * 1.9, e.def.radius * 0.7, 0x000000, 0.2);
    const mound = e.def.burrow || e.def.dive ? this.add.image(e.pos.x, e.pos.y, 'mound').setVisible(false) : null;
    this.enemyViews.set(e.uid, { sprite, bar, bob: Math.random() * Math.PI * 2, shadow, mound, air: e.def.flying ? 1 : 0, pulse: 0, squash: 0, trail: newTrail(1) });
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
    const hz = this.sim.hero;
    if (hz && hz.alive && hz.def.passive.kind === 'drowse') {
      // Hazel's lullaby: a faint lilac ring that breathes slowly
      this.jamG.lineStyle(2, 0xc8a8ff, 0.25 + 0.1 * Math.sin(this.sim.time * 1.5));
      this.jamG.strokeCircle(hz.pos.x, hz.pos.y, hz.def.passive.radius);
      this.jamG.fillStyle(0xc8a8ff, 0.05);
      this.jamG.fillCircle(hz.pos.x, hz.pos.y, hz.def.passive.radius);
    }
    for (const e of this.sim.enemies) {
      if (!e.alive || !e.def.ward) continue;
      // Glowbearer lantern-light: a warm gold disc with a soft rim that breathes
      const pulse = 0.35 + 0.1 * Math.sin(this.sim.time * 2.5);
      this.jamG.fillStyle(0xffd27a, 0.12);
      this.jamG.fillCircle(e.pos.x, e.pos.y, e.def.ward.radius);
      this.jamG.lineStyle(2, 0xffc84a, pulse);
      this.jamG.strokeCircle(e.pos.x, e.pos.y, e.def.ward.radius);
    }
    for (const e of this.sim.enemies) {
      if (!e.alive || !e.def.lure || e.underground) continue;
      // Lanternfrog bulb: a pale halo that swells and fades, so it's clear why every tower is staring at it
      const k = (this.sim.time * 0.9 + e.uid * 0.37) % 1;
      this.jamG.lineStyle(2, 0xe8ff8a, 0.55 * (1 - k));
      this.jamG.strokeCircle(e.pos.x, e.pos.y, 16 + 30 * k);
      this.jamG.fillStyle(0xe8ff8a, 0.1);
      this.jamG.fillCircle(e.pos.x, e.pos.y, 22);
    }
    for (const t of this.sim.towers) {
      if (!t || !((t.hexed ?? 0) > 0)) continue;
      // a Hexcroak curse: a slow violet ring of little sigils turning around the tower's base
      const a0 = this.sim.time * 1.6;
      this.jamG.lineStyle(2, 0xa070e0, 0.6);
      this.jamG.strokeEllipse(t.pos.x, t.pos.y + 10, 64, 26);
      this.jamG.fillStyle(0xc8a0f0, 0.85);
      for (let n = 0; n < 5; n++) {
        const a = a0 + (n * Math.PI * 2) / 5;
        this.jamG.fillCircle(t.pos.x + Math.cos(a) * 32, t.pos.y + 10 + Math.sin(a) * 13, 2.5);
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
      // each enemy family has its own gait (march, waddle, hop, scuttle; flyers flap); Reduce Motion keeps a still pose
      const pose = poseFor(airborne ? 'flap' : gaitFor(e.def), motion.reduced ? 0 : v.bob);
      const lift = v.air * (34 + Math.sin(v.bob * 0.7) * 5) + (1 - v.air) * (e.blockedBy ? pose.lift * 0.4 : pose.lift);
      v.sprite.setPosition(e.pos.x, e.pos.y - lift);
      v.pulse = Math.max(0, v.pulse - dt * 1.6);
      const swell = (1 + e.fed * 0.08) * (1 + v.pulse); // fed Gorgegrubs visibly bulk up; drummers thump
      v.sprite.setScale(swell * pose.sx, swell * pose.sy);
      if (!e.def.momentum) v.sprite.setRotation(pose.rot * (v.sprite.flipX ? -1 : 1));
      if (v.squash > 0) {
        v.squash = Math.max(0, v.squash - dt * 7);
        v.sprite.setScale(v.sprite.scaleX * (1 + v.squash * 0.28), v.sprite.scaleY * (1 - v.squash * 0.22));
      }
      if (e.anchored) v.sprite.setTint(0xa8b4c4); // iron-grey while an Ironkeel holds anchor
      if (e.def.phase) v.sprite.setAlpha(e.phased ? 0.35 : 1); // a Mistfox thinning into fog
      else if (e.def.adapt) {
        // Turnleaf: bark-brown when it has turned toward armor, moon-violet toward magic resist
        const lean = e.armor - e.def.armor - (e.mr - e.def.magicResist);
        if (lean > 0.1) v.sprite.setTint(0xc8a07a);
        else if (lean < -0.1) v.sprite.setTint(0xc0b0ff);
        else v.sprite.clearTint();
      }
      else if (e.def.curl) {
        // Curlshell: squashes into a tight sandy ball while curled
        if (e.curlT > 0) v.sprite.setTint(0xd8c8a0).setScale(v.sprite.scaleX * 0.8, v.sprite.scaleY * 0.75);
        else v.sprite.clearTint();
      }
      else if (e.speedMult > 1) v.sprite.setTint(0xff9a8a);
      else if (e.hasteMult > 1) v.sprite.setTint(0xffc0e8);
      else if (e.hasteTime <= 0 && (v.sprite.tintTopLeft === 0xffc0e8 || v.sprite.tintTopLeft === 0xa8b4c4)) v.sprite.clearTint();
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
      v.shadow?.setPosition(e.pos.x, e.pos.y + (e.def.flying ? 4 : e.def.radius * 0.72)).setDepth(e.pos.y - 1).setVisible(!e.underground);
      if (v.mound) {
        v.mound.setVisible(e.underground).setPosition(e.pos.x, e.pos.y + 2).setDepth(e.pos.y);
        v.sprite.setVisible(!e.underground);
        if (e.underground) {
          v.bar.clear();
          continue;
        }
      }
      if (Math.abs(e.pos.x - prevX) > 0.01) v.sprite.setFlipX(e.pos.x < prevX);
      if (!e.def.momentum && this.sim.mods.momentumMax > 0 && !e.blockedBy && !motion.reduced && this.sim.momentumMult(e) > 1.3 && Math.random() < 0.08) {
        // Prairie Gale: wind-blown critters trail little puffs of dust
        this.particles.setParticleTint(0xd8c8a0);
        this.particles.explode(1, e.pos.x, e.pos.y + e.def.radius * 0.6);
      }
      if (e.def.momentum && !e.def.boss && !e.blockedBy) {
        // Tumblehog: the thistle ball spins faster the more momentum it has built up, with dust kicking up at full roll
        const m = this.sim.momentumMult(e);
        v.sprite.rotation += (e.pos.x < prevX ? -1 : 1) * 0.06 * m * m;
        if (m > 1.6 && !motion.reduced && Math.random() < 0.15) {
          this.particles.setParticleTint(0xc8a878);
          this.particles.explode(1, e.pos.x, e.pos.y + e.def.radius * 0.6);
        }
      }
      v.sprite.setDepth(v.air > 0.5 ? e.pos.y + 1000 : e.pos.y);
      v.bar.clear();
      if (e.def.link) {
        // Heath Wisps: faint threads of light to each linked sister close by (drawn once per pair)
        for (const o of this.sim.enemies) {
          if (o.uid <= e.uid || !o.alive || !o.def.link) continue;
          const d = Math.hypot(o.pos.x - e.pos.x, o.pos.y - e.pos.y);
          if (d > e.def.link.radius) continue;
          v.bar.lineStyle(1.5, 0xd8e8ff, 0.35 * (1 - d / e.def.link.radius) + 0.1);
          v.bar.lineBetween(e.pos.x, e.pos.y - 4 - 34 * v.air, o.pos.x, o.pos.y - 4 - 34 * v.air);
        }
        v.bar.setDepth(e.pos.y + 1000.5);
      }
      if (e.def.drench) {
        // Spray Otter: a soft drifting mist around it marks where spells fall flat
        const t = this.time.now / 600 + e.uid;
        // a crowd of otters would stack their mist into a white fog, so only the first otter in a clump fills it
        const clumped = this.sim.enemies.some((o) => o !== e && o.alive && o.def.drench && o.uid < e.uid && Math.hypot(o.pos.x - e.pos.x, o.pos.y - e.pos.y) < e.def.drench!.radius * 0.6);
        if (!clumped) {
          v.bar.fillStyle(0xbfe0f0, 0.08);
          v.bar.fillCircle(e.pos.x, e.pos.y, e.def.drench.radius);
        }
        v.bar.lineStyle(1, 0xe8f6ff, 0.22);
        v.bar.strokeCircle(e.pos.x, e.pos.y, e.def.drench.radius);
        v.bar.fillStyle(0xe8f6ff, 0.35);
        for (let k = 0; k < 6; k++) {
          const a = t + k * 1.05;
          v.bar.fillCircle(e.pos.x + Math.cos(a) * e.def.drench.radius * 0.7, e.pos.y + Math.sin(a) * e.def.drench.radius * 0.45, 3);
        }
        v.bar.setDepth(e.pos.y - 0.5);
      }
      if (e.bubbled) {
        // Bubbler Newt's bubble: a shining soap-film ring that pops on the next hit
        const by = e.pos.y - 4 - 34 * v.air;
        v.bar.fillStyle(0xc8f0ff, 0.16);
        v.bar.fillCircle(e.pos.x, by, e.def.radius + 6);
        v.bar.lineStyle(1.5, 0xe8fbff, 0.85);
        v.bar.strokeCircle(e.pos.x, by, e.def.radius + 6);
        v.bar.fillStyle(0xffffff, 0.8);
        v.bar.fillCircle(e.pos.x - e.def.radius * 0.45, by - e.def.radius * 0.5, 2);
        v.bar.setDepth(v.air > 0.5 ? e.pos.y + 1000.5 : e.pos.y + 0.5);
      }
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
        const frac = Math.max(0, e.hp / e.maxHp);
        stepTrail(v.trail, frac, dt);
        drawBar(v.bar, x, y, w, 5, frac, v.trail.trail, hpColor(frac));
        // armor / magic-resist markers to the left of the bar
        resistPips(e.armor, e.def.magicResist).forEach((pip, k) => {
          const px = x - 6 - k * 9;
          const py = y + 2.5;
          v.bar.fillStyle(C.ink, 0.9);
          v.bar.fillCircle(px, py, 4.6);
          if (pip === 'armor') {
            v.bar.fillStyle(0xc8d0d8, 1);
            v.bar.fillTriangle(px - 3, py - 2.6, px + 3, py - 2.6, px, py + 3.4);
            v.bar.fillRect(px - 3, py - 3, 6, 1.6);
          } else {
            v.bar.fillStyle(0xc890ff, 1);
            v.bar.fillTriangle(px - 3, py, px + 3, py, px, py - 3.4);
            v.bar.fillTriangle(px - 3, py, px + 3, py, px, py + 3.4);
          }
        });
        v.bar.setDepth(v.air > 0.5 ? e.pos.y + 1000.5 : e.pos.y + 0.5);
      }
      if (e.def.parry && e.parryCharges > 0) {
        // Hexguard Wasp: one little amber cell per shot its comb shield can still turn aside
        const top = e.pos.y - e.def.radius - 24 - 34 * v.air;
        for (let k = 0; k < e.parryCharges; k++) {
          const px = e.pos.x + (k - (e.parryCharges - 1) / 2) * 8;
          v.bar.fillStyle(C.ink, 0.85);
          v.bar.fillCircle(px, top, 3.6);
          v.bar.fillStyle(0xffc83a, 1);
          v.bar.fillCircle(px, top, 2.4);
        }
        v.bar.setDepth(v.air > 0.5 ? e.pos.y + 1000.5 : e.pos.y + 0.5);
      }
      if (e.def.wax && e.waxLeft > 0) {
        // Waxback: a glossy amber band that drains as spells melt the coat
        const w = Math.max(24, e.def.radius * 2.4);
        const x = e.pos.x - w / 2;
        const y = e.pos.y - e.def.radius - 14 - 34 * v.air + 7;
        const full = Math.max(1, Math.round(e.maxHp * e.def.wax.melt));
        v.bar.fillStyle(C.ink, 0.85);
        v.bar.fillRect(x - 1, y, w + 2, 4);
        v.bar.fillStyle(0xf0b840, 1);
        v.bar.fillRect(x, y + 1, w * Math.min(1, e.waxLeft / full), 2);
        v.bar.setDepth(v.air > 0.5 ? e.pos.y + 1000.5 : e.pos.y + 0.5);
      }
    }
    this.updateEnemyCard(dt);
    this.syncSoldiers();
    this.syncStrikes();
    // Frozen towers turn icy.
    this.sim.towers.forEach((t, i) => {
      const v = this.towerViews[i];
      if (!t || !v) return;
      if (t.frozen > 0) v.setTint(0xbfe8ff);
      else if ((t.hexed ?? 0) > 0) v.setTint(0xc8a0f0); // cursed by a Hexcroak: a sickly violet
      else if (v.isTinted) v.clearTint();
    });
    const live = new Set(this.sim.projectiles.map((p) => p.uid));
    for (const p of this.sim.projectiles) {
      const img = this.projViews.get(p.uid);
      if (!img) continue;
      if (p.homing) {
        img.setRotation(Math.atan2(p.lastTargetPos.y - img.y, p.lastTargetPos.x - img.x));
        img.setPosition(p.pos.x, p.pos.y);
        this.fx.track(p.uid, img.x, img.y);
      } else {
        // Arc: lift by a parabola over the flight progress.
        const left = Math.hypot(p.lastTargetPos.x - p.pos.x, p.lastTargetPos.y - p.pos.y);
        const t = p.travel > 0 ? 1 - left / p.travel : 1;
        const lift = Math.sin(Math.PI * Math.max(0, Math.min(1, t))) * Math.min(120, 40 + p.travel * 0.35);
        img.setPosition(p.pos.x, p.pos.y - lift);
        img.rotation += 0.15;
        this.fx.track(p.uid, img.x, img.y, p.pos.x, p.pos.y);
      }
    }
    for (const [uid, img] of this.projViews) {
      if (!live.has(uid)) {
        this.fx.gone(uid, img.x, img.y);
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
        // a thin ring that closes in on the target as the star falls
        const ring = this.add.circle(st.pos.x, st.pos.y, def.radius ?? 60, def.color, 0).setStrokeStyle(2, 0xfff0b0, 0.9).setDepth(2301).setScale(1.7);
        v = { star, mark, ring };
        this.strikeViews.set(st.uid, v);
      }
      const t = 1 - Math.max(0, st.timer) / (def.delay ?? 1);
      const e = t * t; // ease-in fall
      v.star.setPosition(st.pos.x + 260 * (1 - e), -60 + (st.pos.y + 60) * e).setRotation(t * 6);
      v.ring.setScale(1.7 - 0.7 * e).setAlpha(0.4 + 0.6 * t);
      if (!this.paused) starTrail(this, v.star.x, v.star.y, motion.lowFx);
    }
  }

  private syncSoldiers(): void {
    const seen = new Set<number>();
    for (const s of this.sim.soldiers) {
      seen.add(s.uid);
      let v = this.soldierViews.get(s.uid);
      if (!v) {
        v = { sprite: this.add.image(s.pos.x, s.pos.y, s.summoned ? 'ranger' : 'soldier'), bar: this.add.graphics(), trail: newTrail(1) };
        if (s.summoned) {
          v.sprite.setScale(0).setData('popping', true);
          this.tweens.add({ targets: v.sprite, scale: 1, duration: 250, ease: 'Back.easeOut', onComplete: () => v?.sprite.setData('popping', false) });
        }
        this.soldierViews.set(s.uid, v);
      }
      this.drawSoldier(s, v.sprite, v.bar, v.trail);
    }
    for (const [uid, v] of this.soldierViews) {
      if (!seen.has(uid)) {
        v.sprite.destroy();
        v.bar.destroy();
        this.soldierViews.delete(uid);
      }
    }
  }

  private drawSoldier(s: Soldier, sprite: Phaser.GameObjects.Image, bar: Phaser.GameObjects.Graphics, trail: TrailState): void {
    sprite.setVisible(s.alive);
    bar.clear();
    if (!s.alive) return;
    const fighting = s.targetUid !== 0;
    const px = (sprite.getData('px') as number | undefined) ?? s.pos.x;
    const py = (sprite.getData('py') as number | undefined) ?? s.pos.y;
    const walking = !fighting && Math.hypot(s.pos.x - px, s.pos.y - py) > 0.3;
    sprite.setData('px', s.pos.x).setData('py', s.pos.y);
    if (Math.abs(s.pos.x - px) > 0.3) sprite.setFlipX(s.pos.x < px);
    // march with a step, chop in an arc while fighting, breathe while waiting
    const pose = motion.reduced ? { lift: 0, sx: 1, sy: 1, rot: 0 } : unitPose(fighting ? 'fight' : walking ? 'walk' : 'idle', this.time.now, s.uid * 1.7, sprite.flipX ? -1 : 1);
    sprite.setPosition(s.pos.x, s.pos.y - 10 - pose.lift).setDepth(s.pos.y).setRotation(pose.rot);
    if (!sprite.getData('popping')) sprite.setScale(pose.sx, pose.sy); // let a summoned ranger's pop-in finish first
    if (s.summoned && s.life < 3) sprite.setAlpha(0.5 + 0.5 * Math.abs(Math.sin(this.time.now / 120)));
    // status tints so afflictions read at a glance: venom green, honey amber, shock pale blue
    if ((s.poisonT ?? 0) > 0) sprite.setTint(0xa8f07a);
    else if ((s.glazed ?? 0) > 0) sprite.setTint(0xffd070);
    else if ((s.stun ?? 0) > 0) sprite.setTint(0xc8e8ff);
    else if (sprite.isTinted) sprite.clearTint();
    stepTrail(trail, s.hp / s.maxHp, Math.min(this.game.loop.delta / 1000, 0.1));
    if (s.hp < s.maxHp) {
      const w = 24;
      const frac = Math.max(0, s.hp / s.maxHp);
      // our side reads blue (a poisoned soldier's bar turns green as it drains)
      drawBar(bar, s.pos.x - w / 2, s.pos.y - 33, w, 4, frac, trail.trail, (s.poisonT ?? 0) > 0 ? 0x8ad84a : frac > 0.3 ? 0x7fc8ff : 0xff7a5a);
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

  /** A damage number: pops in, arcs up and to one side and fades; big hits pop harder and hold a moment. */
  private floatDamage(x: number, y: number, damage: number, st: { color: string; size: number; big: boolean }): void {
    const t = this.add.text(x, y, String(Math.round(damage)), textStyle(st.size, st.color)).setOrigin(0.5).setDepth(st.big ? 2960 : 2950).setStroke('#1a1410', st.big ? 6 : 4); // above the lighting overlay (2900), under the HUD
    if (motion.reduced) {
      this.tweens.add({ targets: t, y: y - 26, alpha: 0, duration: 650, onComplete: () => t.destroy() });
      return;
    }
    const dx = (Math.random() - 0.5) * (st.big ? 30 : 22);
    t.setScale(0.5);
    // pop in; big hits overshoot to 1.3 and settle back to full size (a yoyo would return to the 0.5 start)
    this.tweens.add({
      targets: t, scale: st.big ? 1.3 : 1.05, duration: st.big ? 110 : 80, ease: 'Back.easeOut',
      onComplete: () => st.big && t.active && this.tweens.add({ targets: t, scale: 1.05, delay: 60, duration: 120 }),
    });
    this.tweens.add({ targets: t, x: x + dx, y: y - (st.big ? 44 : 32), duration: st.big ? 900 : 700, ease: 'Quad.easeOut' });
    this.tweens.add({ targets: t, alpha: 0, delay: st.big ? 450 : 300, duration: st.big ? 450 : 400, onComplete: () => t.destroy() });
  }

  private floatText(x: number, y: number, text: string, color: string, size: number): void {
    const t = this.add.text(x, y, text, textStyle(size, color)).setOrigin(0.5).setDepth(2600);
    this.tweens.add({ targets: t, y: y - 30, alpha: 0, duration: 700, ease: 'Cubic.easeOut', onComplete: () => t.destroy() });
  }

  // ---------- end of battle ----------

  /**
   * A small card under the result panel: lives lost per wave as bars, the worst wave picked out in red with a
   * label, or a "Flawless" line when nothing got through. Bars grow in one after another.
   */
  private addWaveChart(won: boolean, still: boolean): void {
    const played = won ? this.sim.totalWaves : Math.max(1, this.sim.waveIndex + 1);
    const chart = waveChart(this.sim.leaksByWave, played);
    const W = 560;
    const H = 136;
    const card = this.add.container(GAME_W / 2 - W / 2, GAME_H / 2 + 206).setDepth(5001).setName('waveChart');
    const bg = this.add.graphics();
    glossPanel(bg, 0, 0, W, H, { fill: C.ink, alpha: 0.94, rim: 0xc8a050, rimAlpha: 0.5, radius: 16 });
    card.add(bg);
    card.add(this.add.text(14, 10, 'Lives lost per wave', textStyle(pf(13), TEXT.gold)));
    const note =
      chart.worst < 0 ? 'Flawless: nothing got through!' : `Toughest: wave ${chart.worst + 1} (-${chart.bars[chart.worst].lost})`;
    card.add(this.add.text(W - 14, 10, note, textStyle(pf(13), chart.worst < 0 ? '#9be86a' : '#ffb0a0', false)).setOrigin(1, 0));
    const left = 18;
    const base = H - 44;
    const top = 38;
    // run summary under the chart: the tower that did the most, the hero's share and spells cast
    const names: Record<number, string> = {};
    for (const t of this.sim.towers) if (t) names[t.uid] = t.spec ? t.def.specs.find((x) => x.id === t.spec)!.name : `${t.def.name} Lv ${t.tier + 1}`;
    const sum = runSummary(this.sim.dmgBy, this.sim.killsBy, this.sim.spellsCast, names);
    const parts: string[] = [];
    if (sum.top) parts.push(`Best tower: ${sum.top.name} (${shortNum(sum.top.damage)} dmg, ${sum.top.kills} kills)`);
    if (this.sim.hero) parts.push(`${this.sim.hero.def.name}: ${shortNum(sum.hero.damage)} dmg, ${sum.hero.kills} kills`);
    parts.push(`Spells: ${sum.spellsCast}`);
    const line = this.add.graphics();
    line.fillStyle(0xffffff, 0.06);
    line.fillRoundedRect(10, H - 30, W - 20, 22, 8);
    card.add(line);
    card.add(fitWidth(this.add.text(W / 2, H - 19, parts.join('   •   '), textStyle(pf(12), TEXT.cream, false)).setOrigin(0.5).setName('runSummary'), W - 32));
    const slot = (W - left * 2) / played;
    const bw = Math.max(4, Math.min(22, slot - 6));
    const bars = this.add.graphics();
    card.add(bars);
    const axis = this.add.graphics();
    axis.lineStyle(1, 0xffffff, 0.2);
    axis.lineBetween(left - 4, base + 0.5, W - left + 4, base + 0.5);
    card.add(axis);
    const draw = (shown: number) => {
      bars.clear();
      chart.bars.forEach((b, i) => {
        const x = left + slot * i + slot / 2 - bw / 2;
        if (b.lost <= 0) {
          // a clean wave: a small green pip on the axis
          bars.fillStyle(0x6ab04c, 0.9);
          bars.fillCircle(x + bw / 2, base - 3, 2.5);
          return;
        }
        const grow = Phaser.Math.Clamp(shown - i, 0, 1);
        const h = Math.max(4, (base - top) * b.h) * grow;
        bars.fillStyle(i === chart.worst ? 0xff5d4a : 0xff9f43, 1);
        bars.fillRoundedRect(x, base - h, bw, h, Math.min(4, bw / 2));
        bars.fillStyle(0xffffff, 0.25);
        bars.fillRect(x + 2, base - h + 2, Math.max(1, bw * 0.25), Math.max(0, h - 4));
      });
    };
    // wave numbers under every few bars, so long levels stay readable
    const every = played > 14 ? 5 : played > 8 ? 2 : 1;
    for (let i = 0; i < played; i += every) card.add(this.add.text(left + slot * i + slot / 2, base + 1, String(i + 1), textStyle(pf(9), '#9ab09a', false)).setOrigin(0.5, 0));
    if (still || motion.reduced) draw(played);
    else {
      draw(0);
      const t = { v: 0 };
      this.tweens.add({ targets: t, v: played, delay: 900, duration: 120 * played, onUpdate: () => draw(t.v) });
      card.setAlpha(0);
      this.tweens.add({ targets: card, alpha: 1, delay: 700, duration: 250 });
    }
  }

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
    } else if (won && !this.daily) {
      // (daily challenges pay their own reward and never touch campaign stars: their level is eased)
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
    if (!devOn()) {
      // dev-mode test runs never count toward real progress
      writeSave(checked.save);
      showAchievementToasts(this, checked.unlocked);
    }

    const shade = this.add.rectangle(GAME_W / 2, GAME_H / 2, GAME_W, GAME_H, 0x000000, 0).setDepth(5000).setInteractive();
    this.tweens.add({ targets: shade, fillAlpha: 0.55, duration: 300 });
    const er = this.endlessResult;
    const still = motion.reduced || motion.lowFx;
    const happy = won || !!er?.isBest;
    if (happy) victoryRays(this, GAME_W / 2, GAME_H / 2 - 60, 5000.5, still);
    if (won && !er && !still) confetti(this, GAME_W, 5003);
    if (!won && !er && !still) ash(this, GAME_W, GAME_H, 5000.6);
    const panel = this.add.container(GAME_W / 2, GAME_H / 2).setDepth(5001);
    const bg = this.add.graphics();
    bg.fillStyle(0x000000, 0.35);
    bg.fillRoundedRect(-274, -190, 560, 400, 28);
    bg.fillStyle(C.ink, 1);
    bg.fillRoundedRect(-280, -200, 560, 400, 28);
    bg.fillStyle(C.panel, 1);
    bg.fillRoundedRect(-270, -190, 540, 380, 22);
    bg.fillStyle(0xffffff, 0.05);
    bg.fillRoundedRect(-266, -186, 532, 92, { tl: 20, tr: 20, bl: 6, br: 6 }); // gloss ends under the ribbon
    bg.lineStyle(3, happy ? 0xffc83a : 0xb04a4a, 0.85);
    bg.strokeRoundedRect(-276, -196, 552, 392, 26);
    panel.add(bg);
    panel.add(ribbon(this, -140, er ? 400 : 330, happy ? 0xd89a2a : 0x7a2a2a, happy ? 0x8a5a14 : 0x4a1414));
    panel.add(this.add.text(0, -140, er ? 'Endless Run Over' : won ? 'Victory!' : 'The Gate Fell', textStyle(er ? 40 : 48, happy ? '#fff2c0' : '#ffd0c8')).setOrigin(0.5).setStroke(happy ? '#5a3a0a' : '#2a0a0a', 8));
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
      starSlam(this, star, i < stars, 450 + i * 320, { x: GAME_W / 2 - 90 + i * 90, y: GAME_H / 2 - 40 }, 5004, still);
    }
    if (!er) panel.add(
      this.add
        .text(0, 14, won ? `Lives kept: ${this.sim.lives}/${this.sim.maxLives}` : `You held until wave ${this.sim.waveIndex + 1}`, textStyle(22))
        .setOrigin(0.5),
    );
    if (!er) this.addWaveChart(won, still);
    if (dailyPaid) {
      panel.add(this.add.text(0, 74, `Daily challenge bonus: +${dailyPaid.coins} coins, +${dailyPaid.glowsap} glowsap`, textStyle(16, '#9be86a', false)).setOrigin(0.5));
    }
    if (bloom) {
      const t = this.add.text(206, -40, '+1\nSwiftbloom', { ...textStyle(16, '#ffc0e8'), align: 'center' }).setOrigin(0.5).setName('bloomText').setScale(0);
      panel.add(t);
      this.tweens.add({ targets: t, scale: 1, delay: 1250, duration: 300, ease: 'Back.easeOut' });
    }
    if (won && !er) {
      const full = reward.coins + reward.glowsap <= 0;
      const rt = this.add.text(0, 46, full ? 'Village storage is full!' : '', textStyle(17, TEXT.gold, false)).setOrigin(0.5).setName('rewardText');
      panel.add(rt);
      // the reward rolls up once the stars have landed
      if (!full) countUp(this, rt, [reward.coins, reward.glowsap], ([c, g]) => `Village reward: +${c} coins, +${g} glowsap`, 1400, still);
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
