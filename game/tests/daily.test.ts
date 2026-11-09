import { describe, expect, it } from 'vitest';
import { dailyFor, todayString } from '../src/systems/daily';
import { combine, DAILY_MODIFIERS } from '../src/data/daily';
import { BattleSim } from '../src/systems/BattleSim';
import { LEVELS } from '../src/data/levels';

describe('daily challenge', () => {
  it('is deterministic per date and limited to unlocked levels', () => {
    expect(dailyFor('2026-11-07', 5)).toEqual(dailyFor('2026-11-07', 5));
    for (let d = 1; d <= 28; d++) {
      const c = dailyFor(`2026-02-${String(d).padStart(2, '0')}`, 3);
      expect(c.levelIndex).toBeLessThan(3);
      expect(c.modifiers.length).toBe(2);
      expect(c.modifiers[0]).not.toBe(c.modifiers[1]);
      // the first twist always makes it harder
      expect(DAILY_MODIFIERS.find((m) => m.id === c.modifiers[0])!.good).toBeFalsy();
    }
  });
  it('varies across days', () => {
    const set = new Set(Array.from({ length: 20 }, (_, d) => JSON.stringify(dailyFor(`2026-03-${String(d + 1).padStart(2, '0')}`, 15).modifiers)));
    expect(set.size).toBeGreaterThan(4);
  });
  it('formats local dates', () => {
    expect(todayString(new Date(2026, 0, 5))).toBe('2026-01-05');
  });
  it('modifiers change the battle', () => {
    const lvl = LEVELS[0];
    const m = combine(['thrifty', 'glass', 'nospells', 'nohero', 'rich']);
    const sim = new BattleSim(lvl, 'bramble', { mods: m });
    expect(sim.hero).toBeNull();
    expect(sim.lives).toBe(5);
    expect(sim.coins).toBe(Math.round(lvl.startCoins * 1.5));
    expect(sim.price(100)).toBe(80);
    expect(sim.castSpell('starfall', { x: 300, y: 300 })).toBe(false);
    const fast = new BattleSim(lvl, null, { mods: combine(['swift', 'tough']) });
    const normal = new BattleSim(lvl, null);
    const a = fast.spawn('mudling');
    const b = normal.spawn('mudling');
    expect(a.maxHp).toBeGreaterThan(b.maxHp);
    fast.status = normal.status = 'running';
    fast.update(1);
    normal.update(1);
    expect(a.dist).toBeGreaterThan(b.dist);
  });
});

describe('Golden Harvest and Ironbark', () => {
  const lvl = { id: 't', name: 't', blurb: '', mapPos: { x: 0, y: 0 }, startCoins: 100, lives: 20,
    paths: [[{ x: 0, y: 300 }, { x: 1200, y: 300 }]], slots: [], waves: [{ groups: [{ enemy: 'shellback', count: 1, interval: 1 }] }],
    theme: { grass: 0, grassDark: 0, road: 0, roadEdge: 0 } };
  it('Golden Harvest pays 50% more per kill', () => {
    const plain = new BattleSim(lvl, null);
    const gold = new BattleSim(lvl, null, { mods: combine(['harvest']) });
    for (const s of [plain, gold]) {
      const e = s.spawn('shellback', 0, 100);
      (s as unknown as { applyDamage: (e: unknown, d: number) => void }).applyDamage(e, 99999);
    }
    expect(gold.coins - 100).toBe(Math.round((plain.coins - 100) * 1.5));
  });
  it('Ironbark adds armor to every enemy', () => {
    const plain = new BattleSim(lvl, null);
    const iron = new BattleSim(lvl, null, { mods: combine(['ironbark']) });
    const a = plain.spawn('shellback', 0, 100);
    const b = iron.spawn('shellback', 0, 100);
    expect(iron.res(b).armor).toBeCloseTo(Math.min(0.85, plain.res(a).armor + DAILY_MODIFIERS.find((m) => m.id === 'ironbark')!.apply.armorBonus!));
  });
});

import { dailyLevel } from '../src/systems/daily';
import { DAILY_HP_EASE } from '../src/data/daily';
describe('daily level ease', () => {
  it("a daily eases the level's enemy health and leaves everything else alone", () => {
    const base = LEVELS[40];
    const d = dailyLevel(base);
    expect(d.hpMult).toBeCloseTo((base.hpMult ?? 1) * DAILY_HP_EASE);
    expect(d.waves).toBe(base.waves);
    expect(d.id).toBe(base.id);
  });
});

describe('Prairie Gale', () => {
  const lvl = { id: 't', name: 't', blurb: '', mapPos: { x: 0, y: 0 }, startCoins: 100, lives: 20,
    paths: [[{ x: 0, y: 300 }, { x: 3000, y: 300 }]], slots: [], waves: [{ groups: [{ enemy: 'shellback', count: 1, interval: 1 }] }],
    theme: { grass: 0, grassDark: 0, road: 0, roadEdge: 0 } };
  it('every enemy gathers speed while unhit, capped, and a hit resets it; off without the twist', () => {
    const cap = DAILY_MODIFIERS.find((m) => m.id === 'gale')!.apply.momentumMax!;
    const plain = new BattleSim(lvl, null);
    const gale = new BattleSim(lvl, null, { mods: combine(['gale']) });
    for (const s of [plain, gale]) s.status = 'running';
    const a = plain.spawn('shellback', 0, 100);
    const b = gale.spawn('shellback', 0, 100);
    for (let i = 0; i < 60 * 12; i++) {
      plain.update(1 / 60);
      gale.update(1 / 60);
    }
    expect(plain.momentumMult(a)).toBe(1);
    expect(gale.momentumMult(b)).toBeCloseTo(1 + cap);
    expect(b.dist).toBeGreaterThan(a.dist);
    (gale as unknown as { applyDamage: (e: unknown, d: number) => void }).applyDamage(b, 1);
    expect(gale.momentumMult(b)).toBeCloseTo(1);
  });
});

import { dailyFor as pickDaily, LIGHT_TWISTS } from '../src/systems/daily';
import { DAILY_MODIFIERS as MODS } from '../src/data/daily';
describe('daily twist pairing', () => {
  it('never pairs two heavy twists over a year of dates', () => {
    const heavy = (id: string) => { const m = MODS.find((x) => x.id === id)!; return !m.good && !LIGHT_TWISTS.includes(id); };
    for (let d = 0; d < 366; d++) {
      const date = new Date(Date.UTC(2026, 0, 1 + d)).toISOString().slice(0, 10);
      const c = pickDaily(date, 60);
      expect(c.modifiers[0]).not.toBe(c.modifiers[1]);
      expect(heavy(c.modifiers[0]) && heavy(c.modifiers[1])).toBe(false);
    }
  });
});
