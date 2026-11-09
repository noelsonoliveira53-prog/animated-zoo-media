import { APIARY_HP_PER_LEVEL, BUILDINGS, SHRINE_CD_PER_LEVEL, WEIR_BOUNTY_PER_LEVEL, type BuildingId } from '../data/buildings';

/** One stat that changes on upgrade: shown as `label  cur → next` in the building panel. */
export interface PreviewRow { label: string; cur: string; next: string }

const pct = (x: number) => `${Math.round(x * 100)}%`;

/** Battle bonus a building gives at a level (empty when it gives none). */
function bonusAt(type: BuildingId, level: number): { label: string; value: string } | null {
  switch (type) {
    case 'workshop': return { label: 'Tower damage', value: `+${level * 5}%` };
    case 'townhall': return { label: 'Start coins', value: `+${Math.max(0, level - 1) * 40}` };
    case 'barracks': return { label: 'Ranger power', value: `+${level * 25}%` };
    case 'apiary': return { label: 'Hero health', value: `+${pct(level * APIARY_HP_PER_LEVEL)}` };
    case 'weir': return { label: 'Kill coins', value: `+${pct(level * WEIR_BOUNTY_PER_LEVEL)}` };
    case 'shrine': return { label: 'Spell cooldown', value: `-${pct(level * SHRINE_CD_PER_LEVEL)}` };
    default: return null;
  }
}

/**
 * The stats that change when a building goes from `level` to `level + 1` (at most three rows, the most
 * important first). Empty at max level or when nothing measurable changes.
 */
export function upgradePreview(type: BuildingId, level: number): PreviewRow[] {
  const def = BUILDINGS[type];
  const next = def.levels[level];
  if (!next) return [];
  const cur = level > 0 ? def.levels[level - 1] : undefined;
  const rows: PreviewRow[] = [];
  const push = (label: string, a: string, b: string) => { if (a !== b) rows.push({ label, cur: a, next: b }); };
  if (next.produces) {
    push('Per hour', String(cur?.produces?.perHour ?? 0), String(next.produces.perHour));
    push('Holds', String(cur?.produces?.capacity ?? 0), String(next.produces.capacity));
  }
  if (next.storage !== undefined) push('Storage', `+${cur?.storage ?? 0}`, `+${next.storage}`);
  const bonusA = bonusAt(type, level);
  const bonusB = bonusAt(type, level + 1);
  if (bonusA && bonusB) push(bonusB.label, bonusA.value, bonusB.value);
  if (next.hp !== undefined) push('Health', String(cur?.hp ?? 0), String(next.hp));
  return rows.slice(0, 3);
}
