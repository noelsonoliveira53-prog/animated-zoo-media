import Phaser from 'phaser';
import { motion } from '../ui/motion';
import { pf } from '../ui/touch';
import { music } from '../systems/music';
import { themeById } from '../data/musicThemes';
import { LEVELS, isLevelUnlocked, totalStars } from '../data/levels';
import { dailyFor, todayString } from '../systems/daily';
import { DAILY_MODIFIERS } from '../data/daily';
import { ensureVillage, loadSave, writeSave } from '../systems/save';
import { heroTrainCost, trainHero } from '../systems/village';
import { HERO_MAX_LEVEL } from '../data/heroes';
import { HEROES, HERO_ORDER } from '../data/heroes';
import { sfx } from '../systems/audio';
import { Button } from '../ui/Button';
import { C, GAME_H, GAME_W, textStyle, TEXT } from '../ui/theme';

export class MenuScene extends Phaser.Scene {
  constructor() {
    super('Menu');
  }

  create(): void {
    music.setMood('calm');
    music.setTheme(themeById('home'));
    const save = loadSave();
    sfx.setVolume(save.settings.volume, save.settings.muted);
    motion.reduced = !!save.settings.reduceMotion;
    music.setVolume(save.settings.volume, save.settings.music);

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

    // Campaign + village entries, and progress
    new Button(this, 460, 390, 'Campaign', {
      width: 360,
      height: 74,
      fontSize: 32,
      color: 0xff9f43,
      onClick: () => this.scene.start('WorldMap'),
    });
    new Button(this, 460, 480, 'Village', {
      width: 360,
      height: 74,
      fontSize: 32,
      color: C.leaf,
      onClick: () => this.scene.start('Village'),
    });
    this.add.image(GAME_W - 150, 30, 'star').setScale(0.55);
    this.add.text(GAME_W - 128, 30, `${totalStars(save.stars)} / ${LEVELS.length * 3}`, textStyle(20)).setOrigin(0, 0.5);
    this.buildDaily();

    this.buildHeroPicker();
    new Button(this, 240, 662, 'Field Guide', { width: 190, height: 52, fontSize: 19, color: 0xd9c39a, onClick: () => this.scene.start('FieldGuide') });
    new Button(this, 460, 662, 'Achievements', { width: 210, height: 52, fontSize: 19, color: C.gold, onClick: () => this.scene.start('Achievements') });
    new Button(this, 680, 662, 'Settings', { width: 190, height: 52, fontSize: 19, color: C.sky, onClick: () => this.scene.start('Settings') });

    this.add.text(GAME_W - 16, GAME_H - 24, 'v0.9', textStyle(pf(14), TEXT.dim, false)).setOrigin(1, 0.5);
  }

  private buildDaily(): void {
    const save = loadSave();
    const unlocked = LEVELS.filter((_, i) => isLevelUnlocked(i, save.stars)).length;
    const d = dailyFor(todayString(), unlocked);
    const done = save.dailyDone === d.date;
    const names = d.modifiers.map((id) => DAILY_MODIFIERS.find((m) => m.id === id)!.name).join(' + ');
    const b = new Button(this, 460, 562, done ? 'Daily: done ✓ (replay)' : `Daily: ${LEVELS[d.levelIndex].name}`, {
      width: 360,
      height: 54,
      fontSize: 18,
      color: done ? 0x6a8a6a : 0xb07cff,
      onClick: () => this.scene.start('Battle', { daily: true }),
    });
    void b;
    this.add
      .text(460, 600, done ? `Come back tomorrow for a new challenge` : `${names}  •  Win: +${d.reward.coins}c +${d.reward.glowsap}s`, textStyle(pf(13), TEXT.cream, false))
      .setOrigin(0.5);
  }

  private buildHeroPicker(): void {
    const save = loadSave();
    let index = Math.max(0, HERO_ORDER.indexOf(save.hero));
    const x = 1040;
    const y = 470;
    const panel = this.add.graphics();
    panel.fillStyle(C.ink, 0.75);
    panel.fillRoundedRect(x - 190, y - 130, 380, 320, 22);
    this.add.text(x, y - 108, 'Choose your Hero', textStyle(22, TEXT.gold)).setOrigin(0.5);
    const sprite = this.add.image(x, y - 36, 'hero_bramble').setScale(1.6);
    this.tweens.add({ targets: sprite, y: sprite.y - 6, yoyo: true, repeat: -1, duration: 800, ease: 'Sine.easeInOut' });
    const name = this.add.text(x, y + 22, '', textStyle(24)).setOrigin(0.5);
    const info = this.add
      .text(x, y + 80, '', { ...textStyle(14, TEXT.cream, false), align: 'center', wordWrap: { width: 340 } })
      .setOrigin(0.5);

    const rankText = this.add.text(x - 170, y + 152, '', textStyle(15, TEXT.gold)).setOrigin(0, 0.5);
    const trainBtn = new Button(this, x + 95, y + 152, 'Train', {
      width: 170,
      height: 46,
      fontSize: 16,
      color: 0x9be86a,
      onClick: () => {
        const s = loadSave();
        const v = ensureVillage(s);
        const r = trainHero(v, s.heroRanks, HERO_ORDER[index]);
        if (r.ok) {
          writeSave(s);
          sfx.victory();
        } else {
          sfx.leak();
          this.children.getByName('trainMsg')?.destroy();
          const t = this.add.text(x, y + 200, r.reason ?? '', textStyle(pf(15), TEXT.heart)).setOrigin(0.5).setName('trainMsg');
          this.tweens.add({ targets: t, alpha: 0, delay: 1200, duration: 400, onComplete: () => t.destroy() });
        }
        show();
      },
    });

    const show = () => {
      const h = HEROES[HERO_ORDER[index]];
      sprite.setTexture(`hero_${h.id}`);
      name.setText(`${h.name} the ${h.title}`);
      info.setText(`${h.passive.text}\n${h.active.name}: ${h.active.text}`);
      const s = loadSave();
      const rank = s.heroRanks[h.id] ?? 0;
      const cost = heroTrainCost(rank);
      rankText.setText(`Starts at Lv ${Math.min(HERO_MAX_LEVEL, rank + 1)}  ${'●'.repeat(rank)}${'○'.repeat(Math.max(0, 5 - rank))}`);
      trainBtn.label.setText(cost === null ? 'Max rank' : `Train: ${cost} sap`);
      trainBtn.setEnabled(cost !== null && (s.village?.glowsap ?? 600) >= cost);
    };
    const pick = (dir: number) => {
      index = (index + dir + HERO_ORDER.length) % HERO_ORDER.length;
      const s = loadSave();
      s.hero = HERO_ORDER[index];
      writeSave(s);
      show();
    };
    new Button(this, x - 140, y - 36, '<', { width: 56, height: 56, color: C.sky, onClick: () => pick(-1) });
    new Button(this, x + 140, y - 36, '>', { width: 56, height: 56, color: C.sky, onClick: () => pick(1) });
    show();
  }
}
