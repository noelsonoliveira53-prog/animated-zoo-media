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

const SIDES = [
  (k: number) => ({ x: 60, y: 160 + k * 40 }),
  (k: number) => ({ x: 1220, y: 160 + k * 40 }),
  (k: number) => ({ x: 280 + k * 60, y: 80 }),
  (k: number) => ({ x: 280 + k * 60, y: 650 }),
];

/** Smarter deploy: pick the side nearest the defenses; sappers first, brawlers next, slingers 3s later. */
export function raidOnce(army: Record<string, number>, tier: number, seed: number, smart = true) {
  const camp = generateCamp(seed, tier);
  const sim = new RaidSim(camp, army);
  const run = (sec: number) => {
    for (let s = 0; s < sec * 30 && !sim.ended; s++) sim.update(1 / 30);
  };
  if (!smart) {
    let i = 0;
    for (const [id, n] of Object.entries(army))
      for (let c = 0; c < n; c++, i++) sim.deploy(id, edges[i % 2](Math.floor(i / 2) % 12));
  } else {
    const defs = camp.buildings.filter((b) => b.type === 'spit' || b.type === 'mortar').map((b) => ({ x: (b.col + 1) * 40 + 160, y: (b.row + 1) * 40 + 92 }));
    const sideScore = SIDES.map((f) => {
      const p = f(4);
      return Math.min(...defs.map((d) => Math.hypot(d.x - p.x, d.y - p.y)));
    });
    const side = SIDES[sideScore.indexOf(Math.min(...sideScore))];
    let k = 0;
    const put = (id: string) => {
      for (let c = 0; c < (army[id] ?? 0); c++) sim.deploy(id, side((k++ % 10) + 0.5));
    };
    put('sapper');
    put('owl');
    run(1);
    put('brawler');
    run(3);
    put('slinger');
  }
  run(95);
  return { stars: sim.stars, destruction: sim.destruction, loot: sim.loot, survivors: sim.survivingArmy() };
}

if (process.argv[1]?.includes('raid-balance')) {
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
}
