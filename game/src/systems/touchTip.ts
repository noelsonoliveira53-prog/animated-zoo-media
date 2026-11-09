import type { SaveData } from './save';

/** The touch gestures this game uses, shown once on a player's first battle on a touch screen. */
export const TOUCH_TIPS: { icon: 'hold' | 'drag' | 'hero'; title: string; text: string }[] = [
  { icon: 'hold', title: 'Hold to preview', text: 'Press and hold the hero skill to see who it would hit.' },
  { icon: 'drag', title: 'Drag to aim', text: 'Pick a spell, drag on the map, lift to cast. Lift on the spell bar to cancel.' },
  { icon: 'hero', title: 'Drag the hero', text: 'Drag from your hero to send them anywhere. Rally flags drag the same way.' },
];

/** Show the tip on a touch device until the player has seen it once (daily and endless battles included). */
export function shouldShowTouchTip(save: Pick<SaveData, 'settings'>, isTouch: boolean): boolean {
  return isTouch && !save.settings.touchTipSeen;
}
