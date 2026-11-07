import { describe, expect, it } from 'vitest';
import { BattleSim } from '../src/systems/BattleSim';
import type { LevelDef } from '../src/data/types';

const tiny: LevelDef = {
  id: 't',
  name: 'Test',
  startCoins: 500,
  lives: 5,
  theme: { grass: 0, grassDark: 0, road: 0, roadEdge: 0 },
  paths: [[{ x: 0, y: 100 }, { x: 600, y: 100 }]],
  slots: [{ x: 300, y: 160 }, { x: 150, y: 40 }],
  waves: [{ groups: [{ enemy: 'mudling', count: 3, interval: 1 }] }, { groups: [{ enemy: 'mudling', count: 2, interval: 1 }] }],
};

describe('BattleSim', () => {
  it('builds, upgrades and sells towers with correct coins', () => {
    const sim = new BattleSim(tiny);
    expect(sim.build(0, 'thornbow')).not.toBeNull();
    expect(sim.coins).toBe(430);
    expect(sim.build(0, 'glimmer')).toBeNull(); // slot taken
    expect(sim.upgrade(0)).toBe(true);
    expect(sim.coins).toBe(340);
    expect(sim.sell(0)).toBe(true);
    expect(sim.coins).toBe(340 + Math.floor(160 * 0.6));
    expect(sim.towers[0]).toBeNull();
  });

  it('refuses to build without enough coins', () => {
    const sim = new BattleSim({ ...tiny, startCoins: 10 });
    expect(sim.build(0, 'thornbow')).toBeNull();
  });

  it('leaks enemies with no defense and ends in defeat', () => {
    const sim = new BattleSim({ ...tiny, lives: 2 });
    sim.callNextWave();
    for (let i = 0; i < 60 * 30 && sim.isActive(); i++) sim.update(1 / 60);
    expect(sim.status).toBe('defeat');
    expect(sim.lives).toBe(0);
  });

  it('wins with towers covering the path', () => {
    const sim = new BattleSim(tiny);
    sim.build(0, 'glimmer');
    sim.build(1, 'thornbow');
    sim.callNextWave();
    for (let i = 0; i < 60 * 120 && sim.isActive(); i++) sim.update(1 / 60);
    expect(sim.status).toBe('victory');
    expect(sim.lives).toBe(5);
  });

  it('awards an early-call bonus after the first wave', () => {
    const sim = new BattleSim(tiny);
    sim.callNextWave();
    const before = sim.coins;
    sim.callNextWave(); // immediately: full countdown left
    expect(sim.coins).toBeGreaterThan(before);
  });

  it('targets by mode', () => {
    const sim = new BattleSim(tiny);
    const t = sim.build(0, 'thornbow')!;
    const front = sim.spawn('mudling', 0, 320);
    const back = sim.spawn('shellback', 0, 250);
    sim.status = 'running';
    sim.update(1 / 60);
    const shots = sim.drainEvents().filter((e) => e.type === 'shoot');
    expect(shots.length).toBe(1);
    expect((shots[0] as any).projectile.targetUid).toBe(front.uid);
    sim.setTargetMode(0, 'strongest');
    t.cooldown = 0;
    sim.update(1 / 60);
    const shots2 = sim.drainEvents().filter((e) => e.type === 'shoot');
    expect((shots2[0] as any).projectile.targetUid).toBe(back.uid);
  });
});
