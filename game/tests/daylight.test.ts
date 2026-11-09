import { describe, expect, it } from 'vitest';
import { dayLight } from '../src/systems/daylight';

describe('village daylight', () => {
  it('cycles through dawn, day, golden hour and night', () => {
    expect(dayLight(7).name).toBe('dawn');
    expect(dayLight(12).name).toBe('day');
    expect(dayLight(12).alpha).toBe(0);
    expect(dayLight(17).name).toBe('golden');
    expect(dayLight(17).windows).toBe(false);
    expect(dayLight(18).windows).toBe(true);
    expect(dayLight(22).name).toBe('night');
    expect(dayLight(3).windows).toBe(true);
    expect(dayLight(-1).name).toBe('night');
    expect(dayLight(26).name).toBe('night');
  });
});
