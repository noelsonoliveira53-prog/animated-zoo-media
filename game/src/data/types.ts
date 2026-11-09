// Shared typed config for all game data. Logic reads these; it never hard-codes stats.

export type DamageType = 'physical' | 'magic' | 'true';
export type TargetMode = 'first' | 'last' | 'strongest' | 'closest';

export interface Vec2 {
  x: number;
  y: number;
}

export interface EnemyDef {
  id: string;
  name: string;
  blurb: string;
  hp: number;
  speed: number; // pixels / second
  armor: number; // 0..0.9 reduction of physical damage
  magicResist: number; // 0..0.9 reduction of magic damage
  bounty: number; // coins on kill
  livesCost: number; // lives lost when it reaches the gate
  flying?: boolean;
  attack: number; // melee damage per hit against blocking soldiers
  attackRate: number; // melee hits / second
  radius: number; // render + hit size
  color: number; // primary body color
  shield?: number; // damage pool absorbed before hp
  heal?: { amount: number; radius: number; interval: number }; // heals nearby allies
  splitInto?: { enemy: string; count: number }; // spawns children on death
  phases?: BossPhase[]; // triggered once each as hp drops
  chill?: { radius: number; interval: number; duration: number }; // periodically freezes nearby towers
  burrow?: { interval: number; duration: number; speedMult: number }; // dives underground on a cycle
  spawner?: { enemy: string; count: number; interval: number; limit: number }; // releases minions while alive (limit = max total)
  veil?: number; // stealth: towers can only target it within this many px (splash, spells, soldiers still hit)
  enrage?: { below: number; speedMult: number }; // speeds up once hp drops under this fraction
  glare?: { radius: number; duration: number }; // on death, dazzles (freezes) nearby shooting towers
  blink?: { interval: number; distance: number }; // jumps ahead along the road on a timer (breaks free of blockers)
  splashResist?: number; // 0..1 less damage from splash (area) tower shots
  shieldAura?: { amount: number; radius: number; interval: number }; // periodically shields nearby allies
  brittle?: number; // armor lost per hit taken (down to 0)
  swoop?: { interval: number; duration: number }; // flyer that lands for `duration` s every `interval` s
  sporeBurst?: { radius: number; speedMult: number; duration: number }; // on death, hastens nearby allies
  gust?: { interval: number; radius: number; distance: number }; // flyer: shoves nearby free walkers ahead on a timer
  shift?: { interval: number; armor: number; magicResist: number }; // swaps to this armor/MR (and back) every interval s
  revive?: { interval: number; radius: number; window: number; hpFrac: number }; // raises a fallen ally (died within `window` s, in radius)
  thorns?: number; // melee attackers (soldiers, heroes) take this fraction of the damage they deal back
  jam?: { radius: number; slow: number }; // towers within radius fire this fraction slower while it lives
  charge?: { speedMult: number; duration: number; cooldown: number }; // bolts forward for `duration` s when hit
  harden?: { perHit: number; max: number }; // armor grows with every hit taken (up to max)
  dim?: { radius: number; cut: number }; // shooting towers within radius lose this fraction of their range
  echo?: { hpFrac: number }; // on its first death it re-forms once at this fraction of health
  shock?: { interval: number; radius: number; duration: number }; // stuns nearby soldiers and the hero on a timer
  fortify?: { radius: number; bonus: number }; // nearby allies gain this much armor while it lives
  feed?: { radius: number; heal: number; growth: number; maxStacks: number }; // feeds when a nearby ally dies: heals heal×maxHp and grows maxHp by growth (stacks)
  grow?: { into: string; after: number };
  bolt?: { interval: number; range: number; duration: number }; // calls lightning on the nearest tower in range, stunning it
  ground?: { radius: number; share: number }; // takes `share` of the damage aimed at allies within radius onto itself
  mirage?: { into: string; count: number }; // when first hit, leaves `count` decoys (`into`) behind it
  crust?: { max: number; perSec: number }; // armor builds by perSec while unhit (up to +max); any hit cracks it back to base
  molt?: { at: number; armor: number; speedMult: number }; // below `at` health it sheds its shell: armor drops, speed rises
  cleanse?: { radius: number; interval: number }; // washes slows off itself and allies in radius every interval
  ink?: { radius: number; duration: number; cooldown: number }; // when hit, squirts an ink cloud: towers can't target enemies inside it
  ranged?: { range: number; damage: number; interval: number }; // shoots the nearest soldier or hero in range while it walks
  anchor?: { interval: number; duration: number; armor: number }; // drops anchor on a cycle: stops dead and gains armor while anchored
  keg?: { radius: number; damage: number }; // explodes on death, hurting soldiers and the hero within radius
  drum?: { interval: number; radius: number; speedMult: number; duration: number }; // beats a war-drum on a timer: allies in radius (and itself) speed up briefly
  adapt?: { step: number; max: number }; // each hit shifts its hide toward that damage type: +step armor (physical) or MR (magic), up to +max, while the other eases back to base
  phase?: { interval: number; duration: number }; // fades to mist on a cycle: takes no damage while phased (towers still waste shots on it)
  dodge?: number; // chance (0..1) to sidestep a single-target tower shot (splash, chains and spells always land)
  ward?: { radius: number; cut: number }; // allies within radius (not itself) take this fraction less damage of every type
  snatch?: { radius: number; cooldown: number }; // flyer: carries off the nearest soldier within radius (it must respawn), on a cooldown
  wax?: { armor: number; melt: number }; // a waxy coat adds `armor` until it has soaked melt × maxHp of magic damage, then melts off for good
  parry?: { charges: number; regen: number }; // its comb-shield turns aside a whole single-target tower shot per charge (splash, chains' jumps and spells still land); regains one charge every regen s
  glaze?: { duration: number; slow: number }; // its melee hits coat a soldier in honey: that soldier attacks at `slow`× speed for `duration` s
  venom?: { dps: number; duration: number }; // its melee bites poison soldiers: they lose dps health a second for duration s (refreshed by each bite)
  ambush?: number; // burrows in and pops up at this fraction of the road instead of at the entrance
  stall?: number; // while any lives, spell and hero-skill cooldowns tick at this fraction of normal speed (the strongest counts)
  link?: { radius: number }; // shares every hit equally with each linked ally (same trait) within radius
  wool?: number; // thick fleece: each hit loses this much damage (never more than 3/4 of it)
  drench?: { radius: number; cut: number }; // soaks itself and allies within radius: player spells (Starfall, Thornsnare, ...) deal cut less to them
  bubble?: { radius: number; interval: number; count: number }; // every interval s, wraps up to count nearby allies in a bubble that blocks the next hit entirely
  surge?: { interval: number; distance: number; radius: number }; // every interval s, it and its unheld allies within radius are swept distance px down the road
  curl?: { duration: number; cooldown: number; bonus: number; slow: number }; // when hit (off cooldown), curls up: +bonus armor and magic resist, moving at slow× speed, for duration s
  shepherd?: { radius: number }; // herds stragglers: allies within radius walk at least as fast as it does
  tithe?: number; // while it lives, every kill pays this fraction less bounty (the strongest one counts, they don't stack)
  trample?: { damage: number }; // soldiers and the hero can't hold it: it shoves straight through, hurting each one once as it passes
  alarm?: { radius: number; speedMult: number; duration: number }; // the first time it's hit, it whistles: allies within radius (and itself) run at speedMult for duration s
  momentum?: { perSec: number; max: number }; // rolls faster the longer it goes unhit: +perSec speed per second since its last hit, up to +max (any hit resets it)
  blossom?: { radius: number; heal: number }; // on death, heals allies within radius by heal × their maxHp
  dive?: { at: number; duration: number; heal: number }; // once, when a hit drops it below `at` health, it dives into the mud: untargetable for `duration` s (still moving), and heals `heal` × maxHp
  lure?: boolean; // its glowing lure draws every single-target tower in range to shoot it first, whatever the targeting mode
  hex?: { interval: number; range: number; cut: number; duration: number }; // curses the nearest shooting tower in range: it deals `cut` less damage for `duration` s
  rile?: { perSlow: number; max: number }; // every slow it suffers (at most twice a second) adds perSlow to its speed for good, up to +max
  grief?: { radius: number; armor: number }; // on death, allies within radius gain this much armor for good (capped at 85%)
  lifesteal?: number; // heals this fraction of the melee damage it deals to soldiers and heroes
  pilfer?: number; // coins stolen from the player if it reaches the exit
  herd?: { radius: number; perAlly: number; max: number }; // runs faster for each other herd-mate nearby (bonus capped at max) // a planted seed: becomes `into` after `after` seconds unless destroyed
  windborne?: boolean; // shrugs off every slow (frost, snares, quakes, hero skills)
  regen?: { perSec: number; delay: number }; // heals perSec × maxHp each second once it hasn't been hit for `delay` s
  boss?: boolean;
}

export interface BossPhase {
  at: number; // hp fraction that triggers it (e.g. 0.66)
  summon?: { enemy: string; count: number };
  speedMult?: number;
  shield?: number; // grants a fresh shield
  message: string;
}

export interface TowerTier {
  cost: number; // cost to build (tier 0) or upgrade to this tier
  damage: number;
  range: number; // pixels
  fireRate: number; // shots / second
  projectileSpeed: number; // pixels / second
  splash?: number; // splash radius in pixels
  slow?: { factor: number; duration: number }; // speed multiplier + seconds
  lob?: boolean; // arcing shot aimed at a predicted spot instead of homing
  multishot?: number; // fires at this many different targets per volley
  chain?: { count: number; falloff: number; range: number }; // hit jumps to nearby enemies
  armorPierce?: number; // 0..1 share of the target's armor ignored
  soldiers?: SoldierStats; // barracks-style tower: spawns blockers instead of shooting
}

export interface SoldierStats {
  count: number;
  hp: number;
  damage: number; // physical melee damage
  attackRate: number; // hits / second
  respawn: number; // seconds after death
  armor: number;
  regen: number; // hp / second while not fighting
}

export interface TowerSpec {
  id: string;
  name: string;
  text: string;
  color: number;
  stats: TowerTier; // full stat block once specialized (its cost is the specialization price)
}

export interface TowerDef {
  id: string;
  name: string;
  blurb: string;
  damageType: DamageType;
  hitsAir: boolean;
  color: number;
  tiers: TowerTier[];
  specs: [TowerSpec, TowerSpec]; // two branches offered at the top tier
}

export interface SpawnGroup {
  enemy: string;
  count: number;
  interval: number; // seconds between spawns
  delay?: number; // seconds after wave start before first spawn
  path?: number; // path index, default 0
}

export interface WaveDef {
  groups: SpawnGroup[];
}

export interface LevelDef {
  id: string;
  name: string;
  blurb: string;
  mapPos: Vec2; // node position on the world map
  rewardCoins?: number; // village coins for a first clear (used once the village exists)
  startCoins: number;
  lives: number;
  paths: Vec2[][];
  slots: Vec2[];
  waves: WaveDef[];
  theme: { grass: number; grassDark: number; road: number; roadEdge: number; trees?: number[]; snow?: boolean; lava?: boolean; shrooms?: boolean; crystals?: boolean; gale?: boolean; ruins?: boolean; gears?: boolean; abyss?: boolean; orchard?: boolean; storm?: boolean; dunes?: boolean; reef?: boolean; flotilla?: boolean; amber?: boolean; mist?: boolean; canopy?: boolean; comb?: boolean; bog?: boolean; thistle?: boolean; wold?: boolean; canyon?: boolean; brook?: boolean; heath?: boolean; shoal?: boolean };
  finale?: boolean;
  endless?: { hpRamp: number; heroRegen?: number; attackRamp?: number }; // attackRamp: +x enemy melee damage per wave // heroRegen: multiplier on hero regeneration in endless runs // endless mode: health grows by hpRamp per wave instead of the campaign ramp // winning this level plays the ending (the story's last battle)
  ponds?: { x: number; y: number; w: number; h: number }[]; // decorative water
  hpMult?: number; // difficulty ramp: multiplies every enemy's health on this level
  heroSpawn?: Vec2; // where the hero starts/respawns (default: near the first road's exit)
}

export type HeroPassive =
  | { kind: 'toughness'; armor: number; regen: number; text: string }
  | { kind: 'crit'; chance: number; mult: number; text: string }
  | { kind: 'towerHaste'; radius: number; bonus: number; text: string }
  | { kind: 'bounty'; radius: number; bonus: number; text: string }
  | { kind: 'mend'; radius: number; regen: number; text: string }
  | { kind: 'drowse'; radius: number; slow: number; text: string };

export interface HeroActive {
  name: string;
  text: string;
  cooldown: number; // seconds
  kind: 'quake' | 'volley' | 'ring' | 'rally';
  heal?: number; // rally: health restored to every soldier and the hero in radius (scales with hero level)
  damage: number;
  damageType: DamageType;
  radius: number;
  maxTargets?: number;
  fxColor?: number; // tint for the skill's visual effect (defaults to the hero's colour / foxfire gold)
  slow?: { factor: number; duration: number };
}

export interface HeroDef {
  id: string;
  name: string;
  title: string;
  blurb: string;
  color: number;
  hp: number;
  speed: number;
  armor: number;
  regen: number; // hp/s when not fighting
  melee: boolean; // melee heroes block an enemy like soldiers do
  bulwark?: { level: number; holds: number }[]; // melee heroes: how many enemies they can hold at once, by hero level
  toss?: { name: string; damage: number; range: number; interval: number }; // ranged throw at flyers (melee heroes' answer to air)
  attack: { damage: number; type: DamageType; range: number; rate: number; hitsAir: boolean; projectileSpeed: number };
  respawn: number;
  passive: HeroPassive;
  active: HeroActive;
}
