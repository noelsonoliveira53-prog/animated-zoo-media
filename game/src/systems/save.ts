// Persistent progress in localStorage. Every access is guarded: storage can be missing or throw.
import { newVillage, type QueuedTroop, type VillageState } from './village';

export interface SaveData {
  version: number;
  stars: Record<string, number>; // level id -> best stars (0-3)
  hero: string; // selected hero id
  village: VillageState | null; // created on first visit
  heroRanks: Record<string, number>; // persistent hero training (battle start level = rank + 1)
  army: Record<string, number>; // trained raid troops waiting at the Ranger Lodge
  trainQueue: QueuedTroop[]; // troops still training (finish in order)
  raidSeed: number; // rotates after each raid so new camps appear
  seenEnemies: string[]; // enemy ids met in battle (unlocks Field Guide entries)
  stats: Record<string, number>; // lifetime counters for achievements
  achievements: string[]; // unlocked achievement ids
  dailyDone: string; // date (YYYY-MM-DD) of the last completed daily challenge
  settings: { volume: number; muted: boolean; music: boolean };
}

export const SAVE_KEY = 'grovewatch.save.v1';

export function defaultSave(): SaveData {
  return { version: 1, stars: {}, hero: 'bramble', village: null, heroRanks: {}, army: {}, trainQueue: [], raidSeed: 1, seenEnemies: [], stats: {}, achievements: [], dailyDone: '', settings: { volume: 0.6, muted: false, music: true } };
}

export interface StorageLike {
  getItem(key: string): string | null;
  setItem(key: string, value: string): void;
}

function storage(): StorageLike | null {
  try {
    return typeof localStorage === 'undefined' ? null : localStorage;
  } catch {
    return null;
  }
}

export function loadSave(store: StorageLike | null = storage()): SaveData {
  const base = defaultSave();
  if (!store) return base;
  try {
    const raw = store.getItem(SAVE_KEY);
    if (!raw) return base;
    const parsed = JSON.parse(raw) as Partial<SaveData>;
    return {
      version: 1,
      stars: { ...base.stars, ...(parsed.stars ?? {}) },
      hero: typeof parsed.hero === 'string' ? parsed.hero : base.hero,
      village: parsed.village && Array.isArray(parsed.village.buildings) ? parsed.village : null,
      heroRanks: { ...(parsed.heroRanks ?? {}) },
      army: { ...(parsed.army ?? {}) },
      trainQueue: Array.isArray(parsed.trainQueue) ? parsed.trainQueue.filter((q) => q && typeof q.id === 'string' && typeof q.endsAt === 'number') : [],
      raidSeed: typeof parsed.raidSeed === 'number' ? parsed.raidSeed : 1,
      seenEnemies: Array.isArray(parsed.seenEnemies) ? parsed.seenEnemies.filter((x) => typeof x === 'string') : [],
      stats: { ...(parsed.stats ?? {}) },
      achievements: Array.isArray(parsed.achievements) ? parsed.achievements.filter((x) => typeof x === 'string') : [],
      dailyDone: typeof parsed.dailyDone === 'string' ? parsed.dailyDone : '',
      settings: { ...base.settings, ...(parsed.settings ?? {}) },
    };
  } catch {
    return base;
  }
}

export function writeSave(data: SaveData, store: StorageLike | null = storage()): boolean {
  if (!store) return false;
  try {
    store.setItem(SAVE_KEY, JSON.stringify(data));
    return true;
  } catch {
    return false;
  }
}

/** Record stars for a level, keeping the best result. */
export function recordStars(data: SaveData, levelId: string, stars: number): SaveData {
  const best = Math.max(data.stars[levelId] ?? 0, stars);
  return { ...data, stars: { ...data.stars, [levelId]: best } };
}

export function starsForLives(lives: number, maxLives: number): number {
  if (lives <= 0) return 0;
  const frac = lives / maxLives;
  if (frac >= 0.9) return 3;
  if (frac >= 0.5) return 2;
  return 1;
}

/** The village, creating the starter village on first use. */
export function ensureVillage(data: SaveData, now = Date.now()): VillageState {
  if (!data.village) data.village = newVillage(now);
  return data.village;
}

/** Remember enemies the player has met (adds new ids, keeps order, no duplicates). */
export function markSeen(data: SaveData, ids: Iterable<string>): SaveData {
  const set = new Set(data.seenEnemies);
  for (const id of ids) set.add(id);
  return { ...data, seenEnemies: [...set] };
}

/** Wipe all progress but keep settings. */
export function resetProgress(data: SaveData): SaveData {
  return { ...defaultSave(), settings: { ...data.settings } };
}

/** Add to lifetime counters (or raise a max-type counter with mode 'max'). */
export function bumpStats(data: SaveData, add: Record<string, number>, max: Record<string, number> = {}): SaveData {
  const stats = { ...data.stats };
  for (const [k, v] of Object.entries(add)) stats[k] = (stats[k] ?? 0) + v;
  for (const [k, v] of Object.entries(max)) stats[k] = Math.max(stats[k] ?? 0, v);
  return { ...data, stats };
}
