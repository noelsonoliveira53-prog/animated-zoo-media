import { describe, expect, it } from 'vitest';
import { announceText, shouldAnnounce } from '../src/systems/announce';

describe('screen-reader announcements', () => {
  it('words battle events', () => {
    expect(announceText.wave(0, 8)).toBe('Wave 1 of 8 has started.');
    expect(announceText.wave(11, null)).toBe('Wave 12 has started.');
    expect(announceText.leak(1, 19)).toBe('A life lost. 19 lives left.');
    expect(announceText.leak(3, 1)).toBe('3 lives lost. 1 life left.');
    expect(announceText.victory(3)).toBe('Victory! 3 stars.');
    expect(announceText.victory(1)).toBe('Victory! 1 star.');
    expect(announceText.focus('Campaign')).toBe('Campaign');
    expect(announceText.focus('II', 'Pause (Space)')).toBe('II. Pause (Space)');
  });
  it('merges repeats inside the window, speaks new or later ones', () => {
    expect(shouldAnnounce('a', 1000, null)).toBe(true);
    expect(shouldAnnounce('a', 1500, { text: 'a', at: 1000 })).toBe(false);
    expect(shouldAnnounce('a', 2000, { text: 'a', at: 1000 })).toBe(true);
    expect(shouldAnnounce('b', 1100, { text: 'a', at: 1000 })).toBe(true);
    expect(shouldAnnounce('  ', 1100, null)).toBe(false);
  });
});
