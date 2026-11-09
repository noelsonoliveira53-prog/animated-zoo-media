import { STORE_ITEMS, STORE_TIERS, type StoreEffect, type StoreItem } from '../data/store';
import type { Cost } from '../data/buildings';
import type { SaveData } from './save';
import { ensureVillage } from './save';
import type { BattlePerks } from './village';

// Store logic: ranks owned, tier unlocks, prices, buying and the battle perks the upgrades grant.

export function rankOf(save: SaveData, id: string): number {
  return save.store?.[id] ?? 0;
}

export function totalRanks(save: SaveData, belowTier = 99): number {
  return STORE_ITEMS.filter((i) => i.tier < belowTier).reduce((n, i) => n + rankOf(save, i.id), 0);
}

export function tierOpen(save: SaveData, tier: number): boolean {
  const t = STORE_TIERS.find((x) => x.tier === tier);
  return !!t && totalRanks(save, tier) >= t.needRanks;
}

/** Price of the next rank, or null at max rank. */
export function nextPrice(save: SaveData, item: StoreItem): Cost | null {
  const r = rankOf(save, item.id);
  if (r >= item.maxRank) return null;
  return { coins: (item.cost.coins ?? 0) * (r + 1), glowsap: (item.cost.glowsap ?? 0) * (r + 1) };
}

export function buyItem(save: SaveData, id: string): { ok: boolean; reason?: string } {
  const item = STORE_ITEMS.find((i) => i.id === id);
  if (!item) return { ok: false, reason: 'Unknown item' };
  if (!tierOpen(save, item.tier)) return { ok: false, reason: 'Tier locked' };
  const price = nextPrice(save, item);
  if (!price) return { ok: false, reason: 'Already at max rank' };
  const v = ensureVillage(save);
  if (v.coins < (price.coins ?? 0) || v.glowsap < (price.glowsap ?? 0)) return { ok: false, reason: 'Not enough resources' };
  v.coins -= price.coins ?? 0;
  v.glowsap -= price.glowsap ?? 0;
  save.store = { ...(save.store ?? {}), [id]: rankOf(save, id) + 1 };
  return { ok: true };
}

function sum(save: SaveData, kind: StoreEffect): number {
  let total = 0;
  for (const i of STORE_ITEMS) for (const e of i.effects) if (e.kind === kind) total += e.per * rankOf(save, i.id);
  return total;
}

/** Fold the store's upgrades into the village's battle perks. */
export function withStorePerks(base: BattlePerks, save: SaveData): BattlePerks {
  return {
    towerDamageMult: base.towerDamageMult * (1 + sum(save, 'towerDamage')),
    bonusCoins: base.bonusCoins + Math.round(sum(save, 'startCoins')),
    rangerMult: base.rangerMult * (1 + sum(save, 'rangers')),
    spellCdMult: base.spellCdMult * (1 - Math.min(0.5, sum(save, 'spellCd'))),
    heroHpMult: base.heroHpMult * (1 + sum(save, 'heroHp')),
    weirBountyMult: base.weirBountyMult * (1 + sum(save, 'bounty')),
  };
}
