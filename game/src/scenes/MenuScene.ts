import Phaser from 'phaser';
import { LEVELS } from '../data/levels';
import { loadSave } from '../systems/save';
import { sfx } from '../systems/audio';
import { Button } from '../ui/Button';
import { GAME_H, GAME_W, textStyle, TEXT } from '../ui/theme';

export class MenuScene extends Phaser.Scene {
  constructor() {
    super('Menu');
  }

  create(): void {
    const save = loadSave();
    sfx.setVolume(save.settings.volume, save.settings.muted);

    // layered hills backdrop
    const g = this.add.graphics();
    g.fillGradientStyle(0x7fd3ff, 0x7fd3ff, 0xc8f0ff, 0xc8f0ff, 1);
    g.fillRect(0, 0, GAME_W, GAME_H);
    const hills: [number, number, number][] = [
      [0x86c56a, 470, 90],
      [0x6aae52, 540, 70],
      [0x52953f, 620, 60],
    ];
    for (const [color, base, amp] of hills) {
      g.fillStyle(color, 1);
      g.beginPath();
      g.moveTo(0, GAME_H);
      for (let x = 0; x <= GAME_W; x += 20) g.lineTo(x, base - Math.sin(x / 170 + base) * amp * 0.5 - Math.cos(x / 90) * amp * 0.2);
      g.lineTo(GAME_W, GAME_H);
      g.closePath();
      g.fillPath();
    }
    // drifting fireflies
    for (let i = 0; i < 24; i++) {
      const dot = this.add.image(Phaser.Math.Between(0, GAME_W), Phaser.Math.Between(200, 700), 'dot').setTint(0xfff3a0).setScale(0.35).setAlpha(0.8);
      this.tweens.add({
        targets: dot,
        y: dot.y - Phaser.Math.Between(30, 80),
        x: dot.x + Phaser.Math.Between(-40, 40),
        alpha: 0.2,
        duration: Phaser.Math.Between(1800, 3600),
        yoyo: true,
        repeat: -1,
        ease: 'Sine.easeInOut',
      });
    }

    const title = this.add.text(GAME_W / 2, 150, 'GROVEWATCH', textStyle(96, TEXT.gold)).setOrigin(0.5);
    title.setStroke('#1d2b1f', 14);
    this.tweens.add({ targets: title, y: 160, duration: 1600, yoyo: true, repeat: -1, ease: 'Sine.easeInOut' });
    this.add.text(GAME_W / 2, 238, 'Sanctuary Siege', textStyle(36)).setOrigin(0.5);
    this.add
      .text(GAME_W / 2, 290, 'Hold the Mossgate. Stop the Murkhorde.', textStyle(20, TEXT.cream, false))
      .setOrigin(0.5);

    // Level buttons
    LEVELS.forEach((lvl, i) => {
      const y = 400 + i * 90;
      new Button(this, GAME_W / 2, y, lvl.name, {
        width: 360,
        height: 68,
        fontSize: 28,
        onClick: () => this.scene.start('Battle', { levelIndex: i }),
      });
      const stars = save.stars[lvl.id] ?? 0;
      for (let s = 0; s < 3; s++) {
        this.add.image(GAME_W / 2 + 210 + s * 34, y, s < stars ? 'star' : 'star_empty').setScale(0.6);
      }
    });

    this.add.text(16, GAME_H - 30, 'v0.1 — prototype', textStyle(14, TEXT.dim, false));
  }
}
