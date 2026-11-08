import { describe, expect, it } from 'vitest';
import { LEVELS } from '../src/data/levels';
import { weatherFor } from '../src/data/weather';

describe('battle weather', () => {
  it('keeps snow and lava maps on their own effects', () => {
    const snowy = LEVELS.find((l) => l.theme.snow)!;
    expect(weatherFor(snowy.theme).kind).toBe('none');
    const hot = LEVELS.find((l) => l.theme.lava)!;
    expect(weatherFor(hot.theme).kind).toBe('none');
  });
  it('gives every other map some weather, with colours and a spawn rate', () => {
    for (const l of LEVELS) {
      const w = weatherFor(l.theme);
      if (w.kind === 'none') continue;
      expect(w.colors.length, l.id).toBeGreaterThan(0);
      expect(w.every, l.id).toBeGreaterThan(0);
    }
    expect(weatherFor(LEVELS[0].theme).kind).toBe('leaves');
  });
});

import { ambienceFor } from '../src/data/weather';
describe('battle ambience', () => {
  it('maps themes to a bed', () => {
    expect(ambienceFor(LEVELS[0].theme)).toBe('meadow');
    expect(ambienceFor(LEVELS.find((l) => l.theme.lava)!.theme)).toBe('crackle');
    expect(ambienceFor(LEVELS.find((l) => l.theme.storm)!.theme)).toBe('rain');
    expect(ambienceFor(LEVELS.find((l) => l.theme.snow)!.theme)).toBe('wind');
  });
});
