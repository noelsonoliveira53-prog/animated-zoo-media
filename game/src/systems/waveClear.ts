/** The "wave cleared" pill: its text and whether the wave was flawless (no lives lost while it was the latest). */
export function waveClearInfo(index: number, leaksByWave: readonly number[], totalWaves: number, endless: boolean): { title: string; flawless: boolean; left: string } {
  const flawless = (leaksByWave[index] ?? 0) === 0;
  const remaining = Math.max(0, totalWaves - (index + 1));
  const left = endless ? '' : remaining === 1 ? '1 wave to go' : `${remaining} waves to go`;
  return { title: `Wave ${index + 1} cleared`, flawless, left };
}
