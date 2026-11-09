import type { DamageType } from '../data/types';
import { bigHit } from './deathStyle';

export interface DamageTextStyle {
  color: string;
  size: number;
  /** a heavy hit: bigger, bolder, a stronger pop */
  big: boolean;
}

const TYPE_COLOR: Record<DamageType, string> = { physical: '#fff4d6', magic: '#d0a0ff', true: '#ffd23c' };

/** How a damage number should look: coloured by damage type, larger for big hits and for bosses. */
export function damageTextStyle(damage: number, maxHp: number, dtype: DamageType | undefined, boss: boolean): DamageTextStyle {
  const big = bigHit(damage, maxHp) || damage >= 60;
  const size = (big ? 21 : 15) + (boss ? 2 : 0);
  return { color: TYPE_COLOR[dtype ?? 'physical'], size, big };
}
