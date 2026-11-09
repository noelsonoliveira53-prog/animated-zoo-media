import { describe, expect, it } from 'vitest';
import { pickBannerY, roadCover } from '../src/systems/bannerSpot';

describe('banner placement', () => {
  const topEntry = [[{ x: 640, y: -40 }, { x: 640, y: 400 }, { x: 1320, y: 400 }]];
  it('counts road under the banner, with entries weighted', () => {
    const r = { cx: 640, cy: 172, w: 600, h: 84 };
    expect(roadCover(topEntry, r)).toBeGreaterThan(0);
    expect(roadCover(topEntry, { cx: 640, cy: 600, w: 600, h: 84 })).toBe(0);
    // the same length of road counts more near the entry
    const nearEntry = roadCover([[{ x: 0, y: 100 }, { x: 400, y: 100 }]], { cx: 100, cy: 100, w: 100, h: 20 });
    const farOn = roadCover([[{ x: -1000, y: 100 }, { x: 400, y: 100 }]], { cx: 100, cy: 100, w: 100, h: 20 });
    expect(nearEntry).toBeGreaterThan(farOn);
  });
  it('moves off a road that enters at the top centre', () => {
    const pick = pickBannerY(topEntry, 640, 600, 84, [172, 560]);
    expect(pick.y).toBe(560);
    expect(pick.cover).toBe(0);
  });
  it('keeps the first spot when nothing is in the way', () => {
    expect(pickBannerY([[{ x: -40, y: 650 }, { x: 1320, y: 650 }]], 640, 600, 84, [172, 560]).y).toBe(172);
  });
});
