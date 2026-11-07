// Persistent progress in localStorage. Every access is guarded: storage can be missing or throw.

export interface SaveData {
  version: number;
  stars: Record<string, number>; // level id -> best stars (0-3)
  hero: string; // selected hero id
  settings: { volume: number; muted: boolean };
}

export const SAVE_KEY = 'grovewatch.save.v1';

export function defaultSave(): SaveData {
  return { version: 1, stars: {}, hero: 'bramble', settings: { volume: 0.6, muted: false } };
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
