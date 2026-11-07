import { describe, expect, it } from 'vitest';
import { computeDamage } from '../src/systems/combat';

describe('computeDamage', () => {
  const plain = { armor: 0, magicResist: 0 };
  const armored = { armor: 0.6, magicResist: 0 };
  const warded = { armor: 0, magicResist: 0.5 };

  it('passes damage through with no resistances', () => {
    expect(computeDamage(10, 'physical', plain)).toBe(10);
    expect(computeDamage(10, 'magic', plain)).toBe(10);
  });
  it('armor reduces physical but not magic', () => {
    expect(computeDamage(10, 'physical', armored)).toBe(4);
    expect(computeDamage(10, 'magic', armored)).toBe(10);
  });
  it('magic resist reduces magic but not physical', () => {
    expect(computeDamage(10, 'magic', warded)).toBe(5);
    expect(computeDamage(10, 'physical', warded)).toBe(10);
  });
  it('true damage ignores everything', () => {
    expect(computeDamage(10, 'true', { armor: 0.9, magicResist: 0.9 })).toBe(10);
  });
  it('caps resistance at 90% and floors hits at 1', () => {
    expect(computeDamage(10, 'physical', { armor: 5, magicResist: 0 })).toBe(1);
    expect(computeDamage(1, 'physical', { armor: 0.9, magicResist: 0 })).toBe(1);
    expect(computeDamage(0, 'physical', plain)).toBe(0);
  });
});
