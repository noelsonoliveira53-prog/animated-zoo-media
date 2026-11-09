import { describe, expect, it } from 'vitest';
import { clampPage, pageCount, pageItems } from '../src/ui/paging';

describe('paging', () => {
  it('counts pages, with at least one', () => {
    expect(pageCount(0, 18)).toBe(1);
    expect(pageCount(18, 18)).toBe(1);
    expect(pageCount(19, 18)).toBe(2);
  });
  it('slices and clamps', () => {
    const items = Array.from({ length: 20 }, (_, i) => i);
    expect(pageItems(items, 0, 18)).toHaveLength(18);
    expect(pageItems(items, 1, 18)).toEqual([18, 19]);
    expect(pageItems(items, 7, 18)).toEqual([18, 19]);
    expect(clampPage(-3, 20, 18)).toBe(0);
  });
});
