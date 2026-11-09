import { describe, expect, it } from 'vitest';
import { BattleSim } from '../src/systems/BattleSim';
import { SPELLS } from '../src/data/spells';
import type { LevelDef } from '../src/data/types';

const lvl: LevelDef = {
  id: 's',
  name: 'Test',
  blurb: '',
  mapPos: { x: 0, y: 0 },
  startCoins: 0,
  lives: 20,
  theme: { grass: 0, grassDark: 0, road: 0, roadEdge: 0 },
  paths: [[{ x: 0, y: 300 }, { x: 1200, y: 300 }]],
  slots: [],
  waves: [{ groups: [{ enemy: 'mudling', count: 1, interval: 1 }] }],
};
const run = (sim: BattleSim, s: number) => {
  for (let i = 0; i < s * 60; i++) sim.update(1 / 60);
};

describe('global spells', () => {
  it('Starfall hits ground and air after a delay, then goes on cooldown', () => {
    const sim = new BattleSim(lvl);
    sim.status = 'running';
    const a = sim.spawn('shellback', 0, 500);
    const b = sim.spawn('gloomwing', 0, 520);
    const far = sim.spawn('shellback', 0, 900);
    for (const e of [a, b, far]) e.def = { ...e.def, speed: 0 };
    expect(sim.castSpell('starfall', { x: 510, y: 300 })).toBe(true);
    expect(a.hp).toBe(a.maxHp); // not yet
    run(sim, 1.2);
    expect(a.hp).toBeLessThan(a.maxHp);
    expect(b.alive).toBe(false);
    expect(far.hp).toBe(far.maxHp);
    expect(sim.castSpell('starfall', { x: 510, y: 300 })).toBe(false);
    run(sim, SPELLS.starfall.cooldown);
    expect(sim.spellReady('starfall')).toBe(true);
  });

  it('Grove Call needs the road and summons temporary blockers', () => {
    const sim = new BattleSim(lvl);
    sim.status = 'running';
    expect(sim.castSpell('grovecall', { x: 600, y: 600 })).toBe(false); // far from road
    expect(sim.castSpell('grovecall', { x: 600, y: 320 })).toBe(true);
    expect(sim.soldiers.filter((s) => s.summoned).length).toBe(3);
    const e = sim.spawn('shellback', 0, 520);
    run(sim, 2);
    expect(e.blockedBy).not.toBe(0);
    run(sim, SPELLS.grovecall.duration! + 1);
    expect(sim.soldiers.length).toBe(0);
  });
});
