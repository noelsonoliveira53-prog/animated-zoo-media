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
  attackCd: number;
}

export type RaidEvent =
  | { type: 'deploy'; troop: Troop }
  | { type: 'troopHit'; troop: Troop; damage: number; from: Vec2 }
  | { type: 'troopDown'; troop: Troop }
  | { type: 'buildingHit'; building: CampBuilding; damage: number; by: Troop }
  | { type: 'destroyed'; building: CampBuilding; loot: { coins: number; glowsap: number } }
  | { type: 'shot'; from: Vec2; to: Vec2; splash: number; building: CampBuilding }
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

  /** Buildings that count toward destruction (all of them). */
  get standing(): CampBuilding[] {
    return this.camp.buildings.filter((b) => b.hp > 0);
  }

  get destruction(): number {
    const total = this.camp.buildings.length;
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
    const t: Troop = { uid: this.nextUid++, def, pos: { ...p }, hp: def.hp, maxHp: def.hp, alive: true, targetUid: 0, attackCd: 0.3 };
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
    this.updateDefenses(dt);
    this.checkEnd();
  }

  private pickTarget(t: Troop): CampBuilding | undefined {
    const standing = this.standing;
    let pool = standing;
    if (t.def.prefers === 'defense') {
      const defs = standing.filter((b) => CAMP_BUILDINGS[b.type].defense);
      if (defs.length) pool = defs;
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
    const c = buildingCenter(target);
    const reach = buildingRadius(target) + t.def.range;
    const d = Math.hypot(c.x - t.pos.x, c.y - t.pos.y);
    if (d > reach) {
      const step = Math.min(t.def.speed * dt, d - reach + 1);
      t.pos.x += ((c.x - t.pos.x) / d) * step;
      t.pos.y += ((c.y - t.pos.y) / d) * step;
      return;
    }
    t.attackCd -= dt;
    if (t.attackCd > 0) return;
    t.attackCd = 1 / t.def.rate;
    if (t.def.splash) {
      for (const b of this.standing) {
        const bc = buildingCenter(b);
        if (b === target || Math.hypot(bc.x - c.x, bc.y - c.y) <= t.def.splash + buildingRadius(b)) this.hurtBuilding(b, t.def.damage, t);
      }
    } else {
      this.hurtBuilding(target, t.def.damage, t);
    }
  }

  private hurtBuilding(b: CampBuilding, dmg: number, by: Troop): void {
    if (b.hp <= 0) return;
    b.hp -= dmg;
    this.events.push({ type: 'buildingHit', building: b, damage: dmg, by });
    if (b.hp <= 0) {
      b.hp = 0;
      const l = CAMP_BUILDINGS[b.type].loot;
      const gained = l ? { coins: Math.round(l.coins * this.lootMult), glowsap: Math.round(l.glowsap * this.lootMult) } : { coins: 0, glowsap: 0 };
      this.loot.coins += gained.coins;
      this.loot.glowsap += gained.glowsap;
      this.events.push({ type: 'destroyed', building: b, loot: gained });
    }
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
        if (!t.alive || (t.def.flying && !def.hitsAir)) continue;
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
          if (!t.alive || t.def.flying) continue;
          if (Math.hypot(t.pos.x - at.x, t.pos.y - at.y) <= def.splash) this.hurtTroop(t, dmg, c);
        }
      } else {
        this.hurtTroop(best, dmg, c);
      }
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
