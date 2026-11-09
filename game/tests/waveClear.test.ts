import { describe, expect, it } from 'vitest';
import { waveClearInfo } from '../src/systems/waveClear';
import { BattleSim } from '../src/systems/BattleSim';
import { LEVELS } from '../src/data/levels';

describe('waveClearInfo', () => {
  it('names the wave and counts what is left', () => {
    expect(waveClearInfo(0, [], 12, false)).toEqual({ title: 'Wave 1 cleared', flawless: true, left: '11 waves to go' });
    expect(waveClearInfo(10, [], 12, false).left).toBe('1 wave to go');
    expect(waveClearInfo(4, [0, 0, 0, 0, 2], 12, false).flawless).toBe(false);
    expect(waveClearInfo(4, [], 0, true).left).toBe('');
  });
});

describe('sim announces a cleared wave', () => {
  it('fires waveCleared once the first wave is gone', () => {
    const sim = new BattleSim(LEVELS[0]);
    sim.coins = 5000;
    sim.level.slots.forEach((_, k) => { sim.build(k, 'thornbow'); sim.upgrade(k); });
    sim.callNextWave();
    let cleared = -1;
    for (let i = 0; i < 60 * 120 && cleared < 0; i++) {
      sim.update(1 / 60);
      for (const ev of sim.drainEvents()) if (ev.type === 'waveCleared') cleared = ev.index;
    }
    expect(cleared).toBe(0);
  });
});
