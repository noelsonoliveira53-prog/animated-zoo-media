import { describe, expect, it } from 'vitest';
import { TOWERS } from '../src/data/towers';
import type { TowerDef } from '../src/data/types';
import { cardRows, cardTags } from '../src/systems/towerCard';

const defs = Object.values(TOWERS) as TowerDef[];

describe('tower info card', () => {
  it('bars stay within 0..1 for every tier and branch', () => {
    for (const d of defs) for (const t of [...d.tiers, ...d.specs.map((s) => s.stats)]) {
      for (const r of cardRows(t)) { expect(r.value).toBeGreaterThan(0); expect(r.value).toBeLessThanOrEqual(1); }
    }
  });
  it('previews the next tier only where a stat changes', () => {
    for (const d of defs) for (let i = 0; i + 1 < d.tiers.length; i++) {
      const rows = cardRows(d.tiers[i], d.tiers[i + 1]);
      expect(rows.some((r) => r.next !== null)).toBe(true);
      for (const r of rows) if (r.next === null) expect(r.nextText).toBeNull();
    }
  });
  it('no preview when there is no next step', () => {
    for (const r of cardRows(defs[0].tiers[0])) expect(r.next).toBeNull();
  });
  it('barracks show warden rows, shooters show damage rows', () => {
    const barracks = defs.find((d) => d.tiers[0].soldiers)!;
    expect(cardRows(barracks.tiers[0]).map((r) => r.label)).toEqual(['Wardens', 'Melee', 'Reach']);
    const shooter = defs.find((d) => !d.tiers[0].soldiers)!;
    expect(cardRows(shooter.tiers[0]).map((r) => r.label)).toEqual(['Damage', 'Shots/s', 'Range']);
  });
  it('tags start with damage type and air, at most four', () => {
    for (const d of defs) for (const t of [...d.tiers, ...d.specs.map((s) => s.stats)]) {
      const tags = cardTags(d, t);
      expect(tags.length).toBeLessThanOrEqual(4);
      expect(['Physical', 'Magic', 'True dmg']).toContain(tags[0]);
    }
  });
});
