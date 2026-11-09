import { describe, expect, it } from 'vitest';
import { STATUS_EFFECTS } from '../src/data/statusEffects';

describe('status effects guide data', () => {
  it('has six distinct effects with text for every field', () => {
    expect(STATUS_EFFECTS.length).toBe(6);
    expect(new Set(STATUS_EFFECTS.map((e) => e.id)).size).toBe(6);
    for (const e of STATUS_EFFECTS) {
      expect(e.name.length).toBeGreaterThan(2);
      expect(e.blurb.length).toBeGreaterThan(20);
      expect(e.sources.length).toBeGreaterThan(10);
      expect(e.counter.length).toBeGreaterThan(20);
    }
  });
});
