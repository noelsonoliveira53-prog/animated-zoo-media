import { describe, expect, it } from 'vitest';
import { waveChart } from '../src/systems/waveChart';
import { BattleSim } from '../src/systems/BattleSim';
import { LEVELS } from '../src/data/levels';

describe('waveChart', () => {
  it('scales to the worst wave and finds it', () => {
    const c = waveChart([0, 2, 0, 5, 1], 5);
    expect(c.worst).toBe(3);
    expect(c.total).toBe(8);
    expect(c.bars[3].h).toBe(1);
    expect(c.bars[1].h).toBeCloseTo(0.4);
  });
  it('a flawless run has no worst wave', () => {
    const c = waveChart([], 12);
    expect(c.bars).toHaveLength(12);
    expect(c.worst).toBe(-1);
    expect(c.total).toBe(0);
  });
  it('ties go to the earliest wave', () => {
    expect(waveChart([3, 3], 2).worst).toBe(0);
  });
});

describe('sim records lives lost per wave', () => {
  it('a leak is charged to the latest called wave and adds up to the lives lost', () => {
    const sim = new BattleSim(LEVELS[0]);
    sim.callNextWave();
    for (let i = 0; i < 60 * 240 && sim.status === 'running'; i++) sim.update(1 / 60); // no towers: everything leaks
    const lost = sim.maxLives - sim.lives;
    const total = sim.leaksByWave.reduce((a, b) => a + (b ?? 0), 0);
    expect(lost).toBeGreaterThan(0);
    expect(total).toBeGreaterThanOrEqual(lost); // lives floor at 0, the tally doesn't
  });
});
