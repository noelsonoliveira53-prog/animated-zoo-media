import { describe, expect, it } from 'vitest';
import { LEVELS, isLevelUnlocked, setAllLevelsOpen } from '../src/data/levels';

describe('dev mode', () => {
  it('opens every level while on, and restores the normal locks when off', () => {
    expect(isLevelUnlocked(LEVELS.length - 1, {})).toBe(false);
    setAllLevelsOpen(true);
    expect(isLevelUnlocked(LEVELS.length - 1, {})).toBe(true);
    expect(isLevelUnlocked(LEVELS.length, {})).toBe(false);
    setAllLevelsOpen(false);
    expect(isLevelUnlocked(LEVELS.length - 1, {})).toBe(false);
    expect(isLevelUnlocked(1, { [LEVELS[0].id]: 1 })).toBe(true);
  });
});
