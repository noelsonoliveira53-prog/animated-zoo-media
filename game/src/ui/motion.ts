import type Phaser from 'phaser';

// "Reduce motion" accessibility setting: no screen shake and no drifting weather overlays.
// The flag lives here so every scene reads the same value; the Settings scene and boot keep it in sync with the save.
export const motion = { reduced: false, lowFx: false }; // lowFx: the Effects: Low setting (lighter tower effects for weak devices)

/** Screen shake that respects the Reduce motion setting. */
export function shake(scene: Phaser.Scene, duration: number, intensity: number): void {
  if (motion.reduced) return;
  scene.cameras.main.shake(duration, intensity);
}
