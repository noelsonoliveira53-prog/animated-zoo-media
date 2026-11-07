import { describe, expect, it } from 'vitest';
import { ACHIEVEMENTS } from '../src/data/achievements';
import { checkAchievements } from '../src/systems/achievements';
import { bumpStats, defaultSave, ensureVillage } from '../src/systems/save';

describe('achievements', () => {
  it('have unique ids and positive goals', () => {
    const ids = new Set(ACHIEVEMENTS.map((a) => a.id));
    expect(ids.size).toBe(ACHIEVEMENTS.length);
    for (const a of ACHIEVEMENTS) expect(a.goal).toBeGreaterThan(0);
  });

  it('unlock once, pay their reward into the village, and never twice', () => {
    let s = defaultSave();
    ensureVillage(s, 0);
    const before = s.village!.coins;
    s = bumpStats(s, { wins: 1 });
    const r1 = checkAchievements(s);
    expect(r1.unlocked.map((a) => a.id)).toContain('first_win');
    expect(r1.save.village!.coins).toBe(before + 150);
    const r2 = checkAchievements(r1.save);
    expect(r2.unlocked).toEqual([]);
  });

  it('track progress from stats, stars and max counters', () => {
    let s = defaultSave();
    s = bumpStats(s, { kills: 300 });
    s = bumpStats(s, { kills: 250 }, { heroMaxLevel: 4 });
    s = bumpStats(s, {}, { heroMaxLevel: 2 });
    expect(s.stats.kills).toBe(550);
    expect(s.stats.heroMaxLevel).toBe(4);
    const ids = checkAchievements(s).unlocked.map((a) => a.id);
    expect(ids).toContain('kills500');
    expect(ids).not.toContain('hero_max');
    const stars = { ...defaultSave(), stars: { l1: 3, l2: 3, l3: 3, l4: 3, l5: 3 } };
    expect(checkAchievements(stars).unlocked.map((a) => a.id)).toContain('stars15');
  });
});

describe('hero achievements', () => {
  const ach = (id: string) => ACHIEVEMENTS.find((a) => a.id === id)!;
  it('Full Roster counts distinct heroes with a win', () => {
    let s = defaultSave();
    s = bumpStats(s, { wins_hero_bramble: 1 });
    s = bumpStats(s, { wins_hero_bramble: 1, wins_hero_fen: 1 });
    expect(ach('full_roster').progress(s)).toBe(2);
    for (const h of ['ember', 'wren', 'sorrel']) s = bumpStats(s, { [`wins_hero_${h}`]: 1 });
    expect(checkAchievements(s).unlocked.map((a) => a.id)).toContain('full_roster');
  });
  it('Field Medic accumulates soldier healing across battles', () => {
    let s = defaultSave();
    s = bumpStats(s, { soldierHealing: 1800 });
    s = bumpStats(s, { soldierHealing: 1300 });
    expect(ach('field_medic').progress(s)).toBe(3100);
    expect(checkAchievements(s).unlocked.map((a) => a.id)).toContain('field_medic');
  });
});
