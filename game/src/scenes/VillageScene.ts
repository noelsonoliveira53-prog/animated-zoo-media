import Phaser from 'phaser';
import { BUILDINGS, SHOP_ORDER, VILLAGE_COLS, VILLAGE_ROWS, type BuildingId, type Cost } from '../data/buildings';
import { TILE } from './BootScene';
import { loadSave, writeSave, ensureVillage, type SaveData } from '../systems/save';
import {
  busyBuilders,
  builders,
  canAfford,
  capacity,
  collect,
  countOf,
  footprintFree,
  formatTime,
  maxCountOf,
  moveBuilding,
  nextLevel,
  pending,
  placeBuilding,
  tick,
  townHallLevel,
  upgradeBuilding,
  type Building,
  type VillageState,
} from '../systems/village';
import { sfx } from '../systems/audio';
import { Button } from '../ui/Button';
import { C, GAME_H, GAME_W, TEXT, textStyle } from '../ui/theme';

const GRID_W = VILLAGE_COLS * TILE;
const GRID_H = VILLAGE_ROWS * TILE;
const OX = Math.round((GAME_W - GRID_W) / 2);
const OY = 92;

interface BView {
  img: Phaser.GameObjects.Image;
  badge: Phaser.GameObjects.Text;
  bar: Phaser.GameObjects.Graphics;
  bubble: Phaser.GameObjects.Image | null;
  shownLevel: number;
}

type Mode = { kind: 'idle' } | { kind: 'place'; type: BuildingId } | { kind: 'move'; uid: number };

// The home sanctuary: build, upgrade and harvest. Campaign victories send resources here.
export class VillageScene extends Phaser.Scene {
  private save!: SaveData;
  private v!: VillageState;
  private views = new Map<number, BView>();
  private panel: Phaser.GameObjects.Container | null = null;
  private selected: number | null = null;
  private mode: Mode = { kind: 'idle' };
  private ghost: Phaser.GameObjects.Image | null = null;
  private ghostCell = { col: 0, row: 0 };
  private coinText!: Phaser.GameObjects.Text;
  private sapText!: Phaser.GameObjects.Text;
  private builderText!: Phaser.GameObjects.Text;
  private hudBars!: Phaser.GameObjects.Graphics;
  private modeBar: Phaser.GameObjects.Container | null = null;
  private lastSave = 0;

  constructor() {
    super('Village');
  }

  create(): void {
    this.save = loadSave();
    this.v = ensureVillage(this.save);
    this.views.clear();
    this.panel = null;
    this.selected = null;
    this.mode = { kind: 'idle' };
    this.ghost = null;
    this.modeBar = null;
    tick(this.v, Date.now());
    this.persist();

    this.drawGround();
    for (const b of this.v.buildings) this.addView(b);
    this.buildHud();

    this.input.on('pointerdown', (p: Phaser.Input.Pointer) => this.onGroundTap(p));
    this.input.on('pointermove', (p: Phaser.Input.Pointer) => this.updateGhost(p));
    this.time.addEvent({ delay: 250, loop: true, callback: () => this.refresh() });
    this.cameras.main.fadeIn(250, 16, 38, 27);
  }

  private persist(): void {
    this.save.village = this.v;
    writeSave(this.save);
    this.lastSave = Date.now();
  }

  // ---------- drawing ----------

  private drawGround(): void {
    const g = this.add.graphics().setDepth(-10);
    g.fillStyle(0x4d8a38, 1);
    g.fillRect(-20, -20, GAME_W + 40, GAME_H + 40);
    g.fillStyle(0x5f9e45, 1);
    g.fillRoundedRect(OX - 14, OY - 14, GRID_W + 28, GRID_H + 28, 24);
    for (let c = 0; c < VILLAGE_COLS; c++) {
      for (let r = 0; r < VILLAGE_ROWS; r++) {
        g.fillStyle((c + r) % 2 ? 0x67a84c : 0x6cae50, 1);
        g.fillRect(OX + c * TILE, OY + r * TILE, TILE, TILE);
      }
    }
    // a brook along the bottom edge and some flowers outside the grid
    const rnd = new Phaser.Math.RandomDataGenerator(['village']);
    for (let i = 0; i < 40; i++) {
      const x = rnd.pick([rnd.between(10, OX - 24), rnd.between(OX + GRID_W + 24, GAME_W - 10)]);
      const y = rnd.between(100, GAME_H - 10);
      g.fillStyle(rnd.pick([0x3f7f34, 0x2f6a30]), 1);
      g.fillCircle(x, y, rnd.between(10, 18));
    }
  }

  private cellToXY(col: number, row: number): { x: number; y: number } {
    return { x: OX + col * TILE, y: OY + row * TILE };
  }

  private addView(b: Building): void {
    const def = BUILDINGS[b.type];
    const { x, y } = this.cellToXY(b.col, b.row);
    const lvlTex = Math.max(1, b.level);
    const img = this.add.image(x, y, `bld_${b.type}_${lvlTex}`).setOrigin(0, 0).setDepth(b.row + def.size);
    img.setInteractive({ useHandCursor: true });
    img.on('pointerdown', (_p: Phaser.Input.Pointer, _x: number, _y: number, ev: Phaser.Types.Input.EventData) => {
      if (this.mode.kind !== 'idle') return; // let the ground handler place/move
      ev.stopPropagation();
      sfx.unlock();
      this.tapBuilding(b.uid);
    });
    const badge = this.add.text(x + 6, y + 4, '', textStyle(13, TEXT.gold)).setDepth(500);
    const bar = this.add.graphics().setDepth(501);
    this.views.set(b.uid, { img, badge, bar, bubble: null, shownLevel: b.level });
  }

  private syncView(b: Building, now: number): void {
    const v = this.views.get(b.uid);
    if (!v) return;
    const def = BUILDINGS[b.type];
    const { x, y } = this.cellToXY(b.col, b.row);
    const S = def.size * TILE;
    v.img.setPosition(x, y).setDepth(b.row + def.size);
    if (v.shownLevel !== b.level) {
      v.shownLevel = b.level;
      v.img.setTexture(`bld_${b.type}_${Math.max(1, b.level)}`);
      this.tweens.add({ targets: v.img, scaleY: 1.12, duration: 120, yoyo: true });
    }
    const building = b.upgradeEnds !== null;
    v.img.setAlpha(b.level === 0 ? 0.55 : 1);
    v.badge.setPosition(x + 6, y + 4).setText(b.type === 'wall' ? '' : `${Math.max(1, b.level)}`);
    v.bar.clear();
    if (building) {
      const total = (nextLevel(b)?.time ?? 1) * 1000;
      const left = Math.max(0, b.upgradeEnds! - now);
      const frac = 1 - left / total;
      v.bar.fillStyle(C.ink, 0.85);
      v.bar.fillRoundedRect(x + 6, y + S - 20, S - 12, 14, 5);
      v.bar.fillStyle(0xffb84a, 1);
      v.bar.fillRoundedRect(x + 8, y + S - 18, (S - 16) * frac, 10, 4);
      v.badge.setText(`⏳ ${formatTime(left / 1000)}`);
    }
    // ready-to-collect bubble
    const prod = b.level > 0 ? def.levels[b.level - 1].produces : undefined;
    const ready = prod && !building && pending(b, now) >= prod.capacity * 0.05;
    if (ready && !v.bubble) {
      v.bubble = this.add.image(x + S / 2, y - 6, prod.resource === 'coins' ? 'icon_coin' : 'icon_sap').setDepth(600);
      this.tweens.add({ targets: v.bubble, y: y - 14, yoyo: true, repeat: -1, duration: 500, ease: 'Sine.easeInOut' });
    } else if (!ready && v.bubble) {
      v.bubble.destroy();
      v.bubble = null;
    }
    v.bubble?.setX(x + S / 2);
  }

  // ---------- HUD ----------

  private buildHud(): void {
    const g = this.add.graphics().setDepth(900);
    g.fillStyle(C.ink, 0.8);
    g.fillRoundedRect(190, 10, 720, 62, 18);
    this.hudBars = this.add.graphics().setDepth(901);
    this.add.image(222, 41, 'icon_coin').setDepth(902);
    this.coinText = this.add.text(244, 30, '', textStyle(20, TEXT.gold)).setDepth(902);
    this.add.image(482, 41, 'icon_sap').setDepth(902);
    this.sapText = this.add.text(504, 30, '', textStyle(20, '#c8ff8a')).setDepth(902);
    this.add.image(742, 41, 'icon_hammer').setDepth(902);
    this.builderText = this.add.text(764, 30, '', textStyle(20)).setDepth(902);
    this.add.text(GAME_W / 2, 84, '', textStyle(14)).setOrigin(0.5).setDepth(902).setName('thLabel');

    new Button(this, 90, 40, 'Menu', { width: 140, height: 50, fontSize: 20, color: C.sky, onClick: () => this.leave('Menu') }).setDepth(902);
    new Button(this, GAME_W - 110, 40, 'Campaign', { width: 180, height: 50, fontSize: 20, color: 0xff9f43, onClick: () => this.leave('WorldMap') }).setDepth(902);
    new Button(this, GAME_W - 100, GAME_H - 44, 'Build', { width: 160, height: 60, fontSize: 26, color: C.leaf, onClick: () => this.openShop() }).setDepth(902);
    this.refresh();
  }

  private leave(scene: string): void {
    this.persist();
    this.scene.start(scene);
  }

  private refresh(): void {
    const now = Date.now();
    const done = tick(this.v, now);
    for (const b of done) {
      const { x, y } = this.cellToXY(b.col, b.row);
      this.floatText(x + (BUILDINGS[b.type].size * TILE) / 2, y, `${BUILDINGS[b.type].name} level ${b.level}!`, TEXT.gold);
      sfx.victory();
    }
    if (done.length) this.persist();
    for (const b of this.v.buildings) this.syncView(b, now);
    const cap = capacity(this.v);
    this.coinText.setText(`${Math.floor(this.v.coins)} / ${cap}`);
    this.sapText.setText(`${Math.floor(this.v.glowsap)} / ${cap}`);
    this.builderText.setText(`${builders(this.v) - busyBuilders(this.v, now)}/${builders(this.v)} free`);
    const bars = this.hudBars;
    bars.clear();
    for (const [x, val, col] of [
      [244, this.v.coins, C.gold],
      [504, this.v.glowsap, 0x9be86a],
    ] as const) {
      bars.fillStyle(0x000000, 0.5);
      bars.fillRoundedRect(x, 56, 200, 7, 3);
      bars.fillStyle(col, 1);
      bars.fillRoundedRect(x, 56, 200 * Math.min(1, val / Math.max(1, cap)), 7, 3);
    }
    (this.children.getByName('thLabel') as Phaser.GameObjects.Text).setText(`Grove Hall level ${townHallLevel(this.v)}`);
    if (this.selected !== null && this.panel && this.panel.getData('dynamic')) this.openPanel(this.selected, false);
    if (now - this.lastSave > 5000) this.persist();
  }

  // ---------- interaction ----------

  private tapBuilding(uid: number): void {
    const b = this.v.buildings.find((x) => x.uid === uid);
    if (!b) return;
    const got = collect(this.v, uid, Date.now());
    if (got > 0) {
      const prod = BUILDINGS[b.type].levels[b.level - 1].produces!;
      const { x, y } = this.cellToXY(b.col, b.row);
      this.floatText(x + (BUILDINGS[b.type].size * TILE) / 2, y, `+${got}`, prod.resource === 'coins' ? TEXT.gold : '#c8ff8a');
      sfx.coin();
      this.persist();
    } else {
      sfx.click();
    }
    this.openPanel(uid, true);
  }

  private closePanel(): void {
    this.panel?.destroy();
    this.panel = null;
    this.selected = null;
  }

  private costText(cost: Cost): string {
    const parts: string[] = [];
    if (cost.coins) parts.push(`${cost.coins} coins`);
    if (cost.glowsap) parts.push(`${cost.glowsap} glowsap`);
    return parts.length ? parts.join(' + ') : 'free';
  }

  private openPanel(uid: number, animate: boolean): void {
    const b = this.v.buildings.find((x) => x.uid === uid);
    if (!b) return;
    this.panel?.destroy();
    this.selected = uid;
    const def = BUILDINGS[b.type];
    const now = Date.now();
    const W = 640;
    const H = 150;
    const c = this.add.container(GAME_W / 2 - 60, GAME_H - H / 2 - 12).setDepth(1000);
    const bg = this.add.graphics();
    bg.fillStyle(C.ink, 0.95);
    bg.fillRoundedRect(-W / 2, -H / 2, W, H, 20);
    c.add(bg);
    const block = this.add.zone(0, 0, W, H).setInteractive();
    block.on('pointerdown', (_p: Phaser.Input.Pointer, _x: number, _y: number, ev: Phaser.Types.Input.EventData) => ev.stopPropagation());
    c.add(block);
    c.add(this.add.image(-W / 2 + 70, 0, `bld_${b.type}_${Math.max(1, b.level)}`).setScale(Math.min(1, 110 / (def.size * TILE))));
    c.add(this.add.text(-W / 2 + 140, -H / 2 + 14, `${def.name}  •  Level ${Math.max(0, b.level)}`, textStyle(20, TEXT.gold)));
    const cur = b.level > 0 ? def.levels[b.level - 1] : undefined;
    const lines: string[] = [];
    if (cur?.produces) lines.push(`Makes ${cur.produces.perHour} ${cur.produces.resource}/hour (holds ${cur.produces.capacity}). Waiting: ${pending(b, now)}`);
    if (cur?.storage) lines.push(`Stores +${cur.storage} of each resource`);
    if (b.type === 'workshop' && b.level > 0) lines.push(`Battle bonus: towers deal +${b.level * 5}% damage`);
    if (b.type === 'townhall' && b.level > 1) lines.push(`Battle bonus: +${(b.level - 1) * 40} starting coins`);
    if (b.type === 'townhall' && b.level === 1) lines.push('Upgrade for +40 starting coins in every battle.');
    if (b.type === 'barracks' && b.level > 0) lines.push(`Battle bonus: Grove Call Rangers +${b.level * 25}% health and damage`);
    if (b.type === 'builderhut') lines.push('Each Builder Burrow works on one project at a time.');
    if (!lines.length) lines.push(def.blurb);
    c.add(this.add.text(-W / 2 + 140, -H / 2 + 44, lines.join('\n'), { ...textStyle(14, TEXT.cream, false), wordWrap: { width: 300 } }));

    const next = nextLevel(b);
    let dynamic = false;
    if (b.upgradeEnds !== null) {
      dynamic = true;
      c.add(this.add.text(W / 2 - 150, -10, `Building…\n${formatTime((b.upgradeEnds - now) / 1000)} left`, { ...textStyle(18), align: 'center' }).setOrigin(0.5));
    } else if (next) {
      const thOk = townHallLevel(this.v) >= next.th;
      c.add(
        this.add
          .text(W / 2 - 150, -H / 2 + 22, thOk ? `Upgrade: ${this.costText(next.cost)}\n${formatTime(next.time)}` : `Needs Grove Hall ${next.th}`, {
            ...textStyle(14, thOk ? TEXT.cream : TEXT.heart, false),
            align: 'center',
          })
          .setOrigin(0.5, 0),
      );
      const btn = new Button(this, W / 2 - 150, 36, 'Upgrade', {
        width: 160,
        height: 50,
        fontSize: 20,
        color: 0xff9f43,
        onClick: () => {
          const r = upgradeBuilding(this.v, uid, Date.now());
          if (!r.ok) this.toast(r.reason);
          else {
            sfx.build();
            this.persist();
          }
          this.openPanel(uid, false);
        },
      });
      btn.setEnabled(thOk && canAfford(this.v, next.cost));
      c.add(btn);
    } else {
      c.add(this.add.text(W / 2 - 150, -10, 'Max level', textStyle(20, TEXT.gold)).setOrigin(0.5));
    }
    const moveBtn = new Button(this, W / 2 + 70, -30, 'Move', {
      width: 110,
      height: 46,
      fontSize: 18,
      color: C.sky,
      onClick: () => this.startMode({ kind: 'move', uid }),
    });
    const closeBtn = new Button(this, W / 2 + 70, 30, 'Close', { width: 110, height: 46, fontSize: 18, color: 0x8a9a8a, onClick: () => this.closePanel() });
    c.add([moveBtn, closeBtn]);
    c.setData('dynamic', dynamic);
    if (animate) {
      c.setY(c.y + 40).setAlpha(0);
      this.tweens.add({ targets: c, y: c.y - 40, alpha: 1, duration: 180, ease: 'Cubic.easeOut' });
    }
    this.panel = c;
  }

  private openShop(): void {
    this.closePanel();
    this.cancelMode();
    const W = 1100;
    const H = 300;
    const c = this.add.container(GAME_W / 2, GAME_H / 2 + 60).setDepth(1100);
    const bg = this.add.graphics();
    bg.fillStyle(C.ink, 0.96);
    bg.fillRoundedRect(-W / 2, -H / 2, W, H, 24);
    c.add(bg);
    const block = this.add.zone(0, 0, W, H).setInteractive();
    block.on('pointerdown', (_p: Phaser.Input.Pointer, _x: number, _y: number, ev: Phaser.Types.Input.EventData) => ev.stopPropagation());
    c.add(block);
    c.add(this.add.text(0, -H / 2 + 24, 'Build something new', textStyle(24, TEXT.gold)).setOrigin(0.5));
    const cardW = 146;
    SHOP_ORDER.forEach((id, i) => {
      const def = BUILDINGS[id];
      const x = -W / 2 + 30 + cardW / 2 + i * (cardW + 6);
      const count = countOf(this.v, id);
      const max = maxCountOf(this.v, id);
      const lvl = def.levels[0];
      const available = count < max && townHallLevel(this.v) >= lvl.th;
      const affordable = canAfford(this.v, lvl.cost);
      const card = this.add.container(x, 20);
      const cg = this.add.graphics();
      cg.fillStyle(available ? C.panelLight : 0x333b35, 1);
      cg.fillRoundedRect(-cardW / 2, -110, cardW, 220, 14);
      cg.lineStyle(3, available && affordable ? C.gold : 0x666666, 1);
      cg.strokeRoundedRect(-cardW / 2, -110, cardW, 220, 14);
      card.add(cg);
      const icon = this.add.image(0, -50, `bld_${id}_1`);
      icon.setScale(Math.min(1, 90 / (def.size * TILE)));
      if (!available) icon.setTint(0x777777);
      card.add(icon);
      card.add(this.add.text(0, 8, def.name, { ...textStyle(15), align: 'center', wordWrap: { width: cardW - 10 } }).setOrigin(0.5, 0));
      card.add(this.add.text(0, 52, this.costText(lvl.cost), { ...textStyle(13, affordable ? TEXT.gold : TEXT.heart, false), align: 'center', wordWrap: { width: cardW - 10 } }).setOrigin(0.5, 0));
      card.add(this.add.text(0, 88, max > 0 ? `${count}/${max}` : `Grove Hall ${lvl.th}`, textStyle(14, TEXT.dim)).setOrigin(0.5, 0));
      card.setSize(cardW, 220).setInteractive({ useHandCursor: available });
      card.on('pointerdown', (_p: Phaser.Input.Pointer, _x: number, _y: number, ev: Phaser.Types.Input.EventData) => {
        ev.stopPropagation();
        sfx.unlock();
        if (!available) {
          this.toast(count >= max ? 'Upgrade the Grove Hall to build more' : `Needs Grove Hall level ${lvl.th}`);
          return;
        }
        if (!affordable) {
          this.toast('Not enough resources');
          return;
        }
        sfx.click();
        c.destroy();
        this.panel = null;
        this.startMode({ kind: 'place', type: id });
      });
      c.add(card);
    });
    const close = new Button(this, W / 2 - 60, -H / 2 + 26, 'X', { width: 50, height: 44, fontSize: 20, color: C.danger, onClick: () => c.destroy() });
    c.add(close);
    this.panel = c;
  }

  private startMode(mode: Mode): void {
    this.closePanel();
    this.cancelMode();
    this.mode = mode;
    const type = mode.kind === 'place' ? mode.type : mode.kind === 'move' ? this.v.buildings.find((b) => b.uid === mode.uid)!.type : null;
    if (!type) return;
    this.ghost = this.add.image(0, 0, `bld_${type}_1`).setOrigin(0, 0).setAlpha(0.7).setDepth(800);
    this.ghost.setVisible(false);
    const bar = this.add.container(GAME_W / 2, GAME_H - 40).setDepth(1000);
    const bg = this.add.graphics();
    bg.fillStyle(C.ink, 0.9);
    bg.fillRoundedRect(-300, -30, 600, 60, 18);
    bar.add(bg);
    bar.add(this.add.text(-120, 0, mode.kind === 'place' ? `Tap a spot for the ${BUILDINGS[type].name}` : 'Tap the new spot', textStyle(18)).setOrigin(0.5));
    bar.add(new Button(this, 220, 0, 'Cancel', { width: 120, height: 44, fontSize: 18, color: C.danger, onClick: () => this.cancelMode() }));
    this.modeBar = bar;
  }

  private cancelMode(): void {
    this.mode = { kind: 'idle' };
    this.ghost?.destroy();
    this.ghost = null;
    this.modeBar?.destroy();
    this.modeBar = null;
  }

  private cellAt(p: Phaser.Input.Pointer, size: number): { col: number; row: number } {
    // Centre the footprint on the pointer.
    const col = Math.round((p.worldX - OX) / TILE - size / 2);
    const row = Math.round((p.worldY - OY) / TILE - size / 2);
    return { col, row };
  }

  private updateGhost(p: Phaser.Input.Pointer): void {
    if (this.mode.kind === 'idle' || !this.ghost) return;
    const type = this.mode.kind === 'place' ? this.mode.type : this.v.buildings.find((b) => b.uid === (this.mode as { uid: number }).uid)!.type;
    const size = BUILDINGS[type].size;
    const cell = this.cellAt(p, size);
    this.ghostCell = cell;
    const { x, y } = this.cellToXY(cell.col, cell.row);
    const ignore = this.mode.kind === 'move' ? this.mode.uid : -1;
    const ok = footprintFree(this.v, type, cell.col, cell.row, ignore);
    this.ghost.setVisible(true).setPosition(x, y).setTint(ok ? 0xaaffaa : 0xff8888);
  }

  private onGroundTap(p: Phaser.Input.Pointer): void {
    if (this.mode.kind === 'idle') {
      this.closePanel();
      return;
    }
    this.updateGhost(p);
    const { col, row } = this.ghostCell;
    if (this.mode.kind === 'place') {
      const r = placeBuilding(this.v, this.mode.type, col, row, Date.now());
      if (!r.ok) {
        this.toast(r.reason);
        return;
      }
      this.addView(r.building);
      sfx.build();
      this.particlesAt(r.building);
      this.cancelMode();
      this.persist();
    } else {
      if (!moveBuilding(this.v, this.mode.uid, col, row)) {
        this.toast('Something is in the way');
        return;
      }
      sfx.build();
      this.cancelMode();
      this.persist();
    }
    this.refresh();
  }

  private particlesAt(b: Building): void {
    const { x, y } = this.cellToXY(b.col, b.row);
    const s = (BUILDINGS[b.type].size * TILE) / 2;
    const em = this.add.particles(0, 0, 'dot', { speed: { min: 40, max: 160 }, scale: { start: 0.5, end: 0 }, lifespan: 500, tint: 0xd9c39a, emitting: false });
    em.setDepth(700);
    em.explode(18, x + s, y + s);
    this.time.delayedCall(800, () => em.destroy());
  }

  private toast(msg: string): void {
    this.children.getByName('toast')?.destroy();
    const t = this.add.text(GAME_W / 2, 130, msg, textStyle(20, TEXT.heart)).setOrigin(0.5).setDepth(2000).setName('toast');
    this.tweens.add({ targets: t, alpha: 0, delay: 1400, duration: 400, onComplete: () => t.destroy() });
  }

  private floatText(x: number, y: number, text: string, color: string): void {
    const t = this.add.text(x, y, text, textStyle(18, color)).setOrigin(0.5).setDepth(1500);
    this.tweens.add({ targets: t, y: y - 40, alpha: 0, duration: 1100, ease: 'Cubic.easeOut', onComplete: () => t.destroy() });
  }
}
