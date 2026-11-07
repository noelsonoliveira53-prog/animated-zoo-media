import { describe, expect, it } from 'vitest';
import {
  addResources,
  battleReward,
  builders,
  busyBuilders,
  capacity,
  collect,
  footprintFree,
  newVillage,
  pending,
  placeBuilding,
  tick,
  upgradeBuilding,
} from '../src/systems/village';
import { BUILDINGS } from '../src/data/buildings';
import { defaultSave, ensureVillage, loadSave, writeSave, type StorageLike } from '../src/systems/save';

const T0 = 1_000_000;
const HOUR = 3600_000;

describe('village', () => {
  it('starts with a working starter village', () => {
    const v = newVillage(T0);
    expect(v.buildings.find((b) => b.type === 'townhall')).toBeDefined();
    expect(builders(v)).toBe(2);
    expect(capacity(v)).toBe(1000 + 1500);
  });

  it('producers accumulate over time up to their capacity, and collect banks it', () => {
    const v = newVillage(T0);
    const mine = v.buildings.find((b) => b.type === 'coinmine')!;
    expect(pending(mine, T0 + HOUR / 2)).toBe(200);
    expect(pending(mine, T0 + 10 * HOUR)).toBe(500); // capped
    const before = v.coins;
    expect(collect(v, mine.uid, T0 + HOUR / 2)).toBe(200);
    expect(v.coins).toBe(before + 200);
    expect(pending(mine, T0 + HOUR / 2)).toBe(0);
  });

  it('storage caps resources and leaves the rest in the producer', () => {
    const v = newVillage(T0);
    v.coins = capacity(v) - 50;
    const mine = v.buildings.find((b) => b.type === 'coinmine')!;
    expect(collect(v, mine.uid, T0 + HOUR)).toBe(50);
    expect(pending(mine, T0 + HOUR)).toBeGreaterThan(300);
    expect(addResources(v, 999, 0).coins).toBe(0);
  });

  it('upgrades cost resources, need a free builder and finish after their timer', () => {
    const v = newVillage(T0);
    v.coins = 2000;
    v.glowsap = 2000;
    const mine = v.buildings.find((b) => b.type === 'coinmine')!;
    const well = v.buildings.find((b) => b.type === 'sapwell')!;
    const vault = v.buildings.find((b) => b.type === 'vault')!;
    expect(upgradeBuilding(v, mine.uid, T0).ok).toBe(true);
    expect(v.glowsap).toBe(2000 - BUILDINGS.coinmine.levels[1].cost.glowsap!);
    expect(upgradeBuilding(v, well.uid, T0).ok).toBe(true);
    expect(busyBuilders(v, T0)).toBe(2);
    const third = upgradeBuilding(v, vault.uid, T0);
    expect(third.ok).toBe(false);
    expect(tick(v, T0 + 10_000)).toEqual([]);
    const done = tick(v, T0 + 46_000);
    expect(done.map((b) => b.type).sort()).toEqual(['coinmine', 'sapwell']);
    expect(mine.level).toBe(2);
    expect(busyBuilders(v, T0 + 46_000)).toBe(0);
  });

  it('respects Grove Hall requirements and building limits', () => {
    const v = newVillage(T0);
    v.coins = v.glowsap = 2000;
    const r = placeBuilding(v, 'barracks', 0, 0, T0);
    expect(r.ok).toBe(false); // needs Grove Hall 2
    expect(placeBuilding(v, 'coinmine', 0, 0, T0).ok).toBe(true); // 2nd mine allowed at TH1
    tick(v, T0 + 20_000);
    expect(placeBuilding(v, 'coinmine', 19, 0, T0 + 20_000).ok).toBe(false); // max 2 at TH1
  });

  it('blocks overlapping placement and out-of-bounds', () => {
    const v = newVillage(T0);
    expect(footprintFree(v, 'coinmine', 10, 5)).toBe(false); // on the hall
    expect(footprintFree(v, 'coinmine', 21, 0)).toBe(false); // off the edge
    expect(footprintFree(v, 'wall', 0, 0)).toBe(true);
  });

  it('pays more for first clears than replays', () => {
    const first = battleReward(2, 0, 2);
    const replay = battleReward(2, 2, 2);
    const better = battleReward(2, 2, 3);
    expect(first.coins).toBeGreaterThan(better.coins);
    expect(better.coins).toBeGreaterThan(replay.coins);
    expect(battleReward(0, 0, 0)).toEqual({ coins: 0, glowsap: 0 });
  });

  it('persists through the save system', () => {
    const data: Record<string, string> = {};
    const store: StorageLike = { getItem: (k) => data[k] ?? null, setItem: (k, v) => void (data[k] = v) };
    const save = defaultSave();
    const v = ensureVillage(save, T0);
    v.coins = 1234;
    writeSave(save, store);
    expect(loadSave(store).village!.coins).toBe(1234);
  });
});

import { battlePerks, trainHero, HERO_TRAIN_COSTS } from '../src/systems/village';
import { BattleSim } from '../src/systems/BattleSim';

describe('village → battle perks', () => {
  it('village buildings grant battle perks', () => {
    const v = newVillage(T0);
    expect(battlePerks(v)).toEqual({ towerDamageMult: 1, bonusCoins: 0, rangerMult: 1, spellCdMult: 1 });
    v.buildings.push({ uid: 99, type: 'workshop', level: 2, col: 0, row: 0, upgradeEnds: null, lastCollect: T0 });
    v.buildings.push({ uid: 98, type: 'barracks', level: 1, col: 4, row: 0, upgradeEnds: null, lastCollect: T0 });
    v.buildings.find((b) => b.type === 'townhall')!.level = 3;
    const p = battlePerks(v);
    expect(p.towerDamageMult).toBeCloseTo(1.1);
    expect(p.bonusCoins).toBe(80);
    expect(p.rangerMult).toBeCloseTo(1.25);
    expect(battlePerks(null).towerDamageMult).toBe(1);
  });
  it('the Moonpetal Shrine shortens battle spell cooldowns', () => {
    const v = newVillage(T0);
    v.buildings.push({ uid: 97, type: 'shrine', level: 2, col: 0, row: 0, upgradeEnds: null, lastCollect: T0 });
    const p = battlePerks(v);
    expect(p.spellCdMult).toBeCloseTo(0.88);
    const lvl = { id: 't', name: 't', blurb: '', mapPos: { x: 0, y: 0 }, startCoins: 100, lives: 20,
      paths: [[{ x: 0, y: 300 }, { x: 1200, y: 300 }]], slots: [], waves: [{ groups: [{ enemy: 'mudling', count: 1, interval: 1 }] }],
      theme: { grass: 0, grassDark: 0, road: 0, roadEdge: 0 } };
    const plain = new BattleSim(lvl, null);
    const blessed = new BattleSim(lvl, null, { spellCdMult: p.spellCdMult });
    expect(plain.castSpell('starfall', { x: 600, y: 300 })).toBe(true);
    expect(blessed.castSpell('starfall', { x: 600, y: 300 })).toBe(true);
    expect(blessed.spellCd.starfall).toBeCloseTo(plain.spellCd.starfall * 0.88);
    expect(blessed.spellCooldown('starfall')).toBeCloseTo(blessed.spellCd.starfall);
  });
  it('heroes can be trained with glowsap up to max rank', () => {
    const v = newVillage(T0);
    v.glowsap = 20000;
    const ranks: Record<string, number> = {};
    for (let i = 0; i < 5; i++) expect(trainHero(v, ranks, 'fen').ok).toBe(true);
    expect(ranks.fen).toBe(5);
    expect(trainHero(v, ranks, 'fen').ok).toBe(false);
    expect(v.glowsap).toBe(20000 - HERO_TRAIN_COSTS.reduce((a, b) => a + b, 0));
    const poor = newVillage(T0);
    poor.glowsap = 10;
    expect(trainHero(poor, {}, 'fen').ok).toBe(false);
  });
  it('perks and hero rank flow into the battle sim', () => {
    const lvl = {
      id: 'x', name: 'x', blurb: '', mapPos: { x: 0, y: 0 }, startCoins: 200, lives: 5,
      theme: { grass: 0, grassDark: 0, road: 0, roadEdge: 0 },
      paths: [[{ x: 0, y: 100 }, { x: 600, y: 100 }]], slots: [],
      waves: [{ groups: [{ enemy: 'mudling', count: 1, interval: 1 }] }],
    };
    const sim = new BattleSim(lvl, 'bramble', { bonusCoins: 80, rangerMult: 1.5, heroLevel: 3 });
    expect(sim.coins).toBe(280);
    expect(sim.hero!.level).toBe(3);
    expect(sim.hero!.maxHp).toBeGreaterThan(260);
    sim.castSpell('grovecall', { x: 300, y: 100 });
    expect(sim.soldiers[0].maxHp).toBe(105);
  });
  it('the sim applies the multiplier to shots', () => {
    const lvl = {
      id: 'x', name: 'x', blurb: '', mapPos: { x: 0, y: 0 }, startCoins: 500, lives: 5,
      theme: { grass: 0, grassDark: 0, road: 0, roadEdge: 0 },
      paths: [[{ x: 0, y: 100 }, { x: 600, y: 100 }]], slots: [{ x: 300, y: 160 }],
      waves: [{ groups: [{ enemy: 'mudling', count: 1, interval: 1 }] }],
    };
    const sim = new BattleSim(lvl, null, { towerDamageMult: 1.5 });
    sim.build(0, 'thornbow');
    sim.spawn('shellback', 0, 300);
    sim.status = 'running';
    sim.update(1 / 60);
    const shot = sim.drainEvents().find((e) => e.type === 'shoot') as any;
    expect(shot.projectile.damage).toBeCloseTo(7 * 1.5);
  });
});

import { grantSwiftbloom, rushBuilding } from '../src/systems/village';
import { SWIFTBLOOM } from '../src/data/buildings';

describe('swiftbloom speed-ups', () => {
  it('caps how many can be held', () => {
    const v = newVillage(0);
    let got = 0;
    for (let i = 0; i < 10; i++) got += grantSwiftbloom(v);
    expect(got).toBe(SWIFTBLOOM.maxHeld);
    expect(v.swiftblooms).toBe(SWIFTBLOOM.maxHeld);
  });
  it('cuts build time and finishes short builds on the next tick', () => {
    const v = newVillage(0);
    v.coins = v.glowsap = 1e6;
    const hall = v.buildings.find((b) => b.type === 'townhall')!;
    expect(upgradeBuilding(v, hall.uid, 0).ok).toBe(true);
    const ends = hall.upgradeEnds!;
    expect(rushBuilding(v, hall.uid, 0).ok).toBe(false); // none held yet
    grantSwiftbloom(v);
    grantSwiftbloom(v);
    expect(rushBuilding(v, hall.uid, 0).ok).toBe(true);
    expect(hall.upgradeEnds).toBe(Math.max(0, ends - SWIFTBLOOM.seconds * 1000));
    expect(v.swiftblooms).toBe(1);
    // Rush again until done.
    while (hall.upgradeEnds !== null && (v.swiftblooms ?? 0) > 0) {
      rushBuilding(v, hall.uid, 0);
      tick(v, 0);
    }
    if (hall.upgradeEnds === null) expect(hall.level).toBe(2);
  });
  it('refuses when nothing is under construction', () => {
    const v = newVillage(0);
    grantSwiftbloom(v);
    const r = rushBuilding(v, v.buildings[0].uid, 0);
    expect(r.ok).toBe(false);
    expect(v.swiftblooms).toBe(1);
  });
});
