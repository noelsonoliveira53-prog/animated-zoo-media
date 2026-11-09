/** The result screen's run summary, from the sim's damage and kill tallies. */
export interface RunSummary {
  top: { name: string; damage: number; kills: number } | null; // the tower that removed the most health
  hero: { damage: number; kills: number };
  spellsCast: number;
}

/**
 * `names` maps tower uids to their display names (towers sold before the end show as "A sold tower").
 * Damage is health actually removed (overkill excluded), so the numbers read as "how much it did".
 */
export function runSummary(dmgBy: Record<string, number>, killsBy: Record<string, number>, spellsCast: number, names: Record<number, string>): RunSummary {
  let top: RunSummary['top'] = null;
  for (const [key, dmg] of Object.entries(dmgBy)) {
    if (!key.startsWith('tower:') || dmg <= 0) continue;
    if (!top || dmg > top.damage) {
      const uid = Number(key.slice(6));
      top = { name: names[uid] ?? 'A sold tower', damage: Math.round(dmg), kills: killsBy[key] ?? 0 };
    }
  }
  return { top, hero: { damage: Math.round(dmgBy.hero ?? 0), kills: killsBy.hero ?? 0 }, spellsCast };
}

/** 12 345 → "12.3k" so big numbers fit on one short line. */
export function shortNum(n: number): string {
  if (n >= 10000) return `${(n / 1000).toFixed(n >= 100000 ? 0 : 1)}k`;
  return String(Math.round(n));
}
