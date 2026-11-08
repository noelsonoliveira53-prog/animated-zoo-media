import Phaser from 'phaser';
import { fitWidth, pf } from '../ui/touch';
import { music } from '../systems/music';
import { themeById } from '../data/musicThemes';
import { ACHIEVEMENTS } from '../data/achievements';
import { loadSave, writeSave } from '../systems/save';
import { checkAchievements } from '../systems/achievements';
import { showAchievementToasts } from '../ui/toast';
import { Button } from '../ui/Button';
import { C, GAME_H, GAME_W, TEXT, textStyle } from '../ui/theme';
import { clampPage, pageCount, pageItems } from '../ui/paging';
import { motion } from '../ui/motion';
import { addShine, glossPanel, screenBackdrop } from '../ui/panels';

/** 2 columns × 9 rows fill the screen. */
const PER_PAGE = 18;

export class AchievementsScene extends Phaser.Scene {
  constructor() {
    super('Achievements');
  }

  private page = 0;

  init(data?: { page?: number }): void {
    this.page = clampPage(data?.page ?? 0, ACHIEVEMENTS.length, PER_PAGE);
  }

  create(): void {
    music.setMood('calm');
    music.setTheme(themeById('home'));
    // Catch up on anything already earned but not yet awarded (e.g. achievements added since the last battle).
    const checked = checkAchievements(loadSave());
    if (checked.unlocked.length) {
      writeSave(checked.save);
      this.time.delayedCall(400, () => showAchievementToasts(this, checked.unlocked));
    }
    const save = checked.save;
    motion.reduced = !!save.settings.reduceMotion;
    motion.lowFx = !!save.settings.fxLow;
    screenBackdrop(this, GAME_W, GAME_H);
    const done = ACHIEVEMENTS.filter((a) => save.achievements.includes(a.id)).length;
    this.add.text(GAME_W / 2, 44, `Achievements  ${done} / ${ACHIEVEMENTS.length}`, textStyle(34, TEXT.gold)).setOrigin(0.5);
    new Button(this, 90, 44, 'Back', { width: 140, height: 50, fontSize: 20, color: C.sky, onClick: () => this.scene.start('Menu') });

    const pages = pageCount(ACHIEVEMENTS.length, PER_PAGE);
    if (pages > 1) {
      new Button(this, GAME_W - 210, 44, '<', { width: 56, height: 50, fontSize: 24, color: C.sky, onClick: () => this.scene.restart({ page: (this.page + pages - 1) % pages }) });
      new Button(this, GAME_W - 70, 44, '>', { width: 56, height: 50, fontSize: 24, color: C.sky, onClick: () => this.scene.restart({ page: (this.page + 1) % pages }) });
      this.add.text(GAME_W - 140, 44, `${this.page + 1}/${pages}`, textStyle(20)).setOrigin(0.5).setName('pageLabel');
    }

    const cols = 2;
    const cw = 590;
    const ch = 64;
    pageItems(ACHIEVEMENTS, this.page, PER_PAGE).forEach((a, i) => {
      const x = 40 + (i % cols) * (cw + 20);
      const y = 92 + Math.floor(i / cols) * (ch + 4);
      const unlocked = save.achievements.includes(a.id);
      const prog = Math.min(a.goal, a.progress(save));
      const card = this.add.graphics();
      glossPanel(card, x, y, cw, ch, { fill: unlocked ? 0x3f6a3a : C.ink, alpha: unlocked ? 1 : 0.8, rim: unlocked ? C.gold : 0x445544, radius: 12 });
      if (unlocked) {
        // a trophy medallion: warm glow behind the star, and a shine that sweeps the card now and then
        card.fillStyle(0xffd23c, 0.18);
        card.fillCircle(x + 32, y + ch / 2, 24);
        addShine(this, x, y, cw, ch, 4200 + (i % 5) * 700, 0.16);
      }
      const medal = this.add.image(x + 32, y + ch / 2, unlocked ? 'star' : 'star_empty').setScale(0.6);
      if (unlocked && !motion.reduced) this.tweens.add({ targets: medal, scale: 0.68, duration: 1400 + (i % 4) * 200, yoyo: true, repeat: -1, ease: 'Sine.easeInOut' });
      this.add.text(x + 62, y + 8, a.name, textStyle(17, unlocked ? TEXT.gold : TEXT.cream));
      // Leave room for the progress bar + count on the right when there is one.
      fitWidth(this.add.text(x + 62, y + 34, a.text, textStyle(pf(13), TEXT.dim, false)), !unlocked && a.goal > 1 ? cw - 62 - 14 - 150 - 70 : cw - 80);
      const reward = [a.reward.coins ? `${a.reward.coins}c` : '', a.reward.glowsap ? `${a.reward.glowsap}s` : ''].filter(Boolean).join(' + ');
      this.add.text(x + cw - 14, y + 8, reward, textStyle(pf(14), TEXT.gold, false)).setOrigin(1, 0);
      if (!unlocked && a.goal > 1) {
        const bw = 150;
        card.fillStyle(0x000000, 0.5);
        card.fillRoundedRect(x + cw - 14 - bw, y + 38, bw, 10, 5);
        if (prog > 0) {
          const fw = Math.max(10, bw * (prog / a.goal));
          card.fillStyle(C.leaf, 1);
          card.fillRoundedRect(x + cw - 14 - bw, y + 38, fw, 10, 5);
          card.fillStyle(0xffffff, 0.3);
          card.fillRoundedRect(x + cw - 12 - bw, y + 39, fw - 4, 3, 1.5);
        }
        this.add.text(x + cw - 14 - bw - 8, y + 43, `${prog}/${a.goal}`, textStyle(pf(12), TEXT.cream, false)).setOrigin(1, 0.5);
      }
    });
  }
}
