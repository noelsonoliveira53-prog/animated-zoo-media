// Daily challenge modifiers. Each day picks a level and two of these.

export interface Modifiers {
  speedMult: number; // enemy speed
  hpMult: number; // extra enemy health on top of the level's own
  costMult: number; // tower build/upgrade/branch prices
  startCoinsMult: number;
  noSpells: boolean;
  noHero: boolean;
  lives: number | null; // override
  waveGapMult: number; // time between waves
  bountyMult: number; // coins per kill
  armorBonus: number; // added to every enemy's armor
  momentumMax: number; // Prairie Gale: every enemy gathers speed while unhit (+6%/s), up to +this (0 = off)
}

export const NO_MODS: Modifiers = {
  speedMult: 1,
  hpMult: 1,
  costMult: 1,
  startCoinsMult: 1,
  noSpells: false,
  noHero: false,
  lives: null,
  waveGapMult: 1,
  bountyMult: 1,
  armorBonus: 0,
  momentumMax: 0,
};

/** Daily challenges stack two twists on a level tuned without them, so the level's enemy health is eased to make room. */
export const DAILY_HP_EASE = 0.7;

export interface ModifierDef {
  id: string;
  name: string;
  text: string;
  apply: Partial<Modifiers>;
  good?: boolean; // helps the player
}

export const DAILY_MODIFIERS: ModifierDef[] = [
  { id: 'swift', name: 'Swift Horde', text: 'Enemies move 30% faster.', apply: { speedMult: 1.3 } },
  { id: 'tough', name: 'Thick Hides', text: 'Enemies have 25% more health.', apply: { hpMult: 1.25 } },
  { id: 'thrifty', name: 'Beaver Discount', text: 'Towers cost 20% less.', apply: { costMult: 0.8 }, good: true },
  { id: 'rich', name: 'Full Coffers', text: 'Start with 50% more coins.', apply: { startCoinsMult: 1.5 }, good: true },
  { id: 'nospells', name: 'Clouded Sky', text: 'No global spells.', apply: { noSpells: true } },
  { id: 'nohero', name: 'Hero on Leave', text: 'Your hero stays home.', apply: { noHero: true } },
  { id: 'glass', name: 'Thin Hedge', text: 'Only 5 lives.', apply: { lives: 5 } },
  { id: 'frenzy', name: 'Frenzy', text: 'Waves come twice as fast.', apply: { waveGapMult: 0.5 } },
  { id: 'harvest', name: 'Golden Harvest', text: 'Kills pay 50% more coins.', apply: { bountyMult: 1.5 }, good: true },
  { id: 'ironbark', name: 'Ironbark', text: 'Enemies have +6% armor.', apply: { armorBonus: 0.06 } },
  { id: 'gale', name: 'Prairie Gale', text: 'Enemies gather speed while unhit (up to +50%).', apply: { momentumMax: 0.5 } },
];

export function combine(ids: string[]): Modifiers {
  const m: Modifiers = { ...NO_MODS };
  for (const id of ids) {
    const d = DAILY_MODIFIERS.find((x) => x.id === id);
    if (!d) continue;
    const a = d.apply;
    if (a.speedMult) m.speedMult *= a.speedMult;
    if (a.hpMult) m.hpMult *= a.hpMult;
    if (a.costMult) m.costMult *= a.costMult;
    if (a.startCoinsMult) m.startCoinsMult *= a.startCoinsMult;
    if (a.waveGapMult) m.waveGapMult *= a.waveGapMult;
    if (a.bountyMult) m.bountyMult *= a.bountyMult;
    if (a.armorBonus) m.armorBonus += a.armorBonus;
    if (a.momentumMax) m.momentumMax = Math.max(m.momentumMax, a.momentumMax);
    if (a.noSpells) m.noSpells = true;
    if (a.noHero) m.noHero = true;
    if (a.lives) m.lives = a.lives;
  }
  return m;
}
