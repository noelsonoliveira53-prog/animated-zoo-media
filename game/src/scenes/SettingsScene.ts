import Phaser from 'phaser';
import { motion } from '../ui/motion';
import { music } from '../systems/music';
import { themeById } from '../data/musicThemes';
import { loadSave, resetProgress, writeSave } from '../systems/save';
import { sfx } from '../systems/audio';
import { Button } from '../ui/Button';
import { C, GAME_H, GAME_W, TEXT, textStyle } from '../ui/theme';
import { padHit } from '../ui/touch';

export class SettingsScene extends Phaser.Scene {
  constructor() {
    super('Settings');
  }

  create(): void {
    music.setMood('calm');
    music.setTheme(themeById('home'));
    const g = this.add.graphics();
    g.fillGradientStyle(0x22382a, 0x22382a, 0x10261b, 0x10261b, 1);
    g.fillRect(0, 0, GAME_W, GAME_H);
    g.fillStyle(C.ink, 0.8);
    g.fillRoundedRect(GAME_W / 2 - 360, 110, 720, 520, 26);
    this.add.text(GAME_W / 2, 60, 'Settings', textStyle(40, TEXT.gold)).setOrigin(0.5);
    new Button(this, 90, 44, 'Back', { width: 140, height: 50, fontSize: 20, color: C.sky, onClick: () => this.scene.start('Menu') });

    // Volume slider
    const save = loadSave();
    let volume = save.settings.volume;
    const sx = GAME_W / 2 - 220;
    const sw = 440;
    const sy = 220;
    this.add.text(GAME_W / 2 - 320, sy - 50, 'Volume (effects + music)', textStyle(22));
    const label = this.add.text(GAME_W / 2 + 250, sy, '', textStyle(22, TEXT.gold)).setOrigin(0, 0.5);
    const track = this.add.graphics();
    const knob = this.add.circle(0, sy, 18, C.gold).setStrokeStyle(4, C.ink).setInteractive({ draggable: true, useHandCursor: true });
    padHit(knob, 60);
    const drawSlider = () => {
      track.clear();
      track.fillStyle(0x000000, 0.5);
      track.fillRoundedRect(sx, sy - 7, sw, 14, 7);
      track.fillStyle(C.leaf, 1);
      track.fillRoundedRect(sx, sy - 7, sw * volume, 14, 7);
      knob.setX(sx + sw * volume);
      label.setText(`${Math.round(volume * 100)}%`);
    };
    const setVolume = (v: number, save2 = true) => {
      volume = Math.max(0, Math.min(1, v));
      drawSlider();
      const s = loadSave();
      s.settings.volume = volume;
      sfx.setVolume(volume, s.settings.muted);
      music.setVolume(volume, s.settings.music);
      if (save2) writeSave(s);
    };
    knob.on('drag', (_p: Phaser.Input.Pointer, dragX: number) => setVolume((dragX - sx) / sw, false));
    knob.on('dragend', () => {
      setVolume(volume);
      sfx.unlock();
      sfx.coin();
    });
    const trackZone = this.add.zone(sx + sw / 2, sy, sw, 40).setInteractive({ useHandCursor: true });
    trackZone.on('pointerdown', (p: Phaser.Input.Pointer) => {
      setVolume((p.worldX - sx) / sw);
      sfx.unlock();
      sfx.coin();
    });
    drawSlider();

    // Mute toggle
    const muteBtn = new Button(this, GAME_W / 2 - 125, 320, '', {
      width: 230,
      height: 56,
      fontSize: 22,
      color: 0xb07cff,
      onClick: () => {
        const s = loadSave();
        s.settings.muted = !s.settings.muted;
        writeSave(s);
        sfx.setVolume(s.settings.volume, s.settings.muted);
        sfx.unlock();
        sfx.click();
        muteBtn.label.setText(s.settings.muted ? 'Effects: Off' : 'Effects: On');
      },
    });
    muteBtn.label.setText(save.settings.muted ? 'Effects: Off' : 'Effects: On');

    // Music toggle
    const musicBtn = new Button(this, GAME_W / 2 + 125, 320, '', {
      width: 230,
      height: 52,
      fontSize: 20,
      color: 0x7fd3a0,
      onClick: () => {
        const s = loadSave();
        s.settings.music = !s.settings.music;
        writeSave(s);
        sfx.unlock();
        music.setVolume(s.settings.volume, s.settings.music);
        musicBtn.label.setText(s.settings.music ? 'Music: On' : 'Music: Off');
      },
    });
    musicBtn.label.setText(save.settings.music ? 'Music: On' : 'Music: Off');

    // Fullscreen (great on phones)
    const fsBtn = new Button(this, GAME_W / 2 - 125, 392, 'Fullscreen', {
      width: 230,
      height: 56,
      fontSize: 20,
      color: C.sky,
      onClick: () => {
        try {
          if (this.scale.isFullscreen) this.scale.stopFullscreen();
          else this.scale.startFullscreen();
        } catch {
          /* not allowed in this browser */
        }
      },
    });
    void fsBtn;

    // Reduce motion: no screen shake, no drifting weather overlays
    const motionLabel = (on: boolean) => (on ? 'Reduce motion: On' : 'Reduce motion: Off');
    const motionBtn = new Button(this, GAME_W / 2 + 125, 392, motionLabel(!!save.settings.reduceMotion), {
      width: 230,
      height: 56,
      fontSize: 18,
      color: C.leaf,
      onClick: () => {
        const s = loadSave();
        s.settings.reduceMotion = !s.settings.reduceMotion;
        motion.reduced = s.settings.reduceMotion;
        writeSave(s);
        sfx.click();
        motionBtn.label.setText(motionLabel(s.settings.reduceMotion));
      },
    });

    // Reset progress (two taps)
    let armed = false;
    const resetBtn = new Button(this, GAME_W / 2, 470, 'Reset progress', {
      width: 280,
      height: 56,
      fontSize: 20,
      color: C.danger,
      onClick: () => {
        if (!armed) {
          armed = true;
          resetBtn.label.setText('Tap again to confirm');
          this.time.delayedCall(3000, () => {
            armed = false;
            resetBtn.label.setText('Reset progress');
          });
          return;
        }
        writeSave(resetProgress(loadSave()));
        sfx.defeat();
        resetBtn.label.setText('Progress reset');
        armed = false;
      },
    });
    this.add.text(GAME_W / 2, 516, 'Clears stars, village, heroes, army and Field Guide. Settings are kept.', textStyle(14, TEXT.dim, false)).setOrigin(0.5);

    this.add
      .text(GAME_W / 2, 570, 'Grovewatch: Sanctuary Siege\nAll art and sound are generated in code.', { ...textStyle(16, TEXT.cream, false), align: 'center' })
      .setOrigin(0.5);
  }
}
