import Phaser from 'phaser';
import { GAME_H, GAME_W } from './theme';

/** Shared scene lighting: warm light pooling from the top-left and a soft vignette round the edges. */
export function addLighting(scene: Phaser.Scene, depth: number): Phaser.GameObjects.Image {
  const key = 'fx_vignette';
  if (!scene.textures.exists(key)) {
    const tex = scene.textures.createCanvas(key, GAME_W, GAME_H);
    if (tex) {
      const ctx = tex.getContext();
      const light = ctx.createRadialGradient(GAME_W * 0.25, GAME_H * 0.15, 40, GAME_W * 0.25, GAME_H * 0.15, GAME_W * 0.75);
      light.addColorStop(0, 'rgba(255,240,200,0.10)');
      light.addColorStop(1, 'rgba(255,240,200,0)');
      ctx.fillStyle = light;
      ctx.fillRect(0, 0, GAME_W, GAME_H);
      const vig = ctx.createRadialGradient(GAME_W / 2, GAME_H / 2, GAME_H * 0.42, GAME_W / 2, GAME_H / 2, GAME_W * 0.68);
      vig.addColorStop(0, 'rgba(10,14,24,0)');
      vig.addColorStop(1, 'rgba(10,14,24,0.38)');
      ctx.fillStyle = vig;
      ctx.fillRect(0, 0, GAME_W, GAME_H);
      tex.refresh();
    }
  }
  return scene.add.image(0, 0, key).setOrigin(0, 0).setDepth(depth);
}
