import type Phaser from 'phaser';

/**
 * A rounded health bar: dark rim and track, a pale damage trail (`trail` ≥ `frac`), the colored fill and a thin
 * highlight along its top. Shared by enemies, the hero and soldiers. `h` is the inner height.
 */
export function drawBar(g: Phaser.GameObjects.Graphics, x: number, y: number, w: number, h: number, frac: number, trail: number, color: number): void {
  const r = h / 2;
  const seg = (to: number) => {
    // rounded ends, but plain rects when the segment is too thin to round
    const sw = w * Math.max(0, Math.min(1, to));
    if (sw <= 0) return;
    if (sw < h) g.fillRect(x, y, sw, h);
    else g.fillRoundedRect(x, y, sw, h, r);
  };
  g.fillStyle(0x16241c, 0.92);
  g.fillRoundedRect(x - 1.5, y - 1.5, w + 3, h + 3, r + 1.5);
  g.fillStyle(0x3a2420, 1);
  seg(1);
  if (trail > frac + 0.002) {
    g.fillStyle(0xfff0c8, 0.9);
    seg(trail);
  }
  g.fillStyle(color, 1);
  seg(frac);
  if (w * frac > 4) {
    g.fillStyle(0xffffff, 0.32);
    g.fillRect(x + 1.5, y + 0.6, w * frac - 3, Math.max(1, h * 0.28));
  }
}
