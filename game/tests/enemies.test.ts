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

describe('frost enemies', () => {
  it('Rime Wraiths freeze nearby shooting towers but not soldier dens', () => {
    const l2: LevelDef = { ...lvl, startCoins: 1000, slots: [{ x: 300, y: 160 }, { x: 340, y: 40 }] };
    const sim = new BattleSim(l2);
    const shooter = sim.build(0, 'thornbow')!;
    const den = sim.build(1, 'burrow')!;
    sim.status = 'running';
    const w = sim.spawn('rimewraith', 0, 300);
    w.def = { ...w.def, speed: 0 };
    for (let i = 0; i < 60 * 3.5; i++) sim.update(1 / 60);
    expect(shooter.frozen).toBeGreaterThan(0);
    expect(den.frozen).toBe(0);
    sim.drainEvents();
    sim.update(1 / 60);
    expect(sim.drainEvents().some((e) => e.type === 'shoot')).toBe(false);
  });
});

describe('burrowers', () => {
  it('Cinder Moles dive (untargetable, faster) and resurface on a cycle', () => {
    const l2: LevelDef = { ...lvl, startCoins: 1000, slots: [{ x: 600, y: 160 }] };
    const sim = new BattleSim(l2);
    sim.build(0, 'glimmer');
    sim.status = 'running';
    const m = sim.spawn('cindermole', 0, 100);
    for (let i = 0; i < 60 * 4.05; i++) sim.update(1 / 60);
    expect(m.underground).toBe(true);
    expect(m.speedMult).toBeCloseTo(1.5);
    // While underground, towers find no target.
    m.pos = { x: 600, y: 100 };
    sim.drainEvents();
    for (const t of sim.towers) if (t) t.cooldown = 0;
    sim.update(1 / 60);
    expect(sim.drainEvents().some((e) => e.type === 'shoot')).toBe(false);
    for (let i = 0; i < 60 * 2.3; i++) sim.update(1 / 60);
    expect(m.underground).toBe(false);
    expect(m.speedMult).toBe(1);
  });
  it('diving frees the mole from blockers', () => {
    const l2: LevelDef = { ...lvl, startCoins: 1000, slots: [{ x: 400, y: 170 }] };
    const sim = new BattleSim(l2);
    sim.build(0, 'burrow');
    sim.status = 'running';
    for (let i = 0; i < 60; i++) sim.update(1 / 60);
    const m = sim.spawn('cindermole', 0, 360);
    m.burrowCd = 1.5;
    for (let i = 0; i < 60; i++) sim.update(1 / 60);
    expect(m.blockedBy).not.toBe(0);
    for (let i = 0; i < 40; i++) sim.update(1 / 60);
    expect(m.underground).toBe(true);
    expect(m.blockedBy).toBe(0);
  });
});

describe('freeze immunity', () => {
  it('a pack of wraiths cannot keep a tower frozen forever', () => {
    const l2: LevelDef = { ...lvl, startCoins: 1000, slots: [{ x: 300, y: 160 }] };
    const sim = new BattleSim(l2);
    const t = sim.build(0, 'thornbow')!;
    sim.status = 'running';
    for (let i = 0; i < 4; i++) {
      const w = sim.spawn('rimewraith', 0, 290 + i * 8);
      w.def = { ...w.def, speed: 0 };
      w.chillCd = 0.5 + i * 1.2; // staggered breaths
    }
    let thawedFrames = 0;
    for (let i = 0; i < 60 * 12; i++) {
      sim.update(1 / 60);
      if (t.frozen === 0) thawedFrames++;
    }
    expect(thawedFrames).toBeGreaterThan(60 * 4);
  });
});

describe('spawners', () => {
  it('Ash Hives release imps on a timer, up to their limit', () => {
    const sim = new BattleSim(lvl);
    sim.status = 'running';
    const h = sim.spawn('ashhive', 0, 100);
    h.def = { ...h.def, speed: 0 };
    for (let i = 0; i < 60 * 60; i++) sim.update(1 / 60);
    const imps = sim.enemies.filter((e) => e.def.id === 'emberimp').length + 0;
    expect(h.spawned).toBe(6);
    expect(imps).toBeLessThanOrEqual(6);
  });
});

describe('duskcap enemies', () => {
  it('Veilstalkers are only targeted by towers once inside the veil range', () => {
    // Tower at x=400 (60px above the road), range well beyond the veil.
    const l2: LevelDef = { ...lvl, startCoins: 1000, slots: [{ x: 400, y: 40 }] };
    const sim = new BattleSim(l2);
    const t = sim.build(0, 'glimmer')!;
    sim.status = 'running';
    const v = sim.spawn('veilstalker', 0, 220);
    v.def = { ...v.def, speed: 0 };
    const veil = ENEMIES.veilstalker.veil!;
    expect(Math.hypot(v.pos.x - t.pos.x, v.pos.y - t.pos.y)).toBeGreaterThan(veil);
    for (let i = 0; i < 120; i++) sim.update(1 / 60);
    expect(v.hp).toBe(v.maxHp); // in tower range, but hidden
    v.dist = 400;
    v.pos = { x: 400, y: 100 };
    for (let i = 0; i < 120; i++) sim.update(1 / 60);
    expect(v.hp).toBeLessThan(v.maxHp);
  });
  it('Rootragers enrage below half health and speed up', () => {
    const sim = new BattleSim({ ...lvl });
    sim.status = 'running';
    const r = sim.spawn('rootrager', 0, 100);
    sim.update(1 / 60);
    const d0 = r.dist;
    sim.update(0.5);
    const slow = r.dist - d0;
    (sim as any).applyDamage(r, r.maxHp * 0.6);
    sim.update(1 / 60);
    expect(r.enraged).toBe(true);
    expect(sim.events.some((e) => e.type === 'enrage') || r.speedMult === ENEMIES.rootrager.enrage!.speedMult).toBe(true);
    const d1 = r.dist;
    sim.update(0.5);
    expect(r.dist - d1).toBeGreaterThan(slow * 1.8);
  });
});

describe('puffcap spores', () => {
  it('a dying Puffcap hastens nearby allies (not bosses) for a few seconds', () => {
    const sim = new BattleSim({ ...lvl });
    sim.status = 'running';
    const p = sim.spawn('puffcap', 0, 300);
    const near = sim.spawn('mudling', 0, 340);
    const far = sim.spawn('mudling', 0, 700);
    const boss = sim.spawn('murkmaw', 0, 320);
    (sim as any).applyDamage(p, 9999);
    const sb = ENEMIES.puffcap.sporeBurst!;
    expect(near.hasteMult).toBe(sb.speedMult);
    expect(far.hasteMult).toBe(1);
    expect(boss.hasteMult).toBe(1);
    const d0 = near.dist;
    sim.update(0.5);
    const hasted = near.dist - d0;
    for (let i = 0; i < 60 * sb.duration; i++) sim.update(1 / 60);
    expect(near.hasteMult).toBe(1);
    const d1 = near.dist;
    sim.update(0.5);
    expect(hasted).toBeGreaterThan((near.dist - d1) * 1.4);
  });
});

describe('shoal enemies', () => {
  it('Barnaclad armor chips away with every hit, down to zero', () => {
    const sim = new BattleSim({ ...lvl });
    sim.status = 'running';
    const b = sim.spawn('barnaclad', 0, 100);
    expect(b.armor).toBe(ENEMIES.barnaclad.armor);
    for (let i = 0; i < 5; i++) (sim as any).applyDamage(b, 1);
    expect(b.armor).toBeCloseTo(ENEMIES.barnaclad.armor - 5 * ENEMIES.barnaclad.brittle!);
    for (let i = 0; i < 40; i++) (sim as any).applyDamage(b, 1);
    expect(b.armor).toBe(0);
    expect(ENEMIES.mudling.brittle).toBeUndefined();
  });
  it('Gullwings land on a cycle, and only then can ground-only towers hit them', () => {
    const l2: LevelDef = { ...lvl, startCoins: 1000, slots: [{ x: 300, y: 40 }] };
    const sim = new BattleSim(l2);
    const t = sim.build(0, 'boulder')!; // artillery: cannot hit air
    expect(t.def.hitsAir).toBeFalsy();
    sim.status = 'running';
    const g = sim.spawn('gullwing', 0, 300);
    g.def = { ...g.def, speed: 0 };
    expect(sim.airborne(g)).toBe(true);
    const sw = ENEMIES.gullwing.swoop!;
    for (let i = 0; i < 60 * (sw.interval - 0.2); i++) sim.update(1 / 60);
    expect(g.hp).toBe(g.maxHp); // still flying: artillery ignored it
    for (let i = 0; i < 60 * 0.4; i++) sim.update(1 / 60);
    expect(g.landed).toBe(true);
    expect(sim.airborne(g)).toBe(false);
    for (let i = 0; i < 60 * (sw.duration - 0.3); i++) sim.update(1 / 60);
    expect(g.hp).toBeLessThan(g.maxHp);
    for (let i = 0; i < 60 * 0.6; i++) sim.update(1 / 60);
    expect(g.landed).toBe(false);
  });
});

describe('reefwarden', () => {
  it('coats nearby allies (not itself or bosses) in coral shields on a timer', () => {
    const sim = new BattleSim({ ...lvl });
    sim.status = 'running';
    const r = sim.spawn('reefwarden', 0, 300);
    const near = sim.spawn('mudling', 0, 360);
    const far = sim.spawn('mudling', 0, 800);
    const boss = sim.spawn('murkmaw', 0, 320);
    for (const e of [r, near, far, boss]) e.def = { ...e.def, speed: 0 };
    for (let i = 0; i < 60 * ENEMIES.reefwarden.shieldAura!.interval; i++) sim.update(1 / 60);
    expect(near.shield).toBeGreaterThan(0);
    expect(far.shield).toBe(0);
    expect(r.shield).toBe(0);
    expect(boss.shield).toBe(0);
  });
});
