/**
 * Screen-reader announcements: the game is drawn on a canvas, so key moments are also written to a
 * visually hidden aria-live region (wave start, lives lost, victory / defeat, the focused control).
 */

/** Messages for battle events (pure, testable). */
export const announceText = {
  wave: (index: number, total: number | null) => `Wave ${index + 1}${total ? ` of ${total}` : ''} has started.`,
  leak: (lost: number, left: number) => `${lost === 1 ? 'A life' : `${lost} lives`} lost. ${left} ${left === 1 ? 'life' : 'lives'} left.`,
  victory: (stars: number) => `Victory! ${stars} ${stars === 1 ? 'star' : 'stars'}.`,
  defeat: () => 'Defeat. The sanctuary fell.',
  focus: (label: string, tip?: string) => (tip ? `${label}. ${tip}` : label),
};

/**
 * Leaks come in bursts, so messages repeated within `windowMs` merge: returns whether to speak now.
 * `last` is the previous message and the time it was spoken.
 */
export function shouldAnnounce(text: string, now: number, last: { text: string; at: number } | null, windowMs = 900): boolean {
  if (!text.trim()) return false;
  return !last || last.text !== text || now - last.at >= windowMs;
}

let region: HTMLElement | null = null;
let last: { text: string; at: number } | null = null;

function ensureRegion(): HTMLElement | null {
  if (region) return region;
  if (typeof document === 'undefined') return null;
  region = document.getElementById('announcer');
  if (!region) {
    region = document.createElement('div');
    region.id = 'announcer';
    region.setAttribute('aria-live', 'polite');
    region.setAttribute('role', 'status');
    // visually hidden but still read by screen readers
    Object.assign(region.style, { position: 'absolute', width: '1px', height: '1px', overflow: 'hidden', clip: 'rect(0 0 0 0)', whiteSpace: 'nowrap', margin: '-1px', padding: '0', border: '0' });
    document.body.appendChild(region);
  }
  return region;
}

/** Speak a message through the live region (deduplicated within a short window). */
export function announce(text: string): void {
  const now = Date.now();
  if (!shouldAnnounce(text, now, last)) return;
  last = { text, at: now };
  const r = ensureRegion();
  if (!r) return;
  // clear first so the same words repeated later are still read out
  r.textContent = '';
  setTimeout(() => r && (r.textContent = text), 30);
}
