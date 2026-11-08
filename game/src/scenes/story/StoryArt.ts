import Phaser from 'phaser';

/** Shade a color toward black (k = 0..1). */
function darken(c: number, k: number): number {
  const r = (c >> 16) & 255, g = (c >> 8) & 255, b = c & 255;
  return (Math.round(r * (1 - k)) << 16) | (Math.round(g * (1 - k)) << 8) | Math.round(b * (1 - k));
}

/**
 * Three ridges of hills under a chapter card's sky, each a shade darker and nearer, drifting sideways at
 * different speeds for a gentle parallax. Wider than the screen so the drift never shows an edge.
 */
export function parallaxHills(scene: Phaser.Scene, w: number, h: number, base: number, still: boolean): void {
  const layers: [number, number, number, number][] = [
    // base y, amplitude, darkness, drift px
    [h * 0.68, 50, 0.35, 18],
    [h * 0.78, 40, 0.5, 34],
    [h * 0.88, 30, 0.65, 56],
  ];
  layers.forEach(([by, amp, dk, drift], li) => {
    const g = scene.add.graphics(); // drawn in creation order: after the sky, before the panel
    g.fillStyle(darken(base, dk), 1);
    g.beginPath();
    g.moveTo(-100, h);
    for (let x = -100; x <= w + 100; x += 20) g.lineTo(x, by - Math.sin(x / (160 + li * 40) + li) * amp - Math.cos(x / 70 + li * 2) * amp * 0.25);
    g.lineTo(w + 100, h);
    g.closePath();
    g.fillPath();
    if (!still) scene.tweens.add({ targets: g, x: drift, duration: 9000 - li * 1500, yoyo: true, repeat: -1, ease: 'Sine.easeInOut' });
  });
}

/** A softly lit text panel: a glow in the accent colour, a dark glass body, a top gloss and an accent rim. */
export function litPanel(scene: Phaser.Scene, cx: number, cy: number, w: number, h: number, accent: number): void {
  scene.add.ellipse(cx, cy, w * 1.1, h * 1.35, accent, 0.06).setBlendMode(Phaser.BlendModes.ADD);
  const g = scene.add.graphics();
  g.fillStyle(0x000000, 0.3);
  g.fillRoundedRect(cx - w / 2 + 4, cy - h / 2 + 6, w, h, 26);
  g.fillStyle(0x14161e, 0.62);
  g.fillRoundedRect(cx - w / 2, cy - h / 2, w, h, 26);
  g.fillStyle(0xffffff, 0.035);
  g.fillRoundedRect(cx - w / 2 + 6, cy - h / 2 + 4, w - 12, 12, { tl: 20, tr: 20, bl: 3, br: 3 });
  g.lineStyle(2, accent, 0.6);
  g.strokeRoundedRect(cx - w / 2, cy - h / 2, w, h, 26);
}
