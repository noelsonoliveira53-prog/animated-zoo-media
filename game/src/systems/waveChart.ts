/** One bar of the result screen's "lives lost per wave" chart: `h` is 0..1 of the tallest bar. */
export interface ChartBar { lost: number; h: number }

/**
 * Bars for the waves played (`played` of them), scaled so the worst wave fills the chart; `worst` is that wave's
 * index (-1 for a flawless run) and `total` the lives lost overall.
 */
export function waveChart(leaks: readonly number[], played: number): { bars: ChartBar[]; worst: number; total: number } {
  const n = Math.max(0, played);
  const lost = Array.from({ length: n }, (_, i) => leaks[i] ?? 0);
  const max = Math.max(0, ...lost);
  let worst = -1;
  lost.forEach((v, i) => { if (v > 0 && (worst < 0 || v > lost[worst])) worst = i; });
  return { bars: lost.map((v) => ({ lost: v, h: max > 0 ? v / max : 0 })), worst, total: lost.reduce((a, b) => a + b, 0) };
}
