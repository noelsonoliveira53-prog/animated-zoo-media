import { describe, expect, it } from 'vitest';
import { villageHud } from '../src/systems/villageHud';
import { capacity, newVillage, upgradeBuilding } from '../src/systems/village';

describe('villageHud', () => {
  it('reports fills, full stores and builders', () => {
    const v = newVillage(Date.now());
    const cap = capacity(v);
    v.coins = cap;
    v.glowsap = cap / 2;
    const h = villageHud(v, Date.now());
    expect(h.coinFull).toBe(true);
    expect(h.sapFull).toBe(false);
    expect(h.sapFrac).toBeCloseTo(0.5);
    expect(h.builders.every((b) => !b)).toBe(true);
  });
  it('marks a builder busy while something is being built', () => {
    const v = newVillage(Date.now());
    v.coins = v.glowsap = capacity(v);
    const now = Date.now();
    const mine = v.buildings.find((b) => b.type !== 'townhall')!;
    expect(upgradeBuilding(v, mine.uid, now).ok).toBe(true);
    expect(villageHud(v, now + 1000).builders[0]).toBe(true);
  });
});
