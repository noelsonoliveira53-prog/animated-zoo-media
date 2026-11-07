import { describe, expect, it } from 'vitest';
import { BattleSim } from '../src/systems/BattleSim';
import { ENEMIES } from '../src/data/enemies';
import type { LevelDef } from '../src/data/types';

const straight: LevelDef = {
  id: 't2',
  name: 'Test',
  blurb: '',
  mapPos: { x: 0, y: 0 },
  startCoins: 1000,
  lives: 20,
  theme: { grass: 0, grassDark: 0, road: 0, roadEdge: 0 },
  paths: [[{ x: 0, y: 100 }, { x: 800, y: 100 }]],
  slots: [{ x: 300, y: 170 }],
  waves: [{ groups: [{ enemy: 'mudling', count: 1, interval: 1 }] }],
};

function run(sim: BattleSim, seconds: number) {
  for (let i = 0; i < seconds * 60; i++) sim.update(1 / 60);
}

describe('Burrow Den soldiers', () => {
  it('spawns a squad with a rally point on the road', () => {
    const sim = new BattleSim(straight);
    const t = sim.build(0, 'burrow')!;
    expect(sim.soldiers.length).toBe(2);
    expect(t.rally).toEqual({ x: 300, y: 100 });
    sim.upgrade(0);
    expect(sim.soldiers.length).toBe(3);
  });

  it('blocks an enemy so it stops advancing', () => {
    const sim = new BattleSim(straight);
    sim.build(0, 'burrow');
    sim.status = 'running';
    run(sim, 1); // soldiers walk to the road
    const e = sim.spawn('shellback', 0, 250);
    run(sim, 2);
    expect(e.blockedBy).not.toBe(0);
    const held = e.dist;
    run(sim, 1);
    expect(e.dist).toBeCloseTo(held, 5);
  });

  it('kills weak enemies by itself and frees the road', () => {
    const sim = new BattleSim(straight);
    sim.build(0, 'burrow');
    sim.status = 'running';
    run(sim, 1);
    const e = sim.spawn('mudling', 0, 260);
    run(sim, 20);
    expect(e.alive).toBe(false);
    expect(sim.lives).toBe(20);
  });

  it('releases enemies when sold', () => {
    const sim = new BattleSim(straight);
    sim.build(0, 'burrow');
    sim.status = 'running';
    run(sim, 1);
    const e = sim.spawn('shellback', 0, 250);
    run(sim, 2);
    sim.sell(0);
    expect(sim.soldiers.length).toBe(0);
    run(sim, 0.2);
    expect(e.blockedBy).toBe(0);
  });

  it('soldiers die and respawn', () => {
    const sim = new BattleSim(straight);
    sim.build(0, 'burrow');
    sim.status = 'running';
    run(sim, 1);
    const s = sim.soldiers[0];
    s.hp = 1;
    sim.spawn('shellback', 0, 280);
    run(sim, 3);
    expect(sim.soldiers.some((x) => !x.alive)).toBe(true);
    run(sim, 10);
  });
});

describe('Boulder Bellows artillery', () => {
  it('splash hits a whole clump', () => {
    const sim = new BattleSim(straight);
    sim.build(0, 'boulder');
    sim.status = 'running';
    const group = [sim.spawn('shellback', 0, 300), sim.spawn('shellback', 0, 310), sim.spawn('shellback', 0, 320)];
    for (const e of group) e.def = { ...e.def, speed: 0 };
    run(sim, 1.5);
    for (const e of group) expect(e.hp).toBeLessThan(e.maxHp);
  });

  it('cannot target flying enemies', () => {
    ENEMIES.__testfly = { ...ENEMIES.mudling, id: '__testfly', flying: true };
    const sim = new BattleSim(straight);
    sim.build(0, 'boulder');
    sim.status = 'running';
    const e = sim.spawn('__testfly', 0, 300);
    e.def = { ...e.def, speed: 0 };
    run(sim, 3);
    expect(e.hp).toBe(e.maxHp);
    delete ENEMIES.__testfly;
  });
});
