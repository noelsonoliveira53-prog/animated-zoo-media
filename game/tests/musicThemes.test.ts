import { describe, expect, it } from 'vitest';
import { REGION_THEMES, motifAt, MOODS, resolveMood, STINGERS, stingerSeconds, THEMES, themeById, themeForRegion } from '../src/data/musicThemes';
import { REGIONS } from '../src/data/levels';

describe('music themes', () => {
  it('every region has its own battle theme', () => {
    const ids = REGIONS.map((_, r) => themeForRegion(r).id);
    expect(new Set(ids).size).toBe(REGIONS.length);
    expect(ids).not.toContain('home');
  });
  it("each region plays its own region's theme, not a neighbour's", () => {
    const flag = (r: (typeof REGIONS)[number]) => (r.ruins ? 'ruins' : r.gale ? 'gale' : r.glass ? 'glass' : r.shoal ? 'shoal' : r.dusk ? 'dusk' : r.ember ? 'ember' : r.snow ? 'frost' : 'grove');
    REGIONS.forEach((reg, r) => expect(themeForRegion(r).id).toBe(flag(reg)));
    expect(REGION_THEMES.length).toBe(REGIONS.length);
  });
  it('unknown ids and regions fall back safely', () => {
    expect(themeById('nope').id).toBe('home');
    expect(themeForRegion(99).id).toBe(REGION_THEMES[REGION_THEMES.length - 1]);
    expect(themeForRegion(-1).id).toBe('grove');
  });
  it('motifs fit inside their two bars and play each note once per cycle', () => {
    for (const t of THEMES) {
      for (const [, step, len] of t.motif) {
        expect(step).toBeGreaterThanOrEqual(0);
        expect(step + len).toBeLessThanOrEqual(32);
      }
      let count = 0;
      for (let s = 0; s < 64; s++) count += motifAt(t, s).length;
      expect(count).toBe(t.motif.length);
      expect(motifAt(t, 64 + t.motif[0][1])).toEqual(motifAt(t, t.motif[0][1]));
    }
  });
  it('resolveMood transposes and re-tempos without mutating the base mood', () => {
    const frost = themeById('frost');
    const m = resolveMood('battle', frost);
    expect(m.root).toBe(MOODS.battle.root + frost.transpose);
    expect(m.bpm).toBe(Math.round(MOODS.battle.bpm * frost.tempo));
    expect(MOODS.battle.root).toBe(55);
  });
  it('stingers are short', () => {
    for (const id of Object.keys(STINGERS) as (keyof typeof STINGERS)[]) {
      const secs = stingerSeconds(id);
      expect(secs).toBeGreaterThan(0.8);
      expect(secs).toBeLessThan(4);
    }
  });
});
