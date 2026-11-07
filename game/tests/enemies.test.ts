import { describe, expect, it } from 'vitest';
import { BattleSim } from '../src/systems/BattleSim';
import { ENEMIES } from '../src/data/enemies';
import type { LevelDef } from '../src/data/types';

const lvl: LevelDef = {
  id: 'e',
  name: 'Test',
  blurb: '',
  mapPos: { x: 0, y: 0 },
  startCoins: 0,
  lives: 50,
  theme: { grass: 0, grassDark: 0, road: 0, roadEdge: 0 },
  paths: [[{ x: 0, y: 100 }, { x: 2000, y: 100 }]],
  slots: [],
  waves: [{ groups: [{ enemy: 'mudling', count: 1, interval: 1 }] }],
};

function hitAll(sim: BattleSim, dmg: number) {
  // Use private applyDamage through a cast for focused unit tests.
  for (const e of [...sim.enemies]) (sim as any).applyDamage(e, dmg);
}

describe('enemy roster', () => {
  it('has at least 12 enemy types with sane stats', () => {
    const all = Object.values(ENEMIES);
    expect(all.length).toBeGreaterThanOrEqual(12);
    for (const e of all) {
      expect(e.hp).toBeGreaterThan(0);
      expect(e.armor).toBeLessThanOrEqual(0.9);
      expect(e.magicResist).toBeLessThanOrEqual(0.9);
      if (e.splitInto) expect(ENEMIES[e.splitInto.enemy]).toBeDefined();
      for (const ph of e.phases ?? []) if (ph.summon) expect(ENEMIES[ph.summon.enemy]).toBeDefined();
    }
  });

  it('shields absorb damage before hp', () => {
    const sim = new BattleSim(lvl);
    const e = sim.spawn('reedguard', 0, 100);
    (sim as any).applyDamage(e, 50);
    expect(e.hp).toBe(e.maxHp);
    expect(e.shield).toBe(20);
    (sim as any).applyDamage(e, 30);
    expect(e.shield).toBe(0);
    expect(e.hp).toBe(e.maxHp - 10);
    expect(sim.drainEvents().some((ev) => ev.type === 'shieldBreak')).toBe(true);
  });

  it('splitters spawn children on death', () => {
    const sim = new BattleSim(lvl);
    sim.spawn('splotch', 0, 300);
    hitAll(sim, 1000);
    const alive = sim.enemies.filter((e) => e.alive);
    expect(alive.length).toBe(2);
    expect(alive.every((e) => e.def.id === 'mudling')).toBe(true);
  });

  it('healers restore nearby allies', () => {
    const sim = new BattleSim(lvl);
    sim.status = 'running';
    const healer = sim.spawn('bogmender', 0, 300);
    const buddy = sim.spawn('shellback', 0, 320);
    buddy.hp = 50;
    for (let i = 0; i < 60 * 3.2; i++) sim.update(1 / 60);
    expect(buddy.hp).toBeGreaterThan(50);
    expect(healer.alive).toBe(true);
  });

  it('boss phases trigger once, in order', () => {
    const sim = new BattleSim(lvl);
    const boss = sim.spawn('murkmaw', 0, 500);
    (sim as any).applyDamage(boss, boss.maxHp * 0.35); // -> 65%
    expect(boss.phase).toBe(1);
    expect(sim.enemies.filter((e) => e.def.id === 'mudling').length).toBe(6);
    (sim as any).applyDamage(boss, 1); // no re-trigger
    expect(boss.phase).toBe(1);
    (sim as any).applyDamage(boss, boss.maxHp * 0.3); // -> ~35%
    expect(boss.phase).toBe(2);
    expect(boss.shield).toBe(300);
    (sim as any).applyDamage(boss, 300 + boss.maxHp * 0.25); // break shield, -> ~10%
    expect(boss.phase).toBe(3);
    expect(boss.speedMult).toBeGreaterThan(1);
    const phases = sim.drainEvents().filter((ev) => ev.type === 'phase');
    expect(phases.length).toBe(3);
  });

  it('soldiers ignore flyers', () => {
    const l2: LevelDef = { ...lvl, startCoins: 500, slots: [{ x: 400, y: 160 }] };
    const sim = new BattleSim(l2);
    sim.build(0, 'burrow');
    sim.status = 'running';
    for (let i = 0; i < 60; i++) sim.update(1 / 60);
    const flyer = sim.spawn('gloomwing', 0, 350);
    for (let i = 0; i < 60; i++) sim.update(1 / 60);
    expect(flyer.blockedBy).toBe(0);
    expect(flyer.dist).toBeGreaterThan(400);
  });
});
