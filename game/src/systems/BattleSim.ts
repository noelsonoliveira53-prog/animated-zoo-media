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
}

export interface Tower {
  uid: number;
  def: TowerDef;
  tier: number;
  slot: number;
  pos: Vec2;
  cooldown: number;
  target: TargetMode;
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
  | { type: 'victory' }
  | { type: 'defeat' };

export type BattleStatus = 'prep' | 'running' | 'victory' | 'defeat';

/** Seconds of countdown before the next wave auto-starts. */
export const WAVE_GAP = 14;
export const FIRST_WAVE_GAP = 25;

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
    const t: Tower = { uid: this.nextUid++, def, tier: 0, slot, pos: { ...this.level.slots[slot] }, cooldown: 0, target: 'first' };
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
    this.events.push({ type: 'upgrade', tower: t });
    return true;
  }

  sell(slot: number): boolean {
    const t = this.towers[slot];
    if (!t || !this.isActive()) return false;
    const refund = sellValue(t.def, t.tier);
    this.coins += refund;
    this.towers[slot] = null;
    this.events.push({ type: 'sell', tower: t, refund });
    return true;
  }

  setTargetMode(slot: number, mode: TargetMode): void {
    const t = this.towers[slot];
    if (t) t.target = mode;
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
      e.dist += e.def.speed * e.slowFactor * dt;
      const path = this.paths[e.path];
      e.pos = path.pointAt(e.dist);
      if (e.dist >= path.length) {
        e.alive = false;
        this.lives = Math.max(0, this.lives - e.def.livesCost);
        this.events.push({ type: 'leak', enemy: e, lives: e.def.livesCost });
      }
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
      const target = this.pickTarget(t, stats.range);
      if (!target) {
        t.cooldown = 0;
        continue;
      }
      t.cooldown = 1 / stats.fireRate;
      const p: Projectile = {
        uid: this.nextUid++,
        towerUid: t.uid,
        pos: { x: t.pos.x, y: t.pos.y - 18 },
        targetUid: target.uid,
        lastTargetPos: { ...target.pos },
        speed: stats.projectileSpeed,
        damage: stats.damage,
        damageType: t.def.damageType,
        splash: stats.splash ?? 0,
        slow: stats.slow,
        color: t.def.color,
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
      if (target && target.alive) p.lastTargetPos = { ...target.pos };
      const dx = p.lastTargetPos.x - p.pos.x;
      const dy = p.lastTargetPos.y - p.pos.y;
      const d = Math.hypot(dx, dy);
      const move = p.speed * dt;
      if (d <= move + 4) {
        this.impact(p, target && target.alive ? target : null);
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
      for (const e of this.enemies) {
        if (!e.alive) continue;
        if (Math.hypot(e.pos.x - p.lastTargetPos.x, e.pos.y - p.lastTargetPos.y) <= p.splash + e.def.radius) {
          this.damage(e, p);
        }
      }
    } else if (target) {
      this.damage(target, p);
    }
  }

  private damage(e: Enemy, p: Projectile): void {
    const dmg = computeDamage(p.damage, p.damageType, e.def);
    e.hp -= dmg;
    if (p.slow) {
      e.slowFactor = Math.min(e.slowFactor, p.slow.factor);
      e.slowTime = Math.max(e.slowTime, p.slow.duration);
    }
    this.events.push({ type: 'hit', enemy: e, damage: dmg, pos: { ...e.pos } });
    if (e.hp <= 0 && e.alive) {
      e.alive = false;
      this.coins += e.def.bounty;
      this.events.push({ type: 'kill', enemy: e, bounty: e.def.bounty });
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
