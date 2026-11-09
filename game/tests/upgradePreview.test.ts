import { describe, expect, it } from 'vitest';
import { BUILDINGS, type BuildingId } from '../src/data/buildings';
import { upgradePreview } from '../src/systems/upgradePreview';

describe('upgradePreview', () => {
  it('is empty at max level', () => {
    for (const id of Object.keys(BUILDINGS) as BuildingId[]) expect(upgradePreview(id, BUILDINGS[id].levels.length)).toEqual([]);
  });
  it('only lists stats that change, at most three', () => {
    for (const id of Object.keys(BUILDINGS) as BuildingId[]) {
      for (let lv = 0; lv < BUILDINGS[id].levels.length; lv++) {
        const rows = upgradePreview(id, lv);
        expect(rows.length).toBeLessThanOrEqual(3);
        for (const r of rows) expect(r.cur).not.toBe(r.next);
      }
    }
  });
  it('shows production going up for a producer', () => {
    const id = (Object.keys(BUILDINGS) as BuildingId[]).find((k) => BUILDINGS[k].levels[1]?.produces)!;
    const rows = upgradePreview(id, 1);
    const ph = rows.find((r) => r.label === 'Per hour')!;
    expect(Number(ph.next)).toBeGreaterThan(Number(ph.cur));
  });
  it('workshop shows the tower damage bonus step', () => {
    expect(upgradePreview('workshop', 1)).toContainEqual({ label: 'Tower damage', cur: '+5%', next: '+10%' });
  });
});
