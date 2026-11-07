import { describe, expect, it } from 'vitest';
import { motion, shake } from '../src/ui/motion';
import { defaultSave, loadSave, writeSave } from '../src/systems/save';

describe('reduce motion', () => {
  it('shake() is skipped while Reduce motion is on', () => {
    let shakes = 0;
    const scene = { cameras: { main: { shake: () => shakes++ } } } as never;
    motion.reduced = false;
    shake(scene, 100, 0.01);
    motion.reduced = true;
    shake(scene, 100, 0.01);
    motion.reduced = false;
    expect(shakes).toBe(1);
  });
  it('the setting survives a save round-trip and defaults to off', () => {
    const store = new Map<string, string>();
    const ls = { getItem: (k: string) => store.get(k) ?? null, setItem: (k: string, v: string) => void store.set(k, v), removeItem: (k: string) => void store.delete(k) } as unknown as Storage;
    expect(loadSave(ls).settings.reduceMotion ?? false).toBe(false);
    const s = defaultSave();
    s.settings.reduceMotion = true;
    writeSave(s, ls);
    expect(loadSave(ls).settings.reduceMotion).toBe(true);
  });
});
