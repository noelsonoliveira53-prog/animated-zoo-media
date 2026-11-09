import Phaser from 'phaser';
import { motion } from './motion';

/**
 * Scene entrance: a curtain of leaves covers the screen for a moment, then blows away to the right in a staggered
 * gust while the green backdrop fades. Drawn on top of everything and never interactive, so input works at once.
 * Reduce Motion gets a plain quick fade instead.
 */
export function leafReveal(scene: Phaser.Scene, w: number, h: number): void {
  // the boot vignette (index.html) goes away once the first scene is ready
  const boot = typeof document !== 'undefined' ? document.getElementById('boot') : null;
  if (boot && !boot.classList.contains('gone')) {
    boot.classList.add('gone');
    window.setTimeout(() => boot.remove(), 500);
  }
  const top = 99990;
  const back = scene.add.rectangle(w / 2, h / 2, w + 40, h + 40, 0x10261b, 1).setDepth(top).setScrollFactor(0);
  if (motion.reduced) {
    scene.tweens.add({ targets: back, alpha: 0, duration: 220, onComplete: () => back.destroy() });
    return;
  }
  scene.tweens.add({ targets: back, alpha: 0, delay: 120, duration: 380, onComplete: () => back.destroy() });
  const colors = [0x3f7a2e, 0x4f9a38, 0x6aae42, 0x8fdc5a, 0x2f6a30];
  const cols = 8, rows = 5;
  for (let i = 0; i < cols * rows; i++) {
    const c = i % cols, r = Math.floor(i / cols);
    const x = (c + 0.5) * (w / cols) + (Math.random() - 0.5) * 40;
    const y = (r + 0.5) * (h / rows) + (Math.random() - 0.5) * 40;
    const leaf = scene.add.ellipse(x, y, 190, 110, colors[i % colors.length], 1).setDepth(top + 1).setScrollFactor(0).setRotation(Math.random() * 3);
    scene.tweens.add({
      targets: leaf,
      x: x + w * 0.9 + Math.random() * 200,
      y: y - 120 - Math.random() * 160,
      rotation: leaf.rotation + 3,
      scale: 0.3,
      alpha: 0,
      delay: c * 35 + Math.random() * 60,
      duration: 520,
      ease: 'Quad.easeIn',
      onComplete: () => leaf.destroy(),
    });
  }
}
