import Phaser from 'phaser';
import { BootScene } from './scenes/BootScene';
import { MenuScene } from './scenes/MenuScene';
import { BattleScene } from './scenes/BattleScene';
import { WorldMapScene } from './scenes/WorldMapScene';
import { VillageScene } from './scenes/VillageScene';
import { GAME_H, GAME_W } from './ui/theme';

const game = new Phaser.Game({
  type: Phaser.AUTO,
  parent: 'game',
  width: GAME_W,
  height: GAME_H,
  backgroundColor: '#10261b',
  scale: { mode: Phaser.Scale.FIT, autoCenter: Phaser.Scale.CENTER_BOTH },
  input: { activePointers: 2 },
  scene: [BootScene, MenuScene, WorldMapScene, VillageScene, BattleScene],
});

// Expose for automated tests / debugging.
(window as unknown as { __game: Phaser.Game }).__game = game;
