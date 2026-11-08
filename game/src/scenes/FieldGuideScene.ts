import Phaser from 'phaser';
import { music } from '../systems/music';
import { themeById } from '../data/musicThemes';
import { ENEMIES } from '../data/enemies';
import { TOWERS, TOWER_ORDER } from '../data/towers';
import { HEROES, HERO_ORDER } from '../data/heroes';
import { SPELLS, SPELL_ORDER } from '../data/spells';
import { spellFacts } from '../systems/spellInfo';
import { CAMP_BUILDINGS, TROOPS, TROOP_ORDER } from '../data/raid';
import { bossPhaseLines } from '../systems/guideInfo';
import { loadSave } from '../systems/save';
import { sfx } from '../systems/audio';
import { fitWidth, pf } from '../ui/touch';
import { Button } from '../ui/Button';
import { clampPage, pageCount, pageItems } from '../ui/paging';
import { C, GAME_H, GAME_W, TEXT, textStyle } from '../ui/theme';

type Tab = 'enemies' | 'towers' | 'heroes' | 'spells' | 'raids';

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

    this.add.text(400, 44, "Keeper's Field Guide", textStyle(32, TEXT.gold)).setOrigin(0.5);
    new Button(this, 90, 44, 'Back', { width: 140, height: 50, fontSize: 20, color: C.sky, onClick: () => this.scene.start('Menu') });
    (['enemies', 'towers', 'heroes', 'spells', 'raids'] as Tab[]).forEach((t, i) => {
      this.tabButtons[t] = new Button(this, GAME_W - 568 + i * 124, 44, t[0].toUpperCase() + t.slice(1), {
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
        if (e.keg) tags.push(`Powder keg: on death, deals ${e.keg.damage} to soldiers and heroes within ${e.keg.radius}px`);
        if (e.ranged) tags.push(`Gunner: shoots soldiers and heroes within ${e.ranged.range}px for ${e.ranged.damage} every ${e.ranged.interval}s`);
        if (e.anchor) tags.push(`Drops anchor every ${e.anchor.interval}s: stops for ${e.anchor.duration}s with +${Math.round(e.anchor.armor * 100)}% armor`);
        if (e.snatch) tags.push(`Snatches the nearest soldier within ${e.snatch.radius}px every ${e.snatch.cooldown}s (it has to respawn)`);
        if (e.wax) tags.push(`Wax coat: +${Math.round(e.wax.armor * 100)}% armor until magic damage worth ${Math.round(e.wax.melt * 100)}% of its health melts it off`);
        if (e.venom) tags.push(`Venomous bite: soldiers it hits lose ${e.venom.dps} health a second for ${e.venom.duration}s`);
        if (e.link) tags.push(`Linked: every hit is shared equally with each linked ally within ${e.link.radius}px`);
        if (e.wool) tags.push(`Thick wool: each hit loses ${e.wool} damage (at most 3/4 of it), so big hits work best`);
        if (e.drench) tags.push(`Drench: it and allies within ${e.drench.radius}px take ${Math.round(e.drench.cut * 100)}% less damage from your spells`);
        if (e.bubble) tags.push(`Bubbler: every ${e.bubble.interval}s wraps up to ${e.bubble.count} nearby allies in a bubble that blocks the next hit`);
        if (e.surge) tags.push(`Surge: every ${e.surge.interval}s sweeps itself and nearby allies ${e.surge.distance}px down the road`);
        if (e.ambush) tags.push(`Ambusher: tunnels in and pops up ${Math.round(e.ambush * 100)}% of the way down the road`);
        if (e.curl) tags.push(`Curls up when hit: +${Math.round(e.curl.bonus * 100)}% armor and magic resist, at ${Math.round(e.curl.slow * 100)}% speed, for ${e.curl.duration}s (every ${e.curl.cooldown}s at most)`);
        if (e.shepherd) tags.push(`Herds stragglers: allies within ${e.shepherd.radius}px walk at least as fast as it does (${e.speed})`);
        if (e.tithe) tags.push(`Skims ${Math.round(e.tithe * 100)}% off every kill's bounty while it lives`);
        if (e.trample) tags.push(`Can't be held: tramples each soldier (and the hero) it passes for ${e.trample.damage}`);
        if (e.alarm) tags.push(`Raises the alarm when first hit: allies within ${e.alarm.radius}px run ${Math.round((e.alarm.speedMult - 1) * 100)}% faster for ${e.alarm.duration}s`);
        if (e.momentum) tags.push(`Gathers speed while unhit: +${Math.round(e.momentum.perSec * 100)}% per second (up to +${Math.round(e.momentum.max * 100)}%); any hit resets it`);
        if (e.blossom) tags.push(`When it falls, heals allies within ${e.blossom.radius}px by ${Math.round(e.blossom.heal * 100)}% of their health`);
        if (e.dive) tags.push(`Once, when knocked below ${Math.round(e.dive.at * 100)}% health, dives into the mud for ${e.dive.duration}s (untargetable, still moving) and heals ${Math.round(e.dive.heal * 100)}%`);
        if (e.lure) tags.push('Glowing lure: single-target towers in range must shoot it first, whatever their targeting mode');
        if (e.hex) tags.push(`Croaks a curse every ${e.hex.interval}s: the nearest tower within ${e.hex.range}px deals ${Math.round(e.hex.cut * 100)}% less damage for ${e.hex.duration}s`);
        if (e.glaze) tags.push(`Sticky paws: soldiers it hits attack at ${Math.round(e.glaze.slow * 100)}% speed for ${e.glaze.duration}s`);
        if (e.parry) tags.push(`Comb shield: turns aside ${e.parry.charges} whole single-target shots, regaining one every ${e.parry.regen}s (splash and spells always land)`);
        if (e.rile) tags.push(`Riled by slows: each one adds +${Math.round(e.rile.perSlow * 100)}% speed for good (up to +${Math.round(e.rile.max * 100)}%)`);
        if (e.grief) tags.push(`When it falls, allies within ${e.grief.radius}px gain +${Math.round(e.grief.armor * 100)}% armor for good`);
        if (e.ward) tags.push(`Lantern ward: allies within ${e.ward.radius}px take ${Math.round(e.ward.cut * 100)}% less damage of every type (not itself)`);
        if (e.phase) tags.push(`Fades to mist every ${e.phase.interval}s: takes no damage for ${e.phase.duration}s`);
        if (e.dodge) tags.push(`Sidesteps ${Math.round(e.dodge * 100)}% of single-target shots (splash, chains and spells always land)`);
        if (e.lifesteal) tags.push(`Bloodthirsty: heals ${Math.round(e.lifesteal * 100)}% of the melee damage it deals to soldiers and heroes`);
        if (e.drum) tags.push(`War-drum every ${e.drum.interval}s: allies within ${e.drum.radius}px run ×${e.drum.speedMult} for ${e.drum.duration}s`);
        if (e.adapt) tags.push(`Turning hide: each hit adds +${Math.round(e.adapt.step * 100)}% armor (physical) or magic resist (magic), up to +${Math.round(e.adapt.max * 100)}%, and wears the other down`);
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
    if (this.tab === 'raids') {
      // Your raiding troops first, then the Murkhorde camp buildings they face.
      const troops: Entry[] = TROOP_ORDER.map((id) => {
        const t = TROOPS[id];
        const traits = [
          t.flying ? 'Flies over walls; mortars cannot hit it' : '',
          t.prefers === 'defense' ? 'Goes for defenses first' : t.prefers === 'loot' ? 'Goes for loot first' : '',
          t.splash ? `Hits everything within ${t.splash}px` : '',
          t.wallMult ? `×${t.wallMult} damage to walls` : '',
          t.wader ? 'Sludge Pits do not slow it' : '',
          t.lootBonus ? `Buildings it destroys drop +${Math.round(t.lootBonus * 100)}% loot` : '',
          t.heals ? `Heals troops within ${t.heals.radius}px for ${t.heals.amount} every ${t.heals.interval}s` : '',
        ].filter(Boolean);
        return {
          key: `troop_${id}`,
          texture: `troop_${id}`,
          name: t.name,
          locked: false,
          blurb: t.blurb,
          lines: [
            `Health ${t.hp}   •   Damage ${t.damage} × ${t.rate}/s   •   Range ${t.range}`,
            `Speed ${t.speed}   •   ${t.cost} glowsap   •   ${t.space} space   •   Lodge ${t.lodge}`,
            traits.length ? traits.join('  •  ') : 'A plain, honest fighter',
          ],
        };
      });
      const camp: Entry[] = Object.values(CAMP_BUILDINGS).map((b) => {
        const facts = [
          b.hq ? 'The camp\'s heart: destroying it is worth a star' : '',
          b.defense ? `Shoots ${b.defense.damage} × ${b.defense.rate}/s up to ${b.defense.range}px${b.defense.splash ? `, splash ${b.defense.splash}px` : ''}${b.defense.hitsAir ? ', hits flyers' : ', ground only'}` : '',
          b.loot ? `Loot ${b.loot.coins} coins + ${b.loot.glowsap} glowsap (more in tougher camps)` : '',
          b.mend ? `Heals buildings within ${b.mend.range}px for ${b.mend.amount} every ${b.mend.interval}s` : '',
          b.mire ? `Ground troops within ${b.mire.radius}px move at ${Math.round(b.mire.factor * 100)}% speed` : '',
          b.wall ? 'Blocks ground troops; does not count toward destruction' : '',
        ].filter(Boolean);
        return {
          key: `camp_${b.id}`,
          texture: `camp_${b.id}`,
          name: b.name,
          locked: false,
          blurb: b.blurb ?? 'A Murkhorde camp building.',
          lines: [`Health ${b.hp}   •   ${b.size}×${b.size} tiles`, ...(facts.length ? facts : ['Just a building to knock down'])],
        };
      });
      return [...troops, ...camp];
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
      img.setScale(Math.min(tab === 'raids' ? 2 : 1, 64 / Math.max(img.width, img.height))); // small troop sprites may grow
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
    c.add(fitWidth(this.add.text(x, 130, e.name, textStyle(30, '#3a2a1a')).setStroke('#e8dcb8', 0), 470)); // long names shrink to one line
    c.add(this.add.text(x + 150, 190, e.blurb, { ...textStyle(17, '#4a3a2a', false), wordWrap: { width: 300 } }).setStroke('#e8dcb8', 0));
    const body = this.add.text(x, 350, e.lines.join(e.extra ? '\n' : '\n\n'), { ...textStyle(17, '#3a2a1a', false), wordWrap: { width: 470 }, lineSpacing: 4 }).setStroke('#e8dcb8', 0);
    c.add(body);
    if (e.extra) {
      const head = this.add.text(x, 0, e.extra[0], textStyle(17, '#6a3a1a')).setStroke('#e8dcb8', 0);
      const phases = this.add.text(x, 0, e.extra.slice(1).join('\n'), { ...textStyle(pf(15), '#3a2a1a', false), wordWrap: { width: 470 }, lineSpacing: 2 }).setStroke('#e8dcb8', 0).setName('bossPhases');
      c.add([head, phases]);
      // Long boss pages (many traits + phases) shrink as a block so the last phase stays inside the parchment.
      const room = GAME_H - 44 - body.y;
      const need = body.height + 12 + 26 + phases.height;
      const k = Math.min(1, room / need);
      body.setScale(k);
      head.setScale(k).setY(body.y + (body.height + 12) * k);
      phases.setScale(k).setY(head.y + 26 * k);
    }
  }
}
