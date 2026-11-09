import { describe, expect, it } from 'vitest';
import { shouldShowTouchTip, TOUCH_TIPS } from '../src/systems/touchTip';
import { defaultSave, loadSave, writeSave } from '../src/systems/save';

describe('touch tip', () => {
  it('shows once on touch devices only', () => {
    const s = defaultSave();
    expect(shouldShowTouchTip(s, true)).toBe(true);
    expect(shouldShowTouchTip(s, false)).toBe(false);
    s.settings.touchTipSeen = true;
    expect(shouldShowTouchTip(s, true)).toBe(false);
  });
  it('the seen flag survives a save round-trip', () => {
    const mem = new Map<string, string>();
    const store = { getItem: (k: string) => mem.get(k) ?? null, setItem: (k: string, v: string) => void mem.set(k, v), removeItem: (k: string) => void mem.delete(k) };
    const s = defaultSave();
    s.settings.touchTipSeen = true;
    writeSave(s, store);
    expect(loadSave(store).settings.touchTipSeen).toBe(true);
  });
  it('covers the three gestures', () => {
    expect(TOUCH_TIPS.map((t) => t.icon)).toEqual(['hold', 'drag', 'hero']);
  });
});
