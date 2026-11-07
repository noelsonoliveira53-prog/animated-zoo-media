// Specialization duel: each tower type alone, forced into branch A or B. `npx vite-node scripts/spec-duel.ts`
import { LEVELS } from '../src/data/levels';
import { playLevel, type Strategy } from '../src/systems/autoplay';
import { TOWERS, TOWER_ORDER } from '../src/data/towers';
const levels = [1, 2, 4].map((i) => ({ ...LEVELS[i], startCoins: LEVELS[i].startCoins * 6 }));
for (const id of TOWER_ORDER) {
  for (const pick of [0, 1, -1]) {
    const strat: Strategy = {
      name: 'duel', mix: id === 'burrow' ? ['burrow', 'thornbow'] : [id], slotFraction: 1, reserve: 0, upgrades: true,
      hero: 'fen', thinkEvery: 1, useSpells: false, specPick: pick < 0 ? undefined : pick,
    };
    const label = pick < 0 ? 'no-spec*' : TOWERS[id].specs[pick].name;
    const cells = levels.map((l) => {
      let lives = 0, waves = 0;
      for (let s = 1; s <= 4; s++) {
        const r = playLevel(l, pick < 0 ? { ...strat, upgrades: true } : strat, s);
        lives += r.lives; waves += r.wavesReached;
      }
      return `${(waves / 4).toFixed(1)}w/${(lives / 4).toFixed(1)}`;
    });
    console.log(`${TOWERS[id].name.padEnd(16)} ${label.padEnd(20)} ${cells.join('  ')}`);
  }
}
console.log('(start coins x6 so branches get bought) * no-spec rows still specialize (alternating); columns = L2, L3, L5 as avg waves reached / avg lives');
