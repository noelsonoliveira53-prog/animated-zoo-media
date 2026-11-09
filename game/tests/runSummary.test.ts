import { describe, expect, it } from 'vitest';
import { runSummary, shortNum } from '../src/systems/runSummary';
import { BattleSim } from '../src/systems/BattleSim';
import { LEVELS } from '../src/data/levels';

describe('runSummary', () => {
  it('picks the tower with the most damage', () => {
    const r = runSummary({ 'tower:3': 500, 'tower:7': 900, hero: 120, spell: 300 }, { 'tower:7': 12, hero: 2 }, 3, { 3: 'Thornbow Nest', 7: 'Quake Mortar' });
    expect(r.top).toEqual({ name: 'Quake Mortar', damage: 900, kills: 12 });
    expect(r.hero).toEqual({ damage: 120, kills: 2 });
    expect(r.spellsCast).toBe(3);
  });
  it('handles no towers and sold towers', () => {
    expect(runSummary({ hero: 10 }, {}, 0, {}).top).toBeNull();
    expect(runSummary({ 'tower:9': 50 }, {}, 0, {}).top!.name).toBe('A sold tower');
  });
  it('shortens big numbers', () => {
    expect(shortNum(950)).toBe('950');
    expect(shortNum(12345)).toBe('12.3k');
    expect(shortNum(123456)).toBe('123k');
  });
});

describe('sim tallies damage and kills by source', () => {
  it('tower damage never exceeds the health of the foes it killed or hurt, and kills add up', () => {
    const sim = new BattleSim(LEVELS[0]);
    sim.coins = 5000;
    sim.level.slots.forEach((_, k) => sim.build(k, 'thornbow'));
    sim.callNextWave();
    for (let i = 0; i < 60 * 120 && sim.status === 'running'; i++) sim.update(1 / 60);
    const towerDmg = Object.entries(sim.dmgBy).filter(([k]) => k.startsWith('tower:')).reduce((a, [, v]) => a + v, 0);
    const towerKills = Object.entries(sim.killsBy).filter(([k]) => k.startsWith('tower:')).reduce((a, [, v]) => a + v, 0);
    expect(towerDmg).toBeGreaterThan(0);
    expect(towerKills).toBeGreaterThan(0);
    const allKills = Object.values(sim.killsBy).reduce((a, b) => a + b, 0);
    expect(allKills).toBeGreaterThanOrEqual(towerKills);
  });
  it('counts spells cast', () => {
    const sim = new BattleSim(LEVELS[2]);
    sim.callNextWave();
    sim.update(1);
    const before = sim.spellsCast;
    sim.castSpell('starfall', { x: 400, y: 300 });
    expect(sim.spellsCast).toBe(before + 1);
  });
});
