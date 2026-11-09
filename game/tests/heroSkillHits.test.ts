import { describe, expect, it } from 'vitest';
import { BattleSim } from '../src/systems/BattleSim';
import { LEVELS } from '../src/data/levels';

function near(hero: string) {
  const sim = new BattleSim(LEVELS[2], hero);
  const h = sim.hero!;
  const walker = sim.spawn('shellback', 0, 300);
  const flyer = sim.spawn('gloomwing', 0, 300);
  sim.update(1 / 60);
  h.pos.x = walker.pos.x + 10;
  h.pos.y = walker.pos.y;
  return { sim, walker, flyer };
}

describe('heroSkillHits (preview = what the skill hits)', () => {
  it('a quake skips flyers', () => {
    const { sim, walker, flyer } = near('bramble');
    const hits = sim.heroSkillHits();
    expect(hits).toContain(walker);
    expect(hits).not.toContain(flyer);
  });
  it('the skill hits exactly the previewed foes', () => {
    const { sim } = near('fen');
    const preview = sim.heroSkillHits().map((e) => e.uid).sort();
    sim.drainEvents();
    expect(sim.useHeroSkill()).toBe(true);
    const ev = sim.drainEvents().find((e) => e.type === 'heroSkill') as { hits: { uid: number }[] } | undefined;
    expect(ev!.hits.map((e) => e.uid).sort()).toEqual(preview);
  });
  it('no hero, no hits', () => {
    const sim = new BattleSim(LEVELS[2], null as unknown as string);
    expect(sim.heroSkillHits()).toEqual([]);
  });
});
