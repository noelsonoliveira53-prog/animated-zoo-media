import Phaser from 'phaser';
import type { EnemyDef } from '../../data/types';
import { textStyle } from '../../ui/theme';

/**
 * A boss arrives: the screen edges pulse red twice and a nameplate slides across (portrait, name, a key trait),
 * holds a moment, then slides away. Purely visual and never interactive. `still` (Reduce Motion) shows the plate
 * in place briefly with no slide or pulse.
 */
export function bossIntro(scene: Phaser.Scene, def: EnemyDef, trait: string, w: number, h: number, still: boolean): void {
  const key = 'fx_boss_vignette';
  if (!scene.textures.exists(key)) {
    const tex = scene.textures.createCanvas(key, w, h);
    if (tex) {
      const ctx = tex.getContext();
      const grd = ctx.createRadialGradient(w / 2, h / 2, Math.min(w, h) * 0.32, w / 2, h / 2, Math.max(w, h) * 0.62);
      grd.addColorStop(0, 'rgba(160,20,20,0)');
      grd.addColorStop(1, 'rgba(170,20,20,0.75)');
      ctx.fillStyle = grd;
      ctx.fillRect(0, 0, w, h);
      tex.refresh();
    }
  }
  if (!still) {
    const vig = scene.add.image(0, 0, key).setOrigin(0, 0).setDepth(3990).setAlpha(0);
    scene.tweens.add({ targets: vig, alpha: 0.9, duration: 260, yoyo: true, repeat: 1, hold: 120, onComplete: () => vig.destroy() });
  }

  // the nameplate
  const py = h * 0.62;
  const plate = scene.add.container(still ? w / 2 : -420, py).setDepth(4000);
  const g = scene.add.graphics();
  g.fillStyle(0x000000, 0.35);
  g.fillRoundedRect(-300, -50, 620, 108, 18);
  g.fillStyle(0x1a0e10, 0.94);
  g.fillRoundedRect(-310, -56, 620, 108, 18);
  g.fillStyle(0xffffff, 0.05);
  g.fillRoundedRect(-306, -52, 612, 18, { tl: 16, tr: 16, bl: 3, br: 3 });
  g.lineStyle(3, 0xc23a3a, 1);
  g.strokeRoundedRect(-310, -56, 620, 108, 18);
  g.fillStyle(0xc23a3a, 1);
  g.fillCircle(-250, -2, 44);
  g.fillStyle(0x2a1416, 1);
  g.fillCircle(-250, -2, 39);
  plate.add(g);
  const portrait = scene.add.image(-250, 2, `enemy_${def.id}`);
  portrait.setScale(Math.min(1.6, 70 / Math.max(portrait.width, portrait.height)));
  plate.add(portrait);
  plate.add(scene.add.text(-190, -30, 'BOSS APPROACHES', textStyle(14, '#ff9a8a')).setOrigin(0, 0.5));
  const name = scene.add.text(-190, 2, def.name, textStyle(28, '#ffd23c')).setOrigin(0, 0.5).setStroke('#2a0a0a', 6);
  if (name.width > 480) name.setScale(480 / name.width);
  plate.add(name);
  const t = scene.add.text(-190, 32, trait, textStyle(14, '#f0e0d0', false)).setOrigin(0, 0.5);
  if (t.width > 480) t.setScale(480 / t.width);
  plate.add(t);

  if (still) {
    scene.tweens.add({ targets: plate, alpha: 0, delay: 2200, duration: 300, onComplete: () => plate.destroy() });
    return;
  }
  scene.tweens.add({
    targets: plate, x: w / 2, duration: 380, ease: 'Back.easeOut',
    onComplete: () => scene.tweens.add({ targets: plate, x: w + 420, delay: 1800, duration: 340, ease: 'Quad.easeIn', onComplete: () => plate.destroy() }),
  });
  scene.tweens.add({ targets: portrait, scale: portrait.scale * 1.12, duration: 300, yoyo: true, repeat: 3, delay: 380 });
}
