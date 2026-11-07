import { describe, expect, it } from 'vitest';
import { CAMP_BUILDINGS } from '../src/data/raid';
import { buildingCenter, campLoot, generateCamp } from '../src/systems/camp';
import { RaidSim } from '../src/systems/RaidSim';

const run = (sim: RaidSim, s: number) => {
  for (let i = 0; i < s * 30 && !sim.ended; i++) sim.update(1 / 30);
};

describe('camp generation', () => {
  it('is deterministic per seed and tier', () => {
    expect(generateCamp(42, 1)).toEqual(generateCamp(42, 1));
    expect(generateCamp(42, 1)).not.toEqual(generateCamp(43, 1));
  });
  it('places one HQ and no overlapping buildings', () => {
    for (let seed = 1; seed < 20; seed++) {
      const camp = generateCamp(seed, 2);
      expect(camp.buildings.filter((b) => CAMP_BUILDINGS[b.type].hq).length).toBe(1);
      for (const a of camp.buildings)
        for (const b of camp.buildings) {
          if (a === b) continue;
          const sa = CAMP_BUILDINGS[a.type].size;
          const sb = CAMP_BUILDINGS[b.type].size;
          const overlap = a.col < b.col + sb && a.col + sa > b.col && a.row < b.row + sb && a.row + sa > b.row;
          expect(overlap).toBe(false);
        }
    }
  });
  it('higher tiers have more buildings and loot', () => {
    expect(generateCamp(5, 2).buildings.length).toBeGreaterThan(generateCamp(5, 0).buildings.length);
    expect(campLoot(generateCamp(5, 2)).coins).toBeGreaterThan(campLoot(generateCamp(5, 0)).coins);
  });
});

describe('raid sim', () => {
  it('rejects deploying on top of the camp or without troops', () => {
    const camp = generateCamp(1, 0);
    const sim = new RaidSim(camp, { brawler: 1 });
    expect(sim.deploy('brawler', buildingCenter(camp.buildings[0]))).toBeNull();
    expect(sim.deploy('slinger', { x: 60, y: 120 })).toBeNull();
    expect(sim.deploy('brawler', { x: 60, y: 120 })).not.toBeNull();
    expect(sim.deploy('brawler', { x: 60, y: 140 })).toBeNull();
  });

  it('a big army wipes an outpost for 3 stars and full loot', () => {
    const camp = generateCamp(3, 0);
    const sim = new RaidSim(camp, { brawler: 20, sapper: 8, slinger: 10 });
    for (let i = 0; i < 20; i++) sim.deploy('brawler', { x: 70, y: 120 + i * 25 });
    for (let i = 0; i < 8; i++) sim.deploy('sapper', { x: 1210, y: 150 + i * 50 });
    for (let i = 0; i < 10; i++) sim.deploy('slinger', { x: 640, y: 680 - (i % 2) * 10 });
    run(sim, 90);
    expect(sim.destruction).toBe(1);
    expect(sim.stars).toBe(3);
    expect(sim.loot).toEqual(campLoot(camp));
  });

  it('the raid ends when time runs out', () => {
    const camp = generateCamp(3, 2);
    const sim = new RaidSim(camp, { slinger: 1 });
    sim.deploy('slinger', { x: 70, y: 380 });
    run(sim, 95);
    expect(sim.ended).toBe(true);
    expect(sim.stars).toBe(0);
  });

  it('a spit tower kills a slinger that walks into range', () => {
    const camp = { tier: 0, seed: 0, buildings: [{ uid: 1, type: 'spit', col: 10, row: 5, hp: 480, maxHp: 480 }] };
    const sim = new RaidSim(camp, { slinger: 1 });
    const s = sim.deploy('slinger', { x: 400, y: 160 })!;
    run(sim, 20);
    expect(s.alive).toBe(false);
    expect(sim.ended).toBe(true);
    expect(sim.survivingArmy().slinger ?? 0).toBe(0);
  });

  it('mortars cannot hit owls', () => {
    const camp = { tier: 0, seed: 0, buildings: [{ uid: 1, type: 'mortar', col: 10, row: 5, hp: 620, maxHp: 620 }] };
    const sim = new RaidSim(camp, { owl: 1 });
    const owl = sim.deploy('owl', { x: 300, y: 300 })!;
    run(sim, 60);
    expect(owl.hp).toBe(owl.maxHp);
    expect(sim.destruction).toBe(1);
  });
});

import { newVillage, trainTroop, armyCapacity, armySpace } from '../src/systems/village';
describe('army training', () => {
  it('needs a Ranger Lodge, glowsap and free space', () => {
    const v = newVillage(0);
    const army: Record<string, number> = {};
    expect(trainTroop(v, army, 'brawler').ok).toBe(false); // no lodge
    v.buildings.push({ uid: 50, type: 'barracks', level: 1, col: 0, row: 0, upgradeEnds: null, lastCollect: 0 });
    v.glowsap = 10000;
    expect(armyCapacity(v)).toBe(10);
    for (let i = 0; i < 10; i++) expect(trainTroop(v, army, 'brawler').ok).toBe(true);
    expect(trainTroop(v, army, 'brawler').ok).toBe(false); // full
    expect(armySpace(army)).toBe(10);
    expect(trainTroop(v, {}, 'owl').ok).toBe(false); // needs lodge 2
  });
});

describe('camp walls', () => {
  const walled = () => ({
    tier: 0,
    seed: 0,
    buildings: [
      { uid: 1, type: 'hut', col: 12, row: 6, hp: 280, maxHp: 280 },
      { uid: 2, type: 'wall', col: 10, row: 6, hp: 320, maxHp: 320 },
      { uid: 3, type: 'wall', col: 10, row: 7, hp: 320, maxHp: 320 },
    ],
  });
  it('ground troops must break a wall in their way; walls do not count toward destruction', () => {
    const sim = new RaidSim(walled(), { brawler: 1 });
    const t = sim.deploy('brawler', { x: 300, y: CAMP_Y(7) })!;
    run(sim, 6);
    expect(t.wallUid).not.toBe(0);
    expect(sim.camp.buildings[0].hp).toBe(280);
    run(sim, 80);
    expect(sim.destruction).toBe(1);
  });
  it('sappers tear walls down fast and owls fly over', () => {
    const a = new RaidSim(walled(), { sapper: 1 });
    a.deploy('sapper', { x: 300, y: CAMP_Y(7) });
    run(a, 12);
    expect(a.camp.buildings.filter((b) => b.type === 'wall' && b.hp <= 0).length).toBeGreaterThan(0);
    const b = new RaidSim(walled(), { owl: 1 });
    const owl = b.deploy('owl', { x: 300, y: CAMP_Y(7) })!;
    run(b, 6);
    expect(owl.wallUid).toBe(0);
  });
  it('higher-tier camps are walled', () => {
    expect(generateCamp(4, 0).buildings.some((b) => b.type === 'wall')).toBe(false);
    expect(generateCamp(4, 1).buildings.filter((b) => b.type === 'wall').length).toBeGreaterThan(8);
  });
});
function CAMP_Y(row: number) {
  return 92 + row * 40 + 20;
}
