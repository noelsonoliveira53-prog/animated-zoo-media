// Endless balance: how many waves each strategy holds per map. `npx vite-node scripts/endless-balance.ts [seeds] [levelIdx,...]`
import { LEVELS } from '../src/data/levels';
import { ENDLESS_EXPERT, STRATEGIES, playLevel } from '../src/systems/autoplay';
import { makeEndlessLevel } from '../src/systems/endless';

const seeds = Number(process.argv[2] ?? 3);
const only = (process.argv[3] ?? '0,4,9,15').split(',').map(Number);
for (const i of only) {
  const out: string[] = [];
  for (const s of [...STRATEGIES.slice(0, 3), ENDLESS_EXPERT]) {
    let sum = 0;
    for (let seed = 1; seed <= seeds; seed++) sum += Math.max(0, playLevel(makeEndlessLevel(LEVELS[i], seed), s, seed, 20000).wavesReached - 1);
    out.push(`${s.name} ${(sum / seeds).toFixed(1)}`);
  }
  console.log(`${LEVELS[i].name.padEnd(24)} ${out.join(' | ')}`);
}
