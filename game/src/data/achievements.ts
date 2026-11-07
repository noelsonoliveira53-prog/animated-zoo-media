// Achievements: each has a progress function over the save and a small village reward.
import type { SaveData } from '../systems/save';
import { LEVELS, totalStars } from './levels';
import { ENEMIES } from './enemies';

export interface AchievementDef {
  id: string;
  name: string;
  text: string;
  goal: number;
  progress: (s: SaveData) => number;
  reward: { coins?: number; glowsap?: number };
}

const stat = (s: SaveData, k: string) => s.stats[k] ?? 0;
const hall = (s: SaveData) => Math.max(0, ...(s.village?.buildings ?? []).filter((b) => b.type === 'townhall').map((b) => b.level));

export const ACHIEVEMENTS: AchievementDef[] = [
  { id: 'first_win', name: 'First Light', text: 'Win your first battle.', goal: 1, progress: (s) => stat(s, 'wins'), reward: { coins: 150 } },
  { id: 'perfect', name: 'Not One Step Further', text: 'Win a battle without losing a single life.', goal: 1, progress: (s) => stat(s, 'perfectWins'), reward: { glowsap: 250 } },
  { id: 'stars15', name: 'Starcatcher', text: 'Earn 15 stars in the campaign.', goal: 15, progress: (s) => totalStars(s.stars), reward: { coins: 400 } },
  { id: 'stars_all', name: 'Constellation', text: `Earn all ${LEVELS.length * 3} campaign stars.`, goal: LEVELS.length * 3, progress: (s) => totalStars(s.stars), reward: { coins: 2500, glowsap: 2500 } },
  { id: 'boss_murkmaw', name: 'Toad Toppler', text: 'Defeat Old Murkmaw.', goal: 1, progress: (s) => stat(s, 'boss_murkmaw'), reward: { glowsap: 400 } },
  { id: 'boss_grimtusk', name: 'Frost Breaker', text: 'Defeat Grimtusk the Frost Boar.', goal: 1, progress: (s) => stat(s, 'boss_grimtusk'), reward: { glowsap: 600 } },
  { id: 'boss_vulkhar', name: 'Wyrmsbane', text: 'Defeat Vulkhar the Ash Wyrm.', goal: 1, progress: (s) => stat(s, 'boss_vulkhar'), reward: { glowsap: 900 } },
  { id: 'boss_morrowcap', name: 'Weald Warden', text: 'Defeat Matriarch Morrowcap in the Duskcap Weald.', goal: 1, progress: (s) => stat(s, 'boss_morrowcap'), reward: { coins: 1200, glowsap: 1200 } },
  { id: 'weald_stars', name: 'Mistwalker', text: 'Earn 3 stars on every Duskcap Weald level.', goal: 15, progress: (s) => ['l16', 'l17', 'l18', 'l19', 'l20'].reduce((n, id) => n + (s.stars[id] ?? 0), 0), reward: { coins: 2000, glowsap: 2000 } },
  { id: 'endless25', name: 'Unending Vigil', text: 'Hold 25 waves in Endless mode on any map.', goal: 25, progress: (s) => Math.max(0, ...Object.values(s.endlessBest ?? {})), reward: { coins: 1000, glowsap: 1000 } },
  { id: 'boss_saltjaw', name: 'Tide Turner', text: 'Defeat Saltjaw the Tidecrab in the Saltmarrow Shoals.', goal: 1, progress: (s) => stat(s, 'boss_saltjaw'), reward: { coins: 1500, glowsap: 1500 } },
  { id: 'boss_kaleidrax', name: 'Shatterer', text: 'Defeat Kaleidrax, the Shattered Colossus.', goal: 1, progress: (s) => stat(s, 'boss_kaleidrax'), reward: { coins: 1800, glowsap: 1800 } },
  { id: 'boss_zephyrax', name: 'Stormbreaker', text: 'Defeat Zephyrax, the Gale Roc.', goal: 1, progress: (s) => stat(s, 'boss_zephyrax'), reward: { coins: 2000, glowsap: 2000 } },
  { id: 'gale_stars', name: 'Cloudwalker', text: 'Earn 3 stars on every Galecrest Aeries level.', goal: 15, progress: (s) => ['l31', 'l32', 'l33', 'l34', 'l35'].reduce((n, id) => n + (s.stars[id] ?? 0), 0), reward: { coins: 2500, glowsap: 2500 } },
  { id: 'boss_ulmaroth', name: 'Idolbreaker', text: 'Defeat Ulmaroth, the Overgrown Idol.', goal: 1, progress: (s) => stat(s, 'boss_ulmaroth'), reward: { coins: 2200, glowsap: 2200 } },
  { id: 'ruins_stars', name: 'Pathfinder', text: 'Earn 3 stars on every Verdant Ruins level.', goal: 15, progress: (s) => ['l36', 'l37', 'l38', 'l39', 'l40'].reduce((n, id) => n + (s.stars[id] ?? 0), 0), reward: { coins: 2800, glowsap: 2800 } },
  { id: 'boss_grindmaw', name: 'Engine Breaker', text: 'Defeat Grindmaw, the Engine Titan.', goal: 1, progress: (s) => stat(s, 'boss_grindmaw'), reward: { coins: 2400, glowsap: 2400 } },
  { id: 'brass_stars', name: 'Master Tinker', text: 'Earn 3 stars on every Brasswork Hollows level.', goal: 15, progress: (s) => ['l41', 'l42', 'l43', 'l44', 'l45'].reduce((n, id) => n + (s.stars[id] ?? 0), 0), reward: { coins: 3000, glowsap: 3000 } },
  { id: 'boss_velumbra', name: 'Lightbringer', text: 'Defeat Velumbra, the Dark Below.', goal: 1, progress: (s) => stat(s, 'boss_velumbra'), reward: { coins: 2600, glowsap: 2600 } },
  { id: 'abyss_stars', name: 'Starwalker', text: 'Earn 3 stars on every Starwell Abyss level.', goal: 15, progress: (s) => ['l46', 'l47', 'l48', 'l49', 'l50'].reduce((n, id) => n + (s.stars[id] ?? 0), 0), reward: { coins: 3200, glowsap: 3200 } },
  { id: 'boss_mawbloom', name: 'Heartwood', text: 'Defeat Mawbloom, the Rot Heart.', goal: 1, progress: (s) => stat(s, 'boss_mawbloom'), reward: { coins: 2800, glowsap: 2800 } },
  { id: 'orchard_stars', name: 'Harvest Keeper', text: 'Earn 3 stars on every Rotbloom Orchard level.', goal: 15, progress: (s) => ['l51', 'l52', 'l53', 'l54', 'l55'].reduce((n, id) => n + (s.stars[id] ?? 0), 0), reward: { coins: 3400, glowsap: 3400 } },
  { id: 'campaign', name: 'Keeper of the Grove', text: 'Defeat Vulkhar and finish the story.', goal: 1, progress: (s) => ((s.stars[(LEVELS.find((l) => l.finale) ?? LEVELS[LEVELS.length - 1]).id] ?? 0) > 0 ? 1 : 0), reward: { coins: 1500 } },
  { id: 'kills500', name: 'Mud on the Boots', text: 'Defeat 500 Murkhorde critters.', goal: 500, progress: (s) => stat(s, 'kills'), reward: { coins: 300 } },
  { id: 'kills5000', name: 'Horde Breaker', text: 'Defeat 5,000 Murkhorde critters.', goal: 5000, progress: (s) => stat(s, 'kills'), reward: { coins: 1500, glowsap: 1000 } },
  { id: 'specialist', name: 'Specialist', text: 'Buy 10 tower specializations.', goal: 10, progress: (s) => stat(s, 'specs'), reward: { glowsap: 400 } },
  { id: 'hero_max', name: 'Living Legend', text: 'Reach hero level 6 during a battle.', goal: 6, progress: (s) => stat(s, 'heroMaxLevel'), reward: { glowsap: 500 } },
  { id: 'builder', name: 'Busy Beavers', text: 'Construct 10 village buildings.', goal: 10, progress: (s) => stat(s, 'buildingsBuilt'), reward: { coins: 400 } },
  { id: 'hall3', name: 'The Great Oak', text: 'Upgrade the Grove Hall to level 3.', goal: 3, progress: (s) => hall(s), reward: { coins: 800, glowsap: 800 } },
  { id: 'raider', name: 'Turnabout', text: 'Win a raid (at least one star).', goal: 1, progress: (s) => stat(s, 'raidsWon'), reward: { glowsap: 300 } },
  { id: 'razed', name: 'Razed to the Mud', text: 'Earn 3 stars on a Murkhorde Stronghold.', goal: 1, progress: (s) => stat(s, 'stronghold3'), reward: { coins: 1500, glowsap: 1500 } },
  {
    id: 'guide',
    name: 'Naturalist',
    text: 'Discover every enemy in the Field Guide.',
    goal: Object.keys(ENEMIES).length,
    progress: (s) => s.seenEnemies.filter((id) => ENEMIES[id]).length,
    reward: { glowsap: 600 },
  },
];
