// How often towers earn the veteran badge (VETERAN_KILLS) in real runs: expert strategy, a spread of levels.
// `npx vite-node scripts/veteran-balance.ts [seeds] [levelIndex,...]`
import { LEVELS } from '../src/data/levels';
import { STRATEGIES, playLevel } from '../src/systems/autoplay';
import { VETERAN_KILLS } from '../src/systems/veteran';

const seeds = Number(process.argv[2] ?? 3);
const levels = (process.argv[3] ?? '0,4,9,19,39,59,79,99,124').split(',').map(Number);
const strat = STRATEGIES.find((s) => s.name === 'expert-mixed')!;
console.log(`| Level | Towers | Veterans/run | Top tower kills | Median kills |`);
console.log(`|---|---|---|---|---|`);
const all: number[] = [];
for (const i of levels) {
  let vets = 0, towers = 0, top = 0;
  const ks: number[] = [];
  for (let seed = 1; seed <= seeds; seed++) {
    const r = playLevel(LEVELS[i], strat, seed);
    towers += r.towerKills.length;
    vets += r.towerKills.filter((k) => k >= VETERAN_KILLS).length;
    top = Math.max(top, ...r.towerKills, 0);
    ks.push(...r.towerKills);
  }
  ks.sort((a, b) => a - b);
  all.push(...ks);
  console.log(`| ${LEVELS[i].name} | ${(towers / seeds).toFixed(1)} | ${(vets / seeds).toFixed(1)} | ${top} | ${ks[Math.floor(ks.length / 2)] ?? 0} |`);
}
all.sort((a, b) => a - b);
const pct = (p: number) => all[Math.min(all.length - 1, Math.floor(all.length * p))];
console.log(`\nAll towers: p50 ${pct(0.5)}, p75 ${pct(0.75)}, p90 ${pct(0.9)}, max ${all[all.length - 1]}; share at ${VETERAN_KILLS}+: ${((100 * all.filter((k) => k >= VETERAN_KILLS).length) / all.length).toFixed(0)}%`);
