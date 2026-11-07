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

import { pageCount, pageItems } from '../src/ui/paging';

describe('field guide capacity', () => {
  it('enemies are paged 30 per page (6 × 5 grid) and every enemy lands on exactly one page', () => {
    const ids = Object.keys(ENEMIES);
    const pages = pageCount(ids.length, 30);
    const seen = Array.from({ length: pages }, (_, p) => pageItems(ids, p, 30)).flat();
    expect(seen).toEqual(ids);
    for (let p = 0; p < pages; p++) expect(pageItems(ids, p, 30).length).toBeLessThanOrEqual(30);
  });
});

describe('shardglass enemies', () => {
  it('Shardskippers blink ahead on a timer and slip free of blockers', () => {
    const sim = new BattleSim({ ...lvl });
    sim.status = 'running';
    const s = sim.spawn('shardskipper', 0, 100);
    s.def = { ...s.def, speed: 0 };
    s.blockedBy = 99;
    const bl = ENEMIES.shardskipper.blink!;
    for (let i = 0; i < 60 * bl.interval + 2; i++) sim.update(1 / 60);
    expect(s.dist).toBeCloseTo(100 + bl.distance, 0);
    expect(s.blockedBy).toBe(0);
  });
  it('Mirrorbacks take much less splash damage than a normal enemy', () => {
    const sim = new BattleSim({ ...lvl });
    sim.status = 'running';
    const m = sim.spawn('mirrorback', 0, 300);
    const n = sim.spawn('shellback', 0, 300);
    const p = { splash: 60, lastTargetPos: { ...m.pos }, damage: 100, damageType: 'magic', pierce: 0, hitsAir: false, color: 0 } as any;
    m.armor = 0;
    n.armor = 0;
    (sim as any).impact(p, null);
    const mLost = m.maxHp - m.hp;
    const nLost = n.maxHp - n.hp;
    expect(nLost).toBeGreaterThan(0);
    expect(mLost).toBeLessThan(nLost * 0.5);
  });
});

describe('glarefly', () => {
  it('dazzles nearby shooting towers when it dies (not soldier dens, not far towers)', () => {
    const l2: LevelDef = { ...lvl, startCoins: 2000, slots: [{ x: 300, y: 40 }, { x: 330, y: 160 }, { x: 900, y: 40 }] };
    const sim = new BattleSim(l2);
    const near = sim.build(0, 'thornbow')!;
    const den = sim.build(1, 'burrow')!;
    const far = sim.build(2, 'thornbow')!;
    sim.status = 'running';
    const g = sim.spawn('glarefly', 0, 300);
    (sim as any).applyDamage(g, 9999);
    expect(near.frozen).toBeGreaterThan(0);
    expect(den.frozen ?? 0).toBe(0);
    expect(far.frozen ?? 0).toBe(0);
  });
});

describe('Galecrest enemies', () => {
  it('Galehound (windborne) ignores every slow; others are slowed', () => {
    const sim = new BattleSim(lvl, null);
    sim.status = 'running';
    const hound = sim.spawn('galehound', 0, 400);
    const mud = sim.spawn('mudling', 0, 400);
    for (const e of [hound, mud]) sim.slow(e, 0.3, 2);
    expect(hound.slowFactor).toBe(1);
    expect(mud.slowFactor).toBe(0.3);
  });

  it('Cloudram regrows only after going unhit for its delay, and never above max', () => {
    const sim = new BattleSim(lvl, null);
    sim.status = 'running';
    const ram = sim.spawn('cloudram', 0, 400);
    ram.def = { ...ram.def, speed: 0 };
    (sim as any).applyDamage(ram, ram.maxHp / 2);
    const half = ram.hp;
    for (let i = 0; i < 60; i++) sim.update(1 / 60); // 1 s: still inside the delay
    expect(ram.hp).toBe(half);
    for (let i = 0; i < 120; i++) sim.update(1 / 60); // 2 more s: regrowing
    expect(ram.hp).toBeGreaterThan(half);
    expect(sim.regenerating(ram)).toBe(true);
    (sim as any).applyDamage(ram, 1); // a hit resets the timer
    expect(sim.regenerating(ram)).toBe(false);
    for (let i = 0; i < 60 * 30; i++) sim.update(1 / 60);
    expect(ram.hp).toBe(ram.maxHp);
  });
});

describe('Kitewing gust', () => {
  it('blows nearby free walkers ahead, but not held enemies, flyers or itself', () => {
    const sim = new BattleSim(lvl, null);
    sim.status = 'running';
    const kite = sim.spawn('kitewing', 0, 400);
    const free = sim.spawn('mudling', 0, 420);
    const held = sim.spawn('mudling', 0, 380);
    const far = sim.spawn('mudling', 0, 900);
    const fly = sim.spawn('gullwing', 0, 410);
    for (const e of [kite, free, held, far, fly]) e.def = { ...e.def, speed: 0 };
    held.blockedBy = 999;
    const d0 = [kite, free, held, far, fly].map((e) => e.dist);
    for (let i = 0; i < 60 * 5 + 2; i++) {
      held.blockedBy = 999; // stand-in for a soldier holding it (the sim drops unknown blockers each tick)
      sim.update(1 / 60);
    }
    const gu = kite.def.gust!;
    expect(free.dist).toBeCloseTo(d0[1] + gu.distance, 3);
    expect(held.dist).toBe(d0[2]);
    expect(far.dist).toBe(d0[3]);
    expect(fly.dist).toBe(d0[4]);
    expect(kite.dist).toBe(d0[0]);
  });
});

describe('Verdant Ruins enemies', () => {
  it('Shiftscale swaps armor and magic resist on its timer', () => {
    const sim = new BattleSim(lvl, null);
    sim.status = 'running';
    const s = sim.spawn('shiftscale', 0, 400);
    s.def = { ...s.def, speed: 0 };
    const sh = s.def.shift!;
    expect(sim.res(s)).toEqual({ armor: s.def.armor, magicResist: s.def.magicResist });
    for (let i = 0; i < Math.ceil(sh.interval * 60) + 1; i++) sim.update(1 / 60);
    expect(s.shifted).toBe(true);
    expect(sim.res(s)).toEqual({ armor: sh.armor, magicResist: sh.magicResist });
    for (let i = 0; i < Math.ceil(sh.interval * 60) + 1; i++) sim.update(1 / 60);
    expect(s.shifted).toBe(false);
    expect(sim.res(s).armor).toBe(s.def.armor);
  });

  it('Idol Keeper raises a recent nearby fallen ally once, at partial health and no second bounty', () => {
    const sim = new BattleSim(lvl, null);
    sim.status = 'running';
    const keeper = sim.spawn('idolkeeper', 0, 400);
    keeper.def = { ...keeper.def, speed: 0 };
    const mud = sim.spawn('mudling', 0, 450);
    (sim as any).applyDamage(mud, 9999);
    const rv = keeper.def.revive!;
    for (let i = 0; i < Math.ceil(rv.interval * 60) + 2; i++) sim.update(1 / 60);
    const risen = sim.enemies.filter((e) => e.alive && e.def.id === 'mudling');
    expect(risen.length).toBe(1);
    expect(risen[0].revived).toBe(true);
    expect(risen[0].hp).toBe(Math.round(risen[0].maxHp * rv.hpFrac));
    const c0 = sim.coins;
    (sim as any).applyDamage(risen[0], 9999);
    expect(sim.coins).toBe(c0);
    for (let i = 0; i < Math.ceil(rv.interval * 60) + 2; i++) sim.update(1 / 60);
    expect(sim.enemies.filter((e) => e.alive && e.def.id === 'mudling').length).toBe(0); // never raised twice
  });
});

describe('Bramblehide thorns', () => {
  it('hurts a melee hero that hits it, but not ranged attacks', () => {
    const l = { ...lvl, slots: [] } as LevelDef;
    const sim = new BattleSim(l, 'bramble');
    sim.status = 'running';
    const h = sim.hero!;
    h.pos = { x: 400, y: 100 };
    h.dest = null;
    const boar = sim.spawn('bramblehide', 0, 396);
    boar.def = { ...boar.def, speed: 0, attack: 0 };
    for (let i = 0; i < 120; i++) sim.update(1 / 60);
    expect(boar.hp).toBeLessThan(boar.maxHp);
    expect(h.hp).toBeLessThan(h.maxHp);
    const sim2 = new BattleSim(l, 'fen');
    sim2.status = 'running';
    const h2 = sim2.hero!;
    h2.pos = { x: 400, y: 160 };
    h2.dest = null;
    const boar2 = sim2.spawn('bramblehide', 0, 420);
    boar2.def = { ...boar2.def, speed: 0, attack: 0 };
    for (let i = 0; i < 120; i++) sim2.update(1 / 60);
    expect(boar2.hp).toBeLessThan(boar2.maxHp);
    expect(h2.hp).toBe(h2.maxHp);
  });
});
