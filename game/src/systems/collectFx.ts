/** How many little coin / glowsap icons fly to the HUD for a collection: more for bigger hauls, capped so a
 *  "Collect all" over many buildings stays light. */
export function flightCount(amount: number, buildings = 1): number {
  if (amount <= 0) return 0;
  const per = Math.min(6, 2 + Math.floor(Math.log10(Math.max(1, amount))));
  return Math.max(1, Math.min(per, Math.floor(24 / Math.max(1, buildings))));
}
