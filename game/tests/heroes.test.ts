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
  it('defines at least three heroes, all listed in HERO_ORDER', () => {
    expect(HERO_ORDER.length).toBeGreaterThanOrEqual(3);
    expect(new Set(HERO_ORDER).size).toBe(Object.keys(HEROES).length);
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

describe('Wren', () => {
  it("Scholar's Eye pays extra coins only for kills near her", () => {
    const lvl2 = { id: 'w', name: 'W', blurb: '', mapPos: { x: 0, y: 0 }, startCoins: 0, lives: 20, theme: { grass: 0, grassDark: 0, road: 0, roadEdge: 0 },
      paths: [[{ x: 0, y: 300 }, { x: 2000, y: 300 }]], slots: [], waves: [{ groups: [{ enemy: 'mudling', count: 1, interval: 1 }] }] } as LevelDef;
    const sim = new BattleSim(lvl2, 'wren');
    sim.status = 'running';
    sim.hero!.pos = { x: 400, y: 300 };
    const near = sim.spawn('mudling', 0, 420);
    const far = sim.spawn('mudling', 0, 1500);
    const c0 = sim.coins;
    (sim as any).applyDamage(near, 9999);
    const nearPay = sim.coins - c0;
    const c1 = sim.coins;
    (sim as any).applyDamage(far, 9999);
    const farPay = sim.coins - c1;
    expect(nearPay).toBeGreaterThan(farPay);
    expect(nearPay).toBe(Math.round(farPay * (1 + (HEROES.wren.passive as { bonus: number }).bonus)));
  });
});

describe('Bramble shield toss', () => {
  it('throws at flyers in range on its own timer, and never at walkers', () => {
    const lvl3 = { id: 'b', name: 'B', blurb: '', mapPos: { x: 0, y: 0 }, startCoins: 0, lives: 20, theme: { grass: 0, grassDark: 0, road: 0, roadEdge: 0 },
      paths: [[{ x: 0, y: 300 }, { x: 2000, y: 300 }]], slots: [], waves: [{ groups: [{ enemy: 'mudling', count: 1, interval: 1 }] }] } as LevelDef;
    const sim = new BattleSim(lvl3, 'bramble');
    sim.status = 'running';
    sim.hero!.pos = { x: 400, y: 300 };
    const fly = sim.spawn('gloomwing', 0, 480);
    fly.def = { ...fly.def, speed: 0 };
    for (let i = 0; i < 60; i++) sim.update(1 / 60);
    expect(fly.hp).toBeLessThan(fly.maxHp);
    expect(sim.hero!.tossCd).toBeGreaterThan(0);
    const sim2 = new BattleSim(lvl3, 'fen');
    expect(HEROES.fen.toss).toBeUndefined();
    expect(sim2.hero!.tossCd).toBe(0);
  });
});

describe('Bramble bulwark', () => {
  it('holds more enemies at once as he levels up', () => {
    const lvl4 = { id: 'k', name: 'K', blurb: '', mapPos: { x: 0, y: 0 }, startCoins: 0, lives: 20, theme: { grass: 0, grassDark: 0, road: 0, roadEdge: 0 },
      paths: [[{ x: 0, y: 300 }, { x: 2000, y: 300 }]], slots: [], waves: [{ groups: [{ enemy: 'mudling', count: 1, interval: 1 }] }] } as LevelDef;
    const sim = new BattleSim(lvl4, 'bramble');
    sim.status = 'running';
    const h = sim.hero!;
    expect(sim.heroHolds(h)).toBe(1);
    h.level = 3;
    expect(sim.heroHolds(h)).toBe(2);
    h.level = 5;
    expect(sim.heroHolds(h)).toBe(3);
    h.pos = { x: 400, y: 300 };
    h.dest = null;
    const foes = [0, 1, 2, 3].map((k) => sim.spawn('shellback', 0, 396 + k * 3));
    for (const f of foes) f.def = { ...f.def, speed: 0, attack: 0 };
    for (let i = 0; i < 30; i++) sim.update(1 / 60);
    expect(foes.filter((f) => f.blockedBy === h.uid).length).toBe(3);
    expect(HEROES.fen.bulwark).toBeUndefined();
  });
});

describe('Sorrel', () => {
  const lvl4 = { ...lvl, startCoins: 2000, slots: [{ x: 600, y: 370 }] } as LevelDef;
  it('Field Dressing heals soldiers near her (even mid-fight) but not far ones', () => {
    const sim = new BattleSim(lvl4, 'sorrel');
    sim.status = 'running';
    sim.build(0, 'burrow');
    run(sim, 0.5);
    const [a, b] = sim.soldiers;
    sim.hero!.pos = { ...a.pos };
    sim.hero!.dest = null as any;
    a.hp = 10;
    b.hp = 10;
    b.pos = { x: a.pos.x + 600, y: a.pos.y }; // far away
    b.home = { ...b.pos };
    const mend = HEROES.sorrel.passive as { regen: number };
    (sim as any).updateSoldiers(1);
    expect(a.hp).toBeGreaterThanOrEqual(10 + mend.regen);
    expect(b.hp).toBeLessThan(10 + mend.regen);
  });
  it('Second Wind restores health to soldiers in reach and to Sorrel', () => {
    const sim = new BattleSim(lvl4, 'sorrel');
    sim.status = 'running';
    sim.build(0, 'burrow');
    run(sim, 0.5);
    const s = sim.soldiers[0];
    sim.hero!.pos = { ...s.pos };
    s.hp = 5;
    sim.hero!.hp = 20;
    expect(sim.useHeroSkill()).toBe(true);
    const heal = HEROES.sorrel.active.heal!;
    expect(s.hp).toBe(Math.min(s.maxHp, 5 + heal));
    expect(sim.hero!.hp).toBe(Math.min(sim.hero!.maxHp, 20 + heal));
    const ev = sim.drainEvents().find((e) => e.type === 'heroSkill') as any;
    expect(ev.healed.length).toBeGreaterThanOrEqual(2);
  });
});
