import type { EnemyDef, LevelDef, TargetMode, TowerDef, Vec2 } from '../data/types';
import { ENEMIES } from '../data/enemies';
import { TOWERS, sellValue } from '../data/towers';
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
}

export type SimEvent =
  | { type: 'spawn'; enemy: Enemy }
  | { type: 'shoot'; tower: Tower; projectile: Projectile }
  | { type: 'hit'; enemy: Enemy; damage: number; pos: Vec2 }
  | { type: 'splash'; pos: Vec2; radius: number; color: number }
  | { type: 'kill'; enemy: Enemy; bounty: number }
  | { type: 'leak'; enemy: Enemy; lives: number }
  | { type: 'waveStart'; index: number; bonus: number }
  | { type: 'waveCleared'; index: number }
  | { type: 'build'; tower: Tower }
  | { type: 'upgrade'; tower: Tower }
  | { type: 'sell'; tower: Tower; refund: number }
  | { type: 'melee'; pos: Vec2 }
  | { type: 'heal'; source: Enemy; targets: Enemy[]; radius: number }
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
  events: SimEvent[] = [];

  private nextUid = 1;

  constructor(level: LevelDef) {
    this.level = level;
    this.paths = level.paths.map((p) => new Path(p));
    this.coins = level.startCoins;
    this.lives = level.lives;
    this.towers = level.slots.map(() => null);
  }

  get totalWaves(): number {
    return this.level.waves.length;
  }

  get wavesRemaining(): boolean {
    return this.waveIndex < this.totalWaves - 1;
  }

  /** Start the next wave now. Calling early awards bonus coins. */
  callNextWave(): boolean {
    if (this.status === 'victory' || this.status === 'defeat') return false;
    if (!this.wavesRemaining) return false;
    const bonus = this.waveIndex >= 0 || this.status === 'running' ? earlyCallBonus(this.waveCountdown, this.waveIndex + 1) : 0;
    this.coins += bonus;
    this.waveIndex++;
    this.schedules.push({ events: buildSchedule(this.level.waves[this.waveIndex]), cursor: 0, t: 0 });
    this.status = 'running';
    this.waveCountdown = WAVE_GAP;
    this.events.push({ type: 'waveStart', index: this.waveIndex, bonus });
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
    const t: Tower = { uid: this.nextUid++, def, tier: 0, slot, pos, cooldown: 0, target: 'first', rally: null };
    if (def.tiers[0].soldiers) {
      t.rally = this.rallyPointFor(pos, def.tiers[0].range);
      this.syncSquad(t, true);
    }
    this.towers[slot] = t;
    this.events.push({ type: 'build', tower: t });
    return t;
  }

  upgradeCost(tower: Tower): number | null {
    const next = tower.def.tiers[tower.tier + 1];
    return next ? next.cost : null;
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
    const refund = sellValue(t.def, t.tier);
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
    const range = t.def.tiers[t.tier].range;
    if (Math.hypot(p.x - t.pos.x, p.y - t.pos.y) > range) return false;
    t.rally = { ...p };
    for (const s of this.soldiers) if (s.towerUid === t.uid) s.home = this.formation(t.rally, s.index);
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
    const stats = t.def.tiers[t.tier].soldiers;
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
      };
      this.soldiers.push(s);
      squad.push(s);
    }
    for (const s of squad) {
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

    // Wave countdown (auto-start).
    if (this.wavesRemaining) {
      this.waveCountdown -= dt;
      if (this.waveCountdown <= 0) {
        this.waveCountdown = 0;
        this.callNextWave();
      }
    }

    this.spawnEnemies(dt);
    this.updateSoldiers(dt);
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
      hp: def.hp,
      maxHp: def.hp,
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
      if (e.blockedBy) {
        const s = this.soldiers.find((so) => so.uid === e.blockedBy);
        if (!s || !s.alive) {
          e.blockedBy = 0;
        } else if (Math.hypot(s.pos.x - e.pos.x, s.pos.y - e.pos.y) <= SOLDIER_REACH + 4) {
          // Held in place: brawl with the soldier.
          e.attackCd -= dt;
          if (e.attackCd <= 0) {
            e.attackCd = 1 / e.def.attackRate;
            this.hurtSoldier(s, e.def.attack);
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
      const tower = this.towers.find((t) => t?.uid === s.towerUid);
      const stats = tower?.def.tiers[tower.tier].soldiers;
      if (!tower || !stats || !tower.rally) continue;
      if (!s.alive) {
        s.respawnTimer -= dt;
        if (s.respawnTimer <= 0) {
          s.alive = true;
          s.hp = stats.hp;
          s.pos = { x: tower.pos.x, y: tower.pos.y };
        }
        continue;
      }
      // Validate current target.
      let target = s.targetUid ? byUid.get(s.targetUid) : undefined;
      if (target && (!target.alive || Math.hypot(target.pos.x - tower.rally.x, target.pos.y - tower.rally.y) > ENGAGE_RADIUS * 1.5)) {
        this.releaseEnemy(s);
        target = undefined;
      }
      if (!target) {
        target = this.findSoldierTarget(s, tower.rally);
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
      if (!e.alive || e.def.flying) continue;
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
    const tower = this.towers.find((t) => t?.uid === s.towerUid);
    const stats = tower?.def.tiers[tower.tier].soldiers;
    s.hp -= computeDamage(raw, 'physical', { armor: stats?.armor ?? 0, magicResist: 0 });
    if (s.hp <= 0) {
      s.alive = false;
      s.hp = 0;
      s.respawnTimer = stats?.respawn ?? 10;
      this.releaseEnemy(s);
      for (const e of this.enemies) if (e.blockedBy === s.uid) e.blockedBy = 0;
      this.events.push({ type: 'soldierDown', soldier: s });
    }
  }

  private pickTarget(t: Tower, range: number): Enemy | null {
    let best: Enemy | null = null;
    let bestScore = -Infinity;
    for (const e of this.enemies) {
      if (!e.alive) continue;
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

  private fireTowers(dt: number): void {
    for (const t of this.towers) {
      if (!t) continue;
      t.cooldown -= dt;
      if (t.cooldown > 0) continue;
      const stats = t.def.tiers[t.tier];
      if (stats.soldiers || stats.fireRate <= 0) continue;
      const target = this.pickTarget(t, stats.range);
      if (!target) {
        t.cooldown = 0;
        continue;
      }
      t.cooldown = 1 / stats.fireRate;
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
        damage: stats.damage,
        damageType: t.def.damageType,
        splash: stats.splash ?? 0,
        slow: stats.slow,
        color: t.def.color,
        homing: !stats.lob,
        hitsAir: t.def.hitsAir,
        origin,
        travel: Math.hypot(aim.x - origin.x, aim.y - origin.y),
        kind: t.def.id,
      };
      this.projectiles.push(p);
      this.events.push({ type: 'shoot', tower: t, projectile: p });
    }
  }

  private moveProjectiles(dt: number): void {
    const byUid = new Map(this.enemies.map((e) => [e.uid, e]));
    const keep: Projectile[] = [];
    for (const p of this.projectiles) {
      const target = byUid.get(p.targetUid);
      if (p.homing && target && target.alive) p.lastTargetPos = { ...target.pos };
      const dx = p.lastTargetPos.x - p.pos.x;
      const dy = p.lastTargetPos.y - p.pos.y;
      const d = Math.hypot(dx, dy);
      const move = p.speed * dt;
      if (d <= move + 4) {
        this.impact(p, p.homing && target && target.alive ? target : null);
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
        if (!e.alive) continue;
        if (e.def.flying && !p.hitsAir) continue;
        if (Math.hypot(e.pos.x - p.lastTargetPos.x, e.pos.y - p.lastTargetPos.y) <= p.splash + e.def.radius) {
          this.damage(e, p);
        }
      }
    } else if (target) {
      this.damage(target, p);
    }
  }

  private damage(e: Enemy, p: Projectile): void {
    if (p.slow) {
      e.slowFactor = Math.min(e.slowFactor, p.slow.factor);
      e.slowTime = Math.max(e.slowTime, p.slow.duration);
    }
    this.applyDamage(e, computeDamage(p.damage, p.damageType, e.def));
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
      this.coins += e.def.bounty;
      this.events.push({ type: 'kill', enemy: e, bounty: e.def.bounty });
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
