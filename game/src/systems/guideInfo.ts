import type { EnemyDef } from '../data/types';
import { ENEMIES } from '../data/enemies';

/** One short line per boss phase for the Field Guide, e.g. "At 50%: shield 1200, summons 3 Cloudram". */
export function bossPhaseLines(e: EnemyDef): string[] {
  return (e.phases ?? []).map((ph) => {
    const parts: string[] = [];
    if (ph.shield) parts.push(`shield ${ph.shield}`);
    if (ph.summon) parts.push(`summons ${ph.summon.count} ${ENEMIES[ph.summon.enemy]?.name ?? ph.summon.enemy}`);
    if (ph.speedMult) parts.push(`speed ×${ph.speedMult}`);
    return `At ${Math.round(ph.at * 100)}%: ${parts.length ? parts.join(', ') : 'enrages'}`;
  });
}
