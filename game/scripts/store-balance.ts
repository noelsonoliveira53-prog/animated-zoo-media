// Store balance: win rates on a spread of levels with no store upgrades vs a fully bought store.
// `npx vite-node scripts/store-balance.ts [seeds] [levelIdx,...]`
import { LEVELS } from '../src/data/levels';
import { STORE_ITEMS } from '../src/data/store';
import { STRATEGIES, playLevel } from '../src/systems/autoplay';
import { withStorePerks } from '../src/systems/store';
import { battlePerks } from '../src/systems/village';
import { defaultSave } from '../src/systems/save';

const seeds = Number(process.argv[2] ?? 4);
const only = (process.argv[3] ?? '4,29,59,89,119,124').split(',').map(Number);
const full = defaultSave();
full.store = Object.fromEntries(STORE_ITEMS.map((i) => [i.id, i.maxRank]));
const maxed = withStorePerks(battlePerks(null), full);
console.log('maxed store perks', JSON.stringify(maxed));
for (const i of only) {
  const row: string[] = [];
  for (const perks of [undefined, maxed]) {
    const parts = STRATEGIES.slice(0, 3).map((s) => {
      let w = 0;
      for (let seed = 1; seed <= seeds; seed++) if (playLevel(LEVELS[i], s, seed, 1800, undefined, perks).won) w++;
      return `${Math.round((100 * w) / seeds)}`;
    });
    row.push(parts.join('/'));
  }
  console.log(`${String(i + 1).padStart(3)} ${LEVELS[i].name.padEnd(24)} none ${row[0].padEnd(12)} maxed ${row[1]}`);
}
