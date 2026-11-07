import Phaser from 'phaser';
import { music } from '../systems/music';
import { themeById } from '../data/musicThemes';
import { ENEMIES } from '../data/enemies';
import { TOWERS, TOWER_ORDER } from '../data/towers';
import { HEROES, HERO_ORDER } from '../data/heroes';
import { SPELLS, SPELL_ORDER } from '../data/spells';
import { spellFacts } from '../systems/spellInfo';
import { loadSave } from '../systems/save';
import { sfx } from '../systems/audio';
import { Button } from '../ui/Button';
import { clampPage, pageCount, pageItems } from '../ui/paging';
import { C, GAME_H, GAME_W, TEXT, textStyle } from '../ui/theme';

type Tab = 'enemies' | 'towers' | 'heroes' | 'spells';

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
  private page = 0;
  private grid: Phaser.GameObjects.Container | null = null;
  private detail: Phaser.GameObjects.Container | null = null;
  private tabButtons: Record<string, Button> = {};

  constructor() {
    super('FieldGuide');
  }

  create(data: { tab?: Tab }): void {
    music.setMood('calm');
    music.setTheme(themeById('home'));
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

    this.add.text(470, 44, "Keeper's Field Guide", textStyle(34, TEXT.gold)).setOrigin(0.5);
    new Button(this, 90, 44, 'Back', { width: 140, height: 50, fontSize: 20, color: C.sky, onClick: () => this.scene.start('Menu') });
    (['enemies', 'towers', 'heroes', 'spells'] as Tab[]).forEach((t, i) => {
      this.tabButtons[t] = new Button(this, GAME_W - 444 + i * 124, 44, t[0].toUpperCase() + t.slice(1), {
        width: 116,
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
        if (e.veil) tags.push(`Veiled (towers see it within ${e.veil}px)`);
        if (e.glare) tags.push('Dazzles nearby towers when it dies');
        if (e.blink) tags.push(`Blinks ${e.blink.distance}px ahead every ${e.blink.interval}s`);
        if (e.windborne) tags.push('Windborne: immune to every slow');
        if (e.regen) tags.push(`Regrows ${Math.round(e.regen.perSec * 100)}% health/s after ${e.regen.delay}s unhit`);
        if (e.splashResist) tags.push(`Resists ${Math.round(e.splashResist * 100)}% of splash damage`);
        if (e.shieldAura) tags.push('Coral shields nearby allies');
        if (e.brittle) tags.push('Brittle: armor chips away with every hit');
        if (e.swoop) tags.push('Swoops: lands every few seconds');
        if (e.sporeBurst) tags.push('Spore burst: hastens allies on death');
        if (e.enrage) tags.push(`Enrages below ${Math.round(e.enrage.below * 100)}% health`);
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
    if (this.tab === 'spells') {
      return SPELL_ORDER.map((id, i) => {
        const sp = SPELLS[id];
        return { key: id, texture: `icon_${id}`, name: sp.name, locked: false, blurb: sp.text, lines: spellFacts(sp, i + 1) };
      });
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
          ...(h.bulwark ? [`Bulwark: holds ${h.bulwark.map((b) => `${b.holds} enemies from level ${b.level}`).join(', ')}`] : []),
          ...(h.toss ? [`${h.toss.name}: every ${h.toss.interval}s throws his shield at a flyer within ${h.toss.range}px`] : []),
          `${h.active.name} (${h.active.cooldown}s): ${h.active.text}`,
          `Training rank: ${loadSave().heroRanks[id] ?? 0} / 5`,
        ],
      };
    });
  }

  private show(tab: Tab, page = 0): void {
    this.tab = tab;
    for (const [t, b] of Object.entries(this.tabButtons)) b.setColor(t === tab ? 0xff9f43 : C.leaf);
    this.grid?.destroy();
    this.detail?.destroy();
    this.detail = null;
    const all = this.entries();
    const c = this.add.container(0, 0);
    this.grid = c;
    const cols = tab === 'towers' ? 3 : 6;
    // 6 × 5 enemy cards fit the page; more than that spills onto further pages.
    const perPage = tab === 'enemies' ? 30 : 99;
    const pages = pageCount(all.length, perPage);
    this.page = clampPage(page, all.length, perPage);
    const list = pageItems(all, this.page, perPage);
    const cell = tab === 'towers' ? 116 : 98;
    const x0 = 90;
    const y0 = 130;
    const seen = all.filter((e) => !e.locked).length;
    if (pages > 1) {
      const prev = new Button(this, 560, GAME_H - 58, '<', { width: 48, height: 40, fontSize: 20, color: C.sky, onClick: () => this.show(tab, (this.page + pages - 1) % pages) });
      const next = new Button(this, 670, GAME_H - 58, '>', { width: 48, height: 40, fontSize: 20, color: C.sky, onClick: () => this.show(tab, (this.page + 1) % pages) });
      c.add([prev, next, this.add.text(615, GAME_H - 58, `${this.page + 1}/${pages}`, textStyle(18, '#5a4a32', false)).setOrigin(0.5).setStroke('#e8dcb8', 0).setName('guidePage')]);
    }
    c.add(this.add.text(x0, GAME_H - 66, tab === 'enemies' ? `Discovered ${seen} / ${all.length}` : `${all.length} entries`, textStyle(16, '#5a4a32', false)).setStroke('#e8dcb8', 0));
    if (tab === 'spells') {
      c.add(this.add.text(x0, 260, 'How to cast: tap a spell icon at the bottom right of the battlefield (or press its number key), then tap a spot on the road. Each spell recharges on its own timer, so save them for the waves that would break through.', { ...textStyle(17, '#4a3a2a', false), wordWrap: { width: 520 }, lineSpacing: 4 }).setStroke('#e8dcb8', 0));
    }
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
