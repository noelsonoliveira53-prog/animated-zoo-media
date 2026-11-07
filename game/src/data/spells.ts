import type { DamageType, SoldierStats } from './types';

export interface SpellDef {
  id: string;
  name: string;
  text: string;
  cooldown: number; // seconds
  color: number;
  kind: 'meteor' | 'reinforce';
  // meteor
  damage?: number;
  damageType?: DamageType;
  radius?: number;
  delay?: number; // seconds from cast to impact
  // reinforce
  count?: number;
  duration?: number; // seconds the summoned soldiers stay
  soldier?: SoldierStats;
}

// Global powers of the Grove. Both target a point the player taps.
export const SPELLS: Record<string, SpellDef> = {
  starfall: {
    id: 'starfall',
    name: 'Starfall',
    text: 'Calls down a falling star that smashes everything in a wide area, flyers included.',
    cooldown: 50,
    color: 0xffc93c,
    kind: 'meteor',
    damage: 100,
    damageType: 'physical',
    radius: 85,
    delay: 0.9,
  },
  grovecall: {
    id: 'grovecall',
    name: 'Grove Call',
    text: 'Three Rangers leap out of the bushes to hold a spot on the road for a while.',
    cooldown: 35,
    color: 0x8fdc5a,
    kind: 'reinforce',
    count: 3,
    duration: 12,
    soldier: { count: 3, hp: 70, damage: 7, attackRate: 1.2, respawn: 0, armor: 0.15, regen: 0 },
  },
};

export const SPELL_ORDER = ['starfall', 'grovecall'];
