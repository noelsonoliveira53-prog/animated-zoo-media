import { TROOPS } from '../data/raid';
import { APIARY_HP_PER_LEVEL, BUILDINGS, SHRINE_CD_PER_LEVEL, SWIFTBLOOM, VILLAGE_COLS, VILLAGE_ROWS, type BuildingId, type Cost } from '../data/buildings';

// Pure village rules. All time-dependent functions take `now` (ms) so they are testable.

export interface Building {
  uid: number;
  type: BuildingId;
  level: number; // current finished level (0 while the first construction is in progress)
  col: number;
  row: number;
  upgradeEnds: number | null; // ms timestamp when the current construction finishes
  lastCollect: number; // ms timestamp of the last harvest (producers)
}

export interface VillageState {
  coins: number;
  glowsap: number;
  buildings: Building[];
  nextUid: number;
  swiftblooms?: number; // free speed-up tokens (see SWIFTBLOOM)
}

export function newVillage(now: number): VillageState {
  const v: VillageState = { coins: 600, glowsap: 600, buildings: [], nextUid: 1 };
  const place = (type: BuildingId, col: number, row: number) =>
    v.buildings.push({ uid: v.nextUid++, type, level: 1, col, row, upgradeEnds: null, lastCollect: now });
  place('townhall', 10, 5);
  place('coinmine', 6, 3);
  place('sapwell', 15, 3);
  place('vault', 6, 8);
  place('builderhut', 15, 8);
  place('builderhut', 2, 10);
  return v;
}

export function townHallLevel(v: VillageState): number {
  return v.buildings.find((b) => b.type === 'townhall')?.level ?? 1;
}

export function capacity(v: VillageState): number {
  let cap = 0;
  for (const b of v.buildings) {
    if (b.level <= 0) continue;
    cap += BUILDINGS[b.type].levels[b.level - 1].storage ?? 0;
  }
  return cap;
}

export function builders(v: VillageState): number {
  return v.buildings.filter((b) => b.type === 'builderhut' && b.level > 0).length;
}

export function busyBuilders(v: VillageState, now: number): number {
  return v.buildings.filter((b) => b.upgradeEnds !== null && b.upgradeEnds > now).length;
}

export function canAfford(v: VillageState, cost: Cost): boolean {
  return v.coins >= (cost.coins ?? 0) && v.glowsap >= (cost.glowsap ?? 0);
}

function pay(v: VillageState, cost: Cost): void {
  v.coins -= cost.coins ?? 0;
  v.glowsap -= cost.glowsap ?? 0;
}

/** Add resources, clamped to storage capacity. Returns the amounts actually added. */
export function addResources(v: VillageState, coins: number, glowsap: number): { coins: number; glowsap: number } {
  const cap = capacity(v);
  const c = Math.max(0, Math.min(coins, cap - v.coins));
  const g = Math.max(0, Math.min(glowsap, cap - v.glowsap));
  v.coins += c;
  v.glowsap += g;
  return { coins: Math.floor(c), glowsap: Math.floor(g) };
}

/** Finish any constructions whose timer has run out. Returns buildings that just completed. */
export function tick(v: VillageState, now: number): Building[] {
  const done: Building[] = [];
  for (const b of v.buildings) {
    if (b.upgradeEnds !== null && b.upgradeEnds <= now) {
      // Production during construction is lost; restart the harvest clock at completion.
      b.level++;
      b.upgradeEnds = null;
      b.lastCollect = now;
      done.push(b);
    }
  }
  return done;
}

export function countOf(v: VillageState, type: BuildingId): number {
  return v.buildings.filter((b) => b.type === type).length;
}

export function maxCountOf(v: VillageState, type: BuildingId): number {
  const table = BUILDINGS[type].maxCount;
  return table[Math.min(table.length, townHallLevel(v)) - 1] ?? 0;
}

export function footprintFree(v: VillageState, type: BuildingId, col: number, row: number, ignoreUid = -1): boolean {
  const size = BUILDINGS[type].size;
  if (col < 0 || row < 0 || col + size > VILLAGE_COLS || row + size > VILLAGE_ROWS) return false;
  for (const b of v.buildings) {
    if (b.uid === ignoreUid) continue;
    const s = BUILDINGS[b.type].size;
    if (col < b.col + s && col + size > b.col && row < b.row + s && row + size > b.row) return false;
  }
  return true;
}

export type ActionResult = { ok: true; building: Building } | { ok: false; reason: string };

function needBuilder(v: VillageState, now: number, time: number): string | null {
  if (time <= 0) return null;
  return busyBuilders(v, now) >= builders(v) ? 'All builders are busy' : null;
}

export function placeBuilding(v: VillageState, type: BuildingId, col: number, row: number, now: number): ActionResult {
  const def = BUILDINGS[type];
  const lvl = def.levels[0];
  if (countOf(v, type) >= maxCountOf(v, type)) return { ok: false, reason: `Upgrade the Grove Hall to build more ${def.name}s` };
  if (townHallLevel(v) < lvl.th) return { ok: false, reason: `Needs Grove Hall level ${lvl.th}` };
  if (!footprintFree(v, type, col, row)) return { ok: false, reason: 'Something is in the way' };
  if (!canAfford(v, lvl.cost)) return { ok: false, reason: 'Not enough resources' };
  const busy = needBuilder(v, now, lvl.time);
  if (busy) return { ok: false, reason: busy };
  pay(v, lvl.cost);
  const b: Building = {
    uid: v.nextUid++,
    type,
    level: lvl.time > 0 ? 0 : 1,
    col,
    row,
    upgradeEnds: lvl.time > 0 ? now + lvl.time * 1000 : null,
    lastCollect: now,
  };
  v.buildings.push(b);
  return { ok: true, building: b };
}

export function nextLevel(b: Building) {
  return BUILDINGS[b.type].levels[b.level]; // levels[] is 0-based, so this is level+1
}

export function upgradeBuilding(v: VillageState, uid: number, now: number): ActionResult {
  const b = v.buildings.find((x) => x.uid === uid);
  if (!b) return { ok: false, reason: 'No such building' };
  if (b.upgradeEnds !== null) return { ok: false, reason: 'Already under construction' };
  const next = nextLevel(b);
  if (!next) return { ok: false, reason: 'Already at max level' };
  if (townHallLevel(v) < next.th) return { ok: false, reason: `Needs Grove Hall level ${next.th}` };
  if (!canAfford(v, next.cost)) return { ok: false, reason: 'Not enough resources' };
  const busy = needBuilder(v, now, next.time);
  if (busy) return { ok: false, reason: busy };
  collect(v, uid, now); // bank what it made so far
  pay(v, next.cost);
  if (next.time > 0) b.upgradeEnds = now + next.time * 1000;
  else b.level++;
  return { ok: true, building: b };
}

/** Earn one Swiftbloom unless already holding the maximum. Returns how many were granted (0 or 1). */
export function grantSwiftbloom(v: VillageState): number {
  const held = v.swiftblooms ?? 0;
  if (held >= SWIFTBLOOM.maxHeld) return 0;
  v.swiftblooms = held + 1;
  return 1;
}

/** Spend a Swiftbloom to cut up to SWIFTBLOOM.seconds off a construction. If that covers the rest, the next tick() finishes it. */
export function rushBuilding(v: VillageState, uid: number, now: number): ActionResult {
  const b = v.buildings.find((x) => x.uid === uid);
  if (!b) return { ok: false, reason: 'No such building' };
  if (b.upgradeEnds === null) return { ok: false, reason: 'Nothing to speed up' };
  if ((v.swiftblooms ?? 0) <= 0) return { ok: false, reason: 'No Swiftblooms (earn them with 3-star wins)' };
  v.swiftblooms = (v.swiftblooms ?? 0) - 1;
  b.upgradeEnds = Math.max(now, b.upgradeEnds - SWIFTBLOOM.seconds * 1000); // tick() completes it if now due
  return { ok: true, building: b };
}

/** Resources waiting in a producer right now. */
export function pending(b: Building, now: number): number {
  if (b.level <= 0 || b.upgradeEnds !== null) return 0;
  const prod = BUILDINGS[b.type].levels[b.level - 1].produces;
  if (!prod) return 0;
  const hours = Math.max(0, now - b.lastCollect) / 3600000;
  return Math.min(prod.capacity, Math.floor(prod.perHour * hours));
}

/** Harvest a producer into storage. Returns the amount banked. */
export function collect(v: VillageState, uid: number, now: number): number {
  const b = v.buildings.find((x) => x.uid === uid);
  if (!b) return 0;
  const prod = b.level > 0 ? BUILDINGS[b.type].levels[b.level - 1].produces : undefined;
  if (!prod) return 0;
  const amount = pending(b, now);
  if (amount <= 0) return 0;
  const added = prod.resource === 'coins' ? addResources(v, amount, 0).coins : addResources(v, 0, amount).glowsap;
  // Keep the unbanked remainder in the producer when storage is full.
  const leftover = amount - added;
  const perMs = prod.perHour / 3600000;
  b.lastCollect = now - (leftover > 0 ? leftover / perMs : 0);
  return added;
}

/** Harvest every producer at once. Returns the totals banked and which buildings gave how much. */
export function collectAll(v: VillageState, now: number): { coins: number; glowsap: number; per: { uid: number; amount: number }[] } {
  let coins = 0;
  let glowsap = 0;
  const per: { uid: number; amount: number }[] = [];
  for (const b of v.buildings) {
    const prod = b.level > 0 ? BUILDINGS[b.type].levels[b.level - 1].produces : undefined;
    if (!prod) continue;
    const got = collect(v, b.uid, now);
    if (got <= 0) continue;
    if (prod.resource === 'coins') coins += got;
    else glowsap += got;
    per.push({ uid: b.uid, amount: got });
  }
  return { coins, glowsap, per };
}

export function moveBuilding(v: VillageState, uid: number, col: number, row: number): boolean {
  const b = v.buildings.find((x) => x.uid === uid);
  if (!b || !footprintFree(v, b.type, col, row, uid)) return false;
  b.col = col;
  b.row = row;
  return true;
}

/** Village rewards for winning a campaign level. First clears pay the most. */
export function battleReward(levelIndex: number, starsBefore: number, starsNow: number): { coins: number; glowsap: number } {
  const baseC = 200 + levelIndex * 150;
  const baseG = 150 + levelIndex * 120;
  if (starsNow <= 0) return { coins: 0, glowsap: 0 };
  if (starsBefore === 0) return { coins: baseC, glowsap: baseG };
  const extraStars = Math.max(0, starsNow - starsBefore);
  const mult = 0.2 + extraStars * 0.25; // replays still pay a little, new stars pay more
  return { coins: Math.round(baseC * mult), glowsap: Math.round(baseG * mult) };
}

export function formatTime(seconds: number): string {
  const s = Math.max(0, Math.ceil(seconds));
  if (s < 60) return `${s}s`;
  if (s < 3600) return `${Math.floor(s / 60)}m ${s % 60 ? (s % 60) + 's' : ''}`.trim();
  return `${Math.floor(s / 3600)}h ${Math.floor((s % 3600) / 60)}m`;
}

/** Battle perks granted by the village. */
export interface BattlePerks {
  towerDamageMult: number; // Defense Workshop: +5% per level
  bonusCoins: number; // Grove Hall: +40 starting coins per level above 1
  rangerMult: number; // Ranger Lodge: Grove Call Rangers +25% hp/damage per level
  spellCdMult: number; // Moonpetal Shrine: spell cooldowns -6% per level
  heroHpMult: number; // Honeycomb Apiary: hero max health +10% per level
}

export function battlePerks(v: VillageState | null): BattlePerks {
  if (!v) return { towerDamageMult: 1, bonusCoins: 0, rangerMult: 1, spellCdMult: 1, heroHpMult: 1 };
  const lvl = (type: BuildingId) => Math.max(0, ...v.buildings.filter((b) => b.type === type).map((b) => b.level));
  return {
    towerDamageMult: 1 + 0.05 * lvl('workshop'),
    bonusCoins: 40 * Math.max(0, lvl('townhall') - 1),
    rangerMult: 1 + 0.25 * lvl('barracks'),
    spellCdMult: 1 - SHRINE_CD_PER_LEVEL * lvl('shrine'),
    heroHpMult: 1 + APIARY_HP_PER_LEVEL * lvl('apiary'),
  };
}

/** Glowsap cost to train a hero from `rank` to `rank + 1` (null at max). Rank r = starts battles at level r + 1. */
export const HERO_TRAIN_COSTS = [300, 800, 1600, 3000, 5000];
export function heroTrainCost(rank: number): number | null {
  return HERO_TRAIN_COSTS[rank] ?? null;
}

export function trainHero(v: VillageState, ranks: Record<string, number>, heroId: string): { ok: boolean; reason?: string } {
  const rank = ranks[heroId] ?? 0;
  const cost = heroTrainCost(rank);
  if (cost === null) return { ok: false, reason: 'Fully trained' };
  if (v.glowsap < cost) return { ok: false, reason: `Needs ${cost} glowsap` };
  v.glowsap -= cost;
  ranks[heroId] = rank + 1;
  return { ok: true };
}


/** Army housing: 10 space per Ranger Lodge level (0 without a lodge). */
export function armyCapacity(v: VillageState): number {
  const lodge = Math.max(0, ...v.buildings.filter((b) => b.type === 'barracks').map((b) => b.level));
  return lodge * 10;
}

export function lodgeLevel(v: VillageState): number {
  return Math.max(0, ...v.buildings.filter((b) => b.type === 'barracks').map((b) => b.level));
}

export function armySpace(army: Record<string, number>): number {
  return Object.entries(army).reduce((n, [id, c]) => n + (TROOPS[id]?.space ?? 0) * c, 0);
}

export interface QueuedTroop {
  id: string;
  endsAt: number; // ms timestamp when this troop is ready
}

/** Space used by ready troops plus troops still in training. */
export function totalArmySpace(army: Record<string, number>, queue: QueuedTroop[]): number {
  return armySpace(army) + queue.reduce((n, q) => n + (TROOPS[q.id]?.space ?? 0), 0);
}

/**
 * Queue one troop at the Ranger Lodge. Glowsap is paid now; troops train one after another.
 * `queue` is mutated (a troop is appended).
 */
export function trainTroop(
  v: VillageState,
  army: Record<string, number>,
  id: string,
  queue: QueuedTroop[] = [],
  now = Date.now(),
): { ok: boolean; reason?: string } {
  const def = TROOPS[id];
  if (!def) return { ok: false, reason: 'Unknown troop' };
  if (lodgeLevel(v) < def.lodge) return { ok: false, reason: `Needs Ranger Lodge level ${def.lodge}` };
  if (totalArmySpace(army, queue) + def.space > armyCapacity(v)) return { ok: false, reason: 'The Ranger Lodge is full' };
  if (v.glowsap < def.cost) return { ok: false, reason: `Needs ${def.cost} glowsap` };
  v.glowsap -= def.cost;
  const start = Math.max(now, queue.length ? queue[queue.length - 1].endsAt : now);
  queue.push({ id, endsAt: start + def.trainTime * 1000 });
  return { ok: true };
}

/** Move finished troops from the queue into the army. Returns how many finished. */
export function tickTraining(army: Record<string, number>, queue: QueuedTroop[], now = Date.now()): number {
  let done = 0;
  while (queue.length && queue[0].endsAt <= now) {
    const q = queue.shift()!;
    army[q.id] = (army[q.id] ?? 0) + 1;
    done++;
  }
  return done;
}
