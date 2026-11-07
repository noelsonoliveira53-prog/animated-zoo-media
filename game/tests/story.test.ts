import { describe, expect, it } from 'vitest';
import { STORY } from '../src/data/story';
import { LEVELS, REGIONS } from '../src/data/levels';

describe('story cards', () => {
  it('every card belongs to a region finale and has a title and lines', () => {
    const finales = REGIONS.map((r) => LEVELS[r.first + r.count - 1]?.id).filter(Boolean);
    for (const [id, card] of Object.entries(STORY)) {
      expect(finales, id).toContain(id);
      expect(card.title.length).toBeGreaterThan(3);
      expect(card.lines.length).toBeGreaterThanOrEqual(2);
    }
  });
  it('every finished region after the Emberdeep has a card (the Emberdeep keeps its epilogue)', () => {
    REGIONS.forEach((r, i) => {
      const last = LEVELS[r.first + r.count - 1];
      if (!last || i < 3) return;
      expect(STORY[last.id], last.name).toBeDefined();
    });
  });
});
