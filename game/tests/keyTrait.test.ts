import { describe, expect, it } from 'vitest';
import { ENEMIES } from '../src/data/enemies';
import { enemyKeyTrait } from '../src/systems/guideInfo';

describe('new-enemy key traits', () => {
  it('gives every enemy a short line, and flyers and bosses the right one', () => {
    for (const d of Object.values(ENEMIES)) {
      const t = enemyKeyTrait(d);
      expect(t.length).toBeGreaterThan(5);
      expect(t.length).toBeLessThan(70);
      if (d.boss) expect(t.startsWith('Boss')).toBe(true);
      else if (d.flying) expect(t.startsWith('Flies')).toBe(true);
    }
  });
});
