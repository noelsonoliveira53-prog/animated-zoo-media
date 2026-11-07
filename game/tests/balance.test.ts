import { describe, expect, it } from 'vitest';
import { LEVELS } from '../src/data/levels';
import { STRATEGIES, playLevel } from '../src/systems/autoplay';

// Balance guard rails, from the iteration-5 tuning. If a change breaks these, re-run
// `npx vite-node scripts/balance.ts` and update the Balance Notes.
const strat = (name: string) => STRATEGIES.find((s) => s.name === name)!;

describe('balance guard rails', () => {
  it('level 1 is winnable by a novice', () => {
    let wins = 0;
    for (let seed = 1; seed <= 4; seed++) if (playLevel(LEVELS[0], strat('novice'), seed).won) wins++;
    expect(wins).toBeGreaterThanOrEqual(3);
  });

  it('level 2 is winnable by a solid mixed defense', () => {
    for (let seed = 1; seed <= 3; seed++) expect(playLevel(LEVELS[1], strat('casual-mixed'), seed).won).toBe(true);
  });

  it('level 2 cannot be won with a single tower type', () => {
    for (const name of ['only-thornbow', 'only-glimmer', 'only-boulder', 'only-burrow']) {
      expect(playLevel(LEVELS[1], strat(name), 1).won, name).toBe(false);
    }
  });
});
