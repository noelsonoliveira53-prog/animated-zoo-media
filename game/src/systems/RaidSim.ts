import { CAMP_BUILDINGS, RAID_TIME, TROOPS, type TroopDef } from '../data/raid';
import type { Vec2 } from '../data/types';
import { buildingCenter, buildingRadius, tierMult, type Camp, type CampBuilding } from './camp';

// Pure raid simulation: troops attack a Murkhorde camp; camp defenses shoot back.

export interface Troop {
  uid: number;
  def: TroopDef;
  pos: Vec2;
  hp: number;
  maxHp: number;
  alive: boolean;
  targetUid: number;
  wallUid: number; // wall currently blocking this troop
  attackCd: number;
  healCd: number;
  poisonT?: number; // Rattle Trap venom: seconds of poison left
  poisonDps?: number;
  tunneling?: boolean; // Mole Tunneler: underground while it digs toward a target (defenses can't reach it)
}

export type RaidEvent =
  | { type: 'deploy'; troop: Troop }
  | { type: 'troopHit'; troop: Troop; damage: number; from: Vec2 }
  | { type: 'troopDown'; troop: Troop }
  | { type: 'buildingHit'; building: CampBuilding; damage: number; by: Troop }
  | { type: 'destroyed'; building: CampBuilding; loot: { coins: number; glowsap: number } }
  | { type: 'shot'; from: Vec2; to: Vec2; splash: number; building: CampBuilding }
  | { type: 'mend'; from: CampBuilding; healed: CampBuilding[] }
  | { type: 'troopHeal'; troop: Troop; healed: Troop[] }
  | { type: 'poisoned'; troop: Troop; building: CampBuilding }
  | { type: 'swarm'; building: CampBuilding; radius: number; stung: Troop[] }
  | { type: 'end'; stars: number };

export class RaidSim {
  readonly camp: Camp;
  troops: Troop[] = [];
  army: Record<string, number>; // troops still available to deploy
  deployed: Record<string, number> = {};
  time = 0;
  ended = false;
  loot = { coins: 0, glowsap: 0 };
  events: RaidEvent[] = [];
  private cooldowns = new Map<number, number>();
  private nextUid = 1000;
  private dmgMult: number;
  private lootMult: number;

  constructor(camp: Camp, army: Record<string, number>) {
    this.camp = camp;
    this.army = { ...army };
    const m = tierMult(camp.tier);
    this.dmgMult = m.dmg;
    this.lootMult = m.loot;
  }

  get timeLeft(): number {
    return Math.max(0, RAID_TIME - this.time);
  }

  /** Buildings that count toward destruction (everything except walls). */
  get counted(): CampBuilding[] {
    return this.camp.buildings.filter((b) => !CAMP_BUILDINGS[b.type].wall);
  }

  get standing(): CampBuilding[] {
    return this.counted.filter((b) => b.hp > 0);
  }

  get walls(): CampBuilding[] {
    return this.camp.buildings.filter((b) => CAMP_BUILDINGS[b.type].wall && b.hp > 0);
  }

  get destruction(): number {
    const total = this.counted.length;
    return total ? (total - this.standing.length) / total : 0;
  }

  get stars(): number {
    let s = 0;
    if (this.destruction >= 0.5) s++;
    if (this.camp.buildings.some((b) => CAMP_BUILDINGS[b.type].hq && b.hp <= 0)) s++;
    if (this.destruction >= 1) s++;
    return s;
  }

  /** Can troops be placed here? Not on top of the camp: keep a margin around every building. */
  canDeployAt(p: Vec2): boolean {
    return this.camp.buildings.every((b) => {
      const c = buildingCenter(b);
      return Math.hypot(c.x - p.x, c.y - p.y) > buildingRadius(b) + 46;
    });
  }

  deploy(id: string, p: Vec2): Troop | null {
    if (this.ended || (this.army[id] ?? 0) <= 0 || !this.canDeployAt(p)) return null;
    const def = TROOPS[id];
    this.army[id]--;
    this.deployed[id] = (this.deployed[id] ?? 0) + 1;
    const t: Troop = { uid: this.nextUid++, def, pos: { ...p }, hp: def.hp, maxHp: def.hp, alive: true, targetUid: 0, wallUid: 0, attackCd: 0.3, healCd: 0.5 };
    this.troops.push(t);
    this.events.push({ type: 'deploy', troop: t });
    return t;
  }

  drainEvents(): RaidEvent[] {
    const e = this.events;
    this.events = [];
    return e;
  }

  update(dt: number): void {
    let left = dt;
    while (left > 0 && !this.ended) {
      const step = Math.min(left, 1 / 30);
      this.step(step);
      left -= step;
    }
  }

  private step(dt: number): void {
    this.time += dt;
    for (const t of this.troops) if (t.alive) this.updateTroop(t, dt);
    for (const t of this.troops) if (t.alive && t.def.heals) this.tickHeal(t, dt);
    this.tickVenom(dt);
    this.updateDefenses(dt);
    this.updateMenders(dt);
    this.checkEnd();
  }

  private pickTarget(t: Troop): CampBuilding | undefined {
    const standing = this.standing;
    let pool = standing;
    if (t.def.prefers === 'defense') {
      const defs = standing.filter((b) => CAMP_BUILDINGS[b.type].defense);
      if (defs.length) pool = defs;
    } else if (t.def.prefers === 'hq') {
      const hq = standing.filter((b) => CAMP_BUILDINGS[b.type].hq);
      if (hq.length) pool = hq;
    } else if (t.def.prefers === 'loot') {
      const loot = standing.filter((b) => CAMP_BUILDINGS[b.type].loot);
      if (loot.length) pool = loot;
    }
    let best: CampBuilding | undefined;
    let bestD = Infinity;
    for (const b of pool) {
      const c = buildingCenter(b);
      const d = Math.hypot(c.x - t.pos.x, c.y - t.pos.y) - buildingRadius(b);
      if (d < bestD) {
        bestD = d;
        best = b;
      }
    }
    return best;
  }

  private updateTroop(t: Troop, dt: number): void {
    let target = this.camp.buildings.find((b) => b.uid === t.targetUid && b.hp > 0);
    if (!target) {
      target = this.pickTarget(t);
      t.targetUid = target?.uid ?? 0;
    }
    if (!target) return;
    // A wall in the way? Ground troops must break it first.
    let wall = t.wallUid ? this.camp.buildings.find((b) => b.uid === t.wallUid && b.hp > 0) : undefined;
    if (!wall) t.wallUid = 0;
    const c = buildingCenter(target);
    const reach = buildingRadius(target) + t.def.range;
    const d = Math.hypot(c.x - t.pos.x, c.y - t.pos.y);
    t.tunneling = !!t.def.burrows && !wall && d > reach;
    if (!wall && d > reach) {
      const step = Math.min(t.def.speed * this.mireFactor(t) * dt, d - reach + 1);
      const next = { x: t.pos.x + ((c.x - t.pos.x) / d) * step, y: t.pos.y + ((c.y - t.pos.y) / d) * step };
      if (!t.def.flying && !t.def.burrows && t.def.range < 60) {
        wall = this.walls.find((w) => {
          const wc = buildingCenter(w);
          return Math.hypot(wc.x - next.x, wc.y - next.y) < buildingRadius(w) + 10;
        });
        if (wall) t.wallUid = wall.uid;
      }
      if (!wall) {
        t.pos = next;
        return;
      }
    }
    if (wall) {
      t.attackCd -= dt;
      if (t.attackCd > 0) return;
      t.attackCd = 1 / t.def.rate;
      this.hurtBuilding(wall, t.def.damage * (t.def.wallMult ?? 1), t);
      return;
    }
    t.attackCd -= dt;
    if (t.attackCd > 0) return;
    t.attackCd = 1 / t.def.rate;
    if (t.def.splash) {
      for (const b of [...this.standing, ...this.walls]) {
        const bc = buildingCenter(b);
        const mult = CAMP_BUILDINGS[b.type].wall ? (t.def.wallMult ?? 1) : 1;
        if (b === target || Math.hypot(bc.x - c.x, bc.y - c.y) <= t.def.splash + buildingRadius(b)) this.hurtBuilding(b, t.def.damage * mult, t);
      }
    } else {
      this.hurtBuilding(target, t.def.damage, t);
    }
  }

  /** Sludge Pits: ground troops wading near one slow down (the strongest pit in range applies; flyers ignore it). */
  mireFactor(t: Troop): number {
    if (t.def.flying || t.def.wader || t.def.burrows) return 1;
    let f = 1;
    for (const b of this.standing) {
      const m = CAMP_BUILDINGS[b.type].mire;
      if (!m) continue;
      const c = buildingCenter(b);
      if (Math.hypot(c.x - t.pos.x, c.y - t.pos.y) <= m.radius) f = Math.min(f, m.factor);
    }
    return f;
  }

  /** Rattle Traps: ground troops passing near one are poisoned (refreshed while they stay close) and keep losing health afterwards. */
  private tickVenom(dt: number): void {
    const traps = this.standing.filter((b) => CAMP_BUILDINGS[b.type].venom);
    for (const t of this.troops) {
      if (!t.alive) continue;
      if (!t.def.flying && !t.tunneling) {
        for (const b of traps) {
          const v = CAMP_BUILDINGS[b.type].venom!;
          const c = buildingCenter(b);
          if (Math.hypot(c.x - t.pos.x, c.y - t.pos.y) > v.radius + buildingRadius(b)) continue;
          if (!(t.poisonT! > 0)) this.events.push({ type: 'poisoned', troop: t, building: b });
          t.poisonT = v.duration;
          t.poisonDps = Math.max(t.poisonDps ?? 0, v.dps * this.dmgMult);
        }
      }
      if (t.poisonT! > 0) {
        t.poisonT! -= dt;
        t.hp -= (t.poisonDps ?? 0) * dt;
        if (t.poisonT! <= 0) t.poisonDps = 0;
        if (t.hp <= 0) {
          t.alive = false;
          this.events.push({ type: 'troopDown', troop: t });
        }
      }
    }
  }

  /** Toad Mender: every few seconds, tops up hurt troops around it (itself included). */
  private tickHeal(t: Troop, dt: number): void {
    const h = t.def.heals!;
    t.healCd -= dt;
    if (t.healCd > 0) return;
    t.healCd = h.interval;
    const healed: Troop[] = [];
    for (const o of this.troops) {
      if (!o.alive || o.hp >= o.maxHp || Math.hypot(o.pos.x - t.pos.x, o.pos.y - t.pos.y) > h.radius) continue;
      o.hp = Math.min(o.maxHp, o.hp + h.amount);
      healed.push(o);
    }
    if (healed.length) this.events.push({ type: 'troopHeal', troop: t, healed });
  }

  /** Standing Stones: the strongest stone in reach (not the stone itself) softens blows on a building. */
  wardCut(b: CampBuilding): number {
    let cut = 0;
    const c = buildingCenter(b);
    for (const o of this.standing) {
      const w = CAMP_BUILDINGS[o.type].ward;
      if (!w || o === b) continue;
      const oc = buildingCenter(o);
      if (Math.hypot(oc.x - c.x, oc.y - c.y) <= w.radius) cut = Math.max(cut, w.cut);
    }
    return cut;
  }

  private hurtBuilding(b: CampBuilding, dmg: number, by: Troop): void {
    if (b.hp <= 0) return;
    dmg *= 1 - this.wardCut(b);
    b.hp -= dmg;
    this.events.push({ type: 'buildingHit', building: b, damage: dmg, by });
    if (b.hp <= 0) {
      b.hp = 0;
      const l = CAMP_BUILDINGS[b.type].loot;
      const m = this.lootMult * (1 + (by.def.lootBonus ?? 0)); // Otter Scavengers dig out extra
      const gained = l ? { coins: Math.round(l.coins * m), glowsap: Math.round(l.glowsap * m) } : { coins: 0, glowsap: 0 };
      this.loot.coins += gained.coins;
      this.loot.glowsap += gained.glowsap;
      this.events.push({ type: 'destroyed', building: b, loot: gained });
      if (CAMP_BUILDINGS[b.type].burst) this.swarm(b);
    }
  }

  /** Hornet Hive: its fall releases a swarm that stings every troop nearby, flyers included. */
  private swarm(b: CampBuilding): void {
    const burst = CAMP_BUILDINGS[b.type].burst!;
    const c = buildingCenter(b);
    const stung = this.troops.filter((t) => t.alive && !t.tunneling && Math.hypot(t.pos.x - c.x, t.pos.y - c.y) <= burst.radius + buildingRadius(b));
    this.events.push({ type: 'swarm', building: b, radius: burst.radius + buildingRadius(b), stung });
    for (const t of stung) this.hurtTroop(t, burst.damage * this.dmgMult, c);
  }

  private updateDefenses(dt: number): void {
    for (const b of this.standing) {
      const def = CAMP_BUILDINGS[b.type].defense;
      if (!def) continue;
      let cd = (this.cooldowns.get(b.uid) ?? 0) - dt;
      if (cd > 0) {
        this.cooldowns.set(b.uid, cd);
        continue;
      }
      const c = buildingCenter(b);
      let best: Troop | null = null;
      let bestD = def.range;
      for (const t of this.troops) {
        if (!t.alive || t.tunneling || (t.def.flying && !def.hitsAir)) continue;
        const d = Math.hypot(t.pos.x - c.x, t.pos.y - c.y);
        if (d <= bestD) {
          bestD = d;
          best = t;
        }
      }
      if (!best) {
        this.cooldowns.set(b.uid, 0);
        continue;
      }
      cd = 1 / def.rate;
      this.cooldowns.set(b.uid, cd);
      const dmg = def.damage * this.dmgMult;
      this.events.push({ type: 'shot', from: c, to: { ...best.pos }, splash: def.splash ?? 0, building: b });
      if (def.splash) {
        const at = { ...best.pos };
        for (const t of this.troops) {
          if (!t.alive || t.def.flying || t.tunneling) continue;
          if (Math.hypot(t.pos.x - at.x, t.pos.y - at.y) <= def.splash) this.hurtTroop(t, dmg, c);
        }
      } else {
        this.hurtTroop(best, dmg, c);
      }
    }
  }

  /** Mire Shamans pulse healing into damaged camp buildings (walls included) around them, themselves too. */
  private updateMenders(dt: number): void {
    for (const b of this.camp.buildings) {
      const m = CAMP_BUILDINGS[b.type].mend;
      if (!m || b.hp <= 0) continue;
      const cd = (this.cooldowns.get(b.uid) ?? m.interval) - dt;
      if (cd > 0) {
        this.cooldowns.set(b.uid, cd);
        continue;
      }
      this.cooldowns.set(b.uid, m.interval);
      const c = buildingCenter(b);
      const healed: CampBuilding[] = [];
      for (const o of this.camp.buildings) {
        if (o.hp <= 0 || o.hp >= o.maxHp) continue;
        const oc = buildingCenter(o);
        if (Math.hypot(oc.x - c.x, oc.y - c.y) > m.range) continue;
        o.hp = Math.min(o.maxHp, o.hp + m.amount * this.dmgMult);
        healed.push(o);
      }
      if (healed.length) this.events.push({ type: 'mend', from: b, healed });
    }
  }

  private hurtTroop(t: Troop, dmg: number, from: Vec2): void {
    t.hp -= dmg;
    this.events.push({ type: 'troopHit', troop: t, damage: dmg, from });
    if (t.hp <= 0 && t.alive) {
      t.alive = false;
      this.events.push({ type: 'troopDown', troop: t });
    }
  }

  /** Stop early (player pressed End). */
  finish(): void {
    if (this.ended) return;
    this.ended = true;
    this.events.push({ type: 'end', stars: this.stars });
  }

  private checkEnd(): void {
    const armyLeft = Object.values(this.army).reduce((a, b) => a + b, 0);
    const alive = this.troops.some((t) => t.alive);
    if (this.standing.length === 0 || this.time >= RAID_TIME || (!alive && armyLeft === 0 && this.troops.length > 0)) this.finish();
  }

  /** Troops left alive or never deployed come home; the fallen are lost. */
  survivingArmy(): Record<string, number> {
    const out: Record<string, number> = { ...this.army };
    for (const t of this.troops) if (t.alive) out[t.def.id] = (out[t.def.id] ?? 0) + 1;
    return out;
  }
}
