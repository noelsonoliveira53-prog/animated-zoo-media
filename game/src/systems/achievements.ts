import { ACHIEVEMENTS, type AchievementDef } from '../data/achievements';
import { ensureVillage, type SaveData } from './save';
import { addResources } from './village';

/**
 * Unlock every achievement whose goal is met and pay its reward into the village.
 * Returns the updated save and the newly unlocked achievements (for toasts).
 */
export function checkAchievements(data: SaveData): { save: SaveData; unlocked: AchievementDef[] } {
  const save: SaveData = { ...data, achievements: [...data.achievements] };
  const unlocked: AchievementDef[] = [];
  for (const a of ACHIEVEMENTS) {
    if (save.achievements.includes(a.id)) continue;
    if (a.progress(save) >= a.goal) {
      save.achievements.push(a.id);
      unlocked.push(a);
      const v = ensureVillage(save);
      addResources(v, a.reward.coins ?? 0, a.reward.glowsap ?? 0);
    }
  }
  return { save, unlocked };
}
