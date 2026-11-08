import { describe, expect, it } from 'vitest';
import { STORE_ITEMS, STORE_TIERS } from '../src/data/store';
import { buyItem, nextPrice, rankOf, tierOpen, totalRanks, withStorePerks } from '../src/systems/store';
import { defaultSave, ensureVillage, loadSave, writeSave } from '../src/systems/save';
import { battlePerks } from '../src/systems/village';

const rich = () => {
  const s = defaultSave();
  const v = ensureVillage(s, 0);
  v.coins = 1e7;
  v.glowsap = 1e7;
  return s;
};

describe('Keeper\'s Store', () => {
  it('has unique ids, every tier stocked, and tiers that open in order', () => {
    expect(new Set(STORE_ITEMS.map((i) => i.id)).size).toBe(STORE_ITEMS.length);
    for (const t of STORE_TIERS) expect(STORE_ITEMS.some((i) => i.tier === t.tier)).toBe(true);
    const s = rich();
    expect(tierOpen(s, 1)).toBe(true);
    expect(tierOpen(s, 2)).toBe(false);
    expect(buyItem(s, 'runes').ok).toBe(false); // tier 2 is still locked
  });

  it('charges a rising price per rank, stops at max rank and unlocks the next tier', () => {
    const s = rich();
    const v = ensureVillage(s);
    const item = STORE_ITEMS.find((i) => i.id === 'whetted')!;
    const c0 = v.coins;
    expect(buyItem(s, 'whetted').ok).toBe(true);
    expect(v.coins).toBe(c0 - item.cost.coins!);
    expect(nextPrice(s, item)!.coins).toBe(item.cost.coins! * 2);
    while (rankOf(s, 'whetted') < item.maxRank) expect(buyItem(s, 'whetted').ok).toBe(true);
    expect(buyItem(s, 'whetted')).toEqual({ ok: false, reason: 'Already at max rank' });
    expect(totalRanks(s)).toBe(5);
    expect(tierOpen(s, 2)).toBe(true);
    expect(buyItem(s, 'runes').ok).toBe(true);
  });

  it('refuses when the village cannot pay', () => {
    const s = defaultSave();
    const v = ensureVillage(s, 0);
    v.coins = 10;
    v.glowsap = 10;
    expect(buyItem(s, 'warchest')).toEqual({ ok: false, reason: 'Not enough resources' });
    expect(rankOf(s, 'warchest')).toBe(0);
  });

  it('folds ranks into the battle perks', () => {
    const s = rich();
    for (let k = 0; k < 5; k++) buyItem(s, 'whetted');
    for (let k = 0; k < 2; k++) buyItem(s, 'warchest');
    buyItem(s, 'runes');
    const base = battlePerks(s.village);
    const p = withStorePerks(base, s);
    expect(p.towerDamageMult).toBeCloseTo(base.towerDamageMult * 1.15);
    expect(p.bonusCoins).toBe(base.bonusCoins + 40);
    expect(p.spellCdMult).toBeCloseTo(base.spellCdMult * 0.95);
    expect(withStorePerks(base, defaultSave())).toEqual(base);
  });

  it('survives a save and load round trip', () => {
    const mem: Record<string, string> = {};
    const store = { getItem: (k: string) => mem[k] ?? null, setItem: (k: string, v: string) => { mem[k] = v; } };
    const s = rich();
    buyItem(s, 'stew');
    writeSave(s, store);
    expect(rankOf(loadSave(store), 'stew')).toBe(1);
  });
});
