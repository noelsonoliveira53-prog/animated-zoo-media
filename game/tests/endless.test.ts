import { describe, expect, it } from 'vitest';
import { ENDLESS } from '../src/data/endless';
import { ENEMIES } from '../src/data/enemies';
import { LEVELS } from '../src/data/levels';
import { BattleSim } from '../src/systems/BattleSim';
import { endlessPool, makeEndlessLevel, wavesHeld } from '../src/systems/endless';
import { defaultSave, loadSave, writeSave, type StorageLike } from '../src/systems/save';

describe('endless mode', () => {
  it('pool only uses real enemies and grows with the wave number', () => {
    for (const t of ENDLESS.tiers) for (const id of t.enemies) expect(ENEMIES[id], id).toBeTruthy();
    for (const id of ENDLESS.bosses) expect(ENEMIES[id]?.boss, id).toBe(true);
    expect(endlessPool(1).length).toBeLessThan(endlessPool(20).length);
  });
  it('generates valid, deterministic waves with bosses on schedule', () => {
    const a = makeEndlessLevel(LEVELS[1], 7);
    const b = makeEndlessLevel(LEVELS[1], 7);
    expect(a.waves).toEqual(b.waves);
    expect(a.waves).toHaveLength(ENDLESS.waves);
    expect(a.id).not.toBe(LEVELS[1].id);
    for (const w of a.waves) for (const g of w.groups) {
      expect(ENEMIES[g.enemy]).toBeTruthy();
      expect(g.path ?? 0).toBeLessThan(LEVELS[1].paths.length);
      expect(g.count).toBeGreaterThan(0);
    }
    const bossWave = a.waves[ENDLESS.bossEvery - 1];
    expect(bossWave.groups.some((g) => ENEMIES[g.enemy].boss)).toBe(true);
    expect(a.waves[0].groups.some((g) => ENEMIES[g.enemy].boss)).toBe(false);
  });
  it('enemy health ramps every wave', () => {
    const sim = new BattleSim(makeEndlessLevel(LEVELS[0]));
    const h0 = sim.waveHpMult();
    (sim as any).waveIndex = 10;
    expect(sim.waveHpMult()).toBeCloseTo(h0 * (1 + ENDLESS.hpRampPerWave * 10));
  });
  it('waves held counts finished waves', () => {
    expect(wavesHeld(-1)).toBe(0);
    expect(wavesHeld(5)).toBe(5);
  });
  it('best runs persist in the save', () => {
    const mem: Record<string, string> = {};
    const store: StorageLike = { getItem: (k) => mem[k] ?? null, setItem: (k, v) => void (mem[k] = v) };
    const s = defaultSave();
    s.endlessBest = { l3: 12 };
    writeSave(s, store);
    expect(loadSave(store).endlessBest.l3).toBe(12);
  });
});

describe('endless attack ramp', () => {
  it('enemy melee damage ramps with the wave in endless only', () => {
    const e = new BattleSim(makeEndlessLevel(LEVELS[0]));
    expect(e.attackMult()).toBe(1);
    (e as any).waveIndex = 10;
    expect(e.attackMult()).toBeCloseTo(1 + ENDLESS.attackRamp * 10);
    const c = new BattleSim(LEVELS[0]);
    (c as any).waveIndex = 10;
    expect(c.attackMult()).toBe(1);
  });
});

import { endlessMutatorFor, mutatorReward } from '../src/systems/endless';

describe('endless daily mutator', () => {
  it('is deterministic per date and comes from the endless mutator list', () => {
    expect(endlessMutatorFor('2026-11-07').id).toBe(endlessMutatorFor('2026-11-07').id);
    const seen = new Set<string>();
    for (let d = 1; d <= 28; d++) {
      const m = endlessMutatorFor(`2026-02-${String(d).padStart(2, '0')}`);
      expect(ENDLESS.mutators).toContain(m.id);
      seen.add(m.id);
    }
    expect(seen.size).toBeGreaterThan(2);
  });
  it('hard days pay more', () => {
    for (let d = 1; d <= 20; d++) {
      const m = endlessMutatorFor(`2026-03-${String(d).padStart(2, '0')}`);
      expect(mutatorReward(m)).toBe(m.good ? 1 : ENDLESS.hardMutatorReward);
    }
  });
});

import { endlessBosses, nativeEnemies } from '../src/systems/endless';

describe('endless home turf', () => {
  it("a map's own campaign enemies join its endless pool from nativeFrom, and its region boss comes second (after the gentlest)", () => {
    const lvl = LEVELS[77]; // Hollow Oak Crossing (Amberwood)
    expect(nativeEnemies(lvl)).toContain('sapstoat');
    expect(endlessBosses(lvl).slice(0, 2)).toEqual([ENDLESS.bosses[0], 'rustantler']);
    expect(new Set(endlessBosses(lvl)).size).toBe(ENDLESS.bosses.length); // nothing lost or doubled
    const run = makeEndlessLevel(lvl, 3);
    const used = (from: number, to: number) => new Set(run.waves.slice(from - 1, to).flatMap((w) => w.groups.map((g) => g.enemy)));
    const early = used(1, ENDLESS.nativeFrom - 1);
    for (const id of ['sapstoat', 'barkdrum', 'turnleaf']) expect(early.has(id)).toBe(false);
    const later = used(ENDLESS.nativeFrom, 30);
    expect(['sapstoat', 'barkdrum', 'turnleaf'].some((id) => later.has(id))).toBe(true);
    expect(run.waves[2 * ENDLESS.bossEvery - 1].groups.some((g) => g.enemy === 'rustantler')).toBe(true);
    expect(run.waves[ENDLESS.bossEvery - 1].groups.some((g) => g.enemy === ENDLESS.bosses[0])).toBe(true);
    // the first map keeps the classic opening boss
    expect(endlessBosses(LEVELS[0])[0]).toBe('murkmaw');
  });
});
