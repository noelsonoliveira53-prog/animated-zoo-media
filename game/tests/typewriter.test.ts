import { describe, expect, it } from 'vitest';
import { typeSlice } from '../src/ui/typewriter';

describe('typewriter', () => {
  it('reveals characters over time and line breaks are free', () => {
    expect(typeSlice('abc\ndef', 0, 10)).toBe('');
    expect(typeSlice('abc\ndef', 0.3, 10)).toBe('abc');
    expect(typeSlice('abc\ndef', 0.4, 10)).toBe('abc\nd');
    expect(typeSlice('abc\ndef', 5, 10)).toBe('abc\ndef');
  });
});
