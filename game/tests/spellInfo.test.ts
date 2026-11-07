import { describe, expect, it } from 'vitest';
import { SPELLS, SPELL_ORDER } from '../src/data/spells';
import { spellFacts } from '../src/systems/spellInfo';

describe('spell field guide facts', () => {
  it('describes every spell from its data, with recharge and hotkey', () => {
    SPELL_ORDER.forEach((id, i) => {
      const s = SPELLS[id];
      const f = spellFacts(s, i + 1);
      expect(f.length).toBeGreaterThanOrEqual(2);
      expect(f[f.length - 1]).toContain(`Recharge ${s.cooldown}s`);
      expect(f[f.length - 1]).toContain(`Hotkey ${i + 1}`);
      expect(f.join(' ')).not.toContain('undefined');
    });
  });
  it('mentions the snare slow and the meteor radius', () => {
    expect(spellFacts(SPELLS.thornsnare, 3).join(' ')).toContain('25% speed for 3s');
    expect(spellFacts(SPELLS.starfall, 1).join(' ')).toContain(`Radius ${SPELLS.starfall.radius}px`);
  });
});
