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
