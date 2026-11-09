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

/** One short, useful line about a newly met enemy: its most important trait, phrased as advice. */
export function enemyKeyTrait(def: EnemyDef): string {
  if (def.boss) return 'Boss: huge health, changes tactics as it weakens';
  if (def.flying) return 'Flies: soldiers can\'t block it, and stones can\'t reach it';
  if (def.heal) return 'Heals its friends: take it down first';
  if (def.shield) return `Shield of ${def.shield}: soaks up hits before health`;
  if (def.splitInto) return `Splits into ${def.splitInto.count} when it falls`;
  if (def.chill) return 'Freezes nearby towers now and then';
  if (def.veil) return 'Veiled: towers only see it up close';
  if (def.armor >= 0.4) return 'Heavy armor: magic hurts it most';
  if (def.magicResist >= 0.4) return 'Resists magic: use arrows and stones';
  if (def.speed >= 42) return 'Fast: slows and blockers help';
  return 'A sturdy walker';
}
