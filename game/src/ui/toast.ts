import Phaser from 'phaser';
import { pf } from './touch';
import type { AchievementDef } from '../data/achievements';
import { sfx } from '../systems/audio';
import { C, GAME_W, TEXT, textStyle } from './theme';

/** Slide-in "Achievement unlocked" cards, one after another. */
export function showAchievementToasts(scene: Phaser.Scene, list: AchievementDef[], depth = 9000): void {
  list.forEach((a, i) => {
    scene.time.delayedCall(i * 1800, () => {
      const c = scene.add.container(GAME_W / 2, -60).setDepth(depth);
      const bg = scene.add.graphics();
      bg.fillStyle(C.ink, 0.95);
      bg.fillRoundedRect(-260, -36, 520, 72, 18);
      bg.lineStyle(3, C.gold, 1);
      bg.strokeRoundedRect(-260, -36, 520, 72, 18);
      c.add(bg);
      c.add(scene.add.image(-222, 0, 'star').setScale(0.7));
      c.add(scene.add.text(-190, -24, `Achievement: ${a.name}`, textStyle(19, TEXT.gold)));
      const r = [a.reward.coins ? `+${a.reward.coins} coins` : '', a.reward.glowsap ? `+${a.reward.glowsap} glowsap` : ''].filter(Boolean).join(', ');
      c.add(scene.add.text(-190, 4, `${a.text}  ${r}`, { ...textStyle(pf(13), TEXT.cream, false), wordWrap: { width: 430 } }));
      scene.tweens.add({ targets: c, y: 120, duration: 350, ease: 'Back.easeOut' });
      scene.tweens.add({ targets: c, y: -80, delay: 2600, duration: 300, onComplete: () => c.destroy() });
      sfx.coin();
    });
  });
}
