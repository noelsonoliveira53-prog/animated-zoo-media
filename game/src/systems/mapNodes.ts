import type { LevelDef } from '../data/types';
import { ENEMIES } from '../data/enemies';

/** Does any wave in this level bring a boss? (its world-map node wears a crest) */
export function levelHasBoss(level: LevelDef): boolean {
  return level.waves.some((w) => w.groups.some((g) => !!ENEMIES[g.enemy]?.boss));
}

/** Laurel style for a beaten node: none before the first win, green for 1–2 stars, gold for a perfect 3. */
export function laurelFor(stars: number): 'none' | 'green' | 'gold' {
  return stars <= 0 ? 'none' : stars >= 3 ? 'gold' : 'green';
}
