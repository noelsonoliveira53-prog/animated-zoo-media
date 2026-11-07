// Raid balance: full-capacity armies per Ranger Lodge level vs each camp tier.
// `npx vite-node scripts/raid-balance.ts [--naive]` (helpers live in raid-lib.ts so importing them prints nothing)
import { CAMP_TIERS } from '../src/data/raid';
import { ARMIES, raidOnce } from './raid-lib';

console.log('| Army | ' + CAMP_TIERS.map((t) => t.name).join(' | ') + ' |');
console.log('|---|---|---|---|');
for (const [name, army] of Object.entries(ARMIES)) {
  const cells = CAMP_TIERS.map((_, tier) => {
    let stars = 0;
    let dest = 0;
    for (let seed = 1; seed <= 10; seed++) {
      const r = raidOnce(army, tier, seed, !process.argv.includes('--naive'));
      stars += r.stars;
      dest += r.destruction;
    }
    return `${(stars / 10).toFixed(1)}★ ${Math.round((dest / 10) * 100)}%`;
  });
  console.log(`| ${name} | ${cells.join(' | ')} |`);
}

