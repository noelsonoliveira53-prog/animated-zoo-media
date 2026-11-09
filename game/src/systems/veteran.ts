/** Kills after which a tower counts as a veteran and wears a small gold badge. */
export const VETERAN_KILLS = 50;

/** A tower's run record from the sim's tallies: kills, health removed, and whether it has earned the badge. */
export function towerRecord(uid: number, dmgBy: Record<string, number>, killsBy: Record<string, number>): { kills: number; damage: number; veteran: boolean } {
  const kills = killsBy[`tower:${uid}`] ?? 0;
  return { kills, damage: Math.round(dmgBy[`tower:${uid}`] ?? 0), veteran: kills >= VETERAN_KILLS };
}

/** True exactly when this kill pushed the tower over the veteran line (so the badge pops once). */
export function justVeteran(killsAfter: number): boolean {
  return killsAfter === VETERAN_KILLS;
}
