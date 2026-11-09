import { describe, expect, it } from 'vitest';
import { AIR_LIFT, pickEnemy } from '../src/systems/enemyPick';
import type { Enemy } from '../src/systems/BattleSim';

const foe = (x: number, y: number, radius = 12, flying = false, hp = 10) => ({ pos: { x, y }, hp, def: { radius, flying } }) as unknown as Enemy;

describe('pickEnemy', () => {
  it('picks the closest foe under the tap', () => {
    const a = foe(100, 100);
    const b = foe(110, 100);
    expect(pickEnemy([a, b], 108, 100)).toBe(b);
  });
  it('misses when the tap is too far', () => {
    expect(pickEnemy([foe(100, 100)], 140, 100)).toBeNull();
  });
  it('uses the lifted body for flyers', () => {
    const f = foe(100, 100, 12, true);
    expect(pickEnemy([f], 100, 100 - AIR_LIFT)).toBe(f);
    expect(pickEnemy([f], 100, 100 + 20)).toBeNull();
  });
  it('ignores dead foes', () => {
    expect(pickEnemy([foe(100, 100, 12, false, 0)], 100, 100)).toBeNull();
  });
});
