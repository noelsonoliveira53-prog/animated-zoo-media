// Endless diagnosis: per-strategy leaks by wave on one map. `npx vite-node scripts/endless-wall.ts levelIdx seed`
import { LEVELS } from '../src/data/levels';
import { STRATEGIES, playLevel } from '../src/systems/autoplay';
import { makeEndlessLevel } from '../src/systems/endless';
import { BattleSim } from '../src/systems/BattleSim';

const idx = Number(process.argv[2] ?? 114);
const seed = Number(process.argv[3] ?? 1);
const lvl = makeEndlessLevel(LEVELS[idx], seed);
for (const s of STRATEGIES.slice(0, 3)) {
  const leaks: Record<string, number> = {};
  const orig = BattleSim.prototype.drainEvents;
  BattleSim.prototype.drainEvents = function (this: BattleSim & { waveIndex?: number; wave?: number }) {
    const ev = orig.call(this);
    for (const e of ev as { type: string; enemy?: { def: { id: string } }; lives?: number }[]) if (e.type === 'leak') { const k = `w${this.waveIndex ?? this.wave} ${e.enemy!.def.id}`; leaks[k] = (leaks[k] ?? 0) + (e.lives ?? 1); }
    return ev;
  };
  const r = playLevel(lvl, s, seed, 20000);
  BattleSim.prototype.drainEvents = orig;
  console.log(s.name, 'reached', r.wavesReached, JSON.stringify(leaks));
}
console.log('waves 13-16:', lvl.waves.slice(12, 16).map((w, i) => `${i + 13}: ` + w.groups.map((g) => `${g.enemy}x${g.count}`).join(',')).join('\n'));
