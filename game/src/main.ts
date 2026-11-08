import Phaser from 'phaser';
import { sfx } from './systems/audio';
import './systems/dev'; // reads the dev-mode switch before any scene checks level locks
import { BootScene } from './scenes/BootScene';
import { MenuScene } from './scenes/MenuScene';
import { BattleScene } from './scenes/BattleScene';
import { WorldMapScene } from './scenes/WorldMapScene';
import { VillageScene } from './scenes/VillageScene';
import { EndingScene } from './scenes/EndingScene';
import { StoryScene } from './scenes/StoryScene';
import { RaidScene } from './scenes/RaidScene';
import { FieldGuideScene } from './scenes/FieldGuideScene';
import { SettingsScene } from './scenes/SettingsScene';
import { AchievementsScene } from './scenes/AchievementsScene';
import { GAME_H, GAME_W } from './ui/theme';
import { music } from './systems/music';

const game = new Phaser.Game({
  type: Phaser.AUTO,
  parent: 'game',
  width: GAME_W,
  height: GAME_H,
  backgroundColor: '#10261b',
  scale: { mode: Phaser.Scale.FIT, autoCenter: Phaser.Scale.CENTER_BOTH },
  input: { activePointers: 2 },
  scene: [BootScene, MenuScene, WorldMapScene, VillageScene, BattleScene, EndingScene, StoryScene, RaidScene, FieldGuideScene, SettingsScene, AchievementsScene],
});

// No long-press context menu on touch devices (it interrupts tower menus).
window.addEventListener('contextmenu', (e) => e.preventDefault());

// Expose for automated tests / debugging.
(window as unknown as { __game: Phaser.Game; __music: typeof music }).__game = game;
(window as unknown as { __music: typeof music }).__music = music;
(window as unknown as { __sfx: typeof sfx }).__sfx = sfx; // test handle, like __music
