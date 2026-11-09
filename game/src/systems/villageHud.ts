import { builders, busyBuilders, capacity, type VillageState } from './village';

/** What the village HUD shows: fill of each store, whether it's full, and one busy/free flag per builder. */
export interface VillageHud {
  coinFrac: number;
  sapFrac: number;
  coinFull: boolean;
  sapFull: boolean;
  builders: boolean[]; // true = busy, busy ones first
}

export function villageHud(v: VillageState, now: number): VillageHud {
  const cap = Math.max(1, capacity(v));
  const total = builders(v);
  const busy = Math.min(total, busyBuilders(v, now));
  return {
    coinFrac: Math.min(1, v.coins / cap),
    sapFrac: Math.min(1, v.glowsap / cap),
    coinFull: v.coins >= cap,
    sapFull: v.glowsap >= cap,
    builders: Array.from({ length: total }, (_, i) => i < busy),
  };
}
