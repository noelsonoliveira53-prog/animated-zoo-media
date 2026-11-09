import { leafReveal } from '../ui/transition';
import Phaser from 'phaser';
import { STORE_ITEMS, STORE_TIERS, type StoreItem } from '../data/store';
import { themeById } from '../data/musicThemes';
import { buyItem, nextPrice, rankOf, tierOpen, totalRanks } from '../systems/store';
import { devOn } from '../systems/dev';
import { ensureVillage, loadSave, writeSave, type SaveData } from '../systems/save';
import { music } from '../systems/music';
import { sfx } from '../systems/audio';
import { Button } from '../ui/Button';
import { fitWidth, pf } from '../ui/touch';
import { C, GAME_H, GAME_W, TEXT, textStyle } from '../ui/theme';
import { motion } from '../ui/motion';

// The Keeper's Store: three tier rows of permanent upgrades, bought with village coins and glowsap.

const CARD_W = 372;
const CARD_H = 150;
const ROW_Y = [222, 406, 590];

export class StoreScene extends Phaser.Scene {
  private root!: Phaser.GameObjects.Container;
  private back = 'Menu';
  private burst!: Phaser.GameObjects.Particles.ParticleEmitter;
  private sweepTimers: Phaser.Time.TimerEvent[] = [];

  constructor() {
    super('Store');
  }

  init(data?: { from?: string }): void {
    this.back = data?.from ?? 'Menu';
  }

  create(): void {
    leafReveal(this, GAME_W, GAME_H); // a gust of leaves uncovers the scene
    this.sweepTimers = [];
    music.setMood('calm');
    music.setTheme(themeById('home'));
    const save0 = loadSave();
    motion.reduced = !!save0.settings.reduceMotion;
    motion.lowFx = !!save0.settings.fxLow;
    const g = this.add.graphics();
    g.fillGradientStyle(0x2a2238, 0x2a2238, 0x14101e, 0x14101e, 1);
    g.fillRect(0, 0, GAME_W, GAME_H);
    // soft lantern glow behind the counter
    for (let k = 0; k < 3; k++) this.add.circle(GAME_W / 2 + (k - 1) * 420, 120, 220, 0xffc860, 0.05).setBlendMode(Phaser.BlendModes.ADD);
    this.add.text(GAME_W / 2, 42, "Keeper's Store", textStyle(40, TEXT.gold)).setOrigin(0.5).setStroke('#1d1428', 8);
    new Button(this, 90, 42, 'Back', { width: 140, height: 50, fontSize: 20, color: C.sky, onClick: () => this.scene.start(this.back) });
    this.burst = this.add.particles(0, 0, 'dot', { speed: { min: 80, max: 260 }, scale: { start: 0.7, end: 0 }, lifespan: 700, gravityY: 260, emitting: false, blendMode: Phaser.BlendModes.ADD });
    this.burst.setDepth(50);
    this.build();
  }

  private build(): void {
    this.root?.destroy();
    // the shine loops belong to the cards being rebuilt
    for (const t of this.sweepTimers) t.remove();
    this.sweepTimers = [];
    this.root = this.add.container(0, 0);
    const save = loadSave();
    const v = ensureVillage(save);
    // village purse, top right
    const purse = this.add.graphics();
    purse.fillStyle(C.ink, 0.8);
    purse.fillRoundedRect(GAME_W - 380, 18, 360, 50, 14);
    this.root.add(purse);
    this.root.add(this.add.image(GAME_W - 352, 43, 'icon_coin').setScale(0.9));
    this.root.add(this.add.text(GAME_W - 332, 43, devOn() ? '∞' : `${Math.floor(v.coins)}`, textStyle(20, TEXT.gold)).setOrigin(0, 0.5));
    this.root.add(this.add.image(GAME_W - 180, 43, 'icon_sap').setScale(0.9));
    this.root.add(this.add.text(GAME_W - 160, 43, devOn() ? '∞' : `${Math.floor(v.glowsap)}`, textStyle(20, '#c8ff8a')).setOrigin(0, 0.5));
    this.root.add(this.add.text(GAME_W / 2, 84, `Permanent upgrades for every battle  •  ${totalRanks(save)} ranks owned${devOn() ? '  •  DEV: purchases are free' : ''}`, textStyle(pf(14), TEXT.dim, false)).setOrigin(0.5));
    if (devOn()) {
      this.root.add(
        new Button(this, 90, 100, 'Refund all', {
          width: 140,
          height: 36,
          fontSize: 14,
          color: 0xff5a8a,
          onClick: () => {
            const s = loadSave();
            s.store = {};
            writeSave(s);
            this.build();
          },
        }),
      );
    }
    STORE_TIERS.forEach((t, row) => {
      const y = ROW_Y[row];
      const open = tierOpen(save, t.tier);
      this.root.add(this.add.text(36, y - CARD_H / 2 - 14, `${['I', 'II', 'III'][row]}  ${t.name}`, textStyle(17, open ? TEXT.gold : TEXT.dim)).setOrigin(0, 0.5));
      const items = STORE_ITEMS.filter((i) => i.tier === t.tier);
      items.forEach((item, k) => this.card(save, item, 36 + CARD_W / 2 + k * (CARD_W + 26), y + 6, open));
      if (!open) {
        const need = t.needRanks - totalRanks(save, t.tier);
        const lock = this.add.graphics();
        lock.fillStyle(0x0a0812, 0.62);
        lock.fillRoundedRect(28, y + 6 - CARD_H / 2 - 6, GAME_W - 56, CARD_H + 12, 16);
        this.root.add(lock);
        this.root.add(this.lockIcon(GAME_W / 2 - 170, y + 6));
        this.root.add(this.add.text(GAME_W / 2 - 140, y + 6, `Buy ${need} more rank${need === 1 ? '' : 's'} to open`, textStyle(22, TEXT.cream)).setOrigin(0, 0.5));
      }
    });
  }

  private card(save: SaveData, item: StoreItem, x: number, y: number, open: boolean): void {
    const c = this.add.container(x, y);
    this.root.add(c);
    const rank = rankOf(save, item.id);
    const maxed = rank >= item.maxRank;
    const bg = this.add.graphics();
    bg.fillStyle(0x000000, 0.3);
    bg.fillRoundedRect(-CARD_W / 2 + 4, -CARD_H / 2 + 6, CARD_W, CARD_H, 16);
    bg.fillStyle(maxed ? 0x3a3020 : C.panel, 1);
    bg.fillRoundedRect(-CARD_W / 2, -CARD_H / 2, CARD_W, CARD_H, 16);
    // glossy upper half and a thin inner rim light
    bg.fillStyle(0xffffff, 0.035);
    bg.fillRoundedRect(-CARD_W / 2 + 3, -CARD_H / 2 + 3, CARD_W - 6, 34, { tl: 14, tr: 14, bl: 6, br: 6 }); // gloss behind the title only
    bg.lineStyle(1, 0xffffff, 0.12);
    bg.strokeRoundedRect(-CARD_W / 2 + 3, -CARD_H / 2 + 3, CARD_W - 6, CARD_H - 6, 14);
    bg.lineStyle(3, maxed ? 0xffc83a : item.color, open ? 0.9 : 0.3);
    bg.strokeRoundedRect(-CARD_W / 2, -CARD_H / 2, CARD_W, CARD_H, 16);
    c.add(bg);
    if (maxed && !this.still()) c.add(this.sweep(CARD_W, CARD_H, 0xffe08a, 0.16, 3600));
    c.add(this.icon(item, -CARD_W / 2 + 54, -8));
    c.add(fitWidth(this.add.text(-CARD_W / 2 + 104, -CARD_H / 2 + 22, item.name, textStyle(19, TEXT.cream)).setOrigin(0, 0.5), 250));
    // the description steps down from the phone size until it ends above the price row
    const desc = this.add.text(-CARD_W / 2 + 104, -CARD_H / 2 + 44, `${item.text} per rank`, { ...textStyle(pf(13), TEXT.dim, false), wordWrap: { width: 250 } }).setOrigin(0, 0);
    for (let size = pf(13); size > 12 && desc.y + desc.height > CARD_H / 2 - 58; size--) desc.setFontSize(size);
    c.add(desc);
    // rank pips
    for (let r = 0; r < item.maxRank; r++) {
      const pip = this.add.circle(-CARD_W / 2 + 22 + r * 18, CARD_H / 2 - 22, 6, r < rank ? item.color : 0x2a2a34).setStrokeStyle(2, C.ink, 1);
      c.add(pip);
    }
    if (maxed) {
      c.add(this.add.text(CARD_W / 2 - 18, CARD_H / 2 - 22, 'MAX', textStyle(18, TEXT.gold)).setOrigin(1, 0.5));
      return;
    }
    const price = nextPrice(save, item)!;
    const v = ensureVillage(save);
    const afford = devOn() || (v.coins >= (price.coins ?? 0) && v.glowsap >= (price.glowsap ?? 0));
    // next-rank price on its own line, clear of the Buy button
    const py = CARD_H / 2 - 47;
    // laid out by measured widths, so bigger phone text never runs into the icons
    const nextT = this.add.text(-CARD_W / 2 + 104, py, 'Next:', textStyle(pf(13), TEXT.dim, false)).setOrigin(0, 0.5);
    const coinI = this.add.image(nextT.x + nextT.width + 12, py, 'icon_coin').setScale(0.6);
    const coinT = this.add.text(coinI.x + 12, py, `${price.coins}`, textStyle(pf(14), afford ? TEXT.gold : TEXT.heart)).setOrigin(0, 0.5);
    const sapI = this.add.image(coinT.x + coinT.width + 16, py, 'icon_sap').setScale(0.6);
    const sapT = this.add.text(sapI.x + 12, py, `${price.glowsap}`, textStyle(pf(14), afford ? '#c8ff8a' : TEXT.heart)).setOrigin(0, 0.5);
    c.add([nextT, coinI, coinT, sapI, sapT]);
    if (!open) return;
    const btn = new Button(this, CARD_W / 2 - 52, CARD_H / 2 - 24, 'Buy', {
      width: 84,
      height: 40,
      fontSize: 18,
      color: afford ? 0xff9f43 : 0x6a6a7a,
      onClick: () => this.buy(item, x, y),
    });
    btn.setName(`buy_${item.id}`);
    c.add(btn);
    // affordable: a glint sweeps across the Buy button now and then
    if (afford && !this.still()) {
      const glint = this.sweep(84, 36, 0xffffff, 0.45, 2600);
      glint.setPosition(CARD_W / 2 - 52, CARD_H / 2 - 24);
      c.add(glint);
    }
  }

  private buy(item: StoreItem, x: number, y: number): void {
    const s = loadSave();
    const openBefore = STORE_TIERS.filter((t) => tierOpen(s, t.tier)).length;
    if (devOn()) {
      // dev mode: free purchases for testing — fund the purchase, buy, then restore the purse
      const v = ensureVillage(s);
      const keep = { coins: v.coins, glowsap: v.glowsap };
      v.coins = v.glowsap = 1e9;
      const r = buyItem(s, item.id);
      v.coins = keep.coins;
      v.glowsap = keep.glowsap;
      if (!r.ok) return this.toast(r.reason ?? 'Cannot buy');
    } else {
      const r = buyItem(s, item.id);
      if (!r.ok) {
        sfx.click();
        return this.toast(r.reason === 'Not enough resources' ? 'Not enough coins or glowsap' : (r.reason ?? 'Cannot buy'));
      }
    }
    writeSave(s);
    sfx.build();
    sfx.coin();
    this.payFlight(x, y);
    const ring = this.add.circle(x, y, 60, item.color, 0).setStrokeStyle(4, item.color, 0.9).setDepth(45).setScale(0.4);
    this.tweens.add({ targets: ring, scale: 2.4, alpha: 0, duration: 520, ease: 'Quad.easeOut', onComplete: () => ring.destroy() });
    this.burst.setParticleTint(item.color);
    this.burst.explode(26, x, y);
    this.burst.setParticleTint(0xffd060);
    this.burst.explode(14, x, y);
    const flash = this.add.rectangle(x, y, CARD_W, CARD_H, 0xffffff, 0.5).setDepth(40).setBlendMode(Phaser.BlendModes.ADD);
    this.tweens.add({ targets: flash, alpha: 0, duration: 260, onComplete: () => flash.destroy() });
    const rank = rankOf(s, item.id);
    const pop = this.add.text(x, y - 40, `${item.name} ${rank}/${item.maxRank}`, textStyle(20, TEXT.gold)).setOrigin(0.5).setDepth(60);
    this.tweens.add({ targets: pop, y: y - 90, alpha: 0, duration: 900, onComplete: () => pop.destroy() });
    this.build();
    const opened = STORE_TIERS.filter((t) => tierOpen(s, t.tier));
    if (opened.length > openBefore) this.celebrate(opened[opened.length - 1].name, opened.length - 1);
  }

  /** A new tier opened: a golden banner sweeps in over its row, with a fanfare and a shower of sparks. */
  private celebrate(name: string, row: number): void {
    const y = ROW_Y[row] + 6;
    sfx.victory();
    const band = this.add.rectangle(GAME_W / 2, y, GAME_W, 70, 0x1a1208, 0.85).setDepth(70).setScale(0, 1);
    const txt = this.add.text(GAME_W / 2, y, `${name} unlocked!`, textStyle(34, TEXT.gold)).setOrigin(0.5).setDepth(71).setAlpha(0).setStroke('#1d1428', 8);
    this.tweens.add({ targets: band, scaleX: 1, duration: 260, ease: 'Cubic.easeOut' });
    this.tweens.add({ targets: txt, alpha: 1, duration: 260, delay: 120 });
    this.burst.setParticleTint(0xffd060);
    for (let k = 0; k < 6; k++) this.time.delayedCall(k * 90, () => this.burst.explode(16, 160 + k * 190, y));
    this.tweens.add({ targets: [band, txt], alpha: 0, delay: 1700, duration: 400, onComplete: () => { band.destroy(); txt.destroy(); } });
  }

  private still(): boolean {
    return motion.reduced || motion.lowFx;
  }

  /**
   * A slanted band of light that slides across a w×h box (centered on 0,0) and waits, on a loop. The band is
   * narrow and fades in and out at the edges, so no mask is needed.
   */
  private sweep(w: number, h: number, color: number, alpha: number, every: number): Phaser.GameObjects.Container {
    const box = this.add.container(0, 0);
    const band = this.add.polygon(0, 0, [0, h / 2 - 3, 12, h / 2 - 3, 24, -h / 2 + 3, 12, -h / 2 + 3], color, 1).setBlendMode(Phaser.BlendModes.ADD).setAlpha(0);
    box.add(band);
    const run = () => {
      if (!band.active) return;
      band.x = -w / 2 + 2;
      band.setAlpha(0);
      this.tweens.add({ targets: band, x: w / 2 - 26, duration: 520, ease: 'Sine.easeInOut' });
      this.tweens.add({ targets: band, alpha, duration: 260, yoyo: true, ease: 'Sine.easeInOut' });
    };
    this.sweepTimers.push(this.time.addEvent({ delay: every, loop: true, startAt: Math.random() * every, callback: run }));
    return box;
  }

  /** On purchase: a few coins and sap drops fly from the purse into the card. */
  private payFlight(x: number, y: number): void {
    if (this.still()) return;
    for (let k = 0; k < 8; k++) {
      const sap = k % 2 === 1;
      const icon = this.add.image(GAME_W - (sap ? 180 : 352), 43, sap ? 'icon_sap' : 'icon_coin').setScale(0.7).setDepth(55);
      this.tweens.add({
        targets: icon,
        x: x + (Math.random() - 0.5) * 60,
        y: y + (Math.random() - 0.5) * 30,
        scale: 0.3,
        duration: 380 + k * 40,
        ease: 'Cubic.easeIn',
        onComplete: () => icon.destroy(),
      });
    }
  }

  private toast(msg: string): void {
    const t = this.add.text(GAME_W / 2, GAME_H - 30, msg, textStyle(20, TEXT.heart)).setOrigin(0.5).setDepth(60);
    this.tweens.add({ targets: t, alpha: 0, delay: 900, duration: 400, onComplete: () => t.destroy() });
  }

  private lockIcon(x: number, y: number): Phaser.GameObjects.Graphics {
    const g = this.add.graphics();
    g.lineStyle(4, 0xd8d0c0, 1);
    g.beginPath();
    g.arc(x, y - 6, 9, Math.PI, 0);
    g.strokePath();
    g.fillStyle(0xd8d0c0, 1);
    g.fillRoundedRect(x - 13, y - 6, 26, 20, 4);
    g.fillStyle(0x2a2238, 1);
    g.fillCircle(x, y + 3, 3);
    return g;
  }

  /** A code-drawn emblem for each upgrade, picked from its first effect. */
  private icon(item: StoreItem, x: number, y: number): Phaser.GameObjects.Graphics {
    const g = this.add.graphics();
    g.fillStyle(0x000000, 0.25);
    g.fillCircle(x + 2, y + 3, 34);
    g.fillStyle(item.color, 1);
    g.fillCircle(x, y, 34);
    g.lineStyle(3, C.ink, 1);
    g.strokeCircle(x, y, 34);
    g.fillStyle(0xffffff, 0.25);
    g.fillEllipse(x - 10, y - 14, 30, 14);
    g.fillStyle(C.ink, 1);
    g.lineStyle(4, C.ink, 1);
    switch (item.effects[0].kind) {
      case 'towerDamage': // crossed arrowheads
        g.lineBetween(x - 16, y + 16, x + 14, y - 14);
        g.fillTriangle(x + 18, y - 18, x + 6, y - 14, x + 14, y - 6);
        g.lineBetween(x + 16, y + 16, x - 14, y - 14);
        g.fillTriangle(x - 18, y - 18, x - 6, y - 14, x - 14, y - 6);
        break;
      case 'startCoins': // a stack of coins
        for (let k = 0; k < 3; k++) {
          g.fillStyle(0xffe08a, 1);
          g.fillEllipse(x, y + 12 - k * 9, 34, 12);
          g.strokeEllipse(x, y + 12 - k * 9, 34, 12);
        }
        break;
      case 'heroHp': // a heart
        g.fillStyle(0xff5d6a, 1);
        g.fillCircle(x - 8, y - 4, 10);
        g.fillCircle(x + 8, y - 4, 10);
        g.fillTriangle(x - 18, y, x + 18, y, x, y + 20);
        break;
      case 'spellCd': // a four-point star
        g.fillStyle(0xfff6c8, 1);
        g.fillTriangle(x, y - 22, x - 6, y, x + 6, y);
        g.fillTriangle(x, y + 22, x - 6, y, x + 6, y);
        g.fillTriangle(x - 22, y, x, y - 6, x, y + 6);
        g.fillTriangle(x + 22, y, x, y - 6, x, y + 6);
        break;
      case 'rangers': // a shield
        g.fillStyle(0x6a8a4a, 1);
        g.fillRoundedRect(x - 15, y - 18, 30, 22, 4);
        g.fillTriangle(x - 15, y + 2, x + 15, y + 2, x, y + 20);
        g.lineStyle(3, C.ink, 1);
        g.lineBetween(x, y - 16, x, y + 16);
        break;
      case 'bounty': // a four-leaf charm
        g.fillStyle(0x3a9a4a, 1);
        for (const [dx, dy] of [[-8, -8], [8, -8], [-8, 8], [8, 8]]) g.fillCircle(x + dx, y + dy, 9);
        g.fillStyle(C.ink, 1);
        g.fillRect(x - 2, y + 8, 4, 14);
        break;
    }
    return g;
  }
}
