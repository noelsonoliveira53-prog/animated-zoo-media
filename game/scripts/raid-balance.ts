// Raid balance: full-capacity armies per Ranger Lodge level vs each camp tier.
// `npx vite-node scripts/raid-balance.ts`
import { generateCamp } from '../src/systems/camp';
import { RaidSim } from '../src/systems/RaidSim';
import { CAMP_TIERS } from '../src/data/raid';

export const ARMIES: Record<string, Record<string, number>> = {
  'Lodge 1 (10)': { brawler: 5, slinger: 3, sapper: 1 },
  'Lodge 2 (20)': { brawler: 8, slinger: 6, sapper: 3 },
  'Lodge 3 (30)': { brawler: 10, slinger: 8, sapper: 3, owl: 2 },
};

const edges = [
  (k: number) => ({ x: 60, y: 140 + k * 45 }),
  (k: number) => ({ x: 1220, y: 140 + k * 45 }),
  (k: number) => ({ x: 300 + k * 60, y: 80 }),
  (k: number) => ({ x: 300 + k * 60, y: 650 }),
];

export function raidOnce(army: Record<string, number>, tier: number, seed: number) {
  const sim = new RaidSim(generateCamp(seed, tier), army);
  let i = 0;
  // Deploy everything spread over two sides (a reasonable player attack).
  for (const [id, n] of Object.entries(army))
    for (let c = 0; c < n; c++, i++) {
      const edge = edges[i % 2 === 0 ? 0 : 1];
      sim.deploy(id, edge(Math.floor(i / 2) % 12));
    }
  for (let s = 0; s < 95 * 30 && !sim.ended; s++) sim.update(1 / 30);
  return { stars: sim.stars, destruction: sim.destruction, lost: Object.values(army).reduce((a, b) => a + b, 0) - Object.values(sim.survivingArmy()).reduce((a, b) => a + b, 0) };
}

{
  console.log('| Army | ' + CAMP_TIERS.map((t) => t.name).join(' | ') + ' |');
  console.log('|---|---|---|---|');
  for (const [name, army] of Object.entries(ARMIES)) {
    const cells = CAMP_TIERS.map((_, tier) => {
      let stars = 0;
      let dest = 0;
      for (let seed = 1; seed <= 10; seed++) {
        const r = raidOnce(army, tier, seed);
        stars += r.stars;
        dest += r.destruction;
      }
      return `${(stars / 10).toFixed(1)}★ ${Math.round((dest / 10) * 100)}%`;
    });
    console.log(`| ${name} | ${cells.join(' | ')} |`);
  }
}
