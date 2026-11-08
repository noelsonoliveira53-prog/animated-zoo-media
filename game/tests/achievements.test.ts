import { describe, expect, it } from 'vitest';
import { HERO_ORDER } from '../src/data/heroes';
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
    for (const h of HERO_ORDER.slice(2)) s = bumpStats(s, { [`wins_hero_${h}`]: 1 });
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

describe('Moonwatcher and Mudlark', () => {
  it('track the shrine level and Sludge Pits destroyed', () => {
    const moon = ACHIEVEMENTS.find((a) => a.id === 'moonwatch')!;
    const mud = ACHIEVEMENTS.find((a) => a.id === 'mudlark')!;
    const s = defaultSave();
    expect(moon.progress(s)).toBe(0);
    const v = ensureVillage(s);
    v.buildings.push({ uid: 50, type: 'shrine', level: 3, col: 0, row: 0, upgradeEnds: null, lastCollect: 0 });
    expect(moon.progress(s)).toBe(3);
    s.stats = { ...s.stats, sludgeDestroyed: 4 };
    expect(mud.progress(s)).toBe(4);
  });
});

describe('Highcanopy finale', () => {
  it('Crownmane has an achievement, a story card and a place in endless', async () => {
    const { STORY } = await import('../src/data/story');
    const { ENDLESS } = await import('../src/data/endless');
    const { ENEMIES } = await import('../src/data/enemies');
    const s = bumpStats(defaultSave(), { boss_crownmane: 1 });
    expect(checkAchievements(s).unlocked.map((a) => a.id)).toContain('boss_crownmane');
    expect(STORY.l90).toBeDefined();
    expect(ENDLESS.bosses).toContain('crownmane');
    const b = ENEMIES.crownmane;
    expect(b.boss && b.rile && b.snatch && b.phases?.length).toBeTruthy();
  });
});

describe('Honeycomb finale', () => {
  it('Goldwing has an achievement, a story card and a place in endless', async () => {
    const { STORY } = await import('../src/data/story');
    const { ENDLESS } = await import('../src/data/endless');
    const { ENEMIES } = await import('../src/data/enemies');
    const s = bumpStats(defaultSave(), { boss_combqueen: 1 });
    expect(checkAchievements(s).unlocked.map((a) => a.id)).toContain('boss_combqueen');
    expect(STORY.l95).toBeDefined();
    expect(ENDLESS.bosses).toContain('combqueen');
    const b = ENEMIES.combqueen;
    expect(b.boss && b.wax && b.parry && b.phases?.length).toBeTruthy();
  });
});
