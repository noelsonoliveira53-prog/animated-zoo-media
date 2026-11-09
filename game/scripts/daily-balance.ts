// Daily challenge balance: expert win rate with each hard modifier alone and with the nastiest hard pairs, on the
// daily-eased version of a spread of levels. `npx vite-node scripts/daily-balance.ts [seeds] [levelIdx,...] [pairs]`
import { LEVELS } from '../src/data/levels';
import { DAILY_MODIFIERS, combine } from '../src/data/daily';
import { STRATEGIES, playLevel } from '../src/systems/autoplay';
import { dailyLevel } from '../src/systems/daily';

const seeds = Number(process.argv[2] ?? 3);
const levels = (process.argv[3] ?? '4,19,39,74').split(',').map(Number);
const expert = STRATEGIES[0];
const hard = DAILY_MODIFIERS.filter((m) => !m.good).map((m) => m.id);
const combos: string[][] = process.argv[4] === 'pairs'
  ? [['tough', 'thrifty'], ['swift', 'rich'], ['nohero', 'harvest'], ['frenzy', 'gale'], ['glass', 'ironbark'], ['tough', 'ironbark']] // pairs the new picker can roll
  : [[], ...hard.map((h) => [h]), ['glass', 'frenzy'], ['tough', 'swift'], ['nohero', 'nospells'], ['tough', 'ironbark']];
console.log(`| Modifiers | ${levels.map((i) => LEVELS[i].name).join(' | ')} |`);
console.log(`|---|${levels.map(() => '---').join('|')}|`);
for (const ids of combos) {
  const mods = combine(ids);
  const cells = levels.map((i) => {
    let wins = 0;
    for (let s = 1; s <= seeds; s++) if (playLevel(dailyLevel(LEVELS[i]), expert, s, 1800, mods).won) wins++;
    return `${Math.round((wins / seeds) * 100)}%`;
  });
  console.log(`| ${ids.join(' + ') || '(none)'} | ${cells.join(' | ')} |`);
}
