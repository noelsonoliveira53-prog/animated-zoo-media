import { describe, expect, it } from 'vitest';
import { BattleSim } from '../src/systems/BattleSim';
import { HEROES, HERO_ORDER, levelForXp, heroLevelMult } from '../src/data/heroes';
import type { LevelDef } from '../src/data/types';

const lvl: LevelDef = {
  id: 'h',
  name: 'Test',
  blurb: '',
  mapPos: { x: 0, y: 0 },
  startCoins: 500,
  lives: 20,
  theme: { grass: 0, grassDark: 0, road: 0, roadEdge: 0 },
  paths: [[{ x: 0, y: 300 }, { x: 1200, y: 300 }]],
  slots: [{ x: 600, y: 370 }],
  waves: [{ groups: [{ enemy: 'mudling', count: 1, interval: 1 }] }],
};
const run = (sim: BattleSim, s: number) => {
  for (let i = 0; i < s * 60; i++) sim.update(1 / 60);
};

describe('heroes', () => {
  it('defines three heroes', () => {
    expect(HERO_ORDER.length).toBe(3);
    for (const id of HERO_ORDER) expect(HEROES[id]).toBeDefined();
  });

  it('levels from xp thresholds', () => {
    expect(levelForXp(0)).toBe(1);
    expect(levelForXp(40)).toBe(2);
    expect(levelForXp(10000)).toBe(6);
    expect(heroLevelMult(3)).toBeCloseTo(1.24);
  });

  it('spawns near the gate and walks to a move order', () => {
    const sim = new BattleSim(lvl, 'fen');
    expect(sim.hero).not.toBeNull();
    expect(sim.hero!.pos.x).toBeCloseTo(940);
    sim.moveHero({ x: 800, y: 200 });
    run(sim, 3);
    expect(sim.hero!.pos.x).toBeCloseTo(800, 0);
    expect(sim.hero!.pos.y).toBeCloseTo(200, 0);
  });

  it('melee hero blocks and kills an enemy', () => {
    const sim = new BattleSim(lvl, 'bramble');
    sim.status = 'running';
    const e = sim.spawn('shellback', 0, 880);
    run(sim, 1);
    expect(e.blockedBy).toBe(sim.hero!.uid);
    run(sim, 20);
    expect(e.alive).toBe(false);
    expect(sim.lives).toBe(20);
    expect(sim.hero!.xp).toBeGreaterThan(0);
  });

  it('ranged hero shoots enemies in range', () => {
    const sim = new BattleSim(lvl, 'fen');
    sim.status = 'running';
    const e = sim.spawn('gloomwing', 0, 850);
    e.def = { ...e.def, speed: 0 };
    run(sim, 3);
    expect(e.alive).toBe(false);
  });

  it('active skill damages nearby enemies and goes on cooldown', () => {
    const sim = new BattleSim(lvl, 'bramble');
    sim.status = 'running';
    const a = sim.spawn('shellback', 0, 920);
    const b = sim.spawn('shellback', 0, 960);
    expect(sim.useHeroSkill()).toBe(true);
    expect(a.hp).toBeLessThan(a.maxHp);
    expect(b.hp).toBeLessThan(b.maxHp);
    expect(b.slowFactor).toBeLessThan(1);
    expect(sim.useHeroSkill()).toBe(false);
    run(sim, 17);
    expect(sim.hero!.skillCd).toBe(0);
  });

  it('hero dies and respawns', () => {
    const sim = new BattleSim(lvl, 'bramble');
    sim.status = 'running';
    sim.hero!.hp = 1;
    sim.spawn('bogbrute', 0, 900);
    run(sim, 4);
    expect(sim.hero!.alive).toBe(false);
    run(sim, 15);
    expect(sim.hero!.alive).toBe(true);
    expect(sim.hero!.hp).toBe(sim.hero!.maxHp);
  });

  it('Ember speeds up nearby towers', () => {
    const sim = new BattleSim(lvl, 'ember');
    const t = sim.build(0, 'thornbow')!;
    sim.hero!.pos = { x: 600, y: 330 };
    expect(sim.towerHaste(t)).toBeCloseTo(1 + (HEROES.ember.passive as { bonus: number }).bonus);
    sim.hero!.pos = { x: 100, y: 330 };
    expect(sim.towerHaste(t)).toBe(1);
  });
});
