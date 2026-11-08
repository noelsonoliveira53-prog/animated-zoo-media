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

describe('Brasswork enemies', () => {
  it('Cogjammer slows the fire rate of towers in range only while alive; jammers do not stack', () => {
    const l2: LevelDef = { ...lvl, startCoins: 1000, slots: [{ x: 400, y: 160 }, { x: 1600, y: 160 }] };
    const sim = new BattleSim(l2, null);
    const near = sim.build(0, 'thornbow')!;
    const far = sim.build(1, 'thornbow')!;
    const j = sim.spawn('cogjammer', 0, 420);
    const j2 = sim.spawn('cogjammer', 0, 430);
    const slow = j.def.jam!.slow;
    expect(sim.towerJam(near)).toBeCloseTo(1 - slow);
    expect(sim.towerJam(far)).toBe(1);
    (sim as any).applyDamage(j, 99999);
    (sim as any).applyDamage(j2, 99999);
    expect(sim.towerJam(near)).toBe(1);
  });

  it('Steamrunner bolts when hit, then cools down', () => {
    const sim = new BattleSim(lvl, null);
    sim.status = 'running';
    const r = sim.spawn('steamrunner', 0, 400);
    const c = r.def.charge!;
    expect(sim.chargeMult(r)).toBe(1);
    (sim as any).applyDamage(r, 1);
    expect(sim.chargeMult(r)).toBe(c.speedMult);
    for (let i = 0; i < Math.ceil(c.duration * 60) + 2; i++) sim.update(1 / 60);
    expect(sim.chargeMult(r)).toBe(1);
    (sim as any).applyDamage(r, 1); // still cooling down: no second bolt yet
    expect(sim.chargeMult(r)).toBe(1);
  });
});

describe('Rivetshell harden', () => {
  it('gains armor with every hit, up to its cap', () => {
    const sim = new BattleSim(lvl, null);
    const r = sim.spawn('rivetshell', 0, 400);
    const h = r.def.harden!;
    const a0 = sim.res(r).armor;
    (sim as any).applyDamage(r, 1);
    expect(sim.res(r).armor).toBeCloseTo(a0 + h.perHit);
    for (let i = 0; i < 100; i++) (sim as any).applyDamage(r, 0.1);
    expect(sim.res(r).armor).toBe(h.max);
  });
});

describe('Starwell enemies', () => {
  it('Dimlantern shrinks the range of shooting towers near it while alive', () => {
    const l2: LevelDef = { ...lvl, startCoins: 1000, slots: [{ x: 400, y: 160 }, { x: 1600, y: 160 }] };
    const sim = new BattleSim(l2, null);
    const near = sim.build(0, 'thornbow')!;
    const far = sim.build(1, 'thornbow')!;
    const d = sim.spawn('dimlantern', 0, 420);
    expect(sim.towerDim(near)).toBeCloseTo(1 - d.def.dim!.cut);
    expect(sim.towerDim(far)).toBe(1);
    (sim as any).applyDamage(d, 99999);
    expect(sim.towerDim(near)).toBe(1);
  });

  it('Echo Wisp re-forms once at partial health and pays no second bounty', () => {
    const sim = new BattleSim(lvl, null);
    sim.status = 'running';
    const w = sim.spawn('echowisp', 0, 400);
    const c0 = sim.coins;
    (sim as any).applyDamage(w, 9999);
    const paid = sim.coins - c0;
    expect(paid).toBeGreaterThan(0);
    const echo = sim.enemies.filter((e) => e.alive && e.def.id === 'echowisp');
    expect(echo.length).toBe(1);
    expect(echo[0].hp).toBe(Math.round(echo[0].maxHp * w.def.echo!.hpFrac));
    const c1 = sim.coins;
    (sim as any).applyDamage(echo[0], 9999);
    expect(sim.coins).toBe(c1);
    expect(sim.enemies.filter((e) => e.alive && e.def.id === 'echowisp').length).toBe(0);
  });
});

describe('Sparkeel shock', () => {
  it('stuns a nearby melee hero, who lets go of what it holds and stops attacking for a moment', () => {
    const l = { ...lvl, slots: [] } as LevelDef;
    const sim = new BattleSim(l, 'bramble');
    sim.status = 'running';
    const h = sim.hero!;
    h.pos = { x: 400, y: 100 };
    h.dest = null;
    const eel = sim.spawn('sparkeel', 0, 396);
    eel.def = { ...eel.def, speed: 0, attack: 0 };
    for (let i = 0; i < 30; i++) sim.update(1 / 60);
    expect(eel.blockedBy).toBe(h.uid);
    eel.shockCd = 0.001;
    sim.update(1 / 60);
    expect(h.stun).toBeGreaterThan(0);
    expect(eel.blockedBy).toBe(0);
    const hp = eel.hp;
    for (let i = 0; i < 30; i++) sim.update(1 / 60); // still stunned: no hits
    expect(eel.hp).toBe(hp);
  });
});

describe('Rotbloom enemies', () => {
  it('Barkwarden gives nearby allies extra armor while it lives (not itself, not far allies)', () => {
    const sim = new BattleSim(lvl, null);
    const bw = sim.spawn('barkwarden', 0, 400);
    const near = sim.spawn('mudling', 0, 450);
    const far = sim.spawn('mudling', 0, 1200);
    const bonus = bw.def.fortify!.bonus;
    expect(sim.res(near).armor).toBeCloseTo(near.def.armor + bonus);
    expect(sim.res(far).armor).toBe(far.def.armor);
    expect(sim.res(bw).armor).toBe(bw.def.armor);
    (sim as any).applyDamage(bw, 99999);
    expect(sim.res(near).armor).toBe(near.def.armor);
  });

  it('a Rotseed left alone sprouts into its grown form and pays nothing', () => {
    const sim = new BattleSim(lvl, null);
    sim.status = 'running';
    const seed = sim.spawn('rotseed', 0, 400);
    const g = seed.def.grow!;
    const c0 = sim.coins;
    for (let i = 0; i < Math.ceil(g.after * 60) + 2; i++) sim.update(1 / 60);
    expect(seed.alive).toBe(false);
    expect(sim.enemies.some((e) => e.alive && e.def.id === g.into)).toBe(true);
    expect(sim.coins).toBe(c0);
  });

  it('a Gorgegrub feeds on allies dying nearby: grows, heals, and stops at its stack cap', () => {
    const sim = new BattleSim(lvl, null);
    const g = sim.spawn('gorgegrub', 0, 400);
    const f = g.def.feed!;
    g.hp = g.maxHp * 0.5;
    const max0 = g.maxHp;
    const hp0 = g.hp;
    const far = sim.spawn('mudling', 0, 1200);
    (sim as any).applyDamage(far, 99999);
    expect(g.fed).toBe(0);
    const near = sim.spawn('mudling', 0, 420);
    (sim as any).applyDamage(near, 99999);
    expect(g.fed).toBe(1);
    expect(g.maxHp).toBe(max0 + Math.round(max0 * f.growth));
    expect(g.hp).toBeGreaterThan(hp0);
    expect(sim.drainEvents().some((e) => e.type === 'feed')).toBe(true);
    for (let i = 0; i < f.maxStacks + 3; i++) (sim as any).applyDamage(sim.spawn('mudling', 0, 410), 99999);
    expect(g.fed).toBe(f.maxStacks);
  });
});

describe('Thunderhead enemies', () => {
  it('a Stormcaller strikes the nearest shooting tower in range, stunning it, then waits its interval', () => {
    // near pad 60px from the caller, far pad well out of range
    const sim = new BattleSim({ ...lvl, slots: [{ x: 200, y: 160 }, { x: 900, y: 160 }] }, null);
    sim.status = 'running';
    sim.coins = 9999;
    sim.build(0, 'thornbow');
    sim.build(1, 'thornbow');
    const sc = sim.spawn('stormcaller', 0, 200);
    sc.def = { ...sc.def, speed: 0 };
    const b = sc.def.bolt!;
    for (let i = 0; i < Math.ceil(b.interval * 60) + 2; i++) sim.update(1 / 60);
    const ev = sim.drainEvents().filter((e) => e.type === 'bolt');
    expect(ev.length).toBe(1);
    const struck = (ev[0] as any).tower;
    expect(Math.hypot(struck.pos.x - sc.pos.x, struck.pos.y - sc.pos.y)).toBeLessThanOrEqual(b.range);
    expect(struck).toBe(sim.towers[0]);
    expect(struck.frozen + struck.chillImmune).toBeGreaterThan(0);
    expect(sim.towers[1]!.chillImmune).toBe(0);
  });

  it('Thunderhooves run faster in a herd (capped), and alone at base speed', () => {
    const sim = new BattleSim(lvl, null);
    const h = sim.spawn('thunderhoof', 0, 300);
    const herd = h.def.herd!;
    expect(sim.herdMult(h)).toBe(1);
    sim.spawn('thunderhoof', 0, 320);
    expect(sim.herdMult(h)).toBeCloseTo(1 + herd.perAlly);
    for (let i = 0; i < 10; i++) sim.spawn('thunderhoof', 0, 290 + i * 3);
    expect(sim.herdMult(h)).toBeCloseTo(1 + herd.max);
    const far = sim.spawn('thunderhoof', 0, 900);
    expect(sim.herdMult(far)).toBe(1);
  });

  it('a Copperhorn takes its share of damage aimed at nearby allies (not far ones), and its own hits in full', () => {
    const sim = new BattleSim(lvl, null);
    const ox = sim.spawn('copperhorn', 0, 400);
    const g = ox.def.ground!;
    const near = sim.spawn('mudling', 0, 450);
    const far = sim.spawn('mudling', 0, 1200);
    const [o0, n0, f0] = [ox.hp, near.hp, far.hp];
    (sim as any).applyDamage(near, 50);
    expect(near.hp).toBeCloseTo(n0 - 50 * (1 - g.share));
    expect(ox.hp).toBeCloseTo(o0 - 50 * g.share);
    (sim as any).applyDamage(far, 20);
    expect(far.hp).toBe(f0 - 20);
    const o1 = ox.hp;
    (sim as any).applyDamage(ox, 30);
    expect(ox.hp).toBeCloseTo(o1 - 30);
    (sim as any).applyDamage(ox, 99999);
    const n1 = near.hp;
    (sim as any).applyDamage(near, 10);
    expect(near.hp).toBe(n1 - 10);
  });
});

describe('Sunscour enemies', () => {
  it('a Shimmerjack sheds its decoys on the first hit only; decoys pay nothing and cost no lives', () => {
    const sim = new BattleSim(lvl, null);
    const sj = sim.spawn('shimmerjack', 0, 400);
    const n0 = sim.enemies.length;
    (sim as any).applyDamage(sj, 5);
    const decoys = sim.enemies.slice(n0);
    expect(decoys.length).toBe(sj.def.mirage!.count);
    expect(decoys.every((d) => d.def.id === sj.def.mirage!.into && d.dist < sj.dist)).toBe(true);
    (sim as any).applyDamage(sj, 5);
    expect(sim.enemies.length).toBe(n0 + sj.def.mirage!.count);
    const c0 = sim.coins;
    (sim as any).applyDamage(decoys[0], 9999);
    expect(sim.coins).toBe(c0);
    expect(decoys[0].def.livesCost).toBe(0);
  });

  it('a Sandpicker that reaches the exit steals coins (never more than the player has)', () => {
    const sim = new BattleSim(lvl, null);
    sim.status = 'running';
    sim.coins = 500;
    const sp = sim.spawn('sandpicker', 0, 1995);
    for (let i = 0; i < 60 && sp.alive; i++) sim.update(1 / 60);
    expect(sp.alive).toBe(false);
    const ev = sim.drainEvents().find((e) => e.type === 'pilfer') as any;
    expect(ev.coins).toBeGreaterThan(0);
    expect(sim.coins).toBe(500 - ev.coins);
    sim.coins = 10;
    sim.spawn('sandpicker', 0, 1995);
    for (let i = 0; i < 60; i++) sim.update(1 / 60);
    expect(sim.coins).toBe(0);
  });

  it('a Kilnback bakes armor while unhit (capped) and any hit cracks it back to base', () => {
    const sim = new BattleSim(lvl, null);
    sim.status = 'running';
    const k = sim.spawn('kilnback', 0, 300);
    k.def = { ...k.def, speed: 0 };
    const c = k.def.crust!;
    for (let i = 0; i < 60 * 20; i++) sim.update(1 / 60);
    expect(k.armor).toBeCloseTo(k.def.armor + c.max);
    (sim as any).applyDamage(k, 5);
    expect(k.armor).toBe(k.def.armor);
    expect(sim.drainEvents().some((e) => e.type === 'crack')).toBe(true);
  });
});

describe('Coralreach enemies', () => {
  it('a Shellsnap molts once below its threshold: armor drops, speed rises', () => {
    const sim = new BattleSim(lvl, null);
    const c = sim.spawn('shellsnap', 0, 300);
    const m = c.def.molt!;
    (sim as any).applyDamage(c, c.maxHp * (1 - m.at) - 5);
    expect(c.molted).toBe(false);
    expect(c.armor).toBe(c.def.armor);
    (sim as any).applyDamage(c, 10);
    expect(c.molted).toBe(true);
    expect(c.armor).toBe(m.armor);
    expect(c.speedMult).toBeCloseTo(m.speedMult);
    expect(sim.drainEvents().filter((e) => e.type === 'molt').length).toBe(1);
  });

  it('a Tidecaller washes slows off allies in range on its timer (not far ones)', () => {
    const sim = new BattleSim(lvl, null);
    sim.status = 'running';
    const t = sim.spawn('tidecaller', 0, 400);
    const near = sim.spawn('mudling', 0, 450);
    const far = sim.spawn('mudling', 0, 1500);
    for (const e of [t, near, far]) e.def = { ...e.def, speed: 0 };
    for (const e of [near, far]) {
      e.slowFactor = 0.4;
      e.slowTime = 60;
    }
    for (let i = 0; i < Math.ceil(t.def.cleanse!.interval * 60) + 2; i++) sim.update(1 / 60);
    expect(near.slowFactor).toBe(1);
    expect(far.slowFactor).toBe(0.4);
  });

  it('an Inkspitter hit leaves an ink cloud that hides grounded enemies from towers until it fades', () => {
    const sim = new BattleSim({ ...lvl, slots: [{ x: 400, y: 160 }] }, null);
    sim.status = 'running';
    const o = sim.spawn('inkspitter', 0, 400);
    const m = sim.spawn('mudling', 0, 420);
    for (const e of [o, m]) e.def = { ...e.def, speed: 0 };
    (sim as any).applyDamage(o, 5);
    expect(sim.inked(m)).toBe(true);
    expect(sim.inked(o)).toBe(true);
    (sim as any).applyDamage(o, 5); // still on cooldown: no second cloud
    expect(sim.inkClouds.length).toBe(1);
    sim.coins = 999;
    sim.build(0, 'thornbow');
    for (let i = 0; i < 60; i++) sim.update(1 / 60);
    expect(m.hp).toBe(m.maxHp); // the tower can't see into the murk
    for (let i = 0; i < Math.ceil(o.def.ink!.duration * 60); i++) sim.update(1 / 60);
    expect(sim.inked(m)).toBe(false);
  });
});

describe('Blackwake enemies', () => {
  it('a Deckgunner shoots the nearest soldier in range while walking, on its reload timer', () => {
    const sim = new BattleSim({ ...lvl, slots: [{ x: 400, y: 160 }] }, null);
    sim.status = 'running';
    sim.coins = 999;
    sim.build(0, 'burrow');
    for (let i = 0; i < 30; i++) sim.update(1 / 60);
    const s = sim.soldiers[0];
    const g = sim.spawn('deckgunner', 0, Math.max(0, s.pos.x - 120));
    g.def = { ...g.def, speed: 0 };
    s.home = { ...s.pos };
    const hp0 = s.hp;
    for (let i = 0; i < Math.ceil(g.def.ranged!.interval * 60); i++) sim.update(1 / 60);
    expect(sim.drainEvents().some((e) => e.type === 'enemyShot')).toBe(true);
    expect(s.hp).toBeLessThan(hp0);
  });

  it('an Ironkeel drops anchor on its cycle: it stops and armors up, then hauls on', () => {
    const sim = new BattleSim(lvl, null);
    sim.status = 'running';
    const k = sim.spawn('ironkeel', 0, 100);
    const a = k.def.anchor!;
    for (let i = 0; i < Math.ceil(a.interval * 60) + 1; i++) sim.update(1 / 60);
    expect(k.anchored).toBe(true);
    expect(k.armor).toBeCloseTo(Math.min(0.85, k.def.armor + a.armor));
    const d = k.dist;
    for (let i = 0; i < 30; i++) sim.update(1 / 60);
    expect(k.dist).toBe(d);
    for (let i = 0; i < Math.ceil(a.duration * 60) + 1; i++) sim.update(1 / 60);
    expect(k.anchored).toBe(false);
    expect(k.armor).toBe(k.def.armor);
  });

  it("a Powdermonkey's keg blows up on death, hurting soldiers in range only", () => {
    const sim = new BattleSim({ ...lvl, slots: [{ x: 400, y: 160 }] }, null);
    sim.status = 'running';
    sim.coins = 999;
    sim.build(0, 'burrow');
    for (let i = 0; i < 30; i++) sim.update(1 / 60);
    const [a, b] = sim.soldiers;
    b.pos = { x: a.pos.x + 400, y: a.pos.y };
    b.home = { ...b.pos };
    const m = sim.spawn('powdermonkey', 0, 0);
    m.pos = { x: a.pos.x + 20, y: a.pos.y };
    const [ha, hb] = [a.hp, b.hp];
    (sim as any).applyDamage(m, 99999);
    expect(a.hp).toBeLessThan(ha);
    expect(b.hp).toBe(hb);
    expect(sim.drainEvents().some((e) => e.type === 'keg')).toBe(true);
  });
});

describe('Amberwood enemies', () => {
  it('a Barkdrum beats its drum on a timer, hastening itself and nearby allies but not far ones', () => {
    const sim = new BattleSim(lvl, null);
    sim.status = 'running';
    const b = sim.spawn('barkdrum', 0, 300);
    const near = sim.spawn('mudling', 0, 340);
    const far = sim.spawn('mudling', 0, 900);
    near.def = { ...near.def, speed: 0 };
    far.def = { ...far.def, speed: 0 };
    b.def = { ...b.def, speed: 0 };
    const d = b.def.drum!;
    for (let i = 0; i < Math.ceil(d.interval * 0.5 * 60) + 1; i++) sim.update(1 / 60);
    expect(sim.drainEvents().some((e) => e.type === 'drum')).toBe(true);
    expect(near.hasteMult).toBeCloseTo(d.speedMult);
    expect(b.hasteMult).toBeCloseTo(d.speedMult);
    expect(far.hasteMult).toBe(1);
    for (let i = 0; i < Math.ceil(d.duration * 60) + 2; i++) sim.update(1 / 60);
    expect(near.hasteMult).toBe(1);
  });

  it('a Turnleaf turns its hide toward the damage that hits it, letting the other guard slip', () => {
    const sim = new BattleSim({ ...lvl, slots: [{ x: 400, y: 160 }] }, null);
    sim.status = 'running';
    const t = sim.spawn('turnleaf', 0, 400);
    t.def = { ...t.def, speed: 0, hp: 99999 };
    t.hp = t.maxHp = 99999;
    const a = t.def.adapt!;
    const hit = (type: 'physical' | 'magic') => (sim as unknown as { applyDamage: (e: unknown, d: number, ty: string) => void }).applyDamage(t, 10, type);
    for (let i = 0; i < 20; i++) hit('physical');
    expect(t.armor).toBeCloseTo(t.def.armor + a.max);
    expect(t.mr).toBeCloseTo(t.def.magicResist);
    for (let i = 0; i < 3; i++) hit('magic');
    expect(t.mr).toBeCloseTo(t.def.magicResist + 3 * a.step);
    expect(t.armor).toBeCloseTo(t.def.armor + a.max - 3 * a.step);
    // a real magic tower shot turns it too
    sim.coins = 999;
    sim.build(0, 'glimmer');
    const mr0 = t.mr;
    for (let i = 0; i < 60 * 3; i++) sim.update(1 / 60);
    expect(t.mr).toBeGreaterThan(mr0);
  });
});

describe('Sapstoat', () => {
  it('heals itself from the melee damage it deals to a blocking soldier', () => {
    const sim = new BattleSim({ ...lvl, slots: [{ x: 400, y: 160 }] }, null);
    sim.status = 'running';
    sim.coins = 999;
    sim.build(0, 'burrow');
    for (let i = 0; i < 30; i++) sim.update(1 / 60);
    const s = sim.soldiers[0];
    const st = sim.spawn('sapstoat', 0, Math.max(0, s.pos.x - 60));
    st.hp = st.maxHp * 0.5;
    let healed = 0;
    for (let i = 0; i < 60 * 4; i++) {
      sim.update(1 / 60);
      for (const ev of sim.drainEvents()) if (ev.type === 'leech') healed += ev.amount;
    }
    expect(healed).toBeGreaterThan(0);
  });
});

describe('Mistwreath enemies', () => {
  it('a Mistfox fades on its cycle and takes no damage while phased', () => {
    const sim = new BattleSim(lvl, null);
    sim.status = 'running';
    const f = sim.spawn('mistfox', 0, 200);
    f.def = { ...f.def, speed: 0 };
    const ph = f.def.phase!;
    const hit = (d: number) => (sim as unknown as { applyDamage: (e: unknown, d: number, t: string) => void }).applyDamage(f, d, 'physical');
    hit(10);
    expect(f.hp).toBe(f.maxHp - 10);
    for (let i = 0; i < Math.ceil(ph.interval * 60) + 1; i++) sim.update(1 / 60);
    expect(f.phased).toBe(true);
    const hp = f.hp;
    hit(50);
    expect(f.hp).toBe(hp);
    for (let i = 0; i < Math.ceil(ph.duration * 60) + 1; i++) sim.update(1 / 60);
    expect(f.phased).toBe(false);
    hit(10);
    expect(f.hp).toBe(hp - 10);
  });

  it('a Silkcrane dodges about its share of single-target shots, but never splash', () => {
    let dodges = 0;
    let shots = 0;
    for (let seed = 1; seed <= 4; seed++) {
      let r = seed * 9301;
      const sim = new BattleSim({ ...lvl, slots: [{ x: 400, y: 160 }] }, null, { random: () => ((r = (r * 16807) % 2147483647) / 2147483647) });
      sim.status = 'running';
      sim.coins = 999;
      sim.build(0, 'thornbow');
      const c = sim.spawn('silkcrane', 0, 400);
      c.def = { ...c.def, speed: 0, hp: 999999 };
      c.hp = c.maxHp = 999999;
      for (let i = 0; i < 60 * 20; i++) {
        sim.update(1 / 60);
        for (const ev of sim.drainEvents()) {
          if (ev.type === 'dodge') dodges++;
          if (ev.type === 'hit' && ev.enemy === c) shots++;
        }
      }
    }
    const rate = dodges / (dodges + shots);
    expect(rate).toBeGreaterThan(0.2);
    expect(rate).toBeLessThan(0.5);
  });
});

describe('Glowbearer', () => {
  it('its lantern cuts damage to nearby allies of every type, but not to itself or far allies', () => {
    const sim = new BattleSim(lvl, null);
    const g = sim.spawn('glowbearer', 0, 300);
    const near = sim.spawn('mudling', 0, 360);
    const far = sim.spawn('mudling', 0, 900);
    const cut = g.def.ward!.cut;
    const hit = (e: unknown, t: string) => (sim as unknown as { applyDamage: (e: unknown, d: number, t: string) => void }).applyDamage(e, 20, t);
    const n0 = near.hp;
    hit(near, 'magic');
    expect(n0 - near.hp).toBeCloseTo(20 * (1 - cut));
    hit(near, 'true');
    expect(n0 - near.hp).toBeCloseTo(40 * (1 - cut));
    const f0 = far.hp;
    hit(far, 'physical');
    expect(f0 - far.hp).toBe(20);
    const g0 = g.hp;
    hit(g, 'physical');
    expect(g0 - g.hp).toBe(20);
  });
});

describe('Highcanopy enemies', () => {
  it('a Howler gets faster each time it is slowed (at most twice a second), up to its cap', () => {
    const sim = new BattleSim(lvl, null);
    sim.status = 'running';
    const h = sim.spawn('howler', 0, 200);
    const r = h.def.rile!;
    sim.slow(h, 0.5, 1);
    expect(h.speedMult).toBeCloseTo(1 + r.perSlow);
    sim.slow(h, 0.5, 1); // too soon: no extra rile
    expect(h.speedMult).toBeCloseTo(1 + r.perSlow);
    for (let k = 0; k < 20; k++) {
      for (let i = 0; i < 31; i++) sim.update(1 / 60);
      sim.slow(h, 0.5, 1);
    }
    expect(h.speedMult).toBeCloseTo(1 + r.max);
  });

  it('a Ringtail Mourner toughens nearby allies for good when it dies', () => {
    const sim = new BattleSim(lvl, null);
    const m = sim.spawn('mourner', 0, 300);
    const near = sim.spawn('mudling', 0, 340);
    const far = sim.spawn('mudling', 0, 900);
    const a0 = near.armor;
    (sim as unknown as { applyDamage: (e: unknown, d: number) => void }).applyDamage(m, 99999);
    expect(near.armor).toBeCloseTo(Math.min(0.85, a0 + m.def.grief!.armor));
    expect(far.armor).toBe(far.def.armor);
    expect(sim.drainEvents().some((e) => e.type === 'grief')).toBe(true);
  });
});

describe('Canopy Harrier', () => {
  it('carries off the nearest soldier in reach on its cooldown, forcing a respawn', () => {
    const sim = new BattleSim({ ...lvl, slots: [{ x: 400, y: 160 }] }, null);
    sim.status = 'running';
    sim.coins = 999;
    sim.build(0, 'burrow');
    for (let i = 0; i < 40; i++) sim.update(1 / 60);
    const s = sim.soldiers[0];
    const h = sim.spawn('harrier', 0, 100);
    h.def = { ...h.def, speed: 0 };
    h.pos = { x: s.pos.x + 20, y: s.pos.y };
    let snatched = false;
    for (let i = 0; i < Math.ceil(h.def.snatch!.cooldown * 60); i++) {
      sim.update(1 / 60);
      h.pos = { x: s.pos.x + 20, y: s.pos.y };
      if (sim.drainEvents().some((ev) => ev.type === 'snatch')) snatched = true;
      if (snatched) break;
    }
    expect(snatched).toBe(true);
    expect(sim.soldiers.some((so) => !so.alive)).toBe(true);
  });
});

describe('Honeycomb Hills enemies', () => {
  it('a Waxback keeps its thick coat against physical blows until enough magic melts it', () => {
    const sim = new BattleSim(lvl, null);
    const w = sim.spawn('waxback', 0, 300);
    const wax = w.def.wax!;
    const hit = (d: number, t: string) => (sim as unknown as { applyDamage: (e: unknown, d: number, t: string) => void }).applyDamage(w, d, t);
    expect(w.armor).toBeCloseTo(w.def.armor + wax.armor);
    hit(w.maxHp * 0.5, 'physical');
    expect(w.armor).toBeCloseTo(w.def.armor + wax.armor);
    w.hp = w.maxHp;
    hit(w.maxHp * wax.melt * 0.6, 'magic');
    expect(w.armor).toBeCloseTo(w.def.armor + wax.armor);
    hit(w.maxHp * wax.melt * 0.5, 'magic');
    expect(w.armor).toBeCloseTo(w.def.armor);
    expect(sim.drainEvents().some((e) => e.type === 'melt')).toBe(true);
  });

  it('a Hexguard Wasp turns aside its first shots, then regains a charge over time', () => {
    const sim = new BattleSim({ ...lvl, slots: [{ x: 400, y: 160 }] }, null);
    sim.status = 'running';
    sim.coins = 999;
    sim.build(0, 'thornbow');
    const h = sim.spawn('hexguard', 0, 400);
    h.def = { ...h.def, speed: 0 };
    h.hp = h.maxHp = 999999;
    const p = h.def.parry!;
    let parries = 0;
    let firstHitAt = -1;
    for (let i = 0; i < 60 * 12 && firstHitAt < 0; i++) {
      sim.update(1 / 60);
      for (const ev of sim.drainEvents()) {
        if (ev.type === 'parry') parries++;
        if (ev.type === 'hit' && ev.enemy === h && firstHitAt < 0) firstHitAt = sim.time;
      }
    }
    expect(parries).toBeGreaterThanOrEqual(p.charges);
    expect(h.hp).toBeLessThan(h.maxHp);
    // with no shots coming in, a used charge comes back after `regen` seconds
    const q = sim.spawn('hexguard', 0, 1800);
    q.parryCharges = 0;
    q.parryCd = p.regen;
    for (let i = 0; i < Math.ceil(p.regen * 60) + 2; i++) sim.update(1 / 60);
    expect(q.parryCharges).toBeGreaterThanOrEqual(1);
  });
});

describe('Honeypaw Cub', () => {
  it('its swipes leave a blocking soldier swinging at half speed for a while', () => {
    const sim = new BattleSim({ ...lvl, slots: [{ x: 400, y: 160 }] }, null);
    sim.status = 'running';
    sim.coins = 999;
    sim.build(0, 'burrow');
    for (let i = 0; i < 60; i++) sim.update(1 / 60);
    const s = sim.soldiers[0];
    const c = sim.spawn('honeypaw', 0, 380);
    c.hp = c.maxHp = 999999;
    let glazes = 0;
    for (let i = 0; i < 60 * 6 && !glazes; i++) {
      sim.update(1 / 60);
      glazes += sim.drainEvents().filter((e) => e.type === 'glaze').length;
    }
    expect(glazes).toBeGreaterThan(0);
    const victim = sim.soldiers.find((x) => (x.glazed ?? 0) > 0)!;
    expect(victim).toBeDefined();
    expect(victim.glazeSlow).toBe(c.def.glaze!.slow);
    expect(s.stats.attackRate).toBeGreaterThan(0);
  });
});

describe('Glimmerbog enemies', () => {
  it('a Lanternfrog draws a single-target tower even when the tower is set to another mode', () => {
    const sim = new BattleSim({ ...lvl, slots: [{ x: 400, y: 160 }] }, null);
    sim.status = 'running';
    sim.coins = 999;
    sim.build(0, 'thornbow');
    const ahead = sim.spawn('mudling', 0, 460);
    const frog = sim.spawn('lanternfrog', 0, 340);
    for (const e of [ahead, frog]) e.def = { ...e.def, speed: 0 };
    ahead.hp = ahead.maxHp = 99999;
    frog.hp = frog.maxHp = 99999;
    let hitFrog = 0;
    let hitAhead = 0;
    for (let i = 0; i < 60 * 3; i++) {
      sim.update(1 / 60);
      for (const ev of sim.drainEvents()) if (ev.type === 'hit') ev.enemy === frog ? hitFrog++ : ev.enemy === ahead && hitAhead++;
    }
    expect(hitFrog).toBeGreaterThan(0);
    expect(hitAhead).toBe(0);
  });

  it('a Hexcroak curses the nearest tower so its shots hit softer for a while', () => {
    const sim = new BattleSim({ ...lvl, slots: [{ x: 400, y: 160 }] }, null);
    sim.status = 'running';
    sim.coins = 999;
    sim.build(0, 'thornbow');
    const t = sim.towers[0]!;
    const h = sim.spawn('hexcroak', 0, 400);
    h.def = { ...h.def, speed: 0 };
    h.hp = h.maxHp = 99999;
    let hexes = 0;
    for (let i = 0; i < 60 * 4 && !hexes; i++) {
      sim.update(1 / 60);
      hexes += sim.drainEvents().filter((e) => e.type === 'hex').length;
    }
    expect(hexes).toBe(1);
    expect(t.hexed).toBeGreaterThan(0);
    expect(t.hexCut).toBe(h.def.hex!.cut);
    const shot = sim.projectiles.find((p) => p.towerUid === t.uid);
    for (let i = 0; i < 60 && !sim.projectiles.some((p) => p.towerUid === t.uid); i++) sim.update(1 / 60);
    const p = shot ?? sim.projectiles.find((q) => q.towerUid === t.uid)!;
    const plain = new BattleSim({ ...lvl, slots: [{ x: 400, y: 160 }] }, null);
    plain.coins = 999;
    plain.build(0, 'thornbow');
    const base = (plain as unknown as { stats: (t: unknown) => { damage: number } }).stats(plain.towers[0]).damage;
    expect(p.damage).toBeCloseTo(base * (1 - h.def.hex!.cut));
  });
});

describe('Mudskipper', () => {
  it('dives once when knocked below half health: untouchable for a moment, healed, then back up', () => {
    const sim = new BattleSim(lvl, null);
    sim.status = 'running';
    const m = sim.spawn('mudskipper', 0, 300);
    const d = m.def.dive!;
    const hit = (n: number) => (sim as unknown as { applyDamage: (e: unknown, d: number) => void }).applyDamage(m, n);
    hit(m.maxHp * 0.6);
    expect(m.underground).toBe(true);
    expect(m.hp).toBeCloseTo(m.maxHp * (0.4 + d.heal));
    const dist0 = m.dist;
    for (let i = 0; i < Math.ceil(d.duration * 60) + 2; i++) sim.update(1 / 60);
    expect(m.underground).toBe(false);
    expect(m.dist).toBeGreaterThan(dist0);
    hit(m.maxHp * 0.3);
    expect(m.underground).toBe(false); // only once
    expect(sim.drainEvents().filter((e) => e.type === 'dive').length).toBeGreaterThanOrEqual(1);
  });
});

describe('Thistledown enemies', () => {
  it('a Tumblehog speeds up while unhit (capped), and a hit resets it', () => {
    const sim = new BattleSim(lvl, null);
    sim.status = 'running';
    const t = sim.spawn('tumblehog', 0, 100);
    const m = t.def.momentum!;
    expect(sim.momentumMult(t)).toBeCloseTo(1);
    for (let i = 0; i < 60 * 3; i++) sim.update(1 / 60);
    expect(sim.momentumMult(t)).toBeCloseTo(1 + Math.min(m.max, 3 * m.perSec), 1);
    for (let i = 0; i < 60 * 10; i++) sim.update(1 / 60);
    expect(sim.momentumMult(t)).toBeCloseTo(1 + m.max);
    (sim as unknown as { applyDamage: (e: unknown, d: number) => void }).applyDamage(t, 1);
    expect(sim.momentumMult(t)).toBeCloseTo(1);
  });

  it('a Bloomdoe heals hurt allies nearby when it falls, but not far ones', () => {
    const sim = new BattleSim(lvl, null);
    const d = sim.spawn('bloomdoe', 0, 300);
    const near = sim.spawn('mudling', 0, 360);
    const far = sim.spawn('mudling', 0, 900);
    near.hp = far.hp = 1;
    (sim as unknown as { applyDamage: (e: unknown, d: number) => void }).applyDamage(d, 99999);
    expect(near.hp).toBeCloseTo(Math.min(near.maxHp, 1 + near.maxHp * d.def.blossom!.heal));
    expect(far.hp).toBe(1);
    expect(sim.drainEvents().some((e) => e.type === 'blossom')).toBe(true);
  });
});

describe('Lookout Marmot', () => {
  it('whistles on its first hit only: allies nearby (and itself) speed up for a while', () => {
    const sim = new BattleSim(lvl, null);
    const m = sim.spawn('marmot', 0, 300);
    const near = sim.spawn('mudling', 0, 380);
    const far = sim.spawn('mudling', 0, 900);
    const hit = () => (sim as unknown as { applyDamage: (e: unknown, d: number) => void }).applyDamage(m, 5);
    hit();
    const a = m.def.alarm!;
    expect(near.hasteMult).toBeCloseTo(a.speedMult);
    expect(m.hasteMult).toBeCloseTo(a.speedMult);
    expect(far.hasteMult).toBe(1);
    expect(sim.drainEvents().filter((e) => e.type === 'alarm').length).toBe(1);
    hit();
    expect(sim.drainEvents().filter((e) => e.type === 'alarm').length).toBe(0);
  });
});

describe('Patchwork Wolds enemies', () => {
  it('a living Tithe Weasel skims kill bounties; once it falls, full bounty again', () => {
    const sim = new BattleSim(lvl, null);
    const hit = (e: unknown) => (sim as unknown as { applyDamage: (e: unknown, d: number) => void }).applyDamage(e, 99999);
    const w = sim.spawn('titheweasel', 0, 300);
    const c0 = sim.coins;
    hit(sim.spawn('shellback', 0, 500));
    const skimmed = sim.coins - c0;
    hit(w);
    const c1 = sim.coins;
    hit(sim.spawn('shellback', 0, 500));
    const full = sim.coins - c1;
    expect(skimmed).toBe(Math.round(full * (1 - w.def.tithe!)));
  });

  it('a Plough Ox cannot be held and tramples each soldier once as it passes', () => {
    const sim = new BattleSim({ ...lvl, slots: [{ x: 400, y: 160 }] }, null);
    sim.status = 'running';
    sim.coins = 999;
    sim.build(0, 'burrow');
    for (let i = 0; i < 60; i++) sim.update(1 / 60);
    const ox = sim.spawn('ploughox', 0, 330);
    ox.hp = ox.maxHp = 99999;
    const d0 = ox.dist;
    let tramples = 0;
    for (let i = 0; i < 60 * 6; i++) {
      sim.update(1 / 60);
      tramples += sim.drainEvents().filter((e) => e.type === 'trample').length;
      expect(ox.blockedBy).toBe(0);
    }
    expect(ox.dist - d0).toBeGreaterThan(ox.def.speed * 5);
    expect(tramples).toBeGreaterThan(0);
    expect(new Set(ox.trampled).size).toBe(ox.trampled.length);
  });
});

describe('Shepherd Collie', () => {
  it('hurries slow allies near it up to its own speed, but not far ones', () => {
    const sim = new BattleSim(lvl, null);
    const dog = sim.spawn('collie', 0, 300);
    const near = sim.spawn('ploughox', 0, 360);
    const far = sim.spawn('ploughox', 0, 900);
    expect(sim.baseSpeed(near)).toBe(dog.def.speed);
    expect(sim.baseSpeed(far)).toBe(far.def.speed);
    expect(sim.baseSpeed(dog)).toBe(dog.def.speed);
    (sim as unknown as { applyDamage: (e: unknown, d: number) => void }).applyDamage(dog, 99999);
    expect(sim.baseSpeed(near)).toBe(near.def.speed);
  });
});

describe('Rustrock Canyons enemies', () => {
  it('a Sandburrow Gopher pops up partway down the road, not at the gate', () => {
    const sim = new BattleSim(lvl, null);
    const g = sim.spawn('sandburrow', 0);
    expect(g.dist).toBeGreaterThan(0);
    expect(g.dist).toBeCloseTo(2000 * g.def.ambush!, 0);
    expect(sim.drainEvents().some((e) => e.type === 'ambush')).toBe(true);
    const child = sim.spawn('sandburrow', 0, 120); // spawned somewhere explicit (split, revive): stays put
    expect(child.dist).toBe(120);
  });

  it('a Curlshell Armadillo curls when hit: tougher and slower for a while, then on cooldown', () => {
    const sim = new BattleSim(lvl, null);
    sim.status = 'running';
    const a = sim.spawn('curlshell', 0, 300);
    const c = a.def.curl!;
    const base = sim.res(a);
    (sim as unknown as { applyDamage: (e: unknown, d: number) => void }).applyDamage(a, 1);
    expect(a.curlT).toBeCloseTo(c.duration);
    expect(sim.res(a).armor).toBeCloseTo(Math.min(0.85, base.armor + c.bonus));
    expect(sim.res(a).magicResist).toBeCloseTo(Math.min(0.85, base.magicResist + c.bonus));
    const d0 = a.dist;
    for (let i = 0; i < 30; i++) sim.update(1 / 60);
    expect(a.dist - d0).toBeCloseTo(a.def.speed * c.slow * 0.5, 0);
    for (let i = 0; i < Math.ceil(c.duration * 60); i++) sim.update(1 / 60);
    expect(a.curlT).toBeLessThanOrEqual(0);
    (sim as unknown as { applyDamage: (e: unknown, d: number) => void }).applyDamage(a, 1);
    expect(a.curlT).toBeLessThanOrEqual(0); // still cooling down
  });
});

describe('Canyon Rattler', () => {
  it('its bite poisons a blocking soldier, who keeps losing health over time', () => {
    const sim = new BattleSim({ ...lvl, slots: [{ x: 400, y: 160 }] }, null);
    sim.status = 'running';
    sim.coins = 999;
    sim.build(0, 'burrow');
    for (let i = 0; i < 60; i++) sim.update(1 / 60);
    const r = sim.spawn('rattler', 0, 380);
    r.hp = r.maxHp = 999999;
    let bites = 0;
    for (let i = 0; i < 60 * 6 && !bites; i++) {
      sim.update(1 / 60);
      bites += sim.drainEvents().filter((e) => e.type === 'venom').length;
    }
    expect(bites).toBeGreaterThan(0);
    const victim = sim.soldiers.find((s) => (s.poisonT ?? 0) > 0)!;
    expect(victim.poisonDps).toBe(r.def.venom!.dps);
    // pull the snake away so only the poison works on the soldier
    r.hp = 0;
    r.alive = false;
    const hp0 = victim.hp;
    for (let i = 0; i < 60; i++) sim.update(1 / 60);
    expect(victim.hp).toBeLessThan(hp0);
  });
});

describe('Pebblebrook Rapids enemies', () => {
  const hit = (sim: BattleSim, e: unknown, d: number) => (sim as unknown as { applyDamage: (e: unknown, d: number) => void }).applyDamage(e, d);
  it('a Bubbler Newt bubbles nearby allies; a bubble eats one whole hit, then pops', () => {
    const sim = new BattleSim(lvl, null);
    sim.status = 'running';
    const n = sim.spawn('bubbler', 0, 300);
    const near = sim.spawn('mudling', 0, 340);
    const far = sim.spawn('mudling', 0, 900);
    for (let i = 0; i < Math.ceil(n.def.bubble!.interval * 60); i++) sim.update(1 / 60);
    expect(near.bubbled).toBe(true);
    expect(n.bubbled).toBe(true);
    expect(far.bubbled).toBe(false);
    const hp = near.hp;
    hit(sim, near, 50);
    expect(near.hp).toBe(hp);
    expect(near.bubbled).toBe(false);
    hit(sim, near, 5);
    expect(near.hp).toBeLessThan(hp);
    expect(sim.drainEvents().some((e) => e.type === 'pop')).toBe(true);
  });

  it('a Torrent Pike surges itself and unheld neighbours down the road, but not far-off ones', () => {
    const sim = new BattleSim(lvl, null);
    sim.status = 'running';
    const p = sim.spawn('pike', 0, 300);
    const near = sim.spawn('mudling', 0, 330);
    const far = sim.spawn('mudling', 0, 900);
    const s = p.def.surge!;
    p.surgeCd = 0.05; // about to surge
    const steps = 6;
    const before = { p: p.dist, near: near.dist, far: far.dist };
    for (let i = 0; i < steps; i++) sim.update(1 / 60);
    const walk = (e: typeof p) => e.def.speed * (steps / 60);
    expect(p.dist - before.p).toBeGreaterThan(walk(p) + s.distance * 0.9);
    expect(near.dist - before.near).toBeGreaterThan(walk(near) + s.distance * 0.9);
    expect(far.dist - before.far).toBeLessThan(walk(far) + 5);
    expect(sim.drainEvents().some((e) => e.type === 'surge')).toBe(true);
  });
});

describe('Spray Otter', () => {
  it('soaks itself and nearby allies so spells hit them for less; towers are unaffected', () => {
    const sim = new BattleSim(lvl, null);
    sim.status = 'running';
    const o = sim.spawn('sprayotter', 0, 300);
    const near = sim.spawn('mudling', 0, 360);
    const far = sim.spawn('mudling', 0, 1200);
    expect(sim.drenchCut(o)).toBeCloseTo(o.def.drench!.cut);
    expect(sim.drenchCut(near)).toBeCloseTo(o.def.drench!.cut);
    expect(sim.drenchCut(far)).toBe(0);
    o.alive = false;
    expect(sim.drenchCut(near)).toBe(0);
  });
});

describe('Starheath Moors enemies', () => {
  const hit = (sim: BattleSim, e: unknown, d: number) => (sim as unknown as { applyDamage: (e: unknown, d: number) => void }).applyDamage(e, d);
  it('Heath Wisps share every hit equally along the linked string; a lone wisp takes it all', () => {
    const sim = new BattleSim(lvl, null);
    const a = sim.spawn('heathwisp', 0, 300);
    const b = sim.spawn('heathwisp', 0, 340);
    const c = sim.spawn('heathwisp', 0, 380);
    const lone = sim.spawn('heathwisp', 0, 1500);
    const hp = a.hp;
    hit(sim, a, 90);
    expect(a.hp).toBeCloseTo(hp - 30);
    expect(b.hp).toBeCloseTo(hp - 30);
    expect(c.hp).toBeCloseTo(hp - 30);
    hit(sim, lone, 90);
    expect(lone.hp).toBeCloseTo(hp - 90);
    expect(sim.drainEvents().some((e) => e.type === 'link')).toBe(true);
  });

  it('a Moorland Ram shrugs off the first bit of every hit, never more than 3/4 of it', () => {
    const sim = new BattleSim(lvl, null);
    const r = sim.spawn('moorram', 0, 300);
    const w = r.def.wool!;
    const hp = r.hp;
    hit(sim, r, 100);
    expect(r.hp).toBeCloseTo(hp - (100 - w));
    hit(sim, r, 8);
    expect(r.hp).toBeCloseTo(hp - (100 - w) - 2);
  });
});
