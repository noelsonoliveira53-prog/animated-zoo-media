import type Phaser from 'phaser';
// Visual constants shared by every scene: one palette, one font stack.
export const GAME_W = 1280;
export const GAME_H = 720;

export const FONT = '"Trebuchet MS", "Segoe UI", system-ui, sans-serif';

export const C = {
  ink: 0x1d2b1f,
  panel: 0x22382a,
  panelLight: 0x2f4d39,
  cream: 0xfff4d6,
  gold: 0xffc93c,
  heart: 0xff5d6c,
  leaf: 0x8fdc5a,
  danger: 0xe2483d,
  sky: 0x7fd3ff,
};

export const TEXT = {
  cream: '#fff4d6',
  gold: '#ffc93c',
  heart: '#ff8a95',
  ink: '#1d2b1f',
  dim: '#b9c9b0',
};

export function textStyle(size: number, color = TEXT.cream, bold = true): Phaser.Types.GameObjects.Text.TextStyle {
  return {
    fontFamily: FONT,
    fontSize: `${size}px`,
    color,
    fontStyle: bold ? 'bold' : 'normal',
    stroke: '#1d2b1f',
    strokeThickness: Math.max(2, Math.round(size / 6)),
  };
}
