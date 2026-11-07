import type { EnemyDef, HeroDef, LevelDef, SoldierStats, TargetMode, TowerDef, Vec2 } from '../data/types';
import { SPELLS } from '../data/spells';
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
  phase: number; // index of next boss phase to trigger
  speedMult: number;
}

export interface Soldier {
  uid: number;
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
  | { type: 'heroSkill'; hero: Hero; hits: Enemy[] }
  | { type: 'heroShoot'; hero: Hero; projectile: Projectile }
  | { type: 'heroLevel'; hero: Hero }
  | { type: 'heroDown'; hero: Hero }
  | { type: 'heroBack'; hero: Hero }
  | { type: 'heal'; source: Enemy; targets: Enemy[]; radius: number }
  | { type: 'chill'; source: Enemy; towers: Tower[]; radius: number }
  | { type: 'burrow'; enemy: Enemy; down: boolean }
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
  events: SimEvent[] = [];

  private nextUid = 1;

  /** Multiplier on tower shot damage (from the village Defense Workshop). */
  towerDamageMult = 1;

  /** Multiplier on Grove Call Rangers' hp and damage (from the village Ranger Lodge). */
  rangerMult = 1;

  constructor(
    level: LevelDef,
    heroId: string | null = null,
    opts: { towerDamageMult?: number; bonusCoins?: number; rangerMult?: number; heroLevel?: number } = {},
  ) {
    this.level = level;
    this.towerDamageMult = opts.towerDamageMult ?? 1;
    this.rangerMult = opts.rangerMult ?? 1;
    this.paths = level.paths.map((p) => new Path(p));
    this.coins = level.startCoins + (opts.bonusCoins ?? 0);
    this.lives = level.lives;
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
    if (!def || !this.spellReady(id) || !this.isActive()) return false;
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
    } else {
      this.strikes.push({ uid: this.nextUid++, pos: { ...pos }, timer: def.delay ?? 0, spellId: id });
    }
    this.spellCd[id] = def.cooldown;
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
      for (const e of hits) this.applyDamage(e, computeDamage(def.damage ?? 0, def.damageType ?? 'physical', e.def));
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
    if (sk.kind === 'quake') pool = pool.filter((e) => !e.def.flying);
    if (sk.maxTargets) {
      pool.sort((a, b) => b.dist - a.dist);
      pool = pool.slice(0, sk.maxTargets);
    }
    for (const e of pool) {
      if (sk.slow) {
        e.slowFactor = Math.min(e.slowFactor, sk.slow.factor);
        e.slowTime = Math.max(e.slowTime, sk.slow.duration);
      }
      this.applyDamage(e, computeDamage(dmg, sk.damageType, e.def));
    }
    this.events.push({ type: 'heroSkill', hero: h, hits: pool });
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
    const regen = h.def.regen + (h.def.passive.kind === 'toughness' ? h.def.passive.regen : 0);
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
          if (!e.alive || e.def.flying || e.underground) continue;
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
          this.applyDamage(target, computeDamage(this.heroHitDamage(), atk.type, target.def));
        }
        return;
      }
    } else if (h.attackCd <= 0) {
      let best: Enemy | null = null;
      for (const e of this.enemies) {
        if (!e.alive || e.underground || (e.def.flying && !atk.hitsAir)) continue;
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
    if (h.def.passive.kind === 'crit' && Math.random() < h.def.passive.chance) dmg *= h.def.passive.mult;
    return dmg;
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
    this.waveCountdown = WAVE_GAP;
    this.events.push({ type: 'waveStart', index: this.waveIndex, bonus, income });
    return true;
  }

  canBuild(slot: number, towerId: string): boolean {
    const def = TOWERS[towerId];
    return !!def && this.towers[slot] === null && this.coins >= def.tiers[0].cost && this.isActive();
  }

  build(slot: number, towerId: string): Tower | null {
    if (!this.canBuild(slot, towerId)) return null;
    const def = TOWERS[towerId];
    this.coins -= def.tiers[0].cost;
    const pos = { ...this.level.slots[slot] };
    const t: Tower = { uid: this.nextUid++, def, tier: 0, slot, pos, cooldown: 0, target: 'first', rally: null, spec: null, frozen: 0 };
    if (def.tiers[0].soldiers) {
      t.rally = this.rallyPointFor(pos, def.tiers[0].range);
      this.syncSquad(t, true);
    }
    this.towers[slot] = t;
    this.events.push({ type: 'build', tower: t });
    return t;
  }

  upgradeCost(tower: Tower): number | null {
    if (tower.spec) return null;
    const next = tower.def.tiers[tower.tier + 1];
    return next ? next.cost : null;
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
    if (!sp || this.coins < sp.stats.cost) return false;
    this.coins -= sp.stats.cost;
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
    const refund = sellValue(t.def, t.tier, t.spec);
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
      hp: Math.round(def.hp * (this.level.hpMult ?? 1)),
      maxHp: Math.round(def.hp * (this.level.hpMult ?? 1)),
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
      healCd: def.heal ? def.heal.interval : 0,
      chillCd: def.chill ? def.chill.interval * 0.6 : 0,
      underground: false,
      burrowCd: def.burrow ? def.burrow.interval : 0,
      phase: 0,
      speedMult: 1,
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
      if (e.def.heal) this.tickHealer(e, dt);
      if (e.def.chill) this.tickChill(e, dt);
      if (e.def.burrow) this.tickBurrow(e, dt);
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
            if (isHero) this.hurtHero(e.def.attack);
            else this.hurtSoldier(s!, e.def.attack);
          }
          continue;
        }
      }
      e.dist += e.def.speed * e.slowFactor * e.speedMult * dt;
      const path = this.paths[e.path];
      e.pos = path.pointAt(e.dist);
      if (e.dist >= path.length) {
        e.alive = false;
        this.lives = Math.max(0, this.lives - e.def.livesCost);
        this.events.push({ type: 'leak', enemy: e, lives: e.def.livesCost });
      }
    }
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
      t.frozen = Math.max(t.frozen, c.duration);
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
    for (const s of this.soldiers) {
      const stats = s.stats;
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
            this.applyDamage(target, computeDamage(stats.damage, 'physical', target.def));
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
      if (!e.alive || e.def.flying || e.underground) continue;
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
      if (!e.alive || e.underground) continue;
      if (e.def.flying && !t.def.hitsAir) continue;
      const d = Math.hypot(e.pos.x - t.pos.x, e.pos.y - t.pos.y);
      if (d > range) continue;
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
        if (!e.alive || e.underground || taken.has(e.uid) || (e.def.flying && !t.def.hitsAir)) continue;
        if (Math.hypot(e.pos.x - t.pos.x, e.pos.y - t.pos.y) > range) continue;
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
      if (t.frozen > 0) {
        t.frozen = Math.max(0, t.frozen - dt);
        continue;
      }
      t.cooldown -= dt;
      if (t.cooldown > 0) continue;
      const stats = this.stats(t);
      if (stats.soldiers || stats.fireRate <= 0) continue;
      const targets = this.pickTargets(t, stats.range, stats.multishot ?? 1);
      if (!targets.length) {
        t.cooldown = 0;
        continue;
      }
      t.cooldown = 1 / (stats.fireRate * this.towerHaste(t));
      for (const target of targets) {
        const origin = { x: t.pos.x, y: t.pos.y - 18 };
        let aim = { ...target.pos };
        if (stats.lob) {
          // Lead the target: predict where it will be when the rock lands.
          const flight = Math.hypot(aim.x - origin.x, aim.y - origin.y) / stats.projectileSpeed;
          const moving = target.blockedBy ? 0 : target.def.speed * target.slowFactor * target.speedMult;
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
        if (e.def.flying && !p.hitsAir) continue;
        if (Math.hypot(e.pos.x - p.lastTargetPos.x, e.pos.y - p.lastTargetPos.y) <= p.splash + e.def.radius) {
          this.damage(e, p);
        }
      }
    } else if (target) {
      this.damage(target, p);
      if (p.chain) this.chainFrom(target, p);
    }
  }

  private damage(e: Enemy, p: Projectile): void {
    if (p.slow) {
      e.slowFactor = Math.min(e.slowFactor, p.slow.factor);
      e.slowTime = Math.max(e.slowTime, p.slow.duration);
    }
    const armor = e.def.armor * (1 - p.pierce);
    this.applyDamage(e, computeDamage(p.damage, p.damageType, { armor, magicResist: e.def.magicResist }));
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
        if (!e.alive || e.underground || hit.has(e.uid) || (e.def.flying && !p.hitsAir)) continue;
        const d = Math.hypot(e.pos.x - from.pos.x, e.pos.y - from.pos.y);
        if (d < bestD) {
          bestD = d;
          next = e;
        }
      }
      if (!next) break;
      hit.add(next.uid);
      points.push({ ...next.pos });
      this.applyDamage(next, computeDamage(dmg, p.damageType, next.def));
      from = next;
    }
    if (points.length > 1) this.events.push({ type: 'chain', points, color: p.color });
  }

  private applyDamage(e: Enemy, dmg: number): void {
    if (!e.alive) return;
    let left = dmg;
    if (e.shield > 0) {
      const absorbed = Math.min(e.shield, left);
      e.shield -= absorbed;
      left -= absorbed;
      if (e.shield <= 0) this.events.push({ type: 'shieldBreak', enemy: e });
    }
    e.hp -= left;
    this.events.push({ type: 'hit', enemy: e, damage: dmg, pos: { ...e.pos } });
    if (e.hp <= 0) {
      e.alive = false;
      // Tougher levels (higher hpMult) pay proportionally more per kill.
      const bounty = Math.round(e.def.bounty * (this.level.hpMult ?? 1));
      this.coins += bounty;
      this.events.push({ type: 'kill', enemy: e, bounty });
      if (this.hero?.alive) {
        const near = Math.hypot(e.pos.x - this.hero.pos.x, e.pos.y - this.hero.pos.y) < 260;
        this.grantHeroXp(e.def.bounty * (near ? 1 : 0.35));
      }
      if (e.def.splitInto) this.split(e);
      return;
    }
    this.checkPhases(e);
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
