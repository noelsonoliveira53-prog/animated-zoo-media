// Headless balance report: `npx vite-node scripts/balance.ts [runs] [levelIndex,...]`
import { LEVELS } from '../src/data/levels';
import { STRATEGIES, playLevel } from '../src/systems/autoplay';

const runs = Number(process.argv[2] ?? 12);
const only = process.argv[3]?.split(',').map(Number);
const rows: string[] = [];
rows.push(`| Level | Strategy | Win % | Avg lives left | Avg waves reached |`);
rows.push(`|---|---|---|---|---|`);
for (const [i, level] of LEVELS.entries()) {
  if (only && !only.includes(i)) continue;
  for (const strat of STRATEGIES) {
    let wins = 0;
    let lives = 0;
    let waves = 0;
    for (let seed = 1; seed <= runs; seed++) {
      const r = playLevel(level, strat, seed);
      if (r.won) wins++;
      lives += r.lives;
      waves += r.wavesReached;
    }
    rows.push(
      `| ${level.name} | ${strat.name} | ${Math.round((wins / runs) * 100)}% | ${(lives / runs).toFixed(1)}/${level.lives} | ${(waves / runs).toFixed(1)}/${level.waves.length} |`,
    );
  }
}
console.log(rows.join('\n'));
