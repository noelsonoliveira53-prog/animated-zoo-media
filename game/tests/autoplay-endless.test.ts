import { describe, expect, it } from 'vitest';
import { ENDLESS_EXPERT, STRATEGIES, playLevel } from '../src/systems/autoplay';
import { LEVELS } from '../src/data/levels';
import { makeEndlessLevel } from '../src/systems/endless';

describe('endless-aware expert', () => {
  it('only differs from the expert by deepening late (campaign strategies untouched)', () => {
    expect({ ...ENDLESS_EXPERT, name: STRATEGIES[0].name, upgradeFirstAfter: undefined }).toEqual({ ...STRATEGIES[0], upgradeFirstAfter: undefined });
    expect(STRATEGIES.every((s) => s.upgradeFirstAfter === undefined)).toBe(true);
  });
  it('holds at least as long as the plain expert on an endless map', () => {
    const lvl = makeEndlessLevel(LEVELS[4], 1);
    const plain = playLevel(lvl, STRATEGIES[0], 1, 20000).wavesReached;
    const deep = playLevel(makeEndlessLevel(LEVELS[4], 1), ENDLESS_EXPERT, 1, 20000).wavesReached;
    expect(deep).toBeGreaterThanOrEqual(plain);
  }, 120000);
});
