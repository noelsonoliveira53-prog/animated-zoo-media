import type { Vec2 } from '../data/types';

export interface BannerRect {
  cx: number;
  cy: number;
  w: number;
  h: number;
}

/** How much road a rect hides: road length inside it (roads count 32 px wide), entries (first `entryLen` px) triple. */
export function roadCover(paths: Vec2[][], r: BannerRect, entryLen = 260, step = 4): number {
  const x0 = r.cx - r.w / 2 - 32;
  const x1 = r.cx + r.w / 2 + 32;
  const y0 = r.cy - r.h / 2 - 32;
  const y1 = r.cy + r.h / 2 + 32;
  let score = 0;
  for (const pts of paths) {
    let walked = 0;
    for (let k = 1; k < pts.length; k++) {
      const a = pts[k - 1];
      const b = pts[k];
      const len = Math.hypot(b.x - a.x, b.y - a.y);
      for (let d = 0; d < len; d += step) {
        const x = a.x + ((b.x - a.x) * d) / len;
        const y = a.y + ((b.y - a.y) * d) / len;
        if (x >= x0 && x <= x1 && y >= y0 && y <= y1) score += (walked + d < entryLen ? 3 : 1) * step;
      }
      walked += len;
    }
  }
  return score;
}

/** The candidate centre y that hides the least road (earlier candidates win ties), and how much it still hides. */
export function pickBannerY(paths: Vec2[][], cx: number, w: number, h: number, candidates: number[]): { y: number; cover: number } {
  let best = { y: candidates[0], cover: Infinity };
  for (const y of candidates) {
    const cover = roadCover(paths, { cx, cy: y, w, h });
    if (cover < best.cover) best = { y, cover };
  }
  return best;
}
