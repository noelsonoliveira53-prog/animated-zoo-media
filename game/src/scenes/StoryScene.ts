import Phaser from 'phaser';
import { music } from '../systems/music';
import { themeById } from '../data/musicThemes';
import { LEVELS } from '../data/levels';
import { STORY } from '../data/story';
import { sfx } from '../systems/audio';
import { Button } from '../ui/Button';
import { pf } from '../ui/touch';
import { C, GAME_H, GAME_W, TEXT, textStyle } from '../ui/theme';
import { loadSave } from '../systems/save';
import { motion } from '../ui/motion';
import { typewriter } from '../ui/typewriter';
import { addLighting } from '../ui/lighting';
import { litPanel, parallaxHills } from './story/StoryArt';

// A short chapter card after a region boss: the region's sky, a title and a few lines, then on to the next land.
export class StoryScene extends Phaser.Scene {
  constructor() {
    super('Story');
  }

  create(data: { levelId: string }): void {
    music.setMood('calm');
    music.setTheme(themeById('home'));
    const card = STORY[data.levelId];
    const index = LEVELS.findIndex((l) => l.id === data.levelId);
    if (!card) {
      this.scene.start('WorldMap', { focus: index });
      return;
    }
    const g = this.add.graphics();
    g.fillGradientStyle(card.sky[0], card.sky[0], card.sky[1], card.sky[1], 1);
    g.fillRect(0, 0, GAME_W, GAME_H);
    // drifting motes in the region's accent colour
    for (let i = 0; i < 36; i++) {
      const m = this.add.image(Phaser.Math.Between(0, GAME_W), Phaser.Math.Between(120, GAME_H), 'dot').setTint(card.accent).setScale(0.3).setAlpha(0.8);
      this.tweens.add({ targets: m, y: m.y - Phaser.Math.Between(60, 160), alpha: 0, duration: Phaser.Math.Between(2600, 5200), repeat: -1, delay: Phaser.Math.Between(0, 2000) });
    }
    const st = loadSave().settings;
    motion.reduced = !!st.reduceMotion;
    const still = motion.reduced || !!st.fxLow;
    parallaxHills(this, GAME_W, GAME_H, card.sky[1], still);
    addLighting(this, -1);
    litPanel(this, GAME_W / 2, 280, 880, 260, card.accent);
    const title = this.add.text(GAME_W / 2, 210, card.title, textStyle(52, TEXT.gold)).setOrigin(0.5).setAlpha(0).setName('storyTitle');
    const body = this.add
      .text(GAME_W / 2, 270, card.lines.join('\n'), { ...textStyle(pf(22), TEXT.cream, false), align: 'center', wordWrap: { width: 820 }, lineSpacing: 8 })
      .setOrigin(0.5, 0)
      .setAlpha(0);
    this.tweens.add({ targets: title, alpha: 1, y: 220, delay: 300, duration: 900 });
    // the chapter text types itself out (tap to finish it at once)
    const full = card.lines.join('\n');
    body.setText(full).setData('full', full);
    this.time.delayedCall(motion.reduced ? 0 : 1000, () => typewriter(this, body, full, { still: motion.reduced }));
    this.time.delayedCall(500, () => sfx.victory());
    this.time.delayedCall(1600, () => {
      const hasNext = index + 1 < LEVELS.length;
      new Button(this, GAME_W / 2 - 130, 530, hasNext ? 'Onward' : 'World Map', { width: 220, color: 0xff9f43, onClick: () => this.scene.start('WorldMap', { focus: hasNext ? index + 1 : index }) });
      new Button(this, GAME_W / 2 + 130, 530, 'Village', { width: 220, color: C.leaf, onClick: () => this.scene.start('Village') });
    });
  }
}
