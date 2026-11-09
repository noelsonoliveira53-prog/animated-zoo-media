// Hero sweep: the expert strategy with each hero on a spread of levels.
// `npx vite-node scripts/hero-balance.ts [seeds] [levelIndex,...] [hero,...]`
import { LEVELS } from '../src/data/levels';
import { HERO_ORDER } from '../src/data/heroes';
import { STRATEGIES, playLevel } from '../src/systems/autoplay';

const seeds = Number(process.argv[2] ?? 6);
const levels = (process.argv[3] ?? '19,49,79,99,119').split(',').map(Number);
const expert = STRATEGIES.find((s) => s.name === 'expert-mixed')!;
console.log(`| Hero | ${levels.map((i) => LEVELS[i].name).join(' | ')} | Win % | Avg lives |`);
console.log(`|---|${levels.map(() => '---|').join('')}---|---|`);
const only = process.argv[4]?.split(',');
for (const hero of HERO_ORDER.filter((h) => !only || only.includes(h))) {
  let wins = 0;
  let lives = 0;
  const per: string[] = [];
  for (const i of levels) {
    let w = 0;
    for (let seed = 1; seed <= seeds; seed++) {
      const r = playLevel(LEVELS[i], { ...expert, hero }, seed);
      if (r.won) { w++; wins++; }
      lives += r.lives;
    }
    per.push(`${Math.round((100 * w) / seeds)}`);
  }
  const n = seeds * levels.length;
  console.log(`| ${hero} | ${per.join(' | ')} | ${Math.round((100 * wins) / n)}% | ${(lives / n).toFixed(1)} |`);
}
