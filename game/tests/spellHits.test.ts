import { describe, expect, it } from 'vitest';
import { BattleSim } from '../src/systems/BattleSim';
import { LEVELS } from '../src/data/levels';

function setup() {
  const sim = new BattleSim(LEVELS[2]);
  const walker = sim.spawn('shellback', 0, 300);
  const flyer = sim.spawn('gloomwing', 0, 300);
  sim.update(1 / 60);
  return { sim, walker, flyer };
}

describe('spellHits (cast and preview share the same rules)', () => {
  it('a falling star hits walkers and flyers', () => {
    const { sim, walker, flyer } = setup();
    const hits = sim.spellHits('starfall', walker.pos);
    expect(hits).toContain(walker);
    if (Math.hypot(flyer.pos.x - walker.pos.x, flyer.pos.y - walker.pos.y) < 40) expect(hits).toContain(flyer);
  });
  it('a snare grabs only walkers', () => {
    const { sim, walker, flyer } = setup();
    const hits = sim.spellHits('thornsnare', walker.pos);
    expect(hits).toContain(walker);
    expect(hits).not.toContain(flyer);
  });
  it('reinforcements hit no one, and far away hits no one', () => {
    const { sim, walker } = setup();
    expect(sim.spellHits('grovecall', walker.pos)).toEqual([]);
    expect(sim.spellHits('starfall', { x: walker.pos.x + 900, y: walker.pos.y + 900 })).toEqual([]);
  });
});
