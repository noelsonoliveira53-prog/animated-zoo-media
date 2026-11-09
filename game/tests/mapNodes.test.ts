import { describe, expect, it } from 'vitest';
import { LEVELS } from '../src/data/levels';
import { laurelFor, levelHasBoss } from '../src/systems/mapNodes';

describe('world map nodes', () => {
  it('flags boss levels, and the first level has no boss', () => {
    expect(levelHasBoss(LEVELS[0])).toBe(false);
    const bosses = LEVELS.filter(levelHasBoss).length;
    expect(bosses).toBeGreaterThan(10);
    expect(bosses).toBeLessThan(LEVELS.length);
  });
  it('picks a laurel per star count', () => {
    expect(laurelFor(0)).toBe('none');
    expect(laurelFor(1)).toBe('green');
    expect(laurelFor(2)).toBe('green');
    expect(laurelFor(3)).toBe('gold');
  });
});
