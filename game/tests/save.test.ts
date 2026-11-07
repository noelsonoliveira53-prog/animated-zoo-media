import { describe, expect, it } from 'vitest';
import { SAVE_KEY, defaultSave, loadSave, recordStars, starsForLives, writeSave, type StorageLike } from '../src/systems/save';

function memStore(): StorageLike & { data: Record<string, string> } {
  const data: Record<string, string> = {};
  return { data, getItem: (k) => data[k] ?? null, setItem: (k, v) => void (data[k] = v) };
}

describe('save system', () => {
  it('round-trips data', () => {
    const s = memStore();
    const save = recordStars(defaultSave(), 'l1', 2);
    expect(writeSave(save, s)).toBe(true);
    expect(loadSave(s).stars.l1).toBe(2);
  });
  it('keeps the best star count', () => {
    let save = recordStars(defaultSave(), 'l1', 3);
    save = recordStars(save, 'l1', 1);
    expect(save.stars.l1).toBe(3);
  });
  it('survives corrupt or missing storage', () => {
    const s = memStore();
    s.data[SAVE_KEY] = '{not json';
    expect(loadSave(s)).toEqual(defaultSave());
    expect(loadSave(null)).toEqual(defaultSave());
    const throwing: StorageLike = {
      getItem: () => {
        throw new Error('denied');
      },
      setItem: () => {
        throw new Error('denied');
      },
    };
    expect(loadSave(throwing)).toEqual(defaultSave());
    expect(writeSave(defaultSave(), throwing)).toBe(false);
  });
  it('maps lives to stars', () => {
    expect(starsForLives(20, 20)).toBe(3);
    expect(starsForLives(12, 20)).toBe(2);
    expect(starsForLives(3, 20)).toBe(1);
    expect(starsForLives(0, 20)).toBe(0);
  });
});

import { markSeen, resetProgress } from '../src/systems/save';
describe('field guide + reset', () => {
  it('marks enemies seen without duplicates', () => {
    let s = defaultSave();
    s = markSeen(s, ['mudling', 'skitter']);
    s = markSeen(s, ['mudling', 'gnat']);
    expect(s.seenEnemies).toEqual(['mudling', 'skitter', 'gnat']);
  });
  it('reset clears progress but keeps settings', () => {
    const s = { ...markSeen(defaultSave(), ['mudling']), stars: { l1: 3 }, settings: { volume: 0.2, muted: true } };
    const r = resetProgress(s);
    expect(r.stars).toEqual({});
    expect(r.seenEnemies).toEqual([]);
    expect(r.settings).toEqual({ volume: 0.2, muted: true });
  });
  it('old saves without seenEnemies load cleanly', () => {
    const data: Record<string, string> = { [SAVE_KEY]: JSON.stringify({ stars: { l1: 2 } }) };
    const store: StorageLike = { getItem: (k) => data[k] ?? null, setItem: (k, v) => void (data[k] = v) };
    expect(loadSave(store).seenEnemies).toEqual([]);
    expect(loadSave(store).stars.l1).toBe(2);
  });
});
