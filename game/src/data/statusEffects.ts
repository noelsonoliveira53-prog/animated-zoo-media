/** Status effects explained in the Field Guide's Effects tab, each with a live preview. */
export type EffectPreview = 'slow' | 'frozen' | 'venom' | 'shield' | 'stun' | 'honey';

export interface StatusEffect {
  id: EffectPreview;
  name: string;
  color: number;
  /** who suffers it */
  on: 'enemies' | 'towers' | 'soldiers';
  /** texture shown in the preview (a sample enemy, soldier or tower) */
  sample: string;
  blurb: string;
  sources: string;
  counter: string;
}

export const STATUS_EFFECTS: StatusEffect[] = [
  {
    id: 'slow', name: 'Slowed', color: 0x8fdc5a, on: 'enemies', sample: 'enemy_mudling',
    blurb: 'Brambles, frost and sticky sap drag at their feet.',
    sources: 'Thornsnare, the Frost and Sap tower branches, Wren\'s Hush, Bramble\'s Earthshake.',
    counter: 'Slows stack well with splash towers: a slowed crowd stays inside the blast. Some foes (Windborne flyers) shrug slows off.',
  },
  {
    id: 'shield', name: 'Shielded', color: 0x7fd8ff, on: 'enemies', sample: 'enemy_reedguard',
    blurb: 'A pool of extra toughness that soaks up hits before any health is lost.',
    sources: 'Reedguards and other shield-bearers, Shellguard auras, and bosses entering a new phase.',
    counter: 'Many quick hits peel shields fast; save Starfall for after the shield is gone.',
  },
  {
    id: 'frozen', name: 'Frozen tower', color: 0xbfe8ff, on: 'towers', sample: 'tower_thornbow_1',
    blurb: 'Rimewraiths breathe a cold that locks a tower up for a moment.',
    sources: 'Rimewraiths and frost bosses, every few seconds in a circle around them.',
    counter: 'Spread your towers out so one breath can\'t freeze them all, and focus chillers down first.',
  },
  {
    id: 'venom', name: 'Venom', color: 0xa8f07a, on: 'soldiers', sample: 'soldier',
    blurb: 'A bite that keeps burning: the soldier\'s health bar turns green and drains.',
    sources: 'Canyon Rattlers, the Rattling Spire\'s old serpent, and Rattle Traps in raids.',
    counter: 'Sorrel\'s Field Dressing heals it away; fallen soldiers come back clean.',
  },
  {
    id: 'stun', name: 'Shocked', color: 0xc8e8ff, on: 'soldiers', sample: 'soldier',
    blurb: 'A jolt of eel lightning: no attacking or blocking while the sparks crackle.',
    sources: 'Sparkeels and storm bosses, on a timer, in a ring around them.',
    counter: 'Keep a second line of soldiers behind the first, or let towers handle eels before they reach your blockers.',
  },
  {
    id: 'honey', name: 'Honey-glazed', color: 0xffd070, on: 'soldiers', sample: 'soldier',
    blurb: 'A sticky swipe gums up a soldier\'s sword arm, so it attacks slowly.',
    sources: 'Honeypaw Cubs and the Hive Matriarch\'s brood.',
    counter: 'Glaze wears off on its own; ranged towers and magic don\'t care about honey.',
  },
];
