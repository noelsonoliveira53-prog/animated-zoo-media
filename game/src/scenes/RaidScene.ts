import { leafReveal } from '../ui/transition';
import { campShot, deployMark, drawRaidGround, rubble } from './raid/RaidArt';
import { poseFor, unitPose } from '../systems/gait';
import { ash, confetti, countUp, ribbon, starSlam, victoryRays } from './fx/ResultFx';
import { addLighting } from '../ui/lighting';
import { DEV_TROOPS, devOn } from '../systems/dev';
import Phaser from 'phaser';
import { motion, shake } from '../ui/motion';
import { music } from '../systems/music';
import { themeById } from '../data/musicThemes';
import { CAMP_BUILDINGS, CAMP_TIERS, TROOPS, TROOP_ORDER } from '../data/raid';
import { buildingCenter, buildingRadius, CAMP_COLS, CAMP_OX, CAMP_OY, CAMP_ROWS, CAMP_TILE, generateCamp } from '../systems/camp';
import { RaidSim, type RaidEvent, type Troop } from '../systems/RaidSim';
import { bumpStats, ensureVillage, loadSave, writeSave } from '../systems/save';
import { checkAchievements } from '../systems/achievements';
import { showAchievementToasts } from '../ui/toast';
import { addResources } from '../systems/village';
import { sfx } from '../systems/audio';
import { Button } from '../ui/Button';
import { C, GAME_H, GAME_W, TEXT, textStyle } from '../ui/theme';
import { drawBar } from '../ui/bars';
import { fitWidth } from '../ui/touch';
import { newTrail, stepTrail, type TrailState } from '../systems/hpBar';

// Attack a Murkhorde camp with the army trained at the Ranger Lodge.
export class RaidScene extends Phaser.Scene {
  private sim!: RaidSim;
  private selected: string | null = null;
  private buildingViews = new Map<number, { img: Phaser.GameObjects.Image; bar: Phaser.GameObjects.Graphics; trail: TrailState }>();
  private lastVenomText = -9999;
  private mireZones = new Map<number, Phaser.GameObjects.Arc>();
  private troopViews = new Map<number, { img: Phaser.GameObjects.Image; bar: Phaser.GameObjects.Graphics; trail: TrailState }>();
  private hudText!: Phaser.GameObjects.Text;
  private starIcons: Phaser.GameObjects.Image[] = [];
  private deployButtons: { id: string; c: Phaser.GameObjects.Container; count: Phaser.GameObjects.Text; ring: Phaser.GameObjects.Graphics }[] = [];
  private particles!: Phaser.GameObjects.Particles.ParticleEmitter;
  private done = false;
  private lastBanner = -9999;
  private zone!: Phaser.GameObjects.Graphics;

  constructor() {
    super('Raid');
  }

  create(data: { tier: number; seed: number }): void {
    leafReveal(this, GAME_W, GAME_H); // a gust of leaves uncovers the scene
    music.setMood('battle');
    music.setTheme(themeById('ember'));
    const save = loadSave();
    motion.reduced = !!save.settings.reduceMotion;
    motion.lowFx = !!save.settings.fxLow;
    const camp = generateCamp(data.seed, data.tier);
    // Dev mode: a full army of every troop for testing
    const army = devOn() ? Object.fromEntries(TROOP_ORDER.map((id) => [id, DEV_TROOPS])) : save.army;
    this.sim = new RaidSim(camp, army);
    this.done = false;
    this.lastBanner = -9999;
    this.selected = TROOP_ORDER.find((id) => (army[id] ?? 0) > 0) ?? null;
    this.buildingViews.clear();
    this.mireZones.clear();
    this.troopViews.clear();
    this.deployButtons = [];
    this.starIcons = [];

    this.drawGround();
    for (const b of camp.buildings) {
      const def = CAMP_BUILDINGS[b.type];
      const img = this.add.image(CAMP_OX + b.col * CAMP_TILE, CAMP_OY + b.row * CAMP_TILE, `camp_${b.type}`).setOrigin(0, 0);
      img.setDepth(CAMP_OY + (b.row + def.size) * CAMP_TILE);
      this.buildingViews.set(b.uid, { img, bar: this.add.graphics().setDepth(5000), trail: newTrail(1) });
      if (def.mire) {
        // the muddy ground a Sludge Pit soaks: ground troops wade slowly through it
        const c = buildingCenter(b);
        const zone = this.add.circle(c.x, c.y, def.mire.radius, 0x4a5a1e, 0.32).setStrokeStyle(3, 0x8a9a3a, 0.7).setDepth(1);
        this.mireZones.set(b.uid, zone);
      }
      if (def.ward) {
        // the hush around a Standing Stone: blows land soft on everything inside the ring
        const c = buildingCenter(b);
        const zone = this.add.circle(c.x, c.y, def.ward.radius, 0xb8b8c8, 0.1).setStrokeStyle(2, 0xd8d8e8, 0.5).setDepth(1);
        this.mireZones.set(b.uid, zone);
      }
      if (def.venom) {
        // the sand around a Rattle Trap, where the buried snakes can reach
        const c = buildingCenter(b);
        const zone = this.add.circle(c.x, c.y, def.venom.radius + buildingRadius(b), 0xd8b070, 0.18).setStrokeStyle(2, 0xa8f07a, 0.55).setDepth(1);
        this.mireZones.set(b.uid, zone);
      }
    }
    this.particles = this.add.particles(0, 0, 'dot', { speed: { min: 50, max: 180 }, scale: { start: 0.6, end: 0 }, lifespan: 500, emitting: false });
    this.particles.setDepth(6000);

    // HUD
    const top = this.add.graphics().setDepth(7000);
    top.fillStyle(C.ink, 0.78);
    top.fillRoundedRect(GAME_W / 2 - 330, 8, 660, 62, 18);
    this.add.text(GAME_W / 2 - 310, 18, CAMP_TIERS[camp.tier].name, textStyle(18, TEXT.gold)).setDepth(7001);
    this.hudText = this.add.text(GAME_W / 2 - 310, 44, '', textStyle(16)).setDepth(7001);
    for (let i = 0; i < 3; i++) this.starIcons.push(this.add.image(GAME_W / 2 + 230 + i * 34, 39, 'star_empty').setScale(0.55).setDepth(7001));
    new Button(this, 90, 40, 'End', { width: 120, height: 50, fontSize: 20, color: C.danger, onClick: () => this.sim.finish() }).setDepth(7001);
    this.buildDeployBar();

    this.input.on('pointerdown', (p: Phaser.Input.Pointer) => this.tryDeploy(p.worldX, p.worldY));
    this.input.on('pointermove', (p: Phaser.Input.Pointer) => {
      if (p.isDown) this.tryDeploy(p.worldX, p.worldY, true);
    });
    this.cameras.main.fadeIn(250, 16, 38, 27);
    this.banner('Tap outside the camp to send in troops');
  }

  private drawGround(): void {
    drawRaidGround(this, { x: CAMP_OX + 2 * CAMP_TILE, y: CAMP_OY, w: (CAMP_COLS - 4) * CAMP_TILE, h: CAMP_ROWS * CAMP_TILE }, GAME_W, GAME_H);
    addLighting(this, 6500); // above the field and buildings, under the HUD (7000+)
    // Deploy-forbidden glow around buildings is drawn when a troop is selected.
    this.zone = this.add.graphics().setDepth(-5);
  }

  private showForbidden(on: boolean): void {
    this.zone.clear();
    if (!on) return;
    this.zone.fillStyle(0xff5d4a, 0.12);
    for (const b of this.sim.camp.buildings) {
      if (b.hp <= 0) continue;
      const c = buildingCenter(b);
      this.zone.fillCircle(c.x, c.y, (CAMP_BUILDINGS[b.type].size * CAMP_TILE) / 2 + 46);
    }
  }

  private buildDeployBar(): void {
    const ids = TROOP_ORDER.filter((id) => (this.sim.army[id] ?? 0) > 0);
    const w = Math.max(1, ids.length) * 110 + 20;
    const bg = this.add.graphics().setDepth(7000);
    bg.fillStyle(C.ink, 0.8);
    bg.fillRoundedRect(GAME_W / 2 - w / 2, GAME_H - 92, w, 84, 18);
    if (!ids.length) {
      this.add.text(GAME_W / 2, GAME_H - 50, 'No troops! Train some at the Ranger Lodge.', textStyle(18, TEXT.heart)).setOrigin(0.5).setDepth(7001);
      return;
    }
    ids.forEach((id, i) => {
      const x = GAME_W / 2 - w / 2 + 65 + i * 110;
      const c = this.add.container(x, GAME_H - 50).setDepth(7001);
      const ring = this.add.graphics();
      c.add(ring);
      c.add(this.add.image(0, -8, `troop_${id}`).setScale(1.3));
      const count = this.add.text(0, 22, '', textStyle(16, TEXT.gold)).setOrigin(0.5);
      c.add(count);
      c.setSize(96, 76).setInteractive({ useHandCursor: true });
      c.on('pointerdown', (_p: Phaser.Input.Pointer, _x: number, _y: number, ev: Phaser.Types.Input.EventData) => {
        ev.stopPropagation();
        sfx.unlock();
        sfx.click();
        this.selected = id;
        this.refreshBar();
      });
      this.deployButtons.push({ id, c, count, ring });
    });
    this.refreshBar();
  }

  private refreshBar(): void {
    for (const b of this.deployButtons) {
      const n = this.sim.army[b.id] ?? 0;
      b.count.setScale(1).setText(`${TROOPS[b.id].name.split(' ')[1]} ×${n}`);
      fitWidth(b.count, 102); // big counts ("Scavenger ×30") stay inside their 110-wide slot
      b.c.setAlpha(n > 0 ? 1 : 0.4);
      b.ring.clear();
      b.ring.fillStyle(this.selected === b.id ? C.panelLight : 0x22382a, 1);
      b.ring.fillRoundedRect(-48, -38, 96, 76, 12);
      b.ring.lineStyle(3, this.selected === b.id ? C.gold : 0x556655, 1);
      b.ring.strokeRoundedRect(-48, -38, 96, 76, 12);
    }
  }

  private lastDeploy = 0;
  private tryDeploy(x: number, y: number, drag = false): void {
    if (this.done || !this.selected) return;
    if (y > GAME_H - 96 || y < 74) return; // HUD areas
    if (drag && this.time.now - this.lastDeploy < 140) return;
    if ((this.sim.army[this.selected] ?? 0) <= 0) {
      this.selected = TROOP_ORDER.find((id) => (this.sim.army[id] ?? 0) > 0) ?? null;
      this.refreshBar();
      if (!this.selected) return;
    }
    sfx.unlock();
    const t = this.sim.deploy(this.selected, { x, y });
    if (!t) {
      if (!drag) {
        this.showForbidden(true);
        this.time.delayedCall(700, () => this.showForbidden(false));
        this.floatText(x, y, 'Too close!', TEXT.heart);
      }
      return;
    }
    this.lastDeploy = this.time.now;
    this.refreshBar();
  }

  update(_t: number, deltaMs: number): void {
    if (!this.done) this.sim.update(Math.min(deltaMs / 1000, 0.1));
    for (const ev of this.sim.drainEvents()) this.handle(ev);
    this.sync(Math.min(deltaMs / 1000, 0.1));
  }

  private handle(ev: RaidEvent): void {
    switch (ev.type) {
      case 'deploy': {
        const img = this.add.image(ev.troop.pos.x, ev.troop.pos.y, `troop_${ev.troop.def.id}`).setScale(0).setData('popping', true);
        this.tweens.add({ targets: img, scale: 1, duration: 180, ease: 'Back.easeOut', onComplete: () => img.setData('popping', false) });
        this.troopViews.set(ev.troop.uid, { img, bar: this.add.graphics(), trail: newTrail(1) });
        this.particles.setParticleTint(0xd9c39a);
        this.particles.explode(6, ev.troop.pos.x, ev.troop.pos.y);
        // a banner where a squad lands (at most one every 0.6 s, so drag-deploys don't plant a forest of flags)
        const banner = this.time.now - this.lastBanner > 600;
        if (banner) this.lastBanner = this.time.now;
        deployMark(this, ev.troop.pos.x, ev.troop.pos.y, banner);
        sfx.click();
        break;
      }
      case 'buildingHit': {
        const v = this.buildingViews.get(ev.building.uid);
        if (v) {
          // a building under a Standing Stone's hush flashes a dull lavender instead of white
          v.img.setTintFill(this.sim.wardCut(ev.building) > 0 ? 0xb8b8e8 : 0xffffff);
          this.time.delayedCall(50, () => v.img.clearTint());
        }
        sfx.melee();
        break;
      }
      case 'destroyed': {
        const v = this.buildingViews.get(ev.building.uid);
        const c = buildingCenter(ev.building);
        if (v) {
          this.tweens.add({ targets: v.img, alpha: 0.25, scaleY: 0.5, y: v.img.y + 20, duration: 300 });
          v.bar.clear();
        }
        const zone = this.mireZones.get(ev.building.uid);
        if (zone) this.tweens.add({ targets: zone, alpha: 0, duration: 400 });
        this.particles.setParticleTint(0x8a6440);
        this.particles.explode(24, c.x, c.y);
        rubble(this, c.x, c.y, CAMP_BUILDINGS[ev.building.type].size * CAMP_TILE, v?.img.depth ?? c.y);
        shake(this, 150, 0.005);
        if (ev.loot.coins + ev.loot.glowsap > 0) this.floatText(c.x, c.y - 30, `+${ev.loot.coins}c +${ev.loot.glowsap}s`, TEXT.gold);
        sfx.boom();
        break;
      }
      case 'shot': {
        // the defense recoils, its shot flies, and the troop flashes when it lands
        const bv = this.buildingViews.get(ev.building.uid);
        if (bv && !motion.reduced) this.tweens.add({ targets: bv.img, scaleY: 0.94, duration: 60, yoyo: true });
        const target = ev.target;
        campShot(this, ev.from, ev.to, ev.splash, motion.lowFx, () => {
          const tv = this.troopViews.get(target.uid);
          if (tv && tv.img.active) {
            tv.img.setTintFill(0xffffff);
            this.time.delayedCall(70, () => tv.img.active && tv.img.clearTint());
          }
          this.particles.setParticleTint(ev.splash ? 0x6a5a3a : 0xd8ffb0);
          this.particles.explode(ev.splash ? 10 : 4, ev.to.x, ev.to.y - 6);
        });
        break;
      }
      case 'mend': {
        const c = buildingCenter(ev.from);
        const ring = this.add.circle(c.x, c.y, 20, 0x9bff8a, 0.25).setDepth(5400);
        this.tweens.add({ targets: ring, scale: 6, alpha: 0, duration: 500, onComplete: () => ring.destroy() });
        for (const b of ev.healed) {
          const bc = buildingCenter(b);
          this.particles.setParticleTint(0x9bff8a);
          this.particles.explode(4, bc.x, bc.y - 10);
        }
        sfx.trait('mend');
        break;
      }
      case 'troopHeal': {
        const ring = this.add.circle(ev.troop.pos.x, ev.troop.pos.y, 14, 0x9bff8a, 0.3).setDepth(5400);
        this.tweens.add({ targets: ring, scale: 6, alpha: 0, duration: 450, onComplete: () => ring.destroy() });
        for (const o of ev.healed) {
          this.particles.setParticleTint(0x9bff8a);
          this.particles.explode(3, o.pos.x, o.pos.y - 10);
        }
        break;
      }
      case 'swarm': {
        // a cloud of hornets boils out of the broken hive and stings everyone close by
        const c = buildingCenter(ev.building);
        const ring = this.add.circle(c.x, c.y, ev.radius, 0xffc83a, 0.18).setStrokeStyle(3, 0xffc83a, 0.8).setDepth(5400).setScale(0.3);
        this.tweens.add({ targets: ring, scale: 1, alpha: 0, duration: 550, onComplete: () => ring.destroy() });
        this.particles.setParticleTint(0x2a2010);
        this.particles.explode(30, c.x, c.y - 10);
        for (const t of ev.stung) {
          this.particles.setParticleTint(0xffc83a);
          this.particles.explode(4, t.pos.x, t.pos.y - 8);
        }
        if (ev.stung.length) this.floatText(c.x, c.y - 52, 'Swarm!', '#ffd84a');
        sfx.trait('swarm');
        break;
      }
      case 'poisoned': {
        // rattlesnakes strike from the sand at a passing troop
        this.particles.setParticleTint(0xa8f07a);
        this.particles.explode(6, ev.troop.pos.x, ev.troop.pos.y - 6);
        if (this.time.now - this.lastVenomText > 700) {
          this.lastVenomText = this.time.now; // several troops bitten at once share one label and one hiss
          this.floatText(ev.troop.pos.x, ev.troop.pos.y - 40, 'Venom!', '#b8f08a');
          sfx.trait('venom');
        }
        break;
      }
      case 'troopDown': {
        const v = this.troopViews.get(ev.troop.uid);
        if (v) {
          this.tweens.add({ targets: v.img, alpha: 0, scale: 1.4, duration: 200, onComplete: () => v.img.destroy() });
          v.bar.destroy();
          this.troopViews.delete(ev.troop.uid);
        }
        break;
      }
      case 'end':
        this.endRaid();
        break;
      default:
        break;
    }
  }

  private sync(dt: number): void {
    for (const t of this.sim.troops) {
      const v = this.troopViews.get(t.uid);
      if (!v || !t.alive) continue;
      this.drawTroop(t, v.img, v.bar, v.trail, dt);
    }
    for (const b of this.sim.camp.buildings) {
      const v = this.buildingViews.get(b.uid);
      if (!v || b.hp <= 0) continue;
      v.bar.clear();
      const frac = Math.max(0, b.hp / b.maxHp);
      stepTrail(v.trail, frac, dt);
      if (b.hp < b.maxHp) {
        const c = buildingCenter(b);
        const w = CAMP_BUILDINGS[b.type].size * CAMP_TILE * 0.7;
        const y = c.y - (CAMP_BUILDINGS[b.type].size * CAMP_TILE) / 2 - 6;
        // enemy buildings read orange, turning red when nearly razed
        drawBar(v.bar, c.x - w / 2, y, w, 6, frac, v.trail.trail, frac > 0.3 ? 0xff9f43 : 0xff5d4a);
      }
    }
    const pct = Math.round(this.sim.destruction * 100);
    this.hudText.setText(`${pct}% destroyed   •   ${Math.ceil(this.sim.timeLeft)}s   •   Loot ${this.sim.loot.coins}c / ${this.sim.loot.glowsap}s`);
    const stars = this.sim.stars;
    this.starIcons.forEach((img, i) => img.setTexture(i < stars ? 'star' : 'star_empty'));
  }

  private drawTroop(t: Troop, img: Phaser.GameObjects.Image, bar: Phaser.GameObjects.Graphics, trail: TrailState, dt: number): void {
    const lift = t.def.flying ? 18 : 0;
    // troops share the defense soldiers' poses: a marching step, a chopping arc at their target, flyers flap
    const px = (img.getData('px') as number | undefined) ?? t.pos.x;
    const py = (img.getData('py') as number | undefined) ?? t.pos.y;
    const walking = Math.hypot(t.pos.x - px, t.pos.y - py) > 0.2;
    img.setData('px', t.pos.x).setData('py', t.pos.y);
    if (Math.abs(t.pos.x - px) > 0.3) img.setFlipX(t.pos.x < px);
    const facing = img.flipX ? -1 : 1;
    const pose = motion.reduced
      ? { lift: 0, sx: 1, sy: 1, rot: 0 }
      : t.def.flying
        ? poseFor('flap', this.time.now / 80 + t.uid)
        : unitPose(walking ? 'walk' : t.targetUid ? 'fight' : 'idle', this.time.now, t.uid * 1.3, facing);
    img.setPosition(t.pos.x, t.pos.y - 10 - lift - pose.lift - (t.def.flying ? Math.sin(this.time.now / 300 + t.uid) * 3 : 0)).setDepth(t.pos.y + (t.def.flying ? 3000 : 0)).setRotation(pose.rot);
    if (!img.getData('popping')) img.setScale(pose.sx, pose.sy);
    bar.clear();
    if (t.tunneling) {
      // Mole Tunneler underground: only a moving ridge of churned earth shows where it is
      img.setAlpha(0);
      bar.fillStyle(0x6a4a2a, 0.9);
      bar.fillEllipse(t.pos.x, t.pos.y - 2, 22, 10);
      bar.fillStyle(0x8a6a40, 1);
      for (let k = 0; k < 3; k++) bar.fillCircle(t.pos.x - 6 + k * 6, t.pos.y - 5 - ((k + Math.floor(this.time.now / 90)) % 2) * 2, 2.5);
      bar.setDepth(t.pos.y);
      return;
    }
    if (img.alpha < 1) {
      img.setAlpha(1);
      this.particles.setParticleTint(0x8a6a40);
      this.particles.explode(10, t.pos.x, t.pos.y); // pops up in a spray of dirt
    }
    if (t.poisonT! > 0) img.setTint(0xa8f07a);
    else if (img.isTinted && !img.tintFill) img.clearTint();
    const frac = Math.max(0, t.hp / t.maxHp);
    stepTrail(trail, frac, dt);
    if (t.hp < t.maxHp) {
      // our troops read blue like the defense Wardens (green while poisoned, red when nearly down)
      drawBar(bar, t.pos.x - 12, t.pos.y - 33 - lift, 24, 4, frac, trail.trail, t.poisonT! > 0 ? 0x8ad84a : frac > 0.3 ? 0x7fc8ff : 0xff7a5a);
      bar.setDepth(t.pos.y + 3001);
    }
  }

  private endRaid(): void {
    if (this.done) return;
    this.done = true;
    music.setMood('calm');
    const stars = this.sim.stars;
    // Bank loot and return surviving troops; the next raid gets fresh camps.
    const save = loadSave();
    const v = ensureVillage(save);
    const got = addResources(v, this.sim.loot.coins, this.sim.loot.glowsap);
    save.army = this.sim.survivingArmy();
    save.raidSeed = (save.raidSeed ?? 1) + 1;
    const pits = this.sim.camp.buildings.filter((b) => b.type === 'sludge' && b.hp <= 0).length;
    const counted = bumpStats(save, { raidsWon: stars > 0 ? 1 : 0, stronghold3: stars === 3 && this.sim.camp.tier === 2 ? 1 : 0, sludgeDestroyed: pits });
    const checked = checkAchievements(counted);
    if (!devOn()) {
      // dev-mode raids never touch the real army, loot or stats
      writeSave(checked.save);
      this.time.delayedCall(600, () => showAchievementToasts(this, checked.unlocked));
    }
    if (!music.stinger(stars > 0 ? 'victory' : 'defeat')) stars > 0 ? sfx.victory() : sfx.defeat();

    const shade = this.add.rectangle(GAME_W / 2, GAME_H / 2, GAME_W, GAME_H, 0x000000, 0.5).setDepth(8000).setInteractive();
    shade.on('pointerdown', (_p: Phaser.Input.Pointer, _x: number, _y: number, ev: Phaser.Types.Input.EventData) => ev.stopPropagation());
    const won = stars > 0;
    const still = motion.reduced || motion.lowFx;
    if (won) victoryRays(this, GAME_W / 2, GAME_H / 2 - 50, 8000.5, still);
    if (won && !still) confetti(this, GAME_W, 8003);
    if (!won && !still) ash(this, GAME_W, GAME_H, 8000.6);
    const panel = this.add.container(GAME_W / 2, GAME_H / 2).setDepth(8001);
    const bg = this.add.graphics();
    bg.fillStyle(0x000000, 0.35);
    bg.fillRoundedRect(-264, -170, 540, 360, 26);
    bg.fillStyle(C.ink, 1);
    bg.fillRoundedRect(-270, -180, 540, 360, 26);
    bg.fillStyle(C.panel, 1);
    bg.fillRoundedRect(-262, -172, 524, 344, 22);
    bg.fillStyle(0xffffff, 0.05);
    bg.fillRoundedRect(-258, -168, 516, 84, { tl: 20, tr: 20, bl: 6, br: 6 });
    bg.lineStyle(3, won ? 0xffc83a : 0xb04a4a, 0.85);
    bg.strokeRoundedRect(-266, -176, 532, 352, 24);
    panel.add(bg);
    panel.add(ribbon(this, -128, 360, won ? 0xd89a2a : 0x7a2a2a, won ? 0x8a5a14 : 0x4a1414));
    panel.add(this.add.text(0, -128, won ? 'Raid Successful!' : 'Raid Failed', textStyle(38, won ? '#fff2c0' : '#ffd0c8')).setOrigin(0.5).setStroke(won ? '#5a3a0a' : '#2a0a0a', 8));
    for (let i = 0; i < 3; i++) {
      const s = this.add.image(-80 + i * 80, -50, i < stars ? 'star' : 'star_empty').setScale(0);
      panel.add(s);
      starSlam(this, s, i < stars, 420 + i * 300, { x: GAME_W / 2 - 80 + i * 80, y: GAME_H / 2 - 50 }, 8004, still);
    }
    const pct = this.add.text(0, 20, '', textStyle(20)).setOrigin(0.5).setName('raidPct');
    panel.add(pct);
    countUp(this, pct, [Math.round(this.sim.destruction * 100)], ([p]) => `${p}% of the camp destroyed`, 300, still);
    const full = got.coins < this.sim.loot.coins || got.glowsap < this.sim.loot.glowsap;
    const lootText = this.add.text(0, 54, '', textStyle(18, TEXT.gold, false)).setOrigin(0.5).setName('raidLoot');
    panel.add(lootText);
    countUp(this, lootText, [got.coins, got.glowsap], ([c, g]) => `Loot: +${c} coins, +${g} glowsap${full ? ' (storage full)' : ''}`, 1300, still);
    panel.add(new Button(this, 0, 122, 'Back to Village', { width: 260, color: C.leaf, onClick: () => this.scene.start('Village') }));
    panel.setScale(0.6).setAlpha(0);
    this.tweens.add({ targets: panel, scale: 1, alpha: 1, duration: 300, ease: 'Back.easeOut' });
  }

  private banner(msg: string): void {
    const t = this.add.text(GAME_W / 2, 100, msg, textStyle(20)).setOrigin(0.5).setDepth(7002);
    this.tweens.add({ targets: t, alpha: 0, delay: 2500, duration: 500, onComplete: () => t.destroy() });
  }

  private floatText(x: number, y: number, text: string, color: string): void {
    const t = this.add.text(x, y, text, textStyle(16, color)).setOrigin(0.5).setDepth(7500);
    this.tweens.add({ targets: t, y: y - 36, alpha: 0, duration: 900, onComplete: () => t.destroy() });
  }
}
