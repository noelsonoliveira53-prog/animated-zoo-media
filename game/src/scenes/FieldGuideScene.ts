import Phaser from 'phaser';
import { music } from '../systems/music';
import { ENEMIES } from '../data/enemies';
import { TOWERS, TOWER_ORDER } from '../data/towers';
import { HEROES, HERO_ORDER } from '../data/heroes';
import { loadSave } from '../systems/save';
import { sfx } from '../systems/audio';
import { Button } from '../ui/Button';
import { C, GAME_H, GAME_W, TEXT, textStyle } from '../ui/theme';

type Tab = 'enemies' | 'towers' | 'heroes';

interface Entry {
  key: string;
  texture: string;
  name: string;
  locked: boolean;
  lines: string[];
  blurb: string;
}

// The Keepers' Field Guide: everything you've met, with stats and tips.
export class FieldGuideScene extends Phaser.Scene {
  private tab: Tab = 'enemies';
  private grid: Phaser.GameObjects.Container | null = null;
  private detail: Phaser.GameObjects.Container | null = null;
  private tabButtons: Record<string, Button> = {};

  constructor() {
    super('FieldGuide');
  }

  create(data: { tab?: Tab }): void {
    music.setMood('calm');
    this.tab = data?.tab ?? 'enemies';
    const g = this.add.graphics();
    g.fillGradientStyle(0x22382a, 0x22382a, 0x10261b, 0x10261b, 1);
    g.fillRect(0, 0, GAME_W, GAME_H);
    // parchment page
    g.fillStyle(0xe8dcb8, 1);
    g.fillRoundedRect(40, 90, GAME_W - 80, GAME_H - 120, 24);
    g.lineStyle(4, 0x8a6a40, 1);
    g.strokeRoundedRect(40, 90, GAME_W - 80, GAME_H - 120, 24);
    g.lineStyle(2, 0xb59a6a, 1);
    g.lineBetween(GAME_W / 2 + 70, 120, GAME_W / 2 + 70, GAME_H - 60);

    this.add.text(500, 44, "Keeper's Field Guide", textStyle(34, TEXT.gold)).setOrigin(0.5);
    new Button(this, 90, 44, 'Back', { width: 140, height: 50, fontSize: 20, color: C.sky, onClick: () => this.scene.start('Menu') });
    (['enemies', 'towers', 'heroes'] as Tab[]).forEach((t, i) => {
      this.tabButtons[t] = new Button(this, GAME_W - 420 + i * 140, 44, t[0].toUpperCase() + t.slice(1), {
        width: 128,
        height: 46,
        fontSize: 18,
        color: C.leaf,
        onClick: () => this.show(t),
      });
    });
    this.show(this.tab);
  }

  private entries(): Entry[] {
    const save = loadSave();
    if (this.tab === 'enemies') {
      return Object.values(ENEMIES).map((e) => {
        const tags: string[] = [];
        if (e.flying) tags.push('Flying');
        if (e.boss) tags.push('Boss');
        if (e.heal) tags.push('Heals allies');
        if (e.shield) tags.push(`Shield ${e.shield}`);
        if (e.splitInto) tags.push(`Splits into ${e.splitInto.count}`);
        if (e.chill) tags.push('Freezes towers');
        if (e.burrow) tags.push('Burrows');
        if (e.spawner) tags.push('Spawns minions');
        return {
          key: e.id,
          texture: `enemy_${e.id}`,
          name: e.name,
          locked: !save.seenEnemies.includes(e.id),
          blurb: e.blurb,
          lines: [
            `Health ${e.hp}   •   Speed ${e.speed}`,
            `Armor ${Math.round(e.armor * 100)}%   •   Magic resist ${Math.round(e.magicResist * 100)}%`,
            `Costs ${e.livesCost} ${e.livesCost === 1 ? 'life' : 'lives'}   •   Bounty ${e.bounty}`,
            tags.length ? tags.join('  •  ') : 'No special tricks',
          ],
        };
      });
    }
    if (this.tab === 'towers') {
      const out: Entry[] = [];
      for (const id of TOWER_ORDER) {
        const d = TOWERS[id];
        const t0 = d.tiers[0];
        out.push({
          key: id,
          texture: `tower_${id}_2`,
          name: d.name,
          locked: false,
          blurb: d.blurb,
          lines: [
            `${d.damageType === 'magic' ? 'Magic' : 'Physical'} damage   •   ${d.hitsAir ? 'Hits flyers' : 'Ground only'}`,
            t0.soldiers ? `Squad of ${t0.soldiers.count} Wardens, ${t0.soldiers.hp} hp each` : `Damage ${t0.damage}   •   ${t0.fireRate}/s   •   Range ${t0.range}`,
            `Build ${t0.cost}   •   Upgrades ${d.tiers[1].cost} / ${d.tiers[2].cost}`,
          ],
        });
        for (const sp of d.specs) {
          out.push({
            key: `${id}:${sp.id}`,
            texture: `tower_${id}_${sp.id}`,
            name: sp.name,
            locked: false,
            blurb: sp.text,
            lines: [`Top-tier branch of the ${d.name}`, `Costs ${sp.stats.cost}`, sp.stats.soldiers ? `${sp.stats.soldiers.count} soldiers, ${sp.stats.soldiers.hp} hp` : `Damage ${sp.stats.damage}   •   Range ${sp.stats.range}`],
          });
        }
      }
      return out;
    }
    return HERO_ORDER.map((id) => {
      const h = HEROES[id];
      return {
        key: id,
        texture: `hero_${id}`,
        name: `${h.name} the ${h.title}`,
        locked: false,
        blurb: h.blurb,
        lines: [
          `Health ${h.hp}   •   ${h.melee ? 'Melee blocker' : 'Ranged'}${h.attack.hitsAir ? ', hits flyers' : ''}`,
          h.passive.text,
          `${h.active.name} (${h.active.cooldown}s): ${h.active.text}`,
          `Training rank: ${loadSave().heroRanks[id] ?? 0} / 5`,
        ],
      };
    });
  }

  private show(tab: Tab): void {
    this.tab = tab;
    for (const [t, b] of Object.entries(this.tabButtons)) b.setColor(t === tab ? 0xff9f43 : C.leaf);
    this.grid?.destroy();
    this.detail?.destroy();
    this.detail = null;
    const list = this.entries();
    const c = this.add.container(0, 0);
    this.grid = c;
    const cols = tab === 'towers' ? 3 : 6;
    const cell = tab === 'towers' ? 116 : 98;
    const x0 = 90;
    const y0 = 130;
    const seen = list.filter((e) => !e.locked).length;
    c.add(this.add.text(x0, GAME_H - 66, tab === 'enemies' ? `Discovered ${seen} / ${list.length}` : `${list.length} entries`, textStyle(16, '#5a4a32', false)).setStroke('#e8dcb8', 0));
    list.forEach((e, i) => {
      const x = x0 + (i % cols) * cell + cell / 2;
      const y = y0 + Math.floor(i / cols) * (tab === 'towers' ? 96 : cell) + cell / 2 - 10;
      const bg = this.add.graphics();
      bg.fillStyle(0xd4c49c, 1);
      bg.fillRoundedRect(x - cell / 2 + 5, y - 42, cell - 10, 84, 12);
      c.add(bg);
      const img = this.add.image(x, y, e.texture);
      img.setScale(Math.min(1, 64 / Math.max(img.width, img.height)));
      if (e.locked) img.setTintFill(0x5a4a32);
      c.add(img);
      if (e.locked) c.add(this.add.text(x, y, '?', textStyle(28, TEXT.cream)).setOrigin(0.5));
      const hit = this.add.zone(x, y, cell - 10, 84).setInteractive({ useHandCursor: true });
      hit.on('pointerdown', () => {
        sfx.unlock();
        sfx.click();
        this.showDetail(e);
      });
      c.add(hit);
    });
    const first = list.find((e) => !e.locked);
    if (first) this.showDetail(first);
  }

  private showDetail(e: Entry): void {
    this.detail?.destroy();
    const x = GAME_W / 2 + 110;
    const c = this.add.container(0, 0);
    this.detail = c;
    if (e.locked) {
      c.add(this.add.text(x, 150, '???', textStyle(34, '#5a4a32')).setStroke('#e8dcb8', 0));
      c.add(this.add.text(x, 210, 'Not met yet. Face it in battle to fill in this page.', { ...textStyle(18, '#5a4a32', false), wordWrap: { width: 500 } }).setStroke('#e8dcb8', 0));
      return;
    }
    const img = this.add.image(x + 60, 262, e.texture);
    img.setScale(Math.min(2.2, 130 / Math.max(img.width, img.height)));
    this.tweens.add({ targets: img, y: 254, yoyo: true, repeat: -1, duration: 900, ease: 'Sine.easeInOut' });
    c.add(img);
    c.add(this.add.text(x, 130, e.name, { ...textStyle(30, '#3a2a1a'), wordWrap: { width: 540 } }).setStroke('#e8dcb8', 0));
    c.add(this.add.text(x + 150, 190, e.blurb, { ...textStyle(17, '#4a3a2a', false), wordWrap: { width: 300 } }).setStroke('#e8dcb8', 0));
    c.add(this.add.text(x, 350, e.lines.join('\n\n'), { ...textStyle(17, '#3a2a1a', false), wordWrap: { width: 540 }, lineSpacing: 2 }).setStroke('#e8dcb8', 0));
  }
}
