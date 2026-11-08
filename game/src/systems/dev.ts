import { setAllLevelsOpen } from '../data/levels';
import { loadSave, writeSave } from './save';

// Dev mode: a testing switch on the main menu. While it is on, every level is open, battles have
// endless coins, lives and instant spells, the village has endless resources and instant builds,
// and raids get a full army. It never touches real progress (stars, achievements), so switching
// it off puts everything back as it was.

export const DEV_COINS = 999999;
export const DEV_LIVES = 9999;
export const DEV_TROOPS = 30;

let on = false;
try {
  on = !!loadSave().settings.dev;
} catch {
  on = false;
}
setAllLevelsOpen(on);

export function devOn(): boolean {
  return on;
}

export function setDev(value: boolean): void {
  on = value;
  setAllLevelsOpen(value);
  const s = loadSave();
  s.settings = { ...s.settings, dev: value };
  writeSave(s);
}
