import { describe, expect, it } from 'vitest';
import { BattleSim } from '../src/systems/BattleSim';
import { TOWERS, TOWER_ORDER, sellValue } from '../src/data/towers';
import type { LevelDef } from '../src/data/types';

const lvl: LevelDef = {
  id: 'sp',
  name: 'Test',
  blurb: '',
  mapPos: { x: 0, y: 0 },
  startCoins: 5000,
  lives: 20,
  theme: { grass: 0, grassDark: 0, road: 0, roadEdge: 0 },
  paths: [[{ x: 0, y: 300 }, { x: 1200, y: 300 }]],
  slots: [{ x: 600, y: 370 }],
  waves: [{ groups: [{ enemy: 'mudling', count: 1, interval: 1 }] }],
};
const run = (sim: BattleSim, s: number) => {
  for (let i = 0; i < s * 60; i++) sim.update(1 / 60);
};
function maxed(id: string): BattleSim {
  const sim = new BattleSim(lvl);
  sim.build(0, id);
  sim.upgrade(0);
  sim.upgrade(0);
  return sim;
}

describe('tower specializations', () => {
  it('every tower has two distinct branches', () => {
    for (const id of TOWER_ORDER) {
      const d = TOWERS[id];
      expect(d.specs.length).toBe(2);
      expect(d.specs[0].id).not.toBe(d.specs[1].id);
    }
  });

  it('is only available at the top tier, once', () => {
    const sim = new BattleSim(lvl);
    sim.build(0, 'thornbow');
    expect(sim.specialize(0, 0)).toBe(false);
    sim.upgrade(0);
    sim.upgrade(0);
    const before = sim.coins;
    expect(sim.specialize(0, 0)).toBe(true);
    expect(sim.coins).toBe(before - TOWERS.thornbow.specs[0].stats.cost);
    expect(sim.specialize(0, 1)).toBe(false);
    expect(sim.upgradeCost(sim.towers[0]!)).toBeNull();
    expect(sim.stats(sim.towers[0]!).range).toBe(270);
  });

  it('refunds include the specialization', () => {
    expect(sellValue(TOWERS.thornbow, 2, 'hawkeye')).toBe(Math.floor((70 + 90 + 140 + 220) * 0.6));
  });

  it('Bramble Volley hits three targets per volley', () => {
    const sim = maxed('thornbow');
    sim.specialize(0, 1);
    sim.status = 'running';
    for (let i = 0; i < 4; i++) sim.spawn('shellback', 0, 520 + i * 30).def = { ...sim.enemies[i].def, speed: 0 };
    sim.drainEvents();
    sim.update(1 / 60);
    expect(sim.drainEvents().filter((e) => e.type === 'shoot').length).toBe(3);
  });

  it('Hawkeye pierces armor', () => {
    const plain = maxed('thornbow');
    const sniper = maxed('thornbow');
    sniper.specialize(0, 0);
    for (const sim of [plain, sniper]) {
      sim.status = 'running';
      const e = sim.spawn('shellback', 0, 600);
      e.def = { ...e.def, speed: 0, hp: 9999 };
      e.hp = e.maxHp = 9999;
    }
    run(plain, 0.5);
    run(sniper, 0.5);
    const firstHit = (sim: BattleSim) => 9999 - sim.enemies[0].hp;
    // 110 dmg vs 60% armor with 70% pierced -> 110 * (1 - 0.18) ≈ 90 per shot
    expect(firstHit(sniper)).toBeGreaterThanOrEqual(90);
    expect(firstHit(sniper)).toBeGreaterThan(firstHit(plain));
  });

  it('Stormcall lightning chains to nearby enemies', () => {
    const sim = maxed('glimmer');
    sim.specialize(0, 0);
    sim.status = 'running';
    const es = [0, 1, 2, 3].map((i) => {
      const e = sim.spawn('shellback', 0, 560 + i * 40);
      e.def = { ...e.def, speed: 0 };
      return e;
    });
    run(sim, 1);
    expect(es.filter((e) => e.hp < e.maxHp).length).toBeGreaterThanOrEqual(3);
  });

  it('Frostbloom slows a crowd', () => {
    const sim = maxed('glimmer');
    sim.specialize(0, 1);
    sim.status = 'running';
    const a = sim.spawn('shellback', 0, 590);
    const b = sim.spawn('shellback', 0, 610);
    run(sim, 1);
    expect(a.slowFactor).toBeLessThan(1);
    expect(b.slowFactor).toBeLessThan(1);
  });

  it('Thornback Raiders field four soldiers', () => {
    const sim = maxed('burrow');
    expect(sim.soldiers.length).toBe(3);
    sim.specialize(0, 1);
    expect(sim.soldiers.length).toBe(4);
    expect(sim.soldiers[0].stats.damage).toBe(24);
  });
});
