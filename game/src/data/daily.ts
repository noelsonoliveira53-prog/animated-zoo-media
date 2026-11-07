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
};

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
    if (a.noSpells) m.noSpells = true;
    if (a.noHero) m.noHero = true;
    if (a.lives) m.lives = a.lives;
  }
  return m;
}
