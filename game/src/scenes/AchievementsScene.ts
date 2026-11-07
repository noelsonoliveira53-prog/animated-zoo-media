import Phaser from 'phaser';
import { music } from '../systems/music';
import { ACHIEVEMENTS } from '../data/achievements';
import { loadSave } from '../systems/save';
import { Button } from '../ui/Button';
import { C, GAME_H, GAME_W, TEXT, textStyle } from '../ui/theme';

export class AchievementsScene extends Phaser.Scene {
  constructor() {
    super('Achievements');
  }

  create(): void {
    music.setMood('calm');
    const save = loadSave();
    const g = this.add.graphics();
    g.fillGradientStyle(0x22382a, 0x22382a, 0x10261b, 0x10261b, 1);
    g.fillRect(0, 0, GAME_W, GAME_H);
    const done = ACHIEVEMENTS.filter((a) => save.achievements.includes(a.id)).length;
    this.add.text(GAME_W / 2, 44, `Achievements  ${done} / ${ACHIEVEMENTS.length}`, textStyle(34, TEXT.gold)).setOrigin(0.5);
    new Button(this, 90, 44, 'Back', { width: 140, height: 50, fontSize: 20, color: C.sky, onClick: () => this.scene.start('Menu') });

    const cols = 2;
    const cw = 590;
    const ch = 64;
    ACHIEVEMENTS.forEach((a, i) => {
      const x = 40 + (i % cols) * (cw + 20);
      const y = 92 + Math.floor(i / cols) * (ch + 4);
      const unlocked = save.achievements.includes(a.id);
      const prog = Math.min(a.goal, a.progress(save));
      const card = this.add.graphics();
      card.fillStyle(unlocked ? 0x3f6a3a : C.ink, unlocked ? 1 : 0.8);
      card.fillRoundedRect(x, y, cw, ch, 12);
      card.lineStyle(2, unlocked ? C.gold : 0x445544, 1);
      card.strokeRoundedRect(x, y, cw, ch, 12);
      this.add.image(x + 32, y + ch / 2, unlocked ? 'star' : 'star_empty').setScale(0.6);
      this.add.text(x + 62, y + 8, a.name, textStyle(17, unlocked ? TEXT.gold : TEXT.cream));
      this.add.text(x + 62, y + 34, a.text, textStyle(13, TEXT.dim, false));
      const reward = [a.reward.coins ? `${a.reward.coins}c` : '', a.reward.glowsap ? `${a.reward.glowsap}s` : ''].filter(Boolean).join(' + ');
      this.add.text(x + cw - 14, y + 8, reward, textStyle(14, TEXT.gold, false)).setOrigin(1, 0);
      if (!unlocked && a.goal > 1) {
        const bw = 150;
        card.fillStyle(0x000000, 0.5);
        card.fillRoundedRect(x + cw - 14 - bw, y + 38, bw, 10, 5);
        if (prog > 0) {
          card.fillStyle(C.leaf, 1);
          card.fillRoundedRect(x + cw - 14 - bw, y + 38, Math.max(10, bw * (prog / a.goal)), 10, 5);
        }
        this.add.text(x + cw - 14 - bw - 8, y + 43, `${prog}/${a.goal}`, textStyle(12, TEXT.cream, false)).setOrigin(1, 0.5);
      }
    });
  }
}
