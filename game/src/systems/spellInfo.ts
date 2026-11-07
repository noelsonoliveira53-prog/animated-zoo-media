import type { SpellDef } from '../data/spells';

/** Plain-language facts about a spell for the Field Guide, built from its data. */
export function spellFacts(s: SpellDef, hotkey: number): string[] {
  const out: string[] = [];
  if (s.kind === 'meteor') {
    out.push(`Damage ${s.damage} ${s.damageType === 'magic' ? 'magic' : 'physical'}   •   Radius ${s.radius}px`);
    out.push(`Strikes ${s.delay}s after you tap   •   Hits flyers too`);
  } else if (s.kind === 'reinforce') {
    const st = s.soldier!;
    out.push(`Summons ${s.count} soldiers for ${s.duration}s`);
    out.push(`Each: ${st.hp} hp   •   ${st.damage} damage   •   Armor ${Math.round(st.armor * 100)}%`);
  } else {
    out.push(`Damage ${s.damage}   •   Radius ${s.radius}px   •   Walkers only`);
    if (s.slow) out.push(`Slows to ${Math.round(s.slow.factor * 100)}% speed for ${s.slow.duration}s`);
  }
  out.push(`Recharge ${s.cooldown}s   •   Hotkey ${hotkey}`);
  return out;
}
