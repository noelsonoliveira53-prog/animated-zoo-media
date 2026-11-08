import Phaser from 'phaser';
import { addLighting } from './lighting';
import { motion } from './motion';

/** Shared look for menu-style screens: a deep backdrop with lantern glows and drifting motes, and glossy panels. */

export function screenBackdrop(scene: Phaser.Scene, w: number, h: number, top = 0x22382a, bottom = 0x10261b): void {
  const g = scene.add.graphics().setDepth(-20);
  g.fillGradientStyle(top, top, bottom, bottom, 1);
  g.fillRect(0, 0, w, h);
  for (let k = 0; k < 3; k++) scene.add.circle(w / 2 + (k - 1) * 440, 110, 230, 0xffc860, 0.03).setDepth(-19).setBlendMode(Phaser.BlendModes.ADD);
  if (!(motion.reduced || motion.lowFx)) {
    for (let i = 0; i < 18; i++) {
      const m = scene.add.circle(Phaser.Math.Between(0, w), Phaser.Math.Between(0, h), Phaser.Math.FloatBetween(1, 2.2), 0xfff0c0, 0.35).setDepth(-18).setBlendMode(Phaser.BlendModes.ADD);
      scene.tweens.add({ targets: m, y: m.y - Phaser.Math.Between(40, 120), x: m.x + Phaser.Math.Between(-30, 30), alpha: 0.05, duration: Phaser.Math.Between(4000, 8000), yoyo: true, repeat: -1, ease: 'Sine.easeInOut' });
    }
  }
  addLighting(scene, -17);
}

export interface GlossOpts { fill: number; alpha?: number; rim?: number; rimAlpha?: number; radius?: number; shadow?: boolean }

/** A panel with a drop shadow, a gloss band across the top, a thin inner rim light and a colored border. */
export function glossPanel(g: Phaser.GameObjects.Graphics, x: number, y: number, w: number, h: number, o: GlossOpts): void {
  const r = o.radius ?? 14;
  if (o.shadow !== false) {
    g.fillStyle(0x000000, 0.28);
    g.fillRoundedRect(x + 3, y + 5, w, h, r);
  }
  g.fillStyle(o.fill, o.alpha ?? 1);
  g.fillRoundedRect(x, y, w, h, r);
  // a slim gloss along the top edge only, so it never cuts through the text
  g.fillStyle(0xffffff, 0.045);
  g.fillRoundedRect(x + 3, y + 3, w - 6, Math.min(h * 0.2, 16), { tl: r - 2, tr: r - 2, bl: 3, br: 3 });
  g.lineStyle(1, 0xffffff, 0.1);
  g.strokeRoundedRect(x + 3, y + 3, w - 6, h - 6, Math.max(2, r - 3));
  if (o.rim !== undefined) {
    g.lineStyle(2, o.rim, o.rimAlpha ?? 1);
    g.strokeRoundedRect(x, y, w, h, r);
  }
}

/**
 * A slanted band of light that sweeps across a box now and then (no mask: the band is narrow and fades at the
 * ends). Returns the timer so a scene can remove it. Nothing happens with Reduce Motion or Graphics: Low.
 */
export function addShine(scene: Phaser.Scene, x: number, y: number, w: number, h: number, every: number, alpha = 0.3): Phaser.Time.TimerEvent | null {
  if (motion.reduced || motion.lowFx) return null;
  const band = scene.add.polygon(0, 0, [0, h - 4, 14, h - 4, 28, 4, 14, 4], 0xffffff, 1).setOrigin(0, 0).setBlendMode(Phaser.BlendModes.ADD).setAlpha(0);
  band.setPosition(x, y);
  return scene.time.addEvent({
    delay: every,
    loop: true,
    startAt: Math.random() * every,
    callback: () => {
      if (!band.active) return;
      band.x = x + 2;
      band.setAlpha(0);
      scene.tweens.add({ targets: band, x: x + w - 30, duration: 700, ease: 'Sine.easeInOut' });
      scene.tweens.add({ targets: band, alpha, duration: 350, yoyo: true, ease: 'Sine.easeInOut' });
    },
  });
}
