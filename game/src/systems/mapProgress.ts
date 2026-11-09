import { LEVELS, REGIONS, isLevelUnlocked } from '../data/levels';

/** Progress shown on the world map's top ribbon for one region. */
export interface RegionProgress {
  stars: number; // collected in this region
  max: number; // 3 per level in it
  next: { index: number; name: string } | null; // the first unlocked level here still missing a star, or null when all have one
  done: boolean; // every level in the region has 3 stars
}

export function regionProgress(region: number, stars: Record<string, number>): RegionProgress {
  const r = REGIONS[region];
  const ids: number[] = [];
  for (let i = r.first; i < Math.min(LEVELS.length, r.first + r.count); i++) ids.push(i);
  const got = ids.reduce((n, i) => n + (stars[LEVELS[i].id] ?? 0), 0);
  const nextI = ids.find((i) => isLevelUnlocked(i, stars) && (stars[LEVELS[i].id] ?? 0) === 0);
  return {
    stars: got,
    max: ids.length * 3,
    next: nextI === undefined ? null : { index: nextI, name: LEVELS[nextI].name },
    done: ids.length > 0 && got === ids.length * 3,
  };
}
