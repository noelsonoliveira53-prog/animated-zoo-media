import { describe, expect, it } from 'vitest';
import { dailyFor, todayString } from '../src/systems/daily';
import { combine, DAILY_MODIFIERS } from '../src/data/daily';
import { BattleSim } from '../src/systems/BattleSim';
import { LEVELS } from '../src/data/levels';

describe('daily challenge', () => {
  it('is deterministic per date and limited to unlocked levels', () => {
    expect(dailyFor('2026-11-07', 5)).toEqual(dailyFor('2026-11-07', 5));
    for (let d = 1; d <= 28; d++) {
      const c = dailyFor(`2026-02-${String(d).padStart(2, '0')}`, 3);
      expect(c.levelIndex).toBeLessThan(3);
      expect(c.modifiers.length).toBe(2);
      expect(c.modifiers[0]).not.toBe(c.modifiers[1]);
      // the first twist always makes it harder
      expect(DAILY_MODIFIERS.find((m) => m.id === c.modifiers[0])!.good).toBeFalsy();
    }
  });
  it('varies across days', () => {
    const set = new Set(Array.from({ length: 20 }, (_, d) => JSON.stringify(dailyFor(`2026-03-${String(d + 1).padStart(2, '0')}`, 15).modifiers)));
    expect(set.size).toBeGreaterThan(4);
  });
  it('formats local dates', () => {
    expect(todayString(new Date(2026, 0, 5))).toBe('2026-01-05');
  });
  it('modifiers change the battle', () => {
    const lvl = LEVELS[0];
    const m = combine(['thrifty', 'glass', 'nospells', 'nohero', 'rich']);
    const sim = new BattleSim(lvl, 'bramble', { mods: m });
    expect(sim.hero).toBeNull();
    expect(sim.lives).toBe(5);
    expect(sim.coins).toBe(Math.round(lvl.startCoins * 1.5));
    expect(sim.price(100)).toBe(80);
    expect(sim.castSpell('starfall', { x: 300, y: 300 })).toBe(false);
    const fast = new BattleSim(lvl, null, { mods: combine(['swift', 'tough']) });
    const normal = new BattleSim(lvl, null);
    const a = fast.spawn('mudling');
    const b = normal.spawn('mudling');
    expect(a.maxHp).toBeGreaterThan(b.maxHp);
    fast.status = normal.status = 'running';
    fast.update(1);
    normal.update(1);
    expect(a.dist).toBeGreaterThan(b.dist);
  });
});
