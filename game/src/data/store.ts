import type { Cost } from './buildings';

// The Keeper's Store: permanent upgrades bought with village coins and glowsap. Items are grouped into tiers;
// a tier opens once enough ranks have been bought in the tiers before it.

export type StoreEffect = 'towerDamage' | 'startCoins' | 'heroHp' | 'spellCd' | 'rangers' | 'bounty';

export interface StoreItem {
  id: string;
  name: string;
  text: string; // what one rank does, for the store card
  tier: 1 | 2 | 3;
  maxRank: number;
  /** Price of the first rank; rank n (0-based) costs (n + 1) × this. */
  cost: Cost;
  /** Per-rank effects (several for combined items). */
  effects: { kind: StoreEffect; per: number }[];
  color: number;
}

export const STORE_TIERS: { tier: 1 | 2 | 3; name: string; needRanks: number }[] = [
  { tier: 1, name: 'Apprentice Wares', needRanks: 0 },
  { tier: 2, name: 'Journeyman Wares', needRanks: 5 },
  { tier: 3, name: 'Master Wares', needRanks: 10 },
];

export const STORE_ITEMS: StoreItem[] = [
  { id: 'whetted', name: 'Whetted Tips', text: '+3% damage for every tower', tier: 1, maxRank: 5, cost: { coins: 400, glowsap: 200 }, effects: [{ kind: 'towerDamage', per: 0.03 }], color: 0xffd060 },
  { id: 'warchest', name: 'War Chest', text: '+20 starting coins in every battle', tier: 1, maxRank: 5, cost: { coins: 300, glowsap: 150 }, effects: [{ kind: 'startCoins', per: 20 }], color: 0xffb040 },
  { id: 'stew', name: 'Hearty Stew', text: '+6% hero health', tier: 1, maxRank: 3, cost: { coins: 350, glowsap: 250 }, effects: [{ kind: 'heroHp', per: 0.06 }], color: 0xff8a6a },
  { id: 'runes', name: 'Quickened Runes', text: 'Spells recharge 5% faster', tier: 2, maxRank: 3, cost: { coins: 1200, glowsap: 900 }, effects: [{ kind: 'spellCd', per: 0.05 }], color: 0xb07cff },
  { id: 'drill', name: 'Ranger Drill', text: 'Grove Call rangers +12% health and damage', tier: 2, maxRank: 3, cost: { coins: 1000, glowsap: 800 }, effects: [{ kind: 'rangers', per: 0.12 }], color: 0x8fdc5a },
  { id: 'charms', name: 'Lucky Charms', text: 'Kills pay +4% coins', tier: 2, maxRank: 3, cost: { coins: 1100, glowsap: 700 }, effects: [{ kind: 'bounty', per: 0.04 }], color: 0x6ad8c8 },
  { id: 'mastercraft', name: 'Master Craft', text: '+4% damage for every tower', tier: 3, maxRank: 3, cost: { coins: 3000, glowsap: 2400 }, effects: [{ kind: 'towerDamage', per: 0.04 }], color: 0xffe8a0 },
  { id: 'blessing', name: 'Elder Blessing', text: '+8% hero health and spells 4% faster', tier: 3, maxRank: 2, cost: { coins: 3400, glowsap: 3000 }, effects: [{ kind: 'heroHp', per: 0.08 }, { kind: 'spellCd', per: 0.04 }], color: 0xd8a8ff },
  { id: 'hoard', name: "Dragon's Hoard", text: '+40 starting coins and kills pay +5%', tier: 3, maxRank: 2, cost: { coins: 3200, glowsap: 2600 }, effects: [{ kind: 'startCoins', per: 40 }, { kind: 'bounty', per: 0.05 }], color: 0xffc83a },
];
