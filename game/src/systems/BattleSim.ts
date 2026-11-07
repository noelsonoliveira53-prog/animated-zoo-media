import type { DamageType, EnemyDef, HeroDef, LevelDef, SoldierStats, TargetMode, TowerDef, Vec2 } from '../data/types';
import { SPELLS } from '../data/spells';
import { NO_MODS, type Modifiers } from '../data/daily';
import { HEROES, HERO_MAX_LEVEL, HERO_XP, heroLevelMult, levelForXp } from '../data/heroes';
import { ENEMIES } from '../data/enemies';
import { TOWERS, sellValue, towerStats } from '../data/towers';
import { Path } from './path';
import { computeDamage } from './combat';
import { buildSchedule, earlyCallBonus, type SpawnEvent } from './waves';

// Pure, renderer-free battle simulation. The Phaser scene only reads state and drains events,
// which lets the headless balance simulator run the exact same rules.

export interface Enemy {
  uid: number;
  def: EnemyDef;
  hp: number;
  maxHp: number;
  path: number;
  dist: number; // distance travelled along its path
  pos: Vec2;
  slowFactor: number;
  slowTime: number;
  alive: boolean;
  blockedBy: number; // soldier uid holding this enemy, 0 if free
  attackCd: number;
  shield: number;
  maxShield: number;
  healCd: number;
  chillCd: number;
  underground: boolean;
  burrowCd: number;
  spawnCd: number;
  spawned: number;
  phase: number; // index of next boss phase to trigger
  speedMult: number;
  enraged: boolean;
  hasteTime: number; // seconds left of a spore haste
  hasteMult: number;
  armor: number; // current armor (brittle enemies lose some on every hit)
  landed: boolean; // swooping flyers spend part of their cycle on the ground
  swoopCd: number;
  blinkCd: number;
  gustCd: number;
  growT: number; // seconds a Rotseed has been growing
  fed: number; // times a Gorgegrub has fed
  shockCd: number;
  boltCd: number; // Stormcaller lightning timer
  molted: boolean; // Shellsnap has shed its shell
  inkCd: number; // Inkspitter cloud cooldown
  rangedCd: number; // Deckgunner reload
  anchorCd: number; // Ironkeel: time until it next drops / lifts anchor
  anchored: boolean;
  drumCd: number; // Barkdrum: time to its next beat
  phaseCd: number; // Mistfox: time until it fades / returns
  riledAt: number; // Howler: sim time of the last rile (at most one every 0.5s)
  snatchCd: number; // Canopy Harrier: time until it can carry off another soldier
  phased: boolean;
  cleanseCd: number; // Tidecaller wash timer
  mirrored: boolean; // Shimmerjack already shed its decoys
  chargeTime: number; // seconds left of a Steamrunner bolt
  chargeCd: number;
  mr: number; // current magic resist (Shiftscales swap armor and magic resist on a timer)
  shifted: boolean; // Shiftscale is in its second (slick-skin) form
  shiftCd: number;
  reviveCd: number;
  revived: boolean; // raised by an Idol Keeper: pays no bounty and can't be raised again
  sinceHit: number; // seconds since it last took damage (regen enemies heal once this passes their delay)
}

export interface Soldier {
  uid: number;
  stun?: number; // seconds left of a Sparkeel shock (no attacking or blocking)
  towerUid: number;
  index: number; // slot within its squad (for formation offsets)
  pos: Vec2;
  home: Vec2; // rally position
  hp: number;
  maxHp: number;
  alive: boolean;
  respawnTimer: number;
  targetUid: number; // enemy uid engaged, 0 if idle
  attackCd: number;
  stats: SoldierStats;
  anchor: Vec2; // centre of the area this soldier guards
  spawnAt: Vec2; // where it reappears after respawning
  life: number; // seconds left for summoned soldiers; Infinity for tower squads
  summoned: boolean;
}

export interface Strike {
  uid: number;
  pos: Vec2;
  timer: number;
  spellId: string;
}

export interface Hero {
  uid: number;
  stun?: number; // seconds left of a Sparkeel shock
  def: HeroDef;
  pos: Vec2;
  dest: Vec2 | null; // move order
  hp: number;
  maxHp: number;
  alive: boolean;
  respawnTimer: number;
  level: number;
  xp: number;
  attackCd: number;
  skillCd: number;
  tossCd: number;
  targetUid: number;
  facing: number; // -1 left, 1 right
}

export interface Tower {
  uid: number;
  def: TowerDef;
  tier: number;
  slot: number;
  pos: Vec2;
  cooldown: number;
  target: TargetMode;
  rally: Vec2 | null; // for soldier towers
  spec: string | null; // chosen top-tier specialization
  frozen: number; // seconds left frozen (cannot fire)
  chillImmune: number; // seconds left before it can be frozen again (prevents perma-freeze)
}

export interface Projectile {
  uid: number;
  towerUid: number;
  pos: Vec2;
  targetUid: number;
  lastTargetPos: Vec2;
  speed: number;
  damage: number;
  damageType: TowerDef['damageType'];
  splash: number;
  slow?: { factor: number; duration: number };
  color: number;
  homing: boolean;
  hitsAir: boolean;
  origin: Vec2;
  travel: number; // straight-line distance at launch (for arc rendering)
  kind: string; // tower id, for rendering
  pierce: number; // share of armor ignored
  chain?: { count: number; falloff: number; range: number };
}

export type SimEvent =
  | { type: 'spawn'; enemy: Enemy }
  | { type: 'shoot'; tower: Tower; projectile: Projectile }
  | { type: 'hit'; enemy: Enemy; damage: number; pos: Vec2 }
  | { type: 'splash'; pos: Vec2; radius: number; color: number }
  | { type: 'kill'; enemy: Enemy; bounty: number }
  | { type: 'leak'; enemy: Enemy; lives: number }
  | { type: 'waveStart'; index: number; bonus: number; income: number }
  | { type: 'waveCleared'; index: number }
  | { type: 'build'; tower: Tower }
  | { type: 'upgrade'; tower: Tower }
  | { type: 'sell'; tower: Tower; refund: number }
  | { type: 'melee'; pos: Vec2 }
  | { type: 'chain'; points: Vec2[]; color: number }
  | { type: 'specialize'; tower: Tower }
  | { type: 'spellCast'; spellId: string; pos: Vec2 }
  | { type: 'strike'; spellId: string; uid: number; pos: Vec2; radius: number; hits: Enemy[] }
  | { type: 'summonGone'; soldier: Soldier }
  | { type: 'heroSkill'; hero: Hero; hits: Enemy[]; healed?: Vec2[] }
  | { type: 'heroShoot'; hero: Hero; projectile: Projectile }
  | { type: 'heroLevel'; hero: Hero }
  | { type: 'heroDown'; hero: Hero }
  | { type: 'heroBack'; hero: Hero }
  | { type: 'heal'; source: Enemy; targets: Enemy[]; radius: number }
  | { type: 'chill'; source: Enemy; towers: Tower[]; radius: number }
  | { type: 'burrow'; enemy: Enemy; down: boolean }
  | { type: 'enrage'; enemy: Enemy }
  | { type: 'swoop'; enemy: Enemy; landed: boolean }
  | { type: 'blink'; enemy: Enemy; from: Vec2; to: Vec2 }
  | { type: 'shift'; enemy: Enemy; scales: boolean }
  | { type: 'thorns'; pos: Vec2 }
  | { type: 'charge'; enemy: Enemy }
  | { type: 'echo'; enemy: Enemy }
  | { type: 'grow'; enemy: Enemy }
  | { type: 'bolt'; source: Enemy; tower: Tower }
  | { type: 'mirage'; enemy: Enemy; decoys: Enemy[] }
  | { type: 'pilfer'; enemy: Enemy; coins: number }
  | { type: 'crack'; enemy: Enemy }
  | { type: 'molt'; enemy: Enemy }
  | { type: 'enemyShot'; enemy: Enemy; to: Vec2 }
  | { type: 'keg'; pos: Vec2; radius: number; hits: Vec2[] }
  | { type: 'anchor'; enemy: Enemy; down: boolean }
  | { type: 'drum'; enemy: Enemy; radius: number; hasted: Enemy[] }
  | { type: 'leech'; enemy: Enemy; amount: number }
  | { type: 'mist'; enemy: Enemy; on: boolean }
  | { type: 'dodge'; enemy: Enemy }
  | { type: 'rile'; enemy: Enemy; speedMult: number }
  | { type: 'snatch'; enemy: Enemy; pos: Vec2 }
  | { type: 'grief'; enemy: Enemy; radius: number; mourners: Enemy[] }
  | { type: 'ink'; enemy: Enemy; pos: Vec2; radius: number; duration: number }
  | { type: 'cleanse'; source: Enemy; washed: Enemy[]; radius: number }
  | { type: 'ground'; from: Enemy; to: Enemy; damage: number }
  | { type: 'feed'; enemy: Enemy; from: Vec2 }
  | { type: 'shock'; source: Enemy; radius: number; hits: Vec2[] }
  | { type: 'revive'; source: Enemy; enemy: Enemy }
  | { type: 'gust'; source: Enemy; targets: { enemy: Enemy; from: Vec2 }[]; radius: number }
  | { type: 'glare'; enemy: Enemy; towers: Tower[]; radius: number }
  | { type: 'coral'; source: Enemy; targets: Enemy[]; radius: number }
  | { type: 'spores'; enemy: Enemy; radius: number; hasted: Enemy[] }
  | { type: 'shieldBreak'; enemy: Enemy }
  | { type: 'phase'; enemy: Enemy; message: string }
  | { type: 'split'; parent: Enemy; children: Enemy[] }
  | { type: 'soldierDown'; soldier: Soldier }
  | { type: 'victory' }
  | { type: 'defeat' };

export type BattleStatus = 'prep' | 'running' | 'victory' | 'defeat';

/** Seconds of countdown before the next wave auto-starts. */
export const WAVE_GAP = 14;
export const FIRST_WAVE_GAP = 25;
const SOLDIER_SPEED = 110;
/** After thawing, a tower can't be re-frozen for this long, so packs of chillers can't lock it forever. */
const THAW_IMMUNITY = 3;
const C_SHIELD = 0xc9a66b; // Bramble's bark shield

/** Supply coins the sanctuary sends at the start of each wave (index 0-based). Wave 1 gets none. */
export function waveIncome(index: number): number {
  return index === 0 ? 0 : 10 + index * 3;
}
const SOLDIER_REACH = 18;
const ENGAGE_RADIUS = 70;

export class BattleSim {
  readonly level: LevelDef;
  readonly paths: Path[];
  coins: number;
  lives: number;
  status: BattleStatus = 'prep';
  time = 0;
  /** Recently killed enemies an Idol Keeper could raise (pruned as they go stale). */
  fallen: { id: string; path: number; dist: number; pos: Vec2; at: number }[] = [];

  waveIndex = -1; // index of last started wave
  waveCountdown = FIRST_WAVE_GAP;
  private schedules: { events: SpawnEvent[]; cursor: number; t: number }[] = [];

  enemies: Enemy[] = [];
  towers: (Tower | null)[];
  projectiles: Projectile[] = [];
  soldiers: Soldier[] = [];
  hero: Hero | null = null;
  strikes: Strike[] = [];
  spellCd: Record<string, number> = {};
  /** Ink clouds on the road: towers can't see enemies inside them until they fade. */
  inkClouds: { pos: Vec2; radius: number; t: number }[] = [];
  healTotal = 0; // health restored to soldiers by the hero (Sorrel), for the Field Medic achievement
  events: SimEvent[] = [];

  private nextUid = 1;

  /** Multiplier on tower shot damage (from the village Defense Workshop). */
  towerDamageMult = 1;

  /** Daily-challenge modifiers (neutral for normal battles). */
  readonly mods: Modifiers;
  /** Starting lives (for star ratings). */
  readonly maxLives: number;

  /** Multiplier on Grove Call Rangers' hp and damage (from the village Ranger Lodge). */
  rangerMult = 1;

  /** Full cooldown of a spell after the village shrine's discount. */
  spellCooldown(id: string): number {
    return SPELLS[id].cooldown * this.spellCdMult;
  }

  /** Multiplier on spell cooldowns (from the village Moonpetal Shrine). */
  spellCdMult = 1;

  /** Source of chance (crit rolls). Headless runs pass a seeded one so each seed replays exactly. */
  random: () => number = Math.random;

  constructor(
    level: LevelDef,
    heroId: string | null = null,
    opts: { towerDamageMult?: number; bonusCoins?: number; rangerMult?: number; spellCdMult?: number; heroLevel?: number; mods?: Modifiers; random?: () => number } = {},
  ) {
    this.level = level;
    if (opts.random) this.random = opts.random;
    this.mods = opts.mods ?? NO_MODS;
    if (this.mods.noHero) heroId = null;
    this.towerDamageMult = opts.towerDamageMult ?? 1;
    this.rangerMult = opts.rangerMult ?? 1;
    this.spellCdMult = opts.spellCdMult ?? 1;
    this.paths = level.paths.map((p) => new Path(p));
    this.coins = Math.round(level.startCoins * this.mods.startCoinsMult) + (opts.bonusCoins ?? 0);
    this.lives = this.mods.lives ?? level.lives;
    this.maxLives = this.lives;
    this.towers = level.slots.map(() => null);
    if (heroId && HEROES[heroId]) {
      const def = HEROES[heroId];
      const spawn = this.heroSpawnPoint();
      this.hero = {
        uid: this.nextUid++,
        def,
        pos: { ...spawn },
        dest: null,
        hp: def.hp,
        maxHp: def.hp,
        alive: true,
        respawnTimer: 0,
        level: 1,
        xp: 0,
        attackCd: 0,
        skillCd: 0,
        tossCd: 0,
        targetUid: 0,
        facing: -1,
      };
      // Trained heroes start the battle at a higher level.
      const start = Math.max(1, Math.min(HERO_MAX_LEVEL, opts.heroLevel ?? 1));
      if (start > 1) {
        this.hero.level = start;
        this.hero.xp = HERO_XP[start - 1];
        this.hero.maxHp = this.hero.hp = Math.round(def.hp * heroLevelMult(start));
      }
    }
  }

  /** Heroes start (and respawn) near the gate, on the last stretch of the first road. */
  heroSpawnPoint(): Vec2 {
    if (this.level.heroSpawn) return { ...this.level.heroSpawn };
    const p = this.paths[0];
    return p.pointAt(p.length - 260);
  }

  // ---------- spells ----------

  spellReady(id: string): boolean {
    return (this.spellCd[id] ?? 0) <= 0;
  }

  /** Cast a global spell at a point. Reinforcements must target the road. */
  castSpell(id: string, pos: Vec2): boolean {
    const def = SPELLS[id];
    if (!def || this.mods.noSpells || !this.spellReady(id) || !this.isActive()) return false;
    if (def.kind === 'reinforce') {
      let best: { point: Vec2; distance: number } | null = null;
      for (const path of this.paths) {
        const c = path.closest(pos);
        if (!best || c.distance < best.distance) best = c;
      }
      if (!best || best.distance > 60) return false;
      const anchor = { ...best.point };
      for (let i = 0; i < (def.count ?? 1); i++) {
        const base = def.soldier!;
        const stats = { ...base, hp: Math.round(base.hp * this.rangerMult), damage: base.damage * this.rangerMult };
        const home = this.formation(anchor, i);
        this.soldiers.push({
          uid: this.nextUid++,
          towerUid: 0,
          index: i,
          pos: { x: home.x, y: home.y },
          home,
          hp: stats.hp,
          maxHp: stats.hp,
          alive: true,
          respawnTimer: 0,
          targetUid: 0,
          attackCd: 0,
          stats,
          anchor,
          spawnAt: home,
          life: def.duration ?? 10,
          summoned: true,
        });
      }
    } else if (def.kind === 'snare') {
      // Instant: bramble burst roots ground enemies in the area.
      const radius = def.radius ?? 90;
      const hits = this.enemies.filter((e) => e.alive && !e.underground && !this.airborne(e) && Math.hypot(e.pos.x - pos.x, e.pos.y - pos.y) <= radius + e.def.radius);
      for (const e of hits) {
        if (def.slow) {
          this.slow(e, def.slow.factor, def.slow.duration);
        }
        this.applyDamage(e, computeDamage(def.damage ?? 0, def.damageType ?? 'physical', this.res(e)), def.damageType ?? 'physical');
      }
    } else {
      this.strikes.push({ uid: this.nextUid++, pos: { ...pos }, timer: def.delay ?? 0, spellId: id });
    }
    this.spellCd[id] = this.spellCooldown(id);
    this.events.push({ type: 'spellCast', spellId: id, pos: { ...pos } });
    return true;
  }

  private updateSpells(dt: number): void {
    for (const id of Object.keys(this.spellCd)) this.spellCd[id] = Math.max(0, this.spellCd[id] - dt);
    for (const st of this.strikes) {
      st.timer -= dt;
      if (st.timer > 0) continue;
      const def = SPELLS[st.spellId];
      const radius = def.radius ?? 60;
      const hits = this.enemies.filter((e) => e.alive && !e.underground && Math.hypot(e.pos.x - st.pos.x, e.pos.y - st.pos.y) <= radius + e.def.radius);
      for (const e of hits) this.applyDamage(e, computeDamage(def.damage ?? 0, def.damageType ?? 'physical', this.res(e)), def.damageType ?? 'physical');
      this.events.push({ type: 'strike', spellId: st.spellId, uid: st.uid, pos: st.pos, radius, hits });
    }
    this.strikes = this.strikes.filter((st) => st.timer > 0);
    // Clean up expired summons.
    this.soldiers = this.soldiers.filter((s) => !(s.summoned && !s.alive));
  }

  // ---------- hero ----------

  moveHero(to: Vec2): boolean {
    const h = this.hero;
    if (!h || !h.alive || !this.isActive()) return false;
    h.dest = { x: Math.max(20, Math.min(1260, to.x)), y: Math.max(80, Math.min(700, to.y)) };
    this.releaseHeroTarget();
    return true;
  }

  heroStat(base: number): number {
    return this.hero ? base * heroLevelMult(this.hero.level) : base;
  }

  /** Fire the hero's active skill. Returns false if not ready. */
  useHeroSkill(): boolean {
    const h = this.hero;
    if (!h || !h.alive || h.skillCd > 0 || !this.isActive()) return false;
    const sk = h.def.active;
    h.skillCd = sk.cooldown;
    const dmg = this.heroStat(sk.damage);
    let pool = this.enemies.filter((e) => e.alive && !e.underground && Math.hypot(e.pos.x - h.pos.x, e.pos.y - h.pos.y) <= sk.radius);
    if (sk.kind === 'quake') pool = pool.filter((e) => !this.airborne(e));
    if (sk.maxTargets) {
      pool.sort((a, b) => b.dist - a.dist);
      pool = pool.slice(0, sk.maxTargets);
    }
    for (const e of pool) {
      if (sk.slow) {
        this.slow(e, sk.slow.factor, sk.slow.duration);
      }
      this.applyDamage(e, computeDamage(dmg, sk.damageType, this.res(e)), sk.damageType);
    }
    let healed: Vec2[] | undefined;
    if (sk.kind === 'rally' && sk.heal) {
      // Sorrel's Second Wind: patch up every soldier (and herself) in reach.
      const amt = this.heroStat(sk.heal);
      healed = [];
      for (const s of this.soldiers) {
        if (!s.alive || Math.hypot(s.pos.x - h.pos.x, s.pos.y - h.pos.y) > sk.radius) continue;
        const before = s.hp;
        s.hp = Math.min(s.maxHp, s.hp + amt);
        this.healTotal += s.hp - before;
        healed.push({ ...s.pos });
      }
      h.hp = Math.min(h.maxHp, h.hp + amt);
      healed.push({ ...h.pos });
    }
    this.events.push({ type: 'heroSkill', hero: h, hits: pool, healed });
    return true;
  }

  private releaseHeroTarget(): void {
    const h = this.hero;
    if (!h || !h.targetUid) return;
    const e = this.enemies.find((en) => en.uid === h.targetUid);
    if (e && e.blockedBy === h.uid) e.blockedBy = 0;
    h.targetUid = 0;
  }

  private grantHeroXp(amount: number): void {
    const h = this.hero;
    if (!h || h.level >= HERO_MAX_LEVEL) return;
    h.xp += amount;
    const lvl = levelForXp(h.xp);
    if (lvl > h.level) {
      const frac = h.hp / h.maxHp;
      h.level = lvl;
      h.maxHp = Math.round(h.def.hp * heroLevelMult(lvl));
      h.hp = Math.max(h.hp, Math.round(h.maxHp * Math.max(frac, 0.5)));
      this.events.push({ type: 'heroLevel', hero: h });
    }
  }

  private heroArmor(): number {
    const h = this.hero!;
    return h.def.armor + (h.def.passive.kind === 'toughness' ? h.def.passive.armor : 0);
  }

  private hurtHero(raw: number): void {
    const h = this.hero;
    if (!h || !h.alive) return;
    h.hp -= computeDamage(raw, 'physical', { armor: this.heroArmor(), magicResist: 0 });
    if (h.hp <= 0) {
      h.hp = 0;
      h.alive = false;
      h.respawnTimer = h.def.respawn;
      h.dest = null;
      this.releaseHeroTarget();
      for (const e of this.enemies) if (e.blockedBy === h.uid) e.blockedBy = 0;
      this.events.push({ type: 'heroDown', hero: h });
    }
  }

  private updateHero(dt: number): void {
    const h = this.hero;
    if (!h) return;
    if (h.skillCd > 0) h.skillCd = Math.max(0, h.skillCd - dt);
    if (!h.alive) {
      h.respawnTimer -= dt;
      if (h.respawnTimer <= 0) {
        h.alive = true;
        h.hp = h.maxHp;
        h.pos = { ...this.heroSpawnPoint() };
        this.events.push({ type: 'heroBack', hero: h });
      }
      return;
    }
    if (h.stun && h.stun > 0) {
      h.stun -= dt;
      return;
    }
    const regen = (h.def.regen + (h.def.passive.kind === 'toughness' ? h.def.passive.regen : 0)) * (this.level.endless?.heroRegen ?? 1);
    if (h.dest) {
      const before = h.pos.x;
      this.moveToward(h.pos, h.dest, h.def.speed * dt, 0);
      if (h.pos.x !== before) h.facing = h.pos.x < before ? -1 : 1;
      if (Math.hypot(h.dest.x - h.pos.x, h.dest.y - h.pos.y) < 1) h.dest = null;
      h.hp = Math.min(h.maxHp, h.hp + regen * dt);
      return;
    }
    const atk = h.def.attack;
    h.attackCd -= dt;
    if (h.def.toss) this.heroToss(h, dt);
    if (h.def.melee) {
      let target = h.targetUid ? this.enemies.find((e) => e.uid === h.targetUid && e.alive) : undefined;
      if (target && Math.hypot(target.pos.x - h.pos.x, target.pos.y - h.pos.y) > 120) {
        this.releaseHeroTarget();
        target = undefined;
      }
      if (!target) {
        let best: Enemy | undefined;
        let bestD = 90;
        for (const e of this.enemies) {
          if (!e.alive || this.airborne(e) || e.underground) continue;
          const d = Math.hypot(e.pos.x - h.pos.x, e.pos.y - h.pos.y) + (e.blockedBy ? 40 : 0);
          if (d < bestD) {
            bestD = d;
            best = e;
          }
        }
        if (best) {
          target = best;
          h.targetUid = best.uid;
          if (!best.blockedBy) best.blockedBy = h.uid;
        }
      }
      if (target && h.def.bulwark) this.bulwarkHold(h, target);
      if (target) {
        const d = Math.hypot(target.pos.x - h.pos.x, target.pos.y - h.pos.y);
        if (d > SOLDIER_REACH) {
          const before = h.pos.x;
          this.moveToward(h.pos, target.pos, h.def.speed * dt, SOLDIER_REACH - 2);
          if (h.pos.x !== before) h.facing = h.pos.x < before ? -1 : 1;
        } else if (h.attackCd <= 0) {
          h.attackCd = 1 / atk.rate;
          h.facing = target.pos.x < h.pos.x ? -1 : 1;
          this.events.push({ type: 'melee', pos: { ...target.pos } });
          const dealt = computeDamage(this.heroHitDamage(), atk.type, this.res(target));
          this.applyDamage(target, dealt, atk.type);
          if (target.def.thorns) {
            this.hurtHero(dealt * target.def.thorns);
            this.events.push({ type: 'thorns', pos: { ...h.pos } });
          }
        }
        return;
      }
    } else if (h.attackCd <= 0) {
      let best: Enemy | null = null;
      for (const e of this.enemies) {
        if (!e.alive || e.underground || (this.airborne(e) && !atk.hitsAir)) continue;
        if (Math.hypot(e.pos.x - h.pos.x, e.pos.y - h.pos.y) > atk.range) continue;
        if (!best || e.dist > best.dist) best = e;
      }
      if (best) {
        h.attackCd = 1 / atk.rate;
        h.facing = best.pos.x < h.pos.x ? -1 : 1;
        const origin = { x: h.pos.x, y: h.pos.y - 20 };
        const p: Projectile = {
          uid: this.nextUid++,
          towerUid: h.uid,
          pos: { ...origin },
          targetUid: best.uid,
          lastTargetPos: { ...best.pos },
          speed: atk.projectileSpeed,
          damage: this.heroHitDamage(),
          damageType: atk.type,
          splash: 0,
          color: h.def.color,
          homing: true,
          hitsAir: atk.hitsAir,
          origin,
          travel: 0,
          kind: `hero_${h.def.id}`,
          pierce: 0,
        };
        this.projectiles.push(p);
        this.events.push({ type: 'heroShoot', hero: h, projectile: p });
        return;
      }
    }
    if (h.hp < h.maxHp) h.hp = Math.min(h.maxHp, h.hp + regen * dt);
  }

  private heroHitDamage(): number {
    const h = this.hero!;
    let dmg = this.heroStat(h.def.attack.damage);
    if (h.def.passive.kind === 'crit' && this.random() < h.def.passive.chance) dmg *= h.def.passive.mult;
    return dmg;
  }

  /**
   * Health multiplier for enemies spawning now. The level's bonus (hpMult - 1) ramps from 60% on the
   * first wave to 100% on the last, so late levels don't open with brutal waves before the player has
   * an economy. Bounties use the same multiplier.
   */
  waveHpMult(): number {
    if (this.level.endless) return (this.level.hpMult ?? 1) * (1 + this.level.endless.hpRamp * Math.max(0, this.waveIndex));
    const bonus = (this.level.hpMult ?? 1) - 1;
    if (bonus <= 0) return 1 + bonus;
    const f = this.totalWaves > 1 ? Math.max(0, this.waveIndex) / (this.totalWaves - 1) : 1;
    return 1 + bonus * (0.6 + 0.4 * f);
  }

  get totalWaves(): number {
    return this.level.waves.length;
  }

  /** True while the current wave is still spawning enemies. */
  get spawning(): boolean {
    return this.schedules.length > 0;
  }

  get wavesRemaining(): boolean {
    return this.waveIndex < this.totalWaves - 1;
  }

  /** Start the next wave now. Calling early awards bonus coins. */
  callNextWave(): boolean {
    if (this.status === 'victory' || this.status === 'defeat') return false;
    if (!this.wavesRemaining) return false;
    const bonus = this.waveIndex >= 0 || this.status === 'running' ? earlyCallBonus(this.waveCountdown, this.waveIndex + 1) : 0;
    this.waveIndex++;
    const income = waveIncome(this.waveIndex);
    this.coins += bonus + income;
    this.schedules.push({ events: buildSchedule(this.level.waves[this.waveIndex]), cursor: 0, t: 0 });
    this.status = 'running';
    this.waveCountdown = WAVE_GAP * this.mods.waveGapMult;
    this.events.push({ type: 'waveStart', index: this.waveIndex, bonus, income });
    return true;
  }

  canBuild(slot: number, towerId: string): boolean {
    const def = TOWERS[towerId];
    return !!def && this.towers[slot] === null && this.coins >= this.price(def.tiers[0].cost) && this.isActive();
  }

  build(slot: number, towerId: string): Tower | null {
    if (!this.canBuild(slot, towerId)) return null;
    const def = TOWERS[towerId];
    this.coins -= this.price(def.tiers[0].cost);
    const pos = { ...this.level.slots[slot] };
    const t: Tower = { uid: this.nextUid++, def, tier: 0, slot, pos, cooldown: 0, target: 'first', rally: null, spec: null, frozen: 0, chillImmune: 0 };
    if (def.tiers[0].soldiers) {
      t.rally = this.rallyPointFor(pos, def.tiers[0].range);
      this.syncSquad(t, true);
    }
    this.towers[slot] = t;
    this.events.push({ type: 'build', tower: t });
    return t;
  }

  /** Price after daily-challenge discounts. */
  price(cost: number): number {
    return Math.round(cost * this.mods.costMult);
  }

  upgradeCost(tower: Tower): number | null {
    if (tower.spec) return null;
    const next = tower.def.tiers[tower.tier + 1];
    return next ? this.price(next.cost) : null;
  }

  stats(t: Tower) {
    return towerStats(t.def, t.tier, t.spec);
  }

  /** Specializations are offered once a tower reaches its top tier. */
  canSpecialize(t: Tower): boolean {
    return !t.spec && t.tier === t.def.tiers.length - 1;
  }

  specialize(slot: number, specIndex: number): boolean {
    const t = this.towers[slot];
    if (!t || !this.isActive() || !this.canSpecialize(t)) return false;
    const sp = t.def.specs[specIndex];
    if (!sp || this.coins < this.price(sp.stats.cost)) return false;
    this.coins -= this.price(sp.stats.cost);
    t.spec = sp.id;
    if (t.rally) this.syncSquad(t, true);
    this.events.push({ type: 'specialize', tower: t });
    return true;
  }

  upgrade(slot: number): boolean {
    const t = this.towers[slot];
    if (!t || !this.isActive()) return false;
    const cost = this.upgradeCost(t);
    if (cost === null || this.coins < cost) return false;
    this.coins -= cost;
    t.tier++;
    if (t.rally) this.syncSquad(t, true);
    this.events.push({ type: 'upgrade', tower: t });
    return true;
  }

  sell(slot: number): boolean {
    const t = this.towers[slot];
    if (!t || !this.isActive()) return false;
    const refund = sellValue(t.def, t.tier, t.spec, this.mods.costMult);
    this.coins += refund;
    this.towers[slot] = null;
    this.removeSquad(t.uid);
    this.events.push({ type: 'sell', tower: t, refund });
    return true;
  }

  setTargetMode(slot: number, mode: TargetMode): void {
    const t = this.towers[slot];
    if (t) t.target = mode;
  }

  /** Closest road point to a tower, used as its soldiers' rally point. */
  rallyPointFor(pos: Vec2, range: number): Vec2 {
    let best: { point: Vec2; distance: number } | null = null;
    for (const path of this.paths) {
      const c = path.closest(pos);
      if (!best || c.distance < best.distance) best = c;
    }
    if (!best || best.distance > range) return { ...pos };
    return { ...best.point };
  }

  /** Move a soldier tower's rally point (clamped to its range). */
  setRally(slot: number, p: Vec2): boolean {
    const t = this.towers[slot];
    if (!t || !t.rally) return false;
    const range = this.stats(t).range;
    if (Math.hypot(p.x - t.pos.x, p.y - t.pos.y) > range) return false;
    t.rally = { ...p };
    for (const s of this.soldiers) {
      if (s.towerUid !== t.uid) continue;
      s.home = this.formation(t.rally, s.index);
      s.anchor = { ...t.rally };
    }
    return true;
  }

  private formation(center: Vec2, i: number): Vec2 {
    const offsets = [
      { x: -14, y: -8 },
      { x: 14, y: -8 },
      { x: 0, y: 12 },
    ];
    const o = offsets[i % offsets.length];
    return { x: center.x + o.x, y: center.y + o.y };
  }

  /** Ensure a soldier tower has the right squad size; optionally fully heal. */
  private syncSquad(t: Tower, heal: boolean): void {
    const stats = this.stats(t).soldiers;
    if (!stats || !t.rally) return;
    const squad = this.soldiers.filter((s) => s.towerUid === t.uid);
    for (let i = squad.length; i < stats.count; i++) {
      const home = this.formation(t.rally, i);
      const s: Soldier = {
        uid: this.nextUid++,
        towerUid: t.uid,
        index: i,
        pos: { x: t.pos.x, y: t.pos.y },
        home,
        hp: stats.hp,
        maxHp: stats.hp,
        alive: true,
        respawnTimer: 0,
        targetUid: 0,
        attackCd: 0,
        stats,
        anchor: { ...t.rally },
        spawnAt: { ...t.pos },
        life: Infinity,
        summoned: false,
      };
      this.soldiers.push(s);
      squad.push(s);
    }
    for (const s of squad) {
      s.stats = stats;
      s.maxHp = stats.hp;
      if (heal && s.alive) s.hp = stats.hp;
    }
  }

  private removeSquad(towerUid: number): void {
    for (const s of this.soldiers) {
      if (s.towerUid !== towerUid) continue;
      this.releaseEnemy(s);
    }
    this.soldiers = this.soldiers.filter((s) => s.towerUid !== towerUid);
  }

  private releaseEnemy(s: Soldier): void {
    if (!s.targetUid) return;
    const e = this.enemies.find((en) => en.uid === s.targetUid);
    if (e && e.blockedBy === s.uid) e.blockedBy = 0;
    s.targetUid = 0;
  }

  isActive(): boolean {
    return this.status === 'prep' || this.status === 'running';
  }

  drainEvents(): SimEvent[] {
    const e = this.events;
    this.events = [];
    return e;
  }

  /** Advance the simulation by dt seconds. Large steps are subdivided for stability. */
  update(dt: number): void {
    if (!this.isActive()) return;
    let remaining = dt;
    while (remaining > 0) {
      const step = Math.min(remaining, 1 / 60);
      this.step(step);
      remaining -= step;
      if (!this.isActive()) break;
    }
  }

  private step(dt: number): void {
    this.time += dt;
    if (this.inkClouds.length) this.inkClouds = this.inkClouds.filter((c) => (c.t -= dt) > 0);

    // Wave countdown (auto-start). It only runs once the current wave has finished spawning,
    // so waves never stack up on a player who is still building.
    if (this.wavesRemaining && this.schedules.length === 0) {
      this.waveCountdown -= dt;
      if (this.waveCountdown <= 0) {
        this.waveCountdown = 0;
        this.callNextWave();
      }
    }

    this.spawnEnemies(dt);
    this.updateSpells(dt);
    this.updateSoldiers(dt);
    this.updateHero(dt);
    this.moveEnemies(dt);
    this.fireTowers(dt);
    this.moveProjectiles(dt);

    this.enemies = this.enemies.filter((e) => e.alive);
    this.checkEnd();
  }

  private spawnEnemies(dt: number): void {
    for (const s of this.schedules) {
      s.t += dt;
      while (s.cursor < s.events.length && s.events[s.cursor].time <= s.t) {
        const ev = s.events[s.cursor++];
        this.spawn(ev.enemy, ev.path);
      }
    }
    this.schedules = this.schedules.filter((s) => s.cursor < s.events.length);
  }

  spawn(enemyId: string, pathIndex = 0, dist = 0): Enemy {
    const def = ENEMIES[enemyId];
    if (!def) throw new Error(`Unknown enemy ${enemyId}`);
    const path = this.paths[Math.min(pathIndex, this.paths.length - 1)];
    const e: Enemy = {
      uid: this.nextUid++,
      def,
      hp: Math.round(def.hp * this.waveHpMult() * this.mods.hpMult),
      maxHp: Math.round(def.hp * this.waveHpMult() * this.mods.hpMult),
      path: pathIndex,
      dist,
      pos: path.pointAt(dist),
      slowFactor: 1,
      slowTime: 0,
      alive: true,
      blockedBy: 0,
      attackCd: 0,
      shield: def.shield ?? 0,
      maxShield: def.shield ?? 0,
      healCd: def.heal ? def.heal.interval : def.shieldAura ? def.shieldAura.interval * 0.5 : 0,
      chillCd: def.chill ? def.chill.interval * 0.6 : 0,
      underground: false,
      burrowCd: def.burrow ? def.burrow.interval : 0,
      spawnCd: def.spawner ? def.spawner.interval : 0,
      spawned: 0,
      phase: 0,
      speedMult: 1,
      enraged: false,
      hasteTime: 0,
      hasteMult: 1,
      armor: def.armor,
      landed: false,
      swoopCd: def.swoop ? def.swoop.interval : 0,
      gustCd: def.gust ? def.gust.interval : 0,
      growT: 0,
      fed: 0,
      shockCd: def.shock ? def.shock.interval : 0,
      boltCd: def.bolt ? def.bolt.interval * 0.6 : 0,
      molted: false,
      inkCd: 0,
      rangedCd: def.ranged ? def.ranged.interval * 0.5 : 0,
      anchorCd: def.anchor ? def.anchor.interval : 0,
      anchored: false,
      drumCd: def.drum ? def.drum.interval * 0.5 : 0,
      phaseCd: def.phase ? def.phase.interval : 0,
      riledAt: -99,
      snatchCd: def.snatch ? def.snatch.cooldown * 0.5 : 0,
      phased: false,
      cleanseCd: def.cleanse ? def.cleanse.interval : 0,
      blinkCd: def.blink ? def.blink.interval : 0,
      mirrored: false,
      chargeTime: 0,
      chargeCd: 0,
      mr: def.magicResist,
      shifted: false,
      shiftCd: def.shift ? def.shift.interval : 0,
      reviveCd: def.revive ? def.revive.interval : 0,
      revived: false,
      sinceHit: 0,
    };
    this.enemies.push(e);
    this.events.push({ type: 'spawn', enemy: e });
    return e;
  }

  private moveEnemies(dt: number): void {
    for (const e of this.enemies) {
      if (!e.alive) continue;
      if (e.slowTime > 0) {
        e.slowTime -= dt;
        if (e.slowTime <= 0) e.slowFactor = 1;
      }
      if (e.hasteTime > 0) {
        e.hasteTime -= dt;
        if (e.hasteTime <= 0) e.hasteMult = 1;
      }
      e.sinceHit += dt;
      if (e.chargeTime > 0) e.chargeTime -= dt;
      if (e.chargeCd > 0) e.chargeCd -= dt;
      if (this.regenerating(e)) e.hp = Math.min(e.maxHp, e.hp + e.maxHp * e.def.regen!.perSec * dt);
      if (e.def.heal) this.tickHealer(e, dt);
      if (e.def.chill) this.tickChill(e, dt);
      if (e.def.burrow) this.tickBurrow(e, dt);
      if (e.def.spawner) this.tickSpawner(e, dt);
      if (e.def.swoop) this.tickSwoop(e, dt);
      if (e.def.gust) this.tickGust(e, dt);
      if (e.def.grow) {
        e.growT += dt;
        if (e.growT >= e.def.grow.after) {
          // Rotseed sprouts: it is replaced where it stood, and pays nothing.
          e.alive = false;
          const g = this.spawn(e.def.grow.into, e.path, e.dist);
          this.events.push({ type: 'grow', enemy: g });
          continue;
        }
      }
      if (e.def.shock) this.tickShock(e, dt);
      if (e.def.bolt) this.tickBolt(e, dt);
      if (e.def.cleanse) this.tickCleanse(e, dt);
      if (e.def.ranged) this.tickRanged(e, dt);
      if (e.def.anchor) this.tickAnchor(e, dt);
      if (e.def.drum) this.tickDrum(e, dt);
      if (e.def.phase) this.tickPhase(e, dt);
      if (e.def.snatch) this.tickSnatch(e, dt);
      if (e.def.crust && e.sinceHit > 0.4) e.armor = Math.min(e.def.armor + e.def.crust.max, e.armor + e.def.crust.perSec * dt);
      if (e.def.blink) this.tickBlink(e, dt);
      if (e.def.shift) this.tickShift(e, dt);
      if (e.def.revive) this.tickRevive(e, dt);
      if (e.def.shieldAura) this.tickShieldAura(e, dt);
      if (e.def.enrage && !e.enraged && e.hp < e.maxHp * e.def.enrage.below) {
        e.enraged = true;
        e.speedMult = Math.max(e.speedMult, e.def.enrage.speedMult);
        this.events.push({ type: 'enrage', enemy: e });
      }
      if (e.blockedBy) {
        const isHero = !!this.hero && this.hero.uid === e.blockedBy;
        const s = isHero ? null : this.soldiers.find((so) => so.uid === e.blockedBy);
        const blocker = isHero ? this.hero : s;
        if (!blocker || !blocker.alive) {
          e.blockedBy = 0;
        } else if (Math.hypot(blocker.pos.x - e.pos.x, blocker.pos.y - e.pos.y) <= SOLDIER_REACH + 4) {
          // Held in place: brawl with the blocker.
          e.attackCd -= dt;
          if (e.attackCd <= 0) {
            e.attackCd = 1 / e.def.attackRate;
            const hit = e.def.attack * this.attackMult();
            if (isHero) this.hurtHero(hit);
            else this.hurtSoldier(s!, hit);
            if (e.def.lifesteal && e.hp < e.maxHp) {
              // Sapstoat: every bite feeds it.
              const healed = Math.min(e.maxHp - e.hp, hit * e.def.lifesteal);
              e.hp += healed;
              this.events.push({ type: 'leech', enemy: e, amount: healed });
            }
          }
          continue;
        }
      }
      if (e.anchored) continue; // Ironkeel holds fast while its anchor is down
      e.dist += e.def.speed * e.slowFactor * e.speedMult * e.hasteMult * this.chargeMult(e) * this.herdMult(e) * this.drowseMult(e) * this.mods.speedMult * dt;
      const path = this.paths[e.path];
      e.pos = path.pointAt(e.dist);
      if (e.dist >= path.length) {
        e.alive = false;
        this.lives = Math.max(0, this.lives - e.def.livesCost);
        this.events.push({ type: 'leak', enemy: e, lives: e.def.livesCost });
        if (e.def.pilfer) {
          // Sandpicker: makes off with a sack of the player's coins.
          const stolen = Math.min(this.coins, Math.round(e.def.pilfer * this.waveHpMult()));
          this.coins -= stolen;
          this.events.push({ type: 'pilfer', enemy: e, coins: stolen });
        }
      }
    }
  }

  /** Spawners release minions behind themselves on a timer (even while blocked). */
  private tickSpawner(e: Enemy, dt: number): void {
    const sp = e.def.spawner!;
    e.spawnCd -= dt;
    if (e.spawnCd > 0) return;
    e.spawnCd = sp.interval;
    for (let i = 0; i < sp.count && e.spawned < sp.limit; i++, e.spawned++) this.spawn(sp.enemy, e.path, Math.max(0, e.dist - 12 - i * 10));
  }

  /** Flyers with `swoop` drop to the ground for a while (ground towers and soldiers can reach them), then take off. */
  private tickSwoop(e: Enemy, dt: number): void {
    const sw = e.def.swoop!;
    e.swoopCd -= dt;
    if (e.swoopCd > 0) return;
    e.landed = !e.landed;
    e.swoopCd = e.landed ? sw.duration : sw.interval;
    if (!e.landed && e.blockedBy) {
      for (const s of this.soldiers) if (s.targetUid === e.uid) s.targetUid = 0;
      if (this.hero && this.hero.targetUid === e.uid) this.hero.targetUid = 0;
      e.blockedBy = 0;
    }
    this.events.push({ type: 'swoop', enemy: e, landed: e.landed });
  }

  /** Reefwardens coat nearby allies (not themselves, not bosses) in a coral shield on a timer. Reuses healCd. */
  private tickShieldAura(e: Enemy, dt: number): void {
    const sa = e.def.shieldAura!;
    e.healCd -= dt;
    if (e.healCd > 0) return;
    e.healCd = sa.interval;
    const amount = Math.round(sa.amount * this.waveHpMult());
    const targets: Enemy[] = [];
    for (const o of this.enemies) {
      if (!o.alive || o === e || o.def.boss || o.underground) continue;
      if (Math.hypot(o.pos.x - e.pos.x, o.pos.y - e.pos.y) > sa.radius) continue;
      if (o.shield >= amount) continue;
      o.shield = amount;
      o.maxShield = Math.max(o.maxShield, amount);
      targets.push(o);
    }
    this.events.push({ type: 'coral', source: e, targets, radius: sa.radius });
  }

  /** Shardskippers jump ahead along their road on a timer, slipping out of any soldier's grip. */
  private tickBlink(e: Enemy, dt: number): void {
    const bl = e.def.blink!;
    e.blinkCd -= dt;
    if (e.blinkCd > 0) return;
    e.blinkCd = bl.interval;
    const path = this.paths[e.path];
    const from = { ...e.pos };
    e.dist = Math.min(path.length - 1, e.dist + bl.distance);
    e.pos = path.pointAt(e.dist);
    if (e.blockedBy) {
      for (const s of this.soldiers) if (s.targetUid === e.uid) s.targetUid = 0;
      if (this.hero && this.hero.targetUid === e.uid) this.hero.targetUid = 0;
      e.blockedBy = 0;
    }
    this.events.push({ type: 'blink', enemy: e, from, to: { ...e.pos } });
  }

  /** Sparkeel: a shock that stuns nearby soldiers and the hero, so they drop whatever they were holding. */
  /** Deckgunner: pops off a shot at the nearest soldier or hero in range (not while brawling). */
  private tickRanged(e: Enemy, dt: number): void {
    const r = e.def.ranged!;
    e.rangedCd -= dt;
    if (e.rangedCd > 0 || e.blockedBy) return;
    let best: { pos: Vec2; hit: () => void } | null = null;
    let bestD = r.range;
    const dmg = r.damage * this.attackMult();
    for (const s of this.soldiers) {
      if (!s.alive) continue;
      const d = Math.hypot(s.pos.x - e.pos.x, s.pos.y - e.pos.y);
      if (d <= bestD) {
        bestD = d;
        best = { pos: s.pos, hit: () => this.hurtSoldier(s, dmg) };
      }
    }
    const h = this.hero;
    if (h && h.alive) {
      const d = Math.hypot(h.pos.x - e.pos.x, h.pos.y - e.pos.y);
      if (d <= bestD) best = { pos: h.pos, hit: () => this.hurtHero(dmg) };
    }
    if (!best) {
      e.rangedCd = 0.3;
      return;
    }
    e.rangedCd = r.interval;
    this.events.push({ type: 'enemyShot', enemy: e, to: { ...best.pos } });
    best.hit();
  }

  /** Ironkeel: drops anchor (stops, armors up), then hauls it up and sails on. */
  private tickAnchor(e: Enemy, dt: number): void {
    const a = e.def.anchor!;
    e.anchorCd -= dt;
    if (e.anchorCd > 0) return;
    e.anchored = !e.anchored;
    e.anchorCd = e.anchored ? a.duration : a.interval;
    e.armor = e.anchored ? Math.min(0.85, e.def.armor + a.armor) : e.def.armor;
    this.events.push({ type: 'anchor', enemy: e, down: e.anchored });
  }

  /** Barkdrum: a beat on the war-drum hastens itself and nearby allies (not bosses) for a moment. */
  private tickDrum(e: Enemy, dt: number): void {
    const d = e.def.drum!;
    e.drumCd -= dt;
    if (e.drumCd > 0) return;
    e.drumCd = d.interval;
    const hasted: Enemy[] = [];
    for (const o of this.enemies) {
      if (!o.alive || (o.def.boss && o !== e)) continue;
      if (Math.hypot(o.pos.x - e.pos.x, o.pos.y - e.pos.y) > d.radius) continue;
      o.hasteMult = Math.max(o.hasteMult, d.speedMult);
      o.hasteTime = Math.max(o.hasteTime, d.duration);
      hasted.push(o);
    }
    this.events.push({ type: 'drum', enemy: e, radius: d.radius, hasted });
  }

  /** Hazel's lullaby: enemies near a living drowse hero walk slower (windborne ones ignore it). */
  drowseMult(e: Enemy): number {
    const h = this.hero;
    if (!h || !h.alive || h.def.passive.kind !== 'drowse' || e.def.windborne) return 1;
    return Math.hypot(e.pos.x - h.pos.x, e.pos.y - h.pos.y) <= h.def.passive.radius ? 1 - h.def.passive.slow : 1;
  }

  /** Glowbearer: the strongest ward in range (from another enemy) cuts damage taken by this fraction. */
  wardCut(e: Enemy): number {
    let cut = 0;
    for (const o of this.enemies) {
      const w = o.def.ward;
      if (!w || o === e || !o.alive) continue;
      if (Math.hypot(o.pos.x - e.pos.x, o.pos.y - e.pos.y) <= w.radius) cut = Math.max(cut, w.cut);
    }
    return cut;
  }

  /** Canopy Harrier: dives on the nearest soldier in reach and carries it off (it has to respawn). */
  private tickSnatch(e: Enemy, dt: number): void {
    const sn = e.def.snatch!;
    e.snatchCd -= dt;
    if (e.snatchCd > 0) return;
    let best: Soldier | null = null;
    let bestD = sn.radius;
    for (const s of this.soldiers) {
      if (!s.alive) continue;
      const d = Math.hypot(s.pos.x - e.pos.x, s.pos.y - e.pos.y);
      if (d <= bestD) {
        bestD = d;
        best = s;
      }
    }
    if (!best) {
      e.snatchCd = 0.3;
      return;
    }
    e.snatchCd = sn.cooldown;
    this.events.push({ type: 'snatch', enemy: e, pos: { ...best.pos } });
    this.hurtSoldier(best, 1e9);
  }

  /** Mistfox: fades into mist (untouchable) for a moment, then solidifies again, on a cycle. */
  private tickPhase(e: Enemy, dt: number): void {
    const ph = e.def.phase!;
    e.phaseCd -= dt;
    if (e.phaseCd > 0) return;
    e.phased = !e.phased;
    e.phaseCd = e.phased ? ph.duration : ph.interval;
    this.events.push({ type: 'mist', enemy: e, on: e.phased });
  }

  /** Inside an ink cloud? (Grounded enemies only: flyers are above the murk.) */
  inked(e: Enemy): boolean {
    if (!this.inkClouds.length || this.airborne(e)) return false;
    return this.inkClouds.some((c) => Math.hypot(c.pos.x - e.pos.x, c.pos.y - e.pos.y) <= c.radius);
  }

  /** Tidecaller: a wash of seawater rinses slows off it and its neighbours. */
  private tickCleanse(e: Enemy, dt: number): void {
    const c = e.def.cleanse!;
    e.cleanseCd -= dt;
    if (e.cleanseCd > 0) return;
    e.cleanseCd = c.interval;
    const washed: Enemy[] = [];
    for (const o of this.enemies) {
      if (!o.alive || o.slowTime <= 0 || Math.hypot(o.pos.x - e.pos.x, o.pos.y - e.pos.y) > c.radius) continue;
      o.slowTime = 0;
      o.slowFactor = 1;
      washed.push(o);
    }
    if (washed.length) this.events.push({ type: 'cleanse', source: e, washed, radius: c.radius });
  }

  /** Stormcaller: lightning stuns the nearest shooting tower in range (shares the chill immunity window). */
  private tickBolt(e: Enemy, dt: number): void {
    const b = e.def.bolt!;
    e.boltCd -= dt;
    if (e.boltCd > 0) return;
    let best: Tower | null = null;
    let bestD = b.range;
    for (const t of this.towers) {
      if (!t || t.rally || t.chillImmune > 0) continue;
      const d = Math.hypot(t.pos.x - e.pos.x, t.pos.y - e.pos.y);
      if (d <= bestD) {
        bestD = d;
        best = t;
      }
    }
    if (!best) {
      e.boltCd = 0.5; // nothing to strike yet: look again soon
      return;
    }
    e.boltCd = b.interval;
    best.frozen = Math.max(best.frozen, b.duration);
    best.chillImmune = b.duration + THAW_IMMUNITY;
    this.events.push({ type: 'bolt', source: e, tower: best });
  }

  /** Thunderhooves stampede: faster for each other herd-mate close by. */
  herdMult(e: Enemy): number {
    const h = e.def.herd;
    if (!h) return 1;
    let n = 0;
    for (const o of this.enemies) {
      if (o === e || !o.alive || !o.def.herd) continue;
      if (Math.abs(o.dist - e.dist) > h.radius || o.path !== e.path) continue;
      n++;
    }
    return 1 + Math.min(h.max, n * h.perAlly);
  }

  private tickShock(e: Enemy, dt: number): void {
    const sh = e.def.shock!;
    e.shockCd -= dt;
    if (e.shockCd > 0) return;
    e.shockCd = sh.interval;
    const hits: Vec2[] = [];
    for (const s of this.soldiers) {
      if (!s.alive || Math.hypot(s.pos.x - e.pos.x, s.pos.y - e.pos.y) > sh.radius) continue;
      s.stun = sh.duration;
      this.releaseEnemy(s);
      for (const o of this.enemies) if (o.blockedBy === s.uid) o.blockedBy = 0;
      hits.push({ ...s.pos });
    }
    const h = this.hero;
    if (h && h.alive && Math.hypot(h.pos.x - e.pos.x, h.pos.y - e.pos.y) <= sh.radius) {
      h.stun = sh.duration;
      this.releaseHeroTarget();
      for (const o of this.enemies) if (o.blockedBy === h.uid) o.blockedBy = 0;
      hits.push({ ...h.pos });
    }
    this.events.push({ type: 'shock', source: e, radius: sh.radius, hits });
  }

  /** Kitewing: a gust shoves nearby free walkers further along their road. Held enemies and bosses don't budge. */
  private tickGust(e: Enemy, dt: number): void {
    const gu = e.def.gust!;
    e.gustCd -= dt;
    if (e.gustCd > 0) return;
    e.gustCd = gu.interval;
    const targets: { enemy: Enemy; from: Vec2 }[] = [];
    for (const o of this.enemies) {
      if (o === e || !o.alive || o.underground || o.blockedBy || o.def.boss || this.airborne(o)) continue;
      if (Math.hypot(o.pos.x - e.pos.x, o.pos.y - e.pos.y) > gu.radius) continue;
      const path = this.paths[o.path];
      const from = { ...o.pos };
      o.dist = Math.min(path.length - 1, o.dist + gu.distance);
      o.pos = path.pointAt(o.dist);
      targets.push({ enemy: o, from });
    }
    this.events.push({ type: 'gust', source: e, targets, radius: gu.radius });
  }

  /** Shiftscale: swaps between its scaled form (def armor/MR) and its slick form (shift armor/MR) on a timer. */
  private tickShift(e: Enemy, dt: number): void {
    const sh = e.def.shift!;
    e.shiftCd -= dt;
    if (e.shiftCd > 0) return;
    e.shiftCd = sh.interval;
    e.shifted = !e.shifted;
    e.armor = e.shifted ? sh.armor : e.def.armor;
    e.mr = e.shifted ? sh.magicResist : e.def.magicResist;
    this.events.push({ type: 'shift', enemy: e, scales: !e.shifted });
  }

  /** Idol Keeper: raises the most recent fallen ally nearby at partial health. */
  private tickRevive(e: Enemy, dt: number): void {
    const rv = e.def.revive!;
    this.fallen = this.fallen.filter((f) => this.time - f.at <= rv.window);
    e.reviveCd -= dt;
    if (e.reviveCd > 0) return;
    let best = -1;
    for (let i = this.fallen.length - 1; i >= 0; i--) {
      const f = this.fallen[i];
      if (Math.hypot(f.pos.x - e.pos.x, f.pos.y - e.pos.y) <= rv.radius) { best = i; break; }
    }
    if (best < 0) {
      e.reviveCd = 0.5; // nothing to raise yet: look again soon
      return;
    }
    e.reviveCd = rv.interval;
    const f = this.fallen.splice(best, 1)[0];
    const r = this.spawn(f.id, f.path, f.dist);
    r.hp = Math.round(r.maxHp * rv.hpFrac);
    r.revived = true;
    this.events.push({ type: 'revive', source: e, enemy: r });
  }

  /** Endless: enemy melee hits ramp with the wave too (otherwise a blocker can stall forever). 1 in the campaign. */
  attackMult(): number {
    const en = this.level.endless;
    return en ? 1 + (en.attackRamp ?? 0) * Math.max(0, this.waveIndex) : 1;
  }

  /** How many enemies a melee hero can hold at once at their current level (Bramble's Bulwark). */
  heroHolds(h: Hero): number {
    let n = 1;
    for (const b of h.def.bulwark ?? []) if (h.level >= b.level) n = Math.max(n, b.holds);
    return n;
  }

  /** Bulwark: while brawling, also pin extra free ground enemies within reach, up to the hero's hold count. */
  private bulwarkHold(h: Hero, target: Enemy): void {
    const max = this.heroHolds(h);
    if (max <= 1) return;
    let held = this.enemies.filter((e) => e.alive && e.blockedBy === h.uid).length;
    for (const e of this.enemies) {
      if (held >= max) break;
      if (e === target || !e.alive || e.blockedBy || e.underground || this.airborne(e)) continue;
      if (Math.hypot(e.pos.x - h.pos.x, e.pos.y - h.pos.y) > SOLDIER_REACH + 6) continue;
      e.blockedBy = h.uid;
      held++;
    }
  }

  /** Bramble's Shield Toss: a ranged throw at the nearest flyer, on its own timer (works while he brawls). */
  private heroToss(h: Hero, dt: number): void {
    const t = h.def.toss!;
    h.tossCd -= dt;
    if (h.tossCd > 0) return;
    let best: Enemy | null = null;
    let bestD = t.range;
    for (const e of this.enemies) {
      if (!e.alive || !this.airborne(e)) continue;
      const d = Math.hypot(e.pos.x - h.pos.x, e.pos.y - h.pos.y);
      if (d <= bestD) {
        bestD = d;
        best = e;
      }
    }
    if (!best) return;
    h.tossCd = t.interval;
    const origin = { x: h.pos.x, y: h.pos.y - 20 };
    const p: Projectile = {
      uid: this.nextUid++,
      towerUid: h.uid,
      pos: { ...origin },
      targetUid: best.uid,
      lastTargetPos: { ...best.pos },
      speed: 520,
      damage: t.damage * heroLevelMult(h.level),
      damageType: 'physical',
      splash: 0,
      color: C_SHIELD,
      homing: true,
      hitsAir: true,
      origin,
      travel: 0,
      kind: 'hero_toss',
      pierce: 0,
    };
    this.projectiles.push(p);
    this.events.push({ type: 'heroShoot', hero: h, projectile: p });
  }

  /** Wren's Scholar's Eye: enemies that fall near her pay extra coins. */
  bountyMult(e: Enemy): number {
    const h = this.hero;
    const daily = this.mods.bountyMult;
    if (!h || !h.alive || h.def.passive.kind !== 'bounty') return daily;
    return daily * (Math.hypot(e.pos.x - h.pos.x, e.pos.y - h.pos.y) <= h.def.passive.radius ? 1 + h.def.passive.bonus : 1);
  }

  /** In the air right now (flyers, except while a swooper is landed). */
  airborne(e: Enemy): boolean {
    return !!e.def.flying && !e.landed;
  }

  /** Damage resistances, using the enemy's current armor. */
  res(e: Enemy): { armor: number; magicResist: number } {
    return { armor: Math.min(0.85, e.armor + this.fortifyBonus(e) + this.mods.armorBonus), magicResist: e.mr };
  }

  /** Barkwardens toughen nearby allies' bark: the strongest aura in range adds armor (they don't stack). */
  fortifyBonus(e: Enemy): number {
    let b = 0;
    for (const o of this.enemies) {
      const f = o.def.fortify;
      if (!f || o === e || !o.alive) continue;
      if (Math.hypot(o.pos.x - e.pos.x, o.pos.y - e.pos.y) <= f.radius) b = Math.max(b, f.bonus);
    }
    return b;
  }

  /** Burrowers dive underground (untargetable, unblockable, faster) and resurface on a cycle. */
  private tickBurrow(e: Enemy, dt: number): void {
    const b = e.def.burrow!;
    e.burrowCd -= dt;
    if (e.burrowCd > 0) return;
    e.underground = !e.underground;
    e.burrowCd = e.underground ? b.duration : b.interval;
    e.speedMult = e.underground ? Math.max(e.speedMult, b.speedMult) : e.def.phases ? e.speedMult : 1;
    if (e.underground && e.blockedBy) {
      for (const s of this.soldiers) if (s.targetUid === e.uid) s.targetUid = 0;
      if (this.hero && this.hero.targetUid === e.uid) this.hero.targetUid = 0;
      e.blockedBy = 0;
    }
    this.events.push({ type: 'burrow', enemy: e, down: e.underground });
  }

  private tickChill(e: Enemy, dt: number): void {
    const c = e.def.chill!;
    e.chillCd -= dt;
    if (e.chillCd > 0) return;
    e.chillCd = c.interval;
    const hit: Tower[] = [];
    for (const t of this.towers) {
      if (!t || t.rally) continue; // soldier dens keep working
      if (Math.hypot(t.pos.x - e.pos.x, t.pos.y - e.pos.y) > c.radius) continue;
      if (t.chillImmune > 0) continue;
      t.frozen = c.duration;
      t.chillImmune = c.duration + THAW_IMMUNITY;
      hit.push(t);
    }
    this.events.push({ type: 'chill', source: e, towers: hit, radius: c.radius });
  }

  private tickHealer(e: Enemy, dt: number): void {
    const heal = e.def.heal!;
    e.healCd -= dt;
    if (e.healCd > 0) return;
    e.healCd = heal.interval;
    const targets: Enemy[] = [];
    for (const o of this.enemies) {
      if (!o.alive || o.hp >= o.maxHp) continue;
      if (Math.hypot(o.pos.x - e.pos.x, o.pos.y - e.pos.y) > heal.radius) continue;
      o.hp = Math.min(o.maxHp, o.hp + heal.amount);
      targets.push(o);
    }
    this.events.push({ type: 'heal', source: e, targets, radius: heal.radius });
  }

  private updateSoldiers(dt: number): void {
    const byUid = new Map(this.enemies.map((e) => [e.uid, e]));
    const h = this.hero;
    const mend = h && h.alive && h.def.passive.kind === 'mend' ? h.def.passive : null;
    for (const s of this.soldiers) {
      const stats = s.stats;
      // Sorrel's Field Dressing: soldiers near her heal even mid-fight.
      if (mend && s.alive && s.hp < s.maxHp && Math.hypot(s.pos.x - h!.pos.x, s.pos.y - h!.pos.y) <= mend.radius) {
        const before = s.hp;
        s.hp = Math.min(s.maxHp, s.hp + mend.regen * dt);
        this.healTotal += s.hp - before;
      }
      if (s.summoned) {
        s.life -= dt;
        if (s.life <= 0 && s.alive) {
          s.alive = false;
          this.releaseEnemy(s);
          for (const e of this.enemies) if (e.blockedBy === s.uid) e.blockedBy = 0;
          this.events.push({ type: 'summonGone', soldier: s });
        }
      }
      if (!s.alive) {
        if (s.summoned) continue;
        s.respawnTimer -= dt;
        if (s.respawnTimer <= 0) {
          s.alive = true;
          s.hp = stats.hp;
          s.pos = { ...s.spawnAt };
        }
        continue;
      }
      if (s.stun && s.stun > 0) {
        s.stun -= dt;
        continue;
      }
      // Validate current target.
      let target = s.targetUid ? byUid.get(s.targetUid) : undefined;
      if (target && (!target.alive || Math.hypot(target.pos.x - s.anchor.x, target.pos.y - s.anchor.y) > ENGAGE_RADIUS * 1.5)) {
        this.releaseEnemy(s);
        target = undefined;
      }
      if (!target) {
        target = this.findSoldierTarget(s, s.anchor);
        if (target) {
          s.targetUid = target.uid;
          if (!target.blockedBy) target.blockedBy = s.uid;
        }
      }
      if (target) {
        const d = Math.hypot(target.pos.x - s.pos.x, target.pos.y - s.pos.y);
        if (d > SOLDIER_REACH) {
          this.moveToward(s.pos, target.pos, SOLDIER_SPEED * dt, SOLDIER_REACH - 2);
        } else {
          s.attackCd -= dt;
          if (s.attackCd <= 0) {
            s.attackCd = 1 / stats.attackRate;
            this.events.push({ type: 'melee', pos: { ...target.pos } });
            const dealt = computeDamage(stats.damage, 'physical', this.res(target));
            this.applyDamage(target, dealt, 'physical');
            if (target.def.thorns) {
              this.hurtSoldier(s, dealt * target.def.thorns);
              this.events.push({ type: 'thorns', pos: { ...s.pos } });
            }
          }
        }
      } else {
        this.moveToward(s.pos, s.home, SOLDIER_SPEED * dt, 0);
        if (s.hp < s.maxHp) s.hp = Math.min(s.maxHp, s.hp + stats.regen * dt);
      }
    }
  }

  private findSoldierTarget(s: Soldier, rally: Vec2): Enemy | undefined {
    let best: Enemy | undefined;
    let bestScore = -Infinity;
    for (const e of this.enemies) {
      if (!e.alive || this.airborne(e) || e.underground) continue;
      const d = Math.hypot(e.pos.x - rally.x, e.pos.y - rally.y);
      if (d > ENGAGE_RADIUS) continue;
      // Prefer free enemies, then the one furthest along.
      const score = (e.blockedBy ? 0 : 100000) + e.dist - Math.hypot(e.pos.x - s.pos.x, e.pos.y - s.pos.y) * 0.1;
      if (score > bestScore) {
        bestScore = score;
        best = e;
      }
    }
    return best;
  }

  private moveToward(pos: Vec2, to: Vec2, step: number, stopAt: number): void {
    const dx = to.x - pos.x;
    const dy = to.y - pos.y;
    const d = Math.hypot(dx, dy);
    if (d <= stopAt || d === 0) return;
    const m = Math.min(step, d - stopAt);
    pos.x += (dx / d) * m;
    pos.y += (dy / d) * m;
  }

  private hurtSoldier(s: Soldier, raw: number): void {
    s.hp -= computeDamage(raw, 'physical', { armor: s.stats.armor, magicResist: 0 });
    if (s.hp <= 0) {
      s.alive = false;
      s.hp = 0;
      s.respawnTimer = s.stats.respawn;
      this.releaseEnemy(s);
      for (const e of this.enemies) if (e.blockedBy === s.uid) e.blockedBy = 0;
      this.events.push({ type: 'soldierDown', soldier: s });
    }
  }

  private pickTarget(t: Tower, range: number): Enemy | null {
    let best: Enemy | null = null;
    let bestScore = -Infinity;
    for (const e of this.enemies) {
      if (!e.alive || e.underground || this.inked(e)) continue;
      if (this.airborne(e) && !t.def.hitsAir) continue;
      const d = Math.hypot(e.pos.x - t.pos.x, e.pos.y - t.pos.y);
      if (d > range || (e.def.veil && d > e.def.veil)) continue;
      let score: number;
      switch (t.target) {
        case 'first':
          score = e.dist;
          break;
        case 'last':
          score = -e.dist;
          break;
        case 'strongest':
          score = e.hp * 1000 + e.dist;
          break;
        case 'closest':
          score = -d;
          break;
      }
      if (score > bestScore) {
        bestScore = score;
        best = e;
      }
    }
    return best;
  }

  private pickTargets(t: Tower, range: number, n: number): Enemy[] {
    if (n <= 1) {
      const one = this.pickTarget(t, range);
      return one ? [one] : [];
    }
    const picked: Enemy[] = [];
    const taken = new Set<number>();
    for (let k = 0; k < n; k++) {
      let best: Enemy | null = null;
      let bestScore = -Infinity;
      for (const e of this.enemies) {
        if (!e.alive || e.underground || taken.has(e.uid) || this.inked(e) || (this.airborne(e) && !t.def.hitsAir)) continue;
        const d = Math.hypot(e.pos.x - t.pos.x, e.pos.y - t.pos.y);
        if (d > range || (e.def.veil && d > e.def.veil)) continue;
        if (e.dist > bestScore) {
          bestScore = e.dist;
          best = e;
        }
      }
      if (!best) break;
      taken.add(best.uid);
      picked.push(best);
    }
    // Keep the player's targeting mode for the primary shot.
    const primary = this.pickTarget(t, range);
    if (primary && !taken.has(primary.uid) && picked.length) picked[0] = primary;
    return picked;
  }

  private fireTowers(dt: number): void {
    for (const t of this.towers) {
      if (!t) continue;
      if (t.chillImmune > 0) t.chillImmune = Math.max(0, t.chillImmune - dt);
      if (t.frozen > 0) {
        t.frozen = Math.max(0, t.frozen - dt);
        continue;
      }
      t.cooldown -= dt;
      if (t.cooldown > 0) continue;
      const stats = this.stats(t);
      if (stats.soldiers || stats.fireRate <= 0) continue;
      const targets = this.pickTargets(t, stats.range * this.towerDim(t), stats.multishot ?? 1);
      if (!targets.length) {
        t.cooldown = 0;
        continue;
      }
      t.cooldown = 1 / (stats.fireRate * this.towerHaste(t) * this.towerJam(t));
      for (const target of targets) {
        const origin = { x: t.pos.x, y: t.pos.y - 18 };
        let aim = { ...target.pos };
        if (stats.lob) {
          // Lead the target: predict where it will be when the rock lands.
          const flight = Math.hypot(aim.x - origin.x, aim.y - origin.y) / stats.projectileSpeed;
          const moving = target.blockedBy ? 0 : target.def.speed * target.slowFactor * target.speedMult * target.hasteMult * this.chargeMult(target) * this.herdMult(target) * this.drowseMult(target) * this.mods.speedMult;
          aim = this.paths[target.path].pointAt(target.dist + moving * flight);
        }
        const p: Projectile = {
          uid: this.nextUid++,
          towerUid: t.uid,
          pos: { ...origin },
          targetUid: target.uid,
          lastTargetPos: aim,
          speed: stats.projectileSpeed,
          damage: stats.damage * this.towerDamageMult,
          damageType: t.def.damageType,
          splash: stats.splash ?? 0,
          slow: stats.slow,
          color: t.spec ? t.def.specs.find((x) => x.id === t.spec)!.color : t.def.color,
          homing: !stats.lob,
          hitsAir: t.def.hitsAir,
          origin,
          travel: Math.hypot(aim.x - origin.x, aim.y - origin.y),
          kind: t.def.id,
          pierce: stats.armorPierce ?? 0,
          chain: stats.chain,
        };
        this.projectiles.push(p);
        this.events.push({ type: 'shoot', tower: t, projectile: p });
      }
    }
  }

  /** Fire-rate multiplier from hero auras. */
  /** Cogjammers rattle nearby towers: the strongest jammer in range slows the tower's fire rate (they don't stack). */
  towerJam(t: Tower): number {
    let f = 1;
    for (const e of this.enemies) {
      const j = e.def.jam;
      if (!j || !e.alive || e.underground) continue;
      if (Math.hypot(t.pos.x - e.pos.x, t.pos.y - e.pos.y) <= j.radius) f = Math.min(f, 1 - j.slow);
    }
    return f;
  }

  /** Dimlanterns cast gloom: the strongest one in range shrinks a shooting tower's reach (they don't stack). */
  towerDim(t: Tower): number {
    let f = 1;
    for (const e of this.enemies) {
      const d = e.def.dim;
      if (!d || !e.alive || e.underground) continue;
      if (Math.hypot(t.pos.x - e.pos.x, t.pos.y - e.pos.y) <= d.radius) f = Math.min(f, 1 - d.cut);
    }
    return f;
  }

  /** Steamrunners bolt for a moment after being hit. */
  chargeMult(e: Enemy): number {
    return e.chargeTime > 0 && e.def.charge ? e.def.charge.speedMult : 1;
  }

  towerHaste(t: Tower): number {
    const h = this.hero;
    if (!h || !h.alive || h.def.passive.kind !== 'towerHaste') return 1;
    return Math.hypot(t.pos.x - h.pos.x, t.pos.y - h.pos.y) <= h.def.passive.radius ? 1 + h.def.passive.bonus : 1;
  }

  private moveProjectiles(dt: number): void {
    const byUid = new Map(this.enemies.map((e) => [e.uid, e]));
    const keep: Projectile[] = [];
    for (const p of this.projectiles) {
      const target = byUid.get(p.targetUid);
      const reachable = target && target.alive && !target.underground;
      if (p.homing && reachable) p.lastTargetPos = { ...target.pos };
      const dx = p.lastTargetPos.x - p.pos.x;
      const dy = p.lastTargetPos.y - p.pos.y;
      const d = Math.hypot(dx, dy);
      const move = p.speed * dt;
      if (d <= move + 4) {
        this.impact(p, p.homing && reachable ? target : null);
      } else {
        p.pos.x += (dx / d) * move;
        p.pos.y += (dy / d) * move;
        keep.push(p);
      }
    }
    this.projectiles = keep;
  }

  private impact(p: Projectile, target: Enemy | null): void {
    if (p.splash > 0) {
      this.events.push({ type: 'splash', pos: { ...p.lastTargetPos }, radius: p.splash, color: p.color });
      for (const e of [...this.enemies]) {
        if (!e.alive || e.underground) continue;
        if (this.airborne(e) && !p.hitsAir) continue;
        if (Math.hypot(e.pos.x - p.lastTargetPos.x, e.pos.y - p.lastTargetPos.y) <= p.splash + e.def.radius) {
          this.damage(e, p, 1 - (e.def.splashResist ?? 0));
        }
      }
    } else if (target) {
      if (target.def.dodge && this.random() < target.def.dodge) {
        // Silkcrane: a neat sidestep, and the shot sails past
        this.events.push({ type: 'dodge', enemy: target });
        return;
      }
      this.damage(target, p);
      if (p.chain) this.chainFrom(target, p);
    }
  }

  /** Every slow goes through here, so windborne enemies can shrug them all off. */
  slow(e: Enemy, factor: number, duration: number): void {
    if (e.def.windborne) return;
    e.slowFactor = Math.min(e.slowFactor, factor);
    e.slowTime = Math.max(e.slowTime, duration);
    const r = e.def.rile;
    if (r && e.alive && this.time - e.riledAt >= 0.5 && e.speedMult < 1 + r.max) {
      // Howler: being slowed only makes it angrier, and faster for good
      e.riledAt = this.time;
      e.speedMult = Math.min(1 + r.max, e.speedMult + r.perSlow);
      this.events.push({ type: 'rile', enemy: e, speedMult: e.speedMult });
    }
  }

  /** True while a regenerating enemy is knitting itself back together. */
  regenerating(e: Enemy): boolean {
    return !!e.def.regen && e.alive && e.sinceHit >= e.def.regen.delay && e.hp < e.maxHp;
  }

  private damage(e: Enemy, p: Projectile, mult = 1): void {
    if (p.slow) {
      this.slow(e, p.slow.factor, p.slow.duration);
    }
    const armor = this.res(e).armor * (1 - p.pierce);
    this.applyDamage(e, computeDamage(p.damage * mult, p.damageType, { armor, magicResist: e.mr }), p.damageType);
  }

  /** Lightning: jump from the first target to nearby enemies with falling damage. */
  private chainFrom(first: Enemy, p: Projectile): void {
    const c = p.chain!;
    const hit = new Set<number>([first.uid]);
    const points: Vec2[] = [{ ...first.pos }];
    let from = first;
    let dmg = p.damage;
    for (let k = 0; k < c.count; k++) {
      dmg *= c.falloff;
      let next: Enemy | null = null;
      let bestD = c.range;
      for (const e of this.enemies) {
        if (!e.alive || e.underground || hit.has(e.uid) || (this.airborne(e) && !p.hitsAir)) continue;
        const d = Math.hypot(e.pos.x - from.pos.x, e.pos.y - from.pos.y);
        if (d < bestD) {
          bestD = d;
          next = e;
        }
      }
      if (!next) break;
      hit.add(next.uid);
      points.push({ ...next.pos });
      this.applyDamage(next, computeDamage(dmg, p.damageType, this.res(next)), p.damageType);
      from = next;
    }
    if (points.length > 1) this.events.push({ type: 'chain', points, color: p.color });
  }

  private applyDamage(e: Enemy, dmg: number, type?: DamageType): void {
    if (!e.alive) return;
    if (e.phased && dmg > 0) return; // Mistfox: the blow passes straight through the mist
    if (dmg > 0) dmg *= 1 - this.wardCut(e); // Glowbearer lantern-light softens every kind of blow
    if (dmg > 0 && !e.def.ground) {
      // Copperhorn: the nearest one in range draws part of the blow onto itself.
      let gr: Enemy | null = null;
      let bestD = Infinity;
      for (const o of this.enemies) {
        const g = o.def.ground;
        if (!g || !o.alive) continue;
        const d = Math.hypot(o.pos.x - e.pos.x, o.pos.y - e.pos.y);
        if (d <= g.radius && d < bestD) {
          bestD = d;
          gr = o;
        }
      }
      if (gr) {
        const taken = dmg * gr.def.ground!.share;
        dmg -= taken;
        this.events.push({ type: 'ground', from: e, to: gr, damage: taken });
        this.applyDamage(gr, taken, type);
      }
    }
    let left = dmg;
    if (e.shield > 0) {
      const absorbed = Math.min(e.shield, left);
      e.shield -= absorbed;
      left -= absorbed;
      if (e.shield <= 0) this.events.push({ type: 'shieldBreak', enemy: e });
    }
    e.hp -= left;
    if (dmg > 0) e.sinceHit = 0;
    if (e.def.charge && dmg > 0 && e.chargeCd <= 0 && e.hp > 0) {
      e.chargeTime = e.def.charge.duration;
      e.chargeCd = e.def.charge.cooldown;
      this.events.push({ type: 'charge', enemy: e });
    }
    if (e.def.mirage && !e.mirrored && dmg > 0 && e.hp > 0) {
      // Shimmerjack: heat-shimmer copies peel off just behind it.
      e.mirrored = true;
      const decoys: Enemy[] = [];
      for (let k = 0; k < e.def.mirage.count; k++) decoys.push(this.spawn(e.def.mirage.into, e.path, Math.max(0, e.dist - 18 - k * 16)));
      this.events.push({ type: 'mirage', enemy: e, decoys });
    }
    if (e.def.ink && dmg > 0 && e.hp > 0 && e.inkCd <= this.time) {
      // Inkspitter: a startled squirt of ink hangs in the water where it was hit.
      e.inkCd = this.time + e.def.ink.cooldown;
      this.inkClouds.push({ pos: { ...e.pos }, radius: e.def.ink.radius, t: e.def.ink.duration });
      this.events.push({ type: 'ink', enemy: e, pos: { ...e.pos }, radius: e.def.ink.radius, duration: e.def.ink.duration });
    }
    if (e.def.molt && !e.molted && e.hp > 0 && e.hp < e.maxHp * e.def.molt.at) {
      // Shellsnap: the cracked shell falls away; soft, but quick.
      e.molted = true;
      e.armor = e.def.molt.armor;
      e.speedMult = Math.max(e.speedMult, e.def.molt.speedMult);
      this.events.push({ type: 'molt', enemy: e });
    }
    if (e.def.crust && dmg > 0 && e.armor > e.def.armor + 0.05) {
      // Kilnback: the baked shell cracks (this hit already met the thick crust).
      e.armor = e.def.armor;
      this.events.push({ type: 'crack', enemy: e });
    }
    if (e.def.brittle && dmg > 0) e.armor = Math.max(0, e.armor - e.def.brittle);
    if (e.def.harden && dmg > 0) e.armor = Math.min(e.def.harden.max, e.armor + e.def.harden.perHit);
    if (e.def.adapt && dmg > 0 && (type === 'physical' || type === 'magic')) {
      // Turnleaf: its hide turns to meet whatever just hit it, and lets the other guard slip.
      const a = e.def.adapt;
      if (type === 'physical') {
        e.armor = Math.min(e.def.armor + a.max, e.armor + a.step);
        e.mr = Math.max(e.def.magicResist, e.mr - a.step);
      } else {
        e.mr = Math.min(e.def.magicResist + a.max, e.mr + a.step);
        e.armor = Math.max(e.def.armor, e.armor - a.step);
      }
    }
    this.events.push({ type: 'hit', enemy: e, damage: dmg, pos: { ...e.pos } });
    if (e.hp <= 0) {
      e.alive = false;
      // Tougher levels (higher hpMult) pay proportionally more per kill.
      const bounty = e.revived ? 0 : Math.round(e.def.bounty * this.waveHpMult() * this.bountyMult(e));
      if (!e.revived && !e.def.boss && !e.def.revive) this.fallen.push({ id: e.def.id, path: e.path, dist: e.dist, pos: { ...e.pos }, at: this.time });
      if (this.fallen.length > 40) this.fallen.splice(0, this.fallen.length - 40);
      this.coins += bounty;
      this.events.push({ type: 'kill', enemy: e, bounty });
      if (this.hero?.alive) {
        const near = Math.hypot(e.pos.x - this.hero.pos.x, e.pos.y - this.hero.pos.y) < 260;
        this.grantHeroXp(e.def.bounty * (near ? 1 : 0.35));
      }
      if (!e.def.boss) this.feedOn(e);
      if (e.def.splitInto) this.split(e);
      if (e.def.sporeBurst) this.sporeBurst(e);
      if (e.def.grief) {
        // Ringtail Mourner: its fall hardens the resolve (and hides) of those around it
        const g = e.def.grief;
        const mourners = this.enemies.filter((o) => o.alive && o !== e && Math.hypot(o.pos.x - e.pos.x, o.pos.y - e.pos.y) <= g.radius);
        for (const o of mourners) o.armor = Math.min(0.85, o.armor + g.armor);
        this.events.push({ type: 'grief', enemy: e, radius: g.radius, mourners });
      }
      if (e.def.keg) this.kegBlast(e);
      if (e.def.glare) this.glareBurst(e);
      if (e.def.echo && !e.revived) {
        // Echo Wisp: re-forms once where it fell, weaker, paying no second bounty.
        const r = this.spawn(e.def.id, e.path, e.dist);
        r.hp = Math.round(r.maxHp * e.def.echo.hpFrac);
        r.revived = true;
        this.events.push({ type: 'echo', enemy: r });
      }
      return;
    }
    this.checkPhases(e);
  }

  /** Gorgegrubs feed on fallen allies nearby: each meal heals and swells them (up to maxStacks). */
  private feedOn(dead: Enemy): void {
    for (const g of this.enemies) {
      const f = g.def.feed;
      if (!f || !g.alive || g === dead || g.fed >= f.maxStacks) continue;
      if (Math.hypot(g.pos.x - dead.pos.x, g.pos.y - dead.pos.y) > f.radius) continue;
      g.fed++;
      const grow = Math.round(g.maxHp * f.growth);
      g.maxHp += grow;
      g.hp = Math.min(g.maxHp, g.hp + grow + g.maxHp * f.heal);
      this.events.push({ type: 'feed', enemy: g, from: { ...dead.pos } });
    }
  }

  /** Powdermonkey: its keg goes up when it falls, scorching nearby soldiers and the hero. */
  private kegBlast(src: Enemy): void {
    const k = src.def.keg!;
    const dmg = k.damage * this.attackMult();
    const hits: Vec2[] = [];
    for (const s of this.soldiers) {
      if (!s.alive || Math.hypot(s.pos.x - src.pos.x, s.pos.y - src.pos.y) > k.radius) continue;
      hits.push({ ...s.pos });
      this.hurtSoldier(s, dmg);
    }
    const h = this.hero;
    if (h && h.alive && Math.hypot(h.pos.x - src.pos.x, h.pos.y - src.pos.y) <= k.radius) {
      hits.push({ ...h.pos });
      this.hurtHero(dmg);
    }
    this.events.push({ type: 'keg', pos: { ...src.pos }, radius: k.radius, hits });
  }

  /** Glareflies flash on death: nearby shooting towers are dazzled (frozen) briefly. Shares the chill immunity window. */
  private glareBurst(src: Enemy): void {
    const gl = src.def.glare!;
    const hit: Tower[] = [];
    for (const t of this.towers) {
      if (!t || t.rally || t.chillImmune > 0) continue;
      if (Math.hypot(t.pos.x - src.pos.x, t.pos.y - src.pos.y) > gl.radius) continue;
      t.frozen = Math.max(t.frozen, gl.duration);
      t.chillImmune = gl.duration + THAW_IMMUNITY;
      hit.push(t);
    }
    this.events.push({ type: 'glare', enemy: src, towers: hit, radius: gl.radius });
  }

  /** Puffcaps burst on death: nearby living allies (not bosses) move faster for a few seconds. */
  private sporeBurst(src: Enemy): void {
    const sb = src.def.sporeBurst!;
    const hasted: Enemy[] = [];
    for (const e of this.enemies) {
      if (!e.alive || e === src || e.def.boss) continue;
      if (Math.hypot(e.pos.x - src.pos.x, e.pos.y - src.pos.y) > sb.radius) continue;
      e.hasteMult = Math.max(e.hasteMult, sb.speedMult);
      e.hasteTime = Math.max(e.hasteTime, sb.duration);
      hasted.push(e);
    }
    this.events.push({ type: 'spores', enemy: src, radius: sb.radius, hasted });
  }

  private split(parent: Enemy): void {
    const { enemy, count } = parent.def.splitInto!;
    const children: Enemy[] = [];
    for (let i = 0; i < count; i++) {
      const c = this.spawn(enemy, parent.path, Math.max(0, parent.dist - i * 14));
      children.push(c);
    }
    this.events.push({ type: 'split', parent, children });
  }

  private checkPhases(e: Enemy): void {
    const phases = e.def.phases;
    if (!phases) return;
    while (e.phase < phases.length && e.hp / e.maxHp <= phases[e.phase].at) {
      const ph = phases[e.phase++];
      if (ph.speedMult) e.speedMult = ph.speedMult;
      if (ph.shield) {
        e.shield = ph.shield;
        e.maxShield = ph.shield;
      }
      if (ph.summon) {
        for (let i = 0; i < ph.summon.count; i++) this.spawn(ph.summon.enemy, e.path, Math.max(0, e.dist - 20 - i * 16));
      }
      this.events.push({ type: 'phase', enemy: e, message: ph.message });
    }
  }

  private checkEnd(): void {
    if (this.lives <= 0) {
      this.status = 'defeat';
      this.events.push({ type: 'defeat' });
      return;
    }
    if (this.status === 'running' && this.schedules.length === 0 && this.enemies.length === 0) {
      if (!this.wavesRemaining) {
        this.status = 'victory';
        this.events.push({ type: 'victory' });
      } else {
        this.events.push({ type: 'waveCleared', index: this.waveIndex });
        // Stay 'running' so countdown continues; status distinction only matters for the first wave.
        this.status = 'prep';
      }
    }
  }
}
