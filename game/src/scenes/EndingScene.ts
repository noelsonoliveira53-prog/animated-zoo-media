import Phaser from 'phaser';
import { music } from '../systems/music';
import { LEVELS, totalStars } from '../data/levels';
import { loadSave } from '../systems/save';
import { sfx } from '../systems/audio';
import { Button } from '../ui/Button';
import { C, GAME_H, GAME_W, TEXT, textStyle } from '../ui/theme';

// Shown after the final level is won: night turns to dawn over the saved Grove.
export class EndingScene extends Phaser.Scene {
  constructor() {
    super('Ending');
  }

  create(): void {
    music.setMood('calm');
    const save = loadSave();
    const sky = this.add.graphics();
    const dawn = { t: 0 };
    const draw = () => {
      sky.clear();
      const top = Phaser.Display.Color.Interpolate.ColorWithColor(
        Phaser.Display.Color.ValueToColor(0x10182e),
        Phaser.Display.Color.ValueToColor(0x7fd3ff),
        100,
        dawn.t * 100,
      );
      const bottom = Phaser.Display.Color.Interpolate.ColorWithColor(
        Phaser.Display.Color.ValueToColor(0x2a2040),
        Phaser.Display.Color.ValueToColor(0xffd9a0),
        100,
        dawn.t * 100,
      );
      const tc = Phaser.Display.Color.GetColor(top.r, top.g, top.b);
      const bc = Phaser.Display.Color.GetColor(bottom.r, bottom.g, bottom.b);
      sky.fillGradientStyle(tc, tc, bc, bc, 1);
      sky.fillRect(0, 0, GAME_W, GAME_H);
    };
    draw();
    this.tweens.add({ targets: dawn, t: 1, duration: 5000, ease: 'Sine.easeInOut', onUpdate: draw });
    const sun = this.add.circle(GAME_W / 2, GAME_H + 60, 90, 0xffe066).setAlpha(0.9);
    this.tweens.add({ targets: sun, y: 560, duration: 5000, ease: 'Sine.easeOut' });

    // hills + the great oak
    const g = this.add.graphics();
    g.fillStyle(0x4b8f3a, 1);
    g.fillEllipse(300, 720, 900, 300);
    g.fillStyle(0x3f7f34, 1);
    g.fillEllipse(1000, 740, 900, 320);
    g.fillStyle(0x6b4a2b, 1);
    g.fillRect(GAME_W / 2 - 22, 560, 44, 120);
    for (const [dx, dy, r] of [[0, 540, 62], [-58, 568, 44], [58, 568, 44]]) {
      g.fillStyle(0x3f8a3a, 1);
      g.fillCircle(GAME_W / 2 + dx, dy, r);
    }
    // fireflies
    for (let i = 0; i < 30; i++) {
      const f = this.add.image(Phaser.Math.Between(0, GAME_W), Phaser.Math.Between(300, 700), 'dot').setTint(0xfff3a0).setScale(0.3);
      this.tweens.add({ targets: f, y: f.y - Phaser.Math.Between(40, 120), alpha: 0, duration: Phaser.Math.Between(2500, 5000), repeat: -1 });
    }

    const title = this.add.text(GAME_W / 2, 120, 'The Grove is Safe!', textStyle(64, TEXT.gold)).setOrigin(0.5).setAlpha(0);
    const lines = [
      'Old Murkmaw, Grimtusk and Vulkhar have fallen.',
      'The Keepers of the Grove rest under the great oak at last.',
      `Stars earned: ${totalStars(save.stars)} / ${LEVELS.length * 3}`,
    ];
    const body = this.add.text(GAME_W / 2, 215, lines.join('\n'), { ...textStyle(22, TEXT.cream, false), align: 'center' }).setOrigin(0.5, 0).setAlpha(0);
    this.tweens.add({ targets: title, alpha: 1, y: 130, delay: 600, duration: 1200 });
    this.tweens.add({ targets: body, alpha: 1, delay: 1600, duration: 1200 });
    this.time.delayedCall(800, () => sfx.victory());
    this.time.delayedCall(2400, () => {
      new Button(this, GAME_W / 2 - 130, 380, 'Village', { width: 220, color: C.leaf, onClick: () => this.scene.start('Village') });
      new Button(this, GAME_W / 2 + 130, 380, 'Main Menu', { width: 220, color: C.sky, onClick: () => this.scene.start('Menu') });
      this.add.text(GAME_W / 2, 440, 'Replay levels for 3 stars, train your heroes, and grow your village.', textStyle(16, TEXT.cream, false)).setOrigin(0.5);
    });
  }
}
