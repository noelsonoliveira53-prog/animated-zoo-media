import { describe, expect, it } from 'vitest';
import { enemyStatuses, iconX, soldierStatuses } from '../src/systems/statusIcons';

const calm = { slowTime: 0, slowFactor: 1, hasteTime: 0, hasteMult: 1, speedMult: 1, anchored: false };

describe('status icons', () => {
  it('a calm enemy shows none', () => {
    expect(enemyStatuses(calm)).toEqual([]);
  });
  it('shows each enemy status in a fixed order', () => {
    expect(enemyStatuses({ ...calm, slowTime: 1, slowFactor: 0.5 })).toEqual(['slow']);
    expect(enemyStatuses({ slowTime: 1, slowFactor: 0.6, hasteTime: 2, hasteMult: 1.4, speedMult: 1.5, anchored: true })).toEqual(['slow', 'haste', 'rage', 'anchor']);
  });
  it('ignores a slow that has run out or does nothing', () => {
    expect(enemyStatuses({ ...calm, slowTime: 0, slowFactor: 0.5 })).toEqual([]);
    expect(enemyStatuses({ ...calm, slowTime: 2, slowFactor: 1 })).toEqual([]);
  });
  it('shows soldier statuses', () => {
    expect(soldierStatuses({})).toEqual([]);
    expect(soldierStatuses({ poisonT: 2, glazed: 1, stun: 0.5 })).toEqual(['poison', 'glaze', 'stun']);
    expect(soldierStatuses({ poisonT: 0, stun: 1 })).toEqual(['stun']);
  });
  it('lays icons out in a row', () => {
    expect([0, 1, 2].map((k) => iconX(100, k))).toEqual([100, 112, 124]);
  });
});
