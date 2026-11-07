// Damage benchmark per tower branch: `npx vite-node scripts/spec-bench.ts`
// One tower vs three stationary scenarios for 30s; reports DPS and DPS per 100 coins invested.
import { BattleSim } from '../src/systems/BattleSim';
import { TOWERS, TOWER_ORDER, sellValue } from '../src/data/towers';
import type { LevelDef } from '../src/data/types';

const level: LevelDef = {
  id: 'bench', name: 'bench', blurb: '', mapPos: { x: 0, y: 0 }, startCoins: 99999, lives: 999,
  theme: { grass: 0, grassDark: 0, road: 0, roadEdge: 0 },
  paths: [[{ x: 0, y: 300 }, { x: 1200, y: 300 }]], slots: [{ x: 600, y: 380 }], waves: [{ groups: [] }],
};
const scenarios: Record<string, [string, number][]> = {
  armored: [['shellback', 1]],
  crowd: [['mudling', 8]],
  flyers: [['gloomwing', 6]],
};
function bench(id: string, spec: number | null, sc: [string, number][]): number {
  const sim = new BattleSim(level);
  sim.build(0, id);
  if (spec !== null) { sim.upgrade(0); sim.upgrade(0); sim.specialize(0, spec); }
  sim.status = 'running';
  for (const [enemy, n] of sc)
    for (let i = 0; i < n; i++) {
      const e = sim.spawn(enemy, 0, 560 + (i % 4) * 14 + Math.floor(i / 4) * 10);
      e.def = { ...e.def, speed: 0, attack: 0 };
      e.hp = e.maxHp = 1e9;
    }
  let dmg = 0;
  for (let i = 0; i < 30 * 30; i++) {
    sim.update(1 / 30);
    for (const ev of sim.drainEvents()) if (ev.type === 'hit') dmg += ev.damage;
  }
  return dmg / 30;
}
console.log('branch'.padEnd(22), 'cost'.padStart(5), '| armored   crowd   flyers  (DPS, DPS per 100c)');
for (const id of TOWER_ORDER) {
  const d = TOWERS[id];
  const rows: [string, number | null, number][] = [
    [`${d.name} T1`, null, d.tiers[0].cost],
    [d.specs[0].name, 0, d.tiers.reduce((a, t) => a + t.cost, 0) + d.specs[0].stats.cost],
    [d.specs[1].name, 1, d.tiers.reduce((a, t) => a + t.cost, 0) + d.specs[1].stats.cost],
  ];
  for (const [label, spec, cost] of rows) {
    const cells = Object.values(scenarios).map((sc) => {
      const dps = bench(id, spec, sc);
      return `${dps.toFixed(0).padStart(4)}/${((dps / cost) * 100).toFixed(1).padStart(4)}`;
    });
    console.log(label.padEnd(22), String(cost).padStart(5), '|', cells.join('  '));
  }
}
void sellValue;
