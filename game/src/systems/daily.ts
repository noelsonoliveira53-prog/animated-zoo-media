import { DAILY_MODIFIERS } from '../data/daily';
import { LEVELS } from '../data/levels';

export interface DailyChallenge {
  date: string; // YYYY-MM-DD (local)
  levelIndex: number;
  modifiers: string[]; // two modifier ids: one hard, one mixed
  reward: { coins: number; glowsap: number };
}

export function todayString(d = new Date()): string {
  const m = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  return `${d.getFullYear()}-${m}-${day}`;
}

export function hash(str: string): number {
  let h = 2166136261;
  for (let i = 0; i < str.length; i++) {
    h ^= str.charCodeAt(i);
    h = Math.imul(h, 16777619);
  }
  return h >>> 0;
}

/** The challenge for a date, limited to levels the player has unlocked (`unlocked` = count). */
export function dailyFor(date: string, unlocked: number): DailyChallenge {
  const h = hash(`grovewatch:${date}`);
  const pool = Math.max(1, Math.min(LEVELS.length, unlocked));
  const levelIndex = h % pool;
  const hard = DAILY_MODIFIERS.filter((m) => !m.good);
  const first = hard[(h >>> 8) % hard.length];
  const rest = DAILY_MODIFIERS.filter((m) => m.id !== first.id);
  const second = rest[(h >>> 16) % rest.length];
  return {
    date,
    levelIndex,
    modifiers: [first.id, second.id],
    reward: { coins: 300 + levelIndex * 60, glowsap: 300 + levelIndex * 60 },
  };
}
