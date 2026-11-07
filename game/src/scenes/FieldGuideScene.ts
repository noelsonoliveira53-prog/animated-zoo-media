import Phaser from 'phaser';
import { music } from '../systems/music';
import { themeById } from '../data/musicThemes';
import { ENEMIES } from '../data/enemies';
import { TOWERS, TOWER_ORDER } from '../data/towers';
import { HEROES, HERO_ORDER } from '../data/heroes';
import { SPELLS, SPELL_ORDER } from '../data/spells';
import { spellFacts } from '../systems/spellInfo';
import { bossPhaseLines } from '../systems/guideInfo';
import { loadSave } from '../systems/save';
import { sfx } from '../systems/audio';
import { pf } from '../ui/touch';
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
  /** Extra compact lines under the stats (boss phases). */
  extra?: string[];
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
        if (e.gust) tags.push(`Gusts: every ${e.gust.interval}s blows free walkers ${e.gust.distance}px ahead`);
        if (e.shift) tags.push(`Shifts every ${e.shift.interval}s: armor ${Math.round(e.armor * 100)}% ↔ magic resist ${Math.round(e.shift.magicResist * 100)}%`);
        if (e.revive) tags.push(`Raises a fallen ally every ${e.revive.interval}s at ${Math.round(e.revive.hpFrac * 100)}% health`);
        if (e.thorns) tags.push(`Thorns: melee attackers take ${Math.round(e.thorns * 100)}% of their damage back`);
        if (e.jam) tags.push(`Jams towers within ${e.jam.radius}px: ${Math.round(e.jam.slow * 100)}% slower fire`);
        if (e.charge) tags.push(`Bolts at ×${e.charge.speedMult} speed for ${e.charge.duration}s when hit (every ${e.charge.cooldown}s)`);
        if (e.harden) tags.push(`Hardens: +${Math.round(e.harden.perHit * 100)}% armor per hit, up to ${Math.round(e.harden.max * 100)}%`);
        if (e.dim) tags.push(`Gloom: towers within ${e.dim.radius}px lose ${Math.round(e.dim.cut * 100)}% range`);
        if (e.echo) tags.push(`Echoes: re-forms once at ${Math.round(e.echo.hpFrac * 100)}% health`);
        if (e.shock) tags.push(`Shocks every ${e.shock.interval}s: soldiers and heroes within ${e.shock.radius}px are stunned ${e.shock.duration}s`);
        if (e.fortify) tags.push(`Bark-song: allies within ${e.fortify.radius}px gain +${Math.round(e.fortify.bonus * 100)}% armor`);
        if (e.bolt) tags.push(`Calls lightning every ${e.bolt.interval}s: the nearest tower within ${e.bolt.range}px is stunned ${e.bolt.duration}s`);
        if (e.ink) tags.push(`When hit: an ink cloud (${e.ink.radius}px, ${e.ink.duration}s) hides grounded enemies from towers; every ${e.ink.cooldown}s at most`);
        if (e.molt) tags.push(`Molts below ${Math.round(e.molt.at * 100)}% health: armor drops to ${Math.round(e.molt.armor * 100)}%, speed ×${e.molt.speedMult}`);
        if (e.cleanse) tags.push(`Washes slows off itself and allies within ${e.cleanse.radius}px every ${e.cleanse.interval}s`);
        if (e.crust) tags.push(`Sunbaked shell: armor builds to +${Math.round(e.crust.max * 100)}% while unhit; any hit cracks it`);
        if (e.mirage) tags.push(`First hit: sheds ${e.mirage.count} decoy copies that are worth nothing and cost no lives`);
        if (e.pilfer) tags.push(`Thief: steals ${e.pilfer} coins (more on tougher levels) if it gets through`);
        if (e.bounty === 0 && e.livesCost === 0) tags.push('A decoy: worth nothing, harmless at the gate');
        if (e.ground) tags.push(`Draws ${Math.round(e.ground.share * 100)}% of the damage aimed at allies within ${e.ground.radius}px onto itself`);
        if (e.herd) tags.push(`Stampede: +${Math.round(e.herd.perAlly * 100)}% speed per nearby herd-mate (up to +${Math.round(e.herd.max * 100)}%)`);
        if (e.feed) tags.push(`Feeds on allies dying within ${e.feed.radius}px: +${Math.round(e.feed.growth * 100)}% max health and heals (up to ${e.feed.maxStacks} times)`);
        if (e.grow) tags.push(`Sprouts into a ${ENEMIES[e.grow.into]?.name ?? e.grow.into} after ${e.grow.after}s`);
        if (e.spawner) tags.push(`Drops a ${ENEMIES[e.spawner.enemy]?.name ?? e.spawner.enemy} every ${e.spawner.interval}s`);
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
          extra: e.phases?.length ? ['Phases', ...bossPhaseLines(e)] : undefined,
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
      c.add(this.add.text(x, 210, 'Not met yet. Face it in battle to fill in this page.', { ...textStyle(18, '#5a4a32', false), wordWrap: { width: 470 } }).setStroke('#e8dcb8', 0));
      return;
    }
    const img = this.add.image(x + 60, 262, e.texture);
    img.setScale(Math.min(2.2, 130 / Math.max(img.width, img.height)));
    this.tweens.add({ targets: img, y: 254, yoyo: true, repeat: -1, duration: 900, ease: 'Sine.easeInOut' });
    c.add(img);
    c.add(this.add.text(x, 130, e.name, { ...textStyle(30, '#3a2a1a'), wordWrap: { width: 470 } }).setStroke('#e8dcb8', 0));
    c.add(this.add.text(x + 150, 190, e.blurb, { ...textStyle(17, '#4a3a2a', false), wordWrap: { width: 300 } }).setStroke('#e8dcb8', 0));
    const body = this.add.text(x, 350, e.lines.join(e.extra ? '\n' : '\n\n'), { ...textStyle(17, '#3a2a1a', false), wordWrap: { width: 470 }, lineSpacing: 4 }).setStroke('#e8dcb8', 0);
    c.add(body);
    if (e.extra) {
      const y = body.y + body.height + 12;
      c.add(this.add.text(x, y, e.extra[0], textStyle(17, '#6a3a1a')).setStroke('#e8dcb8', 0));
      c.add(this.add.text(x, y + 26, e.extra.slice(1).join('\n'), { ...textStyle(pf(15), '#3a2a1a', false), wordWrap: { width: 470 }, lineSpacing: 2 }).setStroke('#e8dcb8', 0).setName('bossPhases'));
    }
  }
}
