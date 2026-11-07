import { describe, expect, it } from 'vitest';
import { buildSchedule, earlyCallBonus, waveEnemyCount } from '../src/systems/waves';
import { LEVELS } from '../src/data/levels';
import { ENEMIES } from '../src/data/enemies';

describe('wave schedules', () => {
  it('flattens groups into a sorted schedule', () => {
    const s = buildSchedule({
      groups: [
        { enemy: 'a', count: 2, interval: 2 },
        { enemy: 'b', count: 2, interval: 1, delay: 1 },
      ],
    });
    expect(s.map((e) => [e.time, e.enemy])).toEqual([
      [0, 'a'],
      [1, 'b'],
      [2, 'a'],
      [2, 'b'],
    ]);
  });
  it('counts enemies', () => {
    expect(waveEnemyCount({ groups: [{ enemy: 'a', count: 3, interval: 1 }, { enemy: 'b', count: 4, interval: 1 }] })).toBe(7);
  });
  it('gives no bonus when the countdown is over', () => {
    expect(earlyCallBonus(0, 3)).toBe(0);
    expect(earlyCallBonus(10, 0)).toBe(10);
  });
  it('every level references only known enemies', () => {
    for (const l of LEVELS) for (const w of l.waves) for (const g of w.groups) expect(ENEMIES[g.enemy], `${l.id}:${g.enemy}`).toBeDefined();
  });
});
