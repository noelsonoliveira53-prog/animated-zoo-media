import Phaser from 'phaser';
import { C, textStyle } from './theme';
import { sfx } from '../systems/audio';
import { fitWidth, padHit, pf } from './touch';

export interface ButtonOpts {
  width?: number;
  height?: number;
  color?: number;
  fontSize?: number;
  onClick: () => void;
}

/** Chunky rounded button with press feedback. Works with mouse and touch. */
export class Button extends Phaser.GameObjects.Container {
  private bg: Phaser.GameObjects.Graphics;
  readonly label: Phaser.GameObjects.Text;
  private bw: number;
  private bh: number;
  private color: number;
  private enabled = true;

  constructor(scene: Phaser.Scene, x: number, y: number, text: string, opts: ButtonOpts) {
    super(scene, x, y);
    this.bw = opts.width ?? 180;
    this.bh = opts.height ?? 56;
    this.color = opts.color ?? C.leaf;
    this.bg = scene.add.graphics();
    // small labels grow on phones (pf), and every label shrinks to fit inside the button, now and after setText
    this.label = scene.add.text(0, -2, text, textStyle(pf(opts.fontSize ?? 24))).setOrigin(0.5);
    const setText = this.label.setText.bind(this.label);
    this.label.setText = ((value: string | string[]) => {
      setText(value);
      this.fitLabel();
      return this.label;
    }) as typeof this.label.setText;
    this.add([this.bg, this.label]);
    this.draw();
    this.fitLabel();
    this.setSize(this.bw, this.bh);
    this.setInteractive({ useHandCursor: true });
    padHit(this);
    this.on('pointerdown', (_p: Phaser.Input.Pointer, _x: number, _y: number, ev: Phaser.Types.Input.EventData) => {
      ev?.stopPropagation();
      if (!this.enabled) return;
      sfx.unlock();
      sfx.click();
      scene.tweens.add({ targets: this, scale: 0.92, duration: 60, yoyo: true });
      opts.onClick();
    });
    this.on('pointerover', () => this.enabled && this.setScale(1.04));
    this.on('pointerout', () => this.setScale(1));
    scene.add.existing(this);
  }

  private fitLabel(): void {
    this.label.setScale(1);
    fitWidth(this.label, this.bw - 16);
  }

  setEnabled(on: boolean): this {
    this.enabled = on;
    this.setAlpha(on ? 1 : 0.5);
    return this;
  }

  setColor(color: number): this {
    this.color = color;
    this.draw();
    return this;
  }

  private draw(): void {
    const w = this.bw;
    const h = this.bh;
    const dark = Phaser.Display.Color.IntegerToColor(this.color).darken(30).color;
    this.bg.clear();
    this.bg.fillStyle(C.ink, 1);
    this.bg.fillRoundedRect(-w / 2 - 3, -h / 2 - 3, w + 6, h + 9, 16);
    this.bg.fillStyle(dark, 1);
    this.bg.fillRoundedRect(-w / 2, -h / 2 + 4, w, h, 14);
    this.bg.fillStyle(this.color, 1);
    this.bg.fillRoundedRect(-w / 2, -h / 2, w, h - 2, 14);
    this.bg.fillStyle(0xffffff, 0.25);
    this.bg.fillRoundedRect(-w / 2 + 8, -h / 2 + 5, w - 16, h * 0.28, 8);
  }
}
