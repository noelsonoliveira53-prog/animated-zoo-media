import { describe, it, expect } from 'vitest';
import { deathStyle, bigHit } from '../src/systems/deathStyle';
import { ENEMIES } from '../src/data/enemies';

describe('death styles', () => {
  const all = Object.values(ENEMIES);
  it('flyers shed feathers', () => {
    for (const d of all.filter((e) => e.flying)) expect(deathStyle(d).kind).toBe('feathers');
  });
  it('heavily armored walkers crack into shards', () => {
    const tank = all.find((e) => !e.flying && e.armor >= 0.4)!;
    expect(deathStyle(tank).kind).toBe('shards');
  });
  it('bosses are heavy and sizes stay in range', () => {
    for (const d of all) {
      const st = deathStyle(d);
      expect(st.size).toBeGreaterThanOrEqual(0.7);
      expect(st.size).toBeLessThanOrEqual(2.2);
      if (d.boss) expect(st.heavy).toBe(true);
    }
  });
  it('big hits need a sturdy target and a real chunk of health', () => {
    expect(bigHit(50, 100)).toBe(false);
    expect(bigHit(100, 600)).toBe(true);
    expect(bigHit(30, 600)).toBe(false);
  });
});
