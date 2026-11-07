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

export interface TowerDef {
  id: string;
  name: string;
  blurb: string;
  damageType: DamageType;
  hitsAir: boolean;
  color: number;
  tiers: TowerTier[];
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
  startCoins: number;
  lives: number;
  paths: Vec2[][];
  slots: Vec2[];
  waves: WaveDef[];
  theme: { grass: number; grassDark: number; road: number; roadEdge: number };
}
