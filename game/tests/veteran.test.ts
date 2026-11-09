import { describe, expect, it } from 'vitest';
import { justVeteran, towerRecord, VETERAN_KILLS } from '../src/systems/veteran';

describe('veteran towers', () => {
  it('reads a tower record from the tallies', () => {
    expect(towerRecord(4, { 'tower:4': 1234.6 }, { 'tower:4': 12 })).toEqual({ kills: 12, damage: 1235, veteran: false });
    expect(towerRecord(4, {}, { 'tower:4': VETERAN_KILLS }).veteran).toBe(true);
    expect(towerRecord(9, {}, {})).toEqual({ kills: 0, damage: 0, veteran: false });
  });
  it('pops the badge exactly once', () => {
    expect(justVeteran(VETERAN_KILLS - 1)).toBe(false);
    expect(justVeteran(VETERAN_KILLS)).toBe(true);
    expect(justVeteran(VETERAN_KILLS + 1)).toBe(false);
  });
});
