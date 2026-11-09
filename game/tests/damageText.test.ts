import { describe, expect, it } from 'vitest';
import { damageTextStyle } from '../src/systems/damageText';

describe('damage number style', () => {
  it('colours by damage type and grows for big hits and bosses', () => {
    expect(damageTextStyle(10, 500, 'physical', false).color).toBe('#fff4d6');
    expect(damageTextStyle(10, 500, 'magic', false).color).toBe('#d0a0ff');
    expect(damageTextStyle(10, 500, 'true', false).color).toBe('#ffd23c');
    expect(damageTextStyle(10, 500, undefined, false).color).toBe('#fff4d6');
    const small = damageTextStyle(10, 500, 'physical', false);
    const big = damageTextStyle(120, 500, 'physical', false);
    expect(small.big).toBe(false);
    expect(big.big).toBe(true);
    expect(big.size).toBeGreaterThan(small.size);
    expect(damageTextStyle(10, 500, 'physical', true).size).toBeGreaterThan(small.size);
  });
});
