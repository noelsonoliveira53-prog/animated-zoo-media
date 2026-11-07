import { describe, expect, it } from 'vitest';
import { ENEMIES } from '../src/data/enemies';
import { bossPhaseLines } from '../src/systems/guideInfo';

describe('boss phase lines', () => {
  it('describes every phase of every boss, with names not ids', () => {
    for (const e of Object.values(ENEMIES).filter((x) => x.boss)) {
      const lines = bossPhaseLines(e);
      expect(lines.length).toBe(e.phases!.length);
      for (const l of lines) {
        expect(l).toMatch(/^At \d+%: /);
        expect(l).not.toContain('undefined');
      }
    }
    expect(bossPhaseLines(ENEMIES.zephyrax)[1]).toBe('At 50%: shield 1200, summons 3 Cloudram');
    expect(bossPhaseLines(ENEMIES.mudling)).toEqual([]);
  });
});
