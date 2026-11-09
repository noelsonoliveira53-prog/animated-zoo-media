import { describe, expect, it } from 'vitest';
import { BattleSim } from '../src/systems/BattleSim';
import { LEVELS } from '../src/data/levels';

describe('callBonus (what the wave button shows is what a call pays)', () => {
  it('pays nothing for starting the first wave', () => {
    const sim = new BattleSim(LEVELS[2]);
    expect(sim.callBonus()).toBe(0);
  });
  it('matches the coins an early call actually adds', () => {
    const sim = new BattleSim(LEVELS[2]);
    sim.callNextWave();
    sim.update(1);
    const shown = sim.callBonus();
    expect(shown).toBeGreaterThan(0);
    const before = sim.coins;
    let paid = 0;
    sim.drainEvents();
    sim.callNextWave();
    for (const ev of sim.drainEvents()) if (ev.type === 'waveStart') paid = ev.bonus;
    expect(paid).toBe(shown);
    expect(sim.coins).toBeGreaterThanOrEqual(before + shown);
  });
});
