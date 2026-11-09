import { describe, expect, it } from 'vitest';
import { isBackLabel, nextFocus, readingOrder } from '../src/systems/focusNav';

const grid = [
  { x: 100, y: 100 }, { x: 300, y: 104 }, { x: 500, y: 98 },
  { x: 100, y: 300 }, { x: 300, y: 300 }, { x: 500, y: 300 },
];

describe('focusNav', () => {
  it('orders controls top row first, left to right', () => {
    expect(readingOrder([{ x: 300, y: 300 }, { x: 500, y: 100 }, { x: 100, y: 104 }])).toEqual([2, 1, 0]);
  });
  it('Tab starts at the first control and wraps both ways', () => {
    expect(nextFocus(grid, -1, 'next')).toBe(0);
    expect(nextFocus(grid, -1, 'prev')).toBe(5);
    expect(nextFocus(grid, 5, 'next')).toBe(0);
    expect(nextFocus(grid, 0, 'prev')).toBe(5);
    expect(nextFocus(grid, 2, 'next')).toBe(3);
  });
  it('arrows move along rows and columns', () => {
    expect(nextFocus(grid, 0, 'right')).toBe(1);
    expect(nextFocus(grid, 0, 'down')).toBe(3);
    expect(nextFocus(grid, 4, 'up')).toBe(1);
    expect(nextFocus(grid, 4, 'left')).toBe(3);
  });
  it('arrows stay put at an edge', () => {
    expect(nextFocus(grid, 2, 'right')).toBe(2);
    expect(nextFocus(grid, 0, 'up')).toBe(0);
  });
  it('prefers the control in line over a nearer diagonal one', () => {
    const pts = [{ x: 0, y: 0 }, { x: 120, y: 90 }, { x: 0, y: 200 }];
    expect(nextFocus(pts, 0, 'down')).toBe(2);
  });
  it('handles no controls', () => {
    expect(nextFocus([], -1, 'next')).toBe(-1);
  });
  it('recognises back-style labels', () => {
    expect(isBackLabel('← Map')).toBe(true);
    expect(isBackLabel('Back')).toBe(true);
    expect(isBackLabel('✕')).toBe(true);
    expect(isBackLabel('Start!')).toBe(false);
    expect(isBackLabel('Backpack')).toBe(false);
  });
});
