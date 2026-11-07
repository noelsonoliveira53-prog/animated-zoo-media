import { LEVELS } from '../src/data/levels';
import { STRATEGIES, playLevel, rankSlots } from '../src/systems/autoplay';
import { BattleSim } from '../src/systems/BattleSim';
const lvl = Number(process.argv[2] ?? 0);
const strat = STRATEGIES.find((s) => s.name === (process.argv[3] ?? 'novice'))!;
const orig = BattleSim.prototype.update;
const seen = new Map<BattleSim, number>();
const leaks: Record<string, number> = {};
const drain = BattleSim.prototype.drainEvents;
BattleSim.prototype.drainEvents = function () {
  const ev = drain.call(this);
  for (const e of ev) if (e.type === 'leak') { const k = `w${this.waveIndex + 1}:p${e.enemy.path}:${e.enemy.def.id}`; leaks[k] = (leaks[k] ?? 0) + e.lives; }
  return ev;
};
BattleSim.prototype.update = function (dt: number) {
  orig.call(this, dt);
  if (seen.get(this) !== this.waveIndex) {
    seen.set(this, this.waveIndex);
    console.log(`wave ${this.waveIndex + 1} lives ${this.lives} coins ${this.coins} towers ${this.towers.map((t, i) => t ? i + t.def.id[0] + t.tier : '').filter(Boolean).join(',')}`);
  }
};
const sim = new BattleSim(LEVELS[lvl]);
console.log('rank', rankSlots(sim));
console.log(playLevel(LEVELS[lvl], strat, 1));
console.log(leaks);
