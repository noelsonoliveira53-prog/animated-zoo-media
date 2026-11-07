// Economy report: where village resources come from vs what the village costs.
// `npx vite-node scripts/economy.ts`
import { LEVELS } from '../src/data/levels';
import { BUILDINGS, type BuildingId } from '../src/data/buildings';
import { TROOPS, CAMP_TIERS } from '../src/data/raid';
import { battleReward, HERO_TRAIN_COSTS } from '../src/systems/village';
import { generateCamp, campLoot } from '../src/systems/camp';
import { ACHIEVEMENTS } from '../src/data/achievements';
import { raidOnce, ARMIES } from './raid-balance';

const fmt = (n: number) => Math.round(n).toLocaleString('en-US');

// --- income: campaign ---
let cc = 0;
let cg = 0;
let c3 = 0;
let g3 = 0;
LEVELS.forEach((_, i) => {
  const first = battleReward(i, 0, 1);
  const more = battleReward(i, 1, 3);
  cc += first.coins;
  cg += first.glowsap;
  c3 += more.coins;
  g3 += more.glowsap;
});
let ac = 0;
let ag = 0;
for (const a of ACHIEVEMENTS) {
  ac += a.reward.coins ?? 0;
  ag += a.reward.glowsap ?? 0;
}
console.log('## Income');
console.log(`Campaign first clears (1★): ${fmt(cc)} coins / ${fmt(cg)} glowsap; going 1★→3★ everywhere: +${fmt(c3)} / +${fmt(g3)}`);
console.log(`Achievements (all): ${fmt(ac)} coins / ${fmt(ag)} glowsap`);

// production per hour at max counts per Grove Hall level
for (let th = 1; th <= 5; th++) {
  let ch = 0;
  let gh = 0;
  for (const id of ['coinmine', 'sapwell'] as BuildingId[]) {
    const def = BUILDINGS[id];
    const n = def.maxCount[th - 1];
    const lvl = def.levels.filter((l) => l.th <= th).length;
    const p = def.levels[lvl - 1].produces!;
    if (id === 'coinmine') ch += n * p.perHour;
    else gh += n * p.perHour;
  }
  console.log(`Production at Grove Hall ${th} (all producers maxed): ${fmt(ch)} coins/h, ${fmt(gh)} glowsap/h`);
}

// raids: average loot vs army cost lost
console.log('\n## Raids (smart deploy, 10 seeds): avg loot − glowsap cost of troops lost');
for (const [name, army] of Object.entries(ARMIES)) {
  const cost = Object.entries(army).reduce((n, [id, c]) => n + TROOPS[id].cost * c, 0);
  const row = CAMP_TIERS.map((t, tier) => {
    let lootC = 0;
    let lootG = 0;
    let lost = 0;
    for (let seed = 1; seed <= 10; seed++) {
      const r = raidOnce(army, tier, seed);
      lootC += r.loot.coins;
      lootG += r.loot.glowsap;
      for (const [id, c] of Object.entries(army)) lost += (c - (r.survivors[id] ?? 0)) * TROOPS[id].cost;
    }
    return `${t.name}: +${fmt(lootC / 10)}c +${fmt(lootG / 10)}s, lost ${fmt(lost / 10)}s (max ${fmt(campLoot(generateCamp(1, tier)).coins)})`;
  });
  console.log(`${name} (army costs ${fmt(cost)}s): ${row.join(' | ')}`);
}

// --- spending ---
console.log('\n## Spending (full build-out)');
let totalC = 0;
let totalG = 0;
for (const def of Object.values(BUILDINGS)) {
  const n = def.maxCount[4];
  let c = 0;
  let g = 0;
  def.levels.forEach((l, i) => {
    const copies = def.id === 'townhall' ? (i === 0 ? 0 : 1) : n;
    c += (l.cost.coins ?? 0) * copies;
    g += (l.cost.glowsap ?? 0) * copies;
  });
  totalC += c;
  totalG += g;
  console.log(`${def.name.padEnd(18)} ×${n}: ${fmt(c)} coins, ${fmt(g)} glowsap`);
}
const heroes = HERO_TRAIN_COSTS.reduce((a, b) => a + b, 0) * 3;
console.log(`Hero training (3 heroes to rank 5): ${fmt(heroes)} glowsap`);
console.log(`TOTAL: ${fmt(totalC)} coins, ${fmt(totalG + heroes)} glowsap`);
